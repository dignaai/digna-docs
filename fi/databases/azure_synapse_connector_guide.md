# Lähdeyhteys Azure Synapse Analyticsiin

Tässä ohjeessa kuvataan, miten *digna* konfiguroidaan yhdistämään Azure Synapse Analyticsiin joko natiivilla Python-yhdyskäytävällä tai ODBC-ajurilla.
Se tukee sekä serverless- että dedikoituja SQL-pooloja.

Ohje viittaa näyttöön **"Create a Database Connection"**.

![Luo tietokantayhteys](images/data_source_config_input_mask.png)

---

## Natiivinen Python-ajuri

**Kirjasto:** `pymssql`  
**Tuettu todennus:** Vain salasanaan perustuva todennus

> Muihin todennusmenetelmiin tarkoitettu yhteys kannattaa tehdä ODBC-ajurin kautta.

### *digna* -konfiguraatio (natiiviajuri)

Anna seuraavat tiedot näytössä **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-ajuri

ODBC-ajuri voi tukea laajempaa valikoimaa todennus- ja yhteysvaihtoehtoja. Tässä osiossa keskitytään salasanaan perustuvaan todennukseen käyttäen ajuria **ODBC Driver 18 for SQL Server**.

### 1. Asenna ODBC-ajuri

Asenna ajuri **ODBC Driver 18 for SQL Server** (tai vastaava) seuraamalla toimittajan virallista asennusohjetta.

### 2. Määritä ODBC-tietolähde

Seuraa näitä vaiheita määrittääksesi uuden ODBC-tietolähteen käyttäen salasanaan perustuvaa todennusta:

#### Vaihe 1
![Vaihe 1](images/azure_synapse/create_odbc_data_source_step1.png)

Täytä "Server"-kenttä.  
Käytä Synapse-työtilan nimeä ja lisää siihen ".sql.azuresynapse.net".  
**Huom**, jos haluat yhdistää serverless SQL -pooliin, varmista että lisäät "-ondemand" kuten alla olevassa kuvakaappauksessa.

Klikkaa **Next >** -painiketta.

#### Vaihe 2
![Vaihe 2](images/azure_synapse/create_odbc_data_source_step2.png)

Valitse todennusmenetelmä (esim. käyttäjätunnus ja salasana)
ja anna vaaditut tiedot.

Klikkaa **Next >** -painiketta.

#### Vaihe 3
![Vaihe 3](images/azure_synapse/create_odbc_data_source_step3.png)

Valitse ANSI-yhteensopivat asetukset ja klikkaa **Next >** -painiketta.

#### Vaihe 4
![Vaihe 4](images/azure_synapse/create_odbc_data_source_step4.png)

Voit jättää oletusasetukset tai valita tarpeelliset vaihtoehdot 
ja klikata **Finish** -painiketta. 

#### Vaihe 5
![Vaihe 5](images/azure_synapse/create_odbc_data_source_step5.png)

Klikkaa nyt **Test datasource** -painiketta.

#### Vaihe 6
![Vaihe 6](images/azure_synapse/create_odbc_data_source_step6.png)

Kun näet onnistumisnäytön, ODBC on konfiguroitu oikein.

---

Nyt voit konfiguroida *digna*:n käyttämään ODBC-yhteyttä joko **DSN (Data Source Name)** -pohjaisesti tai **DSN-vapaana**.

---

### A. DSN-pohjainen konfigurointi

#### *digna* -konfiguraatio

Näytössä **"Create a Database Connection"** anna seuraavat tiedot:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-ominaisuudet

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> `DSN`-arvon pitää vastata ODBC-ajurin konfiguroinnissa määriteltyä nimeä.

---

### B. DSN-vapaa konfigurointi

#### *digna* -konfiguraatio

Näytössä **"Create a Database Connection"** anna seuraavat tiedot:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-ominaisuudet

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Huomautus** SERVER-ominaisuudesta:  
Käytä Synapse-työtilan nimeä ja lisää siihen ".sql.azuresynapse.net". Jos haluat yhdistää serverless SQL -pooliin, varmista että lisäät "-ondemand" kuten alla olevassa kuvassa.