---
title: Windows Installation Guide – digna Release 2026.06 | digna Documentation
description: Step-by-step guide to installing digna Release 2026.06 on Windows — system requirements, PostgreSQL setup, web server configuration, backend and dashboard configuration, running digna as a Windows service, and upgrading to a new release.
keywords: digna windows installation, digna deployment guide, digna backend setup, digna dashboard installation, postgresql setup, digna windows service, digna upgrade guide
image: /assets/logo_square.png
---

# Guia de Instalação no Windows para digna Release 2026.06

**Release:** 2026.06

**Última Atualização:** 30 de agosto de 2026


---

## Sumário

1. [Introdução](#introduction)
2. [Requisitos do Sistema](#system-requirements)
3. [Configuração Pré-Instalação](#pre-installation-setup)
4. [Configuração do Servidor PostgreSQL](#postgresql-server-setup)
5. [Configuração do Servidor Web](#web-server-configuration)
6. [Instalação Inicial](#initial-installation)
7. [Configuração do Backend](#backend-configuration)
8. [Configuração do Dashboard](#dashboard-configuration)
9. [Executando o digna como Serviço do Windows](#running-digna-as-a-windows-service)
10. [Atualizando para uma Nova Release](#upgrading-to-a-new-release)

---

## Introdução {: #introduction }

### Sobre o digna

digna é uma plataforma abrangente orientada por IA projetada para otimizar a gestão da qualidade de dados em diversos ambientes, como data warehouses, data lakes e lakehouses. Construída para ser altamente escalável e adaptável, a digna resolve desafios modernos de dados por meio de automação, monitoramento em tempo real e detecção de anomalias.

digna consiste em dois componentes principais:

- **dignabackend**: O motor central da aplicação, responsável pelo processamento de dados e execução das verificações de qualidade.
- **dignadashboard**: Uma interface web hospedada em um servidor web, oferecendo uma maneira amigável de interagir com a plataforma digna e visualizar métricas de qualidade de dados.

### Novidades na Release 2026.06

Esta release traz capacidades de observabilidade de dados diretamente para o seu código, permitindo que desenvolvedores monitorem a qualidade dos dados na origem. Consulte as [notas de release](http://docs.digna.ai/changelog/Release_202606/) para detalhes completos.

---

## Requisitos do Sistema {: #system-requirements }

Antes de iniciar a instalação, verifique se o seu sistema atende aos seguintes requisitos mínimos:

| Requirement | Specification |
|---|---|
| **Operating System** | Windows Server or Windows 10/11 |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB available storage |
| **Database** | PostgreSQL Server 12 or higher |
| **Web Server** | IIS, Apache Tomcat, or equivalent |

### Opções de Instalação do Banco de Dados

**Se o PostgreSQL já estiver instalado:**
Você pode adicionar um novo banco de dados para o digna no seu servidor PostgreSQL existente.

**Se for instalar o PostgreSQL na mesma máquina do digna:**

> **Especificações Recomendadas**
>
> - **Memória**: 32 GB RAM (em vez de 16 GB)
> - **Espaço em Disco**: 50 GB disponíveis (em vez de 10 GB)
>
> Essas especificações superiores acomodam tanto o digna quanto o banco de dados PostgreSQL sendo executados simultaneamente.

---

## Configuração Pré-Instalação {: #pre-installation-setup }

Antes de instalar o digna, verifique se dois pré-requisitos principais estão em vigor:

1. **Servidor PostgreSQL** – para armazenar métricas calculadas e dados de performance
2. **Servidor Web** – para hospedar o digna Dashboard

Se esses componentes ainda não estiverem configurados, siga as seções abaixo para instalá-los e configurá-los.

---

## Configuração do Servidor PostgreSQL {: #postgresql-server-setup }

### Se Você Já Tiver PostgreSQL

Se o PostgreSQL já está instalado e em execução na sua máquina local ou se você estiver usando um servidor PostgreSQL remoto gerenciado, você pode pular para a [próxima seção](#web-server-configuration).

### Instalando o PostgreSQL

Siga estes passos para instalar o PostgreSQL no Windows:

#### Passo 1: Baixar o PostgreSQL

1. Visite a [página de downloads do PostgreSQL](https://www.postgresql.org/download/)
2. Selecione **Windows**
3. Baixe o instalador mais recente

#### Passo 2: Executar o Instalador

1. Dê um duplo clique no arquivo do instalador baixado
2. Siga as instruções do assistente de instalação

#### Passo 3: Escolher o Diretório de Instalação

Selecione o diretório onde o PostgreSQL será instalado. O local padrão geralmente é adequado.

#### Passo 4: Selecionar Componentes

Para uma instalação padrão, mantenha as opções de componentes padrão selecionadas.

#### Passo 5: Definir a Senha do Superusuário do PostgreSQL

Digite e confirme uma senha para o superusuário do PostgreSQL (`postgres`). **Armazene essa senha com segurança** — você precisará dela mais tarde.

#### Passo 6: Configurar o Número da Porta

A porta padrão do PostgreSQL é `5432`. Você pode usar a padrão ou especificar uma porta diferente, se necessário.

> **Dica**
>
> Se a porta 5432 já estiver em uso, escolha uma porta alternativa e anote-a para a configuração posterior.

#### Passo 7: Escolher Localidade (Locale)

Selecione a localidade para o seu banco de dados. A configuração padrão geralmente é adequada para a maioria das instalações.

#### Passo 8: Concluir a Instalação

Clique em **Next** nas etapas restantes e, em seguida, clique em **Finish**.

#### Passo 9: Verificar a Instalação

Abra o Prompt de Comando e verifique se o PostgreSQL foi instalado:

```bash
psql --version
```

Você verá a versão do PostgreSQL se a instalação tiver sido bem-sucedida.

---

## Configuração do Servidor Web {: #web-server-configuration }

O digna exige um servidor web para hospedar o dashboard. Escolha uma das seguintes opções:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Você só precisa instalar e configurar **um** desses servidores.

### Configuração do IIS {: #iis-setup }

#### Visão Geral

Internet Information Services (IIS) é o servidor web da Microsoft para hospedagem de sites e aplicações web.

#### Habilitando o IIS

1. **Abra o Painel de Controle**
   - Pressione `Win + R`
   - Digite `control` e pressione Enter

2. **Navegue até Recursos do Windows**
   - Clique em **Programs**
   - Selecione **Turn Windows features on or off**

3. **Habilite o Internet Information Services**
   - Role para baixo e encontre **Internet Information Services (IIS)**
   - Marque a caixa de seleção para habilitá-lo
   - Clique no **+** para expandir e verifique se os seguintes subcomponentes estão selecionados:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Clique em OK** para aplicar as alterações

5. **Verifique a Instalação do IIS**
   - Abra seu navegador
   - Acesse `http://localhost`
   - Você deverá ver a página de boas-vindas do IIS

#### Obrigatório: Módulo URL Rewrite

O IIS requer o componente URL Rewrite. Baixe e instale a partir da [página oficial da Microsoft](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Obrigatório: Tipo MIME para Arquivos Markdown

Para garantir que arquivos Markdown (`.md`) sejam servidos corretamente pelo IIS:

1. Abra o **IIS Manager** (pressione `Win + R`, digite `inetmgr`, pressione Enter)
2. Navegue até **Your Site > MIME Types**
3. Clique em **Add...**
4. Configure:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

> **Importante**
>
> Sem essa configuração, arquivos `.md` podem não ser servidos corretamente.

---

### Configuração do Apache Tomcat {: #apache-tomcat-setup }

#### Visão Geral

Apache Tomcat é um contêiner de servlets Java e servidor web de código aberto.

#### Instalação

1. **Baixar o Apache Tomcat**
   - Visite [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Baixe a distribuição ZIP para Windows

2. **Extrair o Arquivo**
   - Extraia o arquivo ZIP para um diretório no seu sistema
   - Exemplo: `C:\Program Files\Apache Tomcat`

3. **Verificar se o Tomcat Está em Execução**
   - Abra seu navegador
   - Acesse `http://localhost:8080`
   - Você deverá ver a página de boas-vindas do Apache Tomcat

> **Dica**
>
> O Apache Tomcat normalmente é iniciado automaticamente após a instalação. Se não iniciar, navegue até a pasta `bin` e execute `startup.bat`.

---

## Instalação Inicial {: #initial-installation }

### Passo 1: Configurar o Repositório do digna

O repositório do digna armazena todas as métricas calculadas pela plataforma. Ele atua como o banco de dados central para dados analíticos e de performance.

#### Criar Schema do Repositório e Usuário

Abra seu cliente PostgreSQL (pgAdmin, psql ou similar) e execute os seguintes comandos SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Substitua os seguintes placeholders:**

- `<digna_repo_schema>` — Nome do schema desejado (ex.: `dignarepo`)
- `<digna_repo_user>` — Nome de usuário desejado (ex.: `digna_user`)
- `<digna_repo_password>` — Uma senha segura para este usuário

**Exemplo:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

> **Boa Prática**
>
> Use senhas fortes e complexas para usuários do banco de dados. Evite credenciais facilmente adivinháveis.

---

### Passo 2: Extrair o Pacote de Instalação do digna

1. Localize o arquivo ZIP de instalação do digna fornecido a você
2. Extraia-o para o local de instalação desejado
3. Após a extração, você deverá ver os seguintes itens:
   - `dashboard/` — Interface web do dashboard
   - `digna` — Executável principal (backend + CLI combinados)
   - `config.toml` — Arquivo de configuração
   - `license.toml` — Arquivo de licença (copie o seu aqui)

### Passo 3: Instalar o Arquivo de Licença

> **Importante**
>
> O arquivo de licença **não** está incluído no pacote de instalação e será fornecido separadamente pelo digna.

1. Localize o arquivo `license.toml` fornecido a você
2. Copie-o para o diretório raiz da instalação do digna (onde `config.toml` e o executável `digna` estão localizados)

**Por que isso importa:**
O arquivo de licença contém suas informações de cliente, data de expiração da licença e assinatura digital. **Não modifique este arquivo** — qualquer alteração o invalidará.

**Estrutura de diretórios após a configuração:**

```
digna_installation/
├── config.toml         (arquivo de configuração)
├── license.toml        (SEU ARQUIVO DE LICENÇA - copie aqui)
├── digna               (executável principal)
└── dashboard/          (interface web)
    └── (arquivos do dashboard)
```

---

## Configuração do Backend {: #backend-configuration }

### Passo 1: Criar e Editar o Arquivo de Configuração

O arquivo `config_template.toml` é fornecido no diretório de instalação do digna. Você só precisa renomeá-lo para `config.toml`.

**Localização:** `digna_installation/config.toml`

Abra `config.toml` em um editor de texto e configure cada seção abaixo.

#### Seção [app]

Esta seção configura as definições da aplicação backend do digna:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_APP_HOST` | `localhost` or IP address | Nome do host ou IP onde o dignabackend está hospedado |
| `digna_APP_PORT` | `8082` (default) | Porta para os endpoints REST API |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend URL | Se o dashboard estiver em servidor diferente, inclua sua URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Necessário para CORS com credenciais |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Permitir todos os métodos HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Permitir todos os headers |

#### Seção [repo]

Esta seção configura a conexão com o banco de dados PostgreSQL:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_REPO_HOST` | `localhost` or IP | Hostname/IP do servidor PostgreSQL |
| `digna_REPO_PORT` | `5432` (default) | Porta do PostgreSQL |
| `digna_REPO_DB` | `postgres` | Nome do banco de dados |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema criado anteriormente |
| `digna_REPO_USER` | `digna_user` | Usuário criado na configuração do PostgreSQL |
| `digna_REPO_PASSWORD` | Your password | Senha definida durante a criação do schema |

#### Seção [base]

Esta seção contém configurações de segurança e cookies:

```toml
[base]
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_FERNET_KEY` | Encryption key | Usada para criptografar tokens e cookies (valor padrão fornecido) |
| `digna_COOKIE_DOMAIN` | `localhost` | Deve corresponder ao domínio do frontend |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (produção) | Use `true` para conexões HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Sempre habilitado por segurança |
| `digna_COOKIE_SAME_SITE` | `lax` | Previne ataques CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 horas) | Tempo de expiração da sessão em segundos |
| `digna_MAX_WORKERS` | Number of CPU cores - 1 | Número de tarefas de inspeção paralelas |

#### Seção [logging]

Esta seção configura o comportamento de logging:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` or `DEBUG` | `INFO` para produção, `DEBUG` para resolução de problemas |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Número de backups diários de logs a reter |

---

### Passo 3: Inicializar o Repositório

1. Abra o Prompt de Comando
2. Navegue até o diretório de instalação do digna (onde `config.toml` e o executável `digna` estão localizados)
3. Execute o teste de conexão:

```bash
digna repo check
```

Você deverá ver uma confirmação de que a conexão foi estabelecida (o repositório em si ainda não foi inicializado).

### Passo 4: Instalar o Schema do Repositório

No mesmo diretório, execute:

```bash
digna repo install
```

Esse comando instala as tabelas e o schema necessários no seu banco de dados PostgreSQL.

### Passo 5: Iniciar o Servidor digna

No diretório de instalação do digna, inicie o servidor com:

```bash
digna serve --address <host> --port <port>
```

**Parâmetros:**
- `--address` — Nome do host/IP do servidor
- `--port` — Porta do servidor

Você deverá ver mensagens de inicialização confirmando que o servidor está em execução:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Passo 6: Criar um Usuário Admin

1. Abra uma nova janela do Prompt de Comando
2. Navegue até o diretório de instalação do digna
3. Execute o seguinte comando para criar um usuário admin:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Exemplo:**

```bash
digna user add "Admin User" AdminPassword123! --su
```

Isto cria um usuário com privilégios administrativos completos.

> **Boa Prática**
>
> Use uma senha forte com mistura de letras maiúsculas, minúsculas, números e caracteres especiais.

---

## Configuração do Dashboard {: #dashboard-configuration }

### Passo 1: Implantar o Dashboard no Servidor Web

O dashboard do digna tem seu próprio arquivo `config.toml` localizado no diretório `dashboard/`. Esta configuração já é fornecida e não requer alterações durante a configuração inicial. Você só precisa configurá-lo se desejar personalizar a conexão com o backend.

Se precisar modificar a configuração do dashboard (por exemplo, para implantações multi-instância), consulte a documentação do dashboard.

Escolha seu servidor web e siga os passos de implantação correspondentes.

#### Implantando no IIS

1. **Abra o IIS Manager**
   - Pressione `Win + R`, digite `inetmgr`, pressione Enter

2. **Crie um Novo Website**
   - No painel esquerdo, clique com o botão direito em **Sites**
   - Selecione **Add Website...**

3. **Configure o Website**
   - **Site Name**: Insira um nome (ex.: "dignaDashboard")
   - **Physical Path**: Clique em Browse e selecione a pasta `dashboard`
   - **Binding**: Defina o endereço IP e porta (porta padrão 80 para HTTP, 443 para HTTPS)

4. **Inicie o Website**
   - Clique em **OK** para criar o site
   - Clique com o botão direito no novo site e selecione **Start**

5. **Testar a Instalação**
   - Abra seu navegador
   - Acesse `http://localhost` (ou a URL configurada)
   - Você deverá ver a página de login do digna dashboard

#### Implantando no Apache Tomcat

1. **Copiar o Dashboard para o Tomcat**
   - Copie a pasta `dashboard` para o diretório `webapps` do Tomcat
   - Renomeie se necessário (ex.: para `digna`)
   - Exemplo: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verificar a Implantação**
   - Atualize ou recarregue a página de gerenciamento do Tomcat (http://localhost:8080)
   - Você deverá ver "digna" (ou o nome escolhido) listado nas aplicações implantadas

3. **Acessar o Dashboard**
   - Abra seu navegador
   - Acesse `http://localhost:8080/digna`
   - Você deverá ver a página de login do digna dashboard

---

## Executando o digna como um Serviço do Windows {: #running-digna-as-a-windows-service }

### Por que Usar um Serviço do Windows?

Executar o backend do digna como um serviço do Windows garante que ele:
- Inicie automaticamente quando o servidor for inicializado
- Execute em segundo plano sem a necessidade de um Prompt de Comando aberto
- Reinicie automaticamente em caso de falha
- Seja gerenciável através dos Serviços do Windows

### Arquivos de Gerenciamento do Serviço

Todos os arquivos necessários estão localizados no diretório de instalação do digna em: `bin/`

Os seguintes arquivos batch estão disponíveis:
- `install_service.bat` — Registra o digna como um serviço do Windows
- `uninstall_service.bat` — Remove o registro do serviço
- `start_service.bat` — Inicia o serviço registrado
- `stop_service.bat` — Para o serviço em execução

> **Administrador Necessário**
>
> Todos os arquivos batch devem ser executados com privilégios de Administrador.

### Instalando o Serviço

1. **Abra o Prompt de Comando como Administrador**
   - Clique com o botão direito no Prompt de Comando
   - Selecione "Run as Administrator"

2. **Navegue até a pasta bin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Execute o Script de Instalação**
   ```bash
   install_service.bat
   ```

O servidor digna agora está registrado como um serviço do Windows com inicialização **automática** habilitada. O serviço não inicia imediatamente — veja a próxima seção para iniciá-lo.

### Iniciando e Parando o Serviço

#### Para Iniciar o Serviço

1. Abra o Prompt de Comando como Administrador
2. Navegue até `digna\bin`
3. Execute:
   ```bash
   start_service.bat
   ```

#### Para Parar o Serviço

1. Abra o Prompt de Comando como Administrador
2. Navegue até `digna\bin`
3. Execute:
   ```bash
   stop_service.bat
   ```

> **Dica**
>
> Sempre pare o serviço antes de atualizar os arquivos da aplicação.

### Movendo o Serviço para um Novo Diretório

Se precisar realocar a instalação do digna:

1. **Desinstale o Serviço Atual**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Mova os Arquivos da Aplicação**
   - Mova toda a pasta de instalação do digna para o novo local

3. **Reinstale o Serviço**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Inicie o Serviço**
   ```bash
   start_service.bat
   ```

### Desinstalando o Serviço

1. **Pare o Serviço em Execução**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Desinstale o Serviço**
   ```bash
   uninstall_service.bat
   ```

O servidor digna agora está removido do registro como serviço do Windows.

---

## Atualizando para uma Nova Release {: #upgrading-to-a-new-release }

### Antes de Atualizar

**É Obrigatório Criar um Backup do Repositório do digna**

Antes de atualizar o digna, faça backup do seu repositório (PostgreSQL) para proteger contra perda de dados.
Um backup garante que você possa recuperar caso a atualização encontre problemas inesperados.

### Processo de Atualização

#### Passo 1: Parar o Serviço digna

Se o digna estiver sendo executado como serviço do Windows, pare-o primeiro:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Passo 2: Fazer Backup da Instalação Atual do Backend

No diretório de instalação do digna:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### Passo 3: Extrair e Implantar a Nova Versão

1. Extraia o novo arquivo ZIP de instalação do digna
2. Copie o novo executável `digna` e a pasta `dashboard` para o seu diretório de instalação


> **Importante**
>
> O arquivo `config.toml` **nunca** está incluído no ZIP de instalação. Sua configuração existente permanece segura.

### Passo 4: Restaurar Seus Arquivos de Configuração

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Passo 5: Atualizar o Schema do Repositório

Navegue até o diretório de instalação do digna e execute:

```bash
digna repo upgrade
```

Isso atualiza o schema do PostgreSQL para a versão mais recente preservando todos os dados existentes.

### Passo 6: Reiniciar os Serviços

Se estiver rodando como serviço do Windows:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Se estiver executando manualmente, reinicie o servidor:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Se estiver usando IIS ou Tomcat, reinicie o respectivo servidor web.

#### Passo 7: Verificar a Atualização

1. Acesse o digna dashboard
2. Verifique se a interface carrega corretamente
3. Confira os logs do servidor em busca de erros