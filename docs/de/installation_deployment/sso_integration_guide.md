---
title: Single Sign-On (SSO) Integrationsanleitung | digna Dokumentation
description: Schritt-für-Schritt-Anleitung zur Konfiguration von Single Sign-On (SSO) für digna mit OpenID Connect (OIDC). Behandelt Dashboard- und Backend-Konfiguration, Tests, Fehlerbehebung und unterstützte Identitätsanbieter wie Microsoft Entra ID, Google Workspace und Okta.
image: /assets/logo_square.png
keywords:
  - digna sso
  - single sign-on
  - oidc integration
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta integration
  - enterprise authentication
lang: en
robots: index, follow
og_title: digna Single Sign-On (SSO) Integrationsanleitung
og_description: Konfigurieren Sie Single Sign-On für digna mit OpenID Connect. Schritt-für-Schritt-Einrichtung für Microsoft Entra ID, Google Workspace, Okta und andere OIDC-kompatible Identitätsanbieter.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Single Sign-On Integrationsanleitung

---

## Inhaltsverzeichnis

1. [Einführung und Übersicht](#introduction-and-overview)
2. [Konfigurationsschritte](#configuration-steps)
3. [Dashboard-Konfiguration](#dashboard-configuration)
4. [Backend-Konfiguration](#backend-configuration)
5. [Login testen](#testing-login)
6. [Fehlerbehebung](#troubleshooting)
7. [Unterstützte Anbieter](#supported-providers)

---

## Einführung und Übersicht {: #introduction-and-overview }

Dieses Dokument bietet eine Schritt-für-Schritt-Anleitung zur Integration von Single Sign-On (SSO) in die digna-Plattform mithilfe von **OpenID Connect (OIDC)**.

### Was ist SSO?

Single Sign-On ermöglicht es Benutzern, sich sicher bei digna mit ihren Unternehmensanmeldeinformationen über externe Identitätsanbieter anzumelden. Benutzer authentifizieren sich mit ihren Firmenanmeldeinformationen, anstatt separate digna-Passwörter zu verwalten.

### Wie funktioniert es

SSO in digna wird über das OIDC-Protokoll implementiert. Mehrere Identitätsanbieter können parallel konfiguriert werden, indem zwei wichtige Konfigurationsdateien angepasst werden:

- **`dashboard_config.toml`** — Steuert die Login-Oberfläche des Frontends
- **`config.toml`** — Konfiguriert die OIDC-Verbindungen des Backends

### Unterstützte Anbieter {: #supported-providers-overview }

Beispiele in diesem Leitfaden verwenden **Microsoft** und **Google**, aber **jeder OIDC-kompatible Anbieter** kann nach derselben Struktur integriert werden.

Gängige OIDC-Anbieter sind:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Andere OIDC-kompatible Identitätsanbieter

---

## Konfigurationsschritte {: #configuration-steps }

Die SSO-Konfiguration erfordert Änderungen an zwei Dateien. Dieser Abschnitt erklärt, wie jede Datei konfiguriert wird.

### Übersicht der Konfigurationsdateien

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend Login-Oberfläche |
| **config.toml** | `/config.toml` | Backend OIDC-Verbindungen |

Beide Dateien müssen konfiguriert sein, damit SSO ordnungsgemäß funktioniert.

---

## Dashboard-Konfiguration {: #dashboard-configuration }

### Dateipfad

```
dashboard/dashboard_config.toml
```

### Schritt 1: OIDC-Anbieter hinzufügen

Fügen Sie Einträge unter dem Array `[[login.oidc]]` für jeden Identitätsanbieter hinzu, den Sie unterstützen möchten.

**Beispiel mit Microsoft und Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Mit Microsoft anmelden"

[[login.oidc]]
key = "google"
label = "Mit Google anmelden"
```

### Schritt 2: Login-Optionen konfigurieren

Geben Sie an, ob passwortbasierte Anmeldung erlaubt sein soll:

```toml
[login]
usePassword = true
```

### Konfigurationsparameter

#### `[[login.oidc]]` Abschnitt

| Parameter | Typ | Erforderlich | Beschreibung |
|---|---|---|---|
| `key` | string | Ja | Eindeutiger Bezeichner für die OIDC-Verbindung (muss mit dem Schlüssel in config.toml übereinstimmen) |
| `label` | string | Ja | Text, der auf der Login-Schaltfläche angezeigt wird (z. B. "Mit Microsoft anmelden") |

#### `[login]` Abschnitt

| Parameter | Typ | Standard | Beschreibung |
|---|---|---|---|
| `usePassword` | boolean | false | Passwortbasierte Anmeldung zusätzlich zu SSO erlauben |

### Verständnis von usePassword

**Wenn `usePassword = true`:**
- Auf dem Login-Bildschirm werden SSO-Schaltflächen angezeigt (z. B. "Mit Microsoft anmelden")
- Der Login-Bildschirm zeigt zusätzlich Benutzername- und Passwortfelder
- Benutzer können sich mit einer der beiden Methoden authentifizieren
- Ermöglicht hybride Setups, in denen einige Benutzer SSO und andere Passwörter verwenden

**Wenn `usePassword = false` (oder weggelassen):**
- Der Login-Bildschirm zeigt nur SSO-Schaltflächen
- Keine Benutzername-/Passwortfelder
- Nur OIDC-Authentifizierung ist verfügbar

> **💡 Tipp**
>
> Die passwortbasierte Anmeldung ist nur für Benutzer verfügbar, die mit Passwörtern über den Befehl `digna user add` oder über das Dashboard erstellt wurden.

### Komplettes Beispiel

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Mit Microsoft anmelden"

[[login.oidc]]
key = "google"
label = "Mit Google anmelden"

[[login.oidc]]
key = "okta"
label = "Mit Okta anmelden"
```

---

## Backend-Konfiguration {: #backend-configuration }

### Dateipfad

```
/config.toml
```

(Root-Verzeichnis der digna-Installation)

### Schritt 1: OIDC-Anbieterabschnitte hinzufügen

Jeder Anbieter benötigt einen eigenen Abschnitt `[oidc.<key>]`. Der Schlüssel muss mit dem `key` in `dashboard_config.toml` übereinstimmen.

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
| `DIGNA_OIDC_CLIENT_ID` | string | Ja | Client-ID vom Identitätsanbieter | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Ja | Client-Secret vom Identitätsanbieter | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Ja | Callback-URL nach der Authentifizierung | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Ja | OIDC-Konfigurationsendpunkt | `https://login.microsoftonline.com/...` |

> **⚠️ Wichtig**
>
> Ersetzen Sie Platzhalterwerte (`<client_id>`, `<client_secret>`, `<tenant_id>`) durch tatsächliche Anmeldeinformationen aus dem Entwicklerportal Ihres Identitätsanbieters.

### Redirect URI

Die Redirect-URI muss in der Konfiguration Ihres Identitätsanbieters identisch sein:

```
http://localhost:5173/oidc/callback
```

Wenn digna unter einer anderen Domain gehostet wird, passen Sie sie entsprechend an:
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

Nachdem Sie die Konfiguration abgeschlossen haben, überprüfen Sie, ob SSO korrekt funktioniert.

### Pre-Testing-Checkliste

Stellen Sie vor dem Test sicher:

- [ ] `dashboard_config.toml` wurde mit OIDC-Anbietern aktualisiert
- [ ] `config.toml` wurde mit OIDC-Anmeldeinformationen aktualisiert
- [ ] Beide Dateien wurden gespeichert
- [ ] Anmeldeinformationen sind korrekt (Client-ID, Client-Secret)
- [ ] Redirect-URI stimmt mit Ihrer Deployment-URL überein
- [ ] Die Anwendung im Identitätsanbieter ist mit der Redirect-URI konfiguriert

### Testschritte

#### Schritt 1: Dienste neu starten

Starten Sie das digna-Backend und den Webserver neu, um Änderungen zu übernehmen.

**Falls als Windows-Dienst ausgeführt:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Falls manuell ausgeführt:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Bei Verwendung von IIS oder Tomcat:**
Starten Sie Ihren Webserver-Dienst neu.

#### Schritt 2: Dashboard öffnen

Öffnen Sie das digna-Dashboard in Ihrem Browser:

```
http://localhost:5173
```

(oder Ihre konfigurierte Dashboard-URL)

#### Schritt 3: Login-Schaltflächen prüfen

Überprüfen Sie, ob Login-Schaltflächen für jeden konfigurierten Anbieter angezeigt werden:

- ✅ Sie sollten die Schaltfläche "Mit Microsoft anmelden" sehen
- ✅ Sie sollten die Schaltfläche "Mit Google anmelden" sehen
- ✅ (Wenn usePassword = true) Sie sollten Benutzername-/Passwortfelder sehen

Wenn Schaltflächen nicht angezeigt werden:
- Prüfen Sie, ob `dashboard_config.toml` gespeichert wurde
- Prüfen Sie, ob der Dashboard-Dienst neu gestartet wurde
- Prüfen Sie die Browserkonsole (F12) auf Fehler

#### Schritt 4: SSO-Login testen

Klicken Sie auf eine der SSO-Schaltflächen (z. B. "Mit Microsoft anmelden"):

1. Sie sollten zur Login-Seite des Identitätsanbieters weitergeleitet werden
2. Melden Sie sich mit Ihren Unternehmensanmeldeinformationen an
3. Sie sollten zurück zu digna weitergeleitet werden
4. Sie sollten in digna eingeloggt sein

#### Schritt 5: Benutzererstellung prüfen

Nach erfolgreichem SSO-Login:

- ✅ Der Benutzer sollte automatisch in digna angelegt werden
- ✅ Der Benutzer sollte eingeloggt sein
- ✅ Das Benutzerprofil sollte Ihre Identitätsanbieterangaben anzeigen
- ✅ Sie sollten das digna-Dashboard sehen

#### Schritt 6: Passwort-Login testen (falls aktiviert)

Wenn `usePassword = true`:

1. Melden Sie sich bei digna ab
2. Geben Sie auf der Login-Seite Benutzernamen und Passwort ein
3. Sie sollten sich mit Passwort-Anmeldedaten einloggen können

---

## Fehlerbehebung {: #troubleshooting }

### Login-Schaltflächen werden nicht angezeigt

**Symptome:**
- OIDC-Login-Schaltflächen sind auf der Login-Seite nicht sichtbar
- Sie sehen nur Passwortfelder (wenn usePassword = true)

**Ursachen & Lösungen:**
1. Prüfen Sie, ob `dashboard_config.toml` im Verzeichnis `dashboard/` liegt
2. Vergewissern Sie sich, dass `[[login.oidc]]`-Abschnitte mit korrekter Syntax vorhanden sind
3. Starten Sie den Dashboard-Dienst neu
4. Leeren Sie den Browser-Cache (Strg+Umschalt+Entf oder Cmd+Umschalt+Entf)
5. Prüfen Sie die Browserkonsole (F12 → Console) auf Fehler

---

### Redirect-URI Mismatch-Fehler

**Symptome:**
- Nach dem Klick auf die SSO-Schaltfläche Fehler bezüglich "redirect_uri mismatch"
- "The redirect URI is not registered"-Fehler

**Ursachen & Lösungen:**
1. Überprüfen Sie `DIGNA_OIDC_REDIRECT_URI` in `config.toml`
2. Stellen Sie sicher, dass die Redirect-URI in den Einstellungen des Identitätsanbieters registriert ist
3. Achten Sie darauf, dass beide URLs identisch sind (inkl. Protokoll, Domain, Pfad)
4. Prüfen Sie auf Tippfehler in der Redirect-URI
5. Wenn HTTPS verwendet wird, stellen Sie sicher, dass das Zertifikat gültig ist

---

### Ungültige Client-Anmeldeinformationen

**Symptome:**
- "Invalid client ID or secret"-Fehler
- Authentifizierung schlägt mit Anmeldeinformationsfehler fehl

**Ursachen & Lösungen:**
1. Überprüfen Sie `DIGNA_OIDC_CLIENT_ID` und `DIGNA_OIDC_CLIENT_SECRET`
2. Achten Sie auf keine zusätzlichen Leerzeichen oder unerwünschte Zeichen
3. Prüfen Sie, ob die Anmeldeinformationen abgelaufen oder widerrufen wurden
4. Starten Sie das Backend neu, nachdem Sie die Konfiguration aktualisiert haben
5. Prüfen Sie im Identitätsanbieter-Portal, ob die Anmeldeinformationen aktiv sind

---

### Login hängt oder läuft in Timeout

**Symptome:**
- Klick auf SSO-Schaltfläche bewirkt nichts
- Timeout nach einigen Sekunden
- Browser zeigt "Failed to connect" oder ähnliches

**Ursachen & Lösungen:**
1. Vergewissern Sie sich, dass das digna-Backend läuft: `digna repo check`
2. Prüfen Sie die Netzwerkverbindung zum Identitätsanbieter
3. Überprüfen Sie, ob `DIGNA_OIDC_CONFIGURATION_URL` erreichbar ist
4. Prüfen Sie Firewall-Regeln, die ausgehende HTTPS-Verbindungen blockieren könnten
5. Stellen Sie sicher, dass Backend und Dashboard sich gegenseitig erreichen können

---

### Benutzer werden nicht automatisch erstellt

**Symptome:**
- SSO-Login ist erfolgreich, aber Benutzer wird nicht in digna angelegt
- Nach SSO-Login tritt ein Berechtigungsfehler auf

**Ursachen & Lösungen:**
1. Überprüfen Sie die OIDC-Konfiguration
2. Prüfen Sie, ob Benutzerberechtigungen korrekt eingerichtet sind
3. Lesen Sie die digna-Logs auf Fehlermeldungen
4. Starten Sie das Backend neu
5. Kontaktieren Sie support@digna.ai, wenn das Problem bestehen bleibt

---

## Unterstützte Anbieter {: #supported-providers }

### Getestet & Unterstützt

Die folgenden OIDC-Anbieter wurden getestet und funktionieren:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Andere OIDC-Anbieter

Jeder Anbieter, der OpenID Connect unterstützt, kann integriert werden. Erforderliche Informationen:

- Client-ID
- Client-Secret
- OpenID-Konfigurations-URL (in der Regel unter `/.well-known/openid-configuration`)
- Unterstützte Scopes (typischerweise `openid profile email`)

Kontaktieren Sie support@digna.ai, wenn Sie Hilfe bei der Integration eines bestimmten Anbieters benötigen.

---

## Beste Vorgehensweisen

✅ EMPFEHLUNGEN:
- Verwenden Sie in Produktion HTTPS (nicht HTTP)
- Speichern Sie Client-Secrets sicher (verwenden Sie wenn möglich Umgebungsvariablen)
- Rotieren Sie Secrets regelmäßig
- Testen Sie zuerst in einer Nicht-Produktionsumgebung
- Dokumentieren Sie, welche Anbieter konfiguriert sind
- Überwachen Sie Login-Logs auf ungewöhnliche Aktivitäten
- Halten Sie die Konfiguration des Identitätsanbieters synchron mit der digna-Konfiguration

❌ NICHT:
- Speichern Sie Client-Secrets im Versionskontrollsystem
- Verwenden Sie HTTP-Redirect-URIs in der Produktion
- Konfigurieren Sie mehrere Anbieter mit demselben Schlüssel
- Lassen Sie Standard-/Testanmeldeinformationen in der Produktion
- Legen Sie Konfigurationsdateien mit Secrets offen
- Mischen Sie Entwicklungs- und Produktionsanmeldeinformationen

---

## Support

Brauchen Sie Hilfe bei der SSO-Konfiguration?

- 📧 **E-Mail:** support@digna.ai
- 📚 **Dokumentation:** https://docs.digna.ai
- 🌐 **Website:** https://www.digna.ai

---

**Zuletzt aktualisiert:** August 30, 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
