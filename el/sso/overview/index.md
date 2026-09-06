# Επισκόπηση Single Sign-On

---

## Πίνακας Περιεχομένων

1. [Εισαγωγή και Επισκόπηση](#introduction-and-overview)
2. [Οδηγοί Παρόχων](#provider-guides)
3. [Βήματα Ρύθμισης](#configuration-steps)
4. [Ρύθμιση Dashboard](#dashboard-configuration)
5. [Ρύθμιση Backend](#backend-configuration)
6. [Δοκιμή Σύνδεσης](#testing-login)
7. [Αντιμετώπιση Προβλημάτων](#troubleshooting)
8. [Υποστηριζόμενοι Πάροχοι](#supported-providers)

---

## Εισαγωγή και Επισκόπηση {: #introduction-and-overview }

Αυτός ο οδηγός παρέχει βήμα‑προς‑βήμα οδηγίες για την ενσωμάτωση του Single Sign-On (SSO) στην πλατφόρμα digna χρησιμοποιώντας το **OpenID Connect (OIDC)**.

### Τι είναι το SSO;

Το Single Sign-On επιτρέπει στους χρήστες να συνδέονται στο digna με ασφάλεια χρησιμοποιώντας τα εταιρικά τους διαπιστευτήρια μέσω εξωτερικών παρόχων ταυτότητας. Οι χρήστες μπορούν να πιστοποιηθούν με τα εταιρικά τους διαπιστευτήρια αντί να διαχειρίζονται ξεχωριστούς κωδικούς για το digna.

### Πώς Λειτουργεί

Το SSO στο digna υλοποιείται με το πρωτόκολλο OIDC. Πολλοί πάροχοι ταυτότητας μπορούν να ρυθμιστούν παράλληλα μέσω των δύο βασικών αρχείων ρύθμισης:

- **`dashboard_config.toml`** — Ελέγχει το frontend της οθόνης σύνδεσης
- **`config.toml`** — Ρυθμίζει τις OIDC συνδέσεις στο backend

### Υποστηριζόμενοι Πάροχοι {: #supported-providers-overview }

Τα παραδείγματα σε αυτόν τον οδηγό χρησιμοποιούν **Microsoft** και **Google**, αλλά **οποιοσδήποτε πάροχος συμβατός με OIDC** μπορεί να ενσωματωθεί ακολουθώντας την ίδια δομή.

---

## Οδηγοί Παρόχων {: #provider-guides }

Κάθε πάροχος χρειάζεται τις ίδιες τέσσερις τιμές — ένα client ID, ένα client secret, ένα redirect URI και ένα discovery URL — αλλά κάθε πάροχος τις τοποθετεί σε διαφορετικό σημείο στην κονσόλα διαχείρισης, και αρκετοί έχουν ένα βήμα ειδικό για τον πάροχο που οι άλλοι δεν έχουν. Οι οδηγοί παρακάτω καλύπτουν αυτό το μέρος της εργασίας· αυτή η σελίδα καλύπτει το μέρος του digna, που είναι ίδιο για όλους.

| Provider | Οδηγός | Σημειώσεις |
|---|---|---|
| **AD FS** | [Ρύθμιση SSO με AD FS](adfs_sso_guide.md) | Self-hosted; ο μόνος πάροχος εδώ όπου εσείς ελέγχετε την υπηρεσία token |
| **Auth0** | [Ρύθμιση SSO με Auth0](auth0_sso_guide.md) | Το discovery URL είναι ανά tenant, και τα custom domains το αλλάζουν |
| **Google Workspace** | [Ρύθμιση SSO με Google Workspace](google_workspace_sso_guide.md) | Η οθόνη συγκατάθεσης πρέπει να δημοσιευτεί πριν συνδεθούν μη δοκιμαστικοί χρήστες |
| **Keycloak** | [Ρύθμιση SSO με Keycloak](keycloak_sso_guide.md) | Self-hosted; το discovery URL είναι ανά realm |
| **Microsoft Entra ID** | [Ρύθμιση SSO με Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | Το tenant ID εμφανίζεται στο discovery URL· τα secrets λήγουν |
| **Okta** | [Ρύθμιση SSO με Okta](okta_sso_guide.md) | Η επιλογή authorization server αλλάζει το discovery URL |
| **OneLogin** | [Ρύθμιση SSO με OneLogin](onelogin_sso_guide.md) | Ο τύπος εφαρμογής OIDC πρέπει να επιλεγεί κατά τη δημιουργία και δεν αλλάζει |
| **PingOne** | [Ρύθμιση SSO με PingOne](pingone_sso_guide.md) | Το environment ID εμφανίζεται στο discovery URL |

Οποιοσδήποτε άλλος πάροχος συμβατός με OIDC λειτουργεί με τον ίδιο τρόπο — δείτε [Άλλοι Πάροχοι OIDC](#supported-providers).

---

## Βήματα Ρύθμισης {: #configuration-steps }

Η ρύθμιση SSO απαιτεί ενημερώσεις σε δύο αρχεία. Αυτή η ενότητα εξηγεί πώς να ρυθμίσετε το κάθε ένα.

### Επισκόπηση Αρχείων Ρύθμισης

| Αρχείο | Τοποθεσία | Σκοπός |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend της οθόνης σύνδεσης |
| **config.toml** | `/config.toml` | OIDC συνδέσεις backend |

Και τα δύο αρχεία πρέπει να ρυθμιστούν για να λειτουργήσει σωστά το SSO.

---

## Ρύθμιση Dashboard {: #dashboard-configuration }

### Τοποθεσία Αρχείου

```
dashboard/dashboard_config.toml
```

### Βήμα 1: Προσθήκη Παρόχων OIDC

Προσθέστε εγγραφές κάτω από τον πίνακα `[[login.oidc]]` για κάθε πάροχο ταυτότητας που θέλετε να υποστηρίζετε.

**Παράδειγμα με Microsoft και Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Βήμα 2: Διαμόρφωση Επιλογών Σύνδεσης

Καθορίστε αν θα επιτρέπεται η σύνδεση με κωδικό:

```toml
[login]
usePassword = true
```

### Παράμετροι Ρύθμισης

#### Ενότητα `[[login.oidc]]`

| Παράμετρος | Τύπος | Απαραίτητο | Περιγραφή |
|---|---:|---:|---|
| `key` | string | Ναι | Μοναδικός αναγνωριστής για τη σύνδεση OIDC (πρέπει να ταιριάζει με το key στο config.toml) |
| `label` | string | Ναι | Κείμενο που εμφανίζεται στο κουμπί σύνδεσης (π.χ. "Login with Microsoft") |

#### Ενότητα `[login]`

| Παράμετρος | Τύπος | Προεπιλογή | Περιγραφή |
|---|---:|---:|---|
| `usePassword` | boolean | false | Επιτρέπει σύνδεση με κωδικό εκτός από το SSO |

### Κατανόηση του usePassword

**Αν `usePassword = true`:**
- Η οθόνη σύνδεσης δείχνει κουμπιά SSO (π.χ. "Login with Microsoft")
- Η οθόνη σύνδεσης δείχνει επίσης πεδία username και password
- Οι χρήστες μπορούν να πιστοποιηθούν με οποιαδήποτε μέθοδο
- Επιτρέπει υβριδικές ρυθμίσεις όπου κάποιοι χρήστες χρησιμοποιούν SSO και άλλοι κωδικούς

**Αν `usePassword = false` (ή παραληφθεί):**
- Η οθόνη σύνδεσης δείχνει μόνο κουμπιά SSO
- Δεν υπάρχουν πεδία username/password
- Διαθέσιμη μόνο η πιστοποίηση μέσω OIDC

!!! tip "Συμβουλή"

    Η σύνδεση με κωδικό είναι διαθέσιμη μόνο για χρήστες που δημιουργήθηκαν με κωδικούς χρησιμοποιώντας την εντολή `digna user add` ή μέσω του dashboard.

### Πλήρες Παράδειγμα

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## Ρύθμιση Backend {: #backend-configuration }

### Τοποθεσία Αρχείου

```
/config.toml
```

(Root digna installation directory)

### Βήμα 1: Προσθήκη Ενοτήτων Παρόχων OIDC

Κάθε πάροχος πρέπει να έχει αφιερωμένη ενότητα `[oidc.<key>]`. Το key πρέπει να ταιριάζει με το `key` που ορίζεται στο `dashboard_config.toml`.

### Διαμόρφωση για Microsoft

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Διαμόρφωση για Google

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Παράμετροι Ρύθμισης

| Παράμετρος | Τύπος | Απαραίτητο | Περιγραφή | Παράδειγμα |
|---|---:|---:|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Ναι | Client ID από τον πάροχο ταυτότητας | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Ναι | Client secret από τον πάροχο ταυτότητας | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Ναι | URL callback μετά την πιστοποίηση | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Ναι | Endpoint διαμόρφωσης OIDC | `https://login.microsoftonline.com/...` |

!!! warning "Σημαντικό"

    Αντικαταστήστε τις τιμές placeholder (`<client_id>`, `<client_secret>`, `<tenant_id>`) με τα πραγματικά διαπιστευτήρια από την κονσόλα προγραμματιστών του παρόχου ταυτότητας.

### Redirect URI

Το redirect URI πρέπει να είναι ίδιο στην ρύθμιση του παρόχου ταυτότητας:

```
http://localhost:5173/oidc/callback
```

Αν το digna φιλοξενείται σε διαφορετικό domain, ενημερώστε ανάλογα:
- Local: `http://localhost:5173/oidc/callback`
- Production: `https://digna.yourdomain.com/oidc/callback`

### Πλήρες Παράδειγμα

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Δοκιμή Σύνδεσης {: #testing-login }

Μετά την ολοκλήρωση της ρύθμισης, επαληθεύστε ότι το SSO λειτουργεί σωστά.

### Λίστα Ελέγχου πριν τη Δοκιμή

Πριν τη δοκιμή, βεβαιωθείτε:

- [ ] Το `dashboard_config.toml` έχει ενημερωθεί με παρόχους OIDC
- [ ] Το `config.toml` έχει ενημερωθεί με τα OIDC διαπιστευτήρια
- [ ] Και τα δύο αρχεία έχουν αποθηκευτεί
- [ ] Τα διαπιστευτήρια είναι σωστά (client ID, client secret)
- [ ] Το redirect URI ταιριάζει με το URL της ανάπτυξής σας
- [ ] Η εφαρμογή στον πάροχο ταυτότητας είναι ρυθμισμένη με το redirect URI

### Βήματα Δοκιμής

#### Βήμα 1: Επανεκκίνηση Υπηρεσιών

Επανεκκινήστε το backend του digna και τον web server για να εφαρμοστούν οι αλλαγές.

**Αν τρέχετε ως υπηρεσία στα Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Αν τρέχετε ως υπηρεσία σε Linux ή macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Αν τρέχετε χειροκίνητα:**
```bash
digna serve --address localhost --port 8082
```

**Επανεκκινήστε και τον web server** — IIS ή Tomcat στα Windows, nginx ή Apache σε Linux και macOS.

#### Βήμα 2: Άνοιγμα Dashboard

Ανοίξτε το dashboard του digna στο πρόγραμμα περιήγησης:

```
http://localhost:5173
```

(ή το ρυθμισμένο URL του dashboard)

#### Βήμα 3: Επαλήθευση Κουμπιών Σύνδεσης

Ελέγξτε ότι εμφανίζονται κουμπιά σύνδεσης για κάθε ρυθμισμένο πάροχο:

- Πρέπει να εμφανίζεται το κουμπί "Login with Microsoft"
- Πρέπει να εμφανίζεται το κουμπί "Login with Google"
- (Αν usePassword = true) Πρέπει να εμφανίζονται πεδία username/password

Αν τα κουμπιά δεν εμφανίζονται:
- Ελέγξτε ότι το `dashboard_config.toml` αποθηκεύτηκε
- Ελέγξτε ότι η υπηρεσία του dashboard επανεκκινήθηκε
- Ελέγξτε την κονσόλα του browser (F12) για σφάλματα

#### Βήμα 4: Δοκιμή SSO Σύνδεσης

Κάντε κλικ σε ένα από τα κουμπιά SSO (π.χ. "Login with Microsoft"):

1. Θα πρέπει να αναδρομολογηθείτε στη σελίδα σύνδεσης του παρόχου ταυτότητας
2. Συνδεθείτε με τα εταιρικά σας διαπιστευτήρια
3. Θα πρέπει να αναδρομολογηθείτε ξανά στο digna
4. Θα πρέπει να έχετε συνδεθεί στο digna

#### Βήμα 5: Επαλήθευση Δημιουργίας Χρήστη

Μετά από επιτυχή SSO σύνδεση:

- Ο χρήστης θα πρέπει να δημιουργηθεί αυτόματα στο digna
- Ο χρήστης θα πρέπει να έχει συνδεθεί
- Το προφίλ χρήστη θα εμφανίζει τα διαπιστευτήρια του παρόχου ταυτότητας
- Θα πρέπει να δείτε το dashboard του digna

#### Βήμα 6: Δοκιμή Σύνδεσης με Κωδικό (αν είναι ενεργοποιημένο)

Αν `usePassword = true`:

1. Αποσυνδεθείτε από το digna
2. Στη σελίδα σύνδεσης, εισάγετε username και password
3. Θα πρέπει να μπορείτε να συνδεθείτε με τα διαπιστευτήρια κωδικού

---

## Αντιμετώπιση Προβλημάτων {: #troubleshooting }

### Τα Κουμπιά Σύνδεσης Δεν Εμφανίζονται

**Συμπτώματα:**
- Τα κουμπιά OIDC δεν είναι ορατά στην σελίδα σύνδεσης
- Βλέπετε μόνο πεδία κωδικού (αν usePassword = true)

**Αιτίες & Λύσεις:**
1. Ελέγξτε ότι το `dashboard_config.toml` είναι στον φάκελο `dashboard/`
2. Επαληθεύστε ότι οι ενότητες `[[login.oidc]]` υπάρχουν με σωστή σύνταξη
3. Επανεκκινήστε την υπηρεσία του dashboard
4. Καθαρίστε την cache του browser (Ctrl+Shift+Delete ή Cmd+Shift+Delete)
5. Ελέγξτε την κονσόλα του browser (F12 → καρτέλα Console) για σφάλματα

---

### Σφάλμα Redirect URI Mismatch

**Συμπτώματα:**
- Μετά το κλικ στο κουμπί SSO, λάθος για "redirect_uri mismatch"
- Σφάλμα "The redirect URI is not registered"

**Αιτίες & Λύσεις:**
1. Επαληθεύστε το `DIGNA_OIDC_REDIRECT_URI` στο `config.toml` είναι σωστό
2. Επαληθεύστε ότι το redirect URI έχει καταχωρηθεί στις ρυθμίσεις του παρόχου ταυτότητας
3. Βεβαιωθείτε ότι και τα δύο χρησιμοποιούν τα ίδια ακριβώς URLs (συμπεριλαμβανομένου πρωτοκόλλου, domain, path)
4. Ελέγξτε για τυπογραφικά λάθη στο redirect URI
5. Αν χρησιμοποιείτε HTTPS, βεβαιωθείτε ότι το πιστοποιητικό είναι έγκυρο

---

### Σφάλμα Μη Εγκυρων Διαπιστευτηρίων Πελάτη

**Συμπτώματα:**
- Σφάλμα "Invalid client ID or secret"
- Η πιστοποίηση αποτυγχάνει με σφάλμα διαπιστευτηρίων

**Αιτίες & Λύσεις:**
1. Επαληθεύστε ότι `DIGNA_OIDC_CLIENT_ID` και `DIGNA_OIDC_CLIENT_SECRET` είναι σωστά
2. Βεβαιωθείτε ότι δεν υπάρχουν επιπλέον κενά ή ειδικοί χαρακτήρες
3. Ελέγξτε ότι τα διαπιστευτήρια δεν έχουν λήξει ή ανακληθεί
4. Επανεκκινήστε την υπηρεσία backend μετά την ενημέρωση της διαμόρφωσης
5. Ελέγξτε την κονσόλα του παρόχου ταυτότητας για επιβεβαίωση ότι τα διαπιστευτήρια είναι ενεργά

---

### Η Σύνδεση Κρέμεται ή Χάνει Χρόνο

**Συμπτώματα:**
- Το κλικ στο κουμπί SSO δεν κάνει τίποτα
- Χρόνος αναμονής μετά από λίγα δευτερόλεπτα
- Ο browser δείχνει "Failed to connect" ή παρόμοιο

**Αιτίες & Λύσεις:**
1. Επαληθεύστε ότι το backend του digna τρέχει: `digna repo check`
2. Ελέγξτε τη δικτυακή σύνδεση προς τον πάροχο ταυτότητας
3. Επαληθεύστε ότι το `DIGNA_OIDC_CONFIGURATION_URL` είναι προσβάσιμο
4. Ελέγξτε τους κανόνες firewall που επιτρέπουν εξερχόμενες συνδέσεις HTTPS
5. Βεβαιωθείτε ότι backend και dashboard μπορούν να επικοινωνήσουν μεταξύ τους

---

### Οι Χρήστες Δεν Δημιουργούνται Αυτόματα

**Συμπτώματα:**
- Η SSO σύνδεση είναι επιτυχής αλλά ο χρήστης δεν δημιουργείται στο digna
- Λαμβάνετε σφάλμα δικαιωμάτων μετά την SSO σύνδεση

**Αιτίες & Λύσεις:**
1. Επαληθεύστε ότι η διαμόρφωση OIDC είναι σωστή
2. Ελέγξτε ότι τα δικαιώματα χρηστών έχουν ρυθμιστεί σωστά
3. Ανασκοπήστε τα logs του digna για μηνύματα σφάλματος
4. Επανεκκινήστε την υπηρεσία backend
5. Επικοινωνήστε με support@digna.ai αν το πρόβλημα επιμένει

---

## Υποστηριζόμενοι Πάροχοι {: #supported-providers }

### Δοκιμασμένοι & Υποστηριζόμενοι

Οι παρακάτω πάροχοι OIDC έχουν δοκιμαστεί και είναι γνωστό ότι λειτουργούν:

| Provider | Configuration URL | Οδηγός Ρύθμισης |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Ρύθμιση SSO με AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Ρύθμιση SSO με Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Ρύθμιση SSO με Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Ρύθμιση SSO με Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Ρύθμιση SSO με Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Ρύθμιση SSO με Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Ρύθμιση SSO με OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Ρύθμιση SSO με PingOne](pingone_sso_guide.md) |

### Άλλοι Πάροχοι OIDC

Οποιοσδήποτε πάροχος που υποστηρίζει OpenID Connect μπορεί να ενσωματωθεί. Απαιτούμενες πληροφορίες:

- Client ID
- Client secret
- OpenID configuration URL (συνήθως στο `/.well-known/openid-configuration`)
- Υποστηριζόμενα scopes (συνήθως `openid profile email`)

Επικοινωνήστε με support@digna.ai αν χρειάζεστε βοήθεια για την ενσωμάτωση συγκεκριμένου παρόχου.

---

## Καλές Πρακτικές

**ΚΑΝΤΕ:**
- Χρησιμοποιήστε HTTPS σε παραγωγικό περιβάλλον (όχι HTTP)
- Αποθηκεύετε τα client secrets με ασφάλεια (χρησιμοποιήστε environment variables όπου είναι δυνατό)
- Περιστρέφετε τα secrets περιοδικά
- Δοκιμάστε σε μη παραγωγικό περιβάλλον πρώτα
- Τεκμηριώστε ποιους παρόχους έχετε ρυθμίσει
- Παρακολουθείτε τα logs σύνδεσης για ασυνήθιστη δραστηριότητα
- Κρατήστε τη διαμόρφωση του παρόχου ταυτότητας σε συγχρονισμό με τη διαμόρφωση του digna

**ΜΗΝ:**
- Αποθηκεύετε τα client secrets σε version control
- Χρησιμοποιείτε HTTP redirect URIs σε παραγωγή
- Ρυθμίζετε πολλούς παρόχους με το ίδιο key
- Αφήνετε προεπιλεγμένα/δοκιμαστικά διαπιστευτήρια σε παραγωγή
- Εκθέτετε αρχεία διαμόρφωσης που περιέχουν μυστικά
- Αναμειγνύετε διαπιστευτήρια ανάπτυξης και παραγωγής

---

## Υποστήριξη

Χρειάζεστε βοήθεια με τη ρύθμιση του SSO;

- **Email:** support@digna.ai
- **Τεκμηρίωση:** https://docs.digna.ai
- **Ιστότοπος:** https://www.digna.ai

---

**Τελευταία Ενημέρωση:** August 30, 2026  
**Έκδοση:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**