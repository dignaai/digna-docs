# Ρύθμιση SSO με το Google Workspace

Η πλατφόρμα ταυτοποίησης της Google είναι συμβατή με OIDC και χρησιμοποιεί ένα κοινό, γνωστό discovery URL για κάθε πελάτη, οπότε οι μόνες τιμές ανά οργανισμό είναι το client ID και το secret.

Αυτός ο οδηγός καλύπτει την **πλευρά της Google**: τη δημιουργία του OAuth client και τη συλλογή των τιμών που χρειάζεται η digna. Η πλευρά της digna — `dashboard_config.toml`, testing και troubleshooting — είναι ίδια για κάθε provider και περιγράφεται στην [Επισκόπηση Single Sign-On](overview.md).

---

## Πριν Ξεκινήσετε

| Απαίτηση | Σημειώσεις |
|---|---|
| **Google Cloud project** | Οποιοδήποτε project στην ίδια οργάνωση με το Workspace domain σας |
| **Ρόλος** | Editor ή Owner στο project |
| **digna redirect URI** | Η διεύθυνση στην οποία επιστρέφει ο χρήστης μετά το login, π.χ. `https://digna.yourdomain.com/oidc/callback` |

---

## Βήμα 1: Διαμόρφωση της Οθόνης Συναίνεσης OAuth

Η Google δεν θα εκδώσει διαπιστευτήρια μέχρι να υπάρχει η οθόνη συναίνεσης.

1. Ανοίξτε το [Google Cloud Console](https://console.cloud.google.com) και επιλέξτε το project σας
2. Πηγαίνετε σε **APIs & Services → OAuth consent screen**
3. Επιλέξτε τον τύπο χρήστη:
   - **Internal** — μόνο λογαριασμοί στο Workspace domain σας μπορούν να συνδεθούν. Συνιστάται.
   - **External** — οποιοσδήποτε Google λογαριασμός μπορεί να επιχειρήσει είσοδο.
4. Συμπληρώστε το όνομα της εφαρμογής, το user support email και το developer contact email
5. Στο βήμα **Scopes**, προσθέστε `openid`, `.../auth/userinfo.email` και `.../auth/userinfo.profile`
6. Αποθηκεύστε

!!! warning "Οι Εξωτερικές Εφαρμογές Πρέπει Να Δημοσιευτούν"

    Μια οθόνη συναίνεσης **External** ξεκινά σε κατάσταση *Testing*, όπου μόνο οι λογαριασμοί που έχουν προστεθεί ρητά στη λίστα test-user μπορούν να ολοκληρώσουν μια είσοδο. Όλοι οι υπόλοιποι θα βλέπουν το μήνυμα "digna has not completed the Google verification process". Εναλλακτικά, θα πρέπει είτε να μεταβείτε την εφαρμογή σε **In production** κάτω από **Publishing status**, είτε να χρησιμοποιήσετε **Internal** — που δεν έχει αυτούς τους περιορισμούς και είναι η σωστή επιλογή για μια εγκατάσταση μόνο για Workspace.

---

## Βήμα 2: Δημιουργία του OAuth Client

1. Πηγαίνετε σε **APIs & Services → Credentials**
2. Κάντε κλικ στο **Create Credentials → OAuth client ID**
3. Ορίστε το **Application type** σε **Web application**
4. Δώστε ένα όνομα, π.χ. `digna`
5. Στην ενότητα **Authorized redirect URIs**, κάντε κλικ στο **Add URI** και εισάγετε:

```
https://digna.yourdomain.com/oidc/callback
```

6. Κάντε κλικ στο **Create**

!!! note "Δεν Απαιτούνται Authorized JavaScript Origins"

    Η digna ανταλλάσσει τον authorization code από το backend, όχι από το πρόγραμμα περιήγησης, οπότε το πεδίο **Authorized JavaScript origins** μπορεί να παραμείνει κενό. Μόνο το redirect URI έχει σημασία.

---

## Βήμα 3: Συλλογή των Διαπιστευτηρίων

Το παράθυρο διαλόγου που εμφανίζεται μετά τη δημιουργία δείχνει:

- **Client ID** — τελειώνει σε `.apps.googleusercontent.com` → γίνεται `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → γίνεται `DIGNA_OIDC_CLIENT_SECRET`

Και τα δύο παραμένουν ανακτήσιμα αργότερα από τη σελίδα λεπτομερειών των credentials, σε αντίθεση με τους περισσότερους άλλους providers.

---

## Βήμα 4: Το Discovery URL

Η Google χρησιμοποιεί ένα discovery URL για όλους τους πελάτες — δεν υπάρχει αντικατάσταση:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Βήμα 5: Διαμόρφωση digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

Το `key` και στα δύο αρχεία πρέπει να ταιριάζει — εδώ `google`.

---

## Βήμα 6: Δοκιμή

Επανεκκινήστε το backend και τον web server, στη συνέχεια ανοίξτε το dashboard. Δείτε την [Δοκιμή Σύνδεσης](overview.md#testing-login) για την πλήρη λίστα ελέγχου.

---

## Αντιμετώπιση Προβλημάτων με το Google Workspace

### Error 400: redirect_uri_mismatch

Το URI στο `DIGNA_OIDC_REDIRECT_URI` δεν περιλαμβάνεται στη λίστα **Authorized redirect URIs**, ή διαφέρει σε ένα τελικό slash ή στο scheme. Η σελίδα σφάλματος της Google εμφανίζει το URI που έλαβε — συγκρίνετέ το χαρακτήρα προς χαρακτήρα με το καταχωρημένο.

### This App Is Blocked / Has Not Completed Verification

Η οθόνη συναίνεσης είναι **External** και είναι ακόμα σε κατάσταση *Testing*. Δημοσιεύστε την, ή αλλάξτε την εφαρμογή σε **Internal**.

### Access Blocked: Authorization Error

Ο λογαριασμός που επιχειρεί να συνδεθεί βρίσκεται έξω από το Workspace domain σας ενώ η οθόνη συναίνεσης είναι **Internal**. Αυτή είναι η αναμενόμενη συμπεριφορά — οι Internal εφαρμογές αποδέχονται μόνο λογαριασμούς της οργάνωσης.

### Οι Αλλαγές Χρειάζονται Μερικά Λεπτά

Η Google διαδίδει τις αλλαγές σε credentials και στην οθόνη συναίνεσης ασύγχρονα. Ένα πρόσφατα προστιθέμενο redirect URI μπορεί να χρειαστεί λίγα λεπτά για να τεθεί σε ισχύ· αν μια αλλαγή φαίνεται να αγνοείται, περιμένετε και δοκιμάστε ξανά πριν προχωρήσετε σε περαιτέρω διερεύνηση.

---

## Δείτε επίσης

- [Επισκόπηση Single Sign-On](overview.md) — αναφορά διαμόρφωσης, testing και γενική αντιμετώπιση προβλημάτων
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)