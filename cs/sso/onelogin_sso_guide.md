# Nastavení SSO s OneLogin

OneLogin je kompatibilní s OIDC. Jeho odlišnou vlastností je, že typ konektoru se vybírá z katalogu při vytváření aplikace a později ho nelze změnit.

Tento návod pokrývá **stranu OneLogin**: vytvoření aplikace a sesbírání hodnot, které digna potřebuje. Strana digna — `dashboard_config.toml`, testování a řešení problémů — je stejná pro všechny poskytovatele a je popsána v [Přehledu Single Sign-On](overview.md).

---

## Než začnete

| Požadavek | Poznámky |
|---|---|
| **Role v OneLogin** | Vlastník účtu nebo administrátor oprávněný přidávat aplikace |
| **Subdoména** | např. `yourcompany.onelogin.com` |
| **digna redirect URI** | URL, na kterou se uživatel vrací po přihlášení, např. `https://digna.yourdomain.com/oidc/callback` |

---

## Krok 1: Vytvořte OIDC aplikaci

1. Přihlaste se do administrátorského portálu OneLogin
2. Přejděte na **Applications → Applications**
3. Klikněte na **Add App**
4. Vyhledejte `OpenId Connect` a vyberte konektor **OpenId Connect (OIDC)**
5. Nastavte **Display Name** na `digna`
6. Klikněte na **Save**

!!! warning "Typ konektoru je po vytvoření pevně daný"

    OneLogin má samostatné položky v katalogu pro SAML a OIDC a aplikaci nelze z jednoho typu na druhý převést. Pokud omylem zvolíte SAML konektor, smažte aplikaci a přidejte ji znovu — neexistuje žádné nastavení pro přepnutí protokolu.

---

## Krok 2: Nakonfigurujte Redirect URI

1. Otevřete záložku **Configuration**
2. Do pole **Redirect URI's** zadejte callback URL pro digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. Volitelně nastavte **Post Logout Redirect URIs** na URL vaší administrace
4. Klikněte na **Save**

!!! note "Jedna URI na řádek"

    Na rozdíl od poskytovatelů, kteří očekávají seznam oddělený čárkami, pole OneLogin **Redirect URI's** přijímá jednu URI na řádek.

---

## Krok 3: Nastavte typ aplikace a autentizační metodu

1. Otevřete záložku **SSO**
2. Potvrďte, že **Application Type** je *Web*
3. Nastavte **Token Endpoint → Authentication Method** na *POST* (`client_secret_post`) nebo *Basic* (`client_secret_basic`)

!!! warning "Nevolte None"

    Nastavení autentizační metody na *None* udělá z aplikace veřejného klienta bez tajného klíče a výměna kódu na backendu digna bude odmítnuta. Buď POST nebo Basic funguje.

---

## Krok 4: Získání přihlašovacích údajů

Stále v záložce **SSO**:

- **Client ID** → se stane `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → se stane `DIGNA_OIDC_CLIENT_SECRET` (klikněte na **Show client secret**)

Stránka také zobrazuje **Issuer URL**, která potvrzuje discovery URL v dalším kroku.

---

## Krok 5: Přiřaďte uživatele

1. Otevřete záložku **Access**
2. Přidejte role nebo skupiny, jejichž členové mohou používat digna
3. Klikněte na **Save**

!!! note "Nepřiřazení uživatelé jsou po přihlášení zamítnuti"

    Stejně jako u většiny poskytovatelů, OneLogin nejprve autentizuje uživatele a až poté kontroluje nárok na přístup. Nepřiřazený uživatel se úspěšně přihlásí a následně je zamítnut, což se jeví jako chyba digna spíše než rozhodnutí o přístupu.

---

## Krok 6: Sestavte Discovery URL

Nahraďte svou OneLogin subdoménu:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Například:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip " /2/ je verze API"

    Aktuální implementace OIDC OneLoginu běží pod `/oidc/2/`. Starší dokumentace uvádí `/oidc/` bez verze, což ukazuje na ukončenou první verzi. Pokud si nejste jisti, zkontrolujte **Issuer URL** na záložce SSO — discovery URL je issuer plus `/.well-known/openid-configuration`.

---

## Krok 7: Nakonfigurujte digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Přihlásit se přes OneLogin"
```

### `config.toml`

```toml
[oidc.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

Hodnota `key` v obou souborech musí souhlasit — zde `onelogin`.

---

## Krok 8: Testování

Restartujte backend a webový server, poté otevřete administraci. Kompletní kontrolní seznam najdete v [Testování přihlášení](overview.md#testing-login).

---

## Řešení problémů s OneLogin

### `redirect_uri` se neshodovalo

Callback URL chybí v **Configuration → Redirect URI's**, nebo byly položky odděleny čárkami místo nových řádků.

### `invalid_client` v kroku tokenu

**Token Endpoint → Authentication Method** je nastaveno na *None*, nebo je klientský secret v `config.toml` zastaralý. Zobrazte tajemství na záložce **SSO** a porovnejte.

### Aplikace se neobjevuje uživatelům

Žádné role nebo skupina nebyly na záložce **Access** uděleny přístupu.

### 404 na Discovery URL

Subdoména je špatná, nebo URL postrádá `/oidc/2/`. Porovnejte s **Issuer URL** zobrazenou na záložce SSO.

---

## Viz také

- [Přehled Single Sign-On](overview.md) — referenční konfigurace, testování a obecné řešení problémů
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)