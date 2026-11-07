# AI aģentu savienošana ar digna

**digna MCP Server** ļauj AI aģentiem strādāt ar *digna*, izmantojot
[Model Context Protocol](https://modelcontextprotocol.io) (MCP) — atvērtu standartu, ko atbalsta
Claude, Gemini un daudzi citi AI rīki. Ar *digna* savienots aģents var atbildēt uz jautājumiem par
jūsu datiem, izmeklēt brīdinājumus un palīdzēt konfigurēt *digna*. Ko aģenti spēj paveikt, skatiet
sadaļā [digna Agentic](../platform/agentic/Introduction.md).

Šī lapa aptver *digna* pusi, kas ir vienāda visiem AI klientiem. Klientu rokasgrāmatās pēc tam
parādīts, kur ievadīt galapunktu un atslēgu:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop un pielāgotie savienotāji
- [Gemini](gemini_mcp_guide.md): Antigravity un Gemini CLI

!!! info "Beta"

    digna Agentic un līdz ar to digna MCP Server tiek piegādāts kā beta versija
    [Release 2026.11](../changelog/Release_202611.md).

---

## Pirms sākat {: #before-you-start }

Jums nepieciešams:

- *digna* Release 2026.11 vai jaunāka versija
- Licence, kas ietver **digna Agentic**. Bez tās MCP serveris noraida katru pieprasījumu
- *digna* lietotāja konts. Aģents katrā projektā darbojas ar šī lietotāja atļaujām, skatiet
  [Atļaujas](../platform/agentic/how_it_works.md#permissions)
- AI klients, kas savienojas ar attāliem MCP serveriem, izmantojot **streamable HTTP**, un var
  nosūtīt galveni `Authorization`

---

## 1. MCP galapunkta atrašana {: #1-find-the-mcp-endpoint }

MCP serveris ir daļa no *digna* backend, tāpēc nekas papildus nav jāinstalē vai jāpalaiž. Tā
galapunkts ir backend adrese, kurai seko `/mcp`:

```text
https://digna.example.com/mcp
```

Ja backend darbojas tieši uz resursdatora un porta, piemēram, pēc
`digna serve --address 0.0.0.0 --port 8082`, galapunkts ir šī adrese ar `/mcp`:

```text
http://digna-host:8082/mcp
```

Ja backend priekšā atrodas reversais starpniekserveris (reverse proxy), tam jāpārsūta `/mcp` uz
backend kopā ar galveni `Authorization`.

!!! warning "Tīklā izmantojiet HTTPS"

    Katrs pieprasījums satur API atslēgu. Izmantojiet HTTPS vienmēr, kad AI klients un *digna*
    nedarbojas vienā datorā.

### No kurienes nāk savienojums {: #where-the-connection-comes-from }

Lielākā daļa AI klientu savienojas no datora, kurā tie darbojas: Claude Code, Claude Desktop ar
lokālu tiltu, Antigravity un Gemini CLI. Šiem klientiem *digna* jābūt sasniedzamam tikai no šī
datora, piemēram, jūsu uzņēmuma tīklā.

Claude **pielāgotie savienotāji** (custom connectors) darbojas citādi: ar galapunktu savienojas
Anthropic mākonis. Tie darbojas tikai tad, ja galapunkts ir sasniedzams no interneta, izmantojot
HTTPS. *digna* instalācijai, kas sasniedzama tikai jūsu tīklā, izmantojiet klientu, kas darbojas
jūsu datorā.

---

## 2. API atslēgas izveide {: #2-create-an-api-key }

AI klients autentificējas ar *digna* lietotāja API atslēgu.

1. Piesakieties *digna*.
2. Atveriet savu lietotāja profilu apakšējā kreisajā stūrī.
3. Noklikšķiniet uz **API Keys**, pēc tam uz **Add API Key**.
4. Ievadiet nosaukumu, kas norāda, kam atslēga paredzēta, piem., *Claude Code – Marcin*, un
   izvēlieties, kad tās derīgums beidzas.
5. Nokopējiet atslēgu. Tā tiek parādīta tikai vienreiz.

Katrs pieprasījums MCP serverim nosūta atslēgu šajā galvenē:

```text
Authorization: Bearer <api key>
```

Vārds `Bearer` un atstarpe aiz tā ir daļa no galvenes vērtības.

---

## 3. AI klienta savienošana {: #3-connect-your-ai-client }

| AI klients | Savienojas no | Rokasgrāmata |
|---|---|---|
| Claude Code | Jūsu datora | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop ar lokālu tiltu | Jūsu datora | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Claude pielāgotais savienotājs (claude.ai, Claude Desktop, Claude mobile) | Anthropic mākoņa | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE un lietotne | Jūsu datora | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Jūsu datora | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Darbojas arī citi MCP klienti, ja tie atbalsta attālos serverus, izmantojot streamable HTTP ar
pielāgotu galveni. Lielākā daļa no tiem nolasa līdzīgu konfigurāciju. Precīzus failu un atslēgu
nosaukumus skatiet sava klienta dokumentācijā:

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

## 4. Izmēģināšana {: #4-try-it }

Pajautājiet aģentam kaut ko, uz ko var atbildēt tikai *digna*:

- *„Parādi manus digna projektus.”*
- *„Kuri datu avoti projektā X šodien nav zaļi?”*
- *„Izskaidro datu avota Y pēdējo neizdevušos pārbaudi.”*

Ja aģents uzskaita jūsu projektus, savienojums darbojas.

---

## Drošība {: #security }

- **Viena atslēga katrai personai un klientam.** Tad varat atsaukt vienu atslēgu ar
  **Delete API Key**, neietekmējot nevienu citu.
- **Izvēlieties lietotāju apzināti.** Aģents var darīt visu, ko var atslēgas lietotājs. Tikai datu
  izpētei izmantojiet lietotāju ar reader lomu projektos.
- **Neglabājiet atslēgas koplietotos failos.** Neiesniedziet (commit) konfigurācijas failu, kurā ir
  atslēga. Ja klients to atbalsta, nolasiet atslēgu no vides mainīgā.
- **Iestatiet derīguma termiņu.** Izveidojiet jaunu atslēgu, pirms vecā zaudē derīgumu, un
  atjauniniet klientu.
- **Pārskatiet rīku izsaukumus.** Atstājiet klientā ieslēgtu rīku izsaukumu apstiprināšanu,
  vismaz izsaukumiem, kas maina konfigurāciju.

---

## Problēmu novēršana {: #troubleshooting }

### 401 Unauthorized

Atbildē norādīts iemesls:

| Ziņojums | Cēlonis |
|---|---|
| `Missing or malformed Authorization header` | Galvene netika nosūtīta, vai vērtība nesākas ar `Bearer ` |
| `Invalid API key` | Atslēga ir nepareiza vai ir dzēsta |
| `API key expired` | Atslēgas derīgums ir beidzies. Izveidojiet jaunu |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

*digna* licencē nav digna Agentic ieraksta, vai šī ieraksta derīgums ir beidzies. Lūdziet digna
komandai licenci, kas ietver digna Agentic, un instalējiet to, kā aprakstīts jūsu operētājsistēmas
instalēšanas rokasgrāmatā.

### Katrs pieprasījums neizdodas ar nederīgas licences kļūdu

Ir beidzies pašas *digna* licences derīgums. MCP serveris pārstāj atbildēt kopā ar informācijas
paneli, līdz tiek instalēta jauna licence.

### Aģents var lasīt, bet ne mainīt konfigurāciju

Lietotājam, kuram pieder API atslēga, šajā projektā nav editor lomas. Izmantojiet lietotāja ar
editor lomu atslēgu vai lūdziet projekta administratoram mainīt lomu.

### Klients nevar savienoties vispār

Dators, kas savienojas, nevar sasniegt galapunktu. Atveriet galapunkta adresi no šī datora un
pārbaudiet ugunsmūrus, starpniekserverus un sertifikātu. Claude pielāgotā savienotāja gadījumā šis
dators atrodas Anthropic mākonī, skatiet [No kurienes nāk savienojums](#where-the-connection-comes-from).