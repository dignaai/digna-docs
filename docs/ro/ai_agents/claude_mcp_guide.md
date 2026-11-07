---
title: Claude – Conectarea Claude la digna prin MCP | Documentația digna
description: Conectați Claude la digna prin digna MCP Server — Claude Code din linia de comandă sau cu un .mcp.json partajat, Claude Desktop cu o punte locală și conectori personalizați în claude.ai, cu o cheie API în header-ul Authorization.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, conector personalizat claude.ai, digna MCP server, mcp-remote, Authorization Bearer, cheie API digna
---

# Conectați Claude la digna

Acest ghid conectează Claude la **digna MCP Server**. Aveți nevoie de endpoint-ul MCP al instalării
dvs. *digna* și de o cheie API, așa cum este descris în [Prezentarea agenților AI](overview.md).

Exemplele folosesc `https://digna.example.com/mcp` ca endpoint. Înlocuiți-l cu al dvs.

## Alegeți modul de conectare {: #choose-how-to-connect }

| Produs Claude | Se conectează de pe | Funcționează cu *digna* în rețeaua dvs. |
|---|---|---|
| [Claude Code](#claude-code) | Mașina dvs. | Da |
| [Claude Desktop cu o punte locală](#claude-desktop-with-a-local-bridge) | Mașina dvs. | Da |
| [Conector personalizat](#custom-connector) în claude.ai, Claude Desktop și Claude mobil | Cloud-ul Anthropic | Nu. Endpoint-ul trebuie să fie accesibil din internet |

Pentru o instalare *digna* care rulează în rețeaua companiei dvs., folosiți Claude Code sau Claude
Desktop cu o punte locală.

---

## Claude Code {: #claude-code }

### 1. Adăugați serverul {: #1-add-the-server }

Puneți cheia API într-o variabilă de mediu, apoi adăugați serverul:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Shell-ul dvs. completează `$DIGNA_API_KEY` atunci când rulați comanda, astfel încât Claude Code
stochează cheia în propria configurație.

`--scope` decide unde este disponibil serverul:

| Domeniu | Disponibil |
|---|---|
| `local` (implicit) | Pentru dvs., doar în proiectul curent |
| `user` | Pentru dvs., în fiecare proiect |
| `project` | Pentru toți cei care lucrează în proiect, printr-un fișier `.mcp.json` din proiect |

### 2. Partajați serverul cu echipa (opțional) {: #2-share-the-server-with-your-team }

Pentru a oferi tuturor dintr-un proiect același server, adăugați un fișier `.mcp.json` în
rădăcina proiectului. Nu scrieți cheia în fișier. Claude Code completează `${DIGNA_API_KEY}` din
mediul propriu al fiecărei persoane:

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

Fiecare persoană setează `DIGNA_API_KEY` la propria cheie. Prima dată când Claude Code găsește
fișierul, întreabă dacă să folosească serverele din el.

### 3. Verificați conexiunea {: #3-verify-the-connection }

Din shell:

```bash
claude mcp list
```

Serverul `digna` trebuie să afișeze `✔ Connected`. Într-o sesiune Claude Code, rulați `/mcp`
pentru a vedea serverul și instrumentele sale.

---

## Claude Desktop cu o punte locală {: #claude-desktop-with-a-local-bridge }

Fișierul de configurare al Claude Desktop pornește servere MCP locale pe mașina dvs. O punte mică,
pachetul open-source [`mcp-remote`](https://github.com/geelen/mcp-remote), rulează acolo și
redirecționează fiecare cerere către endpoint-ul *digna* cu cheia dvs. API. Deoarece puntea
rulează pe mașina dvs., această metodă funcționează cu *digna* în rețeaua companiei dvs.

!!! note "Un pachet al comunității"

    `mcp-remote` este întreținut de comunitatea sa open-source, nu de Anthropic sau digna.
    Verificați că organizația dvs. permite utilizarea lui înainte de a-l folosi.

### 1. Instalați Node.js {: #1-install-nodejs }

Puntea necesită [Node.js](https://nodejs.org) 18 sau o versiune ulterioară. Claude Desktop
folosește versiunea Node.js instalată pe sistemul dvs. Verificați-o cu:

```bash
node --version
```

### 2. Editați fișierul de configurare {: #2-edit-the-configuration-file }

Deschideți `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Adăugați serverul `digna`. Dacă fișierul are deja o secțiune `mcpServers`, adăugați intrarea
`digna` în ea:

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

!!! warning "Păstrați header-ul exact ca în exemplu"

    Scrieți `Authorization:${AUTH_HEADER}` fără spații și puneți `Bearer <api key>` în `env`.
    Claude Desktop pe Windows nu escapează spațiile din `args`, așa că un spațiu acolo strică
    header-ul.

### 3. Reporniți Claude Desktop {: #3-restart-claude-desktop }

Închideți complet Claude Desktop și porniți-l din nou. Într-un chat nou, faceți clic pe **+** și
deschideți **Connectors**: `digna` trebuie să fie listat și activat.

---

## Conector personalizat {: #custom-connector }

Un conector personalizat (custom connector) face *digna* disponibil în claude.ai, Claude Desktop
și aplicațiile mobile Claude fără nicio configurare locală. Cloud-ul Anthropic se conectează la
endpoint, deci această metodă funcționează doar atunci când:

- Endpoint-ul *digna* este accesibil din internet prin HTTPS
- Organizația dvs. Claude are opțiunea **Request headers** în dialogul **Add custom connector**.
  Anthropic o oferă ca beta unui număr limitat de organizații

!!! warning "Nu pentru digna din rețeaua dvs."

    Tunelurile MCP ale Claude, care ajung la servere dintr-o rețea privată, necesită OAuth pe
    serverul MCP. digna MCP Server se autentifică cu chei API, așa că un tunel nu poate fi folosit.
    Folosiți în schimb [Claude Code](#claude-code) sau
    [Claude Desktop cu o punte locală](#claude-desktop-with-a-local-bridge).

### 1. Deschideți setările conectorilor {: #1-open-the-connector-settings }

- **Planurile Free, Pro, Max și Ultra**: accesați **Customize > Connectors** și faceți clic pe
  **Add custom connector**.
- **Planurile Team și Enterprise**: un Owner accesează **Organization settings > Connectors**, face
  clic pe **Add**, apoi pe **Custom** și alege **Web** dacă i se cere tipul.

### 2. Introduceți detaliile conectorului {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: alegeți `authorization` ca nume de header, introduceți `Bearer <api key>`
   ca valoare, inclusiv cuvântul `Bearer` și spațiul, și marcați-l **Required**.
4. Faceți clic pe **Add**.

!!! warning "Toată lumea partajează cheia"

    Fiecare membru care folosește conectorul lucrează cu aceeași cheie API și, deci, cu același
    utilizator *digna*. Creați un utilizator *digna* dedicat pentru conector și dați-i doar
    proiectele și rolurile pe care le poate avea oricine, de ex. rolul de cititor.

În planurile Team și Enterprise, membrii se conectează apoi din **Customize > Connectors**, unde
conectorul poartă eticheta **Custom**.

Claude nu poate modifica header-ul unui conector existent. Pentru a folosi o cheie nouă, eliminați
conectorul și adăugați-l din nou.

---

## Depanarea Claude {: #troubleshooting-claude }

### claude mcp list afișează Failed to connect

Rulați `claude mcp get digna` pentru a vedea motivul. Un `401` înseamnă că cheia a fost
respinsă; consultați [401 Unauthorized](overview.md#troubleshooting). Claude Code avertizează și
despre spații sau un sfârșit de linie la începutul sau sfârșitul cheii, care apar adesea la
copierea ei.

### digna nu apare în Claude Desktop

- Verificați că este instalat Node.js 18 sau o versiune ulterioară: `node --version`.
- Verificați că `claude_desktop_config.json` este JSON valid. O virgulă lipsă împiedică încărcarea
  tuturor serverelor din fișier.
- Închideți complet Claude Desktop, nu doar fereastra, și porniți-l din nou.

### Conectorul personalizat nu poate ajunge la server

Cloud-ul Anthropic nu poate ajunge la endpoint. Verificați că acesta este accesibil din internet
prin HTTPS cu un certificat valid sau conectați-vă în schimb prin [Claude Code](#claude-code).

---

## Vezi și {: #see-also }

- [Prezentarea agenților AI](overview.md): endpoint, cheie API, securitate și depanare generală
- [Gemini](gemini_mcp_guide.md): conectați Antigravity sau Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): ce pot face agenții AI cu *digna*
