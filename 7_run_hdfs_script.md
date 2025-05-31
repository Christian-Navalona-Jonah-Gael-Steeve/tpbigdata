## 1- Créer un dossier `/data/air_transport` dans le système de fichiers distribué HDFS.
```bash
hdfs dfs -mkdir -p /data/air_transport
```

## 2- Copier le fichier local `airplanes.csv` vers le dossier HDFS
```bash
hdfs dfs -put /home/vagrant/datasets/airplanes.csv /data/air_transport/
```

## 3- Le fichier est verifiable par la commande
```bash
hdfs dfs -ls /data/air_transport
```
