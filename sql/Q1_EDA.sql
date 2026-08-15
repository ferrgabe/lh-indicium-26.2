/*
==============================================================================
  Script: Resumo Estatístico e Temporal do Dataset "orders"
  Dialeto: PostgreSQL
  Descrição: Retorna contagem de linhas, range de datas e métricas do valor total
==============================================================================
*/

SELECT 
    COUNT(*) AS total_linhas,
    MIN(DATE(created_at)) AS data_inicio,
    MAX(DATE(created_at)) AS data_fim,
    MIN(total) AS valor_minimo,
    MAX(total) AS valor_maximo,
    ROUND(AVG(total), 2) AS valor_medio
FROM 
    orders;