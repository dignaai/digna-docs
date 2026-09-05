# Lähdeyhdistin Oraclelle

Tässä ohjeessa kerrotaan, miten *digna* konfiguroidaan yhdistämään Oracle DB:hen joko natiivin Python-ajurin tai ODBC-ajurin kautta.

Ohje viittaa näyttöön **"Create a Database Connection"**.

![Luo tietokantayhteys](images/data_source_config_input_mask.png)

---

## Natiivinen Python-ajuri

**Kirjasto:** `python-oracledb`  
**Tuetut todennustavat:** Vain salasanapohjainen todennus

> Muiden todennusmenetelmien osalta käytä ODBC-ajuria.

### *digna* -konfigurointi (natiivi ajuri)

Anna seuraavat tiedot **"Create a Database Connection"** -näytössä:

```
Teknologia:      Oracle
Isäntäosoite:    Palvelimen nimi tai IP-osoite
Isäntäportti:    Porttinumero, esim. 1521
Tietokannan nimi: Instanssin nimi, palvelun nimi
Skeeman nimi:    Skeema, joka sisältää lähdetiedot
Käyttäjänimi:    Tietokantakäyttäjän nimi
Käyttäjän salasana: Salasana käyttäjälle
Käytä ODBC:      Pois käytöstä (oletus)
```

---

## ODBC-ajuri

ODBC-ajuri voi tukea laajempaa valikoimaa todennus- ja liittymisvaihtoehtoja. Tässä osiossa keskitytään salasanapohjaiseen todennukseen käyttäen ajuria **Oracle in OraDB21Home1**.

### 1. Asenna ODBC-ajuri

Asenna **Oracle in OraDB21Home1** (tai vastaava) seuraamalla toimittajan virallista asennusohjetta.

### 2. Konfiguroi ODBC-tietolähde

Noudata näitä vaiheita konfiguroidaksesi uuden ODBC-tietolähteen salasanapohjaisella todennuksella:

#### Vaihe 1
![Vaihe 1](images/oracle/create_odbc_data_source_step1.png)

Huom:
TNS Service Name on määritettävä oracle-clientin tnsnames.ora-tiedostossa. Siinä annetaan yhteydenselain (isäntä, portti, palvelun nimi).

#### Vaihe 2 – Testaa yhteys

Napsauta **Test Connection** -painiketta.

![Vaihe 2](images/oracle/create_odbc_data_source_step2.png)

Anna salasana ja napsauta **OK**-painiketta.

![Vaihe 2](images/oracle/create_odbc_data_source_step3.png)

---

Nyt voit konfiguroida *digna* käyttämään ODBC-yhteyttä joko **DSN (Data Source Name)** -pohjaisesti tai **DSN-less** -asetuksella.

---

### A. DSN-pohjainen konfiguraatio

#### *digna* -konfigurointi

Anna **"Create a Database Connection"** -näytössä seuraavat tiedot:

```
Teknologia:      Oracle
Tietokannan nimi: Tietokanta, joka sisältää lähdeskeeman
Skeeman nimi:    Skeema, joka sisältää lähdetiedot
Käytä ODBC:      Käytössä
```

#### ODBC-ominaisuudet

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> `DSN` on oltava sama kuin ODBC-ajurin asetuksissa määritelty nimi.

---

### B. DSN-less -konfiguraatio

#### *digna* -konfigurointi

Anna **"Create a Database Connection"** -näytössä seuraavat tiedot:

```
Teknologia:      Oracle
Tietokannan nimi: Skeema, joka sisältää lähdetiedot (sama kuin Skeeman nimi)
Skeeman nimi:    Skeema, joka sisältää lähdetiedot
Käytä ODBC:      Käytössä
```

#### ODBC-ominaisuudet

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```