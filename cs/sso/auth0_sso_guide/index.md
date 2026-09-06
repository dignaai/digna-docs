# Nastavení SSO s Auth0

Auth0 je kompatibilní s OIDC a pro každý tenant vystavuje discovery endpoint. Hlavní věc, kterou je potřeba mít správně, je doména tenanta, která se objevuje v discovery URL a mění se, pokud povolíte vlastní doménu.

Tento průvodce pokrývá **stranu Auth0**: vytvoření aplikace a sesbírání hodnot, které digna potřebuje. Strana digna — `dashboard_config.toml`, testování a ladění — je stejná pro všechny poskytovatele a je popsána v [Přehled Single Sign-On](overview.md).

---

## Než začnete

| Požadavek | Poznámky |
|---|---|
| **Role v Auth0** | Administrátor na tenantu |
| **Doména tenanta** | např. `yourcompany.eu.auth0.com` — segment regionu je důležitý |
| **digna redirect URI** | URL, na kterou se uživatel vrací po přihlášení, např. `https://digna.yourdomain.com/oidc/callback` |

---

## Krok 1: Vytvoření aplikace

1. Přihlaste se do [Řídicího panelu Auth0](https://manage.auth0.com)
2. Přejděte na **Applications → Applications**
3. Klikněte na **Create Application**
4. Pojmenujte ji `digna` a vyberte **Regular Web Applications**
5. Klikněte na **Create**

!!! warning "Zvolte Regular Web Applications"

    *Single Page Application* a *Native* vytvoří veřejné klienty bez tajemství. digna provádí code exchange ze svého backendu a potřebuje důvěrného klienta, proto je správný typ právě **Regular Web Applications**. Na rozdíl od některých poskytovatelů Auth0 umožňuje typ později změnit v **Settings → Application Type**.

---

## Krok 2: Přidání Callback URL

Na kartě **Settings** aplikace:

1. Najděte **Allowed Callback URLs**
2. Zadejte váš digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Volitelně nastavte **Allowed Logout URLs** na URL dashboardu
4. Sjeďte dolů a klikněte na **Save Changes**

!!! note "Oddělovač čárkou, nikoli novým řádkem"

    Auth0 v tomto poli přijímá několik callback URL oddělených čárkami. Seznam oddělený pouze novými řádky je interpretován jako jedna poškozená URL a potichu nic neodpovídá.

---

## Krok 3: Získání přihlašovacích údajů

Stále v **Settings**, v panelu **Basic Information**:

- **Domain** → jde do discovery URL
- **Client ID** → stane se `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → stane se `DIGNA_OIDC_CLIENT_SECRET` (klikněte pro zobrazení)

---

## Krok 4: Potvrďte typ grantů

1. Přejděte na **Settings → Advanced Settings → Grant Types**
2. Ujistěte se, že je zaškrtnuté **Authorization Code**

Je povolený ve výchozím nastavení pro Regular Web Applications. Pokud není zaškrtnutý, přihlášení v digna selže s chybou `unauthorized_client`.

---

## Krok 5: Sestavte Discovery URL

Nahraďte hodnotou **Domain** ze Kroku 3:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Například:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Vlastní domény mění issuer"

    Pokud váš tenant používá vlastní doménu, například `login.yourcompany.com`, použijte tuhle doménu v discovery URL. Smíchání obou — kanonické domény v discovery URL a vlastní v prohlížeči — způsobí nesoulad issueru a token bude po jinak úspěšném přihlášení odmítnut.

---

## Krok 6: Konfigurace digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Login with Auth0"
```

### `config.toml`

```toml
[oidc.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

Hodnota `key` v obou souborech se musí shodovat — zde `auth0`.

---

## Krok 7: Testování

Restartujte backend a webový server, pak otevřete dashboard. Pro úplný kontrolní seznam viz [Testování přihlášení](overview.md#testing-login).

---

## Řešení problémů s Auth0

### Neshoda Callback URL

Chybová stránka Auth0 ukáže URL, kterou obdržela. Přidejte ji do **Allowed Callback URLs**, dbejte na to, aby byly položky oddělené čárkami.

### unauthorized_client

Neje aktivní **Authorization Code** v **Advanced Settings → Grant Types**, nebo typ aplikace není Regular Web Applications.

### Přístup odepřen po úspěšném přihlášení

Pravidlo (Rule), Akce nebo Post-Login trigger v tenantu uživatele zamítá. Zkontrolujte **Actions → Flows → Login** a logy tenanta pod **Monitoring → Logs**, které zobrazí přesný důvod.

### Neshoda issueru

Discovery URL a doména, na kterou byl prohlížeč odeslán, se liší — obvykle kanonická doména tenanta versus vlastní doména. Používejte jednu konzistentně.

---

## Viz také

- [Přehled Single Sign-On](overview.md) — referenční konfigurace, testování a obecné řešení problémů
- [Auth0 – Objevování OpenID Connect](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)