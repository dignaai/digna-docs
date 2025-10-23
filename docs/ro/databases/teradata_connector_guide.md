---
title: Conector Teradata – Integrare bază de date | Documentația digna
description: Configurați *digna* pentru a se conecta la Teradata folosind driverul Python `teradatasql` sau driverul ODBC Teradata. Suportă autentificare pe bază de parolă cu configurații DSN sau fără DSN.
image: /assets/logo_square.png
---


# Source Connector for Teradata

Acest ghid descrie cum să configurați *digna* pentru a se conecta la Teradata folosind fie conectorul Python nativ, fie driverul ODBC.

Se face referire la ecranul **"Create a Database Connection"**.

![Creează o conexiune la baza de date](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `teradatasql`  
**Supported Authentication:** Autentificare pe bază de parolă doar

> ⚠️ Pentru alte metode de autentificare, vă rugăm să folosiți driverul ODBC.

### *digna* Configuration (Native Driver)

Furnizați următoarele informații în ecranul **"Create a Database Connection"**:

```
Tehnologie:      Teradata
Adresa gazdă:    Numele serverului sau adresa IP
Port gazdă:      Numărul portului, ex. 1025
Nume bază date:  Numele bazei de date
Nume schemă:     Numele bazei de date
Nume utilizator: Numele utilizatorului bazei de date
Parolă utilizator: Parola utilizatorului
Utilizare ODBC:  Dezactivat (implicit)
```

---

## ODBC Driver

Driverul ODBC poate suporta o gamă mai largă de opțiuni de autentificare și conectivitate. Această secțiune se concentrează pe autentificarea pe bază de parolă folosind driverul **Teradata Database ODBC Driver 20.00**.

### 1. Install the ODBC Driver

Instalați driverul **Teradata Database ODBC Driver 20.00** (sau similar) urmând ghidul oficial de instalare al vendorului.

### 2. Configure the ODBC Data Source

Urmați pașii de mai jos pentru a configura un nou data source ODBC folosind autentificare pe bază de parolă:

#### Pasul 1
![Pasul 1](images/teradata/create_odbc_data_source_step1.png)

Faceți clic pe butonul **Test**.

#### Pasul 2
![Pasul 2](images/teradata/create_odbc_data_source_step2.png)

Introduceți numele de utilizator și parola.

Faceți clic pe butonul **OK**.  
Când primiți ecranul de succes, ODBC este configurat corect.

---

Acum puteți configura *digna* să utilizeze conexiunea ODBC, fie cu un **DSN (Data Source Name)**, fie cu o configurare **fără DSN**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

În ecranul **"Create a Database Connection"**, furnizați următoarele:

```
Tehnologie:      Teradata
Nume bază date:  Baza de date care conține schema sursă
Nume schemă:     Schema care conține datele sursă
Utilizare ODBC:  Activat
```

#### ODBC Properties

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "utilizatorul bazei de date"
name: "PWD",        value: "parola bazei de date"
```

> 🔹 `DSN` trebuie să corespundă numelui definit în configurația driverului ODBC.

---

### B. DSN-less Configuration

#### *digna* Configuration

În ecranul **"Create a Database Connection"**, furnizați următoarele:

```
Tehnologie:      Teradata
Nume bază date:  Schema care conține datele sursă (același ca Nume schemă)
Nume schemă:     Schema care conține datele sursă
Utilizare ODBC:  Activat
```

#### ODBC Properties

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "numele serverului sau adresa IP"
name: "UID",        value: "utilizatorul bazei de date"
name: "PWD",        value: "parola bazei de date"
```