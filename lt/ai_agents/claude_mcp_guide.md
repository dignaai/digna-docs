# Claude prijungimas prie digna

Šiame vadove Claude prijungiamas prie **digna MCP Server**. Jums reikės savo *digna* diegimo MCP
galinio taško ir API rakto, kaip aprašyta [AI agentų apžvalgoje](overview.md).

Pavyzdžiuose galinis taškas yra `https://digna.example.com/mcp`. Pakeiskite jį savuoju.

## Pasirinkite prisijungimo būdą {: #choose-how-to-connect }

| Claude produktas | Jungiasi iš | Veikia su *digna* jūsų tinkle |
|---|---|---|
| [Claude Code](#claude-code) | Jūsų kompiuterio | Taip |
| [Claude Desktop su vietiniu tiltu](#claude-desktop-with-a-local-bridge) | Jūsų kompiuterio | Taip |
| [Custom connector](#custom-connector) claude.ai, Claude Desktop ir Claude mobiliojoje programėlėje | Anthropic debesies | Ne. Galinis taškas turi būti pasiekiamas iš interneto |

Jei *digna* diegimas veikia jūsų įmonės tinkle, naudokite Claude Code arba Claude Desktop su
vietiniu tiltu.

---

## Claude Code {: #claude-code }

### 1. Pridėkite serverį {: #1-add-the-server }

Įrašykite API raktą į aplinkos kintamąjį, tada pridėkite serverį:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Paleidus komandą jūsų shell įrašo `$DIGNA_API_KEY` reikšmę, todėl Claude Code išsaugo raktą savo
konfigūracijoje.

`--scope` nustato, kur serveris pasiekiamas:

| Scope | Pasiekiamas |
|---|---|
| `local` (numatytasis) | Jums, tik dabartiniame projekte |
| `user` | Jums, visuose projektuose |
| `project` | Visiems, kurie dirba projekte, per projekto `.mcp.json` failą |

### 2. Bendrinkite serverį su komanda (neprivaloma) {: #2-share-the-server-with-your-team }

Kad visi projekto dalyviai turėtų tą patį serverį, į projekto šakninį katalogą pridėkite
`.mcp.json` failą. Nerašykite rakto į failą. Claude Code įrašo `${DIGNA_API_KEY}` iš kiekvieno
asmens aplinkos:

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

Kiekvienas asmuo nustato `DIGNA_API_KEY` savo raktu. Pirmą kartą radęs failą, Claude Code paklausia,
ar naudoti jame esančius serverius.

### 3. Patikrinkite ryšį {: #3-verify-the-connection }

Iš savo shell:

```bash
claude mcp list
```

Serveris `digna` turi rodyti `✔ Connected`. Claude Code sesijoje paleiskite `/mcp`, kad
pamatytumėte serverį ir jo įrankius.

---

## Claude Desktop su vietiniu tiltu {: #claude-desktop-with-a-local-bridge }

Claude Desktop konfigūracijos failas paleidžia vietinius MCP serverius jūsų kompiuteryje. Nedidelis
tiltas, atvirojo kodo paketas [`mcp-remote`](https://github.com/geelen/mcp-remote), veikia ten ir
persiunčia kiekvieną užklausą į *digna* galinį tašką su jūsų API raktu. Kadangi tiltas veikia jūsų
kompiuteryje, šis būdas veikia su *digna* jūsų įmonės tinkle.

!!! note "Bendruomenės paketas"

    `mcp-remote` prižiūri jo atvirojo kodo bendruomenė, o ne Anthropic ar digna. Prieš naudodami
    patikrinkite, ar jūsų organizacija jį leidžia.

### 1. Įdiekite Node.js {: #1-install-nodejs }

Tiltui reikia [Node.js](https://nodejs.org) 18 arba naujesnės versijos. Claude Desktop naudoja jūsų
sistemoje įdiegtą Node.js versiją. Patikrinkite ją komanda:

```bash
node --version
```

### 2. Redaguokite konfigūracijos failą {: #2-edit-the-configuration-file }

Atidarykite `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Pridėkite serverį `digna`. Jei faile jau yra `mcpServers` skyrius, pridėkite `digna` įrašą į jį:

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

!!! warning "Antraštę palikite tiksliai tokią, kaip parodyta"

    Rašykite `Authorization:${AUTH_HEADER}` be tarpų, o `Bearer <api key>` įrašykite į `env`.
    Claude Desktop sistemoje Windows neekranuoja tarpų `args` viduje, todėl tarpas ten sugadina
    antraštę.

### 3. Iš naujo paleiskite Claude Desktop {: #3-restart-claude-desktop }

Visiškai uždarykite Claude Desktop ir vėl jį paleiskite. Naujame pokalbyje spauskite **+** ir
atidarykite **Connectors**: `digna` turi būti sąraše ir įjungtas.

---

## Custom connector {: #custom-connector }

Custom connector padaro *digna* pasiekiamą claude.ai, Claude Desktop ir Claude mobiliosiose
programėlėse be jokio vietinio nustatymo. Prie galinio taško jungiasi Anthropic debesis, todėl tai
veikia tik tada, kai:

- *digna* galinis taškas pasiekiamas iš interneto per HTTPS
- Jūsų Claude organizacija turi parinktį **Request headers** dialoge **Add custom connector**.
  Anthropic ją siūlo kaip beta versiją ribotam organizacijų skaičiui

!!! warning "Netinka digna jūsų tinkle"

    Claude MCP tuneliams, kurie pasiekia privačiame tinkle esančius serverius, MCP serveryje reikia
    OAuth. digna MCP Server autentifikuoja API raktais, todėl tunelio naudoti negalima. Vietoj to
    naudokite [Claude Code](#claude-code) arba
    [Claude Desktop su vietiniu tiltu](#claude-desktop-with-a-local-bridge).

### 1. Atidarykite connector nustatymus {: #1-open-the-connector-settings }

- **Free, Pro, Max ir Ultra planai**: eikite į **Customize > Connectors** ir spauskite
  **Add custom connector**.
- **Team ir Enterprise planai**: Owner eina į **Organization settings > Connectors**, spaudžia
  **Add**, tada **Custom** ir, jei klausiama tipo, pasirenka **Web**.

### 2. Įveskite connector duomenis {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: kaip antraštės pavadinimą pasirinkite `authorization`, kaip reikšmę
   įveskite `Bearer <api key>`, įskaitant žodį `Bearer` ir tarpą, ir pažymėkite ją **Required**.
4. Spauskite **Add**.

!!! warning "Visi naudoja tą patį raktą"

    Kiekvienas narys, naudojantis connector, dirba su tuo pačiu API raktu, taigi ir su tuo pačiu
    *digna* vartotoju. Sukurkite connector skirtą atskirą *digna* vartotoją ir suteikite jam tik
    tuos projektus ir roles, kuriuos gali turėti visi, pvz., skaitytojo rolę.

Team ir Enterprise planuose nariai tada prisijungia skiltyje **Customize > Connectors**, kur
connector pažymėtas žyma **Custom**.

Claude negali pakeisti esamo connector antraštės. Norėdami naudoti naują raktą, pašalinkite
connector ir pridėkite jį iš naujo.

---

## Claude trikčių šalinimas {: #troubleshooting-claude }

### claude mcp list rodo Failed to connect

Paleiskite `claude mcp get digna`, kad pamatytumėte priežastį. `401` reiškia, kad raktas buvo
atmestas; žr. [401 Unauthorized](overview.md#troubleshooting). Claude Code taip pat įspėja apie
tarpus ar eilutės lūžį rakto pradžioje arba pabaigoje, kurie dažnai atsiranda jį kopijuojant.

### digna nerodoma Claude Desktop

- Patikrinkite, ar įdiegta Node.js 18 arba naujesnė versija: `node --version`.
- Patikrinkite, ar `claude_desktop_config.json` yra galiojantis JSON. Trūkstamas kablelis neleidžia
  įkelti nė vieno faile esančio serverio.
- Visiškai uždarykite Claude Desktop, o ne tik langą, ir vėl jį paleiskite.

### Custom connector nepasiekia serverio

Anthropic debesis nepasiekia galinio taško. Patikrinkite, ar jis pasiekiamas iš interneto per HTTPS
su galiojančiu sertifikatu, arba vietoj to prisijunkite per [Claude Code](#claude-code).

---

## Taip pat žr. {: #see-also }

- [AI agentų apžvalga](overview.md): galinis taškas, API raktas, saugumas ir bendrasis trikčių šalinimas
- [Gemini](gemini_mcp_guide.md): prijunkite Antigravity arba Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): ką AI agentai gali daryti su *digna*