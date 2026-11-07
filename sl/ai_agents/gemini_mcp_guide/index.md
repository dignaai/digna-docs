# Povežite Gemini z digna

Ta vodič poveže Googlova orodja Gemini z **digna MCP Server**. Potrebujete končno točko MCP svoje
namestitve *digna* in ključ API, kot je opisano v [Pregledu agentov UI](overview.md).

Primeri kot končno točko uporabljajo `https://digna.example.com/mcp`. Zamenjajte jo s svojo.

## Izberite orodje {: #choose-your-tool }

| Orodje | Za koga | Konfiguracija |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE in aplikacija | Googlova orodja za agente. Antigravity CLI je junija 2026 nadomestil Gemini CLI za osebne račune Google | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Licence Gemini Code Assist Standard in Enterprise ter plačljivi ključi Gemini API | `settings.json` ali `gemini mcp add` |
| Aplikacija Gemini Enterprise | — | Ni podprto. Njen konektor MCP po meri se prijavlja z OAuth ali s storitvenim računom Google Cloud, digna MCP Server pa se overja s ključi API |

Vsa ta orodja se povežejo z računalnika, na katerem tečejo, zato delujejo z *digna* znotraj
omrežja vašega podjetja, dokler ta računalnik doseže končno točko.

---

## Antigravity {: #antigravity }

Antigravity svoje strežnike MCP bere iz datoteke `mcp_config.json`, ki si jo delijo CLI, IDE in
aplikacija.

### 1. Odprite mcp_config.json {: #1-open-mcp-config-json }

| Obseg | Datoteka |
|---|---|
| Vsi vaši projekti | `~/.gemini/config/mcp_config.json` |
| En delovni prostor | `.agents/mcp_config.json` v delovnem prostoru |

Za odpiranje datoteke, ki je v uporabi:

- **CLI**: vnesite `/mcp` in pritisnite ++enter++, da odprete upravitelja MCP.
- **IDE**: v stranski plošči agenta odprite meni **…**, izberite **MCP Servers**, nato
  **Manage MCP Servers**, nato **View raw config**.
- **Aplikacija**: pojdite na **Customizations** > **Installed** > **MCP Servers** in uporabite
  **Copy Config File Path**.

### 2. Dodajte strežnik digna {: #2-add-the-digna-server }

Dodajte vnos `digna`. Če datoteka že ima razdelek `mcpServers`, ga dodajte vanj:

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

Antigravity oddaljene strežnike doseže le prek streamable HTTP, ki ga uporablja digna MCP Server.
Končno točko zapišite kot `serverUrl`; ključ `httpUrl` iz Gemini CLI ni podprt.

### 3. Preverite povezavo {: #3-verify-the-connection }

V CLI vnesite `/mcp`: upravitelj MCP prikaže strežnik `digna` z njegovim stanjem in orodji ter
lahko znova naloži konfiguracijo in prikaže dnevnike povezave. V IDE se strežnik prikaže pod
**Manage MCP Servers**.

!!! warning "Zaščitite datoteko"

    `mcp_config.json` hrani ključ API kot navadno besedilo. Datoteko `.agents/mcp_config.json`
    delovnega prostora hranite zunaj nadzora različic, globalno datoteko pa naj lahko bere le vaš
    račun.

---

## Gemini CLI {: #gemini-cli }

### 1. Dodajte strežnik {: #1-add-the-server }

Ključ API shranite v spremenljivko okolja, nato dodajte strežnik:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Lupina ob zagonu ukaza vstavi vrednost `$DIGNA_API_KEY`, zato Gemini CLI ključ shrani v svoje
nastavitve. Brez `--scope user` se strežnik doda le trenutnemu projektu.

### 2. Ali uredite settings.json {: #2-or-edit-settings-json }

Zgornji ukaz piše v `settings.json`. Če želite datoteko urediti sami:

| Obseg | Datoteka |
|---|---|
| Vsi vaši projekti | `~/.gemini/settings.json` |
| En projekt | `.gemini/settings.json` v projektu |

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

Uporabite `httpUrl`, ključ za streamable HTTP. Podoben ključ `url` izbere starejši prenos SSE, ki
ga digna MCP Server ne ponuja. V imenu strežnika ne uporabljajte podčrtajev.

!!! tip "Trust pustite izklopljen"

    Gemini CLI pred vsakim klicem orodja vpraša za potrditev, razen če ima strežnik
    `"trust": true`. Za *digna* pustite `trust` izklopljen, tako da potrdite vsako spremembo, ki
    jo agent naredi v vaši konfiguraciji.

### 3. Preverite povezavo {: #3-verify-the-connection-gemini-cli }

V lupini:

```bash
gemini mcp list
```

Strežnik `digna` mora biti prikazan kot povezan. Znotraj seje Gemini CLI zaženite `/mcp`, da
vidite strežnik in njegova orodja.

---

## Odpravljanje težav z Gemini {: #troubleshooting-gemini }

### Strežnik je prikazan kot nepovezan

- Preverite, ali se končna točka konča z `/mcp` in je dosegljiva z vašega računalnika.
- Preverite ime ključa: `serverUrl` v Antigravity, `httpUrl` v Gemini CLI.
- `401` pomeni, da je bil ključ zavrnjen; glejte [401 Unauthorized](overview.md#troubleshooting).

### Gemini CLI se za moj račun ne zažene več

Od junija 2026 osebni računi Google namesto Gemini CLI uporabljajo Antigravity CLI. Vnos `digna`
premaknite v `mcp_config.json`, kot je opisano pod [Antigravity](#antigravity), in `httpUrl`
preimenujte v `serverUrl`.

---

## Povezane vsebine {: #see-also }

- [Pregled agentov UI](overview.md): končna točka, ključ API, varnost in splošno odpravljanje težav
- [Claude](claude_mcp_guide.md): povežite Claude Code, Claude Desktop ali konektor po meri
- [digna Agentic](../platform/agentic/Introduction.md): kaj lahko agenti UI počnejo z *digna*