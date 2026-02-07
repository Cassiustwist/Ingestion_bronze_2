import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = os.getenv("DATA_DIR", "data")

raw_path = os.path.join(DATA_DIR, "raw", "orders.csv")
bronze_path = os.path.join(DATA_DIR, "bronze", "bronze_orders.csv")

print(f"Lendo RAW: {raw_path}")
df = pd.read_csv(raw_path)

print("Transformando para Bronze...")
df.columns = [c.strip().lower() for c in df.columns]

print(f"Salvando Bronze: {bronze_path}")
df.to_csv(bronze_path, index=False)

print("✅ Ingestão Bronze concluída!")
