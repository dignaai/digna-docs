# SSO mit Keycloak einrichten

Keycloak ist ein selbstgehosteter, vollständig OIDC-kompatibler Identitätsanbieter. Da Sie ihn selbst betreiben, wird die Discovery-URL aus Ihrem eigenen Hostnamen und Realm aufgebaut statt aus einer Vendor-Domain.

Diese Anleitung behandelt die **Keycloak-Seite**: das Erstellen des Clients und das Sammeln der Werte, die digna benötigt. Die digna-Seite — `dashboard_config.toml`, Testen und Fehlerbehebung — ist für alle Provider gleich und ist in der [Single Sign-On Übersicht](overview.md) beschrieben.

---

## Bevor Sie beginnen

| Anforderung | Hinweise |
|---|---|
| **Keycloak version** | 17 oder höher für die hier verwendeten URL-Pfade — siehe die Anmerkung in Schritt 4 |
| **Keycloak role** | `realm-admin` im Zielrealm oder ein Serveradministrator |
| **Realm** | Das Realm, dem Ihre digna-Benutzer angehören, nicht unbedingt `master` |
| **digna redirect URI** | Die URL, zu der Benutzer nach dem Login zurückkehren, z. B. `https://digna.yourdomain.com/oidc/callback` |

---

## Schritt 1: Wählen Sie das Realm

1. Öffnen Sie die Keycloak-Administrationskonsole
2. Verwenden Sie den Realm-Selektor oben links, um zum Realm zu wechseln, in dem sich Ihre Benutzer befinden

!!! warning "Das master-Realm nicht verwenden"

    Das `master`-Realm ist für die Verwaltung von Keycloak selbst gedacht. Anwendungs-Clients gehören in ein eigenes Realm; digna im `master`-Realm zu platzieren, gewährt dessen Benutzern Zugriff auf die Keycloak-Administrationskonsole.

---

## Schritt 2: Erstellen des Clients

1. Gehen Sie zu **Clients** und klicken Sie auf **Create client**
2. Konfigurieren Sie:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — dies wird zu `DIGNA_OIDC_CLIENT_ID`
3. Klicken Sie auf **Next**
4. Auf dem Schritt **Capability config** schalten Sie **Client authentication** **On**
5. Lassen Sie **Standard flow** aktiviert; die anderen Flows werden nicht benötigt
6. Klicken Sie auf **Next**

!!! warning "Client-Authentifizierung muss aktiviert sein"

    Wenn **Client authentication** deaktiviert ist, erstellt Keycloak einen *public* Client, der gar keine Zugangsdaten hat — die **Credentials**-Registerkarte in Schritt 4 wird dann nicht vorhanden sein. digna benötigt einen confidential Client. Diese Einstellung kann nach der Erstellung korrigiert werden, falls Sie einen Fehler machen.

---

## Schritt 3: Setzen der Redirect-URI

Auf dem Schritt **Login settings** (oder später auf dem Tab **Settings**):

1. **Valid redirect URIs**: geben Sie Ihre digna-Callback-URL ein:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: leer lassen, oder auf `+` setzen, um die Redirect-URIs zu spiegeln
3. Klicken Sie auf **Save**

!!! tip "Wildcards vermeiden"

    Keycloak akzeptiert Muster wie `https://digna.yourdomain.com/*`. Ein Wildcard erlaubt jedem Pfad auf diesem Host, einen Authorization-Code zu empfangen. Verwenden Sie daher möglichst die exakte Callback-URL.

---

## Schritt 4: Das Client-Geheimnis ermitteln

1. Öffnen Sie den **Credentials**-Tab
2. Bestätigen Sie, dass **Client Authenticator** *Client Id and Secret* ist
3. Kopieren Sie das **Client secret** → wird zu `DIGNA_OIDC_CLIENT_SECRET`

Das Secret bleibt hier abrufbar und kann mit **Regenerate** neu erstellt werden.

---

## Schritt 5: Aufbau der Discovery-URL

Setzen Sie Ihren Keycloak-Host und den Realm-Namen ein:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Zum Beispiel:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 und früher enthalten /auth"

    Vor Keycloak 17 lagen alle Endpunkte unter einem `/auth`-Präfix:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Distributionen, die `KC_HTTP_RELATIVE_PATH=/auth` setzen, behalten das alte Layout auch in aktuellen Versionen. Wenn die URL ohne `/auth` einen 404 zurückgibt, versuchen Sie es mit `/auth`.

Öffnen Sie die URL in einem Browser, bevor Sie fortfahren. Ein JSON-Dokument bestätigt, dass Host und Realm korrekt sind.

---

## Schritt 6: digna konfigurieren

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Mit Keycloak anmelden"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

Der `key` in beiden Dateien muss übereinstimmen — hier `keycloak`. Beachten Sie, dass er nicht mit der Keycloak-**Client ID** identisch sein muss, auch wenn es zur Nachvollziehbarkeit einfacher ist, sie gleich zu halten.

---

## Schritt 7: Testen

Starten Sie das Backend und den Webserver neu und öffnen Sie dann das Dashboard. Siehe [Testing Login](overview.md#testing-login) für die vollständige Checkliste.

---

## Fehlerbehebung: Keycloak

### Invalid parameter: redirect_uri

Die Callback-URL ist nicht in **Valid redirect URIs** enthalten. Keycloak protokolliert die erhaltene URI im Serverlog — das ist der schnellste Weg, die exakte Abweichung zu erkennen.

### Der Credentials-Tab fehlt

Der Client ist public. Aktivieren Sie **Client authentication** unter **Settings → Capability config**.

### 404 bei der Discovery-URL

Entweder ist der Realm-Name falsch, oder die Installation verwendet das `/auth`-Präfix. Prüfen Sie die Realm-Liste in der Admin-Konsole und versuchen Sie beide URL-Formen.

### unauthorized_client oder invalid_client

**Standard flow** ist unter **Capability config** deaktiviert, oder das Secret wurde in Keycloak neu generiert, ohne `config.toml` zu aktualisieren.

### Zertifikatsfehler vom Backend

Ein selbstgehosteter Keycloak mit privatem oder selbstsigniertem Zertifikat schlägt bei dignas ausgehendem HTTPS-Aufruf zur Discovery-URL fehl. Installieren Sie die ausstellende CA in den Truststore der Maschine, auf der das digna-Backend läuft.

---

## Siehe auch

- [Single Sign-On Übersicht](overview.md) — Konfigurationsreferenz, Testen und allgemeine Fehlerbehebung
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)