---
title: Agenti UI – Pregled integracije MCP | digna Dokumentacija
description: Povežite Claude, Gemini in druge agente UI z digna prek digna MCP Server. Poiščite končno točko MCP, ustvarite ključ API, preverite licenco in omrežne zahteve ter izberite vodič za svoj odjemalec UI.
image: /assets/logo_square.png
keywords: digna MCP server, Model Context Protocol, povezava AI agenta, agent UI, Claude MCP, Gemini MCP, Antigravity MCP, digna ključ API, digna Agentic
---

# Povežite agente UI z digna

**digna MCP Server** agentom umetne inteligence (UI) omogoča delo z *digna* prek
[Model Context Protocol](https://modelcontextprotocol.io) (MCP), odprtega standarda, ki ga
podpirajo Claude, Gemini in številna druga orodja UI. Agent, povezan z *digna*, lahko odgovarja na
vprašanja o vaših podatkih, raziskuje opozorila in pomaga pri konfiguraciji *digna*. Kaj zmorejo
agenti, si oglejte v [digna Agentic](../platform/agentic/Introduction.md).

Ta stran opisuje stran *digna*, ki je enaka za vse odjemalce UI. Vodiči za odjemalce nato
pokažejo, kam vnesete končno točko in ključ:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop in konektorji po meri
- [Gemini](gemini_mcp_guide.md): Antigravity in Gemini CLI

!!! info "Beta"

    digna Agentic in z njim digna MCP Server sta na voljo kot različica beta v
    [Release 2026.11](../changelog/Release_202611.md).

---

## Preden začnete {: #before-you-start }

Potrebujete:

- *digna* Release 2026.11 ali novejšo različico
- Licenco, ki vključuje **digna Agentic**. Brez nje strežnik MCP zavrne vsako zahtevo
- Uporabniški račun *digna*. Agent v vsakem projektu deluje s pravicami tega uporabnika, glejte
  [Pravice](../platform/agentic/how_it_works.md#permissions)
- Odjemalec UI, ki se z oddaljenimi strežniki MCP povezuje prek **streamable HTTP** in lahko
  pošlje glavo `Authorization`

---

## 1. Poiščite končno točko MCP {: #1-find-the-mcp-endpoint }

Strežnik MCP je del zaledja *digna*, zato ni treba ničesar dodatno namestiti ali zagnati. Njegova
končna točka je naslov zaledja, ki mu sledi `/mcp`:

```text
https://digna.example.com/mcp
```

Če zaledje teče neposredno na gostitelju in vratih, na primer po
`digna serve --address 0.0.0.0 --port 8082`, je končna točka ta naslov z `/mcp`:

```text
http://digna-host:8082/mcp
```

Če je pred zaledjem obratni posrednik (reverse proxy), mora ta posredovati `/mcp` zaledju skupaj z
glavo `Authorization`.

!!! warning "V omrežju uporabljajte HTTPS"

    Vsaka zahteva vsebuje ključ API. HTTPS uporabljajte vedno, kadar odjemalec UI in *digna* nista
    na istem računalniku.

### Od kod prihaja povezava {: #where-the-connection-comes-from }

Večina odjemalcev UI se poveže z računalnika, na katerem teče: Claude Code, Claude Desktop z
lokalnim mostom, Antigravity in Gemini CLI. Zanje mora biti *digna* dosegljiva le s tega
računalnika, na primer znotraj omrežja vašega podjetja.

Claudovi **konektorji po meri** (custom connectors) so drugačni: s končno točko se poveže oblak
Anthropic. Delujejo le, če je končna točka dosegljiva iz interneta prek HTTPS. Za namestitev
*digna*, ki je dosegljiva le znotraj vašega omrežja, uporabite odjemalec, ki teče na vašem
računalniku.

---

## 2. Ustvarite ključ API {: #2-create-an-api-key }

Odjemalec UI se overi s ključem API uporabnika *digna*.

1. Prijavite se v *digna*.
2. Odprite svoj uporabniški profil v spodnjem levem kotu.
3. Kliknite **API Keys**, nato **Add API Key**.
4. Vnesite ime, ki pove, čemu je ključ namenjen, npr. *Claude Code – Marcin*, in izberite, kdaj
   poteče.
5. Kopirajte ključ. Prikazan je le enkrat.

Vsaka zahteva strežniku MCP pošlje ključ v tej glavi:

```text
Authorization: Bearer <api key>
```

Beseda `Bearer` in presledek za njo sta del vrednosti glave.

---

## 3. Povežite svoj odjemalec UI {: #3-connect-your-ai-client }

| Odjemalec UI | Poveže se z | Vodič |
|---|---|---|
| Claude Code | Vaš računalnik | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop z lokalnim mostom | Vaš računalnik | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Konektor po meri za Claude (claude.ai, Claude Desktop, Claude za mobilne naprave) | Oblak Anthropic | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE in aplikacija | Vaš računalnik | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Vaš računalnik | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Delujejo tudi drugi odjemalci MCP, če podpirajo oddaljene strežnike prek streamable HTTP z glavo
po meri. Večina jih bere konfiguracijo, kot je ta. Točna imena datoteke in ključev poiščite v
dokumentaciji svojega odjemalca:

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

## 4. Preizkusite {: #4-try-it }

Agenta vprašajte nekaj, na kar lahko odgovori le *digna*:

- *»Izpiši moje projekte digna.«*
- *»Kateri podatkovni viri v projektu X danes niso zeleni?«*
- *»Pojasni zadnje neuspešno preverjanje podatkovnega vira Y.«*

Če agent izpiše vaše projekte, povezava deluje.

---

## Varnost {: #security }

- **En ključ na osebo in odjemalec.** Tako lahko posamezen ključ prekličete z **Delete API Key**,
  ne da bi to vplivalo na koga drugega.
- **Uporabnika izberite premišljeno.** Agent lahko naredi vse, kar lahko naredi uporabnik ključa.
  Samo za raziskovanje podatkov uporabite uporabnika z vlogo bralca v projektih.
- **Ključev ne hranite v skupnih datotekah.** Ne potrjujte (commit) konfiguracijske datoteke, ki
  vsebuje ključ. Kjer odjemalec to podpira, ključ preberite iz spremenljivke okolja.
- **Nastavite rok veljavnosti.** Pred potekom starega ključa ustvarite novega in posodobite
  odjemalec.
- **Preglejte klice orodij.** Potrjevanje klicev orodij v odjemalcu pustite vklopljeno, vsaj za
  klice, ki spreminjajo konfiguracijo.

---

## Odpravljanje težav {: #troubleshooting }

### 401 Unauthorized

Odgovor pove razlog:

| Sporočilo | Vzrok |
|---|---|
| `Missing or malformed Authorization header` | Glava ni bila poslana ali se vrednost ne začne z `Bearer ` |
| `Invalid API key` | Ključ je napačen ali je bil izbrisan |
| `API key expired` | Ključ je potekel. Ustvarite novega |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

Licenca *digna* nima vnosa digna Agentic ali pa je ta vnos potekel. Pri ekipi digna zaprosite za
licenco, ki vključuje digna Agentic, in jo namestite, kot je opisano v namestitvenem vodiču za vaš
operacijski sistem.

### Vsaka zahteva ne uspe z napako neveljavne licence

Potekla je sama licenca *digna*. Strežnik MCP skupaj z nadzorno ploščo preneha odgovarjati, dokler
ni nameščena nova licenca.

### Agent lahko bere, ne more pa spreminjati konfiguracije

Uporabnik, ki mu pripada ključ API, v tem projektu nima vloge urejevalca. Uporabite ključ
uporabnika z vlogo urejevalca ali prosite skrbnika projekta, da spremeni vlogo.

### Odjemalec se sploh ne more povezati

Računalnik, ki se povezuje, ne doseže končne točke. Odprite naslov končne točke s tega računalnika
ter preverite požarne zidove, posredniške strežnike in potrdilo. Pri konektorju po meri za Claude
je ta računalnik v oblaku Anthropic, glejte [Od kod prihaja povezava](#where-the-connection-comes-from).
