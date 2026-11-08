# Οδηγός Εγκατάστασης Linux για την digna Έκδοση 2026.11

**Έκδοση:** 2026.11

**Τελευταία ενημέρωση:** 7 Νοεμβρίου 2026


---

## Περιεχόμενα

1. [Εισαγωγή](#introduction)
2. [Απαιτήσεις Συστήματος](#system-requirements)
3. [Προεγκατάσταση](#pre-installation-setup)
4. [Ρύθμιση PostgreSQL Server](#postgresql-server-setup)
5. [Ρύθμιση Web Server](#web-server-configuration)
6. [Αρχική Εγκατάσταση](#initial-installation)
7. [Διαμόρφωση Backend](#backend-configuration)
8. [Διαμόρφωση Dashboard](#dashboard-configuration)
9. [Εκτέλεση digna ως υπηρεσία systemd](#running-digna-as-a-systemd-service)
10. [Αναβάθμιση σε Νέα Έκδοση](#upgrading-to-a-new-release)

---

## Εισαγωγή {: #introduction }

### Σχετικά με την digna

digna είναι μια ολοκληρωμένη πλατφόρμα με AI, σχεδιασμένη για την βελτιστοποίηση της διαχείρισης ποιότητας δεδομένων σε διάφορα περιβάλλοντα δεδομένων όπως warehouses, lakes και lakehouses. Χτισμένη για να είναι ιδιαίτερα επεκτάσιμη και προσαρμόσιμη, η digna αντιμετωπίζει σύγχρονα προβλήματα δεδομένων μέσω αυτοματισμού, παρακολούθησης σε πραγματικό χρόνο και ανίχνευσης ανωμαλιών.

Η digna αποτελείται από δύο κύρια συστατικά:

- **digna**: ο πυρήνας της εφαρμογής, υπεύθυνος για την επεξεργασία δεδομένων και την εκτέλεση ελέγχων ποιότητας. Ενοποιεί το backend και τη διεπαφή γραμμής εντολών σε ένα μόνο εκτελέσιμο αρχείο, αντικαθιστώντας τα ξεχωριστά προγράμματα `dignabackend` και `dignacli` των προηγούμενων εκδόσεων.
- **dignadashboard**: Διεπαφή web που φιλοξενείται σε web server και παρέχει φιλικό περιβάλλον για αλληλεπίδραση με την πλατφόρμα digna και οπτικοποίηση μετρήσεων ποιότητας δεδομένων.

### Τι νέο φέρνει η Έκδοση 2026.11

Αυτή η έκδοση προσθέτει το digna Data Reconciliation, το digna Agentic με τον digna MCP Server και το digna Engine, το οποίο μπορεί να κάνει profiling δεδομένων μέσα στο digna και να ελέγχει την ακεραιότητα αναφορών μεταξύ διαφορετικών τεχνολογιών βάσεων δεδομένων. Δείτε τις [σημειώσεις έκδοσης](../../../changelog/Release_202611.md) για πλήρεις λεπτομέρειες.

Για μια εγκατάσταση, η έκδοση φέρνει έναν νέο μηχανισμό migrations για το repository, μια προαιρετική ενότητα `[duckdb]` στο `config.toml` για το digna Engine και ένα νέο αρχείο άδειας. Η [ενότητα αναβάθμισης](#upgrading-to-a-new-release) καλύπτει καθένα από αυτά.

### Ψάχνετε για Windows ή macOS;

Αυτός ο οδηγός καλύπτει Linux. Για άλλες πλατφόρμες, δείτε τον [Οδηγό Εγκατάστασης για Windows](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) ή τον [Οδηγό Εγκατάστασης για macOS](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md).

### Σε ποιες διανομές αναφέρεται αυτός ο οδηγός;

Οι οδηγίες είναι γραμμένες για τις δύο πιο κοινές οικογένειες server. Όπου διαφέρουν, παρέχονται και οι δύο εντολές:

- **Οικογένεια Debian** — Debian, Ubuntu. Διαχειριστής πακέτων: `apt`.
- **Οικογένεια RHEL** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Διαχειριστής πακέτων: `dnf`.

Οποιαδήποτε σύγχρονη διανομή με `systemd` θα λειτουργήσει· μόνο τα ονόματα πακέτων και μερικές διαδρομές διαμόρφωσης αλλάζουν.

---

## Απαιτήσεις Συστήματος {: #system-requirements }

Πριν ξεκινήσετε την εγκατάσταση, βεβαιωθείτε ότι το σύστημά σας πληροί τις ακόλουθες ελάχιστες απαιτήσεις:

| Απαίτηση | Προδιαγραφή |
|---|---|
| **Λειτουργικό Σύστημα** | Ubuntu 22.04 LTS ή νεότερο, Debian 12 ή νεότερο, RHEL 9 / Rocky 9 / AlmaLinux 9 ή νεότερο |
| **Αρχιτεκτονική** | x86_64 (amd64) ή arm64 |
| **Init System** | systemd |
| **Μνήμη (Ελάχιστη Ρύθμιση)** | 16 GB RAM |
| **Χώρος στο Δίσκο** | 10 GB διαθέσιμος αποθηκευτικός χώρος |
| **Βάση Δεδομένων** | PostgreSQL Server 12 ή νεότερος |
| **Web Server** | nginx, Apache httpd, ή ισοδύναμο |

!!! info "digna Engine"

    Για τις συνδέσεις βάσεων δεδομένων που χρησιμοποιούν το digna Engine ως τοποθεσία profiling, το profiling εκτελείται στον ίδιο τον host του digna. Προβλέψτε επιπλέον μνήμη και χώρο στον δίσκο για αυτές, δείτε την [ενότητα \[duckdb\]](#duckdb-section).

### Επιλογές Εγκατάστασης Βάσης Δεδομένων

**Εάν το PostgreSQL είναι ήδη εγκατεστημένο:**
Μπορείτε να προσθέσετε μια νέα βάση δεδομένων για την digna στον υπάρχοντα PostgreSQL Server σας.

**Εάν εγκαθιστάτε το PostgreSQL στον ίδιο μηχάνημα με την digna:**

!!! info "Συνιστώμενες Προδιαγραφές"

    - **Μνήμη**: 32 GB RAM (αντί για 16 GB)
    - **Χώρος στο Δίσκο**: 50 GB διαθέσιμος αποθηκευτικός χώρος (αντί για 10 GB)

    Αυτές οι υψηλότερες προδιαγραφές προσαρμόζονται ώστε να τρέχουν ταυτόχρονα τόσο η digna όσο και η PostgreSQL βάθος δεδομένων.

### Έλεγχος Διανομής και Αρχιτεκτονικής

Πολλές εντολές σε αυτόν τον οδηγό διαφέρουν μεταξύ των οικογενειών Debian και RHEL. Για να ελέγξετε σε ποια είστε, εκτελέστε:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` ή `ID=debian` — χρησιμοποιήστε τις εντολές `apt`.
- `ID=rhel`, `rocky`, `almalinux` ή `fedora` — χρησιμοποιήστε τις εντολές `dnf`.
- `x86_64` ή `aarch64` — η αρχιτεκτονική του πακέτου εγκατάστασης που χρειάζεστε.

---

## Προεγκατάσταση {: #pre-installation-setup }

Πριν εγκαταστήσετε την digna, βεβαιωθείτε ότι δύο βασικές προϋποθέσεις είναι σε ισχύ:

1. **PostgreSQL Server** – για αποθήκευση υπολογισμένων μετρικών και δεδομένων απόδοσης
2. **Web Server** – για τη φιλοξενία του digna Dashboard

Εάν αυτά τα στοιχεία δεν είναι ήδη ρυθμισμένα, ακολουθήστε τις παρακάτω ενότητες για να τα εγκαταστήσετε και να τα διαμορφώσετε.

### Ανανέωση του Ευρετηρίου Πακέτων

Ενημερώστε τις λίστες πακέτων πριν εγκαταστήσετε οτιδήποτε:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Σημείωση"

    Σε όλο αυτόν τον οδηγό, η πρώτη εντολή σε ένα ζεύγος είναι για την **οικογένεια Debian** και η δεύτερη για την **οικογένεια RHEL**. Εκτελέστε μόνο αυτήν που ταιριάζει στο σύστημά σας.

---

## Ρύθμιση PostgreSQL Server {: #postgresql-server-setup }

### Εάν Έχετε Ήδη το PostgreSQL

Εάν το PostgreSQL είναι ήδη εγκατεστημένο και ενεργοποιημένο στον τοπικό σας υπολογιστή ή αν χρησιμοποιείτε έναν διαχειριζόμενο απομακρυσμένο PostgreSQL server, μπορείτε να προχωρήσετε στην [επόμενη ενότητα](#web-server-configuration).

### Εγκατάσταση PostgreSQL

#### Βήμα 1: Εγκαταστήστε το Πακέτο Server

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Συμβουλή"

    Τα πακέτα των διανομών μπορεί να υστερούν έναντι της τρέχουσας έκδοσης PostgreSQL. Εάν χρειάζεστε συγκεκριμένη νεότερη έκδοση, χρησιμοποιήστε το επίσημο [PostgreSQL apt ή yum repository](https://www.postgresql.org/download/linux/).

#### Βήμα 2: Αρχικοποίηση του Database Cluster

Στην **οικογένεια Debian**, το πακέτο δημιουργεί και ξεκινάει αυτόματα ένα cluster — παραλείψτε αυτό το βήμα.

Στην **οικογένεια RHEL**, το cluster πρέπει να δημιουργηθεί ρητά:

```bash
sudo postgresql-setup --initdb
```

#### Βήμα 3: Εκκίνηση και Ενεργοποίηση της Υπηρεσίας

```bash
sudo systemctl enable --now postgresql
```

Αυτό ξεκινάει αμέσως την PostgreSQL και την ρυθμίζει να ξεκινάει αυτόματα κατά την εκκίνηση.

#### Βήμα 4: Επαλήθευση της Εγκατάστασης

```bash
psql --version
sudo systemctl status postgresql
```

Θα πρέπει να δείτε την έκδοση του PostgreSQL και την υπηρεσία ως `active (running)`.

#### Βήμα 5: Σύνδεση στον Server

Ένα πακέτο PostgreSQL για Linux δημιουργεί έναν system λογαριασμό `postgres` που κατέχει το cluster. Συνδεθείτε μέσω αυτού:

```bash
sudo -u postgres psql
```

!!! note "Σημείωση — το Linux διαφέρει από τα Windows εδώ"

    Ο installer των Windows σας ζητάει να ορίσετε κωδικό για τον superuser `postgres` κατά την εγκατάσταση. Τα πακέτα Linux δεν το κάνουν. Αντ' αυτού, οι τοπικές συνδέσεις ελέγχονται με **peer authentication**: ο χρήστης του λειτουργικού συστήματος `postgres` επιτρέπεται να συνδεθεί ως ο χρήστης βάσης δεδομένων `postgres` χωρίς κωδικό.

    Γι' αυτό η παραπάνω εντολή χρησιμοποιεί `sudo -u postgres`. Το digna backend συνδέεται μέσω TCP με όνομα χρήστη και κωδικό, οπότε θα δημιουργήσετε έναν ρητό χρήστη digna στην ενότητα [Αρχική Εγκατάσταση](#initial-installation).

#### Βήμα 6: Επιβεβαίωση Θύρας

Η προεπιλεγμένη θύρα PostgreSQL είναι `5432`. Για να επιβεβαιώσετε σε ποια θύρα ακούει ο server σας:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Σημειώστε την τιμή — θα τη χρειαστείτε κατά τη ρύθμιση του backend της digna.

#### Βήμα 7: Ενεργοποίηση Επαλήθευσης με Κωδικό για τον Χρήστη digna

Η digna συνδέεται με την PostgreSQL μέσω TCP ως `digna_user`, το οποίο απαιτεί έλεγχο ταυτότητας με κωδικό και όχι peer authentication. Ελέγξτε ότι το `pg_hba.conf` το επιτρέπει.

Εντοπίστε το αρχείο:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Ανοίξτε το σε έναν επεξεργαστή και επιβεβαιώστε ότι οι γραμμές για το τοπικό TCP χρησιμοποιούν `scram-sha-256` (ή `md5` σε παλαιότερους servers) αντί για `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Επαναφορτώστε την PostgreSQL μετά από οποιαδήποτε αλλαγή:

```bash
sudo systemctl reload postgresql
```

!!! warning "Σημαντικό"

    Εάν η digna αναφέρει `FATAL: Ident authentication failed for user "digna_user"`, αυτή η ρύθμιση είναι η αιτία.

#### Βήμα 8: Εάν η PostgreSQL Τρέχει σε Άλλο Μηχάνημα

Για να δεχτεί συνδέσεις από διαφορετικό host, ορίστε το `listen_addresses` στο `postgresql.conf` και προσθέστε μια αντίστοιχη γραμμή `host` για το δίκτυό σας στο `pg_hba.conf`:

```
listen_addresses = '*'
```

Έπειτα ανοίξτε τη θύρα στο firewall και επανεκκινήστε την υπηρεσία:

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## Ρύθμιση Web Server {: #web-server-configuration }

Η digna χρειάζεται web server για να φιλοξενήσει το dashboard. Επιλέξτε μία από τις παρακάτω επιλογές:

- [nginx](#nginx-setup) — ελαφρύ και συνιστώμενο
- [Apache httpd](#apache-setup) — ευρέως διαδεδομένη εναλλακτική

Χρειάζεται να εγκαταστήσετε και να διαμορφώσετε **έναν μόνο** από αυτούς τους servers.

Και οι δύο ενότητες διαμορφώνουν δύο πράγματα που εξαρτάται το dashboard:

- **Single-page-application fallback**, ώστε το ανανέωμα ενός URL του dashboard να μην επιστρέφει 404
- **Τύπος MIME για `.md`**, ώστε τα αρχεία Markdown να σερβίρονται σωστά

### Ρύθμιση nginx {: #nginx-setup }

#### Επισκόπηση

Το nginx είναι ένας ελαφρύς, υψηλών επιδόσεων web server κατάλληλος για την παροχή του στατικού digna dashboard.

#### Εγκατάσταση

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### Εκκίνηση του nginx

```bash
sudo systemctl enable --now nginx
```

#### Επαλήθευση της Εγκατάστασης

1. Ανοίξτε τον browser σας
2. Πλοηγηθείτε στο `http://localhost`
3. Θα πρέπει να δείτε τη σελίδα καλωσορίσματος του nginx

#### Άνοιγμα Firewall

Εάν ο server προσεγγίζεται από άλλες μηχανές, επιτρέψτε την κίνηση HTTP:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Διαμόρφωση Site για το Dashboard

Το nginx περιλαμβάνει κάθε αρχείο στον κατάλογο `conf.d` και στις δύο οικογένειες διανομών. Δημιουργήστε ένα ξεχωριστό αρχείο διαμόρφωσης για την digna εκεί:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Επικολλήστε τα παρακάτω, αντικαθιστώντας το `/opt/digna/dashboard` με την πραγματική διαδρομή στο εξαγόμενο φάκελο `dashboard`:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
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

    Χωρίς την οδηγία `try_files`, η ανανέωση οποιασδήποτε σελίδας του dashboard εκτός από το root URL επιστρέφει 404. Αυτό είναι το αντίστοιχο του URL Rewrite module που απαιτείται από το IIS στα Windows.

#### Απενεργοποίηση της Προεπιλεγμένης Τοποθεσίας

Μόνο ένα server block μπορεί να είναι το `default_server` για μια θύρα. Στην **οικογένεια Debian**, αφαιρέστε την πακεταρισμένη προεπιλογή ώστε να μην υπάρχει σύγκρουση:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

Στην **οικογένεια RHEL**, σχολιάστε ή διαγράψτε το block `server { ... }` μέσα στο `/etc/nginx/nginx.conf`.

#### Εφαρμογή της Διαμόρφωσης

Δοκιμάστε τη σύνταξη της διαμόρφωσης και μετά επαναφορτώστε το nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Ρύθμιση Apache httpd {: #apache-setup }

#### Επισκόπηση

Το Apache httpd είναι διαθέσιμο στα προεπιλεγμένα repositories όλων των υποστηριζόμενων διανομών. Το πακέτο ονομάζεται `apache2` στην οικογένεια Debian και `httpd` στην οικογένεια RHEL.

#### Εγκατάσταση

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Εκκίνηση του Apache

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Επαλήθευση της Εγκατάστασης

1. Ανοίξτε τον browser σας
2. Πλοηγηθείτε στο `http://localhost`
3. Θα πρέπει να δείτε την προεπιλεγμένη σελίδα του Apache της διανομής

#### Απαιτείται: Ενεργοποίηση mod_rewrite

Το dashboard απαιτεί URL rewriting.

Στην **οικογένεια Debian**, ενεργοποιήστε το module και επανεκκινήστε:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

Στην **οικογένεια RHEL**, το `mod_rewrite` φορτώνεται από προεπιλογή. Επιβεβαιώστε το:

```bash
httpd -M | grep rewrite
```

#### Απαιτείται: Επιτρέψτε .htaccess Overrides

Ανοίξτε το αρχείο διαμόρφωσης για το document root σας:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Εντοπίστε το block `<Directory>` που καλύπτει το document root (`/var/www/html` και στις δύο οικογένειες) και αλλάξτε:

```apache
AllowOverride None
```

σε:

```apache
AllowOverride All
```

#### Απαιτείται: MIME Type για Αρχεία Markdown

Στο ίδιο αρχείο, προσθέστε την παρακάτω γραμμή ώστε τα αρχεία Markdown να σερβίρονται σωστά:

```apache
AddType text/markdown .md
```

!!! warning "Σημαντικό"

    Χωρίς αυτή τη ρύθμιση, τα `.md` αρχεία μπορεί να μην σερβίρονται σωστά.

#### Εφαρμογή της Διαμόρφωσης

Ελέγξτε τη σύνταξη της διαμόρφωσης και μετά επανεκκινήστε τον Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Αρχική Εγκατάσταση {: #initial-installation }

### Βήμα 1: Ρύθμιση του Repository της digna

Το repository της digna αποθηκεύει όλες τις μετρικές που υπολογίζει η digna. Λειτουργεί ως η κεντρική βάση δεδομένων για αναλυτικά και δεδομένα απόδοσης.

#### Δημιουργία Σχήματος Repository και Χρήστη

Ανοίξτε τον PostgreSQL client σας (psql, pgAdmin ή παρόμοιο) και εκτελέστε τις ακόλουθες εντολές SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Αντικαταστήστε τα παρακάτω placeholders:**

- `<digna_repo_schema>` — Το επιθυμητό όνομα του schema (π.χ., `dignarepo`)
- `<digna_repo_user>` — Το επιθυμητό όνομα χρήστη (π.χ., `digna_user`)
- `<digna_repo_password>` — Ένας ασφαλής κωδικός για αυτόν τον χρήστη

**Παράδειγμα:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Για να τρέξετε αυτά από το shell σε ένα βήμα:

```bash
sudo -u postgres psql
```

Έπειτα επικολλήστε τις δηλώσεις στο `postgres=#` prompt και πληκτρολογήστε `\q` για έξοδο.

!!! tip "Καλύτερη Πρακτική"

    Χρησιμοποιήστε ισχυρούς, σύνθετους κωδικούς για χρήστες βάσης δεδομένων. Αποφύγετε εύκολα μαντεύσιμα διαπιστευτήρια.

---

### Βήμα 2: Αποσυμπίεση του Πακέτου Εγκατάστασης digna

1. Εντοπίστε το αρχείο ZIP εγκατάστασης digna που σας έχει παρασχεθεί
2. Αποσυμπιέστε το στον επιθυμητό κατάλογο εγκατάστασης — για παράδειγμα `/opt/digna`
3. Μετά την αποσυμπίεση, θα πρέπει να δείτε τα παρακάτω αντικείμενα:
   - `dashboard/` — Διεπαφή web dashboard
   - `digna` — Κύριο εκτελέσιμο (backend + CLI σε ένα)

!!! info "Τα αρχεία διαμόρφωσης και άδειας δεν περιλαμβάνονται στο πακέτο"

    Ούτε το `config.toml` ούτε το `dashboard/dashboard_config.toml` παρέχονται με την εγκατάσταση — τα δημιουργείτε και τα δύο εσείς, στις ενότητες [Διαμόρφωση Backend](#backend-configuration) και [Διαμόρφωση Dashboard](#dashboard-configuration). Ούτε το `license.toml` παρέχεται με το πακέτο· η digna το παρέχει ξεχωριστά, όπως περιγράφεται στο Βήμα 3.

Για να αποσυμπιέσετε από το shell:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
```

!!! note "Σημείωση"

    Εάν το `unzip` δεν είναι εγκατεστημένο, προσθέστε το με `sudo apt install -y unzip` ή `sudo dnf install -y unzip`.

#### Κάντε το Εκτελέσιμο Να Είναι Ενεργό

Ανάλογα με τον τρόπο μεταφοράς του αρχείου, το bit εκτέλεσης μπορεί να μην έχει διατηρηθεί. Ορίστε το ρητά:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Δημιουργία Λογαριασμού Υπηρεσίας

Συνιστάται να τρέχετε το backend με έναν αφιερωμένο μη προνομιούχο χρήστη για παραγωγικές εγκαταστάσεις:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Σημείωση"

    Στην οικογένεια RHEL το αντίστοιχο μονοπάτι shell είναι `/sbin/nologin`.

### Βήμα 3: Εγκατάσταση του Αρχείου Άδειας

!!! warning "Σημαντικό"

    Το αρχείο άδειας **δεν** περιλαμβάνεται στο πακέτο εγκατάστασης και θα παρασχεθεί ξεχωριστά από την digna.

1. Εντοπίστε το αρχείο `license.toml` που σας έχει παρασχεθεί
2. Αντιγράψτε το στον ριζικό κατάλογο εγκατάστασης της digna (όπου βρίσκεται το `config.toml` και το εκτελέσιμο `digna`)

**Γιατί έχει σημασία:**
Το αρχείο άδειας περιέχει τις πληροφορίες πελάτη σας, ημερομηνία λήξης άδειας και ψηφιακή υπογραφή. **Μην τροποποιείτε αυτό το αρχείο** — οποιαδήποτε αλλαγή θα το ακυρώσει.

**Δομή καταλόγου μετά τη ρύθμιση:**

```
/opt/digna/
├── config.toml         (αρχείο διαμόρφωσης)
├── license.toml        (ΤΟ ΑΡΧΕΙΟ ΑΔΕΙΑΣ ΣΑΣ - αντιγράψτε εδώ)
├── digna               (κύριο εκτελέσιμο)
├── bin/                (scripts διαχείρισης υπηρεσίας)
└── dashboard/          (διεπαφή web)
    └── (αρχεία dashboard)
```

---

## Διαμόρφωση Backend {: #backend-configuration }

### Βήμα 1: Δημιουργία και Επεξεργασία του Αρχείου Διαμόρφωσης

Το αρχείο `config_template.toml` παρέχεται στον κατάλογο εγκατάστασης της digna. Απλά μετονομάστε το σε `config.toml`.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Τοποθεσία:** `/opt/digna/config.toml`

Ανοίξτε το `config.toml` σε έναν επεξεργαστή κειμένου και ρυθμίστε κάθε ενότητα παρακάτω.

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

    Εάν σερβίρετε το dashboard από nginx ή Apache στην προεπιλεγμένη θύρα HTTP, το origin που πρέπει να επιτρέψετε είναι `http://localhost` — ή το δημόσιο URL του server όταν το dashboard προσεγγίζεται από άλλες μηχανές.

!!! info "Η ενότητα [app] είναι προαιρετική"

    Από την Έκδοση 2026.11, και τα δύο κλειδιά, καθώς και ολόκληρη η ενότητα `[app]`, μπορούν να παραλειφθούν. Αυτή είναι η σωστή ρύθμιση όταν ένας reverse proxy σερβίρει το dashboard και το backend κάτω από ένα origin: ο browser τότε δεν κάνει αιτήματα μεταξύ διαφορετικών origins, και από προεπιλογή δεν επιτρέπεται κανένα.

#### Ενότητα [repo]

Αυτή η ενότητα διαμορφώνει τη σύνδεση με τη βάση PostgreSQL:

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

!!! tip "Καλύτερη Πρακτική"

    Το `config.toml` περιέχει κωδικό βάσης δεδομένων σε απλό κείμενο. Περιορίστε τα δικαιώματα έτσι ώστε μόνο ο λογαριασμός υπηρεσίας να μπορεί να το διαβάσει:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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

    Για να βρείτε τον αριθμό των πυρήνων CPU διαθέσιμων στο server σας, τρέξτε `nproc`.

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

Αυτή η ενότητα διαμορφώνει τη συμπεριφορά logging:

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
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Προεπιλογή: ο προσωρινός κατάλογος του συστήματος (`$TMPDIR`, ή `/tmp` όταν δεν έχει οριστεί) | Κατάλογος για προσωρινά αρχεία όταν τα δεδομένα δεν χωρούν στη μνήμη |

!!! tip "Διαστασιολόγηση του digna Engine"

    Προβλέψτε έως `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` μνήμης στον host του digna, επιπλέον όσης χρησιμοποιεί το ίδιο το digna, και αρκετό ελεύθερο χώρο στον δίσκο του προσωρινού καταλόγου ώστε να χωρά η μεγαλύτερη επιθεωρούμενη ημερομηνία των πηγών δεδομένων που χρησιμοποιούν το digna Engine. Ορίστε το `DIGNA_DUCKDB_TEMP_DIRECTORY` σε δίσκο με αυτόν τον χώρο, εγγράψιμο από τον λογαριασμό που εκτελεί το digna:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
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

1. Ανοίξτε ένα τερματικό
2. Πλοηγηθείτε στον κατάλογο εγκατάστασης της digna (όπου βρίσκονται το `config.toml` και το εκτελέσιμο `digna`)
3. Τρέξτε το τεστ σύνδεσης:

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

    Σε Linux, ο τρέχων κατάλογος δεν είναι στο PATH σας, οπότε το εκτελέσιμο καλείται ως `./digna` αντί για `digna`. Για να χρησιμοποιείτε τη συντομότερη μορφή παντού, προσθέστε έναν συμβολικό σύνδεσμο:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Βήμα 4: Εγκατάσταση του Σχήματος Repository

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

### Βήμα 5: Δημιουργία Διαχειριστή (Admin)

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

    Περιβάλλετε τον κωδικό με μονά εισαγωγικά. Τα `bash` και `zsh` αντιμετωπίζουν χαρακτήρες όπως `!`, `$` και `*` ειδικά, και ένας ανεπιπλέοντος κωδικός που περιέχει τέτοιους χαρακτήρες δεν θα περαστεί όπως πληκτρολογήθηκε.

!!! tip "Καλύτερη Πρακτική"

    Χρησιμοποιήστε ισχυρό κωδικό με μείγμα κεφαλαίων, πεζών, αριθμών και ειδικών χαρακτήρων.

---

### Βήμα 6: Εκκίνηση του digna Server

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

    Εάν το dashboard σερβίρεται από διαφορετική μηχανή από το backend, ανοίξτε και τη θύρα του API στο firewall:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "Ο διακομιστής δεσμεύει το τερματικό"

    Το `serve` εκτελείται στο προσκήνιο και συνεχίζει μέχρι να το σταματήσετε με ++ctrl+c++. Αφήστε το να εκτελείται όσο ολοκληρώνετε την εγκατάσταση· για αυτόματη εκκίνηση κατά την εκκίνηση του συστήματος, δείτε [Εκτέλεση του digna ως υπηρεσίας systemd](#running-digna-as-a-systemd-service).

## Διαμόρφωση Dashboard {: #dashboard-configuration }

### Βήμα 1: Ανάπτυξη του Dashboard στον Web Server

Το digna dashboard διαβάζει τη δική του διαμόρφωση από το `dashboard/dashboard_config.toml`. Το αρχείο αυτό δεν παρέχεται με την εγκατάσταση — το δημιουργείτε στον κατάλογο `dashboard/`, δίπλα στα αρχεία του dashboard.

Το περιεχόμενό του περιγράφεται στην ενότητα [Ενιαία Σύνδεση (SSO)](../../../sso/overview.md), όπου και χρειάζεται το αρχείο: περιέχει τις επιλογές σύνδεσης που προσφέρει το dashboard και, για αναπτύξεις πολλαπλών instances, τη σύνδεση με το backend.

Επιλέξτε τον web server σας και ακολουθήστε τα αντίστοιχα βήματα ανάπτυξης.

#### Ανάπτυξη σε nginx

Εάν ακολουθήσατε την ενότητα [Ρύθμισης nginx](#nginx-setup), το server block ήδη δείχνει στον φάκελο `dashboard` και δεν απαιτείται αντιγραφή.

1. **Επιβεβαιώστε τη διαδρομή**
   - Ανοίξτε `/etc/nginx/conf.d/digna.conf`
   - Επαληθεύστε ότι το `root` δείχνει στον εξαγόμενο φάκελο `dashboard`

2. **Βεβαιωθείτε ότι ο φάκελος είναι αναγνώσιμος**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Επαναφόρτωση nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Δοκιμή της Εγκατάστασης**
   - Ανοίξτε τον browser σας
   - Πλοηγηθείτε στο `http://localhost` (ή στο ρυθμισμένο URL)
   - Θα πρέπει να δείτε τη σελίδα εισόδου του digna dashboard

#### Ανάπτυξη σε Apache httpd

1. **Αντιγράψτε το Dashboard στο Document Root**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Προσθέστε τους Κανόνες Rewrite**

   Δημιουργήστε ένα αρχείο `.htaccess` μέσα στον εγκατεστημένο φάκελο ώστε οι διαδρομές του dashboard να επιβιώνουν στο ανανέωμα του browser:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
   ```

   Επικολλήστε τα παρακάτω:

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

3. **Επανεκκινήστε τον Apache**
   ```bash
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Πρόσβαση στο Dashboard**
   - Ανοίξτε τον browser σας
   - Πλοηγηθείτε στο `http://localhost/digna`
   - Θα πρέπει να δείτε τη σελίδα εισόδου του digna dashboard

### Βήμα 2: SELinux (μόνο για RHEL Family)

Στο RHEL, Rocky, AlmaLinux και Fedora, το SELinux είναι στο Enforcing από προεπιλογή και θα εμποδίσει τον web server από το να διαβάζει αρχεία εκτός των αναμενόμενων τοποθεσιών. Ελέγξτε εάν είναι ενεργό:

```bash
getenforce
```

Εάν το αποτέλεσμα είναι `Enforcing` και σερβίρετε το dashboard από `/opt/digna/dashboard`, επισημάνετε τον κατάλογο ώστε ο web server να μπορεί να τον διαβάσει:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Σημείωση"

    Εάν το `semanage` δεν βρεθεί, εγκαταστήστε το με `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Σημαντικό"

    Ένα dashboard που επιστρέφει **403 Forbidden** σε ένα φρεσκορυθμισμένο RHEL server είναι σχεδόν πάντα πρόβλημα επισήμανσης SELinux και όχι θέμα δικαιωμάτων αρχείων. Επιβεβαιώστε με `sudo ausearch -m avc -ts recent`.

---

## Εκτέλεση digna ως υπηρεσία systemd {: #running-digna-as-a-systemd-service }

### Γιατί να τρέξετε την digna ως υπηρεσία;

Η εκτέλεση του backend της digna ως υπηρεσία systemd διασφαλίζει ότι:

- Ξεκινά αυτόματα κατά την εκκίνηση του μηχανήματος
- Τρέχει στο παρασκήνιο χωρίς ανοιχτό παράθυρο τερματικού
- Επανεκκινά αυτόματα αν καταρρεύσει
- Μπορεί να διαχειριστεί μέσω του `systemctl`, του τυπικού διαχειριστή υπηρεσιών του Linux

### Αρχεία Διαχείρισης Υπηρεσίας

Όλα τα απαραίτητα αρχεία βρίσκονται στον κατάλογο εγκατάστασης της digna κάτω από: `bin/`

Τα ακόλουθα shell scripts είναι διαθέσιμα:

- `install_service.sh` — Εγγράφει την digna στο systemd
- `uninstall_service.sh` — Αφαιρεί την εγγραφή της υπηρεσίας
- `start_service.sh` — Ξεκινά την εγγεγραμμένη υπηρεσία
- `stop_service.sh` — Σταματά την τρέχουσα υπηρεσία

!!! warning "Απαιτούνται Δικαιώματα Root"

    Όλα τα scripts πρέπει να εκτελούνται με `sudo`, επειδή η εγγραφή μιας υπηρεσίας που ξεκινάει κατά την εκκίνηση γράφει ένα unit file στο `/etc/systemd/system`.

### Κάντε τα Scripts Εκτελέσιμα

Η αποσυμπίεση μπορεί να μην έχει διατηρήσει το executable bit. Πριν την πρώτη χρήση:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Εγκατάσταση της Υπηρεσίας

1. **Ανοίξτε ένα τερματικό**

2. **Πλοηγηθείτε στον φάκελο bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Τρέξτε το script εγκατάστασης**
   ```bash
   sudo ./install_service.sh
   ```

Η digna server έχει τώρα εγγραφεί στο systemd με **αυτόματη εκκίνηση** ενεργοποιημένη. Η υπηρεσία δεν ξεκινά αμέσως — δείτε την επόμενη ενότητα για να την ξεκινήσετε.

### Εκκίνηση και Στάση της Υπηρεσίας

#### Για να ξεκινήσετε την υπηρεσία

1. Ανοίξτε ένα τερματικό
2. Πλοηγηθείτε στο `/opt/digna/bin`
3. Εκτελέστε:
   ```bash
   sudo ./start_service.sh
   ```

#### Για να σταματήσετε την υπηρεσία

1. Ανοίξτε ένα τερματικό
2. Πλοηγηθείτε στο `/opt/digna/bin`
3. Εκτελέστε:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Συμβουλή"

    Πάντα σταματάτε την υπηρεσία πριν ενημερώσετε αρχεία εφαρμογής.

### Διαχείριση της Υπηρεσίας με systemctl

Μόλις εγγραφεί, η υπηρεσία μπορεί επίσης να ελεγχθεί με τις τυπικές εντολές systemd από οποιονδήποτε κατάλογο:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Επιβεβαίωση της Υπηρεσίας

Για να επιβεβαιώσετε ότι η υπηρεσία είναι εγγεγραμμένη και τρέχει:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` σημαίνει ότι η υπηρεσία ξεκινάει κατά την εκκίνηση· `active` σημαίνει ότι τρέχει τώρα.

### Προβολή των Logs της Υπηρεσίας

Το systemd καταγράφει ό,τι γράφει το backend στην κονσόλα. Για να το διαβάσετε:

```bash
sudo journalctl -u digna -n 100
```

Για να ακολουθήσετε το log ζωντανά ενώ αναπαράγετε ένα πρόβλημα:

```bash
sudo journalctl -u digna -f
```

!!! tip "Συμβουλή"

    Αυτός είναι ο ταχύτερος τρόπος για να διαγνώσετε μια υπηρεσία που ξεκινά και αμέσως σταματάει. Μια αποτυχία σύνδεσης στο repository ή ένα λείπον `license.toml` αναφέρεται εδώ.

### Μετακίνηση της Υπηρεσίας σε Νέο Κατάλογο

Το unit αρχείο αποθηκεύει την απόλυτη διαδρομή προς το εκτελέσιμο, οπότε η μετακίνηση της εγκατάστασης απαιτεί επανεγγραφή της υπηρεσίας:

1. **Απεγκαταστήστε την τρέχουσα υπηρεσία**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Μετακινήστε τα αρχεία της εφαρμογής**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Εγκαταστήστε ξανά την υπηρεσία**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Ξεκινήστε την υπηρεσία**
   ```bash
   sudo ./start_service.sh
   ```

### Απεγκατάσταση της Υπηρεσίας

1. **Σταματήστε την τρέχουσα υπηρεσία**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Απεγκαταστήστε την υπηρεσία**
   ```bash
   sudo ./uninstall_service.sh
   ```

Η digna server έχει πλέον αφαιρεθεί από το systemd.

---

## Αναβάθμιση σε Νέα Έκδοση {: #upgrading-to-a-new-release }

Αυτή η ενότητα περιγράφει την αναβάθμιση μιας εγκατάστασης της Έκδοσης 2026.06 στην Έκδοση 2026.11.

!!! warning "Αναβάθμιση Από Έκδοση Παλαιότερη Της 2026.06"

    Εκτελέστε πρώτα τα βήματα αναβάθμισης της Έκδοσης 2026.06: [Αναβάθμιση σε Νέα Έκδοση](../Release%202026.06/installation_guide_digna_linux_2026_06.md#upgrading-to-a-new-release). Στη συνέχεια, συνεχίστε με τα παρακάτω βήματα.

### Πριν την Αναβάθμιση

**Η δημιουργία αντιγράφου ασφαλείας (backup) του digna Repository είναι υποχρεωτική**

Πριν αναβαθμίσετε την digna, δημιουργήστε backup του repository σας (PostgreSQL) για προστασία από απώλεια δεδομένων. Ένα backup εξασφαλίζει ότι μπορείτε να ανακτήσετε σε περίπτωση απρόβλεπτων προβλημάτων κατά την αναβάθμιση.

Για να δημιουργήσετε backup από το shell:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Αίτηση για το Αρχείο Άδειας της Έκδοσης 2026.11**

Η Έκδοση 2026.11 χρειάζεται νέο `license.toml`. Ζητήστε το από την ομάδα της digna πριν ξεκινήσετε και έχετέ το έτοιμο για το [Βήμα 7](#step-7-replace-the-license-file).

### Διαδικασία Αναβάθμισης

#### Βήμα 1: Σταματήστε την υπηρεσία digna {: #step-1-stop-the-digna-service }

Εάν η digna τρέχει ως υπηρεσία systemd, σταματήστε την πρώτα:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Εάν η digna τρέχει σε πρώτο πλάνο, πατήστε ++ctrl+c++ στο παράθυρο τερματικού της.

#### Βήμα 2: Δημιουργήστε αντίγραφο της τρέχουσας εγκατάστασης {: #step-2-backup-current-installation }

Στον κατάλογο εγκατάστασης digna, μετονομάστε το εκτελέσιμο και τον φάκελο του dashboard της τρέχουσας εγκατάστασης, ώστε η νέα έκδοση να μπορεί να αναπτυχθεί δίπλα τους:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

Κρατήστε το `digna_old` μέχρι να επαληθεύσετε την αναβάθμιση και τον `dashboard_old` μέχρι να επαναφέρετε από αυτόν τα αρχεία διαμόρφωσής σας (δείτε το Βήμα 4). Μετά μπορείτε να διαγράψετε και τα δύο.

#### Βήμα 3: Αποσυμπίεση και Ανάπτυξη της Νέας Έκδοσης {: #step-3-extract-and-deploy-new-version }

1. Αποσυμπιέστε το νέο πακέτο εγκατάστασης digna ZIP
2. Αντιγράψτε το νέο εκτελέσιμο `digna` και τον φάκελο `dashboard` στον κατάλογο εγκατάστασης
3. Επαναφέρετε το bit εκτέλεσης και την ιδιοκτησία του λογαριασμού υπηρεσίας:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Σημαντικό"

    Ούτε το `config.toml` ούτε το `dashboard/dashboard_config.toml` περιλαμβάνονται ποτέ στο ZIP εγκατάστασης — η ομάδα της digna δεν παρέχει ποτέ κανένα από τα δύο αρχεία. Η υπάρχουσα διαμόρφωσή σας επομένως δεν επηρεάζεται από την αναβάθμιση, και τα αντίγραφα στους μετονομασμένους φακέλους `*_old` είναι τα μόνα που έχετε.

#### Βήμα 4: Επαναφορά των Αρχείων Διαμόρφωσης {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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

Το dashboard είναι ένα σύνολο στατικών αρχείων, οπότε ο web server σας — και ο browser — μπορεί να εξακολουθούν να σερβίρουν την προηγούμενη έκδοση. Επαναφορτώστε ή επανεκκινήστε τον web server που φιλοξενεί τον φάκελο `dashboard` και στη συνέχεια φορτώστε ξανά τη σελίδα με πλήρη ανανέωση (++ctrl+f5++).

#### Βήμα 6: Επικυρώστε τη διαμόρφωση {: #step-6-validate-the-configuration }

Βεβαιωθείτε ότι το `config.toml` είναι πλήρες πριν αγγίξετε το repository:

```bash
./digna config check
```

Κάθε ενότητα πρέπει να αναφέρει OK. Διορθώστε ό,τι αναφέρεται ως FAILED, αφαιρέστε τα κλειδιά που παρατίθενται κάτω από το **Unknown keys** και εκτελέστε ξανά την εντολή πριν συνεχίσετε.

#### Βήμα 7: Αντικατάσταση του Αρχείου Άδειας {: #step-7-replace-the-license-file }

Ένα αρχείο άδειας κανονικά μεταφέρεται από τη μία έκδοση στην επόμενη. Η Έκδοση 2026.11 αποτελεί εξαίρεση: προσθέτει δύο αδειοδοτούμενα modules, το digna Data Reconciliation και το digna Agentic, και μια άδεια που εκδόθηκε πριν από την 2026.11 δεν τα περιέχει. Αντιγράψτε το `license.toml` που σας παρείχε η ομάδα της digna για την Έκδοση 2026.11 στον κατάλογο εγκατάστασης, αντικαθιστώντας το παλιό:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
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

Εάν τρέχετε ως υπηρεσία systemd:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Εάν τρέχετε χειροκίνητα, επανεκκινήστε τον server:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Εάν χρησιμοποιείτε nginx ή Apache, επαναφορτώστε τον αντίστοιχο web server:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

Στην οικογένεια RHEL, εφαρμόστε ξανά την επισήμανση SELinux εάν αντικαταστάθηκε ο κατάλογος `dashboard`:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Βήμα 10: Επαλήθευση της Αναβάθμισης {: #step-10-verify-the-upgrade }

1. Επιβεβαιώστε την έκδοση του νέου εκτελέσιμου:

    ```bash
    ./digna version
    ```

    Η πρώτη γραμμή πρέπει να είναι `Release: 2026.11`.

2. Ανοίξτε το digna dashboard και επιβεβαιώστε ότι η διεπαφή φορτώνει σωστά.
3. Ελέγξτε τα logs του server για σφάλματα:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. Δοκιμάστε τις συνδέσεις βάσεων δεδομένων σας — δείτε [Δοκιμή σύνδεσης](../../../databases/overview.md#testing-a-connection). Μετά από αναβάθμιση από έκδοση πριν από την 2026.06, μεταφέρετε πρώτα σε ODBC κάθε σύνδεση που δεν το χρησιμοποιούσε ήδη.

Για να ξεκινήσετε με τα νέα modules, δείτε [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md), [Σύνδεση ενός AI Agent](../../../platform/agentic/connect_ai_agent.md) για τον digna MCP Server και [Τοποθεσία Profiling](../../../platform/profiling/profiling_location.md) για το digna Engine.