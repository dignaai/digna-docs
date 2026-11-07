# Connecter Gemini à digna

Ce guide connecte les outils Gemini de Google au **digna MCP Server**. Vous avez besoin du point de
terminaison MCP de votre installation *digna* et d'une clé d'API, comme décrit dans la
[présentation des agents IA](overview.md).

Les exemples utilisent `https://digna.example.com/mcp` comme point de terminaison. Remplacez-le par le
vôtre.

## Choisir votre outil {: #choose-your-tool }

| Outil | Pour | Configuration |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE et application | Les outils d'agent de Google. Antigravity CLI a remplacé Gemini CLI pour les comptes Google individuels en juin 2026 | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Licences Gemini Code Assist Standard et Enterprise, et clés d'API Gemini payantes | `settings.json` ou `gemini mcp add` |
| Application Gemini Enterprise | — | Non pris en charge. Son connecteur MCP personnalisé se connecte avec OAuth ou un compte de service Google Cloud, alors que le digna MCP Server s'authentifie avec des clés d'API |

Tous ces outils se connectent depuis la machine sur laquelle ils s'exécutent ; ils fonctionnent donc
avec *digna* au sein du réseau de votre entreprise, tant que cette machine peut joindre le point de
terminaison.

---

## Antigravity {: #antigravity }

Antigravity lit ses serveurs MCP dans `mcp_config.json`, partagé par la CLI, l'IDE et l'application.

### 1. Ouvrir mcp_config.json {: #1-open-mcp-config-json }

| Portée | Fichier |
|---|---|
| Tous vos projets | `~/.gemini/config/mcp_config.json` |
| Un espace de travail | `.agents/mcp_config.json` dans l'espace de travail |

Pour ouvrir le fichier utilisé :

- **CLI** : tapez `/mcp` et appuyez sur ++enter++ pour ouvrir le gestionnaire MCP.
- **IDE** : dans le panneau latéral de l'agent, ouvrez le menu **…**, sélectionnez **MCP Servers**,
  puis **Manage MCP Servers**, puis **View raw config**.
- **Application** : allez dans **Customizations** > **Installed** > **MCP Servers** et utilisez
  **Copy Config File Path**.

### 2. Ajouter le serveur digna {: #2-add-the-digna-server }

Ajoutez l'entrée `digna`. Si le fichier contient déjà une section `mcpServers`, ajoutez-la à
celle-ci :

```json
{
  "mcpServers": {
    "digna": {
      "serverUrl": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

Antigravity n'atteint les serveurs distants qu'en HTTP streamable, le transport qu'utilise le digna
MCP Server. Indiquez le point de terminaison dans `serverUrl` ; la clé `httpUrl` de Gemini CLI n'est
pas prise en charge.

### 3. Vérifier la connexion {: #3-verify-the-connection }

Dans la CLI, tapez `/mcp` : le gestionnaire MCP affiche le serveur `digna` avec son état et ses
outils, et peut recharger la configuration et afficher les journaux de connexion. Dans l'IDE, le
serveur apparaît sous **Manage MCP Servers**.

!!! warning "Protégez le fichier"

    `mcp_config.json` contient la clé d'API en clair. Gardez un fichier d'espace de travail
    `.agents/mcp_config.json` hors du contrôle de version, et ne permettez qu'à votre propre compte
    de lire le fichier global.

---

## Gemini CLI {: #gemini-cli }

### 1. Ajouter le serveur {: #1-add-the-server }

Placez la clé d'API dans une variable d'environnement, puis ajoutez le serveur :

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Votre shell remplace `$DIGNA_API_KEY` par sa valeur lorsque vous exécutez la commande ; Gemini CLI
enregistre donc la clé dans ses paramètres. Sans `--scope user`, le serveur est ajouté uniquement au
projet actuel.

### 2. Ou modifier settings.json {: #2-or-edit-settings-json }

La commande ci-dessus écrit dans `settings.json`. Pour modifier le fichier vous-même :

| Portée | Fichier |
|---|---|
| Tous vos projets | `~/.gemini/settings.json` |
| Un projet | `.gemini/settings.json` dans le projet |

```json
{
  "mcpServers": {
    "digna": {
      "httpUrl": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

Utilisez `httpUrl`, la clé pour le HTTP streamable. La clé voisine `url` sélectionne l'ancien
transport SSE, que le digna MCP Server ne propose pas. N'utilisez pas de tiret bas dans le nom du
serveur.

!!! tip "Laissez trust désactivé"

    Gemini CLI demande confirmation avant chaque appel d'outil, sauf si le serveur a
    `"trust": true`. Laissez `trust` désactivé pour *digna*, afin de confirmer chaque modification
    qu'un agent apporte à votre configuration.

### 3. Vérifier la connexion {: #3-verify-the-connection-gemini-cli }

Depuis votre shell :

```bash
gemini mcp list
```

Le serveur `digna` doit apparaître comme connecté. Dans une session Gemini CLI, exécutez `/mcp` pour
voir le serveur et ses outils.

---

## Dépannage de Gemini {: #troubleshooting-gemini }

### Le serveur apparaît comme déconnecté

- Vérifiez que le point de terminaison se termine par `/mcp` et qu'il est joignable depuis votre
  machine.
- Vérifiez le nom de la clé : `serverUrl` dans Antigravity, `httpUrl` dans Gemini CLI.
- Un `401` signifie que la clé a été refusée ; voir [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI ne démarre plus pour mon compte

Depuis juin 2026, les comptes Google individuels utilisent Antigravity CLI au lieu de Gemini CLI.
Déplacez l'entrée `digna` vers `mcp_config.json` comme décrit sous [Antigravity](#antigravity), et
renommez `httpUrl` en `serverUrl`.

---

## Voir aussi {: #see-also }

- [Présentation des agents IA](overview.md) : point de terminaison, clé d'API, sécurité et dépannage général
- [Claude](claude_mcp_guide.md) : connecter Claude Code, Claude Desktop ou un connecteur personnalisé
- [digna Agentic](../platform/agentic/Introduction.md) : ce que les agents IA peuvent faire avec *digna*