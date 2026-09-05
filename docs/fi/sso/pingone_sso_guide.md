---
title: PingOne SSO – Single Sign-On -integraatio | digna-dokumentaatio
description: Konfiguroi Single Sign-On dignalle PingOnen avulla OpenID Connect -protokollalla — OIDC-web-sovelluksen asennus, uudelleenohjaus-URI:t, client credentials, environment ID, aluekohtaiset domainit ja vastaava digna-konfiguraatio.
image: /assets/logo_square.png
keywords: digna sso, pingone sso, ping identity, pingone oidc, environment id, openid connect, yritystason todentaminen
---

# Ota SSO käyttöön PingOnen kanssa

PingOne on OIDC-yhteensopiva. Kaksi sen arvosta vaatii erityistä huomiota: **ympäristön ID**, joka näkyy jokaisessa endpoint-URL:issa, ja **aluekohtainen domain**, joka vaihtelee Pohjois-Amerikan, Euroopan, Kanadan, Aasian-Tyynenmeren ja Australian tenanttien välillä.

Tämä ohje kattaa **PingOne-puolen**: sovelluksen luomisen ja arvojen keräämisen, joita digna tarvitsee. digna-puoli — `dashboard_config.toml`, testaus ja vianetsintä — on sama kaikille tarjoajille ja on kuvattu [Single Sign-On Overview](overview.md):ssa.

---

## Ennen kuin aloitat

| Vaatimus | Huomautukset |
|---|---|
| **PingOne-rooli** | Environment Admin tai Identity Data Admin kohdeympäristössä |
| **Ympäristö** | Se PingOne-ympäristö, johon dignan käyttäjät kuuluvat |
| **digna uudelleenohjaus-URI** | URL johon käyttäjät palaavat kirjautumisen jälkeen, esim. `https://digna.yourdomain.com/oidc/callback` |

---

## Vaihe 1: Luo sovellus

1. Kirjaudu PingOne-hallintakonsoliin ja valitse ympäristösi
2. Siirry kohtaan **Applications → Applications**
3. Klikkaa **+**-painiketta
4. Anna **Application Name**-kenttään `digna`
5. Valitse **OIDC Web App**
6. Klikkaa **Save**

!!! warning "Valitse OIDC Web App — älä Single-Page Appia"

    *Single-Page App* ja *Native App* luovat julkisia clientteja, jotka eivät voi pitää salaista. digna vaihtaa backendistään authorization coden ja tarvitsee siksi luottamuksellisen **OIDC Web App** -tyypin.

---

## Vaihe 2: Määritä uudelleenohjaus-URI

1. Avaa sovelluksen **Configuration**-välilehti
2. Klikkaa kynäikonia muokataksesi
3. Varmista, että **Response Type** on *Code* ja **Grant Type** on *Authorization Code*
4. Lisää **Redirect URIs**-kohtaan dignan callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

5. Aseta **Token Endpoint Authentication Method** joko *Client Secret Post* tai *Client Secret Basic*
6. Klikkaa **Save**

---

## Vaihe 3: Ota sovellus käyttöön

Sovelluksen rivillä tai yksityiskohtapaneelissa kytke togglen asetukseksi **enabled**.

!!! warning "Uudet sovellukset ovat aluksi poissa käytöstä"

    PingOne luo sovellukset oletuksena poissa käytössä. Pois käytöstä oleva sovellus tuottaa virheen authorisointivaiheessa, jossa kytkimestä ei mainita, joten tämä kannattaa varmistaa ennen muiden asioiden vianetsintää.

---

## Vaihe 4: Myönnä scopet

1. Avaa **Resources**-välilehti
2. Varmista, että `openid` on myönnetty, ja lisää **OpenID Connect**-resurssista `profile` ja `email`
3. Klikkaa **Save**

---

## Vaihe 5: Lisää käyttäjiä

1. Avaa **Access**-välilehti
2. Lisää population tai ryhmät, joiden jäsenet saavat käyttää dignaa
3. Klikkaa **Save**

---

## Vaihe 6: Kerää tunnistetiedot ja ympäristön ID

Configuration-välilehdellä laajenna **General**:

- **Client ID** → tulee `DIGNA_OIDC_CLIENT_ID`-muuttujaksi
- **Client Secret** → tulee `DIGNA_OIDC_CLIENT_SECRET`-muuttujaksi (klikkaa silmäikonia)
- **Environment ID** → menee discovery-URL:iin

Sama välilehti listaa valmiiksi muodostetun **OIDC Discovery Endpoint**-arvon, jonka voi kopioida suoraan sen sijaan, että kokoonpanisi sen käsin.

---

## Vaihe 7: Rakenna discovery-URL

Korvaa environment ID ja alueesi domain:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Alue | Domain |
|---|---|
| Pohjois-Amerikka | `auth.pingone.com` |
| Eurooppa | `auth.pingone.eu` |
| Kanada | `auth.pingone.ca` |
| Aasia-Tyynenmeri | `auth.pingone.asia` |
| Australia | `auth.pingone.com.au` |

Esimerkiksi eurooppalaiselle ympäristölle:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Kopioi se mieluummin kuin kirjoita"

    Aluekohtainen domain on yleisin virhe PingOne-integraatiossa, ja väärä alue antaa 404-virheen eikä hyödyllistä virheilmoitusta. Käytä Step 6:n **OIDC Discovery Endpoint** -arvoa.

---

## Vaihe 8: Konfiguroi digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Kirjaudu PingOnella"
```

### `config.toml`

```toml
[oidc.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<vaiheessa 6 kopioitu client secret>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

Molempien tiedostojen `key`-arvojen on oltava samat — tässä `pingone`.

---

## Vaihe 9: Testaa

Käynnistä backend ja web-palvelin uudelleen, ja avaa dashboard. Katso täydellinen tarkistuslista kohdasta [Testing Login](overview.md#testing-login).

---

## PingOne-vianmääritys

### 404 discovery-URL:issa

Aluekohtainen domain tai environment ID on väärä. Vertaa sovelluksen Configuration-välilehdellä näkyvään **OIDC Discovery Endpoint** -arvoon.

### NOT_FOUND tai sovellus on pois käytöstä

Sovelluksen toggle kohdasta Vaihe 3 on yhä pois päältä.

### Redirect URI ei täsmää

PingOne vertaa kokonaista merkkijonoa. Tarkista **Configuration → Redirect URIs** mahdollisen loppuviivan tai eri scheman varalta.

### Kirjautuminen onnistuu, mutta sähköpostivaatimus ei saavu dignalle

`email`- ja `profile`-scopet eivät ole myönnetty Resources-välilehdellä.

### Käyttäjä ei näe sovellusta

Access-välilehdellä ei ole myönnetty populaatiota tai ryhmää.

---

## Katso myös

- [Single Sign-On Overview](overview.md) — konfiguraatio, testaus ja yleinen vianmääritys
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)