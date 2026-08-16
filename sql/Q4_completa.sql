/*
==============================================================================
  Questão 4 - Análise de Clientes (Arquivo Unificado)
  Dialeto: PostgreSQL
  Descrição: Solução completa calculando Ticket Médio, Diversidade de Categorias,
             identificação do Top 10 VIP e a categoria mais consumida pelo grupo.
==============================================================================
*/

/*
------------------------------------------------------------------------------
  Questão 4.1: Ticket Médio, Diversidade e Filtro dos 10 Clientes "Fiéis"
  (Retorna os 10 clientes de elite com diversidade >= 13)
------------------------------------------------------------------------------
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
    ROUND(co.ticket_medio, 2) AS ticket_medio,
    cc.diversidade_categorias,
    co.faturamento_total,
    co.frequencia
FROM customer_orders co
JOIN customer_categories cc ON co.customer_id = cc.customer_id
WHERE cc.diversidade_categorias >= 13
ORDER BY 
    co.ticket_medio DESC,
    co.customer_id ASC
LIMIT 10;


/*
------------------------------------------------------------------------------
  Questão 4 (Complemento): Categoria Mais Consumida pelo Grupo Top 10
------------------------------------------------------------------------------
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