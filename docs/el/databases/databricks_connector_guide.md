---
title: Databricks Connector with Unity Catalog – Ενσωμάτωση Βάσης Δεδομένων | digna Documentation
description: Διαμορφώστε το digna για σύνδεση με Databricks και Unity Catalog χρησιμοποιώντας τον native Python connector ή τον ODBC driver. Υποστηρίζει ταυτοποίηση με token και ευέλικτη συνδεσιμότητα.
image: /assets/logo_square.png
---

# Source Connector for Databricks - with Unity Catalog

Αυτός ο οδηγός περιγράφει πώς να διαμορφώσετε το *digna* ώστε να συνδεθεί με το Databricks χρησιμοποιώντας είτε τον native Python connector είτε τον ODBC driver.

Αναφέρεται στην οθόνη **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> ⚠️ Για άλλες μεθόδους ταυτοποίησης, χρησιμοποιήστε τον ODBC driver.

### Personal Access Token (PAT)

Για να κάνετε ταυτοποίηση χρησιμοποιώντας personal access token, ανατρέξτε στην επίσημη τεκμηρίωση της Databricks:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Παρέχετε τις ακόλουθες πληροφορίες στην οθόνη **"Create a Database Connection"**:

```
Technology:      Databricks
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Name of the catalog to use. 
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Ο ODBC driver υποστηρίζει ευρύτερο φάσμα μεθόδων ταυτοποίησης και επιλογών συνδεσιμότητας. Αυτή η ενότητα επικεντρώνεται στην ταυτοποίηση με token χρησιμοποιώντας τον **Simba Spark ODBC Driver**.

### 1. Install the ODBC Driver

Εγκαταστήστε τον **Simba Spark ODBC Driver** ακολουθώντας τον επίσημο οδηγό εγκατάστασης του προμηθευτή.

### 2. Configure the ODBC Data Source

Ακολουθήστε τα παρακάτω βήματα για να διαμορφώσετε ένα νέο ODBC data source χρησιμοποιώντας Personal Access Token:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test the connection

Κάντε κλικ στο κουμπί **TEST**. Μια επιτυχημένη σύνδεση θα μοιάζει έτσι:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Τώρα μπορείτε να διαμορφώσετε το *digna* ώστε να χρησιμοποιεί τη σύνδεση ODBC, είτε με **DSN (Data Source Name)** είτε χωρίς DSN.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Στην οθόνη **"Create a Database Connection"**, παρέχετε τα ακόλουθα:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 To `DSN` πρέπει να αντιστοιχεί στο όνομα που έχει οριστεί στη ρύθμιση του ODBC driver σας.

---

### B. DSN-less Configuration

#### *digna* Configuration

Στην οθόνη **"Create a Database Connection"**, παρέχετε τα ακόλουθα:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name = "Driver",          value = "{Simba Spark ODBC Driver}"
name = "Host",            value = "xxxxxxxxxxxxxxxxxxx.databricks.com"
name = "Port",            value = "443"
name = "HTTPPath",        value = "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
name = "SSL",             value = "1"
name = "ThriftTransport", value = "2"
name = "AuthMech",        value = "3"
name = "UID",             value = "token"
name = "PWD",             value = "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```