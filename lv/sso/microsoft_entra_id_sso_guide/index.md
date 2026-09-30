# Iestatīt SSO ar Microsoft Entra ID

Microsoft Entra ID (agrāk Azure Active Directory) ir pakalpojumu sniedzējs, kas pilnībā atbilst OIDC standartam, tāpēc digna ar to integrējas, izmantojot standarta atklāšanas (discovery) gala punktu.

Šis ceļvedis aptver **Entra ID pusi**: lietotnes reģistrēšanu un četru vērtību vākšanu, kas nepieciešamas digna. digna puse — `dashboard_config.toml`, testēšana un problēmu novēršana — ir vienāda visiem pakalpojumu sniedzējiem un aprakstīta [Single Sign-On pārskatā](overview.md).

---

## Pirms sākat

| Prasība | Piezīmes |
|---|---|
| **Entra ID loma** | Application Administrator, Cloud Application Administrator vai Global Administrator |
| **digna redirect URI** | URL, uz kuru lietotāji atgriežas pēc pieteikšanās, piem. `https://digna.yourdomain.com/oidc/callback` |
| **Tenants** | Direktorijs, kurā piesakās jūsu lietotāji |

---

## 1. solis: Reģistrēt lietotni

1. Piesakieties [Microsoft Entra admin center](https://entra.microsoft.com)
2. Dodieties uz **Identity → Applications → App registrations**
3. Noklikšķiniet **New registration**
4. Konfigurējiet:
   - **Name**: `digna` (tiek parādīts lietotājiem piekrišanas ekrānā)
   - **Supported account types**: *Accounts in this organizational directory only* viena tenanta izvietojumam
5. Sadaļā **Redirect URI** atlasiet platformu **Web** un ievadiet savu digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

6. Noklikšķiniet **Register**

!!! warning "Svarīgi"

    Platformai jābūt **Web**, nevis *Single-page application*. digna apmaina autorizācijas kodu no backend, izmantojot klienta slepeno atslēgu (client secret), ko SPA platformas tips neatļauj.

---

## 2. solis: Savākt klienta un tenanta ID

Lietotnes lapā **Overview** nokopējiet:

- **Application (client) ID** → kļūst par `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → tiek izmantots discovery URL

---

## 3. solis: Izveidot klienta slepeno atslēgu

1. Dodieties uz **Certificates & secrets → Client secrets**
2. Noklikšķiniet **New client secret**
3. Ievadiet aprakstu un izvēlieties derīguma termiņu
4. Noklikšķiniet **Add**
5. Nekavējoties nokopējiet kolonnas **Value** vērtību

!!! warning "Kopējiet Value, nevis Secret ID"

    **Value** tiek parādīta tikai vienreiz, šajā lapā, un vēlāk to vairs nevar iegūt. Blakus esošais **Secret ID** izskatās līdzīgi, taču tā nav slepenā atslēga — tā izmantošana pieteikšanās laikā izraisa kļūdu `invalid_client`. Ja aizejat no lapas, pirms esat to nokopējis, izdzēsiet slepeno atslēgu un izveidojiet jaunu.

!!! tip "Padoms"

    Entra ID ierobežo slepenās atslēgas derīgumu līdz 24 mēnešiem, tāpēc katrai SSO integrācijai ir derīguma beigu datums. Pierakstiet to vietā, kur to redzēsiet — slepenās atslēgas derīguma beigas atslēdz SSO visiem lietotājiem vienlaikus, bez jebkāda brīdinājuma pieteikšanās lapā.

---

## 4. solis: Pārbaudīt API atļaujas

1. Dodieties uz **API permissions**
2. Pārliecinieties, ka ir pieejama **Microsoft Graph → User.Read** (delegated) — tā tiek pievienota pēc noklusējuma

Scope `openid`, `profile` un `email`, ko pieprasa digna, ir daļa no standarta OIDC kopas, un tiem nav nepieciešama atsevišķa atļauja. Ja jūsu tenants pieprasa administratora piekrišanu visām lietotnēm, noklikšķiniet **Grant admin consent for &lt;tenant&gt;**.

---

## 5. solis: Izveidot discovery URL

Ievietojiet **Directory (tenant) ID** vērtību no 2. soļa:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Izmantojiet v2.0 gala punktu"

    Segments `/v2.0/` ir svarīgs. v1.0 gala punkts `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` izsniedz tokenus vecākā formātā un neatgriež standarta OIDC claims, ko sagaida digna.

Pirms turpināt, atveriet URL pārlūkā. JSON dokuments apstiprina, ka tenant ID ir pareizs.

---

## 6. solis: Konfigurēt digna

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

Abos failos `key` vērtībai jāsakrīt — šeit `microsoft`.

---

## 7. solis: Testēt

Restartējiet backend un web serveri, pēc tam atveriet dashboard. Pilnu pārbaudes sarakstu skatiet sadaļā [Pieteikšanās testēšana](overview.md#testing-login).

---

## Entra ID problēmu novēršana

### AADSTS50011: redirect URI neatbilstība

URI iestatījumā `DIGNA_OIDC_REDIRECT_URI` atšķiras no tā, kas reģistrēts 1. solī. Entra ID salīdzina pilnu virkni, tāpēc beigu slīpsvītra, `http` pret `https` vai cits ports tiek uzskatīti par neatbilstību. Pārbaudiet **Authentication → Web → Redirect URIs**.

### AADSTS7000215: nederīga klienta slepenā atslēga

Vai nu **Value** vietā tika nokopēts **Secret ID**, vai arī slepenās atslēgas derīgums ir beidzies. Izveidojiet jaunu slepeno atslēgu un nokopējiet kolonnu Value.

### AADSTS650057: nederīgs resurss

Lietotnes reģistrācija ir izdzēsta vai pieder citam tenantam, nevis tam, kas norādīts discovery URL. Pārbaudiet Directory (tenant) ID lapā Overview.

### Lietotāji piesakās, bet nekas nenotiek

Ja tenants pieprasa administratora piekrišanu un tā nav piešķirta, pāradresācija atgriežas bez izmantojama tokena. Piešķiriet administratora piekrišanu sadaļā **API permissions**.

---

## Skatīt arī

- [Single Sign-On pārskats](overview.md) — konfigurācijas atsauce, testēšana un vispārīga problēmu novēršana
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)