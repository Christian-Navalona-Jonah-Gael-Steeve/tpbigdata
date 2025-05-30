import csv
import happybase

connection = happybase.Connection(host='localhost', port=9090)

if b'routes' not in connection.tables():
    connection.create_table('routes', {'cf1': dict()})

table = connection.table('routes')

with open('datasets/routes.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        key = row['index']
        data = {}

        for column, value in row.items():
            if column != 'index':
                data[f'cf1:{column}'.encode()] = value.encode()
        print(data)
        table.put(key, data)
    print("Data inserted successfully into HBase table 'routes'.")