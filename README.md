# Desafio Técnico Lighthouse Indicium 26.2 - LH Nauticals

Este repositório contém a resolução do teste técnico prático do Lighthouse 26.2 focado na estruturação, ingestão e modelagem de dados transacionais do e-commerce da LH Nautical.

---

## Estrutura do Repositório

O projeto foi organizado visando a clareza e a separação de responsabilidades:
- `data/`: Contém os arquivos `.csv` brutos.
- `sql/`: Arquivos e consultas SQL utilizadas no projeto.
- `script/`: Scripts Python modulares para geração de schema, ingestão no banco e modelagem preditiva.
- `error_logs/`: Logs de monitoramento gerados durante a ingestão de dados.

---

## Decisões Arquiteturais e Boas Práticas

Para garantir boas práticas, o pipeline foi desenhado de forma modular. Em vez de criar fluxos que dependem de exportações manuais de arquivos `.csv`, alguns dos scripts em Python de consomem a consulta de extração diretamente dos arquivos da pasta `sql/`. 

A classe de conexão ao PostgreSQL (`DatabaseConnector`), desenvolvida originalmente na etapa de ingestão de dados (`data_loader.py`), foi importada e reutilizada nos outros modelos preditivos, seguindo o princípio Dont Repeat Yourself (DRY). O DRY melhora a organização de código e facilita a manutenção a longo prazo.

---

### QUESTÃO 1 - EDA

#### 1.1 - Dados de EDA

1. Os dados abaixo foram obtidos através da execução da query `Q1_EDA` na pasta `sql/`

Quantidade total de linhas: 48998 registros
Quantidade total de colunas: 13 colunas
Intervalo de datas analisado (data mínima e máxima) da coluna created_at: 01/01/2020  01:19:28 até 31/12/2026  23:43:09

Para a coluna "total", calcule:

- Valor mínimo: 32,62
- Valor máximo: 127262,02
- Valor médio: 28704,99

#### 1.2 - Qual é o valor médio registrado na coluna "total"?
O valor médio da coluna total é 28704,99.

#### 1.3 - Um breve diagnóstico sobre a confiabilidade da tabela orders para análises futuras. Comentando sobre possíveis outliers e qualidade dos dados. 
Foi realizada inicialmente uma análise via z-score, porém o método foi descartado por ser inadequado pela natureza de distribuição assimétrica dos dados (cauda longa), com a média e o desvio-padrão inflacionados por valores extremos. Desta forma, optei pelo método não-paramétrico de Intervalo Interquartil (IQR), que identificou 5.212 registros (~10% da base) acima de R$ 54.830,00. Contudo, tratam-se de outliers de negócio legítimos (transações de alto valor) e não de erros no dataset. Para preservar a receita total, esses dados devem ser mantidos no dataset.
Sobre a qualidade dos dados, não foram identificados valores nulos ou inconsistências na base. Desta forma, o dataset está pronto para ingestão e análises posteriores. No entanto, para pipelines de BI e Machine Learning, pode ser necessário realizar uma marcação nas colunas outliers para identificar as transações de alto valor.

### QUESTÃO 2 - SCHEMA
Para gerar o schema, é necessário fazer a execução do código abaixo:
1. `python schema_generator.py ../data -o ../sql/schema.sql`

Esse código analisa os arquivos presentes na pasta passada como argumento (data/), e infere os tipos através de algumas técnicas, como expressões regulares, pool de booleans e atribuição para varchar quando não identifica nenhum padrão anterior. Depois, o código cria as instruções para o DDL do CREATE TABLE e gera o arquivo. Conforme as aulas do ciclo preparatório, esses arquivos vão compor a camada bronze, diante disso e da complexidade de código, optei por não incluir atribuição de FKs nesta etapa, embora na modelagem seja possível observar as relações entre tabelas.

### QUESTÃO 3 - PREVISÃO DE DEMANDA
O código python para esta tarefa pode ser executado através da pasta raiz com o comando:
1. `python script/data_loader.py data --password postgres`

Este código faz a conexão com o banco de dados, usa parâmetros padronizados e passa uma senha (para o banco que estou usando, é "postgres"). Depois cria o schema do banco com as colunas geradas na etapa anterior (do arquivo schema.sql). Para popular o banco, é realizada uma validação entre cabeçalho do arquivo x cabeçalho da tabela no banco. Caso ocorra algum erro na importação, a linha com erro é ignorada e é gerado um log de erro na pasta error_logs.

#### 3.2 Total de linhas somadas das tabelas: customers, orders, order_items e payments
Para chegar neste resultado, foi utilizada a query `Q3_soma.sql`, que faz um COUNT de cada tabela e depois soma tudo. O resultado obtido foi 251864.

### QUESTÃO 4 - ANÁLISE DE CLIENTES
Os resultados foram obtidos através da execução das querys:
1. `Q4.1_tkm_diversidade.sql` na pasta `sql/`
2. `Q4.2_top10_elite.sql` na pasta `sql/`
3. `Q4.3_consumo_top10.sql` na pasta `sql/`

#### 4.1.1 Ticket médio por cliente
A query `Q4.1_tkm_diversidade.sql` gera um relatório analítico informando o Ticket Médio e diversidade de produtos por cliente.

#### 4.1.2 A identificação dos 10 clientes "Fiéis" (maior Ticket Médio entre aqueles com diversidade >= 13 categorias).
Para identificar os top 10 cliente fiéis, foi executada a query `Q4.2_top10_elite.sql`. Para garantir o top 10, foi usado um ORDER BY pelo ticket médio combinado com um LIMIT 10. 

#### 4.2.1 Como obter as categorias mais vendidas? (mapeamento da cadeia de chaves)
Para identificar as categorias mais vendidas, a query `Q4.3_consumo_top10.sql` foi executada. Ela conecta cada item com sua categoria, realizando um cruzamento das tabelas/colunas:
orders.id > order_items.order_id > product_variants.product_variant_id > products.product_id > categories.category_id.
Em seguida, ao agrupar as linhas por category_id (e categories.name) e agregar SUM(oi.quantity), é possível obter a categoria de produto mais vendida entre os top 10 clientes. **O produto mais comprado foi category_id 8 - Hélices, com 492 vendas**

#### 4.2.2 Qual lógica foi utilizada para filtrar os clientes com diversidade mínima?
Calculei a diversidade de categorias contando o número de categorias únicas compradas por cliente: COUNT(DISTINCT products.category_id). Para filtrar por 13 ou mais categorias distintas, é preciso usar a cláusula HAVING COUNT(DISTINCT p.category_id) >= 13 dentro da agregação por customer_id. O uso de DISTINCT é obrigatório para garantir que compras repetidas de produtos numa mesma categoria não inflacionem a contagem.

#### 4.2.3 Como garantir que a contagem de itens refletisse apenas os Top 10?
A seleção dos clientes em ficou isolada em uma subconsulta (top10_elite), já aplicando o desempate (ticket_medio DESC, customer_id ASC) depois, apliquei LIMIT 10, para retornar somente os 10 clientes de maior ticket medio.
Na consulta final que contabiliza as vendas por categoria, existe um INNER JOIN entre a tabela de pedidos (orders) e essa subconsulta contendo apenas os 10 clientes. Esse INNER JOIN serve para como um "filtro", garantindo que a soma das quantidades (SUM(quantity)) considerasse só os itens de pedidos desse grupo.

### QUESTÃO 5 - DIMENSÃO DE CALENDÁRIO
Os resultados foram obtidos através da execução da query:
1. `Q5_calendario.sql` na pasta `sql/`

#### 5.1.1 Desenvolvimento de um calendário com os dias da semana (em portugues)
A consulta `Q5_calendario.sql` foi estruturada com subconsultas, vale destacar a subconsulta datas_limite, que define a data inicio e data fim na tabela orders. A partir dessas datas a sub dim_calendario efetivamente cria o calendário, com EXTRACT(DOW from d) atribuindo valores em português para seu equivalente numérico no SQL, e depois, através da função generate_series com parâmetro step 1, cria um registro por  entre a data inicio e data fim.

#### 5.1.2 LEFT JOIN entre o calendário e a tabela de vendas agregação de vendas por dia (soma de valor_venda), substituição de valores nulos por zero para dias sem vendas
Após montar a tabela vendas_diarias_pos agrupando por data, é realizada uma soma do valor total de vendas por dia. Na sequência, a partir de calendario_com_vendas é realizado um LEFT JOIN entre a dim_calendario e a vendas_diarias_pos, usando a data para fazer o relacionamento. O LEFT JOIN garante que todas as datas do calendário sejam mantidas, mesmo Se não houver vendas naquele dia. (executar sem left join puxaria somente dias com vendas). Para finalizar, a clausula COALESCE(v.valor_venda, 0) substitui os NULLs por 0, para garantir que ele será contabilizado em cálculos de média por exemplo.

#### 5.2.1 - Por que é necessário utilizar uma tabela de datas (calendário) em vez de agrupar diretamente a tabela de vendas?
A tabela orders só registra eventos de compra. Se a loja abrir em um domingo e não realizar vendas, essa data não gera um registro no banco de dados. Assim, não podemos agrupar diretamente a tabela de vendas porque o SQL contaria só os dias com vendas para calcular a média, o que é inconsistente e impactaria no resultado. O calendário garante que todos os dias passados entrem no cálculo da média.

#### 5.2.2 - O que aconteceria com a média de vendas se um dia da semana tivesse muitos dias sem nenhuma venda registrada?
Sem a tabela de dimensão de calendário a média seria maior, porque na conta de divisão, haveriam menos dias no divisor e esses dias de venda zero seriam ignorados no cálculo. Isso pode induzir a decisões erradas, visto que o valor verdadeiro é menor. Com o calendário, os dias sem venda entram na conta valendo 0, puxando a média para baixo e mostrando a performance real daquele dia.

### QUESTÃO 6 - PREVISÃO DE DEMANDA

Como executar o script de previsão de demanda:
1. Abra o terminal.
2. Navegue até a pasta `script` do projeto.
3. Execute o script passando a senha do seu usuário do banco de dados. Os demais parâmetros de conexão (host `localhost`, porta `5432`, database `postgres` e usuário `postgres`) já estão configurados por padrão, mas podem ser alterados via argumentos se necessário:

```bash
python previsao_baseline.py --password sua_senha_aqui
```

#### 6.3.1 - Como o baseline foi construído?

Utilizando uma média móvel simples de 3 períodos. A previsão de vendas para o mês atual é a média aritmética da quantidade vendida nos três meses anteriores (t-1, t-2, t-3). É um modelo mais simples, mas que pode revelar como as vendas se comportam (não foi o mais adequado para essa base de dados, dou mais detalhes no item 6.3.3).

#### 6.3.2 - Como evitou data leakage?
Para evitar que dados de fora do período desejado interferissem no treinamento, foi aplicada a função .shift(1) na lógica da média móvel no código. Com isso, previsão projetada para o mês de Janeiro de 2026 não enxerga nenhuma métrica de Janeiro em diante, utilizando somente dados reais dos últimos 3 meses de 2025.

#### 6.3.3 - Uma limitação do modelo proposto.
Umas das limitações desse método é que ele pressupõe que o resultado dos últimos 3 meses serão iguais aos próximos 3 meses. Do ponto de vista de análise de negócio, uma empresa que do ramo de vendas pode ter muita interferência de sazonalidade, como feriados, datas comemorativas e alterações no clima (por exemplo, mais vendas no verão). Um exemplo visível é o previsto x realizado, em 2026-01 a previsão foi de 38.7 vendas do produto, enquanto o real foi de 79, evidenciando o aumento de vendas por conta do verão. Neste cenário fictício, o estoque teria acabado muito antes do previsto, devido a uma má interpretação dos dados.

- [cite_start]🔗 **Script de Previsão:** [`script/previsao_baseline.py`](script/previsao_baseline.py) [cite: 535]
- [cite_start]🔗 **Consulta de Extração:** [`sql/Q6_previsao_demanda.sql`](sql/Q6_previsao_demanda.sql) [cite: 535]

### QUESTÃO 7 - SIMILARIDADE DE COSSENO

Durante a validação dos resultados do algoritmo, identifiquei que o produto com maior similaridade retornado inicialmente foi "asdf". Uma análise exploratória na tabela products revelou a existência de artefatos de cadastro (ex: "asdf", "TBD", "Cliente Genérico").

Conforme discutindo no ciclo preparatório, manter esses dados iria gerar um efeito "Garbage In, Garbage Out". Sendo assim, apliquei um tratamento diretamente na query de extração (Q7_Similaridade_cosseno.sql). Além de remover esses nomes corrompidos, adicionei a regra de negócio WHERE p.is_active = TRUE, para garantir que o motor de recomendação não tente sugerir um produto que já está desativado ou esgotado no catálogo.

Resultado da execução:
============================================================
RANKING DE RECOMENDAÇÃO: Motor de Popa 1949
============================================================
1. Motor de Popa 5331 (Similaridade: 0.2566)
2. Cabo Náutico 2105 (Similaridade: 0.2562)
3. Vela Mestra 1913 (Similaridade: 0.2558)
4. Defensa Náutica 3153 (Similaridade: 0.2529)
5. Sonar Transducer 7193 (Similaridade: 0.2475)

#### 7.2 - O produto com MAIOR similaridade é:
Motor de Popa 5331

#### 7.3.1 - Como a matriz foi construída?
A matriz de interação Usuário x Produto é uma tabela cruzada, então foi agrupado os ids únicos dos clientes (customer_id) nas linhas, os nomes dos produtos nas colunas e o cruzamento mostra a interação entre eles. Para focar apenas na presença/ausência da compra, as duplicatas foram removidas. Onde ocorreu a interseção de compra, é preenchido com o valor 1 e nas células onde o cliente nunca comprou aquele produto é preenchido com 0.

#### 7.3.2 - O que significa a similaridade de cosseno nesse contexto?
Similaridade de cosseno é um conceito de álgebra linear que representa o ângulo formado entre dois vetores (cos() = A.B/ |A||B|)
Ou seja, cada produto é representado por um vetor e as dimensões são os clientes. A similaridade de cosseno calcula a sobreposição dos clientes. Se dois produtos tem cosseno próximo a 1, significa que eles foram comprados quase que pelas exatas mesmas pessoas, ou seja, tem o mesmo comportamento. Com isso, podemos inferir nas recomendações ideais um para o outro cliente que tem o mesmo padrão de consumo.

#### 7.3.3 - Uma limitação desse método de recomendação.
Esse modelo está fortemente associado a dados históricos, desta forma, ao inserir um produto novo, seus vetores serão 0 e ele não será relacionado com nenhum outro produto (logo, também não será exibido na seleção recomendada). Esse modelo também pode sofrer interferência por vieses, por exemplo, caso um cliente compre um produto muito genérico que todos compram, esse produto terá alta similaridade e pode ser exibido em recomendações de vários produtos do catálogo.