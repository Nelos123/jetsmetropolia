import csv
import mysql.connector

conn = mysql.connector.connect(host='127.0.0.1', database='flight_game', user='root', password='', autocommit=True)
cur = conn.cursor()

# Luo country-taulu
cur.execute("DROP TABLE IF EXISTS airport")
cur.execute("DROP TABLE IF EXISTS country")

cur.execute("""
CREATE TABLE country (
    id INT PRIMARY KEY,
    iso_country VARCHAR(10),
    name VARCHAR(100),
    continent VARCHAR(10)
)""")

# Tuo countries.csv
with open('countries.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            cur.execute(
                "INSERT IGNORE INTO country (id, iso_country, name, continent) VALUES (%s, %s, %s, %s)",
                (int(row['id']), row['code'], row['name'], row['continent'])
            )
        except Exception:
            pass

print("Maat tuotu:", cur.rowcount)

# Luo airport-taulu
cur.execute("""
CREATE TABLE airport (
    id INT PRIMARY KEY,
    ident VARCHAR(20),
    type VARCHAR(50),
    name VARCHAR(200),
    latitude_deg FLOAT,
    longitude_deg FLOAT,
    continent VARCHAR(10),
    iso_country VARCHAR(10),
    municipality VARCHAR(100)
)""")

# airports.csv ei ole otsikkorivejä, sarakkeet:
# id, ident, type, name, lat, lng, elev, continent, iso_country, iso_region, municipality, ...
with open('airports.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    count = 0
    for row in reader:
        if len(row) < 9:
            continue
        try:
            cur.execute(
                "INSERT IGNORE INTO airport (id, ident, type, name, latitude_deg, longitude_deg, continent, iso_country, municipality) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    int(row[0]),
                    row[1],
                    row[2],
                    row[3],
                    float(row[4]) if row[4] else None,
                    float(row[5]) if row[5] else None,
                    row[7],
                    row[8],
                    row[10] if len(row) > 10 else None
                )
            )
            count += 1
        except Exception:
            pass

print(f"Lentokentät tuotu: {count}")

# Testaa kysely
cur.execute("""SELECT COUNT(*) FROM airport a JOIN country c ON a.iso_country = c.iso_country
WHERE a.continent = 'EU' AND a.iso_country != 'FI'
AND a.iso_country NOT IN ('FO','GI','GG','IM','JE')
AND a.type IN ('large_airport','medium_airport')""")
print("EU-kenttiä kannassa:", cur.fetchone()[0])

cur.close()
conn.close()
print("Valmis!")
