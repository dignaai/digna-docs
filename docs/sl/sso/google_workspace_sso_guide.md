---
title: Google Workspace SSO – Integracija Single Sign-On | digna Dokumentacija
description: Konfigurirajte Single Sign-On za digna z Google Workspace prek OpenID Connect — zaslon za soglasje OAuth, ID odjemalca OAuth, pooblaščeni preusmeritveni URI-ji in ustrezna digna konfiguracija.
image: /assets/logo_square.png
keywords: digna sso, google workspace sso, google oidc, zaslon za soglasje oauth, openid connect, podjetna avtentikacija
---

# Nastavite SSO z Google Workspace

Googlova platforma za identiteto je združljiva z OIDC in za vse stranke uporablja en sam, dobro znan discovery URL, zato sta edini vrednosti, specifični za organizacijo, ID odjemalca in skrivnost.

Ta vodič zajema **Google stran**: ustvarjanje odjemalca OAuth in zbiranje vrednosti, ki jih potrebuje digna. Digna stran — `dashboard_config.toml`, testiranje in odpravljanje težav — je enaka za vse ponudnike in je opisana v [Pregled Single Sign-On](overview.md).

---

## Preden začnete

| Zahteva | Opombe |
|---|---|
| **Projekt Google Cloud** | Kateri koli projekt v isti organizaciji kot vaša domena Workspace |
| **Vloga** | Editor ali Owner na projektu |
| **digna redirect URI** | URL, na katerega se uporabniki vrnejo po prijavi, npr. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. korak: Konfigurirajte zaslon za soglasje OAuth

Google ne bo izdal poverilnic, dokler zaslon za soglasje ne obstaja.

1. Odprite [Google Cloud Console](https://console.cloud.google.com) in izberite svoj projekt
2. Pojdite na **APIs & Services → OAuth consent screen**
3. Izberite tip uporabnika:
   - **Internal** — prijavijo se lahko samo računi v vaši domeni Workspace. Priporočeno.
   - **External** — prijavo lahko poskusi kateri koli Google račun.
4. Izpolnite ime aplikacije, e-pošto za podporo uporabnikom in kontaktno e-pošto razvijalca
5. V koraku **Scopes** dodajte `openid`, `.../auth/userinfo.email` in `.../auth/userinfo.profile`
6. Shranite

!!! warning "Zunanje aplikacije morajo biti objavljene"

    Zaslon za soglasje **External** se začne v stanju *Testing*, v katerem lahko prijavo dokončajo samo računi, ki so izrecno dodani na seznam testnih uporabnikov. Vsi ostali vidijo sporočilo "digna has not completed the Google verification process". Aplikacijo pod **Publishing status** preklopite na **In production** ali pa uporabite **Internal** — ki takšne omejitve nima in je prava izbira za namestitev samo za Workspace.

---

## 2. korak: Ustvarite odjemalca OAuth

1. Pojdite na **APIs & Services → Credentials**
2. Kliknite **Create Credentials → OAuth client ID**
3. **Application type** nastavite na **Web application**
4. Poimenujte ga, npr. `digna`
5. Pod **Authorized redirect URIs** kliknite **Add URI** in vnesite:

```
https://digna.yourdomain.com/oidc/callback
```

6. Kliknite **Create**

!!! note "Authorized JavaScript origins niso potrebni"

    digna izmenja avtorizacijsko kodo v zaledju, ne v brskalniku, zato lahko polje **Authorized JavaScript origins** ostane prazno. Pomemben je samo redirect URI.

---

## 3. korak: Zberite poverilnice

Pogovorno okno, ki se prikaže po ustvarjanju, prikazuje:

- **Client ID** — konča se z `.apps.googleusercontent.com` → postane `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → postane `DIGNA_OIDC_CLIENT_SECRET`

Za razliko od večine drugih ponudnikov lahko obe vrednosti pozneje znova pridobite na strani s podrobnostmi poverilnice.

---

## 4. korak: Discovery URL

Google za vse stranke uporablja en discovery URL — ničesar ni treba zamenjati:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## 5. korak: Konfigurirajte digna

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
[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

Vrednost `key` se mora v obeh datotekah ujemati — tukaj `google`.

---

## 6. korak: Testirajte

Znova zaženite zaledje in spletni strežnik, nato odprite nadzorno ploščo. Za celoten kontrolni seznam si oglejte [Testiranje prijave](overview.md#testing-login).

---

## Odpravljanje težav z Google Workspace

### Error 400: redirect_uri_mismatch

URI v `DIGNA_OIDC_REDIRECT_URI` ni na seznamu **Authorized redirect URIs** ali pa se razlikuje po poševnici na koncu ali shemi. Googlova stran z napako prikaže URI, ki ga je prejela — primerjajte ga znak za znakom z registriranim.

### This App Is Blocked / Has Not Completed Verification

Zaslon za soglasje je **External** in je še vedno v stanju *Testing*. Objavite ga ali pa aplikacijo preklopite na **Internal**.

### Access Blocked: Authorization Error

Račun, ki se poskuša prijaviti, je zunaj vaše domene Workspace, zaslon za soglasje pa je **Internal**. To je predvideno vedenje — aplikacije Internal sprejemajo samo račune v organizaciji.

### Spremembe trajajo nekaj minut

Google spremembe poverilnic in zaslona za soglasje razširja asinhrono. Novo dodan redirect URI lahko začne delovati šele po nekaj minutah; če se zdi, da je bila sprememba prezrta, počakajte in poskusite znova, preden začnete z nadaljnjim raziskovanjem.

---

## Povezane vsebine

- [Pregled Single Sign-On](overview.md) — referenca konfiguracije, testiranje in splošno odpravljanje težav
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
