# AI agentų prijungimas prie digna

**digna MCP Server** leidžia AI agentams dirbti su *digna* per
[Model Context Protocol](https://modelcontextprotocol.io) (MCP) – atvirą standartą, kurį palaiko
Claude, Gemini ir daugelis kitų AI įrankių. Prie *digna* prijungtas agentas gali atsakyti į
klausimus apie jūsų duomenis, tirti įspėjimus ir padėti konfigūruoti *digna*. Ką agentai gali
daryti, žr. [digna Agentic](../platform/agentic/Introduction.md).

Šiame puslapyje aprašoma *digna* pusė, kuri yra vienoda visiems AI klientams. Klientų vadovuose
parodyta, kur šiuos duomenis įvesti:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop ir custom connector
- [Gemini](gemini_mcp_guide.md): Antigravity ir Gemini CLI

!!! info "Beta"

    digna Agentic, o kartu ir digna MCP Server, pateikiami kaip beta versija
    [Release 2026.11](../changelog/Release_202611.md).

---

## Prieš pradedant {: #before-you-start }

Jums reikia:

- *digna* Release 2026.11 arba naujesnės versijos
- Licencijos, kuri apima **digna Agentic**. Be jos MCP serveris atmeta kiekvieną užklausą
- *digna* vartotojo paskyros. Agentas kiekviename projekte veikia su šio vartotojo teisėmis, žr.
  [Teisės](../platform/agentic/how_it_works.md#permissions)
- AI kliento, kuris jungiasi prie nuotolinių MCP serverių per **streamable HTTP** ir gali siųsti
  `Authorization` antraštę

---

## 1. Raskite MCP galinį tašką {: #1-find-the-mcp-endpoint }

MCP serveris yra *digna* backend'o dalis, todėl nieko papildomai diegti ar paleisti nereikia. Jo
galinis taškas yra backend'o adresas, po kurio eina `/mcp`:

```text
https://digna.example.com/mcp
```

Jei backend'as veikia tiesiogiai serveryje ir prievade, pavyzdžiui, paleistas komanda
`digna serve --address 0.0.0.0 --port 8082`, galinis taškas yra tas adresas su `/mcp`:

```text
http://digna-host:8082/mcp
```

Jei priešais backend'ą yra atvirkštinis tarpinis serveris (reverse proxy), jis turi persiųsti `/mcp`
į backend'ą kartu su `Authorization` antrašte.

!!! warning "Tinkle naudokite HTTPS"

    Kiekvienoje užklausoje yra API raktas. Naudokite HTTPS visada, kai AI klientas ir *digna*
    veikia ne tame pačiame kompiuteryje.

### Iš kur ateina ryšys {: #where-the-connection-comes-from }

Dauguma AI klientų jungiasi iš kompiuterio, kuriame jie veikia: Claude Code, Claude Desktop su
vietiniu tiltu, Antigravity ir Gemini CLI. Jiems *digna* turi būti pasiekiama tik iš to kompiuterio,
pavyzdžiui, jūsų įmonės tinkle.

Claude **custom connector** veikia kitaip: prie galinio taško jungiasi Anthropic debesis. Jie
veikia tik tada, kai galinis taškas pasiekiamas iš interneto per HTTPS. Jei *digna* diegimas
pasiekiamas tik jūsų tinkle, naudokite klientą, kuris veikia jūsų kompiuteryje.

---

## 2. Sukurkite API raktą {: #2-create-an-api-key }

AI klientas autentifikuojasi *digna* vartotojo API raktu.

1. Prisijunkite prie *digna*.
2. Apatiniame kairiajame kampe atidarykite savo vartotojo profilį.
3. Spauskite **API Keys**, tada **Add API Key**.
4. Įveskite pavadinimą, nurodantį, kam skirtas raktas, pvz., *Claude Code – Marcin*, ir pasirinkite,
   kada jo galiojimas baigiasi.
5. Nukopijuokite raktą. Jis rodomas tik vieną kartą.

Kiekviena užklausa MCP serveriui siunčia raktą šioje antraštėje:

```text
Authorization: Bearer <api key>
```

Žodis `Bearer` ir po jo einantis tarpas yra antraštės reikšmės dalis.

---

## 3. Prijunkite savo AI klientą {: #3-connect-your-ai-client }

| AI klientas | Jungiasi iš | Vadovas |
|---|---|---|
| Claude Code | Jūsų kompiuterio | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop su vietiniu tiltu | Jūsų kompiuterio | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Claude custom connector (claude.ai, Claude Desktop, Claude mobilioji programėlė) | Anthropic debesies | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE ir programa | Jūsų kompiuterio | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Jūsų kompiuterio | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Kiti MCP klientai taip pat veikia, jei palaiko nuotolinius serverius per streamable HTTP su
pasirinktine antrašte. Dauguma jų skaito tokią konfigūraciją. Tikslius failų ir raktų pavadinimus
rasite savo kliento dokumentacijoje:

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

## 4. Išbandykite {: #4-try-it }

Paklauskite agento ko nors, į ką gali atsakyti tik *digna*:

- *„Išvardyk mano digna projektus.“*
- *„Kurie projekto X duomenų šaltiniai šiandien nėra žali?“*
- *„Paaiškink paskutinį nepavykusį duomenų šaltinio Y patikrinimą.“*

Jei agentas išvardija jūsų projektus, ryšys veikia.

---

## Saugumas {: #security }

- **Vienas raktas kiekvienam asmeniui ir klientui.** Tada galėsite atšaukti vieną raktą su
  **Delete API Key**, nepaveikdami nieko kito.
- **Vartotoją rinkitės apgalvotai.** Agentas gali daryti viską, ką gali rakto vartotojas. Jei
  reikia tik tirti duomenis, naudokite vartotoją, kuris projektuose turi skaitytojo rolę.
- **Nelaikykite raktų bendrinamuose failuose.** Nekomituokite konfigūracijos failo, kuriame yra
  raktas. Jei klientas tai palaiko, skaitykite raktą iš aplinkos kintamojo.
- **Nustatykite galiojimo pabaigą.** Sukurkite naują raktą prieš baigiantis senojo galiojimui ir
  atnaujinkite klientą.
- **Peržiūrėkite įrankių iškvietimus.** Palikite įjungtą kliento įrankių iškvietimų patvirtinimą,
  bent jau iškvietimams, kurie keičia konfigūraciją.

---

## Trikčių šalinimas {: #troubleshooting }

### 401 Unauthorized

Atsakyme nurodyta priežastis:

| Pranešimas | Priežastis |
|---|---|
| `Missing or malformed Authorization header` | Antraštė nebuvo išsiųsta arba reikšmė neprasideda `Bearer ` |
| `Invalid API key` | Raktas neteisingas arba buvo ištrintas |
| `API key expired` | Rakto galiojimas baigėsi. Sukurkite naują |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

*digna* licencijoje nėra digna Agentic įrašo arba to įrašo galiojimas baigėsi. Paprašykite digna
komandos licencijos, kuri apima digna Agentic, ir įdiekite ją, kaip aprašyta jūsų operacinės
sistemos diegimo vadove.

### Kiekviena užklausa nepavyksta su negaliojančios licencijos klaida

Baigėsi pačios *digna* licencijos galiojimas. MCP serveris kartu su prietaisų skydeliu nustoja
atsakinėti, kol įdiegiama nauja licencija.

### Agentas gali skaityti, bet negali keisti konfigūracijos

Vartotojas, kuriam priklauso API raktas, tame projekte neturi redaktoriaus rolės. Naudokite
vartotojo su redaktoriaus role raktą arba paprašykite projekto administratoriaus pakeisti rolę.

### Klientas visai negali prisijungti

Jungiantis kompiuteris nepasiekia galinio taško. Atidarykite galinio taško adresą iš to kompiuterio
ir patikrinkite ugniasienes, tarpinius serverius ir sertifikatą. Claude custom connector atveju tas
kompiuteris yra Anthropic debesyje, žr. [Iš kur ateina ryšys](#where-the-connection-comes-from).