---
title: Microsoft Entra ID SSO – Integração de Single Sign-On | Documentação digna
description: Configure Single Sign-On para digna com Microsoft Entra ID (antigo Azure AD) usando OpenID Connect — registro de aplicativo, URI de redirect, client secret, ID do tenant e a configuração correspondente no digna.
image: /assets/logo_square.png
keywords: digna sso, microsoft entra id, azure ad sso, integração oidc, registro de aplicativo, autenticação empresarial
---

# Configurar SSO com Microsoft Entra ID

O Microsoft Entra ID (antigo Azure Active Directory) é um provedor totalmente compatível com OIDC, então o digna se integra a ele por meio do endpoint de discovery padrão.

Este guia cobre o **lado do Entra ID**: registrar o aplicativo e recolher os quatro valores que o digna precisa. O lado do digna — `dashboard_config.toml`, testes e resolução de problemas — é o mesmo para todos os provedores e está descrito na [Visão Geral do Single Sign-On](overview.md).

---

## Antes de Começar

| Requisito | Observações |
|---|---|
| **Função no Entra ID** | Application Administrator, Cloud Application Administrator ou Global Administrator |
| **URI de redirect do digna** | A URL para onde os usuários retornam após o login, ex.: `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | O diretório no qual seus usuários fazem login |

---

## Passo 1: Registrar o Aplicativo

1. Faça login no [Microsoft Entra admin center](https://entra.microsoft.com)
2. Vá para **Identity → Applications → App registrations**
3. Clique em **New registration**
4. Configure:
   - **Name**: `digna` (exibido aos usuários na tela de consentimento)
   - **Supported account types**: *Accounts in this organizational directory only* para uma implantação single-tenant
5. Em **Redirect URI**, selecione a plataforma **Web** e insira sua URL de callback do digna:

```
https://digna.yourdomain.com/oidc/callback
```

6. Clique em **Register**

!!! warning "Importante"

    A plataforma deve ser **Web**, não *Single-page application*. O digna troca o código de autorização a partir do backend usando um client secret, o que o tipo de plataforma SPA não permite.

---

## Passo 2: Recolher os IDs do Cliente e do Tenant

Na página **Overview** do aplicativo, copie:

- **Application (client) ID** → torna-se `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → entra na URL de discovery

---

## Passo 3: Criar um Client Secret

1. Vá para **Certificates & secrets → Client secrets**
2. Clique em **New client secret**
3. Insira uma descrição e escolha uma validade
4. Clique em **Add**
5. Copie imediatamente a coluna **Value**

!!! warning "Copie o Value, Não o Secret ID"

    O **Value** é exibido apenas uma vez, nesta página, e não pode ser recuperado depois. O **Secret ID** ao lado parece semelhante, mas não é o secret — usá-lo produz um erro `invalid_client` no login. Se você sair da página antes de copiar, exclua o secret e crie um novo.

!!! tip "Dica"

    O Entra ID limita a validade dos secrets a 24 meses, então toda integração de SSO tem uma data de expiração. Anote-a em algum lugar onde você a verá — um secret expirado derruba o SSO para todos os usuários de uma só vez, sem nenhum aviso na página de login.

---

## Passo 4: Confirmar as Permissões de API

1. Vá para **API permissions**
2. Confirme que **Microsoft Graph → User.Read** (delegada) está presente — ela é adicionada por padrão

Os scopes `openid`, `profile` e `email` que o digna solicita fazem parte do conjunto padrão do OIDC e não precisam de concessão separada. Se o seu tenant exigir consentimento de administrador para todos os aplicativos, clique em **Grant admin consent for &lt;tenant&gt;**.

---

## Passo 5: Construir a URL de Discovery

Substitua o **Directory (tenant) ID** do Passo 2:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Use o Endpoint v2.0"

    O segmento `/v2.0/` é importante. O endpoint v1.0 em `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` emite tokens em um formato mais antigo e não retorna as claims OIDC padrão que o digna espera.

Abra a URL em um navegador antes de continuar. Um documento JSON confirma que o ID do tenant está correto.

---

## Passo 6: Configurar o digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"
```

### `config.toml`

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

A `key` em ambos os arquivos deve coincidir — `microsoft` aqui.

---

## Passo 7: Testar

Reinicie o backend e o servidor web, depois abra o dashboard. Veja [Teste de Login](overview.md#testing-login) para a lista completa de verificação.

---

## Resolução de Problemas do Entra ID

### AADSTS50011: Incompatibilidade do URI de Redirect

O URI em `DIGNA_OIDC_REDIRECT_URI` difere daquele registrado no Passo 1. O Entra ID compara a string completa, portanto uma barra final, `http` versus `https` ou uma porta diferente contam como incompatibilidade. Verifique **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Client Secret Inválido

Ou o **Secret ID** foi copiado em vez do **Value**, ou o secret expirou. Crie um novo secret e copie a coluna Value.

### AADSTS650057: Recurso Inválido

O registro do aplicativo foi excluído ou pertence a um tenant diferente daquele da URL de discovery. Confirme o Directory (tenant) ID na página Overview.

### Os Usuários Fazem Login, mas Nada Acontece

Se o tenant exigir consentimento de administrador e ele não tiver sido concedido, o redirect retorna sem um token utilizável. Conceda o consentimento de administrador em **API permissions**.

---

## Veja Também

- [Visão Geral do Single Sign-On](overview.md) — referência de configuração, testes e resolução geral de problemas
- [Microsoft: fluxo de código de autorização OAuth 2.0](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
