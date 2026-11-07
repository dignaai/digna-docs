---
title: Claude – Povezava Claude z digna prek MCP | digna Dokumentacija
description: Povežite Claude z digna prek digna MCP Server — Claude Code iz ukazne vrstice ali s skupno datoteko .mcp.json, Claude Desktop z lokalnim mostom in konektorji po meri v claude.ai, s ključem API v glavi Authorization.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, claude.ai konektor po meri, digna MCP server, mcp-remote, Authorization Bearer, digna ključ API
---

# Povežite Claude z digna

Ta vodič poveže Claude z **digna MCP Server**. Potrebujete končno točko MCP svoje namestitve
*digna* in ključ API, kot je opisano v [Pregledu agentov UI](overview.md).

Primeri kot končno točko uporabljajo `https://digna.example.com/mcp`. Zamenjajte jo s svojo.

## Izberite način povezave {: #choose-how-to-connect }

| Izdelek Claude | Poveže se z | Deluje z *digna* znotraj vašega omrežja |
|---|---|---|
| [Claude Code](#claude-code) | Vaš računalnik | Da |
| [Claude Desktop z lokalnim mostom](#claude-desktop-with-a-local-bridge) | Vaš računalnik | Da |
| [Konektor po meri](#custom-connector) v claude.ai, Claude Desktop in Claude za mobilne naprave | Oblak Anthropic | Ne. Končna točka mora biti dosegljiva iz interneta |

Za namestitev *digna*, ki teče znotraj omrežja vašega podjetja, uporabite Claude Code ali Claude
Desktop z lokalnim mostom.

---

## Claude Code {: #claude-code }

### 1. Dodajte strežnik {: #1-add-the-server }

Ključ API shranite v spremenljivko okolja, nato dodajte strežnik:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Lupina ob zagonu ukaza vstavi vrednost `$DIGNA_API_KEY`, zato Claude Code ključ shrani v svojo
konfiguracijo.

`--scope` določa, kje je strežnik na voljo:

| Obseg | Na voljo |
|---|---|
| `local` (privzeto) | Vam, samo v trenutnem projektu |
| `user` | Vam, v vseh projektih |
| `project` | Vsem, ki delajo v projektu, prek datoteke `.mcp.json` v projektu |

### 2. Delite strežnik z ekipo (neobvezno) {: #2-share-the-server-with-your-team }

Če želite vsem v projektu omogočiti isti strežnik, v korensko mapo projekta dodajte datoteko
`.mcp.json`. Ključa ne zapišite v datoteko. Claude Code vrednost `${DIGNA_API_KEY}` vstavi iz
okolja vsake osebe:

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

Vsaka oseba nastavi `DIGNA_API_KEY` na svoj ključ. Ko Claude Code datoteko najde prvič, vpraša,
ali naj uporabi strežnike v njej.

### 3. Preverite povezavo {: #3-verify-the-connection }

V lupini:

```bash
claude mcp list
```

Strežnik `digna` mora prikazati `✔ Connected`. Znotraj seje Claude Code zaženite `/mcp`, da
vidite strežnik in njegova orodja.

---

## Claude Desktop z lokalnim mostom {: #claude-desktop-with-a-local-bridge }

Konfiguracijska datoteka Claude Desktop zaganja lokalne strežnike MCP na vašem računalniku. Majhen
most, odprtokodni paket [`mcp-remote`](https://github.com/geelen/mcp-remote), teče tam in vsako
zahtevo z vašim ključem API posreduje končni točki *digna*. Ker most teče na vašem računalniku, ta
način deluje tudi z *digna* znotraj omrežja vašega podjetja.

!!! note "Paket skupnosti"

    `mcp-remote` vzdržuje njegova odprtokodna skupnost, ne Anthropic ali digna. Pred uporabo
    preverite, ali ga vaša organizacija dovoljuje.

### 1. Namestite Node.js {: #1-install-nodejs }

Most potrebuje [Node.js](https://nodejs.org) 18 ali novejši. Claude Desktop uporablja različico
Node.js, nameščeno v vašem sistemu. Preverite jo z:

```bash
node --version
```

### 2. Uredite konfiguracijsko datoteko {: #2-edit-the-configuration-file }

Odprite `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Dodajte strežnik `digna`. Če datoteka že ima razdelek `mcpServers`, vanj dodajte vnos `digna`:

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

!!! warning "Glavo zapišite točno tako, kot je prikazano"

    `Authorization:${AUTH_HEADER}` zapišite brez presledkov, `Bearer <api key>` pa postavite v
    `env`. Claude Desktop v sistemu Windows presledkov v `args` ne ubeži, zato presledek tam
    pokvari glavo.

### 3. Znova zaženite Claude Desktop {: #3-restart-claude-desktop }

Claude Desktop popolnoma zaprite in ga znova zaženite. V novem klepetu kliknite **+** in odprite
**Connectors**: `digna` mora biti na seznamu in vklopljena.

---

## Konektor po meri {: #custom-connector }

Konektor po meri (custom connector) omogoči *digna* v claude.ai, Claude Desktop in mobilnih
aplikacijah Claude brez kakršne koli lokalne nastavitve. S končno točko se poveže oblak Anthropic,
zato ta način deluje le, če:

- Je končna točka *digna* dosegljiva iz interneta prek HTTPS
- Ima vaša organizacija Claude v pogovornem oknu **Add custom connector** možnost
  **Request headers**. Anthropic jo kot beta ponuja omejenemu številu organizacij

!!! warning "Ni za digna znotraj vašega omrežja"

    Claudovi tuneli MCP, ki dosežejo strežnike v zasebnem omrežju, zahtevajo OAuth na strežniku
    MCP. digna MCP Server se overja s ključi API, zato tunela ni mogoče uporabiti. Namesto tega
    uporabite [Claude Code](#claude-code) ali
    [Claude Desktop z lokalnim mostom](#claude-desktop-with-a-local-bridge).

### 1. Odprite nastavitve konektorjev {: #1-open-the-connector-settings }

- **Paketi Free, Pro, Max in Ultra**: pojdite na **Customize > Connectors** in kliknite
  **Add custom connector**.
- **Paketa Team in Enterprise**: Owner gre na **Organization settings > Connectors**, klikne
  **Add**, nato **Custom** in izbere **Web**, če je vprašan po vrsti.

### 2. Vnesite podatke konektorja {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: za ime glave izberite `authorization`, kot vrednost vnesite
   `Bearer <api key>`, vključno z besedo `Bearer` in presledkom, ter jo označite kot **Required**.
4. Kliknite **Add**.

!!! warning "Vsi si delijo ključ"

    Vsak član, ki uporablja konektor, dela z istim ključem API in torej z istim uporabnikom
    *digna*. Za konektor ustvarite namenskega uporabnika *digna* in mu dodelite le projekte in
    vloge, ki jih sme imeti vsakdo, npr. vlogo bralca.

V paketih Team in Enterprise se člani nato povežejo pod **Customize > Connectors**, kjer ima
konektor oznako **Custom**.

Claude ne more spremeniti glave obstoječega konektorja. Če želite uporabiti nov ključ, konektor
odstranite in ga znova dodajte.

---

## Odpravljanje težav s Claude {: #troubleshooting-claude }

### claude mcp list prikaže Failed to connect

Zaženite `claude mcp get digna`, da vidite razlog. `401` pomeni, da je bil ključ zavrnjen; glejte
[401 Unauthorized](overview.md#troubleshooting). Claude Code opozori tudi na presledke ali prelom
vrstice na začetku ali koncu ključa, ki se pogosto pojavijo pri kopiranju.

### digna se ne prikaže v Claude Desktop

- Preverite, ali je nameščen Node.js 18 ali novejši: `node --version`.
- Preverite, ali je `claude_desktop_config.json` veljaven JSON. Manjkajoča vejica prepreči
  nalaganje vseh strežnikov v datoteki.
- Claude Desktop popolnoma zaprite, ne le okna, in ga znova zaženite.

### Konektor po meri ne doseže strežnika

Oblak Anthropic ne doseže končne točke. Preverite, ali je dosegljiva iz interneta prek HTTPS z
veljavnim potrdilom, ali pa se namesto tega povežite prek [Claude Code](#claude-code).

---

## Povezane vsebine {: #see-also }

- [Pregled agentov UI](overview.md): končna točka, ključ API, varnost in splošno odpravljanje težav
- [Gemini](gemini_mcp_guide.md): povežite Antigravity ali Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): kaj lahko agenti UI počnejo z *digna*
