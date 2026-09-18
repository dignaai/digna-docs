# Référence du SDK Python digna 2026.06

Cette section documente le SDK Python de ***digna***. Elle est organisée comme une référence multipage : utilisez cette vue d'ensemble pour comprendre le client, puis poursuivez avec les pages dédiées au démarrage rapide, aux ressources, aux modèles, aux erreurs et à la documentation d'API générée.

Le SDK est publié sous la forme du paquet `digna-sdk` et expose un client stable et versionné pour l'API REST de ***digna***.

---

## Notions de base du SDK

---

### Vue d'ensemble

Le SDK repose sur une conception de client orientée ressources. Chaque domaine de l'API est exposé comme un client de premier niveau sur le `DignaClient` racine, avec des modèles de requête et de réponse typés et une gestion cohérente des erreurs.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Fonctionnalités principales

- **Modèles typés** — chaque requête et chaque réponse est validée avec pydantic, si bien que votre éditeur et votre vérificateur de types détectent les erreurs avant tout appel réseau.
- **Orienté ressources** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` et `client.inspection_statuses` exposent chacun de simples méthodes `list` / `get` / `create` / `update` / `delete`.
- **Erreurs explicites** — les erreurs d'API lèvent `DignaAPIError` (ou une sous-classe plus spécifique comme `DignaAuthenticationError`, `DignaAuthorizationError` ou `DignaNotFoundError`) au lieu de renvoyer silencieusement `None`.

### Installation

```bash
pip install digna-sdk
```

---

## Pages de référence

Cette version est répartie sur les pages suivantes :

- [Démarrage rapide](quickstart.md) — se connecter et effectuer ses premiers appels.
- [Ressources](resources.md) — la liste complète des clients de ressources disponibles.
- [Modèles](models.md) — les modèles pydantic utilisés en entrée et en sortie.
- [Erreurs](errors.md) — la hiérarchie des exceptions.
- [Référence de l'API](reference.md) — documentation de référence générée automatiquement.