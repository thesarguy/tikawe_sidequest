
# Sidequest

Sidequest on websovellus jossa käyttäjät voivat luoda ja selata sidequesteja eli pieniä tehtäviä tai aktiviteetteja. 

# Toiminnot

- Käyttäjä voi luoda tunnuksen ja kirjautua sisään/ulos, sekä katsella ilman tunnusta
- Kirjautunut käyttäjä voi luoda, muokata ja poistaa sidequesteja
- Kirjautunut käyttäjä voi merkata sidequestin suoritetuksi tai ei-suoritetuksi
- Sidequesteja voi hakea nimellä
- Sidequesteja voi lajitella nimen, keston tai suoritusstatuksen mukaan

# Sovelluksen käynnistäminen

1. Asenna Flask: pip install flask

2. luo config.py tiedoston juureen, ja lisää siihen: secret_key = "(oma salainen avain tähän)"

2. Luo tietokanta: python -c "import sqlite3; db=sqlite3.connect('database.db'); db.executescript(open('schema.sql').read()); db.commit()"

3. Käynnistä sovellus pythonin terminaalissa: python -m flask run
4. Avaa selaimessa: http://127.0.0.1:5000

# Testaaminen

- Luo tunnus rekisteröitymissivulla
- Kirjaudu sisään
- Luo uusi sidequest "Luo uusi sidequest" -linkistä
- Muokkaa tai poista sidequestia avaamalla sen sivu
- Kokeile hakua ja lajittelua etusivulla

# to-do

- suoritusmerkintä on kaikkien käyttäjien kanssa yhteinen, muutetaan käyttäjäkohtaiseksi tulevaisuudessa
- tällä hetkellä ei ole esimerkki sidequesteja, vaan test-caseja sivun toimintaa varten, pitäisi tehdä iso kasa niitä lisää,
- ulkoasun parantaminen
- salasana- ja käyttäjänimivaatimukset
- tilastot
- muokkaushistoria