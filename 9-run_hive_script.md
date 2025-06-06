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
