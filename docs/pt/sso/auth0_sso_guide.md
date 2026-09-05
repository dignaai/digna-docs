---
title: Auth0 SSO – Integração de Single Sign-On | Documentação digna
description: Configure Single Sign-On para digna com Auth0 usando OpenID Connect — configuração de Regular Web Application, URLs de callback permitidos, credenciais do cliente, domínio do tenant e a configuração correspondente no digna.
image: /assets/logo_square.png
keywords: digna sso, auth0 sso, auth0 oidc, aplicação web regular, urls de callback, openid connect, autenticação empresarial
---

# Configurar SSO com Auth0

Auth0 é compatível com OIDC e expõe um endpoint de discovery por tenant. O principal a acertar é o domínio do tenant, que aparece na URL de discovery e muda se você ativar um domínio personalizado.

Este guia cobre o **lado do Auth0**: criar a aplicação e recolher os valores que o digna precisa. O lado do digna — `dashboard_config.toml`, testes e resolução de problemas — é o mesmo para todos os provedores e está descrito na [Visão Geral do Single Sign-On](overview.md).

---

## Antes de Começar

| Requisito | Observações |
|---|---|
| **Função no Auth0** | Administrador no tenant |
| **Domínio do tenant** | ex.: `yourcompany.eu.auth0.com` — o segmento de região é importante |
| **URI de redirect do digna** | A URL para onde os usuários retornam após o login, ex.: `https://digna.yourdomain.com/oidc/callback` |

---

## Passo 1: Criar a Aplicação

1. Faça login no [Painel do Auth0](https://manage.auth0.com)
2. Vá para **Applications → Applications**
3. Clique em **Create Application**
4. Nomeie como `digna` e escolha **Regular Web Applications**
5. Clique em **Create**

!!! warning "Escolha 'Regular Web Applications'"

    *Single Page Application* e *Native* criam clientes públicos sem secret. O digna realiza a troca de código a partir do seu backend e precisa de um cliente confidencial, então **Regular Web Applications** é o tipo correto. Ao contrário de alguns provedores, o Auth0 permite alterar o tipo depois em **Settings → Application Type**.

---

## Passo 2: Adicionar a URL de Callback

Na aba **Settings** da aplicação:

1. Encontre **Allowed Callback URLs**
2. Insira sua URL de callback do digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. Opcionalmente defina **Allowed Logout URLs** para a URL do seu dashboard
4. Role até o final e clique em **Save Changes**

!!! note "Separadas por vírgulas, não por novas linhas"

    O Auth0 aceita várias URLs de callback neste campo, separadas por vírgulas. Uma lista separada apenas por quebras de linha é interpretada como uma única URL malformada e não corresponde silenciosamente a nada.

---

## Passo 3: Recolher as Credenciais

Ainda em **Settings**, no painel **Basic Information**:

- **Domain** → entra na URL de discovery
- **Client ID** → torna-se `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → torna-se `DIGNA_OIDC_CLIENT_SECRET` (clique para revelar)

---

## Passo 4: Confirmar o Grant Type

1. Vá para **Settings → Advanced Settings → Grant Types**
2. Confirme que **Authorization Code** está marcado

Ele vem habilitado por padrão para Regular Web Applications. Se estiver desmarcado, o login do digna falha com `unauthorized_client`.

---

## Passo 5: Construir a URL de Discovery

Substitua o **Domain** do Passo 3:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Por exemplo:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Domínios Personalizados Alteram o Issuer"

    Se o seu tenant usa um domínio personalizado como `login.yourcompany.com`, use esse domínio na URL de discovery. Misturar os dois — o domínio canônico na URL de discovery e o personalizado no navegador — produz uma incompatibilidade de issuer, e o token é rejeitado após um login que, por outro lado, foi bem-sucedido.

---

## Passo 6: Configurar o digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Login with Auth0"
```

### `config.toml`

```toml
[oidc.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

A `key` em ambos os arquivos deve coincidir — `auth0` aqui.

---

## Passo 7: Testar

Reinicie o backend e o servidor web, depois abra o dashboard. Veja [Teste de Login](overview.md#testing-login) para a lista completa de verificação.

---

## Resolução de Problemas do Auth0

### URL de Callback incompatível

A página de erro do Auth0 indica a URL que recebeu. Adicione-a em **Allowed Callback URLs**, verificando se as entradas estão separadas por vírgulas.

### unauthorized_client

**Authorization Code** não está habilitado em **Advanced Settings → Grant Types**, ou o tipo de aplicação não é Regular Web Applications.

### Acesso negado após um login bem-sucedido

Uma Rule, Action ou trigger pós-login no tenant está rejeitando o usuário. Verifique **Actions → Flows → Login** e os logs do tenant em **Monitoring → Logs**, que mostram o motivo exato.

### Incompatibilidade do Issuer

A URL de discovery e o domínio para o qual o navegador foi enviado diferem — geralmente o domínio canônico do tenant versus um domínio personalizado. Use um de forma consistente.

---

## Veja Também

- [Visão Geral do Single Sign-On](overview.md) — referência de configuração, testes e resolução geral de problemas
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)