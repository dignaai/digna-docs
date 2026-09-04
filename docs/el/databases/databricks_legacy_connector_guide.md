---
title: Συνδετήρας Databricks (Legacy, χωρίς Unity Catalog) | Τεκμηρίωση digna
description: Διαμορφώστε το digna για σύνδεση με το Databricks χωρίς Unity Catalog χρησιμοποιώντας τον native Python connector ή τον Simba Spark ODBC driver. Υποστηρίζει πιστοποίηση με token και ευέλικτη συνδεσιμότητα.
image: /assets/logo_square.png
---

# Source Connector for Databricks - without Unity Catalog

Ο οδηγός αυτός περιγράφει πώς να διαμορφώσετε το *digna* ώστε να συνδεθεί με το Databricks χρησιμοποιώντας είτε τον native Python connector είτε τον ODBC driver.

Αναφέρεται στην οθόνη **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> Για άλλες μεθόδους πιστοποίησης, χρησιμοποιήστε τον ODBC driver.

### Personal Access Token (PAT)

Για να πραγματοποιήσετε πιστοποίηση με personal access token, ανατρέξτε στην επίσημη τεκμηρίωση της Databricks:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Παρέχετε τις ακόλουθες πληροφορίες στην οθόνη **"Create a Database Connection"**:

```
Technology:      Databricks (Legacy)
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Ο ODBC driver υποστηρίζει ευρύτερο φάσμα επιλογών πιστοποίησης και συνδεσιμότητας. Αυτή η ενότητα εστιάζει στην πιστοποίηση με token χρησιμοποιώντας τον **Simba Spark ODBC Driver**.

### 1. Install the ODBC Driver

Εγκαταστήστε τον **Simba Spark ODBC Driver** ακολουθώντας τον επίσημο οδηγό εγκατάστασης του vendor.

### 2. Configure the ODBC Data Source

Ακολουθήστε τα παρακάτω βήματα για να διαμορφώσετε μια νέα πηγή δεδομένων ODBC χρησιμοποιώντας Personal Access Token:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test the connection

Κάντε κλικ στο κουμπί **TEST**. Μια επιτυχημένη σύνδεση θα μοιάζει κάπως έτσι:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Τώρα μπορείτε να διαμορφώσετε το *digna* να χρησιμοποιεί τη σύνδεση ODBC, είτε με **DSN (Data Source Name)** είτε με ρύθμιση **χωρίς DSN (DSN-less)**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Στην οθόνη **"Create a Database Connection"**, παρέχετε τα εξής:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> Το `DSN` πρέπει να ταιριάζει με το όνομα που ορίζετε στη διαμόρφωση του ODBC driver σας.

---

### B. DSN-less Configuration

#### *digna* Configuration

Στην οθόνη **"Create a Database Connection"**, παρέχετε τα εξής:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
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