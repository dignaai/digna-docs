---
title: AI-agendid – MCP-integratsiooni ülevaade | digna dokumentatsioon
description: Ühenda Claude, Gemini ja teised AI-agendid dignaga digna MCP Serveri kaudu. Leia MCP lõpp-punkt, loo API võti, kontrolli litsentsi- ja võrgunõudeid ning vali oma AI-kliendi juhend.
image: /assets/logo_square.png
keywords: digna MCP server, Model Context Protocol, AI-agendi ühendamine, Claude MCP, Gemini MCP, Antigravity MCP, digna API võti, digna Agentic
---

# Ühenda AI-agendid dignaga

**digna MCP Server** võimaldab AI-agentidel töötada *dignaga*
[Model Context Protocoli](https://modelcontextprotocol.io) (MCP) kaudu. See on avatud standard, mida
toetavad Claude, Gemini ja paljud teised AI-tööriistad. *dignaga* ühendatud agent saab vastata
küsimustele sinu andmete kohta, uurida hoiatusi ja aidata *dignat* konfigureerida. Vaata
[digna Agentic](../platform/agentic/Introduction.md), mida agendid teha saavad.

See leht käsitleb *digna* poolt, mis on kõigi AI-klientide jaoks sama. Klientide juhendid näitavad
seejärel, kuhu need andmed sisestada:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop ja custom connectorid
- [Gemini](gemini_mcp_guide.md): Antigravity ja Gemini CLI

!!! info "Beeta"

    digna Agentic ja koos sellega digna MCP Server tarnitakse beetaversioonina väljalaskes
    [Release 2026.11](../changelog/Release_202611.md).

---

## Enne alustamist {: #before-you-start }

Sul on vaja:

- *digna* Release 2026.11 või uuemat
- Litsentsi, mis sisaldab **digna Agenticut**. Ilma selleta lükkab MCP-server iga päringu tagasi
- *digna* kasutajakontot. Agent tegutseb igas projektis selle kasutaja õigustega, vaata
  [Õigused](../platform/agentic/how_it_works.md#permissions)
- AI-klienti, mis ühendub kaug-MCP-serveritega **streamable HTTP** kaudu ja suudab saata
  `Authorization` päise

---

## 1. Leia MCP lõpp-punkt {: #1-find-the-mcp-endpoint }

MCP-server on osa *digna* backendist, seega pole midagi lisaks vaja paigaldada ega käivitada. Selle
lõpp-punkt on backendi aadress, millele järgneb `/mcp`:

```text
https://digna.example.com/mcp
```

Kui backend töötab otse hostis ja pordis, näiteks pärast käsku
`digna serve --address 0.0.0.0 --port 8082`, on lõpp-punkt see aadress koos `/mcp`-ga:

```text
http://digna-host:8082/mcp
```

Kui backendi ees on pöördpuhverserver (reverse proxy), peab see edastama `/mcp` backendile koos
`Authorization` päisega.

!!! warning "Kasuta võrgus HTTPS-i"

    Iga päring sisaldab API võtit. Kasuta HTTPS-i alati, kui AI-klient ja *digna* ei asu samas
    masinas.

### Kust ühendus tuleb {: #where-the-connection-comes-from }

Enamik AI-kliente ühendub masinast, milles nad töötavad: Claude Code, Claude Desktop kohaliku
sillaga, Antigravity ja Gemini CLI. Nende jaoks peab *digna* olema kättesaadav ainult sellest
masinast, näiteks sinu ettevõtte võrgu sees.

Claude'i **custom connectorid** on teistsugused: lõpp-punktiga ühendub Anthropicu pilv. Need
töötavad ainult siis, kui lõpp-punkt on internetist HTTPS-i kaudu kättesaadav. Kui *digna*
paigaldus on kättesaadav ainult sinu võrgu sees, kasuta klienti, mis töötab sinu masinas.

---

## 2. Loo API võti {: #2-create-an-api-key }

AI-klient autendib end *digna* kasutaja API võtmega.

1. Logi *dignasse* sisse.
2. Ava vasakus alanurgas oma kasutajaprofiil.
3. Klõpsa **API Keys** ja seejärel **Add API Key**.
4. Sisesta nimi, mis ütleb, milleks võti on, nt *Claude Code – Marcin*, ja vali, millal see
   aegub.
5. Kopeeri võti. Seda näidatakse ainult üks kord.

Iga MCP-serverile saadetav päring sisaldab võtit selles päises:

```text
Authorization: Bearer <api key>
```

Sõna `Bearer` ja sellele järgnev tühik on päise väärtuse osa.

---

## 3. Ühenda oma AI-klient {: #3-connect-your-ai-client }

| AI-klient | Ühendub | Juhend |
|---|---|---|
| Claude Code | Sinu masinast | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop kohaliku sillaga | Sinu masinast | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Claude custom connector (claude.ai, Claude Desktop, Claude mobiilirakendus) | Anthropicu pilvest | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE ja rakendus | Sinu masinast | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Sinu masinast | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Ka teised MCP-kliendid töötavad, kui need toetavad kaugservereid streamable HTTP kaudu kohandatud
päisega. Enamik neist loeb sellist konfiguratsiooni. Täpsed faili- ja võtmenimed leiad oma kliendi
dokumentatsioonist:

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

## 4. Proovi järele {: #4-try-it }

Küsi agendilt midagi, millele saab vastata ainult *digna*:

- *"Loetle minu digna projektid."*
- *"Millised projekti X andmeallikad ei ole täna rohelised?"*
- *"Selgita andmeallika Y viimast ebaõnnestunud kontrolli."*

Kui agent loetleb sinu projektid, ühendus töötab.

---

## Turvalisus {: #security }

- **Üks võti inimese ja kliendi kohta.** Siis saad üksiku võtme **Delete API Key** abil tühistada,
  ilma et see kedagi teist mõjutaks.
- **Vali kasutaja läbimõeldult.** Agent saab teha kõike, mida võtme kasutaja saab teha. Ainult
  andmete uurimiseks kasuta kasutajat, kellel on projektides lugeja roll.
- **Hoia võtmed jagatud failidest eemal.** Ära commiti konfiguratsioonifaili, mis sisaldab võtit.
  Kui klient seda toetab, loe võti keskkonnamuutujast.
- **Määra aegumisaeg.** Loo uus võti enne, kui vana aegub, ja uuenda klienti.
- **Vaata tööriistakutsed üle.** Hoia kliendi tööriistakutsete kinnitamine sisse lülitatuna,
  vähemalt konfiguratsiooni muutvate kutsete puhul.

---

## Tõrkeotsing {: #troubleshooting }

### 401 Unauthorized

Vastus ütleb põhjuse:

| Teade | Põhjus |
|---|---|
| `Missing or malformed Authorization header` | Päist ei saadetud või väärtus ei alga sõnaga `Bearer ` |
| `Invalid API key` | Võti on vale või see on kustutatud |
| `API key expired` | Võti on aegunud. Loo uus |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

*digna* litsentsis puudub digna Agenticu kirje või see kirje on aegunud. Küsi digna meeskonnalt
litsentsi, mis sisaldab digna Agenticut, ja paigalda see oma operatsioonisüsteemi
paigaldusjuhendi järgi.

### Iga päring ebaõnnestub kehtetu litsentsi veaga

*digna* litsents ise on aegunud. MCP-server lõpetab vastamise koos juhtpaneeliga, kuni uus
litsents on paigaldatud.

### Agent saab konfiguratsiooni lugeda, kuid mitte muuta

API võtme taga oleval kasutajal pole selles projektis toimetaja rolli. Kasuta toimetaja rolliga
kasutaja võtit või palu projekti administraatoril rolli muuta.

### Klient ei saa üldse ühendust

Ühenduv masin ei jõua lõpp-punktini. Ava lõpp-punkti aadress sellest masinast ning kontrolli
tulemüüre, puhverservereid ja sertifikaati. Claude'i custom connectori puhul asub see masin
Anthropicu pilves, vaata [Kust ühendus tuleb](#where-the-connection-comes-from).
