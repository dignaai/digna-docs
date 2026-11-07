# Conectar o Gemini ao digna

Este guia conecta as ferramentas Gemini do Google ao **digna MCP Server**. Você precisa do endpoint
MCP da sua instalação do *digna* e de uma chave de API, conforme descrito na
[Visão Geral de Agentes de IA](overview.md).

Os exemplos usam `https://digna.example.com/mcp` como endpoint. Substitua-o pelo seu.

## Escolher a Sua Ferramenta {: #choose-your-tool }

| Ferramenta | Para | Configuração |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE e aplicativo | As ferramentas de agente do Google. O Antigravity CLI substituiu o Gemini CLI para contas Google individuais em junho de 2026 | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Licenças Gemini Code Assist Standard e Enterprise, e chaves pagas da Gemini API | `settings.json` ou `gemini mcp add` |
| Aplicativo Gemini Enterprise | — | Não suportado. O seu conector MCP personalizado faz login com OAuth ou com uma conta de serviço do Google Cloud, enquanto o digna MCP Server se autentica com chaves de API |

Todas essas ferramentas se conectam a partir da máquina em que rodam, então funcionam com o *digna*
dentro da rede da sua empresa, desde que essa máquina consiga alcançar o endpoint.

---

## Antigravity {: #antigravity }

O Antigravity lê os seus servidores MCP de `mcp_config.json`, compartilhado pelo CLI, pelo IDE e pelo
aplicativo.

### 1. Abrir o mcp_config.json {: #1-open-mcp-config-json }

| Escopo | Arquivo |
|---|---|
| Todos os seus projetos | `~/.gemini/config/mcp_config.json` |
| Um workspace | `.agents/mcp_config.json` no workspace |

Para abrir o arquivo em uso:

- **CLI**: digite `/mcp` e pressione ++enter++ para abrir o gerenciador de MCP.
- **IDE**: no painel lateral do agente, abra o menu **…**, selecione **MCP Servers**, depois
  **Manage MCP Servers** e então **View raw config**.
- **Aplicativo**: vá para **Customizations** > **Installed** > **MCP Servers** e use
  **Copy Config File Path**.

### 2. Adicionar o Servidor digna {: #2-add-the-digna-server }

Adicione a entrada `digna`. Se o arquivo já tiver uma seção `mcpServers`, adicione-a ali:

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

O Antigravity alcança servidores remotos apenas via streamable HTTP, que é o que o digna MCP Server
usa. Escreva o endpoint como `serverUrl`; a chave `httpUrl` do Gemini CLI não é suportada.

### 3. Verificar a Conexão {: #3-verify-the-connection }

No CLI, digite `/mcp`: o gerenciador de MCP mostra o servidor `digna` com o seu status e as suas
ferramentas, e pode recarregar a configuração e mostrar os logs de conexão. No IDE, o servidor
aparece em **Manage MCP Servers**.

!!! warning "Proteja o Arquivo"

    O `mcp_config.json` guarda a chave de API em texto simples. Mantenha um `.agents/mcp_config.json`
    de workspace fora do controle de versão e permita que apenas a sua própria conta leia o arquivo
    global.

---

## Gemini CLI {: #gemini-cli }

### 1. Adicionar o Servidor {: #1-add-the-server }

Coloque a chave de API em uma variável de ambiente e depois adicione o servidor:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

O seu shell substitui `$DIGNA_API_KEY` quando você executa o comando, então o Gemini CLI armazena a
chave nas suas configurações. Sem `--scope user`, o servidor é adicionado apenas ao projeto atual.

### 2. Ou Editar o settings.json {: #2-or-edit-settings-json }

O comando acima grava em `settings.json`. Para editar o arquivo você mesmo:

| Escopo | Arquivo |
|---|---|
| Todos os seus projetos | `~/.gemini/settings.json` |
| Um projeto | `.gemini/settings.json` no projeto |

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

Use `httpUrl`, a chave para streamable HTTP. A chave parecida `url` seleciona o transporte SSE mais
antigo, que o digna MCP Server não oferece. Não use sublinhados no nome do servidor.

!!! tip "Deixe o Trust Desativado"

    O Gemini CLI pergunta antes de cada chamada de ferramenta, a menos que o servidor tenha
    `"trust": true`. Deixe `trust` desativado para o *digna*, para que você confirme cada alteração
    que um agente fizer na sua configuração.

### 3. Verificar a Conexão {: #3-verify-the-connection-gemini-cli }

No seu shell:

```bash
gemini mcp list
```

O servidor `digna` precisa aparecer como conectado. Dentro de uma sessão do Gemini CLI, execute
`/mcp` para ver o servidor e as suas ferramentas.

---

## Resolução de Problemas do Gemini {: #troubleshooting-gemini }

### O Servidor Aparece como Desconectado

- Verifique se o endpoint termina em `/mcp` e está acessível a partir da sua máquina.
- Verifique o nome da chave: `serverUrl` no Antigravity, `httpUrl` no Gemini CLI.
- Um `401` significa que a chave foi rejeitada; veja [401 Unauthorized](overview.md#troubleshooting).

### O Gemini CLI Não Inicia Mais para a Minha Conta

Desde junho de 2026, as contas Google individuais usam o Antigravity CLI em vez do Gemini CLI. Mova a
entrada `digna` para `mcp_config.json` conforme descrito em [Antigravity](#antigravity) e renomeie
`httpUrl` para `serverUrl`.

---

## Veja Também {: #see-also }

- [Visão Geral de Agentes de IA](overview.md): endpoint, chave de API, segurança e resolução de
  problemas geral
- [Claude](claude_mcp_guide.md): conectar o Claude Code, o Claude Desktop ou um conector
  personalizado
- [digna Agentic](../platform/agentic/Introduction.md): o que os agentes de IA podem fazer com o
  *digna*