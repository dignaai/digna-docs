# API REST de digna 2026.11

L'API REST de *digna* permet à vos propres outils et pipelines de travailler avec *digna* en HTTP et
JSON : lire les projets et les résultats d'inspection, gérer les sources de données, les jeux de
données et les attributs, et lancer des inspections, par exemple à la fin d'un chargement de données.
Le [Python SDK](../../sdk/Release%202026.11/index.md) utilise la même API.

Cette page décrit ce que toutes les requêtes ont en commun. Les pages de ressources présentent chaque
endpoint avec ses paramètres, son corps de requête, ses réponses et ses schémas :

| Ressource | Endpoints |
|---|---|
| [Projects](projects.md) | Lire les projets |
| [DB Connections](db_connections.md) | Lire les connexions aux bases de données |
| [Data Sources](data_sources.md) | Créer, lire, modifier et supprimer des sources de données |
| [Data Sets](data_sets.md) | Créer, lire, modifier et supprimer des jeux de données |
| [Attributes](attributes.md) | Créer, lire, modifier et supprimer des attributs |
| [Check Definitions](check_definitions.md) | Lire les définitions de contrôles |
| [Inspection Requests](inspection_requests.md) | Lancer des inspections et suivre leur progression |
| [Inspection Statuses](inspection_statuses.md) | Lire les résultats d'inspection par projet, source de données et jeu de données |

---

## URL de base {: #base-url }

L'API fait partie du backend de *digna*. Chaque chemin commence par `/v1`, après l'adresse du backend :

```text
https://digna.example.com/v1/projects
```

L'adresse du backend est celle qu'utilise le tableau de bord : `baseUrl` dans la section `[api]` de
`dashboard/dashboard_config.toml`. Utilisez HTTPS dès que l'appelant et *digna* ne se trouvent pas sur
la même machine, car chaque requête transporte une clé d'API.

---

## Authentification {: #authentication }

Chaque requête envoie la clé d'API d'un utilisateur *digna* dans l'en-tête `Authorization` :

```text
Authorization: Bearer <api key>
```

Pour créer une clé, ouvrez votre profil utilisateur en bas à gauche du tableau de bord, cliquez sur
**API Keys**, puis sur **Add API Key**, et copiez la clé. Elle n'est affichée qu'une seule fois. Les
mêmes clés fonctionnent pour le [digna MCP Server](../../ai_agents/overview.md).

Une requête s'exécute avec les autorisations de l'utilisateur de la clé. Créer, modifier et supprimer
nécessite le rôle d'éditeur dans le projet ; sinon, la requête est refusée avec `403` et le message
`You don't have permission to edit this project`.

!!! tip "Utilisez un utilisateur dédié à l'automatisation"

    Créez un utilisateur *digna* pour chaque intégration, attribuez-lui uniquement les projets et les
    rôles dont il a besoin, et créez sa clé avec une date d'expiration. Vous pourrez alors révoquer
    l'accès d'une intégration en supprimant sa clé, sans affecter qui que ce soit d'autre.

---

## Envoyer une requête {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Les réponses sont au format JSON. Les listes sont renvoyées sous forme de tableau JSON. Les corps de
requête sont également en JSON et envoyés avec `Content-Type: application/json`.

---

## Limites et filtres {: #limits-and-filters }

Les endpoints de liste renvoient au plus `limit` éléments : 200 par défaut, et jusqu'à 5000. Une valeur
en dehors de cette plage est rejetée avec `400`. Il n'existe ni offset ni jeton de page : affinez donc
une liste avec ses filtres, par exemple `project_id`, `data_source_id`, ou `start_date` et `end_date`
pour les statuts d'inspection.

Une requête qui dure plus de 60 secondes est annulée avec `408 Request Timeout`.

---

## Erreurs {: #errors }

Une réponse d'erreur a un corps JSON contenant un code et un message :

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Statut | Code | Signification |
|---|---|---|
| `400` | `BAD_REQUEST` | La requête n'est pas valide, par exemple un `limit` hors plage |
| `401` | `NOT_AUTHENTICATED` | La clé d'API est absente, mal formée, inconnue ou expirée |
| `403` | `NOT_AUTHORIZED` | L'utilisateur de la clé n'a pas le rôle requis par cette requête |
| `403` | `INVALID_LICENSE` | La licence *digna* a expiré |
| `404` | `NOT_FOUND` | Le projet, la source de données ou un autre élément n'existe pas |
| `500` | `INTERNAL_ERROR` | Une erreur inattendue dans *digna*. Le journal du backend contient les détails |

Le `message` d'une réponse `401` indique ce qui ne va pas avec la clé :

| Message | Cause |
|---|---|
| `Missing Authorization header` | Aucun en-tête `Authorization` n'a été envoyé |
| `Invalid Authorization header format` | La valeur ne commence pas par `Bearer ` |
| `Invalid API key` | La clé est erronée, ou elle a été supprimée |
| `API key expired` | La clé a expiré. Créez-en une nouvelle |

---

## Exécuter une inspection {: #running-an-inspection }

Une intégration typique lance une inspection lorsqu'un chargement de données est terminé, attend sa
fin, puis lit le résultat :

1. **Lancez l'inspection** avec [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   La réponse contient l'`id` de la demande.
2. **Suivez sa progression** avec [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   Son `status` passe de `PENDING` à `RUNNING` puis à `COMPLETED`, ou se termine en `FAILED`,
   `ABORTED` ou `CANCELLED`. Interrogez-la à nouveau toutes les quelques secondes jusqu'à ce qu'il ne
   change plus.
3. **Lisez le résultat** avec [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   pour les dates inspectées. Chaque élément a un `status` global : `0` (OK), `1` (avertissement),
   `2` (critique) ou `-1` (aucun statut), ainsi qu'un statut par module avec le nombre de contrôles
   réussis, incertains et échoués.

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

## Document OpenAPI {: #openapi-document }

Chaque installation de *digna* décrit cette API dans un document OpenAPI 3.1 et propose une Swagger UI
interactive pour y essayer des requêtes :

| Quoi | Adresse |
|---|---|
| Document OpenAPI | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Le document de Release 2026.11 est également disponible ici : [openapi.json](openapi.json). Utilisez-le
pour générer un client dans un autre langage.

!!! note "Seuls les endpoints /v1 sont couverts"

    Le tableau de bord communique aussi avec le backend par d'autres endpoints, internes. Ils ne font
    pas partie de cette API et peuvent changer à chaque version : construisez donc vos intégrations
    uniquement sur les endpoints `/v1`.