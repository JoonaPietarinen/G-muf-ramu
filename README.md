# Geemufooramu <sub><sub>(GameForum, japanese)

Sovellus ei ainakaan vielä ole testattavissa fly.io osoitteessa


Tilanne tällä hetkellä:
- [x]Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen. <br/>
- [x]Käyttäjä näkee sovelluksen "etusivulla" listan alueista <br/>
- [x]Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön. <br/>
- [x]Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun. <br/>



Aloitus sivulta pääset rekisteröitymään, kirjautumaan tai etusivulle, josta voit valita alueen, jossa näet jo julkaistut ketjut ja voit julkaista uusia ketjuja.<br/>
Jos olet kirjautunut sisään, voit lisätä uusia ketjuja alueille tai viestejä ketjuihin. <br/>



##ASENNUS

Kloonaa tämä repositorio omalle koneellesi.
```
git clone https://github.com/JoonaPietarinen/Geemufooramu
cd GeemuFooramu
```
siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:
```
DATABASE_URL=postgresql:///<new-db-name>
SECRET_KEY=<salainen-avain>
```
Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```
Määritä vielä tietokannan skeema komennolla
```
psql < schema.sql
```
Luo ensimmäiset ketjut ja viestit komennolla
```
psql < test1.sql
```

Nyt voit käynnistää sovelluksen komennolla
```
flask run
```
IDEA:

Pelikeskustelusovellus <br/>
Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe (tietty peli, softa yms.). Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Sovelluksen ominaisuuksia:

- [x]Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen. <br/> 
- [ ]Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan. <br/>
- [x]Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön. <br/>
- [x]Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun. <br/>
- [ ]Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin. <br/>
- [ ]Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana. <br/>
- [ ]Ylläpitäjä voi lisätä ja poistaa keskustelualueita. <br/>
- [ ]Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle. <br/>
