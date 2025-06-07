# Import des données dans CouchBase

### 1. Installation des dépendances

Installer les librairies python :

-

```bash
python3 -m pip install --user couchbase
```

> Assurez-vous d'avoir au moins la version 4.0.0 du SDK Python de Couchbase

### 2. Création du clusted depuis Couchbase Web UI

Accéder à Couchbase Web UI:
`http://localhost:10005/`

Créer le cluster avec

- ClusterName: `airlines`
- UserName: `vagrant_user`
- Password: `vagrant_pwd`

Créer le bucket:

- Bucketname: `airlines`

### 3. Exécution du script

Importer le dossier `scripts` dans `/home/vagrant`

Exécuter le script

```bash
cd /home/vagrant/scripts
python3 couchbase_script.py
```

### 4. Vérification

Accéder à Couchbase Web UI:
`http://localhost:10005/`

Lancer la requête pour récupérer la liste des airlines

```sql
SELECT * FROM airlines;
```

NB: Créer un index

```sql
CREATE PRIMARY INDEX ON `airlines`;
```
