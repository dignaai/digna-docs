# Allika konnektor Oracle'i jaoks

See juhend kirjeldab, kuidas konfigureerida *digna* ühendamaks Oracle DB-ga, kasutades kas natiivset Pythoni konnektorit või ODBC draiverit.

See viitab ekraanile **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natiivne Pythoni draiver

**Raamatukogu:** `python-oracledb`  
**Toetatud autentimine:** Ainult paroolipõhine autentimine

> Kui soovite muid autentimismeetodeid, kasutage ODBC draiverit.

### *digna* konfiguratsioon (natiivne draiver)

Esitage järgmine info ekraanil **"Create a Database Connection"**:

```
Technology:      Oracle
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1521
Database Name:   Instance name, service name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC draiver

ODBC draiver võib toetada laiemat valikut autentimis- ja ühendusvõimalusi. See jaotis keskendub paroolipõhisele autentimisele, kasutades draiverit **Oracle in OraDB21Home1**.

### 1. Installige ODBC draiver

Installige **Oracle in OraDB21Home1** (või sarnane) järgides tootja ametlikku installijuhendit.

### 2. Konfigureerige ODBC andmeallikas

Järgige neid samme, et konfigureerida uus ODBC andmeallikas paroolipõhise autentimisega:

#### Samm 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Märkus:
TNS Service Name peab olema konfigureeritud teie Oracle kliendi tnsnames.ora failis. Siin määratlete ühenduse kirjelduse (host, port, service name).

#### Samm 2 – Testi ühendus

Klõpsake nuppu **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Sisestage parool ja klõpsake **OK** nuppu.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Nüüd saate konfigureerida *digna* ODBC ühenduse kasutamiseks kas **DSN (Data Source Name)** või **DSN-ita** seadistusega.

---

### A. DSN-põhine konfiguratsioon

#### *digna* konfiguratsioon

Ekraanil **"Create a Database Connection"** esitage järgmine:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC omadused

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> `DSN` peab vastama nimele, mis on määratud teie ODBC draiveri konfiguratsioonis.

---

### B. DSN-ita konfiguratsioon

#### *digna* konfiguratsioon

Ekraanil **"Create a Database Connection"** esitage järgmine:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC omadused

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```