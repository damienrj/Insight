from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2


engine = create_engine('postgres://remote@localhost/data')
print engine.url

con = None
con = psycopg2.connect(database = 'data', user = 'remote', host='localhost')


query = """
SELECT * FROM recent WHERE "BusinessName" = '1000 Washington Cafe';
"""

query_results = pd.read_sql_query(query, engine)

print(query_results.shape)
