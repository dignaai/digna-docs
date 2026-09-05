# Source Connector for MS SQL Server

Acest ghid descrie cum să configurezi *digna* pentru a se conecta la SQLServer folosind fie conectorul nativ Python, fie driverul ODBC.

Se face referire la ecranul **"Creare conexiune la bază de date"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Supported Authentication:** Autentificare bazată pe parolă doar

> Pentru alte metode de autentificare, te rugăm să folosești driverul ODBC.

### *digna* Configuration (Native Driver)

Furnizează următoarele informații în ecranul **"Creare conexiune la bază de date"**:

```
Technology:      MS SQL Server
Host Address:    Nume server sau adresă IP
Host Port:       Număr port, de ex. 1433
Database Name:   Numele bazei de date
Schema Name:     Schema care conține datele sursă
User Name:       Numele de utilizator al bazei de date
User Password:   Parola utilizatorului
Use ODBC:        Dezactivat (implicit)
```

---

## ODBC Driver

Driverul ODBC poate suporta o gamă mai largă de opțiuni de autentificare și conectivitate. Această secțiune se concentrează pe autentificarea bazată pe parolă folosind driverul **SQL Server**.

### 1. Install the ODBC Driver

Instalează driverul **SQL Server** (sau similar) urmând ghidul oficial de instalare al furnizorului.

### 2. Configure the ODBC Data Source

Urmează pașii de mai jos pentru a configura o nouă sursă de date ODBC folosind autentificare bazată pe parolă:

#### Step 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Apasă butonul **Next >**.

#### Step 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Alege metoda de autentificare (de ex. utilizator și parolă)
și furnizează datele necesare.

Apasă butonul **Next >**.

#### Step 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Alege setările compatibile ANSI, apoi apasă butonul **Next >**.

#### Step 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Poți lăsa setările implicite sau alege opțiuni de logging după necesități 
și apasă butonul **Finish**. 

#### Step 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Acum apasă butonul **Test datasource**.

#### Step 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

Când primești ecranul de succes, ODBC este configurat corect.

---

Acum poți configura *digna* să folosească conexiunea ODBC, fie cu un **DSN (Data Source Name)**, fie cu o configurație **fără DSN**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

În ecranul **"Creare conexiune la bază de date"**, furnizează următoarele:

```
Technology:      MS SQL Server
Database Name:   Baza de date care conține schema sursă
Schema Name:     Schema care conține datele sursă
Use ODBC:        Activat
```

#### ODBC Properties

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "utilizatorul bazei de date"
name: "PWD",        value: "parola bazei de date"
name: "DATABASE",   value: "numele bazei de date care conține schema cu datele sursă"

```

> `DSN` trebuie să corespundă cu numele definit în configurația driverului ODBC.

---

### B. DSN-less Configuration

#### *digna* Configuration

În ecranul **"Creare conexiune la bază de date"**, furnizează următoarele:

```
Technology:      MS SQL Server
Database Name:   Schema care conține datele sursă (aceeași ca Schema Name)
Schema Name:     Schema care conține datele sursă
Use ODBC:        Activat
```

#### ODBC Properties

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "numele serverului sau adresa IP"
name: "UID",        value: "utilizatorul bazei de date"
name: "PWD",        value: "parola bazei de date"
name: "DATABASE",   value: "numele bazei de date care conține schema cu datele sursă"
```