---
title: MS SQL Server -lähdeyhdistin – Tietokantaintegraatio | digna-dokumentaatio
description: Konfiguroi digna yhdistämään Microsoft SQL Serveriin käyttämällä pymssql Python -ajuria tai SQL Serverin ODBC-ajuria. Tukee salasanaan perustuvaa todennusta DSN- tai DSN-vapaissa asetuksissa.
image: /assets/logo_square.png
---


# MS SQL Server -lähdeyhdistin

Tässä ohjeessa kerrotaan, miten *digna* konfiguroidaan yhdistämään SQL Serveriin joko natiivin Python-ajurin tai ODBC-ajurin kautta.

Se viittaa ruutuun **"Create a Database Connection"**.

![Luo tietokantayhteys](images/data_source_config_input_mask.png)

---

## Natiivinen Python-ajuri

**Kirjasto:** `pymssql`  
**Tuetut todennustavat:** Vain salasanaan perustuva todennus

> ⚠️ Muissa todennustavoissa käytä ODBC-ajuria.

### *digna* -konfigurointi (natiivinen ajuri)

Anna seuraavat tiedot **"Create a Database Connection"** -ruudussa:

```
Technology:      MS SQL Server
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-ajuri

ODBC-ajuri voi tukea laajempaa valikoimaa todennus- ja yhteysvaihtoehtoja. Tässä osiossa keskitytään salasanaan perustuvaan todennukseen ajurilla **SQL Server**.

### 1. Asenna ODBC-ajuri

Asenna ajuri **SQL Server** (tai vastaava) seuraamalla toimittajan virallista asennusohjetta.

### 2. Konfiguroi ODBC-datat lähde

Seuraa näitä vaiheita konfiguroidaksesi uuden ODBC-datapisteen salasanaan perustuvalla todennuksella:

#### Vaihe 1
![Vaihe 1](images/sqlserver/create_odbc_data_source_step1.png)

Klikkaa **Next >** -painiketta.

#### Vaihe 2
![Vaihe 2](images/sqlserver/create_odbc_data_source_step2.png)

Valitse todennustapa (esim. käyttäjätunnus ja salasana)
ja anna tarvittavat tiedot.

Klikkaa **Next >** -painiketta.

#### Vaihe 3
![Vaihe 3](images/sqlserver/create_odbc_data_source_step3.png)

Valitse ANSI-yhteensopivat asetukset ja klikkaa **Next >** -painiketta.

#### Vaihe 4
![Vaihe 4](images/sqlserver/create_odbc_data_source_step4.png)

Voit jättää oletusasetukset tai valita tarvittaessa lokitusvaihtoehtoja
ja klikata **Finish** -painiketta. 

#### Vaihe 5
![Vaihe 5](images/sqlserver/create_odbc_data_source_step5.png)

Klikkaa nyt **Test datasource** -painiketta.

#### Vaihe 6
![Vaihe 6](images/sqlserver/create_odbc_data_source_step6.png)

Kun saat onnistumisilmoituksen, ODBC on konfiguroitu oikein.

---

Nyt voit konfiguroida *digna*:n käyttämään ODBC-yhteyttä joko **DSN (Data Source Name)** -pohjaisesti tai **DSN-less** -asetuksella.

---

### A. DSN-pohjainen konfigurointi

#### *digna* -konfigurointi

Anna **"Create a Database Connection"** -ruudussa seuraavat tiedot:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-ominaisuudet

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 `DSN` on oltava sama kuin ODBC-ajurin konfiguraatiossa määritelty nimi.

---

### B. DSN-vapaa konfigurointi

#### *digna* -konfigurointi

Anna **"Create a Database Connection"** -ruudussa seuraavat tiedot:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-ominaisuudet

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```