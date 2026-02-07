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
