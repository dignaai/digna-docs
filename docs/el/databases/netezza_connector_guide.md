---
title: Netezza Connector – Ενσωμάτωση Βάσης Δεδομένων | Τεκμηρίωση digna
description: Διαμορφώστε το digna ώστε να συνδεθεί με το Netezza χρησιμοποιώντας τον ODBC driver NetezzaSQL. Υποστηρίζει αυθεντικοποίηση με κωδικό μέσω DSN ή DSN-less ρυθμίσεων για ευέλικτη συνδεσιμότητα.
image: /assets/logo_square.png
---


# Source Connector for Netezza

Αυτός ο οδηγός περιγράφει πώς να διαμορφώσετε το *digna* ώστε να συνδεθεί με το Netezza χρησιμοποιώντας τον ODBC driver.

Αναφέρεται στην οθόνη **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## ODBC Driver

Ο ODBC driver μπορεί να υποστηρίζει διάφορες επιλογές αυθεντικοποίησης και συνδεσιμότητας. Αυτή η ενότητα εστιάζει στην αυθεντικοποίηση με κωδικό χρησιμοποιώντας τον driver **NetezzaSQL**.

### 1. Install the ODBC Driver

Εγκαταστήστε τον driver **NetezzaSQL** (ή παρόμοιο) ακολουθώντας τον επίσημο οδηγό εγκατάστασης του προμηθευτή.

### 2. Configure the ODBC Data Source

Ακολουθήστε αυτά τα βήματα για να διαμορφώσετε μια νέα πηγή δεδομένων ODBC χρησιμοποιώντας αυθεντικοποίηση με κωδικό:

#### Step 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Ανάλογα με τον Netezza driver σας, τις απαιτήσεις εγκατάστασης και ασφάλειας, μπορεί να χρειαστεί να εισαγάγετε επίσης δεδομένα στις καρτέλες **Advanced DSN Options**, **SSL DSN Options** ή **Driver Options**. Για την πιο απλή ρύθμιση αρκεί να εισάγετε δεδομένα στην καρτέλα **DSN Options**.

Κάντε κλικ στο κουμπί **Test Connection**.

#### Step 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Όταν λάβετε την οθόνη επιτυχίας, ο ODBC έχει ρυθμιστεί σωστά.

---

Τώρα μπορείτε να διαμορφώσετε το *digna* ώστε να χρησιμοποιήσει τη σύνδεση ODBC, είτε με **DSN (Data Source Name)** είτε με ρύθμιση **DSN-less**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Στην οθόνη **"Create a Database Connection"**, εισάγετε τα εξής:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 Το `DSN` πρέπει να ταιριάζει με το όνομα που έχει οριστεί στη ρύθμιση του ODBC driver σας.

---

### B. DSN-less Configuration

#### *digna* Configuration

Στην οθόνη **"Create a Database Connection"**, εισάγετε τα εξής:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```