---
title: Claude – Conectar o Claude ao digna via MCP | Documentação digna
description: Conecte o Claude ao digna por meio do digna MCP Server — Claude Code pela linha de comando ou por um .mcp.json compartilhado, Claude Desktop com uma ponte local e conectores personalizados no claude.ai, com uma chave de API no cabeçalho Authorization.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, conector personalizado claude.ai, digna MCP server, mcp-remote, Authorization Bearer, chave de API do digna
---

# Conectar o Claude ao digna

Este guia conecta o Claude ao **digna MCP Server**. Você precisa do endpoint MCP da sua instalação
do *digna* e de uma chave de API, conforme descrito na [Visão Geral de Agentes de IA](overview.md).

Os exemplos usam `https://digna.example.com/mcp` como endpoint. Substitua-o pelo seu.

## Escolher Como Conectar {: #choose-how-to-connect }

| Produto Claude | Conecta-se a partir de | Funciona com o *digna* dentro da sua rede |
|---|---|---|
| [Claude Code](#claude-code) | Sua máquina | Sim |
| [Claude Desktop com uma ponte local](#claude-desktop-with-a-local-bridge) | Sua máquina | Sim |
| [Conector personalizado](#custom-connector) no claude.ai, Claude Desktop e Claude mobile | Nuvem da Anthropic | Não. O endpoint precisa estar acessível pela internet |

Para uma instalação do *digna* que roda dentro da rede da sua empresa, use o Claude Code ou o Claude
Desktop com uma ponte local.

---

## Claude Code {: #claude-code }

### 1. Adicionar o Servidor {: #1-add-the-server }

Coloque a chave de API em uma variável de ambiente e depois adicione o servidor:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

O seu shell substitui `$DIGNA_API_KEY` quando você executa o comando, então o Claude Code armazena a
chave na própria configuração.

`--scope` define onde o servidor fica disponível:

| Escopo | Disponível |
|---|---|
| `local` (padrão) | Para você, apenas no projeto atual |
| `user` | Para você, em todos os projetos |
| `project` | Para todos que trabalham no projeto, por meio de um arquivo `.mcp.json` no projeto |

### 2. Compartilhar o Servidor com a Sua Equipe (Opcional) {: #2-share-the-server-with-your-team }

Para dar a todos de um projeto o mesmo servidor, adicione um arquivo `.mcp.json` à raiz do projeto.
Não escreva a chave no arquivo. O Claude Code preenche `${DIGNA_API_KEY}` a partir do ambiente de
cada pessoa:

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

Cada pessoa define `DIGNA_API_KEY` com a própria chave. Na primeira vez que o Claude Code encontra o
arquivo, ele pergunta se deve usar os servidores definidos nele.

### 3. Verificar a Conexão {: #3-verify-the-connection }

No seu shell:

```bash
claude mcp list
```

O servidor `digna` precisa mostrar `✔ Connected`. Dentro de uma sessão do Claude Code, execute `/mcp`
para ver o servidor e as suas ferramentas.

---

## Claude Desktop com uma Ponte Local {: #claude-desktop-with-a-local-bridge }

O arquivo de configuração do Claude Desktop inicia servidores MCP locais na sua máquina. Uma pequena
ponte, o pacote de código aberto [`mcp-remote`](https://github.com/geelen/mcp-remote), roda ali e
encaminha cada requisição ao endpoint do *digna* com a sua chave de API. Como a ponte roda na sua
máquina, isso funciona com o *digna* dentro da rede da sua empresa.

!!! note "Um Pacote da Comunidade"

    O `mcp-remote` é mantido pela sua comunidade de código aberto, não pela Anthropic nem pela
    digna. Verifique se a sua organização permite o seu uso antes de utilizá-lo.

### 1. Instalar o Node.js {: #1-install-nodejs }

A ponte precisa do [Node.js](https://nodejs.org) 18 ou posterior. O Claude Desktop usa a versão do
Node.js instalada no seu sistema. Verifique-a com:

```bash
node --version
```

### 2. Editar o Arquivo de Configuração {: #2-edit-the-configuration-file }

Abra `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Adicione o servidor `digna`. Se o arquivo já tiver uma seção `mcpServers`, adicione a entrada
`digna` a ela:

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

!!! warning "Mantenha o Cabeçalho Exatamente como Mostrado"

    Escreva `Authorization:${AUTH_HEADER}` sem espaços e coloque `Bearer <api key>` em `env`.
    O Claude Desktop no Windows não escapa espaços dentro de `args`, então um espaço ali quebra o
    cabeçalho.

### 3. Reiniciar o Claude Desktop {: #3-restart-claude-desktop }

Encerre o Claude Desktop completamente e inicie-o novamente. Em um novo chat, clique em **+** e abra
**Connectors**: `digna` precisa aparecer na lista e estar ativado.

---

## Conector Personalizado {: #custom-connector }

Um conector personalizado disponibiliza o *digna* no claude.ai, no Claude Desktop e nos aplicativos
móveis do Claude sem nenhuma configuração local. É a nuvem da Anthropic que se conecta ao endpoint,
então isso só funciona quando:

- O endpoint do *digna* está acessível pela internet via HTTPS
- A sua organização do Claude tem a opção **Request headers** na caixa de diálogo
  **Add custom connector**. A Anthropic a oferece como beta para um conjunto limitado de
  organizações

!!! warning "Não Serve para o digna Dentro da Sua Rede"

    Os túneis MCP do Claude, que alcançam servidores dentro de uma rede privada, exigem OAuth no
    servidor MCP. O digna MCP Server se autentica com chaves de API, então não é possível usar um
    túnel. Use [Claude Code](#claude-code) ou [Claude Desktop com uma ponte local](#claude-desktop-with-a-local-bridge)
    em vez disso.

### 1. Abrir as Configurações de Conectores {: #1-open-the-connector-settings }

- **Planos Free, Pro, Max e Ultra**: vá para **Customize > Connectors** e clique em
  **Add custom connector**.
- **Planos Team e Enterprise**: um Owner vai para **Organization settings > Connectors**, clica em
  **Add**, depois em **Custom**, e escolhe **Web** se for perguntado o tipo.

### 2. Inserir os Detalhes do Conector {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: escolha `authorization` como nome do cabeçalho, insira `Bearer <api key>`
   como valor, incluindo a palavra `Bearer` e o espaço, e marque-o como **Required**.
4. Clique em **Add**.

!!! warning "Todos Compartilham a Chave"

    Todo membro que usa o conector trabalha com a mesma chave de API e, portanto, com o mesmo
    usuário do *digna*. Crie um usuário do *digna* dedicado ao conector e dê a ele apenas os
    projetos e as funções que todos podem ter, ex.: a função de leitor.

Nos planos Team e Enterprise, os membros então se conectam em **Customize > Connectors**, onde o
conector traz o rótulo **Custom**.

O Claude não permite alterar o cabeçalho de um conector existente. Para usar uma nova chave, remova
o conector e adicione-o novamente.

---

## Resolução de Problemas do Claude {: #troubleshooting-claude }

### claude mcp list Mostra Failed to connect

Execute `claude mcp get digna` para ver o motivo. Um `401` significa que a chave foi rejeitada; veja
[401 Unauthorized](overview.md#troubleshooting). O Claude Code também avisa sobre espaços ou uma
quebra de linha no início ou no fim da chave, que muitas vezes aparecem ao copiá-la.

### O digna Não Aparece no Claude Desktop

- Verifique se o Node.js 18 ou posterior está instalado: `node --version`.
- Verifique se `claude_desktop_config.json` é um JSON válido. Uma vírgula faltando impede que todos
  os servidores do arquivo sejam carregados.
- Encerre o Claude Desktop completamente, não apenas a janela, e inicie-o novamente.

### O Conector Personalizado Não Consegue Alcançar o Servidor

A nuvem da Anthropic não consegue alcançar o endpoint. Verifique se ele está acessível pela internet
via HTTPS com um certificado válido, ou conecte-se pelo [Claude Code](#claude-code).

---

## Veja Também {: #see-also }

- [Visão Geral de Agentes de IA](overview.md): endpoint, chave de API, segurança e resolução de
  problemas geral
- [Gemini](gemini_mcp_guide.md): conectar o Antigravity ou o Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): o que os agentes de IA podem fazer com o
  *digna*
