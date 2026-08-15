#!/usr/bin/env python3
"""
Previsão de Demanda com Baseline (Média Móvel 3 Meses)
Conecta ao PostgreSQL, executa a query a partir do arquivo SQL e gera a previsão.
"""

import sys
import argparse
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_absolute_error
import warnings

# Suprime os avisos do pandas sobre uso direto de conexão psycopg2 (caso ocorram)
warnings.filterwarnings('ignore', category=UserWarning)

# Importa o DatabaseConnector do seu script data_loader.py
# (Presume-se que previsao_baseline.py e data_loader.py estão na mesma pasta 'script')
try:
    from data_loader import DatabaseConnector
except ImportError:
    print("Erro: Não foi possível importar DatabaseConnector de data_loader.py.")
    print("Certifique-se de que ambos estão na mesma pasta.")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Gera Previsão de Demanda Baseline')
    parser.add_argument('--host', default='localhost', help='Host do PostgreSQL')
    parser.add_argument('--port', type=int, default=5432, help='Porta')
    parser.add_argument('--database', default='postgres', help='Database')
    parser.add_argument('--user', default='postgres', help='Usuário')
    parser.add_argument('--password', default='postgres', help='Senha')
    args = parser.parse_args()

    # 1. Configurar os caminhos respeitando a estrutura do seu projeto
    # Como o script roda dentro da pasta 'script', a raiz é o diretório "pai"
    root_dir = Path(__file__).resolve().parent.parent
    sql_file_path = root_dir / 'sql' / 'Q6_previsao_demanda.sql'

    if not sql_file_path.exists():
        print(f"Erro: Arquivo SQL não encontrado no caminho: {sql_file_path}")
        sys.exit(1)

    print(f"Lendo query SQL de: {sql_file_path}")
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_query = f.read()

    # 2. Configurar e Instanciar a conexão usando a sua classe do data_loader.py
    db_config = {
        'host': args.host,
        'port': args.port,
        'database': args.database,
        'user': args.user,
        'password': args.password
    }
    
    db = DatabaseConnector(db_config)

    # 3. Conectar e extrair os dados
    print("\nConectando ao banco de dados para extração...")
    if not db.connect():
        print("Falha ao conectar ao banco de dados. Verifique suas credenciais.")
        sys.exit(1)

    try:
        # Extrai os dados diretamente para um DataFrame do Pandas
        df = pd.read_sql_query(sql_query, db.connection)
        print(f"✓ Dados extraídos com sucesso! ({len(df)} linhas retornadas)\n")
    except Exception as e:
        print(f"Erro ao executar a query: {e}")
        sys.exit(1)
    finally:
        db.disconnect()

    # 4. Preparação dos Dados para o Modelo Preditivo
    print("Iniciando processamento e modelagem (Média Móvel de 3 Meses)...")
    df['mes_venda'] = pd.to_datetime(df['mes_venda'])
    df = df.sort_values('mes_venda').set_index('mes_venda')

    # Criação do Baseline de acordo com as premissas do teste
    # O .shift(1) garante que prevemos o futuro usando estritamente o passado (Evita Data Leakage)
    df['previsao_baseline'] = df['quantidade_vendida'].rolling(window=3).mean().shift(1)

    # 5. Avaliação do Período de Teste (Primeiro Trimestre de 2026)
    teste = df['2026-01-01':'2026-03-31'].copy()
    
    # Remove eventuais nulos resultantes da janela deslizante e dados sem valor real
    teste_valido = teste.dropna(subset=['previsao_baseline', 'quantidade_vendida'])
    
    if teste_valido.empty:
        print("Aviso: Não há dados reais ou previstos suficientes no Q1 2026 para calcular o MAE.")
        return

    # Cálculo da métrica MAE
    mae = mean_absolute_error(teste_valido['quantidade_vendida'], teste_valido['previsao_baseline'])
    
    # Cálculo para a Questão 6.2 (Soma do Q1 2026)
    soma_previsao_q1 = round(teste_valido['previsao_baseline'].sum())

    # 6. Apresentação dos Resultados
    print("="*60)
    print("RESULTADOS DA PREVISÃO - BÚSSOLA DE BORDO 702 (Q1 2026)")
    print("="*60)
    print(f"Métrica de Erro (MAE): {mae:.2f} unidades")
    print(f"[Questão 6.2] Soma Total Prevista para Q1 2026: {soma_previsao_q1} unidades")
    print("="*60)
    
    print("\nDetalhamento Mensal do Q1 2026:")
    for data, row in teste_valido.iterrows():
        print(f" - {data.strftime('%Y-%m')}: Previsto = {row['previsao_baseline']:.1f} | Real = {row['quantidade_vendida']:.1f}")


if __name__ == "__main__":
    main()