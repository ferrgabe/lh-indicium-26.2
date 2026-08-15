/*
==============================================================================
  Script: Questão 5 - Dimensão de Calendário e Média Real de Vendas
  Dialeto: PostgreSQL
  Descrição: Gera um calendário, cruza com vendas das lojas físicas (pos),
             trata dias sem vendas como 0 e calcula a média real por dia da semana.
==============================================================================
*/

-- cria um range de datas, da menor até a maior
WITH datas_limite AS (
    SELECT 
        MIN(placed_at::date) AS data_inicio,
        MAX(placed_at::date) AS data_fim
    FROM orders
),
-- gera a dimensão contínua de datas e traduz os dias da semana para Português
dim_calendario AS (
    SELECT 
        d::date AS data,
        EXTRACT(DOW FROM d) AS numero_dia_semana,
        CASE EXTRACT(DOW FROM d)
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terça-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sábado'
        END AS dia_semana
    FROM datas_limite,
    	-- a função generate series cria uma série com step de 1 dia, para cobrir dias sem vendas
         generate_series(data_inicio, data_fim, '1 day'::interval) AS d
),
-- agrupar a soma de vendas para lojas físicas (pos)
vendas_diarias_pos AS (
    SELECT 
        placed_at::date AS data,
        SUM(total) AS valor_venda
    FROM orders
    WHERE channel = 'pos'
    GROUP BY placed_at::date
),
-- left join para que dias sem vendas tenham valor 0
calendario_com_vendas AS (
    SELECT 
        c.data,
        c.numero_dia_semana,
        c.dia_semana,
        COALESCE(v.valor_venda, 0) AS valor_venda
    FROM dim_calendario c
    LEFT JOIN vendas_diarias_pos v ON c.data = v.data
)

-- agregação final por dia da semana
SELECT 
    dia_semana,
    ROUND(AVG(valor_venda), 2) AS media_vendas_diaria,
    ROUND(SUM(valor_venda), 2) AS faturamento_total,
    COUNT(data) AS quantidade_dias_no_periodo
FROM calendario_com_vendas
GROUP BY 
    numero_dia_semana, 
    dia_semana
ORDER BY 
    numero_dia_semana ASC;