---
title: PingOne SSO – Ενσωμάτωση Single Sign-On | Τεκμηρίωση digna
description: Ρυθμίστε το Single Sign-On για το digna με το PingOne χρησιμοποιώντας OpenID Connect — ρύθμιση εφαρμογής OIDC web, redirect URIs, client credentials, environment ID, περιφερειακοί τομείς και η αντίστοιχη ρύθμιση στο digna.
image: /assets/logo_square.png
keywords: digna sso, pingone sso, ping identity, pingone oidc, environment id, OpenID Connect, εταιρική αυθεντικοποίηση
---

# Ρύθμιση SSO με το PingOne

Το PingOne είναι συμβατό με OIDC. Δύο από τις τιμές του χρειάζονται προσοχή: το **Environment ID**, που εμφανίζεται σε κάθε URL endpoint, και ο **περιφερειακός τομέας**, που διαφέρει μεταξύ των tenants της Βόρειας Αμερικής, Ευρώπης, Καναδά, Ασίας-Ειρηνικού και Αυστραλίας.

Αυτός ο οδηγός καλύπτει την **πλευρά του PingOne**: τη δημιουργία της εφαρμογής και τη συλλογή των τιμών που χρειάζεται το digna. Η πλευρά του digna — `dashboard_config.toml`, δοκιμές και αντιμετώπιση προβλημάτων — είναι η ίδια για κάθε πάροχο και περιγράφεται στην [Single Sign-On Overview](overview.md).

---

## Προτού Ξεκινήσετε

| Απαίτηση | Σημειώσεις |
|---|---|
| **Ρόλος στο PingOne** | Environment Admin ή Identity Data Admin στο στοχευόμενο περιβάλλον |
| **Περιβάλλον** | Το περιβάλλον PingOne στο οποίο ανήκουν οι χρήστες του digna |
| **digna redirect URI** | Το URL στο οποίο επιστρέφουν οι χρήστες μετά το login, π.χ. `https://digna.yourdomain.com/oidc/callback` |

---

## Βήμα 1: Δημιουργία της Εφαρμογής

1. Συνδεθείτε στο PingOne admin console και επιλέξτε το περιβάλλον σας
2. Μεταβείτε σε **Applications → Applications**
3. Κάντε κλικ στο πλήκτρο **+**
4. Εισαγάγετε `digna` ως **Application Name**
5. Επιλέξτε **OIDC Web App**
6. Κλικ στο **Save**

!!! warning "Επιλέξτε OIDC Web App, όχι Single-Page App"

    Τα *Single-Page App* και *Native App* δημιουργούν public clients που δεν μπορούν να διατηρήσουν secret. Το digna ανταλλάσσει τον authorization code από το backend του και χρειάζεται τον εμπιστευτικό τύπο **OIDC Web App**.

---

## Βήμα 2: Διαμόρφωση του Redirect URI

1. Ανοίξτε την καρτέλα **Configuration** της εφαρμογής
2. Κάντε κλικ στο εικονίδιο του μολυβιού για επεξεργασία
3. Επιβεβαιώστε ότι το **Response Type** είναι *Code* και το **Grant Type** είναι *Authorization Code*
4. Στην ενότητα **Redirect URIs**, εισάγετε το callback URL του digna:

```
https://digna.yourdomain.com/oidc/callback
```

5. Ορίστε το **Token Endpoint Authentication Method** σε *Client Secret Post* ή *Client Secret Basic*
6. Κλικ στο **Save**

---

## Βήμα 3: Ενεργοποιήστε την Εφαρμογή

Στη σειρά ή στο πάνελ λεπτομερειών της εφαρμογής, μεταβείτε το toggle σε **enabled**.

!!! warning "Οι νέες εφαρμογές ξεκινούν απενεργοποιημένες"

    Το PingOne δημιουργεί τις εφαρμογές σε κατάσταση απενεργοποίησης. Μια απενεργοποιημένη εφαρμογή προκαλεί σφάλμα στο βήμα εξουσιοδότησης που δεν αναφέρει το toggle, οπότε αξίζει να το επιβεβαιώσετε πριν την περαιτέρω αντιμετώπιση προβλημάτων.

---

## Βήμα 4: Χορήγηση των Scopes

1. Ανοίξτε την καρτέλα **Resources**
2. Επιβεβαιώστε ότι το `openid` είναι χορηγημένο, και προσθέστε τα `profile` και `email` από το resource **OpenID Connect**
3. Κλικ στο **Save**

---

## Βήμα 5: Ανάθεση Χρηστών

1. Ανοίξτε την καρτέλα **Access**
2. Προσθέστε το population ή τις ομάδες των μελών που μπορούν να χρησιμοποιήσουν το digna
3. Κλικ στο **Save**

---

## Βήμα 6: Συλλογή των Credentials και του Environment ID

Στην καρτέλα **Configuration**, αναπτύξτε την ενότητα **General**:

- **Client ID** → γίνεται `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → γίνεται `DIGNA_OIDC_CLIENT_SECRET` (κάντε κλικ στο εικονίδιο του ματιού)
- **Environment ID** → χρησιμοποιείται στο discovery URL

Η ίδια καρτέλα εμφανίζει το έτοιμο **OIDC Discovery Endpoint**, το οποίο μπορείτε να αντιγράψετε απευθείας αντί να το συναρμολογήσετε χειροκίνητα.

---

## Βήμα 7: Δημιουργία του Discovery URL

Αντικαταστήστε το environment ID και τον τομέα για την περιοχή σας:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Περιοχή | Τομέας |
|---|---|
| Βόρεια Αμερική | `auth.pingone.com` |
| Ευρώπη | `auth.pingone.eu` |
| Καναδάς | `auth.pingone.ca` |
| Ασία-Ειρηνικός | `auth.pingone.asia` |
| Αυστραλία | `auth.pingone.com.au` |

Για ένα ευρωπαϊκό περιβάλλον:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Αντιγράψτε το αντί να το πληκτρολογήσετε"

    Ο περιφερειακός τομέας είναι το πιο συνηθισμένο λάθος σε μια ενσωμάτωση PingOne, και μια λάθος περιοχή δίνει 404 αντί για ένα χρήσιμο μήνυμα. Χρησιμοποιήστε την τιμή **OIDC Discovery Endpoint** από το Βήμα 6.

---

## Βήμα 8: Ρύθμιση του digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Login with PingOne"
```

### `config.toml`

```toml
[oidc.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

Το `key` και στα δύο αρχεία πρέπει να ταιριάζει — `pingone` εδώ.

---

## Βήμα 9: Δοκιμή

Επανεκκινήστε το backend και τον web server, στη συνέχεια ανοίξτε το dashboard. Δείτε την [Testing Login](overview.md#testing-login) για την πλήρη λίστα ελέγχου.

---

## Αντιμετώπιση Προβλημάτων με το PingOne

### 404 στο Discovery URL

Ο περιφερειακός τομέας ή το Environment ID είναι λάθος. Συγκρίνετε με το **OIDC Discovery Endpoint** που εμφανίζεται στην καρτέλα Configuration της εφαρμογής.

### NOT_FOUND ή Εφαρμογή Απενεργοποιημένη

Το toggle της εφαρμογής από το Βήμα 3 είναι ακόμα απενεργοποιημένο.

### Redirect URI Mismatch

Το PingOne ταιριάζει ολόκληρο το string. Ελέγξτε **Configuration → Redirect URIs** για τυχόν τελικό slash ή διαφορά στο scheme.

### Το Login Επιτυγχάνει αλλά δεν Φτάνει το Email Claim στο digna

Τα scopes `email` και `profile` δεν έχουν χορηγηθεί στην καρτέλα **Resources**.

### Ο Χρήστης Δεν Βλέπει την Εφαρμογή

Καμία πληθυσμιακή ομάδα ή ομάδα δεν έχει λάβει πρόσβαση στην καρτέλα **Access**.

---

## Δείτε επίσης

- [Single Sign-On Overview](overview.md) — αναφορά ρυθμίσεων, δοκιμών και γενικής αντιμετώπισης προβλημάτων
- [PingOne: Διαμόρφωση εφαρμογής OIDC](https://docs.pingidentity.com/pingone/)