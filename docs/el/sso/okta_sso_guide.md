---
title: Okta SSO – Ενσωμάτωση Single Sign-On | Τεκμηρίωση digna
description: Διαμορφώστε το Single Sign-On για το digna με το Okta χρησιμοποιώντας OpenID Connect — ενσωμάτωση εφαρμογής, URI ανακατεύθυνσης σύνδεσης, διαπιστευτήρια πελάτη, επιλογή authorization server και η αντίστοιχη ρύθμιση του digna.
image: /assets/logo_square.png
keywords: digna sso, okta sso, okta oidc, ενσωμάτωση εφαρμογής, authorization server, openid connect, enterprise authentication
---

# Ρύθμιση SSO με το Okta

Το Okta συμμορφώνεται με OIDC, με μια ιδιαιτερότητα που συναντούν οι περισσότερες πρώτες ενσωματώσεις: ένα Okta org εκθέτει περισσότερους από έναν authorization servers, και ο καθένας έχει το δικό του discovery URL.

Αυτός ο οδηγός καλύπτει την **πλευρά του Okta**: τη δημιουργία της ενσωμάτωσης εφαρμογής και τη συλλογή των τιμών που χρειάζεται το digna. Η πλευρά του digna — `dashboard_config.toml`, δοκιμές και αντιμετώπιση προβλημάτων — είναι ίδια για κάθε πάροχο και περιγράφεται στην [Επισκόπηση Single Sign-On](overview.md).

---

## Πριν Ξεκινήσετε

| Απαίτηση | Σημειώσεις |
|---|---|
| **Okta role** | Super Administrator, ή ρόλος διαχειριστή με δικαίωμα δημιουργίας ενσωματώσεων εφαρμογών |
| **Okta domain** | π.χ. `yourcompany.okta.com`, ή ένα προσαρμοσμένο domain αν έχει διαμορφωθεί |
| **digna redirect URI** | Το URL στο οποίο επιστρέφουν οι χρήστες μετά την είσοδο, π.χ. `https://digna.yourdomain.com/oidc/callback` |

---

## Βήμα 1: Δημιουργία της Ενσωμάτωσης Εφαρμογής

1. Συνδεθείτε στο Okta Admin Console
2. Μεταβείτε σε **Applications → Applications**
3. Κάντε κλικ στο **Create App Integration**
4. Επιλέξτε:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Κάντε κλικ στο **Next**

!!! warning "Ο Τύπος Εφαρμογής Δεν Μπορεί Να Αλλαχθεί"

    Επιλογή *Single-Page Application* αντί για *Web Application* δημιουργεί έναν public client χωρίς secret, και η ανταλλαγή κώδικα στο backend του digna θα αποτύχει με `invalid_client`. Ο τύπος ορίζεται κατά τη δημιουργία — λάθος επιλογή σημαίνει διαγραφή της εφαρμογής και νέα δημιουργία.

---

## Βήμα 2: Ρύθμιση της Ενσωμάτωσης

1. **App integration name**: `digna`
2. **Grant type**: αφήστε επιλεγμένο το *Authorization Code*
3. **Sign-in redirect URIs**: εισάγετε το callback URL του digna:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: προαιρετικό
5. Στην ενότητα **Assignments**, επιλέξτε ποιος μπορεί να χρησιμοποιήσει την ενσωμάτωση — μια συγκεκριμένη ομάδα είναι πιο ασφαλής από το *Allow everyone in your organization to access*
6. Κάντε κλικ στο **Save**

!!! note "Απαιτείται Εκχώρηση"

    Το Okta αυθεντικοποιεί τον χρήστη και μετά ελέγχει αν έχει εκχωρηθεί στην εφαρμογή. Ένας μη εκχωρημένος χρήστης φτάνει στη σελίδα εισόδου του Okta, συνδέεται επιτυχώς και απορρίπτεται κατά την ανακατεύθυνση πίσω. Αν η είσοδος δουλεύει για εσάς αλλά όχι για συναδέλφους, η εκχώρηση είναι το πρώτο που πρέπει να ελέγξετε.

---

## Βήμα 3: Συλλογή των Διαπιστευτηρίων

Στην καρτέλα **General** της εφαρμογής, κάτω από **Client Credentials**:

- **Client ID** → γίνεται `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → γίνεται `DIGNA_OIDC_CLIENT_SECRET` (κάντε κλικ στο εικονίδιο του ματιού για αποκάλυψη)

---

## Βήμα 4: Επιλογή του Authorization Server

Αυτό είναι το βήμα που καθορίζει το discovery URL. Μεταβείτε σε **Security → API** για να δείτε τους authorization servers στο org σας.

**Org authorization server** — εκδίδει tokens για το ίδιο το Okta org:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — συμπεριλαμβανομένου αυτού που δημιουργεί το Okta με το όνομα `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Για τον ενσωματωμένο server, το `<auth_server_id>` είναι κυριολεκτικά `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Ποιο;"

    Χρησιμοποιήστε τον **org** authorization server εκτός αν ο οργανισμός σας χρησιμοποιεί ήδη έναν custom για πολιτικές πρόσβασης API. Οι λογαριασμοί Okta Developer έχουν ως προεπιλογή το `default`; πολλοί οργανισμοί το απενεργοποιούν. Ανοίξτε και τα δύο URLs σε έναν browser — αυτό που επιστρέφει JSON αντί για σφάλμα είναι το διαθέσιμο για εσάς.

---

## Βήμα 5: Διαμόρφωση του digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

### `config.toml`

```toml
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

Το `key` και στα δύο αρχεία πρέπει να ταιριάζει — `okta` στην προκειμένη περίπτωση.

---

## Βήμα 6: Δοκιμή

Επανεκκινήστε το backend και τον web server, στη συνέχεια ανοίξτε το dashboard. Δείτε την [Δοκιμή Εισόδου](overview.md#testing-login) για την πλήρη λίστα ελέγχου.

---

## Αντιμετώπιση Προβλημάτων με το Okta

### Το redirect URI Δεν Είναι Καταχωρημένο

Το Okta εμφανίζει το προβληματικό URI στο σφάλμα. Συγκρίνετέ το με **General → Sign-in redirect URIs**; το Okta ταιριάζει την πλήρη συμβολοσειρά συμπεριλαμβανομένης οποιασδήποτε τελικής κάθετου (/).

### Ο Χρήστης Δεν Έχει Εκχωρηθεί στην Εφαρμογή Πελάτη

Ο λογαριασμός δεν βρίσκεται στη λίστα εκχώρησης της εφαρμογής. Προσθέστε τον χρήστη ή την ομάδα του στην ενότητα **Assignments**.

### 400 Bad Request: Invalid Authorization Server

Το `<auth_server_id>` στο discovery URL δεν υπάρχει, συχνά γιατί το `default` έχει αφαιρεθεί από ένα org. Ελέγξτε **Security → API** για τους servers που είναι πραγματικά διαθέσιμοι.

### invalid_client στο Βήμα του Token

Η ενσωμάτωση δημιουργήθηκε ως Single-Page Application και δεν έχει client secret. Δημιουργήστε ξανά την ενσωμάτωση ως Web Application.

---

## Δείτε Επίσης

- [Επισκόπηση Single Sign-On](overview.md) — αναφορά ρυθμίσεων, δοκιμών και γενικής αντιμετώπισης προβλημάτων
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)