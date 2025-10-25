---
title: Συνδετήρας Apache Hive – Ενσωμάτωση Βάσης Δεδομένων | digna Documentation
description: Ρυθμίστε το digna για σύνδεση με το Apache Hive χρησιμοποιώντας τον εγγενή οδηγό PyHive ή τον ODBC οδηγό της Cloudera. Υποστηρίζει έλεγχο ταυτότητας με κωδικό πρόσβασης και ρυθμίσεις με DSN ή χωρίς DSN.
image: /assets/logo_square.png
---


# Συνδετήρας Πηγής για το Hive

Αυτός ο οδηγός περιγράφει πώς να ρυθμίσετε το *digna* ώστε να συνδεθεί με το Hive χρησιμοποιώντας είτε τον εγγενή Python connector είτε τον ODBC driver.

Αναφέρεται στην οθόνη **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Εγγενής Python Driver

**Βιβλιοθήκη:** `PyHive`  
**Υποστηριζόμενος Έλεγχος Ταυτότητας:** Μόνο έλεγχος ταυτότητας με κωδικό πρόσβασης

> ⚠️ Για άλλες μεθόδους ελέγχου ταυτότητας, χρησιμοποιήστε τον ODBC driver.

### Ρύθμιση *digna* (Εγγενής Driver)

Παρέχετε τις παρακάτω πληροφορίες στην οθόνη **"Create a Database Connection"**:

```
Technology:      Apache Hive
Host Address:    Όνομα διακομιστή ή διεύθυνση IP
Host Port:       Αριθμός θύρας, π.χ. 10000
Database Name:   Σχήμα που περιέχει τα δεδομένα πηγής
Schema Name:     Σχήμα που περιέχει τα δεδομένα πηγής
User Name:       Όνομα χρήστη της βάσης δεδομένων
User Password:   Κωδικός πρόσβασης για τον χρήστη
Use ODBC:        Απενεργοποιημένο (προεπιλογή)
```

---

## ODBC Driver

Ο ODBC driver μπορεί να υποστηρίζει ευρύτερο φάσμα μεθόδων ελέγχου ταυτότητας και επιλογών σύνδεσης. Αυτή η ενότητα επικεντρώνεται στον έλεγχο ταυτότητας με κωδικό πρόσβασης χρησιμοποιώντας τον driver **Cloudera ODBC Driver for Apache Hive**.

### 1. Εγκαταστήστε τον ODBC Driver

Εγκαταστήστε τον **Cloudera ODBC Driver for Apache Hive** (ή παρόμοιο) ακολουθώντας τον επίσημο οδηγό εγκατάστασης του προμηθευτή.

### 2. Διαμορφώστε το ODBC Data Source

Ακολουθήστε αυτά τα βήματα για να διαμορφώσετε μια νέα πηγή δεδομένων ODBC χρησιμοποιώντας έλεγχο ταυτότητας με κωδικό πρόσβασης:

#### Βήμα 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Βήμα 2 – Δοκιμή της σύνδεσης

Καταχωρίστε τον κωδικό πρόσβασης και κάντε κλικ στο κουμπί **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Μετά από επιτυχή δοκιμή, πατήστε το κουμπί **OK**.

---

Τώρα μπορείτε να ρυθμίσετε το *digna* να χρησιμοποιεί τη σύνδεση ODBC, είτε με **DSN (Data Source Name)** είτε με ρύθμιση **χωρίς DSN**.

---

### A. Ρύθμιση με DSN

#### Ρύθμιση *digna*

Στην οθόνη **"Create a Database Connection"**, παρέχετε τα εξής:

```
Technology:      Apache Hive
Database Name:   Σχήμα που περιέχει τα δεδομένα πηγής (το ίδιο με το Schema Name)
Schema Name:     Σχήμα που περιέχει τα δεδομένα πηγής
Use ODBC:        Ενεργοποιημένο
```

#### Ιδιότητες ODBC

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{ο κωδικός σας μέσα σε αγκύλες}"
```

> 🔹 Το `DSN` πρέπει να αντιστοιχεί στο όνομα που έχει οριστεί στη διαμόρφωση του ODBC driver σας.

---

### B. Ρύθμιση χωρίς DSN

#### Ρύθμιση *digna*

Στην οθόνη **"Create a Database Connection"**, παρέχετε τα εξής:

```
Technology:      Apache Hive
Database Name:   Σχήμα που περιέχει τα δεδομένα πηγής (το ίδιο με το Schema Name)
Schema Name:     Σχήμα που περιέχει τα δεδομένα πηγής
Use ODBC:        Ενεργοποιημένο
```

#### Ιδιότητες ODBC

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "το όνομα του διακομιστή σας ή διεύθυνση IP"
name: "PORT",       value: "Αριθμός θύρας, π.χ. 10000"
name: "Schema",     value: "Σχήμα που περιέχει τα δεδομένα πηγής"
name: "UID",        value: "ο χρήστης hive σας"
name: "PWD",        value: "ο κωδικός hive σας"
name: "AuthMech",   value: "3"
```