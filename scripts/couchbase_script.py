import csv
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator

cluster = Cluster('couchbase://localhost', ClusterOptions(
    PasswordAuthenticator('vagrant_user', 'vagrant_pwd')))
bucket = cluster.bucket('airlines')
collection = bucket.default_collection()

with open('/home/vagrant/datasets/airlines.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        key = row['index']
        collection.upsert(key, row)
