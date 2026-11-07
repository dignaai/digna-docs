---
title: Agents IA – Présentation de l'intégration MCP | Documentation digna
description: Connectez Claude, Gemini et d'autres agents IA à digna via le digna MCP Server. Trouvez le point de terminaison MCP, créez une clé d'API, vérifiez la licence et les prérequis réseau, et choisissez le guide de votre client IA.
image: /assets/logo_square.png
keywords: digna MCP server, Model Context Protocol, connecter un agent IA, Claude MCP, Gemini MCP, Antigravity MCP, clé d'API digna, digna Agentic
---

# Connecter des agents IA à digna

Le **digna MCP Server** permet aux agents IA de travailler avec *digna* via le
[Model Context Protocol](https://modelcontextprotocol.io) (MCP), un standard ouvert pris en charge par
Claude, Gemini et de nombreux autres outils d'IA. Un agent connecté à *digna* peut répondre à des
questions sur vos données, analyser des alertes et aider à configurer *digna*. Consultez
[digna Agentic](../platform/agentic/Introduction.md) pour savoir ce que les agents peuvent faire.

Cette page couvre le côté *digna*, identique pour tous les clients IA. Les guides des clients
montrent ensuite où saisir ces informations :

- [Claude](claude_mcp_guide.md) : Claude Code, Claude Desktop et connecteurs personnalisés
- [Gemini](gemini_mcp_guide.md) : Antigravity et Gemini CLI

!!! info "Bêta"

    digna Agentic, et avec lui le digna MCP Server, est livré en version bêta dans la
    [Release 2026.11](../changelog/Release_202611.md).

---

## Avant de commencer {: #before-you-start }

Vous avez besoin de :

- *digna* Release 2026.11 ou ultérieure
- Une licence qui inclut **digna Agentic**. Sans elle, le serveur MCP refuse toutes les requêtes
- Un compte utilisateur *digna*. L'agent agit avec les autorisations de cet utilisateur dans chaque
  projet, voir [Autorisations](../platform/agentic/how_it_works.md#permissions)
- Un client IA qui se connecte à des serveurs MCP distants en **HTTP streamable** et peut envoyer un
  en-tête `Authorization`

---

## 1. Trouver le point de terminaison MCP {: #1-find-the-mcp-endpoint }

Le serveur MCP fait partie du backend *digna* : il n'y a donc rien à installer ni à démarrer en plus.
Son point de terminaison est l'adresse du backend suivie de `/mcp` :

```text
https://digna.example.com/mcp
```

Si le backend s'exécute directement sur un hôte et un port, par exemple après
`digna serve --address 0.0.0.0 --port 8082`, le point de terminaison est cette adresse suivie de
`/mcp` :

```text
http://digna-host:8082/mcp
```

Si un reverse proxy se trouve devant le backend, il doit transmettre `/mcp` au backend avec l'en-tête
`Authorization`.

!!! warning "Utilisez HTTPS sur un réseau"

    Chaque requête transporte une clé d'API. Utilisez HTTPS dès que le client IA et *digna* ne sont
    pas sur la même machine.

### D'où vient la connexion {: #where-the-connection-comes-from }

La plupart des clients IA se connectent depuis la machine sur laquelle ils s'exécutent : Claude Code,
Claude Desktop avec une passerelle locale, Antigravity et Gemini CLI. Pour eux, *digna* doit
simplement être joignable depuis cette machine, par exemple au sein du réseau de votre entreprise.

Les **connecteurs personnalisés** de Claude sont différents : c'est le cloud d'Anthropic qui se
connecte au point de terminaison. Ils ne fonctionnent que si le point de terminaison est joignable
depuis Internet en HTTPS. Pour une installation *digna* joignable uniquement au sein de votre réseau,
utilisez un client qui s'exécute sur votre machine.

---

## 2. Créer une clé d'API {: #2-create-an-api-key }

Un client IA s'authentifie avec la clé d'API d'un utilisateur *digna*.

1. Connectez-vous à *digna*.
2. Ouvrez votre profil utilisateur dans le coin inférieur gauche.
3. Cliquez sur **API Keys**, puis sur **Add API Key**.
4. Saisissez un nom qui indique à quoi sert la clé, par ex. *Claude Code – Marcin*, et choisissez sa
   date d'expiration.
5. Copiez la clé. Elle n'est affichée qu'une seule fois.

Chaque requête au serveur MCP envoie la clé dans cet en-tête :

```text
Authorization: Bearer <api key>
```

Le mot `Bearer` et l'espace qui le suit font partie de la valeur de l'en-tête.

---

## 3. Connecter votre client IA {: #3-connect-your-ai-client }

| Client IA | Se connecte depuis | Guide |
|---|---|---|
| Claude Code | Votre machine | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop avec une passerelle locale | Votre machine | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Connecteur personnalisé Claude (claude.ai, Claude Desktop, Claude mobile) | Le cloud d'Anthropic | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE et application | Votre machine | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Votre machine | [Gemini](gemini_mcp_guide.md#gemini-cli) |

D'autres clients MCP fonctionnent également s'ils prennent en charge les serveurs distants en HTTP
streamable avec un en-tête personnalisé. La plupart lisent une configuration comme celle-ci.
Consultez la documentation de votre client pour les noms exacts du fichier et des clés :

```json
{
  "mcpServers": {
    "digna": {
      "type": "http",
      "url": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

---

## 4. Essayer {: #4-try-it }

Posez à l'agent une question à laquelle seul *digna* peut répondre :

- *« Liste mes projets digna. »*
- *« Quelles sources de données du projet X ne sont pas vertes aujourd'hui ? »*
- *« Explique le dernier contrôle en échec de la source de données Y. »*

Si l'agent liste vos projets, la connexion fonctionne.

---

## Sécurité {: #security }

- **Une clé par personne et par client.** Vous pouvez ainsi révoquer une seule clé, avec
  **Delete API Key**, sans affecter les autres.
- **Choisissez l'utilisateur avec soin.** L'agent peut faire tout ce que l'utilisateur de la clé peut
  faire. Pour analyser des données uniquement, utilisez un utilisateur ayant le rôle de lecteur dans
  les projets.
- **Ne mettez pas de clés dans des fichiers partagés.** Ne committez pas un fichier de configuration
  qui contient une clé. Lorsque le client le permet, lisez la clé depuis une variable
  d'environnement.
- **Définissez une date d'expiration.** Créez une nouvelle clé avant l'expiration de l'ancienne et
  mettez à jour le client.
- **Vérifiez les appels d'outils.** Laissez activée la confirmation des appels d'outils dans le
  client, au moins pour les appels qui modifient la configuration.

---

## Dépannage {: #troubleshooting }

### 401 Unauthorized

La réponse indique la raison :

| Message | Cause |
|---|---|
| `Missing or malformed Authorization header` | Aucun en-tête n'a été envoyé, ou la valeur ne commence pas par `Bearer ` |
| `Invalid API key` | La clé est erronée ou a été supprimée |
| `API key expired` | La clé a expiré. Créez-en une nouvelle |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

La licence *digna* ne contient pas d'entrée digna Agentic, ou cette entrée a expiré. Demandez à
l'équipe digna une licence qui inclut digna Agentic, et installez-la comme le décrit le guide
d'installation de votre système d'exploitation.

### Toutes les requêtes échouent avec une erreur de licence invalide

La licence *digna* elle-même a expiré. Le serveur MCP cesse de répondre, tout comme le tableau de
bord, jusqu'à l'installation d'une nouvelle licence.

### L'agent peut lire la configuration mais pas la modifier

L'utilisateur associé à la clé d'API n'a pas le rôle d'éditeur dans ce projet. Utilisez la clé d'un
utilisateur ayant le rôle d'éditeur, ou demandez à un administrateur du projet de changer le rôle.

### Le client ne parvient pas du tout à se connecter

La machine qui se connecte ne peut pas joindre le point de terminaison. Ouvrez l'adresse du point de
terminaison depuis cette machine, et vérifiez les pare-feu, les proxys et le certificat. Pour un
connecteur personnalisé Claude, cette machine se trouve dans le cloud d'Anthropic, voir
[D'où vient la connexion](#where-the-connection-comes-from).
