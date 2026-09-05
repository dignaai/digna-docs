# PostgreSQL-i lähteühendaja

See juhend kirjeldab, kuidas konfigureerida *digna* ühenduma Postgresiga kas natiivse Python-ühendaja või ODBC-draiveri abil.

See viitab ekraanile **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natiivne Python-draiver

**Library:** `psycopg`  
**Toetatav autentimine:** Ainult paroolipõhine autentimine

> Muude autentimismeetodite jaoks kasutage palun ODBC-draiverit.

### *digna* konfiguratsioon (natiivne draiver)

Sisestage järgmine info ekraanil **"Create a Database Connection"**:

```
Technology:      Postgres
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 5432
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-draiver

ODBC-draiver võib toetada laiemat valikut autentimis- ja ühenduvusvõimalusi. See jaotis keskendub paroolipõhisele autentimisele, kasutades draiverit **PostgreSQL Unicode(x64)**.

### 1. Paigaldage ODBC-draiver

Paigaldage **PostgreSQL Unicode(x64)** (või sarnane) järgides tootja ametlikku paigaldusjuhendit.

### 2. Konfigureerige ODBC-andmeallikas

Järgige neid samme uue ODBC-andmeallika konfigureerimiseks paroolipõhise autentimisega:

#### Samm 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Märkus: Kui teie andmebaasi seadistus nõuab konkreetse "SSLMode" valimist, veenduge, et kasutaksite sama ka DSN-ita konfiguratsiooni määratlemisel.

#### Samm 2 – Testige ühendust

Klõpsake nuppu **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Nüüd saate konfigureerida *digna* kasutama ODBC-ühendust kas **DSN (Data Source Name)** või **DSN-ita** seadistusega.

---

### A. DSN-põhine konfiguratsioon

#### *digna* konfiguratsioon

Ekraanil **"Create a Database Connection"** sisestage järgmine:

```
Technology:      PostgreSQL
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-omadused

```
name: "DSN",    value: "PostgreSQL35W"
```

> `DSN` peab vastama nimele, mis on määratletud teie ODBC-draiveri konfiguratsioonis.

---

### B. DSN-ita konfiguratsioon

#### *digna* konfiguratsioon

Ekraanil **"Create a Database Connection"** sisestage järgmine:

```
Technology:      PostgreSQL
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-omadused

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```