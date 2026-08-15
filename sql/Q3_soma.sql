/*
==============================================================================
  Script: Contagem Total de Linhas (Múltiplas Tabelas)
  Dialeto: PostgreSQL
  Descrição: Retorna o somatório de linhas das tabelas principais.
==============================================================================
*/
SELECT 
    (SELECT COUNT(*) FROM customers) +
    (SELECT COUNT(*) FROM orders) +
    (SELECT COUNT(*) FROM order_items) +
    (SELECT COUNT(*) FROM payments) AS total_linhas_somadas;