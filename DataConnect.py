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
  Coil.DateConsommation,
  Coil.Produit,
  Coil.Fournisseur,
  Coil.Nuance,
  Coil.CodeAcier,
  Bobine.CoilId,
  Segment.BobineId,
  Segment.BobinePhysId,
  Segment.Xpos,
  Segment.Absorptivite,
  Coil.Epaisseur,
  Coil.Largeur,
  Segment.ConsigneTemperatureLunetteCoin,
  Segment.CorrectionNuanceAppliquee,
  Segment.TemperatureLunCoin,
  Segment.ConsigneTemperatureBainAvant,
  Segment.ConsigneTemperatureBainArriere,
  Segment.TemperatureZincAV,
  Segment.TemperatureZincAR,
  Segment.TemperatureBainAlu,
  Segment.TendanceBain,
  Coil.THR,
  Segment.VitesseCentre
FROM
  Segment
  INNER JOIN Bobine ON Segment.BobineId = Bobine.Id
  INNER JOIN Coil ON Bobine.CoilId = Coil.Id
  INNER JOIN vw_MesureEct_Z5 ON vw_MesureEct_Z5.BobineId = Segment.BobineId
WHERE
  Coil.DateConsommation > '01/01/2022' AND
  vw_MesureEct_Z5.VIT_SCENT < 2.5 
ORDER BY
  Segment.BobineId DESC,
  Segment.Xpos;
""" )

# fetch the data returned by the query
data = cursor.fetchall()

# save the data as a CSV file
with open('data_process.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

# close the cursor and connection
cursor.close()
conn.close()