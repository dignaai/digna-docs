---
title: OneLogin SSO – Integração de Single Sign-On | Documentação digna
description: Configure Single Sign-On para digna com OneLogin usando OpenID Connect — criação do aplicativo OIDC, URIs de redirect, credenciais do cliente, autenticação do endpoint de token e a configuração correspondente no digna.
image: /assets/logo_square.png
keywords: digna sso, onelogin sso, onelogin oidc, openid connect, autenticação do endpoint de token, autenticação empresarial
---

# Configurar SSO com OneLogin

O OneLogin é compatível com OIDC. Sua característica distintiva é que o tipo de conector é escolhido em um catálogo quando o aplicativo é criado e não pode ser alterado depois.

Este guia cobre o **lado do OneLogin**: criar o aplicativo e recolher os valores que o digna precisa. O lado do digna — `dashboard_config.toml`, testes e resolução de problemas — é o mesmo para todos os provedores e está descrito na [Visão Geral do Single Sign-On](overview.md).

---

## Antes de Começar

| Requisito | Observações |
|---|---|
| **Função no OneLogin** | Proprietário da conta ou um administrador com permissão para adicionar aplicativos |
| **Subdomínio** | ex.: `yourcompany.onelogin.com` |
| **URI de redirect do digna** | A URL para onde os usuários retornam após o login, ex.: `https://digna.yourdomain.com/oidc/callback` |

---

## Passo 1: Criar o Aplicativo OIDC

1. Faça login no portal de administração do OneLogin
2. Vá para **Applications → Applications**
3. Clique em **Add App**
4. Pesquise por `OpenId Connect` e selecione o conector **OpenId Connect (OIDC)**
5. Defina o **Display Name** como `digna`
6. Clique em **Save**

!!! warning "O Tipo de Conector É Fixado na Criação"

    O OneLogin tem entradas de catálogo separadas para SAML e OIDC, e um aplicativo não pode ser convertido de um para o outro. Se você escolher um conector SAML por engano, exclua o aplicativo e adicione-o novamente — não há nenhuma configuração para trocar de protocolo.

---

## Passo 2: Configurar o URI de Redirect

1. Abra a aba **Configuration**
2. Em **Redirect URI's**, insira sua URL de callback do digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. Opcionalmente defina **Post Logout Redirect URIs** para a URL do seu dashboard
4. Clique em **Save**

!!! note "Um URI por Linha"

    Ao contrário de provedores que esperam uma lista separada por vírgulas, o campo **Redirect URI's** do OneLogin recebe um URI por linha.

---

## Passo 3: Definir o Tipo de Aplicativo e o Método de Autenticação

1. Abra a aba **SSO**
2. Confirme que **Application Type** está como *Web*
3. Defina **Token Endpoint → Authentication Method** como *POST* (`client_secret_post`) ou *Basic* (`client_secret_basic`)

!!! warning "Não Escolha None"

    Definir o método de autenticação como *None* torna o aplicativo um cliente público sem secret, e a troca de código no backend do digna será rejeitada. Tanto POST quanto Basic funcionam.

---

## Passo 4: Recolher as Credenciais

Ainda na aba **SSO**:

- **Client ID** → torna-se `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → torna-se `DIGNA_OIDC_CLIENT_SECRET` (clique em **Show client secret**)

A página também mostra a **Issuer URL**, que confirma a URL de discovery da próxima etapa.

---

## Passo 5: Atribuir Usuários

1. Abra a aba **Access**
2. Adicione as funções ou grupos cujos membros podem usar o digna
3. Clique em **Save**

!!! note "Usuários Não Atribuídos São Recusados Após o Login"

    Como na maioria dos provedores, o OneLogin primeiro autentica o usuário e depois verifica a autorização. Um usuário não atribuído faz login com sucesso e em seguida é recusado, o que parece um erro do digna, e não uma decisão de controle de acesso.

---

## Passo 6: Construir a URL de Discovery

Substitua pelo seu subdomínio do OneLogin:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Por exemplo:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "O /2 É a Versão da API"

    A implementação atual de OIDC do OneLogin fica em `/oidc/2/`. Documentações mais antigas mostram `/oidc/` sem versão, o que aponta para a primeira versão, já descontinuada. Em caso de dúvida, verifique a **Issuer URL** na aba SSO — a URL de discovery é o issuer mais `/.well-known/openid-configuration`.

---

## Passo 7: Configurar o digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Login with OneLogin"
```

### `config.toml`

```toml
[oidc_clients.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

A `key` em ambos os arquivos deve coincidir — `onelogin` aqui.

---

## Passo 8: Testar

Reinicie o backend e o servidor web, depois abra o dashboard. Veja [Teste de Login](overview.md#testing-login) para a lista completa de verificação.

---

## Resolução de Problemas do OneLogin

### redirect_uri did not match

A URL de callback está faltando em **Configuration → Redirect URI's**, ou as entradas foram separadas por vírgulas em vez de quebras de linha.

### invalid_client na Etapa do Token

**Token Endpoint → Authentication Method** está definido como *None*, ou o client secret em `config.toml` está desatualizado. Revele o secret na aba **SSO** e compare.

### O Aplicativo Não Aparece para os Usuários

Nenhuma função ou grupo recebeu acesso na aba **Access**.

### 404 na URL de Discovery

O subdomínio está errado, ou a URL omite `/oidc/2/`. Compare com a **Issuer URL** exibida na aba SSO.

---

## Veja Também

- [Visão Geral do Single Sign-On](overview.md) — referência de configuração, testes e resolução geral de problemas
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)
