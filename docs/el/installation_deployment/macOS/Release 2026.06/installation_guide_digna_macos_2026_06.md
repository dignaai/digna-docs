---
title: Οδηγός Εγκατάστασης macOS – digna Έκδοση 2026.06 | Τεκμηρίωση digna
description: Οδηγός βήμα-προς-βήμα για την εγκατάσταση της digna Έκδοση 2026.06 σε macOS — απαιτήσεις συστήματος, ρύθμιση Homebrew και PostgreSQL, διαμόρφωση nginx ή Apache, ρύθμιση backend και dashboard, εκτέλεση digna ως υπηρεσία στο παρασκήνιο και αναβάθμιση σε νέα έκδοση.
keywords: digna macos εγκατάσταση, οδηγός ανάπτυξης digna mac, ρύθμιση backend digna, εγκατάσταση dashboard digna, postgresql homebrew, nginx macos, υπηρεσία launchd digna, οδηγός αναβάθμισης digna
image: /assets/logo_square.png
---

# Οδηγός Εγκατάστασης macOS για digna Έκδοση 2026.06

**Έκδοση:** 2026.06

**Τελευταία Ενημέρωση:** 5 Σεπτεμβρίου 2026


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

- **dignabackend**: Ο πυρήνας της εφαρμογής, υπεύθυνος για επεξεργασία δεδομένων και εκτέλεση ελέγχων ποιότητας.
- **dignadashboard**: Διεπαφή web που φιλοξενείται σε web server και προσφέρει έναν φιλικό τρόπο αλληλεπίδρασης με την πλατφόρμα digna και οπτικοποίησης μετρικών ποιότητας δεδομένων.

### Τι νέο φέρνει η Έκδοση 2026.06

Αυτή η έκδοση φέρνει δυνατότητες παρατηρησιμότητας δεδομένων απευθείας στον κώδικα, επιτρέποντας στους προγραμματιστές να παρακολουθούν την ποιότητα των δεδομένων στην πηγή. Δείτε τις [σημειώσεις έκδοσης](http://docs.digna.ai/changelog/Release_202606/) για πλήρεις λεπτομέρειες.

### Ψάχνετε για Windows ή Linux;

Αυτός ο οδηγός καλύπτει macOS. Για άλλες πλατφόρμες, δείτε τον [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) ή τον [Linux Installation Guide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

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
   - `config.toml` — Αρχείο ρυθμίσεων
   - `license.toml` — Αρχείο άδειας (τοποθετήστε εδώ τη δική σας άδεια)

Για να αποσυμπιέσετε από το Terminal:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
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
| `digna_APP_HOST` | `localhost` ή διεύθυνση IP | Όνομα host ή IP όπου φιλοξενείται το dignabackend |
| `digna_APP_PORT` | `8082` (προεπιλεγμένο) | Θύρα για τα REST API endpoints |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL frontend | Εάν το dashboard είναι σε διαφορετικό server, συμπεριλάβετε το URL του |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Απαιτείται για CORS με credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Επιτρέπονται όλες οι HTTP μέθοδοι |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Επιτρέπονται όλα τα headers |

!!! note "Σημείωση"

    Εάν σερβίρετε το dashboard από το nginx του Homebrew στην προεπιλεγμένη θύρα, το origin που πρέπει να επιτρέψετε είναι `http://localhost:8080`.

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
| `digna_REPO_HOST` | `localhost` ή IP | Όνομα host/IP του PostgreSQL server |
| `digna_REPO_PORT` | `5432` (προεπιλεγμένο) | Θύρα PostgreSQL |
| `digna_REPO_DB` | `postgres` | Όνομα βάσης δεδομένων |
| `digna_REPO_SCHEMA` | `dignarepo` | Το schema που δημιουργήσατε νωρίτερα |
| `digna_REPO_USER` | `digna_user` | Ο χρήστης που δημιουργήθηκε στην εγκατάσταση PostgreSQL |
| `digna_REPO_PASSWORD` | Ο κωδικός σας | Ο κωδικός που ορίσατε κατά τη δημιουργία του schema |

#### Ενότητα [base]

Αυτή η ενότητα περιέχει ρυθμίσεις ασφάλειας και cookies:

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
| `digna_COOKIE_DOMAIN` | `localhost` | Ταιριάξτε με το domain του frontend |
| `digna_COOKIE_SECURE` | `false` (τοπικά) / `true` (production) | Χρησιμοποιήστε `true` για συνδέσεις HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Πάντα ενεργοποιημένο για ασφάλεια |
| `digna_COOKIE_SAME_SITE` | `lax` | Αποτρέπει επιθέσεις CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ώρες) | Χρονικό όριο συνεδρίας σε δευτερόλεπτα |
| `digna_MAX_WORKERS` | Αριθμός πυρήνων CPU - 1 | Αριθμός παράλληλων εργασιών επιθεώρησης |

!!! tip "Συμβουλή"

    Για να βρείτε τον αριθμό πυρήνων CPU στο Mac σας, εκτελέστε `sysctl -n hw.ncpu`.

#### Ενότητα [logging]

Αυτή η ενότητα ρυθμίζει τη συμπεριφορά καταγραφής:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Παράμετρος | Τιμή | Σημειώσεις |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` ή `DEBUG` | `INFO` για παραγωγή, `DEBUG` για ανάλυση προβλημάτων |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Αριθμός ημερήσιων backups logs που θα διατηρούνται |

---

### Βήμα 2: Αρχικοποίηση του Repository

1. Ανοίξτε το **Terminal**
2. Πλοηγηθείτε στον κατάλογο εγκατάστασης της digna (όπου βρίσκονται το `config.toml` και το εκτελέσιμο `digna`)
3. Εκτελέστε το τεστ σύνδεσης:

```bash
cd /opt/digna
./digna repo check
```

Θα πρέπει να δείτε επιβεβαίωση ότι η σύνδεση έχει επιτευχθεί (το repository αυτό καθαυτό δεν έχει ακόμη αρχικοποιηθεί).

!!! note "Σημείωση"

    Στο macOS, οι εντολές στον τρέχοντα κατάλογο δεν είναι στο PATH σας, οπότε το εκτελέσιμο καλείται ως `./digna` αντί για `digna`. Για να χρησιμοποιείτε τη συντομότερη μορφή παντού, προσθέστε τον κατάλογο εγκατάστασης στο PATH σας:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Βήμα 3: Εγκατάσταση του Schema του Repository

Στον ίδιο κατάλογο, τρέξτε:

```bash
./digna repo install
```

Αυτή η εντολή εγκαθιστά τους απαραίτητους πίνακες και το schema στη βάση PostgreSQL σας.

### Βήμα 4: Εκκίνηση του διακομιστή digna

Στον κατάλογο εγκατάστασης της digna, ξεκινήστε τον server με:

```bash
./digna serve --address <host> --port <port>
```

**Παράμετροι:**
- `--address` — Όνομα host/IP
- `--port` — Θύρα server

Θα δείτε μηνύματα εκκίνησης που επιβεβαιώνουν ότι ο server τρέχει:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Συμβουλή"

    Την πρώτη φορά που θα ξεκινήσετε τον server, το macOS μπορεί να ζητήσει αν θέλετε η εφαρμογή να δέχεται εισερχόμενες δικτυακές συνδέσεις. Κάντε κλικ στο **Allow**, διαφορετικά το dashboard δεν θα μπορεί να συνδεθεί με το backend.

### Βήμα 5: Δημιουργία Διαχειριστή (Admin User)

1. Ανοίξτε ένα **νέο** παράθυρο Terminal
2. Πλοηγηθείτε στον κατάλογο εγκατάστασης της digna
3. Εκτελέστε την παρακάτω εντολή για να δημιουργήσετε έναν admin χρήστη:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Παράδειγμα:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Αυτό δημιουργεί έναν χρήστη με username `admin` και πλήρη δικαιώματα διαχειριστή.

!!! tip "Συμβουλή"

    Βάλτε τον κωδικό μέσα σε απλά εισαγωγικά. Το `zsh` αντιμετωπίζει ειδικά χαρακτήρες όπως `!`, `$` και `*`, και ένας απροστάτευτος κωδικός που τα περιέχει δεν θα περάσει σωστά.

!!! tip "Βέλτιστη Πρακτική"

    Χρησιμοποιήστε έναν ισχυρό κωδικό με ανάμειξη κεφαλαίων, πεζών, αριθμών και ειδικών χαρακτήρων.

---

## Διαμόρφωση Dashboard {: #dashboard-configuration }

### Βήμα 1: Ανάπτυξη του Dashboard στον Web Server

Το dashboard της digna έχει το δικό του ξεχωριστό αρχείο `config.toml` που βρίσκεται στον φάκελο `dashboard/`. Αυτή η ρύθμιση παρέχεται ήδη και συνήθως δεν χρειάζεται αλλαγές κατά την αρχική εγκατάσταση. Θα χρειαστεί να την τροποποιήσετε μόνο εάν απαιτείται προσαρμογή της σύνδεσης προς το backend.

Εάν χρειαστεί να αλλάξετε τη διαμόρφωση του dashboard (π.χ. για multi-instance deployments), ανατρέξτε στην τεκμηρίωση του dashboard.

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

### Πριν Αναβαθμίσετε

**Η δημιουργία αντιγράφου ασφαλείας του Repository της digna είναι ΥΠΟΧΡΕΩΤΙΚΗ**

Πριν αναβαθμίσετε την digna, κάντε backup του repository (PostgreSQL) για να προστατευθείτε από απώλεια δεδομένων.
Ένα backup σας επιτρέπει να επαναφέρετε σε περίπτωση που η αναβάθμιση αντιμετωπίσει απρόβλεπτα προβλήματα.

Για να δημιουργήσετε backup από το Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Διαδικασία Αναβάθμισης

#### Βήμα 1: Σταματήστε την Υπηρεσία digna

Αν η digna τρέχει ως υπηρεσία στο παρασκήνιο, σταματήστε την πρώτα:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Αν η digna τρέχει σε πρώτο πλάνο, πατήστε `Ctrl + C` στο παράθυρο Terminal όπου εκτελείται.

#### Βήμα 2: Backup της Τρέχουσας Εγκατάστασης Backend

Στον κατάλογο εγκατάστασης της digna:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### Βήμα 3: Αποσυμπίεση και Ανάπτυξη Νέας Έκδοσης

1. Αποσυμπιέστε το νέο ZIP αρχείο εγκατάστασης digna
2. Αντιγράψτε το νέο εκτελέσιμο `digna` και τον φάκελο `dashboard` στον κατάλογο εγκατάστασης
3. Επαναφέρετε το bit εκτέλεσης και, αν χρειάζεται, αφαιρέστε την ιδιότητα καραντίνας:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Σημαντικό"

    Το αρχείο `config.toml` **δεν** περιλαμβάνεται ποτέ στο ZIP εγκατάστασης. Η υπάρχουσα διαμόρφωσή σας παραμένει ασφαλής.

### Βήμα 4: Επαναφορά των Αρχείων Διαμόρφωσης

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Βήμα 5: Αναβάθμιση του Schema του Repository

Πλοηγηθείτε στον κατάλογο εγκατάστασης της digna και εκτελέστε:

```bash
cd /opt/digna
./digna repo upgrade
```

Αυτό ενημερώνει το schema του PostgreSQL στην τελευταία έκδοση διατηρώντας όλα τα υπάρχοντα δεδομένα.

### Βήμα 6: Επανεκκίνηση Υπηρεσιών

Εάν τρέχει ως υπηρεσία στο παρασκήνιο:

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

#### Βήμα 7: Επαλήθευση Αναβάθμισης

1. Πλοηγηθείτε στο dashboard της digna
2. Επιβεβαιώστε ότι το περιβάλλον φορτώνει σωστά
3. Ελέγξτε τα logs του server για τυχόν σφάλματα