---
title: Databricks Connector – Ενσωμάτωση Βάσης Δεδομένων | Τεκμηρίωση digna
description: Διαμορφώστε το digna ώστε να συνδέεται στο Databricks με Unity Catalog μέσω ODBC με ένα connection string χωρίς DSN. Καλύπτει τον Databricks ODBC driver, τα personal access tokens, το HTTP path και τις ρυθμίσεις σύνδεσης στην πλευρά του digna.
image: /assets/logo_square.png
---

# Source Connector για το Databricks

Αυτός ο οδηγός περιγράφει πώς να διαμορφώσετε το *digna* ώστε να συνδέεται στο Databricks μέσω
**ODBC**, χρησιμοποιώντας ένα connection string **χωρίς DSN** (DSN-less).

Η πλευρά του *digna* στη ρύθμιση είναι ίδια για κάθε τεχνολογία — πού δημιουργούνται οι
συνδέσεις, πώς κρυπτογραφούνται οι τιμές των ιδιοτήτων, πώς δοκιμάζεται μια σύνδεση και τι
σημαίνουν τα profiling modes. Περιγράφεται στην [Επισκόπηση Συνδέσεων Βάσεων Δεδομένων](overview.md).
Αυτή η σελίδα καλύπτει ό,τι είναι ειδικό για το Databricks.

!!! note "Απαιτείται Unity Catalog"

    Το *digna* διαβάζει τους διαθέσιμους catalogs από το `system.information_schema.catalogs`,
    οπότε το workspace πρέπει να έχει ενεργοποιημένο το Unity Catalog. Παλαιότερες εκδόσεις του
    *digna* πρόσφεραν ξεχωριστή τεχνολογία "Databricks Legacy" για workspaces χωρίς Unity
    Catalog· αυτή δεν είναι πλέον διαθέσιμη.

---

## 1. Εγκατάσταση του ODBC Driver {: #1-install-the-odbc-driver }

Εγκαταστήστε τον **Databricks ODBC Driver** στο μηχάνημα που εκτελεί το backend του *digna*,
ακολουθώντας τον [οδηγό εγκατάστασης της Databricks](https://docs.databricks.com/aws/en/integrations/odbc/).

Ανάλογα με την έκδοση, ο driver καταχωρίζεται ως **Simba Spark ODBC Driver** ή ως
**Databricks ODBC Driver**. Διαβάστε το ακριβές καταχωρισμένο όνομα στον host σας, όπως
περιγράφεται στην ενότητα [Εγκατάσταση του ODBC Driver στον Host του digna](overview.md#install-the-driver).

---

## 2. Συλλογή των Στοιχείων Σύνδεσης {: #2-gather-the-connection-details }

Όλες οι τιμές προέρχονται από το SQL warehouse (ή το cluster) που θέλετε να χρησιμοποιεί το
*digna*. Ανοίξτε το στο Databricks workspace και μεταβείτε στο **Connection details**:

| Πεδίο Databricks | Χρησιμοποιείται ως |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, συνήθως `443` |
| **HTTP path** | `HTTPPath` |

Για την αυθεντικοποίηση, δημιουργήστε ένα **personal access token** — δείτε
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Τα tokens ανήκουν σε έναν χρήστη ή service principal, και αυτό το principal χρειάζεται
`USE CATALOG`, `USE SCHEMA` και `SELECT` στα δεδομένα πηγής.

---

## 3. Ιδιότητες ODBC {: #3-odbc-properties }

!!! important "Παράδειγμα, όχι προδιαγραφή"

    Το παρακάτω σύνολο είναι ένας συνδυασμός που είναι γνωστό ότι λειτουργεί. Οι ιδιότητες
    ανήκουν στον driver Databricks/Simba, οπότε τα ονόματα, οι προεπιλογές και οι αποδεκτές
    τιμές τους διαφέρουν ανάμεσα σε εκδόσεις driver — ο driver έχει μετονομαστεί και οι επιλογές
    αυθεντικοποίησής του έχουν επεκταθεί περισσότερες από μία φορές — και ανάμεσα σε πλατφόρμες.
    Χρησιμοποιήστε το ως σημείο εκκίνησης και ελέγξτε την τεκμηρίωση της έκδοσης driver που
    εγκαταστήσατε.

Προσθέστε τις παρακάτω ιδιότητες στην οθόνη **Add DB Connection**:

| Κλειδί | Παράδειγμα τιμής | Σημειώσεις |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Πρέπει να ταιριάζει με το όνομα του driver που είναι καταχωρισμένο στον host του *digna* |
| `Host` | `<workspace>.cloud.databricks.com` | Server hostname του warehouse, π.χ. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | HTTP path του warehouse ή του cluster |
| `SSL` | `1` | Τα endpoints του Databricks λειτουργούν μόνο με TLS |
| `ThriftTransport` | `2` | HTTP transport, που είναι αυτό που χρησιμοποιούν τα SQL endpoints |
| `AuthMech` | `3` | Αυθεντικοποίηση με token |
| `UID` | `token` | Η κυριολεκτική λέξη `token`, όχι όνομα χρήστη |
| `PWD` | `dapi…` | Το personal access token. Επιλέξτε **Encrypted** |
| `UseNativeQuery` | `1` | Μεταβιβάζει τη SQL του *digna* αμετάβλητη — δείτε παρακάτω |

Το connection string που προκύπτει μοιάζει ως εξής:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Διατηρήστε το `UseNativeQuery=1`"

    Με `UseNativeQuery=0` — την προεπιλογή του driver — ο driver ξαναγράφει την εισερχόμενη SQL
    σε ό,τι θεωρεί φορητή σύνταξη ODBC. Το *digna* παράγει ήδη Databricks SQL, οπότε η
    αναδιατύπωση μπορεί να αλλάξει τα backticks και τα literals ημερομηνιών, και το profiling
    αποτυγχάνει τότε σε εντολές που είναι έγκυρες όπως είναι γραμμένες.

### OAuth αντί για token

Για ένα service principal με αυθεντικοποίηση OAuth machine-to-machine, αντικαταστήστε τα
`AuthMech`, `UID` και `PWD` με:

| Κλειδί | Παράδειγμα τιμής | Σημειώσεις |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Client credentials |
| `Auth_Client_ID` | `<application id>` | Service principal |
| `Auth_Client_Secret` | `<client secret>` | Επιλέξτε **Encrypted** |

---

## 4. Διαμόρφωση του *digna* {: #4-digna-configuration }

Στην οθόνη **Add DB Connection**, δώστε τα εξής:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Σημειώσεις για το Databricks {: #5-notes-on-databricks }

- **Το warehouse πρέπει να εκτελείται**, ή να μπορεί να ξεκινήσει, όταν συνδέεται το *digna*.
  Ένα warehouse που επανέρχεται από κατάσταση διακοπής μπορεί να χρειαστεί περισσότερο χρόνο από
  το χρονικό όριο σύνδεσης — αν η δοκιμή αποτύχει στην πρώτη απόπειρα μετά από περίοδο
  αδράνειας, δοκιμάστε ξανά.
- **Οι catalogs προέρχονται από το workspace.** Σε αντίθεση με τις περισσότερες τεχνολογίες, μία
  σύνδεση Databricks προσεγγίζει κάθε catalog που επιτρέπεται να δει το principal, οπότε μία
  μόνο σύνδεση μπορεί να εξυπηρετεί πηγές σε διαφορετικούς catalogs.
- **Profiling modes.** Το *Permanent* δημιουργεί τους πίνακες εργασίας στο **Work Schema** μέσα
  στον catalog της πηγής, οπότε το principal χρειάζεται `CREATE TABLE` εκεί. Το *Session*
  χρησιμοποιεί `CREATE TEMPORARY TABLE` και δεν αγγίζει το **Work Schema**. Το *Standard*
  χρειάζεται μόνο πρόσβαση ανάγνωσης.
- **Τα serverless warehouses λειτουργούν** με τον ίδιο τρόπο· διαφέρει μόνο το `HTTPPath`.

---

## 6. Επαλήθευση του Driver (προαιρετικό) {: #6-verifying-the-driver-optional }

Η διαμόρφωση μιας πηγής δεδομένων ODBC δεν απαιτείται για σύνδεση χωρίς DSN, αλλά το παράθυρο
διαλόγου του ίδιου του driver είναι ένας βολικός τρόπος να επιβεβαιώσετε ότι ο driver, το
warehouse και το token λειτουργούν, πριν τα εισαγάγετε στο *digna*.

#### Βήμα 1
![Βήμα 1](images/databricks/create_odbc_data_source_step1.png)

#### Βήμα 2
![Βήμα 2](images/databricks/create_odbc_data_source_step2.png)

#### Βήμα 3
![Βήμα 3](images/databricks/create_odbc_data_source_step3.png)

#### Βήμα 4
![Βήμα 4](images/databricks/create_odbc_data_source_step4.png)

#### Βήμα 5 – Δοκιμή της σύνδεσης

Κάντε κλικ στο κουμπί **TEST**. Μια επιτυχημένη σύνδεση θα πρέπει να μοιάζει ως εξής:

![Βήμα 5](images/databricks/create_odbc_data_source_step5.png)

Ο host, το HTTP path και το token που εισάγονται εδώ είναι ακριβώς οι τιμές που παίρνουν οι
ιδιότητες της [ενότητας 3](#3-odbc-properties).
