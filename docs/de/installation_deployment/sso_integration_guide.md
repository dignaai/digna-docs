---
title: Single Sign-On (SSO) Integrationsanleitung | digna Dokumentation
description: Schritt-für-Schritt-Anleitung zur Konfiguration von Single Sign-On (SSO) für digna mit OpenID Connect (OIDC). Behandelt Dashboard- und Backend-Konfiguration, Tests, Fehlerbehebung und unterstützte Identity Provider wie Microsoft Entra ID, Google Workspace und Okta.
image: /assets/logo_square.png
keywords:
  - digna sso
  - Single Sign-On
  - OIDC-Integration
  - OpenID Connect
  - Microsoft Entra ID
  - Azure AD SSO
  - Google Workspace SSO
  - Okta-Integration
  - Unternehmensauthentifizierung
lang: en
robots: index, follow
og_title: digna Single Sign-On (SSO) Integration Guide
og_description: Configure Single Sign-On for digna using OpenID Connect. Step-by-step setup for Microsoft Entra ID, Google Workspace, Okta, and other OIDC-compliant identity providers.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Single Sign-On Integrationsanleitung

---

## Inhaltsverzeichnis

1. [Einführung und Überblick](#introduction-and-overview)
2. [Konfigurationsschritte](#configuration-steps)
3. [Dashboard-Konfiguration](#dashboard-configuration)
4. [Backend-Konfiguration](#backend-configuration)
5. [Login testen](#testing-login)
6. [Fehlerbehebung](#troubleshooting)
7. [Unterstützte Provider](#supported-providers)

---

## Einführung und Überblick {: #introduction-and-overview }

Diese Anleitung beschreibt Schritt für Schritt, wie Single Sign-On (SSO) in der digna-Plattform mithilfe von **OpenID Connect (OIDC)** integriert wird.

### Was ist SSO?

Single Sign-On ermöglicht es Benutzern, sich mit ihren Unternehmensanmeldedaten sicher bei digna anzumelden, indem externe Identity Provider verwendet werden. Nutzer können sich mit ihren Firmenanmeldedaten authentifizieren, anstatt separate digna-Passwörter zu verwalten.

### Wie funktioniert es?

SSO in digna wird über das OIDC-Protokoll umgesetzt. Mehrere Identity Provider können parallel konfiguriert werden, indem zwei zentrale Konfigurationsdateien angepasst werden:

- **`dashboard_config.toml`** — Steuert die Frontend-Anmeldeschnittstelle
- **`config.toml`** — Konfiguriert die Backend-OIDC-Verbindungen

### Unterstützte Provider {: #supported-providers-overview }

Beispiele in dieser Anleitung verwenden **Microsoft** und **Google**, aber **jeder OIDC-konforme Provider** kann nach demselben Schema integriert werden.

Gängige OIDC-Provider sind:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Weitere OIDC-konforme Identity Provider

---

## Konfigurationsschritte {: #configuration-steps }

Die SSO-Konfiguration erfordert Änderungen an zwei Dateien. Dieser Abschnitt erklärt, wie jede Datei zu konfigurieren ist.

### Übersicht der Konfigurationsdateien

| Datei | Speicherort | Zweck |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend-Anmeldeschnittstelle |
| **config.toml** | `/config.toml` | Backend OIDC-Verbindungen |

Beide Dateien müssen konfiguriert werden, damit SSO korrekt funktioniert.

---

## Dashboard-Konfiguration {: #dashboard-configuration }

### Dateispeicherort

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

### Schritt 2: Anmeldeoptionen konfigurieren

Geben Sie an, ob passwortbasierte Anmeldung erlaubt sein soll:

```toml
[login]
usePassword = true
```

### Konfigurationsparameter

#### `[[login.oidc]]` Abschnitt

| Parameter | Typ | Erforderlich | Beschreibung |
|---|---|---|---|
| `key` | string | Ja | Eindeutiger Bezeichner für die OIDC-Verbindung (muss mit dem Key in config.toml übereinstimmen) |
| `label` | string | Ja | Text, der auf der Anmelde-Schaltfläche angezeigt wird (z. B. "Login with Microsoft") |

#### `[login]` Abschnitt

| Parameter | Typ | Standard | Beschreibung |
|---|---|---|---|
| `usePassword` | boolean | false | Erlaubt passwortbasierte Anmeldung zusätzlich zu SSO |

### Bedeutung von usePassword

**Wenn `usePassword = true`:**
- Der Anmeldebildschirm zeigt SSO-Schaltflächen (z. B. "Login with Microsoft")
- Der Anmeldebildschirm zeigt zusätzlich Felder für Benutzername und Passwort
- Benutzer können sich mit einer der beiden Methoden authentifizieren
- Ermöglicht hybride Setups, in denen einige Benutzer SSO und andere Passwörter verwenden

**Wenn `usePassword = false` (oder weggelassen):**
- Der Anmeldebildschirm zeigt nur SSO-Schaltflächen
- Keine Benutzername-/Passwort-Felder
- Nur OIDC-Authentifizierung ist verfügbar

!!! tip "Tipp"

    Die passwortbasierte Anmeldung ist nur für Benutzer verfügbar, die mit Passwörtern erstellt wurden (z. B. mittels des Befehls `digna user add` oder über das Dashboard).

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

### Dateispeicherort

```
/config.toml
```

(Root-Verzeichnis der digna-Installation)

### Schritt 1: OIDC-Provider-Abschnitte hinzufügen

Jeder Provider benötigt einen eigenen Abschnitt `[oidc.<key>]`. Der Key muss mit dem `key` in `dashboard_config.toml` übereinstimmen.

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

    Ersetzen Sie Platzhalterwerte (`<client_id>`, `<client_secret>`, `<tenant_id>`) durch die tatsächlichen Zugangsdaten aus dem Entwicklerportal Ihres Identity Providers.

### Redirect URI

Die Redirect-URI muss mit der in der Identity-Provider-Konfiguration registrierten URI übereinstimmen:

```
http://localhost:5173/oidc/callback
```

Wenn digna unter einer anderen Domain gehostet wird, passen Sie die URI entsprechend an:
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

Nach Abschluss der Konfiguration prüfen Sie, ob SSO korrekt funktioniert.

### Vorbereitungs-Checkliste

Bevor Sie testen, vergewissern Sie sich:

- [ ] `dashboard_config.toml` wurde mit OIDC-Providern aktualisiert
- [ ] `config.toml` wurde mit OIDC-Zugangsdaten aktualisiert
- [ ] Beide Dateien wurden gespeichert
- [ ] Zugangsdaten sind korrekt (Client ID, Client Secret)
- [ ] Redirect-URI stimmt mit Ihrer Deployment-URL überein
- [ ] Die Anwendung im Identity Provider ist mit der Redirect-URI konfiguriert

### Testschritte

#### Schritt 1: Dienste neu starten

Starten Sie das digna-Backend und den Webserver neu, damit die Änderungen wirksam werden.

**Wenn als Windows-Dienst ausgeführt:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Wenn manuell ausgeführt:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Bei Verwendung von IIS oder Tomcat:**
Starten Sie den Webserver-Dienst neu.

#### Schritt 2: Dashboard öffnen

Öffnen Sie das digna-Dashboard in Ihrem Browser:

```
http://localhost:5173
```

(oder Ihre konfigurierte Dashboard-URL)

#### Schritt 3: Anmelde-Schaltflächen prüfen

Stellen Sie sicher, dass für jeden konfigurierten Provider eine Anmelde-Schaltfläche angezeigt wird:

- Es sollte eine Schaltfläche "Login with Microsoft" sichtbar sein
- Es sollte eine Schaltfläche "Login with Google" sichtbar sein
- (Wenn usePassword = true) Es sollten Benutzername-/Passwort-Felder sichtbar sein

Wenn Schaltflächen nicht erscheinen:
- Prüfen Sie, ob `dashboard_config.toml` gespeichert wurde
- Prüfen Sie, ob der Dashboard-Dienst neu gestartet wurde
- Prüfen Sie die Browser-Konsole (F12) auf Fehler

#### Schritt 4: SSO-Anmeldung testen

Klicken Sie auf eine der SSO-Schaltflächen (z. B. "Login with Microsoft"):

1. Sie sollten zur Login-Seite des Identity Providers weitergeleitet werden
2. Melden Sie sich mit Ihren Unternehmensanmeldedaten an
3. Sie sollten zurück zu digna weitergeleitet werden
4. Sie sollten in digna angemeldet sein

#### Schritt 5: Benutzererstellung prüfen

Nach erfolgreicher SSO-Anmeldung:

- Der Benutzer sollte automatisch in digna angelegt werden
- Der Benutzer sollte angemeldet sein
- Das Benutzerprofil sollte Informationen des Identity Providers anzeigen
- Sie sollten das digna-Dashboard sehen

#### Schritt 6: Passwort-Anmeldung testen (falls aktiviert)

Wenn `usePassword = true`:

1. Melden Sie sich von digna ab
2. Geben Sie auf der Anmeldeseite Benutzername und Passwort ein
3. Sie sollten sich mit Passwortanmeldeinformationen anmelden können

---

## Fehlerbehebung {: #troubleshooting }

### Anmelde-Schaltflächen erscheinen nicht

**Symptome:**
- OIDC-Anmelde-Schaltflächen sind auf der Anmeldeseite nicht sichtbar
- Sie sehen nur Passwortfelder (wenn usePassword = true)

**Ursachen & Lösungen:**
1. Prüfen Sie, ob `dashboard_config.toml` im Verzeichnis `dashboard/` liegt
2. Vergewissern Sie sich, dass `[[login.oidc]]`-Abschnitte mit korrekter Syntax vorhanden sind
3. Starten Sie den Dashboard-Dienst neu
4. Leeren Sie den Browser-Cache (Strg+Umschalt+Entf oder Cmd+Shift+Delete)
5. Prüfen Sie die Browser-Konsole (F12 → Konsole) auf Fehler

---

### Redirect-URI Mismatch-Fehler

**Symptome:**
- Nach Klick auf die SSO-Schaltfläche erscheint ein Fehler zu "redirect_uri mismatch"
- Fehler "The redirect URI is not registered"

**Ursachen & Lösungen:**
1. Prüfen Sie `DIGNA_OIDC_REDIRECT_URI` in `config.toml` auf Korrektheit
2. Vergewissern Sie sich, dass die Redirect-URI im Identity Provider registriert ist
3. Stellen Sie sicher, dass beide URLs identisch sind (inklusive Protokoll, Domain, Pfad)
4. Prüfen Sie auf Tippfehler in der Redirect-URI
5. Wenn HTTPS verwendet wird, stellen Sie sicher, dass das Zertifikat gültig ist

---

### Ungültige Client-Zugangsdaten

**Symptome:**
- Fehler "Invalid client ID or secret"
- Authentifizierung schlägt mit Zugangsdatenfehler fehl

**Ursachen & Lösungen:**
1. Prüfen Sie `DIGNA_OIDC_CLIENT_ID` und `DIGNA_OIDC_CLIENT_SECRET` auf Richtigkeit
2. Achten Sie auf keine zusätzlichen Leerzeichen oder ungewollte Sonderzeichen
3. Prüfen Sie, ob die Zugangsdaten abgelaufen oder widerrufen wurden
4. Starten Sie den Backend-Dienst nach dem Aktualisieren der Konfiguration neu
5. Prüfen Sie im Identity Provider-Portal, ob die Zugangsdaten aktiv sind

---

### Anmeldung bleibt hängen oder läuft ins Timeout

**Symptome:**
- Klick auf SSO-Schaltfläche bewirkt nichts
- Timeout nach einigen Sekunden
- Browser zeigt "Failed to connect" oder ähnliches

**Ursachen & Lösungen:**
1. Prüfen Sie, ob das digna-Backend läuft: `digna repo check`
2. Prüfen Sie die Netzwerkverbindung zum Identity Provider
3. Vergewissern Sie sich, dass `DIGNA_OIDC_CONFIGURATION_URL` erreichbar ist
4. Prüfen Sie Firewall-Regeln, die ausgehende HTTPS-Verbindungen blockieren könnten
5. Prüfen Sie, ob Backend und Dashboard sich gegenseitig erreichen können

---

### Benutzer werden nicht automatisch erstellt

**Symptome:**
- SSO-Anmeldung gelingt, aber der Benutzer wird nicht in digna angelegt
- Nach SSO-Anmeldung tritt ein Berechtigungsfehler auf

**Ursachen & Lösungen:**
1. Prüfen Sie die OIDC-Konfiguration auf Korrektheit
2. Prüfen Sie, ob Benutzerberechtigungen korrekt eingerichtet sind
3. Überprüfen Sie die digna-Logs auf Fehlermeldungen
4. Starten Sie den Backend-Dienst neu
5. Kontaktieren Sie support@digna.ai, falls das Problem bestehen bleibt

---

## Unterstützte Provider {: #supported-providers }

### Getestet & Unterstützt

Die folgenden OIDC-Provider wurden getestet und sind bekannt funktionsfähig:

| Provider | Konfigurations-URL | Einrichtungshilfe |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft-Dokumentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google-Dokumentation](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta-Dokumentation](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Andere OIDC-Provider

Jeder Provider, der OpenID Connect unterstützt, kann integriert werden. Benötigte Informationen:

- Client ID
- Client Secret
- OpenID-Konfigurations-URL (in der Regel unter `/.well-known/openid-configuration`)
- Unterstützte Scopes (typischerweise `openid profile email`)

Kontaktieren Sie support@digna.ai, wenn Sie Hilfe bei der Integration eines bestimmten Providers benötigen.

---

## Best Practices

**TUNEN SIE:**
- Verwenden Sie in der Produktion HTTPS (nicht HTTP)
- Speichern Sie Client-Secrets sicher (verwenden Sie nach Möglichkeit Umgebungsvariablen)
- Rotieren Sie Secrets regelmäßig
- Testen Sie zuerst in einer Nicht-Produktionsumgebung
- Dokumentieren Sie, welche Provider konfiguriert sind
- Überwachen Sie Anmeldeprotokolle auf ungewöhnliche Aktivitäten
- Halten Sie die Konfiguration des Identity Providers und die digna-Konfiguration synchron

**NIE:**
- Speichern Sie Client-Secrets in Versionskontrolle
- Verwenden Sie HTTP-Redirect-URIs in der Produktion
- Konfigurieren Sie mehrere Provider mit demselben Key
- Belassen Sie Standard-/Test-Zugangsdaten in der Produktion
- Legen Sie Konfigurationsdateien mit Secrets offen
- Mischen Sie Entwicklungs- und Produktionszugangsdaten

---

## Support

Benötigen Sie Hilfe bei der SSO-Konfiguration?

- **E-Mail:** support@digna.ai
- **Dokumentation:** https://docs.digna.ai
- **Website:** https://www.digna.ai

---

**Zuletzt aktualisiert:** 30. August 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**