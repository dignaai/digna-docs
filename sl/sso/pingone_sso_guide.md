# Nastavite SSO s PingOne

PingOne je združljiv z OIDC. Pri dveh njegovih vrednostih je potrebna previdnost: pri **ID-ju okolja** (environment ID), ki se pojavi v vsakem URL-ju končne točke, in pri **regionalni domeni**, ki se razlikuje med severnoameriškimi, evropskimi, kanadskimi, azijsko-pacifiškimi in avstralskimi najemniki.

Ta vodič zajema **PingOne stran**: ustvarjanje aplikacije in zbiranje vrednosti, ki jih potrebuje digna. Digna stran — `dashboard_config.toml`, testiranje in odpravljanje težav — je enaka za vse ponudnike in je opisana v [Pregled Single Sign-On](overview.md).

---

## Preden začnete

| Zahteva | Opombe |
|---|---|
| **Vloga v PingOne** | Environment Admin ali Identity Data Admin v ciljnem okolju |
| **Okolje** | Okolje PingOne, ki mu pripadajo vaši uporabniki digna |
| **digna redirect URI** | URL, na katerega se uporabniki vrnejo po prijavi, npr. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. korak: Ustvarite aplikacijo

1. Prijavite se v skrbniško konzolo PingOne in izberite svoje okolje
2. Pojdite na **Applications → Applications**
3. Kliknite gumb **+**
4. Kot **Application Name** vnesite `digna`
5. Izberite **OIDC Web App**
6. Kliknite **Save**

!!! warning "Izberite OIDC Web App, ne Single-Page App"

    *Single-Page App* in *Native App* ustvarita javna odjemalca, ki ne moreta hraniti skrivnosti. digna izmenja avtorizacijsko kodo v svojem zaledju in potrebuje zaupni tip **OIDC Web App**.

---

## 2. korak: Konfigurirajte redirect URI

1. Odprite zavihek **Configuration** aplikacije
2. Za urejanje kliknite ikono svinčnika
3. Preverite, da je **Response Type** nastavljen na *Code* in **Grant Type** na *Authorization Code*
4. Pod **Redirect URIs** vnesite svoj digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

5. **Token Endpoint Authentication Method** nastavite na *Client Secret Post* ali *Client Secret Basic*
6. Kliknite **Save**

---

## 3. korak: Omogočite aplikacijo

V vrstici aplikacije ali na plošči s podrobnostmi preklopite stikalo na **enabled**.

!!! warning "Nove aplikacije so na začetku onemogočene"

    PingOne ustvari aplikacije v onemogočenem stanju. Onemogočena aplikacija povzroči napako v koraku avtorizacije, ki stikala ne omenja, zato je vredno to preveriti, preden začnete odpravljati karkoli drugega.

---

## 4. korak: Dodelite obsege

1. Odprite zavihek **Resources**
2. Preverite, da je `openid` dodeljen, in dodajte `profile` ter `email` iz vira **OpenID Connect**
3. Kliknite **Save**

---

## 5. korak: Dodelite uporabnike

1. Odprite zavihek **Access**
2. Dodajte populacijo ali skupine, katerih člani lahko uporabljajo digna
3. Kliknite **Save**

---

## 6. korak: Zberite poverilnice in ID okolja

Na zavihku **Configuration** razširite **General**:

- **Client ID** → postane `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → postane `DIGNA_OIDC_CLIENT_SECRET` (kliknite ikono očesa)
- **Environment ID** → gre v discovery URL

Na istem zavihku je naveden tudi pripravljen **OIDC Discovery Endpoint**, ki ga lahko kopirate neposredno, namesto da ga sestavljate ročno.

---

## 7. korak: Sestavite discovery URL

Vstavite ID okolja in domeno za svojo regijo:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Regija | Domena |
|---|---|
| Severna Amerika | `auth.pingone.com` |
| Evropa | `auth.pingone.eu` |
| Kanada | `auth.pingone.ca` |
| Azija in Pacifik | `auth.pingone.asia` |
| Avstralija | `auth.pingone.com.au` |

Za evropsko okolje:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Kopirajte ga, namesto da ga tipkate"

    Regionalna domena je daleč najpogostejša napaka pri integraciji PingOne, napačna regija pa vrne 404 namesto koristnega sporočila. Uporabite vrednost **OIDC Discovery Endpoint** iz 6. koraka.

---

## 8. korak: Konfigurirajte digna

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
[oidc_clients.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

Vrednost `key` se mora v obeh datotekah ujemati — tukaj `pingone`.

---

## 9. korak: Testirajte

Znova zaženite zaledje in spletni strežnik, nato odprite nadzorno ploščo. Za celoten kontrolni seznam si oglejte [Testiranje prijave](overview.md#testing-login).

---

## Odpravljanje težav s PingOne

### 404 na discovery URL-ju

Regionalna domena ali ID okolja je napačen. Primerjajte z vrednostjo **OIDC Discovery Endpoint**, prikazano na zavihku Configuration aplikacije.

### NOT_FOUND ali Application Disabled

Stikalo aplikacije iz 3. koraka je še vedno izklopljeno.

### Neujemanje redirect URI-ja

PingOne primerja celoten niz. V **Configuration → Redirect URIs** preverite poševnico na koncu ali razliko v shemi.

### Prijava uspe, vendar zahtevek email ne doseže digna

Obsega `email` in `profile` nista bila dodeljena na zavihku **Resources**.

### Uporabnik ne vidi aplikacije

Na zavihku **Access** nobena populacija ali skupina nima dodeljenega dostopa.

---

## Povezane vsebine

- [Pregled Single Sign-On](overview.md) — referenca konfiguracije, testiranje in splošno odpravljanje težav
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)