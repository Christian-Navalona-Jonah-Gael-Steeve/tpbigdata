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

def count_routes_by_active_african_airlines():
    query = """
        SELECT
          ac.name AS airline_name,
          COUNT(*) AS nb_routes
        FROM routes_hbase r
        JOIN airports_mysql a ON r.Source_airport = a.iata
        JOIN airlines_couchbase ac ON r.Airline = ac.iata
        WHERE ac.active = 'Y'
          AND a.country IN (
            'Madagascar', 'Kenya', 'Nigeria', 'South Africa', 'Egypt', 'Algeria'
          )
        GROUP BY ac.name
        ORDER BY nb_routes DESC
        LIMIT 20
    """

    results = run_query(query)
    insert_into_oracle(
        results,
        'SYS.ACTIVE_AFRICAN_AIRLINES_ROUTES',
        ['Airline_name', 'Nb_routes'],
        [
            ('Airline_name', 'VARCHAR2(100)'),
            ('Nb_routes', 'NUMBER')
        ]
    )
    return results

def get_airlines_using_boeing():
    query = """
        SELECT DISTINCT ac.name AS airline_name, ap.name AS airplane_used
        FROM routes_hbase r
        JOIN airlines_couchbase ac ON r.Airline = ac.iata
        JOIN airplanes_hdfs ap ON LOCATE(ap.iata_code, r.Equipment) > 0
        WHERE ap.name LIKE '%Boeing%'
        LIMIT 30
    """
    results = run_query(query)
    insert_into_oracle(
        results,
        'SYS.AIRLINES_USING_BOEING',
        ['Airline_name', 'Airplane_used'],
        [
            ('Airline_name', 'VARCHAR2(100)'),
            ('Airplane_used', 'VARCHAR2(100)')
        ]
    )
    return results

def get_top_countries_by_incoming_routes():
    query = """
        SELECT
          a.country,
          COUNT(*) AS total_incoming_routes
        FROM routes_hbase r
        JOIN airports_mysql a ON r.Destination_airport = a.iata
        GROUP BY a.country
        ORDER BY total_incoming_routes DESC
        LIMIT 10
    """
    results = run_query(query)
    insert_into_oracle(
        results,
        'SYS.TOP_COUNTRIES_INCOMING_ROUTES',
        ['Country', 'Total_incoming_routes'],
        [
            ('Country', 'VARCHAR2(100)'),
            ('Total_incoming_routes', 'NUMBER')
        ]
    )
    return results

def get_symmetric_routes():
    query = """
        SELECT
          r1.Source_airport,
          r1.Destination_airport,
          r1.Airline
        FROM routes_hbase r1
        JOIN routes_hbase r2
          ON r1.Source_airport = r2.Destination_airport
          AND r1.Destination_airport = r2.Source_airport
          AND r1.Airline = r2.Airline
        WHERE r1.Source_airport < r1.Destination_airport
        LIMIT 20
    """
    results = run_query(query)
    insert_into_oracle(
        results,
        'SYS.SYMMETRIC_ROUTES',
        ['Source_airport', 'Destination_airport', 'Airline'],
        [
            ('Source_airport', 'VARCHAR2(10)'),
            ('Destination_airport', 'VARCHAR2(10)'),
            ('Airline', 'VARCHAR2(10)')
        ]
    )
    return results

#  6. Compagnies qui desservent le plus de pays différents
def get_airlines_serving_most_countries():
    query = """
        SELECT
            ac.name AS airline_name,
            COUNT(DISTINCT a.country) AS countries_served
        FROM routes_hbase r
        JOIN airports_mysql a ON r.Destination_airport = a.iata
        JOIN airlines_couchbase ac ON r.Airline = ac.iata
        GROUP BY ac.name
        ORDER BY countries_served DESC
        LIMIT 10
    """
    results = run_query(query)
    insert_into_oracle(
        results,
        'SYS.AIRLINES_MOST_COUNTRIES',
        ['Airline_name', 'Countries_served'],
        [
            ('Airline_name', 'VARCHAR2(100)'),
            ('Countries_served', 'NUMBER')
        ]
    )
    return results

#  7. Top 10 des routes les plus utilisées (par nombre de compagnies)
def get_most_common_routes():
    query = """
        SELECT
            r.Source_airport,
            r.Destination_airport,
            COUNT(DISTINCT r.Airline) AS airline_count
        FROM routes_hbase r
        GROUP BY r.Source_airport, r.Destination_airport
        ORDER BY airline_count DESC
        LIMIT 10
    """
    results = run_query(query)
    insert_into_oracle(
        results,
        'SYS.MOST_COMMON_ROUTES',
        ['Source_airport', 'Destination_airport', 'Airline_count'],
        [
            ('Source_airport', 'VARCHAR2(10)'),
            ('Destination_airport', 'VARCHAR2(10)'),
            ('Airline_count', 'NUMBER')
        ]
    )
    return results

# 8. Moyenne des avions utilisés par route (si plusieurs équipements)
def get_average_planes_per_route():
    query = """
        SELECT
            COUNT(DISTINCT ap.iata_code) * 1.0 / COUNT(DISTINCT r.Source_airport || '-' || r.Destination_airport) AS avg_planes_per_route
        FROM routes_hbase r
        JOIN airplanes_hdfs ap ON instr(r.Equipment, ap.iata_code) > 0
    """
    results = run_query(query)
    insert_into_oracle(
        results,
        'SYS.AVG_PLANES_PER_ROUTE',
        ['Avg_planes_per_route'],
        [
            ('Avg_planes_per_route', 'FLOAT')
        ]
    )
    return results

# 9. Routes internationales uniquement (source et destination ≠ pays)
def get_international_routes():
    query = """
        SELECT
            r.Source_airport,
            a1.country AS source_country,
            r.Destination_airport,
            a2.country AS destination_country,
            r.Airline
        FROM routes_hbase r
        JOIN airports_mysql a1 ON r.Source_airport = a1.iata
        JOIN airports_mysql a2 ON r.Destination_airport = a2.iata
        WHERE a1.country != a2.country
        LIMIT 50
    """
    results = run_query(query)
    insert_into_oracle(
        results,
        'SYS.INTERNATIONAL_ROUTES',
        ['Source_airport', 'Source_country', 'Destination_airport', 'Destination_country', 'Airline'],
        [
            ('Source_airport', 'VARCHAR2(10)'),
            ('Source_country', 'VARCHAR2(100)'),
            ('Destination_airport', 'VARCHAR2(10)'),
            ('Destination_country', 'VARCHAR2(100)'),
            ('Airline', 'VARCHAR2(10)')
        ]
    )
    return results

# 10. Liste des avions les plus utilisés avec leur nombre d’occurrences
def get_most_used_airplanes():
    query = """
        SELECT
            ap.name AS airplane_name,
            COUNT(*) AS usage_count
        FROM routes_hbase r
        JOIN airplanes_hdfs ap ON instr(r.Equipment, ap.iata_code) > 0
        GROUP BY ap.name
        ORDER BY usage_count DESC
        LIMIT 10
    """
    results = run_query(query)
    insert_into_oracle(
        results,
        'SYS.MOST_USED_AIRPLANES',
        ['Airplane_name', 'Usage_count'],
        [
            ('Airplane_name', 'VARCHAR2(100)'),
            ('Usage_count', 'NUMBER')
        ]
    )
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

print(get_routes_from_madagascar())