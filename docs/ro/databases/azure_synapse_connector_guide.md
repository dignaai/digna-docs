---
title: Azure Synapse Connector – Integrare Bază de Date | digna Documentation
description: Configurați digna pentru a se conecta la Azure Synapse Analytics folosind fie driverul nativ Python, fie driverul ODBC. Suportă atât pool-urile SQL serverless, cât și cele dedicate.
image: /assets/logo_square.png
---


# Source Connector for Azure Synapse Analytics

Acest ghid descrie cum să configurați *digna* pentru a se conecta la Azure Synapse Analytics folosind fie conectorul nativ Python, fie driverul ODBC.
Este compatibil atât cu pool-urile SQL serverless, cât și cu cele dedicate.

Se face referire la ecranul **"Create a Database Connection"**.

![Creează o conexiune la baza de date](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Supported Authentication:** Autentificare pe bază de parolă (doar)

> Pentru alte metode de autentificare, vă rugăm să folosiți driverul ODBC.

### Configurarea *digna* (Driver nativ)

Furnizați următoarele informații în ecranul **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Numele bazei de date
Schema Name:     Schema care conține datele sursă
User Name:       Numele utilizatorului bazei de date
User Password:   Parola utilizatorului
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Driverul ODBC poate oferi un set mai larg de opțiuni de autentificare și conectivitate. Această secțiune se concentrează pe autentificarea pe bază de parolă folosind driverul **ODBC Driver 18 for SQL Server**.

### 1. Instalați driverul ODBC

Instalați driverul **ODBC Driver 18 for SQL Server** (sau unul similar) urmând ghidul oficial de instalare al furnizorului.

### 2. Configurați sursa de date ODBC

Urmați acești pași pentru a configura o nouă sursă de date ODBC folosind autentificare pe bază de parolă:

#### Pasul 1
![Pasul 1](images/azure_synapse/create_odbc_data_source_step1.png)

Completează câmpul "Server".
Folosiți numele workspace-ului Synapse și adăugați sufixul ".sql.azuresynapse.net".   
**Atenție**, dacă doriți să vă conectați folosind un serverless SQL pool, asigurați-vă că includeți "-ondemand" așa cum se arată în captura de ecran de mai jos.

Faceți clic pe butonul **Next >**.

#### Pasul 2
![Pasul 2](images/azure_synapse/create_odbc_data_source_step2.png)

Alegeți metoda de autentificare (de ex. nume de utilizator și parolă)
și furnizați datele necesare.

Faceți clic pe butonul **Next >**.

#### Pasul 3
![Pasul 3](images/azure_synapse/create_odbc_data_source_step3.png)

Alegeți setările conforme ANSI, apoi faceți clic pe butonul **Next >**.

#### Pasul 4
![Pasul 4](images/azure_synapse/create_odbc_data_source_step4.png)

Puteți lăsa setările implicite sau alege opțiuni după necesitate
și faceți clic pe butonul **Finish**. 

#### Pasul 5
![Pasul 5](images/azure_synapse/create_odbc_data_source_step5.png)

Acum faceți clic pe butonul **Testează sursa de date**.

#### Pasul 6
![Pasul 6](images/azure_synapse/create_odbc_data_source_step6.png)

Când primiți ecranul de succes, ODBC este configurat corect.

---

Acum puteți configura *digna* să utilizeze conexiunea ODBC, fie cu un **DSN (Data Source Name)**, fie o configurare **fără DSN (DSN-less)**.

---

### A. Configurare bazată pe DSN

#### Configurarea *digna*

În ecranul **"Create a Database Connection"**, furnizați următoarele:

```
Technology:      MS SQL Server
Database Name:   Baza de date care conține schema sursă
Schema Name:     Schema care conține datele sursă
Use ODBC:        Enabled
```

#### Proprietăți ODBC

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "utilizatorul bazei de date"
name: "PWD",        value: "parola utilizatorului bazei de date"
name: "DATABASE",   value: "numele bazei de date care conține schema de date sursă"

```

> `DSN` trebuie să corespundă numelui definit în configurația driverului ODBC.

---

### B. Configurare fără DSN (DSN-less)

#### Configurarea *digna*

În ecranul **"Create a Database Connection"**, furnizați următoarele:

```
Technology:      MS SQL Server
Database Name:   Schema care conține datele sursă (același ca Schema Name)
Schema Name:     Schema care conține datele sursă
Use ODBC:        Enabled
```

#### Proprietăți ODBC

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "utilizatorul bazei de date"
name: "PWD",        value: "parola utilizatorului bazei de date"
name: "DATABASE",   value: "numele bazei de date care conține schema de date sursă"
```

**Notă** referitoare la proprietatea SERVER:  
Folosiți numele workspace-ului Synapse și adăugați sufixul ".sql.azuresynapse.net". Dacă doriți să vă conectați folosind un serverless SQL pool, asigurați-vă că includeți "-ondemand" așa cum se arată în captura de ecran de mai jos.