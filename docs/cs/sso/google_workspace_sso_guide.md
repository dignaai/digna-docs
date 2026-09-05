---
title: Google Workspace SSO – Integrace Single Sign-On | Dokumentace digna
description: Nakonfigurujte Single Sign-On pro digna s použitím Google Workspace a OpenID Connect — obrazovka souhlasu OAuth, OAuth client ID, autorizované redirect URI a odpovídající konfigurace digna.
image: /assets/logo_square.png
keywords: digna sso, google workspace sso, google oidc, oauth obrazovka souhlasu, openid connect, firemní autentizace
---

# Nastavení SSO pro Google Workspace

Platforma identity Google je kompatibilní s OIDC a používá jednu dobře známou discovery URL pro každého zákazníka, takže jediné hodnoty závislé na organizaci jsou client ID a secret.

Tento návod pokrývá **stranu Google**: vytvoření OAuth klienta a získání hodnot, které digna potřebuje. Strana digna — `dashboard_config.toml`, testování a řešení problémů — je stejná pro všechny poskytovatele a je popsána v [Přehled Single Sign-On](overview.md).

---

## Než začnete

| Požadavek | Poznámky |
|---|---|
| **Google Cloud project** | Jakýkoli projekt ve stejné organizaci jako vaše doména Workspace |
| **Role** | Editor nebo Owner v projektu |
| **digna redirect URI** | URL, na kterou se uživatelé vrátí po přihlášení, např. `https://digna.yourdomain.com/oidc/callback` |

---

## Krok 1: Konfigurace obrazovky souhlasu OAuth

Google nevydá přihlašovací údaje, dokud obrazovka souhlasu neexistuje.

1. Otevřete [Google Cloud Console](https://console.cloud.google.com) a vyberte svůj projekt
2. Přejděte na **APIs & Services → OAuth consent screen**
3. Zvolte typ uživatele:
   - **Internal** — přihlásit se mohou pouze účty ve vaší doméně Workspace. Doporučeno.
   - **External** — pokusit se přihlásit může kterýkoli Google účet.
4. Vyplňte název aplikace, e-mail podpory uživatelů a e-mail kontaktní osoby vývojáře
5. V kroku **Scopes** přidejte `openid`, `.../auth/userinfo.email` a `.../auth/userinfo.profile`
6. Uložte

!!! warning "External Apps Must Be Published"

    Obrazovka souhlasu nastavená jako **External** začne ve stavu *Testing*, kde se mohou přihlásit pouze účty explicitně přidané do seznamu testovacích uživatelů. Ostatní uvidí hlášení „digna has not completed the Google verification process“. Buď přepněte aplikaci na **In production** v části **Publishing status**, nebo použijte **Internal** — to nemá toto omezení a je správnou volbou pro nasazení v rámci Workspace.

---

## Krok 2: Vytvoření OAuth klienta

1. Přejděte na **APIs & Services → Credentials**
2. Klikněte na **Create Credentials → OAuth client ID**
3. Nastavte **Application type** na **Web application**
4. Pojmenujte ho, např. `digna`
5. Pod **Authorized redirect URIs** klikněte **Add URI** a zadejte:

```
https://digna.yourdomain.com/oidc/callback
```

6. Klikněte **Create**

!!! note "Authorized JavaScript Origins Are Not Needed"

    digna směňuje autorizační kód na backendu, ne v prohlížeči, takže pole **Authorized JavaScript origins** může zůstat prázdné. Důležitá je pouze redirect URI.

---

## Krok 3: Získání přihlašovacích údajů

Dialog, který se zobrazí po vytvoření, ukazuje:

- **Client ID** — končí na `.apps.googleusercontent.com` → stane se `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → stane se `DIGNA_OIDC_CLIENT_SECRET`

Obě hodnoty zůstanou později dostupné na stránce s detailem přihlašovacích údajů, na rozdíl od většiny jiných poskytovatelů.

---

## Krok 4: Discovery URL

Google používá jedno discovery URL pro všechny zákazníky — není nic, co byste měli nahrazovat:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Krok 5: Konfigurace digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Přihlásit se přes Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

Hodnota `key` v obou souborech se musí shodovat — zde `google`.

---

## Krok 6: Testování

Restartujte backend a webový server, potom otevřete dashboard. Kompletní kontrolní seznam najdete v [Testování přihlášení](overview.md#testing-login).

---

## Řešení problémů s Google Workspace

### Error 400: redirect_uri_mismatch

URI v `DIGNA_OIDC_REDIRECT_URI` není v seznamu **Authorized redirect URIs**, nebo se liší koncovým lomítkem či schématem. Google na chybové stránce ukazuje URI, které obdržel — porovnejte jej znak po znaku se zaregistrovanou hodnotou.

### This App Is Blocked / Has Not Completed Verification

Obrazovka souhlasu je **External** a je stále ve stavu *Testing*. Publikujte ji, nebo přepněte aplikaci na **Internal**.

### Access Blocked: Authorization Error

Účet, který se pokouší přihlásit, je mimo vaši doménu Workspace zatímco je obrazovka souhlasu nastavena jako **Internal**. To je zamýšlené chování — internal aplikace přijímají jen účty v organizaci.

### Changes Take Several Minutes

Google propaguje změny přihlašovacích údajů a obrazovky souhlasu asynchronně. Nově přidané redirect URI může trvat několik minut, než se projeví; pokud se změna zdá ignorována, počkejte a zkuste to znovu předtím, než začnete zjišťovat další příčiny.

---

## Viz také

- [Přehled Single Sign-On](overview.md) — referenční konfigurace, testování a obecné řešení problémů
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)