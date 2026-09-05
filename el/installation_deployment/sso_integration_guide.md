# Single Sign-On Integration Guide

---

## Table of Contents

1. [Introduction and Overview](#introduction-and-overview)
2. [Configuration Steps](#configuration-steps)
3. [Dashboard Configuration](#dashboard-configuration)
4. [Backend Configuration](#backend-configuration)
5. [Testing Login](#testing-login)
6. [Troubleshooting](#troubleshooting)
7. [Supported Providers](#supported-providers)

---

## Introduction and Overview {: #introduction-and-overview }

Αυτός ο οδηγός παρέχει βήμα προς βήμα οδηγίες για την ενσωμάτωση του Single Sign-On (SSO) στην πλατφόρμα digna χρησιμοποιώντας το πρωτόκολλο **OpenID Connect (OIDC)**.

### Τι είναι το SSO;

Το Single Sign-On επιτρέπει στους χρήστες να συνδέονται στο digna με ασφάλεια χρησιμοποιώντας τα εταιρικά τους διαπιστευτήρια μέσω εξωτερικών παρόχων ταυτότητας. Οι χρήστες μπορούν να αυθεντικοποιούνται με τα εταιρικά τους διαπιστευτήρια αντί να διαχειρίζονται ξεχωριστούς κωδικούς για το digna.

### Πώς λειτουργεί

Το SSO στο digna υλοποιείται χρησιμοποιώντας το πρωτόκολλο OIDC. Μπορούν να ρυθμιστούν πολλοί πάροχοι ταυτόχρονα προσαρμόζοντας δύο σημαντικά αρχεία διαμόρφωσης:

- **`dashboard_config.toml`** — Ελέγχει το frontend της οθόνης σύνδεσης
- **`config.toml`** — Διαμορφώνει τις OIDC συνδέσεις στο backend

### Υποστηριζόμενοι πάροχοι {: #supported-providers-overview }

Παραδείγματα σε αυτόν τον οδηγό χρησιμοποιούν **Microsoft** και **Google**, αλλά **οποιοσδήποτε OIDC-συμβατός πάροχος** μπορεί να ενσωματωθεί ακολουθώντας την ίδια δομή.

Συνηθισμένοι OIDC πάροχοι περιλαμβάνουν:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Άλλοι OIDC-συμβατοί πάροχοι ταυτότητας

---

## Configuration Steps {: #configuration-steps }

Η διαμόρφωση του SSO απαιτεί ενημερώσεις σε δύο αρχεία. Αυτή η ενότητα εξηγεί πώς να διαμορφώσετε το καθένα.

### Overview of Configuration Files

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend login interface |
| **config.toml** | `/config.toml` | Backend OIDC connections |

Και τα δύο αρχεία πρέπει να διαμορφωθούν για να λειτουργήσει σωστά το SSO.

---

## Dashboard Configuration {: #dashboard-configuration }

### File Location

```
dashboard/dashboard_config.toml
```

### Step 1: Add OIDC Providers

Προσθέστε εγγραφές κάτω από τον πίνακα `[[login.oidc]]` για κάθε πάροχο ταυτότητας που θέλετε να υποστηρίξετε.

**Παράδειγμα με Microsoft και Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Step 2: Configure Login Options

Καθορίστε αν θα επιτρέπεται η σύνδεση με βάση κωδικό πρόσβασης:

```toml
[login]
usePassword = true
```

### Configuration Parameters

#### `[[login.oidc]]` Section

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | Unique identifier for the OIDC connection (must match key in config.toml) |
| `label` | string | Yes | Text displayed on the login button (e.g., "Login with Microsoft") |

#### `[login]` Section

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | Allow password-based login in addition to SSO |

### Understanding usePassword

**If `usePassword = true`:**
- Η οθόνη σύνδεσης εμφανίζει κουμπιά SSO (π.χ. "Login with Microsoft")
- Η οθόνη σύνδεσης εμφανίζει επίσης πεδία username και password
- Οι χρήστες μπορούν να αυθεντικοποιηθούν με οποιαδήποτε από τις δύο μεθόδους
- Επιτρέπει υβριδικές ρυθμίσεις όπου κάποιοι χρήστες χρησιμοποιούν SSO και άλλοι κωδικό

**If `usePassword = false` (or omitted):**
- Η οθόνη σύνδεσης εμφανίζει μόνο τα κουμπιά SSO
- Δεν εμφανίζονται πεδία username/password
- Διαθέσιμη μόνο η OIDC αυθεντικοποίηση

!!! tip "Tip"

    Η σύνδεση με κωδικό είναι διαθέσιμη μόνο για χρήστες που δημιουργήθηκαν με κωδικούς χρησιμοποιώντας την εντολή `digna user add` ή μέσω του dashboard.

### Complete Example

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

## Backend Configuration {: #backend-configuration }

### File Location

```
/config.toml
```

(Root digna installation directory)

### Step 1: Add OIDC Provider Sections

Κάθε πάροχος πρέπει να έχει ξεχωριστή ενότητα `[oidc.<key>]`. Το key πρέπει να ταιριάζει με το `key` που ορίζεται στο `dashboard_config.toml`.

### Microsoft Configuration

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google Configuration

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Configuration Parameters

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | Client ID from identity provider | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | Client secret from identity provider | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | Callback URL after authentication | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | OIDC configuration endpoint | `https://login.microsoftonline.com/...` |

!!! warning "Important"

    Αντικαταστήστε τις τιμές placeholder (`<client_id>`, `<client_secret>`, `<tenant_id>`) με τα πραγματικά διαπιστευτήρια από το developer portal του παρόχου ταυτότητας.

### Redirect URI

Το redirect URI πρέπει να είναι το ίδιο με αυτό που έχετε καταχωρήσει στις ρυθμίσεις του παρόχου ταυτότητας:

```
http://localhost:5173/oidc/callback
```

Αν το digna φιλοξενείται σε διαφορετικό domain, ενημερώστε αναλόγως:
- Local: `http://localhost:5173/oidc/callback`
- Production: `https://digna.yourdomain.com/oidc/callback`

### Complete Example

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

## Testing Login {: #testing-login }

Μετά την ολοκλήρωση της διαμόρφωσης, επαληθεύστε ότι το SSO λειτουργεί σωστά.

### Pre-Testing Checklist

Πριν τις δοκιμές, βεβαιωθείτε ότι:

- [ ] Το `dashboard_config.toml` έχει ενημερωθεί με τους OIDC παρόχους
- [ ] Το `config.toml` έχει ενημερωθεί με τα OIDC διαπιστευτήρια
- [ ] Και τα δύο αρχεία έχουν αποθηκευτεί
- [ ] Τα διαπιστευτήρια είναι σωστά (client ID, client secret)
- [ ] Το Redirect URI ταιριάζει με το URL της ανάπτυξής σας
- [ ] Η εφαρμογή στον πάροχο ταυτότητας είναι διαμορφωμένη με το redirect URI

### Testing Steps

#### Step 1: Restart Services

Επανεκκινήστε το backend και τον web server του digna για να εφαρμοστούν οι αλλαγές.

**If running as Windows service:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**If running manually:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**If using IIS or Tomcat:**
Επανεκκινήστε την υπηρεσία του web server σας.

#### Step 2: Open Dashboard

Ανοίξτε το dashboard του digna στον περιηγητή σας:

```
http://localhost:5173
```

(ή το ρυθμισμένο URL του dashboard)

#### Step 3: Verify Login Buttons

Ελέγξτε ότι τα κουμπιά σύνδεσης εμφανίζονται για κάθε ρυθμισμένο πάροχο:

- Πρέπει να εμφανίζεται το κουμπί "Login with Microsoft"
- Πρέπει να εμφανίζεται το κουμπί "Login with Google"
- (Αν `usePassword = true`) Πρέπει να εμφανίζονται πεδία username/password

Αν τα κουμπιά δεν εμφανίζονται:
- Ελέγξτε ότι το `dashboard_config.toml` αποθηκεύτηκε
- Ελέγξτε ότι η υπηρεσία του dashboard επανεκκινήθηκε
- Δείτε την κονσόλα του περιηγητή (F12) για σφάλματα

#### Step 4: Test SSO Login

Κάντε κλικ σε ένα από τα κουμπιά SSO (π.χ. "Login with Microsoft"):

1. Θα πρέπει να ανακατευθυνθείτε στη σελίδα σύνδεσης του παρόχου ταυτότητας
2. Συνδεθείτε με τα εταιρικά σας διαπιστευτήρια
3. Θα πρέπει να ανακατευθυνθείτε πίσω στο digna
4. Θα πρέπει να έχετε συνδεθεί στο digna

#### Step 5: Verify User Creation

Μετά από επιτυχή SSO σύνδεση:

- Ο χρήστης θα πρέπει να δημιουργείται αυτόματα στο digna
- Ο χρήστης θα πρέπει να είναι συνδεδεμένος
- Το προφίλ του χρήστη θα εμφανίζει τα στοιχεία από τον πάροχο ταυτότητας
- Θα πρέπει να βλέπετε το dashboard του digna

#### Step 6: Test Password Login (If Enabled)

Αν `usePassword = true`:

1. Αποσυνδεθείτε από το digna
2. Στη σελίδα σύνδεσης, εισαγάγετε username και password
3. Θα πρέπει να μπορείτε να συνδεθείτε με τα διαπιστευτήρια κωδικού

---

## Troubleshooting {: #troubleshooting }

### Login Buttons Don't Appear

**Symptoms:**
- Τα κουμπιά OIDC δεν εμφανίζονται στη σελίδα σύνδεσης
- Βλέπετε μόνο πεδία κωδικού (αν `usePassword = true`)

**Causes & Solutions:**
1. Ελέγξτε ότι το `dashboard_config.toml` βρίσκεται στον κατάλογο `dashboard/`
2. Επιβεβαιώστε ότι οι ενότητες `[[login.oidc]]` υπάρχουν με σωστή σύνταξη
3. Επανεκκινήστε την υπηρεσία του dashboard
4. Καθαρίστε την cache του περιηγητή (Ctrl+Shift+Delete ή Cmd+Shift+Delete)
5. Ελέγξτε την κονσόλα του περιηγητή (F12 → Console) για σφάλματα

---

### Redirect URI Mismatch Error

**Symptoms:**
- Μετά το κλικ στο κουμπί SSO, εμφανίζεται σφάλμα για "redirect_uri mismatch"
- Σφάλμα "The redirect URI is not registered"

**Causes & Solutions:**
1. Επαληθεύστε ότι το `DIGNA_OIDC_REDIRECT_URI` στο `config.toml` είναι σωστό
2. Επαληθεύστε ότι το redirect URI είναι καταχωρημένο στις ρυθμίσεις του παρόχου ταυτότητας
3. Βεβαιωθείτε ότι και τα δύο χρησιμοποιούν ακριβώς το ίδιο URL (συμπεριλαμβανομένου πρωτοκόλλου, domain, path)
4. Ελέγξτε για ορθογραφικά λάθη στο redirect URI
5. Αν χρησιμοποιείτε HTTPS, βεβαιωθείτε ότι το πιστοποιητικό είναι έγκυρο

---

### Invalid Client Credentials Error

**Symptoms:**
- Σφάλμα "Invalid client ID or secret"
- Η αυθεντικοποίηση αποτυγχάνει με σφάλμα διαπιστευτηρίων

**Causes & Solutions:**
1. Επαληθεύστε ότι το `DIGNA_OIDC_CLIENT_ID` και το `DIGNA_OIDC_CLIENT_SECRET` είναι σωστά
2. Βεβαιωθείτε ότι δεν υπάρχουν επιπλέον κενά ή μη επιθυμητοί χαρακτήρες
3. Ελέγξτε ότι τα διαπιστευτήρια δεν έχουν λήξει ή ανακληθεί
4. Επανεκκινήστε την υπηρεσία backend μετά την ενημέρωση της διαμόρφωσης
5. Ελέγξτε την κονσόλα του παρόχου ταυτότητας για να επιβεβαιώσετε ότι τα διαπιστευτήρια είναι ενεργά

---

### Login Hangs or Times Out

**Symptoms:**
- Το κλικ στο κουμπί SSO δεν κάνει τίποτα
- Υπάρχει timeout μετά από μερικά δευτερόλεπτα
- Ο περιηγητής εμφανίζει "Failed to connect" ή παρόμοιο μήνυμα

**Causes & Solutions:**
1. Επαληθεύστε ότι το backend του digna τρέχει: `digna repo check`
2. Ελέγξτε τη συνδεσιμότητα δικτύου προς τον πάροχο ταυτότητας
3. Επαληθεύστε ότι η `DIGNA_OIDC_CONFIGURATION_URL` είναι προσβάσιμη
4. Ελέγξτε τους κανόνες firewall ώστε να επιτρέπονται εξερχόμενες HTTPS συνδέσεις
5. Επαληθεύστε ότι το backend και το dashboard μπορούν να επικοινωνήσουν μεταξύ τους

---

### Users Not Automatically Created

**Symptoms:**
- Η SSO σύνδεση επιτυγχάνει αλλά ο χρήστης δεν δημιουργείται στο digna
- Λαμβάνετε σφάλμα δικαιωμάτων μετά την SSO σύνδεση

**Causes & Solutions:**
1. Επαληθεύστε ότι η OIDC διαμόρφωση είναι σωστή
2. Ελέγξτε ότι τα δικαιώματα χρηστών έχουν ρυθμιστεί σωστά
3. Ελέγξτε τα logs του digna για μηνύματα σφάλματος
4. Επανεκκινήστε την υπηρεσία backend
5. Επικοινωνήστε με support@digna.ai αν το ζήτημα επιμείνει

---

## Supported Providers {: #supported-providers }

### Tested & Supported

Οι παρακάτω OIDC πάροχοι έχουν δοκιμαστεί και είναι γνωστό ότι λειτουργούν:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Τεκμηρίωση Microsoft](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Τεκμηρίωση Google](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Τεκμηρίωση Okta](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Other OIDC Providers

Οποιοσδήποτε πάροχος που υποστηρίζει το OpenID Connect μπορεί να ενσωματωθεί. Απαιτούμενες πληροφορίες:

- Client ID
- Client secret
- OpenID configuration URL (συνήθως στο `/.well-known/openid-configuration`)
- Υποστηριζόμενα scopes (συνήθως `openid profile email`)

Επικοινωνήστε με support@digna.ai αν χρειάζεστε βοήθεια για την ενσωμάτωση κάποιου συγκεκριμένου παρόχου.

---

## Best Practices

**DO:**
- Χρησιμοποιείτε HTTPS στην παραγωγή (όχι HTTP)
- Αποθηκεύετε τα client secrets με ασφάλεια (χρησιμοποιήστε μεταβλητές περιβάλλοντος αν είναι δυνατό)
- Περιστρέφετε τα secrets περιοδικά
- Δοκιμάζετε πρώτα σε μη παραγωγικό περιβάλλον
- Τεκμηριώνετε ποιοι πάροχοι είναι ρυθμισμένοι
- Παρακολουθείτε τα logs σύνδεσης για ασυνήθιστη δραστηριότητα
- Κρατάτε τη διαμόρφωση του παρόχου ταυτότητας σε συγχρονισμό με τη διαμόρφωση του digna

**DON'T:**
- Αποθηκεύετε client secrets σε σύστημα ελέγχου έκδοσης
- Χρησιμοποιείτε HTTP redirect URIs στην παραγωγή
- Διαμορφώνετε πολλούς παρόχους με το ίδιο key
- Αφήνετε default/test διαπιστευτήρια στην παραγωγή
- Εκθέτετε αρχεία διαμόρφωσης που περιέχουν μυστικά
- Αναμειγνύετε αναπτυξιακά και παραγωγικά διαπιστευτήρια

---

## Support

Χρειάζεστε βοήθεια με τη διαμόρφωση SSO;

- **Email:** support@digna.ai
- **Documentation:** https://docs.digna.ai
- **Website:** https://www.digna.ai

---

**Last Updated:** August 30, 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**