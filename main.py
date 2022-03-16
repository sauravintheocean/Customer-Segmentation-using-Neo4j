from neo4j import GraphDatabase
import pandas as pd


graph = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j","jaisriram"))
session = graph.session()


#tx = graph.begin()

query = """
  MATCH (c:Customer)-[r1:MADE]->(t:Transaction)-[r2:CONTAINS]->(:Product)
  WITH SUM(r2.price) AS monetary,
     COUNT(DISTINCT t) AS frequency,
       c.customerID AS customer,
       MIN(
        duration.inDays(
        date(datetime({epochmillis: apoc.date.parse(t.transactionDate, 'ms', 'MM/dd/yyyy')})), 
        date()
      ).days
    ) AS recency
  RETURN customer, recency, frequency, monetary
"""

# create the dataframe
#results = tx.run(query).data()
results = session.run(query)
df = pd.DataFrame(results)
df.columns =['customer', 'recency', 'frequency', 'monetary']

# edit the recency value
df['recency'] = df['recency'] - df['recency'].min()

###############################################################################
# three quantiles to rfm values
df['r_val'] = pd.qcut(df['recency'], q=3, labels=range(3, 0, -1))
df['f_val'] = pd.qcut(df['frequency'], q=3, labels=range(1, 4))
df['m_val'] = pd.qcut(df['monetary'], q=3, labels=range(1, 4))

# create the segment value
df['rfm_val'] = (
    df['r_val'].astype(str) + 
    df['f_val'].astype(str) + 
    df['m_val'].astype(str)
)

# example names for segments
mapping = {
    'Best customers': '333',
    'No purchases recently': '133',
    'Low loyalty': '111',
    'New customers': '311'
}

# print the results
for k, v in mapping.items():
    print(k + ',')
    print(df[df.rfm_val == v].drop('customer', axis=1).describe().T)
    print()