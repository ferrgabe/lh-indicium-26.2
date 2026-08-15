#!/usr/bin/env python3
"""
Schema Detector & DDL Generator
Detecta automaticamente schemas de arquivos CSV e gera instruções CREATE TABLE para PostgreSQL.
Utiliza apenas bibliotecas padrão do Python 3.
"""

import csv
import os
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class SchemaDetector:
    """
    Classe responsável por analisar arquivos CSV e inferir os tipos de dados
    mais apropriados para cada coluna no PostgreSQL.
    """
    
    # Padrões de regex para detecção de tipos de dados
    DATE_PATTERNS = [
        r'^\d{4}-\d{2}-\d{2}$',          # YYYY-MM-DD
        r'^\d{2}/\d{2}/\d{4}$',          # DD/MM/YYYY
        r'^\d{2}/\d{2}/\d{2}$',          # DD/MM/YY
        r'^\d{4}/\d{2}/\d{2}$',          # YYYY/MM/DD
        r'^\d{2}-\d{2}-\d{4}$',          # DD-MM-YYYY
        r'^\d{8}$',                      # YYYYMMDD
    ]
    
    TIMESTAMP_PATTERNS = [
        r'^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}',      # ISO timestamp
        r'^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}\.\d+',  # ISO com microsegundos
        r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$',        # BR format timestamp
    ]
    
    NUMERIC_PATTERNS = [
        r'^-?\d+$',                     # Inteiro
        r'^-?\d+\.\d+$',                # Decimal
    ]
    
    BOOLEAN_TRUE_VALUES = {'true', 't', 'yes', 'y', '1', 'sim', 's'}
    BOOLEAN_FALSE_VALUES = {'false', 'f', 'no', 'n', '0', 'nao', 'não'}

    def __init__(self, sample_size: int = 200000, null_threshold: float = 0.3):
        """
        Inicializa o detector de schema.
        
        Args:
            sample_size: Número de linhas para análise de tipo
            null_threshold: Percentual de valores nulos para considerar coluna como nullable
        """
        self.sample_size = sample_size
        self.null_threshold = null_threshold
        self.null_markers = {'', 'null', 'none', 'nan', 'na', 'n/a', '#n/d', '-', '...'}

    def read_csv_file(self, filepath: str) -> Tuple[List[str], List[List[str]]]:
        """
        Lê um arquivo CSV e retorna cabeçalho e dados.
        
        Args:
            filepath: Caminho para o arquivo CSV
            
        Returns:
            Tupla com lista de cabeçalhos e lista de linhas de dados
        """
        rows = []
        headers = []
        
        # Detecta o encoding mais comum
        encodings_to_try = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings_to_try:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    # Detecta o delimiter
                    sample = f.read(8192)
                    f.seek(0)
                    
                    dialect = csv.Sniffer().sniff(sample)
                    reader = csv.reader(f, dialect)
                    
                    try:
                        headers = next(reader)
                        # Limpa nomes de colunas
                        headers = [self._clean_column_name(h) for h in headers]
                        
                        for i, row in enumerate(reader):
                            if i >= self.sample_size:
                                break
                            rows.append(row)
                    except StopIteration:
                        print(f"AVISO: Arquivo {filepath} está vazio ou corrompido")
                        return [], []
                        
                break
            except (UnicodeDecodeError, csv.Error) as e:
                if encoding == encodings_to_try[-1]:
                    raise ValueError(f"Não foi possível ler {filepath} com nenhum encoding suportado")
                continue
                
        return headers, rows

    def _clean_column_name(self, name: str) -> str:
        """
        Limpa e padroniza nomes de colunas para uso no PostgreSQL.
        
        Args:
            name: Nome original da coluna
            
        Returns:
            Nome limpo e padronizado
        """
        # Remove caracteres especiais e espaços extras
        cleaned = name.strip()
        # Substitui espaços e caracteres especiais por underscore
        cleaned = re.sub(r'[^\w\s]', '', cleaned)
        cleaned = re.sub(r'\s+', '_', cleaned).lower()
        # Garante que comece com letra
        if cleaned and cleaned[0].isdigit():
            cleaned = f'col_{cleaned}'
        # Remove underscores duplicados
        cleaned = re.sub(r'_+', '_', cleaned)
        # Remove underscore no início/fim
        cleaned = cleaned.strip('_')
        
        return cleaned or 'unnamed_column'

    def _is_null_value(self, value: str) -> bool:
        """Verifica se um valor deve ser considerado nulo."""
        return value.strip().lower() in self.null_markers

    def _detect_date_type(self, value: str) -> bool:
        """Verifica se um valor corresponde a um padrão de data."""
        value = value.strip()
        if not value:
            return False
            
        for pattern in self.DATE_PATTERNS:
            if re.match(pattern, value):
                try:
                    # Tenta converter para validar
                    datetime.strptime(value, '%Y-%m-%d')
                    return True
                except ValueError:
                    try:
                        datetime.strptime(value, '%d/%m/%Y')
                        return True
                    except ValueError:
                        continue
        return False

    def _detect_timestamp_type(self, value: str) -> bool:
        """Verifica se um valor corresponde a um padrão de timestamp."""
        for pattern in self.TIMESTAMP_PATTERNS:
            if re.match(pattern, value.strip()):
                return True
        return False

    def _detect_numeric_type(self, value: str) -> Tuple[bool, bool]:
        """
        Verifica se um valor é numérico e se é decimal.
        
        Returns:
            Tupla (is_numeric, is_decimal)
        """
        value = value.strip()
        if not value:
            return False, False
            
        # Remove separadores de milhar e formatação
        clean_value = value.replace(',', '')
        clean_value = clean_value.replace('R$', '').replace('$', '')
        clean_value = clean_value.replace('%', '').strip()
        
        try:
            int(clean_value)
            return True, False
        except ValueError:
            try:
                float(clean_value)
                return True, True
            except ValueError:
                return False, False

    def _detect_boolean_type(self, value: str) -> bool:
        """Verifica se um valor é booleano."""
        value = value.strip().lower()
        return value in self.BOOLEAN_TRUE_VALUES or value in self.BOOLEAN_FALSE_VALUES

    def infer_column_type(self, values: List[str]) -> Tuple[str, bool]:
        """
        Infere o tipo SQL mais adequado para uma coluna baseado nos valores.
        
        Args:
            values: Lista de valores da coluna
            
        Returns:
            Tupla (tipo_postgresql, is_nullable)
        """
        # Filtra valores não nulos para análise
        non_null_values = [v for v in values if v and not self._is_null_value(v)]
        null_count = len(values) - len(non_null_values)
        
        if not non_null_values:
            return 'TEXT', True  # Coluna vazia, usa TEXT por segurança
        
        is_nullable = null_count > 0
        
        # Análise de tipo com percentuais
        total = len(non_null_values)
        
        # Verifica booleanos (precisa de 90% ou mais de valores booleanos)
        bool_count = sum(1 for v in non_null_values if self._detect_boolean_type(v))
        if bool_count / total >= 0.9:
            return 'BOOLEAN', is_nullable
        
        # Verifica datas e timestamps
        date_count = sum(1 for v in non_null_values if self._detect_date_type(v))
        if date_count / total >= 0.8:
            return 'DATE', is_nullable
            
        timestamp_count = sum(1 for v in non_null_values if self._detect_timestamp_type(v))
        if timestamp_count / total >= 0.8:
            return 'TIMESTAMP', is_nullable
        
        # Verifica números
        numeric_analysis = [self._detect_numeric_type(v) for v in non_null_values]
        numeric_count = sum(1 for is_num, _ in numeric_analysis if is_num)
        
        if numeric_count / total >= 0.9999:
            # Verifica se são inteiros ou decimais
            decimal_count = sum(1 for _, is_dec in numeric_analysis if is_dec)
            if decimal_count > 0:
                # Calcula precisão e escala para DECIMAL
                max_digits = 0
                max_decimals = 0
                for v in non_null_values:
                    clean = v.replace(',', '').replace('R$', '').replace('$', '').strip()
                    try:
                        if '.' in clean:
                            parts = clean.split('.')
                            max_digits = max(max_digits, len(parts[0]) + len(parts[1]))
                            max_decimals = max(max_decimals, len(parts[1]))
                        else:
                            max_digits = max(max_digits, len(clean))
                    except:
                        continue
                
                # precision = min(max_digits, 18)
                # scale = min(max_decimals, 6)
                return f'DECIMAL({12}, {2})', is_nullable
            else:
                # Verifica se é INTEGER ou BIGINT ou VARCHAR
                max_abs_value = 0
                for v in non_null_values:
                    try:
                        abs_val = abs(int(v.replace(',', '').strip()))
                        max_abs_value = max(max_abs_value, abs_val)
                    except:
                        pass
                
                if max_abs_value <= 2147483647:  # INTEGER range
                    return 'INTEGER', is_nullable
                elif max_abs_value <= 9223372036854775807:
                    return 'BIGINT', is_nullable
                else:
                    pass
        
        # Verifica tamanho do texto
        max_length = max(len(v) for v in non_null_values)
        
        if max_length <= 255:
            return f'VARCHAR({max_length + 20})', is_nullable  # +20 para margem de segurança
        elif max_length <= 65535:
            return 'TEXT', is_nullable
        else:
            return 'TEXT', is_nullable  # PostgreSQL TEXT pode armazenar até 1GB

    def analyze_file(self, filepath: str) -> Dict:
        """
        Analisa um arquivo CSV e retorna o schema inferido.
        
        Args:
            filepath: Caminho para o arquivo CSV
            
        Returns:
            Dicionário com informações do schema
        """
        print(f"Analisando: {filepath}")
        
        headers, rows = self.read_csv_file(filepath)
        
        if not headers:
            return None
        
        # Transpõe dados para análise por coluna
        columns_data = {header: [] for header in headers}
        for row in rows:
            for i, value in enumerate(row):
                if i < len(headers):
                    columns_data[headers[i]].append(value)
        
        # Adiciona valores vazios para linhas com menos colunas
        for header in headers:
            while len(columns_data[header]) < len(rows):
                columns_data[header].append('')
        
        # Inferência de tipos
        columns = []
        for header in headers:
            col_type, is_nullable = self.infer_column_type(columns_data[header])
            columns.append({
                'name': header,
                'type': col_type,
                'nullable': is_nullable
            })
        
        return {
            'table_name': self._derive_table_name(filepath),
            'source_file': os.path.basename(filepath),
            'columns': columns
        }

    def _derive_table_name(self, filepath: str) -> str:
        """
        Deriva um nome de tabela a partir do nome do arquivo.
        
        Args:
            filepath: Caminho para o arquivo
            
        Returns:
            Nome da tabela formatado
        """
        basename = os.path.splitext(os.path.basename(filepath))[0]
        # Converte para snake_case
        table_name = re.sub(r'[^\w\s]', '', basename)
        table_name = re.sub(r'\s+', '_', table_name).lower()
        table_name = re.sub(r'_+', '_', table_name)
        return table_name.strip('_') or 'table_from_csv'


class DDLGenerator:
    """Gera instruções DDL para PostgreSQL a partir de schemas detectados."""
    
    def generate_create_table(self, schema: Dict, add_drop: bool = True) -> str:
        """
        Gera instrução CREATE TABLE.
        
        Args:
            schema: Dicionário com informações do schema
            add_drop: Se deve adicionar DROP TABLE antes do CREATE
            
        Returns:
            String com a instrução DDL
        """
        table_name = schema['table_name']
        columns = schema['columns']
        
        ddl = []
        
        # Comentário sobre a origem
        ddl.append(f"-- Tabela gerada a partir do arquivo: {schema['source_file']}")
        ddl.append(f"-- Data de geração: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        ddl.append(f"-- Schema inferido automaticamente\n")
        
        # DROP TABLE se solicitado
        if add_drop:
            ddl.append(f"DROP TABLE IF EXISTS {table_name} CASCADE;\n")
        
        # CREATE TABLE
        ddl.append(f"CREATE TABLE {table_name} (")
        
        # Colunas
        column_defs = []
        for col in columns:
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            column_defs.append(f"    {col['name']} {col['type']} {nullable}")
        
        ddl.append(",\n".join(column_defs))
        ddl.append("\n);")
        
        # Comentários adicionais
        ddl.append(f"\n-- Comentários da tabela:")
        ddl.append(f"COMMENT ON TABLE {table_name} IS 'Dados importados do arquivo {schema['source_file']}';")
        
        # Comentários das colunas
        for col in columns:
            comment = f"Coluna gerada automaticamente, tipo inferido: {col['type']}"
            ddl.append(f"COMMENT ON COLUMN {table_name}.{col['name']} IS '{comment}';")
        
        return "\n".join(ddl)

    def generate_merged_ddl(self, schemas: List[Dict], add_drop: bool = True) -> str:
        """
        Gera um único arquivo DDL com todas as tabelas.
        
        Args:
            schemas: Lista de schemas detectados
            add_drop: Se deve adicionar DROP TABLE antes dos CREATE
            
        Returns:
            String com todas as instruções DDL
        """
        ddl_parts = []
        
        # Cabeçalho do arquivo
        ddl_parts.append("-- ============================================")
        ddl_parts.append("-- Schema SQL gerado automaticamente")
        ddl_parts.append(f"-- Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        ddl_parts.append(f"-- Total de tabelas: {len(schemas)}")
        ddl_parts.append("-- ============================================\n")
        
        # Transaction para garantir atomicidade
        ddl_parts.append("BEGIN;\n")
        
        # Gera CREATE TABLE para cada schema
        for i, schema in enumerate(schemas):
            if schema:
                ddl_parts.append(self.generate_create_table(schema, add_drop))
                if i < len(schemas) - 1:
                    ddl_parts.append("\n")  # Linha em branco entre tabelas
        
        # Commit da transaction
        ddl_parts.append("\nCOMMIT;")
        
        # Nota de rodapé
        ddl_parts.append("\n-- ============================================")
        ddl_parts.append("-- Fim do arquivo de schema")
        ddl_parts.append("-- Verifique os tipos inferidos antes de executar em produção")
        ddl_parts.append("-- ============================================")
        
        return "\n".join(ddl_parts)


def process_csv_directory(directory_path: str, output_file: str = "schema.sql", 
                         sample_size: int = 1000, recursive: bool = True) -> None:
    """
    Processa todos os arquivos CSV em um diretório e gera arquivo SQL.
    
    Args:
        directory_path: Caminho para o diretório com arquivos CSV
        output_file: Nome do arquivo SQL de saída
        sample_size: Número de linhas para análise de tipo
        recursive: Se deve procurar em subdiretórios
    """
    # Configura detectores e geradores
    detector = SchemaDetector(sample_size=sample_size)
    generator = DDLGenerator()
    
    # Encontra arquivos CSV
    csv_files = []
    if recursive:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.lower().endswith('.csv'):
                    csv_files.append(os.path.join(root, file))
    else:
        for file in os.listdir(directory_path):
            if file.lower().endswith('.csv'):
                csv_files.append(os.path.join(directory_path, file))
    
    if not csv_files:
        print("Nenhum arquivo CSV encontrado no diretório especificado.")
        return
    
    print(f"Encontrados {len(csv_files)} arquivos CSV para processamento.\n")
    
    # Analisa cada arquivo
    schemas = []
    for csv_file in sorted(csv_files):
        try:
            schema = detector.analyze_file(csv_file)
            if schema:
                schemas.append(schema)
                print(f"✓ {schema['table_name']}: {len(schema['columns'])} colunas detectadas")
        except Exception as e:
            print(f"✗ Erro ao processar {csv_file}: {str(e)}")
    
    if not schemas:
        print("\nNenhum schema válido foi gerado.")
        return
    
    # Gera arquivo SQL
    print(f"\nGerando arquivo SQL com {len(schemas)} tabelas...")
    ddl_content = generator.generate_merged_ddl(schemas)
    
    # Salva arquivo
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ddl_content)
    
    print(f"✓ Arquivo '{output_file}' gerado com sucesso!")
    
    # Gera resumo
    print("\n" + "="*60)
    print("RESUMO DO SCHEMA GERADO:")
    print("="*60)
    for schema in schemas:
        print(f"\nTabela: {schema['table_name']}")
        print(f"  Origem: {schema['source_file']}")
        print(f"  Colunas:")
        for col in schema['columns']:
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            print(f"    - {col['name']}: {col['type']} [{nullable}]")


def main():
    """Função principal do script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Detecta schemas de arquivos CSV e gera DDL para PostgreSQL',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python schema_detector.py /caminho/para/csvs
  python schema_detector.py /caminho/para/csvs -o meu_schema.sql
  python schema_detector.py /caminho/para/csvs -s 500 --no-recursive
        """
    )
    
    parser.add_argument(
        'directory',
        help='Diretório contendo os arquivos CSV'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='schema.sql',
        help='Arquivo SQL de saída (default: schema.sql)'
    )
    
    parser.add_argument(
        '-s', '--sample-size',
        type=int,
        default=200000,
        help='Número de linhas para análise de tipo (default: 200000)'
    )
    
    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='Não processar subdiretórios recursivamente'
    )
    
    args = parser.parse_args()
    
    # Verifica se o diretório existe
    if not os.path.isdir(args.directory):
        print(f"Erro: Diretório '{args.directory}' não encontrado.")
        return 1
    
    print(f"Iniciando detecção de schema...")
    print(f"Diretório: {args.directory}")
    print(f"Arquivo de saída: {args.output}")
    print(f"Tamanho da amostra: {args.sample_size} linhas")
    print(f"Processamento recursivo: {not args.no_recursive}\n")
    
    try:
        process_csv_directory(
            directory_path=args.directory,
            output_file=args.output,
            sample_size=args.sample_size,
            recursive=not args.no_recursive
        )
        return 0
    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())