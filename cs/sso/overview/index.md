# Přehled Single Sign-On

---

## Obsah

1. [Úvod a přehled](#introduction-and-overview)
2. [Průvodci pro poskytovatele](#provider-guides)
3. [Kroky konfigurace](#configuration-steps)
4. [Konfigurace dashboardu](#dashboard-configuration)
5. [Konfigurace backendu](#backend-configuration)
6. [Testování přihlášení](#testing-login)
7. [Odstraňování problémů](#troubleshooting)
8. [Podporovaní poskytovatelé](#supported-providers)

---

## Úvod a přehled {: #introduction-and-overview }

Tento průvodce poskytuje krok za krokem instrukce pro integraci Single Sign-On (SSO) s platformou digna pomocí **OpenID Connect (OIDC)**.

### Co je SSO?

Single Sign-On umožňuje uživatelům bezpečně se přihlásit do digna pomocí podnikových přihlašovacích údajů přes externí identity providery. Uživatelé se mohou autentizovat svými firemními účty místo správy samostatných hesel pro digna.

### Jak to funguje

SSO v digna je implementováno pomocí protokolu OIDC. Více identity providerů lze nakonfigurovat paralelně úpravou dvou klíčových konfiguračních souborů:

- **`dashboard_config.toml`** — Řídí frontend rozhraní pro přihlášení
- **`config.toml`** — Konfiguruje backend OIDC připojení

### Podporovaní poskytovatelé {: #supported-providers-overview }

Příklady v tomto průvodci používají **Microsoft** a **Google**, ale **jakýkoli poskytovatel kompatibilní s OIDC** může být integrován podle stejné struktury.

---

## Průvodci pro poskytovatele {: #provider-guides }

Každý poskytovatel vyžaduje čtyři stejné hodnoty — client ID, client secret, redirect URI a discovery URL — ale každý je umisťuje na jiném místě v administraci a někteří mají specifický krok, který ostatní nemají. Níže uvedené průvodce pokrývají tuto část práce; tato stránka pokrývá část týkající se digna, která je pro všechny stejné.

| Poskytovatel | Průvodce | Stojí za to vědět |
|---|---|---|
| **AD FS** | [Nastavení SSO s AD FS](adfs_sso_guide.md) | Self-hosted; jediný poskytovatel zde, kde ovládáte token service |
| **Auth0** | [Nastavení SSO s Auth0](auth0_sso_guide.md) | Discovery URL je per-tenant a vlastní domény ho mění |
| **Google Workspace** | [Nastavení SSO s Google Workspace](google_workspace_sso_guide.md) | Úplné zveřejnění obrazovky souhlasu je nutné, aby se mohli přihlásit uživatelé mimo testovací režim |
| **Keycloak** | [Nastavení SSO s Keycloak](keycloak_sso_guide.md) | Self-hosted; discovery URL je per-realm |
| **Microsoft Entra ID** | [Nastavení SSO s Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | Tenant ID se objevuje v discovery URL; tajné klíče vyprší |
| **Okta** | [Nastavení SSO s Okta](okta_sso_guide.md) | Volba autorizačního serveru mění discovery URL |
| **OneLogin** | [Nastavení SSO s OneLogin](onelogin_sso_guide.md) | Typ OIDC aplikace musí být zvolen při vytvoření a nelze jej změnit |
| **PingOne** | [Nastavení SSO s PingOne](pingone_sso_guide.md) | Environment ID se objevuje v discovery URL |

Jakýkoli jiný provider kompatibilní s OIDC funguje stejným způsobem — viz [Jiní OIDC poskytovatelé](#supported-providers).

---

## Kroky konfigurace {: #configuration-steps }

Konfigurace SSO vyžaduje aktualizace dvou souborů. Tato sekce vysvětluje, jak nakonfigurovat každý z nich.

### Přehled konfiguračních souborů

| Soubor | Umístění | Účel |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend rozhraní pro přihlášení |
| **config.toml** | `/config.toml` | Backend OIDC připojení |

Oba soubory musí být nakonfigurovány, aby SSO fungovalo správně.

---

## Konfigurace dashboardu {: #dashboard-configuration }

### Umístění souboru

```
dashboard/dashboard_config.toml
```

### Krok 1: Přidat OIDC poskytovatele

Přidejte položky pod pole `[[login.oidc]]` pro každého identity providera, kterého chcete podporovat.

**Příklad s Microsoft a Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Přihlásit se přes Microsoft"

[[login.oidc]]
key = "google"
label = "Přihlásit se přes Google"
```

### Krok 2: Nakonfigurovat možnosti přihlášení

Určete, zda má být povoleno přihlášení pomocí hesla:

```toml
[login]
usePassword = true
```

### Konfigurační parametry

#### Sekce `[[login.oidc]]`

| Parametr | Typ | Povinné | Popis |
|---|---|---|---|
| `key` | string | Ano | Unikátní identifikátor pro OIDC připojení (musí odpovídat klíči v config.toml) |
| `label` | string | Ano | Text zobrazený na tlačítku přihlášení (např. "Přihlásit se přes Microsoft") |

#### Sekce `[login]`

| Parametr | Typ | Výchozí | Popis |
|---|---|---|---|
| `usePassword` | boolean | false | Umožnit přihlášení pomocí hesla kromě SSO |

### Porozumění usePassword

**Pokud `usePassword = true`:**
- Na přihlašovací obrazovce se zobrazí tlačítka SSO (např. "Přihlásit se přes Microsoft")
- Na přihlašovací obrazovce se také zobrazí pole pro uživatelské jméno a heslo
- Uživatelé se mohou autentizovat oběma způsoby
- Umožňuje hybridní nastavení, kde někteří uživatelé používají SSO a jiní hesla

**Pokud `usePassword = false` (nebo vynecháno):**
- Přihlašovací obrazovka zobrazí pouze tlačítka SSO
- Žádná pole pro uživatelské jméno/heslo
- K dispozici je pouze OIDC autentizace

!!! tip "Tip"

    Přihlášení pomocí hesla je dostupné pouze pro uživatele, kteří byli vytvořeni s hesly pomocí příkazu `digna user add` nebo přes dashboard.

### Kompletní příklad

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Přihlásit se přes Microsoft"

[[login.oidc]]
key = "google"
label = "Přihlásit se přes Google"

[[login.oidc]]
key = "okta"
label = "Přihlásit se přes Okta"
```

---

## Konfigurace backendu {: #backend-configuration }

### Umístění souboru

```
/config.toml
```

(Root adresář instalace digna)

### Krok 1: Přidat sekce pro OIDC poskytovatele

Každý poskytovatel musí mít dedikovanou sekci `[oidc.<key>]`. Klíč musí odpovídat `key` definovanému v `dashboard_config.toml`.

### Konfigurace pro Microsoft

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Konfigurace pro Google

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Konfigurační parametry

| Parametr | Typ | Povinné | Popis | Příklad |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Ano | Client ID od identity providera | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Ano | Client secret od identity providera | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Ano | Callback URL po autentizaci | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Ano | OIDC konfigurační endpoint | `https://login.microsoftonline.com/...` |

!!! warning "Důležité"

    Nahraďte zástupné hodnoty (`<client_id>`, `<client_secret>`, `<tenant_id>`) skutečnými údaji z vývojářského portálu vašeho identity providera.

### Redirect URI

Redirect URI musí být stejná i v konfiguraci vašeho identity providera:

```
http://localhost:5173/oidc/callback
```

Pokud je digna nasazeno na jiné doméně, aktualizujte odpovídajícím způsobem:
- Lokálně: `http://localhost:5173/oidc/callback`
- Produkce: `https://digna.yourdomain.com/oidc/callback`

### Kompletní příklad

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

## Testování přihlášení {: #testing-login }

Po dokončení konfigurace ověřte, že SSO funguje správně.

### Před-testovací kontrolní seznam

Před testováním se ujistěte:

- [ ] `dashboard_config.toml` byl aktualizován o OIDC poskytovatele
- [ ] `config.toml` byl aktualizován s OIDC údaji
- [ ] Oba soubory byly uloženy
- [ ] Údaje jsou správné (client ID, client secret)
- [ ] Redirect URI odpovídá URL vašeho nasazení
- [ ] Aplikace u identity providera je nakonfigurována s redirect URI

### Kroky testování

#### Krok 1: Restart služeb

Restartujte backend digna a webový server, aby se změny projevily.

**Pokud běží jako služba ve Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Pokud běží jako služba na Linuxu nebo macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Pokud běží ručně:**
```bash
digna serve --address localhost --port 8082
```

**Restartujte také webový server** — IIS nebo Tomcat na Windows, nginx nebo Apache na Linuxu a macOS.

#### Krok 2: Otevřete dashboard

Otevřete digna dashboard ve vašem prohlížeči:

```
http://localhost:5173
```

(nebo vámi nakonfigurované URL dashboardu)

#### Krok 3: Ověřte tlačítka pro přihlášení

Zkontrolujte, že se zobrazí tlačítka pro přihlášení pro každého nakonfigurovaného poskytovatele:

- Mělo by se zobrazit tlačítko "Přihlásit se přes Microsoft"
- Mělo by se zobrazit tlačítko "Přihlásit se přes Google"
- (Pokud usePassword = true) Měla by se zobrazit pole pro uživatelské jméno/heslo

Pokud se tlačítka nezobrazí:
- Zkontrolujte, že `dashboard_config.toml` byl uložen
- Zkontrolujte, že dashboard služba byla restartována
- Zkontrolujte konzoli prohlížeče (F12) pro chyby

#### Krok 4: Otestujte SSO přihlášení

Klikněte na jedno z SSO tlačítek (např. "Přihlásit se přes Microsoft"):

1. Měli byste být přesměrováni na přihlašovací stránku identity providera
2. Přihlaste se pomocí vašich firemních přihlašovacích údajů
3. Měli byste být přesměrováni zpět do digna
4. Měli byste být přihlášeni do digna

#### Krok 5: Ověřte vytvoření uživatele

Po úspěšném SSO přihlášení:

- Uživatelský účet by měl být automaticky vytvořen v digna
- Uživatel by měl být přihlášen
- Profil uživatele by měl zobrazit údaje z identity providera
- Měli byste vidět digna dashboard

#### Krok 6: Otestujte přihlášení heslem (pokud povoleno)

Pokud `usePassword = true`:

1. Odhlaste se z digna
2. Na přihlašovací stránce zadejte uživatelské jméno a heslo
3. Měli byste se být schopni přihlásit pomocí hesla

---

## Odstraňování problémů {: #troubleshooting }

### Tlačítka pro přihlášení se nezobrazují

**Příznaky:**
- OIDC tlačítka se nezobrazují na přihlašovací stránce
- Vidíte pouze pole pro heslo (pokud usePassword = true)

**Příčiny a řešení:**
1. Zkontrolujte, že `dashboard_config.toml` je v adresáři `dashboard/`
2. Ověřte, že sekce `[[login.oidc]]` jsou přítomny a syntax je správná
3. Restartujte dashboard službu
4. Vymažte cache prohlížeče (Ctrl+Shift+Delete nebo Cmd+Shift+Delete)
5. Zkontrolujte konzoli prohlížeče (F12 → Console) pro chyby

---

### Chyba shody Redirect URI

**Příznaky:**
- Po kliknutí na SSO tlačítko chyba ohledně "redirect_uri mismatch"
- Chyba "The redirect URI is not registered"

**Příčiny a řešení:**
1. Ověřte, že `DIGNA_OIDC_REDIRECT_URI` v `config.toml` je správné
2. Ověřte, že redirect URI je zaregistrováno v nastavení identity providera
3. Ujistěte se, že oba používají identické URL (včetně protokolu, domény a cesty)
4. Zkontrolujte překlepy v redirect URI
5. Pokud používáte HTTPS, ujistěte se, že certifikát je platný

---

### Chyba neplatných klientských údajů

**Příznaky:**
- Chyba "Invalid client ID or secret"
- Autentizace selže kvůli chybným údajům

**Příčiny a řešení:**
1. Ověřte `DIGNA_OIDC_CLIENT_ID` a `DIGNA_OIDC_CLIENT_SECRET` jsou správné
2. Ujistěte se, že nejsou přidané nepovolené mezery nebo znaky
3. Zkontrolujte, že údaje nevypršely nebo nebyly zrušeny
4. Restartujte backend službu po aktualizaci konfigurace
5. Zkontrolujte konzoli identity providera, že jsou údaje aktivní

---

### Přihlášení se zasekne nebo vyprší čas

**Příznaky:**
- Kliknutí na SSO tlačítko nic neudělá
- Po několika sekundách vyprší čas
- Prohlížeč zobrazí "Failed to connect" nebo podobně

**Příčiny a řešení:**
1. Ověřte, že backend digna běží: `digna repo check`
2. Zkontrolujte síťové připojení k identity providerovi
3. Ověřte, že `DIGNA_OIDC_CONFIGURATION_URL` je dostupné
4. Zkontrolujte pravidla firewallu, že povolují odchozí HTTPS spojení
5. Ověřte, že backend a dashboard se navzájem dosáhnou

---

### Uživatelé se nevytvářejí automaticky

**Příznaky:**
- SSO přihlášení uspěje, ale uživatel není vytvořen v digna
- Po SSO přihlášení se objeví chyba oprávnění

**Příčiny a řešení:**
1. Ověřte, že OIDC konfigurace je správná
2. Zkontrolujte nastavení oprávnění uživatelů
3. Prohlédněte logy digna pro chybové zprávy
4. Restartujte backend službu
5. Pokud problém přetrvává, kontaktujte support@digna.ai

---

## Podporovaní poskytovatelé {: #supported-providers }

### Testováno a podporováno

Následující OIDC poskytovatelé byli testováni a jsou známi, že fungují:

| Poskytovatel | Konfigurační URL | Průvodce nastavením |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Nastavení SSO s AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Nastavení SSO s Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Nastavení SSO s Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Nastavení SSO s Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Nastavení SSO s Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Nastavení SSO s Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Nastavení SSO s OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Nastavení SSO s PingOne](pingone_sso_guide.md) |

### Jiní OIDC poskytovatelé

Jakýkoli provider, který podporuje OpenID Connect, lze integrovat. Požadované informace:

- Client ID
- Client secret
- OpenID konfigurační URL (obvykle na `/.well-known/openid-configuration`)
- Podporované scope (typicky `openid profile email`)

Kontaktujte support@digna.ai, pokud potřebujete pomoc s integrací konkrétního providera.

---

## Nejlepší praktiky

**DĚLAT:**
- V produkci používejte HTTPS (ne HTTP)
- Uchovávejte client secret bezpečně (pokud možno v proměnných prostředí)
- Pravidelně rotujte tajné klíče
- Nejprve testujte v neprodukčním prostředí
- Dokumentujte, kteří poskytovatelé jsou nakonfigurováni
- Monitorujte přihlašovací logy pro neobvyklou aktivitu
- Držte konfiguraci identity providera v synchronizaci s konfigurací digna

**NEDĚLAT:**
- Neukládejte client secrets do verzovacího systému
- Nepoužívejte HTTP redirect URI v produkci
- Nekonfigurujte více poskytovatelů se stejným klíčem
- Nenechávejte výchozí/testovací přihlašovací údaje v produkci
- Nezveřejňujte konfigurační soubory obsahující tajné klíče
- Nemíchejte vývojové a produkční přihlašovací údaje

---

## Podpora

Potřebujete pomoc s konfigurací SSO?

- **Email:** support@digna.ai
- **Dokumentace:** https://docs.digna.ai
- **Web:** https://www.digna.ai

---

**Poslední aktualizace:** 30. srpna 2026  
**Verze:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**