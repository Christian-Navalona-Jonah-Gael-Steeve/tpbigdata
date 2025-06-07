from pyhive import hive
import pandas as pd
import cx_Oracle

# Connexion à Hive
def get_hive_connection():
    return hive.Connection(host='localhost', port=10000, username='vagrant')

# Exécute une requête et retourne un DataFrame
def run_query(query):
    conn = get_hive_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    result = cursor.fetchall()
    return pd.DataFrame(result, columns=columns)

# ============ REQUÊTES SIMPLES ============

def get_all_airplanes():
    query = "SELECT * FROM airplanes_hdfs LIMIT 2"
    return run_query(query)
def get_all_routes():
    query = "SELECT * FROM routes_hbase LIMIT 2"
    return run_query(query)

def get_routes_from_madagascar():
    query = """
        SELECT
          r.Airline AS airline,
          ac.name AS airline_name,
          r.Source_airport AS source_airport,
          a1.city AS source_city,
          r.Destination_airport AS destination_airport,
          a2.city AS destination_city,
          ap.name AS airplane_name
        FROM routes_hbase r
        JOIN airports_mysql a1 ON source_airport = a1.iata
        JOIN airports_mysql a2 ON destination_airport = a2.iata
        LEFT JOIN airlines_couchbase ac ON airline = ac.iata
        LEFT JOIN airplanes_hdfs ap ON instr(r.Equipment, ap.iata_code) > 0
        WHERE a1.country = 'Madagascar'
        LIMIT 50
    """
    results = run_query(query)
    insert_into_oracle(results, 'SYS.MADAGASCAR_ROUTES', ['Airline', 'Airline_name', 'Source_airport', 'Source_city', 'Destination_airport', 'Destination_city', 'Airplane_name'],
                       [
                            ('Airline', 'VARCHAR2(10)'),
                            ('Airline_name', 'VARCHAR2(100)'),
                            ('Source_airport', 'VARCHAR2(10)'),
                            ('Source_city', 'VARCHAR2(100)'),
                            ('Destination_airport', 'VARCHAR2(10)'),
                            ('Destination_city', 'VARCHAR2(100)'),
                            ('Airplane_name', 'VARCHAR2(100)')
                        ])
    return results


def insert_into_oracle(df, table_name, defaultColumns, columns_types):
    print(df)
    df.columns = defaultColumns
    conn = cx_Oracle.connect("sys", "OracleWelcome1", "localhost:1521/ORCLCDB", mode=cx_Oracle.SYSDBA)
    cursor = conn.cursor()

    # Création dynamique de la table avec colonnes/types fournis
    col_defs = ', '.join([f"{col} {typ}" for col, typ in columns_types])
    create_sql = f"CREATE TABLE {table_name} ({col_defs})"
    try:
        cursor.execute(create_sql)
        print(f"Table {table_name} créée.")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        if error.code == 955:  # ORA-00955: name is already used by an existing object
            print(f"Table {table_name} existe déjà.")
        else:
            raise

    columns = df.columns.tolist()
    placeholders = ', '.join([f':{col}' for col in columns])
    insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
    print(insert_sql)
    for _, row in df.iterrows():
        print("Bind values:", row.to_dict())
        cursor.execute(insert_sql, row.to_dict())
    conn.commit()
    cursor.close()
    conn.close()

# def count_routes_by_active_african_airlines():
#     query = """
#         SELECT
#           ac.name AS airline_name,
#           COUNT(*) AS nb_routes
#         FROM routes_hbase r
#         JOIN airports_mysql a ON r.Source_airport = a.iata
#         JOIN airlines_couchbase ac ON r.Airline = ac.iata
#         WHERE ac.active = 'Y'
#           AND a.country IN (
#             'Madagascar', 'Kenya', 'Nigeria', 'South Africa', 'Egypt', 'Algeria'
#           )
#         GROUP BY ac.name
#         ORDER BY nb_routes DESC
#         LIMIT 20
#     """
#     return run_query(query)

# def get_airlines_using_boeing():
#     query = """
#         SELECT DISTINCT ac.name AS airline_name, ap.name AS airplane_used
#         FROM routes_hbase r
#         JOIN airlines_couchbase ac ON r.Airline = ac.iata
#         JOIN airplanes_hdfs ap ON LOCATE(ap.iata_code, r.Equipment) > 0
#         WHERE ap.name LIKE '%Boeing%'
#         LIMIT 30
#     """
#     return run_query(query)

# def get_top_countries_by_incoming_routes():
#     query = """
#         SELECT
#           a.country,
#           COUNT(*) AS total_incoming_routes
#         FROM routes_hbase r
#         JOIN airports_mysql a ON r.Destination_airport = a.iata
#         GROUP BY a.country
#         ORDER BY total_incoming_routes DESC
#         LIMIT 10
#     """
#     return run_query(query)

# def get_symmetric_routes():
#     query = """
#         SELECT
#           r1.Source_airport,
#           r1.Destination_airport,
#           r1.Airline
#         FROM routes_hbase r1
#         JOIN routes_hbase r2
#           ON r1.Source_airport = r2.Destination_airport
#           AND r1.Destination_airport = r2.Source_airport
#           AND r1.Airline = r2.Airline
#         WHERE r1.Source_airport < r1.Destination_airport
#         LIMIT 20
#     """
#     return run_query(query)


print("ROUTES à Madagascar :")
print(get_routes_from_madagascar())