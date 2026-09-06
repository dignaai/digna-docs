# SSO nustatymas su Keycloak

Keycloak yra savarankiškai talpinamas, pilnai OIDC suderinamas tapatybės tiekėjas. Kadangi jį diegiate patys, discovery URL kuriamas pagal jūsų hosto pavadinimą ir realm, o ne tiekėjo domeną.

Šis vadovas apima **Keycloak pusę**: kliento sukūrimą ir reikšmių surinkimą, kurių reikia digna. digna pusė — `dashboard_config.toml`, testavimas ir trikčių šalinimas — yra tokia pati visiems tiekėjams ir aprašyta [Vieno prisijungimo apžvalgoje](overview.md).

---

## Prieš pradėdami

| Reikalavimas | Pastabos |
|---|---|
| **Keycloak versija** | 17 arba naujesnė dėl čia naudojamų URL kelių — žr. pastabą 4 žingsnyje |
| **Keycloak rolė** | `realm-admin` tiksliniame realm arba serverio administratorius |
| **Realm** | Realm, kuriam priklauso jūsų digna vartotojai — nebūtinai `master` |
| **digna peradresavimo URI** | URL, į kurį vartotojai grįžta po prisijungimo, pvz. `https://digna.yourdomain.com/oidc/callback` |

---

## 1 veiksmas: Pasirinkite realm

1. Atidarykite Keycloak administravimo konsolę
2. Viršutiniame kairiajame kampe naudokite realm pasirinkimą, kad pereitumėte į realm, kuriame yra jūsų vartotojai

!!! warning "Nenaudokite `master` realm"

    `master` realm skirtas Keycloak administravimui. Programų klientai turi būti atskirome realm; dedant digna į `master` suteikiama jo vartotojams prieiga į Keycloak administravimo konsolę.

---

## 2 veiksmas: Sukurkite klientą

1. Eikite į **Clients** ir spauskite **Create client**
2. Konfigūruokite:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — tai taps `DIGNA_OIDC_CLIENT_ID`
3. Spauskite **Next**
4. **Capability config** žingsnyje įjunkite **Client authentication**
5. Palikite įjungtą **Standard flow**; kiti flow nėra reikalingi
6. Spauskite **Next**

!!! warning "Kliento autentifikacija turi būti įjungta"

    Jei **Client authentication** išjungtas, Keycloak sukurs *public* klientą, kuris neturi jokių kredencialų — **Credentials** skirtuko 4 žingsnyje nebus. digna reikia konfidencialaus kliento. Šį nustatymą galima pakeisti ir po kliento sukūrimo, jei padarysite klaidą.

---

## 3 veiksmas: Nustatykite peradresavimo URI

Skiltyje **Login settings** (arba vėliau skirtuke **Settings**):

1. **Valid redirect URIs**: įveskite savo digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: palikite tuščią, arba nustatykite į `+`, kad atkartotų redirect URIs
3. Spauskite **Save**

!!! tip "Venkite žvaigždutinių raidžių (wildcard)"

    Keycloak leidžia šablonus, pvz. `https://digna.yourdomain.com/*`. Wildcard leidžia bet kuriam keliui šiame hoste gauti autorizacijos kodą, todėl geriau nurodyti tikslius callback URL.

---

## 4 veiksmas: Surinkite kliento slaptąjį raktą

1. Atidarykite skirtuką **Credentials**
2. Patikrinkite, kad **Client Authenticator** būtų *Client Id and Secret*
3. Nukopijuokite **Client secret** → tai taps `DIGNA_OIDC_CLIENT_SECRET`

Slaptasis raktas lieka čia prieinamas ir gali būti atnaujintas su **Regenerate**.

---

## 5 veiksmas: Sudarykite discovery URL

Pakeiskite savo Keycloak hostą ir realm pavadinimą:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Pavyzdžiui:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 ir ankstesnės versijos įtraukia `/auth`"

    Iki Keycloak 17 visos galūnės buvo po `/auth` prefiksu:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Distribucijos, kurios nustato `KC_HTTP_RELATIVE_PATH=/auth`, ir šiuolaikinėse versijose palieka seną išdėstymą. Jei URL be `/auth` gražina 404, išbandykite jį su `/auth`.

Atidarykite URL naršyklėje prieš tęsdami. JSON dokumentas patvirtins, kad hostas ir realm yra teisingi.

---

## 6 veiksmas: Konfigūruokite digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Prisijungti per Keycloak"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

Abiejuose failuose esantis `key` turi sutapti — čia `keycloak`. Atkreipkite dėmesį, kad jis nebūtinai turi atitikti Keycloak **Client ID**, nors tokiu atveju lengviau sekti.

---

## 7 veiksmas: Testavimas

Paleiskite iš naujo backend ir web serverį, tada atidarykite dashboard. Pilną kontrolinį sąrašą žr. [Testavimas: Prisijungimas](overview.md#testing-login).

---

## Trikčių šalinimas su Keycloak

### Invalid parameter: redirect_uri

Callback URL nėra įtrauktas į **Valid redirect URIs**. Keycloak serverio loge užfiksuoja gautą URI — tai greičiausias būdas pamatyti tikslų neatitikimą.

### Trūksta Credentials skirtuko

Klientas yra public. Įjunkite **Client authentication** sekcijoje **Settings → Capability config**.

### 404 discovery URL

Arba realm pavadinimas neteisingas, arba diegimas naudoja `/auth` prefiksą. Patikrinkite realm sąrašą administravimo konsolėje ir išbandykite abi URL formas.

### unauthorized_client arba invalid_client

**Standard flow** išjungtas **Capability config**, arba slaptasis raktas buvo atnaujintas Keycloak be `config.toml` atnaujinimo.

### Sertifikato klaidos iš backend

Savarankiškai talpinamas Keycloak su privačiu arba savarankiškai pasirašytu sertifikatu nepraeis digna išorinių HTTPS užklausų į discovery URL. Įdiekite išleidžiančią CA į mašinos, kurioje veikia digna backend, pasitikėjimo saugyklą.

---

## Žr. taip pat

- [Vieno prisijungimo apžvalga](overview.md) — konfigūracijos nuoroda, testavimas ir bendras trikčių šalinimas
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)