# SSO mit AD FS einrichten

Active Directory Federation Services ist die On-Premises-Option: Ihre eigenen Server stellen die Tokens aus, und die Discovery-URL ist Ihr eigener Hostname. AD FS unterstützt OpenID Connect ab **Windows Server 2016**.

Diese Anleitung deckt die **AD FS-Seite** ab: Erstellen der Anwendungsgruppe und Sammeln der Werte, die digna benötigt. Die digna-Seite — `dashboard_config.toml`, Testen und Fehlerbehebung — ist für alle Provider gleich und wird in der [Single Sign-On Übersicht](overview.md) beschrieben.

---

## Bevor Sie beginnen

| Anforderung | Hinweise |
|---|---|
| **AD FS-Version** | Windows Server 2016 oder neuer — ältere Versionen unterstützen OIDC nicht |
| **Zugriff** | Lokaler Administrator auf dem AD FS-Server |
| **Federation service name** | z. B. `adfs.yourdomain.com` |
| **digna redirect URI** | Die URL, zu der Benutzer nach dem Login zurückkehren, z. B. `https://digna.yourdomain.com/oidc/callback` |

---

## Schritt 1: Anwendungsgruppe erstellen

1. Öffnen Sie auf dem AD FS-Server **AD FS Management**
2. Rechtsklicken Sie **Application Groups** und wählen Sie **Add Application Group**
3. Geben Sie `digna` als Namen ein
4. Unter **Standalone applications** — oder **Client-Server applications** je nach Version — wählen Sie **Server application accessing a web API**
5. Klicken Sie **Next**

---

## Schritt 2: Die Serveranwendung konfigurieren

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS generiert eine GUID. Kopieren Sie sie — das wird `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: Geben Sie Ihre digna-Callback-URL ein und klicken Sie **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Klicken Sie **Next**

!!! warning "Klicken Sie auf Hinzufügen, nicht nur auf Weiter"

    Das Redirect-URI-Feld hat einen eigenen **Add**-Button. Wenn Sie eine URI eingeben und auf **Next** klicken, ohne **Add** zu drücken, wird sie verworfen und der Assistent warnt nicht. Vergewissern Sie sich, dass die URI in der Liste unter dem Feld erscheint, bevor Sie fortfahren.

---

## Schritt 3: Das Shared Secret erzeugen

1. Aktivieren Sie **Generate a shared secret**
2. Kopieren Sie das erzeugte Secret → wird `DIGNA_OIDC_CLIENT_SECRET`
3. Klicken Sie **Next**

!!! warning "Das Secret wird nur einmal angezeigt"

    AD FS zeigt das Shared Secret nur auf dieser Assistentenseite an und kann es später nicht erneut anzeigen. Wenn Sie es verlieren, setzen Sie es später in den Eigenschaften der Anwendungsgruppe zurück.

---

## Schritt 4: Die Web-API konfigurieren

1. **Identifier**: Geben Sie denselben Client-Identifier aus Schritt 2 ein und klicken Sie **Add**
2. Klicken Sie **Next**
3. Wählen Sie eine **Access Control Policy** — *Permit everyone* ist der einfachste Startpunkt; beschränken Sie sie für den Produktivbetrieb auf eine Gruppe
4. Klicken Sie **Next**

---

## Schritt 5: Die erlaubten Scopes gewähren

Im Schritt **Configure Application Permissions** aktivieren Sie:

- `openid`
- `profile`
- `email`

Klicken Sie dann **Next** und schließen Sie den Assistenten ab.

!!! warning "`openid` ist nicht standardmäßig aktiviert"

    AD FS wählt in manchen Versionen nur `user_impersonation` vor. Ohne `openid` gibt der Token-Endpunkt ein OAuth-Access-Token statt eines ID-Tokens zurück, und digna kann den Benutzer nicht identifizieren.

---

## Schritt 6: Den Discovery-Endpunkt bestätigen

Ersetzen Sie Ihren Federation Service-Namen:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Beispiel:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Öffnen Sie diese URL im Browser. Ein JSON-Dokument bestätigt, dass OIDC aktiviert ist und der Hostname korrekt ist.

!!! note "Das Backend muss dem Zertifikat vertrauen"

    Eine interne Zertifizierungsstelle ist bei AD FS üblich. Die Maschine, die das digna-Backend ausführt, führt selbst einen ausgehenden HTTPS-Aufruf zu dieser URL aus, daher muss die ausstellende CA im Trust Store dieser Maschine sein — nicht nur in den Browsern der Benutzer.

---

## Schritt 7: digna konfigurieren

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Anmelden mit Active Directory"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<das in Schritt 3 kopierte Shared Secret>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

Der `key` in beiden Dateien muss übereinstimmen — hier `adfs`.

---

## Schritt 8: Testen

Starten Sie das Backend und den Webserver neu und öffnen Sie dann das Dashboard. Siehe [Login testen](overview.md#testing-login) für die vollständige Checkliste.

---

## Fehlerbehebung für AD FS

### MSIS9611: Der Client darf nicht auf die Ressource zugreifen

Der Web-API-Identifier aus Schritt 4 stimmt nicht mit dem Client-Identifier überein, oder die Scopes aus Schritt 5 wurden nicht gewährt. Beides lässt sich in den Eigenschaften der Anwendungsgruppe bearbeiten.

### MSIS9602: Ungültige redirect_uri

Die URI wurde eingegeben, aber nicht mit dem **Add**-Button hinzugefügt, oder sie weicht von `DIGNA_OIDC_REDIRECT_URI` ab. Prüfen Sie **Application Groups → digna → digna backend → Properties**.

### Es wird kein ID-Token zurückgegeben

Der `openid`-Scope fehlt in den Anwendungsberechtigungen.

### Das Backend kann die Discovery-URL nicht erreichen

Entweder löst DNS auf dem Backend-Host den Federation-Service-Namen nicht auf, oder das AD FS-Zertifikat wird dort nicht vertraut. Testen Sie mit `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` direkt vom digna-Server aus.

### Zu prüfende Ereignisse

Der AD FS-Server protokolliert Fehler im Event Viewer unter **Applications and Services Logs → AD FS → Admin**, in der Regel mit einer detaillierteren Ursache als die Browseranzeige.

---

## Siehe auch

- [Single Sign-On Übersicht](overview.md) — Konfigurationsreferenz, Tests und allgemeine Fehlerbehebung
- [Microsoft: AD FS OpenID Connect scenarios](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)