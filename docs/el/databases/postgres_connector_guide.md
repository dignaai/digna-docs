---
title: Σύνδεση PostgreSQL – Ενοποίηση Βάσης Δεδομένων | Τεκμηρίωση digna
description: Ρυθμίστε το digna για σύνδεση με PostgreSQL χρησιμοποιώντας τον psycopg Python driver ή τον ODBC driver του PostgreSQL. Υποστηρίζει έλεγχο ταυτότητας με κωδικό πρόσβασης σε ρυθμίσεις με DSN ή χωρίς DSN.
image: /assets/logo_square.png
---


# Source Connector for PostgreSQL

Αυτός ο οδηγός περιγράφει πώς να ρυθμίσετε το *digna* για να συνδεθεί σε Postgres είτε χρησιμοποιώντας τον εγγενή Python connector είτε τον οδηγό ODBC.

Αναφέρεται στην οθόνη **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Βιβλιοθήκη:** `psycopg`  
**Υποστηριζόμενος Έλεγχος Ταυτότητας:** Μόνο έλεγχος ταυτότητας βάσει κωδικού πρόσβασης

> Για άλλες μεθόδους ελέγχου ταυτότητας, παρακαλώ χρησιμοποιήστε τον οδηγό ODBC.

### Ρύθμιση του *digna* (Εγγενής Driver)

Παρέχετε τις ακόλουθες πληροφορίες στην οθόνη **"Create a Database Connection"**:

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

## ODBC Driver

Ο οδηγός ODBC ενδέχεται να υποστηρίζει ευρύτερο φάσμα επιλογών ελέγχου ταυτότητας και συνδεσιμότητας. Αυτή η ενότητα επικεντρώνεται στον έλεγχο ταυτότητας με κωδικό πρόσβασης χρησιμοποιώντας τον οδηγό **PostgreSQL Unicode(x64)**.

### 1. Install the ODBC Driver

Εγκαταστήστε τον **PostgreSQL Unicode(x64)** (ή παρόμοιο) ακολουθώντας τον επίσημο οδηγό εγκατάστασης του προμηθευτή.

### 2. Configure the ODBC Data Source

Ακολουθήστε αυτά τα βήματα για να ρυθμίσετε μια νέα πηγή δεδομένων ODBC χρησιμοποιώντας έλεγχο ταυτότητας με κωδικό πρόσβασης:

#### Βήμα 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Σημείωση: Εάν η ρύθμιση της βάσης δεδομένων σας απαιτεί να επιλέξετε συγκεκριμένο "SSLMode", βεβαιωθείτε ότι θα το χρησιμοποιήσετε επίσης κατά τον ορισμό μιας DSN-less ρύθμισης.

#### Βήμα 2 – Test the connection

Κάντε κλικ στο κουμπί **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Τώρα μπορείτε να ρυθμίσετε το *digna* να χρησιμοποιεί τη σύνδεση ODBC, είτε με **DSN (Data Source Name)** είτε με ρύθμιση **DSN-less**.

---

### A. DSN-Based Configuration

#### Ρύθμιση του *digna*

Στην οθόνη **"Create a Database Connection"**, δώστε τα εξής:

```
Technology:      PostgreSQL
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Ιδιότητες ODBC

```
name: "DSN",    value: "PostgreSQL35W"
```

> Το `DSN` πρέπει να ταιριάζει με το όνομα που ορίζεται στη ρύθμιση του οδηγού ODBC σας.

---

### B. DSN-less Configuration

#### Ρύθμιση του *digna*

Στην οθόνη **"Create a Database Connection"**, δώστε τα εξής:

```
Technology:      PostgreSQL
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Ιδιότητες ODBC

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```