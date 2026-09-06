# SSO seadistamine Keycloakiga

Keycloak on ise majutatav, täielikult OIDC-ühilduv identiteedipakkuja. Kuna käitate seda ise, koostatakse discovery URL teie enda hosti nime ja realmi järgi, mitte teenusepakkuja domeeni alusel.

See juhend käsitleb **Keycloak’i poolt**: kliendi loomist ja väärtuste kogumist, mida digna vajab. digna pool — `dashboard_config.toml`, testimine ja tõrkeotsing — on sama iga pakkuja puhul ja on kirjeldatud [Single Sign-On ülevaates](overview.md).

---

## Enne alustamist

| Nõue | Märkused |
|---|---|
| **Keycloak versioon** | 17 või uuem kasutatavate URL-radade jaoks — vt märkust Sammus 4 |
| **Keycloak roll** | `realm-admin` sihtrealmil või serveri administraator |
| **Realm** | Realm, millele teie digna kasutajad kuuluvad, mitte tingimata `master` |
| **digna redirect URI** | URL, kuhu kasutajad peale sisselogimist naasevad, nt `https://digna.yourdomain.com/oidc/callback` |

---

## Samm 1: Valige realm

1. Avage Keycloak administraatori konsool
2. Kasutage vasakus ülanurgas realm-i valijat, et lülituda rea(l)mi, kus teie kasutajad asuvad

!!! warning "Ärge kasutage master realmi"

    `master` realm on mõeldud Keycloak’i enda haldamiseks. Rakenduste kliendid peaksid olema pühendatud realmis; digna paigutamine `master`-i annab selle kasutajatele tee Keycloak’i administratsioonikonsooli.

---

## Samm 2: Loo klient

1. Minge **Clients** ja klõpsake **Create client**
2. Konfigureerige:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — sellest saab `DIGNA_OIDC_CLIENT_ID`
3. Klõpsake **Next**
4. **Capability config** sammul lülitage **Client authentication** **On**
5. Jätke **Standard flow** lubatuks; teisi floowe pole vaja
6. Klõpsake **Next**

!!! warning "Client Authentication peab olema sisse lülitatud"

    Kui **Client authentication** on välja lülitatud, loob Keycloak *public* kliendi, millel puuduvad mingidki mandaadid — Step 4-s ei eksisteeri **Credentials** vahekaarti. digna vajab konfidentsiaalset klienti. See lüliti on võimalik muuta ka pärast kliendi loomist, kui vale valik tehti.

---

## Samm 3: Määra redirect URI

**Login settings** sammul (või hiljem **Settings** vahekaardil):

1. **Valid redirect URIs**: sisestage oma digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: jätke tühi või seadke `+`, et peegeldada redirect URI-sid
3. Klõpsake **Save**

!!! tip "Väldi tärnide (wildcard) kasutamist"

    Keycloak aktsepteerib mustreid nagu `https://digna.yourdomain.com/*`. Tärn võimaldab mis tahes teel sellel hostil saada autoriseerimiskoodi, seega eelistage täpset callback-URL-i.

---

## Samm 4: Koguge kliendi salaõnn

1. Avage **Credentials** vahekaart
2. Kinnitage, et **Client Authenticator** on *Client Id and Secret*
3. Kopeerige **Client secret** → saab `DIGNA_OIDC_CLIENT_SECRET`

Salajast võtit saab siit tulevikus uuesti vaadata ja vajadusel **Regenerate** abil genereerida.

---

## Samm 5: Koosta discovery URL

Asendage oma Keycloak host ja realmi nimi:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Näiteks:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 ja varasemad sisaldasid /auth"

    Enne Keycloak 17 olid kõik lõpp-punktid `/auth` prefiksi all:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Distributsioonid, mis kasutavad `KC_HTTP_RELATIVE_PATH=/auth`, säilitavad vana paigutuse ka uuemates versioonides. Kui URL ilma `/auth`-ta tagastab 404, proovige seda varianti.

Avage URL brauseris enne jätkamist. JSON-dokument kinnitab, et host ja realm on õiged.

---

## Samm 6: Konfigureeri digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Login with Keycloak"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

Mõlemas failis peab `key` kattuma — siin `keycloak`. Pane tähele, et see ei pea olema võrdne Keycloak’i **Client ID**-ga, kuigi sama hoidmine on kergem järgida.

---

## Samm 7: Testimine

Taaskäivitage backend ja veebiserver, seejärel avage dashboard. Täispunktide kontrollnimekirja jaoks vaadake [Sisselogimise testimine](overview.md#testing-login).

---

## Keycloak tõrkeotsing

### Vigane parameeter: redirect_uri

Callback-URL ei ole kaetud **Valid redirect URIs**-ga. Keycloak logib serverilogisse saadud URI, mis on kiireim viis täpse mittevastavuse nägemiseks.

### Credentials vahekaart puudub

Klient on public. Lülitage **Client authentication** sisse **Settings → Capability config** alt.

### 404 discovery URL-il

Võimalik, et realm on vale või deploy kasutab `/auth` prefiksit. Kontrollige realm-ide nimekirja administraatori konsoolis ja proovige mõlemat URL-i varianti.

### unauthorized_client või invalid_client

**Standard flow** on keelatud **Capability config** all, või salajane võti regeneriti Keycloak’is ilma `config.toml`-i värskendamata.

### Sertifikaadi vead backendist

Ise majutatav Keycloak, mis kasutab privaatset või ise allkirjastatud sertifikaati, ebaõnnestub digna väljaminev HTTPS-päring discovery URL-ile. Paigaldage väljastava CA sertifikaat masina usalduspoolele, kus jookseb digna backend.

---

## Vaata ka

- [Single Sign-On ülevaade](overview.md) — konfiguratsiooni viide, testimine ja üldine tõrkeotsing
- [Keycloak: Rakenduste turvamine](https://www.keycloak.org/docs/latest/securing_apps/)