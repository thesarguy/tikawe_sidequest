import sqlite3

REMOVE_SEED = False  # Vaihda True jos haluat poistaa esimerkkidatan ilman että pitää aloittaa alusta

def add_seed():
    db = sqlite3.connect("database.db")
    db.execute("INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)",
               ("demo", "pbkdf2:sha256:600000$demo$demo"))
    user_id = db.execute("SELECT id FROM users WHERE username = 'demo'").fetchone()[0]

    sidequests = [
    (
        "Tee oma pizza taikinasta asti",
        "Älä osta valmistaikinaa. Tee taikina itse jauhoista, hiivasta ja vedestä, anna sen nousta ja paista pizza uunissa. Täytteet saat valita itse.",
        "keskitaso",
        "useita tunteja"
    ),
    (
        "Käy museossa jossa et ole käynyt",
        "Valitse museo Helsingistä tai lähialueelta johon et ole ennen astunut sisään. Käy siellä ja katso näyttely kunnolla, älä vain kuittaa käyntiä ovella.",
        "helppo",
        "1–3 tuntia"
    ),
    (
        "Opi yksi korttitemppu",
        "Valitse yksi korttitemppu YouTubesta, harjoittele se niin hyvin että pystyt esittämään sen kaverille vakuuttavasti ilman että temppu paljastuu.",
        "helppo",
        "30–60 min"
    ),
    (
        "Piirrä lempieläimesi",
        "Piirrä lempieläimesi paperille kynällä tai tussilla. Ei tarvitse olla taideteos, tärkeintä on että eläin on tunnistettavissa. Voit halutessasi värittää sen.",
        "helppo",
        "15–30 min"
    ),
    (
        "Käy Aalto-yliopistolla sanomassa että HY on parempi",
        "Mene fyysisesti Aalto-yliopiston kampukselle Otaniemeen. Sano ääneen vähintään yhdelle ihmiselle että Helsingin yliopisto on parempi. Dokumentoi reaktio.",
        "helppo",
        "1–3 tuntia"
    ),
    (
        "Opettele Rubikin kuution ratkaisu",
        "Osta tai lainaa Rubikin kuutio ja opettele ratkaisemaan se alusta loppuun ohjeen avulla. Questi on suoritettu kun pystyt ratkaisemaan sen itsenäisesti ilman ohjetta.",
        "haastava",
        "useita päiviä"
    ),
    (
        "Tee yksi ohjelmointiprojekti ilman tekoälyä",
        "Tee jokin pieni ohjelmointiprojekti, vaikka komentorivityökalu, peli tai skripti käyttämättä lainkaan tekoälyä (ei ChatGPT, ei Claude, ei Copilot). Voit käyttää dokumentaatiota ja Stack Overflowia.",
        "haastava",
        "useita tunteja"
    ),
    (
        "Tee phone clean-up",
        "Käy läpi puhelimesi kuvagalleria ja poista turhat kuvat. Poista myös sovellukset joita et ole avannut yli kuukauteen. Tavoite: puhelin tuntuu taas kevyeltä.",
        "helppo",
        "30–60 min"
    ),
    (
        "Tee oma playlist vähintään 15 biisistä",
        "Luo Spotifyyn, YouTubeen tai muuhun palveluun playlist jossa on vähintään 15 kappaletta. Playlistin pitää noudattaa jotain teemaa tai tunnelmaa, ei sekalainen sattuma.",
        "helppo",
        "15–30 min"
    ),
    (
        "Pyydä Linus Torvaldsiltä kirjallinen lupa olla käyttämättä Linuxia",
        "Linus Torvalds vierailee silloin tällöin Suomessa. Etsi tilaisuus jossa hän on paikalla, mene paikalle ja pyydä häneltä kirjallinen lupa siihen että saat käyttää Windowsia tai macOS:ää ilman syyllisyydentunnetta. Dokumentoi vastaus.",
        "erittäin haastava",
        "useita päiviä"
    ),
    (
        "Asenna Linux, käytä sitä viikon ajan ja asenna sitten Windows takaisin",
        "Asenna jokin Linux-distro (esim. Ubuntu tai Fedora) koneellesi ja käytä sitä ainoana käyttöjärjestelmänä viikon ajan. Viikon jälkeen saat asentaa Windowsin takaisin, tai sitten et.",
        "erittäin haastava",
        "useita päiviä"
    ),
    (
        "Kirjoita käsin runo siitä miksi TIRA on hankalaa",
        "Kirjoita käsin, paperille, runo joka kuvaa tietorakenteet ja algoritmit -kurssin tuskaa. Runon ei tarvitse olla pitkä, mutta sen pitää olla aito.",
        "helppo",
        "15–30 min"
    ),
    (
        "Juo vain vettä 30 päivän ajan",
        "Ei kahvia, ei energiajuomia, ei mehua, ei alkoholia. Pelkkää vettä 30 päivän ajan. TKT-opiskelijalle tämä on todennäköisesti vaikein tämän sivuston questiiteista.",
        "erittäin haastava",
        "useita päiviä"
    ),
    (
        "Kirjoita päiväkirjaa viikon ajan",
        "Kirjoita joka päivä vähintään yksi kappale siitä mitä tapahtui ja mitä ajattelit. Voit kirjoittaa käsin tai koneella. Questi on suoritettu kun sinulla on seitsemän päivän merkinnät.",
        "helppo",
        "useita päiviä"
    ),
]

    db.executemany("""
        INSERT INTO sidequests (title, description, difficulty, estimated_duration, user_id, created_at, status)
        VALUES (?, ?, ?, ?, ?, datetime('now'), 1)
    """, [(s[0], s[1], s[2], s[3], user_id) for s in sidequests])

    db.commit()
    db.close()
    print(f"Lisätty {len(sidequests)} sidequestia!")


def remove_seed():
    db = sqlite3.connect("database.db")
    db.execute("DELETE FROM sidequests WHERE user_id = (SELECT id FROM users WHERE username = 'demo')")
    db.execute("DELETE FROM users WHERE username = 'demo'")
    db.commit()
    db.close()
    print("Esimerkkidata poistettu!")


if REMOVE_SEED:
    remove_seed()
else:
    add_seed()