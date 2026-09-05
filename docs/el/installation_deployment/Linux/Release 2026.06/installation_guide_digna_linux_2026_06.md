---
title: Οδηγός Εγκατάστασης Linux – digna Έκδοση 2026.06 | Τεκμηρίωση digna
description: Βημα προς βήμα οδηγίες για την εγκατάσταση της digna Έκδοση 2026.06 σε Linux — απαιτήσεις συστήματος, ρύθμιση PostgreSQL, ρύθμιση nginx ή Apache, διαμόρφωση backend και dashboard, εκτέλεση digna ως υπηρεσία systemd και αναβάθμιση σε νέα έκδοση.
keywords: digna εγκατάσταση linux, οδηγός ανάπτυξης digna, ρύθμιση backend digna, εγκατάσταση dashboard digna, postgresql linux, nginx linux, υπηρεσία digna systemd, οδηγός αναβάθμισης digna
image: /assets/logo_square.png
---

# Οδηγός Εγκατάστασης Linux για την digna Έκδοση 2026.06

**Έκδοση:** 2026.06

**Τελευταία ενημέρωση:** 5 Σεπτεμβρίου 2026


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

- **dignabackend**: Ο πυρήνας της εφαρμογής, υπεύθυνος για την επεξεργασία δεδομένων και την εκτέλεση ελέγχων ποιότητας.
- **dignadashboard**: Διεπαφή web που φιλοξενείται σε web server και παρέχει φιλικό περιβάλλον για αλληλεπίδραση με την πλατφόρμα digna και οπτικοποίηση μετρήσεων ποιότητας δεδομένων.

### Τι νέο φέρνει η Έκδοση 2026.06

Αυτή η έκδοση φέρνει δυνατότητες παρατηρησιμότητας δεδομένων απευθείας στον κώδικα σας, επιτρέποντας στους προγραμματιστές να παρακολουθούν την ποιότητα των δεδομένων στην πηγή. Δείτε τις [σημειώσεις έκδοσης](http://docs.digna.ai/changelog/Release_202606/) για πλήρεις λεπτομέρειες.

### Ψάχνετε για Windows ή macOS;

Αυτός ο οδηγός καλύπτει Linux. Για άλλες πλατφόρμες, δείτε τον [Οδηγό Εγκατάστασης για Windows](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) ή τον [Οδηγό Εγκατάστασης για macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

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
   - `config.toml` — Αρχείο διαμόρφωσης
   - `license.toml` — Αρχείο άδειας (τοποθετήστε εδώ τη δική σας άδεια)

Για να αποσυμπιέσετε από το shell:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
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

Αυτή η ενότητα διαμορφώνει τις ρυθμίσεις της εφαρμογής backend της digna:

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
| `digna_APP_HOST` | `localhost` ή IP διεύθυνση | Hostname ή IP όπου φιλοξενείται το dignabackend |
| `digna_APP_PORT` | `8082` (προεπιλογή) | Θύρα για τα REST API endpoints |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL frontend | Αν το dashboard βρίσκεται σε διαφορετικό server, συμπεριλάβετε το URL του |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Απαραίτητο για CORS με credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Επιτρέπει όλες τις μεθόδους HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Επιτρέπει όλα τα headers |

!!! note "Σημείωση"

    Εάν σερβίρετε το dashboard από nginx ή Apache στην προεπιλεγμένη θύρα HTTP, το origin που πρέπει να επιτρέψετε είναι `http://localhost` — ή το δημόσιο URL του server όταν το dashboard προσεγγίζεται από άλλες μηχανές.

#### Ενότητα [repo]

Αυτή η ενότητα διαμορφώνει τη σύνδεση με τη βάση PostgreSQL:

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
| `digna_REPO_DB` | `postgres` | Όνομα βάσης |
| `digna_REPO_SCHEMA` | `dignarepo` | Το schema που δημιουργήθηκε νωρίτερα |
| `digna_REPO_USER` | `digna_user` | Ο χρήστης που δημιουργήθηκε στην PostgreSQL ρύθμιση |
| `digna_REPO_PASSWORD` | Ο κωδικός σας | Κωδικός που ορίσατε κατά τη δημιουργία του schema |

!!! tip "Καλύτερη Πρακτική"

    Το `config.toml` περιέχει κωδικό βάσης δεδομένων σε απλό κείμενο. Περιορίστε τα δικαιώματα έτσι ώστε μόνο ο λογαριασμός υπηρεσίας να μπορεί να το διαβάσει:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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
| `digna_FERNET_KEY` | Κλειδί κρυπτογράφησης | Χρησιμοποιείται για την κρυπτογράφηση tokens και cookies (παρέχεται προεπιλεγμένο) |
| `digna_COOKIE_DOMAIN` | `localhost` | Ταιριάξτε με το domain του frontend |
| `digna_COOKIE_SECURE` | `false` (τοπικά) / `true` (παραγωγή) | Χρησιμοποιήστε `true` για συνδέσεις HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Πάντα ενεργοποιημένο για ασφάλεια |
| `digna_COOKIE_SAME_SITE` | `lax` | Προστατεύει από CSRF επιθέσεις |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ώρες) | Χρόνος λήξης συνεδρίας σε δευτερόλεπτα |
| `digna_MAX_WORKERS` | Αριθμός CPU cores - 1 | Αριθμός παράλληλων εργασιών επιθεώρησης |

!!! tip "Συμβουλή"

    Για να βρείτε τον αριθμό των πυρήνων CPU διαθέσιμων στο server σας, τρέξτε `nproc`.

#### Ενότητα [logging]

Αυτή η ενότητα διαμορφώνει τη συμπεριφορά logging:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Παράμετρος | Τιμή | Σημειώσεις |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` ή `DEBUG` | `INFO` για παραγωγή, `DEBUG` για αντιμετώπιση προβλημάτων |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Αριθμός ημερήσιων αντιγράφων log που κρατούνται |

---

### Βήμα 2: Αρχικοποίηση του Repository

1. Ανοίξτε ένα τερματικό
2. Πλοηγηθείτε στον κατάλογο εγκατάστασης της digna (όπου βρίσκονται το `config.toml` και το εκτελέσιμο `digna`)
3. Τρέξτε το τεστ σύνδεσης:

```bash
cd /opt/digna
./digna repo check
```

Θα πρέπει να δείτε μια επιβεβαίωση ότι η σύνδεση έχει εγκαθιδρυθεί (το ίδιο το repository δεν έχει ακόμα αρχικοποιηθεί).

!!! note "Σημείωση"

    Σε Linux, ο τρέχων κατάλογος δεν είναι στο PATH σας, οπότε το εκτελέσιμο καλείται ως `./digna` αντί για `digna`. Για να χρησιμοποιείτε τη συντομότερη μορφή παντού, προσθέστε έναν συμβολικό σύνδεσμο:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Βήμα 3: Εγκατάσταση του Σχήματος Repository

Στον ίδιο κατάλογο, τρέξτε:

```bash
./digna repo install
```

Αυτή η εντολή εγκαθιστά τους απαραίτητους πίνακες και το σχήμα στη βάση PostgreSQL σας.

### Βήμα 4: Εκκίνηση του digna Server

Στον κατάλογο εγκατάστασης της digna, ξεκινήστε τον server με:

```bash
./digna serve --address <host> --port <port>
```

**Παράμετροι:**
- `--address` — Hostname/IP του server
- `--port` — Θύρα του server

Θα πρέπει να δείτε μηνύματα εκκίνησης που επιβεβαιώνουν ότι ο server τρέχει:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Συμβουλή"

    Εάν το dashboard σερβίρεται από διαφορετική μηχανή από το backend, ανοίξτε και τη θύρα του API στο firewall:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

### Βήμα 5: Δημιουργία Διαχειριστή (Admin)

1. Ανοίξτε ένα **νέο** παράθυρο τερματικού
2. Πλοηγηθείτε στον κατάλογο εγκατάστασης της digna
3. Εκτελέστε την ακόλουθη εντολή για να δημιουργήσετε έναν admin χρήστη:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Παράδειγμα:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Αυτό δημιουργεί έναν χρήστη με όνομα `admin` και πλήρη διαχειριστικά προνόμια.

!!! tip "Συμβουλή"

    Περιβάλλετε τον κωδικό με μονά εισαγωγικά. Τα `bash` και `zsh` αντιμετωπίζουν χαρακτήρες όπως `!`, `$` και `*` ειδικά, και ένας ανεπιπλέοντος κωδικός που περιέχει τέτοιους χαρακτήρες δεν θα περαστεί όπως πληκτρολογήθηκε.

!!! tip "Καλύτερη Πρακτική"

    Χρησιμοποιήστε ισχυρό κωδικό με μείγμα κεφαλαίων, πεζών, αριθμών και ειδικών χαρακτήρων.

---

## Διαμόρφωση Dashboard {: #dashboard-configuration }

### Βήμα 1: Ανάπτυξη του Dashboard στον Web Server

Το digna dashboard έχει το δικό του ξεχωριστό αρχείο `config.toml` που βρίσκεται στον κατάλογο `dashboard/`. Αυτή η διαμόρφωση παρέχεται ήδη και δεν απαιτεί αλλαγές κατά την αρχική εγκατάσταση. Θα χρειαστεί να την αλλάξετε μόνο εάν θέλετε να προσαρμόσετε τη σύνδεση με το backend.

Εάν χρειάζεται να τροποποιήσετε τη διαμόρφωση του dashboard (π.χ., για multi-instance deployments), ανατρέξτε στην τεκμηρίωση του dashboard.

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

### Πριν την Αναβάθμιση

**Η δημιουργία αντιγράφου ασφαλείας (backup) του digna Repository είναι ΥΠΟΧΡΕΩΤΙΚΗ**

Πριν αναβαθμίσετε την digna, δημιουργήστε backup του repository σας (PostgreSQL) για προστασία από απώλεια δεδομένων.
Ένα backup εξασφαλίζει ότι μπορείτε να ανακτήσετε σε περίπτωση απρόβλεπτων προβλημάτων κατά την αναβάθμιση.

Για να δημιουργήσετε backup από το shell:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Διαδικασία Αναβάθμισης

#### Βήμα 1: Σταματήστε την υπηρεσία digna

Εάν η digna τρέχει ως υπηρεσία systemd, σταματήστε την πρώτα:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Εάν η digna τρέχει σε πρώτο πλάνο, πατήστε `Ctrl + C` στο παράθυρο του τερματικού όπου τρέχει.

#### Βήμα 2: Backup της Τρέχουσας Εγκατάστασης Backend

Στον κατάλογο εγκατάστασης της digna:

```bash
cd /opt/digna
sudo mv digna digna_old
```
```bash
sudo mv dashboard dashboard_old
```

#### Βήμα 3: Αποσυμπίεση και Ανάπτυξη της Νέας Έκδοσης

1. Αποσυμπιέστε το νέο πακέτο εγκατάστασης digna ZIP
2. Αντιγράψτε το νέο εκτελέσιμο `digna` και το φάκελο `dashboard` στον κατάλογο εγκατάστασης
3. Επαναφέρετε το bit εκτέλεσης και την ιδιοκτησία του λογαριασμού υπηρεσίας:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Σημαντικό"

    Το αρχείο `config.toml` **δε**ν περιλαμβάνεται ποτέ στο ZIP εγκατάστασης. Η υπάρχουσα διαμόρφωσή σας παραμένει ασφαλής.

### Βήμα 4: Επαναφορά των Αρχείων Διαμόρφωσης

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Βήμα 5: Αναβάθμιση του Σχήματος Repository

Πλοηγηθείτε στον κατάλογο εγκατάστασης της digna και τρέξτε:

```bash
cd /opt/digna
./digna repo upgrade
```

Αυτό ενημερώνει το σχήμα PostgreSQL στην πιο πρόσφατη έκδοση ενώ διατηρεί όλα τα υπάρχοντα δεδομένα.

### Βήμα 6: Επανεκκίνηση των Υπηρεσιών

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

#### Βήμα 7: Επαλήθευση της Αναβάθμισης

1. Πρόσβαση στο digna dashboard
2. Επιβεβαιώστε ότι η διεπαφή φορτώνει σωστά
3. Ελέγξτε τα logs του server για τυχόν σφάλματα:

```bash
sudo journalctl -u digna -n 100
```