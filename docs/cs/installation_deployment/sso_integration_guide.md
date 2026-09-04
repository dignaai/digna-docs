---
title: Integrace Single Sign-On (SSO) | digna Dokumentace
description: Krok za krokem průvodce konfigurací Single Sign-On (SSO) pro digna pomocí OpenID Connect (OIDC). Pokrývá konfiguraci dashboardu a backendu, testování, odstraňování problémů a podporované identity providery včetně Microsoft Entra ID, Google Workspace a Okta.
image: /assets/logo_square.png
keywords:
  - digna sso
  - single sign-on
  - oidc integration
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta integration
  - enterprise authentication
lang: cs
robots: index, follow
og_title: digna Integrace Single Sign-On (SSO)
og_description: Konfigurujte Single Sign-On pro digna pomocí OpenID Connect. Krok za krokem nastavení pro Microsoft Entra ID, Google Workspace, Okta a další identity providery podporující OIDC.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Průvodce integrací Single Sign-On

---

## Obsah

1. [Úvod a přehled](#introduction-and-overview)
2. [Kroky konfigurace](#configuration-steps)
3. [Konfigurace dashboardu](#dashboard-configuration)
4. [Konfigurace backendu](#backend-configuration)
5. [Testování přihlášení](#testing-login)
6. [Odstraňování problémů](#troubleshooting)
7. [Podporovaní provideri](#supported-providers)

---

## Úvod a přehled {: #introduction-and-overview }

Tento průvodce poskytuje krok za krokem instrukce pro integraci Single Sign-On (SSO) s platformou digna pomocí **OpenID Connect (OIDC)**.

### Co je SSO?

Single Sign-On umožňuje uživatelům bezpečně se přihlásit do digna pomocí jejich podnikových přihlašovacích údajů přes externí identity providery. Uživatelé se mohou autentizovat pomocí firemních přihlašovacích údajů místo správy samostatných hesel pro digna.

### Jak to funguje

SSO v digna je implementováno pomocí protokolu OIDC. Více identity providerů lze nakonfigurovat paralelně úpravou dvou klíčových konfiguračních souborů:

- **`dashboard_config.toml`** — Řídí rozhraní přihlášení na frontendu
- **`config.toml`** — Konfiguruje OIDC připojení na backendu

### Podporovaní provideri {: #supported-providers-overview }

Příklady v tomto průvodci používají **Microsoft** a **Google**, ale **jakýkoli provider kompatibilní s OIDC** lze integrovat podle stejné struktury.

Běžní OIDC provideri zahrnují:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Další identity providery kompatibilní s OIDC

---

## Kroky konfigurace {: #configuration-steps }

Konfigurace SSO vyžaduje úpravy dvou souborů. Tato sekce vysvětluje, jak nakonfigurovat každý z nich.

### Přehled konfiguračních souborů

| Soubor | Umístění | Účel |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Rozhraní přihlášení na frontendu |
| **config.toml** | `/config.toml` | OIDC připojení na backendu |

Oba soubory musí být nakonfigurovány, aby SSO fungovalo správně.

---

## Konfigurace dashboardu {: #dashboard-configuration }

### Umístění souboru

```
dashboard/dashboard_config.toml
```

### Krok 1: Přidat OIDC providery

Přidejte položky do pole `[[login.oidc]]` pro každého identity providera, kterého chcete podporovat.

**Příklad s Microsoft a Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Krok 2: Konfigurace možností přihlášení

Určete, zda má být povoleno přihlášení pomocí hesla:

```toml
[login]
usePassword = true
```

### Konfigurační parametry

#### Sekce `[[login.oidc]]`

| Parametr | Typ | Povinné | Popis |
|---|---:|---:|---|
| `key` | string | Ano | Unikátní identifikátor pro OIDC připojení (musí odpovídat klíči v config.toml) |
| `label` | string | Ano | Text zobrazený na tlačítku přihlášení (např. "Login with Microsoft") |

#### Sekce `[login]`

| Parametr | Typ | Výchozí | Popis |
|---|---:|---:|---|
| `usePassword` | boolean | false | Povolit přihlášení pomocí hesla kromě SSO |

### Co znamená usePassword

**Pokud `usePassword = true`:**
- Na obrazovce přihlášení se zobrazí tlačítka SSO (např. "Login with Microsoft")
- Zobrazí se také pole pro uživatelské jméno a heslo
- Uživatelé se mohou autentizovat oběma způsoby
- Umožňuje hybridní nastavení, kde někteří uživatelé používají SSO a jiní hesla

**Pokud `usePassword = false` (nebo není uvedeno):**
- Na obrazovce přihlášení se zobrazí pouze tlačítka SSO
- Žádná pole pro uživatelské jméno/heslo
- K dispozici je pouze OIDC autentizace

> **Tip**
>
> Přihlášení pomocí hesla je dostupné pouze pro uživatele, kteří byli vytvořeni s hesly pomocí příkazu `digna user add` nebo přes dashboard.

### Kompletní příklad

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## Konfigurace backendu {: #backend-configuration }

### Umístění souboru

```
/config.toml
```

(Root adresář instalace digna)

### Krok 1: Přidat sekce pro OIDC providery

Každý provider musí mít samostatnou sekci `[oidc.<key>]`. Klíč musí odpovídat hodnotě `key` definované v `dashboard_config.toml`.

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
|---|---:|---:|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Ano | Client ID od identity providera | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Ano | Client secret od identity providera | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Ano | Callback URL po autentizaci | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Ano | OIDC konfigurační endpoint | `https://login.microsoftonline.com/...` |

> **Důležité**
>
> Nahraďte zástupné hodnoty (`<client_id>`, `<client_secret>`, `<tenant_id>`) skutečnými údaji z vývojářského portálu vašeho identity providera.

### Redirect URI

Redirect URI musí být stejná jako v konfiguraci vašeho identity providera:

```
http://localhost:5173/oidc/callback
```

Pokud je digna nasazeno na jiné doméně, upravte ji podle potřeby:
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

### Kontrolní seznam před testováním

Před testováním se ujistěte, že:

- [ ] `dashboard_config.toml` byl aktualizován o OIDC providery
- [ ] `config.toml` byl aktualizován o OIDC přihlašovací údaje
- [ ] Oba soubory byly uloženy
- [ ] Přihlašovací údaje jsou správné (client ID, client secret)
- [ ] Redirect URI odpovídá vaší URL nasazení
- [ ] Aplikace v identity provideru je nakonfigurována s redirect URI

### Kroky testování

#### Krok 1: Restartovat služby

Restartujte backend digna a webový server, aby se změny projevily.

**Pokud běží jako Windows služba:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Pokud běží manuálně:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Pokud používáte IIS nebo Tomcat:**
Restartujte službu vašeho webového serveru.

#### Krok 2: Otevřít dashboard

Otevřete digna dashboard ve vašem prohlížeči:

```
http://localhost:5173
```

(nebo vaši nakonfigurovanou URL dashboardu)

#### Krok 3: Ověřit tlačítka přihlášení

Zkontrolujte, že se zobrazí tlačítka pro přihlášení pro každého nakonfigurovaného providera:

- Mělo by být vidět tlačítko "Login with Microsoft"
- Mělo by být vidět tlačítko "Login with Google"
- (Pokud usePassword = true) Měla by být viditelná pole pro uživatelské jméno/heslo

Pokud se tlačítka nezobrazují:
- Zkontrolujte, že `dashboard_config.toml` byl uložen
- Zkontrolujte, že dashboard služba byla restartována
- Podívejte se do konzole prohlížeče (F12) pro chyby

#### Krok 4: Otestovat SSO přihlášení

Klikněte na jedno z SSO tlačítek (např. "Login with Microsoft"):

1. Měli byste být přesměrováni na přihlašovací stránku identity providera
2. Přihlaste se pomocí podnikových přihlašovacích údajů
3. Měli byste být přesměrováni zpět do digna
4. Měli byste být přihlášeni do digna

#### Krok 5: Ověřit vytvoření uživatele

Po úspěšném SSO přihlášení:

- Uživatel by měl být automaticky vytvořen v digna
- Uživatel by měl být přihlášen
- Profil uživatele by měl zobrazit údaje z identity providera
- Měli byste vidět digna dashboard

#### Krok 6: Otestovat přihlášení pomocí hesla (pokud povoleno)

Pokud `usePassword = true`:

1. Odhlaste se z digna
2. Na přihlašovací stránce zadejte uživatelské jméno a heslo
3. Měli byste se dokázat přihlásit pomocí hesla

---

## Odstraňování problémů {: #troubleshooting }

### Tlačítka přihlášení se nezobrazují

**Příznaky:**
- OIDC tlačítka pro přihlášení nejsou viditelná na přihlašovací stránce
- Vidíte pouze pole pro heslo (pokud je usePassword = true)

**Příčiny a řešení:**
1. Zkontrolujte, že `dashboard_config.toml` je ve složce `dashboard/`
2. Ověřte, že sekce `[[login.oidc]]` jsou přítomné a syntakticky správné
3. Restartujte dashboard službu
4. Vymažte cache prohlížeče (Ctrl+Shift+Delete nebo Cmd+Shift+Delete)
5. Zkontrolujte konzoli prohlížeče (F12 → záložka Console) pro chyby

---

### Chyba nesouladu Redirect URI

**Příznaky:**
- Po kliknutí na SSO tlačítko chyba o "redirect_uri mismatch"
- Chyba "The redirect URI is not registered"

**Příčiny a řešení:**
1. Ověřte `DIGNA_OIDC_REDIRECT_URI` v `config.toml` je správné
2. Zkontrolujte, že redirect URI je registrováno v nastavení identity providera
3. Ujistěte se, že oba URI používají identickou URL (včetně protokolu, domény a cesty)
4. Zkontrolujte překlepy v redirect URI
5. Pokud používáte HTTPS, ověřte platnost certifikátu

---

### Chyba neplatných přihlašovacích údajů klienta

**Příznaky:**
- Chyba "Invalid client ID or secret"
- Autentizace selže s chybou přihlašovacích údajů

**Příčiny a řešení:**
1. Ověřte, že `DIGNA_OIDC_CLIENT_ID` a `DIGNA_OIDC_CLIENT_SECRET` jsou správné
2. Ujistěte se, že nejsou přidané mezery nebo nechtěné speciální znaky
3. Zkontrolujte, že přihlašovací údaje neexpirují nebo nebyly odvolány
4. Restartujte backend službu po aktualizaci konfigurace
5. Zkontrolujte konzoli identity providera, zda jsou přihlašovací údaje aktivní

---

### Přihlášení se zasekává nebo vyprší časový limit

**Příznaky:**
- Po kliknutí na SSO tlačítko se nic neděje
- Vypršení časového limitu po několika sekundách
- Prohlížeč ukazuje "Failed to connect" nebo podobnou chybu

**Příčiny a řešení:**
1. Ověřte, že backend digna běží: `digna repo check`
2. Zkontrolujte síťové připojení k identity provideru
3. Ověřte, že `DIGNA_OIDC_CONFIGURATION_URL` je přístupné
4. Zkontrolujte pravidla firewallu pro povolení odchozích HTTPS spojení
5. Ověřte, že backend a dashboard se navzájem dosahují

---

### Uživatelé nejsou automaticky vytvořeni

**Příznaky:**
- SSO přihlášení proběhne úspěšně, ale uživatel není vytvořen v digna
- Po SSO přihlášení dojde k chybě oprávnění

**Příčiny a řešení:**
1. Ověřte, že OIDC konfigurace je správná
2. Zkontrolujte nastavení oprávnění uživatelů
3. Prohlédněte logy digna pro chybová hlášení
4. Restartujte backend službu
5. Kontaktujte support@digna.ai, pokud problém přetrvává

---

## Podporovaní provideri {: #supported-providers }

### Testováno a podporováno

Následující OIDC providery byly otestovány a jsou známy jako funkční:

| Provider | Konfigurační URL | Průvodce nastavením |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Ostatní OIDC provideri

Jakýkoli provider podporující OpenID Connect lze integrovat. Požadované informace:

- Client ID
- Client secret
- OpenID konfigurační URL (obvykle na `/.well-known/openid-configuration`)
- Podporované scope (typicky `openid profile email`)

Kontaktujte support@digna.ai, pokud potřebujete pomoc s integrací konkrétního providera.

---

## Doporučené postupy

DO:
- Používejte HTTPS v produkci (ne HTTP)
- Uchovávejte client secret bezpečně (pokud možno použijte environment proměnné)
- Periodicky rotujte tajné klíče
- Testujte nejprve v neprodukčním prostředí
- Dokumentujte, kteří provideri jsou nakonfigurováni
- Monitorujte logy přihlášení kvůli neobvyklé aktivitě
- Udržujte konfiguraci identity providera v syncu s konfigurací digna

DON'T:
- Neukládejte client secret do verzovacího systému
- Nepoužívejte HTTP redirect URI v produkci
- Nekonfigurujte více providerů se stejným klíčem
- Nenechávejte výchozí/testovací přihlašovací údaje v produkci
- Nezveřejňujte konfigurační soubory obsahující tajné údaje
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
