# Installation et d'exécution de CouchBase pour l'utilisateur Vagrant

## 🛠️ Installation de CouchBase

### 1. Télécharger et installer CouchBase pour Oracle Linux 8

Accédez au répertoire de l'utilisateur `vagrant` :

```bash
cd /home/vagrant
```

Téléchargez le package rpm de CouchBase :

```bash
wget https://packages.couchbase.com/releases/7.6.2/couchbase-server-community-7.6.2-linux.x86_64.rpm
```

Installer le package :

```bash
sudo dnf install -y couchbase-server-community-7.6.2-linux.x86_64.rpm
```

### 2. Configurer CouchBase

Configurer CouchBase pour rendre le web UI accessible  sur la machine host.
Ajouter la ligne ci-dessous dans le vagrant file :

```
config.vm.network :forwarded_port, guest: 8091, host: 10005
```
Accessible sur localhost:10005

---