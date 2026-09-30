# Iestatīt SSO ar OneLogin

OneLogin atbilst OIDC standartam. Tā īpatnība ir tāda, ka konektora tips tiek izvēlēts no kataloga lietotnes izveides brīdī, un vēlāk to mainīt nevar.

Šis ceļvedis aptver **OneLogin pusi**: lietotnes izveidi un vērtību vākšanu, kas nepieciešamas digna. digna puse — `dashboard_config.toml`, testēšana un problēmu novēršana — ir vienāda visiem pakalpojumu sniedzējiem un aprakstīta [Single Sign-On pārskatā](overview.md).

---

## Pirms sākat

| Prasība | Piezīmes |
|---|---|
| **OneLogin loma** | Konta īpašnieks vai administrators, kuram atļauts pievienot lietotnes |
| **Apakšdomēns** | piem. `yourcompany.onelogin.com` |
| **digna redirect URI** | URL, uz kuru lietotāji atgriežas pēc pieteikšanās, piem. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. solis: Izveidot OIDC lietotni

1. Piesakieties OneLogin Admin portālā
2. Dodieties uz **Applications → Applications**
3. Noklikšķiniet **Add App**
4. Meklējiet `OpenId Connect` un atlasiet konektoru **OpenId Connect (OIDC)**
5. Iestatiet **Display Name** uz `digna`
6. Noklikšķiniet **Save**

!!! warning "Konektora tips tiek noteikts izveides brīdī"

    OneLogin katalogā ir atsevišķi ieraksti SAML un OIDC, un lietotni nevar pārveidot no viena uz otru. Ja kļūdas pēc izvēlaties SAML konektoru, izdzēsiet lietotni un pievienojiet to no jauna — nav iestatījuma, ar ko pārslēgt protokolu.

---

## 2. solis: Konfigurēt redirect URI

1. Atveriet cilni **Configuration**
2. Laukā **Redirect URI's** ievadiet savu digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Pēc izvēles iestatiet **Post Logout Redirect URIs** uz sava dashboard URL
4. Noklikšķiniet **Save**

!!! note "Viens URI katrā rindā"

    Atšķirībā no pakalpojumu sniedzējiem, kas sagaida ar komatiem atdalītu sarakstu, OneLogin laukā **Redirect URI's** katrā rindā norāda vienu URI.

---

## 3. solis: Iestatīt lietotnes tipu un autentifikācijas metodi

1. Atveriet cilni **SSO**
2. Pārliecinieties, ka **Application Type** ir *Web*
3. Iestatiet **Token Endpoint → Authentication Method** uz *POST* (`client_secret_post`) vai *Basic* (`client_secret_basic`)

!!! warning "Neizvēlieties None"

    Ja autentifikācijas metodi iestatāt uz *None*, lietotne kļūst par publisku klientu bez slepenās atslēgas (secret), un digna backend koda apmaiņa tiks noraidīta. Der gan POST, gan Basic.

---

## 4. solis: Savākt akreditācijas datus

Joprojām cilnē **SSO**:

- **Client ID** → kļūst par `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → kļūst par `DIGNA_OIDC_CLIENT_SECRET` (noklikšķiniet **Show client secret**)

Lapā redzams arī **Issuer URL**, kas apstiprina discovery URL nākamajā solī.

---

## 5. solis: Piešķirt lietotājus

1. Atveriet cilni **Access**
2. Pievienojiet lomas vai grupas, kuru dalībnieki var izmantot digna
3. Noklikšķiniet **Save**

!!! note "Nepiešķirti lietotāji tiek atraidīti pēc pieteikšanās"

    Tāpat kā lielākā daļa pakalpojumu sniedzēju, OneLogin vispirms autentificē lietotāju un tikai pēc tam pārbauda tiesības. Nepiešķirts lietotājs veiksmīgi piesakās un pēc tam tiek atraidīts, kas izskatās pēc digna kļūdas, nevis piekļuves kontroles lēmuma.

---

## 6. solis: Izveidot discovery URL

Ievietojiet savu OneLogin apakšdomēnu:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Piemēram:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "/2 ir API versija"

    Pašreizējā OneLogin OIDC implementācija atrodas zem `/oidc/2/`. Vecākā dokumentācijā redzams `/oidc/` bez versijas, kas norāda uz izbeigto pirmo versiju. Šaubu gadījumā pārbaudiet **Issuer URL** cilnē SSO — discovery URL ir issuer plus `/.well-known/openid-configuration`.

---

## 7. solis: Konfigurēt digna

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
[oidc_clients.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

Abos failos `key` vērtībai jāsakrīt — šeit `onelogin`.

---

## 8. solis: Testēt

Restartējiet backend un web serveri, pēc tam atveriet dashboard. Pilnu pārbaudes sarakstu skatiet sadaļā [Pieteikšanās testēšana](overview.md#testing-login).

---

## OneLogin problēmu novēršana

### redirect_uri did not match

Callback URL trūkst laukā **Configuration → Redirect URI's**, vai arī ieraksti tika atdalīti ar komatiem, nevis jaunām rindām.

### invalid_client tokena solī

**Token Endpoint → Authentication Method** ir iestatīts uz *None*, vai arī klienta slepenā atslēga failā `config.toml` ir novecojusi. Parādiet slepeno atslēgu cilnē **SSO** un salīdziniet.

### Lietotne lietotājiem neparādās

Cilnē **Access** nevienai lomai vai grupai nav piešķirta piekļuve.

### 404 pie discovery URL

Apakšdomēns ir nepareizs, vai arī URL trūkst `/oidc/2/`. Salīdziniet ar **Issuer URL**, kas redzams cilnē SSO.

---

## Skatīt arī

- [Single Sign-On pārskats](overview.md) — konfigurācijas atsauce, testēšana un vispārīga problēmu novēršana
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)