# Riferimento SDK Python digna 2026.06

Questa sezione documenta l'SDK Python per ***digna***. È organizzata come un riferimento su più pagine: questa panoramica serve a comprendere il client, per poi proseguire con le pagine dedicate a guida rapida, risorse, modelli, errori e documentazione API generata.

L'SDK è pubblicato come pacchetto `digna-sdk` ed espone un client stabile e versionato per l'API REST di ***digna***.

---

## Concetti di base dell'SDK

---

### Panoramica

L'SDK adotta un design del client orientato alle risorse. Ogni area dell'API è esposta come client di primo livello sul `DignaClient` principale, con modelli di richiesta e risposta tipizzati e una gestione degli errori coerente.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Funzionalità principali

- **Modelli tipizzati** — ogni richiesta e ogni risposta viene validata con pydantic, così l'editor e il type checker individuano gli errori prima di raggiungere la rete.
- **Orientato alle risorse** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` e `client.inspection_statuses` espongono ciascuno semplici metodi `list` / `get` / `create` / `update` / `delete`.
- **Errori chiari** — gli errori dell'API sollevano `DignaAPIError` (o una sottoclasse più specifica come `DignaAuthenticationError`, `DignaAuthorizationError` o `DignaNotFoundError`) invece di restituire silenziosamente `None`.

### Installazione

```bash
pip install digna-sdk
```

---

## Pagine di riferimento

Questa release è organizzata nelle pagine seguenti:

- [Guida rapida](quickstart.md) — connettersi ed effettuare le prime chiamate.
- [Risorse](resources.md) — l'elenco completo dei client di risorse disponibili.
- [Modelli](models.md) — i modelli pydantic usati per input e output.
- [Errori](errors.md) — la gerarchia delle eccezioni.
- [Riferimento API](reference.md) — documentazione di riferimento generata automaticamente.