import csv
import os

for file_name in sorted(os.listdir('.')):
    if file_name.lower().endswith('.csv'):
        file_path = os.path.join('.', file_name)
        with open(file_path, mode='r', encoding='utf-8-sig') as f:
            # Tenta detectar delimitador (, ou ;)
            sample = f.read(1024)
            f.seek(0)
            delimiter = ';' if ';' in sample else ','
            
            reader = csv.reader(f, delimiter=delimiter)
            headers = next(reader, None)
            
            print(f"Tabela: {file_name}")
            print(f"Colunas: {headers}")
            print("-" * 50)