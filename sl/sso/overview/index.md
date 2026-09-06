# Pregled enotne prijave (SSO)

---

## Vsebina

1. [Uvod in pregled](#introduction-and-overview)
2. [Vodniki za ponudnike](#provider-guides)
3. [Koraki konfiguracije](#configuration-steps)
4. [Konfiguracija nadzorne plošče](#dashboard-configuration)
5. [Konfiguracija zaledja](#backend-configuration)
6. [Testiranje prijave](#testing-login)
7. [Odpravljanje težav](#troubleshooting)
8. [Podprti ponudniki](#supported-providers)

---

## Uvod in pregled {: #introduction-and-overview }

Ta vodič vsebuje korak-po-korak navodila za integracijo enotne prijave (SSO) s platformo digna z uporabo **OpenID Connect (OIDC)**.

### Kaj je SSO?

Enotna prijava omogoča uporabnikom, da se v digna prijavijo varno z uporabo svojih podjetniških poverilnic prek zunanjih ponudnikov identitete. Uporabniki se lahko overijo s svojimi korporativnimi poverilnicami, namesto da upravljajo ločena digna gesla.

### Kako deluje

SSO v digna je implementiran z uporabo protokola OIDC. Več ponudnikov identitete je mogoče konfigurirati vzporedno z urejanjem dveh ključnih konfiguracijskih datotek:

- **`dashboard_config.toml`** — Nadzoruje vmesnik za prijavo na sprednji strani
- **`config.toml`** — Konfigurira OIDC povezave na zaledju

### Podprti ponudniki {: #supported-providers-overview }

Primeri v tem vodiču uporabljajo **Microsoft** in **Google**, vendar je mogoče integrirati **kateregakoli ponudnika, ki podpira OIDC**, z enako strukturo konfiguracije.

---

## Vodniki za ponudnike {: #provider-guides }

Vsak ponudnik zahteva iste štiri vrednosti — ID odjemalca, skrivnost odjemalca, preusmeritveni URI in URL za discovery — vendar jih vsak ponudnik postavi na drugo mesto v svojem skrbniškem konzolu, nekateri pa imajo tudi korak specifičen za ponudnika, ki ga drugi nimajo. Spodnji vodiči pokrivajo to polovico dela; ta stran pokriva digna polovico, ki je za vse enaka.

| Provider | Guide | Worth knowing |
|---|---|---|
| **AD FS** | [Nastavitev SSO z AD FS](adfs_sso_guide.md) | Samostojno gostovanje; edini ponudnik tukaj, kjer vi nadzirate storitev za žetone |
| **Auth0** | [Nastavitev SSO z Auth0](auth0_sso_guide.md) | Discovery URL je vezan na najemnika, lastne domene ga spremenijo |
| **Google Workspace** | [Nastavitev SSO z Google Workspace](google_workspace_sso_guide.md) | Zaslon za soglasje mora biti objavljen, preden se lahko prijavijo ne-testni uporabniki |
| **Keycloak** | [Nastavitev SSO s Keycloak](keycloak_sso_guide.md) | Samostojno gostovanje; discovery URL je vezan na realm |
| **Microsoft Entra ID** | [Nastavitev SSO z Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | ID najemnika se pojavi v discovery URL; skrivnosti potečejo |
| **Okta** | [Nastavitev SSO z Okta](okta_sso_guide.md) | Izbira avtentikacijskega strežnika spremeni discovery URL |
| **OneLogin** | [Nastavitev SSO z OneLogin](onelogin_sso_guide.md) | Vrsta OIDC aplikacije se mora izbrati ob kreaciji in je ni mogoče spremeniti |
| **PingOne** | [Nastavitev SSO s PingOne](pingone_sso_guide.md) | ID okolja se pojavi v discovery URL |

Kateri koli drug ponudnik, ki podpira OIDC, deluje enako — glejte [Drugi ponudniki OIDC](#supported-providers).

---

## Koraki konfiguracije {: #configuration-steps }

Konfiguracija SSO zahteva posodobitve dveh datotek. Ta razdelek pojasnjuje, kako konfigurirati vsako izmed njiju.

### Pregled konfiguracijskih datotek

| Datoteka | Lokacija | Namen |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Vmesnik za prijavo na sprednji strani |
| **config.toml** | `/config.toml` | OIDC povezave na zaledju |

Obe datoteki morata biti konfigurirani, da SSO deluje pravilno.

---

## Konfiguracija nadzorne plošče {: #dashboard-configuration }

### Lokacija datoteke

```
dashboard/dashboard_config.toml
```

### 1. korak: Dodajte OIDC ponudnike

Dodajte vnose pod poljem `[[login.oidc]]` za vsakega ponudnika identitete, ki ga želite podpreti.

**Primer z Microsoft in Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Prijava z Microsoftom"

[[login.oidc]]
key = "google"
label = "Prijava z Google"
```

### 2. korak: Konfigurirajte možnosti prijave

Določite, ali naj bo dopuščena prijava z geslom:

```toml
[login]
usePassword = true
```

### Parametri konfiguracije

#### `[[login.oidc]]` razdelek

| Parameter | Tip | Obvezno | Opis |
|---|---|---|---|
| `key` | string | Da | Edinstven identifikator za OIDC povezavo (mora se ujemati s ključem v config.toml) |
| `label` | string | Da | Besedilo, prikazano na gumbu za prijavo (npr. "Prijava z Microsoftom") |

#### `[login]` razdelek

| Parameter | Tip | Privzeto | Opis |
|---|---|---|---|
| `usePassword` | boolean | false | Dovoli prijavo z geslom poleg SSO |

### Razumevanje usePassword

**Če je `usePassword = true`:**
- Na zaslonu za prijavo se prikažejo gumbi za SSO (npr. "Prijava z Microsoftom")
- Na zaslonu za prijavo so tudi polja za uporabniško ime in geslo
- Uporabniki se lahko overijo z obema metodama
- Omogoča hibridne nastavitve, kjer nekateri uporabniki uporabljajo SSO, drugi pa gesla

**Če je `usePassword = false` (ali izpuščeno):**
- Na zaslonu za prijavo se prikazujejo le gumbi za SSO
- Ni polj za uporabniško ime/geslo
- Na voljo je samo OIDC avtentikacija

!!! tip "Namig"

    Prijava z geslom je na voljo samo za uporabnike, ki so bili ustvarjeni z gesli z ukazom `digna user add` ali prek nadzorne plošče.

### Popoln primer

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Prijava z Microsoftom"

[[login.oidc]]
key = "google"
label = "Prijava z Google"

[[login.oidc]]
key = "okta"
label = "Prijava z Okta"
```

---

## Konfiguracija zaledja {: #backend-configuration }

### Lokacija datoteke

```
/config.toml
```

(Rodovitna namestitvena mapa digna)

### 1. korak: Dodajte razdelke za ponudnike OIDC

Za vsakega ponudnika mora obstajati namenski razdelek `[oidc.<key>]`. Ključ se mora ujemati s `key`, določenim v `dashboard_config.toml`.

### Konfiguracija za Microsoft

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Konfiguracija za Google

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Parametri konfiguracije

| Parameter | Tip | Obvezno | Opis | Primer |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Da | Client ID od ponudnika identitete | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Da | Client secret od ponudnika identitete | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Da | URL za klic nazaj po avtentikaciji | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Da | OIDC konfiguracijska točka | `https://login.microsoftonline.com/...` |

!!! warning "Pomembno"

    Zamenjajte nadomestne vrednosti (`<client_id>`, `<client_secret>`, `<tenant_id>`) z dejavnimi poverilnicami iz konzole ponudnika identitete.

### Redirect URI

Preusmeritveni URI mora biti enak kot v konfiguraciji ponudnika identitete:

```
http://localhost:5173/oidc/callback
```

Če je digna gostovan na drugem domeni, ustrezno posodobite:
- Lokalno: `http://localhost:5173/oidc/callback`
- Produkcija: `https://digna.yourdomain.com/oidc/callback`

### Popoln primer

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

## Testiranje prijave {: #testing-login }

Po dokončani konfiguraciji preverite, ali SSO pravilno deluje.

### Predtestni seznam

Pred testiranjem zagotovite:

- [ ] `dashboard_config.toml` je posodobljen z OIDC ponudniki
- [ ] `config.toml` je posodobljen z OIDC poverilnicami
- [ ] Obe datoteki sta shranjeni
- [ ] Poverilnice so pravilne (client ID, client secret)
- [ ] Redirect URI se ujema z vašo nameščeno lokacijo
- [ ] Aplikacija pri ponudniku identitete je konfigurirana s preusmeritvenim URI

### Koraki testiranja

#### 1. korak: Ponovni zagon storitev

Ponovno zaženite digna zaledje in spletni strežnik, da uveljavite spremembe.

**Če tečete kot storitev na Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Če tečete kot storitev na Linux ali macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Če tečete ročno:**
```bash
digna serve --address localhost --port 8082
```

**Ponovno zaženite tudi spletni strežnik** — IIS ali Tomcat na Windows, nginx ali Apache na Linux in macOS.

#### 2. korak: Odprite nadzorno ploščo

Odprite digna nadzorno ploščo v brskalniku:

```
http://localhost:5173
```

(ali vaš konfiguriran URL nadzorne plošče)

#### 3. korak: Preverite gumbe za prijavo

Preverite, ali se prikažejo gumbi za prijavo za vsakega konfiguriranega ponudnika:

- Moral bi videti gumb "Prijava z Microsoftom"
- Moral bi videti gumb "Prijava z Google"
- (Če je usePassword = true) Moral bi videti polja za uporabniško ime/geslo

Če se gumbi ne prikažejo:
- Preverite, da je `dashboard_config.toml` shranjen
- Preverite, da je bila storitev nadzorne plošče ponovno zagnana
- Preverite konzolo brskalnika (F12) za napake

#### 4. korak: Preizkusite SSO prijavo

Kliknite enega izmed SSO gumbov (npr. "Prijava z Microsoftom"):

1. Preusmerjeni boste na stran za prijavo ponudnika identitete
2. Prijavite se s svojimi podjetniškimi poverilnicami
3. Preusmerjeni boste nazaj v digna
4. Vpis v digna bi bil uspešen

#### 5. korak: Preverite ustvarjanje uporabnika

Po uspešni SSO prijavi:

- Uporabnik bi moral biti samodejno ustvarjen v digna
- Uporabnik bi moral biti vpisan
- Profil uporabnika bi moral prikazati poverilnice ponudnika identitete
- Videli bi nadzorno ploščo digna

#### 6. korak: Preizkus prijave z geslom (če omogočeno)

Če je `usePassword = true`:

1. Odjavite se iz digna
2. Na strani za prijavo vnesite uporabniško ime in geslo
3. Morali bi se lahko prijaviti z geslom

---

## Odpravljanje težav {: #troubleshooting }

### Gumbi za prijavo se ne prikažejo

**Simptomi:**
- Gumbi za OIDC prijavo niso vidni na strani za prijavo
- Vidite le polja za geslo (če je usePassword = true)

**Vzroki in rešitve:**
1. Preverite, ali je `dashboard_config.toml` v mapi `dashboard/`
2. Preverite, ali so prisotni razdelki `[[login.oidc]]` s pravilno sintakso
3. Ponovno zaženite storitev nadzorne plošče
4. Počistite predpomnilnik brskalnika (Ctrl+Shift+Delete ali Cmd+Shift+Delete)
5. Preverite konzolo brskalnika (F12 → Console) za napake

---

### Napaka neujemanja Redirect URI

**Simptomi:**
- Po kliku gumba SSO se pojavi napaka o "redirect_uri mismatch"
- Napaka "The redirect URI is not registered"

**Vzroki in rešitve:**
1. Preverite, ali je `DIGNA_OIDC_REDIRECT_URI` v `config.toml` pravilen
2. Preverite, ali je redirect URI registriran v nastavitvah ponudnika identitete
3. Zagotovite, da obe strani uporabljata identične URL-je (vključno s protokolom, domeno, potjo)
4. Preverite morebitne tipkarske napake v redirect URI
5. Če uporabljate HTTPS, preverite, ali je potrdilo veljavno

---

### Napaka neveljavnih poverilnic odjemalca

**Simptomi:**
- Napaka "Invalid client ID or secret"
- Avtentikacija neuspešna zaradi napake poverilnic

**Vzroki in rešitve:**
1. Preverite, ali sta `DIGNA_OIDC_CLIENT_ID` in `DIGNA_OIDC_CLIENT_SECRET` pravilna
2. Prepričajte se, da ni dodatnih presledkov ali posebnih znakov
3. Preverite, ali poverilnice niso potekle ali bile razveljavljene
4. Ponovno zaženite zaledno storitev po posodobitvi konfiguracije
5. Preverite konzolo ponudnika identitete, da potrdite, da so poverilnice aktivne

---

### Prijava se zmrzne ali poteče čas

**Simptomi:**
- Klik gumba SSO ne naredi nič
- Potek časa po nekaj sekundah
- Brskalnik prikaže "Failed to connect" ali podobno

**Vzroki in rešitve:**
1. Preverite, ali digna zaledje teče: `digna repo check`
2. Preverite omrežno povezljivost do ponudnika identitete
3. Preverite, ali je `DIGNA_OIDC_CONFIGURATION_URL` dostopen
4. Preverite pravilnike požarnega zidu, ki dovoljujejo odhodne HTTPS povezave
5. Preverite, ali zaledje in nadzorna plošča medsebojno dostopata

---

### Uporabniki se ne ustvarijo samodejno

**Simptomi:**
- SSO prijava uspe, vendar uporabnik ni ustvarjen v digna
- Po SSO prijavi se pojavi napaka o dovoljenjih

**Vzroki in rešitve:**
1. Preverite, ali je OIDC konfiguracija pravilna
2. Preverite, ali so nastavljena dovoljenja uporabnikov
3. Preučite dnevnike digna za morebitna sporočila o napakah
4. Ponovno zaženite zaledno storitev
5. Če težava vztraja, kontaktirajte support@digna.ai

---

## Podprti ponudniki {: #supported-providers }

### Testirano in podprto

Naslednji OIDC ponudniki so testirani in jih poznamo:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Nastavitev SSO z AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Nastavitev SSO z Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Nastavitev SSO z Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Nastavitev SSO s Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Nastavitev SSO z Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Nastavitev SSO z Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Nastavitev SSO z OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Nastavitev SSO s PingOne](pingone_sso_guide.md) |

### Drugi ponudniki OIDC

Kateri koli ponudnik, ki podpira OpenID Connect, je mogoče integrirati. Potrebne informacije:

- Client ID
- Client secret
- OpenID konfiguracijski URL (običajno na `/.well-known/openid-configuration`)
- Podprti obsegi (običajno `openid profile email`)

Kontaktirajte support@digna.ai, če potrebujete pomoč pri integraciji določenega ponudnika.

---

## Priporočene prakse

**NALOGE:**
- Uporabljajte HTTPS v produkciji (ne HTTP)
- Shrani skrivnosti odjemalca varno (po možnosti uporabite okoljske spremenljivke)
- Občasno obračajte (rotate) skrivnosti
- Najprej testirajte v neprodukcijskem okolju
- Dokumentirajte, kateri ponudniki so konfigurirani
- Spremljajte dnevnike prijav zaradi sumljive aktivnosti
- Sinhronizirajte nastavitve ponudnika identitete s konfiguracijo digna

**NE DELAJTE:**
- Ne shranjujte skrivnosti odjemalca v upravljanju različic
- Ne uporabljajte HTTP redirect URI v produkciji
- Ne konfigurirajte več ponudnikov z istim ključem
- Ne puščajte privzetih/testnih poverilnic v produkciji
- Ne izpostavljajte konfiguracijskih datotek, ki vsebujejo skrivnosti
- Ne mešajte razvojnih in produkcijskih poverilnic

---

## Podpora

Potrebujete pomoč pri konfiguraciji SSO?

- **Email:** support@digna.ai
- **Dokumentacija:** https://docs.digna.ai
- **Spletna stran:** https://www.digna.ai

---

**Zadnja posodobitev:** August 30, 2026  
**Različica:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**