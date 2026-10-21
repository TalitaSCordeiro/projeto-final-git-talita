# Projeto Final Git - Engenharia de Dados (CVU)

**Autor(a):** Talita Santos Cordeiro ([@TalitaSCordeiro](https://github.com/TalitaSCordeiro))
**Projeto:** Onboarding / Git Roadmap - LICA

---

## 📌 Descrição
Este repositório contém o projeto final do treinamento de Git do Laboratório de Inteligência Computacional Aplicada (LICA). O projeto consiste em um pipeline de Engenharia de Dados focado na extração, transformação e carregamento (ETL) de dados sobre o Custo Variável Unitário (CVU) de usinas térmicas.

Os dados são extraídos da API de dados abertos do Operador Nacional do Sistema Elétrico (ONS), processados para remoção de duplicatas e ordenação, e por fim consolidados e particionados por subsistema.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3
- **Bibliotecas:** `pandas` (manipulação de dados), `curl_cffi` (requisições HTTP)
- **Versionamento:** Git, GitHub e GitLab

## 📂 Estrutura do Repositório
- `main.py`: Script principal de orquestração do pipeline (Extract, Transform, Validate, Load e Split).
- `requirements.txt`: Lista de dependências e bibliotecas Python necessárias.
- `data/`: Diretório que armazena os dados brutos (`source_raw/`) e os dados limpos e particionados (`processed/`).

## 💻 Como Rodar o Projeto

1. **Clone o repositório e acesse a pasta:**
   ```bash
   git clone https://github.com/TalitaSCordeiro/projeto-final-git-talita.git
   
   # Acesse a pasta
   cd projeto-final-git-talita

   # Instale dependências
   pip install -r requirements.txt

   # Execute o projeto
   python main.py


## 👥 Colaboradores

| Nome                   | GitHub                                                 |
| ---------------------- | ------------------------------------------------------ |
| Talita Santos Cordeiro | [@TalitaSCordeiro](https://github.com/TalitaSCordeiro) |
