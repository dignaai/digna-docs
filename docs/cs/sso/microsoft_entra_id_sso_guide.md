---
title: Microsoft Entra ID SSO – integrace Single Sign-On | Dokumentace digna
description: Nakonfigurujte Single Sign-On pro digna pomocí Microsoft Entra ID (dříve Azure AD) přes OpenID Connect — registrace aplikace, přesměrovací URI, client secret, tenant ID a odpovídající konfigurace digna.
image: /assets/logo_square.png
keywords: digna sso, microsoft entra id, azure ad sso, oidc integrace, registrace aplikace, podnikové ověřování
---

# Nastavení SSO s Microsoft Entra ID

Microsoft Entra ID (dříve Azure Active Directory) je plně kompatibilní poskytovatel OIDC, takže se digna integruje přes standardní discovery endpoint.

Tento průvodce pokrývá **stranu Entra ID**: registraci aplikace a získání čtyř hodnot, které digna potřebuje. Strana digna — `dashboard_config.toml`, testování a řešení problémů — je stejná pro všechny poskytovatele a je popsána v [Single Sign-On Overview](overview.md).

---

## Než začnete

| Požadavek | Poznámky |
|---|---|
| **Role v Entra ID** | Application Administrator, Cloud Application Administrator nebo Global Administrator |
| **digna redirect URI** | URL, na kterou se uživatel vrací po přihlášení, např. `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | adresář, do kterého se vaši uživatelé přihlašují |

---

## Krok 1: Zaregistrujte aplikaci

1. Přihlaste se do [Microsoft Entra admin center](https://entra.microsoft.com)
2. Přejděte na **Identity → Applications → App registrations**
3. Klikněte na **New registration**
4. Konfigurace:
   - **Name**: `digna` (zobrazuje se uživatelům na obrazovce souhlasu)
   - **Supported account types**: *Accounts in this organizational directory only* pro nasazení v rámci jednoho tenantu
5. V části **Redirect URI** vyberte platformu **Web** a zadejte vaše callback URL pro digna:

```
https://digna.yourdomain.com/oidc/callback
```

6. Klikněte na **Register**

!!! warning "Důležité"

    Platforma musí být **Web**, ne *Single-page application*. digna vyměňuje autorizační kód ze serveru pomocí client secret, což typ platformy SPA neumožňuje.

---

## Krok 2: Získejte Client a Tenant ID

Na stránce **Overview** aplikace zkopírujte:

- **Application (client) ID** → bude `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → použije se v discovery URL

---

## Krok 3: Vytvořte Client Secret

1. Přejděte na **Certificates & secrets → Client secrets**
2. Klikněte na **New client secret**
3. Zadejte popis a zvolte dobu vypršení platnosti
4. Klikněte na **Add**
5. Okamžitě zkopírujte sloupec **Value**

!!! warning "Zkopírujte Value, ne Secret ID"

    Hodnota v sloupci **Value** je zobrazena pouze jednou na této stránce a nelze ji později získat zpět. Vedle ní se zobrazuje podobné pole **Secret ID**, které však není tajným klíčem — použití Secret ID způsobí při přihlášení chybu `invalid_client`. Pokud stránku opustíte dříve, než hodnotu zkopírujete, smažte tajný klíč a vytvořte nový.

!!! tip "Tip"

    Entra ID omezuje životnost secretu na maximálně 24 měsíců, takže každá SSO integrace má datum vypršení. Poznamenejte si ho na místě, kde ho uvidíte — expirovaný secret způsobí výpadek SSO pro všechny uživatele najednou, bez varování na přihlašovací stránce.

---

## Krok 4: Potvrďte API oprávnění

1. Přejděte na **API permissions**
2. Ověřte, že je přítomno **Microsoft Graph → User.Read** (delegované) — je přidáno ve výchozím nastavení

Scope, které digna požaduje (`openid`, `profile` a `email`) jsou součástí standardní sady OIDC a nepotřebují samostatné udělení. Pokud váš tenant vyžaduje administrátorský souhlas pro všechny aplikace, klikněte na **Grant admin consent for <tenant>**.

---

## Krok 5: Sestavte Discovery URL

Nahraďte **Directory (tenant) ID** ze kroku 2:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Použijte koncový bod v2.0"

    Segment `/v2.0/` je důležitý. Koncový bod v1.0 na `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` vydává tokeny ve starším formátu a nevrací standardní OIDC claimy, které digna očekává.

Otevřete URL v prohlížeči před dalším pokračováním. JSON dokument potvrdí, že je tenant ID správné.

---

## Krok 6: Nakonfigurujte digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Přihlásit se přes Microsoft"
```

### `config.toml`

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

Hodnota `key` v obou souborech se musí shodovat — zde `microsoft`.

---

## Krok 7: Otestujte

Restartujte backend a webový server, poté otevřete dashboard. Kompletní kontrolní seznam najdete v [Testing Login](overview.md#testing-login).

---

## Řešení problémů s Entra ID

### AADSTS50011: Nesoulad Redirect URI

URI v `DIGNA_OIDC_REDIRECT_URI` se liší od toho registrovaného v kroku 1. Entra ID porovnává celý řetězec, takže koncová lomítka, `http` versus `https` nebo jiný port se počítají jako nesoulad. Zkontrolujte **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Neplatný klientský secret

Buď jste zkopírovali **Secret ID** místo **Value**, nebo secret vypršel. Vytvořte nový secret a zkopírujte sloupec Value.

### AADSTS650057: Neplatný resource

Registrace aplikace byla smazána nebo patří jinému tenantu, než je ten v discovery URL. Ověřte Directory (tenant) ID na stránce Overview.

### Uživatelé se přihlásí, ale nic se nestane

Pokud tenant vyžaduje administrátorský souhlas a ten nebyl udělen, přesměrování se vrátí bez použitelného tokenu. Udělte admin souhlas v **API permissions**.

---

## Viz také

- [Single Sign-On Overview](overview.md) — referenční konfigurace, testování a obecné řešení problémů
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)