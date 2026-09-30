# Nastavite SSO z Auth0

Auth0 je združljiv z OIDC in za vsakega najemnika (tenant) ponuja končno točko discovery. Najpomembneje je pravilno nastaviti domeno najemnika, ki se pojavi v discovery URL-ju in se spremeni, če omogočite prilagojeno domeno.

Ta vodič zajema **Auth0 stran**: ustvarjanje aplikacije in zbiranje vrednosti, ki jih potrebuje digna. Digna stran — `dashboard_config.toml`, testiranje in odpravljanje težav — je enaka za vse ponudnike in je opisana v [Pregled Single Sign-On](overview.md).

---

## Preden začnete

| Zahteva | Opombe |
|---|---|
| **Vloga v Auth0** | Skrbnik (Admin) najemnika |
| **Domena najemnika** | npr. `yourcompany.eu.auth0.com` — segment regije je pomemben |
| **digna redirect URI** | URL, na katerega se uporabniki vrnejo po prijavi, npr. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. korak: Ustvarite aplikacijo

1. Prijavite se v [Auth0 Dashboard](https://manage.auth0.com)
2. Pojdite na **Applications → Applications**
3. Kliknite **Create Application**
4. Poimenujte jo `digna` in izberite **Regular Web Applications**
5. Kliknite **Create**

!!! warning "Izberite Regular Web Applications"

    *Single Page Application* in *Native* ustvarita javna odjemalca brez skrivnosti. digna izvede izmenjavo kode v svojem zaledju in potrebuje zaupnega odjemalca, zato je **Regular Web Applications** pravilen tip. Za razliko od nekaterih ponudnikov Auth0 omogoča, da tip pozneje spremenite pod **Settings → Application Type**.

---

## 2. korak: Dodajte callback URL

Na zavihku **Settings** aplikacije:

1. Poiščite **Allowed Callback URLs**
2. Vnesite svoj digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Po želji nastavite **Allowed Logout URLs** na URL svoje nadzorne plošče
4. Pomaknite se na dno in kliknite **Save Changes**

!!! note "Ločeno z vejicami, ne z novimi vrsticami"

    Auth0 v tem polju sprejme več callback URL-jev, ločenih z vejicami. Seznam, ločen samo z novimi vrsticami, se prebere kot en nepravilno oblikovan URL in se brez opozorila ne ujema z ničemer.

---

## 3. korak: Zberite poverilnice

Še vedno v **Settings**, v plošči **Basic Information**:

- **Domain** → gre v discovery URL
- **Client ID** → postane `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → postane `DIGNA_OIDC_CLIENT_SECRET` (kliknite za razkritje)

---

## 4. korak: Preverite tip dodelitve (grant type)

1. Pojdite na **Settings → Advanced Settings → Grant Types**
2. Preverite, da je označen **Authorization Code**

Za Regular Web Applications je privzeto omogočen. Če je bil odznačen, prijava v digna ne uspe z napako `unauthorized_client`.

---

## 5. korak: Sestavite discovery URL

Vstavite **Domain** iz 3. koraka:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Na primer:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Prilagojene domene spremenijo izdajatelja"

    Če vaš najemnik uporablja prilagojeno domeno, kot je `login.yourcompany.com`, uporabite to domeno v discovery URL-ju. Mešanje obeh — kanonične domene v discovery URL-ju in prilagojene v brskalniku — povzroči neujemanje izdajatelja (issuer), žeton pa je zavrnjen po sicer uspešni prijavi.

---

## 6. korak: Konfigurirajte digna

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
[oidc_clients.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

Vrednost `key` se mora v obeh datotekah ujemati — tukaj `auth0`.

---

## 7. korak: Testirajte

Znova zaženite zaledje in spletni strežnik, nato odprite nadzorno ploščo. Za celoten kontrolni seznam si oglejte [Testiranje prijave](overview.md#testing-login).

---

## Odpravljanje težav z Auth0

### Neujemanje callback URL-ja

Stran z napako Auth0 navede URL, ki ga je prejela. Dodajte ga v **Allowed Callback URLs** in preverite, da so vnosi ločeni z vejicami.

### unauthorized_client

**Authorization Code** ni omogočen pod **Advanced Settings → Grant Types** ali pa tip aplikacije ni Regular Web Applications.

### Dostop zavrnjen po uspešni prijavi

Pravilo (Rule), dejanje (Action) ali sprožilec Post-Login v najemniku zavrača uporabnika. Preverite **Actions → Flows → Login** in dnevnike najemnika pod **Monitoring → Logs**, ki prikažejo natančen razlog.

### Neujemanje izdajatelja

Discovery URL in domena, na katero je bil preusmerjen brskalnik, se razlikujeta — običajno kanonična domena najemnika in prilagojena domena. Dosledno uporabljajte eno od njiju.

---

## Povezane vsebine

- [Pregled Single Sign-On](overview.md) — referenca konfiguracije, testiranje in splošno odpravljanje težav
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)