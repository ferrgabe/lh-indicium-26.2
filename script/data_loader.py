#!/usr/bin/env python3
"""
Data Loader - Carrega arquivos CSV para PostgreSQL
Respeita o schema previamente criado e não realiza transformações nos dados.
"""

import csv
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import argparse
import re
import json

# Biblioteca externa para conexão com PostgreSQL
try:
    import psycopg2
    from psycopg2 import sql, extras
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
except ImportError:
    print("Erro: psycopg2 não está instalado. Instale com: pip install psycopg2-binary")
    sys.exit(1)


class DatabaseConnector:
    """Gerencia a conexão com o banco de dados PostgreSQL."""
    
    def __init__(self, config: Dict):
        """
        Inicializa o conector com configurações de conexão.
        
        Args:
            config: Dicionário com parâmetros de conexão
        """
        self.config = config
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Estabelece conexão com o banco de dados."""
        try:
            self.connection = psycopg2.connect(
                host=self.config.get('host', 'localhost'),
                port=self.config.get('port', 5432),
                database=self.config.get('database', 'postgres'),
                user=self.config.get('user', 'postgres'),
                password=self.config.get('password', 'postgres'),
                connect_timeout=30
            )
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.connection.cursor()
            
            logging.info(f"Conectado ao PostgreSQL {self.config['host']}:{self.config['port']}")
            logging.info(f"Banco de dados: {self.config['database']}")
            
            # Testa a conexão
            self.cursor.execute("SELECT version();")
            version = self.cursor.fetchone()[0]
            logging.info(f"Versão: {version}")
            
            return True
            
        except psycopg2.Error as e:
            logging.error(f"Erro ao conectar ao PostgreSQL: {e}")
            return False
    
    def disconnect(self):
        """Fecha a conexão com o banco de dados."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
                logging.info("Conexão com PostgreSQL fechada.")
        except Exception as e:
            logging.error(f"Erro ao desconectar: {e}")
    
    def execute_schema_file(self, schema_file: str):
        """
        Executa um arquivo SQL de schema.
        
        Args:
            schema_file: Caminho para o arquivo SQL
        """
        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            logging.info(f"Executando schema de: {schema_file}")
            self.cursor.execute(schema_sql)
            logging.info("Schema executado com sucesso!")
            
        except FileNotFoundError:
            logging.error(f"Arquivo de schema não encontrado: {schema_file}")
            raise
        except psycopg2.Error as e:
            logging.error(f"Erro ao executar schema: {e}")
            self.connection.rollback()
            raise
    
    def get_table_columns(self, table_name: str) -> Dict[str, str]:
        """
        Obtém as colunas e seus tipos de uma tabela do banco.
        
        Args:
            table_name: Nome da tabela
            
        Returns:
            Dicionário com nome da coluna e tipo
        """
        query = """
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
              AND table_name = %s
            ORDER BY ordinal_position;
        """
        
        self.cursor.execute(query, (table_name.lower(),))
        columns = {}
        
        for row in self.cursor.fetchall():
            columns[row[0]] = row[1]
        
        return columns
    
    def get_table_list(self) -> List[str]:
        """
        Lista todas as tabelas no schema public.
        
        Returns:
            Lista de nomes de tabelas
        """
        query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
              AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """
        
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]


class CSVLoader:
    """Responsável por carregar dados dos CSVs para as tabelas do PostgreSQL."""
    
    def __init__(self, db_connector: DatabaseConnector):
        """
        Inicializa o loader.
        
        Args:
            db_connector: Instância do conector de banco de dados
        """
        self.db = db_connector
        self.statistics = {
            'processed_files': 0,
            'failed_files': 0,
            'total_rows': 0,
            'errors': []
        }
    
    def _derive_table_name(self, filename: str) -> str:
        """
        Deriva o nome da tabela a partir do nome do arquivo.
        
        Args:
            filename: Nome do arquivo CSV
            
        Returns:
            Nome da tabela correspondente
        """
        # Remove extensão e converte para snake_case
        basename = os.path.splitext(os.path.basename(filename))[0]
        
        # Aplica as mesmas regras do detector de schema
        import re
        table_name = re.sub(r'[^\w\s]', '', basename)
        table_name = re.sub(r'\s+', '_', table_name).lower()
        table_name = re.sub(r'_+', '_', table_name)
        
        return table_name.strip('_') or 'table_from_csv'
    
    def _read_csv_with_config(self, filepath: str) -> Tuple[List[str], List[List[str]]]:
        """
        Lê arquivo CSV detectando automaticamente configurações.
        Não faz nenhum tratamento nos dados.
        
        Args:
            filepath: Caminho do arquivo CSV
            
        Returns:
            Tupla (headers, rows)
        """
        encodings_to_try = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252', 'utf-8-sig']
        
        for encoding in encodings_to_try:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    # Detecta o dialect automaticamente
                    sample = f.read(8192)
                    f.seek(0)
                    
                    dialect = csv.Sniffer().sniff(sample)
                    reader = csv.reader(f, dialect)
                    
                    # Obtém cabeçalhos
                    try:
                        headers = next(reader)
                    except StopIteration:
                        logging.warning(f"Arquivo vazio: {filepath}")
                        return [], []
                    
                    # Lê todas as linhas (sem tratamento)
                    rows = list(reader)
                    
                    logging.info(f"Arquivo lido com encoding {encoding}: {len(rows)} linhas")
                    return headers, rows
                    
            except (UnicodeDecodeError, csv.Error) as e:
                if encoding == encodings_to_try[-1]:
                    raise ValueError(f"Não foi possível ler {filepath}: {str(e)}")
                continue
        
        return [], []
    
    def _validate_columns(self, csv_headers: List[str], table_columns: Dict[str, str]) -> bool:
        """
        Valida se as colunas do CSV correspondem às da tabela.
        
        Args:
            csv_headers: Headers do arquivo CSV
            table_columns: Colunas existentes na tabela
            
        Returns:
            True se válido, False caso contrário
        """
        # Limpa nomes das colunas do CSV (mesma lógica do detector)
        import re
        cleaned_headers = []
        for header in csv_headers:
            cleaned = header.strip()
            cleaned = re.sub(r'[^\w\s]', '', cleaned)
            cleaned = re.sub(r'\s+', '_', cleaned).lower()
            cleaned = re.sub(r'_+', '_', cleaned)
            cleaned = cleaned.strip('_')
            cleaned_headers.append(cleaned)
        
        # Verifica correspondência
        table_col_names = [col.lower() for col in table_columns.keys()]
        
        missing_in_csv = set(table_col_names) - set(cleaned_headers)
        missing_in_table = set(cleaned_headers) - set(table_col_names)
        
        if missing_in_csv:
            logging.warning(f"Colunas na tabela mas não no CSV: {missing_in_csv}")
        
        if missing_in_table:
            logging.warning(f"Colunas no CSV mas não na tabela: {missing_in_table}")
            # Não é erro crítico - vamos carregar apenas as colunas que existem
        
        return True
    
    def load_csv_to_table(self, csv_filepath: str) -> bool:
        """
        Carrega dados de um arquivo CSV para sua tabela correspondente.
        
        Args:
            csv_filepath: Caminho para o arquivo CSV
            
        Returns:
            True se sucesso, False se falha
        """
        start_time = datetime.now()
        table_name = self._derive_table_name(csv_filepath)
        
        logging.info(f"\n{'='*60}")
        logging.info(f"Processando: {os.path.basename(csv_filepath)}")
        logging.info(f"Tabela destino: {table_name}")
        
        try:
            # Verifica se a tabela existe
            table_list = self.db.get_table_list()
            if table_name not in table_list:
                logging.error(f"Tabela '{table_name}' não existe. Execute o schema primeiro.")
                self.statistics['failed_files'] += 1
                self.statistics['errors'].append(f"Tabela não encontrada: {table_name}")
                return False
            
            # Obtém colunas da tabela
            table_columns = self.db.get_table_columns(table_name)
            if not table_columns:
                logging.error(f"Tabela '{table_name}' não possui colunas definidas")
                return False
            
            logging.info(f"Colunas na tabela: {list(table_columns.keys())}")
            
            # Lê o CSV
            csv_headers, csv_rows = self._read_csv_with_config(csv_filepath)
            
            if not csv_headers:
                logging.warning(f"Arquivo CSV vazio ou sem headers: {csv_filepath}")
                return False
            
            logging.info(f"CSV Headers originais: {csv_headers}")
            logging.info(f"Total de linhas no CSV: {len(csv_rows)}")
            
            # Valida colunas
            self._validate_columns(csv_headers, table_columns)
            
            # Mapeia colunas do CSV para colunas da tabela
            column_mapping = self._map_columns(csv_headers, table_columns)
            
            if not column_mapping:
                logging.error("Não foi possível mapear nenhuma coluna")
                return False
            
            logging.info(f"Mapeamento de colunas: {column_mapping}")
            
            # Prepara e executa o INSERT
            inserted_count = self._batch_insert(table_name, csv_rows, column_mapping, table_columns)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logging.info(f"✓ {inserted_count} linhas inseridas em {duration:.2f} segundos")
            
            self.statistics['processed_files'] += 1
            self.statistics['total_rows'] += inserted_count
            
            return True
            
        except Exception as e:
            logging.error(f"✗ Erro ao processar {csv_filepath}: {str(e)}")
            self.statistics['failed_files'] += 1
            self.statistics['errors'].append(f"{csv_filepath}: {str(e)}")
            return False
    
    def _map_columns(self, csv_headers: List[str], table_columns: Dict[str, str]) -> Dict[int, str]:
        """
        Mapeia índices das colunas do CSV para nomes de colunas da tabela.
        
        Args:
            csv_headers: Headers do CSV
            table_columns: Colunas da tabela
            
        Returns:
            Dicionário {csv_index: table_column_name}
        """
        import re
        
        # Limpa headers do CSV
        cleaned_headers = []
        for header in csv_headers:
            cleaned = header.strip()
            cleaned = re.sub(r'[^\w\s]', '', cleaned)
            cleaned = re.sub(r'\s+', '_', cleaned).lower()
            cleaned = re.sub(r'_+', '_', cleaned)
            cleaned = cleaned.strip('_')
            cleaned_headers.append(cleaned)
        
        # Mapeia por correspondência exata
        mapping = {}
        table_col_names = {col.lower(): col for col in table_columns.keys()}
        
        for i, csv_col in enumerate(cleaned_headers):
            if csv_col in table_col_names:
                mapping[i] = table_col_names[csv_col]
        
        return mapping
    
    def _prepare_row_values(self, row: List[str], column_mapping: Dict[int, str], 
                           table_columns: Dict[str, str]) -> Dict[str, Optional[str]]:
        """
        Prepara os valores de uma linha para inserção.
        Não faz conversão de tipos, apenas limpa strings vazias para NULL.
        
        Args:
            row: Linha do CSV
            column_mapping: Mapeamento de colunas
            table_columns: Definição das colunas da tabela
            
        Returns:
            Dicionário {column_name: value}
        """
        values = {}
        
        for csv_index, col_name in column_mapping.items():
            # Obtém o valor da linha
            if csv_index < len(row):
                value = row[csv_index]
            else:
                value = ''
            
            # Se for string vazia ou null, converte para None (NULL no banco)
            if value.strip() == '' or value.strip().lower() in ['null', 'none', 'nan']:
                values[col_name] = None
            else:
                # Mantém o valor original, sem tratamento
                values[col_name] = value
        
        return values
    
    def _batch_insert(self, table_name: str, rows: List[List[str]], 
                  column_mapping: Dict[int, str], 
                  table_columns: Dict[str, str], 
                  batch_size: int = 1000) -> int:

        if not rows:
            return 0
        
        columns = list(column_mapping.values())
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))
        
        insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
        
        total_inserted = 0
        
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            batch_values = []
            
            for row in batch:
                row_data = self._prepare_row_values(row, column_mapping, table_columns)
                values = tuple(row_data[col] for col in columns)
                batch_values.append(values)
            
            try:
                # Usa executemany que é mais estável
                extras.execute_batch(self.db.cursor, insert_sql, batch_values, page_size=batch_size)
                total_inserted += len(batch_values)
                
            except psycopg2.Error as e:
                logging.error(f"Erro no lote: {e}")
                # Fallback linha a linha
                for values in batch_values:
                    try:
                        self.db.cursor.execute(insert_sql, values)
                        total_inserted += 1
                    except psycopg2.Error as line_error:
                        logging.warning(f"  Erro: {line_error}")
            
            logging.info(f"  Progresso: {total_inserted}/{len(rows)}")
        
        return total_inserted
    
    def load_all_csvs(self, directory_path: str, pattern: str = "*.csv", recursive: bool = True):
        """
        Carrega todos os arquivos CSV de um diretório.
        
        Args:
            directory_path: Caminho do diretório
            pattern: Padrão de arquivos (default: *.csv)
            recursive: Se deve procurar em subdiretórios
        """
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
            logging.error(f"Nenhum arquivo CSV encontrado em: {directory_path}")
            return
        
        logging.info(f"\n{'='*60}")
        logging.info(f"Total de arquivos CSV encontrados: {len(csv_files)}")
        logging.info(f"{'='*60}")
        
        # Processa cada arquivo
        for csv_file in sorted(csv_files):
            self.load_csv_to_table(csv_file)
    
    def print_statistics(self):
        """Imprime estatísticas do carregamento."""
        print(f"\n{'='*60}")
        print("ESTATÍSTICAS DO CARREGAMENTO:")
        print(f"{'='*60}")
        print(f"Arquivos processados com sucesso: {self.statistics['processed_files']}")
        print(f"Arquivos com falha: {self.statistics['failed_files']}")
        print(f"Total de linhas inseridas: {self.statistics['total_rows']}")
        
        if self.statistics['errors']:
            print(f"\nErros encontrados:")
            for error in self.statistics['errors']:
                print(f"  - {error}")

class ErrorLogger:
    """
    Sistema dedicado para logging de erros durante o carregamento de dados.
    Gera logs detalhados apenas quando erros ocorrem.
    """
    
    def __init__(self, error_log_dir: str = "error_logs"):
        """
        Inicializa o logger de erros.
        
        Args:
            error_log_dir: Diretório onde os logs de erro serão salvos
        """
        self.error_log_dir = Path(error_log_dir)
        self.error_log_dir.mkdir(exist_ok=True)
        
        # Arquivos de log
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Log detalhado de erros (apenas quando há erros)
        self.error_file = self.error_log_dir / f"errors_{timestamp}.log"
        self.error_entries = []
        
        # Resumo executivo em JSON
        self.summary_file = self.error_log_dir / f"error_summary_{timestamp}.json"
        self.error_summary = {
            'timestamp': timestamp,
            'total_errors': 0,
            'files_affected': set(),
            'error_types': {},
            'tables_affected': set()
        }
        
        # Configura logger específico para erros
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Configura logger específico para erros."""
        logger = logging.getLogger(f"ErrorLogger_{datetime.now().timestamp()}")
        logger.setLevel(logging.ERROR)
        
        # Handler para arquivo
        file_handler = logging.FileHandler(self.error_file, encoding='utf-8')
        file_handler.setLevel(logging.ERROR)
        
        # Formato detalhado
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        
        return logger
    
    def log_schema_error(self, csv_file: str, table_name: str, column_name: str, 
                         value: str, data_type: str, error_msg: str, row_number: int = None):
        """
        Registra erro de schema/tipo de dados.
        
        Args:
            csv_file: Arquivo CSV de origem
            table_name: Nome da tabela
            column_name: Nome da coluna
            value: Valor que causou o erro
            data_type: Tipo de dado esperado
            error_msg: Mensagem de erro
            row_number: Número da linha no CSV
        """
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'SCHEMA_ERROR',
            'severity': 'HIGH',
            'file': str(csv_file),
            'table': table_name,
            'column': column_name,
            'value': str(value)[:200],  # Limita tamanho
            'expected_type': data_type,
            'error_message': error_msg,
            'row_number': row_number,
            'solution': self._suggest_solution(error_msg, data_type, value)
        }
        
        self._record_error(error_entry)
        
    def log_insert_error(self, csv_file: str, table_name: str, row_data: Dict,
                        error_msg: str, row_number: int = None):
        """
        Registra erro de inserção.
        
        Args:
            csv_file: Arquivo CSV de origem
            table_name: Nome da tabela
            row_data: Dados da linha que falhou
            error_msg: Mensagem de erro
            row_number: Número da linha no CSV
        """
        # Analisa o erro para extrair informações
        column_name = self._extract_column_from_error(error_msg)
        
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'INSERT_ERROR',
            'severity': 'HIGH',
            'file': str(csv_file),
            'table': table_name,
            'column': column_name,
            'row_data': {k: str(v)[:100] for k, v in row_data.items()},
            'error_message': error_msg,
            'row_number': row_number,
            'solution': self._suggest_solution(error_msg, None, None)
        }
        
        self._record_error(error_entry)
    
    def log_batch_error(self, csv_file: str, table_name: str, batch_info: Dict,
                       error_msg: str):
        """
        Registra erro em lote de inserção.
        
        Args:
            csv_file: Arquivo CSV de origem
            table_name: Nome da tabela
            batch_info: Informações do lote
            error_msg: Mensagem de erro
        """
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'BATCH_ERROR',
            'severity': 'MEDIUM',
            'file': str(csv_file),
            'table': table_name,
            'batch_info': batch_info,
            'error_message': error_msg,
            'solution': self._suggest_solution(error_msg, None, None)
        }
        
        self._record_error(error_entry)
    
    def _record_error(self, error_entry: Dict):
        """Registra erro no sistema de logging."""
        
        # Adiciona à lista de erros
        self.error_entries.append(error_entry)
        
        # Atualiza resumo
        self.error_summary['total_errors'] += 1
        self.error_summary['files_affected'].add(error_entry.get('file', 'unknown'))
        self.error_summary['tables_affected'].add(error_entry.get('table', 'unknown'))
        
        error_type = error_entry['type']
        self.error_summary['error_types'][error_type] = \
            self.error_summary['error_types'].get(error_type, 0) + 1
        
        # Log no arquivo
        self.logger.error(self._format_error_message(error_entry))
    
    def _extract_column_from_error(self, error_msg: str) -> Optional[str]:
        """Extrai nome da coluna da mensagem de erro."""
        # PostgreSQL geralmente indica a coluna no erro
        patterns = [
            r'column "(\w+)"',
            r'coluna "(\w+)"',
            r'campo "(\w+)"',
            r'field "(\w+)"'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, error_msg, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _suggest_solution(self, error_msg: str, data_type: str = None, 
                         value: Any = None) -> str:
        """
        Sugere soluções baseadas no tipo de erro.
        
        Args:
            error_msg: Mensagem de erro
            data_type: Tipo de dado esperado
            value: Valor problemático
            
        Returns:
            Sugestão de solução
        """
        suggestions = []
        
        # Erros numéricos
        if 'numeric' in error_msg.lower() or 'estouro' in error_msg.lower():
            suggestions.append("Aumentar a precisão/escala da coluna DECIMAL")
            suggestions.append("ALTER TABLE [tabela] ALTER COLUMN [coluna] TYPE DECIMAL(precisão, escala);")
            if value:
                suggestions.append(f"Valor problemático: {value}")
        
        # Erros de data
        elif 'date' in error_msg.lower() or 'timestamp' in error_msg.lower():
            suggestions.append("Verificar formato de data no CSV")
            suggestions.append("Considerar usar TEXT para datas em formato não padrão")
        
        # Erros de tamanho
        elif 'varchar' in error_msg.lower() or 'character varying' in error_msg.lower():
            suggestions.append("Aumentar o tamanho da coluna VARCHAR")
            suggestions.append("ALTER TABLE [tabela] ALTER COLUMN [coluna] TYPE VARCHAR(maior_tamanho);")
        
        # Erros de valor nulo
        elif 'not null' in error_msg.lower() or 'não nulo' in error_msg.lower():
            suggestions.append("Definir valor default para a coluna")
            suggestions.append("ALTER TABLE [tabela] ALTER COLUMN [coluna] SET DEFAULT 'valor_default';")
            suggestions.append("Ou permitir NULL: ALTER TABLE [tabela] ALTER COLUMN [coluna] DROP NOT NULL;")
        
        # Erros genéricos
        else:
            suggestions.append("Analisar o valor problemático")
            suggestions.append("Verificar compatibilidade de tipos de dados")
            suggestions.append("Considerar revisar o schema da tabela")
        
        return " | ".join(suggestions[:3])
    
    def _format_error_message(self, error_entry: Dict) -> str:
        """
        Formata mensagem de erro para o arquivo de log.
        
        Args:
            error_entry: Dicionário com informações do erro
            
        Returns:
            Mensagem formatada
        """
        parts = []
        
        parts.append(f"\n{'='*80}")
        parts.append(f"ERRO {error_entry['type']} - Severidade: {error_entry['severity']}")
        parts.append(f"{'='*80}")
        parts.append(f"Timestamp: {error_entry['timestamp']}")
        parts.append(f"Arquivo: {error_entry['file']}")
        parts.append(f"Tabela: {error_entry['table']}")
        
        if error_entry.get('column'):
            parts.append(f"Coluna: {error_entry['column']}")
        
        if error_entry.get('row_number'):
            parts.append(f"Linha no CSV: {error_entry['row_number']}")
        
        if error_entry.get('value'):
            parts.append(f"Valor problemático: {error_entry['value']}")
        
        if error_entry.get('expected_type'):
            parts.append(f"Tipo esperado: {error_entry['expected_type']}")
        
        parts.append(f"\nMensagem de Erro:")
        parts.append(f"  {error_entry['error_message']}")
        
        if error_entry.get('row_data'):
            parts.append(f"\nDados da Linha:")
            for key, value in error_entry['row_data'].items():
                parts.append(f"  {key}: {value}")
        
        if error_entry.get('solution'):
            parts.append(f"\n💡 SOLUÇÃO SUGERIDA:")
            parts.append(f"  {error_entry['solution']}")
        
        if error_entry.get('batch_info'):
            parts.append(f"\nInformações do Lote:")
            for key, value in error_entry['batch_info'].items():
                parts.append(f"  {key}: {value}")
        
        parts.append(f"{'='*80}\n")
        
        return '\n'.join(parts)
    
    def generate_error_report(self) -> str:
        """
        Gera relatório consolidado de erros.
        
        Returns:
            Caminho do arquivo de relatório
        """
        if not self.error_entries:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.error_log_dir / f"error_report_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("RELATÓRIO DE ERROS - DATA LOADER\n")
            f.write("="*80 + "\n")
            f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total de Erros: {len(self.error_entries)}\n\n")
            
            # Resumo por arquivo
            f.write("ERROS POR ARQUIVO:\n")
            f.write("-"*40 + "\n")
            errors_by_file = {}
            for error in self.error_entries:
                file = error['file']
                if file not in errors_by_file:
                    errors_by_file[file] = {'count': 0, 'types': {}, 'tables': set()}
                errors_by_file[file]['count'] += 1
                errors_by_file[file]['types'][error['type']] = \
                    errors_by_file[file]['types'].get(error['type'], 0) + 1
                errors_by_file[file]['tables'].add(error['table'])
            
            for file, info in errors_by_file.items():
                f.write(f"\n📁 {os.path.basename(file)}\n")
                f.write(f"   Total erros: {info['count']}\n")
                f.write(f"   Tabelas afetadas: {', '.join(info['tables'])}\n")
                f.write(f"   Tipos de erro:\n")
                for error_type, count in info['types'].items():
                    f.write(f"     - {error_type}: {count}\n")
            
            # Erros mais comuns
            f.write(f"\n\nERROS POR TIPO:\n")
            f.write("-"*40 + "\n")
            for error_type, count in self.error_summary['error_types'].items():
                f.write(f"  {error_type}: {count} ocorrências\n")
            
            # Soluções sugeridas
            f.write(f"\n\nSOLUÇÕES SUGERIDAS:\n")
            f.write("-"*40 + "\n")
            unique_solutions = set()
            for error in self.error_entries:
                if error.get('solution'):
                    unique_solutions.add(error['solution'])
            
            for i, solution in enumerate(unique_solutions, 1):
                f.write(f"\n{i}. {solution}\n")
            
            f.write(f"\n\n{'='*80}\n")
            f.write("FIM DO RELATÓRIO\n")
            f.write(f"{'='*80}\n")
        
        # Atualiza e salva resumo JSON
        self.error_summary['files_affected'] = list(self.error_summary['files_affected'])
        self.error_summary['tables_affected'] = list(self.error_summary['tables_affected'])
        
        with open(self.summary_file, 'w', encoding='utf-8') as f:
            json.dump(self.error_summary, f, indent=2, ensure_ascii=False)
        
        return str(report_file)
    
    def has_errors(self) -> bool:
        """Verifica se há erros registrados."""
        return len(self.error_entries) > 0
    
    def get_error_count(self) -> int:
        """Retorna número total de erros."""
        return len(self.error_entries)


class EnhancedCSVLoader(CSVLoader):
    """
    Versão melhorada do CSVLoader com logging dedicado de erros.
    """
    
    def __init__(self, db_connector, error_logger: ErrorLogger):
        """
        Inicializa o loader melhorado.
        
        Args:
            db_connector: Conector do banco de dados
            error_logger: Logger de erros dedicado
        """
        super().__init__(db_connector)
        self.error_logger = error_logger
        self.current_file = None
        self.current_table = None
    
    def load_csv_to_table(self, csv_filepath: str) -> bool:
        """
        Carrega dados com logging detalhado de erros.
        
        Args:
            csv_filepath: Caminho para o arquivo CSV
            
        Returns:
            True se sucesso, False se falha
        """
        self.current_file = csv_filepath
        start_time = datetime.now()
        table_name = self._derive_table_name(csv_filepath)
        self.current_table = table_name
        
        logging.info(f"\n{'='*60}")
        logging.info(f"Processando: {os.path.basename(csv_filepath)}")
        logging.info(f"Tabela destino: {table_name}")
        
        try:
            # Verifica se a tabela existe
            table_list = self.db.get_table_list()
            if table_name not in table_list:
                error_msg = f"Tabela '{table_name}' não existe"
                self.error_logger.log_schema_error(
                    csv_filepath, table_name, None, None, None, error_msg
                )
                self.statistics['failed_files'] += 1
                return False
            
            # Obtém colunas da tabela
            table_columns = self.db.get_table_columns(table_name)
            if not table_columns:
                error_msg = f"Tabela '{table_name}' não possui colunas definidas"
                self.error_logger.log_schema_error(
                    csv_filepath, table_name, None, None, None, error_msg
                )
                return False
            
            # Lê o CSV
            csv_headers, csv_rows = self._read_csv_with_config(csv_filepath)
            
            if not csv_headers:
                return False
            
            logging.info(f"Total de linhas no CSV: {len(csv_rows)}")
            
            # Mapeia colunas
            column_mapping = self._map_columns(csv_headers, table_columns)
            
            if not column_mapping:
                error_msg = "Não foi possível mapear nenhuma coluna"
                self.error_logger.log_schema_error(
                    csv_filepath, table_name, None, None, None, error_msg
                )
                return False
            
            # Insere dados com logging de erros
            inserted_count, error_count = self._batch_insert_with_error_logging(
                table_name, csv_rows, column_mapping, table_columns
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logging.info(f"✓ {inserted_count} linhas inseridas em {duration:.2f} segundos")
            if error_count > 0:
                logging.warning(f"⚠ {error_count} linhas com erro não foram inseridas")
            
            self.statistics['processed_files'] += 1
            self.statistics['total_rows'] += inserted_count
            
            return True
            
        except Exception as e:
            logging.error(f"✗ Erro ao processar {csv_filepath}: {str(e)}")
            self.error_logger.log_schema_error(
                csv_filepath, table_name, None, None, None, str(e)
            )
            self.statistics['failed_files'] += 1
            return False
    
    def _batch_insert_with_error_logging(self, table_name: str, rows: List[List[str]], 
                                        column_mapping: Dict[int, str], 
                                        table_columns: Dict[str, str], 
                                        batch_size: int = 1000) -> Tuple[int, int]:
        """
        Insere dados em lotes com logging detalhado de erros.
        
        Returns:
            Tupla (inseridos_com_sucesso, erros)
        """
        if not rows:
            return 0, 0
        
        columns = list(column_mapping.values())
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))
        
        insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
        
        total_inserted = 0
        total_errors = 0
        
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            
            for row_index, row in enumerate(batch):
                global_row_index = i + row_index + 1  # +1 para pular o header
                
                try:
                    # Prepara valores
                    row_data = self._prepare_row_values(row, column_mapping, table_columns)
                    values = tuple(row_data[col] for col in columns)
                    
                    # Tenta inserir
                    self.db.cursor.execute(insert_sql, values)
                    total_inserted += 1
                    
                except psycopg2.Error as e:
                    total_errors += 1
                    error_msg = str(e)
                    
                    # Log detalhado do erro
                    self.error_logger.log_insert_error(
                        csv_file=self.current_file,
                        table_name=table_name,
                        row_data=row_data,
                        error_msg=error_msg,
                        row_number=global_row_index
                    )
                    
                    # Log resumido no console
                    if total_errors <= 10:  # Limita logs no console
                        logging.warning(f"  Linha {global_row_index}: {error_msg[:100]}")
                    
                except Exception as e:
                    total_errors += 1
                    logging.debug(f"  Erro inesperado linha {global_row_index}: {str(e)}")
            
            logging.info(f"  Progresso: {total_inserted}/{len(rows)} " + 
                        (f"(erros: {total_errors})" if total_errors > 0 else ""))
        
        return total_inserted, total_errors

def setup_logging(log_file: Optional[str] = None):
    """Configura o sistema de logging."""
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    if log_file:
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format=log_format
        )


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description='Carrega dados de arquivos CSV para PostgreSQL',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python data_loader.py /caminho/csvs
  python data_loader.py /caminho/csvs --host localhost --port 5432 --database postgres --user postgres --password senha123
  python data_loader.py /caminho/csvs --schema meu_schema.sql --log load.log
        """
    )
    
    # Argumentos de diretório e arquivos
    parser.add_argument('directory', help='Diretório contendo os arquivos CSV')
    parser.add_argument('--schema', default='schema.sql', 
                       help='Arquivo SQL com schema (default: schema.sql)')
    parser.add_argument('--no-execute-schema', action='store_true',
                       help='Não executar o arquivo de schema (já existe)')
    
    # Argumentos de conexão
    parser.add_argument('--host', default='localhost', help='Host do PostgreSQL (default: localhost)')
    parser.add_argument('--port', type=int, default=5432, help='Porta do PostgreSQL (default: 5432)')
    parser.add_argument('--database', default='postgres', help='Nome do banco de dados (default: postgres)')
    parser.add_argument('--user', default='postgres', help='Usuário do banco (default: postgres)')
    parser.add_argument('--password', default='', help='Senha do banco de dados')
    
    # Argumentos de processamento
    parser.add_argument('--batch-size', type=int, default=1000, 
                       help='Tamanho do lote para inserção (default: 1000)')
    parser.add_argument('--log', help='Arquivo de log (opcional)')
    parser.add_argument('--no-recursive', action='store_true',
                       help='Não processar subdiretórios')
    
    args = parser.parse_args()
    
    # Configura logging
    setup_logging(args.log)
    
    logging.info("="*60)
    logging.info("DATA LOADER - PostgreSQL CSV Importer")
    logging.info("="*60)
    logging.info(f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Configuração de conexão
    db_config = {
        'host': args.host,
        'port': args.port,
        'database': args.database,
        'user': args.user,
        'password': args.password
    }
    
    # Inicializa componentes
    error_logger = ErrorLogger("error_logs")
    db = DatabaseConnector(db_config)
    loader = EnhancedCSVLoader(db, error_logger)
    
    try:
        # Conecta ao banco
        logging.info("\nConectando ao PostgreSQL...")
        if not db.connect():
            logging.error("Falha ao conectar ao banco de dados")
            return 1
        
        # Executa schema se necessário
        if not args.no_execute_schema:
            if os.path.exists(args.schema):
                logging.info(f"\nExecutando schema: {args.schema}")
                try:
                    db.execute_schema_file(args.schema)
                    logging.info("Schema executado com sucesso!")
                except Exception as e:
                    logging.error(f"Erro ao executar schema: {e}")
                    return 1
            else:
                logging.warning(f"Arquivo de schema não encontrado: {args.schema}")
                logging.warning("Continuando sem execução de schema...")
        
        # Lista tabelas existentes
        tables = db.get_table_list()
        logging.info(f"\nTabelas encontradas no banco: {tables}")
        
        # Carrega os CSVs
        logging.info(f"\nIniciando carregamento dos CSVs...")
        loader.load_all_csvs(
            args.directory, 
            recursive=not args.no_recursive
        )
        
        # Exibe estatísticas
        loader.print_statistics()
        
        return 0
        
    except KeyboardInterrupt:
        logging.info("\nProcessamento interrompido pelo usuário")
        loader.print_statistics()
        return 1
        
    except Exception as e:
        logging.error(f"Erro fatal: {str(e)}")
        return 1
        
    finally:
        db.disconnect()
        logging.info(f"Fim: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    exit(main())