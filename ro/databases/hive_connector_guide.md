# Conector sursă pentru Hive

Acest ghid descrie cum să configurezi *digna* pentru a se conecta la Hive folosind fie conectorul Python nativ, fie driverul ODBC.

Se face referire la ecranul **"Creează o conexiune la bază de date"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Driver Python nativ

**Library:** `PyHive`  
**Autentificare acceptată:** Doar autentificare pe bază de parolă

> Pentru alte metode de autentificare, utilizează driverul ODBC.

### Configurare *digna* (Driver nativ)

Furnizează următoarele informații în ecranul **"Creează o conexiune la bază de date"**:

```
Technology:      Apache Hive
Host Address:    Numele serverului sau adresa IP
Host Port:       Numărul portului, ex. 10000
Database Name:   Schema care conține datele sursă
Schema Name:     Schema care conține datele sursă
User Name:       Numele de utilizator al bazei de date
User Password:   Parola utilizatorului
Use ODBC:        Dezactivat (implicit)
```

---

## Driver ODBC

Driverul ODBC poate suporta o gamă mai largă de opțiuni de autentificare și conectivitate. Această secțiune se concentrează pe autentificarea pe bază de parolă folosind driverul **Cloudera ODBC Driver for Apache Hive**.

### 1. Instalează driverul ODBC

Instalează **Cloudera ODBC Driver for Apache Hive** (sau un driver similar) urmând ghidul oficial de instalare al furnizorului.

### 2. Configurează sursa de date ODBC

Urmărește pașii pentru a configura o nouă sursă de date ODBC folosind autentificare pe bază de parolă:

#### Pasul 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Pasul 2 – Testează conexiunea

Furnizează parola și apasă butonul **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

După un test reușit, apasă butonul **OK**.

---

Acum poți configura *digna* să folosească conexiunea ODBC, fie cu **DSN (Data Source Name)**, fie într-o configurație **fără DSN**.

---

### A. Configurare bazată pe DSN

#### Configurare *digna*

În ecranul **"Creează o conexiune la bază de date"**, furnizează următoarele:

```
Technology:      Apache Hive
Database Name:   Schema care conține datele sursă (aceeași cu Schema Name)
Schema Name:     Schema care conține datele sursă
Use ODBC:        Activat
```

#### Proprietăți ODBC

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{parola ta între acolade}"
```

> `DSN` trebuie să corespundă numelui definit în configurația driverului ODBC.

---

### B. Configurare fără DSN

#### Configurare *digna*

În ecranul **"Creează o conexiune la bază de date"**, furnizează următoarele:

```
Technology:      Apache Hive
Database Name:   Schema care conține datele sursă (aceeași cu Schema Name)
Schema Name:     Schema care conține datele sursă
Use ODBC:        Activat
```

#### Proprietăți ODBC

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "numele serverului tău sau adresa IP"
name: "PORT",       value: "Numărul portului, ex. 10000"
name: "Schema",     value: "Schema care conține datele sursă"
name: "UID",        value: "utilizatorul tău hive"
name: "PWD",        value: "parola ta Hive"
name: "AuthMech",   value: "3"
```