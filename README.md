# WebScrapingAnalytics_Imobiliario
# 📊 Projeto de Análise de Dados Imobiliários e IBGE
Este projeto realiza coleta, processamento e análise de dados do Zap Imóveis (via web scraping) e IBGE (via API), armazenando em um banco PostgreSQL com modelagem em camadas (bronze, silver, gold).

## ⚙️ Pré-requisitos
- Python 3.10+
- Poetry (gerenciador de dependências)
- PostgreSQL 13+
- Microsoft Edge + WebDriver (para scraping)

## 🚀 Configuração Inicial
1. Instale o Poetry
    ```bash
    pip install poetry
    ```
2. Clone o repositório
    ```bash
    git clone https://github.com/Gabriel-albuq/WebScrapingAnalytics_Imobiliario
    cd WebScrapingAnalytics_Imobiliario
    ```
3. Instale as dependências
    ```bash
    poetry install
    ```
4. Ative o ambiente virtual
    ```bash
    poetry shell
    ```

## 🔧 Configuração do Ambiente
### Banco de Dados (PostgreSQL)
Crie um arquivo `.env` na raiz com:

```ini
# PostgreSQL
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

```
### Edge Driver
Manter o arquivo msedgedriver.exe na raiz.

## 🗃️ Estrutura de Pastas
```
├── data/                                    # Dados brutos/processados
│   ├── outputs/
│       ├── bronze/                          # JSON/CSV originais
│       ├── silver/                          # Dados estruturados
│       └── gold/                            # Dados analíticos
│
├── src/
│   ├── analysis/                            # Análise dos dados
│   ├── extract_data_ibge/                   # Scripts de coleta do IBGE
│   ├── extract_webscraping_imobiliario/     # Scripts de coleta do Zap Imoveis
│   ├── layer01_bronze_postgres/             # Processamento da camada Bronze
│   ├── layer02_silver_postgres/             # Transformação de dados (Silver)
│   ├── layer03_gold_postgres/               # Modelagem Analítica (Gold)
│   └── tests/                               # Testes (a implementar)
│
├── msedgedriver.exe                         # WebDriver para Microsoft Edge
├── .env                                     # Variáveis de ambiente
└── pyproject.toml                           # Dependências do projeto
```

## 🛠️ Como Executar