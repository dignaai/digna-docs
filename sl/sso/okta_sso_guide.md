# Nastavite SSO z Okta

Okta je združljiva z OIDC, z eno posebnostjo, ki zmede večino tistih, ki integrirajo prvič: Okta org razkriva več avtentikacijskih strežnikov, pri čemer ima vsak svoj discovery URL.

Ta vodič zajema **Okta stran**: ustvarjanje integracije aplikacije in zbiranje vrednosti, ki jih potrebuje digna. Digna stran — `dashboard_config.toml`, testiranje in odpravljanje napak — je enaka za vse ponudnike in je opisana v [Pregled Single Sign-On](overview.md).

---

## Preden začnete

| Zahteva | Opombe |
|---|---|
| **Vloga v Okta** | Super Administrator, ali vloga skrbnika z dovoljenjem za ustvarjanje integracij aplikacij |
| **Okta domena** | npr. `yourcompany.okta.com`, ali prilagojena domena, če je nastavljena |
| **digna redirect URI** | URL, na katerega se uporabniki vrnejo po prijavi, npr. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. korak: Ustvarite integracijo aplikacije

1. Prijavite se v Okta Admin Console
2. Pojdite na **Applications → Applications**
3. Kliknite **Create App Integration**
4. Izberite:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Kliknite **Next**

!!! warning "Tip aplikacije ni mogoče spremeniti"

    Če izberete *Single-Page Application* namesto *Web Application*, ustvarite javnega klienta brez skrivnosti, in dignajev strežnik za izmenjavo kode ne bo uspel z napako `invalid_client`. Tip je fiksiran ob ustvarjanju — napačna izbira pomeni brisanje aplikacije in začetek znova.

---

## 2. korak: Konfigurirajte integracijo

1. **Ime integracije aplikacije**: `digna`
2. **Grant type**: pustite izbran *Authorization Code*
3. **Sign-in redirect URIs**: vnesite vaš digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: neobvezno
5. Pod **Assignments**, izberite, kdo sme uporabljati integracijo — določena skupina je varnejša kot *Allow everyone in your organization to access*
6. Kliknite **Save**

!!! note "Dodelitev je obvezna"

    Okta avtenticira uporabnika in nato preveri, ali je dodeljen aplikaciji. Nedodeljen uporabnik pride do Okta strani za prijavo, se uspešno prijavi in mu je zavrnjen dostop ob preusmeritvi nazaj. Če se vam prijava uspe, sodelavcem pa ne, je prva stvar, ki jo preverite — dodelitev.

---

## 3. korak: Zberite poverilnice

Na zavihku **General** aplikacije, pod **Client Credentials**:

- **Client ID** → postane `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → postane `DIGNA_OIDC_CLIENT_SECRET` (kliknite ikono očesa za razkritje)

---

## 4. korak: Izberite avtentikacijski strežnik

To je korak, ki določi vaš discovery URL. Pojdite na **Security → API**, da vidite avtentikacijske strežnike v vaši organizaciji.

**Org authorization server** — izdaja žetone za samo Okta org:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — vključno s tistim, ki ga Okta ustvari z imenom `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Za vgrajeni strežnik je `<auth_server_id>` dobesedno `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Kateri izbrati?"

    Uporabite **org** avtentikacijski strežnik, razen če vaša organizacija že standardizira na prilagojenem za politike dostopa do API-jev. Okta Developer računi privzeto uporabljajo `default`; mnoge podjetne organizacije ga onemogočijo. Odprite oba URL-ja v brskalniku — tisti, ki vrne JSON namesto napake, je tisti, ki je na voljo vam.

---

## 5. korak: Konfigurirajte digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Prijava z Okta"
```

### `config.toml`

```toml
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<skrivnost odjemalca, kopirana v 3. koraku>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

Ključ v obeh datotekah se mora ujemati — tukaj `okta`.

---

## 6. korak: Testirajte

Znova zaženite backend in spletni strežnik, nato odprite nadzorno ploščo. Oglejte si [Testiranje prijave](overview.md#testing-login) za celoten kontrolni seznam.

---

## Odpravljanje težav z Okta

### Preusmeritveni URI ni registriran

Okta v napaki navede problematični URI. Primerjajte ga z **General → Sign-in redirect URIs**; Okta primerja celoten niz, vključno z morebitno poševnico na koncu.

### Uporabnik ni dodeljen aplikaciji

Račun ni na seznamu dodelitev aplikacije. Dodajte uporabnika ali njegovo skupino pod **Assignments**.

### 400 Bad Request: Invalid Authorization Server

`<auth_server_id>` v discovery URL-ju ne obstaja, najpogosteje `default` na organizaciji, kjer je bil odstranjen. Preverite **Security → API** za strežnike, ki so dejansko na voljo.

### invalid_client pri koraku tokena

Integracija je bila ustvarjena kot Single-Page Application in nima skrivnosti klienta. Ustvarite jo znova kot Web Application.

---

## Povezane vsebine

- [Pregled Single Sign-On](overview.md) — referenca konfiguracije, testiranje in splošno odpravljanje težav
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)