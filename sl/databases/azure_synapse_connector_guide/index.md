# Vhodni konektor za Azure Synapse Analytics

Ta vodič opisuje, kako konfigurirati *digna*, da se poveže z Azure Synapse Analytics z uporabo bodisi izvornega Python konektorja ali ODBC gonilnika.
Podpira tako serverless kot dedicated SQL poole.

Sklicuje se na zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Izvorni Python gonilnik

**Knjižnica:** `pymssql`  
**Podprta avtentikacija:** Samo avtentikacija z geslom

> Za druge metode avtentikacije uporabite ODBC gonilnik.

### Konfiguracija *digna* (izvorni gonilnik)

Vnesite naslednje podatke na zaslonu **"Create a Database Connection"**:

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

## ODBC gonilnik

ODBC gonilnik lahko podpira širši nabor možnosti avtentikacije in povezljivosti. Ta razdelek se osredotoča na avtentikacijo z geslom z uporabo gonilnika **ODBC Driver 18 for SQL Server**.

### 1. Namestite ODBC gonilnik

Namestite gonilnik **ODBC Driver 18 for SQL Server** (ali podoben) tako, da sledite uradnemu navodilu za namestitev ponudnika.

### 2. Konfigurirajte ODBC podatkovni vir

Sledite tem korakom za konfiguracijo novega ODBC podatkovnega vira z avtentikacijo na osnovi gesla:

#### Korak 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Izpolnite polje "Server".
Uporabite ime synapse delovnega prostora in ga razširite z ".sql.azuresynapse.net".  
**Pozor**, če se želite povezati z uporabo serverless SQL poola, poskrbite, da vključite "-ondemand", kot je prikazano na spodnji sliki.

Kliknite gumb **Next >**.

#### Korak 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Izberite metodo avtentikacije (npr. uporabniško ime in geslo)
in vnesite zahtevane podatke.

Kliknite gumb **Next >**.

#### Korak 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Izberite ANSI združljive nastavitve, nato kliknite gumb **Next >**.

#### Korak 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Lahko pustite privzete nastavitve ali izberete možnosti po potrebi 
in kliknite gumb **Finish**. 

#### Korak 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Zdaj kliknite gumb **Test datasource**.

#### Korak 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Ko prejmete zaslon s potrditvijo uspeha, je ODBC pravilno konfiguriran.

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC povezavo, bodisi z **DSN (Data Source Name)** ali z **DSN-less** nastavkom.

---

### A. Konfiguracija na osnovi DSN

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> `DSN` mora ustrezati imenu, definiranemu v nastavitvi vašega ODBC gonilnika.

---

### B. DSN-less konfiguracija

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Opomba** glede lastnosti SERVER:  
Uporabite ime synapse delovnega prostora in ga razširite z ".sql.azuresynapse.net". Če se želite povezati z uporabo serverless SQL poola, poskrbite, da vključite "-ondemand", kot je prikazano na spodnji sliki.