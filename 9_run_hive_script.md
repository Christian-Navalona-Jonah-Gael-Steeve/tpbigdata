## 1- Démarrer Hive

```bash
nohup hive --service metastore > hive_metastore.log 2>&1 &
nohup hiveserver2 > hive_server.log 2>&1 &
```

## 2- Se connecter à Hive

```bash
beeline -u jdbc:hive2://localhost:10000 vagrant
```

## 3- Créer des tables externes dans Hive

### 3-1 airports (mysql)

```sql
CREATE EXTERNAL TABLE airports_mysql (
  airport_id INT,
  name STRING,
  city STRING,
  country STRING,
  iata STRING,
  icao STRING,
  latitude DOUBLE,
  longitude DOUBLE,
  altitude INT,
  timezone STRING,
  dst STRING,
  tz_database_time_zone STRING,
  type STRING,
  source STRING
)
STORED BY 'org.apache.hive.storage.jdbc.JdbcStorageHandler'
TBLPROPERTIES (
  "hive.sql.database.type" = "MYSQL",
  "hive.sql.jdbc.driver" = "com.mysql.jdbc.Driver",
  "hive.sql.jdbc.url" = "jdbc:mysql://localhost:3306/air_transport",
  "hive.sql.dbcp.username" = "root",
  "hive.sql.dbcp.password" = "",
  "hive.sql.table" = "airports"
);
```

Vérification:

```sql
SELECT * FROM airports_mysql LIMIT 10;
```

### 3-2 routes (hbase)

```sql
CREATE EXTERNAL TABLE routes_hbase (
  index STRING,
  Airline STRING,
  Airline_ID STRING,
  Source_airport STRING,
  Source_airport_ID STRING,
  Destination_airport STRING,
  Destination_airport_ID STRING,
  Codeshare STRING,
  Stops INT,
  Equipment STRING
)
STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
WITH SERDEPROPERTIES (
  "hbase.columns.mapping" = ":key,cf1:Airline,cf1:Airline ID,cf1:Source airport,cf1:Source airport ID,cf1:Destination airport,cf1:Destination airport ID,cf1:Codeshare,cf1:Stops,cf1:Equipment"
)
TBLPROPERTIES (
  "hbase.table.name" = "routes"
);
```

Vérification:

```sql
SELECT * FROM routes_hbase LIMIT 10;
```

### 3-3 airplanes (hdfs)

```sql
CREATE EXTERNAL TABLE airplanes_hdfs (
    index INT,
    name STRING,
    iata_code STRING,
    icao_code STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/data/air_transport/airplanes'
TBLPROPERTIES ('skip.header.line.count'='1');
```

Vérification:

```sql
SELECT * FROM airplanes_hdfs ORDER BY INDEX DESC LIMIT 10;
```

## 4- Créer des tables internes dans Hive 
### airlines (couchbases)
Étape 1 : Télécharger et extraire le connecteur Couchbase-Spark

```bash
cd /vagrant/scripts
wget https://packages.couchbase.com/clients/connectors/spark/3.5.2/Couchbase-Spark-Connector_2.12-3.5.2.zip?_gl=1*190af9b*_gcl_au*OTE5MzA0MzY0LjE3NDkyMTQ0MjA.
unzip Couchbase-Spark-Connector_2.12-3.5.2.zip
```

Étape 2 : Créer la table Hive airlines_couchbase
Dans Beeline :

```sql
CREATE TABLE airlines_couchbase (
  airline_id INT,
  name STRING,
  alias STRING,
  iata STRING,
  icao STRING,
  callsign STRING,
  country STRING,
  active STRING
)
STORED AS PARQUET;

```
Étape 3 : Créer le script de synchronisation Couchbase → Hive
`/vagrant/scripts/hive_couchbase_script.py`
Ce script lit les données de Couchbase, les nettoie, filtre les doublons, et insère les nouvelles lignes dans Hive toutes les 60 secondes.

```py
from pyspark.sql import SparkSession
import time

# Création de la session Spark avec configuration pour Couchbase et Hive
spark = SparkSession.builder \
    .appName("CouchbaseToSpark_Hive_Streaming") \
    .config("spark.couchbase.connectionString", "couchbase://localhost") \
    .config("spark.couchbase.username", "vagrant_user") \
    .config("spark.couchbase.password", "vagrant_pwd") \
    .config("spark.sql.catalogImplementation", "hive") \
    .config("spark.hadoop.hive.metastore.uris", "thrift://localhost:9083") \
    .enableHiveSupport() \
    .getOrCreate()

def load_and_write():
    # Lecture des données depuis Couchbase
    df = spark.read.format("couchbase.query") \
        .option("bucket", "airlines") \
        .option("scope", "_default") \
        .option("collection", "_default") \
        .load()

    # Sélection et renommage
    df_clean = df.selectExpr(
        "`index` as index",
        "`Airline ID` as airline_id",
        "`Name` as name",
        "`Alias` as alias",
        "`IATA` as iata",
        "`ICAO` as icao",
        "`Callsign` as callsign",
        "`Country` as country",
        "`Active` as active"
    )

    # Lecture des index déjà insérés dans Hive
    try:
        df_hive = spark.table("airlines_hive").select("index")
    except:
        # Si la table Hive n'existe pas encore
        df_hive = spark.createDataFrame([], df_clean.schema)

    # Anti-join pour éviter les doublons
    df_new = df_clean.join(df_hive, on="index", how="left_anti")

    # Insère seulement les nouvelles lignes
    new_count = df_new.count()
    if new_count > 0:
        df_new.write.mode("append").insertInto("airlines_hive")
        print(f"✅ {new_count} nouvelles lignes insérées dans Hive.")
    else:
        print("⚠️ Aucune nouvelle ligne à insérer.")

try:
    # Boucle infinie pour charger et écrire les données toutes les 60 secondes
    while True:
        load_and_write()
        print("⏳ Pause de 60 secondes avant la prochaine lecture...")
        time.sleep(60)
except KeyboardInterrupt:
    print("🛑 Arrêt du script par l'utilisateur.")
finally:
    spark.stop()

```


Étape 4 : Lancer le script


```bash
spark-submit \
  --master local[*] \
  --jars /vagrant/scripts/spark-connector-assembly-3.5.2.jar \
  /vagrant/scripts/hive_couchbase_sript.py
```

Vérification :
Dans Beeline :

```sql
SELECT * FROM airlines_couchbase LIMIT 10;
```