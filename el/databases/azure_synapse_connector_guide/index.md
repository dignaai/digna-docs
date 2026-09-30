# Source Connector για το Azure Synapse Analytics

Αυτός ο οδηγός περιγράφει πώς να διαμορφώσετε το *digna* ώστε να συνδέεται στο Azure Synapse
Analytics μέσω **ODBC**, χρησιμοποιώντας ένα connection string **χωρίς DSN** (DSN-less).
Υποστηρίζονται τόσο τα serverless όσο και τα dedicated SQL pools.

Η πλευρά του *digna* στη ρύθμιση είναι ίδια για κάθε τεχνολογία — πού δημιουργούνται οι
συνδέσεις, πώς κρυπτογραφούνται οι τιμές των ιδιοτήτων, πώς δοκιμάζεται μια σύνδεση και τι
σημαίνουν τα profiling modes. Περιγράφεται στην [Επισκόπηση Συνδέσεων Βάσεων Δεδομένων](overview.md).
Αυτή η σελίδα καλύπτει ό,τι είναι ειδικό για το Azure Synapse.

!!! note "Technology"

    Το Synapse χρησιμοποιεί τη διάλεκτο του SQL Server, οπότε η σύνδεση δημιουργείται με
    **Technology: SQL Server**. Δείτε [MS SQL Server](sqlserver_connector_guide.md) για έναν
    server on-premises.

---

## 1. Εγκατάσταση του ODBC Driver {: #1-install-the-odbc-driver }

Εγκαταστήστε τον **ODBC Driver 18 for SQL Server** στο μηχάνημα που εκτελεί το backend του
*digna*, ακολουθώντας τον [οδηγό εγκατάστασης της Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server),
και διαβάστε το ακριβές καταχωρισμένο όνομα του driver στον host σας, όπως περιγράφεται στην
ενότητα [Εγκατάσταση του ODBC Driver στον Host του digna](overview.md#install-the-driver).

---

## 2. Ιδιότητες ODBC {: #2-odbc-properties }

!!! important "Παράδειγμα, όχι προδιαγραφή"

    Το παρακάτω σύνολο είναι ένας συνδυασμός που είναι γνωστό ότι λειτουργεί. Οι ιδιότητες
    ανήκουν στον ODBC driver της Microsoft, οπότε τα ονόματα, οι προεπιλογές και οι αποδεκτές
    τιμές τους διαφέρουν ανάμεσα σε εκδόσεις driver και πλατφόρμες, και το τι απαιτεί το
    workspace εξαρτάται από το πώς είναι διαμορφωμένο — τύπος pool, μέθοδος αυθεντικοποίησης,
    firewall. Χρησιμοποιήστε το ως σημείο εκκίνησης και ελέγξτε την τεκμηρίωση της έκδοσης
    driver που εγκαταστήσατε.

Προσθέστε τις παρακάτω ιδιότητες στην οθόνη **Add DB Connection**:

| Κλειδί | Παράδειγμα τιμής | Σημειώσεις |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Πρέπει να ταιριάζει με το όνομα του driver που είναι καταχωρισμένο στον host του *digna* |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Όνομα του workspace μαζί με το επίθημα του endpoint — δείτε παρακάτω |
| `DATABASE` | `dignadata` | Η βάση δεδομένων που περιέχει τα schemas πηγής. Είναι η μόνη βάση δεδομένων στην οποία αυτή η σύνδεση μπορεί να κάνει profiling |
| `UID` | `sqladminuser` | SQL login |
| `PWD` | `<password>` | Επιλέξτε **Encrypted** |

Το connection string που προκύπτει μοιάζει ως εξής:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### Η τιμή `SERVER`

Πάρτε το όνομα του Synapse workspace και προσθέστε το επίθημα του endpoint:

| Pool | `SERVER` |
|---|---|
| **Serverless SQL pool** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Dedicated SQL pool** | `<workspace>.sql.azuresynapse.net` |

!!! warning "Το τμήμα `-ondemand` παραλείπεται εύκολα"

    Χωρίς αυτό, το όνομα αντιστοιχεί στο dedicated endpoint, και η σύνδεση είτε αποτυγχάνει είτε
    φτάνει σιωπηλά σε διαφορετικό pool από το επιθυμητό. Και τα δύο endpoints εμφανίζονται στη
    σελίδα επισκόπησης του workspace στο Azure portal.

### Firewall

Το firewall του Synapse workspace πρέπει να επιτρέπει την εξερχόμενη διεύθυνση του host του
*digna*. Προσθέστε την στην ενότητα **Networking** του workspace πριν δοκιμάσετε τη σύνδεση —
μια αποκλεισμένη διεύθυνση εμφανίζεται ως λήξη χρονικού ορίου σύνδεσης και όχι ως σφάλμα
αυθεντικοποίησης.

### Αυθεντικοποίηση με Microsoft Entra ID

Αντί για SQL login, ο driver μπορεί να αυθεντικοποιηθεί μέσω Entra ID. Αντικαταστήστε τα
`UID`/`PWD` με τη μέθοδο αυθεντικοποίησης που αναμένει το workspace σας, για παράδειγμα:

| Κλειδί | Παράδειγμα τιμής | Σημειώσεις |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | Το `UID` παίρνει τότε το application (client) ID και το `PWD` το client secret |
| `Authentication` | `ActiveDirectoryMSI` | Managed identity του host του *digna*, δεν χρειάζονται διαπιστευτήρια |

---

## 3. Διαμόρφωση του *digna* {: #3-digna-configuration }

Στην οθόνη **Add DB Connection**, δώστε τα εξής:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Σημειώσεις για το Azure Synapse {: #4-notes-on-azure-synapse }

- **Τα serverless pools υποστηρίζουν μόνο *Standard* profiling.** Ένα serverless SQL pool δεν
  μπορεί να δημιουργήσει πίνακες σε βάση δεδομένων, οπότε δεν μπορεί να εκτελεστεί ούτε
  *Permanent* ούτε *Session* profiling. Το *Standard* υπολογίζει τις μετρικές απευθείας στην
  πηγή, κάτι που είναι και η φθηνότερη επιλογή, αφού το serverless χρεώνεται ανά όγκο δεδομένων
  που επεξεργάζεται.
- **Μία σύνδεση βλέπει μία βάση δεδομένων.** Το *digna* προσφέρει τα schemas της βάσης δεδομένων
  που ορίζεται στο `DATABASE`, επειδή το Synapse, όπως και ο SQL Server, αναφέρει μόνο την
  τρέχουσα βάση δεδομένων ως catalog.
- **Η κρυπτογράφηση είναι ενεργή από προεπιλογή** στον Driver 18, και τα endpoints του Synapse
  παρουσιάζουν έγκυρα δημόσια πιστοποιητικά, οπότε δεν χρειάζεται ιδιότητα `Encrypt` ή
  `TrustServerCertificate`.
- **Ένα serverless endpoint μπορεί να επανέρχεται από αδράνεια** στην πρώτη σύνδεση. Αν η δοκιμή
  σύνδεσης λήξει λόγω χρονικού ορίου σε ένα pool που δεν έχει χρησιμοποιηθεί για κάποιο διάστημα,
  δοκιμάστε ξανά.

---

## 5. Επαλήθευση του Driver (προαιρετικό) {: #5-verifying-the-driver-optional }

Η διαμόρφωση μιας πηγής δεδομένων ODBC δεν απαιτείται για σύνδεση χωρίς DSN, αλλά ο οδηγός
(wizard) του ίδιου του driver είναι ένας βολικός τρόπος να επιβεβαιώσετε ότι ο driver λειτουργεί
και ότι το workspace δέχεται τα διαπιστευτήριά σας, πριν τα εισαγάγετε στο *digna*.

#### Βήμα 1
![Βήμα 1](images/azure_synapse/create_odbc_data_source_step1.png)

Συμπληρώστε το πεδίο "Server".
Χρησιμοποιήστε το όνομα του Synapse workspace και επεκτείνετέ το με ".sql.azuresynapse.net".  
**Προσοχή**: αν θέλετε να συνδεθείτε μέσω serverless SQL pool, βεβαιωθείτε ότι συμπεριλάβατε το
"-ondemand", όπως φαίνεται στο παραπάνω στιγμιότυπο οθόνης.

Κάντε κλικ στο κουμπί **Next >**.

#### Βήμα 2
![Βήμα 2](images/azure_synapse/create_odbc_data_source_step2.png)

Επιλέξτε τη μέθοδο αυθεντικοποίησης (π.χ. όνομα χρήστη και κωδικός πρόσβασης)
και δώστε τα απαιτούμενα στοιχεία.

Κάντε κλικ στο κουμπί **Next >**.

#### Βήμα 3
![Βήμα 3](images/azure_synapse/create_odbc_data_source_step3.png)

Επιλέξτε τις ρυθμίσεις συμβατότητας ANSI και έπειτα κάντε κλικ στο κουμπί **Next >**.

#### Βήμα 4
![Βήμα 4](images/azure_synapse/create_odbc_data_source_step4.png)

Μπορείτε να αφήσετε τις προεπιλεγμένες ρυθμίσεις ή να επιλέξετε όσες χρειάζεστε
και να κάνετε κλικ στο κουμπί **Finish**. 

#### Βήμα 5
![Βήμα 5](images/azure_synapse/create_odbc_data_source_step5.png)

Τώρα κάντε κλικ στο κουμπί **Test datasource**.

#### Βήμα 6
![Βήμα 6](images/azure_synapse/create_odbc_data_source_step6.png)

Μια οθόνη επιτυχίας επιβεβαιώνει ότι ο driver, το endpoint και τα διαπιστευτήρια λειτουργούν. Οι
τιμές που εισαγάγατε είναι ακριβώς οι τιμές που παίρνουν οι ιδιότητες της [ενότητας 2](#2-odbc-properties).