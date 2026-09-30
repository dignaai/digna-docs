---
title: PostgreSQL Connector – Ενσωμάτωση Βάσης Δεδομένων | Τεκμηρίωση digna
description: Διαμορφώστε το digna ώστε να συνδέεται στο PostgreSQL μέσω ODBC με ένα connection string χωρίς DSN. Καλύπτει τον driver psqlODBC, τις απαιτούμενες ιδιότητες ODBC, τα SSL modes και τις ρυθμίσεις σύνδεσης στην πλευρά του digna.
image: /assets/logo_square.png
---


# Source Connector για το PostgreSQL

Αυτός ο οδηγός περιγράφει πώς να διαμορφώσετε το *digna* ώστε να συνδέεται στο PostgreSQL μέσω
**ODBC**, χρησιμοποιώντας ένα connection string **χωρίς DSN** (DSN-less).

Η πλευρά του *digna* στη ρύθμιση είναι ίδια για κάθε τεχνολογία — πού δημιουργούνται οι
συνδέσεις, πώς κρυπτογραφούνται οι τιμές των ιδιοτήτων, πώς δοκιμάζεται μια σύνδεση και τι
σημαίνουν τα profiling modes. Περιγράφεται στην [Επισκόπηση Συνδέσεων Βάσεων Δεδομένων](overview.md).
Αυτή η σελίδα καλύπτει ό,τι είναι ειδικό για το PostgreSQL.

---

## 1. Εγκατάσταση του ODBC Driver {: #1-install-the-odbc-driver }

Εγκαταστήστε τον PostgreSQL ODBC driver (**psqlODBC**) στο μηχάνημα που εκτελεί το backend του
*digna*, ακολουθώντας τον επίσημο οδηγό εγκατάστασης του κατασκευαστή.

Ο driver καταχωρίζεται με όνομα που διαφέρει ανά πλατφόρμα και πακέτο — συνήθως
**PostgreSQL Unicode(x64)** στα Windows και **PostgreSQL ODBC Driver(UNICODE)** στο Linux.
Διαβάστε το ακριβές όνομα στον host σας, όπως περιγράφεται στην ενότητα
[Εγκατάσταση του ODBC Driver στον Host του digna](overview.md#install-the-driver), και
χρησιμοποιήστε αυτό το όνομα για την ιδιότητα `DRIVER` παρακάτω.

---

## 2. Ιδιότητες ODBC {: #2-odbc-properties }

!!! important "Παράδειγμα, όχι προδιαγραφή"

    Το παρακάτω σύνολο είναι ένας συνδυασμός που είναι γνωστό ότι λειτουργεί. Οι ιδιότητες
    ανήκουν στον driver psqlODBC, οπότε τα ονόματα, οι προεπιλογές και οι αποδεκτές τιμές τους
    διαφέρουν ανάμεσα σε εκδόσεις driver και πλατφόρμες, και το τι απαιτεί ο server σας —
    ειδικά ως προς το SSL — μπορεί επίσης να διαφέρει. Χρησιμοποιήστε το ως σημείο εκκίνησης και
    ελέγξτε την τεκμηρίωση της έκδοσης driver που εγκαταστήσατε.

Προσθέστε τις παρακάτω ιδιότητες στην οθόνη **Add DB Connection**:

| Κλειδί | Παράδειγμα τιμής | Σημειώσεις |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Πρέπει να ταιριάζει με το όνομα του driver που είναι καταχωρισμένο στον host του *digna* |
| `SERVER` | `db.example.com` | Όνομα server ή διεύθυνση IP |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Η βάση δεδομένων που περιέχει τα schemas πηγής. Είναι η μόνη βάση δεδομένων στην οποία αυτή η σύνδεση μπορεί να κάνει profiling |
| `UID` | `digna_source_user` | Χρήστης βάσης δεδομένων |
| `PWD` | `<password>` | Επιλέξτε **Encrypted** |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` ή `verify-full` — πρέπει να γίνεται δεκτό από τον server |

Το connection string που προκύπτει μοιάζει ως εξής:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Οποιαδήποτε άλλη επιλογή του psqlODBC μπορεί να προστεθεί ως επιπλέον ιδιότητα — για
παράδειγμα `ReadOnly=1` για session μόνο ανάγνωσης, ή `ConnSettings` για εκτέλεση εντολών `SET`
κατά τη σύνδεση.

---

## 3. Διαμόρφωση του *digna* {: #3-digna-configuration }

Στην οθόνη **Add DB Connection**, δώστε τα εξής:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Σημειώσεις για το PostgreSQL {: #4-notes-on-postgresql }

- **Το `SSLMode` πρέπει να ταιριάζει με τον server.** Ένας server διαμορφωμένος με `hostssl`
  απορρίπτει το `SSLMode=disable`, και τα `verify-ca` ή `verify-full` απαιτούν επιπλέον το root
  certificate να είναι διαθέσιμο στον driver στον host του *digna*. Αν χρειάστηκε να επιλέξετε
  συγκεκριμένο mode κατά τη δοκιμή του driver, χρησιμοποιήστε το ίδιο και εδώ.
- **Μία σύνδεση βλέπει μία βάση δεδομένων.** Το *digna* προσφέρει τα schemas της βάσης δεδομένων
  που ορίζεται στο `DATABASE`, επειδή το PostgreSQL αναφέρει μόνο την τρέχουσα βάση δεδομένων
  ως catalog. Πίνακες πηγής σε άλλη βάση δεδομένων χρειάζονται δική τους σύνδεση.
- **Profiling modes.** Το *Permanent* δημιουργεί τους πίνακες εργασίας στο **Work Schema**, οπότε
  ο χρήστης χρειάζεται `CREATE` σε αυτό το schema. Το *Session* χρησιμοποιεί
  `CREATE TEMPORARY TABLE` και δεν αγγίζει το **Work Schema**. Το *Standard* χρειάζεται μόνο
  πρόσβαση ανάγνωσης.

---

## 5. Επαλήθευση του Driver (προαιρετικό) {: #5-verifying-the-driver-optional }

Η διαμόρφωση μιας πηγής δεδομένων ODBC δεν απαιτείται για σύνδεση χωρίς DSN, αλλά το παράθυρο
διαλόγου του ίδιου του driver είναι ένας βολικός τρόπος να επιβεβαιώσετε ότι ο driver λειτουργεί
και ότι ο server δέχεται τα διαπιστευτήρια και το SSL mode σας, πριν τα εισαγάγετε στο *digna*.

#### Βήμα 1
![Βήμα 1](images/postgres/create_odbc_data_source_step1.png)

#### Βήμα 2 – Δοκιμή της σύνδεσης

Κάντε κλικ στο κουμπί **Test Connection**.

![Βήμα 2](images/postgres/create_odbc_data_source_step2.png)

Οι τιμές που εισαγάγατε εδώ είναι ακριβώς οι τιμές που παίρνουν οι ιδιότητες της
[ενότητας 2](#2-odbc-properties).
