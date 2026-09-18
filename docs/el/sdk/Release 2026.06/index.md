---
title: Οδηγός αναφοράς digna Python SDK 2026.06 | Τεκμηρίωση digna
description: Πλήρης οδηγός αναφοράς για την έκδοση digna Python SDK 2026.06
image: /assets/logo_square.png
---

# Οδηγός αναφοράς digna Python SDK 2026.06

Αυτή η ενότητα τεκμηριώνει το Python SDK για το ***digna***. Είναι οργανωμένη ως αναφορά πολλών σελίδων: χρησιμοποιήστε αυτή την επισκόπηση για να κατανοήσετε τον client και συνεχίστε στη συνέχεια με τις ξεχωριστές σελίδες για τη γρήγορη εκκίνηση, τους πόρους, τα μοντέλα, τα σφάλματα και την αυτόματα παραγόμενη τεκμηρίωση API.

Το SDK δημοσιεύεται ως πακέτο `digna-sdk` και προσφέρει έναν σταθερό client με έκδοση για το REST API του ***digna***.

---

## Βασικά στοιχεία του SDK

---

### Επισκόπηση

Το SDK ακολουθεί έναν σχεδιασμό client προσανατολισμένο στους πόρους. Κάθε περιοχή του API διατίθεται ως αυτοτελής client στο ανώτερο αντικείμενο `DignaClient`, με τυποποιημένα μοντέλα αιτήματος και απόκρισης και συνεπή διαχείριση σφαλμάτων.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Βασικά χαρακτηριστικά

- **Τυποποιημένα μοντέλα** — κάθε αίτημα και κάθε απόκριση επικυρώνεται με το pydantic, ώστε ο επεξεργαστής και ο έλεγχος τύπων να εντοπίζουν τα λάθη πριν από την κλήση στο δίκτυο.
- **Προσανατολισμός στους πόρους** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` και `client.inspection_statuses` προσφέρουν ο καθένας απλές μεθόδους `list` / `get` / `create` / `update` / `delete`.
- **Σαφή σφάλματα** — τα σφάλματα του API εγείρουν `DignaAPIError` (ή μια πιο ειδική υποκλάση, όπως `DignaAuthenticationError`, `DignaAuthorizationError` ή `DignaNotFoundError`) αντί να επιστρέφουν σιωπηλά `None`.

### Εγκατάσταση

```bash
pip install digna-sdk
```

---

## Σελίδες αναφοράς

Αυτή η έκδοση είναι οργανωμένη στις εξής σελίδες:

- [Γρήγορη εκκίνηση](quickstart.md) — σύνδεση και πρώτες κλήσεις.
- [Πόροι](resources.md) — ο πλήρης κατάλογος των διαθέσιμων clients πόρων.
- [Μοντέλα](models.md) — τα μοντέλα pydantic που χρησιμοποιούνται για είσοδο και έξοδο.
- [Σφάλματα](errors.md) — η ιεραρχία των εξαιρέσεων.
- [Αναφορά API](reference.md) — αυτόματα παραγόμενη τεκμηρίωση αναφοράς.
