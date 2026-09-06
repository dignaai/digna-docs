# Ρύθμιση SSO με Microsoft Entra ID

Το Microsoft Entra ID (πρώην Azure Active Directory) είναι πλήρως συμβατό με OIDC, οπότε το digna ενσωματώνεται μέσω του τυπικού discovery endpoint.

Αυτός ο οδηγός καλύπτει την **πλευρά του Entra ID**: την εγγραφή της εφαρμογής και τη συλλογή των τεσσάρων τιμών που χρειάζεται το digna. Η πλευρά του digna — `dashboard_config.toml`, δοκιμές και αντιμετώπιση προβλημάτων — είναι ίδια για κάθε πάροχο και περιγράφεται στην [Επισκόπηση Single Sign-On](overview.md).

---

## Πριν Ξεκινήσετε

| Απαίτηση | Σημειώσεις |
|---|---|
| **Ρόλος στο Entra ID** | Application Administrator, Cloud Application Administrator, ή Global Administrator |
| **digna redirect URI** | Η διεύθυνση στην οποία επιστρέφουν οι χρήστες μετά τη σύνδεση, π.χ. `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | Ο κατάλογος στον οποίο συνδέονται οι χρήστες σας |

---

## Βήμα 1: Εγγραφή της Εφαρμογής

1. Συνδεθείτε στο [Microsoft Entra admin center](https://entra.microsoft.com)
2. Πηγαίνετε σε **Identity → Applications → App registrations**
3. Κάντε κλικ στο **New registration**
4. Ρυθμίστε:
   - **Name**: `digna` (εμφανίζεται στους χρήστες στην οθόνη συγκατάθεσης)
   - **Supported account types**: *Accounts in this organizational directory only* για εγκατάσταση single-tenant
5. Στην ενότητα **Redirect URI**, επιλέξτε πλατφόρμα **Web** και εισάγετε το callback URL του digna:

```
https://digna.yourdomain.com/oidc/callback
```

6. Κάντε κλικ στο **Register**

!!! warning "Σημαντικό"

    Η πλατφόρμα πρέπει να είναι **Web**, όχι *Single-page application*. Το digna ανταλλάσσει τον authorization code από το backend χρησιμοποιώντας client secret, κάτι που ο τύπος πλατφόρμας SPA δεν επιτρέπει.

---

## Βήμα 2: Αντιγραφή των Client και Tenant IDs

Στη σελίδα **Overview** της εφαρμογής, αντιγράψτε:

- **Application (client) ID** → γίνεται `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → μπαίνει στο discovery URL

---

## Βήμα 3: Δημιουργία Client Secret

1. Πηγαίνετε σε **Certificates & secrets → Client secrets**
2. Κάντε κλικ στο **New client secret**
3. Εισάγετε μια περιγραφή και επιλέξτε λήξη
4. Κάντε κλικ στο **Add**
5. Αντιγράψτε αμέσως τη στήλη **Value**

!!! warning "Αντιγράψτε την Value, όχι το Secret ID"

    Η **Value** εμφανίζεται μόνο μία φορά, σε αυτή τη σελίδα, και δεν μπορεί να ανακτηθεί αργότερα. Το **Secret ID** δίπλα της μοιάζει παρόμοιο αλλά δεν είναι το secret — η χρήση του προκαλεί σφάλμα `invalid_client` κατά τη σύνδεση. Αν φύγετε από τη σελίδα πριν την αντιγραφή, διαγράψτε το secret και δημιουργήστε καινούργιο.

!!! tip "Συμβουλή"

    Το Entra ID περιορίζει τη διάρκεια ζωής των secret στα 24 μήνες, οπότε κάθε ενσωμάτωση SSO έχει ημερομηνία λήξης. Σημειώστε την κάπου όπου θα τη δείτε — ένα ληγμένο secret διακόπτει το SSO για όλους τους χρήστες ταυτόχρονα, χωρίς προειδοποίηση στη σελίδα σύνδεσης.

---

## Βήμα 4: Επιβεβαίωση Δικαιωμάτων API

1. Πηγαίνετε σε **API permissions**
2. Επιβεβαιώστε ότι υπάρχει **Microsoft Graph → User.Read** (delegated) — προστίθεται από προεπιλογή

Τα scopes `openid`, `profile` και `email` που ζητά το digna ανήκουν στο πρότυπο OIDC και δεν χρειάζονται ξεχωριστή έγκριση. Αν ο tenant σας απαιτεί admin consent για όλες τις εφαρμογές, κάντε κλικ στο **Grant admin consent for &lt;tenant&gt;**.

---

## Βήμα 5: Δημιουργία του Discovery URL

Αντικαταστήστε το **Directory (tenant) ID** από το Βήμα 2:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Χρησιμοποιήστε το v2.0 Endpoint"

    Το τμήμα `/v2.0/` είναι σημαντικό. Το v1.0 endpoint στο `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` εκδίδει tokens σε παλαιότερο format και δεν επιστρέφει τα πρότυπα claims OIDC που περιμένει το digna.

Ανοίξτε το URL σε έναν browser πριν συνεχίσετε. Ένα JSON έγγραφο επιβεβαιώνει ότι το tenant ID είναι σωστό.

---

## Βήμα 6: Ρύθμιση του digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"
```

### `config.toml`

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

Το `key` και στα δύο αρχεία πρέπει να ταιριάζει — εδώ `microsoft`.

---

## Βήμα 7: Δοκιμή

Κάντε επανεκκίνηση του backend και του web server, και μετά ανοίξτε το dashboard. Δείτε την [Δοκιμή Σύνδεσης](overview.md#testing-login) για την πλήρη λίστα ελέγχου.

---

## Αντιμετώπιση Προβλημάτων Entra ID

### AADSTS50011: Redirect URI Mismatch

Η URI στο `DIGNA_OIDC_REDIRECT_URI` διαφέρει από αυτήν που καταχωρήσατε στο Βήμα 1. Το Entra ID συγκρίνει ολόκληρο το string, οπότε ένα trailing slash, `http` αντί για `https`, ή διαφορετική θύρα μετράνε ως διαφορά. Ελέγξτε **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Invalid Client Secret

Ή αντιγράφηκε το **Secret ID** αντί για την **Value**, ή το secret έχει λήξει. Δημιουργήστε καινούργιο secret και αντιγράψτε τη στήλη Value.

### AADSTS650057: Invalid Resource

Η εγγραφή της εφαρμογής διαγράφηκε ή ανήκει σε διαφορετικό tenant από αυτόν στο discovery URL. Επιβεβαιώστε το Directory (tenant) ID στη σελίδα Overview.

### Οι χρήστες συνδέονται αλλά δεν συμβαίνει τίποτα

Αν ο tenant απαιτεί admin consent και δεν έχει δοθεί, η ανακατεύθυνση επιστρέφει χωρίς χρήσιμο token. Χορηγήστε admin consent κάτω από **API permissions**.

---

## Δείτε επίσης

- [Επισκόπηση Single Sign-On](overview.md) — αναφορά ρυθμίσεων, δοκιμές και γενική αντιμετώπιση προβλημάτων
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)