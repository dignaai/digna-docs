---
title: Πράκτορες AI – Επισκόπηση Ενσωμάτωσης MCP | Τεκμηρίωση digna
description: Συνδέστε το Claude, το Gemini και άλλους πράκτορες AI στο digna μέσω του digna MCP Server. Βρείτε το endpoint MCP, δημιουργήστε ένα κλειδί API, ελέγξτε την άδεια χρήσης και τις απαιτήσεις δικτύου και επιλέξτε τον οδηγό για το client AI σας.
image: /assets/logo_square.png
keywords: digna MCP server, Model Context Protocol, σύνδεση πράκτορα AI, AI agent, Claude MCP, Gemini MCP, Antigravity MCP, κλειδί API digna, digna Agentic
---

# Σύνδεση Πρακτόρων AI στο digna

Ο **digna MCP Server** επιτρέπει σε πράκτορες AI να εργάζονται με το *digna* μέσω του
[Model Context Protocol](https://modelcontextprotocol.io) (MCP), ενός ανοιχτού προτύπου που
υποστηρίζεται από το Claude, το Gemini και πολλά άλλα εργαλεία AI. Ένας πράκτορας συνδεδεμένος
στο *digna* μπορεί να απαντά σε ερωτήσεις για τα δεδομένα σας, να διερευνά ειδοποιήσεις και να
βοηθά στη διαμόρφωση του *digna*. Δείτε το [digna Agentic](../platform/agentic/Introduction.md)
για το τι μπορούν να κάνουν οι πράκτορες.

Αυτή η σελίδα καλύπτει την πλευρά του *digna*, η οποία είναι ίδια για κάθε client AI. Οι οδηγοί
των clients δείχνουν στη συνέχεια πού καταχωρίζονται το endpoint και το κλειδί:

- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop και προσαρμοσμένοι connectors
- [Gemini](gemini_mcp_guide.md): Antigravity και Gemini CLI

!!! info "Beta"

    Το digna Agentic, και μαζί του ο digna MCP Server, παραδίδεται ως έκδοση beta στο
    [Release 2026.11](../changelog/Release_202611.md).

---

## Πριν Ξεκινήσετε {: #before-you-start }

Χρειάζεστε:

- *digna* Release 2026.11 ή νεότερο
- Μια άδεια χρήσης που περιλαμβάνει το **digna Agentic**. Χωρίς αυτήν, ο MCP server απορρίπτει
  κάθε αίτημα
- Έναν λογαριασμό χρήστη *digna*. Ο πράκτορας ενεργεί με τα δικαιώματα αυτού του χρήστη σε κάθε
  project, δείτε [Δικαιώματα](../platform/agentic/how_it_works.md#permissions)
- Ένα client AI που συνδέεται σε απομακρυσμένους MCP servers μέσω **streamable HTTP** και μπορεί να
  στείλει μια κεφαλίδα `Authorization`

---

## 1. Εύρεση του MCP Endpoint {: #1-find-the-mcp-endpoint }

Ο MCP server είναι μέρος του backend του *digna*, οπότε δεν χρειάζεται να εγκαταστήσετε ή να
εκκινήσετε τίποτα επιπλέον. Το endpoint του είναι η διεύθυνση του backend ακολουθούμενη από
`/mcp`:

```text
https://digna.example.com/mcp
```

Αν το backend εκτελείται απευθείας σε έναν host και μια θύρα, για παράδειγμα μετά από
`digna serve --address 0.0.0.0 --port 8082`, το endpoint είναι αυτή η διεύθυνση με `/mcp`:

```text
http://digna-host:8082/mcp
```

Αν μπροστά από το backend βρίσκεται ένας reverse proxy, πρέπει να προωθεί το `/mcp` στο backend
μαζί με την κεφαλίδα `Authorization`.

!!! warning "Χρησιμοποιήστε HTTPS σε Δίκτυο"

    Κάθε αίτημα μεταφέρει ένα κλειδί API. Χρησιμοποιείτε HTTPS όποτε το client AI και το *digna*
    δεν βρίσκονται στο ίδιο μηχάνημα.

### Από Πού Προέρχεται η Σύνδεση {: #where-the-connection-comes-from }

Τα περισσότερα clients AI συνδέονται από το μηχάνημα στο οποίο εκτελούνται: Claude Code, Claude
Desktop με τοπική γέφυρα, Antigravity και Gemini CLI. Για αυτά, το *digna* αρκεί να είναι
προσβάσιμο από εκείνο το μηχάνημα, για παράδειγμα μέσα στο εταιρικό σας δίκτυο.

Οι **προσαρμοσμένοι connectors** (custom connectors) του Claude είναι διαφορετικοί: στο endpoint
συνδέεται το cloud της Anthropic. Λειτουργούν μόνο όταν το endpoint είναι προσβάσιμο από το
διαδίκτυο μέσω HTTPS. Για μια εγκατάσταση *digna* που είναι προσβάσιμη μόνο μέσα στο δίκτυό σας,
χρησιμοποιήστε ένα client που εκτελείται στο μηχάνημά σας.

---

## 2. Δημιουργία Κλειδιού API {: #2-create-an-api-key }

Ένα client AI αυθεντικοποιείται με το κλειδί API ενός χρήστη *digna*.

1. Συνδεθείτε στο *digna*.
2. Ανοίξτε το προφίλ χρήστη σας στην κάτω αριστερή γωνία.
3. Κάντε κλικ στο **API Keys** και μετά στο **Add API Key**.
4. Εισαγάγετε ένα όνομα που δείχνει για τι προορίζεται το κλειδί, π.χ. *Claude Code – Marcin*, και
   επιλέξτε πότε λήγει.
5. Αντιγράψτε το κλειδί. Εμφανίζεται μόνο μία φορά.

Κάθε αίτημα προς τον MCP server στέλνει το κλειδί σε αυτή την κεφαλίδα:

```text
Authorization: Bearer <api key>
```

Η λέξη `Bearer` και το κενό μετά από αυτήν αποτελούν μέρος της τιμής της κεφαλίδας.

---

## 3. Σύνδεση του Client AI {: #3-connect-your-ai-client }

| Client AI | Συνδέεται από | Οδηγός |
|---|---|---|
| Claude Code | Το μηχάνημά σας | [Claude](claude_mcp_guide.md#claude-code) |
| Claude Desktop με τοπική γέφυρα | Το μηχάνημά σας | [Claude](claude_mcp_guide.md#claude-desktop-with-a-local-bridge) |
| Προσαρμοσμένος connector του Claude (claude.ai, Claude Desktop, Claude για κινητά) | Το cloud της Anthropic | [Claude](claude_mcp_guide.md#custom-connector) |
| Antigravity CLI, IDE και εφαρμογή | Το μηχάνημά σας | [Gemini](gemini_mcp_guide.md#antigravity) |
| Gemini CLI | Το μηχάνημά σας | [Gemini](gemini_mcp_guide.md#gemini-cli) |

Λειτουργούν και άλλα clients MCP, εφόσον υποστηρίζουν απομακρυσμένους servers μέσω streamable
HTTP με προσαρμοσμένη κεφαλίδα. Τα περισσότερα διαβάζουν μια διαμόρφωση σαν την παρακάτω. Ελέγξτε
την τεκμηρίωση του client σας για τα ακριβή ονόματα αρχείου και κλειδιών:

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

## 4. Δοκιμή {: #4-try-it }

Ρωτήστε τον πράκτορα κάτι που μόνο το *digna* μπορεί να απαντήσει:

- *«Εμφάνισε τη λίστα με τα projects μου στο digna.»*
- *«Ποιες πηγές δεδομένων στο project X δεν είναι πράσινες σήμερα;»*
- *«Εξήγησε τον πιο πρόσφατο αποτυχημένο έλεγχο της πηγής δεδομένων Y.»*

Αν ο πράκτορας εμφανίσει τα projects σας, η σύνδεση λειτουργεί.

---

## Ασφάλεια {: #security }

- **Ένα κλειδί ανά άτομο και client.** Έτσι μπορείτε να ανακαλέσετε ένα μεμονωμένο κλειδί, με το
  **Delete API Key**, χωρίς να επηρεάσετε κανέναν άλλον.
- **Επιλέξτε τον χρήστη συνειδητά.** Ο πράκτορας μπορεί να κάνει ό,τι μπορεί να κάνει ο χρήστης
  του κλειδιού. Μόνο για διερεύνηση δεδομένων, χρησιμοποιήστε έναν χρήστη με τον ρόλο αναγνώστη
  (reader) στα projects.
- **Κρατήστε τα κλειδιά έξω από κοινόχρηστα αρχεία.** Μην κάνετε commit ένα αρχείο διαμόρφωσης
  που περιέχει κλειδί. Όπου το υποστηρίζει το client, διαβάστε το κλειδί από μια μεταβλητή
  περιβάλλοντος.
- **Ορίστε ημερομηνία λήξης.** Δημιουργήστε ένα νέο κλειδί πριν λήξει το παλιό και ενημερώστε το
  client.
- **Ελέγχετε τις κλήσεις εργαλείων.** Κρατήστε ενεργοποιημένη την επιβεβαίωση του client για τις
  κλήσεις εργαλείων, τουλάχιστον για κλήσεις που αλλάζουν τη διαμόρφωση.

---

## Αντιμετώπιση Προβλημάτων {: #troubleshooting }

### 401 Unauthorized

Η απόκριση αναφέρει τον λόγο:

| Μήνυμα | Αιτία |
|---|---|
| `Missing or malformed Authorization header` | Δεν στάλθηκε κεφαλίδα ή η τιμή δεν ξεκινά με `Bearer ` |
| `Invalid API key` | Το κλειδί είναι λάθος ή έχει διαγραφεί |
| `API key expired` | Το κλειδί έχει λήξει. Δημιουργήστε ένα νέο |

### 403 Forbidden: `The license does not include the agentic (MCP) feature`

Η άδεια χρήσης του *digna* δεν έχει καταχώριση digna Agentic ή αυτή η καταχώριση έχει λήξει.
Ζητήστε από την ομάδα του digna μια άδεια χρήσης που περιλαμβάνει το digna Agentic και
εγκαταστήστε την όπως περιγράφει ο οδηγός εγκατάστασης για το λειτουργικό σας σύστημα.

### Κάθε Αίτημα Αποτυγχάνει με Σφάλμα Μη Έγκυρης Άδειας Χρήσης

Έχει λήξει η ίδια η άδεια χρήσης του *digna*. Ο MCP server σταματά να απαντά, μαζί με το
dashboard, μέχρι να εγκατασταθεί νέα άδεια χρήσης.

### Ο Πράκτορας Μπορεί να Διαβάσει Αλλά Όχι να Αλλάξει τη Διαμόρφωση

Ο χρήστης πίσω από το κλειδί API δεν έχει τον ρόλο συντάκτη (editor) σε εκείνο το project. Χρησιμοποιήστε το
κλειδί ενός χρήστη με τον ρόλο συντάκτη ή ζητήστε από έναν διαχειριστή του project να αλλάξει τον
ρόλο.

### Το Client Δεν Μπορεί να Συνδεθεί Καθόλου

Το μηχάνημα που συνδέεται δεν μπορεί να φτάσει στο endpoint. Ανοίξτε τη διεύθυνση του endpoint
από εκείνο το μηχάνημα και ελέγξτε τα firewalls, τους proxies και το πιστοποιητικό. Για έναν
προσαρμοσμένο connector του Claude, αυτό το μηχάνημα βρίσκεται στο cloud της Anthropic, δείτε
[Από Πού Προέρχεται η Σύνδεση](#where-the-connection-comes-from).
