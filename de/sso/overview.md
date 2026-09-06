# Single Sign-On Übersicht

---

## Inhaltsverzeichnis

1. [Einführung und Übersicht](#introduction-and-overview)
2. [Provider-Anleitungen](#provider-guides)
3. [Konfigurationsschritte](#configuration-steps)
4. [Dashboard-Konfiguration](#dashboard-configuration)
5. [Backend-Konfiguration](#backend-configuration)
6. [Login testen](#testing-login)
7. [Fehlerbehebung](#troubleshooting)
8. [Unterstützte Provider](#supported-providers)

---

## Einführung und Übersicht {: #introduction-and-overview }

Dieser Leitfaden bietet Schritt-für-Schritt-Anweisungen zur Integration von Single Sign-On (SSO) in die digna-Plattform mithilfe von **OpenID Connect (OIDC)**.

### Was ist SSO?

Single Sign-On ermöglicht es Benutzern, sich mit ihren Unternehmenszugangsdaten über externe Identity Provider sicher bei digna anzumelden. Anwender können sich mit ihren Firmenzugangsdaten authentifizieren, anstatt separate digna-Passwörter zu verwalten.

### Funktionsweise

SSO in digna wird über das OIDC-Protokoll umgesetzt. Mehrere Identity Provider können parallel konfiguriert werden, indem zwei zentrale Konfigurationsdateien angepasst werden:

- **`dashboard_config.toml`** — Steuert die Frontend-Login-Oberfläche
- **`config.toml`** — Konfiguriert die Backend-OIDC-Verbindungen

### Unterstützte Provider {: #supported-providers-overview }

Beispiele in diesem Leitfaden verwenden **Microsoft** und **Google**, aber **jeder OIDC-kompatible Provider** kann nach derselben Struktur integriert werden.

---

## Provider-Anleitungen {: #provider-guides }

Jeder Provider benötigt dieselben vier Werte — eine Client-ID, ein Client-Secret, eine Redirect-URI und eine Discovery-URL — aber jeder Anbieter legt diese Werte an anderer Stelle in seiner Admin-Konsole ab, und einige haben provider-spezifische Schritte, die andere nicht haben. Die untenstehenden Anleitungen decken diesen Teil ab; diese Seite behandelt den digna-Teil, der für alle gleich ist.

| Provider | Anleitung | Wissenswert |
|---|---|---|
| **AD FS** | [Set up SSO with AD FS](adfs_sso_guide.md) | Self-hosted; der einzige hier, bei dem Sie den Token-Dienst selbst kontrollieren |
| **Auth0** | [Set up SSO with Auth0](auth0_sso_guide.md) | Discovery-URL ist pro Tenant; benutzerdefinierte Domains ändern sie |
| **Google Workspace** | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) | Der Consent-Screen muss veröffentlicht werden, bevor nicht-test Nutzer sich anmelden können |
| **Keycloak** | [Set up SSO with Keycloak](keycloak_sso_guide.md) | Self-hosted; Discovery-URL ist pro Realm |
| **Microsoft Entra ID** | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | Tenant-ID erscheint in der Discovery-URL; Secrets laufen ab |
| **Okta** | [Set up SSO with Okta](okta_sso_guide.md) | Auswahl des Authorization Servers ändert die Discovery-URL |
| **OneLogin** | [Set up SSO with OneLogin](onelogin_sso_guide.md) | Der OIDC-App-Typ muss bei der Erstellung gewählt werden und kann später nicht geändert werden |
| **PingOne** | [Set up SSO with PingOne](pingone_sso_guide.md) | Environment-ID erscheint in der Discovery-URL |

Jeder andere OIDC-kompatible Provider funktioniert auf die gleiche Weise — siehe [Other OIDC Providers](#supported-providers).

---

## Konfigurationsschritte {: #configuration-steps }

Die SSO-Konfiguration erfordert Änderungen an zwei Dateien. Dieser Abschnitt erklärt, wie jede Datei zu konfigurieren ist.

### Übersicht der Konfigurationsdateien

| Datei | Speicherort | Zweck |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend-Login-Oberfläche |
| **config.toml** | `/config.toml` | Backend-OIDC-Verbindungen |

Beide Dateien müssen für ein funktionierendes SSO korrekt konfiguriert sein.

---

## Dashboard-Konfiguration {: #dashboard-configuration }

### Dateipfad

```
dashboard/dashboard_config.toml
```

### Schritt 1: OIDC-Provider hinzufügen

Fügen Sie Einträge unter dem Array `[[login.oidc]]` für jeden Identity Provider hinzu, den Sie unterstützen möchten.

**Beispiel mit Microsoft und Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Schritt 2: Login-Optionen konfigurieren

Geben Sie an, ob passwortbasierte Anmeldungen erlaubt sein sollen:

```toml
[login]
usePassword = true
```

### Konfigurationsparameter

#### `[[login.oidc]]` Abschnitt

| Parameter | Typ | Erforderlich | Beschreibung |
|---|---|---|---|
| `key` | string | Ja | Eindeutiger Bezeichner für die OIDC-Verbindung (muss mit dem key in config.toml übereinstimmen) |
| `label` | string | Ja | Text, der auf dem Login-Button angezeigt wird (z. B. "Login with Microsoft") |

#### `[login]` Abschnitt

| Parameter | Typ | Standard | Beschreibung |
|---|---|---|---|
| `usePassword` | boolean | false | Erlaubt passwortbasierte Anmeldung zusätzlich zu SSO |

### Bedeutung von usePassword

**Wenn `usePassword = true`:**
- Der Login-Bildschirm zeigt SSO-Buttons (z. B. "Login with Microsoft")
- Der Login-Bildschirm zeigt zusätzlich Benutzername- und Passwortfelder
- Benutzer können sich mit beiden Methoden authentifizieren
- Ermöglicht hybride Setups, in denen einige Benutzer SSO und andere Passwörter verwenden

**Wenn `usePassword = false` (oder weggelassen):**
- Der Login-Bildschirm zeigt nur SSO-Buttons
- Keine Benutzername-/Passwortfelder
- Nur OIDC-Authentifizierung ist verfügbar

!!! tip "Tipp"

    Die passwortbasierte Anmeldung ist nur für Benutzer verfügbar, die mit Passwörtern über den Befehl `digna user add` oder über das Dashboard erstellt wurden.

### Komplettes Beispiel

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## Backend-Konfiguration {: #backend-configuration }

### Dateipfad

```
/config.toml
```

(Root-Verzeichnis der digna-Installation)

### Schritt 1: OIDC-Provider-Abschnitte hinzufügen

Jeder Provider muss einen eigenen `[oidc.<key>]`-Abschnitt haben. Der key muss mit dem in `dashboard_config.toml` definierten `key` übereinstimmen.

### Microsoft-Konfiguration

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google-Konfiguration

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Konfigurationsparameter

| Parameter | Typ | Erforderlich | Beschreibung | Beispiel |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Ja | Client-ID vom Identity Provider | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Ja | Client-Secret vom Identity Provider | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Ja | Callback-URL nach der Authentifizierung | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Ja | OIDC-Konfigurationsendpunkt | `https://login.microsoftonline.com/...` |

!!! warning "Wichtig"

    Ersetzen Sie Platzhalterwerte (`<client_id>`, `<client_secret>`, `<tenant_id>`) durch tatsächliche Anmeldeinformationen aus dem Entwicklerportal Ihres Identity Providers.

### Redirect URI

Die Redirect-URI muss in der Konfiguration Ihres Identity Providers identisch sein:

```
http://localhost:5173/oidc/callback
```

Wenn digna unter einer anderen Domain gehostet wird, passen Sie diese entsprechend an:
- Lokal: `http://localhost:5173/oidc/callback`
- Produktion: `https://digna.yourdomain.com/oidc/callback`

### Komplettes Beispiel

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Login testen {: #testing-login }

Nachdem Sie die Konfiguration abgeschlossen haben, vergewissern Sie sich, dass SSO korrekt funktioniert.

### Vor dem Test: Checkliste

Stellen Sie vor dem Test sicher:

- [ ] `dashboard_config.toml` wurde mit OIDC-Providern aktualisiert
- [ ] `config.toml` wurde mit OIDC-Anmeldeinformationen aktualisiert
- [ ] Beide Dateien wurden gespeichert
- [ ] Anmeldeinformationen sind korrekt (Client-ID, Client-Secret)
- [ ] Redirect-URI stimmt mit Ihrer Deployment-URL überein
- [ ] Die Anwendung beim Identity Provider ist mit der Redirect-URI konfiguriert

### Testschritte

#### Schritt 1: Dienste neu starten

Starten Sie das digna-Backend und den Webserver neu, um Änderungen anzuwenden.

**Wenn als Dienst unter Windows ausgeführt:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Wenn als Dienst unter Linux oder macOS ausgeführt:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Wenn manuell ausgeführt:**
```bash
digna serve --address localhost --port 8082
```

**Starten Sie auch den Webserver neu** — IIS oder Tomcat unter Windows, nginx oder Apache unter Linux und macOS.

#### Schritt 2: Dashboard öffnen

Öffnen Sie das digna-Dashboard in Ihrem Browser:

```
http://localhost:5173
```

(oder Ihre konfigurierte Dashboard-URL)

#### Schritt 3: Login-Buttons prüfen

Prüfen Sie, ob Login-Buttons für jeden konfigurierten Provider angezeigt werden:

- Es sollte ein "Login with Microsoft"-Button sichtbar sein
- Es sollte ein "Login with Google"-Button sichtbar sein
- (Wenn usePassword = true) Es sollten Benutzername-/Passwortfelder sichtbar sein

Wenn Buttons nicht angezeigt werden:
- Prüfen Sie, ob `dashboard_config.toml` gespeichert wurde
- Prüfen Sie, ob der Dashboard-Service neu gestartet wurde
- Prüfen Sie die Browserkonsole (F12) auf Fehler

#### Schritt 4: SSO-Login testen

Klicken Sie einen der SSO-Buttons (z. B. "Login with Microsoft"):

1. Sie sollten zur Login-Seite des Identity Providers weitergeleitet werden
2. Melden Sie sich mit Ihren Unternehmenszugangsdaten an
3. Sie sollten zurück zu digna weitergeleitet werden
4. Sie sollten bei digna eingeloggt sein

#### Schritt 5: Benutzererstellung prüfen

Nach erfolgreichem SSO-Login:

- Der Benutzer sollte automatisch in digna angelegt werden
- Der Benutzer sollte eingeloggt sein
- Das Benutzerprofil sollte Ihre Identity-Provider-Daten anzeigen
- Sie sollten das digna-Dashboard sehen

#### Schritt 6: Passwort-Login testen (falls aktiviert)

Wenn `usePassword = true`:

1. Melden Sie sich bei digna ab
2. Geben Sie auf der Loginseite Benutzername und Passwort ein
3. Sie sollten sich mit Passwort anmelden können

---

## Fehlerbehebung {: #troubleshooting }

### Login-Buttons werden nicht angezeigt

**Symptome:**
- OIDC-Login-Buttons nicht auf der Login-Seite sichtbar
- Nur Passwortfelder sichtbar (wenn usePassword = true)

**Ursachen & Lösungen:**
1. Prüfen Sie, ob `dashboard_config.toml` im Verzeichnis `dashboard/` liegt
2. Vergewissern Sie sich, dass `[[login.oidc]]`-Abschnitte mit korrekter Syntax vorhanden sind
3. Starten Sie den Dashboard-Service neu
4. Löschen Sie den Browser-Cache (Strg+Shift+Entf oder Cmd+Shift+Entf)
5. Prüfen Sie die Browserkonsole (F12 → Console) auf Fehler

---

### Redirect-URI Mismatch-Fehler

**Symptome:**
- Nach Klick auf den SSO-Button erscheint ein Fehler zu "redirect_uri mismatch"
- Fehler "The redirect URI is not registered"

**Ursachen & Lösungen:**
1. Überprüfen Sie `DIGNA_OIDC_REDIRECT_URI` in `config.toml`
2. Vergewissern Sie sich, dass die Redirect-URI im Identity Provider registriert ist
3. Stellen Sie sicher, dass beide exakt identische URLs verwenden (inkl. Protokoll, Domain, Pfad)
4. Prüfen Sie auf Tippfehler in der Redirect-URI
5. Wenn HTTPS verwendet wird, stellen Sie sicher, dass das Zertifikat gültig ist

---

### Ungültige Client-Anmeldeinformationen

**Symptome:**
- Fehler "Invalid client ID or secret"
- Authentifizierung schlägt mit Anmeldeinformationsfehler fehl

**Ursachen & Lösungen:**
1. Überprüfen Sie `DIGNA_OIDC_CLIENT_ID` und `DIGNA_OIDC_CLIENT_SECRET` auf Richtigkeit
2. Stellen Sie sicher, dass keine zusätzlichen Leerzeichen oder Sonderzeichen vorhanden sind
3. Prüfen Sie, ob die Anmeldeinformationen nicht abgelaufen oder widerrufen wurden
4. Starten Sie das Backend neu, nachdem Sie die Konfiguration aktualisiert haben
5. Prüfen Sie das Identity Provider-Portal, um zu bestätigen, dass die Anmeldeinformationen aktiv sind

---

### Login hängt oder läuft in einen Timeout

**Symptome:**
- Klick auf den SSO-Button bewirkt nichts
- Timeout nach einigen Sekunden
- Browser zeigt "Failed to connect" oder ähnliches

**Ursachen & Lösungen:**
1. Vergewissern Sie sich, dass das digna-Backend läuft: `digna repo check`
2. Prüfen Sie die Netzwerkverbindung zum Identity Provider
3. Stellen Sie sicher, dass `DIGNA_OIDC_CONFIGURATION_URL` erreichbar ist
4. Prüfen Sie Firewall-Regeln, die ausgehende HTTPS-Verbindungen blockieren könnten
5. Prüfen Sie, ob Backend und Dashboard sich gegenseitig erreichen können

---

### Benutzer werden nicht automatisch erstellt

**Symptome:**
- SSO-Login gelingt, aber Benutzer wird nicht in digna angelegt
- Nach SSO-Login tritt ein Berechtigungsfehler auf

**Ursachen & Lösungen:**
1. Überprüfen Sie, ob die OIDC-Konfiguration korrekt ist
2. Prüfen Sie, ob Benutzerberechtigungen korrekt eingerichtet sind
3. Überprüfen Sie die digna-Logs auf Fehlermeldungen
4. Starten Sie das Backend neu
5. Kontaktieren Sie support@digna.ai, wenn das Problem weiterhin besteht

---

## Unterstützte Provider {: #supported-providers }

### Getestet & Unterstützt

Die folgenden OIDC-Provider wurden getestet und sind bekannt, dass sie funktionieren:

| Provider | Konfigurations-URL | Einrichtungsanleitung |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Set up SSO with AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Set up SSO with Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Set up SSO with Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Set up SSO with Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Set up SSO with OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Set up SSO with PingOne](pingone_sso_guide.md) |

### Andere OIDC-Provider

Jeder Provider, der OpenID Connect unterstützt, kann integriert werden. Erforderliche Informationen:

- Client-ID
- Client-Secret
- OpenID-Konfigurations-URL (meist unter `/.well-known/openid-configuration`)
- Unterstützte Scopes (typischerweise `openid profile email`)

Kontaktieren Sie support@digna.ai, wenn Sie Hilfe bei der Integration eines bestimmten Providers benötigen.

---

## Best Practices

**TUN SIE:**
- Verwenden Sie in der Produktion HTTPS (nicht HTTP)
- Speichern Sie Client-Secrets sicher (verwenden Sie wenn möglich Umgebungsvariablen)
- Rotieren Sie Secrets periodisch
- Testen Sie zunächst in einer Nicht-Produktionsumgebung
- Dokumentieren Sie, welche Provider konfiguriert sind
- Überwachen Sie Login-Logs auf ungewöhnliche Aktivitäten
- Halten Sie die Konfiguration des Identity Providers mit der digna-Konfiguration synchron

**TUN SIE NICHT:**
- Speichern Sie Client-Secrets in der Versionskontrolle
- Verwenden Sie HTTP-Redirect-URIs in der Produktion
- Konfigurieren Sie mehrere Provider mit demselben Key
- Lassen Sie Standard-/Testanmeldeinformationen in der Produktion
- Legen Sie Konfigurationsdateien mit Secrets offen
- Mischen Sie Entwicklungs- und Produktionsanmeldeinformationen

---

## Support

Brauchen Sie Hilfe bei der SSO-Konfiguration?

- **E-Mail:** support@digna.ai
- **Dokumentation:** https://docs.digna.ai
- **Website:** https://www.digna.ai

---

**Zuletzt aktualisiert:** 30. August 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**