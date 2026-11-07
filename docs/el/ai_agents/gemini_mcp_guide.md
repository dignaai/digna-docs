---
title: Gemini – Σύνδεση του Antigravity και του Gemini CLI στο digna μέσω MCP | Τεκμηρίωση digna
description: Συνδέστε τα εργαλεία Gemini της Google στο digna μέσω του digna MCP Server — Antigravity CLI, IDE και εφαρμογή με mcp_config.json, και Gemini CLI με settings.json ή gemini mcp add, χρησιμοποιώντας ένα κλειδί API στην κεφαλίδα Authorization.
image: /assets/logo_square.png
keywords: Gemini MCP, Antigravity MCP, Antigravity CLI, agy, Gemini CLI MCP, mcp_config.json, digna MCP server, Authorization Bearer, κλειδί API digna
---

# Σύνδεση του Gemini στο digna

Αυτός ο οδηγός συνδέει τα εργαλεία Gemini της Google στον **digna MCP Server**. Χρειάζεστε το
endpoint MCP της εγκατάστασης *digna* σας και ένα κλειδί API, όπως περιγράφεται στην
[Επισκόπηση Πρακτόρων AI](overview.md).

Τα παραδείγματα χρησιμοποιούν το `https://digna.example.com/mcp` ως endpoint. Αντικαταστήστε το με
το δικό σας.

## Επιλογή Εργαλείου {: #choose-your-tool }

| Εργαλείο | Για | Διαμόρφωση |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE και εφαρμογή | Τα εργαλεία πρακτόρων της Google. Το Antigravity CLI αντικατέστησε το Gemini CLI για τους ατομικούς λογαριασμούς Google τον Ιούνιο του 2026 | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Άδειες Gemini Code Assist Standard και Enterprise, καθώς και επί πληρωμή κλειδιά Gemini API | `settings.json` ή `gemini mcp add` |
| Εφαρμογή Gemini Enterprise | — | Δεν υποστηρίζεται. Ο προσαρμοσμένος MCP connector της συνδέεται με OAuth ή με λογαριασμό υπηρεσίας Google Cloud, ενώ ο digna MCP Server αυθεντικοποιεί με κλειδιά API |

Όλα αυτά τα εργαλεία συνδέονται από το μηχάνημα στο οποίο εκτελούνται, οπότε λειτουργούν με το
*digna* μέσα στο εταιρικό σας δίκτυο, εφόσον αυτό το μηχάνημα μπορεί να φτάσει στο endpoint.

---

## Antigravity {: #antigravity }

Το Antigravity διαβάζει τους MCP servers του από το `mcp_config.json`, το οποίο μοιράζονται το
CLI, το IDE και η εφαρμογή.

### 1. Άνοιγμα του mcp_config.json {: #1-open-mcp-config-json }

| Εύρος | Αρχείο |
|---|---|
| Όλα τα projects σας | `~/.gemini/config/mcp_config.json` |
| Ένα workspace | `.agents/mcp_config.json` στο workspace |

Για να ανοίξετε το αρχείο που χρησιμοποιείται:

- **CLI**: πληκτρολογήστε `/mcp` και πατήστε ++enter++ για να ανοίξει ο διαχειριστής MCP.
- **IDE**: στο πλαϊνό πάνελ του πράκτορα, ανοίξτε το μενού **…**, επιλέξτε **MCP Servers**, μετά
  **Manage MCP Servers** και μετά **View raw config**.
- **Εφαρμογή**: μεταβείτε στο **Customizations** > **Installed** > **MCP Servers** και
  χρησιμοποιήστε το **Copy Config File Path**.

### 2. Προσθήκη του Server digna {: #2-add-the-digna-server }

Προσθέστε την καταχώριση `digna`. Αν το αρχείο έχει ήδη ενότητα `mcpServers`, προσθέστε την εκεί:

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

Το Antigravity φτάνει σε απομακρυσμένους servers μόνο μέσω streamable HTTP, το οποίο χρησιμοποιεί
ο digna MCP Server. Γράψτε το endpoint ως `serverUrl`· το κλειδί `httpUrl` του Gemini CLI δεν
υποστηρίζεται.

### 3. Επαλήθευση της Σύνδεσης {: #3-verify-the-connection }

Στο CLI, πληκτρολογήστε `/mcp`: ο διαχειριστής MCP εμφανίζει τον server `digna` με την κατάστασή
του και τα εργαλεία του, και μπορεί να επαναφορτώσει τη διαμόρφωση και να εμφανίσει τα logs
σύνδεσης. Στο IDE, ο server εμφανίζεται στο **Manage MCP Servers**.

!!! warning "Προστατέψτε το Αρχείο"

    Το `mcp_config.json` περιέχει το κλειδί API σε απλό κείμενο. Κρατήστε ένα
    `.agents/mcp_config.json` του workspace εκτός ελέγχου εκδόσεων και επιτρέψτε μόνο στον δικό
    σας λογαριασμό να διαβάζει το καθολικό αρχείο.

---

## Gemini CLI {: #gemini-cli }

### 1. Προσθήκη του Server {: #1-add-the-server }

Βάλτε το κλειδί API σε μια μεταβλητή περιβάλλοντος και μετά προσθέστε τον server:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

Το shell σας συμπληρώνει το `$DIGNA_API_KEY` όταν εκτελείτε την εντολή, οπότε το Gemini CLI
αποθηκεύει το κλειδί στις ρυθμίσεις του. Χωρίς `--scope user`, ο server προστίθεται μόνο στο
τρέχον project.

### 2. Ή Επεξεργασία του settings.json {: #2-or-edit-settings-json }

Η παραπάνω εντολή γράφει στο `settings.json`. Για να επεξεργαστείτε το αρχείο μόνοι σας:

| Εύρος | Αρχείο |
|---|---|
| Όλα τα projects σας | `~/.gemini/settings.json` |
| Ένα project | `.gemini/settings.json` στο project |

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

Χρησιμοποιήστε το `httpUrl`, το κλειδί για streamable HTTP. Το παρόμοιο κλειδί `url` επιλέγει την
παλαιότερη μεταφορά SSE, την οποία ο digna MCP Server δεν προσφέρει. Μη χρησιμοποιείτε κάτω
παύλες στο όνομα του server.

!!! tip "Αφήστε το Trust Απενεργοποιημένο"

    Το Gemini CLI ζητά επιβεβαίωση πριν από κάθε κλήση εργαλείου, εκτός αν ο server έχει
    `"trust": true`. Αφήστε το `trust` απενεργοποιημένο για το *digna*, ώστε να επιβεβαιώνετε
    κάθε αλλαγή που κάνει ένας πράκτορας στη διαμόρφωσή σας.

### 3. Επαλήθευση της Σύνδεσης {: #3-verify-the-connection-gemini-cli }

Από το shell σας:

```bash
gemini mcp list
```

Ο server `digna` πρέπει να εμφανίζεται ως συνδεδεμένος. Μέσα σε μια συνεδρία Gemini CLI,
εκτελέστε `/mcp` για να δείτε τον server και τα εργαλεία του.

---

## Αντιμετώπιση Προβλημάτων στο Gemini {: #troubleshooting-gemini }

### Ο Server Εμφανίζεται ως Αποσυνδεδεμένος

- Ελέγξτε ότι το endpoint τελειώνει σε `/mcp` και είναι προσβάσιμο από το μηχάνημά σας.
- Ελέγξτε το όνομα του κλειδιού: `serverUrl` στο Antigravity, `httpUrl` στο Gemini CLI.
- Ένα `401` σημαίνει ότι το κλειδί απορρίφθηκε· δείτε [401 Unauthorized](overview.md#troubleshooting).

### Το Gemini CLI Δεν Ξεκινά Πλέον για τον Λογαριασμό μου

Από τον Ιούνιο του 2026, οι ατομικοί λογαριασμοί Google χρησιμοποιούν το Antigravity CLI αντί για
το Gemini CLI. Μεταφέρετε την καταχώριση `digna` στο `mcp_config.json` όπως περιγράφεται στην
ενότητα [Antigravity](#antigravity) και μετονομάστε το `httpUrl` σε `serverUrl`.

---

## Δείτε Επίσης {: #see-also }

- [Επισκόπηση Πρακτόρων AI](overview.md): endpoint, κλειδί API, ασφάλεια και γενική αντιμετώπιση προβλημάτων
- [Claude](claude_mcp_guide.md): σύνδεση του Claude Code, του Claude Desktop ή ενός προσαρμοσμένου connector
- [digna Agentic](../platform/agentic/Introduction.md): τι μπορούν να κάνουν οι πράκτορες AI με το *digna*
