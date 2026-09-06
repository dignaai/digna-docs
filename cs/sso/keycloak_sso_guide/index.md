# Nastavení SSO s Keycloak

Keycloak je samostatně provozovaný poskytovatel identity plně kompatibilní s OIDC. Protože jej provozujete sami, discovery URL se sestavuje z vaší vlastní domény a názvu realm, nikoli z domény poskytovatele.

Tento průvodce pokrývá **stranu Keycloak**: vytvoření klienta a získání hodnot, které digna potřebuje. Strana digna — `dashboard_config.toml`, testování a řešení problémů — je stejná pro každého poskytovatele a je popsána v [Přehled Single Sign-On](overview.md).

---

## Než začnete

| Požadavek | Poznámky |
|---|---|
| **Keycloak version** | 17 nebo novější pro zde použité cesty URL — viz poznámka v Kroku 4 |
| **Keycloak role** | `realm-admin` na cílovém realm, nebo administrátor serveru |
| **Realm** | Realm, do kterého patří vaši digna uživatelé, nemusí to být nutně `master` |
| **digna redirect URI** | URL, kam se uživatelé vrací po přihlášení, např. `https://digna.yourdomain.com/oidc/callback` |

---

## Krok 1: Vyberte realm

1. Otevřete Keycloak admin console
2. V levém horním rohu použijte volbu pro výběr realm a přepněte na realm, ve kterém jsou vaši uživatelé

!!! warning "Nepoužívejte realm master"

    Realm `master` je určen pro správu samotného Keycloak. Aplikační klienti patří do samostatného realm; umístění digna do `master` by jeho uživatelům poskytlo přístup do administrační konzole Keycloak.

---

## Krok 2: Vytvoření klienta

1. Přejděte na **Clients** a klikněte na **Create client**
2. Nakonfigurujte:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — to se stane `DIGNA_OIDC_CLIENT_ID`
3. Klikněte **Next**
4. Na kroku **Capability config** zapněte **Client authentication** (nastavte na **On**)
5. Nechte povolený **Standard flow**; ostatní flow nejsou potřeba
6. Klikněte **Next**

!!! warning "Client Authentication musí být zapnuto"

    Pokud je **Client authentication** vypnuto, Keycloak vytvoří *public* klienta, který nemá vůbec žádné přihlašovací údaje — na kartě **Credentials** v Kroku 4 nebude nic k dispozici. digna potřebuje confidential klienta. Tento přepínač lze po vytvoření změnit, pokud jste udělali chybu.

---

## Krok 3: Nastavte Redirect URI

Na kroku **Login settings** (nebo později na kartě **Settings**):

1. **Valid redirect URIs**: zadejte callback URL vašeho digna:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: nechte prázdné, nebo nastavte na `+` pro zrcadlení redirect URIs
3. Klikněte **Save**

!!! tip "Vyhněte se zástupným znakům"

    Keycloak přijímá vzory jako `https://digna.yourdomain.com/*`. Zástupný znak umožní jakékoli cestě na tomto hostu přijmout autorizační kód, proto preferujte přesnou callback URL.

---

## Krok 4: Získejte klientské tajemství

1. Otevřete kartu **Credentials**
2. Potvrďte, že **Client Authenticator** je *Client Id and Secret*
3. Zkopírujte **Client secret** → stane se `DIGNA_OIDC_CLIENT_SECRET`

Tajné heslo zůstane zde dostupné a lze jej znovu vygenerovat pomocí **Regenerate**.

---

## Krok 5: Sestavte Discovery URL

Dosadíte svůj Keycloak host a název realm:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Například:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 a starší zahrnovaly /auth"

    Před Keycloak 17 se všechny endpointy nacházely pod prefixem `/auth`:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Distribuce, které nastaví `KC_HTTP_RELATIVE_PATH=/auth`, si ponechávají staré rozložení i na novějších verzích. Pokud URL bez `/auth` vrací 404, zkuste ji s `/auth`.

Otevřete URL v prohlížeči před pokračováním. JSON dokument potvrdí, že host a realm jsou správné.

---

## Krok 6: Nakonfigurujte digna

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

Hodnota `key` v obou souborech musí být stejná — zde `keycloak`. Poznamenejte, že nemusí být shodná s Keycloak **Client ID**, i když je snazší, když je to stejné.

---

## Krok 7: Testování

Restartujte backend a webový server, poté otevřete dashboard. Kompletní kontrolní seznam najdete v [Testování přihlášení](overview.md#testing-login).

---

## Řešení problémů s Keycloak

### Invalid parameter: redirect_uri

Callback URL není zahrnuta v **Valid redirect URIs**. Keycloak zapisuje URI, které obdržel, do serverového logu — to je nejrychlejší způsob, jak zjistit přesnou neshodu.

### Karta Credentials chybí

Klient je public. Zapněte **Client authentication** v **Settings → Capability config**.

### 404 na Discovery URL

Buď je špatný název realm, nebo nasazení používá prefix `/auth`. Zkontrolujte seznam realm v administrační konzoli a vyzkoušejte obě formy URL.

### unauthorized_client nebo invalid_client

**Standard flow** je vypnuté v **Capability config**, nebo bylo v Keycloak znovu vygenerováno tajemství bez aktualizace v `config.toml`.

### Chyby certifikátu z backendu

Samostatně provozovaný Keycloak s privátním nebo self-signed certifikátem způsobí selhání odchozího HTTPS volání digna na discovery URL. Nainstalujte vystavující CA do trust store stroje, na kterém běží digna backend.

---

## Viz také

- [Přehled Single Sign-On](overview.md) — referenční konfigurace, testování a obecné řešení problémů
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)