---
title: Οδηγός Εγκατάστασης macOS – digna Έκδοση 2026.11 | Τεκμηρίωση digna
description: Οδηγός βήμα-προς-βήμα για την εγκατάσταση της digna Έκδοση 2026.11 σε macOS — απαιτήσεις συστήματος, ρύθμιση Homebrew και PostgreSQL, διαμόρφωση nginx ή Apache, ρύθμιση backend και dashboard, εκτέλεση digna ως υπηρεσία στο παρασκήνιο και αναβάθμιση από την Έκδοση 2026.06.
keywords: digna macos εγκατάσταση, οδηγός ανάπτυξης digna mac, ρύθμιση backend digna, εγκατάσταση dashboard digna, postgresql homebrew, nginx macos, υπηρεσία launchd digna, οδηγός αναβάθμισης digna
image: /assets/logo_square.png
---

# Οδηγός Εγκατάστασης macOS για digna Έκδοση 2026.11

**Έκδοση:** 2026.11

**Τελευταία Ενημέρωση:** 7 Νοεμβρίου 2026


---

## Πίνακας Περιεχομένων

1. [Εισαγωγή](#introduction)
2. [Απαιτήσεις Συστήματος](#system-requirements)
3. [Προεγκατάσταση](#pre-installation-setup)
4. [Ρύθμιση Διακομιστή PostgreSQL](#postgresql-server-setup)
5. [Διαμόρφωση Web Server](#web-server-configuration)
6. [Αρχική Εγκατάσταση](#initial-installation)
7. [Διαμόρφωση Backend](#backend-configuration)
8. [Διαμόρφωση Dashboard](#dashboard-configuration)
9. [Εκτέλεση digna ως Υπηρεσία στο Παρασκήνιο](#running-digna-as-a-background-service)
10. [Αναβάθμιση σε Νέα Έκδοση](#upgrading-to-a-new-release)

---

## Εισαγωγή {: #introduction }

### Σχετικά με την digna

digna είναι μια ολοκληρωμένη πλατφόρμα με τεχνητή νοημοσύνη σχεδιασμένη να βελτιστοποιεί τη διαχείριση ποιότητας δεδομένων σε διάφορα περιβάλλοντα δεδομένων όπως warehouses, lakes και lakehouses. Σχεδιασμένη για υψηλή κλίμακα και ευελιξία, η digna αντιμετωπίζει σύγχρονες προκλήσεις δεδομένων μέσω αυτοματοποίησης, παρακολούθησης σε πραγματικό χρόνο και εντοπισμού ανωμαλιών.

Η digna αποτελείται από δύο κύρια συστατικά:

- **digna**: ο πυρήνας της εφαρμογής, υπεύθυνος για την επεξεργασία δεδομένων και την εκτέλεση ελέγχων ποιότητας. Ενοποιεί το backend και τη διεπαφή γραμμής εντολών σε ένα μόνο εκτελέσιμο αρχείο, αντικαθιστώντας τα ξεχωριστά προγράμματα `dignabackend` και `dignacli` των προηγούμενων εκδόσεων.
- **dignadashboard**: Διεπαφή web που φιλοξενείται σε web server και προσφέρει έναν φιλικό τρόπο αλληλεπίδρασης με την πλατφόρμα digna και οπτικοποίησης μετρικών ποιότητας δεδομένων.

### Τι νέο φέρνει η Έκδοση 2026.11

Αυτή η έκδοση προσθέτει το digna Data Reconciliation, το digna Agentic με τον digna MCP Server και το digna Engine, το οποίο μπορεί να κάνει profiling δεδομένων μέσα στο digna και να ελέγχει την ακεραιότητα αναφορών μεταξύ διαφορετικών τεχνολογιών βάσεων δεδομένων. Δείτε τις [σημειώσεις έκδοσης](../../../changelog/Release_202611.md) για πλήρεις λεπτομέρειες.

Για μια εγκατάσταση, η έκδοση φέρνει έναν νέο μηχανισμό migrations για το repository, μια προαιρετική ενότητα `[duckdb]` στο `config.toml` για το digna Engine και ένα νέο αρχείο άδειας. Η [ενότητα αναβάθμισης](#upgrading-to-a-new-release) καλύπτει καθένα από αυτά.

### Ψάχνετε για Windows ή Linux;

Αυτός ο οδηγός καλύπτει macOS. Για άλλες πλατφόρμες, δείτε τον [Windows Installation Guide](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) ή τον [Linux Installation Guide](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Απαιτήσεις Συστήματος {: #system-requirements }

Πριν ξεκινήσετε την εγκατάσταση, βεβαιωθείτε ότι το σύστημά σας πληροί τις ακόλουθες ελάχιστες απαιτήσεις:

| Απαίτηση | Προδιαγραφή |
|---|---|
| **Λειτουργικό Σύστημα** | macOS 13 (Ventura) ή νεότερο |
| **Αρχιτεκτονική** | Apple Silicon (arm64) ή Intel (x86_64) |
| **Μνήμη (Ελάχιστη Εγκατάσταση)** | 16 GB RAM |
| **Χώρος Δίσκου** | 10 GB διαθέσιμος χώρος |
| **Βάση Δεδομένων** | PostgreSQL Server 12 ή νεότερο |
| **Web Server** | nginx, Apache httpd, ή αντίστοιχο |
| **Εργαλεία Γραμμής Εντολών** | Xcode Command Line Tools (απαραίτητα για Homebrew) |

!!! info "digna Engine"

    Για τις συνδέσεις βάσεων δεδομένων που χρησιμοποιούν το digna Engine ως τοποθεσία profiling, το profiling εκτελείται στον ίδιο τον host του digna. Προβλέψτε επιπλέον μνήμη και χώρο στον δίσκο για αυτές, δείτε την [ενότητα \[duckdb\]](#duckdb-section).

### Επιλογές Εγκατάστασης Βάσης Δεδομένων

**Εάν το PostgreSQL είναι ήδη εγκατεστημένο:**
Μπορείτε να προσθέσετε μια νέα βάση δεδομένων για την digna στο υπάρχον PostgreSQL Server.

**Εάν εγκαθιστάτε το PostgreSQL στο ίδιο μηχάνημα με την digna:**

!!! info "Συνιστώμενες Προδιαγραφές"

    - **Μνήμη**: 32 GB RAM (αντί για 16 GB)
    - **Χώρος Δίσκου**: 50 GB διαθέσιμος χώρος (αντί για 10 GB)

    Αυτές οι υψηλότερες προδιαγραφές καλύπτουν τόσο την digna όσο και τη βάση PostgreSQL που τρέχει ταυτόχρονα.

### Έλεγχος Αρχιτεκτονικής

Ποια διαδρομή χρησιμοποιείται σε αυτόν τον οδηγό διαφέρει ανάμεσα σε Apple Silicon και Intel Macs. Για να ελέγξετε ποια έχετε, ανοίξτε το **Terminal** και εκτελέστε:

```bash
uname -m
```

- `arm64` — Apple Silicon. Το Homebrew εγκαθίσταται στο `/opt/homebrew`.
- `x86_64` — Intel. Το Homebrew εγκαθίσταται στο `/usr/local`.

!!! tip "Συμβουλή"

    Αντί να κωδικοποιείτε μια από τις δύο διαδρομές, αυτός ο οδηγός χρησιμοποιεί `$(brew --prefix)`, που επεκτείνεται στη σωστή τοποθεσία και για τις δύο αρχιτεκτονικές. Μπορείτε να αντιγράψετε τις εντολές αυτούσιες.

---

## Προεγκατάσταση {: #pre-installation-setup }

Πριν εγκαταστήσετε την digna, βεβαιωθείτε ότι υπάρχουν τρεις βασικές προϋποθέσεις:

1. **Homebrew** – ο διαχειριστής πακέτων που χρησιμοποιείται για την εγκατάσταση των παρακάτω στοιχείων
2. **PostgreSQL Server** – για την αποθήκευση υπολογισμένων μετρικών και δεδομένων απόδοσης
3. **Web Server** – για τη φιλοξενία του Dashboard της digna

Εάν αυτά τα συστατικά δεν έχουν εγκατασταθεί ήδη, ακολουθήστε τις παρακάτω ενότητες για να τα εγκαταστήσετε και να τα ρυθμίσετε.

### Εγκατάσταση Homebrew

Το Homebrew είναι ο τυπικός διαχειριστής πακέτων για macOS και χρησιμοποιείται σε όλο αυτόν τον οδηγό για την εγκατάσταση του PostgreSQL και του nginx.

#### Βήμα 1: Έλεγχος Εγκατάστασης Homebrew

Ανοίξτε το **Terminal** (πατήστε `Cmd + Space`, πληκτρολογήστε `Terminal`, πατήστε Enter) και εκτελέστε:

```bash
brew --version
```

Εάν εμφανιστεί αριθμός έκδοσης, προχωρήστε στην ενότητα [Ρύθμιση Διακομιστή PostgreSQL](#postgresql-server-setup).

#### Βήμα 2: Εγκατάσταση Homebrew

Εάν η εντολή δεν βρέθηκε, εγκαταστήστε το Homebrew ακολουθώντας τις οδηγίες στον [επίσημο ιστότοπο Homebrew](https://brew.sh). Ο εγκαταστάτης επίσης εγκαθιστά τα Xcode Command Line Tools εάν δεν υπάρχουν ήδη.

#### Βήμα 3: Προσθήκη Homebrew στο PATH

Σε Apple Silicon, ο εγκαταστάτης εκτυπώνει δύο εντολές για να προσθέσετε το Homebrew στο περιβάλλον του shell σας. Εκτελέστε τις όπως υποδεικνύεται και στη συνέχεια επιβεβαιώστε:

```bash
brew --prefix
```

Αυτό θα πρέπει να εκτυπώσει `/opt/homebrew` σε Apple Silicon ή `/usr/local` σε Intel.

---

## Ρύθμιση Διακομιστή PostgreSQL {: #postgresql-server-setup }

### Εάν Έχετε Ήδη PostgreSQL

Εάν το PostgreSQL είναι ήδη εγκαταστημένο και εκτελείται τοπικά ή χρησιμοποιείτε έναν managed απομακρυσμένο PostgreSQL server, μπορείτε να παραλείψετε στην [επόμενη ενότητα](#web-server-configuration).

### Επιλογές Εγκατάστασης

Το macOS προσφέρει δύο απλούς τρόπους εγκατάστασης του PostgreSQL. Επιλέξτε **ένα**:

- [Homebrew](#postgresql-homebrew) — εγκατάσταση μέσω γραμμής εντολών, συνιστάται για server deployments
- [Postgres.app](#postgresql-app) — γραφική εγκατάσταση, βολική για τοπική αξιολόγηση

### Εγκατάσταση PostgreSQL με Homebrew {: #postgresql-homebrew }

#### Βήμα 1: Εγκατάσταση του Formula PostgreSQL

```bash
brew install postgresql@16
```

#### Βήμα 2: Προσθήκη PostgreSQL στο PATH

Τα versioned PostgreSQL formulas είναι *keg-only*, που σημαίνει ότι το Homebrew δεν συνδέει αυτόματα τις εντολές τους στο PATH σας. Προσθέστε τις χειροκίνητα:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Σημείωση"

    Αυτό υποθέτει το προεπιλεγμένο shell `zsh` που χρησιμοποιεί το macOS. Εάν χρησιμοποιείτε `bash`, προσθέστε την ίδια γραμμή στο `~/.bash_profile`.

#### Βήμα 3: Εκκίνηση της Υπηρεσίας PostgreSQL

```bash
brew services start postgresql@16
```

Αυτό ξεκινά το PostgreSQL άμεσα και το ρυθμίζει να ξεκινά αυτόματα όταν συνδεθείτε.

#### Βήμα 4: Επαλήθευση Εγκατάστασης

```bash
psql --version
```

Θα πρέπει να δείτε την έκδοση του PostgreSQL εάν η εγκατάσταση ήταν επιτυχής.

#### Βήμα 5: Σύνδεση στον Διακομιστή

```bash
psql postgres
```

!!! warning "Σημαντικό — στο macOS Διαφέρει Από τα Windows"

    Ο installer των Windows σας ζητά να δημιουργήσετε έναν superuser `postgres` και κωδικό. Το Homebrew δεν το κάνει. Αντίθετα δημιουργεί έναν superuser με το όνομα του **λογαριασμού macOS** σας, χωρίς κωδικό, προσβάσιμο μόνο από το τοπικό μηχάνημα.

    Αυτό σημαίνει ότι δεν υπάρχει ρόλος `postgres` σε μια καθαρή εγκατάσταση μέσω Homebrew. Χρησιμοποιήστε το όνομα του δικού σας λογαριασμού όταν χρειαστεί superuser και δημιουργήστε έναν ρητό χρήστη για την digna όπως περιγράφεται στην [Αρχική Εγκατάσταση](#initial-installation).

#### Βήμα 6: Επιβεβαίωση Θύρας

Η προεπιλεγμένη θύρα PostgreSQL είναι `5432`. Για να επιβεβαιώσετε τη θύρα στην οποία ακούει ο server:

```bash
psql postgres -c "SHOW port;"
```

Σημειώστε την τιμή — θα τη χρειαστείτε κατά τη ρύθμιση του backend της digna.

### Εγκατάσταση PostgreSQL με Postgres.app {: #postgresql-app }

Εάν προτιμάτε γραφική εγκατάσταση:

1. Κατεβάστε το [Postgres.app](https://postgresapp.com) και σύρετέ το στο φάκελο **Applications**
2. Ανοίξτε την εφαρμογή και κάντε κλικ στο **Initialize** για να δημιουργήσετε νέο server
3. Ακολουθήστε τις οδηγίες της εφαρμογής για να προσθέσετε τα εργαλεία γραμμής εντολών στο PATH σας
4. Επαληθεύστε την εγκατάσταση:

```bash
psql --version
```

Το Postgres.app επίσης δημιουργεί έναν superuser με το όνομα του λογαριασμού macOS σας.

---

## Διαμόρφωση Web Server {: #web-server-configuration }

Η digna χρειάζεται web server για να φιλοξενήσει το dashboard. Επιλέξτε έναν από τους παρακάτω:

- [nginx](#nginx-setup) — εγκατάσταση μέσω Homebrew, συνιστάται
- [Apache httpd](#apache-setup) — περιλαμβάνεται στο macOS

Χρειάζεται να εγκαταστήσετε και να διαμορφώσετε **έναν** από αυτούς τους servers.

Και οι δύο ενότητες ρυθμίζουν δύο στοιχεία από τα οποία εξαρτάται το dashboard:

- **Single-page-application fallback**, ώστε όταν κάνετε ανανέωση σε μια URL του dashboard να μην επιστρέφεται 404
- **Τύπος MIME για `.md`**, ώστε τα αρχεία Markdown να σερβίρονται σωστά

### Ρύθμιση nginx {: #nginx-setup }

#### Επισκόπηση

Το nginx είναι ελαφρύς, υψηλής απόδοσης web server, κατάλληλος για τη φιλοξενία του στατικού dashboard της digna.

#### Εγκατάσταση

```bash
brew install nginx
```

#### Εκκίνηση nginx

```bash
brew services start nginx
```

#### Επαλήθευση Εγκατάστασης

1. Ανοίξτε τον browser σας
2. Πλοηγηθείτε στο `http://localhost:8080`
3. Πρέπει να δείτε τη σελίδα καλωσορίσματος του nginx

!!! note "Σημείωση — Η Προεπιλεγμένη Θύρα Είναι 8080, Όχι 80"

    Το Homebrew ρυθμίζει το nginx να ακούει στην θύρα `8080` ώστε να μπορεί να τρέξει χωρίς δικαιώματα διαχειριστή. Στο macOS, η σύνδεση σε θύρα `80` ή οποιαδήποτε άλλη θύρα κάτω από 1024 απαιτεί δικαιώματα root.

    Για να σερβίρετε το dashboard στην θύρα 80, αλλάξτε `listen 8080;` σε `listen 80;` στη διαμόρφωση πιο κάτω και ξεκινήστε το nginx με `sudo brew services start nginx` αντίστοιχα.

#### Διαμόρφωση Site για το Dashboard

Η διαμόρφωση nginx του Homebrew περιλαμβάνει κάθε αρχείο στον φάκελο `servers`. Δημιουργήστε ένα αφιερωμένο αρχείο διαμόρφωσης για την digna εκεί:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Επικολλήστε το παρακάτω, αντικαθιστώντας `/path/to/digna/dashboard` με την πραγματική διαδρομή του αποσυμπιεσμένου φακέλου `dashboard`:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Σημαντικό"

    Χωρίς τη δέσμη `try_files`, η ανανέωση οποιασδήποτε σελίδας του dashboard εκτός της ρίζας επιστρέφει 404. Αυτό είναι το αντίστοιχο του URL Rewrite module που απαιτείται από το IIS στα Windows.

#### Εφαρμογή της Διαμόρφωσης

Ελέγξτε τη σύνταξη της διαμόρφωσης για σφάλματα, και μετά κάντε reload το nginx:

```bash
nginx -t
brew services restart nginx
```

---

### Ρύθμιση Apache httpd {: #apache-setup }

#### Επισκόπηση

Το macOS περιλαμβάνει τον Apache httpd, οπότε δεν απαιτείται εγκατάσταση. Είναι απενεργοποιημένος από προεπιλογή.

#### Εκκίνηση Apache

```bash
sudo apachectl start
```

#### Επαλήθευση Εγκατάστασης

1. Ανοίξτε τον browser σας
2. Πλοηγηθείτε στο `http://localhost`
3. Πρέπει να δείτε το μήνυμα "It works!"

#### Απαιτούμενο: Ενεργοποίηση mod_rewrite

Το dashboard απαιτεί URL rewriting. Ανοίξτε τη διαμόρφωση του Apache:

```bash
sudo nano /etc/apache2/httpd.conf
```

Βρείτε την ακόλουθη γραμμή και αφαιρέστε το αρχικό `#` για να την αποσχολιάσετε:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Απαιτούμενο: Επιτρέψτε overrides με .htaccess

Στο ίδιο αρχείο, εντοπίστε το μπλοκ `<Directory "/Library/WebServer/Documents">` και αλλάξτε:

```apache
AllowOverride None
```

σε:

```apache
AllowOverride All
```

#### Απαιτούμενο: Τύπος MIME για Αρχεία Markdown

Ακόμη στο `httpd.conf`, προσθέστε την ακόλουθη γραμμή ώστε τα αρχεία Markdown να σερβίρονται σωστά:

```apache
AddType text/markdown .md
```

!!! warning "Σημαντικό"

    Χωρίς αυτή τη ρύθμιση, τα αρχεία `.md` ενδέχεται να μην σερβίρονται σωστά.

#### Εφαρμογή της Διαμόρφωσης

Ελέγξτε τη σύνταξη της διαμόρφωσης, και μετά κάντε επανεκκίνηση του Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Αρχική Εγκατάσταση {: #initial-installation }

### Βήμα 1: Ρύθμιση του Repository της digna

Το repository της digna αποθηκεύει όλες τις μετρικές που υπολογίζει η digna. Λειτουργεί ως κεντρική βάση δεδομένων για αναλυτικά και δεδομένα απόδοσης.

#### Δημιουργία Schema και Χρήστη για το Repository

Ανοίξτε τον PostgreSQL client σας (psql, pgAdmin ή παρόμοιο) και εκτελέστε τις ακόλουθες εντολές SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Αντικαταστήστε τις ακόλουθες θέσεις κράτησης:**

- `<digna_repo_schema>` — Το επιθυμητό όνομα schema (π.χ., `dignarepo`)
- `<digna_repo_user>` — Το επιθυμητό όνομα χρήστη (π.χ., `digna_user`)
- `<digna_repo_password>` — Ένας ασφαλής κωδικός για αυτόν τον χρήστη

**Παράδειγμα:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Για να τρέξετε αυτά από το Terminal σε ένα βήμα:

```bash
psql postgres
```

Έπειτα επικολλήστε τις εντολές στο prompt `postgres=#` και πληκτρολογήστε `\q` για έξοδο.

!!! tip "Βέλτιστη Πρακτική"

    Χρησιμοποιήστε ισχυρούς, σύνθετους κωδικούς για τους χρήστες της βάσης δεδομένων. Αποφύγετε ευκόλως μαντευόμενα διαπιστευτήρια.

---

### Βήμα 2: Αποσυμπίεση του Πακέτου Εγκατάστασης digna

1. Εντοπίστε το αρχείο ZIP εγκατάστασης digna που σας παρέχεται
2. Αποσυμπιέστε το στην επιθυμητή τοποθεσία εγκατάστασης — για παράδειγμα `/opt/digna` ή `~/digna`
3. Μετά την αποσυμπίεση, πρέπει να δείτε τα ακόλουθα στοιχεία:
   - `dashboard/` — Διεπαφή web dashboard
   - `digna` — Κύριο εκτελέσιμο (backend + CLI σε ένα)

!!! info "Τα αρχεία διαμόρφωσης και άδειας δεν περιλαμβάνονται στο πακέτο"

    Ούτε το `config.toml` ούτε το `dashboard/dashboard_config.toml` παρέχονται με την εγκατάσταση — τα δημιουργείτε και τα δύο εσείς, στις ενότητες [Διαμόρφωση Backend](#backend-configuration) και [Διαμόρφωση Dashboard](#dashboard-configuration). Ούτε το `license.toml` παρέχεται με το πακέτο· η digna το παρέχει ξεχωριστά, όπως περιγράφεται στο Βήμα 3.

Για να αποσυμπιέσετε από το Terminal:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
```

#### Κάντε το Εκτελέσιμο Runnable

Ανάλογα με τον τρόπο μεταφοράς του αρχείου, το bit εκτέλεσης ενδέχεται να μην διατηρηθεί. Ορίστε το ρητά:

```bash
cd /opt/digna
chmod +x digna
```

#### Εάν το macOS Αποκλείει την Εφαρμογή

Αρχεία που έχουν ληφθεί μέσω browser ή mail client έχουν σημαδευτεί με καραντίνα. Εάν το macOS αναφέρει ότι η εφαρμογή *"cannot be opened because the developer cannot be verified"*, αφαιρέστε την ιδιότητα από τον κατάλογο εγκατάστασης:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Εναλλακτικά, ανοίξτε τις **System Settings → Απόρρητο & Ασφάλεια**, εντοπίστε το αποκλεισμένο στοιχείο στο κάτω μέρος της σελίδας και κάντε κλικ στο **Open Anyway**.

!!! note "Σημείωση"

    Αυτό το βήμα είναι απαραίτητο μόνο εάν το macOS πραγματικά μπλοκάρει το εκτελέσιμο. Πακέτα που μεταφέρονται μέσω SSH ή από εσωτερικούς file shares συνήθως δεν είναι σε καραντίνα.

### Βήμα 3: Εγκατάσταση του Αρχείου Άδειας

!!! warning "Σημαντικό"

    Το αρχείο άδειας **δεν** περιλαμβάνεται στο πακέτο εγκατάστασης και θα σας παρασχεθεί ξεχωριστά από την digna.

1. Εντοπίστε το αρχείο `license.toml` που σας παρέχεται
2. Αντιγράψτε το στο root directory εγκατάστασης της digna (όπου βρίσκονται το `config.toml` και το εκτελέσιμο `digna`)

**Γιατί έχει σημασία:**
Το αρχείο άδειας περιέχει πληροφορίες πελάτη, ημερομηνία λήξης άδειας και ψηφιακή υπογραφή. **Μην τροποποιείτε αυτό το αρχείο** — οποιαδήποτε αλλαγή θα το ακυρώσει.

**Δομή καταλόγου μετά τη ρύθμιση:**

```
/opt/digna/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
├── bin/                (service management scripts)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Διαμόρφωση Backend {: #backend-configuration }

### Βήμα 1: Δημιουργία και Επεξεργασία του Αρχείου Ρυθμίσεων

Το αρχείο `config_template.toml` περιλαμβάνεται στον κατάλογο εγκατάστασης της digna. Απλά μετονομάστε το σε `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Τοποθεσία:** `/opt/digna/config.toml`

Ανοίξτε το `config.toml` σε έναν επεξεργαστή κειμένου και ρυθμίστε κάθε ενότητα όπως παρακάτω.

#### Ενότητα [app]

Αυτή η ενότητα διαμορφώνει την κοινή χρήση πόρων μεταξύ διαφορετικών origins (CORS) ανάμεσα στο dashboard και το backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Παράμετρος | Τιμή | Σημειώσεις |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | URL του dashboard | Τα URL από τα οποία σερβίρεται το dashboard. Αιτήματα του browser από οποιοδήποτε άλλο origin απορρίπτονται |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Απαραίτητο, ώστε ο browser να στέλνει το cookie συνεδρίας με κάθε αίτημα |

!!! note "Σημείωση"

    Εάν σερβίρετε το dashboard από το nginx του Homebrew στην προεπιλεγμένη θύρα, το origin που πρέπει να επιτρέψετε είναι `http://localhost:8080`.

!!! info "Η ενότητα [app] είναι προαιρετική"

    Από την Έκδοση 2026.11, και τα δύο κλειδιά, καθώς και ολόκληρη η ενότητα `[app]`, μπορούν να παραλειφθούν. Αυτή είναι η σωστή ρύθμιση όταν ένας reverse proxy σερβίρει το dashboard και το backend κάτω από ένα origin: ο browser τότε δεν κάνει αιτήματα μεταξύ διαφορετικών origins, και από προεπιλογή δεν επιτρέπεται κανένα.

#### Ενότητα [repo]

Αυτή η ενότητα ρυθμίζει τη σύνδεση με τη βάση PostgreSQL:

```toml
[repo]
DIGNA_REPO_HOST = "localhost"
DIGNA_REPO_PORT = 5432
DIGNA_REPO_DB = "postgres"
DIGNA_REPO_SCHEMA = "dignarepo"
DIGNA_REPO_USER = "digna_user"
DIGNA_REPO_PASSWORD = "YourSecurePassword123!"
DIGNA_REPO_SSLMODE = "prefer"
DIGNA_REPO_NUM_CONNS = 16
```

| Παράμετρος | Τιμή | Σημειώσεις |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` ή IP | Hostname/IP του PostgreSQL server |
| `DIGNA_REPO_PORT` | `5432` (προεπιλογή) | Θύρα PostgreSQL |
| `DIGNA_REPO_DB` | `postgres` | Όνομα βάσης |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Το schema που δημιουργήθηκε νωρίτερα |
| `DIGNA_REPO_USER` | `digna_user` | Ο χρήστης που δημιουργήθηκε στη ρύθμιση του PostgreSQL |
| `DIGNA_REPO_PASSWORD` | Ο κωδικός σας | Κωδικός που ορίσατε κατά τη δημιουργία του schema |
| `DIGNA_REPO_SSLMODE` | `prefer` (προεπιλογή) | Προαιρετικό. Λειτουργία SSL του PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` ή `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (προεπιλογή) | Προαιρετικό. Αριθμός συνδέσεων που διατηρεί ανοιχτές το digna προς το repository |

#### Ενότητα [base]

Αυτή η ενότητα περιέχει ρυθμίσεις ασφάλειας, cookies και επιθεωρήσεων:

```toml
[base]
DIGNA_FERNET_KEY = "DU4a0yJ-OqvbKCL4hNQn_CsknH-V1vWmHZqBUl-AY44="
DIGNA_COOKIE_DOMAIN = "localhost"
DIGNA_COOKIE_SECURE = false
DIGNA_COOKIE_HTTPONLY = true
DIGNA_TOKEN_EXPIRES_IN = 86400
DIGNA_MAX_WORKERS = 4
DIGNA_FRONTEND_BASEURL = "http://localhost/"
DIGNA_SOURCE_QUERY_TIMEOUT_SEC = 3600
DIGNA_SOURCE_LOGIN_TIMEOUT_SEC = 30
```

| Παράμετρος | Τιμή | Σημειώσεις |
|---|---|---|
| `DIGNA_FERNET_KEY` | Η τιμή που φαίνεται παραπάνω | Κλειδί της κρυπτογράφησης που χρησιμοποιούσαν οι προηγούμενες εκδόσεις. Πρέπει να υπάρχει· διατηρήστε την τιμή που φαίνεται |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Ο host μέσω του οποίου προσεγγίζεται το dashboard. Το `""` δεν ορίζει domain, κάτι που είναι σωστό πίσω από proxy που σερβίρει το dashboard και το backend κάτω από ένα origin |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Πρέπει να είναι `true` όποτε το digna σερβίρεται μέσω HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Κρατά το cookie συνεδρίας εκτός πρόσβασης από scripts |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 ώρες) | Χρόνος λήξης συνεδρίας σε δευτερόλεπτα |
| `DIGNA_MAX_WORKERS` | Αριθμός CPU cores - 1 | Αριθμός επιθεωρήσεων που μπορούν να εκτελούνται ταυτόχρονα |
| `DIGNA_FRONTEND_BASEURL` | URL του dashboard | Υποχρεωτικό. Χρησιμοποιείται για τους συνδέσμους στα μηνύματα ειδοποιήσεων, οπότε πρέπει να είναι URL που μπορούν να ανοίξουν οι παραλήπτες |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (προεπιλογή) | Προαιρετικό. Δευτερόλεπτα που μπορεί να εκτελείται ένα μεμονωμένο ερώτημα σε βάση δεδομένων πηγής πριν διακοπεί· το `0` απενεργοποιεί το χρονικό όριο |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (προεπιλογή) | Προαιρετικό. Δευτερόλεπτα αναμονής για σύνδεση με βάση δεδομένων πηγής· το `0` περιμένει επ' αόριστον |

!!! tip "Συμβουλή"

    Για να βρείτε τον αριθμό πυρήνων CPU στο Mac σας, εκτελέστε `sysctl -n hw.ncpu`.

#### Ενότητα [encryption]

Αυτή η ενότητα περιέχει το κλειδί που χρησιμοποιείται για την κρυπτογράφηση ευαίσθητων τιμών που αποθηκεύονται στο repository. Είναι **υποχρεωτική** — το `config check` αναφέρει την ενότητα `[encryption]` ως FAILED αν λείπει το κλειδί.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Παράμετρος | Τιμή | Σημειώσεις |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Κλειδί κωδικοποιημένο σε Base64 | Κρυπτογραφεί ευαίσθητες τιμές που αποθηκεύονται στο repository digna |

!!! warning "Προστατέψτε το config.toml"

    Αυτό το κλειδί είναι σταθερή τιμή, ίδια σε όλες τις εγκαταστάσεις digna, και είναι αυτό που αποκρυπτογραφεί τις ευαίσθητες τιμές του repository σας. Περιορίστε το `config.toml` στον λογαριασμό που εκτελεί το digna, κρατήστε το αρχείο εκτός συστήματος ελέγχου εκδόσεων και κοινόχρηστων δίσκων και εξαιρέστε το από κάθε αντίγραφο ασφαλείας που φυλάσσεται λιγότερο ασφαλώς από το ίδιο το repository.

#### Ενότητα [logging]

Αυτή η ενότητα ρυθμίζει τη συμπεριφορά καταγραφής:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Παράμετρος | Τιμή | Σημειώσεις |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` ή `DEBUG` | `INFO` για παραγωγή, `DEBUG` για αντιμετώπιση προβλημάτων. Γίνονται επίσης δεκτά τα `TRACE`, `WARN` και `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (προεπιλογή) | Προαιρετικό. Κατάλογος για τα εναλλασσόμενα αρχεία log, σχετικά με τον κατάλογο εργασίας |
| `DIGNA_LOGGING_MAX_FILES` | `30` (προεπιλογή) | Προαιρετικό. Αριθμός εναλλασσόμενων αρχείων log που διατηρούνται |

#### Ενότητα [duckdb] (Προαιρετική) {: #duckdb-section }

Νέο στην Έκδοση 2026.11. Αυτή η ενότητα ορίζει τους πόρους του **digna Engine**, το οποίο κάνει profiling δεδομένων μέσα στο digna για συνδέσεις βάσεων δεδομένων με τοποθεσία profiling **digna Engine**, και εκτελεί ελέγχους ακεραιότητας αναφορών μεταξύ πηγών δεδομένων σε διαφορετικές συνδέσεις βάσεων δεδομένων. Δείτε [Τοποθεσία Profiling](../../../platform/profiling/profiling_location.md).

Η ενότητα είναι προαιρετική. Χωρίς αυτήν ισχύουν οι παρακάτω προεπιλογές.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Παράμετρος | Τιμή | Σημειώσεις |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (προεπιλογή) | Μνήμη, σε MB, που μπορεί να χρησιμοποιήσει μία εκτέλεση του digna Engine. Έως `DIGNA_MAX_WORKERS` εκτελέσεις μπορούν να είναι ενεργές ταυτόχρονα |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Προεπιλογή: ο προσωρινός κατάλογος του συστήματος (`$TMPDIR` του λογαριασμού που εκτελεί το digna) | Κατάλογος για προσωρινά αρχεία όταν τα δεδομένα δεν χωρούν στη μνήμη |

!!! tip "Διαστασιολόγηση του digna Engine"

    Προβλέψτε έως `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` μνήμης στον host του digna, επιπλέον όσης χρησιμοποιεί το ίδιο το digna, και αρκετό ελεύθερο χώρο στον δίσκο του προσωρινού καταλόγου ώστε να χωρά η μεγαλύτερη επιθεωρούμενη ημερομηνία των πηγών δεδομένων που χρησιμοποιούν το digna Engine. Ορίστε το `DIGNA_DUCKDB_TEMP_DIRECTORY` σε δίσκο με αυτόν τον χώρο, εγγράψιμο από τον λογαριασμό που εκτελεί το digna:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    Χρειάζεστε αυτή την ενότητα μόνο αν τουλάχιστον μία σύνδεση βάσης δεδομένων χρησιμοποιεί το digna Engine ή αν ένας έλεγχος ακεραιότητας αναφορών συγκρίνει πηγές δεδομένων σε διαφορετικές συνδέσεις.

---

### Βήμα 2: Επικυρώστε τη διαμόρφωση

Πριν αρχικοποιήσετε το repository, ελέγξτε ότι το `config.toml` είναι πλήρες και σωστά δομημένο. Στον κατάλογο εγκατάστασης digna εκτελέστε:

```bash
./digna config check
```

Κάθε ενότητα επικυρώνεται ξεχωριστά, ώστε ένα μεμονωμένο σφάλμα να μην κρύβει την κατάσταση των υπολοίπων:

```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: OK
 - OIDC config(s): OK
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Διορθώστε ό,τι αναφέρεται ως FAILED και εκτελέστε ξανά την εντολή πριν συνεχίσετε. Ένα WARNING κάτω από το **Unknown keys** παραθέτει κλειδιά του `config.toml` που το digna δεν διαβάζει· δεν έχουν καμία επίδραση, οπότε αφαιρέστε τα ή διορθώστε τη γραφή τους. Ο πλήρης κατάλογος επιλογών βρίσκεται στην [αναφορά CLI](../../../cli/Command_Line_Interface_202611.md).

### Βήμα 3: Αρχικοποίηση του Repository

1. Ανοίξτε το **Terminal**
2. Πλοηγηθείτε στον κατάλογο εγκατάστασης της digna (όπου βρίσκονται το `config.toml` και το εκτελέσιμο `digna`)
3. Εκτελέστε το τεστ σύνδεσης:

```bash
cd /opt/digna
./digna repo check
```

Σε ένα νέο schema, η εντολή συνδέεται και στη συνέχεια αναφέρει ότι δεν έχει εγκατασταθεί ακόμη repository:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Σε αυτό το σημείο αυτό είναι το αναμενόμενο αποτέλεσμα: επιβεβαιώνει ότι το digna φτάνει στο PostgreSQL και στο schema. Ένα σφάλμα σύνδεσης ή ελέγχου ταυτότητας, αντίθετα, παραπέμπει στην ενότητα `[repo]` ή στη ρύθμιση του PostgreSQL.

!!! note "Σημείωση"

    Στο macOS, οι εντολές στον τρέχοντα κατάλογο δεν είναι στο PATH σας, οπότε το εκτελέσιμο καλείται ως `./digna` αντί για `digna`. Για να χρησιμοποιείτε τη συντομότερη μορφή παντού, προσθέστε τον κατάλογο εγκατάστασης στο PATH σας:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Βήμα 4: Εγκατάσταση του Schema του Repository

Στον ίδιο κατάλογο, τρέξτε:

```bash
./digna repo upgrade
```

Αυτή η εντολή εγκαθιστά τους απαραίτητους πίνακες στο schema του repository και ολοκληρώνεται με:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "Το repo upgrade εγκαθιστά και αναβαθμίζει"

    Από την Έκδοση 2026.11, το `repo upgrade` εγκαθιστά ένα νέο repository και αναβαθμίζει ένα υπάρχον. Το `repo install` εξακολουθεί να λειτουργεί ως άλλο όνομα για την ίδια εντολή.

### Βήμα 5: Δημιουργία Διαχειριστή (Admin User)

Ο χρήστης διαχειριστή δημιουργείται απευθείας στο schema του repository, οπότε ο server δεν χρειάζεται ακόμη να εκτελείται. Στον κατάλογο εγκατάστασης της digna, εκτελέστε:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Παράδειγμα:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Αυτό δημιουργεί έναν χρήστη με τη διεύθυνση ηλεκτρονικού ταχυδρομείου `admin@example.com` και πλήρη δικαιώματα διαχειριστή.

!!! tip "Συμβουλή"

    Βάλτε τον κωδικό μέσα σε απλά εισαγωγικά. Το `zsh` αντιμετωπίζει ειδικά χαρακτήρες όπως `!`, `$` και `*`, και ένας απροστάτευτος κωδικός που τα περιέχει δεν θα περάσει σωστά.

!!! tip "Βέλτιστη Πρακτική"

    Χρησιμοποιήστε έναν ισχυρό κωδικό με ανάμειξη κεφαλαίων, πεζών, αριθμών και ειδικών χαρακτήρων.

---

### Βήμα 6: Εκκίνηση του διακομιστή digna

Στον κατάλογο εγκατάστασης της digna, ξεκινήστε τον server με:

```bash
./digna serve --address <host> --port <port>
```

**Παράμετροι:**
- `--address` — Hostname/IP του server (προεπιλογή `127.0.0.1`)
- `--port` — Θύρα του server (προεπιλογή `8000`)

Όταν ο server είναι σε λειτουργία, εμφανίζει τη διεύθυνση στην οποία ακούει:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Συμβουλή"

    Την πρώτη φορά που θα ξεκινήσετε τον server, το macOS μπορεί να ζητήσει αν θέλετε η εφαρμογή να δέχεται εισερχόμενες δικτυακές συνδέσεις. Κάντε κλικ στο **Allow**, διαφορετικά το dashboard δεν θα μπορεί να συνδεθεί με το backend.

!!! note "Ο διακομιστής δεσμεύει το τερματικό"

    Το `serve` εκτελείται στο προσκήνιο και συνεχίζει μέχρι να το σταματήσετε με ++ctrl+c++. Αφήστε το να εκτελείται όσο ολοκληρώνετε την εγκατάσταση· για αυτόματη εκκίνηση κατά την εκκίνηση του συστήματος, δείτε [Εκτέλεση του digna ως υπηρεσίας παρασκηνίου](#running-digna-as-a-background-service).

## Διαμόρφωση Dashboard {: #dashboard-configuration }

### Βήμα 1: Ανάπτυξη του Dashboard στον Web Server

Το digna dashboard διαβάζει τη δική του διαμόρφωση από το `dashboard/dashboard_config.toml`. Το αρχείο αυτό δεν παρέχεται με την εγκατάσταση — το δημιουργείτε στον κατάλογο `dashboard/`, δίπλα στα αρχεία του dashboard.

Το περιεχόμενό του περιγράφεται στην ενότητα [Ενιαία Σύνδεση (SSO)](../../../sso/overview.md), όπου και χρειάζεται το αρχείο: περιέχει τις επιλογές σύνδεσης που προσφέρει το dashboard και, για αναπτύξεις πολλαπλών instances, τη σύνδεση με το backend.

Επιλέξτε τον web server σας και ακολουθήστε τα αντίστοιχα βήματα ανάπτυξης.

#### Ανάπτυξη σε nginx

Εάν ακολουθήσατε την ενότητα [nginx Setup](#nginx-setup), το server block ήδη δείχνει στον φάκελο `dashboard` σας και δεν απαιτείται αντιγραφή.

1. **Επιβεβαιώστε τη διαδρομή**
   - Ανοίξτε `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Ελέγξτε ότι το `root` δείχνει στον αποσυμπιεσμένο φάκελο `dashboard`

2. **Βεβαιωθείτε ότι ο φάκελος είναι αναγνώσιμος**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Reload nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Δοκιμή Εγκατάστασης**
   - Ανοίξτε τον browser σας
   - Πλοηγηθείτε στο `http://localhost:8080` (ή στο διαμορφωμένο URL)
   - Πρέπει να δείτε τη σελίδα σύνδεσης του dashboard της digna

#### Ανάπτυξη σε Apache httpd

1. **Αντιγράψτε το Dashboard στο Document Root**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Προσθήκη Κανόνων Rewrite**

   Δημιουργήστε ένα αρχείο `.htaccess` μέσα στο αναπτυγμένο φάκελο ώστε οι διαδρομές του dashboard να επιβιώνουν κατά την ανανέωση:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Επικολλήστε το παρακάτω:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **Επανεκκίνηση Apache**
   ```bash
   sudo apachectl restart
   ```

4. **Πρόσβαση στο Dashboard**
   - Ανοίξτε τον browser σας
   - Πλοηγηθείτε στο `http://localhost/digna`
   - Πρέπει να δείτε τη σελίδα σύνδεσης του dashboard της digna

---

## Εκτέλεση digna ως Υπηρεσία στο Παρασκήνιο {: #running-digna-as-a-background-service }

### Γιατί να τρέχετε την digna ως Υπηρεσία;

Η εκτέλεση του backend της digna ως υπηρεσία στο παρασκήνιο εξασφαλίζει ότι:

- Ξεκινά αυτόματα όταν το μηχάνημα εκκινεί
- Τρέχει στο παρασκήνιο χωρίς ανοιχτό παράθυρο Terminal
- Επανεκκινείται αυτόματα αν καταρρεύσει
- Μπορεί να διαχειρίζεται μέσω του `launchctl`, του διαχειριστή υπηρεσιών του macOS

### Αρχεία Διαχείρισης Υπηρεσίας

Όλα τα απαραίτητα αρχεία βρίσκονται στον κατάλογο εγκατάστασης της digna κάτω από: `bin/`

Τα ακόλουθα shell scripts είναι διαθέσιμα:

- `install_service.sh` — Εγγράφει την digna στο launchd
- `uninstall_service.sh` — Καταργεί την εγγραφή της υπηρεσίας
- `start_service.sh` — Ξεκινά την εγγεγραμμένη υπηρεσία
- `stop_service.sh` — Σταματά την τρέχουσα υπηρεσία

!!! warning "Απαιτείται Διαχειριστής"

    Όλα τα scripts πρέπει να εκτελεστούν με `sudo`, επειδή η εγγραφή μιας υπηρεσίας που ξεκινά στην εκκίνηση γράφει στο `/Library/LaunchDaemons`.

### Κάνοντας τα Scripts Εκτελέσιμα

Η αποσυμπίεση μπορεί να μην διατηρήσει το bit εκτέλεσης. Πριν την πρώτη χρήση:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Εγκατάσταση της Υπηρεσίας

1. **Ανοίξτε Terminal**

2. **Πλοηγηθείτε στον φάκελο bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Τρέξτε το script εγκατάστασης**
   ```bash
   sudo ./install_service.sh
   ```

Η digna τώρα έχει εγγραφεί στο launchd με **αυτόματη εκκίνηση** ενεργοποιημένη. Η υπηρεσία δεν ξεκινά άμεσα — δείτε την επόμενη ενότητα για να την ξεκινήσετε.

### Εκκίνηση και Σταμάτημα της Υπηρεσίας

#### Για να Ξεκινήσετε την Υπηρεσία

1. Ανοίξτε Terminal
2. Πλοηγηθείτε στο `/opt/digna/bin`
3. Τρέξτε:
   ```bash
   sudo ./start_service.sh
   ```

#### Για να Σταματήσετε την Υπηρεσία

1. Ανοίξτε Terminal
2. Πλοηγηθείτε στο `/opt/digna/bin`
3. Τρέξτε:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Συμβουλή"

    Πάντα σταματήστε την υπηρεσία πριν ενημερώσετε αρχεία της εφαρμογής.

### Επαλήθευση της Υπηρεσίας

Για να επιβεβαιώσετε ότι η υπηρεσία έχει εγγραφεί και τρέχει:

```bash
sudo launchctl list | grep digna
```

Μια γραμμή που ξεκινά με process ID δείχνει ότι η υπηρεσία τρέχει. Ένα `-` στην πρώτη στήλη σημαίνει ότι είναι εγγεγραμμένη αλλά σταματημένη.

### Μετακίνηση της Υπηρεσίας σε Νέο Κατάλογο

Το launchd αποθηκεύει την απόλυτη διαδρομή προς το εκτελέσιμο, οπότε η μετακίνηση της εγκατάστασης απαιτεί επανεγγραφή της υπηρεσίας:

1. **Απεγκατάσταση της Τρέχουσας Υπηρεσίας**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Μετακίνηση των Αρχείων της Εφαρμογής**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Επανεγκατάσταση της Υπηρεσίας**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Εκκίνηση της Υπηρεσίας**
   ```bash
   sudo ./start_service.sh
   ```

### Απεγκατάσταση της Υπηρεσίας

1. **Σταματήστε την Τρέχουσα Υπηρεσία**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Καταργήστε την Εγγραφή της Υπηρεσίας**
   ```bash
   sudo ./uninstall_service.sh
   ```

Η digna πλέον έχει καταργηθεί από το launchd.

---

## Αναβάθμιση σε Νέα Έκδοση {: #upgrading-to-a-new-release }

Αυτή η ενότητα περιγράφει την αναβάθμιση μιας εγκατάστασης της Έκδοσης 2026.06 στην Έκδοση 2026.11.

!!! warning "Αναβάθμιση Από Έκδοση Παλαιότερη Της 2026.06"

    Εκτελέστε πρώτα τα βήματα αναβάθμισης της Έκδοσης 2026.06: [Αναβάθμιση σε Νέα Έκδοση](../Release%202026.06/installation_guide_digna_macos_2026_06.md#upgrading-to-a-new-release). Στη συνέχεια, συνεχίστε με τα παρακάτω βήματα.

### Πριν την Αναβάθμιση

**Η δημιουργία αντιγράφου ασφαλείας (backup) του digna Repository είναι υποχρεωτική**

Πριν αναβαθμίσετε την digna, δημιουργήστε backup του repository σας (PostgreSQL) για προστασία από απώλεια δεδομένων. Ένα backup εξασφαλίζει ότι μπορείτε να ανακτήσετε σε περίπτωση απρόβλεπτων προβλημάτων κατά την αναβάθμιση.

Για να δημιουργήσετε backup από το Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Αίτηση για το Αρχείο Άδειας της Έκδοσης 2026.11**

Η Έκδοση 2026.11 χρειάζεται νέο `license.toml`. Ζητήστε το από την ομάδα της digna πριν ξεκινήσετε και έχετέ το έτοιμο για το [Βήμα 7](#step-7-replace-the-license-file).

### Διαδικασία Αναβάθμισης

#### Βήμα 1: Σταματήστε την υπηρεσία digna {: #step-1-stop-the-digna-service }

Εάν η digna τρέχει ως υπηρεσία στο παρασκήνιο, σταματήστε την πρώτα:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Εάν η digna τρέχει σε πρώτο πλάνο, πατήστε ++ctrl+c++ στο παράθυρο Terminal της.

#### Βήμα 2: Δημιουργήστε αντίγραφο της τρέχουσας εγκατάστασης {: #step-2-backup-current-installation }

Στον κατάλογο εγκατάστασης digna, μετονομάστε το εκτελέσιμο και τον φάκελο του dashboard της τρέχουσας εγκατάστασης, ώστε η νέα έκδοση να μπορεί να αναπτυχθεί δίπλα τους:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

Κρατήστε το `digna_old` μέχρι να επαληθεύσετε την αναβάθμιση και τον `dashboard_old` μέχρι να επαναφέρετε από αυτόν τα αρχεία διαμόρφωσής σας (δείτε το Βήμα 4). Μετά μπορείτε να διαγράψετε και τα δύο.

#### Βήμα 3: Αποσυμπίεση και Ανάπτυξη της Νέας Έκδοσης {: #step-3-extract-and-deploy-new-version }

1. Αποσυμπιέστε το νέο πακέτο εγκατάστασης digna ZIP
2. Αντιγράψτε το νέο εκτελέσιμο `digna` και τον φάκελο `dashboard` στον κατάλογο εγκατάστασης
3. Επαναφέρετε το bit εκτέλεσης και, αν χρειάζεται, αφαιρέστε το χαρακτηριστικό καραντίνας:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Σημαντικό"

    Ούτε το `config.toml` ούτε το `dashboard/dashboard_config.toml` περιλαμβάνονται ποτέ στο ZIP εγκατάστασης — η ομάδα της digna δεν παρέχει ποτέ κανένα από τα δύο αρχεία. Η υπάρχουσα διαμόρφωσή σας επομένως δεν επηρεάζεται από την αναβάθμιση, και τα αντίγραφα στους μετονομασμένους φακέλους `*_old` είναι τα μόνα που έχετε.

#### Βήμα 4: Επαναφορά των Αρχείων Διαμόρφωσης {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

Η Έκδοση 2026.11 δεν απαιτεί καμία αλλαγή στο `config.toml`: ένα αρχείο που λειτουργεί με την Έκδοση 2026.06 συνεχίζει να λειτουργεί. Δύο αλλαγές είναι προαιρετικές:

- Προσθέστε μια [ενότητα `[duckdb]`](#duckdb-section) αν οι συνδέσεις βάσεων δεδομένων πρόκειται να χρησιμοποιούν το digna Engine και οι προεπιλογές του δεν ταιριάζουν στον host σας.
- Παραλείψτε την ενότητα `[app]` αν ένας reverse proxy σερβίρει το dashboard και το backend κάτω από ένα origin.

!!! warning "Ρυθμίσεις που το digna δεν διαβάζει"

    Προηγούμενες εκδόσεις αυτού του οδηγού έδειχναν ορισμένες ρυθμίσεις που το digna δεν διαβάζει. Δεν έχουν καμία επίδραση, και το `config check` τις παραθέτει κάτω από το **Unknown keys** στο Βήμα 6. Αφαιρέστε ή διορθώστε τες:

    - Τα `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`, `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` και `digna_LOGGING_BACKUP_COUNT` δεν υπάρχουν. Αφαιρέστε τα.
    - Τα ονόματα των ρυθμίσεων κάνουν διάκριση πεζών-κεφαλαίων. Το digna διαβάζει `DIGNA_REPO_HOST`, όχι `digna_REPO_HOST`. Γράψτε κάθε όνομα με κεφαλαία, όπως στην ενότητα [Διαμόρφωση Backend](#backend-configuration).

!!! warning "Ενιαία σύνδεση: διατηρήστε το [[oidc_clients]]"

    Το digna διαβάζει τους παρόχους ενιαίας σύνδεσης ως λίστα καταχωρήσεων `[[oidc_clients]]`, καθεμία με το δικό της `DIGNA_OIDC_KEY`. Αν αλλάξατε τους παρόχους σας σε ενότητες `[oidc_clients.<key>]`, όπως έδειχνε μια προηγούμενη έκδοση αυτού του οδηγού, επαναφέρετέ τους. Το `config check` αναφέρει το `OIDC config(s)` ως FAILED όσο υπάρχει αυτή η μορφή:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Επαναλάβετε την καταχώρηση για κάθε πάροχο και διατηρήστε κάθε `DIGNA_OIDC_KEY` ίδιο με το `key` στο `dashboard_config.toml`. Επηρεάζονται μόνο οι εγκαταστάσεις που χρησιμοποιούν ενιαία σύνδεση.

#### Βήμα 5: Επαναφόρτωση του Web Server {: #step-5-reload-the-web-server }

Το dashboard είναι ένα σύνολο στατικών αρχείων, οπότε ο web server σας — και ο browser — μπορεί να εξακολουθούν να σερβίρουν την προηγούμενη έκδοση. Επαναφορτώστε ή επανεκκινήστε τον web server που φιλοξενεί τον φάκελο `dashboard` και στη συνέχεια φορτώστε ξανά τη σελίδα με πλήρη ανανέωση (++cmd+shift+r++).

#### Βήμα 6: Επικυρώστε τη διαμόρφωση {: #step-6-validate-the-configuration }

Βεβαιωθείτε ότι το `config.toml` είναι πλήρες πριν αγγίξετε το repository:

```bash
./digna config check
```

Κάθε ενότητα πρέπει να αναφέρει OK. Διορθώστε ό,τι αναφέρεται ως FAILED, αφαιρέστε τα κλειδιά που παρατίθενται κάτω από το **Unknown keys** και εκτελέστε ξανά την εντολή πριν συνεχίσετε.

#### Βήμα 7: Αντικατάσταση του Αρχείου Άδειας {: #step-7-replace-the-license-file }

Ένα αρχείο άδειας κανονικά μεταφέρεται από τη μία έκδοση στην επόμενη. Η Έκδοση 2026.11 αποτελεί εξαίρεση: προσθέτει δύο αδειοδοτούμενα modules, το digna Data Reconciliation και το digna Agentic, και μια άδεια που εκδόθηκε πριν από την 2026.11 δεν τα περιέχει. Αντιγράψτε το `license.toml` που σας παρείχε η ομάδα της digna για την Έκδοση 2026.11 στον κατάλογο εγκατάστασης, αντικαθιστώντας το παλιό:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Μην κρατήσετε την προηγούμενη άδεια"

    Με την προηγούμενη άδεια το digna εξακολουθεί να ξεκινά, αλλά το digna Data Reconciliation και ο digna MCP Server παραμένουν απενεργοποιημένα. Κάθε εντολή που ελέγχει την άδεια — `user`, `inspection`, `repo` — διακόπτεται πριν αγγίξει το repository όταν ο έλεγχος αποτύχει. Επαληθεύστε τη νέα άδεια πριν προχωρήσετε:

    ```bash
    ./digna license check
    ```

#### Βήμα 8: Αναβάθμιση του Σχήματος Repository {: #step-8-upgrade-the-repository-schema }

Στον κατάλογο εγκατάστασης της digna, εκτελέστε:

```bash
cd /opt/digna
./digna repo upgrade
```

Η Έκδοση 2026.11 διαχειρίζεται το schema του repository με migrations που φέρουν αριθμό έκδοσης. Η πρώτη αναβάθμιση από προηγούμενη έκδοση φέρνει το schema στην τελευταία έκδοση του προηγούμενου μηχανισμού, την καταγράφει ως σημείο εκκίνησης και στη συνέχεια εφαρμόζει τα migrations της Έκδοσης 2026.11. Ολοκληρώνεται με:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Όλα τα υπάρχοντα δεδομένα διατηρούνται. Για να δείτε την κατάσταση του repository οποιαδήποτε στιγμή, εκτελέστε `./digna repo check`: παραθέτει το πιο πρόσφατο εφαρμοσμένο migration και όσα εκκρεμούν.

!!! warning "Το digna δεν ξεκινά με παρωχημένο repository"

    Από την Έκδοση 2026.11, ο server αρνείται να ξεκινήσει όσο το repository χρειάζεται αναβάθμιση, και το αναφέρει, για παράδειγμα:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Εκτελέστε το `repo upgrade` πριν ξεκινήσετε τον server ή την υπηρεσία.

#### Βήμα 9: Επανεκκίνηση των Υπηρεσιών {: #step-9-restart-services }

Εάν τρέχετε ως υπηρεσία στο παρασκήνιο:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Εάν τρέχετε χειροκίνητα, επανεκκινήστε τον server:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Εάν χρησιμοποιείτε nginx ή Apache, επανεκκινήστε τον αντίστοιχο web server:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Βήμα 10: Επαλήθευση της Αναβάθμισης {: #step-10-verify-the-upgrade }

1. Επιβεβαιώστε την έκδοση του νέου εκτελέσιμου:

    ```bash
    ./digna version
    ```

    Η πρώτη γραμμή πρέπει να είναι `Release: 2026.11`.

2. Ανοίξτε το digna dashboard και επιβεβαιώστε ότι η διεπαφή φορτώνει σωστά.
3. Ελέγξτε την έξοδο του server και τα αρχεία στον κατάλογο `logs` για σφάλματα.
4. Δοκιμάστε τις συνδέσεις βάσεων δεδομένων σας — δείτε [Δοκιμή σύνδεσης](../../../databases/overview.md#testing-a-connection). Μετά από αναβάθμιση από έκδοση πριν από την 2026.06, μεταφέρετε πρώτα σε ODBC κάθε σύνδεση που δεν το χρησιμοποιούσε ήδη.

Για να ξεκινήσετε με τα νέα modules, δείτε [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md), [Σύνδεση ενός AI Agent](../../../platform/agentic/connect_ai_agent.md) για τον digna MCP Server και [Τοποθεσία Profiling](../../../platform/profiling/profiling_location.md) για το digna Engine.
