# Referência do SDK Python digna 2026.06

Esta seção documenta o SDK Python do ***digna***. Ela está organizada como uma referência de várias páginas: use esta visão geral para entender o cliente e continue nas páginas dedicadas a início rápido, recursos, modelos, erros e documentação de API gerada.

O SDK é publicado como o pacote `digna-sdk` e expõe um cliente estável e versionado para a API REST do ***digna***.

---

## Noções Básicas do SDK

---

### Visão Geral

O SDK adota um design de cliente orientado a recursos. Cada área da API é exposta como um cliente de primeira classe no `DignaClient` principal, com modelos de requisição e resposta tipados e tratamento de erros consistente.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Principais Funcionalidades

- **Modelos tipados** — cada requisição e cada resposta é validada com pydantic, de modo que seu editor e seu verificador de tipos detectam erros antes de qualquer chamada de rede.
- **Orientado a recursos** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` e `client.inspection_statuses` expõem métodos simples de `list` / `get` / `create` / `update` / `delete`.
- **Erros claros** — erros da API levantam `DignaAPIError` (ou uma subclasse mais específica, como `DignaAuthenticationError`, `DignaAuthorizationError` ou `DignaNotFoundError`) em vez de retornar `None` silenciosamente.

### Instalação

```bash
pip install digna-sdk
```

---

## Páginas de Referência

Esta versão está organizada nas seguintes páginas:

- [Início Rápido](quickstart.md) — conectar-se e fazer as primeiras chamadas.
- [Recursos](resources.md) — a lista completa dos clientes de recursos disponíveis.
- [Modelos](models.md) — os modelos pydantic usados para entrada e saída.
- [Erros](errors.md) — a hierarquia de exceções.
- [Referência da API](reference.md) — documentação de referência gerada automaticamente.