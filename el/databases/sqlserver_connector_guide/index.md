# Source Connector για τον MS SQL Server

Αυτός ο οδηγός περιγράφει πώς να διαμορφώσετε το *digna* ώστε να συνδέεται στον Microsoft SQL
Server μέσω **ODBC**, χρησιμοποιώντας ένα connection string **χωρίς DSN** (DSN-less).

Η πλευρά του *digna* στη ρύθμιση είναι ίδια για κάθε τεχνολογία — πού δημιουργούνται οι
συνδέσεις, πώς κρυπτογραφούνται οι τιμές των ιδιοτήτων, πώς δοκιμάζεται μια σύνδεση και τι
σημαίνουν τα profiling modes. Περιγράφεται στην [Επισκόπηση Συνδέσεων Βάσεων Δεδομένων](overview.md).
Αυτή η σελίδα καλύπτει ό,τι είναι ειδικό για τον SQL Server.

!!! note "Azure Synapse Analytics"

    Το Synapse διαμορφώνεται επίσης ως σύνδεση SQL Server, με διαφορετικό όνομα host και μερικά
    επιπλέον ζητήματα — δείτε [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Εγκατάσταση του ODBC Driver {: #1-install-the-odbc-driver }

Εγκαταστήστε τον **ODBC Driver 18 for SQL Server** στο μηχάνημα που εκτελεί το backend του
*digna*, ακολουθώντας τον [οδηγό εγκατάστασης της Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

Ο driver που περιλαμβάνεται στα Windows με το απλό όνομα **SQL Server** λειτουργεί επίσης, αλλά
έχει αντικατασταθεί εδώ και καιρό και δεν υποστηρίζει ούτε σύγχρονες ρυθμίσεις TLS ούτε
αυθεντικοποίηση Azure. Χρησιμοποιήστε τον μόνο όπου η εγκατάσταση του τρέχοντος driver δεν είναι
εφικτή.

Διαβάστε το ακριβές καταχωρισμένο όνομα του driver στον host σας, όπως περιγράφεται στην ενότητα
[Εγκατάσταση του ODBC Driver στον Host του digna](overview.md#install-the-driver).

---

## 2. Ιδιότητες ODBC {: #2-odbc-properties }

!!! important "Παράδειγμα, όχι προδιαγραφή"

    Το παρακάτω σύνολο είναι ένας συνδυασμός που είναι γνωστό ότι λειτουργεί. Οι ιδιότητες
    ανήκουν στον ODBC driver της Microsoft, οπότε τα ονόματα, οι προεπιλογές και οι αποδεκτές
    τιμές τους διαφέρουν ανάμεσα σε εκδόσεις driver — για παράδειγμα, ο Driver 18 κρυπτογραφεί
    από προεπιλογή, ενώ ο Driver 17 όχι — και ανάμεσα σε πλατφόρμες. Χρησιμοποιήστε το ως σημείο
    εκκίνησης και ελέγξτε την τεκμηρίωση της έκδοσης driver που εγκαταστήσατε.

Προσθέστε τις παρακάτω ιδιότητες στην οθόνη **Add DB Connection**:

| Κλειδί | Παράδειγμα τιμής | Σημειώσεις |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Πρέπει να ταιριάζει με το όνομα του driver που είναι καταχωρισμένο στον host του *digna* |
| `SERVER` | `sql.example.com` | Όνομα server ή διεύθυνση IP. Named instances: `host\instance`· μη προεπιλεγμένο port: `host,1433` |
| `PORT` | `1433` | Παραλείψτε το όταν το port είναι ήδη μέρος του `SERVER` |
| `DATABASE` | `digna_source_db` | Η βάση δεδομένων που περιέχει τα schemas πηγής. Είναι η μόνη βάση δεδομένων στην οποία αυτή η σύνδεση μπορεί να κάνει profiling |
| `UID` | `digna_source_user` | Χρήστης βάσης δεδομένων |
| `PWD` | `<password>` | Επιλέξτε **Encrypted** |

Το connection string που προκύπτει μοιάζει ως εξής:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Κρυπτογράφηση με τον ODBC Driver 18

Ο Driver 18 κρυπτογραφεί τις συνδέσεις από προεπιλογή και επικυρώνει το πιστοποιητικό του
server. Σε έναν server με πιστοποιητικό που ο host του *digna* δεν εμπιστεύεται — συνήθως ένα
self-signed πιστοποιητικό — η σύνδεση αποτυγχάνει με σφάλμα αλυσίδας πιστοποιητικών. Προσθέστε:

| Κλειδί | Παράδειγμα τιμής | Σημειώσεις |
|---|---|---|
| `Encrypt` | `yes` | Προεπιλογή στον Driver 18· ορίστε `no` μόνο αν ο server δεν υποστηρίζει TLS |
| `TrustServerCertificate` | `yes` | Παρακάμπτει την επικύρωση του πιστοποιητικού. Βολικό σε περιβάλλοντα δοκιμών· στην παραγωγή προτιμήστε την εγκατάσταση του πιστοποιητικού |

### Windows Authentication

Για να συνδεθείτε ως ο λογαριασμός που εκτελεί το service του *digna* αντί για SQL login,
αφαιρέστε τα `UID` και `PWD` και προσθέστε:

| Κλειδί | Παράδειγμα τιμής | Σημειώσεις |
|---|---|---|
| `Trusted_Connection` | `yes` | Ο λογαριασμός του service του *digna* χρειάζεται τα δικαιώματα στη βάση δεδομένων |

---

## 3. Διαμόρφωση του *digna* {: #3-digna-configuration }

Στην οθόνη **Add DB Connection**, δώστε τα εξής:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Σημειώσεις για τον MS SQL Server {: #4-notes-on-ms-sql-server }

- **Μία σύνδεση βλέπει μία βάση δεδομένων.** Το *digna* προσφέρει τα schemas της βάσης δεδομένων
  που ορίζεται στο `DATABASE`, επειδή ο SQL Server αναφέρει μόνο την τρέχουσα βάση δεδομένων ως
  catalog. Πίνακες πηγής σε άλλη βάση δεδομένων χρειάζονται δική τους σύνδεση.
- **Profiling modes.** Το *Permanent* δημιουργεί τους πίνακες εργασίας στο **Work Schema**, οπότε
  ο χρήστης χρειάζεται `CREATE TABLE` εκεί. Το *Session* χρησιμοποιεί τοπικούς προσωρινούς πίνακες
  (`#wt_…`) στο `tempdb` και δεν αγγίζει το **Work Schema**. Το *Standard* χρειάζεται μόνο
  πρόσβαση ανάγνωσης.
- **Το `SERVER` περιέχει το instance και το port.** Με named instance, το `host\instance`
  απαιτεί να είναι προσβάσιμο το service SQL Server Browser· το `host,port` το αποφεύγει.

---

## 5. Επαλήθευση του Driver (προαιρετικό) {: #5-verifying-the-driver-optional }

Η διαμόρφωση μιας πηγής δεδομένων ODBC δεν απαιτείται για σύνδεση χωρίς DSN, αλλά ο οδηγός
(wizard) του ίδιου του driver είναι ένας βολικός τρόπος να επιβεβαιώσετε ότι ο driver λειτουργεί
και ότι ο server δέχεται τα διαπιστευτήριά σας, πριν τα εισαγάγετε στο *digna*.

#### Βήμα 1
![Βήμα 1](images/sqlserver/create_odbc_data_source_step1.png)

Κάντε κλικ στο κουμπί **Next >**.

#### Βήμα 2
![Βήμα 2](images/sqlserver/create_odbc_data_source_step2.png)

Επιλέξτε τη μέθοδο αυθεντικοποίησης (π.χ. όνομα χρήστη και κωδικός πρόσβασης)
και δώστε τα απαιτούμενα στοιχεία.

Κάντε κλικ στο κουμπί **Next >**.

#### Βήμα 3
![Βήμα 3](images/sqlserver/create_odbc_data_source_step3.png)

Επιλέξτε τις ρυθμίσεις συμβατότητας ANSI και έπειτα κάντε κλικ στο κουμπί **Next >**.

#### Βήμα 4
![Βήμα 4](images/sqlserver/create_odbc_data_source_step4.png)

Μπορείτε να αφήσετε τις προεπιλεγμένες ρυθμίσεις ή να επιλέξετε επιλογές καταγραφής (logging)
όπως χρειάζεστε και να κάνετε κλικ στο κουμπί **Finish**. 

#### Βήμα 5
![Βήμα 5](images/sqlserver/create_odbc_data_source_step5.png)

Τώρα κάντε κλικ στο κουμπί **Test datasource**.

#### Βήμα 6
![Βήμα 6](images/sqlserver/create_odbc_data_source_step6.png)

Μια οθόνη επιτυχίας επιβεβαιώνει ότι ο driver και τα διαπιστευτήρια λειτουργούν. Οι τιμές που
εισαγάγατε είναι ακριβώς οι τιμές που παίρνουν οι ιδιότητες της [ενότητας 2](#2-odbc-properties).