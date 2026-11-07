---
title: Prezentare generală REST API 2026.11 | Documentație digna
description: Folosiți API-ul REST digna v1 pentru a citi proiecte și rezultate ale inspecțiilor, a gestiona surse de date, seturi de date și atribute și a porni inspecții — URL de bază, autentificare cu cheie API, paginare, erori și documentul OpenAPI.
image: /assets/logo_square.png
keywords: digna REST API, digna API, digna OpenAPI, cheie API digna, API pentru cereri de inspecție, API pentru calitatea datelor, Swagger UI
---

# digna REST API 2026.11

API-ul REST *digna* permite instrumentelor și pipeline-urilor dvs. să lucreze cu *digna* prin HTTP
și JSON: să citească proiecte și rezultate ale inspecțiilor, să gestioneze surse de date, seturi de
date și atribute și să pornească inspecții, de exemplu la finalul unei încărcări de date.
[Python SDK](../../sdk/Release%202026.11/index.md) folosește același API.

Această pagină descrie ce au în comun toate cererile. Paginile de resurse prezintă fiecare punct
final cu parametrii, corpul cererii, răspunsurile și schemele sale:

| Resursă | Puncte finale |
|---|---|
| [Projects](projects.md) | Citirea proiectelor |
| [DB Connections](db_connections.md) | Citirea conexiunilor la baze de date |
| [Data Sources](data_sources.md) | Crearea, citirea, actualizarea și ștergerea surselor de date |
| [Data Sets](data_sets.md) | Crearea, citirea, actualizarea și ștergerea seturilor de date |
| [Attributes](attributes.md) | Crearea, citirea, actualizarea și ștergerea atributelor |
| [Check Definitions](check_definitions.md) | Citirea definițiilor de verificare |
| [Inspection Requests](inspection_requests.md) | Pornirea inspecțiilor și urmărirea progresului lor |
| [Inspection Statuses](inspection_statuses.md) | Citirea rezultatelor inspecțiilor pe proiect, sursă de date și set de date |

---

## URL de bază {: #base-url }

API-ul face parte din backend-ul *digna*. Fiecare cale începe cu `/v1`, după adresa backend-ului:

```text
https://digna.example.com/v1/projects
```

Adresa backend-ului este cea pe care o folosește dashboard-ul: `baseUrl` din secțiunea `[api]` a
fișierului `dashboard/dashboard_config.toml`. Folosiți HTTPS ori de câte ori apelantul și *digna*
nu se află pe aceeași mașină, deoarece fiecare cerere conține o cheie API.

---

## Autentificare {: #authentication }

Fiecare cerere trimite cheia API a unui utilizator *digna* în antetul `Authorization`:

```text
Authorization: Bearer <api key>
```

Pentru a crea o cheie, deschideți profilul de utilizator din colțul din stânga jos al
dashboard-ului, faceți clic pe **API Keys**, apoi pe **Add API Key** și copiați cheia. Aceasta este
afișată o singură dată. Aceleași chei funcționează și pentru
[digna MCP Server](../../ai_agents/overview.md).

O cerere rulează cu permisiunile utilizatorului căruia îi aparține cheia. Crearea, modificarea și
ștergerea necesită rolul de editor în proiect; în caz contrar, cererea este refuzată cu `403` și
mesajul `You don't have permission to edit this project`.

!!! tip "Folosiți un utilizator dedicat pentru automatizare"

    Creați câte un utilizator *digna* pentru fiecare integrare, acordați-i doar proiectele și
    rolurile de care are nevoie și creați-i cheia cu o dată de expirare. Astfel puteți revoca
    accesul unei integrări ștergându-i cheia, fără a afecta pe nimeni altcineva.

---

## Trimiterea unei cereri {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Răspunsurile sunt în format JSON. Listele sunt returnate ca tablou JSON. Corpurile cererilor sunt
tot în format JSON și se trimit cu `Content-Type: application/json`.

---

## Limite și filtre {: #limits-and-filters }

Punctele finale de listare returnează cel mult `limit` elemente: implicit 200 și până la 5000. O
valoare în afara acestui interval este respinsă cu `400`. Nu există offset sau token de pagină, așa
că restrângeți o listă cu ajutorul filtrelor sale, de exemplu `project_id`, `data_source_id` sau
`start_date` și `end_date` la stările inspecțiilor.

O cerere care durează mai mult de 60 de secunde este anulată cu `408 Request Timeout`.

---

## Erori {: #errors }

Un răspuns de eroare are un corp JSON cu un cod și un mesaj:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Stare | Cod | Semnificație |
|---|---|---|
| `400` | `BAD_REQUEST` | Cererea este invalidă, de exemplu o valoare `limit` în afara intervalului |
| `401` | `NOT_AUTHENTICATED` | Cheia API lipsește, are un format greșit, este necunoscută sau a expirat |
| `403` | `NOT_AUTHORIZED` | Utilizatorul cheii nu are rolul necesar pentru această cerere |
| `403` | `INVALID_LICENSE` | Licența *digna* a expirat |
| `404` | `NOT_FOUND` | Proiectul, sursa de date sau alt element nu există |
| `500` | `INTERNAL_ERROR` | O eroare neașteptată în *digna*. Detaliile se află în jurnalul backend-ului |

Câmpul `message` al unui răspuns `401` arată ce este în neregulă cu cheia:

| Mesaj | Cauză |
|---|---|
| `Missing Authorization header` | Nu a fost trimis niciun antet `Authorization` |
| `Invalid Authorization header format` | Valoarea nu începe cu `Bearer ` |
| `Invalid API key` | Cheia este greșită sau a fost ștearsă |
| `API key expired` | Cheia a expirat. Creați una nouă |

---

## Rularea unei inspecții {: #running-an-inspection }

O integrare tipică pornește o inspecție după ce s-a încheiat o încărcare de date, așteaptă
finalizarea ei și citește rezultatul:

1. **Porniți inspecția** cu [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   Răspunsul conține `id`-ul cererii.
2. **Urmăriți progresul** cu [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   Câmpul `status` trece de la `PENDING` prin `RUNNING` la `COMPLETED` sau se încheie ca `FAILED`,
   `ABORTED` ori `CANCELLED`. Interogați din nou la câteva secunde, până când nu se mai schimbă.
3. **Citiți rezultatul** cu [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   pentru zilele inspectate. Fiecare element are un `status` general: `0` (OK), `1` (avertisment),
   `2` (critic) sau `-1` (fără stare), precum și o stare pentru fiecare modul, cu numărul de
   verificări reușite, incerte și eșuate.

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

## Documentul OpenAPI {: #openapi-document }

Fiecare instalare *digna* descrie acest API într-un document OpenAPI 3.1 și oferă o interfață
interactivă Swagger UI în care puteți încerca cereri:

| Ce | Adresă |
|---|---|
| Document OpenAPI | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Documentul pentru Release 2026.11 este disponibil și aici: [openapi.json](openapi.json). Folosiți-l
pentru a genera un client în alt limbaj de programare.

!!! note "Sunt acoperite doar punctele finale /v1"

    Dashboard-ul comunică cu backend-ul și prin alte puncte finale, interne. Acestea nu fac parte
    din acest API și se pot schimba cu orice versiune, așa că construiți integrările doar pe
    punctele finale `/v1`.
