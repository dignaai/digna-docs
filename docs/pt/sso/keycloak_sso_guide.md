---
title: Keycloak SSO – Integração de Single Sign-On | Documentação digna
description: Configure Single Sign-On para digna com Keycloak usando OpenID Connect — configuração de realm e cliente, autenticação do cliente, URIs de redirect válidos, client secret e a configuração correspondente no digna.
image: /assets/logo_square.png
keywords: digna sso, keycloak sso, keycloak oidc, realm, cliente confidencial, openid connect, provedor de identidade auto-hospedado
---

# Configurar SSO com Keycloak

O Keycloak é um provedor de identidade auto-hospedado e totalmente compatível com OIDC. Como você mesmo o executa, a URL de discovery é construída a partir do seu próprio nome de host e realm, e não de um domínio de fornecedor.

Este guia cobre o **lado do Keycloak**: criar o cliente e recolher os valores que o digna precisa. O lado do digna — `dashboard_config.toml`, testes e resolução de problemas — é o mesmo para todos os provedores e está descrito na [Visão Geral do Single Sign-On](overview.md).

---

## Antes de Começar

| Requisito | Observações |
|---|---|
| **Versão do Keycloak** | 17 ou posterior para os caminhos de URL usados aqui — veja a nota no Passo 4 |
| **Função no Keycloak** | `realm-admin` no realm de destino, ou um administrador do servidor |
| **Realm** | O realm ao qual seus usuários do digna pertencem, não necessariamente `master` |
| **URI de redirect do digna** | A URL para onde os usuários retornam após o login, ex.: `https://digna.yourdomain.com/oidc/callback` |

---

## Passo 1: Selecionar o Realm

1. Abra o console de administração do Keycloak
2. Use o seletor de realm no canto superior esquerdo para mudar para o realm em que seus usuários estão

!!! warning "Não Use o Realm master"

    O realm `master` destina-se à administração do próprio Keycloak. Clientes de aplicações pertencem a um realm dedicado; colocar o digna no `master` dá aos seus usuários um caminho para o console de administração do Keycloak.

---

## Passo 2: Criar o Cliente

1. Vá para **Clients** e clique em **Create client**
2. Configure:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — torna-se `DIGNA_OIDC_CLIENT_ID`
3. Clique em **Next**
4. Na etapa **Capability config**, ative **Client authentication** (**On**)
5. Deixe **Standard flow** habilitado; os outros fluxos não são necessários
6. Clique em **Next**

!!! warning "Client Authentication Deve Estar Ativado"

    Com **Client authentication** desativado, o Keycloak cria um cliente *público*, que não tem nenhuma credencial — a aba **Credentials** do Passo 4 não existirá. O digna precisa de um cliente confidencial. Essa opção pode ser alterada após a criação, caso você erre.

---

## Passo 3: Definir o URI de Redirect

Na etapa **Login settings** (ou depois, na aba **Settings**):

1. **Valid redirect URIs**: insira sua URL de callback do digna:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: deixe vazio, ou defina como `+` para espelhar os URIs de redirect
3. Clique em **Save**

!!! tip "Evite Curingas"

    O Keycloak aceita padrões como `https://digna.yourdomain.com/*`. Um curinga permite que qualquer caminho nesse host receba um código de autorização, portanto prefira a URL de callback exata.

---

## Passo 4: Recolher o Client Secret

1. Abra a aba **Credentials**
2. Confirme que **Client Authenticator** está como *Client Id and Secret*
3. Copie o **Client secret** → torna-se `DIGNA_OIDC_CLIENT_SECRET`

O secret continua disponível aqui e pode ser gerado novamente com **Regenerate**.

---

## Passo 5: Construir a URL de Discovery

Substitua pelo seu host do Keycloak e pelo nome do realm:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Por exemplo:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 e Anteriores Incluem /auth"

    Antes do Keycloak 17, todos os endpoints ficavam sob um prefixo `/auth`:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Distribuições que definem `KC_HTTP_RELATIVE_PATH=/auth` mantêm o layout antigo também nas versões atuais. Se a URL sem `/auth` retornar 404, tente com ele.

Abra a URL em um navegador antes de continuar. Um documento JSON confirma que o host e o realm estão corretos.

---

## Passo 6: Configurar o digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Login with Keycloak"
```

### `config.toml`

```toml
[oidc_clients.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

A `key` em ambos os arquivos deve coincidir — `keycloak` aqui. Observe que ela não precisa ser igual ao **Client ID** do Keycloak, embora mantê-los iguais facilite o acompanhamento.

---

## Passo 7: Testar

Reinicie o backend e o servidor web, depois abra o dashboard. Veja [Teste de Login](overview.md#testing-login) para a lista completa de verificação.

---

## Resolução de Problemas do Keycloak

### Invalid parameter: redirect_uri

A URL de callback não está coberta por **Valid redirect URIs**. O Keycloak registra no log do servidor o URI que recebeu, que é a forma mais rápida de ver a divergência exata.

### A Aba Credentials Não Aparece

O cliente é público. Ative **Client authentication** em **Settings → Capability config**.

### 404 na URL de Discovery

Ou o nome do realm está errado, ou a implantação usa o prefixo `/auth`. Verifique a lista de realms no console de administração e tente as duas formas de URL.

### unauthorized_client ou invalid_client

**Standard flow** está desabilitado em **Capability config**, ou o secret foi gerado novamente no Keycloak sem atualizar `config.toml`.

### Erros de Certificado no Backend

Um Keycloak auto-hospedado por trás de um certificado privado ou autoassinado fará falhar a chamada HTTPS de saída do digna para a URL de discovery. Instale a CA emissora no repositório de confiança da máquina que executa o backend do digna.

---

## Veja Também

- [Visão Geral do Single Sign-On](overview.md) — referência de configuração, testes e resolução geral de problemas
- [Keycloak: Protegendo aplicações](https://www.keycloak.org/docs/latest/securing_apps/)
