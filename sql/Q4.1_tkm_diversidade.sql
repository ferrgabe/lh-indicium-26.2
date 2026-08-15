/*
==============================================================================
  Questão 4 - Parte 1: Ticket Médio e Diversidade por Cliente
  Dialeto: PostgreSQL
==============================================================================
*/
WITH customer_orders AS (
    SELECT 
        customer_id,
        COUNT(id) AS frequencia,
        SUM(total) AS faturamento_total,
        SUM(total)::NUMERIC / COUNT(id) AS ticket_medio
    FROM orders
    GROUP BY customer_id
),
customer_categories AS (
    SELECT 
        o.customer_id,
        COUNT(DISTINCT p.category_id) AS diversidade_categorias
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN product_variants pv ON oi.product_variant_id = pv.id
    JOIN products p ON pv.product_id = p.id
    GROUP BY o.customer_id
)
SELECT 
    co.customer_id,
    co.faturamento_total,
    co.frequencia,
    ROUND(co.ticket_medio, 2) AS ticket_medio,
    cc.diversidade_categorias
FROM customer_orders co
JOIN customer_categories cc ON co.customer_id = cc.customer_id
ORDER BY co.customer_id ASC;