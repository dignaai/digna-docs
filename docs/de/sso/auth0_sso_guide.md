---
title: Auth0 SSO – Single Sign-On-Integration | digna Dokumentation
description: Konfigurieren Sie Single Sign-On für digna mit Auth0 über OpenID Connect — Einrichtung für Regular Web Applications, erlaubte Callback-URLs, Client-Zugangsdaten, Mandantendomain und die passende digna-Konfiguration.
image: /assets/logo_square.png
keywords: digna sso, auth0 sso, auth0 oidc, Regular Web Application, Callback-URLs, OpenID Connect, Enterprise-Authentifizierung
---

# SSO mit Auth0 einrichten

Auth0 ist OIDC-kompatibel und stellt pro Mandant einen Discovery-Endpunkt bereit. Entscheidend ist die korrekte Mandantendomain, die in der Discovery-URL erscheint und sich ändert, wenn Sie eine benutzerdefinierte Domain aktivieren.

Diese Anleitung behandelt die **Auth0-Seite**: die Erstellung der Anwendung und das Sammeln der Werte, die digna benötigt. Die digna-Seite — `dashboard_config.toml`, Tests und Fehlerbehebung — ist bei jedem Provider gleich und ist in der [Single Sign-On Übersicht](overview.md) beschrieben.

---

## Bevor Sie beginnen

| Anforderung | Hinweise |
|---|---|
| **Auth0-Rolle** | Admin im Mandanten |
| **Mandantendomain** | z. B. `yourcompany.eu.auth0.com` — der Regionsabschnitt ist relevant |
| **digna Redirect-URI** | Die URL, zu der Benutzer nach dem Login zurückkehren, z. B. `https://digna.yourdomain.com/oidc/callback` |

---

## Schritt 1: Anwendung erstellen

1. Melden Sie sich beim [Auth0-Dashboard](https://manage.auth0.com) an
2. Gehen Sie zu **Applications → Applications**
3. Klicken Sie auf **Create Application**
4. Benennen Sie sie `digna` und wählen Sie **Regular Web Applications**
5. Klicken Sie auf **Create**

!!! warning "Wählen Sie 'Regular Web Applications'"

    *Single Page Application* und *Native* erzeugen öffentliche Clients ohne Secret. digna führt den Code-Austausch vom Backend aus durch und benötigt einen confidential client, daher ist **Regular Web Applications** der richtige Typ. Anders als einige Provider erlaubt Auth0, den Typ später unter **Settings → Application Type** zu ändern.

---

## Schritt 2: Callback-URL hinzufügen

Auf dem Reiter **Settings** der Anwendung:

1. Finden Sie **Allowed Callback URLs**
2. Geben Sie Ihre digna-Callback-URL ein:

```
https://digna.yourdomain.com/oidc/callback
```

3. Optional: Setzen Sie **Allowed Logout URLs** auf Ihre Dashboard-URL
4. Scrollen Sie nach unten und klicken Sie auf **Save Changes**

!!! note "Komma-getrennt, nicht zeilenweise"

    Auth0 akzeptiert mehrere Callback-URLs in diesem Feld, getrennt durch Kommata. Eine Liste, die nur durch Zeilenumbrüche getrennt ist, wird als eine fehlerhafte URL interpretiert und passt stillschweigend auf nichts.

---

## Schritt 3: Zugangsdaten sammeln

Immer noch unter **Settings**, im Panel **Basic Information**:

- **Domain** → gehört in die Discovery-URL
- **Client ID** → wird zu `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → wird zu `DIGNA_OIDC_CLIENT_SECRET` (klicken, um es anzuzeigen)

---

## Schritt 4: Grant-Typ bestätigen

1. Gehen Sie zu **Settings → Advanced Settings → Grant Types**
2. Bestätigen Sie, dass **Authorization Code** angehakt ist

Bei Regular Web Applications ist dies standardmäßig aktiviert. Wenn es deaktiviert ist, schlägt dignas Login mit `unauthorized_client` fehl.

---

## Schritt 5: Discovery-URL erstellen

Setzen Sie die **Domain** aus Schritt 3 ein:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Zum Beispiel:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Custom Domains ändern den Issuer"

    Wenn Ihr Mandant eine benutzerdefinierte Domain wie `login.yourcompany.com` verwendet, benutzen Sie diese Domain in der Discovery-URL. Die Mischung beider Domains — die kanonische Domain in der Discovery-URL und die benutzerdefinierte im Browser — führt zu einem Issuer-Mismatch, und das Token wird nach einem ansonsten erfolgreichen Login abgelehnt.

---

## Schritt 6: digna konfigurieren

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

Der `key` in beiden Dateien muss übereinstimmen — hier `auth0`.

---

## Schritt 7: Testen

Starten Sie das Backend und den Webserver neu und öffnen Sie dann das Dashboard. Siehe [Login testen](overview.md#testing-login) für die vollständige Checkliste.

---

## Fehlerbehebung bei Auth0

### Callback-URL stimmt nicht überein

Die Fehlerseite von Auth0 nennt die empfangene URL. Fügen Sie diese zu **Allowed Callback URLs** hinzu und achten Sie darauf, dass die Einträge komma-getrennt sind.

### unauthorized_client

**Authorization Code** ist unter **Advanced Settings → Grant Types** nicht aktiviert, oder der Anwendungstyp ist nicht Regular Web Applications.

### Zugriff verweigert nach erfolgreichem Login

Eine Rule, Action oder ein Post-Login-Trigger im Mandanten lehnt den Benutzer ab. Prüfen Sie **Actions → Flows → Login** und die Mandanten-Logs unter **Monitoring → Logs**, die den genauen Grund anzeigen.

### Issuer-Mismatch

Die Discovery-URL und die Domain, an die der Browser gesendet wurde, stimmen nicht überein — meist die kanonische Mandantendomain vs. eine benutzerdefinierte Domain. Verwenden Sie eine Domain durchgängig.

---

## Siehe auch

- [Single Sign-On Übersicht](overview.md) — Konfigurationsreferenz, Tests und allgemeine Fehlerbehebung
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)