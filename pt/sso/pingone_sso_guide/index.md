# Configurar SSO com PingOne

O PingOne é compatível com OIDC. Dois dos seus valores exigem cuidado: o **ID do ambiente**, que aparece em todas as URLs de endpoint, e o **domínio regional**, que difere entre os tenants da América do Norte, Europa, Canadá, Ásia-Pacífico e Austrália.

Este guia cobre o **lado do PingOne**: criar o aplicativo e recolher os valores que o digna precisa. O lado do digna — `dashboard_config.toml`, testes e resolução de problemas — é o mesmo para todos os provedores e está descrito na [Visão Geral do Single Sign-On](overview.md).

---

## Antes de Começar

| Requisito | Observações |
|---|---|
| **Função no PingOne** | Environment Admin ou Identity Data Admin no ambiente de destino |
| **Ambiente** | O ambiente do PingOne ao qual seus usuários do digna pertencem |
| **URI de redirect do digna** | A URL para onde os usuários retornam após o login, ex.: `https://digna.yourdomain.com/oidc/callback` |

---

## Passo 1: Criar o Aplicativo

1. Faça login no console de administração do PingOne e selecione seu ambiente
2. Vá para **Applications → Applications**
3. Clique no botão **+**
4. Insira `digna` como **Application Name**
5. Selecione **OIDC Web App**
6. Clique em **Save**

!!! warning "Escolha OIDC Web App, Não Single-Page App"

    *Single-Page App* e *Native App* criam clientes públicos que não podem guardar um secret. O digna troca o código de autorização a partir do seu backend e precisa do tipo confidencial **OIDC Web App**.

---

## Passo 2: Configurar o URI de Redirect

1. Abra a aba **Configuration** do aplicativo
2. Clique no ícone de lápis para editar
3. Confirme que **Response Type** é *Code* e **Grant Type** é *Authorization Code*
4. Em **Redirect URIs**, insira sua URL de callback do digna:

```
https://digna.yourdomain.com/oidc/callback
```

5. Defina **Token Endpoint Authentication Method** como *Client Secret Post* ou *Client Secret Basic*
6. Clique em **Save**

---

## Passo 3: Habilitar o Aplicativo

Na linha do aplicativo ou no painel de detalhes, coloque a chave em **enabled**.

!!! warning "Novos Aplicativos Começam Desabilitados"

    O PingOne cria aplicativos em estado desabilitado. Um aplicativo desabilitado produz um erro na etapa de autorização que não menciona a chave, por isso vale a pena confirmar isso antes de depurar qualquer outra coisa.

---

## Passo 4: Conceder os Scopes

1. Abra a aba **Resources**
2. Confirme que `openid` está concedido e adicione `profile` e `email` a partir do recurso **OpenID Connect**
3. Clique em **Save**

---

## Passo 5: Atribuir Usuários

1. Abra a aba **Access**
2. Adicione a população ou os grupos cujos membros podem usar o digna
3. Clique em **Save**

---

## Passo 6: Recolher as Credenciais e o ID do Ambiente

Na aba **Configuration**, expanda **General**:

- **Client ID** → torna-se `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → torna-se `DIGNA_OIDC_CLIENT_SECRET` (clique no ícone de olho)
- **Environment ID** → entra na URL de discovery

A mesma aba lista o **OIDC Discovery Endpoint** pronto, que você pode copiar diretamente em vez de montá-lo à mão.

---

## Passo 7: Construir a URL de Discovery

Substitua pelo ID do ambiente e pelo domínio da sua região:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Região | Domínio |
|---|---|
| América do Norte | `auth.pingone.com` |
| Europa | `auth.pingone.eu` |
| Canadá | `auth.pingone.ca` |
| Ásia-Pacífico | `auth.pingone.asia` |
| Austrália | `auth.pingone.com.au` |

Para um ambiente europeu:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Copie em Vez de Digitar"

    O domínio regional é o erro mais comum em uma integração com o PingOne, e uma região errada retorna um 404 em vez de uma mensagem útil. Use o valor de **OIDC Discovery Endpoint** do Passo 6.

---

## Passo 8: Configurar o digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Login with PingOne"
```

### `config.toml`

```toml
[oidc_clients.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

A `key` em ambos os arquivos deve coincidir — `pingone` aqui.

---

## Passo 9: Testar

Reinicie o backend e o servidor web, depois abra o dashboard. Veja [Teste de Login](overview.md#testing-login) para a lista completa de verificação.

---

## Resolução de Problemas do PingOne

### 404 na URL de Discovery

O domínio regional ou o ID do ambiente está errado. Compare com o **OIDC Discovery Endpoint** exibido na aba Configuration do aplicativo.

### NOT_FOUND ou Aplicativo Desabilitado

A chave do aplicativo do Passo 3 ainda está desligada.

### Incompatibilidade do URI de Redirect

O PingOne compara a string completa. Verifique em **Configuration → Redirect URIs** se há uma barra final ou uma diferença de esquema.

### O Login É Bem-Sucedido, mas Nenhuma Claim de E-mail Chega ao digna

Os scopes `email` e `profile` não foram concedidos na aba **Resources**.

### O Usuário Não Consegue Ver o Aplicativo

Nenhuma população ou grupo recebeu acesso na aba **Access**.

---

## Veja Também

- [Visão Geral do Single Sign-On](overview.md) — referência de configuração, testes e resolução geral de problemas
- [PingOne: configuração de aplicativos OIDC](https://docs.pingidentity.com/pingone/)