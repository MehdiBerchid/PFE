import pyodbc
import csv

server_name = 'srvv-sias-dv'
db_name = 'DVPROCESS'
username = 'ext'
password = 'passwordExt'

# Set up the connection string
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server_name};'
    f'DATABASE={db_name};'
    f'UID={username};'
    f'PWD={password};'
    'Encrypt=yes;'
    'TrustServerCertificate=yes;'
    'Connection Timeout=30;'
)

# Connect to the database
conn = pyodbc.connect(conn_str)

# set up a cursor to execute SQL queries
cursor = conn.cursor()

# execute a SQL query to retrieve data
cursor.execute( """
SELECT
  CoefficientNuancePreset.CodeAcier,
  CoefficientNuancePreset.CodeNuance,
  CoefficientNuancePreset.TemperatureImmersion
FROM
  CoefficientNuancePreset
""" )

# fetch the data returned by the query
data = cursor.fetchall()

# save the data as a CSV file
with open('process_nuance.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

# close the cursor and connection
cursor.close()
conn.close()