# Allikapistik (Source Connector) Hive'ile

See juhend kirjeldab, kuidas konfigureerida *digna* ühenduma Hive'iga kas natiivse Pythoni ühendaja või ODBC draiveri kaudu.

See viitab ekraanile **"Loo andmebaasiühendus"**.

![Loo andmebaasiühendus](images/data_source_config_input_mask.png)

---

## Natiivne Pythoni draiver

**Raamatukogu:** `PyHive`  
**Toetatav autentimine:** Ainult paroolipõhine autentimine

> Muude autentimisviiside jaoks kasutage ODBC-draiverit.

### *digna* konfiguratsioon (natiivne draiver)

Sisestage järgmine teave ekraanil **"Loo andmebaasiühendus"**:

```
Tehnoloogia:      Apache Hive
Hosti aadress:    Serveri nimi või IP-aadress
Hosti port:       Pordinumbr, nt 10000
Andmebaasi nimi:   Skeem, mis sisaldab allikaandmeid
Skeemi nimi:      Skeem, mis sisaldab allikaandmeid
Kasutajanimi:     Andmebaasi kasutajanimi
Kasutaja parool:  Kasutaja parool
Kasuta ODBC:      Keelatud (vaikimisi)
```

---

## ODBC draiver

ODBC draiver võib toetada laiemat valikut autentimis- ja ühendusvalikuid. See lõik keskendub paroolipõhisele autentimisele draiveriga **Cloudera ODBC Driver for Apache Hive**.

### 1. Paigaldage ODBC draiver

Paigaldage **Cloudera ODBC Driver for Apache Hive** (või sarnane) vastavalt tootja ametlikule paigaldusjuhisele.

### 2. Konfigureerige ODBC andmeallikas

Järgige neid samme uue ODBC andmeallika konfigureerimiseks, kasutades paroolipõhist autentimist:

#### Samm 1
![Samm 1](images/hive/create_odbc_data_source_step1.png)


#### Samm 2 – Testige ühendust

Sisestage parool ja klõpsake nuppu **Test**.

![Samm 2](images/hive/create_odbc_data_source_step2.png)

Pärast edukat testi klõpsake nuppu **OK**.

---

Nüüd saate konfigureerida *digna* kasutama ODBC-ühendust kas **DSN (Data Source Name)** või **DSN-vaba** seadistuse kaudu.

---

### A. DSN-põhine konfiguratsioon

#### *digna* konfiguratsioon

Ekraanil **"Loo andmebaasiühendus"** sisestage järgmine:

```
Tehnoloogia:      Apache Hive
Andmebaasi nimi:   Skeem, mis sisaldab allikaandmeid (sama mis Skeemi nimi)
Skeemi nimi:       Skeem, mis sisaldab allikaandmeid
Kasuta ODBC:       Lubatud
```

#### ODBC omadused

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{your password in curly braces}"
```

> `DSN` peab vastama teie ODBC draiveri konfiguratsioonis määratud nimele.

---

### B. DSN-vaba konfiguratsioon

#### *digna* konfiguratsioon

Ekraanil **"Loo andmebaasiühendus"** sisestage järgmine:

```
Tehnoloogia:      Apache Hive
Andmebaasi nimi:   Skeem, mis sisaldab allikaandmeid (sama mis Skeemi nimi)
Skeemi nimi:       Skeem, mis sisaldab allikaandmeid
Kasuta ODBC:       Lubatud
```

#### ODBC omadused

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 10000"
name: "Schema",     value: "Schema that contains the source data"
name: "UID",        value: "your hive user'
name: "PWD",        value: "your hive password"
name: "AuthMech",   value: "3"
```