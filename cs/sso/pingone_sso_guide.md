# Nastavení SSO s PingOne

PingOne je kompatibilní s OIDC. Dvě jeho hodnoty vyžadují pozornost: **Environment ID** (ID prostředí), které se objevuje v každé URL koncového bodu, a **regionální doména**, která se liší mezi nájemci v Severní Americe, Evropě, Kanadě, Asii a Austrálii.

Tento průvodce pokrývá **stranu PingOne**: vytvoření aplikace a získání hodnot, které digna potřebuje. Strana digna — `dashboard_config.toml`, testování a odstraňování problémů — je stejná pro všechny poskytovatele a je popsána v [Přehledu Single Sign-On](overview.md).

---

## Než začnete

| Požadavek | Poznámky |
|---|---|
| **Role v PingOne** | Environment Admin nebo Identity Data Admin v cílovém prostředí |
| **Prostředí** | PingOne prostředí, ke kterému patří vaši uživatelé digna |
| **digna redirect URI** | URL, na kterou se uživatel vrací po přihlášení, např. `https://digna.yourdomain.com/oidc/callback` |

---

## Krok 1: Vytvoření aplikace

1. Přihlaste se do administrační konzole PingOne a vyberte své prostředí
2. Přejděte na **Applications → Applications**
3. Klikněte na tlačítko **+**
4. Zadejte `digna` jako **Application Name**
5. Vyberte **OIDC Web App**
6. Klikněte na **Save**

!!! warning "Vyberte OIDC Web App, ne Single-Page App"

    *Single-Page App* a *Native App* vytvoří veřejné klienty, kteří nemohou uchovávat tajný klíč. digna směňuje autorizační kód na svém backendu a potřebuje důvěrný typ **OIDC Web App**.

---

## Krok 2: Konfigurace Redirect URI

1. Otevřete kartu **Configuration** aplikace
2. Klikněte na ikonu tužky pro úpravu
3. Potvrďte, že **Response Type** je *Code* a **Grant Type** je *Authorization Code*
4. Do pole **Redirect URIs** zadejte callback URL digna:

```
https://digna.yourdomain.com/oidc/callback
```

5. Nastavte **Token Endpoint Authentication Method** na *Client Secret Post* nebo *Client Secret Basic*
6. Klikněte na **Save**

---

## Krok 3: Povolení aplikace

Na řádku aplikace nebo v panelu s detaily přepněte přepínač na **enabled**.

!!! warning "Nové aplikace začínají jako disabled"

    PingOne vytváří aplikace ve stavu disabled. Disabled aplikace způsobí chybu v autorizaci, která se nepřipomíná na tento přepínač, takže to stojí za kontrolu dříve, než začnete cokoli ladit.

---

## Krok 4: Udělení rozsahů (scopes)

1. Otevřete kartu **Resources**
2. Potvrďte, že `openid` je udělen, a přidejte `profile` a `email` ze zdroje **OpenID Connect**
3. Klikněte na **Save**

---

## Krok 5: Přiřazení uživatelů

1. Otevřete kartu **Access**
2. Přidejte populaci nebo skupiny, jejichž členové mohou používat digna
3. Klikněte na **Save**

---

## Krok 6: Získání pověření a ID prostředí

Na kartě **Configuration** rozbalte **General**:

- **Client ID** → bude `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → bude `DIGNA_OIDC_CLIENT_SECRET` (klikněte na ikonu oka)
- **Environment ID** → vloží se do discovery URL

Na téže kartě je uveden i hotový **OIDC Discovery Endpoint**, který můžete zkopírovat přímo místo ručního sestavování.

---

## Krok 7: Sestavení Discovery URL

Nahraďte environment ID a doménu podle vašeho regionu:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Region | Doména |
|---|---|
| Severní Amerika | `auth.pingone.com` |
| Evropa | `auth.pingone.eu` |
| Kanada | `auth.pingone.ca` |
| Asie a Pacifik | `auth.pingone.asia` |
| Austrálie | `auth.pingone.com.au` |

Pro evropské prostředí:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Zkopírujte to místo psaní"

    Regionální doména je nejčastější chybou při integraci PingOne a chybný region vrátí 404 místo srozumitelné zprávy. Použijte hodnotu **OIDC Discovery Endpoint** z Kroku 6.

---

## Krok 8: Konfigurace digna

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
[oidc.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

Hodnota `key` v obou souborech se musí shodovat — `pingone` zde.

---

## Krok 9: Testování

Restartujte backend a webový server, pak otevřete dashboard. Kompletní kontrolní seznam najdete v [Testování přihlášení](overview.md#testing-login).

---

## Řešení problémů s PingOne

### 404 na Discovery URL

Regionální doména nebo environment ID jsou nesprávné. Porovnejte s **OIDC Discovery Endpoint** zobrazeným na kartě Configuration aplikace.

### NOT_FOUND nebo aplikace je disabled

Přepínač aplikace z Kroku 3 je stále vypnutý.

### Nesoulad Redirect URI

PingOne porovnává celý řetězec. Zkontrolujte **Configuration → Redirect URIs** kvůli koncovému lomítku nebo rozdílu ve schématu.

### Přihlášení uspěje, ale do digna nedorazí claim s e-mailem

Na kartě **Resources** nebyly uděleny scopes `email` a `profile`.

### Uživatel nevidí aplikaci

Na kartě **Access** nebyla žádné populace nebo skupiny udělena přístup.

---

## Viz také

- [Přehled Single Sign-On](overview.md) — referenční konfigurace, testování a obecné řešení problémů
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)