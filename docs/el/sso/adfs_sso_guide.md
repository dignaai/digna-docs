---
title: AD FS SSO – Ενσωμάτωση Single Sign-On | Τεκμηρίωση digna
description: Ρυθμίστε το Single Sign-On για το digna με Active Directory Federation Services χρησιμοποιώντας OpenID Connect — ομάδα εφαρμογών, εφαρμογή διακομιστή, κοινόχρηστο μυστικό, επιτρεπόμενα scopes και η αντίστοιχη ρύθμιση του digna.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, υπηρεσίες ομοσπονδίας Active Directory, adfs oidc, application group, openid connect, on-premises identity provider
---

# Ρύθμιση SSO με AD FS

Το Active Directory Federation Services είναι η on‑premises επιλογή: οι δικοί σας διακομιστές εκδίδουν τα tokens και το discovery URL είναι το δικό σας host name. Το AD FS υποστηρίζει OpenID Connect από τα **Windows Server 2016** και μετά.

Αυτός ο οδηγός καλύπτει την **πλευρά του AD FS**: τη δημιουργία της application group και τη συλλογή των τιμών που χρειάζεται το digna. Η πλευρά του digna — `dashboard_config.toml`, δοκιμές και αντιμετώπιση προβλημάτων — είναι ίδια για κάθε provider και περιγράφεται στην [Επισκόπηση Single Sign-On](overview.md).

---

## Πριν Ξεκινήσετε

| Απαίτηση | Σημειώσεις |
|---|---|
| **Έκδοση AD FS** | Windows Server 2016 ή νεότερο — οι παλαιότερες εκδόσεις δεν υποστηρίζουν OIDC |
| **Πρόσβαση** | Τοπικός διαχειριστής στον AD FS server |
| **Όνομα υπηρεσίας ομοσπονδίας** | π.χ. `adfs.yourdomain.com` |
| **digna redirect URI** | Το URL στο οποίο επιστρέφουν οι χρήστες μετά τη σύνδεση, π.χ. `https://digna.yourdomain.com/oidc/callback` |

---

## Βήμα 1: Δημιουργία της Ομάδας Εφαρμογών

1. Στον AD FS server, ανοίξτε το **AD FS Management**
2. Δεξί κλικ σε **Application Groups** και επιλέξτε **Add Application Group**
3. Εισαγάγετε `digna` ως όνομα
4. Κάτω από **Standalone applications** — ή **Client-Server applications** ανάλογα με την έκδοσή σας — επιλέξτε **Server application accessing a web API**
5. Κάντε κλικ στο **Next**

---

## Βήμα 2: Διαμόρφωση της Εφαρμογής Διακομιστή

1. **Name**: `digna backend`
2. **Client Identifier**: Το AD FS δημιουργεί ένα GUID. Αντιγράψτε το — αυτό γίνεται `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: εισαγάγετε το callback URL του digna και κάντε κλικ στο **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Κάντε κλικ στο **Next**

!!! warning "Πατήστε Προσθήκη, όχι μόνο Επόμενο"

    Το πεδίο του redirect URI έχει δικό του κουμπί **Add**. Η πληκτρολόγηση ενός URI και το κλικ στο **Next** χωρίς το πάτημα του **Add** το απορρίπτει, και ο οδηγός δεν ειδοποιεί. Βεβαιωθείτε ότι το URI εμφανίζεται στη λίστα κάτω από το πεδίο πριν συνεχίσετε.

---

## Βήμα 3: Δημιουργία του Κοινόχρηστου Μυστικού

1. Επιλέξτε **Generate a shared secret**
2. Αντιγράψτε το δημιουργημένο μυστικό → γίνεται `DIGNA_OIDC_CLIENT_SECRET`
3. Κάντε κλικ στο **Next**

!!! warning "Το μυστικό εμφανίζεται μία φορά"

    Το AD FS εμφανίζει το κοινόχρηστο μυστικό μόνο σε αυτή τη σελίδα του οδηγού και δεν μπορεί να το εμφανίσει ξανά. Αν το χάσετε, επαναφέρετέ το αργότερα από τις ιδιότητες της application group.

---

## Βήμα 4: Διαμόρφωση του Web API

1. **Identifier**: εισαγάγετε τον ίδιο client identifier από το Βήμα 2 και κάντε κλικ στο **Add**
2. Κάντε κλικ στο **Next**
3. Επιλέξτε μία **Access Control Policy** — *Permit everyone* είναι ο πιο απλός αρχικός κανόνας· περιορίστε το σε ομάδα για παραγωγή
4. Κάντε κλικ στο **Next**

---

## Βήμα 5: Εκχώρηση των Επιτρεπόμενων Scopes

Στο βήμα **Configure Application Permissions**, επιλέξτε:

- `openid`
- `profile`
- `email`

Έπειτα κάντε κλικ στο **Next** και ολοκληρώστε τον οδηγό.

!!! warning "Το openid Δεν Επιλέγεται Από Προεπιλογή"

    Το AD FS σε κάποιες εκδόσεις επιλέγει μόνο το `user_impersonation`. Χωρίς το `openid`, το token endpoint επιστρέφει ένα OAuth access token αντί για ID token, και το digna δεν μπορεί να ταυτοποιήσει τον χρήστη.

---

## Βήμα 6: Επιβεβαίωση του Discovery Endpoint

Αντικαταστήστε το όνομα της υπηρεσίας ομοσπονδίας:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Για παράδειγμα:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Ανοίξτε το σε ένα πρόγραμμα περιήγησης. Ένα έγγραφο JSON επιβεβαιώνει ότι το OIDC είναι ενεργοποιημένο και ότι το host name είναι σωστό.

!!! note "Ο Backend Πρέπει να Εμπιστεύεται το Πιστοποιητικό"

    Συνήθως το AD FS χρησιμοποιεί εσωτερική αρχή πιστοποίησης. Η μηχανή που τρέχει το backend του digna κάνει τη δική της εξερχόμενη κλήση HTTPS σε αυτό το URL, οπότε η εκδίδουσα CA πρέπει να βρίσκεται στο trust store αυτής της μηχανής — όχι μόνο στα προγράμματα περιήγησης των χρηστών που συνδέονται.

---

## Βήμα 7: Ρύθμιση του digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Σύνδεση με Active Directory"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

Το `key` και στα δύο αρχεία πρέπει να ταιριάζει — `adfs` εδώ.

---

## Βήμα 8: Δοκιμή

Επανεκκινήστε το backend και τον web server, και στη συνέχεια ανοίξτε το dashboard. Δείτε την [Επισκόπηση Single Sign-On](overview.md#testing-login) για τη λίστα ελέγχου δοκιμών.

---

## Αντιμετώπιση Προβλημάτων AD FS

### MSIS9611: The Client Is Not Allowed to Access the Resource

Ο identifier του web API στο Βήμα 4 δεν ταιριάζει με τον client identifier, ή τα scopes στο Βήμα 5 δεν εγκρίθηκαν. Και τα δύο μπορούν να επεξεργαστούν από τις ιδιότητες της application group.

### MSIS9602: Invalid redirect_uri

Το URI πληκτρολογήθηκε αλλά δεν προστέθηκε με το κουμπί **Add**, ή διαφέρει από το `DIGNA_OIDC_REDIRECT_URI`. Ελέγξτε **Application Groups → digna → digna backend → Properties**.

### Δεν Επιστρέφεται ID Token

Λείπει το scope `openid` από τα permissions της εφαρμογής.

### Ο Backend Δεν Μπορεί να Προσεγγίσει το Discovery URL

Είτε το DNS στον host του backend δεν επιλύει το όνομα της υπηρεσίας ομοσπονδίας, είτε το πιστοποιητικό του AD FS δεν είναι εμπιστευμένο εκεί. Δοκιμάστε με `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` από τον ίδιο τον server του digna.

### Συμβάντα που Πρέπει να Ελέγξετε

Ο AD FS server καταγράφει αποτυχίες σε **Applications and Services Logs → AD FS → Admin** στο Event Viewer, συνήθως με πιο συγκεκριμένο λόγο από αυτόν που εμφανίζει ο browser.

---

## Δείτε Επίσης

- [Επισκόπηση Single Sign-On](overview.md) — αναφορά ρυθμίσεων, δοκιμές και γενική αντιμετώπιση προβλημάτων
- [Microsoft: Σενάρια AD FS OpenID Connect](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)