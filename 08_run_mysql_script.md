## 1- Utiliser le bon répertoire autorisé par secure_file_priv

Exécute cette commande dans le terminal (pas dans MySQL) :
```bash
mysql -u root -p -e "SHOW VARIABLES LIKE 'secure_file_priv';"
```
Elle retournera un chemin comme par exemple :
`/var/lib/mysql-files/`

## 2- Déplace ton fichier dans ce dossier :
Supposons que secure_file_priv = /var/lib/mysql-files/ :
```bash
sudo cp /home/vagrant/datasets/airports.csv /var/lib/mysql-files/
```
## 3- Connexion à MYSQL:
```bash
mysql -u root
```
## 4- Script MYSQL:
```SQL
CREATE DATABASE air_transport;
USE air_transport;

CREATE TABLE airports (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    iata VARCHAR(10),
    icao VARCHAR(10),
    latitude DOUBLE,
    longitude DOUBLE,
    altitude INT,
    timezone VARCHAR(10),
    dst VARCHAR(10),
    tz_database_time_zone VARCHAR(100),
    type VARCHAR(100),
    source VARCHAR(100)
);

LOAD DATA INFILE '/var/lib/mysql-files/airports.csv' 
INTO TABLE airports 
FIELDS TERMINATED BY ','
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS 
(@index,airport_id, name, city, country,iata,icao,latitude,longitude,altitude,timezone,dst,tz_database_time_zone,type,source);
```

## 4- Vérification
Dans mysql
```SQL
Select * from airports
```
retournera la liste des airports
