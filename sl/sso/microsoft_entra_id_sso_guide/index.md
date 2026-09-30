# Nastavite SSO z Microsoft Entra ID

Microsoft Entra ID (prej Azure Active Directory) je ponudnik, ki je v celoti združljiv z OIDC, zato se digna z njim poveže prek standardne končne točke discovery.

Ta vodič zajema **Entra ID stran**: registracijo aplikacije in zbiranje štirih vrednosti, ki jih potrebuje digna. Digna stran — `dashboard_config.toml`, testiranje in odpravljanje težav — je enaka za vse ponudnike in je opisana v [Pregled Single Sign-On](overview.md).

---

## Preden začnete

| Zahteva | Opombe |
|---|---|
| **Vloga v Entra ID** | Application Administrator, Cloud Application Administrator ali Global Administrator |
| **digna redirect URI** | URL, na katerega se uporabniki vrnejo po prijavi, npr. `https://digna.yourdomain.com/oidc/callback` |
| **Najemnik (tenant)** | Imenik, v katerega se prijavljajo vaši uporabniki |

---

## 1. korak: Registrirajte aplikacijo

1. Prijavite se v [Microsoft Entra admin center](https://entra.microsoft.com)
2. Pojdite na **Identity → Applications → App registrations**
3. Kliknite **New registration**
4. Konfigurirajte:
   - **Name**: `digna` (prikazano uporabnikom na zaslonu za soglasje)
   - **Supported account types**: *Accounts in this organizational directory only* za namestitev z enim najemnikom
5. Pod **Redirect URI** izberite platformo **Web** in vnesite svoj digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

6. Kliknite **Register**

!!! warning "Pomembno"

    Platforma mora biti **Web**, ne *Single-page application*. digna izmenja avtorizacijsko kodo v zaledju s skrivnostjo odjemalca, česar tip platforme SPA ne dovoljuje.

---

## 2. korak: Zberite ID odjemalca in ID najemnika

Na strani **Overview** aplikacije kopirajte:

- **Application (client) ID** → postane `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → gre v discovery URL

---

## 3. korak: Ustvarite skrivnost odjemalca

1. Pojdite na **Certificates & secrets → Client secrets**
2. Kliknite **New client secret**
3. Vnesite opis in izberite rok veljavnosti
4. Kliknite **Add**
5. Takoj kopirajte stolpec **Value**

!!! warning "Kopirajte Value, ne Secret ID"

    **Value** je prikazana samo enkrat, na tej strani, in je pozneje ni mogoče pridobiti. **Secret ID** poleg nje je videti podobno, vendar ni skrivnost — če ga uporabite, se ob prijavi pojavi napaka `invalid_client`. Če stran zapustite, preden kopirate vrednost, skrivnost izbrišite in ustvarite novo.

!!! tip "Nasvet"

    Entra ID omejuje življenjsko dobo skrivnosti na 24 mesecev, zato ima vsaka integracija SSO datum poteka. Zabeležite si ga nekam, kjer ga boste videli — potekla skrivnost onemogoči SSO za vse uporabnike naenkrat, brez opozorila na strani za prijavo.

---

## 4. korak: Preverite dovoljenja API

1. Pojdite na **API permissions**
2. Preverite, da je prisotno **Microsoft Graph → User.Read** (delegirano) — privzeto je dodano

Obsegi `openid`, `profile` in `email`, ki jih zahteva digna, so del standardnega nabora OIDC in ne potrebujejo ločene odobritve. Če vaš najemnik za vse aplikacije zahteva soglasje skrbnika, kliknite **Grant admin consent for &lt;tenant&gt;**.

---

## 5. korak: Sestavite discovery URL

Vstavite **Directory (tenant) ID** iz 2. koraka:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Uporabite končno točko v2.0"

    Segment `/v2.0/` je pomemben. Končna točka v1.0 na `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` izdaja žetone v starejši obliki in ne vrača standardnih zahtevkov (claims) OIDC, ki jih pričakuje digna.

Preden nadaljujete, odprite URL v brskalniku. Dokument JSON potrjuje, da je ID najemnika pravilen.

---

## 6. korak: Konfigurirajte digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"
```

### `config.toml`

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

Vrednost `key` se mora v obeh datotekah ujemati — tukaj `microsoft`.

---

## 7. korak: Testirajte

Znova zaženite zaledje in spletni strežnik, nato odprite nadzorno ploščo. Za celoten kontrolni seznam si oglejte [Testiranje prijave](overview.md#testing-login).

---

## Odpravljanje težav z Entra ID

### AADSTS50011: Redirect URI Mismatch

URI v `DIGNA_OIDC_REDIRECT_URI` se razlikuje od tistega, registriranega v 1. koraku. Entra ID primerja celoten niz, zato se kot neujemanje štejejo poševnica na koncu, `http` namesto `https` ali drugačna vrata. Preverite **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Invalid Client Secret

Bodisi je bil kopiran **Secret ID** namesto **Value** bodisi je skrivnost potekla. Ustvarite novo skrivnost in kopirajte stolpec Value.

### AADSTS650057: Invalid Resource

Registracija aplikacije je bila izbrisana ali pripada drugemu najemniku kot tistemu v discovery URL-ju. Preverite Directory (tenant) ID na strani Overview.

### Uporabniki se prijavijo, vendar se nič ne zgodi

Če najemnik zahteva soglasje skrbnika in to ni bilo podeljeno, se preusmeritev vrne brez uporabnega žetona. Soglasje skrbnika podelite pod **API permissions**.

---

## Povezane vsebine

- [Pregled Single Sign-On](overview.md) — referenca konfiguracije, testiranje in splošno odpravljanje težav
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)