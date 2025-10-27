---
title: PostgreSQL-liitin – Tietokantaintegraatio | digna-dokumentaatio
description: Määritä digna muodostamaan yhteys PostgreSQL:ään käyttäen psycopg Python -ajuria tai PostgreSQL ODBC -ajuria. Tukee salasanapohjaista todennusta DSN- tai DSN-less-asetuksilla.
image: /assets/logo_square.png
---


# Lähdeyhteys PostgreSQL:ään

Tässä ohjeessa kuvataan, miten *digna* konfiguroidaan muodostamaan yhteys Postgresiin joko natiivin Python-ajurin tai ODBC-ajurin kautta.

Tämä viittaa kohtaan **"Luo tietokantayhteys"**.

![Luo tietokantayhteys](images/data_source_config_input_mask.png)

---

## Natiivinen Python-ajuri

**Kirjasto:** `psycopg`  
**Tuettu todennus:** Vain salasanapohjainen todennus

> ⚠️ Muihin todennusmenetelmiin käytä ODBC-ajuria.

### *digna* -määritys (natiivinen ajuri)

Anna seuraavat tiedot **"Luo tietokantayhteys"** -näytössä:

```
Teknologia:         Postgres
Isäntäosoite:       Palvelimen nimi tai IP-osoite
Isäntäportti:       Porttinumero, esim. 5432
Tietokannan nimi:   Tietokannan nimi
Skeeman nimi:       Skeema, joka sisältää lähdetiedot
Käyttäjänimi:       Tietokannan käyttäjänimi
Käyttäjän salasana: Salasana käyttäjälle
Käytä ODBC:         Pois käytöstä (oletus)
```

---

## ODBC-ajuri

ODBC-ajuri voi tukea laajempaa valikoimaa todennus- ja yhteysoptioita. Tässä keskitytään salasanapohjaiseen todennukseen ajurin **PostgreSQL Unicode(x64)** avulla.

### 1. Asenna ODBC-ajuri

Asenna **PostgreSQL Unicode(x64)** (tai vastaava) noudattamalla toimittajan virallista asennusohjetta.

### 2. Määritä ODBC-tietolähde

Noudata näitä vaiheita määrittääksesi uuden ODBC-tietolähteen salasanapohjaisella todennuksella:

#### Vaihe 1
![Vaihe 1](images/postgres/create_odbc_data_source_step1.png)

Huom: Jos tietokanta-asetuksissasi täytyy valita tietty "SSLMode", käytä samaa asetusta myös DSN-less-konfiguraatiossa.

#### Vaihe 2 – Testaa yhteys

Paina **Test Connection** -painiketta.

![Vaihe 2](images/postgres/create_odbc_data_source_step2.png)

---

Nyt voit määrittää *digna*:n käyttämään ODBC-yhteyttä joko **DSN (Data Source Name)** -pohjaisesti tai **DSN-less** -asetuksella.

---

### A. DSN-pohjainen määritys

#### *digna* -määritys

Anna **"Luo tietokantayhteys"** -näytössä seuraavat tiedot:

```
Teknologia:         PostgreSQL
Tietokannan nimi:   Tietokanta, joka sisältää lähdeskeeman
Skeeman nimi:       Skeema, joka sisältää lähdetiedot
Käytä ODBC:         Käytössä
```

#### ODBC-ominaisuudet

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 `DSN` pitää vastata ODBC-ajurin konfiguraatiossa määriteltyä nimeä.

---

### B. DSN-less-määritys

#### *digna* -määritys

Anna **"Luo tietokantayhteys"** -näytössä seuraavat tiedot:

```
Teknologia:         PostgreSQL
Tietokannan nimi:   Skeema, joka sisältää lähdetiedot (sama kuin Skeeman nimi)
Skeeman nimi:       Skeema, joka sisältää lähdetiedot
Käytä ODBC:         Käytössä
```

#### ODBC-ominaisuudet

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "palvelimesi nimi tai IP-osoite"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres tai muu tietokantasi nimi"
name: "UID",        value: "postgres-käyttäjätunnuksesi"
name: "PWD",        value: "postgres-käyttäjän salasana"
name: "SSLMode",    value: "require"
```