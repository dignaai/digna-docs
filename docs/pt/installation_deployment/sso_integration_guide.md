---
title: Guia de Integração de Single Sign-On (SSO) | Documentação digna
description: Guia passo a passo para configurar Single Sign-On (SSO) para digna usando OpenID Connect (OIDC). Abrange configuração do dashboard e backend, testes, solução de problemas e provedores de identidade suportados incluindo Microsoft Entra ID, Google Workspace e Okta.
image: /assets/logo_square.png
keywords:
  - digna sso
  - single sign-on
  - integração oidc
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - integração okta
  - autenticação corporativa
lang: pt
robots: index, follow
og_title: digna Guia de Integração Single Sign-On (SSO)
og_description: Configure Single Sign-On para digna usando OpenID Connect. Configuração passo a passo para Microsoft Entra ID, Google Workspace, Okta e outros provedores compatíveis com OIDC.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Guia de Integração Single Sign-On

---

## Sumário

1. [Introdução e Visão Geral](#introduction-and-overview)
2. [Etapas de Configuração](#configuration-steps)
3. [Configuração do Dashboard](#dashboard-configuration)
4. [Configuração do Backend](#backend-configuration)
5. [Teste de Login](#testing-login)
6. [Solução de Problemas](#troubleshooting)
7. [Provedores Suportados](#supported-providers)

---

## Introdução e Visão Geral {: #introduction-and-overview }

Este guia fornece instruções passo a passo para integrar Single Sign-On (SSO) com a plataforma digna usando **OpenID Connect (OIDC)**.

### O que é SSO?

Single Sign-On permite que usuários entrem no digna com segurança usando suas credenciais corporativas por meio de provedores de identidade externos. Os usuários podem se autenticar com as credenciais da empresa em vez de gerenciar senhas separadas para o digna.

### Como Funciona

O SSO no digna é implementado usando o protocolo OIDC. Vários provedores de identidade podem ser configurados em paralelo ajustando dois arquivos de configuração principais:

- **`dashboard_config.toml`** — Controla a interface de login do frontend
- **`config.toml`** — Configura as conexões OIDC do backend

### Provedores Suportados {: #supported-providers-overview }

Os exemplos neste guia usam **Microsoft** e **Google**, mas **qualquer provedor compatível com OIDC** pode ser integrado seguindo a mesma estrutura.

Provedores OIDC comuns incluem:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Outros provedores de identidade compatíveis com OIDC

---

## Etapas de Configuração {: #configuration-steps }

A configuração de SSO requer atualizações em dois arquivos. Esta seção explica como configurar cada um.

### Visão Geral dos Arquivos de Configuração

| Arquivo | Local | Finalidade |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Interface de login do frontend |
| **config.toml** | `/config.toml` | Conexões OIDC do backend |

Ambos os arquivos devem ser configurados para que o SSO funcione corretamente.

---

## Configuração do Dashboard {: #dashboard-configuration }

### Local do Arquivo

```
dashboard/dashboard_config.toml
```

### Etapa 1: Adicionar Provedores OIDC

Adicione entradas sob o array `[[login.oidc]]` para cada provedor de identidade que deseja suportar.

**Exemplo com Microsoft e Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Etapa 2: Configurar Opções de Login

Especifique se o login por senha deve ser permitido:

```toml
[login]
usePassword = true
```

### Parâmetros de Configuração

#### Seção `[[login.oidc]]`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `key` | string | Sim | Identificador único para a conexão OIDC (deve corresponder ao key em config.toml) |
| `label` | string | Sim | Texto exibido no botão de login (por exemplo, "Login with Microsoft") |

#### Seção `[login]`

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `usePassword` | boolean | false | Permite login por senha além do SSO |

### Entendendo usePassword

**Se `usePassword = true`:**
- A tela de login mostra botões SSO (por exemplo, "Login with Microsoft")
- A tela de login também mostra campos de nome de usuário e senha
- Os usuários podem se autenticar por qualquer um dos métodos
- Permite configurações híbridas onde alguns usuários usam SSO e outros usam senha

**Se `usePassword = false` (ou omitido):**
- A tela de login mostra apenas os botões SSO
- Não há campos de nome de usuário/senha
- Apenas autenticação OIDC está disponível

> **💡 Dica**
>
> O login por senha só está disponível para usuários que foram criados com senha usando o comando `digna user add` ou via dashboard.

### Exemplo Completo

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## Configuração do Backend {: #backend-configuration }

### Local do Arquivo

```
/config.toml
```

(Diretório raiz de instalação do digna)

### Etapa 1: Adicionar Seções de Provedor OIDC

Cada provedor deve ter uma seção dedicada `[oidc.<key>]`. O key deve corresponder ao `key` definido em `dashboard_config.toml`.

### Configuração Microsoft

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Configuração Google

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Parâmetros de Configuração

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Sim | Client ID fornecido pelo provedor de identidade | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Sim | Client secret fornecido pelo provedor de identidade | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Sim | URL de callback após autenticação | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Sim | Endpoint de configuração OIDC | `https://login.microsoftonline.com/...` |

> **⚠️ Importante**
>
> Substitua os valores de placeholder (`<client_id>`, `<client_secret>`, `<tenant_id>`) pelas credenciais reais do portal do provedor de identidade.

### Redirect URI

A redirect URI deve ser a mesma na configuração do seu provedor de identidade:

```
http://localhost:5173/oidc/callback
```

Se o digna estiver hospedado em um domínio diferente, atualize conforme:
- Local: `http://localhost:5173/oidc/callback`
- Produção: `https://digna.yourdomain.com/oidc/callback`

### Exemplo Completo

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Teste de Login {: #testing-login }

Após concluir a configuração, verifique se o SSO está funcionando corretamente.

### Lista de Verificação Pré-Teste

Antes de testar, certifique-se de:

- [ ] `dashboard_config.toml` foi atualizado com provedores OIDC
- [ ] `config.toml` foi atualizado com credenciais OIDC
- [ ] Ambos os arquivos foram salvos
- [ ] As credenciais estão corretas (client ID, client secret)
- [ ] A redirect URI corresponde à URL da sua implantação
- [ ] O aplicativo no provedor de identidade está configurado com a redirect URI

### Etapas de Teste

#### Etapa 1: Reiniciar Serviços

Reinicie o backend e o servidor web do digna para aplicar as mudanças.

**Se estiver executando como serviço do Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Se estiver executando manualmente:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Se estiver usando IIS ou Tomcat:**
Reinicie o serviço do servidor web.

#### Etapa 2: Abrir Dashboard

Abra o dashboard do digna no seu navegador:

```
http://localhost:5173
```

(ou sua URL configurada do dashboard)

#### Etapa 3: Verificar Botões de Login

Verifique se os botões de login aparecem para cada provedor configurado:

- ✅ Deve ver o botão "Login with Microsoft"
- ✅ Deve ver o botão "Login with Google"
- ✅ (Se usePassword = true) Deve ver campos de usuário/senha

Se os botões não aparecerem:
- Verifique se `dashboard_config.toml` foi salvo
- Verifique se o serviço do dashboard foi reiniciado
- Verifique o console do navegador (F12) em busca de erros

#### Etapa 4: Testar Login SSO

Clique em um dos botões SSO (por exemplo, "Login with Microsoft"):

1. Você deve ser redirecionado para a página de login do provedor de identidade
2. Faça login com suas credenciais corporativas
3. Você deve ser redirecionado de volta ao digna
4. Você deve estar autenticado no digna

#### Etapa 5: Verificar Criação do Usuário

Após login SSO bem-sucedido:

- ✅ O usuário deve ser criado automaticamente no digna
- ✅ O usuário deve estar autenticado
- ✅ O perfil do usuário deve exibir suas credenciais do provedor de identidade
- ✅ Você deve ver o dashboard do digna

#### Etapa 6: Testar Login por Senha (Se Habilitado)

Se `usePassword = true`:

1. Faça logout do digna
2. Na página de login, insira usuário e senha
3. Você deve conseguir entrar com credenciais de senha

---

## Solução de Problemas {: #troubleshooting }

### Botões de Login Não Aparecem

**Sintomas:**
- Botões de login OIDC não visíveis na página de login
- Apenas campos de senha visíveis (se usePassword = true)

**Causas e Soluções:**
1. Verifique se `dashboard_config.toml` está no diretório `dashboard/`
2. Confirme se as seções `[[login.oidc]]` estão presentes com a sintaxe correta
3. Reinicie o serviço do dashboard
4. Limpe o cache do navegador (Ctrl+Shift+Delete ou Cmd+Shift+Delete)
5. Verifique o console do navegador (F12 → aba Console) por erros

---

### Erro de Incompatibilidade do Redirect URI

**Sintomas:**
- Após clicar no botão SSO, erro sobre "redirect_uri mismatch"
- Erro "The redirect URI is not registered"

**Causas e Soluções:**
1. Verifique se `DIGNA_OIDC_REDIRECT_URI` em `config.toml` está correto
2. Verifique se a redirect URI está registrada nas configurações do provedor de identidade
3. Garanta que ambos usem URLs idênticas (incluindo protocolo, domínio, caminho)
4. Procure por erros de digitação na redirect URI
5. Se estiver usando HTTPS, verifique se o certificado é válido

---

### Erro de Credenciais de Cliente Inválidas

**Sintomas:**
- Erro "Invalid client ID or secret"
- Autenticação falha com erro de credenciais

**Causas e Soluções:**
1. Verifique se `DIGNA_OIDC_CLIENT_ID` e `DIGNA_OIDC_CLIENT_SECRET` estão corretos
2. Assegure-se de que não há espaços extras ou caracteres indesejados
3. Verifique se as credenciais não expiraram ou foram revogadas
4. Reinicie o serviço do backend após atualizar a configuração
5. Verifique o console do provedor de identidade para confirmar que as credenciais estão ativas

---

### Login Congela ou Expira

**Sintomas:**
- Clicar no botão SSO não faz nada
- Timeout após alguns segundos
- Navegador mostra "Failed to connect" ou similar

**Causas e Soluções:**
1. Verifique se o backend do digna está em execução: `digna repo check`
2. Cheque a conectividade de rede com o provedor de identidade
3. Verifique se `DIGNA_OIDC_CONFIGURATION_URL` está acessível
4. Verifique regras de firewall que permitam conexões HTTPS de saída
5. Confirme se backend e dashboard conseguem se comunicar

---

### Usuários Não São Criados Automaticamente

**Sintomas:**
- Login SSO tem sucesso, mas usuário não é criado no digna
- Recebe erro de permissão após login SSO

**Causas e Soluções:**
1. Verifique se a configuração OIDC está correta
2. Confira se as permissões de usuário estão configuradas
3. Revise os logs do digna em busca de mensagens de erro
4. Reinicie o serviço do backend
5. Contate support@digna.ai se o problema persistir

---

## Provedores Suportados {: #supported-providers }

### Testados & Suportados

Os seguintes provedores OIDC foram testados e são conhecidos por funcionar:

| Provedor | URL de Configuração | Guia de Configuração |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Outros Provedores OIDC

Qualquer provedor que suporte OpenID Connect pode ser integrado. Informações necessárias:

- Client ID
- Client secret
- URL de configuração OpenID (geralmente em `/.well-known/openid-configuration`)
- Scopes suportados (tipicamente `openid profile email`)

Contacte support@digna.ai se precisar de ajuda para integrar um provedor específico.

---

## Boas Práticas

✅ **FAÇA:**
- Use HTTPS em produção (não HTTP)
- Armazene segredos de cliente com segurança (use variáveis de ambiente quando possível)
- Rodecie segredos periodicamente
- Teste primeiro em ambiente não-produtivo
- Documente quais provedores estão configurados
- Monitore logs de login para atividades incomuns
- Mantenha a configuração do provedor de identidade sincronizada com a configuração do digna

❌ **NÃO:**
- Armazene segredos de cliente no controle de versão
- Use URIs de redirect HTTP em produção
- Configure múltiplos provedores com a mesma key
- Deixe credenciais padrão/teste em produção
- Exponha arquivos de configuração contendo segredos
- Misture credenciais de desenvolvimento e produção

---

## Suporte

Precisa de ajuda com a configuração de SSO?

- 📧 **Email:** support@digna.ai
- 📚 **Documentação:** https://docs.digna.ai
- 🌐 **Website:** https://www.digna.ai

---

**Última Atualização:** 30 de agosto de 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**