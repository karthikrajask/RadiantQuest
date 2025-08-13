


# #############################################################################
# IMPORTS
# #############################################################################

import psycopg2
import pandas as pd
from sqlalchemy import create_engine



# #############################################################################
# Conversion
# #############################################################################

# Create Database
conn = psycopg2.connect(database="postgres", user="postgres", password="password", host="localhost", port="5432")
conn.autocommit = True
cur = conn.cursor()
cur.execute("CREATE DATABASE mydb")
conn.close()

# Get Database Running
engine = create_engine('postgresql://postgres:password@localhost:5432/mydb')

# Project Explorer Data
df = pd.read_csv('../../data/data_processed.csv')
df.to_sql('project_overview', engine, if_exists='replace', index=False)

# Investment Navigator Data
df = pd.read_excel('../../data/data_processed/national_statistics.xlsx')
df.to_sql('national_data', engine, if_exists='replace', index=False)

# Tender Data
df = pd.read_csv('../../data/tender_processed.csv')
df.to_sql('tender_navigator', engine, if_exists='replace', index=False)