---
title: AD FS SSO – Integrace Single Sign-On | digna Dokumentace
description: Konfigurace Single Sign-On pro digna s Active Directory Federation Services pomocí OpenID Connect — skupina aplikací, serverová aplikace, sdílené tajemství, povolené scope a odpovídající konfigurace digna.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, Active Directory Federation Services, adfs oidc, skupina aplikací, OpenID Connect, on-premises poskytovatel identity
---

# Nastavení SSO s AD FS

Active Directory Federation Services je on-premises volba: vlastní servery vydávají tokeny a discovery URL je vaše vlastní doména. AD FS podporuje OpenID Connect od **Windows Server 2016**.

Tento průvodce pokrývá **stranu AD FS**: vytvoření skupiny aplikací a sebrání hodnot, které besoin digna. Strana digna — `dashboard_config.toml`, testování a řešení problémů — je stejná pro každého poskytovatele a je popsána v [Přehledu Single Sign-On](overview.md).

---

## Před začátkem

| Požadavek | Poznámky |
|---|---|
| **Verze AD FS** | Windows Server 2016 nebo novější — starší verze nepodporují OIDC |
| **Přístup** | Lokální administrátor na AD FS serveru |
| **Název služby federace** | např. `adfs.yourdomain.com` |
| **Přesměrovací URI digna** | URL, na kterou se uživatelé vrátí po přihlášení, např. `https://digna.yourdomain.com/oidc/callback` |

---

## Krok 1: Vytvoření skupiny aplikací

1. Na AD FS serveru otevřete **AD FS Management**
2. Pravým tlačítkem klikněte na **Application Groups** a zvolte **Add Application Group**
3. Zadejte název `digna`
4. Pod **Standalone applications** — nebo **Client-Server applications** podle vaší verze — zvolte **Server application accessing a web API**
5. Klikněte na **Next**

---

## Krok 2: Konfigurace serverové aplikace

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS vygeneruje GUID. Zkopírujte ho — stane se `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: zadejte vaši callback URL pro digna a klikněte **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Klikněte **Next**

!!! warning "Klikněte na Add, ne pouze na Next"

    Pole pro redirect URI má vlastní tlačítko **Add**. Pokud napíšete URI a kliknete na **Next** bez stisknutí **Add**, URI se zahodí a průvodce nevypíše varování. Před pokračováním se ujistěte, že se URI zobrazí v seznamu pod polem.

---

## Krok 3: Vygenerujte sdílené tajemství

1. Zaškrtněte **Generate a shared secret**
2. Zkopírujte vygenerované tajemství → stane se `DIGNA_OIDC_CLIENT_SECRET`
3. Klikněte **Next**

!!! warning "Tajné heslo je zobrazeno pouze jednou"

    AD FS zobrazí sdílené tajemství pouze na této stránce průvodce a později ho nelze znovu zobrazit. Pokud ho ztratíte, obnovte ho později v nastavení vlastností skupiny aplikací.

---

## Krok 4: Konfigurace Web API

1. **Identifier**: zadejte stejný client identifier z Kroku 2 a klikněte **Add**
2. Klikněte **Next**
3. Zvolte **Access Control Policy** — *Permit everyone* je nejjednodušší začátek; v produkci to omezte na konkrétní skupinu
4. Klikněte **Next**

---

## Krok 5: Udělení povolených scopes

Na kroku **Configure Application Permissions** zaškrtněte:

- `openid`
- `profile`
- `email`

Poté klikněte **Next** a dokončete průvodce.

!!! warning "openid není zaškrtnuto implicitně"

    AD FS v některých verzích předvybere pouze `user_impersonation`. Bez `openid` vrací token endpoint OAuth access token místo ID tokenu a digna nemůže uživatele identifikovat.

---

## Krok 6: Potvrďte discovery endpoint

Nahraďte svou hodnotu federation service name:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Například:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Otevřete to v prohlížeči. JSON dokument potvrdí, že OIDC je povoleno a že je název hostitele správný.

!!! note "Backend musí důvěřovat certifikátu"

    Pro AD FS je běžné používat interní certifikační autoritu. Stroj, na kterém běží digna backend, sám provádí odchozí HTTPS volání na tuto URL, takže vydávající CA musí být v důvěryhodném úložišti toho stroje — ne jen v prohlížečích uživatelů.

---

## Krok 7: Konfigurace digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Login with Active Directory"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

Hodnota `key` v obou souborech musí souhlasit — zde `adfs`.

---

## Krok 8: Testování

Restartujte backend a webový server, poté otevřete dashboard. Kompletní kontrolní seznam najdete v [Testování přihlášení](overview.md#testing-login).

---

## Řešení problémů s AD FS

### MSIS9611: The Client Is Not Allowed to Access the Resource

Identifier web API v Kroku 4 neodpovídá client identifieru, nebo nebyly uděleny scopes v Kroku 5. Obě nastavení lze upravit v properties skupiny aplikací.

### MSIS9602: Invalid redirect_uri

URI bylo napsáno, ale nebylo přidáno tlačítkem **Add**, nebo se liší od `DIGNA_OIDC_REDIRECT_URI`. Zkontrolujte **Application Groups → digna → digna backend → Properties**.

### Nebyl vrácen ID token

Chybí scope `openid` mezi oprávněními aplikace.

### Backend nemůže dosáhnout discovery URL

Buď DNS na backend hostiteli nerozlišuje název federace, nebo tamní AD FS certifikát není důvěryhodný. Otestujte pomocí `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` přímo ze serveru digna.

### Události k prohlédnutí

AD FS server loguje chyby do **Applications and Services Logs → AD FS → Admin** ve Event Vieweru, obvykle s konkrétnějším důvodem, než jaký zobrazuje prohlížeč.

---

## Viz také

- [Přehled Single Sign-On](overview.md) — referenční konfigurace, testování a obecné řešení problémů
- [Microsoft: Scénáře AD FS OpenID Connect](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)