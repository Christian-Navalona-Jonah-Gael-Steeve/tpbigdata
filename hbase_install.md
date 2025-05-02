# Installation et d'exécution de HBase pour l'utilisateur Vagrant

## 🛠️ Installation de HBase

### 1. Télécharger et extraire les binaires de HBase pour Hadoop 3

Accédez au répertoire personnel de l'utilisateur `vagrant` :

```bash
cd /home/vagrant
```

Téléchargez la version stable de HBase 2.5.11 :

```bash
wget https://dlcdn.apache.org/hbase/2.5.11/hbase-2.5.11-hadoop3-bin.tar.gz
```

Extrayez l’archive téléchargée :

```bash
tar -xzf hbase-2.5.11-hadoop3-bin.tar.gz
```

Renommez le dossier extrait pour plus de clarté :

```bash
mv hbase-2.5.11-hadoop3-bin /home/vagrant/hbase
```

### 2. Configurer HBase

Accédez au répertoire de configuration :

```bash
cd /home/vagrant/hbase/conf
```

#### Modifier le fichier `hbase-env.sh` pour définir JAVA_HOME

```bash
nano hbase-env.sh
```

Ajoutez la ligne suivante :

```bash
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
```

#### Modifier le fichier `hbase-site.xml` :

```bash
nano hbase-site.xml
```

Remplacer le contenu par :

```xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--
/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
-->
<configuration>
	<!--
    The following properties are set for running HBase as a single process on a
    developer workstation. With this configuration, HBase is running in
    "stand-alone" mode and without a distributed file system. In this mode, and
    without further configuration, HBase and ZooKeeper data are stored on the
    local filesystem, in a path under the value configured for `hbase.tmp.dir`.
    This value is overridden from its default value of `/tmp` because many
    systems clean `/tmp` on a regular basis. Instead, it points to a path within
    this HBase installation directory.

    Running against the `LocalFileSystem`, as opposed to a distributed
    filesystem, runs the risk of data integrity issues and data loss. Normally
    HBase will refuse to run in such an environment. Setting
    `hbase.unsafe.stream.capability.enforce` to `false` overrides this behavior,
    permitting operation. This configuration is for the developer workstation
    only and __should not be used in production!__
        See also https://hbase.apache.org/book.html#standalone_dist
  -->
  
  <!-- Enable distributed mode -->
  <property>
    <name>hbase.cluster.distributed</name>
    <value>true</value>
  </property>

  <!-- Directory where HBase stores data in HDFS -->
  <property>
    <name>hbase.rootdir</name>
    <value>hdfs://localhost:9000/hbase</value>
  </property>

  <!-- ZooKeeper quorum (localhost for single-node setup) -->
  <property>
    <name>hbase.zookeeper.quorum</name>
    <value>localhost</value>
  </property>

  <property>
    <name>hbase.zookeeper.property.dataDir</name>
    <value>/home/vagrant/zookeeper</value>
  </property>

  <!-- HBase temp dir (used for writing files before moving to HDFS) -->
  <property>
    <name>hbase.tmp.dir</name>
    <value>/home/vagrant/hbase-tmp</value>
  </property>

  <!-- Allow running on local filesystem without HDFS checks (optional but useful for dev) -->
  <property>
    <name>hbase.unsafe.stream.capability.enforce</name>
    <value>false</value>
  </property>

</configuration>
```

### 3. Créer les répertoires nécessaires

#### Créer le répertoire ZooKeeper

```bash
mkdir -p /home/vagrant/zookeeper
chown -R vagrant:vagrant /home/vagrant/zookeeper
```

💡  ZooKeeper est utilisé par HBase pour la coordination des services distribués. Ce répertoire est utilisé pour stocker ses données.

#### Créer le répertoire temporaire HBase

```bash
mkdir -p /home/vagrant/hbase-tmp
chown -R vagrant:vagrant /home/vagrant/hbase-tmp
```

💡  Ce répertoire temporaire est utilisé pour stocker temporairement des fichiers avant leur déplacement vers HDFS.

### 4. Définir les serveurs de régions

```bash
echo "localhost" > regionservers
```

💡  Indique à HBase que le serveur de régions (RegionServer) tourne en local.

### 5. Démarrer Hadoop et YARN

```bash
start-dfs.sh
start-yarn.sh
```

💡  HDFS doit être démarré avant HBase car HBase stocke ses données sur HDFS.

### 6. Créer le répertoire HBase dans HDFS

```bash
hdfs dfs -mkdir -p /hbase
hdfs dfs -chown vagrant:vagrant /hbase
```

💡  C’est le répertoire principal où HBase va stocker ses données dans HDFS.

### 7. Ajouter les variables d’environnement

```bash
echo 'export HBASE_HOME=/home/vagrant/hbase' >> ~/.bashrc
echo 'export PATH=$HBASE_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

💡  Cela permet d'accéder facilement aux commandes `hbase` depuis n'importe quel terminal.

---

## ▶️ Exécution de HBase et de son Shell

### 1. S'assurer que les variables d’environnement sont chargées

```bash
echo 'export HBASE_HOME=/home/vagrant/hbase' >> ~/.bashrc
echo 'export PATH=$HBASE_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### 2. Démarrer Hadoop et YARN (si ce n’est pas encore fait)

```bash
start-dfs.sh
start-yarn.sh
```

### 3. Démarrer HBase

```bash
start-hbase.sh
```

### 4. Lancer le shell HBase

```bash
hbase shell
```

### 5. Vérifier le statut

```bash
status
```

---