# Ρύθμιση SSO με OneLogin

Η OneLogin συμμορφώνεται με OIDC. Το χαρακτηριστικό της είναι ότι ο τύπος του connector επιλέγεται από έναν κατάλογο κατά τη δημιουργία της εφαρμογής και δεν μπορεί να αλλάξει αργότερα.

Αυτός ο οδηγός καλύπτει την **πλευρά της OneLogin**: τη δημιουργία της εφαρμογής και τη συλλογή των τιμών που χρειάζεται το digna. Η πλευρά του digna — `dashboard_config.toml`, δοκιμές και αντιμετώπιση προβλημάτων — είναι η ίδια για κάθε πάροχο και περιγράφεται στην [Επισκόπηση Single Sign-On](overview.md).

---

## Πριν Ξεκινήσετε

| Απαίτηση | Σημειώσεις |
|---|---|
| **Ρόλος στην OneLogin** | Ιδιοκτήτης λογαριασμού ή διαχειριστής με δικαίωμα προσθήκης εφαρμογών |
| **Subdomain** | π.χ. `yourcompany.onelogin.com` |
| **digna redirect URI** | Το URL στο οποίο επιστρέφουν οι χρήστες μετά τη σύνδεση, π.χ. `https://digna.yourdomain.com/oidc/callback` |

---

## Βήμα 1: Δημιουργία της εφαρμογής OIDC

1. Συνδεθείτε στο OneLogin Admin portal
2. Μεταβείτε σε **Applications → Applications**
3. Κάντε κλικ στο **Add App**
4. Αναζητήστε `OpenId Connect` και επιλέξτε τον connector **OpenId Connect (OIDC)**
5. Ορίστε το **Display Name** σε `digna`
6. Κάντε κλικ στο **Save**

!!! warning "Ο Τύπος Connector Ορίζεται Κατά τη Δημιουργία"

    Η OneLogin έχει ξεχωριστές καταχωρίσεις καταλόγου για SAML και OIDC, και μια εφαρμογή δεν μπορεί να μετατραπεί από τη μία στην άλλη. Εάν επιλέξετε κατά λάθος έναν SAML connector, διαγράψτε την εφαρμογή και προσθέστε την ξανά — δεν υπάρχει ρύθμιση για αλλαγή πρωτοκόλλου.

---

## Βήμα 2: Διαμόρφωση του Redirect URI

1. Ανοίξτε την καρτέλα **Configuration**
2. Στο πεδίο **Redirect URI's**, εισάγετε το URL callback του digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. Προαιρετικά ορίστε τα **Post Logout Redirect URIs** στο URL του dashboard σας
4. Κάντε κλικ στο **Save**

!!! note "Ένα URI ανά Γραμμή"

    Σε αντίθεση με παρόχους που αναμένουν λίστα διαχωρισμένη με κόμμα, το πεδίο **Redirect URI's** της OneLogin δέχεται ένα URI ανά γραμμή.

---

## Βήμα 3: Ορίστε τον Τύπο Εφαρμογής και τη Μέθοδο Αυθεντικοποίησης

1. Ανοίξτε την καρτέλα **SSO**
2. Επιβεβαιώστε ότι το **Application Type** είναι *Web*
3. Ορίστε το **Token Endpoint → Authentication Method** σε *POST* (`client_secret_post`) ή *Basic* (`client_secret_basic`)

!!! warning "Μην Επιλέξετε 'None'"

    Ο ορισμός της μεθόδου αυθεντικοποίησης σε *None* κάνει την εφαρμογή δημόσιο client χωρίς secret, και η ανταλλαγή κώδικα στο backend του digna θα απορριφθεί. Είτε POST είτε Basic λειτουργεί.

---

## Βήμα 4: Συλλογή των Διαπιστευτηρίων

Ενώ βρίσκεστε στην καρτέλα **SSO**:

- **Client ID** → γίνεται `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → γίνεται `DIGNA_OIDC_CLIENT_SECRET` (κάντε κλικ στο **Show client secret**)

Η σελίδα δείχνει επίσης το **Issuer URL**, που επιβεβαιώνει το discovery URL στο επόμενο βήμα.

---

## Βήμα 5: Ανάθεση Χρηστών

1. Ανοίξτε την καρτέλα **Access**
2. Προσθέστε τους ρόλους ή τις ομάδες των μελών που επιτρέπεται να χρησιμοποιούν το digna
3. Κάντε κλικ στο **Save**

!!! note "Οι Μη Ανατεθειμένοι Χρήστες Απορρίπτονται Μετά τη Σύνδεση"

    Όπως συμβαίνει με τους περισσότερους παρόχους, η OneLogin αυθεντικοποιεί πρώτα τον χρήστη και ελέγχει στη συνέχεια τα δικαιώματα. Ένας μη ανατεθειμένος χρήστης συνδέεται με επιτυχία και στη συνέχεια απορρίπτεται, κάτι που φαίνεται ως σφάλμα του digna αντί για απόφαση πρόσβασης.

---

## Βήμα 6: Δημιουργία του Discovery URL

Αντικαταστήστε το subdomain της OneLogin:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Για παράδειγμα:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "/2 Είναι η Έκδοση του API"

    Η τρέχουσα υλοποίηση OIDC της OneLogin βρίσκεται κάτω από το `/oidc/2/`. Παλαιότερη τεκμηρίωση εμφανίζει `/oidc/` χωρίς έκδοση, που δείχνει την παρωχημένη πρώτη έκδοση. Ελέγξτε το **Issuer URL** στην καρτέλα SSO αν έχετε αμφιβολίες — το discovery URL είναι το issuer συν `/.well-known/openid-configuration`.

---

## Βήμα 7: Διαμόρφωση του digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Login with OneLogin"
```

### `config.toml`

```toml
[oidc.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

Το `key` και στα δύο αρχεία πρέπει να ταιριάζει — `onelogin` εδώ.

---

## Βήμα 8: Δοκιμή

Επανεκκινήστε το backend και τον web server, και στη συνέχεια ανοίξτε το dashboard. Δείτε την ενότητα [Δοκιμή Σύνδεσης](overview.md#testing-login) για την πλήρη λίστα ελέγχου.

---

## Αντιμετώπιση Προβλημάτων OneLogin

### redirect_uri δεν ταίριαξε

Το callback URL λείπει από τα **Configuration → Redirect URI's**, ή οι καταχωρίσεις χωρίστηκαν με κόμματα αντί για νέα γραμμή.

### invalid_client στο Βήμα Token

Το **Token Endpoint → Authentication Method** είναι ρυθμισμένο σε *None*, ή το client secret στο `config.toml` είναι παρωχημένο. Αποκρύψτε/εμφανίστε το secret στην καρτέλα **SSO** και συγκρίνετε.

### Η Εφαρμογή Δεν Εμφανίζεται στους Χρήστες

Δεν έχει δοθεί σε κανένα ρόλο ή ομάδα πρόσβαση στην καρτέλα **Access**.

### 404 στο Discovery URL

Το subdomain είναι λάθος, ή το URL παραλείπει το `/oidc/2/`. Συγκρίνετε με το **Issuer URL** που εμφανίζεται στην καρτέλα SSO.

---

## Δείτε Επίσης

- [Επισκόπηση Single Sign-On](overview.md) — αναφορά διαμόρφωσης, δοκιμές και γενική αντιμετώπιση προβλημάτων
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)