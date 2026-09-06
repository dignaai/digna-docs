# Configurar SSO com o Google Workspace

A plataforma de identidade do Google é compatível com OIDC e usa uma única URL de descoberta well-known para todos os clientes, portanto os únicos valores por organização são o client ID e o client secret.

Este guia cobre o **lado do Google**: criar o cliente OAuth e coletar os valores que o digna precisa. O lado do digna — `dashboard_config.toml`, testes e solução de problemas — é o mesmo para todos os provedores e está descrito na [Visão geral do Single Sign-On](overview.md).

---

## Antes de começar

| Requisito | Observações |
|---|---|
| **Projeto do Google Cloud** | Qualquer projeto na mesma organização do seu domínio Workspace |
| **Função** | Editor ou Owner no projeto |
| **URI de redirecionamento do digna** | A URL para a qual os usuários retornam após o login, por exemplo `https://digna.yourdomain.com/oidc/callback` |

---

## Passo 1: Configurar a tela de consentimento OAuth

O Google não emitirá credenciais até que a tela de consentimento exista.

1. Abra o [Google Cloud Console](https://console.cloud.google.com) e selecione seu projeto
2. Vá para **APIs & Services → OAuth consent screen**
3. Escolha o tipo de usuário:
   - **Internal** — somente contas do seu domínio Workspace podem fazer login. Recomendado.
   - **External** — qualquer conta do Google pode tentar fazer login.
4. Preencha o nome do app, o e-mail de suporte ao usuário e o e-mail de contato do desenvolvedor
5. Na etapa **Scopes**, adicione `openid`, `.../auth/userinfo.email` e `.../auth/userinfo.profile`
6. Salve

!!! warning "Aplicativos externos devem ser publicados"

    Uma tela de consentimento **External** começa com status *Testing*, onde apenas as contas explicitamente adicionadas à lista de test-users podem completar um login. Todo mundo vê a mensagem "digna has not completed the Google verification process". Ou coloque o app em **In production** em **Publishing status**, ou use **Internal** — que não tem essa restrição e é a escolha correta para uma implantação apenas para Workspace.

---

## Passo 2: Criar o cliente OAuth

1. Vá para **APIs & Services → Credentials**
2. Clique em **Create Credentials → OAuth client ID**
3. Defina **Application type** como **Web application**
4. Dê um nome, por exemplo `digna`
5. Em **Authorized redirect URIs**, clique em **Add URI** e insira:

```
https://digna.yourdomain.com/oidc/callback
```

6. Clique em **Create**

!!! note "Origens JavaScript Autorizadas Não São Necessárias"

    O digna troca o authorization code a partir do backend, não do navegador, portanto o campo **Authorized JavaScript origins** pode ser deixado vazio. Apenas o redirect URI importa.

---

## Passo 3: Coletar as credenciais

O diálogo que aparece após a criação mostra:

- **Client ID** — termina em `.apps.googleusercontent.com` → torna-se `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → torna-se `DIGNA_OIDC_CLIENT_SECRET`

Ambos continuam recuperáveis posteriormente na página de detalhes da credencial, ao contrário da maioria dos outros provedores.

---

## Passo 4: A URL de descoberta

O Google usa uma URL de descoberta única para todos os clientes — não há nada para substituir:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Passo 5: Configurar o digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Entrar com o Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

A `key` em ambos os arquivos deve corresponder — `google` aqui.

---

## Passo 6: Teste

Reinicie o backend e o servidor web, depois abra o dashboard. Veja [Testando o login](overview.md#testing-login) para a lista completa de verificação.

---

## Solução de problemas do Google Workspace

### Erro 400: redirect_uri_mismatch

O URI em `DIGNA_OIDC_REDIRECT_URI` não está na lista de **Authorized redirect URIs**, ou difere por uma barra final ou esquema. A página de erro do Google mostra o URI que recebeu — compare-o caractere por caractere com o registrado.

### Este aplicativo está bloqueado / não concluiu a verificação

A tela de consentimento é **External** e ainda está em *Testing*. Publique-a, ou altere o app para **Internal**.

### Acesso bloqueado: Authorization Error

A conta que está tentando fazer login está fora do seu domínio Workspace enquanto a tela de consentimento é **Internal**. Esse é o comportamento esperado — apps Internal aceitam apenas contas da organização.

### Alterações levam vários minutos

O Google propaga mudanças em credenciais e na tela de consentimento de forma assíncrona. Um redirect URI recém-adicionado pode levar alguns minutos para entrar em vigor; se uma mudança parecer ignorada, aguarde e tente novamente antes de investigar mais a fundo.

---

## Veja também

- [Visão geral do Single Sign-On](overview.md) — referência de configuração, testes e solução de problemas geral
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)