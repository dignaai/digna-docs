---
title: Συνδετήρας Azure Synapse – Ενσωμάτωση Βάσης Δεδομένων | digna Documentation
description: Διαμορφώστε το digna για σύνδεση με το Azure Synapse Analytics χρησιμοποιώντας είτε τον native Python driver είτε τον ODBC driver. Υποστηρίζει τόσο serverless όσο και dedicated SQL pools.
image: /assets/logo_square.png
canonical_url: https://docs.digna.ai/databases/azure_synapse_connector_guide/
---


# Source Connector for Azure Synapse Analytics

Αυτός ο οδηγός περιγράφει πώς να διαμορφώσετε το *digna* για σύνδεση με το Azure Synapse Analytics χρησιμοποιώντας είτε τον native connector για Python είτε τον ODBC driver. Υποστηρίζονται τόσο τα serverless όσο και τα dedicated SQL pools.

Αναφέρεται στην οθόνη **"Create a Database Connection"**.

![Δημιουργία σύνδεσης βάσης δεδομένων](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Υποστηριζόμενη Αυθεντικοποίηση:** Μόνο αυθεντικοποίηση με κωδικό (password-based authentication)

> Για άλλες μεθόδους αυθεντικοποίησης, χρησιμοποιήστε τον ODBC driver.

### *digna* Configuration (Native Driver)

Παρέχετε τις ακόλουθες πληροφορίες στην οθόνη **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Ο ODBC driver μπορεί να υποστηρίζει ευρύτερο φάσμα επιλογών αυθεντικοποίησης και συνδεσιμότητας. Αυτή η ενότητα εστιάζει στην αυθεντικοποίηση με κωδικό χρησιμοποιώντας τον driver **ODBC Driver 18 for SQL Server**.

### 1. Εγκατάσταση του ODBC Driver

Εγκαταστήστε τον driver **ODBC Driver 18 for SQL Server** (ή παρόμοιο) ακολουθώντας τον επίσημο οδηγό εγκατάστασης του προμηθευτή.

### 2. Διαμόρφωση της Πηγής Δεδομένων ODBC

Ακολουθήστε τα παρακάτω βήματα για να διαμορφώσετε μια νέα πηγή δεδομένων ODBC χρησιμοποιώντας αυθεντικοποίηση με κωδικό:

#### Βήμα 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Συμπληρώστε το πεδίο "Server". Χρησιμοποιήστε το όνομα του Synapse workspace και επεκτείνετέ το με ".sql.azuresynapse.net".  
**Προσοχή**, αν θέλετε να συνδεθείτε με χρήση ενός serverless SQL pool, βεβαιωθείτε ότι περιλαμβάνετε το "-ondemand" όπως φαίνεται στο παρακάτω στιγμιότυπο.

Πατήστε το κουμπί **Next >**.

#### Βήμα 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Επιλέξτε τη μέθοδο αυθεντικοποίησης (π.χ. username και password) και εισάγετε τα απαιτούμενα δεδομένα.

Πατήστε το κουμπί **Next >**.

#### Βήμα 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Επιλέξτε τις ρυθμίσεις συμβατές με ANSI και στη συνέχεια πατήστε το κουμπί **Next >**.

#### Βήμα 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Μπορείτε να αφήσετε τις προεπιλεγμένες ρυθμίσεις ή να επιλέξετε άλλες επιλογές όπως χρειάζεται και να κάνετε κλικ στο κουμπί **Finish**.

#### Βήμα 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Τώρα πατήστε το κουμπί **Test datasource**.

#### Βήμα 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Όταν λάβετε την οθόνη επιτυχίας, ο ODBC έχει διαμορφωθεί σωστά.

---

Τώρα μπορείτε να διαμορφώσετε το *digna* να χρησιμοποιήσει τη σύνδεση ODBC, είτε με **DSN (Data Source Name)** είτε με ρύθμιση χωρίς DSN (DSN-less).

---

### A. DSN-Based Configuration

#### *digna* Configuration

Στην οθόνη **"Create a Database Connection"**, συμπληρώστε τα παρακάτω:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> Το `DSN` πρέπει να ταιριάζει με το όνομα που ορίζετε στη διαμόρφωση του ODBC driver σας.

---

### B. DSN-less Configuration

#### *digna* Configuration

Στην οθόνη **"Create a Database Connection"**, συμπληρώστε τα παρακάτω:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Σημείωση** σχετικά με την ιδιότητα SERVER:  
Χρησιμοποιήστε το όνομα του Synapse workspace και επεκτείνετέ το με ".sql.azuresynapse.net". Αν θέλετε να συνδεθείτε μέσω ενός serverless SQL pool, φροντίστε να συμπεριλάβετε το "-ondemand" όπως φαίνεται στο παρακάτω στιγμιότυπο.