import oracledb
import pandas
import csv
from dotenv import load_dotenv
import os
import preprocess

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_DSN = os.getenv("DB_DSN")
LIB_DIR = os.getenv("LIB_DIR")

oracledb.init_oracle_client(lib_dir=LIB_DIR)

# Check Connection
def bulk_load_csv(data_packed: dict[str, pandas.DataFrame]):
    try:
        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        cursor = conn.cursor()
        
        tables = list(data_packed.keys())
        
        for name in reversed(tables):
            cursor.execute(f"DELETE FROM {name}")
        conn.commit()
        print("Tables cleared.")
        
        for name, df in data_packed.items():
            with open(f"./data/{name}.csv", mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                data_to_insert = [row for row in reader]
            unpackedColumns = ", ".join(df.columns)
            cols = list(df.columns)
            placeholders = []
            for i, col in enumerate(cols, 1):
                if col == 'vid_upload_date':
                    placeholders.append(f"TO_DATE(:{i}, 'YYYY-MM-DD')")
                else:
                    placeholders.append(f":{i}")
            numInputs = ", ".join(placeholders)
            SQL = f"insert into {name} ({unpackedColumns}) values ({numInputs})"
            
            print(f"Beginning bulk load of {name}... ({len(data_to_insert)} rows)")
            cursor.executemany(SQL, data_to_insert)
            conn.commit()
            print(f"Load complete.")
            
    except Exception as e:
        print(f"Error during bulk load: {e}")
        if 'conn' in locals():
            conn.rollback()
            
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()  
        
def main():
    bulk_load_csv(preprocess.export_data(preprocess.generate_processed_data()))
    
if __name__ == "__main__":
    main()