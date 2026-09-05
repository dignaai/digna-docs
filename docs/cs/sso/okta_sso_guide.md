---
title: Okta SSO – Integrace Single Sign-On | digna Dokumentace
description: Nakonfigurujte Single Sign-On pro digna s Okta pomocí OpenID Connect — integrace aplikace, přesměrovací URI pro přihlášení, přihlašovací údaje klienta, volba autorizačního serveru a odpovídající konfigurace digna.
image: /assets/logo_square.png
keywords: digna sso, okta sso, okta oidc, integrace aplikace, autorizační server, openid connect, podnikové ověřování
---

# Nastavení SSO s Okta

Okta je kompatibilní s OIDC, s jedním záludným detailem, který potká většinu prvních integrací: organizace Okta vystavuje více než jeden autorizační server a každý má vlastní discovery URL.

Tento průvodce pokrývá **stranu Okta**: vytvoření integrace aplikace a sběr hodnot, které digna potřebuje. Strana digna — `dashboard_config.toml`, testování a řešení problémů — je pro každého poskytovatele stejná a je popsaná v [Přehledu Single Sign-On](overview.md).

---

## Než začnete

| Requirement | Notes |
|---|---|
| **Okta role** | Super Administrator, nebo administrátorská role oprávněná vytvářet integrace aplikací |
| **Okta domain** | např. `yourcompany.okta.com`, nebo vlastní doména pokud je nakonfigurována |
| **digna redirect URI** | URL, na kterou se uživatelé vrátí po přihlášení, např. `https://digna.yourdomain.com/oidc/callback` |

---

## Krok 1: Vytvoření integrace aplikace

1. Přihlaste se do Okta Admin Console
2. Přejděte na **Applications → Applications**
3. Klikněte na **Create App Integration**
4. Vyberte:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Klikněte **Next**

!!! warning "Typ aplikace nelze změnit"

    Volba *Single-Page Application* místo *Web Application* vytvoří veřejného klienta bez tajného klíče a výměna kódu na straně backendu digna selže s chybou `invalid_client`. Typ je pevně nastaven při vytvoření — špatná volba znamená smazat aplikaci a začít znovu.

---

## Krok 2: Konfigurace integrace

1. **App integration name**: `digna`
2. **Grant type**: ponechte vybrané *Authorization Code*
3. **Sign-in redirect URIs**: zadejte vaši digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: volitelné
5. V sekci **Assignments** vyberte, kdo může integraci používat — konkrétní skupina je bezpečnější než *Allow everyone in your organization to access*
6. Klikněte **Save**

!!! note "Přiřazení je povinné"

    Okta ověří uživatele a poté zkontroluje, zda je přiřazen k aplikaci. Nepřiřazený uživatel dorazí na stránku přihlášení Okta, úspěšně se přihlásí a následně je odmítnut při přesměrování zpět. Pokud přihlášení funguje pro vás, ale ne pro kolegy, je přiřazení první věcí, kterou zkontrolovat.

---

## Krok 3: Získání přihlašovacích údajů

Na kartě aplikace **General**, v sekci **Client Credentials**:

- **Client ID** → se stane `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → se stane `DIGNA_OIDC_CLIENT_SECRET` (klikněte na ikonu oka pro zobrazení)

---

## Krok 4: Výběr autorizačního serveru

Tento krok určuje vaše discovery URL. Přejděte na **Security → API**, kde uvidíte autorizační servery ve vaší organizaci.

**Org authorization server** — vydává tokeny pro samotnou Okta org:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — včetně toho, který Okta vytvoří s názvem `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Pro vestavěný server je `<auth_server_id>` doslova `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Který?"

    Použijte autorizační server **org**, pokud vaše organizace již nedefinuje standardní vlastní server pro politiky přístupu k API. Okta Developer účty mají výchozí `default`; mnoho enterprise organizací jej zakáže. Otevřete obě URL v prohlížeči — ta, která vrátí JSON místo chyby, je ta, která je pro vás dostupná.

---

## Krok 5: Konfigurace digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

### `config.toml`

```toml
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

Hodnota `key` v obou souborech se musí shodovat — zde `okta`.

---

## Krok 6: Testování

Restartujte backend a webový server, poté otevřete dashboard. Kompletní kontrolní seznam najdete v [Testování přihlášení](overview.md#testing-login).

---

## Řešení problémů s Okta

### Přesměrovací URI není zaregistrované

Okta v chybě pojmenuje problematické URI. Porovnejte ho s **General → Sign-in redirect URIs**; Okta porovnává celý řetězec včetně případné koncové lomítka.

### Uživatel není přiřazen ke klientské aplikaci

Účet není na seznamu přiřazení aplikace. Přidejte uživatele nebo jeho skupinu v sekci **Assignments**.

### 400 Bad Request: Invalid Authorization Server

`<auth_server_id>` v discovery URL neexistuje, nejčastěji `default` v organizaci, kde byl odstraněn. Zkontrolujte v **Security → API**, které servery jsou skutečně dostupné.

### invalid_client v kroku tokenu

Integrace byla vytvořena jako Single-Page Application a nemá client secret. Vytvořte ji znovu jako Web Application.

---

## Viz také

- [Přehled Single Sign-On](overview.md) — referenční konfigurace, testování a obecné řešení problémů
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)