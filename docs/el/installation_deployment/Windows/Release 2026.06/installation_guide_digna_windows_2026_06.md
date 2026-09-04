---
title: Οδηγός Εγκατάστασης για Windows – digna Έκδοση 2026.06 | τεκμηρίωση digna
description: Βήμα-βήμα οδηγός για την εγκατάσταση της digna Έκδοση 2026.06 σε Windows — απαιτήσεις συστήματος, ρύθμιση PostgreSQL, ρύθμιση web server, ρύθμιση backend και dashboard, εκτέλεση digna ως Windows service και αναβάθμιση σε νέα έκδοση.
keywords: digna εγκατάσταση windows, οδηγός ανάπτυξης digna, ρύθμιση backend digna, εγκατάσταση dashboard digna, ρύθμιση postgresql, υπηρεσία windows digna, οδηγός αναβάθμισης digna
image: /assets/logo_square.png
---

# Οδηγός Εγκατάστασης για Windows για την digna Έκδοση 2026.06

**Έκδοση:** 2026.06

**Τελευταία Ενημέρωση:** 30 Αυγούστου 2026


---

## Περιεχόμενα

1. [Εισαγωγή](#introduction)
2. [Απαιτήσεις Συστήματος](#system-requirements)
3. [Προεγκατάσταση](#pre-installation-setup)
4. [Ρύθμιση PostgreSQL Server](#postgresql-server-setup)
5. [Ρύθμιση Web Server](#web-server-configuration)
6. [Αρχική Εγκατάσταση](#initial-installation)
7. [Ρύθμιση Backend](#backend-configuration)
8. [Ρύθμιση Dashboard](#dashboard-configuration)
9. [Εκτέλεση digna ως Υπηρεσία Windows](#running-digna-as-a-windows-service)
10. [Αναβάθμιση σε Νέα Έκδοση](#upgrading-to-a-new-release)

---

## Εισαγωγή {: #introduction }

### Σχετικά με την digna

Η digna είναι μια ολοκληρωμένη πλατφόρμα με δυνατότητες AI σχεδιασμένη να βελτιστοποιεί τη διαχείριση ποιότητας δεδομένων σε διάφορα περιβάλλοντα δεδομένων όπως warehouses, lakes και lakehouses. Σχεδιασμένη για υψηλή κλιμάκωση και προσαρμοστικότητα, η digna αντιμετωπίζει σύγχρονες προκλήσεις δεδομένων μέσω αυτοματοποίησης, παρακολούθησης σε πραγματικό χρόνο και ανίχνευσης ανωμαλιών.

Η digna αποτελείται από δύο κύρια στοιχεία:

- **dignabackend**: Ο βασικός κινητήρας της εφαρμογής, υπεύθυνος για επεξεργασία δεδομένων και εκτέλεση ελέγχων ποιότητας.
- **dignadashboard**: Διεπαφή web που φιλοξενείται σε web server και παρέχει φιλικό τρόπο αλληλεπίδρασης με την πλατφόρμα digna και οπτικοποίησης μετρήσεων ποιότητας δεδομένων.

### Τι νέο φέρνει η Έκδοση 2026.06

Αυτή η έκδοση ενσωματώνει δυνατότητες observability δεδομένων απευθείας στον κώδικα σας, επιτρέποντας στους προγραμματιστές να παρακολουθούν την ποιότητα των δεδομένων στην πηγή. Δείτε τις [σημειώσεις έκδοσης](http://docs.digna.ai/changelog/Release_202606/) για πλήρεις λεπτομέρειες.

---

## Απαιτήσεις Συστήματος {: #system-requirements }

Πριν ξεκινήσετε την εγκατάσταση, βεβαιωθείτε ότι το σύστημά σας ικανοποιεί τις παρακάτω ελάχιστες απαιτήσεις:

| Απαίτηση | Προδιαγραφή |
|---|---|
| **Λειτουργικό Σύστημα** | Windows Server ή Windows 10/11 |
| **Μνήμη (Ελάχιστη Ρύθμιση)** | 16 GB RAM |
| **Χώρος Δίσκου** | 10 GB διαθέσιμος χώρος |
| **Βάση Δεδομένων** | PostgreSQL Server 12 ή νεότερο |
| **Web Server** | IIS, Apache Tomcat ή ισοδύναμο |

### Επιλογές Εγκατάστασης Βάσης Δεδομένων

**Αν το PostgreSQL είναι ήδη εγκατεστημένο:**
Μπορείτε να προσθέσετε μια νέα βάση δεδομένων για την digna στη υπάρχουσα PostgreSQL εγκατάστασή σας.

**Αν εγκαθιστάτε PostgreSQL στην ίδια μηχανή με την digna:**

> **⚠️ Συνιστώμενες Προδιαγραφές**
>
> - **Μνήμη**: 32 GB RAM (αντί για 16 GB)
> - **Χώρος Δίσκου**: 50 GB διαθέσιμος χώρος (αντί για 10 GB)
>
> Αυτές οι αυξημένες προδιαγραφές επιτρέπουν την ταυτόχρονη λειτουργία της digna και της βάσης PostgreSQL.

---

## Προεγκατάσταση {: #pre-installation-setup }

Πριν εγκαταστήσετε την digna, βεβαιωθείτε ότι υπάρχουν δύο βασικές προϋποθέσεις:

1. **PostgreSQL Server** – για την αποθήκευση των υπολογισμένων μετρήσεων και των δεδομένων απόδοσης
2. **Web Server** – για τη φιλοξενία του digna Dashboard

Αν αυτά τα στοιχεία δεν έχουν ρυθμιστεί ήδη, ακολουθήστε τις επόμενες ενότητες για να τα εγκαταστήσετε και να τα ρυθμίσετε.

---

## Ρύθμιση PostgreSQL Server {: #postgresql-server-setup }

### Αν έχετε ήδη PostgreSQL

Αν το PostgreSQL είναι ήδη εγκατεστημένο και λειτουργεί τοπικά ή χρησιμοποιείτε managed remote PostgreSQL server, μπορείτε να προχωρήσετε στην [επόμενη ενότητα](#web-server-configuration).

### Εγκατάσταση PostgreSQL

Ακολουθήστε τα παρακάτω βήματα για να εγκαταστήσετε το PostgreSQL σε Windows:

#### Βήμα 1: Κατεβάστε το PostgreSQL

1. Επισκεφτείτε τη σελίδα [PostgreSQL Downloads](https://www.postgresql.org/download/)
2. Επιλέξτε **Windows**
3. Κατεβάστε το τελευταίο installer

#### Βήμα 2: Εκτελέστε τον Installer

1. Κάντε διπλό κλικ στο αρχείο του installer που κατεβάσατε
2. Ακολουθήστε τα βήματα του οδηγού εγκατάστασης

#### Βήμα 3: Επιλογή Καταλόγου Εγκατάστασης

Επιλέξτε τον φάκελο όπου θα εγκατασταθεί το PostgreSQL. Η προεπιλεγμένη τοποθεσία είναι συνήθως κατάλληλη.

#### Βήμα 4: Επιλογή Συστατικών

Για μια τυπική εγκατάσταση, κρατήστε τις προεπιλεγμένες επιλογές συστατικών.

#### Βήμα 5: Ορίστε Κωδικό για τον PostgreSQL Superuser

Εισάγετε και επιβεβαιώστε έναν κωδικό για τον PostgreSQL superuser (`postgres`). **Αποθηκεύστε αυτόν τον κωδικό με ασφάλεια** — θα τον χρειαστείτε αργότερα.

#### Βήμα 6: Ρυθμίστε τον Αριθμό Θύρας

Η προεπιλεγμένη θύρα του PostgreSQL είναι `5432`. Μπορείτε να χρησιμοποιήσετε την προεπιλογή ή να ορίσετε διαφορετική θύρα εάν χρειάζεται.

> **💡 Συμβουλή**
>
> Αν η θύρα 5432 χρησιμοποιείται ήδη, επιλέξτε μια εναλλακτική θύρα και σημειώστε την για μελλοντική ρύθμιση.

#### Βήμα 7: Επιλογή Locale

Επιλέξτε το locale για τη βάση δεδομένων σας. Η προεπιλεγμένη ρύθμιση είναι κατάλληλη για τις περισσότερες εγκαταστάσεις.

#### Βήμα 8: Ολοκλήρωση Εγκατάστασης

Κάντε κλικ **Next** στα υπόλοιπα βήματα και στη συνέχεια **Finish**.

#### Βήμα 9: Επαλήθευση Εγκατάστασης

Ανοίξτε το Command Prompt και επαληθεύστε ότι το PostgreSQL εγκαταστάθηκε:

```bash
psql --version
```

Θα πρέπει να εμφανιστεί η έκδοση του PostgreSQL αν η εγκατάσταση ήταν επιτυχής.

---

## Ρύθμιση Web Server {: #web-server-configuration }

Η digna απαιτεί web server για τη φιλοξενία του dashboard. Επιλέξτε μία από τις παρακάτω επιλογές:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Χρειάζεται να εγκαταστήσετε και να ρυθμίσετε **έναν** από αυτούς τους servers.

### Ρύθμιση IIS {: #iis-setup }

#### Επισκόπηση

Το Internet Information Services (IIS) είναι ο web server της Microsoft για φιλοξενία ιστοτόπων και web εφαρμογών.

#### Ενεργοποίηση IIS

1. **Ανοίξτε τον Πίνακα Ελέγχου**
   - Πατήστε `Win + R`
   - Πληκτρολογήστε `control` και πατήστε Enter

2. **Μεταβείτε σε Windows Features**
   - Κλικ στο **Programs**
   - Επιλέξτε **Turn Windows features on or off**

3. **Ενεργοποιήστε το Internet Information Services**
   - Βρείτε **Internet Information Services (IIS)**
   - Τσεκάρετε το checkbox για να το ενεργοποιήσετε
   - Κάντε κλικ στο **+** για να επεκτείνετε και βεβαιωθείτε ότι επιλέχθηκαν τα υποσυστατικά:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Κλικ στο OK** για εφαρμογή αλλαγών

5. **Επαλήθευση Εγκατάστασης IIS**
   - Ανοίξτε τον browser
   - Μεταβείτε στο `http://localhost`
   - Θα πρέπει να δείτε την σελίδα υποδοχής του IIS

#### Απαιτείται: URL Rewrite Module

Το IIS απαιτεί το component URL Rewrite. Κατεβάστε και εγκαταστήστε το από την [επίσημη σελίδα της Microsoft](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Απαιτείται: MIME Type για Αρχεία Markdown

Για να σιγουρευτείτε ότι τα αρχεία Markdown (`.md`) σερβίρονται σωστά από το IIS:

1. Ανοίξτε το **IIS Manager** (πατήστε `Win + R`, πληκτρολογήστε `inetmgr`, πατήστε Enter)
2. Μεταβείτε σε **Your Site > MIME Types**
3. Κλικ στο **Add...**
4. Διαμορφώστε:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

> **⚠️ Σημαντικό**
>
> Χωρίς αυτή τη ρύθμιση, τα `.md` αρχεία ενδέχεται να μην σερβίρονται σωστά.

---

### Ρύθμιση Apache Tomcat {: #apache-tomcat-setup }

#### Επισκόπηση

Το Apache Tomcat είναι open-source servlet container και web server βασισμένος σε Java.

#### Εγκατάσταση

1. **Κατεβάστε το Apache Tomcat**
   - Επισκεφτείτε τη σελίδα [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Κατεβάστε τη Windows ZIP διανομή

2. **Αποσυμπιέστε το Αρχείο**
   - Αποσυμπιέστε το ZIP σε φάκελο στο σύστημά σας
   - Παράδειγμα: `C:\Program Files\Apache Tomcat`

3. **Επαλήθευση ότι το Tomcat Εκτελείται**
   - Ανοίξτε τον browser
   - Μεταβείτε στο `http://localhost:8080`
   - Θα πρέπει να δείτε τη σελίδα υποδοχής του Apache Tomcat

> **💡 Συμβουλή**
>
> Το Apache Tomcat συνήθως ξεκινά αυτόματα μετά την εγκατάσταση. Αν δεν ξεκινήσει, μεταβείτε στο φάκελο `bin` και εκτελέστε `startup.bat`.

---

## Αρχική Εγκατάσταση {: #initial-installation }

### Βήμα 1: Δημιουργία του Repository της digna

Το repository της digna αποθηκεύει όλες τις μετρήσεις που υπολογίζει η digna. Λειτουργεί ως κεντρική βάση για αναλυτικά και δεδομένα απόδοσης.

#### Δημιουργία Schema και Χρήστη

Ανοίξτε τον PostgreSQL client σας (pgAdmin, psql ή παρόμοιο) και εκτελέστε τις ακόλουθες εντολές SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Αντικαταστήστε τους παρακάτω δεικτοδείκτες:**

- `<digna_repo_schema>` — Το όνομα του schema που θέλετε (π.χ., `dignarepo`)
- `<digna_repo_user>` — Το όνομα χρήστη που θέλετε (π.χ., `digna_user`)
- `<digna_repo_password>` — Ένας ασφαλής κωδικός για αυτό το χρήστη

**Παράδειγμα:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

> **✅ Καλές Πρακτικές**
>
> Χρησιμοποιήστε ισχυρούς, σύνθετους κωδικούς για τους χρήστες της βάσης. Αποφύγετε ευκόλως μαντεύσιμες διαπιστευτήριες.

---

### Βήμα 2: Εξαγωγή του Πακέτου Εγκατάστασης digna

1. Βρείτε το αρχείο ZIP εγκατάστασης της digna που σας παρασχέθηκε
2. Εξαγάγετέ το στην επιθυμητή τοποθεσία εγκατάστασης
3. Μετά την εξαγωγή, θα πρέπει να δείτε τα παρακάτω στοιχεία:
   - `dashboard/` — Διεπαφή web dashboard
   - `digna` — Κύριο εκτελέσιμο (backend + CLI σε ένα)
   - `config.toml` — Αρχείο ρύθμισης
   - `license.toml` — Αρχείο άδειας (τοποθετήστε εδώ τη δική σας άδεια)

### Βήμα 3: Εγκατάσταση του Αρχείου Άδειας

> **⚠️ Σημαντικό**
>
> Το αρχείο άδειας **δεν** περιλαμβάνεται στο πακέτο εγκατάστασης και θα σας παραδοθεί ξεχωριστά από την digna.

1. Εντοπίστε το αρχείο `license.toml` που σας παραχωρήθηκε
2. Αντιγράψτε το στον root κατάλογο εγκατάστασης της digna (όπου βρίσκονται το `config.toml` και το εκτελέσιμο `digna`)

**Γιατί αυτό είναι σημαντικό:**
Το αρχείο άδειας περιέχει πληροφορίες πελάτη, ημερομηνία λήξης άδειας και ψηφιακή υπογραφή. **Μην τροποποιείτε αυτό το αρχείο** — οποιαδήποτε αλλαγή το ακυρώνει.

**Δομή φακέλων μετά τη ρύθμιση:**

```
digna_installation/
├── config.toml         (αρχείο ρύθμισης)
├── license.toml        (ΤΟ ΑΡΧΕΙΟ ΑΔΕΙΑΣ ΣΑΣ - αντιγράψτε το εδώ)
├── digna               (κύριο εκτελέσιμο)
└── dashboard/          (web διεπαφή)
    └── (αρχεία dashboard)
```

---

## Ρύθμιση Backend {: #backend-configuration }

### Βήμα 1: Δημιουργία και Επεξεργασία του Αρχείου Ρύθμισης

Το αρχείο `config_template.toml` παρέχεται στον κατάλογο εγκατάστασης της digna. Απλά μετονομάστε το σε `config.toml`.

**Τοποθεσία:** `digna_installation/config.toml`

Ανοίξτε το `config.toml` σε έναν επεξεργαστή κειμένου και ρυθμίστε κάθε ενότητα παρακάτω.

#### Ενότητα [app]

Αυτή η ενότητα ρυθμίζει τις ρυθμίσεις της εφαρμογής backend της digna:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Παράμετρος | Τιμή | Σημειώσεις |
|---|---|---|
| `digna_APP_HOST` | `localhost` ή διεύθυνση IP | Hostname ή IP όπου φιλοξενείται το dignabackend |
| `digna_APP_PORT` | `8082` (προεπιλογή) | Θύρα για τα REST API endpoints |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL frontend | Αν το dashboard είναι σε διαφορετικό server, συμπεριλάβετε την URL του |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Απαιτείται για CORS με credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Επιτρέπει όλες τις μεθόδους HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Επιτρέπει όλα τα headers |

#### Ενότητα [repo]

Αυτή η ενότητα ρυθμίζει τη σύνδεση με τη βάση PostgreSQL:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Παράμετρος | Τιμή | Σημειώσεις |
|---|---|---|
| `digna_REPO_HOST` | `localhost` ή IP | Hostname/IP του PostgreSQL server |
| `digna_REPO_PORT` | `5432` (προεπιλογή) | Θύρα PostgreSQL |
| `digna_REPO_DB` | `postgres` | Όνομα βάσης δεδομένων |
| `digna_REPO_SCHEMA` | `dignarepo` | Το schema που δημιουργήθηκε νωρίτερα |
| `digna_REPO_USER` | `digna_user` | Ο χρήστης που δημιουργήθηκε στη ρύθμιση PostgreSQL |
| `digna_REPO_PASSWORD` | Ο κωδικός σας | Ο κωδικός που ορίστηκε κατά τη δημιουργία του schema |

#### Ενότητα [base]

Αυτή η ενότητα περιέχει ρυθμίσεις ασφαλείας και cookies:

```toml
[base]
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| Παράμετρος | Τιμή | Σημειώσεις |
|---|---|---|
| `digna_FERNET_KEY` | Κλειδί κρυπτογράφησης | Χρησιμοποιείται για κρυπτογράφηση tokens και cookies (παρέχεται προεπιλογή) |
| `digna_COOKIE_DOMAIN` | `localhost` | Να ταιριάζει με το domain του frontend |
| `digna_COOKIE_SECURE` | `false` (τοπικά) / `true` (production) | Χρησιμοποιήστε `true` για συνδέσεις HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Πάντα ενεργοποιημένο για λόγους ασφαλείας |
| `digna_COOKIE_SAME_SITE` | `lax` | Αποτρέπει επιθέσεις CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ώρες) | Χρόνος λήξης συνεδρίας σε δευτερόλεπτα |
| `digna_MAX_WORKERS` | Αριθμός πυρήνων CPU - 1 | Αριθμός παράλληλων εργασιών επιθεώρησης |

#### Ενότητα [logging]

Αυτή η ενότητα ρυθμίζει τη συμπεριφορά logging:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Παράμετρος | Τιμή | Σημειώσεις |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` ή `DEBUG` | `INFO` για παραγωγή, `DEBUG` για αποσφαλμάτωση |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Αριθμός ημερησίων αντιγράφων logs προς διατήρηση |

---

### Βήμα 3: Αρχικοποίηση του Repository

1. Ανοίξτε το Command Prompt
2. Μεταβείτε στον κατάλογο εγκατάστασης της digna (όπου βρίσκονται το `config.toml` και το εκτελέσιμο `digna`)
3. Εκτελέστε το τεστ σύνδεσης:

```bash
digna repo check
```

Θα πρέπει να δείτε μια επιβεβαίωση ότι η σύνδεση έχει εγκαθιδρυθεί (το repository δεν έχει αρχικοποιηθεί ακόμα).

### Βήμα 4: Εγκατάσταση Schema του Repository

Στον ίδιο κατάλογο, εκτελέστε:

```bash
digna repo install
```

Αυτή η εντολή εγκαθιστά τους απαραίτητους πίνακες και το schema στη βάση PostgreSQL σας.

### Βήμα 5: Εκκίνηση του digna Server

Στον κατάλογο εγκατάστασης της digna, ξεκινήστε τον server με:

```bash
digna serve --address <host> --port <port>
```

**Παράμετροι:**
- `--address` — Hostname/IP του server
- `--port` — Θύρα server

Θα πρέπει να δείτε μηνύματα εκκίνησης που επιβεβαιώνουν ότι ο server εκτελείται:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Βήμα 6: Δημιουργία Χρήστη Admin

1. Ανοίξτε ένα **νέο** παράθυρο Command Prompt
2. Μεταβείτε στον κατάλογο εγκατάστασης της digna
3. Εκτελέστε την παρακάτω εντολή για να δημιουργήσετε χρήστη με δικαιώματα admin:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Παράδειγμα:**

```bash
digna user add "Admin User" AdminPassword123! --su
```

Αυτό δημιουργεί έναν χρήστη με πλήρη διοικητικά προνόμια.

> **✅ Καλές Πρακτικές**
>
> Χρησιμοποιήστε ισχυρό κωδικό με συνδυασμό κεφαλαίων, πεζών, αριθμών και ειδικών χαρακτήρων.

---

## Ρύθμιση Dashboard {: #dashboard-configuration }

### Βήμα 1: Ανάπτυξη Dashboard στον Web Server

Το dashboard της digna έχει δικό του ξεχωριστό αρχείο `config.toml` που βρίσκεται στον φάκελο `dashboard/`. Αυτή η ρύθμιση παρέχεται ήδη και δεν απαιτεί αλλαγές κατά την αρχική εγκατάσταση. Θα χρειαστεί να την τροποποιήσετε μόνο αν θέλετε να προσαρμόσετε τη σύνδεση με το backend.

Αν χρειάζεται να τροποποιήσετε τη ρύθμιση του dashboard (π.χ. για multi-instance deployments), συμβουλευτείτε την τεκμηρίωση του dashboard.

Επιλέξτε τον web server σας και ακολουθήστε τα αντίστοιχα βήματα ανάπτυξης.

#### Ανάπτυξη στο IIS

1. **Ανοίξτε το IIS Manager**
   - Πατήστε `Win + R`, πληκτρολογήστε `inetmgr`, πατήστε Enter

2. **Δημιουργία Νέου Website**
   - Στο αριστερό πάνελ, δεξί κλικ στο **Sites**
   - Επιλέξτε **Add Website...**

3. **Διαμόρφωση του Website**
   - **Site Name**: Εισάγετε ένα όνομα (π.χ., "dignaDashboard")
   - **Physical Path**: Πατήστε Browse και επιλέξτε το φάκελο `dashboard`
   - **Binding**: Ορίστε IP και θύρα (προεπιλεγμένη θύρα 80 για HTTP, 443 για HTTPS)

4. **Έναρξη του Website**
   - Κλικ **OK** για δημιουργία της τοποθεσίας
   - Δεξί κλικ στο νέο site και επιλέξτε **Start**

5. **Έλεγχος Εγκατάστασης**
   - Ανοίξτε τον browser
   - Μεταβείτε στο `http://localhost` (ή στην ρυθμισμένη URL)
   - Θα πρέπει να δείτε τη σελίδα σύνδεσης του digna dashboard

#### Ανάπτυξη σε Apache Tomcat

1. **Αντιγραφή Dashboard στο Tomcat**
   - Αντιγράψτε τον φάκελο `dashboard` στο directory `webapps` του Tomcat
   - Μετονομάστε τον αν χρειάζεται (π.χ. σε `digna`)
   - Παράδειγμα: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Επαλήθευση Ανάπτυξης**
   - Ανανέωση ή επαναφόρτωση της σελίδας διαχείρισης του Tomcat (http://localhost:8080)
   - Θα πρέπει να δείτε "digna" (ή το όνομα που επιλέξατε) στη λίστα των εφαρμογών

3. **Πρόσβαση στο Dashboard**
   - Ανοίξτε τον browser
   - Μεταβείτε στο `http://localhost:8080/digna`
   - Θα πρέπει να δείτε τη σελίδα σύνδεσης του digna dashboard

---

## Εκτέλεση digna ως Υπηρεσία Windows {: #running-digna-as-a-windows-service }

### Γιατί να Χρησιμοποιήσετε μια Υπηρεσία Windows;

Η εκτέλεση του backend της digna ως υπηρεσία Windows διασφαλίζει ότι:
- Ξεκινά αυτόματα κατά την εκκίνηση του server
- Τρέχει στο παρασκήνιο χωρίς ανοιχτό Command Prompt
- Επανεκκινείται αυτόματα σε περίπτωση κατάρρευσης
- Μπορεί να διαχειρίζεται μέσω των Windows Services

### Αρχεία Διαχείρισης Υπηρεσίας

Όλα τα απαραίτητα αρχεία βρίσκονται στον κατάλογο εγκατάστασης της digna υπό: `bin/`

Τα παρακάτω batch αρχεία είναι διαθέσιμα:
- `install_service.bat` — Εγγράφει την digna ως υπηρεσία Windows
- `uninstall_service.bat` — Απεγγράφει την υπηρεσία
- `start_service.bat` — Ξεκινά την υπηρεσία
- `stop_service.bat` — Σταματά την υπηρεσία

> **⚠️ Απαιτείται Διαχειριστής**
>
> Όλα τα batch αρχεία πρέπει να εκτελούνται με δικαιώματα Administrator.

### Εγκατάσταση της Υπηρεσίας

1. **Ανοίξτε το Command Prompt ως Διαχειριστής**
   - Δεξί κλικ στο Command Prompt
   - Επιλέξτε "Run as Administrator"

2. **Μεταβείτε στον φάκελο bin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Εκτελέστε το script εγκατάστασης**
   ```bash
   install_service.bat
   ```

Η digna εγγράφεται πλέον ως υπηρεσία Windows με **αυτόματη εκκίνηση**. Η υπηρεσία δεν ξεκινά άμεσα — δείτε την επόμενη ενότητα για να την ξεκινήσετε.

### Εκκίνηση και Σταμάτημα της Υπηρεσίας

#### Για να Ξεκινήσετε την Υπηρεσία

1. Ανοίξτε το Command Prompt ως Διαχειριστής
2. Μεταβείτε στο `digna\bin`
3. Εκτελέστε:
   ```bash
   start_service.bat
   ```

#### Για να Σταματήσετε την Υπηρεσία

1. Ανοίξτε το Command Prompt ως Διαχειριστής
2. Μεταβείτε στο `digna\bin`
3. Εκτελέστε:
   ```bash
   stop_service.bat
   ```

> **💡 Συμβουλή**
>
> Πάντα σταματάτε την υπηρεσία πριν ενημερώσετε αρχεία της εφαρμογής.

### Μετακίνηση της Υπηρεσίας σε Νέο Κατάλογο

Αν χρειαστεί να μεταφέρετε την εγκατάσταση της digna:

1. **Απεγκαταστήστε την Τρέχουσα Υπηρεσία**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Μετακινήστε τα Αρχεία της Εφαρμογής**
   - Μετακινήστε ολόκληρο το φάκελο εγκατάστασης της digna στη νέα τοποθεσία

3. **Εγκαταστήστε ξανά την Υπηρεσία**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Ξεκινήστε την Υπηρεσία**
   ```bash
   start_service.bat
   ```

### Απεγκατάσταση της Υπηρεσίας

1. **Σταματήστε την Τρέχουσα Υπηρεσία**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Απεγκαταστήστε την Υπηρεσία**
   ```bash
   uninstall_service.bat
   ```

Η digna δεν είναι πλέον εγγεγραμμένη ως υπηρεσία Windows.

---

## Αναβάθμιση σε Νέα Έκδοση {: #upgrading-to-a-new-release }

### Πριν την Αναβάθμιση

**Η Δημιουργία Backup του Repository digna είναι Υποχρεωτική**

Πριν αναβαθμίσετε την digna, δημιουργήστε αντίγραφο ασφαλείας του repository (PostgreSQL) για να προστατευτείτε από απώλεια δεδομένων.
Ένα backup διασφαλίζει ότι μπορείτε να επαναφέρετε σε περίπτωση που η αναβάθμιση αντιμετωπίσει απρόοπτα προβλήματα.

### Διαδικασία Αναβάθμισης

#### Βήμα 1: Σταματήστε την υπηρεσία digna

Αν η digna τρέχει ως υπηρεσία Windows, σταματήστε την πρώτα:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Βήμα 2: Backup της Τρέχουσας Εγκατάστασης Backend

Στον κατάλογο εγκατάστασης της digna:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### Βήμα 3: Εξαγωγή και Ανάπτυξη της Νέας Έκδοσης

1. Εξαγάγετε το νέο αρχείο ZIP εγκατάστασης της digna
2. Αντιγράψτε το νέο εκτελέσιμο `digna` και τον φάκελο `dashboard` στον κατάλογο εγκατάστασης σας


> **✅ Σημαντικό**
>
> Το αρχείο `config.toml` **ποτέ** δεν περιλαμβάνεται στο ZIP εγκατάστασης. Η υπάρχουσα ρύθμισή σας παραμένει ασφαλής.

### Βήμα 4: Επαναφορά των Αρχείων Ρύθμισης

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Βήμα 5: Αναβάθμιση του Schema του Repository

Μεταβείτε στον κατάλογο εγκατάστασης της digna και εκτελέστε:

```bash
digna repo upgrade
```

Αυτό ενημερώνει το schema του PostgreSQL στην τελευταία έκδοση διατηρώντας όλα τα υπάρχοντα δεδομένα.

### Βήμα 6: Επανεκκίνηση Υπηρεσιών

Αν τρέχετε ως υπηρεσία Windows:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Αν τρέχετε χειροκίνητα, επανεκκινήστε τον server:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Αν χρησιμοποιείτε IIS ή Tomcat, επανεκκινήστε τον αντίστοιχο web server.

#### Βήμα 7: Επαλήθευση της Αναβάθμισης

1. Εκκινήστε το digna dashboard
2. Επαληθεύστε ότι η διεπαφή φορτώνει σωστά
3. Ελέγξτε τα logs του server για τυχόν σφάλματα
