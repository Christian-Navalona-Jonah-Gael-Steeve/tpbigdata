-- 1. 🔍 Trouver toutes les routes partant d’un aéroport de Madagascar, avec nom de la compagnie et du type d’avion

SELECT
  r.Airline,
  ac.name AS airline_name,
  r.Source_airport,
  a1.city AS source_city,
  r.Destination_airport,
  a2.city AS destination_city,
  ap.name AS airplane_name
FROM routes_hbase r
JOIN airports_mysql a1 ON r.Source_airport = a1.iata
JOIN airports_mysql a2 ON r.Destination_airport = a2.iata
LEFT JOIN airlines_couchbase ac ON r.Airline = ac.iata
LEFT JOIN airplanes_hdfs ap ON instr(r.Equipment, ap.iata_code) > 0
WHERE a1.country = 'Madagascar'
LIMIT 50;

-- 2. 📊 Nombre de routes par compagnie active opérant depuis l’Afrique
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
LIMIT 20;

-- 3. ✈️ Lister les compagnies aériennes utilisant au moins un avion "Boeing"

SELECT DISTINCT ac.name AS airline_name, ap.name AS airplane_used
FROM routes_hbase r
JOIN airlines_couchbase ac ON r.Airline = ac.iata
JOIN airplanes_hdfs ap ON instr(r.Equipment, ap.iata_code) > 0
WHERE ap.name LIKE '%Boeing%'
LIMIT 30;

-- 4. 🌍 Top 10 des pays avec le plus de routes entrantes
SELECT
  a.country,
  COUNT(*) AS total_incoming_routes
FROM routes_hbase r
JOIN airports_mysql a ON r.Destination_airport = a.iata
GROUP BY a.country
ORDER BY total_incoming_routes DESC
LIMIT 10;

-- 5. 🔁 Routes aller-retour entre deux mêmes aéroports (symétriques)
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
LIMIT 20;

-- 6. 🏆 Compagnies qui desservent le plus de pays différents
SELECT
  ac.name AS airline_name,
  COUNT(DISTINCT a.country) AS countries_served
FROM routes_hbase r
JOIN airports_mysql a ON r.Destination_airport = a.iata
JOIN airlines_couchbase ac ON r.Airline = ac.iata
GROUP BY ac.name
ORDER BY countries_served DESC
LIMIT 10;

-- 7. 🔝 Top 10 des routes les plus utilisées (par nombre de compagnies)
SELECT
  r.Source_airport,
  r.Destination_airport,
  COUNT(DISTINCT r.Airline) AS airline_count
FROM routes_hbase r
GROUP BY r.Source_airport, r.Destination_airport
ORDER BY airline_count DESC
LIMIT 10;

-- 8. 📈 Moyenne des avions utilisés par route (si plusieurs équipements)
SELECT
  COUNT(DISTINCT ap.iata_code) * 1.0 / COUNT(DISTINCT r.Source_airport || '-' || r.Destination_airport) AS avg_planes_per_route
FROM routes_hbase r
JOIN airplanes_hdfs ap ON instr(r.Equipment, ap.iata_code) > 0;

-- 9. 🌐 Routes internationales uniquement (source et destination ≠ pays)
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
LIMIT 50;

-- 10. ✈️ Liste des avions les plus utilisés avec leur nombre d’occurrences
SELECT
  ap.name AS airplane_name,
  COUNT(*) AS usage_count
FROM routes_hbase r
JOIN airplanes_hdfs ap ON instr(r.Equipment, ap.iata_code) > 0
GROUP BY ap.name
ORDER BY usage_count DESC
LIMIT 10;
