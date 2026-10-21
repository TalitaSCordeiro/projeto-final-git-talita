from curl_cffi import requests
from pathlib import Path
import pandas as pd

url = "https://dados.ons.org.br/api/3/action/package_show?id=cvu-usitermica"
SOURCE_RAW_PATH = Path("data/cvu-usitermica/source_raw")
PROCESSED_PATH = Path("data/cvu-usitermica/processed")
REQUIRED_COLS = {"dat_iniciosemana", "id_subsistema", "nom_usina", "val_cvu"}


def extract() -> list[Path]:
    print("=" * 30)
    print("Iniciando Extract")
    print("=" * 30)

    response = requests.get(url, impersonate="chrome")
    response.raise_for_status()

    resources = response.json()["result"]["resources"]

    print("Iniciando download...")
    paths = []
    for item in resources:
        if item["format"] != "CSV":
            continue

        year = item["name"].split("-")[2]

        if int(year)<2023: #TEMPORÁRIO
            continue

        SOURCE_RAW_PATH.mkdir(parents=True, exist_ok=True)
        file_path = SOURCE_RAW_PATH / f"cvu_usitermica_{year}.csv"
        paths.append(file_path)

        if file_path.exists():#TEMPORÁRIO
            print(f"O arquivo já existe: {file_path}")
            continue

        response = requests.get(item["url"], impersonate="chrome")
        response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(response.content)
            print(f"Salvo em {file_path}")

    print("Extração finalizada")
    return paths


def transform(paths: list[Path]) -> pd.DataFrame:
    print("=" * 30)
    print("Iniciando transformação")
    print("=" * 30)

    dfs = []
    print("Concatenando arquivos baixados...")
    for path in paths:
        df = pd.read_csv(path, sep=";")
        dfs.append(df)

    df = pd.concat(dfs)

    print("Aplicando Transformações...")

    sum = df.duplicated().sum()
    print(f"Eliminando {sum} registros..")
    df = df.drop_duplicates()

    print("Ordenando valores...")
    df = df.sort_values(by="dat_iniciosemana")

    print("Transformações Finalizada")

    return df


def validate(df) -> None:
    print("=" * 30)
    print("Iniciando validação")
    print("=" * 30)

    #Dataframe nulo
    if df.empty:
        raise ValueError("Validação falhou: o dataframe está nulo")

    #Colunas Obrigatórias
    missing_cols = REQUIRED_COLS - set(df.columns)
    if missing_cols:
        raise KeyError(f"Validação falhou: colunas ausentes {missing_cols}")

    #Integridade
    if df["id_subsistema"]. isna().any():
        raise ValueError("Falhou: Existema registros sem subsistema informado")

    print("Validação finalizada.")


def load(df, file_path: Path) -> Path:
    df.to_csv(file_path, index=False)
    print(f"Salvo em {file_path}")
    return file_path

def split_by_subsystem(df: pd.DataFrame) -> dict:
    print("=" * 30)
    print("Iniciando divisão por subsistema")
    print("=" * 30)
    
    coluna_subsistema = 'nom_subsistema' 
    
    if coluna_subsistema not in df.columns:
        colunas_possiveis = [col for col in df.columns if 'subsistema' in col.lower()]
        if not colunas_possiveis:
            raise ValueError(f"Coluna de subsistema não encontrada. Colunas atuais: {df.columns.tolist()}")
        coluna_subsistema = colunas_possiveis[0]

    df_dict = {}
    for subsistema in df[coluna_subsistema].dropna().unique():
        df_dict[subsistema] = df[df[coluna_subsistema] == subsistema].copy()
        
    print("Divisão finalizada.")
    return df_dict

def main() -> None:
    paths = extract()
    df = transform(paths)
    validate(df)
    
    file_path_full = PROCESSED_PATH / "cvu_usitermica_completo.csv"
    load(df, file_path_full)
    
    dfs_separados = split_by_subsystem(df)
    for subsistema, df_sub in dfs_separados.items():
        nome_arquivo = f"cvu_usitermica_{subsistema.lower().replace(' ', '_')}.csv"
        file_path_sub = PROCESSED_PATH / nome_arquivo
        load(df_sub, file_path_sub)

if __name__ == '__main__':
    main()