# SSO mit Google Workspace einrichten

Die Identity-Plattform von Google ist OIDC-konform und verwendet für alle Kunden eine einzige, wohlbekannte Discovery-URL. Die einzigen organisationsspezifischen Werte sind also die Client-ID und das Geheimnis.

Diese Anleitung behandelt die **Google-Seite**: Erstellen des OAuth-Clients und Sammeln der Werte, die digna benötigt. Die digna-Seite — `dashboard_config.toml`, Testen und Fehlerbehebung — ist für alle Provider identisch und in der [Single Sign-On Übersicht](overview.md) beschrieben.

---

## Bevor Sie beginnen

| Anforderung | Hinweise |
|---|---|
| **Google Cloud project** | Beliebiges Projekt in derselben Organisation wie Ihre Workspace-Domain |
| **Role** | Editor oder Owner im Projekt |
| **digna redirect URI** | Die URL, zu der Nutzer nach dem Login zurückkehren, z. B. `https://digna.yourdomain.com/oidc/callback` |

---

## Schritt 1: Den OAuth-Zustimmungsbildschirm konfigurieren

Google stellt keine Zugangsdaten aus, solange der Zustimmungsbildschirm nicht existiert.

1. Öffnen Sie die [Google Cloud Console](https://console.cloud.google.com) und wählen Sie Ihr Projekt aus
2. Gehen Sie zu **APIs & Services → OAuth consent screen**
3. Wählen Sie den Nutzertyp:
   - **Internal** — nur Konten in Ihrer Workspace-Domain können sich anmelden. Empfohlen.
   - **External** — jedes Google-Konto kann versuchen, sich anzumelden.
4. Füllen Sie App-Name, Support-E-Mail für Nutzer und Entwicklerkontakt-E-Mail aus
5. Fügen Sie im Schritt **Scopes** `openid`, `.../auth/userinfo.email` und `.../auth/userinfo.profile` hinzu
6. Speichern

!!! warning "Externe Apps müssen veröffentlicht werden"

    Ein **External**-Zustimmungsbildschirm startet im Status *Testing*, wobei nur explizit zur Testnutzerliste hinzugefügte Konten eine Anmeldung abschließen können. Alle anderen sehen „digna has not completed the Google verification process“. Schalten Sie die App entweder unter **Publishing status** auf **In production**, oder verwenden Sie **Internal** — das hat diese Einschränkung nicht und ist die richtige Wahl für eine ausschließlich Workspace-basierte Bereitstellung.

---

## Schritt 2: Den OAuth-Client erstellen

1. Gehen Sie zu **APIs & Services → Credentials**
2. Klicken Sie auf **Create Credentials → OAuth client ID**
3. Setzen Sie **Application type** auf **Web application**
4. Geben Sie einen Namen an, z. B. `digna`
5. Unter **Authorized redirect URIs** klicken Sie auf **Add URI** und geben Sie ein:

```
https://digna.yourdomain.com/oidc/callback
```

6. Klicken Sie auf **Create**

!!! note "Authorized JavaScript Origins sind nicht erforderlich"

    digna tauscht den Autorisierungscode über das Backend aus, nicht über den Browser, daher kann das Feld **Authorized JavaScript origins** leer bleiben. Nur die Redirect-URI ist relevant.

---

## Schritt 3: Die Zugangsdaten erfassen

Der Dialog, der nach der Erstellung erscheint, zeigt:

- **Client ID** — endet auf `.apps.googleusercontent.com` → wird zu `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → wird zu `DIGNA_OIDC_CLIENT_SECRET`

Beide Werte können später noch von der Detailseite der Anmeldeinformationen abgerufen werden, im Gegensatz zu den meisten anderen Providern.

---

## Schritt 4: Die Discovery-URL

Google verwendet eine Discovery-URL für alle Kunden — hier ist nichts zu ersetzen:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Schritt 5: digna konfigurieren

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

Der `key` in beiden Dateien muss übereinstimmen — hier `google`.

---

## Schritt 6: Testen

Starten Sie Backend und Webserver neu und öffnen Sie dann das Dashboard. Siehe [Login testen](overview.md#testing-login) für die vollständige Checkliste.

---

## Fehlerbehebung für Google Workspace

### Fehler 400: redirect_uri_mismatch

Die URI in `DIGNA_OIDC_REDIRECT_URI` steht nicht in der Liste der **Authorized redirect URIs**, oder unterscheidet sich durch einen abschließenden Schrägstrich oder das Schema. Die Fehlerseite von Google zeigt die empfangene URI an — vergleichen Sie diese Zeichen für Zeichen mit der registrierten URI.

### Diese App ist blockiert / Hat die Verifizierung nicht abgeschlossen

Der Zustimmungsbildschirm ist **External** und befindet sich noch im Status *Testing*. Veröffentlichen Sie ihn oder wechseln Sie die App auf **Internal**.

### Zugriff blockiert: Autorisierungsfehler

Das Konto, das sich anzumelden versucht, gehört nicht zu Ihrer Workspace-Domain, während der Zustimmungsbildschirm auf **Internal** gesetzt ist. Das ist das beabsichtigte Verhalten — Internal-Apps akzeptieren nur Konten aus der Organisation.

### Änderungen benötigen mehrere Minuten

Google propagiert Änderungen an Zugangsdaten und dem Zustimmungsbildschirm asynchron. Eine neu hinzugefügte Redirect-URI kann ein paar Minuten brauchen, bis sie wirksam wird; wenn eine Änderung ignoriert zu werden scheint, warten Sie kurz und versuchen Sie es erneut, bevor Sie weiter untersuchen.

---

## Siehe auch

- [Single Sign-On Übersicht](overview.md) — Konfigurationsreferenz, Testen und allgemeine Fehlerbehebung
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)