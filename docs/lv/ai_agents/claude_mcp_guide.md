---
title: Claude — Claude savienošana ar digna, izmantojot MCP | digna dokumentācija
description: Savienojiet Claude ar digna, izmantojot digna MCP Server — Claude Code no komandrindas vai ar koplietotu .mcp.json, Claude Desktop ar lokālu tiltu un pielāgotie savienotāji claude.ai, ar API atslēgu galvenē Authorization.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, claude.ai pielāgotais savienotājs, digna MCP server, mcp-remote, Authorization Bearer, digna API atslēga
---

# Claude savienošana ar digna

Šajā rokasgrāmatā Claude tiek savienots ar **digna MCP Server**. Jums nepieciešams jūsu *digna*
instalācijas MCP galapunkts un API atslēga, kā aprakstīts [AI aģentu pārskatā](overview.md).

Piemēros kā galapunkts izmantots `https://digna.example.com/mcp`. Aizstājiet to ar savu.

## Savienojuma veida izvēle {: #choose-how-to-connect }

| Claude produkts | Savienojas no | Darbojas ar *digna* jūsu tīklā |
|---|---|---|
| [Claude Code](#claude-code) | Jūsu datora | Jā |
| [Claude Desktop ar lokālu tiltu](#claude-desktop-with-a-local-bridge) | Jūsu datora | Jā |
| [Pielāgotais savienotājs](#custom-connector) claude.ai, Claude Desktop un Claude mobile | Anthropic mākoņa | Nē. Galapunktam jābūt sasniedzamam no interneta |

*digna* instalācijai, kas darbojas jūsu uzņēmuma tīklā, izmantojiet Claude Code vai Claude Desktop
ar lokālu tiltu.

---

## Claude Code {: #claude-code }

### 1. Servera pievienošana {: #1-add-the-server }

Ievietojiet API atslēgu vides mainīgajā un pēc tam pievienojiet serveri:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Jūsu čaula (shell) aizpilda `$DIGNA_API_KEY`, kad izpildāt komandu, tāpēc Claude Code saglabā
atslēgu savā konfigurācijā.

`--scope` nosaka, kur serveris ir pieejams:

| Scope | Pieejams |
|---|---|
| `local` (noklusējums) | Jums, tikai pašreizējā projektā |
| `user` | Jums, katrā projektā |
| `project` | Ikvienam, kas strādā projektā, izmantojot `.mcp.json` failu projektā |

### 2. Servera kopīgošana ar komandu (neobligāti) {: #2-share-the-server-with-your-team }

Lai visiem projekta dalībniekiem būtu tas pats serveris, pievienojiet `.mcp.json` failu projekta
saknes direktorijā. Neierakstiet atslēgu failā. Claude Code aizpilda `${DIGNA_API_KEY}` no katras
personas paša vides:

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

Katra persona iestata `DIGNA_API_KEY` uz savu atslēgu. Pirmo reizi atrodot failu, Claude Code
jautā, vai izmantot tajā norādītos serverus.

### 3. Savienojuma pārbaude {: #3-verify-the-connection }

No čaulas:

```bash
claude mcp list
```

Serverim `digna` jārāda `✔ Connected`. Claude Code sesijā izpildiet `/mcp`, lai redzētu serveri un
tā rīkus.

---

## Claude Desktop ar lokālu tiltu {: #claude-desktop-with-a-local-bridge }

Claude Desktop konfigurācijas fails palaiž lokālus MCP serverus jūsu datorā. Neliels tilts — atvērtā
koda pakotne [`mcp-remote`](https://github.com/geelen/mcp-remote) — darbojas tur un pārsūta katru
pieprasījumu uz *digna* galapunktu ar jūsu API atslēgu. Tā kā tilts darbojas jūsu datorā, šis
risinājums darbojas ar *digna* jūsu uzņēmuma tīklā.

!!! note "Kopienas pakotne"

    `mcp-remote` uztur tās atvērtā koda kopiena, nevis Anthropic vai digna. Pirms to izmantojat,
    pārbaudiet, vai jūsu organizācija to atļauj.

### 1. Node.js instalēšana {: #1-install-nodejs }

Tiltam nepieciešams [Node.js](https://nodejs.org) 18 vai jaunāka versija. Claude Desktop izmanto
jūsu sistēmā instalēto Node.js versiju. Pārbaudiet to ar:

```bash
node --version
```

### 2. Konfigurācijas faila rediģēšana {: #2-edit-the-configuration-file }

Atveriet `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Pievienojiet serveri `digna`. Ja failā jau ir sadaļa `mcpServers`, pievienojiet ierakstu `digna`
tajā:

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

!!! warning "Saglabājiet galveni tieši tādu, kā parādīts"

    Rakstiet `Authorization:${AUTH_HEADER}` bez atstarpēm un ievietojiet `Bearer <api key>`
    sadaļā `env`. Claude Desktop operētājsistēmā Windows neaizsargā (escape) atstarpes `args`
    iekšienē, tāpēc atstarpe tur sabojā galveni.

### 3. Claude Desktop restartēšana {: #3-restart-claude-desktop }

Pilnībā aizveriet Claude Desktop un palaidiet to vēlreiz. Jaunā tērzēšanā noklikšķiniet uz **+** un
atveriet **Connectors**: `digna` jābūt sarakstā un ieslēgtam.

---

## Pielāgotais savienotājs {: #custom-connector }

Pielāgotais savienotājs padara *digna* pieejamu claude.ai, Claude Desktop un Claude mobilajās
lietotnēs bez jebkādas lokālas iestatīšanas. Ar galapunktu savienojas Anthropic mākonis, tāpēc tas
darbojas tikai tad, ja:

- *digna* galapunkts ir sasniedzams no interneta, izmantojot HTTPS
- Jūsu Claude organizācijai dialoglodziņā **Add custom connector** ir opcija **Request headers**.
  Anthropic to piedāvā kā beta versiju ierobežotam organizāciju lokam

!!! warning "Nav paredzēts digna jūsu tīklā"

    Claude MCP tuneļiem, kas sasniedz serverus privātā tīklā, MCP serverī nepieciešams OAuth.
    digna MCP Server autentificē ar API atslēgām, tāpēc tuneli izmantot nevar. Tā vietā izmantojiet
    [Claude Code](#claude-code) vai [Claude Desktop ar lokālu tiltu](#claude-desktop-with-a-local-bridge).

### 1. Savienotāju iestatījumu atvēršana {: #1-open-the-connector-settings }

- **Free, Pro, Max un Ultra plāni**: dodieties uz **Customize > Connectors** un noklikšķiniet
  **Add custom connector**.
- **Team un Enterprise plāni**: Owner dodas uz **Organization settings > Connectors**, noklikšķina
  **Add**, pēc tam **Custom** un, ja tiek jautāts par tipu, izvēlas **Web**.

### 2. Savienotāja datu ievadīšana {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: kā galvenes nosaukumu izvēlieties `authorization`, kā vērtību ievadiet
   `Bearer <api key>`, ieskaitot vārdu `Bearer` un atstarpi, un atzīmējiet to kā **Required**.
4. Noklikšķiniet **Add**.

!!! warning "Visi koplieto atslēgu"

    Katrs dalībnieks, kas izmanto savienotāju, strādā ar to pašu API atslēgu un līdz ar to ar to
    pašu *digna* lietotāju. Izveidojiet savienotājam atsevišķu *digna* lietotāju un piešķiriet tam
    tikai tos projektus un lomas, kas drīkst būt ikvienam, piem., reader lomu.

Team un Enterprise plānos dalībnieki pēc tam pievienojas sadaļā **Customize > Connectors**, kur
savienotājam ir etiķete **Custom**.

Claude nevar mainīt esoša savienotāja galveni. Lai izmantotu jaunu atslēgu, noņemiet savienotāju un
pievienojiet to vēlreiz.

---

## Claude problēmu novēršana {: #troubleshooting-claude }

### claude mcp list rāda Failed to connect

Izpildiet `claude mcp get digna`, lai redzētu iemeslu. `401` nozīmē, ka atslēga tika noraidīta;
skatiet [401 Unauthorized](overview.md#troubleshooting). Claude Code arī brīdina par atstarpēm vai
rindas pārnesumu atslēgas sākumā vai beigās, kas bieži rodas, to kopējot.

### digna neparādās Claude Desktop

- Pārbaudiet, vai ir instalēts Node.js 18 vai jaunāka versija: `node --version`.
- Pārbaudiet, vai `claude_desktop_config.json` ir derīgs JSON. Trūkstošs komats neļauj ielādēt
  nevienu failā norādīto serveri.
- Pilnībā aizveriet Claude Desktop, ne tikai logu, un palaidiet to vēlreiz.

### Pielāgotais savienotājs nevar sasniegt serveri

Anthropic mākonis nevar sasniegt galapunktu. Pārbaudiet, vai tas ir sasniedzams no interneta,
izmantojot HTTPS ar derīgu sertifikātu, vai tā vietā savienojieties, izmantojot
[Claude Code](#claude-code).

---

## Skatīt arī {: #see-also }

- [AI aģentu pārskats](overview.md): galapunkts, API atslēga, drošība un vispārīga problēmu novēršana
- [Gemini](gemini_mcp_guide.md): Antigravity vai Gemini CLI savienošana
- [digna Agentic](../platform/agentic/Introduction.md): ko AI aģenti var paveikt ar *digna*
