# Lähdeyhteys Netezzaan

Tässä ohjeessa kerrotaan, miten *digna* määritetään yhdistämään Netezzaan ODBC-ajurin avulla.

Se viittaa näyttöön **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## ODBC Driver

ODBC-ajuri voi tukea useita todennus- ja yhteysvaihtoehtoja. Tässä osiossa keskitytään salasanapohjaiseen todennukseen käyttäen ajuria **NetezzaSQL**.

### 1. Install the ODBC Driver

Asenna ajuri **NetezzaSQL** (tai vastaava) toimittajan virallisen asennusohjeen mukaan.

### 2. Configure the ODBC Data Source

Noudata näitä vaiheita määrittääksesi uuden ODBC-tietolähteen salasanapohjaisella todennuksella:

#### Step 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Riippuen Netezza-ajuristasi, asennuksesta ja turvallisuusvaatimuksista, saatat joutua myös antamaan tietoja välilehdillä **Advanced DSN Options**, **SSL DSN Options** tai **Driver Options**. Yksinkertaisimmassa asetuksessa riittää, että täytät tiedot **DSN Options** -välilehdelle.

Klikkaa **Test Connection** -painiketta.

#### Step 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Kun saat onnistumisilmoituksen, ODBC on konfiguroitu oikein.

---

Nyt voit määrittää *digna* käyttämään ODBC-yhteyttä joko **DSN (Data Source Name)** -asetuksella tai **DSN-less** -konfiguraatiolla.

---

### A. DSN-Based Configuration

#### *digna* -määritys

Näytössä **"Create a Database Connection"**, anna seuraavat tiedot:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-ominaisuudet

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> `DSN`-arvon on vastattava ODBC-ajurikonfiguraatiossa määriteltyä nimeä.

---

### B. DSN-less Configuration

#### *digna* -määritys

Näytössä **"Create a Database Connection"**, anna seuraavat tiedot:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-ominaisuudet

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```