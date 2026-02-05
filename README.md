Abaixo está um README pronto (você cola no seu novo repositório). Ele cria um projeto RAW → BRONZE → Postgres com um CSV diferente (orders). Ele também já inclui .env.example e o .gitignore correto (pra você NÃO subir senha nem dados).

README.md (copie e cole)
# Projeto Bronze — Ingestão CSV (Orders) — Guia Prático

Objetivo: repetir do zero o fluxo completo:

1) clonar projeto
2) criar/ativar venv
3) instalar dependências
4) configurar .env (sem subir senha no Git)
5) colocar CSV em data/raw
6) gerar bronze CSV em data/bronze
7) carregar bronze no PostgreSQL (schema bronze)

---

## 0) Requisitos

- Windows + PowerShell
- Python 3.11 instalado
- PostgreSQL rodando local (pgAdmin ok)

---

## 1) Clone do repositório

```powershell
git clone <COLE_AQUI_O_LINK_DO_SEU_REPO>
cd <NOME_DA_PASTA_DO_REPO>
code .

2) Criar e ativar a venv (Python 3.11)

Se você tiver mais de uma versão, garanta Python 3.11 assim:

py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version


Resultado esperado:

Python 3.11.x

Terminal com (.venv)

3) Instalar dependências
python -m pip install --upgrade pip
pip install -r requirements.txt

4) Configurar variáveis de ambiente
4.1) Crie um arquivo .env na raiz (NÃO subir no Git)

Copie o arquivo .env.example e renomeie para .env.

Preencha com seus dados locais do Postgres.

5) Criar a estrutura de dados

Crie as pastas:

data/
  raw/
  bronze/

6) Criar o CSV de entrada (RAW)

Crie o arquivo:

data/raw/orders.csv

Conteúdo:

order_id,customer_id,order_date,total_amount,status
1001,10,2026-02-01,250.50,PAID
1002,11,2026-02-01,99.90,PENDING
1003,10,2026-02-02,15.00,CANCELLED

7) Rodar a ingestão Bronze (RAW → BRONZE CSV)
python ingest_bronze_orders.py


Resultado esperado:

arquivo criado em data/bronze/bronze_orders.csv

mensagem de sucesso no terminal

8) Carregar Bronze no Postgres (BRONZE CSV → BANCO)
python load_bronze_orders_to_db.py


Resultado esperado:

schema bronze criado (se não existir)

tabela bronze.orders criada/atualizada

9) Conferir no pgAdmin

No pgAdmin, rode:

SELECT * FROM bronze.orders;


Você deve ver 3 linhas.

10) Versionar código (Git)

⚠️ NUNCA suba .env ou dados de data/.

git status
git add .
git commit -m "feat: pipeline bronze orders (raw->bronze->db)"
git push

Estrutura do projeto (esperada)
.
├─ data/
│  ├─ raw/
│  │  └─ orders.csv
│  └─ bronze/
│     └─ bronze_orders.csv
├─ .env               (NÃO versionar)
├─ .env.example
├─ .gitignore
├─ ingest_bronze_orders.py
├─ load_bronze_orders_to_db.py
├─ read_csv_test.py
├─ requirements.txt
└─ README.md


---

## Arquivos que você vai criar no repo (cole exatamente)

### `.gitignore`
```gitignore
.venv/
__pycache__/
.env
data/
*.log
.ipynb_checkpoints/

requirements.txt
pandas
python-dotenv
SQLAlchemy
psycopg2-binary

.env.example
DATA_DIR=data

DB_HOST=localhost
DB_PORT=5432
DB_NAME=empregadados_local
DB_USER=postgres
DB_PASS=SUA_SENHA_AQUI

DB_SCHEMA=bronze
DB_TABLE=orders
RAW_FILE=orders.csv
BRONZE_FILE=bronze_orders.csv

read_csv_test.py
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = os.getenv("DATA_DIR", "data")
raw_file = os.getenv("RAW_FILE", "orders.csv")

csv_path = os.path.join(DATA_DIR, "raw", raw_file)

print("Lendo RAW:", csv_path)
df = pd.read_csv(csv_path)
print(df.head())
print("Linhas:", len(df))
print("Colunas:", list(df.columns))

ingest_bronze_orders.py
import os
import pandas as pd
from dotenv import load_dotenv

def main():
    load_dotenv()

    data_dir = os.getenv("DATA_DIR", "data")
    raw_file = os.getenv("RAW_FILE", "orders.csv")
    bronze_file = os.getenv("BRONZE_FILE", "bronze_orders.csv")

    raw_path = os.path.join(data_dir, "raw", raw_file)
    bronze_path = os.path.join(data_dir, "bronze", bronze_file)

    os.makedirs(os.path.dirname(bronze_path), exist_ok=True)

    df = pd.read_csv(raw_path)

    # Bronze: padronização mínima (colunas minúsculas)
    df.columns = [c.strip().lower() for c in df.columns]

    df.to_csv(bronze_path, index=False)

    print("✅ Bronze gerado com sucesso")
    print("🟫 Bronze salvo em:", bronze_path)
    print("📊 Linhas:", len(df))
    print("📋 Colunas:", list(df.columns))

if __name__ == "__main__":
    main()

load_bronze_orders_to_db.py
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

def main():
    load_dotenv()

    data_dir = os.getenv("DATA_DIR", "data")
    bronze_file = os.getenv("BRONZE_FILE", "bronze_orders.csv")

    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")

    schema = os.getenv("DB_SCHEMA", "bronze")
    table = os.getenv("DB_TABLE", "orders")

    bronze_path = os.path.join(data_dir, "bronze", bronze_file)
    df = pd.read_csv(bronze_path)

    url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(url, pool_pre_ping=True)

    with engine.begin() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema};"))

    # replace para estudo (em produção geralmente é append/merge)
    df.to_sql(table, engine, schema=schema, if_exists="replace", index=False)

    print("✅ Carregado com sucesso no Postgres")
    print(f"📌 Tabela: {schema}.{table}")
    print("📊 Linhas:", len(df))

if __name__ == "__main__":
    main()
