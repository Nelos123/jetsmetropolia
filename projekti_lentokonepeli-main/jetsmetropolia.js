// Pelin tila
let peliTila = {kayttajanimi: '', pisteet: 0, yhteispisteet: 0, yritykset: 3, nykyinenLentokentta: null, kaytetytMaat: [], kaikkiMaat: []};

// Muotoilee pisteet (k = tuhat)
function muotoilePisteet(pisteet) {
    if (pisteet >= 1000) {return Math.floor(pisteet / 1000) + 'k';}
    return pisteet;
}

let globe;
let maaPolygonit = [];

// Maakohtaiset koordinaatit
const maaKoordinaatit = {'Finland': { lat: 64, lng: 26 }, 'Sweden': { lat: 62, lng: 15 }, 'Norway': { lat: 60, lng: 10 }, 'Denmark': { lat: 56, lng: 10 }, 'Iceland': { lat: 65, lng: -18 },
    'Estonia': { lat: 59, lng: 26 }, 'Latvia': { lat: 57, lng: 25 }, 'Lithuania': { lat: 55, lng: 24 }, 'Poland': { lat: 52, lng: 20 }, 'Germany': { lat: 51, lng: 10 },
    'Netherlands': { lat: 52, lng: 5 }, 'Belgium': { lat: 50.5, lng: 4 }, 'Luxembourg': { lat: 49.8, lng: 6.1 }, 'France': { lat: 46, lng: 2 }, 'Spain': { lat: 40, lng: -4 },
    'Portugal': { lat: 39.5, lng: -8 }, 'Italy': { lat: 42.8, lng: 12.6 }, 'Switzerland': { lat: 47, lng: 8 }, 'Austria': { lat: 47.5, lng: 14 }, 'Czech Republic': { lat: 49.8, lng: 15.5 }, 
    'Slovakia': { lat: 48.7, lng: 19.7 }, 'Hungary': { lat: 47, lng: 19.5 }, 'Slovenia': { lat: 46, lng: 15 }, 'Croatia': { lat: 45, lng: 16 }, 'Bosnia and Herzegovina': { lat: 44, lng: 18 },
    'Serbia': { lat: 44, lng: 21 }, 'Montenegro': { lat: 42.5, lng: 19 }, 'Albania': { lat: 41, lng: 20 }, 'North Macedonia': { lat: 41.6, lng: 21.7 }, 'Greece': { lat: 39, lng: 22 },
    'Bulgaria': { lat: 43, lng: 25 }, 'Romania': { lat: 46, lng: 25 }, 'Moldova': { lat: 47, lng: 29 }, 'Ukraine': { lat: 49, lng: 32 }, 'Belarus': { lat: 54, lng: 28 }, 'Russia': { lat: 60, lng: 100 },
    'United Kingdom': { lat: 54, lng: -2 }, 'Ireland': { lat: 53, lng: -8 }, 'Turkey': { lat: 39, lng: 35 }, 'Cyprus': { lat: 35, lng: 33 }
};

// Alustaa 3D-kartan
function alustaGlobe() {
    const container = document.getElementById('globeViz');
    const height = window.innerHeight - 140;
    
    globe = Globe()
        (container)
        .globeImageUrl('//unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
        .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
        .backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
        .width(container.offsetWidth)
        .height(height)
        .atmosphereColor('lightskyblue')
        .atmosphereAltitude(0.25)
        .labelsData(maaPolygonit)
        .labelLat(d => d.lat)
        .labelLng(d => d.lng)
        .labelText(d => d.name)
        .labelSize(1.5)
        .labelColor(() => '#00ff00')
        .labelDotRadius(0.8)
        .labelAltitude(0.01);

    globe.pointOfView({ lat: 50, lng: 10, altitude: 2 });
}

// Korostaa oikean maan kartalla
function korostaMaa(maanNimi) {
    const koordinaatit = maaKoordinaatit[maanNimi];
    if (!koordinaatit) return;
    
    maaPolygonit = [{lat: koordinaatit.lat, lng: koordinaatit.lng, name: maanNimi}];
    
    if (globe) {
        globe.labelsData(maaPolygonit);
        globe.pointOfView({lat: koordinaatit.lat, lng: koordinaatit.lng, altitude: 1.5 }, 1000);}
}

// Poistaa korostukset
function tyhjennaKorostukset() {
    maaPolygonit = [];
    if (globe) {
        globe.labelsData([]);
        globe.pointOfView({ lat: 50, lng: 10, altitude: 2 }, 1000);
    }
}

// Lataa kartan sivun avautuessa
window.addEventListener('load', () => {
    alustaGlobe();
});

// Säätää kartan kokoa ikkunan koon muuttuessa
window.addEventListener('resize', () => {
    if (globe) {
        const container = document.getElementById('globeViz');
        const height = window.innerHeight - 140;
        globe.width(container.offsetWidth).height(height);
    }
});

// Aloittaa pelin
async function aloitaPeli() {
    const kayttajanimi = document.getElementById('kayttajanimi').value.trim();
    
    if (!kayttajanimi) {
        alert('Anna käyttäjänimi!');
        return;
    }
    
    peliTila.kayttajanimi = kayttajanimi;

    const vastaus = await fetch('http://127.0.0.1:5000/api/start', {method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username: kayttajanimi })});
    const data = await vastaus.json();
    peliTila.kaikkiMaat = data.countries;
    peliTila.yhteispisteet = data.total_points || 0;

    document.getElementById('kirjautumisruutu').classList.add('piilotettu');
    document.getElementById('peliruutu').classList.remove('piilotettu');
    document.getElementById('maita-jaljella').textContent = muotoilePisteet(peliTila.yhteispisteet);

    lataaSeuraavaLentokentta();
}

// Lataa seuraavan lentokentän
async function lataaSeuraavaLentokentta() {
    const vastaus = await fetch('http://127.0.0.1:5000/api/airport', {method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ used_countries: peliTila.kaytetytMaat })});
    if (vastaus.status === 404) {
        naytaLoppuruutu();
        return;
    }

    const data = await vastaus.json();
    peliTila.nykyinenLentokentta = data;
    peliTila.yritykset = 3;

    document.getElementById('lentokentta-nimi').textContent = data.airport;
    document.getElementById('vihje1').textContent = `Väkiluku: ${data.population}`;
    document.getElementById('vihje2').classList.add('piilotettu');
    document.getElementById('vihje3').classList.add('piilotettu');
    document.getElementById('yrityksia-jaljella').textContent = '3';
    document.getElementById('viesti').innerHTML = '';
    
    paivitaMaaNapit();
}

// Päivittää maanappien listan
function paivitaMaaNapit() {
    const maaLista = document.getElementById('maa-lista');
    maaLista.innerHTML = '';
    
    const jaljellaMaat = peliTila.kaikkiMaat.filter(maa => !peliTila.kaytetytMaat.includes(maa));
    
    jaljellaMaat.forEach(maa => {
        const nappi = document.createElement('button');
        nappi.className = 'maa-nappi';
        nappi.textContent = maa;
        nappi.onclick = () => tarkistaArvaus(maa);
        maaLista.appendChild(nappi);
    });
}

// Tarkistaa käyttäjän arvauksen
async function tarkistaArvaus(arvaus) {
    if (!arvaus || peliTila.yritykset <= 0) return;

    const vastaus = await fetch('http://127.0.0.1:5000/api/guess', {method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({guess: arvaus, correct: peliTila.nykyinenLentokentta.country, tries: peliTila.yritykset})});

    const data = await vastaus.json();

    if (data.correct) {
        const pisteet = peliTila.yritykset;
        peliTila.pisteet += pisteet;
        
        if (!peliTila.kaytetytMaat.includes(peliTila.nykyinenLentokentta.country)) {
            peliTila.kaytetytMaat.push(peliTila.nykyinenLentokentta.country);
        }
        
        await paivitaPisteet(pisteet);
        korostaMaa(peliTila.nykyinenLentokentta.country);
        
        peliTila.yhteispisteet += pisteet;
        
        naytaViesti(`✓ Oikein! +${pisteet} pistettä`, 'success');
        document.getElementById('nykyiset-pisteet').textContent = peliTila.pisteet;
        document.getElementById('maita-jaljella').textContent = muotoilePisteet(peliTila.yhteispisteet);
        
        setTimeout(() => {
            tyhjennaKorostukset();
            lataaSeuraavaLentokentta();
        }, 3000);
    } else {
        peliTila.yritykset--;
        document.getElementById('yrityksia-jaljella').textContent = peliTila.yritykset;

        if (peliTila.yritykset > 0) {
            naytaViesti(`✗ Väärin! ${data.hint}`, 'error');
            
            if (peliTila.yritykset === 2) {
                document.getElementById('vihje2').textContent = data.hint;
                document.getElementById('vihje2').classList.remove('piilotettu');
            } else if (peliTila.yritykset === 1) {
                document.getElementById('vihje3').textContent = data.hint;
                document.getElementById('vihje3').classList.remove('piilotettu');
            }
        } else {
            if (!peliTila.kaytetytMaat.includes(peliTila.nykyinenLentokentta.country)) {
                peliTila.kaytetytMaat.push(peliTila.nykyinenLentokentta.country);
            }
            
            korostaMaa(peliTila.nykyinenLentokentta.country);
            naytaViesti(`✗ Oikea vastaus: ${peliTila.nykyinenLentokentta.country} (+0 pistettä)`, 'error');
            document.getElementById('maita-jaljella').textContent = muotoilePisteet(peliTila.yhteispisteet);
            
            setTimeout(() => {
                tyhjennaKorostukset();
                lataaSeuraavaLentokentta();
            }, 4000);
        }
    }
}

// Näyttää viestin käyttäjälle
function naytaViesti(teksti, tyyppi) {
    const viesti = document.getElementById('viesti');
    viesti.textContent = teksti;
    viesti.className = `message ${tyyppi}`;
}

// Lopettaa pelin
async function lopetaPeli() {
    await tallennaPeli();
    naytaLoppuruutu();
}

// Tallentaa pelin lopputuloksen
async function tallennaPeli() {
    await fetch('http://127.0.0.1:5000/api/save', {method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({username: peliTila.kayttajanimi, points: peliTila.pisteet, countries_visited: peliTila.kaytetytMaat.length})
    });
}

// Päivittää pisteet tietokantaan
async function paivitaPisteet(pisteet) {
    await fetch('http://127.0.0.1:5000/api/update-points', {method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({username: peliTila.kayttajanimi, points: pisteet})
    });
}

// Näyttää loppuruudun
async function naytaLoppuruutu() {
    document.getElementById('peliruutu').classList.add('piilotettu');
    document.getElementById('loppuruutu').classList.remove('piilotettu');
    document.getElementById('lopulliset-pisteet').textContent = peliTila.pisteet;
    document.getElementById('maita-kayty').textContent = peliTila.kaytetytMaat.length;
    
    await lataaTulostaulukko();
}

// Lataa tulostaulukon
async function lataaTulostaulukko() {
    try {
        const vastaus = await fetch('http://127.0.0.1:5000/api/leaderboard');
        const tulokset = await vastaus.json();
        const lista = document.getElementById('tulostaulukko-lista');
        lista.innerHTML = '';
        const top5 = tulokset.slice(0, 5);
        top5.forEach((tulos, index) => {
            const rivi = document.createElement('div');
            rivi.className = 'tulostaulukko-rivi';
            const nimi = document.createElement('span');
            nimi.className = 'tulostaulukko-nimi';
            nimi.textContent = `${index + 1}. ${tulos.username}`;
            const pisteet = document.createElement('span');
            pisteet.className = 'tulostaulukko-pisteet';
            pisteet.textContent = muotoilePisteet(tulos.total_points) + ' pistettä';
            rivi.appendChild(nimi);
            rivi.appendChild(pisteet);
            lista.appendChild(rivi);
        });
    } catch (virhe) {
        console.error('Virhe tulostaulukon latauksessa:', virhe);
    }
}

// Enter-näppäin kirjautumisessa
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('kayttajanimi').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') aloitaPeli();
    });
});
