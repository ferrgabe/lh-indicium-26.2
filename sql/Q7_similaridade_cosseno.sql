/*
==============================================================================
  Script: Questão 7 - Extração para Recomendação (Similaridade de Cosseno)
  Dialeto: PostgreSQL
  Descrição: Extrai a relação única entre clientes e produtos comprados.
             Aplica regras de Data Quality para remover artefatos de teste
             e garante que apenas itens ativos sejam recomendados.
==============================================================================
*/
SELECT DISTINCT
    o.customer_id,
    p.name AS product_name
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN product_variants pv ON oi.product_variant_id = pv.id
JOIN products p ON pv.product_id = p.id
WHERE 
    p.is_active = TRUE  -- Regra de Negócio: Apenas produtos disponíveis
    AND p.name NOT IN (
        'asdf', 
        'Cliente Genérico', 
        'Genérico', 
        'João da Silva', 
        'NAO INFORMADO', 
        'TBD'
    ); -- Regra de Qualidade: Remoção de artefatos de ERP/Testes