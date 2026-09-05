# Netezzai andmeallika ühendaja

See juhend kirjeldab, kuidas konfigureerida *digna* ühendamaks Netezzaga, kasutades ODBC-draiverit.

See viitab ekraanile **"Create a Database Connection"**.

![Loo andmebaasiühendus](images/data_source_config_input_mask.png)

---

## ODBC-draiver

ODBC-draiver võib toetada erinevaid autentimis- ja ühenduse valikuid. See jaotis keskendub paroolipõhisele autentimisele, kasutades draiverit **NetezzaSQL**.

### 1. Installige ODBC-draiver

Installige draiver **NetezzaSQL** (või sarnane) järgides tootja ametlikku paigaldusjuhendit.

### 2. Konfigureerige ODBC-andmeallikas

Järgige neid samme, et konfigureerida uus ODBC-andmeallikas, kasutades paroolipõhist autentimist:

#### Step 1
![Samm 1](images/netezza/create_odbc_data_source_step1.png)

Sõltuvalt teie Netezza draiverist, seadistuse ja turvanõuetest võib olla vajalik täita ka vahekaardid **Advanced DSN Options**, **SSL DSN Options** või **Driver Options**. Lihtsama seadistuse puhul piisab andmete sisestamisest vahekaardil **DSN Options**.

Klõpsake nuppu **Test Connection**.

#### Step 2
![Samm 2](images/netezza/create_odbc_data_source_step2.png)

Kui näete edukuse ekraani, on ODBC õigesti konfigureeritud.

---

Nüüd saate konfigureerida *digna* kasutamaks ODBC-ühendust kas läbi **DSN (Data Source Name)** või **DSN-vaba** seadistuse.

---

### A. DSN-põhine konfiguratsioon

#### *digna* konfigureerimine

Ekraanil **"Create a Database Connection"** täitke järgmised väljad:

```
Technology:      Netezza
Database Name:   Andmebaas, mis sisaldab lähte skeemi
Schema Name:     Skeem, mis sisaldab lähteandmeid
Use ODBC:        Enabled
```

#### ODBC atribuudid

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "teie andmebaasi kasutaja"
name: "PWD",        value: "teie andmebaasi parool"
```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-vaba konfiguratsioon

#### *digna* konfigureerimine

Ekraanil **"Create a Database Connection"** täitke järgmised väljad:

```
Technology:      Netezza
Database Name:   Skeem, mis sisaldab lähteandmeid (sama mis Schema Name)
Schema Name:     Skeem, mis sisaldab lähteandmeid
Use ODBC:        Enabled
```

#### ODBC atribuudid

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "teie serveri nimi või IP-aadress"
name: "PORT",       value: "Pordi number, nt 5480"
name: "DATABASE",   value: "andmebaasi nimi, mis sisaldab lähteandmete skeemi"
name: "UID",        value: "teie andmebaasi kasutaja"
name: "PWD",        value: "teie andmebaasi parool"
```