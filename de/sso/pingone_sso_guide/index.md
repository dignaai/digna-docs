# SSO mit PingOne einrichten

PingOne ist OIDC-kompatibel. Zwei Werte benötigen besondere Aufmerksamkeit: die **Umgebungs‑ID**, die in jeder Endpunkt-URL vorkommt, und die **regionale Domain**, die sich zwischen nordamerikanischen, europäischen, kanadischen, asiatisch-pazifischen und australischen Mandanten unterscheidet.

Diese Anleitung behandelt die **PingOne-Seite**: das Erstellen der Anwendung und das Sammeln der Werte, die digna benötigt. Die digna-Seite — `dashboard_config.toml`, Tests und Troubleshooting — ist bei allen Anbietern gleich und in der [Single Sign-On Übersicht](overview.md) beschrieben.

---

## Bevor Sie beginnen

| Anforderung | Hinweise |
|---|---|
| **PingOne-Rolle** | Environment Admin oder Identity Data Admin in der Ziel-Umgebung |
| **Umgebung** | Die PingOne-Umgebung, zu der Ihre digna-Benutzer gehören |
| **digna Redirect URI** | Die URL, zu der Benutzer nach dem Login zurückkehren, z. B. `https://digna.yourdomain.com/oidc/callback` |

---

## Schritt 1: Anwendung erstellen

1. Melden Sie sich in der PingOne-Admin-Konsole an und wählen Sie Ihre Umgebung aus  
2. Gehen Sie zu **Applications → Applications**  
3. Klicken Sie auf die **+**-Schaltfläche  
4. Geben Sie `digna` als **Application Name** ein  
5. Wählen Sie **OIDC Web App**  
6. Klicken Sie auf **Save**

!!! warning "OIDC Web App wählen, nicht Single-Page App"

    *Single-Page App* und *Native App* erzeugen öffentliche Clients, die kein Secret halten können. digna tauscht den Autorisierungscode vom Backend aus und benötigt deshalb den vertraulichen **OIDC Web App**-Typ.

---

## Schritt 2: Redirect URI konfigurieren

1. Öffnen Sie den **Configuration**-Tab der Anwendung  
2. Klicken Sie auf das Stiftsymbol, um zu bearbeiten  
3. Stellen Sie sicher, dass **Response Type** auf *Code* und **Grant Type** auf *Authorization Code* gesetzt ist  
4. Unter **Redirect URIs** geben Sie Ihre digna-Callback-URL ein:

```
https://digna.yourdomain.com/oidc/callback
```

5. Setzen Sie **Token Endpoint Authentication Method** auf *Client Secret Post* oder *Client Secret Basic*  
6. Klicken Sie auf **Save**

---

## Schritt 3: Anwendung aktivieren

Schalten Sie auf der Zeile oder Detailansicht der Anwendung den Schalter auf **enabled**.

!!! warning "Neue Anwendungen sind standardmäßig deaktiviert"

    PingOne legt neue Anwendungen im deaktivierten Zustand an. Eine deaktivierte Anwendung führt beim Autorisierungsschritt zu einem Fehler, der den Schalter nicht erwähnt — prüfen Sie das deshalb, bevor Sie andere Fehlerquellen untersuchen.

---

## Schritt 4: Scopes gewähren

1. Öffnen Sie den **Resources**-Tab  
2. Stellen Sie sicher, dass `openid` gewährt ist, und fügen Sie `profile` und `email` aus der **OpenID Connect**-Ressource hinzu  
3. Klicken Sie auf **Save**

---

## Schritt 5: Benutzer zuweisen

1. Öffnen Sie den **Access**-Tab  
2. Fügen Sie die Population oder Gruppen hinzu, deren Mitglieder digna nutzen dürfen  
3. Klicken Sie auf **Save**

---

## Schritt 6: Credentials und Umgebungs‑ID erfassen

Im **Configuration**-Tab erweitern Sie **General**:

- **Client ID** → wird zu `DIGNA_OIDC_CLIENT_ID`  
- **Client Secret** → wird zu `DIGNA_OIDC_CLIENT_SECRET` (Klicken Sie auf das Augensymbol)  
- **Environment ID** → gehört in die Discovery-URL

Auf demselben Tab wird auch der fertige **OIDC Discovery Endpoint** angezeigt, den Sie direkt kopieren können, statt ihn manuell zusammenzusetzen.

---

## Schritt 7: Discovery-URL erstellen

Setzen Sie die Umgebungs‑ID und die Domain für Ihre Region ein:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Region | Domain |
|---|---|
| Nordamerika | `auth.pingone.com` |
| Europa | `auth.pingone.eu` |
| Kanada | `auth.pingone.ca` |
| Asien-Pazifik | `auth.pingone.asia` |
| Australien | `auth.pingone.com.au` |

Für eine europäische Umgebung:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Kopieren statt eintippen"

    Die regionale Domain ist der häufigste Fehler bei einer PingOne-Integration; eine falsche Region führt zu einem 404 statt zu einer hilfreichen Fehlermeldung. Verwenden Sie den **OIDC Discovery Endpoint**-Wert aus Schritt 6.

---

## Schritt 8: digna konfigurieren

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Login with PingOne"
```

### `config.toml`

```toml
[oidc.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

Der `key` muss in beiden Dateien übereinstimmen — hier `pingone`.

---

## Schritt 9: Testen

Starten Sie das Backend und den Webserver neu und öffnen Sie dann das Dashboard. Die vollständige Checkliste finden Sie unter [Login testen](overview.md#testing-login).

---

## PingOne-Fehlerbehebung

### 404 auf der Discovery-URL

Die regionale Domain oder die Umgebungs‑ID ist falsch. Vergleichen Sie mit dem **OIDC Discovery Endpoint**, der im Configuration-Tab der Anwendung angezeigt wird.

### NOT_FOUND oder Anwendung deaktiviert

Der Anwendungsschalter aus Schritt 3 steht noch auf aus.

### Redirect URI stimmt nicht überein

PingOne vergleicht die gesamte Zeichenkette. Prüfen Sie **Configuration → Redirect URIs** auf einen abschließenden Slash oder Unterschiede im Schema (http vs. https).

### Login gelingt, aber kein Email-Claim erreicht digna

Die Scopes `email` und `profile` wurden nicht im **Resources**-Tab gewährt.

### Der Benutzer sieht die Anwendung nicht

Es wurde keine Population oder Gruppe im **Access**-Tab zur Anwendung hinzugefügt.

---

## Siehe auch

- [Single Sign-On Übersicht](overview.md) — Konfigurationsreferenz, Tests und allgemeine Fehlerbehebung  
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)