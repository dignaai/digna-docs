# Configurar SSO com AD FS

O Active Directory Federation Services é a opção on-premises: seus próprios servidores emitem os tokens, e a URL de discovery é o seu próprio nome de host. O AD FS suporta OpenID Connect a partir do **Windows Server 2016**.

Este guia cobre o **lado do AD FS**: criar o grupo de aplicativos e recolher os valores que o digna precisa. O lado do digna — `dashboard_config.toml`, testes e resolução de problemas — é o mesmo para todos os provedores e está descrito na [Visão Geral do Single Sign-On](overview.md).

---

## Antes de Começar

| Requisito | Observações |
|---|---|
| **Versão do AD FS** | Windows Server 2016 ou posterior — versões anteriores não têm suporte a OIDC |
| **Acesso** | Administrador local no servidor AD FS |
| **Nome do serviço de federação** | ex.: `adfs.yourdomain.com` |
| **URI de redirect do digna** | A URL para onde os usuários retornam após o login, ex.: `https://digna.yourdomain.com/oidc/callback` |

---

## Passo 1: Criar o Grupo de Aplicativos

1. No servidor AD FS, abra o **AD FS Management**
2. Clique com o botão direito em **Application Groups** e escolha **Add Application Group**
3. Insira `digna` como nome
4. Em **Standalone applications** — ou **Client-Server applications**, dependendo da sua versão — selecione **Server application accessing a web API**
5. Clique em **Next**

---

## Passo 2: Configurar o Aplicativo de Servidor

1. **Name**: `digna backend`
2. **Client Identifier**: o AD FS gera um GUID. Copie-o — ele se torna `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: insira sua URL de callback do digna e clique em **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Clique em **Next**

!!! warning "Clique em Add, Não Apenas em Next"

    O campo de URI de redirect tem seu próprio botão **Add**. Digitar um URI e clicar em **Next** sem pressionar **Add** o descarta, e o assistente não dá nenhum aviso. Confirme que o URI aparece na lista abaixo do campo antes de continuar.

---

## Passo 3: Gerar o Segredo Compartilhado

1. Marque **Generate a shared secret**
2. Copie o segredo gerado → torna-se `DIGNA_OIDC_CLIENT_SECRET`
3. Clique em **Next**

!!! warning "O Segredo É Exibido Uma Única Vez"

    O AD FS exibe o segredo compartilhado apenas nesta página do assistente e não pode mostrá-lo novamente. Se você o perder, redefina-o depois nas propriedades do grupo de aplicativos.

---

## Passo 4: Configurar a Web API

1. **Identifier**: insira o mesmo client identifier do Passo 2 e clique em **Add**
2. Clique em **Next**
3. Escolha uma **Access Control Policy** — *Permit everyone* é o ponto de partida mais simples; restrinja-a a um grupo em produção
4. Clique em **Next**

---

## Passo 5: Conceder os Scopes Permitidos

Na etapa **Configure Application Permissions**, marque:

- `openid`
- `profile`
- `email`

Depois clique em **Next** e conclua o assistente.

!!! warning "openid Não Vem Marcado por Padrão"

    Em algumas versões, o AD FS pré-seleciona apenas `user_impersonation`. Sem `openid`, o endpoint de token retorna um access token OAuth em vez de um ID token, e o digna não consegue identificar o usuário.

---

## Passo 6: Confirmar o Endpoint de Discovery

Substitua pelo nome do seu serviço de federação:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Por exemplo:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Abra-a em um navegador. Um documento JSON confirma que o OIDC está habilitado e que o nome de host está correto.

!!! note "O Backend Deve Confiar no Certificado"

    Uma autoridade certificadora interna é comum no AD FS. A máquina que executa o backend do digna faz sua própria chamada HTTPS de saída para esta URL, portanto a CA emissora deve estar no repositório de confiança dessa máquina — não apenas nos navegadores das pessoas que fazem login.

---

## Passo 7: Configurar o digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Login with Active Directory"
```

### `config.toml`

```toml
[oidc_clients.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

A `key` em ambos os arquivos deve coincidir — `adfs` aqui.

---

## Passo 8: Testar

Reinicie o backend e o servidor web, depois abra o dashboard. Veja [Teste de Login](overview.md#testing-login) para a lista completa de verificação.

---

## Resolução de Problemas do AD FS

### MSIS9611: O Cliente Não Tem Permissão para Acessar o Recurso

O identificador da web API no Passo 4 não corresponde ao client identifier, ou os scopes do Passo 5 não foram concedidos. Ambos podem ser editados nas propriedades do grupo de aplicativos.

### MSIS9602: redirect_uri Inválido

O URI foi digitado, mas não adicionado com o botão **Add**, ou difere de `DIGNA_OIDC_REDIRECT_URI`. Verifique **Application Groups → digna → digna backend → Properties**.

### Nenhum ID Token É Retornado

O scope `openid` está faltando nas permissões do aplicativo.

### O Backend Não Consegue Acessar a URL de Discovery

Ou o DNS no host do backend não resolve o nome do serviço de federação, ou o certificado do AD FS não é confiável ali. Teste com `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` a partir do próprio servidor do digna.

### Eventos a Verificar

O servidor AD FS registra as falhas em **Applications and Services Logs → AD FS → Admin** no Event Viewer, geralmente com um motivo mais específico do que o navegador mostra.

---

## Veja Também

- [Visão Geral do Single Sign-On](overview.md) — referência de configuração, testes e resolução geral de problemas
- [Microsoft: cenários de OpenID Connect do AD FS](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)