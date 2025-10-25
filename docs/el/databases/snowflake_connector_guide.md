---
title: Snowflake Connector – Ενσωμάτωση Βάσης Δεδομένων | digna Documentation
description: Διαμορφώστε το digna για σύνδεση με το Snowflake χρησιμοποιώντας τον Python connector ή τον Snowflake ODBC driver. Υποστηρίζει πιστοποίηση με κωδικό πρόσβασης σε ρυθμίσεις με ή χωρίς DSN.
image: /assets/logo_square.png
---


# Συνδετήρας Πηγής για το Snowflake

Αυτός ο οδηγός περιγράφει πώς να διαμορφώσετε το *digna* ώστε να συνδεθεί με το Snowflake χρησιμοποιώντας είτε τον εγγενή Python connector είτε τον ODBC driver.

Αναφέρεται στην οθόνη **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Γηγενής Python Driver

**Βιβλιοθήκη:** `snowflake-connector-python`  
**Υποστηριζόμενη μέθοδος πιστοποίησης:** Μόνο πιστοποίηση με κωδικό πρόσβασης

> ⚠️ Για άλλες μεθόδους αυθεντικοποίησης, χρησιμοποιήστε τον ODBC driver.

### Διαμόρφωση *digna* (Γηγενής Driver)

Δώστε τις ακόλουθες πληροφορίες στην οθόνη **"Create a Database Connection"**:

```
Technology:      Snowflake
Host Address:    Snowflake account name
Host Port:       Not needed
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
User Name:       User name and warehouse in the format "user<@>warehouse"
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Ο ODBC driver μπορεί να υποστηρίζει ευρύτερο φάσμα επιλογών πιστοποίησης και συνδεσιμότητας. Αυτή η ενότητα επικεντρώνεται στην πιστοποίηση με κωδικό πρόσβασης χρησιμοποιώντας τον **SnowflakeDSIIDriver**.

### 1. Εγκατάσταση του ODBC Driver

Εγκαταστήστε τον **SnowflakeDSIIDriver** ακολουθώντας τον επίσημο οδηγό εγκατάστασης του προμηθευτή.

### 2. Διαμόρφωση της Πηγής Δεδομένων ODBC

Ακολουθήστε αυτά τα βήματα για να διαμορφώσετε μια νέα πηγή δεδομένων ODBC χρησιμοποιώντας πιστοποίηση με κωδικό πρόσβασης:

#### Βήμα 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Σημειώσεις:
- Εάν δεν δώσετε τιμές για Database, Schema και Warehouse, τότε θα χρειαστεί να τις παράσχετε ως ιδιότητες ODBC κατά τη διαμόρφωση της πηγής δεδομένων στο *digna*.
- Η τιμή για το "Server" αποτελείται από το όνομα του λογαριασμού Snowflake ακολουθούμενο από ".snowflakecomputing.com"

#### Βήμα 2 – Δοκιμή της σύνδεσης

Κάντε κλικ στο κουμπί **TEST**. Μια επιτυχημένη σύνδεση θα μοιάζει ως εξής:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Τώρα μπορείτε να διαμορφώσετε το *digna* ώστε να χρησιμοποιεί τη σύνδεση ODBC, είτε με **DSN (Data Source Name)** είτε με ρύθμιση **χωρίς DSN (DSN-less)**.

---

### A. Διαμόρφωση με DSN

#### Διαμόρφωση *digna*

Στην οθόνη **"Create a Database Connection"**, δώστε τα ακόλουθα:

```
Technology:      Snowflake
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Ιδιότητες ODBC

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionally:
name: "Database",       value: "Database that contains the source schema"
name: "Schema",         value: "Schema that contains the source data"
name: "Warehouse",      value: "Warehouse to use for the execution of the SQLs"
```

> 🔹 Το `DSN` πρέπει να ταιριάζει με το όνομα που έχει οριστεί στη διαμόρφωση του ODBC driver σας.

---

### B. Διαμόρφωση χωρίς DSN (DSN-less)

#### Διαμόρφωση *digna*

Στην οθόνη **"Create a Database Connection"**, δώστε τα ακόλουθα:

```
Technology:      Snowflake
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Ιδιότητες ODBC

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Database that contains the source schema"
name: "Schema",     value: "Schema that contains the source data"
name: "Warehouse",  value: "Warehouse to use for the execution of the SQLs"
```