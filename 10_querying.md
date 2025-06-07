## ⚠️ Avant de commencer, vérifier le statut de Hbase

# 1 - Préparation de l'environnement

### Dans vagrant ssh

```bash
# Installer les dépendances nécessaires

python3 -m pip install cx_Oracle
```

### Installation d'Oracle Instant Client

```bash
wget https://download.oracle.com/otn_software/linux/instantclient/2370000/instantclient-basic-linux.x64-23.7.0.25.01.zip

sudo mkdir -p /home/vagrant/opt/oracle

sudo unzip instantclient-basiclite-linux.x64-21.13.0.0.0dbru.zip -d /home/vagrant/opt/oracle

export ORACLE_HOME=/home/vagrant/opt/oracle/instantclient_23_7
export LD_LIBRARY_PATH=$ORACLE_HOME:$LD_LIBRARY_PATH
export PATH=$ORACLE_HOME:$PATH
source ~/.bashrc
```

# 2 - Connexion à Oracle (Dans un terminal spécifique)

```bash
sudo su oracle
sqlplus sys as sysdba

alter user sys identified by OracleWelcome1;
```

Encore dans sqlplus

```bash
STARTUP;
```

# 3 - Lancer le script

```bash
python3 query_test.py
```

```python
# liste des tables créées

MADAGASCAR_ROUTES
ACTIVE_AFRICAN_AIRLINES_ROUTES
AIRLINES_USING_BOEING
TOP_COUNTRIES_INCOMING_ROUTES
SYMMETRIC_ROUTES
AIRLINES_MOST_COUNTRIES
MOST_COMMON_ROUTES
AVG_PLANES_PER_ROUTE
INTERNATIONAL_ROUTES
MOST_USED_AIRPLANES
```
