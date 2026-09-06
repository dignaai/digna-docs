# SSO mit Microsoft Entra ID einrichten

Microsoft Entra ID (ehemals Azure Active Directory) ist ein voll OIDC-kompatibler Provider, daher integriert sich digna über den standardmäßigen Discovery-Endpunkt.

Diese Anleitung behandelt die **Entra ID-Seite**: die Registrierung der Anwendung und das Sammeln der vier Werte, die digna benötigt. Die digna-Seite — `dashboard_config.toml`, Tests und Fehlerbehebung — ist für alle Provider gleich und wird im [Single Sign-On Overview](overview.md) beschrieben.

---

## Bevor Sie beginnen

| Anforderung | Hinweise |
|---|---|
| **Entra ID-Rolle** | Application Administrator, Cloud Application Administrator oder Global Administrator |
| **digna Redirect-URI** | Die URL, zu der Benutzer nach der Anmeldung zurückkehren, z. B. `https://digna.yourdomain.com/oidc/callback` |
| **Mandant** | Das Verzeichnis, bei dem sich Ihre Benutzer anmelden |

---

## Schritt 1: Anwendung registrieren

1. Melden Sie sich im [Microsoft Entra admin center](https://entra.microsoft.com) an
2. Gehen Sie zu **Identity → Applications → App registrations**
3. Klicken Sie auf **New registration**
4. Konfigurieren Sie:
   - **Name**: `digna` (wird Benutzern im Consent-Screen angezeigt)
   - **Supported account types**: *Accounts in this organizational directory only* für eine Single-Tenant-Bereitstellung
5. Unter **Redirect URI** wählen Sie die Plattform **Web** und geben Ihre digna-Callback-URL ein:

```
https://digna.yourdomain.com/oidc/callback
```

6. Klicken Sie auf **Register**

!!! warning "Wichtig"

    Die Plattform muss **Web** sein, nicht *Single-page application*. digna tauscht den Autorisierungscode vom Backend mithilfe eines Client-Secrets aus, was der SPA-Plattformtyp nicht erlaubt.

---

## Schritt 2: Client- und Tenant-IDs erfassen

Kopieren Sie auf der **Overview**-Seite der Anwendung:

- **Application (client) ID** → wird `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → gehört in die Discovery-URL

---

## Schritt 3: Ein Client-Secret erstellen

1. Gehen Sie zu **Certificates & secrets → Client secrets**
2. Klicken Sie auf **New client secret**
3. Geben Sie eine Beschreibung ein und wählen Sie eine Ablaufzeit
4. Klicken Sie auf **Add**
5. Kopieren Sie sofort die **Value**-Spalte

!!! warning "Kopieren Sie den Value, nicht die Secret ID"

    Der **Value** wird nur einmal auf dieser Seite angezeigt und kann später nicht mehr abgerufen werden. Die daneben stehende **Secret ID** sieht ähnlich aus, ist aber nicht das Secret — dessen Verwendung führt beim Login zu einem `invalid_client`-Fehler. Navigieren Sie nicht weg, bevor Sie den Wert kopiert haben; löschen Sie andernfalls das Secret und erstellen Sie ein neues.

!!! tip "Tipp"

    Entra ID begrenzt die Lebensdauer von Secrets auf maximal 24 Monate, sodass jede SSO-Integration ein Ablaufdatum hat. Notieren Sie es an einer Stelle, die Sie sehen — ein abgelaufenes Secret unterbricht SSO für alle Benutzer gleichzeitig, ohne Warnung auf der Login-Seite.

---

## Schritt 4: API-Berechtigungen bestätigen

1. Gehen Sie zu **API permissions**
2. Bestätigen Sie, dass **Microsoft Graph → User.Read** (delegiert) vorhanden ist — dies wird standardmäßig hinzugefügt

Die von digna angeforderten Scopes `openid`, `profile` und `email` sind Teil des standardmäßigen OIDC-Sets und benötigen keine gesonderte Zustimmung. Wenn Ihr Mandant Administratorzustimmung für alle Anwendungen verlangt, klicken Sie auf **Grant admin consent for <tenant>**.

---

## Schritt 5: Die Discovery-URL erstellen

Ersetzen Sie die **Directory (tenant) ID** aus Schritt 2:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Verwenden Sie den v2.0-Endpunkt"

    Der `/v2.0/`-Abschnitt ist wichtig. Der v1.0-Endpunkt unter `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` stellt Token in einem älteren Format aus und liefert nicht die standardmäßigen OIDC-Claims, die digna erwartet.

Öffnen Sie die URL vor dem Fortfahren im Browser. Ein JSON-Dokument bestätigt, dass die Tenant-ID korrekt ist.

---

## Schritt 6: digna konfigurieren

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"
```

### `config.toml`

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

Der `key` in beiden Dateien muss übereinstimmen — hier `microsoft`.

---

## Schritt 7: Testen

Starten Sie das Backend und den Webserver neu und öffnen Sie dann das Dashboard. Weitere Prüfpunkte finden Sie unter [Testing Login](overview.md#testing-login).

---

## Fehlerbehebung Entra ID

### AADSTS50011: Redirect URI Mismatch

Die URI in `DIGNA_OIDC_REDIRECT_URI` unterscheidet sich von der in Schritt 1 registrierten. Entra ID vergleicht die gesamte Zeichenkette, daher zählen ein abschließender Schrägstrich, `http` gegenüber `https` oder ein anderer Port als Unterschied. Überprüfen Sie **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Invalid Client Secret

Entweder wurde die **Secret ID** statt des **Value** kopiert, oder das Secret ist abgelaufen. Erstellen Sie ein neues Secret und kopieren Sie die Value-Spalte.

### AADSTS650057: Invalid Resource

Die Anwendungsregistrierung wurde gelöscht oder gehört zu einem anderen Mandanten als dem in der Discovery-URL. Bestätigen Sie die Directory (tenant) ID auf der Overview-Seite.

### Benutzer melden sich an, aber es passiert nichts

Wenn der Mandant Administratorzustimmung verlangt und diese nicht erteilt wurde, kehrt der Redirect ohne ein verwertbares Token zurück. Erteilen Sie die Administratorzustimmung unter **API permissions**.

---

## Siehe auch

- [Single Sign-On Overview](overview.md) — Konfigurationsreferenz, Tests und allgemeine Fehlerbehebung
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)