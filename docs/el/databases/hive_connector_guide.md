---
title: Apache Hive Connector – Ενσωμάτωση Βάσης Δεδομένων | Τεκμηρίωση digna
description: Διαμορφώστε το digna ώστε να συνδέεται στο Apache Hive μέσω ODBC με ένα connection string χωρίς DSN. Καλύπτει τον Cloudera Hive ODBC driver, τους μηχανισμούς αυθεντικοποίησης, τα transport modes και τις ρυθμίσεις σύνδεσης στην πλευρά του digna.
image: /assets/logo_square.png
---


# Source Connector για το Hive

Αυτός ο οδηγός περιγράφει πώς να διαμορφώσετε το *digna* ώστε να συνδέεται στο Apache Hive μέσω
**ODBC**, χρησιμοποιώντας ένα connection string **χωρίς DSN** (DSN-less).

Η πλευρά του *digna* στη ρύθμιση είναι ίδια για κάθε τεχνολογία — πού δημιουργούνται οι
συνδέσεις, πώς κρυπτογραφούνται οι τιμές των ιδιοτήτων, πώς δοκιμάζεται μια σύνδεση και τι
σημαίνουν τα profiling modes. Περιγράφεται στην [Επισκόπηση Συνδέσεων Βάσεων Δεδομένων](overview.md).
Αυτή η σελίδα καλύπτει ό,τι είναι ειδικό για το Hive.

---

## 1. Εγκατάσταση του ODBC Driver {: #1-install-the-odbc-driver }

Εγκαταστήστε τον **Cloudera ODBC Driver for Apache Hive** στο μηχάνημα που εκτελεί το backend
του *digna*, ακολουθώντας τον επίσημο οδηγό εγκατάστασης του κατασκευαστή.

Διαβάστε το ακριβές καταχωρισμένο όνομα του driver στον host σας, όπως περιγράφεται στην ενότητα
[Εγκατάσταση του ODBC Driver στον Host του digna](overview.md#install-the-driver).

---

## 2. Ιδιότητες ODBC {: #2-odbc-properties }

!!! important "Παράδειγμα, όχι προδιαγραφή"

    Το παρακάτω σύνολο είναι ένας συνδυασμός που είναι γνωστό ότι λειτουργεί. Οι ιδιότητες
    ανήκουν στον Cloudera Hive driver, οπότε τα ονόματα, οι προεπιλογές και οι αποδεκτές τιμές
    τους διαφέρουν ανάμεσα σε εκδόσεις driver και πλατφόρμες, και το τι δέχεται ο HiveServer2
    εξαρτάται πλήρως από το πώς είναι ασφαλισμένο το cluster — μηχανισμός αυθεντικοποίησης,
    transport mode, TLS, gateway. Χρησιμοποιήστε το ως σημείο εκκίνησης και ελέγξτε την
    τεκμηρίωση της έκδοσης driver που εγκαταστήσατε.

Προσθέστε τις παρακάτω ιδιότητες στην οθόνη **Add DB Connection**:

| Κλειδί | Παράδειγμα τιμής | Σημειώσεις |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Πρέπει να ταιριάζει με το όνομα του driver που είναι καταχωρισμένο στον host του *digna* |
| `HOST` | `hive.example.com` | Όνομα host ή διεύθυνση IP του HiveServer2 |
| `PORT` | `10000` | Port του HiveServer2· `10001` για HTTP transport |

Το connection string που προκύπτει μοιάζει ως εξής:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Αυθεντικοποίηση

Ένας HiveServer2 χωρίς ασφάλεια δέχεται τις τρεις παραπάνω ιδιότητες όπως είναι. Όπου είναι
ενεργοποιημένη η αυθεντικοποίηση, προσθέστε:

| Κλειδί | Παράδειγμα τιμής | Σημειώσεις |
|---|---|---|
| `AuthMech` | `3` | `0` χωρίς αυθεντικοποίηση, `2` μόνο όνομα χρήστη, `3` όνομα χρήστη και κωδικός πρόσβασης, `1` Kerberos |
| `UID` | `digna_source_user` | Απαιτείται για `AuthMech` `2` και `3` |
| `PWD` | `<password>` | Απαιτείται για `AuthMech` `3`. Επιλέξτε **Encrypted** |

Για Kerberos (`AuthMech=1`), ο host του *digna* χρειάζεται επιπλέον ένα έγκυρο ticket ή keytab,
καθώς και τις ιδιότητες `KrbHostFQDN`, `KrbServiceName` και `KrbRealm` που τεκμηριώνει ο driver.

### Transport και TLS

| Κλειδί | Παράδειγμα τιμής | Σημειώσεις |
|---|---|---|
| `ThriftTransport` | `2` | `0` binary (η προεπιλογή, port 10000), `1` SASL, `2` HTTP (port 10001, και αυτό που αναμένει ένα Knox gateway) |
| `HTTPPath` | `cliservice` | Με `ThriftTransport=2` |
| `SSL` | `1` | Όπου ο HiveServer2 είναι ασφαλισμένος με TLS |
| `Schema` | `dignadata` | Η βάση δεδομένων Hive στην οποία ξεκινά το session. Προαιρετικό — το *digna* χρησιμοποιεί πλήρως προσδιορισμένα ονόματα στα queries του |

---

## 3. Διαμόρφωση του *digna* {: #3-digna-configuration }

Στην οθόνη **Add DB Connection**, δώστε τα εξής:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Σημειώσεις για το Hive {: #4-notes-on-hive }

- **Οι catalogs προέρχονται από τον driver.** Το Hive δεν έχει δικό του catalog, οπότε το
  *digna* παίρνει ό,τι αναφέρει ο driver — συνήθως μία μόνο καταχώριση με όνομα `HIVE` — και
  παραθέτει τις βάσεις δεδομένων Hive ως schemas κάτω από αυτήν.
- **Το Work Schema είναι μια βάση δεδομένων Hive.** Για το *Permanent* profiling, ο χρήστης
  χρειάζεται δικαίωμα δημιουργίας και διαγραφής πινάκων σε αυτήν, και η υποκείμενη θέση
  αποθήκευσης πρέπει να είναι εγγράψιμη.
- **Profiling modes.** Το *Permanent* δημιουργεί τους πίνακες εργασίας στο **Work Schema**. Το
  *Session* χρησιμοποιεί `CREATE TEMPORARY TABLE`, που απαιτεί HiveServer2 με υποστήριξη
  προσωρινών πινάκων, και δεν αγγίζει το **Work Schema**. Το *Standard* χρειάζεται μόνο
  πρόσβαση ανάγνωσης και είναι το mode που επιλέγετε σε cluster όπου το *digna* δεν έχει καθόλου
  πρόσβαση εγγραφής.
- **Το profiling είναι ένα σύνολο queries, όχι σάρωση.** Κάθε στατιστικό υπολογίζεται από τον
  HiveServer2, οπότε η ουρά (queue) στην οποία υποβάλλει εργασίες ο χρήστης του *digna* πρέπει να
  έχει επαρκή χωρητικότητα για το χρονικό παράθυρο του inspection.

---

## 5. Επαλήθευση του Driver (προαιρετικό) {: #5-verifying-the-driver-optional }

Η διαμόρφωση μιας πηγής δεδομένων ODBC δεν απαιτείται για σύνδεση χωρίς DSN, αλλά το παράθυρο
διαλόγου του ίδιου του driver είναι ένας βολικός τρόπος να επιβεβαιώσετε ότι ο driver, το
transport mode και τα διαπιστευτήριά σας λειτουργούν, πριν τα εισαγάγετε στο *digna*.

#### Βήμα 1
![Βήμα 1](images/hive/create_odbc_data_source_step1.png)

Τα πεδία **Host**, **Port**, **Database**, **Mechanism** και **Thrift Transport** εδώ
αντιστοιχούν στις ιδιότητες `HOST`, `PORT`, `Schema`, `AuthMech` και `ThriftTransport` της
[ενότητας 2](#2-odbc-properties).

#### Βήμα 2 – Δοκιμή της σύνδεσης

Δώστε τον κωδικό πρόσβασης και κάντε κλικ στο κουμπί **Test**.

![Βήμα 2](images/hive/create_odbc_data_source_step2.png)

Μετά από επιτυχημένη δοκιμή, κάντε κλικ στο κουμπί **OK**.
