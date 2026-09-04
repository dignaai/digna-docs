---
title: Teradata-liitin – tietokantaintegraatio | digna-dokumentaatio
description: Konfiguroi digna yhdistämään Teradataan käyttämällä teradatasql Python -ajuria tai Teradata ODBC -ajuria. Tukee salasanaperusteista todennusta DSN- tai DSN-less-asetuksilla.
image: /assets/logo_square.png
---


# Teradata-lähdeyhteys

Tämä ohje kuvaa, miten konfiguroidaan *digna* yhdistämään Teradataan joko natiivin Python-yhdistäjän tai ODBC-ajurin kautta.

Oppaassa viitataan näyttöön **"Luo tietokantayhteys"**.

![Luo tietokantayhteys](images/data_source_config_input_mask.png)

---

## Natiivinen Python-ajuri

**Kirjasto:** `teradatasql`  
**Tuettu todennus:** Vain salasanaperusteinen todennus

> Muiden todennustapojen kohdalla käytä ODBC-ajuria.

### *digna* -konfiguraatio (natiivinen ajuri)

Anna seuraavat tiedot **"Luo tietokantayhteys"** -näytöllä:

```
Technology:      Teradata
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1025
Database Name:   Database name
Schema Name:     Database name
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-ajuri

ODBC-ajuri voi tukea laajempaa valikoimaa todennus- ja yhteysvaihtoehtoja. Tämä osio keskittyy salasanaperusteiseen todennukseen käyttäen ajuria **Teradata Database ODBC Driver 20.00**.

### 1. Asenna ODBC-ajuri

Asenna ajuri **Teradata Database ODBC Driver 20.00** (tai vastaava) seuraamalla toimittajan virallista asennusopasta.

### 2. Konfiguroi ODBC-tietolähde

Noudata näitä ohjeita konfiguroidaksesi uuden ODBC-tietolähteen salasanaperusteisella todennuksella:

#### Vaihe 1
![Vaihe 1](images/teradata/create_odbc_data_source_step1.png)

Napsauta **Test**-painiketta.

#### Vaihe 2
![Vaihe 2](images/teradata/create_odbc_data_source_step2.png)

Anna käyttäjätunnus ja salasana.

Napsauta **OK**-painiketta.
Kun saat onnistumisilmoituksen, ODBC on konfiguroitu oikein.

---

Nyt voit konfiguroida *digna*:n käyttämään ODBC-yhteyttä joko **DSN (Data Source Name)** -asetuksella tai **DSN-less** -asetuksella.

---

### A. DSN-pohjainen konfigurointi

#### *digna* -konfiguraatio

Anna **"Luo tietokantayhteys"** -näytöllä seuraavat tiedot:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-ominaisuudet

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> `DSN` on oltava sama kuin ODBC-ajurin konfiguraatiossa määritelty nimi.

---

### B. DSN-less -konfigurointi

#### *digna* -konfiguraatio

Anna **"Luo tietokantayhteys"** -näytöllä seuraavat tiedot:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-ominaisuudet

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
