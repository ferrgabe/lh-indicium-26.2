/*
==============================================================================
  Script: Questão 6 - Criação de Dataset Unificado para Previsão de Demanda
  Dialeto: PostgreSQL
  Produto: Bússola de Bordo 702
  Granularidade: Mensal
==============================================================================
*/
SELECT 
    DATE_TRUNC('month', o.placed_at)::DATE AS mes_venda,
    SUM(oi.quantity) AS quantidade_vendida
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN product_variants pv ON oi.product_variant_id = pv.id
JOIN products p ON pv.product_id = p.id
WHERE 
    p.name = 'Bússola de Bordo 702'
    AND o.status IN ('paid', 'confirmed', 'completed')
GROUP BY 
    DATE_TRUNC('month', o.placed_at)
ORDER BY 
    mes_venda ASC;