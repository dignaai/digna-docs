---
title: Claude – Connecter Claude à digna via MCP | Documentation digna
description: Connectez Claude à digna via le digna MCP Server — Claude Code en ligne de commande ou avec un fichier .mcp.json partagé, Claude Desktop avec une passerelle locale, et les connecteurs personnalisés de claude.ai, avec une clé d'API dans l'en-tête Authorization.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, connecteur personnalisé claude.ai, digna MCP server, mcp-remote, Authorization Bearer, clé d'API digna
---

# Connecter Claude à digna

Ce guide connecte Claude au **digna MCP Server**. Vous avez besoin du point de terminaison MCP de
votre installation *digna* et d'une clé d'API, comme décrit dans la
[présentation des agents IA](overview.md).

Les exemples utilisent `https://digna.example.com/mcp` comme point de terminaison. Remplacez-le par le
vôtre.

## Choisir le mode de connexion {: #choose-how-to-connect }

| Produit Claude | Se connecte depuis | Fonctionne avec *digna* au sein de votre réseau |
|---|---|---|
| [Claude Code](#claude-code) | Votre machine | Oui |
| [Claude Desktop avec une passerelle locale](#claude-desktop-with-a-local-bridge) | Votre machine | Oui |
| [Connecteur personnalisé](#custom-connector) dans claude.ai, Claude Desktop et Claude mobile | Le cloud d'Anthropic | Non. Le point de terminaison doit être joignable depuis Internet |

Pour une installation *digna* qui s'exécute au sein du réseau de votre entreprise, utilisez Claude
Code ou Claude Desktop avec une passerelle locale.

---

## Claude Code {: #claude-code }

### 1. Ajouter le serveur {: #1-add-the-server }

Placez la clé d'API dans une variable d'environnement, puis ajoutez le serveur :

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Votre shell remplace `$DIGNA_API_KEY` par sa valeur lorsque vous exécutez la commande ; Claude Code
enregistre donc la clé dans sa propre configuration.

`--scope` détermine où le serveur est disponible :

| Portée | Disponible |
|---|---|
| `local` (par défaut) | Pour vous, uniquement dans le projet actuel |
| `user` | Pour vous, dans tous les projets |
| `project` | Pour toutes les personnes qui travaillent sur le projet, via un fichier `.mcp.json` dans le projet |

### 2. Partager le serveur avec votre équipe (facultatif) {: #2-share-the-server-with-your-team }

Pour fournir le même serveur à toutes les personnes d'un projet, ajoutez un fichier `.mcp.json` à la
racine du projet. N'écrivez pas la clé dans le fichier. Claude Code remplace `${DIGNA_API_KEY}` à
partir de l'environnement de chaque personne :

```json
{
  "mcpServers": {
    "digna": {
      "type": "http",
      "url": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${DIGNA_API_KEY}"
      }
    }
  }
}
```

Chaque personne définit `DIGNA_API_KEY` avec sa propre clé. La première fois que Claude Code trouve le
fichier, il demande s'il faut utiliser les serveurs qu'il contient.

### 3. Vérifier la connexion {: #3-verify-the-connection }

Depuis votre shell :

```bash
claude mcp list
```

Le serveur `digna` doit afficher `✔ Connected`. Dans une session Claude Code, exécutez `/mcp` pour
voir le serveur et ses outils.

---

## Claude Desktop avec une passerelle locale {: #claude-desktop-with-a-local-bridge }

Le fichier de configuration de Claude Desktop démarre des serveurs MCP locaux sur votre machine. Une
petite passerelle, le paquet open source [`mcp-remote`](https://github.com/geelen/mcp-remote),
s'y exécute et transmet chaque requête au point de terminaison *digna* avec votre clé d'API. Comme la
passerelle s'exécute sur votre machine, cela fonctionne avec *digna* au sein du réseau de votre
entreprise.

!!! note "Un paquet communautaire"

    `mcp-remote` est maintenu par sa communauté open source, et non par Anthropic ou digna. Vérifiez
    que votre organisation l'autorise avant de l'utiliser.

### 1. Installer Node.js {: #1-install-nodejs }

La passerelle nécessite [Node.js](https://nodejs.org) 18 ou ultérieur. Claude Desktop utilise la
version de Node.js installée sur votre système. Vérifiez-la avec :

```bash
node --version
```

### 2. Modifier le fichier de configuration {: #2-edit-the-configuration-file }

Ouvrez `claude_desktop_config.json` :

- **macOS** : `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows** : `%APPDATA%\Claude\claude_desktop_config.json`

Ajoutez le serveur `digna`. Si le fichier contient déjà une section `mcpServers`, ajoutez-y l'entrée
`digna` :

```json
{
  "mcpServers": {
    "digna": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://digna.example.com/mcp",
        "--transport",
        "http-only",
        "--header",
        "Authorization:${AUTH_HEADER}"
      ],
      "env": {
        "AUTH_HEADER": "Bearer <api key>"
      }
    }
  }
}
```

!!! warning "Gardez l'en-tête exactement tel quel"

    Écrivez `Authorization:${AUTH_HEADER}` sans espace, et placez `Bearer <api key>` dans `env`.
    Claude Desktop sous Windows n'échappe pas les espaces dans `args` : un espace à cet endroit rend
    l'en-tête invalide.

### 3. Redémarrer Claude Desktop {: #3-restart-claude-desktop }

Quittez complètement Claude Desktop et relancez-le. Dans une nouvelle conversation, cliquez sur **+**
et ouvrez **Connectors** : `digna` doit y figurer et être activé.

---

## Connecteur personnalisé {: #custom-connector }

Un connecteur personnalisé rend *digna* disponible dans claude.ai, Claude Desktop et les applications
mobiles Claude, sans aucune configuration locale. C'est le cloud d'Anthropic qui se connecte au point
de terminaison ; cela ne fonctionne donc que si :

- Le point de terminaison *digna* est joignable depuis Internet en HTTPS
- Votre organisation Claude dispose de l'option **Request headers** dans la boîte de dialogue
  **Add custom connector**. Anthropic la propose en bêta à un nombre limité d'organisations

!!! warning "Pas pour digna au sein de votre réseau"

    Les tunnels MCP de Claude, qui atteignent des serveurs au sein d'un réseau privé, exigent OAuth
    sur le serveur MCP. Le digna MCP Server s'authentifie avec des clés d'API ; un tunnel ne peut
    donc pas être utilisé. Utilisez plutôt [Claude Code](#claude-code) ou
    [Claude Desktop avec une passerelle locale](#claude-desktop-with-a-local-bridge).

### 1. Ouvrir les paramètres des connecteurs {: #1-open-the-connector-settings }

- **Forfaits Free, Pro, Max et Ultra** : allez dans **Customize > Connectors** et cliquez sur
  **Add custom connector**.
- **Forfaits Team et Enterprise** : un Owner va dans **Organization settings > Connectors**, clique
  sur **Add**, puis sur **Custom**, et choisit **Web** si le type est demandé.

### 2. Saisir les détails du connecteur {: #2-enter-the-connector-details }

1. **MCP server URL** : `https://digna.example.com/mcp`
2. **Authentication** : **No sign-in**
3. **Request headers** : choisissez `authorization` comme nom d'en-tête, saisissez `Bearer <api key>`
   comme valeur, y compris le mot `Bearer` et l'espace, et cochez **Required**.
4. Cliquez sur **Add**.

!!! warning "Tout le monde partage la clé"

    Chaque membre qui utilise le connecteur travaille avec la même clé d'API, et donc avec le même
    utilisateur *digna*. Créez un utilisateur *digna* dédié au connecteur et donnez-lui uniquement
    les projets et les rôles que tout le monde peut avoir, par ex. le rôle de lecteur.

Avec les forfaits Team et Enterprise, les membres se connectent ensuite sous
**Customize > Connectors**, où le connecteur porte le libellé **Custom**.

Claude ne peut pas modifier l'en-tête d'un connecteur existant. Pour utiliser une nouvelle clé,
supprimez le connecteur et ajoutez-le à nouveau.

---

## Dépannage de Claude {: #troubleshooting-claude }

### claude mcp list affiche Failed to connect

Exécutez `claude mcp get digna` pour en voir la raison. Un `401` signifie que la clé a été refusée ;
voir [401 Unauthorized](overview.md#troubleshooting). Claude Code signale aussi les espaces ou un
saut de ligne au début ou à la fin de la clé, qui apparaissent souvent lors du copier-coller.

### digna n'apparaît pas dans Claude Desktop

- Vérifiez que Node.js 18 ou ultérieur est installé : `node --version`.
- Vérifiez que `claude_desktop_config.json` est un JSON valide. Une virgule manquante empêche le
  chargement de tous les serveurs du fichier.
- Quittez complètement Claude Desktop, pas seulement la fenêtre, et relancez-le.

### Le connecteur personnalisé ne parvient pas à joindre le serveur

Le cloud d'Anthropic ne parvient pas à joindre le point de terminaison. Vérifiez qu'il est joignable
depuis Internet en HTTPS avec un certificat valide, ou connectez-vous plutôt via
[Claude Code](#claude-code).

---

## Voir aussi {: #see-also }

- [Présentation des agents IA](overview.md) : point de terminaison, clé d'API, sécurité et dépannage général
- [Gemini](gemini_mcp_guide.md) : connecter Antigravity ou Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md) : ce que les agents IA peuvent faire avec *digna*
