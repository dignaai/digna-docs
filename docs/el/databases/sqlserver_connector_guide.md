---
title: Συνδετήρας MS SQL Server – Ενσωμάτωση Βάσης Δεδομένων | Τεκμηρίωση digna
description: Διαμορφώστε το digna για σύνδεση με Microsoft SQL Server χρησιμοποιώντας τον Python οδηγό pymssql ή τον ODBC οδηγό SQL Server. Υποστηρίζει έλεγχο ταυτότητας με κωδικό σε ρυθμίσεις με DSN ή χωρίς DSN.
image: /assets/logo_square.png
---


# Source Connector for MS SQL Server

Ο παρών οδηγός περιγράφει πώς να διαμορφώσετε το *digna* ώστε να συνδεθεί με SQL Server είτε χρησιμοποιώντας τον γηγενή Python connector είτε τον ODBC driver.

Αναφέρεται στην οθόνη **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Υποστηριζόμενος Έλεγχος Ταυτότητας:** Μόνο έλεγχος ταυτότητας με κωδικό (password)

> ⚠️ Για άλλες μεθόδους ελέγχου ταυτότητας, χρησιμοποιήστε τον ODBC driver.

### *digna* Ρυθμίσεις (Native Driver)

Παρέχετε τις παρακάτω πληροφορίες στην οθόνη **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Ο ODBC driver μπορεί να υποστηρίζει ευρύτερο φάσμα επιλογών ελέγχου ταυτότητας και συνδεσιμότητας. Αυτή η ενότητα επικεντρώνεται στον έλεγχο ταυτότητας με κωδικό χρησιμοποιώντας τον οδηγό **SQL Server**.

### 1. Εγκατάσταση του ODBC Driver

Εγκαταστήστε τον οδηγό **SQL Server** (ή παρόμοιο) ακολουθώντας τον επίσημο οδηγό εγκατάστασης του κατασκευαστή.

### 2. Διαμόρφωση της Πηγής Δεδομένων ODBC

Ακολουθήστε αυτά τα βήματα για να διαμορφώσετε μια νέα πηγή δεδομένων ODBC χρησιμοποιώντας έλεγχο ταυτότητας με κωδικό:

#### Βήμα 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Κάντε κλικ στο κουμπί **Next >**.

#### Βήμα 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Επιλέξτε τη μέθοδο ελέγχου ταυτότητας (π.χ. όνομα χρήστη και κωδικός) και εισάγετε τα απαιτούμενα δεδομένα.

Κάντε κλικ στο κουμπί **Next >**.

#### Βήμα 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Επιλέξτε τις ρυθμίσεις συμβατές με ANSI και στη συνέχεια κάντε κλικ στο κουμπί **Next >**.

#### Βήμα 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Μπορείτε να αφήσετε τις προεπιλεγμένες ρυθμίσεις ή να επιλέξετε επιλογές καταγραφής (logging) όπως απαιτείται και να κάνετε κλικ στο κουμπί **Finish**. 

#### Βήμα 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Τώρα κάντε κλικ στο κουμπί ** Test datasource **.

#### Βήμα 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

Όταν λάβετε την οθόνη επιτυχίας, ο ODBC έχει διαμορφωθεί σωστά.

---

Τώρα μπορείτε να διαμορφώσετε το *digna* ώστε να χρησιμοποιήσει τη σύνδεση ODBC, είτε με **DSN (Data Source Name)** είτε με ρύθμιση **χωρίς DSN (DSN-less)**.

---

### A. DSN-Based Configuration

#### *digna* Ρυθμίσεις

Στην οθόνη **"Create a Database Connection"**, παρέχετε τα εξής:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Ιδιότητες ODBC

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 Το `DSN` πρέπει να ταιριάζει με το όνομα που έχει οριστεί στη διαμόρφωση του ODBC driver.

---

### B. DSN-less Configuration

#### *digna* Ρυθμίσεις

Στην οθόνη **"Create a Database Connection"**, παρέχετε τα εξής:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Ιδιότητες ODBC

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```