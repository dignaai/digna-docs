# Source Connector για το Oracle

Αυτός ο οδηγός περιγράφει πώς να διαμορφώσετε το *digna* ώστε να συνδέεται στο Oracle Database
μέσω **ODBC**, χρησιμοποιώντας ένα connection string **χωρίς DSN** (DSN-less).

Η πλευρά του *digna* στη ρύθμιση είναι ίδια για κάθε τεχνολογία — πού δημιουργούνται οι
συνδέσεις, πώς κρυπτογραφούνται οι τιμές των ιδιοτήτων, πώς δοκιμάζεται μια σύνδεση και τι
σημαίνουν τα profiling modes. Περιγράφεται στην [Επισκόπηση Συνδέσεων Βάσεων Δεδομένων](overview.md).
Αυτή η σελίδα καλύπτει ό,τι είναι ειδικό για το Oracle.

---

## 1. Εγκατάσταση του ODBC Driver {: #1-install-the-odbc-driver }

Ο Oracle ODBC driver είναι μέρος του **Oracle Client** (αρκεί το πακέτο "ODBC" του Instant
Client). Εγκαταστήστε τον στο μηχάνημα που εκτελεί το backend του *digna*, ακολουθώντας τον
επίσημο οδηγό εγκατάστασης του κατασκευαστή.

Ο driver καταχωρίζεται ως **Oracle in `<OracleHomeName>`** — για παράδειγμα
`Oracle in OraDB21Home1` ή `Oracle in instantclient_21_13`. Το όνομα του home διαφέρει ανά
εγκατάσταση, οπότε διαβάστε το ακριβές όνομα στον host σας, όπως περιγράφεται στην ενότητα
[Εγκατάσταση του ODBC Driver στον Host του digna](overview.md#install-the-driver).

---

## 2. Ιδιότητες ODBC {: #2-odbc-properties }

!!! important "Παράδειγμα, όχι προδιαγραφή"

    Το παρακάτω σύνολο είναι ένας συνδυασμός που είναι γνωστό ότι λειτουργεί. Οι ιδιότητες
    ανήκουν στον Oracle ODBC driver, οπότε τα ονόματα, οι προεπιλογές και οι αποδεκτές τιμές
    τους διαφέρουν ανάμεσα σε εκδόσεις client, και ειδικά το όνομα του driver εξαρτάται από το
    Oracle home στον host σας. Χρησιμοποιήστε το ως σημείο εκκίνησης και ελέγξτε την τεκμηρίωση
    της έκδοσης client που εγκαταστήσατε.

Προσθέστε τις παρακάτω ιδιότητες στην οθόνη **Add DB Connection**:

| Κλειδί | Παράδειγμα τιμής | Σημειώσεις |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Πρέπει να ταιριάζει με το όνομα του driver που είναι καταχωρισμένο στον host του *digna* |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Η βάση δεδομένων στην οποία γίνεται η σύνδεση — δείτε παρακάτω |
| `UID` | `DIGNA_SOURCE_USER` | Χρήστης βάσης δεδομένων |
| `PWD` | `<password>` | Επιλέξτε **Encrypted** |

Το connection string που προκύπτει μοιάζει ως εξής:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### Η τιμή `DBQ`

Το `DBQ` δέχεται τρεις μορφές. Είναι ισοδύναμες για το *digna*· διαφέρουν ως προς το τι πρέπει
να διαμορφωθεί στον host του *digna*:

| Μορφή | Παράδειγμα | Απαιτεί |
|---|---|---|
| **Πλήρης connect descriptor** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Τίποτα — όλα βρίσκονται στην ιδιότητα. Συνιστάται |
| **TNS alias** | `DIGNA_SOURCE` | Το alias πρέπει να υπάρχει στο `tnsnames.ora` του Oracle Client στον host του *digna* |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Έναν Oracle Client που υποστηρίζει Easy Connect (12c και νεότερο) |

!!! tip "Προτιμήστε τον πλήρη descriptor"

    Ένα TNS alias μεταφέρει τον μισό ορισμό της σύνδεσης σε ένα αρχείο στον host του *digna*,
    όπου ξεχνιέται εύκολα όταν ο host ξαναστήνεται ή το *digna* μεταφέρεται. Ο πλήρης
    descriptor κρατά τη σύνδεση αυτοτελή — που είναι και ο σκοπός μιας ρύθμισης χωρίς DSN.

Σημειώστε ότι οι παρενθέσεις ενός descriptor δεν προκαλούν πρόβλημα μέσα σε ένα connection
string, αλλά αν ο κωδικός σας περιέχει `;`, βάλτε τον σε άγκιστρα: `PWD={p@ss;word}`.

---

## 3. Διαμόρφωση του *digna* {: #3-digna-configuration }

Στην οθόνη **Add DB Connection**, δώστε τα εξής:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Σημειώσεις για το Oracle {: #4-notes-on-oracle }

- **Τα schemas είναι χρήστες.** Το *digna* παραθέτει τους χρήστες του Oracle ως schemas, οπότε
  το schema πηγής είναι ο ιδιοκτήτης των πινάκων — `DIGNA_SOURCE_USER` στο παραπάνω παράδειγμα. Ο
  χρήστης της σύνδεσης χρειάζεται `SELECT` σε αυτούς τους πίνακες, είτε απευθείας είτε μέσω
  ρόλου.
- **Μία σύνδεση βλέπει μία βάση δεδομένων.** Ο catalog που προσφέρει το *digna* είναι η βάση
  δεδομένων στην οποία είναι συνδεδεμένη η σύνδεση, οπότε το `DBQ` καθορίζει ποιο service, και
  επομένως ποια βάση δεδομένων, υποβάλλεται σε profiling.
- **Τα αναγνωριστικά γίνονται case-sensitive όταν μπαίνουν σε εισαγωγικά.** Το *digna* βάζει σε
  εισαγωγικά τα ονόματα που διαβάζει από το data dictionary, δηλαδή ό,τι αποθηκεύει το Oracle —
  κεφαλαία για αντικείμενα χωρίς εισαγωγικά.
- **Profiling modes.** Το *Permanent* δημιουργεί τους πίνακες εργασίας στο **Work Schema**, οπότε
  ο χρήστης χρειάζεται `CREATE TABLE` εκεί και quota στο tablespace. Το *Session* χρησιμοποιεί
  έναν private temporary table (`ORA$PTT_…`, Oracle 18c και νεότερο) και δεν αγγίζει το
  **Work Schema**. Το *Standard* χρειάζεται μόνο πρόσβαση ανάγνωσης.

---

## 5. Επαλήθευση του Driver (προαιρετικό) {: #5-verifying-the-driver-optional }

Η διαμόρφωση μιας πηγής δεδομένων ODBC δεν απαιτείται για σύνδεση χωρίς DSN, αλλά το παράθυρο
διαλόγου του ίδιου του driver είναι ένας βολικός τρόπος να επιβεβαιώσετε ότι ο Oracle Client, το
service name και τα διαπιστευτήριά σας λειτουργούν, πριν τα εισαγάγετε στο *digna*.

#### Βήμα 1
![Βήμα 1](images/oracle/create_odbc_data_source_step1.png)

Το **TNS Service Name** που προσφέρεται εδώ προέρχεται από το `tnsnames.ora` της εγκατάστασης
του Oracle Client σας — εκεί ορίζεται το alias, και μαζί του ο host, το port και το service
name. Στο *digna* μπορείτε να χρησιμοποιήσετε το alias ως `DBQ` ή, εναλλακτικά, τον πλήρη
descriptor.

#### Βήμα 2 – Δοκιμή της σύνδεσης

Κάντε κλικ στο κουμπί **Test Connection**.

![Βήμα 2](images/oracle/create_odbc_data_source_step2.png)

Δώστε τον κωδικό πρόσβασης και κάντε κλικ στο κουμπί **OK**.

![Βήμα 3](images/oracle/create_odbc_data_source_step3.png)

Ένα μήνυμα επιτυχίας επιβεβαιώνει ότι ο driver και τα διαπιστευτήρια λειτουργούν.