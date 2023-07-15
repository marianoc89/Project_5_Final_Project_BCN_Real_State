import pandas as pd
import numpy as np
import pymysql
import sqlalchemy as alch
from getpass import getpass

#Creating a function that uploads df to SQL bcn_real_state Schema

def load_into_db (schema, table_name, df):
    """This function should: 
    1. Declare variables: password & connection string
    2. Establish the connection
    3. Run a create and a drop queries
    4. Insert table into schema
    5. Return some feedback: how many rows have been inserted. Retrieve the total rows from workbench
    and format it into a string.

    """
    #requesting pass
    password = getpass('Please enter pass here: ')
    #creating connection
    dbName = schema
    connectionData=f"mysql+pymysql://root:{password}@localhost/{dbName}"
    engine = alch.create_engine(connectionData)
    engine.execute(f'''DROP TABLE IF EXISTS {table_name}''')
    #sending df to sql
    df.to_sql(con=engine, name=table_name, if_exists='replace',  index=False)
    #feedback with # rows added
    feedback = f'MySQL table {table_name} created with {len(df)} rows inserted into.'
    #query to check table in mysql
    queried_df = pd.read_sql_query(f"""
                        SELECT *
                        FROM {table_name}
                        LIMIT 10;""", engine)
    return feedback