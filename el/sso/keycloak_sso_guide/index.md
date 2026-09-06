# Ρύθμιση SSO με Keycloak

Το Keycloak είναι ένας αυτο-φιλοξενούμενος (self-hosted), πλήρως συμβατός με OIDC παροχέας ταυτότητας. Δεδομένου ότι το διαχειρίζεστε εσείς, το discovery URL σχηματίζεται από το δικό σας host name και realm αντί για domain τρίτου.

Αυτός ο οδηγός καλύπτει την **πλευρά του Keycloak**: τη δημιουργία του client και τη συλλογή των τιμών που χρειάζεται το digna. Η πλευρά του digna — `dashboard_config.toml`, δοκιμές και αντιμετώπιση προβλημάτων — είναι ίδια για κάθε πάροχο και περιγράφεται στην [Επισκόπηση Single Sign-On](overview.md).

---

## Πριν Ξεκινήσετε

| Απαίτηση | Σημειώσεις |
|---|---|
| **Keycloak version** | 17 ή νεότερη για τα URL paths που χρησιμοποιούνται εδώ — δείτε τη σημείωση στο Βήμα 4 |
| **Keycloak role** | `realm-admin` στο στοχευόμενο realm, ή διαχειριστής του server |
| **Realm** | Το realm στο οποίο ανήκουν οι χρήστες του digna, όχι απαραίτητα το `master` |
| **digna redirect URI** | Το URL στο οποίο επιστρέφουν οι χρήστες μετά την είσοδο, π.χ. `https://digna.yourdomain.com/oidc/callback` |

---

## Βήμα 1: Επιλέξτε το Realm

1. Ανοίξτε το Keycloak admin console  
2. Χρησιμοποιήστε τον επιλογέα realm επάνω-αριστερά για να αλλάξετε στο realm όπου βρίσκονται οι χρήστες σας

!!! warning "Μην χρησιμοποιείτε το realm master"

    Το `master` realm προορίζεται για τη διαχείριση του ίδιου του Keycloak. Οι εφαρμογές και οι clients πρέπει να τοποθετούνται σε ένα αφιερωμένο realm· βάζοντας το digna στο `master` δίνει στους χρήστες του πρόσβαση στην κονσόλα διαχείρισης του Keycloak.

---

## Βήμα 2: Δημιουργήστε το Client

1. Μεταβείτε σε **Clients** και πατήστε **Create client**
2. Διαμορφώστε:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — αυτό γίνεται `DIGNA_OIDC_CLIENT_ID`
3. Κάντε κλικ στο **Next**
4. Στο βήμα **Capability config**, ενεργοποιήστε το **Client authentication** **On**
5. Αφήστε το **Standard flow** ενεργοποιημένο· οι άλλες ροές δεν χρειάζονται
6. Κάντε κλικ στο **Next**

!!! warning "Το Client Authentication πρέπει να είναι On"

    Αν το **Client authentication** είναι απενεργοποιημένο, το Keycloak δημιουργεί έναν *public* client, που δεν έχει καθόλου credentials — η καρτέλα **Credentials** στο Βήμα 4 δεν θα υπάρχει. Το digna χρειάζεται confidential client. Αυτό το toggle μπορεί να αλλάξει μετά τη δημιουργία αν γίνει λάθος.

---

## Βήμα 3: Ορίστε το Redirect URI

Στο βήμα **Login settings** (ή στην καρτέλα **Settings** αργότερα):

1. **Valid redirect URIs**: εισάγετε το URL callback του digna:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: αφήστε το κενό, ή ορίστε `+` για να αντικατοπτρίζει τα redirect URIs
3. Κάντε κλικ στο **Save**

!!! tip "Αποφύγετε τα Wildcards"

    Το Keycloak δέχεται μοτίβα όπως `https://digna.yourdomain.com/*`. Ένα wildcard επιτρέπει σε οποιοδήποτε path σε αυτόν τον host να λάβει authorization code, οπότε προτιμήστε το ακριβές callback URL.

---

## Βήμα 4: Συλλέξτε το Client Secret

1. Ανοίξτε την καρτέλα **Credentials**
2. Επιβεβαιώστε ότι το **Client Authenticator** είναι *Client Id and Secret*
3. Αντιγράψτε το **Client secret** → γίνεται `DIGNA_OIDC_CLIENT_SECRET`

Το secret παραμένει ανακτήσιμο εδώ και μπορεί να ανανεωθεί με **Regenerate**.

---

## Βήμα 5: Δημιουργήστε το Discovery URL

Αντικαταστήστε το Keycloak host και το όνομα realm:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Για παράδειγμα:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Το Keycloak 16 και παλαιότερα περιλαμβάνουν /auth"

    Πριν από το Keycloak 17, κάθε endpoint βρισκόταν κάτω από το πρόθεμα `/auth`:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Διανομές που ρυθμίζουν `KC_HTTP_RELATIVE_PATH=/auth` διατηρούν τη παλιά διάταξη και σε τρέχουσες εκδόσεις. Αν το URL χωρίς `/auth` επιστρέφει 404, δοκιμάστε το με.

Ανοίξτε το URL σε έναν browser πριν συνεχίσετε. Ένα έγγραφο JSON επιβεβαιώνει ότι το host και το realm είναι σωστά.

---

## Βήμα 6: Ρυθμίστε το digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Σύνδεση με Keycloak"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

Το `key` και στα δύο αρχεία πρέπει να ταιριάζει — `keycloak` εδώ. Σημειώστε ότι δεν χρειάζεται να είναι ίδιο με το Keycloak **Client ID**, αν και το να τα κρατήσετε ίδια είναι πιο εύκολο για να ακολουθείτε.

---

## Βήμα 7: Δοκιμή

Επανεκκινήστε το backend και τον web server, και μετά ανοίξτε το dashboard. Δείτε τη [Δοκιμή Σύνδεσης](overview.md#testing-login) για την πλήρη λίστα ελέγχου.

---

## Αντιμετώπιση Προβλημάτων Keycloak

### Invalid parameter: redirect_uri

Το callback URL δεν καλύπτεται από τα **Valid redirect URIs**. Το Keycloak καταγράφει το URI που έλαβε στο server log, το οποίο είναι ο γρηγορότερος τρόπος να δείτε την ακριβή ασυμφωνία.

### Η καρτέλα Credentials λείπει

Ο client είναι public. Ενεργοποιήστε το **Client authentication** κάτω από **Settings → Capability config**.

### 404 στο Discovery URL

Είτε το όνομα realm είναι λάθος, είτε η εγκατάσταση χρησιμοποιεί το πρόθεμα `/auth`. Ελέγξτε τη λίστα realm στην admin console και δοκιμάστε και τις δύο μορφές του URL.

### unauthorized_client ή invalid_client

Το **Standard flow** είναι απενεργοποιημένο κάτω από **Capability config**, ή το secret ανανεώθηκε στο Keycloak χωρίς να ενημερωθεί το `config.toml`.

### Σφάλματα Πιστοποιητικού από το Backend

Ένα αυτο-φιλοξενούμενο Keycloak με ιδιωτικό ή self-signed πιστοποιητικό θα αποτύχει στο outbound HTTPS call του digna προς το discovery URL. Εγκαταστήστε την CA που εξέδωσε το πιστοποιητικό στο trust store της μηχανής που τρέχει το backend του digna.

---

## Δείτε Επίσης

- [Επισκόπηση Single Sign-On](overview.md) — αναφορά ρυθμίσεων, δοκιμών και γενικής αντιμετώπισης προβλημάτων
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)