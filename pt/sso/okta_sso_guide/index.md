# Configurar SSO com Okta

O Okta é compatível com OIDC, com um detalhe que pega a maioria das primeiras integrações: uma org do Okta expõe mais de um servidor de autorização, e cada um tem sua própria URL de discovery.

Este guia cobre o **lado do Okta**: criar a integração de aplicativo e recolher os valores que o digna precisa. O lado do digna — `dashboard_config.toml`, testes e resolução de problemas — é o mesmo para todos os provedores e está descrito na [Visão Geral do Single Sign-On](overview.md).

---

## Antes de Começar

| Requisito | Observações |
|---|---|
| **Função no Okta** | Super Administrator, ou uma função de administrador com permissão para criar integrações de aplicativo |
| **Domínio do Okta** | ex.: `yourcompany.okta.com`, ou um domínio personalizado, se configurado |
| **URI de redirect do digna** | A URL para onde os usuários retornam após o login, ex.: `https://digna.yourdomain.com/oidc/callback` |

---

## Passo 1: Criar a Integração de Aplicativo

1. Faça login no Okta Admin Console
2. Vá para **Applications → Applications**
3. Clique em **Create App Integration**
4. Selecione:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Clique em **Next**

!!! warning "O Tipo de Aplicativo Não Pode Ser Alterado"

    Escolher *Single-Page Application* em vez de *Web Application* cria um cliente público sem secret, e a troca de código no backend do digna falhará com `invalid_client`. O tipo é fixado na criação — uma escolha errada significa excluir o aplicativo e começar de novo.

---

## Passo 2: Configurar a Integração

1. **App integration name**: `digna`
2. **Grant type**: deixe *Authorization Code* selecionado
3. **Sign-in redirect URIs**: insira sua URL de callback do digna:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: opcional
5. Em **Assignments**, escolha quem pode usar a integração — um grupo específico é mais seguro do que *Allow everyone in your organization to access*
6. Clique em **Save**

!!! note "A Atribuição É Obrigatória"

    O Okta autentica o usuário e depois verifica se ele está atribuído ao aplicativo. Um usuário não atribuído chega à página de login do Okta, faz login com sucesso e é recusado no redirect de volta. Se o login funciona para você, mas não para colegas, a atribuição é a primeira coisa a verificar.

---

## Passo 3: Recolher as Credenciais

Na aba **General** do aplicativo, em **Client Credentials**:

- **Client ID** → torna-se `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → torna-se `DIGNA_OIDC_CLIENT_SECRET` (clique no ícone de olho para revelar)

---

## Passo 4: Escolher o Servidor de Autorização

Esta é a etapa que determina sua URL de discovery. Vá para **Security → API** para ver os servidores de autorização da sua org.

**Servidor de autorização da org** — emite tokens para a própria org do Okta:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Servidor de autorização personalizado** — incluindo o que o Okta cria com o nome `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Para o servidor integrado, `<auth_server_id>` é literalmente `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Qual Escolher?"

    Use o servidor de autorização da **org**, a menos que sua organização já padronize um servidor personalizado para políticas de acesso a APIs. Contas Okta Developer usam `default` por padrão; muitas orgs corporativas o desabilitam. Abra as duas URLs em um navegador — aquela que retorna JSON em vez de um erro é a que está disponível para você.

---

## Passo 5: Configurar o digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

### `config.toml`

```toml
[oidc_clients.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

A `key` em ambos os arquivos deve coincidir — `okta` aqui.

---

## Passo 6: Testar

Reinicie o backend e o servidor web, depois abra o dashboard. Veja [Teste de Login](overview.md#testing-login) para a lista completa de verificação.

---

## Resolução de Problemas do Okta

### The redirect URI Is Not Registered

O Okta indica no erro o URI problemático. Compare-o com **General → Sign-in redirect URIs**; o Okta compara a string completa, incluindo qualquer barra final.

### User Is Not Assigned to the Client Application

A conta não está na lista de atribuições do aplicativo. Adicione o usuário ou o grupo dele em **Assignments**.

### 400 Bad Request: Servidor de Autorização Inválido

O `<auth_server_id>` na URL de discovery não existe — na maioria das vezes `default`, em uma org onde ele foi removido. Verifique em **Security → API** os servidores realmente disponíveis.

### invalid_client na Etapa do Token

A integração foi criada como Single-Page Application e não tem client secret. Recrie-a como Web Application.

---

## Veja Também

- [Visão Geral do Single Sign-On](overview.md) — referência de configuração, testes e resolução geral de problemas
- [Okta: OpenID Connect e OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)