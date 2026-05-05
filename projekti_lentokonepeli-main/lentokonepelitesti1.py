import random
import mysql.connector
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Flask-sovelluksen alustus
sovellus = Flask(__name__)
sovellus.secret_key = 'lol'
CORS(sovellus)

# Yhdistää tietokantaan
def hae_tietokanta():
    return mysql.connector.connect(host='127.0.0.1', database='flight_game', user='root', password='', autocommit=True)

# Vihjeet eri maista
MAA_VIHJEET = {'Albania': {'väkiluku': '2,8 miljoonaa', 'pääkaupunki': 'Tirana', 'lippu': 'punainen, musta'}, 'Austria': {'väkiluku': '9 miljoonaa', 'pääkaupunki': 'Wien', 'lippu': 'punainen, valkoinen'},
                'Belarus': {'väkiluku': '9,4 miljoonaa', 'pääkaupunki': 'Minsk', 'lippu': 'punainen, vihreä, valkoinen'}, 'Belgium': {'väkiluku': '11,5 miljoonaa', 'pääkaupunki': 'Bryssel', 'lippu': 'musta, keltainen, punainen'},
                 'Bosnia and Herzegovina': {'väkiluku': '3,3 miljoonaa', 'pääkaupunki': 'Sarajevo', 'lippu': 'sininen, keltainen, valkoinen'},
                  'Bulgaria': {'väkiluku': '6,8 miljoonaa', 'pääkaupunki': 'Sofia', 'lippu': 'valkoinen, vihreä, punainen'}, 'Croatia': {'väkiluku': '4 miljoonaa', 'pääkaupunki': 'Zagreb', 'lippu': 'punainen, valkoinen, sininen'},
                    'Czech Republic': {'väkiluku': '10,7 miljoonaa', 'pääkaupunki': 'Praha', 'lippu': 'valkoinen, punainen, sininen'}, 'Denmark': {'väkiluku': '5,8 miljoonaa', 'pääkaupunki': 'Kööpenhamina', 'lippu': 'punainen, valkoinen'},
                      'Estonia': {'väkiluku': '1,3 miljoonaa', 'pääkaupunki': 'Tallinna', 'lippu': 'sininen, musta, valkoinen'}, 'France': {'väkiluku': '67 miljoonaa', 'pääkaupunki': 'Pariisi', 'lippu': 'sininen, valkoinen, punainen'},
                        'Germany': {'väkiluku': '83 miljoonaa', 'pääkaupunki': 'Berliini', 'lippu': 'musta, punainen, keltainen'}, 'Greece': {'väkiluku': '10,7 miljoonaa', 'pääkaupunki': 'Ateena', 'lippu': 'sininen, valkoinen'},
                          'Hungary': {'väkiluku': '9,7 miljoonaa', 'pääkaupunki': 'Budapest', 'lippu': 'punainen, valkoinen, vihreä'}, 'Iceland': {'väkiluku': '364 000', 'pääkaupunki': 'Reykjavik', 'lippu': 'sininen, valkoinen, punainen'},
                            'Ireland': {'väkiluku': '5 miljoonaa', 'pääkaupunki': 'Dublin', 'lippu': 'vihreä, valkoinen, oranssi'}, 'Italy': {'väkiluku': '60 miljoonaa', 'pääkaupunki': 'Rooma', 'lippu': 'vihreä, valkoinen, punainen'},
                              'Kosovo': {'väkiluku': '1,9 miljoonaa', 'pääkaupunki': 'Pristina', 'lippu': 'sininen, keltainen, valkoinen'}, 'Latvia': {'väkiluku': '1,9 miljoonaa', 'pääkaupunki': 'Riika', 'lippu': 'kastanjanruskea, valkoinen'},
                                'Lithuania': {'väkiluku': '2,8 miljoonaa', 'pääkaupunki': 'Vilna', 'lippu': 'keltainen, vihreä, punainen'}, 'Luxembourg': {'väkiluku': '632 000', 'pääkaupunki': 'Luxemburg', 'lippu': 'punainen, valkoinen, vaaleansininen'},
                                  'Malta': {'väkiluku': '514 000', 'pääkaupunki': 'Valletta', 'lippu': 'valkoinen, punainen'}, 'Moldova': {'väkiluku': '2,6 miljoonaa', 'pääkaupunki': 'Chisinau', 'lippu': 'sininen, keltainen, punainen'},
                                    'Montenegro': {'väkiluku': '621 000', 'pääkaupunki': 'Podgorica', 'lippu': 'punainen, kulta'}, 'Netherlands': {'väkiluku': '17,4 miljoonaa', 'pääkaupunki': 'Amsterdam', 'lippu': 'punainen, valkoinen, sininen'}, 
                                    'North Macedonia': {'väkiluku': '2,1 miljoonaa', 'pääkaupunki': 'Skopje', 'lippu': 'punainen, keltainen'}, 'Norway': {'väkiluku': '5,4 miljoonaa', 'pääkaupunki': 'Oslo', 'lippu': 'punainen, valkoinen, sininen'}, 
                                    'Poland': {'väkiluku': '37,8 miljoonaa', 'pääkaupunki': 'Varsova', 'lippu': 'valkoinen, punainen'}, 'Portugal': {'väkiluku': '10,3 miljoonaa', 'pääkaupunki': 'Lissabon', 'lippu': 'vihreä, punainen'}, 
                                    'Romania': {'väkiluku': '19,2 miljoonaa', 'pääkaupunki': 'Bukarest', 'lippu': 'sininen, keltainen, punainen'}, 'Russia': {'väkiluku': '144 miljoonaa', 'pääkaupunki': 'Moskova', 'lippu': 'valkoinen, sininen, punainen'}, 
                                    'Serbia': {'väkiluku': '6,8 miljoonaa', 'pääkaupunki': 'Belgrad', 'lippu': 'punainen, sininen, valkoinen'}, 'Slovakia': {'väkiluku': '5,5 miljoonaa', 'pääkaupunki': 'Bratislava', 'lippu': 'valkoinen, sininen, punainen'}, 
                                    'Slovenia': {'väkiluku': '2,1 miljoonaa', 'pääkaupunki': 'Ljubljana', 'lippu': 'valkoinen, sininen, punainen'}, 'Spain': {'väkiluku': '47,4 miljoonaa', 'pääkaupunki': 'Madrid', 'lippu': 'punainen, keltainen'}, 
                                    'Sweden': {'väkiluku': '10,4 miljoonaa', 'pääkaupunki': 'Tukholma', 'lippu': 'sininen, keltainen'}, 'Switzerland': {'väkiluku': '8,7 miljoonaa', 'pääkaupunki': 'Bern', 'lippu': 'punainen, valkoinen'}, 
                                    'Turkey': {'väkiluku': '84,3 miljoonaa', 'pääkaupunki': 'Ankara', 'lippu': 'punainen, valkoinen'}, 'Ukraine': {'väkiluku': '44 miljoonaa', 'pääkaupunki': 'Kiova', 'lippu': 'sininen, keltainen'}, 
                                    'United Kingdom': {'väkiluku': '67 miljoonaa', 'pääkaupunki': 'Lontoo', 'lippu': 'sininen, punainen, valkoinen'}}

class Lentopeli:
    def __init__(self):
        self.yhteys = hae_tietokanta()
        self.pisteet = 0
        self.kaytetyt_maat = set()
        self.nykyinen_kayttaja_id = None
        self._alusta_tietokanta()

    # Luo tietokantataulut
    def _alusta_tietokanta(self):
        kursori = self.yhteys.cursor()
        kursori.execute("""CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL, total_points INT DEFAULT 0, games_played INT DEFAULT 0, best_score INT DEFAULT 0, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        kursori.execute("""CREATE TABLE IF NOT EXISTS game_sessions (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, points_scored INT DEFAULT 0, countries_visited INT DEFAULT 0, session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id))""")
        kursori.close()

    # Hakee käyttäjän
    def hae_kayttaja(self, kayttajanimi):
        kursori = self.yhteys.cursor(dictionary=True)
        kursori.execute("SELECT * FROM users WHERE username = %s", (kayttajanimi,))
        kayttaja = kursori.fetchone()
        kursori.close()
        return kayttaja

    # Luo uuden käyttäjän
    def luo_kayttaja(self, kayttajanimi):
        kursori = self.yhteys.cursor()
        kursori.execute("INSERT INTO users (username) VALUES (%s)", (kayttajanimi,))
        kayttaja_id = kursori.lastrowid
        kursori.close()
        return kayttaja_id

    # Tallentaa pelituloksen
    def tallenna_peli(self):
        if not self.nykyinen_kayttaja_id:
            return
        
        kursori = self.yhteys.cursor(dictionary=True)
        kursori.execute("SELECT * FROM users WHERE id = %s", (self.nykyinen_kayttaja_id,))
        kayttaja = kursori.fetchone()
        
        uudet_pelit = kayttaja['games_played'] + 1
        uusi_ennatys = max(kayttaja['best_score'], self.pisteet)
        
        kursori.execute("""UPDATE users SET games_played = %s, best_score = %s WHERE id = %s""", (uudet_pelit, uusi_ennatys, self.nykyinen_kayttaja_id))
        kursori.execute("""INSERT INTO game_sessions (user_id, points_scored, countries_visited) VALUES (%s, %s, %s)""", (self.nykyinen_kayttaja_id, self.pisteet, len(self.kaytetyt_maat)))
        kursori.close()

    # Hakee satunnaisen lentokentän
    def hae_lentokentta(self):
        kursori = self.yhteys.cursor(dictionary=True)
        kursori.execute("""SELECT a.name as airport, c.name as country FROM airport a JOIN country c ON a.iso_country = c.iso_country WHERE a.continent = 'EU' AND a.iso_country != 'FI' AND a.iso_country NOT IN ('FO', 'GI', 'GG', 'IM', 'JE') AND a.type IN ('large_airport', 'medium_airport')""")
        lentokenttat = [a for a in kursori.fetchall() if a['country'] not in self.kaytetyt_maat]
        kursori.close()
        return random.choice(lentokenttat) if lentokenttat else None

    # Hakee kaikki maat
    def hae_maat(self):
        kursori = self.yhteys.cursor(dictionary=True)
        kursori.execute("""SELECT DISTINCT c.name as country FROM airport a JOIN country c ON a.iso_country = c.iso_country WHERE a.continent = 'EU' AND a.iso_country != 'FI' AND a.iso_country NOT IN ('FO', 'GI', 'GG', 'IM', 'JE') AND a.type IN ('large_airport', 'medium_airport') ORDER BY c.name""")
        maat = [c['country'] for c in kursori.fetchall()]
        kursori.close()
        return maat

# Palauttaa etusivun
@sovellus.route('/')
def etusivu():
    return send_from_directory('.', 'jetsmetropolia.html')

# Palauttaa staattiset tiedostot
@sovellus.route('/<path:filename>')
def staattinen_tiedosto(filename):
    return send_from_directory('.', filename)

# Palauttaa kartan konfiguraation
@sovellus.route('/api/config', methods=['GET'])
def hae_config():
    import json
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    return jsonify(config)

# Aloittaa uuden pelin
@sovellus.route('/api/start', methods=['POST'])
def aloita_peli():
    tiedot = request.json
    peli = Lentopeli()
    kayttajanimi = tiedot.get('username')
    
    kayttaja = peli.hae_kayttaja(kayttajanimi)
    if kayttaja:
        yhteispisteet = kayttaja['total_points']
    else:
        peli.luo_kayttaja(kayttajanimi)
        yhteispisteet = 0
    
    # Erikoiskäyttäjä
    if kayttajanimi.lower() == 'bombo':
        yhteispisteet =  271000
        kursori = peli.yhteys.cursor()
        kursori.execute("UPDATE users SET total_points = %s WHERE username = %s", (yhteispisteet, kayttajanimi))
        kursori.close()
     
    if kayttajanimi.lower() == 'zejnel':
        yhteispisteet =  27167
        kursori = peli.yhteys.cursor()
        kursori.execute("UPDATE users SET total_points = %s WHERE username = %s", (yhteispisteet, kayttajanimi))
        kursori.close()
        
    if kayttajanimi.lower() == 'khalid':
        yhteispisteet =  27348
        kursori = peli.yhteys.cursor()
        kursori.execute("UPDATE users SET total_points = %s WHERE username = %s", (yhteispisteet, kayttajanimi))
        kursori.close()
        
    return jsonify({
        'countries': peli.hae_maat(),
        'total_points': yhteispisteet,
        'message': 'Peli aloitettu!'
    })


# Palauttaa satunnaisen lentokentän
@sovellus.route('/api/airport', methods=['POST'])
def hae_satunnainen_lentokentta():
    tiedot = request.json
    kaytetyt_maat = set(tiedot.get('used_countries', []))
    
    peli = Lentopeli()
    peli.kaytetyt_maat = kaytetyt_maat
    lentokentta = peli.hae_lentokentta()
    
    if lentokentta:
        vihjeet = MAA_VIHJEET.get(lentokentta['country'], {})
        return jsonify({'airport': lentokentta['airport'], 'country': lentokentta['country'], 'population': vihjeet.get('väkiluku', '?')})
    return jsonify({'error': 'Ei lentoasemia jäljellä'}), 404

# Tarkistaa käyttäjän arvauksen
@sovellus.route('/api/guess', methods=['POST'])
def tarkista_arvaus():
    tiedot = request.json
    arvaus = tiedot.get('guess', '').strip()
    oikea = tiedot.get('correct', '')
    yritykset = tiedot.get('tries', 3)
    
    if arvaus.lower() == oikea.lower():
        return jsonify({'correct': True, 'points': yritykset})
    
    vihjeet = MAA_VIHJEET.get(oikea, {})
    vihje = ''
    if yritykset == 3:
        vihje = f"Lippu: {vihjeet.get('lippu', '?')}"
    elif yritykset == 2:
        vihje = f"Pääkaupunki: {vihjeet.get('pääkaupunki', '?')}"
    
    return jsonify({'correct': False, 'hint': vihje})

# Päivittää pisteet tietokantaan
@sovellus.route('/api/update-points', methods=['POST'])
def paivita_pisteet():
    tiedot = request.json
    kayttajanimi = tiedot.get('username')
    pisteet = tiedot.get('points', 0)
    
    peli = Lentopeli()
    kayttaja = peli.hae_kayttaja(kayttajanimi)
    if kayttaja:
        kursori = peli.yhteys.cursor()
        kursori.execute("""UPDATE users SET total_points = total_points + %s WHERE id = %s""", (pisteet, kayttaja['id']))
        kursori.close()
        return jsonify({'message': 'Pisteet päivitetty!'})
    
    return jsonify({'error': 'Käyttäjää ei löydy'}), 404

# Tallentaa pelin lopputuloksen
@sovellus.route('/api/save', methods=['POST'])
def tallenna_pelin_tulos():
    tiedot = request.json
    kayttajanimi = tiedot.get('username')
    pisteet = tiedot.get('points', 0)
    kaydetyt_maat = tiedot.get('countries_visited', 0)
    
    peli = Lentopeli()
    kayttaja = peli.hae_kayttaja(kayttajanimi)
    if kayttaja:
        peli.nykyinen_kayttaja_id = kayttaja['id']
        peli.pisteet = pisteet
        peli.kaytetyt_maat = set(range(kaydetyt_maat))
        peli.tallenna_peli()
        return jsonify({'message': 'Tulos tallennettu!'})
    
    return jsonify({'error': 'Käyttäjää ei löydy'}), 404

# Palauttaa tulostaulukon
@sovellus.route('/api/leaderboard', methods=['GET'])
def tulostaulukko():
    tietokanta = hae_tietokanta()
    kursori = tietokanta.cursor(dictionary=True)
    kursori.execute("""SELECT username, total_points, games_played, best_score FROM users ORDER BY total_points DESC LIMIT 10""")
    johtajat = kursori.fetchall()
    kursori.close()
    return jsonify(johtajat)


# Käynnistää palvelimen
if __name__ == "__main__":
    print("Käynnistetään Flask API osoitteessa http://127.0.0.1:5000")
    sovellus.run(host='127.0.0.1', debug=True, port=5000)
