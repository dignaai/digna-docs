---
title: Επισκόπηση REST API 2026.11 | Τεκμηρίωση digna
description: Χρησιμοποιήστε το digna REST API v1 για να διαβάζετε projects και αποτελέσματα επιθεωρήσεων, να διαχειρίζεστε πηγές δεδομένων, σύνολα δεδομένων και χαρακτηριστικά και να ξεκινάτε επιθεωρήσεις — βασικό URL, αυθεντικοποίηση με κλειδί API, σελιδοποίηση, σφάλματα και το έγγραφο OpenAPI.
image: /assets/logo_square.png
keywords: digna REST API, digna API, digna OpenAPI, κλειδί API digna, API αιτημάτων επιθεώρησης, API ποιότητας δεδομένων, Swagger UI
---

# digna REST API 2026.11

Το REST API του *digna* επιτρέπει στα δικά σας εργαλεία και pipelines να συνεργάζονται με το
*digna* μέσω HTTP και JSON: να διαβάζουν projects και αποτελέσματα επιθεωρήσεων, να διαχειρίζονται
πηγές δεδομένων, σύνολα δεδομένων και χαρακτηριστικά και να ξεκινούν επιθεωρήσεις, για παράδειγμα
στο τέλος μιας φόρτωσης δεδομένων. Το [Python SDK](../../sdk/Release%202026.11/index.md)
χρησιμοποιεί το ίδιο API.

Αυτή η σελίδα καλύπτει ό,τι έχουν κοινό όλα τα αιτήματα. Οι σελίδες των πόρων παραθέτουν κάθε
endpoint με τις παραμέτρους, το σώμα αιτήματος, τις αποκρίσεις και τα σχήματά του:

| Πόρος | Endpoints |
|---|---|
| [Projects](projects.md) | Ανάγνωση projects |
| [DB Connections](db_connections.md) | Ανάγνωση συνδέσεων βάσεων δεδομένων |
| [Data Sources](data_sources.md) | Δημιουργία, ανάγνωση, ενημέρωση και διαγραφή πηγών δεδομένων |
| [Data Sets](data_sets.md) | Δημιουργία, ανάγνωση, ενημέρωση και διαγραφή συνόλων δεδομένων |
| [Attributes](attributes.md) | Δημιουργία, ανάγνωση, ενημέρωση και διαγραφή χαρακτηριστικών |
| [Check Definitions](check_definitions.md) | Ανάγνωση ορισμών ελέγχων |
| [Inspection Requests](inspection_requests.md) | Έναρξη επιθεωρήσεων και παρακολούθηση της προόδου τους |
| [Inspection Statuses](inspection_statuses.md) | Ανάγνωση αποτελεσμάτων επιθεωρήσεων ανά project, πηγή δεδομένων και σύνολο δεδομένων |

---

## Βασικό URL {: #base-url }

Το API είναι μέρος του backend του *digna*. Κάθε διαδρομή ξεκινά με `/v1`, μετά τη διεύθυνση του
backend:

```text
https://digna.example.com/v1/projects
```

Η διεύθυνση του backend είναι αυτή που χρησιμοποιεί το dashboard: το `baseUrl` στην ενότητα `[api]`
του `dashboard/dashboard_config.toml`. Χρησιμοποιείτε HTTPS όποτε ο καλών και το *digna* δεν
βρίσκονται στο ίδιο μηχάνημα, επειδή κάθε αίτημα μεταφέρει ένα κλειδί API.

---

## Αυθεντικοποίηση {: #authentication }

Κάθε αίτημα στέλνει το κλειδί API ενός χρήστη *digna* στην κεφαλίδα `Authorization`:

```text
Authorization: Bearer <api key>
```

Για να δημιουργήσετε ένα κλειδί, ανοίξτε το προφίλ χρήστη σας στην κάτω αριστερή γωνία του
dashboard, κάντε κλικ στο **API Keys** και μετά στο **Add API Key** και αντιγράψτε το κλειδί.
Εμφανίζεται μόνο μία φορά. Τα ίδια κλειδιά λειτουργούν και για τον
[digna MCP Server](../../ai_agents/overview.md).

Ένα αίτημα εκτελείται με τα δικαιώματα του χρήστη στον οποίο ανήκει το κλειδί. Η δημιουργία, η
αλλαγή και η διαγραφή απαιτούν τον ρόλο συντάκτη (editor) στο project· διαφορετικά, το αίτημα
απορρίπτεται με `403` και το μήνυμα `You don't have permission to edit this project`.

!!! tip "Χρησιμοποιήστε έναν αποκλειστικό χρήστη για αυτοματοποίηση"

    Δημιουργήστε έναν χρήστη *digna* για κάθε ενσωμάτωση, δώστε του μόνο τα projects και τους
    ρόλους που χρειάζεται και δημιουργήστε το κλειδί του με ημερομηνία λήξης. Έτσι μπορείτε να
    ανακαλέσετε την πρόσβαση μιας ενσωμάτωσης διαγράφοντας το κλειδί της, χωρίς να επηρεάσετε
    κανέναν άλλον.

---

## Αποστολή αιτήματος {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Οι αποκρίσεις είναι σε JSON. Οι λίστες επιστρέφονται ως πίνακας JSON. Τα σώματα αιτημάτων είναι
επίσης σε JSON και αποστέλλονται με `Content-Type: application/json`.

---

## Όρια και φίλτρα {: #limits-and-filters }

Τα endpoints λιστών επιστρέφουν το πολύ `limit` στοιχεία: 200 από προεπιλογή και έως 5000. Μια
τιμή εκτός αυτού του εύρους απορρίπτεται με `400`. Δεν υπάρχει offset ούτε token σελίδας, οπότε
περιορίστε μια λίστα με τα φίλτρα της, για παράδειγμα `project_id`, `data_source_id` ή
`start_date` και `end_date` στις καταστάσεις επιθεώρησης.

Ένα αίτημα που διαρκεί περισσότερο από 60 δευτερόλεπτα ακυρώνεται με `408 Request Timeout`.

---

## Σφάλματα {: #errors }

Μια απόκριση σφάλματος έχει σώμα JSON με έναν κωδικό και ένα μήνυμα:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Κατάσταση | Κωδικός | Σημασία |
|---|---|---|
| `400` | `BAD_REQUEST` | Το αίτημα δεν είναι έγκυρο, για παράδειγμα ένα `limit` εκτός εύρους |
| `401` | `NOT_AUTHENTICATED` | Το κλειδί API λείπει, έχει λανθασμένη μορφή, είναι άγνωστο ή έχει λήξει |
| `403` | `NOT_AUTHORIZED` | Ο χρήστης του κλειδιού δεν έχει τον ρόλο που απαιτεί αυτό το αίτημα |
| `403` | `INVALID_LICENSE` | Η άδεια χρήσης του *digna* έχει λήξει |
| `404` | `NOT_FOUND` | Το project, η πηγή δεδομένων ή άλλο στοιχείο δεν υπάρχει |
| `500` | `INTERNAL_ERROR` | Απρόσμενο σφάλμα στο *digna*. Οι λεπτομέρειες βρίσκονται στο log του backend |

Το `message` μιας απόκρισης `401` δείχνει τι δεν πάει καλά με το κλειδί:

| Μήνυμα | Αιτία |
|---|---|
| `Missing Authorization header` | Δεν στάλθηκε κεφαλίδα `Authorization` |
| `Invalid Authorization header format` | Η τιμή δεν ξεκινά με `Bearer ` |
| `Invalid API key` | Το κλειδί είναι λάθος ή έχει διαγραφεί |
| `API key expired` | Το κλειδί έχει λήξει. Δημιουργήστε ένα νέο |

---

## Εκτέλεση επιθεώρησης {: #running-an-inspection }

Μια τυπική ενσωμάτωση ξεκινά μια επιθεώρηση όταν ολοκληρωθεί μια φόρτωση δεδομένων, περιμένει να
τελειώσει και διαβάζει το αποτέλεσμα:

1. **Ξεκινήστε την επιθεώρηση** με [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   Η απόκριση περιέχει το `id` του αιτήματος.
2. **Παρακολουθήστε την πρόοδό της** με [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   Το `status` της περνά από `PENDING` μέσω `RUNNING` σε `COMPLETED` ή καταλήγει σε `FAILED`,
   `ABORTED` ή `CANCELLED`. Ρωτήστε ξανά κάθε λίγα δευτερόλεπτα, μέχρι να μην αλλάζει πια.
3. **Διαβάστε το αποτέλεσμα** με [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   για τις ημερομηνίες που επιθεωρήθηκαν. Κάθε στοιχείο έχει μια συνολική κατάσταση `status`:
   `0` (OK), `1` (προειδοποίηση), `2` (κρίσιμη) ή `-1` (χωρίς κατάσταση), καθώς και μια κατάσταση
   ανά module με τον αριθμό των επιτυχημένων, αβέβαιων και αποτυχημένων ελέγχων.

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

## Έγγραφο OpenAPI {: #openapi-document }

Κάθε εγκατάσταση του *digna* περιγράφει αυτό το API σε ένα έγγραφο OpenAPI 3.1 και προσφέρει ένα
διαδραστικό Swagger UI για να δοκιμάζετε αιτήματα:

| Τι | Διεύθυνση |
|---|---|
| Έγγραφο OpenAPI | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Το έγγραφο του Release 2026.11 είναι επίσης διαθέσιμο εδώ: [openapi.json](openapi.json).
Χρησιμοποιήστε το για να δημιουργήσετε ένα client σε άλλη γλώσσα προγραμματισμού.

!!! note "Καλύπτονται μόνο τα endpoints /v1"

    Το dashboard επικοινωνεί με το backend και μέσω άλλων, εσωτερικών endpoints. Αυτά δεν αποτελούν
    μέρος αυτού του API και μπορεί να αλλάξουν με οποιαδήποτε έκδοση, οπότε βασίστε τις
    ενσωματώσεις μόνο στα endpoints `/v1`.
