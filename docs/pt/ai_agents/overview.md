---
title: Agentes de IA – Visão Geral da Integração MCP | Documentação digna
description: Conecte Claude, Gemini e outros agentes de IA ao digna por meio do digna MCP Server. Encontre o endpoint MCP, crie uma chave de API, verifique os requisitos de licença e de rede e escolha o guia para o seu cliente de IA.
image: /assets/logo_square.png
keywords: digna MCP server, Model Context Protocol, conectar agente de IA, Claude MCP, Gemini MCP, Antigravity MCP, chave de API do digna, digna Agentic
---

# Conectar Agentes de IA ao digna

O **digna MCP Server** permite que agentes de IA trabalhem com o *digna* por meio do
[Model Context Protocol](https://modelcontextprotocol.io) (MCP), um padrão aberto suportado por
Claude, Gemini e muitas outras ferramentas de IA. Um agente conectado ao *digna* pode responder a
perguntas sobre os seus dados, investigar alertas e ajudar a configurar o *digna*. Veja
[digna Agentic](../platform/agentic/Introduction.md) para saber o que os agentes podem fazer.

Esta página cobre o lado do *digna*, que é o mesmo para todos os clientes de IA. Os guias de cada
cliente mostram onde inserir essas informações:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop e conectores personalizados
- [Gemini](gemini_mcp_guide.md): Antigravity e Gemini CLI

!!! info "Beta"

    O digna Agentic, e com ele o digna MCP Server, é entregue como versão beta na
    [Release 2026.11](../changelog/Release_202611.md).

---

## Antes de Começar {: #before-you-start }

Você precisa de:

- *digna* Release 2026.11 ou posterior
- Uma licença que inclua o **digna Agentic**. Sem ela, o servidor MCP recusa todas as requisições
- Uma conta de usuário do *digna*. O agente atua com as permissões desse usuário em cada projeto,
  veja [Permissões](../platform/agentic/how_it_works.md#permissions)
- Um cliente de IA que se conecte a servidores MCP remotos via **streamable HTTP** e consiga enviar
  um cabeçalho `Authorization`

---

## 1. Encontrar o Endpoint MCP {: #1-find-the-mcp-endpoint }

O servidor MCP faz parte do backend do *digna*, portanto não há nada extra para instalar ou
iniciar. O endpoint é o endereço do backend seguido de `/mcp`:

```text
https://digna.example.com/mcp
```

Se o backend roda diretamente em um host e uma porta, por exemplo depois de
`digna serve --address 0.0.0.0 --port 8082`, o endpoint é esse endereço com `/mcp`:

```text
http://digna-host:8082/mcp
```

Se houver um proxy reverso na frente do backend, ele precisa encaminhar `/mcp` para o backend junto
com o cabeçalho `Authorization`.

!!! warning "Use HTTPS em Rede"

    Toda requisição carrega uma chave de API. Use HTTPS sempre que o cliente de IA e o *digna* não
    estiverem na mesma máquina.

### De Onde Vem a Conexão {: #where-the-connection-comes-from }

A maioria dos clientes de IA se conecta a partir da máquina em que roda: Claude Code, Claude Desktop
com uma ponte local, Antigravity e Gemini CLI. Para eles, o *digna* só precisa estar acessível a
partir dessa máquina, por exemplo dentro da rede da sua empresa.

Os **conectores personalizados** do Claude são diferentes: é a nuvem da Anthropic que se conecta ao
endpoint. Eles só funcionam quando o endpoint está acessível pela internet via HTTPS. Para uma
instalação do *digna* acessível apenas dentro da sua rede, use um cliente que rode na sua máquina.

---

## 2. Criar uma Chave de API {: #2-create-an-api-key }

Um cliente de IA se autentica com a chave de API de um usuário do *digna*.

1. Faça login no *digna*.
2. Abra o seu perfil de usuário no canto inferior esquerdo.
3. Clique em **API Keys** e depois em **Add API Key**.
4. Insira um nome que diga para que serve a chave, ex.: *Claude Code – Marcin*, e escolha quando
   ela expira.
5. Copie a chave. Ela é exibida apenas uma vez.

Toda requisição ao servidor MCP envia a chave neste cabeçalho:

```text
Authorization: Bearer <api key>
```

A palavra `Bearer` e o espaço depois dela fazem parte do valor do cabeçalho.

---

## 3. Conectar o Seu Cliente de IA {: #3-connect-your-ai-client }

| Cliente de IA | Conecta-se a partir de | Guia |
|---|---|---|
| Claude Code | Sua máquina | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop com uma ponte local | Sua máquina | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Conector personalizado do Claude (claude.ai, Claude Desktop, Claude mobile) | Nuvem da Anthropic | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE e aplicativo | Sua máquina | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Sua máquina | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Outros clientes MCP também funcionam se suportarem servidores remotos via streamable HTTP com um
cabeçalho personalizado. A maioria deles lê uma configuração como esta. Consulte a documentação do
seu cliente para saber os nomes exatos do arquivo e das chaves:

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

## 4. Experimentar {: #4-try-it }

Pergunte ao agente algo que só o *digna* pode responder:

- *"Liste os meus projetos no digna."*
- *"Quais fontes de dados no projeto X não estão verdes hoje?"*
- *"Explique a última verificação com falha da fonte de dados Y."*

Se o agente listar os seus projetos, a conexão funciona.

---

## Segurança {: #security }

- **Uma chave por pessoa e por cliente.** Assim você pode revogar uma única chave, com
  **Delete API Key**, sem afetar mais ninguém.
- **Escolha o usuário com cuidado.** O agente pode fazer tudo o que o usuário da chave pode fazer.
  Apenas para investigar dados, use um usuário com a função de leitor nos projetos.
- **Mantenha as chaves fora de arquivos compartilhados.** Não faça commit de um arquivo de
  configuração que contenha uma chave. Quando o cliente suportar, leia a chave de uma variável de
  ambiente.
- **Defina uma data de expiração.** Crie uma nova chave antes que a antiga expire e atualize o
  cliente.
- **Revise as chamadas de ferramentas.** Mantenha ativada a confirmação de chamadas de ferramentas
  do cliente, pelo menos para chamadas que alteram a configuração.

---

## Resolução de Problemas {: #troubleshooting }

### 401 Unauthorized

A resposta informa o motivo:

| Mensagem | Causa |
|---|---|
| `Missing or malformed Authorization header` | Nenhum cabeçalho foi enviado, ou o valor não começa com `Bearer ` |
| `Invalid API key` | A chave está errada ou foi excluída |
| `API key expired` | A chave expirou. Crie uma nova |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

A licença do *digna* não tem uma entrada digna Agentic, ou essa entrada expirou. Peça à equipe do
digna uma licença que inclua o digna Agentic e instale-a conforme descrito no guia de instalação do
seu sistema operacional.

### Toda Requisição Falha com um Erro de Licença Inválida

A própria licença do *digna* expirou. O servidor MCP para de responder junto com o dashboard até que
uma nova licença seja instalada.

### O Agente Consegue Ler, mas Não Alterar a Configuração

O usuário por trás da chave de API não tem a função de editor nesse projeto. Use a chave de
um usuário com a função de editor, ou peça a um administrador do projeto que altere a função.

### O Cliente Não Consegue Se Conectar

A máquina que se conecta não consegue alcançar o endpoint. Abra o endereço do endpoint a partir
dessa máquina e verifique firewalls, proxies e o certificado. No caso de um conector personalizado
do Claude, essa máquina está na nuvem da Anthropic, veja
[De Onde Vem a Conexão](#where-the-connection-comes-from).
