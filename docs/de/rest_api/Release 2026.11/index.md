---
title: REST-API-Übersicht 2026.11 | digna Dokumentation
description: Mit der digna REST-API v1 lesen Sie Projekte und Inspektionsergebnisse, verwalten Datenquellen, Datensätze und Attribute und starten Inspektionen — Basis-URL, Authentifizierung mit API-Schlüssel, Paginierung, Fehler und das OpenAPI-Dokument.
image: /assets/logo_square.png
keywords: digna REST-API, digna API, digna OpenAPI, digna API-Schlüssel, API für Inspektionsanfragen, Datenqualitäts-API, Swagger UI
---

# digna REST-API 2026.11

Mit der *digna* REST-API arbeiten Ihre eigenen Tools und Pipelines über HTTP und JSON mit *digna*:
Sie lesen Projekte und Inspektionsergebnisse, verwalten Datenquellen, Datensätze und Attribute und
starten Inspektionen, zum Beispiel am Ende eines Datenladevorgangs. Das [Python SDK](../../sdk/Release%202026.11/index.md)
verwendet dieselbe API.

Diese Seite beschreibt, was alle Anfragen gemeinsam haben. Die Ressourcenseiten führen jeden Endpunkt
mit seinen Parametern, seinem Request-Body, seinen Antworten und Schemas auf:

| Ressource | Endpunkte |
|---|---|
| [Projects](projects.md) | Projekte lesen |
| [DB Connections](db_connections.md) | Datenbankverbindungen lesen |
| [Data Sources](data_sources.md) | Datenquellen erstellen, lesen, ändern und löschen |
| [Data Sets](data_sets.md) | Datensätze erstellen, lesen, ändern und löschen |
| [Attributes](attributes.md) | Attribute erstellen, lesen, ändern und löschen |
| [Check Definitions](check_definitions.md) | Check-Definitionen lesen |
| [Inspection Requests](inspection_requests.md) | Inspektionen starten und ihren Fortschritt verfolgen |
| [Inspection Statuses](inspection_statuses.md) | Inspektionsergebnisse pro Projekt, Datenquelle und Datensatz lesen |

---

## Basis-URL {: #base-url }

Die API ist Teil des *digna*-Backends. Jeder Pfad beginnt nach der Adresse des Backends mit `/v1`:

```text
https://digna.example.com/v1/projects
```

Die Adresse des Backends ist dieselbe, die das Dashboard verwendet: `baseUrl` im Abschnitt `[api]`
von `dashboard/dashboard_config.toml`. Verwenden Sie HTTPS, sobald der Aufrufer und *digna* nicht auf
demselben Rechner laufen, denn jede Anfrage enthält einen API-Schlüssel.

---

## Authentifizierung {: #authentication }

Jede Anfrage sendet den API-Schlüssel eines *digna*-Benutzers im Header `Authorization`:

```text
Authorization: Bearer <api key>
```

Um einen Schlüssel zu erstellen, öffnen Sie Ihr Benutzerprofil unten links im Dashboard, klicken auf
**API-Schlüssel** und dann auf **API-Schlüssel hinzufügen** und kopieren den Schlüssel. Er wird nur
einmal angezeigt. Dieselben Schlüssel funktionieren auch für den [digna MCP Server](../../ai_agents/overview.md).

Eine Anfrage läuft mit den Berechtigungen des Benutzers, dem der Schlüssel gehört. Zum Erstellen,
Ändern und Löschen ist die Editorrolle im Projekt nötig; andernfalls wird die Anfrage mit `403` und
der Meldung `You don't have permission to edit this project` abgelehnt.

!!! tip "Einen eigenen Benutzer für die Automatisierung verwenden"

    Legen Sie für jede Integration einen eigenen *digna*-Benutzer an, geben Sie ihm nur die Projekte
    und Rollen, die er braucht, und erstellen Sie seinen Schlüssel mit einem Ablaufdatum. Dann können
    Sie den Zugriff einer einzelnen Integration widerrufen, indem Sie ihren Schlüssel löschen, ohne
    andere zu beeinträchtigen.

---

## Eine Anfrage senden {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Antworten sind JSON. Listen werden als JSON-Array zurückgegeben. Auch Request-Bodys sind JSON und
werden mit `Content-Type: application/json` gesendet.

---

## Limits und Filter {: #limits-and-filters }

Listen-Endpunkte geben höchstens `limit` Einträge zurück: standardmäßig 200, maximal 5000. Ein Wert
außerhalb dieses Bereichs wird mit `400` abgelehnt. Es gibt weder Offset noch Seiten-Token. Grenzen
Sie eine Liste deshalb mit ihren Filtern ein, zum Beispiel `project_id`, `data_source_id` oder
`start_date` und `end_date` bei den Inspektionsstatus.

Eine Anfrage, die länger als 60 Sekunden dauert, wird mit `408 Request Timeout` abgebrochen.

---

## Fehler {: #errors }

Eine Fehlerantwort hat einen JSON-Body mit einem Code und einer Meldung:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Status | Code | Bedeutung |
|---|---|---|
| `400` | `BAD_REQUEST` | Die Anfrage ist ungültig, zum Beispiel ein `limit` außerhalb des Bereichs |
| `401` | `NOT_AUTHENTICATED` | Der API-Schlüssel fehlt, ist fehlerhaft formatiert, unbekannt oder abgelaufen |
| `403` | `NOT_AUTHORIZED` | Dem Benutzer des Schlüssels fehlt die Rolle, die diese Anfrage erfordert |
| `403` | `INVALID_LICENSE` | Die *digna*-Lizenz ist abgelaufen |
| `404` | `NOT_FOUND` | Das Projekt, die Datenquelle oder ein anderes Element existiert nicht |
| `500` | `INTERNAL_ERROR` | Ein unerwarteter Fehler in *digna*. Details stehen im Backend-Log |

Die `message` einer `401`-Antwort sagt, was mit dem Schlüssel nicht stimmt:

| Meldung | Ursache |
|---|---|
| `Missing Authorization header` | Es wurde kein `Authorization`-Header gesendet |
| `Invalid Authorization header format` | Der Wert beginnt nicht mit `Bearer ` |
| `Invalid API key` | Der Schlüssel ist falsch oder wurde gelöscht |
| `API key expired` | Der Schlüssel ist abgelaufen. Erstellen Sie einen neuen |

---

## Eine Inspektion ausführen {: #running-an-inspection }

Eine typische Integration startet eine Inspektion, wenn ein Datenladevorgang abgeschlossen ist, wartet
auf ihr Ende und liest das Ergebnis:

1. **Starten Sie die Inspektion** mit [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   Die Antwort enthält die `id` der Anfrage.
2. **Verfolgen Sie ihren Fortschritt** mit [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   Ihr `status` wechselt von `PENDING` über `RUNNING` zu `COMPLETED` oder endet als `FAILED`,
   `ABORTED` oder `CANCELLED`. Fragen Sie alle paar Sekunden erneut ab, bis er sich nicht mehr ändert.
3. **Lesen Sie das Ergebnis** mit [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   für die inspizierten Tage. Jeder Eintrag hat einen Gesamt-`status`: `0` (OK), `1` (Warnung),
   `2` (kritisch) oder `-1` (kein Status), und einen Status pro Modul mit der Anzahl der bestandenen,
   unsicheren und fehlgeschlagenen Checks.

```bash
curl -X POST https://digna.example.com/v1/inspection-requests \
  -H "Authorization: Bearer $DIGNA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "project_id": 1,
    "include_all_data_sources": true,
    "data_source_ids": [],
    "start_date": "2026-11-06",
    "end_date": "2026-11-06",
    "mode": "DAILY",
    "weekly_mode_weekdays": [],
    "monthly_mode_days": [],
    "use_notification": true
  }'
```

---

## OpenAPI-Dokument {: #openapi-document }

Jede *digna*-Installation beschreibt diese API in einem OpenAPI-3.1-Dokument und bietet eine
interaktive Swagger UI, in der Sie Anfragen dagegen ausprobieren können:

| Was | Adresse |
|---|---|
| OpenAPI-Dokument | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Das Dokument von Release 2026.11 finden Sie auch hier: [openapi.json](openapi.json). Damit können Sie
einen Client in einer anderen Sprache generieren.

!!! note "Nur die /v1-Endpunkte sind abgedeckt"

    Das Dashboard kommuniziert mit dem Backend auch über andere, interne Endpunkte. Sie gehören nicht
    zu dieser API und können sich mit jedem Release ändern. Bauen Sie Integrationen daher nur auf den
    `/v1`-Endpunkten auf.
