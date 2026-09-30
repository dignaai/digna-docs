---
title: AD FS SSO – Single Sign-On-integratie | digna Documentatie
description: Configureer Single Sign-On voor digna met Active Directory Federation Services via OpenID Connect — application group, server application, shared secret, toegestane scopes en de bijbehorende digna-configuratie.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, active directory federation services, adfs oidc, application group, openid connect, on-premises identiteitsprovider
---

# SSO instellen met AD FS

Active Directory Federation Services is de on-premises optie: je eigen servers geven de tokens uit, en de discovery-URL is je eigen hostnaam. AD FS ondersteunt OpenID Connect vanaf **Windows Server 2016**.

Deze gids behandelt de **AD FS-kant**: het aanmaken van de application group en het verzamelen van de waarden die digna nodig heeft. De digna-kant — `dashboard_config.toml`, testen en oplossen van problemen — is voor elke provider hetzelfde en wordt beschreven in het [Overzicht Single Sign-On](overview.md).

---

## Voordat je begint

| Vereiste | Opmerkingen |
|---|---|
| **AD FS-versie** | Windows Server 2016 of later — eerdere versies ondersteunen geen OIDC |
| **Toegang** | Lokale beheerder op de AD FS-server |
| **Naam van de federation service** | bijv. `adfs.yourdomain.com` |
| **digna redirect URI** | De URL waar gebruikers na het inloggen naar terugkeren, bijv. `https://digna.yourdomain.com/oidc/callback` |

---

## Stap 1: Maak de Application Group aan

1. Open op de AD FS-server **AD FS Management**
2. Klik met de rechtermuisknop op **Application Groups** en kies **Add Application Group**
3. Voer `digna` in als naam
4. Selecteer onder **Standalone applications** — of **Client-Server applications**, afhankelijk van je versie — **Server application accessing a web API**
5. Klik **Next**

---

## Stap 2: Configureer de Server Application

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS genereert een GUID. Kopieer deze — dit wordt `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: voer je digna callback-URL in en klik **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Klik **Next**

!!! warning "Klik op Add, niet alleen op Next"

    Het veld voor de redirect URI heeft een eigen knop **Add**. Als je een URI typt en op **Next** klikt zonder op **Add** te drukken, wordt hij weggegooid, en de wizard geeft geen waarschuwing. Controleer of de URI in de lijst onder het veld staat voordat je verdergaat.

---

## Stap 3: Genereer het Shared Secret

1. Vink **Generate a shared secret** aan
2. Kopieer het gegenereerde secret → wordt `DIGNA_OIDC_CLIENT_SECRET`
3. Klik **Next**

!!! warning "Het secret wordt één keer getoond"

    AD FS toont het shared secret alleen op deze wizardpagina en kan het niet opnieuw weergeven. Als je het kwijtraakt, reset je het later via de eigenschappen van de application group.

---

## Stap 4: Configureer de Web API

1. **Identifier**: voer dezelfde client identifier uit Stap 2 in en klik **Add**
2. Klik **Next**
3. Kies een **Access Control Policy** — *Permit everyone* is het eenvoudigste startpunt; beperk het voor productie tot een groep
4. Klik **Next**

---

## Stap 5: Ken de toegestane scopes toe

Vink op de stap **Configure Application Permissions** aan:

- `openid`
- `profile`
- `email`

Klik daarna op **Next** en rond de wizard af.

!!! warning "openid is standaard niet aangevinkt"

    In sommige versies selecteert AD FS vooraf alleen `user_impersonation`. Zonder `openid` retourneert het token-endpoint een OAuth-access token in plaats van een ID-token, en kan digna de gebruiker niet identificeren.

---

## Stap 6: Controleer het discovery-endpoint

Vul de naam van je federation service in:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Bijvoorbeeld:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Open de URL in een browser. Een JSON-document bevestigt dat OIDC is ingeschakeld en dat de hostnaam klopt.

!!! note "De backend moet het certificaat vertrouwen"

    Een interne certificeringsinstantie is gebruikelijk bij AD FS. De machine waarop de digna-backend draait, doet zelf een uitgaande HTTPS-aanroep naar deze URL, dus de uitgevende CA moet in de truststore van die machine staan — niet alleen in de browsers van de mensen die inloggen.

---

## Stap 7: Configureer digna

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
[oidc_clients.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

De `key` moet in beide bestanden overeenkomen — hier `adfs`.

---

## Stap 8: Test

Herstart de backend en de webserver, en open daarna het dashboard. Zie [Inloggen testen](overview.md#testing-login) voor de volledige checklist.

---

## Problemen oplossen met AD FS

### MSIS9611: The Client Is Not Allowed to Access the Resource

De web-API-identifier uit Stap 4 komt niet overeen met de client identifier, of de scopes uit Stap 5 zijn niet toegekend. Beide kun je aanpassen via de eigenschappen van de application group.

### MSIS9602: Invalid redirect_uri

De URI is getypt maar niet toegevoegd met de knop **Add**, of wijkt af van `DIGNA_OIDC_REDIRECT_URI`. Controleer **Application Groups → digna → digna backend → Properties**.

### Er wordt geen ID-token geretourneerd

De scope `openid` ontbreekt in de applicatierechten.

### De backend kan de discovery-URL niet bereiken

Ofwel lost DNS op de backendhost de naam van de federation service niet op, ofwel wordt het AD FS-certificaat daar niet vertrouwd. Test met `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` vanaf de digna-server zelf.

### Te controleren events

De AD FS-server logt fouten in Event Viewer onder **Applications and Services Logs → AD FS → Admin**, meestal met een specifiekere reden dan de browser toont.

---

## Zie ook

- [Overzicht Single Sign-On](overview.md) — configuratiereferentie, testen en algemene probleemoplossing
- [Microsoft: AD FS OpenID Connect scenarios](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)
