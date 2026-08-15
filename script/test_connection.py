#!/usr/bin/env python3
"""
Script auxiliar para testar conexão e verificar configurações.
"""

import sys
try:
    import psycopg2
except ImportError:
    print("psycopg2 não encontrado. Execute: pip install psycopg2-binary")
    sys.exit(1)

def test_connection():
    """Testa a conexão com PostgreSQL e exibe informações do banco."""
    
    print("="*60)
    print("TESTE DE CONEXÃO POSTGRESQL")
    print("="*60)
    
    # Configurações
    config = {
        'host': input("Host [localhost]: ").strip() or 'localhost',
        'port': input("Porta [5432]: ").strip() or '5432',
        'database': input("Database [postgres]: ").strip() or 'postgres',
        'user': input("Usuário [postgres]: ").strip() or 'postgres',
        'password': input("Senha: [postgres]").strip() or 'postgres'
    }
    
    try:
        # Tenta conectar
        print(f"\nConectando a {config['host']}:{config['port']}...")
        
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password'],
            connect_timeout=10
        )
        
        print("✓ Conexão estabelecida com sucesso!\n")
        
        # Informações do servidor
        cur = conn.cursor()
        
        # Versão
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print(f"Versão: {version}")
        
        # Tamanho do banco
        cur.execute(f"SELECT pg_database_size('{config['database']}')/1024/1024 AS size_mb;")
        size = cur.fetchone()[0]
        print(f"Tamanho do banco: {size:.2f} MB")
        
        # Tabelas existentes
        cur.execute("""
            SELECT table_name, 
                   (SELECT count(*) FROM information_schema.columns WHERE table_name = t.table_name) as columns
            FROM information_schema.tables t
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = cur.fetchall()
        
        if tables:
            print(f"\nTabelas existentes ({len(tables)}):")
            for table, col_count in tables:
                print(f"  - {table} ({col_count} colunas)")
        else:
            print("\nNenhuma tabela encontrada no schema public.")
        
        cur.close()
        conn.close()
        
        print("\n✓ Teste concluído com sucesso!")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n✗ Erro de conexão: {e}")
        print("\nVerifique:")
        print("1. Se o PostgreSQL está rodando")
        print("2. Se host/porta estão corretos")
        print("3. Se usuário/senha estão corretos")
        print("4. Se o firewall permite a conexão")
        return False
        
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        return False


if __name__ == "__main__":
    test_connection()