---
title: Visão Geral do Single Sign-On (SSO) | Documentação digna
description: Como o Single Sign-On funciona no digna usando OpenID Connect (OIDC). Abrange a configuração do dashboard e do backend, testes, resolução de problemas e links para guias de configuração por provedor para Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak, OneLogin, PingOne e AD FS.
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
  - autenticação empresarial
lang: pt
robots: index, follow
og_title: Guia de Integração de Single Sign-On (SSO) do digna
og_description: Configure Single Sign-On para o digna usando OpenID Connect. Configuração passo a passo para Microsoft Entra ID, Google Workspace, Okta e outros provedores de identidade compatíveis com OIDC.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Visão Geral do Single Sign-On

---

## Sumário

1. [Introdução e Visão Geral](#introduction-and-overview)
2. [Guias por Provedor](#provider-guides)
3. [Etapas de Configuração](#configuration-steps)
4. [Configuração do Dashboard](#dashboard-configuration)
5. [Configuração do Backend](#backend-configuration)
6. [Teste de Login](#testing-login)
7. [Resolução de Problemas](#troubleshooting)
8. [Provedores Suportados](#supported-providers)

---

## Introdução e Visão Geral {: #introduction-and-overview }

Este guia fornece instruções passo a passo para integrar Single Sign-On (SSO) à plataforma digna usando **OpenID Connect (OIDC)**.

### O Que é SSO?

O Single Sign-On permite que os usuários façam login no digna com segurança usando suas credenciais corporativas por meio de provedores de identidade externos. Os usuários podem se autenticar com suas credenciais corporativas em vez de gerenciar senhas separadas para o digna.

### Como Funciona

O SSO no digna é implementado usando o protocolo OIDC. Vários provedores de identidade podem ser configurados em paralelo ajustando dois arquivos de configuração principais:

- **`dashboard_config.toml`** — Controla a interface de login do frontend
- **`config.toml`** — Configura as conexões OIDC do backend

### Provedores Suportados {: #supported-providers-overview }

Os exemplos deste guia usam **Microsoft** e **Google**, mas **qualquer provedor compatível com OIDC** pode ser integrado seguindo a mesma estrutura.

---

## Guias por Provedor {: #provider-guides }

Todo provedor precisa dos mesmos quatro valores — um client ID, um client secret, um URI de redirect e uma URL de discovery —, mas cada um os coloca em um lugar diferente do seu console de administração, e vários têm uma etapa específica que os outros não têm. Os guias abaixo cobrem essa metade do trabalho; esta página cobre a metade do digna, que é idêntica para todos eles.

| Provedor | Guia | Vale a pena saber |
|---|---|---|
| **AD FS** | [Configurar SSO com AD FS](adfs_sso_guide.md) | Auto-hospedado; o único provedor aqui em que você controla o serviço de tokens |
| **Auth0** | [Configurar SSO com Auth0](auth0_sso_guide.md) | A URL de discovery é por tenant, e domínios personalizados a alteram |
| **Google Workspace** | [Configurar SSO com Google Workspace](google_workspace_sso_guide.md) | A tela de consentimento deve ser publicada antes que usuários que não são de teste possam fazer login |
| **Keycloak** | [Configurar SSO com Keycloak](keycloak_sso_guide.md) | Auto-hospedado; a URL de discovery é por realm |
| **Microsoft Entra ID** | [Configurar SSO com Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | O ID do tenant aparece na URL de discovery; os secrets expiram |
| **Okta** | [Configurar SSO com Okta](okta_sso_guide.md) | A escolha do servidor de autorização altera a URL de discovery |
| **OneLogin** | [Configurar SSO com OneLogin](onelogin_sso_guide.md) | O tipo de app OIDC deve ser escolhido na criação e não pode ser alterado |
| **PingOne** | [Configurar SSO com PingOne](pingone_sso_guide.md) | O ID do ambiente aparece na URL de discovery |

Qualquer outro provedor compatível com OIDC funciona da mesma forma — veja [Outros Provedores OIDC](#supported-providers).

---

## Etapas de Configuração {: #configuration-steps }

A configuração de SSO requer alterações em dois arquivos. Esta seção explica como configurar cada um deles.

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

### Passo 1: Adicionar Provedores OIDC

Adicione entradas no array `[[login.oidc]]` para cada provedor de identidade que você deseja suportar.

**Exemplo com Microsoft e Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Passo 2: Configurar as Opções de Login

Especifique se o login com senha deve ser permitido:

```toml
[login]
usePassword = true
```

### Parâmetros de Configuração

#### Seção `[[login.oidc]]`

| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `key` | string | Sim | Identificador único da conexão OIDC (deve corresponder à key em config.toml) |
| `label` | string | Sim | Texto exibido no botão de login (ex.: "Login with Microsoft") |

#### Seção `[login]`

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `usePassword` | boolean | false | Permite login com senha além do SSO |

### Entendendo o usePassword

**Se `usePassword = true`:**
- A tela de login mostra botões de SSO (ex.: "Login with Microsoft")
- A tela de login também mostra campos de nome de usuário e senha
- Os usuários podem se autenticar com qualquer um dos métodos
- Permite configurações híbridas em que alguns usuários usam SSO e outros usam senhas

**Se `usePassword = false` (ou omitido):**
- A tela de login mostra apenas botões de SSO
- Sem campos de nome de usuário/senha
- Apenas a autenticação OIDC está disponível

!!! tip "Dica"

    O login com senha só está disponível para usuários que foram criados com senha usando o comando `digna user add` ou pelo dashboard.

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

(Diretório raiz da instalação do digna)

### Passo 1: Adicionar Seções de Provedores OIDC

Cada provedor deve ter uma seção `[oidc_clients.<key>]` dedicada. A key deve corresponder à `key` definida em `dashboard_config.toml`.

### Configuração da Microsoft

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Configuração do Google

```toml
[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Parâmetros de Configuração

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Sim | Client ID do provedor de identidade | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Sim | Client secret do provedor de identidade | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Sim | URL de callback após a autenticação | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Sim | Endpoint de configuração OIDC | `https://login.microsoftonline.com/...` |

!!! warning "Importante"

    Substitua os valores de exemplo (`<client_id>`, `<client_secret>`, `<tenant_id>`) pelas credenciais reais do portal de desenvolvedor do seu provedor de identidade.

### URI de Redirect

O URI de redirect deve ser o mesmo na configuração do seu provedor de identidade:

```
http://localhost:5173/oidc/callback
```

Se o digna estiver hospedado em outro domínio, ajuste de acordo:
- Local: `http://localhost:5173/oidc/callback`
- Produção: `https://digna.yourdomain.com/oidc/callback`

### Exemplo Completo

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Teste de Login {: #testing-login }

Após concluir a configuração, verifique se o SSO está funcionando corretamente.

### Lista de Verificação Antes do Teste

Antes de testar, certifique-se de que:

- [ ] `dashboard_config.toml` foi atualizado com os provedores OIDC
- [ ] `config.toml` foi atualizado com as credenciais OIDC
- [ ] Ambos os arquivos foram salvos
- [ ] As credenciais estão corretas (client ID, client secret)
- [ ] O URI de redirect corresponde à URL da sua implantação
- [ ] A aplicação no provedor de identidade está configurada com o URI de redirect

### Etapas de Teste

#### Passo 1: Reiniciar os Serviços

Reinicie o backend do digna e o servidor web para aplicar as alterações.

**Se estiver executando como serviço no Windows:**
```bash
cd C:\path\to\digna
digna windows stop
digna windows start
```

**Se estiver executando como serviço no Linux ou macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Se estiver executando manualmente:**
```bash
digna serve --address localhost --port 8082
```

**Reinicie também o servidor web** — IIS ou Tomcat no Windows, nginx ou Apache no Linux e macOS.

#### Passo 2: Abrir o Dashboard

Abra o dashboard do digna no seu navegador:

```
http://localhost:5173
```

(ou a URL do dashboard que você configurou)

#### Passo 3: Verificar os Botões de Login

Verifique se os botões de login aparecem para cada provedor configurado:

- Deve aparecer o botão "Login with Microsoft"
- Deve aparecer o botão "Login with Google"
- (Se usePassword = true) Devem aparecer os campos de nome de usuário/senha

Se os botões não aparecerem:
- Verifique se `dashboard_config.toml` foi salvo
- Verifique se o serviço do dashboard foi reiniciado
- Verifique o console do navegador (F12) em busca de erros

#### Passo 4: Testar o Login com SSO

Clique em um dos botões de SSO (ex.: "Login with Microsoft"):

1. Você deve ser redirecionado para a página de login do provedor de identidade
2. Faça login com suas credenciais corporativas
3. Você deve ser redirecionado de volta ao digna
4. Você deve estar logado no digna

#### Passo 5: Verificar a Criação do Usuário

Após um login com SSO bem-sucedido:

- O usuário deve ser criado automaticamente no digna
- O usuário deve estar logado
- O perfil do usuário deve exibir as credenciais do seu provedor de identidade
- Você deve ver o dashboard do digna

#### Passo 6: Testar o Login com Senha (Se Habilitado)

Se `usePassword = true`:

1. Faça logout do digna
2. Na página de login, insira um nome de usuário e uma senha
3. Você deve conseguir fazer login com as credenciais de senha

---

## Resolução de Problemas {: #troubleshooting }

### Os Botões de Login Não Aparecem

**Sintomas:**
- Botões de login OIDC não visíveis na página de login
- Apenas os campos de senha aparecem (se usePassword = true)

**Causas e Soluções:**
1. Verifique se `dashboard_config.toml` está no diretório `dashboard/`
2. Verifique se as seções `[[login.oidc]]` estão presentes com a sintaxe correta
3. Reinicie o serviço do dashboard
4. Limpe o cache do navegador (Ctrl+Shift+Delete ou Cmd+Shift+Delete)
5. Verifique o console do navegador (F12 → aba Console) em busca de erros

---

### Erro de Incompatibilidade do URI de Redirect

**Sintomas:**
- Após clicar no botão de SSO, aparece um erro sobre "redirect_uri mismatch"
- Erro "The redirect URI is not registered"

**Causas e Soluções:**
1. Verifique se `DIGNA_OIDC_REDIRECT_URI` em `config.toml` está correto
2. Verifique se o URI de redirect está registrado nas configurações do provedor de identidade
3. Certifique-se de que ambos usam URLs idênticas (incluindo protocolo, domínio e caminho)
4. Verifique se há erros de digitação no URI de redirect
5. Se estiver usando HTTPS, certifique-se de que o certificado é válido

---

### Erro de Credenciais de Cliente Inválidas

**Sintomas:**
- Erro "Invalid client ID or secret"
- A autenticação falha com um erro de credenciais

**Causas e Soluções:**
1. Verifique se `DIGNA_OIDC_CLIENT_ID` e `DIGNA_OIDC_CLIENT_SECRET` estão corretos
2. Certifique-se de que não há espaços extras ou caracteres especiais
3. Verifique se as credenciais não expiraram nem foram revogadas
4. Reinicie o serviço de backend após atualizar a configuração
5. Verifique no console do provedor de identidade se as credenciais estão ativas

---

### O Login Trava ou Expira

**Sintomas:**
- Clicar no botão de SSO não faz nada
- Tempo esgotado após alguns segundos
- O navegador mostra "Failed to connect" ou algo semelhante

**Causas e Soluções:**
1. Verifique se o backend do digna está em execução: `digna repo check`
2. Verifique a conectividade de rede com o provedor de identidade
3. Verifique se `DIGNA_OIDC_CONFIGURATION_URL` está acessível
4. Verifique se as regras de firewall permitem conexões HTTPS de saída
5. Verifique se o backend e o dashboard conseguem se comunicar

---

### Usuários Não São Criados Automaticamente

**Sintomas:**
- O login com SSO é bem-sucedido, mas o usuário não é criado no digna
- Erro de permissão após o login com SSO

**Causas e Soluções:**
1. Verifique se a configuração OIDC está correta
2. Verifique se as permissões de usuário estão configuradas
3. Revise os logs do digna em busca de mensagens de erro
4. Reinicie o serviço de backend
5. Entre em contato com support@digna.ai se o problema persistir

---

## Provedores Suportados {: #supported-providers }

### Testados e Suportados

Os seguintes provedores OIDC foram testados e comprovadamente funcionam:

| Provedor | URL de Configuração | Guia de Configuração |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Configurar SSO com AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Configurar SSO com Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Configurar SSO com Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Configurar SSO com Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Configurar SSO com Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Configurar SSO com Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Configurar SSO com OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Configurar SSO com PingOne](pingone_sso_guide.md) |

### Outros Provedores OIDC

Qualquer provedor que suporte OpenID Connect pode ser integrado. Informações necessárias:

- Client ID
- Client secret
- URL de configuração do OpenID (geralmente em `/.well-known/openid-configuration`)
- Scopes suportados (normalmente `openid profile email`)

Entre em contato com support@digna.ai se precisar de ajuda para integrar um provedor específico.

---

## Boas Práticas

**FAÇA:**
- Use HTTPS em produção (não HTTP)
- Armazene os client secrets com segurança (use variáveis de ambiente, se possível)
- Troque os secrets periodicamente
- Teste primeiro em um ambiente que não seja de produção
- Documente quais provedores estão configurados
- Monitore os logs de login em busca de atividades incomuns
- Mantenha a configuração do provedor de identidade sincronizada com a configuração do digna

**NÃO FAÇA:**
- Armazenar client secrets no controle de versão
- Usar URIs de redirect HTTP em produção
- Configurar vários provedores com a mesma key
- Deixar credenciais padrão/de teste em produção
- Expor arquivos de configuração que contenham secrets
- Misturar credenciais de desenvolvimento e de produção

---

## Suporte

Precisa de ajuda com a configuração de SSO?

- **E-mail:** support@digna.ai
- **Documentação:** https://docs.digna.ai
- **Site:** https://www.digna.ai

---

**Última Atualização:** 30 de agosto de 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
