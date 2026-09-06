# Nustatykite SSO su Microsoft Entra ID

Microsoft Entra ID (anksčiau Azure Active Directory) yra visiškai OIDC suderinamas teikėjas, todėl digna integruojasi su juo per standartinį discovery endpoint.

Šis vadovas apima **Entra ID pusę**: programos registraciją ir keturių reikšmių, kurių reikia digna, surinkimą. digna pusė — `dashboard_config.toml`, testavimas ir trikčių šalinimas — yra vienoda visiems tiekėjams ir aprašyta [Single Sign-On Overview](overview.md).

---

## Prieš pradėdami

| Reikalavimas | Pastabos |
|---|---|
| **Entra ID rolė** | Application Administrator, Cloud Application Administrator, arba Global Administrator |
| **digna redirect URI** | URL, į kurį vartotojai grįžta po prisijungimo, pvz. `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | Aplanko katalogas, į kurį jūsų vartotojai prisijungia |

---

## Žingsnis 1: Programos registracija

1. Prisijunkite prie [Microsoft Entra administravimo centro](https://entra.microsoft.com)
2. Eikite į **Identity → Applications → App registrations**
3. Spauskite **New registration**
4. Konfigūruokite:
   - **Name**: `digna` (rodoma vartotojams sutikimo lange)
   - **Supported account types**: *Accounts in this organizational directory only* — vieno nuomininko diegimui
5. Skiltyje **Redirect URI** pasirinkite platformą **Web** ir įveskite savo digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

6. Spauskite **Register**

!!! warning "Svarbu"

    Platforma turi būti **Web**, ne *Single-page application*. digna mainais į backend'ą keičia autorizacijos kodą naudodama kliento slaptąjį raktą, kurio SPA platforma neleidžia.

---

## Žingsnis 2: Surinkite kliento ir tenant ID

Programos **Overview** puslapyje nukopijuokite:

- **Application (client) ID** → vėliau tapo `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → dedamas į discovery URL

---

## Žingsnis 3: Sukurkite kliento slaptąjį raktą

1. Eikite į **Certificates & secrets → Client secrets**
2. Spauskite **New client secret**
3. Įveskite aprašymą ir pasirinkite galiojimo laiką
4. Spauskite **Add**
5. Iškart nukopijuokite stulpelį **Value**

!!! warning "Kopijuokite Value, ne Secret ID"

    Stulpelis **Value** rodomas tik vieną kartą, šiame puslapyje, ir vėliau jo nebus galima atkurti. Šalia esantis **Secret ID** panašiai atrodo, bet nėra slaptoji reikšmė — jo naudojimas sukels `invalid_client` klaidą prisijungimo metu. Jei išeisite iš puslapio prieš kopijuodami, ištrinkite slaptažodį ir sukurkite naują.

!!! tip "Patarimas"

    Entra ID riboja slaptųjų raktų galiojimą iki 24 mėnesių, tad kiekviena SSO integracija turi galiojimo datą. Pažymėkite ją vietoje, kur ją pastebėsite — pasibaigęs raktas nutrauks SSO visiems vartotojams vienu metu, be įspėjimo prisijungimo puslapyje.

---

## Žingsnis 4: Patikrinkite API leidimus

1. Eikite į **API permissions**
2. Patikrinkite, kad būtų pridėta **Microsoft Graph → User.Read** (deleguotas) — ji pridedama pagal nutylėjimą

`openid`, `profile` ir `email` scope'ai, kurių prašo digna, yra standartinio OIDC rinkinio dalis ir nereikalauja atskiro suteikimo. Jei jūsų tenant reikalauja administratoriaus sutikimo visoms programoms, spauskite **Grant admin consent for &lt;tenant&gt;**.

---

## Žingsnis 5: Sudarykite discovery URL

Pakeiskite **Directory (tenant) ID** iš 2 žingsnio:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Naudokite v2.0 galinį tašką"

    Segmentas `/v2.0/` yra svarbus. v1.0 galinis taškas `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` išduoda žetonus senesniu formatu ir negrąžina standartinių OIDC claim'ų, kurių tikisi digna.

Atidarykite URL naršyklėje prieš tęsdami. JSON dokumentas patvirtins, kad tenant ID yra teisingas.

---

## Žingsnis 6: Konfigūruokite digna

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
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

Reikšmė `key` abiejuose failuose turi sutapti — čia tai `microsoft`.

---

## Žingsnis 7: Testavimas

Perkraukite backend'ą ir web serverį, tada atidarykite administravimo skydelį. Visą tikrinimo kontrolinį sąrašą rasite [Testing Login](overview.md#testing-login).

---

## Entra ID trikčių šalinimas

### AADSTS50011: Redirect URI neatitikimas

URI, nurodytas `DIGNA_OIDC_REDIRECT_URI`, skiriasi nuo to, kuris užregistruotas 1 žingsnyje. Entra ID palygina visą eilutę, tad galutinė brūkšnelio vieta, `http` prieš `https` arba kitas portas — viskas laikoma neatitikimu. Patikrinkite **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Neteisingas kliento slaptasis raktas

Arba buvo nukopijuotas **Secret ID** vietoje **Value**, arba slaptasis raktas yra pasibaigęs. Sukurkite naują slaptąjį raktą ir nukopijuokite stulpelį Value.

### AADSTS650057: Neteisingas išteklius

Programos registracija buvo ištrinta arba priklauso kitam tenant nei tas, nurodytas discovery URL. Patikrinkite Directory (tenant) ID Overview puslapyje.

### Vartotojai prisijungia, bet nieko neįvyksta

Jei tenant reikalauja administratoriaus sutikimo ir jis nebuvo suteiktas, peradresavimas grįžta be galiojančio žetono. Suteikite administratoriaus sutikimą skiltyje **API permissions**.

---

## Taip pat žiūrėkite

- [Single Sign-On Overview](overview.md) — konfigūracijos nuoroda, testavimas ir bendras trikčių šalinimas
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)