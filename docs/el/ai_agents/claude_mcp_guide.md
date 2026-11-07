---
title: Claude – Σύνδεση του Claude στο digna μέσω MCP | Τεκμηρίωση digna
description: Συνδέστε το Claude στο digna μέσω του digna MCP Server — Claude Code από τη γραμμή εντολών ή με ένα κοινόχρηστο .mcp.json, Claude Desktop με τοπική γέφυρα και προσαρμοσμένοι connectors στο claude.ai, με ένα κλειδί API στην κεφαλίδα Authorization.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, claude.ai custom connector, digna MCP server, mcp-remote, Authorization Bearer, κλειδί API digna
---

# Σύνδεση του Claude στο digna

Αυτός ο οδηγός συνδέει το Claude στον **digna MCP Server**. Χρειάζεστε το endpoint MCP της
εγκατάστασης *digna* σας και ένα κλειδί API, όπως περιγράφεται στην
[Επισκόπηση Πρακτόρων AI](overview.md).

Τα παραδείγματα χρησιμοποιούν το `https://digna.example.com/mcp` ως endpoint. Αντικαταστήστε το με
το δικό σας.

## Επιλογή Τρόπου Σύνδεσης {: #choose-how-to-connect }

| Προϊόν Claude | Συνδέεται από | Λειτουργεί με *digna* μέσα στο δίκτυό σας |
|---|---|---|
| [Claude Code](#claude-code) | Το μηχάνημά σας | Ναι |
| [Claude Desktop με τοπική γέφυρα](#claude-desktop-with-a-local-bridge) | Το μηχάνημά σας | Ναι |
| [Προσαρμοσμένος connector](#custom-connector) στο claude.ai, στο Claude Desktop και στο Claude για κινητά | Το cloud της Anthropic | Όχι. Το endpoint πρέπει να είναι προσβάσιμο από το διαδίκτυο |

Για μια εγκατάσταση *digna* που εκτελείται μέσα στο εταιρικό σας δίκτυο, χρησιμοποιήστε το Claude
Code ή το Claude Desktop με τοπική γέφυρα.

---

## Claude Code {: #claude-code }

### 1. Προσθήκη του Server {: #1-add-the-server }

Βάλτε το κλειδί API σε μια μεταβλητή περιβάλλοντος και μετά προσθέστε τον server:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

Το shell σας συμπληρώνει το `$DIGNA_API_KEY` όταν εκτελείτε την εντολή, οπότε το Claude Code
αποθηκεύει το κλειδί στη δική του διαμόρφωση.

Το `--scope` καθορίζει πού είναι διαθέσιμος ο server:

| Εύρος | Διαθέσιμος |
|---|---|
| `local` (προεπιλογή) | Σε εσάς, μόνο στο τρέχον project |
| `user` | Σε εσάς, σε κάθε project |
| `project` | Σε όλους όσοι εργάζονται στο project, μέσω ενός αρχείου `.mcp.json` στο project |

### 2. Κοινή Χρήση του Server με την Ομάδα σας (Προαιρετικό) {: #2-share-the-server-with-your-team }

Για να δώσετε σε όλους σε ένα project τον ίδιο server, προσθέστε ένα αρχείο `.mcp.json` στη ρίζα
του project. Μη γράψετε το κλειδί στο αρχείο. Το Claude Code συμπληρώνει το `${DIGNA_API_KEY}` από
το περιβάλλον του κάθε ατόμου:

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

Κάθε άτομο ορίζει το `DIGNA_API_KEY` στο δικό του κλειδί. Την πρώτη φορά που το Claude Code βρίσκει
το αρχείο, ρωτά αν θα χρησιμοποιήσει τους servers που περιέχει.

### 3. Επαλήθευση της Σύνδεσης {: #3-verify-the-connection }

Από το shell σας:

```bash
claude mcp list
```

Ο server `digna` πρέπει να εμφανίζει `✔ Connected`. Μέσα σε μια συνεδρία Claude Code, εκτελέστε
`/mcp` για να δείτε τον server και τα εργαλεία του.

---

## Claude Desktop με Τοπική Γέφυρα {: #claude-desktop-with-a-local-bridge }

Το αρχείο διαμόρφωσης του Claude Desktop εκκινεί τοπικούς MCP servers στο μηχάνημά σας. Μια μικρή
γέφυρα, το πακέτο ανοιχτού κώδικα [`mcp-remote`](https://github.com/geelen/mcp-remote),
εκτελείται εκεί και προωθεί κάθε αίτημα στο endpoint του *digna* με το κλειδί API σας. Επειδή η
γέφυρα εκτελείται στο μηχάνημά σας, αυτή η μέθοδος λειτουργεί με το *digna* μέσα στο εταιρικό σας
δίκτυο.

!!! note "Ένα Πακέτο της Κοινότητας"

    Το `mcp-remote` συντηρείται από την κοινότητα ανοιχτού κώδικα που το αναπτύσσει, όχι από την
    Anthropic ή το digna. Ελέγξτε ότι ο οργανισμός σας το επιτρέπει πριν το χρησιμοποιήσετε.

### 1. Εγκατάσταση του Node.js {: #1-install-nodejs }

Η γέφυρα χρειάζεται [Node.js](https://nodejs.org) 18 ή νεότερο. Το Claude Desktop χρησιμοποιεί
την έκδοση Node.js που είναι εγκατεστημένη στο σύστημά σας. Ελέγξτε την με:

```bash
node --version
```

### 2. Επεξεργασία του Αρχείου Διαμόρφωσης {: #2-edit-the-configuration-file }

Ανοίξτε το `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Προσθέστε τον server `digna`. Αν το αρχείο έχει ήδη ενότητα `mcpServers`, προσθέστε την
καταχώριση `digna` σε αυτήν:

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

!!! warning "Διατηρήστε την Κεφαλίδα Ακριβώς Όπως Φαίνεται"

    Γράψτε `Authorization:${AUTH_HEADER}` χωρίς κενά και βάλτε το `Bearer <api key>` στο `env`.
    Το Claude Desktop στα Windows δεν κάνει escape τα κενά μέσα στο `args`, οπότε ένα κενό εκεί
    χαλάει την κεφαλίδα.

### 3. Επανεκκίνηση του Claude Desktop {: #3-restart-claude-desktop }

Τερματίστε πλήρως το Claude Desktop και ξεκινήστε το ξανά. Σε μια νέα συνομιλία, κάντε κλικ στο
**+** και ανοίξτε το **Connectors**: το `digna` πρέπει να εμφανίζεται στη λίστα και να είναι
ενεργοποιημένο.

---

## Προσαρμοσμένος Connector {: #custom-connector }

Ένας προσαρμοσμένος connector (custom connector) κάνει το *digna* διαθέσιμο στο claude.ai, στο
Claude Desktop και στις εφαρμογές Claude για κινητά χωρίς καμία τοπική ρύθμιση. Στο endpoint
συνδέεται το cloud της Anthropic, οπότε αυτή η μέθοδος λειτουργεί μόνο όταν:

- Το endpoint του *digna* είναι προσβάσιμο από το διαδίκτυο μέσω HTTPS
- Ο οργανισμός σας στο Claude διαθέτει την επιλογή **Request headers** στο παράθυρο διαλόγου
  **Add custom connector**. Η Anthropic την προσφέρει ως beta σε περιορισμένο αριθμό οργανισμών

!!! warning "Όχι για digna Μέσα στο Δίκτυό σας"

    Τα MCP tunnels του Claude, που φτάνουν σε servers μέσα σε ιδιωτικό δίκτυο, απαιτούν OAuth
    στον MCP server. Ο digna MCP Server αυθεντικοποιεί με κλειδιά API, οπότε δεν μπορεί να
    χρησιμοποιηθεί tunnel. Χρησιμοποιήστε αντί αυτού το [Claude Code](#claude-code) ή το
    [Claude Desktop με τοπική γέφυρα](#claude-desktop-with-a-local-bridge).

### 1. Άνοιγμα των Ρυθμίσεων Connector {: #1-open-the-connector-settings }

- **Πλάνα Free, Pro, Max και Ultra**: μεταβείτε στο **Customize > Connectors** και κάντε κλικ στο
  **Add custom connector**.
- **Πλάνα Team και Enterprise**: ένας Owner μεταβαίνει στο **Organization settings > Connectors**,
  κάνει κλικ στο **Add**, μετά στο **Custom** και επιλέγει **Web** αν ερωτηθεί για τον τύπο.

### 2. Εισαγωγή των Στοιχείων του Connector {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: επιλέξτε `authorization` ως όνομα κεφαλίδας, εισαγάγετε
   `Bearer <api key>` ως τιμή, μαζί με τη λέξη `Bearer` και το κενό, και σημειώστε την ως
   **Required**.
4. Κάντε κλικ στο **Add**.

!!! warning "Όλοι Μοιράζονται το Κλειδί"

    Κάθε μέλος που χρησιμοποιεί τον connector εργάζεται με το ίδιο κλειδί API, και επομένως με
    τον ίδιο χρήστη *digna*. Δημιουργήστε έναν ξεχωριστό χρήστη *digna* για τον connector και
    δώστε του μόνο τα projects και τους ρόλους που επιτρέπεται να έχει ο καθένας, π.χ. τον ρόλο
    αναγνώστη.

Στα πλάνα Team και Enterprise, τα μέλη συνδέονται στη συνέχεια από το **Customize > Connectors**,
όπου ο connector φέρει την ετικέτα **Custom**.

Το Claude δεν μπορεί να αλλάξει την κεφαλίδα ενός υπάρχοντος connector. Για να χρησιμοποιήσετε
ένα νέο κλειδί, αφαιρέστε τον connector και προσθέστε τον ξανά.

---

## Αντιμετώπιση Προβλημάτων στο Claude {: #troubleshooting-claude }

### Το claude mcp list Εμφανίζει Failed to connect

Εκτελέστε `claude mcp get digna` για να δείτε την αιτία. Ένα `401` σημαίνει ότι το κλειδί
απορρίφθηκε· δείτε [401 Unauthorized](overview.md#troubleshooting). Το Claude Code προειδοποιεί
επίσης για κενά ή αλλαγή γραμμής στην αρχή ή στο τέλος του κλειδιού, που συχνά προκύπτουν κατά
την αντιγραφή του.

### Το digna Δεν Εμφανίζεται στο Claude Desktop

- Ελέγξτε ότι είναι εγκατεστημένο το Node.js 18 ή νεότερο: `node --version`.
- Ελέγξτε ότι το `claude_desktop_config.json` είναι έγκυρο JSON. Ένα κόμμα που λείπει εμποδίζει
  τη φόρτωση όλων των servers του αρχείου.
- Τερματίστε πλήρως το Claude Desktop, όχι μόνο το παράθυρο, και ξεκινήστε το ξανά.

### Ο Προσαρμοσμένος Connector Δεν Μπορεί να Φτάσει στον Server

Το cloud της Anthropic δεν μπορεί να φτάσει στο endpoint. Ελέγξτε ότι είναι προσβάσιμο από το
διαδίκτυο μέσω HTTPS με έγκυρο πιστοποιητικό ή συνδεθείτε αντί αυτού μέσω του
[Claude Code](#claude-code).

---

## Δείτε Επίσης {: #see-also }

- [Επισκόπηση Πρακτόρων AI](overview.md): endpoint, κλειδί API, ασφάλεια και γενική αντιμετώπιση προβλημάτων
- [Gemini](gemini_mcp_guide.md): σύνδεση του Antigravity ή του Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): τι μπορούν να κάνουν οι πράκτορες AI με το *digna*
