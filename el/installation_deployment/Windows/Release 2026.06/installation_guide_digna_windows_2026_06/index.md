# Οδηγός Εγκατάστασης Windows για το digna Release 2026.06

**Release:** 2026.06

**Τελευταία Ενημέρωση:** 30 Αυγούστου 2026


---

## Πίνακας Περιεχομένων

1. [Εισαγωγή](#introduction)
2. [Απαιτήσεις Συστήματος](#system-requirements)
3. [Προεγκατάσταση](#pre-installation-setup)
4. [Διαμόρφωση PostgreSQL Server](#postgresql-server-setup)
5. [Διαμόρφωση Web Server](#web-server-configuration)
6. [Αρχική Εγκατάσταση](#initial-installation)
7. [Διαμόρφωση Backend](#backend-configuration)
8. [Διαμόρφωση Dashboard](#dashboard-configuration)
9. [Εκτέλεση του digna ως Υπηρεσία Windows](#running-digna-as-a-windows-service)
10. [Αναβάθμιση σε Νέα Έκδοση](#upgrading-to-a-new-release)

---

## Εισαγωγή {: #introduction }

### Σχετικά με το digna

Το digna είναι μια ολοκληρωμένη πλατφόρμα με AI που έχει σχεδιαστεί για να βελτιστοποιεί τη διαχείριση ποιότητας δεδομένων σε διάφορα περιβάλλοντα δεδομένων όπως warehouses, lakes και lakehouses. Χτισμένο για υψηλή κλιμάκωση και προσαρμοστικότητα, το digna αντιμετωπίζει τις σύγχρονες προκλήσεις δεδομένων μέσω αυτοματισμού, παρακολούθησης σε πραγματικό χρόνο και ανίχνευσης ανωμαλιών.

Το digna αποτελείται από δύο κύρια συστατικά:

- **dignabackend**: Ο βασικός πυρήνας της εφαρμογής, υπεύθυνος για την επεξεργασία δεδομένων και την εκτέλεση ελέγχων ποιότητας.
- **dignadashboard**: Μια web διεπαφή που φιλοξενείται σε web server, παρέχοντας έναν φιλικό τρόπο αλληλεπίδρασης με την πλατφόρμα digna και οπτικοποίησης μετρικών ποιότητας δεδομένων.

### Τι νέο υπάρχει στην Έκδοση 2026.06

Αυτή η έκδοση ενσωματώνει δυνατότητες παρατηρησιμότητας δεδομένων άμεσα στον κώδικα σας, επιτρέποντας στους προγραμματιστές να παρακολουθούν την ποιότητα των δεδομένων στην πηγή. Δείτε τις [σημειώσεις έκδοσης](http://docs.digna.ai/changelog/Release_202606/) για πλήρεις λεπτομέρειες.

### Ψάχνετε για macOS ή Linux;

Αυτός ο οδηγός καλύπτει τα Windows. Για άλλες πλατφόρμες, δείτε τον [Οδηγό Εγκατάστασης για macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) ή τον [Οδηγό Εγκατάστασης για Linux](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Απαιτήσεις Συστήματος {: #system-requirements }

Πριν ξεκινήσετε την εγκατάσταση, βεβαιωθείτε ότι το σύστημά σας πληροί τις παρακάτω ελάχιστες απαιτήσεις:

| Απαίτηση | Προδιαγραφή |
|---|---|
| **Λειτουργικό Σύστημα** | Windows Server ή Windows 10/11 |
| **Μνήμη (Ελάχιστη Εγκατάσταση)** | 16 GB RAM |
| **Χώρος Δίσκου** | 10 GB διαθέσιμου χώρου |
| **Βάση Δεδομένων** | PostgreSQL Server 12 ή νεότερο |
| **Web Server** | IIS, Apache Tomcat, ή αντίστοιχο |

### Επιλογές Εγκατάστασης Βάσης Δεδομένων

**Αν το PostgreSQL είναι ήδη εγκατεστημένο:**
Μπορείτε να προσθέσετε μια νέα βάση δεδομένων για το digna στον υπάρχοντα PostgreSQL Server.

**Αν θα εγκαταστήσετε το PostgreSQL στο ίδιο μηχάνημα με το digna:**

!!! info "Συνιστώμενες Προδιαγραφές"

    - **Μνήμη**: 32 GB RAM (αντί για 16 GB)
    - **Χώρος Δίσκου**: 50 GB διαθέσιμος χώρος (αντί για 10 GB)

    Αυτές οι υψηλότερες προδιαγραφές υποστηρίζουν τόσο το digna όσο και τη βάση δεδομένων PostgreSQL που τρέχουν ταυτόχρονα.

---

## Προεγκατάσταση {: #pre-installation-setup }

Πριν εγκαταστήσετε το digna, βεβαιωθείτε ότι υπάρχουν δύο βασικές προϋποθέσεις:

1. **PostgreSQL Server** – για την αποθήκευση υπολογισμένων μετρικών και δεδομένων απόδοσης
2. **Web Server** – για τη φιλοξενία του digna Dashboard

Αν αυτά τα στοιχεία δεν έχουν ρυθμιστεί ακόμη, ακολουθήστε τις παρακάτω ενότητες για να τα εγκαταστήσετε και να τα ρυθμίσετε.

---

## Διαμόρφωση PostgreSQL Server {: #postgresql-server-setup }

### Αν έχετε ήδη PostgreSQL

Αν το PostgreSQL είναι ήδη εγκατεστημένο και λειτουργεί τοπικά ή χρησιμοποιείτε διαχειριζόμενο απομακρυσμένο PostgreSQL server, μπορείτε να μεταβείτε στην [επόμενη ενότητα](#web-server-configuration).

### Εγκατάσταση PostgreSQL

Ακολουθήστε αυτά τα βήματα για να εγκαταστήσετε το PostgreSQL σε Windows:

#### Βήμα 1: Κατεβάστε το PostgreSQL

1. Επισκεφτείτε τη σελίδα [PostgreSQL Downloads](https://www.postgresql.org/download/)
2. Επιλέξτε **Windows**
3. Κατεβάστε τον πιο πρόσφατο installer

#### Βήμα 2: Εκτελέστε τον Installer

1. Κάντε διπλό κλικ στο αρχείο installer που κατεβάσατε
2. Ακολουθήστε τα βήματα του οδηγού εγκατάστασης

#### Βήμα 3: Επιλογή Καταλόγου Εγκατάστασης

Επιλέξτε τον κατάλογο όπου θα εγκατασταθεί το PostgreSQL. Η προεπιλεγμένη τοποθεσία είναι συνήθως κατάλληλη.

#### Βήμα 4: Επιλογή Στοιχείων Εγκατάστασης

Για μία τυπική εγκατάσταση, κρατήστε τις προεπιλεγμένες επιλογές των συστατικών.

#### Βήμα 5: Ορισμός Κωδικού του Superuser του PostgreSQL

Εισάγετε και επιβεβαιώστε έναν κωδικό για τον superuser του PostgreSQL (`postgres`). **Αποθηκεύστε αυτόν τον κωδικό με ασφάλεια** — θα τον χρειαστείτε αργότερα.

#### Βήμα 6: Διαμόρφωση Αριθμού Θύρας

Η προεπιλεγμένη θύρα του PostgreSQL είναι `5432`. Μπορείτε να χρησιμοποιήσετε την προεπιλογή ή να ορίσετε άλλη θύρα εάν χρειάζεται.

!!! tip "Συμβουλή"

    Αν η θύρα 5432 χρησιμοποιείται ήδη, επιλέξτε μια εναλλακτική θύρα και σημειώστε την για μελλοντικές ρυθμίσεις.

#### Βήμα 7: Επιλογή Locale

Επιλέξτε το locale για τη βάση δεδομένων σας. Η προεπιλογή είναι συνήθως κατάλληλη για τις περισσότερες εγκαταστάσεις.

#### Βήμα 8: Ολοκλήρωση Εγκατάστασης

Κάντε κλικ στο **Next** για τα υπόλοιπα βήματα και τέλος **Finish**.

#### Βήμα 9: Επαλήθευση Εγκατάστασης

Ανοίξτε το Command Prompt και επαληθεύστε ότι το PostgreSQL είναι εγκατεστημένο:

```bash
psql --version
```

Θα δείτε την έκδοση του PostgreSQL αν η εγκατάσταση ήταν επιτυχής.

---

## Διαμόρφωση Web Server {: #web-server-configuration }

Το digna απαιτεί έναν web server για να φιλοξενήσει το dashboard. Επιλέξτε μία από τις ακόλουθες επιλογές:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Χρειάζεται να εγκαταστήσετε και να ρυθμίσετε **έναν** μόνο από αυτούς τους servers.

### Ρύθμιση IIS {: #iis-setup }

#### Επισκόπηση

Το Internet Information Services (IIS) είναι ο web server της Microsoft για τη φιλοξενία ιστοτόπων και web εφαρμογών.

#### Ενεργοποίηση IIS

1. **Άνοιγμα Πίνακα Ελέγχου**
   - Πατήστε `Win + R`
   - Πληκτρολογήστε `control` και πατήστε Enter

2. **Μετάβαση σε Windows Features**
   - Κάντε κλικ στο **Programs**
   - Επιλέξτε **Turn Windows features on or off**

3. **Ενεργοποίηση Internet Information Services**
   - Κάντε κύλιση και βρείτε **Internet Information Services (IIS)**
   - Επιλέξτε το checkbox για να το ενεργοποιήσετε
   - Κάντε κλικ στο **+** για να επεκτείνετε και επαληθεύστε ότι έχουν επιλεγεί τα εξαρτήματα:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Κλικ στο OK** για να εφαρμοστούν οι αλλαγές

5. **Επαλήθευση Εγκατάστασης IIS**
   - Ανοίξτε τον browser σας
   - Μεταβείτε στο `http://localhost`
   - Πρέπει να δείτε τη σελίδα καλωσορίσματος του IIS

#### Απαιτείται: URL Rewrite Module

Το IIS χρειάζεται το component URL Rewrite. Κατεβάστε και εγκαταστήστε το από τη [επίσημη σελίδα της Microsoft](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Απαιτείται: MIME Type για Αρχεία Markdown

Για να διασφαλίσετε ότι τα αρχεία Markdown (`.md`) σερβίρονται σωστά από το IIS:

1. Ανοίξτε το **IIS Manager** (πατήστε `Win + R`, πληκτρολογήστε `inetmgr`, πατήστε Enter)
2. Πλοηγηθείτε στο **Your Site > MIME Types**
3. Κάντε κλικ στο **Add...**
4. Διαμορφώστε:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Σημαντικό"

    Χωρίς αυτήν τη ρύθμιση, τα αρχεία `.md` ενδέχεται να μην σερβίρονται σωστά.

---

### Ρύθμιση Apache Tomcat {: #apache-tomcat-setup }

#### Επισκόπηση

Το Apache Tomcat είναι ένας open-source servlet container και web server Java.

#### Εγκατάσταση

1. **Κατεβάστε το Apache Tomcat**
   - Επισκεφτείτε [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Κατεβάστε τη διανομή ZIP για Windows

2. **Αποσυμπιέστε το αρχειο**
   - Αποσυμπιέστε το ZIP σε έναν κατάλογο στο σύστημά σας
   - Παράδειγμα: `C:\Program Files\Apache Tomcat`

3. **Επαληθεύστε ότι το Tomcat τρέχει**
   - Ανοίξτε τον browser σας
   - Μεταβείτε στο `http://localhost:8080`
   - Πρέπει να δείτε τη σελίδα καλωσορίσματος του Apache Tomcat

!!! tip "Συμβουλή"

    Το Apache Tomcat συνήθως ξεκινά αυτόματα μετά την εγκατάσταση. Αν δεν ξεκίνησε, πλοηγηθείτε στο φάκελο `bin` και τρέξτε `startup.bat`.

---

## Αρχική Εγκατάσταση {: #initial-installation }

### Βήμα 1: Ρύθμιση του Repository του digna

Το repository του digna αποθηκεύει όλες τις μετρικές που υπολογίζει το digna. Λειτουργεί ως κεντρική βάση δεδομένων για αναλυτικά και δεδομένα απόδοσης.

#### Δημιουργία Schema και Χρήστη για το Repository

Ανοίξτε τον PostgreSQL client σας (pgAdmin, psql ή παρόμοιο) και εκτελέστε τις ακόλουθες εντολές SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Αντικαταστήστε τα παρακάτω placeholders:**

- `<digna_repo_schema>` — Το όνομα του schema που επιθυμείτε (π.χ., `dignarepo`)
- `<digna_repo_user>` — Το όνομα χρήστη που επιθυμείτε (π.χ., `digna_user`)
- `<digna_repo_password>` — Ένας ασφαλής κωδικός για αυτόν τον χρήστη

**Παράδειγμα:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Καλύτερη Πρακτική"

    Χρησιμοποιήστε ισχυρούς, πολύπλοκους κωδικούς για τους χρήστες της βάσης δεδομένων. Αποφύγετε εύκολα μαντεύσιμες διαπιστεύσεις.

---

### Βήμα 2: Εξαγωγή του Πακέτου Εγκατάστασης του digna

1. Εντοπίστε το αρχείο ZIP εγκατάστασης του digna που σας παρασχέθηκε
2. Εξαγάγετέ το στην επιθυμητή τοποθεσία εγκατάστασης
3. Μετά την εξαγωγή, θα δείτε τα εξής στοιχεία:
   - `dashboard/` — Web διεπαφή dashboard
   - `digna` — Κύριο εκτελέσιμο (backend + CLI σε ένα)
   - `config.toml` — Αρχείο ρυθμίσεων
   - `license.toml` — Αρχείο άδειας (τοποθετήστε εδώ τη δική σας άδεια)

### Βήμα 3: Εγκατάσταση του Αρχείου Άδειας

!!! warning "Σημαντικό"

    Το αρχείο άδειας **δεν** περιλαμβάνεται στο πακέτο εγκατάστασης και θα σας παρασχεθεί χωριστά από την digna.

1. Εντοπίστε το αρχείο `license.toml` που σας παρασχέθηκε
2. Αντιγράψτε το στον ριζικό κατάλογο εγκατάστασης του digna (όπου βρίσκονται το `config.toml` και το εκτελέσιμο `digna`)

**Γιατί είναι σημαντικό:**
Το αρχείο άδειας περιέχει τις πληροφορίες πελάτη, την ημερομηνία λήξης της άδειας και την ψηφιακή υπογραφή. **Μην τροποποιήσετε αυτό το αρχείο** — οποιαδήποτε αλλαγή θα το ακυρώσει.

**Δομή καταλόγων μετά τη ρύθμιση:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Διαμόρφωση Backend {: #backend-configuration }

### Βήμα 1: Δημιουργία και Επεξεργασία του Αρχείου Διαμόρφωσης

Το αρχείο `config_template.toml` παρέχεται στον κατάλογο εγκατάστασης του digna. Απλώς μετονομάστε το σε `config.toml`.

**Τοποθεσία:** `digna_installation/config.toml`

Ανοίξτε το `config.toml` σε έναν επεξεργαστή κειμένου και διαμορφώστε κάθε ενότητα όπως παρακάτω.

#### Ενότητα [app]

Αυτή η ενότητα διαμορφώνει τις ρυθμίσεις της εφαρμογής backend:

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
| `digna_APP_CORS_ALLOW_ORIGINS` | URL frontend | Αν το dashboard είναι σε διαφορετικό server, προσθέστε το URL του |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Απαραίτητο για CORS με credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Επιτρέπει όλες τις HTTP μεθόδους |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Επιτρέπει όλα τα headers |

#### Ενότητα [repo]

Αυτή η ενότητα διαμορφώνει τη σύνδεση με τη βάση δεδομένων PostgreSQL:

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
| `digna_REPO_SCHEMA` | `dignarepo` | Το schema που δημιουργήσατε νωρίτερα |
| `digna_REPO_USER` | `digna_user` | Ο χρήστης που δημιουργήσατε στο PostgreSQL |
| `digna_REPO_PASSWORD` | Ο κωδικός σας | Κωδικός που ορίσατε κατά τη δημιουργία του schema |

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
| `digna_FERNET_KEY` | Κλειδί κρυπτογράφησης | Χρησιμοποιείται για την κρυπτογράφηση tokens και cookies (παρέχεται προεπιλογή) |
| `digna_COOKIE_DOMAIN` | `localhost` | Να ταιριάζει με το domain του frontend |
| `digna_COOKIE_SECURE` | `false` (τοπικά) / `true` (production) | Χρησιμοποιήστε `true` για συνδέσεις HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Πάντα ενεργοποιημένο για ασφάλεια |
| `digna_COOKIE_SAME_SITE` | `lax` | Αποτρέπει επιθέσεις CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ώρες) | Χρονικό όριο συνεδρίας σε δευτερόλεπτα |
| `digna_MAX_WORKERS` | Αριθμός πυρήνων CPU - 1 | Αριθμός παράλληλων εργασιών επιθεώρησης |

#### Ενότητα [logging]

Αυτή η ενότητα διαμορφώνει τη συμπεριφορά logging:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Παράμετρος | Τιμή | Σημειώσεις |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` ή `DEBUG` | `INFO` για παραγωγή, `DEBUG` για αποσφαλμάτωση |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Αριθμός ημερήσιων αντίγραφων logs που θα φυλάσσονται |

---

### Βήμα 3: Αρχικοποίηση του Repository

1. Ανοίξτε Command Prompt
2. Πλοηγηθείτε στον κατάλογο εγκατάστασης του digna (όπου βρίσκονται `config.toml` και το εκτελέσιμο `digna`)
3. Εκτελέστε τον έλεγχο σύνδεσης:

```bash
digna repo check
```

Θα πρέπει να δείτε μια επιβεβαίωση ότι η σύνδεση έχει εγκαθιδρυθεί (το repository δεν έχει εγκατασταθεί ακόμα).

### Βήμα 4: Εγκατάσταση του Schema του Repository

Στον ίδιο κατάλογο, εκτελέστε:

```bash
digna repo install
```

Η εντολή αυτή εγκαθιστά τους απαραίτητους πίνακες και το schema στη βάση δεδομένων PostgreSQL.

### Βήμα 5: Εκκίνηση του digna Server

Στον κατάλογο εγκατάστασης του digna, ξεκινήστε τον server με:

```bash
digna serve --address <host> --port <port>
```

**Παράμετροι:**
- `--address` — Hostname/IP του server
- `--port` — Θύρα του server

Θα δείτε μηνύματα εκκίνησης που επιβεβαιώνουν ότι ο server τρέχει:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Βήμα 6: Δημιουργία Χρήστη Διαχειριστή

1. Ανοίξτε ένα **νέο** παράθυρο Command Prompt
2. Πλοηγηθείτε στον κατάλογο εγκατάστασης του digna
3. Εκτελέστε την ακόλουθη εντολή για να δημιουργήσετε έναν χρήστη admin:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Παράδειγμα:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

Αυτό δημιουργεί έναν χρήστη με πλήρη δικαιώματα διαχειριστή.

!!! tip "Καλύτερη Πρακτική"

    Χρησιμοποιήστε έναν ισχυρό κωδικό με μείγμα κεφαλαίων, πεζών, αριθμών και ειδικών χαρακτήρων.

---

## Διαμόρφωση Dashboard {: #dashboard-configuration }

### Βήμα 1: Ανάπτυξη του Dashboard στον Web Server

Το digna dashboard έχει το δικό του ξεχωριστό αρχείο `config.toml` που βρίσκεται στον κατάλογο `dashboard/`. Αυτή η διαμόρφωση παρέχεται ήδη και δεν απαιτεί αλλαγές κατά την αρχική εγκατάσταση. Θα χρειαστεί να την τροποποιήσετε μόνο αν θέλετε να προσαρμόσετε τη σύνδεση με το backend.

Αν χρειάζεται να τροποποιήσετε τη ρύθμιση του dashboard (π.χ., για multi-instance deployments), ανατρέξτε στην τεκμηρίωση του dashboard.

Επιλέξτε τον web server σας και ακολουθήστε τα αντίστοιχα βήματα ανάπτυξης.

#### Ανάπτυξη στο IIS

1. **Άνοιγμα IIS Manager**
   - Πατήστε `Win + R`, πληκτρολογήστε `inetmgr`, πατήστε Enter

2. **Δημιουργία Νέου Website**
   - Στο αριστερό πάνελ, κάντε δεξί κλικ στο **Sites**
   - Επιλέξτε **Add Website...**

3. **Διαμόρφωση του Website**
   - **Site Name**: Εισάγετε ένα όνομα (π.χ., "dignaDashboard")
   - **Physical Path**: Κάντε κλικ στο Browse και επιλέξτε τον φάκελο `dashboard`
   - **Binding**: Ορίστε διεύθυνση IP και θύρα (προεπιλεγμένη θύρα 80 για HTTP, 443 για HTTPS)

4. **Έναρξη του Website**
   - Κάντε κλικ στο **OK** για να δημιουργήσετε τον ιστότοπο
   - Κάντε δεξί κλικ στο νέο site και επιλέξτε **Start**

5. **Έλεγχος Εγκατάστασης**
   - Ανοίξτε τον browser σας
   - Μεταβείτε στο `http://localhost` (ή στο ρυθμισμένο URL)
   - Πρέπει να δείτε τη σελίδα εισόδου του digna dashboard

#### Ανάπτυξη σε Apache Tomcat

1. **Αντιγραφή Dashboard στο Tomcat**
   - Αντιγράψτε το φάκελο `dashboard` στον κατάλογο `webapps` του Tomcat
   - Μετονομάστε τον αν χρειάζεται (π.χ., σε `digna`)
   - Παράδειγμα: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Επαλήθευση Ανάπτυξης**
   - Ανανέωση ή φόρτωση της διαχειριστικής σελίδας του Tomcat (http://localhost:8080)
   - Θα πρέπει να δείτε το "digna" (ή το όνομα που επιλέξατε) στη λίστα των αναπτυγμένων εφαρμογών

3. **Πρόσβαση στο Dashboard**
   - Ανοίξτε τον browser σας
   - Μεταβείτε στο `http://localhost:8080/digna`
   - Πρέπει να δείτε τη σελίδα εισόδου του digna dashboard

---

## Εκτέλεση του digna ως Υπηρεσία Windows {: #running-digna-as-a-windows-service }

### Γιατί να χρησιμοποιήσετε Υπηρεσία Windows;

Η εκτέλεση του digna backend ως υπηρεσία Windows διασφαλίζει ότι:
- Ξεκινά αυτόματα όταν κάνει boot ο server
- Τρέχει στο παρασκήνιο χωρίς ανοιχτό παράθυρο Command Prompt
- Επανεκκινείται αυτόματα αν παρουσιαστεί σφάλμα
- Μπορεί να διαχειρίζεται μέσω των Windows Services

### Αρχεία Διαχείρισης Υπηρεσίας

Όλα τα απαραίτητα αρχεία βρίσκονται στο φάκελο εγκατάστασης του digna υπό: `bin/`

Τα παρακάτω αρχεία batch είναι διαθέσιμα:
- `install_service.bat` — Εγγράφει το digna ως υπηρεσία Windows
- `uninstall_service.bat` — Αφαιρεί την εγγραφή της υπηρεσίας
- `start_service.bat` — Ξεκινά την υπηρεσία
- `stop_service.bat` — Σταματά την υπηρεσία

!!! warning "Απαιτούνται δικαιώματα διαχειριστή"

    Όλα τα batch αρχεία πρέπει να εκτελούνται με δικαιώματα Administrator.

### Εγκατάσταση της Υπηρεσίας

1. **Άνοιγμα Command Prompt ως Administrator**
   - Δεξί κλικ στο Command Prompt
   - Επιλέξτε "Run as Administrator"

2. **Πλοήγηση στο φάκελο bin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Εκτέλεση του Script Εγκατάστασης**
   ```bash
   install_service.bat
   ```

Η υπηρεσία digna καταχωρείται τώρα ως υπηρεσία Windows με ενεργοποιημένη την **αυτόματη εκκίνηση**. Η υπηρεσία δεν ξεκινά αμέσως — δείτε την επόμενη ενότητα για το πώς να την ξεκινήσετε.

### Εκκίνηση και Σταμάτημα της Υπηρεσίας

#### Για να ξεκινήσετε την υπηρεσία

1. Ανοίξτε Command Prompt ως Administrator
2. Πλοηγηθείτε στο `digna\bin`
3. Εκτελέστε:
   ```bash
   start_service.bat
   ```

#### Για να σταματήσετε την υπηρεσία

1. Ανοίξτε Command Prompt ως Administrator
2. Πλοηγηθείτε στο `digna\bin`
3. Εκτελέστε:
   ```bash
   stop_service.bat
   ```

!!! tip "Συμβουλή"

    Πάντα σταματάτε την υπηρεσία πριν ενημερώσετε αρχεία της εφαρμογής.

### Μετακίνηση της Υπηρεσίας σε Νέο Κατάλογο

Αν χρειαστεί να μετακινήσετε την εγκατάσταση του digna:

1. **Απεγκατάσταση της τρέχουσας υπηρεσίας**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Μετακίνηση των αρχείων της εφαρμογής**
   - Μετακινήστε ολόκληρο τον φάκελο εγκατάστασης του digna στη νέα τοποθεσία

3. **Εγκατάσταση ξανά της υπηρεσίας**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Εκκίνηση της υπηρεσίας**
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

Η υπηρεσία digna έχει πλέον αφαιρεθεί από τις υπηρεσίες των Windows.

---

## Αναβάθμιση σε Νέα Έκδοση {: #upgrading-to-a-new-release }

### Πριν την Αναβάθμιση

**Η δημιουργία αντιγράφου ασφαλείας του Repository του digna είναι ΥΠΟΧΡΕΩΤΙΚΗ**

Πριν αναβαθμίσετε το digna, κάντε backup το repository σας (PostgreSQL) για να προστατευτείτε από απώλεια δεδομένων.
Ένα backup εξασφαλίζει ότι μπορείτε να επαναφέρετε τα δεδομένα αν η αναβάθμιση αντιμετωπίσει απρόβλεπτα προβλήματα.

### Διαδικασία Αναβάθμισης

#### Βήμα 1: Σταματήστε την υπηρεσία digna

Αν το digna τρέχει ως υπηρεσία Windows, σταματήστε το πρώτα:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Βήμα 2: Δημιουργία αντιγράφου του τρέχοντος backend

Στον κατάλογο εγκατάστασης του digna:

```bash
# Μετονομασία φακέλου που περιέχει το dignabackend
ren dignabackend dignabackend_old
```
```bash
# Μετονομασία του dashboard
ren dashboard dashboard_old
```

#### Βήμα 3: Εξαγωγή και Ανάπτυξη της Νέας Έκδοσης

1. Εξαγάγετε το νέο αρχείο ZIP εγκατάστασης του digna
2. Αντιγράψτε το νέο εκτελέσιμο `digna` και τον φάκελο `dashboard` στον κατάλογο εγκατάστασής σας


!!! warning "Σημαντικό"

    Το αρχείο `config.toml` **ποτέ** δεν περιλαμβάνεται στο ZIP εγκατάστασης. Η υπάρχουσα διαμόρφωσή σας παραμένει ασφαλής.

### Βήμα 4: Επαναφορά των Αρχείων Διαμόρφωσης

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Βήμα 5: Αναβάθμιση του Schema του Repository

Πλοηγηθείτε στον κατάλογο εγκατάστασης του digna και εκτελέστε:

```bash
digna repo upgrade
```

Αυτό ενημερώνει το schema του PostgreSQL στην τελευταία έκδοση διατηρώντας όλα τα υπάρχοντα δεδομένα.

### Βήμα 6: Επανεκκίνηση των Υπηρεσιών

Αν τρέχει ως υπηρεσία Windows:

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

1. Πρόσβαση στο digna dashboard
2. Επαληθεύστε ότι η διεπαφή φορτώνει σωστά
3. Ελέγξτε τα logs του server για τυχόν σφάλματα