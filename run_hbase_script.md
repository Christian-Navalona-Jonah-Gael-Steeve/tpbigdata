# 🗃️ Insertion de données dans HBase avec Python (HappyBase)

Ce projet permet d'insérer des données à partir d'un fichier CSV dans une base HBase en utilisant Python et la bibliothèque HappyBase.

---

## ✅ Prérequis

- HBase installé localement
- Hadoop (HDFS + YARN)
- Python 3.6+
- Pipenv ou virtualenv
- Fichier `routes.csv`

---

## 🛠️ Installation de l’environnement Python

```bash
python3 -m venv env
source env/bin/activate
pip install happybase thriftpy2
```

---

## 🚀 Lancement des services nécessaires

Assurez-vous de démarrer tous les services Hadoop & HBase avant de lancer le script : (Voir fichier hbase_install.md si nécessaire)

```bash
start-dfs.sh
start-yarn.sh
start-hbase.sh
```

## Démarrer le serveur Thrift (nécessaire pour HappyBase) :

Vérifier que les variables sont bien chargées:

```bash
export HBASE_HOME=/home/vagrant/hbase
export PATH=$HBASE_HOME/bin:$PATH
source ~/.bashrc
```

```bash
hbase thrift start
```

---

## 📝 Exemple de contenu du fichier `routes.csv`

```csv
id,name,distance
1,Route A,10.5
2,Route B,20.3
3,Route C,15.7
```

---

## 🐍 Lancement du script Python

```bash
python hbase_script.py
```

---

## 📜 Contenu du script `hbase_script.py`

```python
import csv
import happybase

# Connexion à HBase
connection = happybase.Connection(host='localhost', port=9090)

# Création de la table avec une famille de colonnes cf1 (si elle n'existe pas déjà)
if b'routes' not in connection.tables():
    connection.create_table('routes', {'cf1': dict()})

# Accès à la table
table = connection.table('routes')

# Lecture du fichier CSV
with open('datasets/routes.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        key = row['index']
        data = {}

        # Pour chaque colonne, insérer sous la forme cf1:<nom_colonne>
        for column, value in row.items():
            if column != 'index':  # 'index' est la clé primaire, donc on ne l'insère pas comme colonne
                data[f'cf1:{column}'.encode()] = value.encode()

        # Insertion dans HBase
        table.put(key, data)
```

---

## ✅ Résultat

Les données du fichier `routes.csv` sont insérées dans la table `routes` dans HBase, sous la famille de colonnes `cf1`.
