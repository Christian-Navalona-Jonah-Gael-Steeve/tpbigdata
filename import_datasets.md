# Importer les datasets sur la VM

### 1. Monter le dossier /vagrant avec les datasets

Accédez au répertoire source `...\3_MV_BIGDATA_NEW\1INSTALL_MV_BIGDATA_BOX`
- Créez-y un dossier `datasets`
- Rajouter les fichiers csv (datasets) dedans

Lorsqu'on lance `vagrant up`, le dossier `datasets` sera aussi monté dans `vagrant`
Pour vérfier:

```bash
ls /vagrant/datasets
```

### 2. Copier les datasets sur la VM

Copier ce dossier vers le répertoir de l'utilisateur vagrant `/home/vagrant`

```bash
cd /home/vagrant
cp -r /vagrant/datasets .
```

Vérifier
```bash
ls /home/vagrant/datasets
```
