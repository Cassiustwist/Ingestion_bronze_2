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
