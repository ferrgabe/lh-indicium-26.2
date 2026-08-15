#!/usr/bin/env python3
"""
Motor de Recomendação - LH Nautical
Baseado em Similaridade de Cosseno (Item-Based Collaborative Filtering)
Conecta ao PostgreSQL, lê a query estruturada e calcula a proximidade dos produtos.
"""

import sys
import argparse
import pandas as pd
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
import warnings

# Suprime os avisos do pandas
warnings.filterwarnings('ignore', category=UserWarning)

# Importa o DatabaseConnector do seu script data_loader.py
try:
    from data_loader import DatabaseConnector
except ImportError:
    print("Erro: Não foi possível importar DatabaseConnector de data_loader.py.")
    print("Certifique-se de que ambos estão na pasta 'script'.")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Motor de Recomendação Vitrine')
    parser.add_argument('--host', default='localhost', help='Host do PostgreSQL')
    parser.add_argument('--port', type=int, default=5432, help='Porta')
    parser.add_argument('--database', default='postgres', help='Database')
    parser.add_argument('--user', default='postgres', help='Usuário')
    parser.add_argument('--password', default='postgres', help='Senha')
    args = parser.parse_args()

    # 1. Configurar caminho para ler o arquivo SQL
    root_dir = Path(__file__).resolve().parent.parent
    sql_file_path = root_dir / 'sql' / 'Q7_similaridade_cosseno.sql'

    if not sql_file_path.exists():
        print(f"Erro: Arquivo SQL não encontrado em: {sql_file_path}")
        sys.exit(1)

    print(f"Lendo query SQL de: {sql_file_path}")
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_query = f.read()

    # 2. Conectar ao banco e extrair dados
    db_config = {
        'host': args.host,
        'port': args.port,
        'database': args.database,
        'user': args.user,
        'password': args.password
    }
    
    db = DatabaseConnector(db_config)
    print("\nConectando ao banco de dados...")
    
    if not db.connect():
        print("Falha ao conectar ao banco de dados. Verifique suas credenciais.")
        sys.exit(1)
        
    try:
        df = pd.read_sql_query(sql_query, db.connection)
        print(f"✓ Dados extraídos! ({len(df)} interações únicas cliente-produto)\n")
    except Exception as e:
        print(f"Erro ao executar a query: {e}")
        sys.exit(1)
    finally:
        db.disconnect()
    
    # 3. Construção da Matriz Usuário x Produto
    print("Construindo a Matriz Usuário x Produto...")
    
    # A query já traz DISTINCT, mas garantimos a ausência de duplicatas locais
    df_unique = df.drop_duplicates(subset=['customer_id', 'product_name']).copy()
    df_unique['comprou'] = 1
    
    # Cria a matriz pivotada (Linhas: Clientes | Colunas: Produtos | Valores: 1 ou 0)
    matriz_user_item = df_unique.pivot(
        index='customer_id', 
        columns='product_name', 
        values='comprou'
    ).fillna(0)
    
    # 4. Cálculo de Similaridade de Cosseno (Produto x Produto)
    print("Calculando a Similaridade de Cosseno entre produtos...")
    
    # Transpomos a matriz (.T) para Produto (linhas) x Clientes (colunas)
    matriz_item_user = matriz_user_item.T
    
    matriz_similaridade = cosine_similarity(matriz_item_user)
    
    df_sim = pd.DataFrame(
        matriz_similaridade, 
        index=matriz_item_user.index, 
        columns=matriz_item_user.index
    )
    
    # 5. Ranking de Recomendação
    produto_alvo = "Motor de Popa 1949"
    
    if produto_alvo not in df_sim.columns:
        print(f"Erro: O produto '{produto_alvo}' não foi encontrado na base.")
        return
    
    # Isola o alvo, dropa ele mesmo (score 1.0) e ordena decrescente
    ranking = df_sim[produto_alvo].drop(produto_alvo).sort_values(ascending=False)
    
    print("\n" + "="*60)
    print(f"RANKING DE RECOMENDAÇÃO: {produto_alvo}")
    print("="*60)
    
    top_5 = ranking.head(5)
    for i, (produto, score) in enumerate(top_5.items(), 1):
        print(f"{i}. {produto} (Similaridade: {score:.4f})")
    
    print("\n[Resposta Questão 7.2] O produto com MAIOR similaridade é:")
    print(f"-> {top_5.index[0]}\n")

if __name__ == "__main__":
    main()