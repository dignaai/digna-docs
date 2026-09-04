---
title: Oracle Connector – Ενσωμάτωση Βάσης Δεδομένων | Τεκμηρίωση digna
description: Διαμορφώστε το digna για σύνδεση με Oracle χρησιμοποιώντας τον python-oracledb driver ή τον Oracle ODBC driver. Υποστηρίζει αυθεντικοποίηση με κωδικό (password) είτε με DSN είτε χωρίς DSN.
image: /assets/logo_square.png
---


# Source Connector for Oracle

Αυτός ο οδηγός περιγράφει πώς να διαμορφώσετε το *digna* για σύνδεση με Oracle DB είτε χρησιμοποιώντας τον native Python connector είτε τον ODBC driver.

Αναφέρεται στην οθόνη **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `python-oracledb`  
**Supported Authentication:** Password-based authentication only

> Για άλλες μεθόδους αυθεντικοποίησης, χρησιμοποιήστε τον ODBC driver.

### *digna* Configuration (Native Driver)

Παρέχετε τις παρακάτω πληροφορίες στην οθόνη **"Create a Database Connection"**:

```
Technology:      Oracle
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1521
Database Name:   Instance name, service name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Ο ODBC driver μπορεί να υποστηρίζει ευρύτερο φάσμα επιλογών αυθεντικοποίησης και συνδεσιμότητας. Αυτή η ενότητα επικεντρώνεται στην αυθεντικοποίηση με κωδικό χρησιμοποιώντας τον driver **Oracle in OraDB21Home1**.

### 1. Install the ODBC Driver

Εγκαταστήστε τον **Oracle in OraDB21Home1** (ή παρόμοιο) ακολουθώντας τον επίσημο οδηγό εγκατάστασης του προμηθευτή.

### 2. Configure the ODBC Data Source

Ακολουθήστε τα παρακάτω βήματα για να διαμορφώσετε ένα νέο ODBC data source χρησιμοποιώντας αυθεντικοποίηση με κωδικό:

#### Step 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Σημείωση:
Το TNS Service Name πρέπει να διαμορφωθεί στο αρχείο tnsnames.ora της εγκατάστασης του Oracle client σας. Εκεί παρέχετε τον connection descriptor (host, port, service name).

#### Step 2 – Test the connection

Κάντε κλικ στο κουμπί **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Πληκτρολογήστε τον κωδικό (password) και κάντε κλικ στο κουμπί **OK**.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Τώρα μπορείτε να διαμορφώσετε το *digna* να χρησιμοποιήσει τη σύνδεση ODBC, είτε με **DSN (Data Source Name)** είτε με ρύθμιση **χωρίς DSN (DSN-less)**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Στην οθόνη **"Create a Database Connection"**, παρέχετε τα εξής:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> Το `DSN` πρέπει να συμφωνεί με το όνομα που έχει οριστεί στη διαμόρφωση του ODBC driver σας.

---

### B. DSN-less Configuration

#### *digna* Configuration

Στην οθόνη **"Create a Database Connection"**, παρέχετε τα εξής:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```