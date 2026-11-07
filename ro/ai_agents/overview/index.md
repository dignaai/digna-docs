# Conectați agenți AI la digna

**digna MCP Server** permite agenților AI să lucreze cu *digna* prin
[Model Context Protocol](https://modelcontextprotocol.io) (MCP), un standard deschis acceptat de
Claude, Gemini și multe alte instrumente AI. Un agent conectat la *digna* poate răspunde la
întrebări despre datele dvs., poate investiga alertele și poate ajuta la configurarea *digna*.
Consultați [digna Agentic](../platform/agentic/Introduction.md) pentru a vedea ce pot face agenții.

Această pagină acoperă partea *digna*, care este aceeași pentru orice client AI. Ghidurile pentru
clienți arată apoi unde se introduc endpoint-ul și cheia:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop și conectori personalizați
- [Gemini](gemini_mcp_guide.md): Antigravity și Gemini CLI

!!! info "Beta"

    digna Agentic și, odată cu acesta, digna MCP Server sunt livrate ca versiune beta în
    [Release 2026.11](../changelog/Release_202611.md).

---

## Înainte de a începe {: #before-you-start }

Aveți nevoie de:

- *digna* Release 2026.11 sau o versiune ulterioară
- O licență care include **digna Agentic**. Fără aceasta, serverul MCP refuză orice cerere
- Un cont de utilizator *digna*. Agentul acționează cu permisiunile acestui utilizator în fiecare
  proiect, consultați [Permisiuni](../platform/agentic/how_it_works.md#permissions)
- Un client AI care se conectează la servere MCP la distanță prin **streamable HTTP** și poate
  trimite un header `Authorization`

---

## 1. Găsiți endpoint-ul MCP {: #1-find-the-mcp-endpoint }

Serverul MCP face parte din backend-ul *digna*, deci nu trebuie instalat sau pornit nimic
suplimentar. Endpoint-ul său este adresa backend-ului urmată de `/mcp`:

```text
https://digna.example.com/mcp
```

Dacă backend-ul rulează direct pe un host și un port, de exemplu după
`digna serve --address 0.0.0.0 --port 8082`, endpoint-ul este acea adresă cu `/mcp`:

```text
http://digna-host:8082/mcp
```

Dacă în fața backend-ului se află un reverse proxy, acesta trebuie să redirecționeze `/mcp` către
backend împreună cu header-ul `Authorization`.

!!! warning "Folosiți HTTPS într-o rețea"

    Fiecare cerere conține o cheie API. Folosiți HTTPS ori de câte ori clientul AI și *digna* nu se
    află pe aceeași mașină.

### De unde vine conexiunea {: #where-the-connection-comes-from }

Majoritatea clienților AI se conectează de pe mașina pe care rulează: Claude Code, Claude Desktop
cu o punte locală, Antigravity și Gemini CLI. Pentru aceștia, *digna* trebuie doar să fie
accesibil de pe acea mașină, de exemplu din rețeaua companiei dvs.

**Conectorii personalizați** (custom connectors) ai Claude sunt diferiți: cloud-ul Anthropic se
conectează la endpoint. Ei funcționează doar atunci când endpoint-ul este accesibil din internet
prin HTTPS. Pentru o instalare *digna* accesibilă doar în interiorul rețelei dvs., folosiți un
client care rulează pe mașina dvs.

---

## 2. Creați o cheie API {: #2-create-an-api-key }

Un client AI se autentifică cu cheia API a unui utilizator *digna*.

1. Conectați-vă la *digna*.
2. Deschideți profilul de utilizator din colțul din stânga jos.
3. Faceți clic pe **API Keys**, apoi pe **Add API Key**.
4. Introduceți un nume care indică scopul cheii, de ex. *Claude Code – Marcin*, și alegeți când
   expiră.
5. Copiați cheia. Este afișată o singură dată.

Fiecare cerere către serverul MCP trimite cheia în acest header:

```text
Authorization: Bearer <api key>
```

Cuvântul `Bearer` și spațiul de după el fac parte din valoarea header-ului.

---

## 3. Conectați clientul AI {: #3-connect-your-ai-client }

| Client AI | Se conectează de pe | Ghid |
|---|---|---|
| Claude Code | Mașina dvs. | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop cu o punte locală | Mașina dvs. | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Conector personalizat Claude (claude.ai, Claude Desktop, Claude mobil) | Cloud-ul Anthropic | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE și aplicație | Mașina dvs. | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Mașina dvs. | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Funcționează și alți clienți MCP, dacă acceptă servere la distanță prin streamable HTTP cu un
header personalizat. Majoritatea citesc o configurație ca aceasta. Consultați documentația
clientului dvs. pentru numele exacte ale fișierului și cheilor:

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

## 4. Încercați {: #4-try-it }

Întrebați agentul ceva la care doar *digna* poate răspunde:

- *„Listează proiectele mele digna.”*
- *„Care surse de date din proiectul X nu sunt verzi astăzi?”*
- *„Explică cea mai recentă verificare eșuată a sursei de date Y.”*

Dacă agentul vă listează proiectele, conexiunea funcționează.

---

## Securitate {: #security }

- **O cheie pentru fiecare persoană și client.** Astfel puteți revoca o singură cheie, cu
  **Delete API Key**, fără a afecta pe nimeni altcineva.
- **Alegeți utilizatorul în mod deliberat.** Agentul poate face tot ce poate face utilizatorul
  cheii. Doar pentru investigarea datelor, folosiți un utilizator cu rolul de cititor în proiecte.
- **Nu păstrați cheile în fișiere partajate.** Nu faceți commit unui fișier de configurare care
  conține o cheie. Acolo unde clientul permite, citiți cheia dintr-o variabilă de mediu.
- **Setați o dată de expirare.** Creați o cheie nouă înainte ca cea veche să expire și actualizați
  clientul.
- **Verificați apelurile de instrumente.** Păstrați activată confirmarea clientului pentru apelurile
  de instrumente, cel puțin pentru apelurile care modifică configurația.

---

## Depanare {: #troubleshooting }

### 401 Unauthorized

Răspunsul indică motivul:

| Mesaj | Cauză |
|---|---|
| `Missing or malformed Authorization header` | Nu a fost trimis niciun header sau valoarea nu începe cu `Bearer ` |
| `Invalid API key` | Cheia este greșită sau a fost ștearsă |
| `API key expired` | Cheia a expirat. Creați una nouă |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

Licența *digna* nu are o intrare digna Agentic sau acea intrare a expirat. Cereți echipei digna o
licență care include digna Agentic și instalați-o așa cum descrie ghidul de instalare pentru
sistemul dvs. de operare.

### Fiecare cerere eșuează cu o eroare de licență invalidă

Licența *digna* însăși a expirat. Serverul MCP nu mai răspunde, la fel ca dashboard-ul, până când
este instalată o licență nouă.

### Agentul poate citi, dar nu poate modifica configurația

Utilizatorul din spatele cheii API nu are rolul de editor în acel proiect. Folosiți cheia unui
utilizator cu rolul de editor sau cereți unui administrator de proiect să schimbe rolul.

### Clientul nu se poate conecta deloc

Mașina care se conectează nu poate ajunge la endpoint. Deschideți adresa endpoint-ului de pe acea
mașină și verificați firewall-urile, proxy-urile și certificatul. Pentru un conector personalizat
Claude, acea mașină se află în cloud-ul Anthropic, consultați
[De unde vine conexiunea](#where-the-connection-comes-from).