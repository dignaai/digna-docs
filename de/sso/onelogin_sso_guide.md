# SSO mit OneLogin einrichten

OneLogin ist OIDC-kompatibel. Charakteristisch ist, dass der Connector-Typ beim Erstellen der App aus einem Katalog ausgewählt wird und danach nicht mehr geändert werden kann.

Diese Anleitung behandelt die **OneLogin-Seite**: das Erstellen der Anwendung und das Sammeln der Werte, die digna benötigt. Die digna-Seite — `dashboard_config.toml`, Tests und Fehlerbehebung — ist für alle Anbieter gleich und im [Single Sign-On Overview](overview.md) beschrieben.

---

## Bevor Sie beginnen

| Anforderung | Hinweise |
|---|---|
| **OneLogin-Rolle** | Kontoinhaber oder ein Administrator mit Berechtigung, Anwendungen hinzuzufügen |
| **Subdomain** | z. B. `yourcompany.onelogin.com` |
| **digna Redirect-URI** | Die URL, zu der Benutzer nach der Anmeldung zurückkehren, z. B. `https://digna.yourdomain.com/oidc/callback` |

---

## Schritt 1: Die OIDC-Anwendung erstellen

1. Melden Sie sich im OneLogin-Admin-Portal an
2. Gehen Sie zu **Applications → Applications**
3. Klicken Sie auf **Add App**
4. Suchen Sie nach `OpenId Connect` und wählen Sie den **OpenId Connect (OIDC)** Connector aus
5. Setzen Sie den **Display Name** auf `digna`
6. Klicken Sie auf **Save**

!!! warning "Der Connector-Typ ist bei der Erstellung festgelegt"

    OneLogin hat separate Katalogeinträge für SAML und OIDC, und eine Anwendung kann nicht von einem Typ in den anderen konvertiert werden. Wenn Sie versehentlich einen SAML-Connector wählen, löschen Sie die App und fügen Sie sie erneut hinzu — es gibt keine Einstellung zum Protokollwechsel.

---

## Schritt 2: Die Redirect-URI konfigurieren

1. Öffnen Sie den **Configuration**-Tab
2. Geben Sie in **Redirect URI's** Ihre digna-Callback-URL ein:

```
https://digna.yourdomain.com/oidc/callback
```

3. Optional: Setzen Sie **Post Logout Redirect URIs** auf Ihre Dashboard-URL
4. Klicken Sie auf **Save**

!!! note "Eine URI pro Zeile"

    Im Gegensatz zu Providern, die eine komma-getrennte Liste erwarten, nimmt OneLogin im Feld **Redirect URI's** eine URI pro Zeile entgegen.

---

## Schritt 3: Anwendungstyp und Authentifizierungsmethode festlegen

1. Öffnen Sie den **SSO**-Tab
2. Bestätigen Sie, dass **Application Type** auf *Web* steht
3. Setzen Sie **Token Endpoint → Authentication Method** auf *POST* (`client_secret_post`) oder *Basic* (`client_secret_basic`)

!!! warning "Wählen Sie nicht None"

    Wenn die Authentifizierungsmethode auf *None* gesetzt ist, wird die Anwendung zu einem öffentlichen Client ohne Secret, und dignas Backend-Code-Austausch wird abgelehnt. Entweder POST oder Basic funktioniert.

---

## Schritt 4: Die Anmeldedaten sammeln

Weiter im **SSO**-Tab:

- **Client ID** → wird zu `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → wird zu `DIGNA_OIDC_CLIENT_SECRET` (klicken Sie auf **Show client secret**)

Die Seite zeigt außerdem die **Issuer URL** an, die die Discovery-URL im nächsten Schritt bestätigt.

---

## Schritt 5: Benutzer zuweisen

1. Öffnen Sie den **Access**-Tab
2. Fügen Sie die Rollen oder Gruppen hinzu, deren Mitglieder digna verwenden dürfen
3. Klicken Sie auf **Save**

!!! note "Nicht zugewiesene Benutzer werden nach der Anmeldung abgewiesen"

    Wie bei den meisten Anbietern authentifiziert OneLogin zunächst den Benutzer und prüft anschließend die Berechtigung. Ein nicht zugewiesener Benutzer meldet sich erfolgreich an und wird dann abgewiesen, was eher wie ein digna-Fehler aussieht als wie eine Zugriffssteuerungsentscheidung.

---

## Schritt 6: Die Discovery-URL erstellen

Ersetzen Sie Ihre OneLogin-Subdomain:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Zum Beispiel:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "Das /2 ist die API-Version"

    OneLogins aktuelle OIDC-Implementierung befindet sich unter `/oidc/2/`. Ältere Dokumentation zeigt `/oidc/` ohne Versionsangabe, was auf die eingestellte erste Version verweist. Prüfen Sie bei Zweifeln die **Issuer URL** im SSO-Tab — die Discovery-URL ist die Issuer-URL plus `/.well-known/openid-configuration`.

---

## Schritt 7: digna konfigurieren

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Login with OneLogin"
```

### `config.toml`

```toml
[oidc.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

Der `key` in beiden Dateien muss übereinstimmen — hier `onelogin`.

---

## Schritt 8: Test

Starten Sie Backend und Webserver neu und öffnen Sie dann das Dashboard. Siehe [Testing Login](overview.md#testing-login) für die vollständige Checkliste.

---

## Fehlerbehebung OneLogin

### redirect_uri did not match

Die Callback-URL fehlt unter **Configuration → Redirect URI's**, oder die Einträge wurden durch Kommas statt durch Zeilenumbrüche getrennt.

### invalid_client at the Token Step

**Token Endpoint → Authentication Method** ist auf *None* gesetzt, oder das Client-Secret in `config.toml` ist veraltet. Zeigen Sie das Secret im **SSO**-Tab an und vergleichen Sie es.

### Die App wird Benutzern nicht angezeigt

Keine Rolle oder Gruppe hat auf dem **Access**-Tab Zugriff erhalten.

### 404 auf der Discovery-URL

Die Subdomain ist falsch oder die URL lässt `/oidc/2/` weg. Vergleichen Sie mit der **Issuer URL** im SSO-Tab.

---

## Siehe auch

- [Single Sign-On Overview](overview.md) — Konfigurationsreferenz, Tests und allgemeine Fehlerbehebung
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)