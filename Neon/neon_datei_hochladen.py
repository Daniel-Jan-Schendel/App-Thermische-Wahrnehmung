import pandas as pd
from sqlalchemy import create_engine
import time

# 🔑 Direkter, verifizierter Link zu deinem neuen Projekt (smart_building)
String1 = "postgresql://neondb_owner:npg_fWR8OHIJyC1Z@ep-summer-art-as4axoig.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require"

# PATH
CSV_PATH =  pd.read_csv("Daten/db_bereinigt_final.csv")

try:
    print("🔌 Verbindung zum PROJEKT und Einlesen der lokalen CSV‑Datei...")
    df = pd.read_csv(CSV_PATH, encoding='latin1')
    
    # Wir ersetzen die Punkte in den Headern durch Unterstriche für PostgreSQL
    df.columns = df.columns.str.replace('.', '_', regex=False)
    
    # Wir modifizieren die Metadaten im Speicher der Geschwindigkeitssensoren, um wissenschaftliche Notation zu vermeiden.
    for col in ['air_speed', 'air_speed_1_1', 'air_speed_0_6', 'air_speed_0_1']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').round(4)

    engine = create_engine(String1)
    print("🚀 Start der massiven Projekteinjektion...")
    start_time = time.time()
    
    # 🧱 1. DIM_BUILDINGS
    print("🧱 Creando y cargando el catálogo de Edificios Únicos...")
    cols_buildings = ['building_id', 'region', 'country', 'city', 'latitude', 'longitude', 'climate', 'building_type', 'cooling_type']
    df_buildings = df[cols_buildings].drop_duplicates(subset=['building_id'])
    df_buildings.to_sql(name='dim_buildings', con=engine, if_exists='replace', index=False)
    
    # 📊 2. FACT_THERMAL_RECORDS 
    print("📊 Creando y cargando la Tabla de Hechos Completa (109,033 filas)...")
    df.to_sql(name='fact_thermal_records', con=engine, if_exists='replace', index=False, chunksize=10000)
    
    end_time = time.time()
    print(f"\n🎉 [Erfolgreiche Bereitstellung im Projekt]")
    print(f"⏱️ Gesamtzeit für das Hochladen in die Cloud: {round(end_time - start_time, 2)} segundos.")

except Exception as e:
    print(f"❌ Fehler während der Lade-Pipeline: {e}")
