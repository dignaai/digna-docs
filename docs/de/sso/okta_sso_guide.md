---
title: Okta SSO – Single Sign-On-Integration | digna Dokumentation
description: Konfigurieren Sie Single Sign-On für digna mit Okta über OpenID Connect — App-Integration, Sign-in-Redirect-URIs, Client-Credentials, Wahl des Authorization Servers und die passende digna-Konfiguration.
image: /assets/logo_square.png
keywords: digna sso, okta sso, okta oidc, App-Integration, Autorisierungsserver, OpenID Connect, Unternehmens-Authentifizierung
---

# SSO mit Okta einrichten

Okta ist OIDC-kompatibel, hat aber eine Besonderheit, die bei den meisten Erstintegrationen auffällt: Eine Okta-Organisation stellt mehr als einen Authorization Server bereit, und jeder hat seine eigene Discovery-URL.

Diese Anleitung behandelt die **Okta-Seite**: Erstellen der App-Integration und Ermitteln der Werte, die digna benötigt. Die digna-Seite — `dashboard_config.toml`, Tests und Fehlerbehebung — ist bei jedem Anbieter gleich und wird in der [Single Sign-On-Übersicht](overview.md) beschrieben.

---

## Bevor Sie beginnen

| Requirement | Notes |
|---|---|
| **Okta role** | Super Administrator, oder eine Admin-Rolle mit Berechtigung, App-Integrationen zu erstellen |
| **Okta domain** | z. B. `yourcompany.okta.com`, oder eine benutzerdefinierte Domain, falls konfiguriert |
| **digna redirect URI** | Die URL, zu der Benutzer nach dem Login zurückkehren, z. B. `https://digna.yourdomain.com/oidc/callback` |

---

## Schritt 1: App-Integration erstellen

1. Melden Sie sich beim Okta Admin Console an
2. Gehen Sie zu **Applications → Applications**
3. Klicken Sie auf **Create App Integration**
4. Wählen Sie:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Klicken Sie auf **Next**

!!! warning "Anwendungstyp kann nicht geändert werden"

    Die Auswahl von *Single-Page Application* statt *Web Application* erstellt einen Public Client ohne Secret, und dignas Backend-Code-Austausch schlägt mit `invalid_client` fehl. Der Typ ist bei der Erstellung fest — eine falsche Wahl erfordert das Löschen der App und einen Neuanfang.

---

## Schritt 2: Integration konfigurieren

1. **App integration name**: `digna`
2. **Grant type**: belassen Sie *Authorization Code* ausgewählt
3. **Sign-in redirect URIs**: Geben Sie Ihre digna-Callback-URL ein:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: optional
5. Unter **Assignments** wählen Sie, wer die Integration verwenden darf — eine bestimmte Gruppe ist sicherer als *Allow everyone in your organization to access*
6. Klicken Sie auf **Save**

!!! note "Zuweisung ist erforderlich"

    Okta authentifiziert den Benutzer und prüft anschließend, ob dieser der Anwendung zugewiesen ist. Ein nicht zugewiesener Benutzer erreicht die Okta-Anmeldeseite, meldet sich erfolgreich an und wird bei der Weiterleitung zurück abgewiesen. Wenn die Anmeldung für Sie funktioniert, aber nicht für Kolleg:innen, ist die Zuweisung der erste Prüfpunkt.

---

## Schritt 3: Zugangsdaten sammeln

Auf der Registerkarte **General** der Anwendung, unter **Client Credentials**:

- **Client ID** → wird zu `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → wird zu `DIGNA_OIDC_CLIENT_SECRET` (klicken Sie auf das Augensymbol, um es anzuzeigen)

---

## Schritt 4: Den Authorization Server wählen

Dies ist der Schritt, der Ihre Discovery-URL bestimmt. Gehen Sie zu **Security → API**, um die Authorization Server in Ihrer Organization zu sehen.

**Org authorization server** — stellt Tokens für die Okta-Organisation selbst aus:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — einschließlich des von Okta erstellten Servers namens `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Beim integrierten Server ist `<auth_server_id>` tatsächlich `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Welchen verwenden?"

    Verwenden Sie den **org** Authorization Server, es sei denn, Ihre Organisation standardisiert bereits auf einen Custom Server für API-Zugriffsrichtlinien. Okta Developer-Accounts verwenden standardmäßig `default`; viele Unternehmens-Organisationen deaktivieren ihn. Öffnen Sie beide URLs im Browser — diejenige, die JSON statt eines Fehlers zurückgibt, ist die für Sie verfügbare.

---

## Schritt 5: digna konfigurieren

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Mit Okta anmelden"
```

### `config.toml`

```toml
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

Der `key` in beiden Dateien muss übereinstimmen — hier `okta`.

---

## Schritt 6: Testen

Starten Sie das Backend und den Webserver neu und öffnen Sie dann das Dashboard. Siehe [Testing Login](overview.md#testing-login) für die vollständige Checkliste.

---

## Fehlerbehebung Okta

### Die Redirect-URI ist nicht registriert

Okta nennt die fehlerhafte URI in der Fehlermeldung. Vergleichen Sie sie mit **General → Sign-in redirect URIs**; Okta vergleicht die vollständige Zeichenkette einschließlich eines eventuell vorhandenen abschließenden Schrägstrichs.

### Der Benutzer ist der Client-Anwendung nicht zugewiesen

Das Konto befindet sich nicht in der Zuweisungsliste der Anwendung. Fügen Sie den Benutzer oder dessen Gruppe unter **Assignments** hinzu.

### 400 Bad Request: Invalid Authorization Server

Die `<auth_server_id>` in der Discovery-URL existiert nicht, meist `default` in einer Organization, in der er entfernt wurde. Prüfen Sie **Security → API** auf die tatsächlich verfügbaren Server.

### invalid_client beim Token-Schritt

Die Integration wurde als Single-Page Application erstellt und hat kein Client-Secret. Erstellen Sie sie erneut als Web Application.

---

## Siehe auch

- [Single Sign-On-Übersicht](overview.md) — Konfigurationsreferenz, Tests und allgemeine Fehlerbehebung
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)