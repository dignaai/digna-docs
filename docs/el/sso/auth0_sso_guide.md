---
title: Auth0 SSO – Ενσωμάτωση Single Sign-On | τεκμηρίωση digna
description: Διαμορφώστε το Single Sign-On για το digna με Auth0 χρησιμοποιώντας OpenID Connect — ρύθμιση για regular web application, επιτρεπτά callback URLs, διαπιστευτήρια πελάτη, domain του tenant και η αντίστοιχη διαμόρφωση του digna.
image: /assets/logo_square.png
keywords: ενσωμάτωση digna sso, auth0 sso, auth0 oidc, regular web application, callback urls, openid connect, enterprise authentication
---

# Ρύθμιση SSO με Auth0

Το Auth0 συμμορφώνεται με OIDC και παρέχει ένα discovery endpoint ανά tenant. Το κύριο που πρέπει να προσέξετε είναι το tenant domain, το οποίο εμφανίζεται στο discovery URL και αλλάζει εάν ενεργοποιήσετε custom domain.

Αυτός ο οδηγός καλύπτει το **Auth0 μέρος**: τη δημιουργία της εφαρμογής και τη συλλογή των τιμών που χρειάζεται το digna. Το μέρος του digna — `dashboard_config.toml`, οι δοκιμές και η αντιμετώπιση προβλημάτων — είναι το ίδιο για κάθε πάροχο και περιγράφεται στο [Single Sign-On Overview](overview.md).

---

## Πριν Ξεκινήσετε

| Απαίτηση | Σημειώσεις |
|---|---|
| **Auth0 role** | Admin στο tenant |
| **Tenant domain** | π.χ. `yourcompany.eu.auth0.com` — το segment της περιοχής έχει σημασία |
| **digna redirect URI** | Το URL στο οποίο επιστρέφουν οι χρήστες μετά το login, π.χ. `https://digna.yourdomain.com/oidc/callback` |

---

## Βήμα 1: Δημιουργία της Εφαρμογής

1. Συνδεθείτε στον [Πίνακα ελέγχου Auth0](https://manage.auth0.com)
2. Μεταβείτε σε **Applications → Applications**
3. Κάντε κλικ στο **Create Application**
4. Ονομάστε την `digna` και επιλέξτε **Regular Web Applications**
5. Κάντε κλικ στο **Create**

!!! warning "Επιλέξτε Regular Web Applications"

    *Single Page Application* και *Native* δημιουργούν public clients χωρίς secret. Το digna εκτελεί την ανταλλαγή κώδικα από το backend του και χρειάζεται confidential client, οπότε **Regular Web Applications** είναι ο σωστός τύπος. Σε αντίθεση με κάποιους παρόχους, το Auth0 σας επιτρέπει να αλλάξετε τον τύπο αργότερα κάτω από **Settings → Application Type**.

---

## Βήμα 2: Προσθήκη του Callback URL

Στην καρτέλα **Settings** της εφαρμογής:

1. Εντοπίστε το **Allowed Callback URLs**
2. Εισάγετε το digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Προαιρετικά ορίστε τα **Allowed Logout URLs** στο URL του dashboard σας
4. Κάντε κύλιση στο κάτω μέρος και πατήστε **Save Changes**

!!! note "Κόμμα-χωρισμένα, όχι newline-χωρισμένα"

    Το Auth0 δέχεται πολλαπλά callback URLs σε αυτό το πεδίο, χωρισμένα με κόμματα. Μια λίστα χωρισμένη μόνο με newlines θεωρείται ένα λάθος URL και δεν ταιριάζει σιωπηλά με τίποτα.

---

## Βήμα 3: Συλλογή των Διαπιστευτηρίων

Ακόμη στην καρτέλα **Settings**, στον πίνακα **Basic Information**:

- **Domain** → πηγαίνει στο discovery URL
- **Client ID** → γίνεται `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → γίνεται `DIGNA_OIDC_CLIENT_SECRET` (κάντε κλικ για να το εμφανίσετε)

---

## Βήμα 4: Επιβεβαίωση του Grant Type

1. Μεταβείτε σε **Settings → Advanced Settings → Grant Types**
2. Επιβεβαιώστε ότι το **Authorization Code** είναι επιλεγμένο

Είναι ενεργοποιημένο εξ ορισμού για Regular Web Applications. Αν έχει απεπιλεγεί, το login του digna αποτυγχάνει με `unauthorized_client`.

---

## Βήμα 5: Δημιουργία της Discovery URL

Αντικαταστήστε το **Domain** από το Βήμα 3:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Για παράδειγμα:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Τα Custom Domains αλλάζουν τον Issuer"

    Εάν ο tenant σας χρησιμοποιεί custom domain όπως `login.yourcompany.com`, χρησιμοποιήστε εκείνο το domain στο discovery URL. Ο συνδυασμός — το canonical domain στο discovery URL και το custom στο browser — δημιουργεί mismatch του issuer, και το token απορρίπτεται μετά από ένα επιτυχημένο login.

---

## Βήμα 6: Διαμόρφωση digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Login with Auth0"
```

### `config.toml`

```toml
[oidc.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

Το `key` και στα δύο αρχεία πρέπει να ταιριάζει — εδώ `auth0`.

---

## Βήμα 7: Δοκιμή

Επανεκκινήστε το backend και τον web server, και μετά ανοίξτε το dashboard. Δείτε το [Testing Login](overview.md#testing-login) για την πλήρη λίστα ελέγχου.

---

## Επίλυση Προβλημάτων Auth0

### Mismatch στο Callback URL

Η σελίδα σφάλματος του Auth0 εμφανίζει το URL που έλαβε. Προσθέστε το στα **Allowed Callback URLs**, ελέγχοντας ότι οι καταχωρήσεις είναι χωρισμένες με κόμματα.

### unauthorized_client

Το **Authorization Code** δεν είναι ενεργοποιημένο κάτω από **Advanced Settings → Grant Types**, ή ο τύπος της εφαρμογής δεν είναι Regular Web Applications.

### Access Denied μετά από Επιτυχημένο Login

Κανόνας (Rule), Action ή Post-Login trigger στον tenant απορρίπτει τον χρήστη. Ελέγξτε **Actions → Flows → Login** και τα logs του tenant κάτω από **Monitoring → Logs**, που δείχνουν τον ακριβή λόγο.

### Issuer Mismatch

Το discovery URL και το domain στο οποίο στάλθηκε ο browser διαφέρουν — συνήθως το canonical tenant domain έναντι ενός custom domain. Χρησιμοποιήστε το ίδιο domain συνεπώς.

---

## Δείτε επίσης

- [Single Sign-On Overview](overview.md) — αναφορά ρυθμίσεων, δοκιμές και γενική αντιμετώπιση προβλημάτων
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)