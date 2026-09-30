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

- **digna**: o núcleo da aplicação, responsável por processar os dados e executar as verificações de qualidade. Reúne o backend e a interface de linha de comando em um único executável, substituindo os programas separados `dignabackend` e `dignacli` das versões anteriores.
- **dignadashboard**: Uma interface web hospedada em um servidor web, oferecendo uma maneira amigável de interagir com a plataforma digna e visualizar métricas de qualidade de dados.

### Novidades na Release 2026.06

Esta release traz capacidades de observabilidade de dados diretamente para o seu código, permitindo que desenvolvedores monitorem a qualidade dos dados na origem. Consulte as [notas de release](http://docs.digna.ai/changelog/Release_202606/) para detalhes completos.

### Procurando macOS ou Linux?

Este guia cobre o Windows. Para outras plataformas, veja o [macOS Installation Guide](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) ou o [Linux Installation Guide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

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

!!! info "Especificações Recomendadas"

    - **Memória**: 32 GB RAM (em vez de 16 GB)
    - **Espaço em Disco**: 50 GB disponíveis (em vez de 10 GB)

    Essas especificações superiores acomodam tanto o digna quanto o banco de dados PostgreSQL sendo executados simultaneamente.

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

!!! tip "Dica"

    Se a porta 5432 já estiver em uso, escolha uma porta alternativa e anote-a para a configuração posterior.

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

!!! warning "Importante"

    Sem essa configuração, arquivos `.md` podem não ser servidos corretamente.

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

!!! tip "Dica"

    O Apache Tomcat normalmente é iniciado automaticamente após a instalação. Se não iniciar, navegue até a pasta `bin` e execute `startup.bat`.

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

!!! tip "Boa Prática"

    Use senhas fortes e complexas para usuários do banco de dados. Evite credenciais facilmente adivinháveis.

---

### Passo 2: Extrair o Pacote de Instalação do digna

1. Localize o arquivo ZIP de instalação do digna fornecido a você
2. Extraia-o para o local de instalação desejado
3. Após a extração, você deverá ver os seguintes itens:
   - `dashboard/` — Interface web do dashboard
   - `digna` — Executável principal (backend + CLI combinados)

!!! info "Os arquivos de configuração e de licença não estão no pacote"

    Nem o `config.toml` nem o `dashboard/dashboard_config.toml` acompanham a instalação — você
    cria os dois, em [Configuração do Backend](#backend-configuration) e
    [Configuração do Dashboard](#dashboard-configuration). O `license.toml` também não acompanha;
    o digna o fornece separadamente, conforme descrito no Passo 3.

### Passo 3: Instalar o Arquivo de Licença

!!! warning "Importante"

    O arquivo de licença **não** está incluído no pacote de instalação e será fornecido separadamente pelo digna.

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
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Notes |
|---|---|---|
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
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
DIGNA_SCHEDULER_MAX_DELAY = 100
DIGNA_CLEANUP_TIME = "12:00"
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Deve corresponder ao domínio do frontend |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (produção) | Use `true` para conexões HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Sempre habilitado por segurança |
| `digna_COOKIE_SAME_SITE` | `lax` | Previne ataques CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 horas) | Tempo de expiração da sessão em segundos |
| `digna_MAX_WORKERS` | Number of CPU cores - 1 | Número de tarefas de inspeção paralelas |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Atraso máximo, em segundos, que o agendador pode acrescentar antes de iniciar uma tarefa pendente |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Horário (formato 24 h `HH:MM`) em que a limpeza diária começa |

#### Seção [encryption]

Esta seção contém a chave usada para criptografar os valores sensíveis armazenados no repositório. Ela é **obrigatória** — `config check` informa a seção `[encryption]` como FAILED se a chave estiver ausente.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Chave codificada em Base64 | Criptografa os valores sensíveis armazenados no repositório digna |

!!! warning "Proteja o config.toml"

    Esta chave é um valor fixo, idêntico em todas as instalações do digna, e é ela que descriptografa os valores sensíveis do seu repositório. Restrinja o `config.toml` à conta que executa o digna, mantenha o arquivo fora do controle de versão e de unidades compartilhadas e exclua-o de qualquer backup guardado com menos segurança que o próprio repositório.

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

### Passo 2: Validar a Configuração

Antes de inicializar o repositório, verifique se o `config.toml` está completo e bem formado. No diretório de instalação do digna, execute:

```bash
digna config check
```

Cada seção é validada separadamente, de modo que um único erro não esconde o estado das demais:

```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: OK
 - OIDC config(s): OK

Overall: OK
```

Corrija tudo o que for informado como FAILED e execute o comando novamente antes de continuar. A lista completa de opções está na [referência da CLI](../../../cli/Command_Line_Interface_202606.md).

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

### Passo 5: Criar um Usuário Admin

1. Abra uma nova janela do Prompt de Comando
2. Navegue até o diretório de instalação do digna
3. Execute o seguinte comando para criar um usuário admin:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Exemplo:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Isto cria um usuário com privilégios administrativos completos.

!!! tip "Boa Prática"

    Use uma senha forte com mistura de letras maiúsculas, minúsculas, números e caracteres especiais.

---

### Passo 6: Iniciar o Servidor digna

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

!!! note "O servidor ocupa o terminal"

    `serve` roda em primeiro plano e continua até você pará-lo com ++ctrl+c++. Deixe-o rodando enquanto termina a configuração; para iniciá-lo automaticamente na inicialização, consulte [Executar o digna como Serviço do Windows](#running-digna-as-a-windows-service).

## Configuração do Dashboard {: #dashboard-configuration }

### Passo 1: Implantar o Dashboard no Servidor Web

O dashboard do digna lê sua própria configuração do arquivo `dashboard/dashboard_config.toml`. Esse arquivo não acompanha a instalação — você o cria no diretório `dashboard/`, junto com os arquivos do dashboard.

O conteúdo dele está descrito em [Single Sign-On](../../../sso/overview.md), que é também onde o arquivo é necessário: ele contém as opções de login que o dashboard oferece e, em implantações multi-instância, a conexão com o backend.

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

### Os Comandos `windows`

O serviço é gerenciado pelo próprio executável `digna`, por meio dos subcomandos
`digna windows`. Não há arquivos batch para executar.

| Comando | Finalidade |
|---|---|
| `digna windows install` | Registra o digna como um serviço do Windows |
| `digna windows start` | Inicia o serviço registrado |
| `digna windows stop` | Para o serviço em execução |
| `digna windows uninstall` | Remove o registro do serviço |

!!! warning "Administrador Necessário"

    Os quatro comandos devem ser executados em um Prompt de Comando aberto como Administrador.

Todos os comandos aceitam `--name` para se referir a um serviço registrado com um nome diferente
do padrão. A lista completa de opções está na [referência da CLI](../../../cli/Command_Line_Interface_202606.md).

### Instalando o Serviço

1. **Abra o Prompt de Comando como Administrador**
   - Clique com o botão direito no Prompt de Comando
   - Selecione "Run as Administrator"

2. **Navegue até o diretório de instalação do digna**
   ```bash
   cd C:\path\to\digna
   ```

3. **Registre o serviço**
   ```bash
   digna windows install
   ```

!!! important "Informe o endereço e a porta, a menos que os padrões sirvam para você"

    O `install` grava o endereço e a porta no registro do serviço, e o serviço se vincula
    exatamente ao que foi gravado. Os padrões são `127.0.0.1` e `8000`, que aceitam conexões
    apenas da própria máquina. Um dashboard em outro host não consegue alcançá-lo, então informe
    o endereço em que o backend deve escutar:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Esses valores não são lidos do `config.toml`. Para alterá-los depois, desinstale o serviço e
    instale-o novamente com os novos valores.

O serviço é registrado com inicialização **automática**, então ele iniciará junto com o Windows.
Ele não inicia imediatamente — veja a próxima seção.

#### Opções de Instalação

| Opção | Padrão | Finalidade |
|---|---|---|
| `--name` | `digna` | Nome com o qual o serviço é registrado |
| `--display-name` | `digna` | Nome exibido no services.msc |
| `--description` | `digna data quality backend` | Descrição exibida no services.msc |
| `--address` | `127.0.0.1` | Endereço ao qual o serviço vincula sua API |
| `--port` | `8000` | Porta à qual o serviço vincula sua API |
| `--working-dir` | o diretório do executável `digna` | Diretório que contém `config.toml` e `license.toml`, usado pelo serviço como diretório de trabalho |
| `--start-type` | `auto` | `auto` inicia com o Windows, `manual` inicia apenas quando solicitado, `disabled` registra o serviço, mas se recusa a iniciá-lo |
| `--account` | `LocalSystem` | Conta sob a qual o serviço é executado, por exemplo `DOMAIN\user` ou `.\user` |
| `--password` | | Senha da `--account` |

!!! tip "Executando com uma conta de domínio"

    A `LocalSystem` não tem identidade de rede, então a autenticação do Windows no SQL Server e
    qualquer acesso a um compartilhamento de rede falharão. Instale com `--account` e `--password`
    quando o serviço precisar acessar recursos como um usuário específico.

### Iniciando e Parando o Serviço

#### Para Iniciar o Serviço

```bash
digna windows start
```

#### Para Parar o Serviço

```bash
digna windows stop
```

!!! tip "Dica"

    Sempre pare o serviço antes de atualizar os arquivos da aplicação.

### Movendo o Serviço para um Novo Diretório

Se precisar realocar a instalação do digna:

1. **Pare o serviço atual e remova o registro dele**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Mova os Arquivos da Aplicação**
   - Mova toda a pasta de instalação do digna para o novo local

3. **Registre o serviço novamente a partir do novo local**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Repita os valores de `--address`, `--port` ou `--account` que você usou na primeira vez — o
   registro anterior não existe mais.

4. **Inicie o Serviço**
   ```bash
   digna windows start
   ```

### Desinstalando o Serviço

1. **Pare o Serviço em Execução**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Remova o Registro do Serviço**
   ```bash
   digna windows uninstall
   ```

O servidor digna agora está removido do registro como serviço do Windows.

---

## Atualizando para uma Nova Release {: #upgrading-to-a-new-release }

### Antes de Atualizar

**Verifique Primeiro Todas as Conexões de Banco de Dados**

A partir da Release 2026.06, o digna acessa cada tecnologia de origem por **ODBC**. As versões anteriores ofereciam a escolha entre um driver próprio por tecnologia e ODBC, selecionada pelo botão **Use ODBC**. A equipe do digna decidiu se apoiar apenas em ODBC, porque uma interface única e padronizada oferece mais do que um conjunto de drivers sob medida:

- **Autenticação** — a autenticação faz parte do ODBC, então uma conexão pode usar tudo o que o seu driver suportar: senhas, tokens e PATs, Kerberos e Active Directory, MFA e logon único pelo navegador, identidades na nuvem, certificados de cliente e TLS. Novos métodos chegam com uma atualização do driver, em vez de esperar por uma versão do digna.
- **Drivers mantidos pelos fabricantes dos bancos de dados** — o driver do próprio fabricante acompanha as novas versões do servidor e as correções de segurança, e você pode atualizá-lo no seu próprio ritmo, independentemente do digna.
- **Uma única forma de configurar tudo** — cada tecnologia é uma lista de propriedades chave/valor, com a mesma interface, a mesma criptografia de valores sensíveis e a mesma solução de problemas, em vez de um conjunto de campos diferente por origem.
- **Ajuste e alcance** — opções do driver como tempos limite, configurações de TLS, proxies e tamanhos de leitura estão disponíveis para todas as origens, e qualquer tecnologia com um driver ODBC compatível pode ser conectada, inclusive aquelas para as quais o digna não publica um guia dedicado.

Na prática, isso significa que o botão **Use ODBC** e os campos separados de host, porta, banco de dados, usuário e senha não existem mais. **Toda conexão que ainda não usa ODBC precisa ser convertida para ODBC** — não há conversão automática, portanto planeje isso antes de atualizar:

1. Revise cada conexão de banco de dados definida na sua instalação e anote as que ainda não usam ODBC — cada uma precisará ser reconfigurada.
2. Instale o driver ODBC correspondente no host do digna — as conexões são abertas pelo servidor que executa o backend do digna, não pelo navegador. Consulte [Instalar o Driver ODBC no Host do digna](../../../databases/overview.md#install-the-driver).
3. Tenha as propriedades ODBC prontas para cada conexão afetada. Os [guias por tecnologia](../../../databases/overview.md#technology-guides) trazem, para cada origem, um conjunto de propriedades comprovado.

Após a atualização, converta cada conexão afetada para ODBC e teste-a pelo dashboard — consulte [Criar uma Conexão de Banco de Dados](../../../databases/overview.md#create-a-database-connection) e [Testar uma Conexão](../../../databases/overview.md#testing-a-connection).

!!! warning "Conexões Databricks Legacy"

    O conector Databricks Legacy foi removido nesta release. Migre essas conexões para o conector [Databricks](../../../databases/databricks_connector_guide.md).

**É Obrigatório Criar um Backup do Repositório do digna**

Antes de atualizar o digna, faça backup do seu repositório (PostgreSQL) para proteger contra perda de dados.
Um backup garante que você possa recuperar caso a atualização encontre problemas inesperados.

### Processo de Atualização

#### Passo 1: Parar o Serviço Antigo e Remover Seu Registro

Se o digna estiver sendo executado como serviço do Windows, pare-o com os **arquivos batch da sua
instalação atual** — os comandos `digna windows` pertencem à nova release e ainda não estão
disponíveis:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

Em seguida, remova o registro do serviço, novamente com o arquivo batch antigo. O registro aponta
para o executável antigo e seus scripts, que esta atualização substitui, portanto ele não pode ser
reaproveitado:

```bash
uninstall_service.bat
```

!!! warning "Remova o registro antes de renomear qualquer coisa"

    O `uninstall_service.bat` fica na pasta `bin` que você está prestes a renomear, e é a única
    coisa capaz de remover o registro que ele criou. Execute-o enquanto a instalação antiga ainda
    estiver no lugar. Se a pasta já tiver sido renomeada, volte ao nome original, remova o registro
    e então continue.

    Anote a conta sob a qual o serviço era executado, além do endereço e da porta em que ele
    atendia — você precisará deles no Passo 9.

#### Passo 2: Fazer Backup da Instalação Atual

No diretório de instalação do digna, renomeie as pastas da instalação atual para que a nova release possa ser implantada ao lado delas:

```bash
# Rename the folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename the folder containing dignacli
ren dignacli dignacli_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

!!! info "dignabackend e dignacli não são mais usados"

    A partir da Release 2026.06, `dignabackend` e `dignacli` são substituídos pelo executável único `digna`, que reúne o backend e a CLI. Mantenha `dignabackend_old` e `dignacli_old` apenas até verificar a atualização — depois você pode excluir as duas pastas. Mantenha `dashboard_old` até restaurar dele os seus arquivos de configuração (veja o passo 4). A pasta `bin` também deixa de existir: seus arquivos batch controlavam o serviço antigo e a 2026.06 não os inclui, então, depois que o registro do serviço for removido no Passo 1, eles só servem para confundir.

#### Passo 3: Extrair e Implantar a Nova Versão

1. Extraia o novo arquivo ZIP de instalação do digna
2. Copie o novo executável `digna` e a pasta `dashboard` para o seu diretório de instalação


!!! warning "Importante"

    Nem o `config.toml` nem o `dashboard/dashboard_config.toml` são incluídos no ZIP de
    instalação — a equipe do digna nunca distribui nenhum dos dois arquivos. Por isso, sua
    configuração existente não é afetada pela atualização, e as cópias nas pastas renomeadas
    `*_old` são as únicas que você tem.

#### Passo 4: Restaurar Seus Arquivos de Configuração

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
!!! warning "A Release 2026.06 altera o config.toml"

    Três configurações são novas e obrigatórias, e três não são mais usadas. Um `config.toml` herdado de uma versão anterior não contém as novas configurações, e o digna não iniciará enquanto elas estiverem ausentes. Acrescente o seguinte ao seu `config.toml` existente:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Acrescente as duas chaves `[base]` à sua seção `[base]` existente e adicione `[encryption]` como uma nova seção. Em seguida, remova as configurações que não são mais usadas: **`digna_FERNET_KEY`** de `[base]`, e **`digna_APP_HOST`** e **`digna_APP_PORT`** de `[app]` — o servidor agora obtém o endereço e a porta de `digna serve`.

    O que cada configuração faz está descrito em [Configuração do Backend](#backend-configuration).

!!! warning "Logon único: o formato de [oidc_clients] mudou"

    A release 2026.06 substitui a matriz de tabelas por uma tabela por provedor, nomeada a partir da chave do provedor. `DIGNA_OIDC_KEY` deixa de existir — a chave agora faz parte do cabeçalho da seção.

    Antes:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Depois:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Repita a seção para cada provedor e mantenha cada chave igual ao `key` definido em `dashboard_config.toml`. O `digna config check` informa `oidc_clients` como FAILED enquanto a forma antiga permanecer. Apenas as instalações que usam logon único são afetadas.

#### Passo 5: Recarregar o Servidor Web

O dashboard é um conjunto de arquivos estáticos, então seu servidor web — e o navegador — podem
ainda estar servindo a versão anterior. Recarregue ou reinicie o servidor web que hospeda a pasta
`dashboard` e, em seguida, recarregue a página com uma atualização forçada (++ctrl+f5++).

#### Passo 6: Validar a Configuração

Confirme que o `config.toml` atualizado está completo antes de mexer no repositório:

```bash
digna config check
```

Todas as seções devem informar OK. Corrija tudo o que for informado como FAILED e execute o comando novamente antes de continuar.

#### Passo 7: Substituir o Arquivo de Licença

Cada release é licenciada separadamente. Copie o `license.toml` que a equipe do digna forneceu
para esta release para o diretório de instalação, substituindo o antigo:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Não mantenha a licença anterior"

    Um `license.toml` emitido para uma release anterior não cobre esta, e todo comando que
    verifica a licença — `user`, `inspection`, `repo` — é interrompido antes de mexer no
    repositório quando a verificação falha. Verifique-a antes de prosseguir:

    ```bash
    digna license check
    ```

#### Passo 8: Atualizar o Schema do Repositório

Navegue até o diretório de instalação do digna e execute:

```bash
digna repo upgrade
```

Isso atualiza o schema do PostgreSQL para a versão mais recente preservando todos os dados existentes.

#### Passo 9: Registrar e Iniciar o Serviço

O registro antigo foi removido no Passo 1, então o serviço é registrado novamente — desta vez com
o executável `digna`, que não tem arquivos batch:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

Informe em `--address` e `--port` os valores em que o serviço antigo atendia, a menos que você
queira os novos padrões `127.0.0.1` e `8000`; eles são gravados no registro e não são mais lidos
do `config.toml`. Acrescente `--account` e `--password` se o serviço antigo era executado com uma
conta de domínio. Consulte
[Executando o digna como um Serviço do Windows](#running-digna-as-a-windows-service) para a lista
completa de opções.

Se estiver executando manualmente, reinicie o servidor:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Se estiver usando IIS ou Tomcat, reinicie o respectivo servidor web.

#### Passo 10: Verificar a Atualização

1. Acesse o digna dashboard
2. Verifique se a interface carrega corretamente
3. Confira os logs do servidor em busca de erros
4. Converta para ODBC todas as conexões que ainda não o usavam e depois teste todas as conexões — consulte [Testar uma Conexão](../../../databases/overview.md#testing-a-connection)