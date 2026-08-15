/*
==============================================================================
  Questão 4 - Parte 3: Categoria Mais Consumida pelo Grupo Top 10
  Dialeto: PostgreSQL
==============================================================================
*/
WITH top10_elite AS (
    SELECT 
        o.customer_id
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN product_variants pv ON oi.product_variant_id = pv.id
    JOIN products p ON pv.product_id = p.id
    GROUP BY o.customer_id
    HAVING COUNT(DISTINCT p.category_id) >= 13
    ORDER BY 
        (SUM(DISTINCT o.total)::NUMERIC / COUNT(DISTINCT o.id)) DESC,
        o.customer_id ASC
    LIMIT 10
)
SELECT 
    p.category_id,
    c.name AS nome_categoria,
    SUM(oi.quantity) AS total_itens_comprados
FROM top10_elite e
JOIN orders o ON e.customer_id = o.customer_id
JOIN order_items oi ON o.id = oi.order_id
JOIN product_variants pv ON oi.product_variant_id = pv.id
JOIN products p ON pv.product_id = p.id
LEFT JOIN categories c ON p.category_id = c.id
GROUP BY 
    p.category_id,
    c.name
ORDER BY 
    total_itens_comprados DESC
LIMIT 1;