---
title: Guia de Instalação no Windows – digna Release 2026.11 | digna Documentation
description: Guia passo a passo para instalar o digna Release 2026.11 no Windows — requisitos do sistema, configuração do PostgreSQL, configuração do servidor web, configuração do backend e do dashboard, execução do digna como serviço do Windows e atualização a partir da Release 2026.06.
keywords: digna windows installation, digna deployment guide, digna backend setup, digna dashboard installation, postgresql setup, digna windows service, digna upgrade guide
image: /assets/logo_square.png
---

# Guia de Instalação no Windows para digna Release 2026.11

**Release:** 2026.11

**Última Atualização:** 7 de novembro de 2026


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

### Novidades na Release 2026.11

Esta release adiciona o digna Data Reconciliation, o digna Agentic com o digna MCP Server e o digna Engine, que pode fazer o profiling dos dados dentro do digna e verificar a integridade referencial entre diferentes tecnologias de banco de dados. Consulte as [notas de versão](../../../changelog/Release_202611.md) para detalhes completos.

Para uma instalação, a release traz um novo mecanismo de migração do repositório, uma seção `[duckdb]` opcional no `config.toml` para o digna Engine e um novo arquivo de licença. A [seção de atualização](#upgrading-to-a-new-release) aborda cada um deles.

### Procurando macOS ou Linux?

Este guia cobre o Windows. Para outras plataformas, veja o [macOS Installation Guide](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) ou o [Linux Installation Guide](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    As conexões de banco de dados que usam o digna Engine como local de profiling passam pelo profiling no
    próprio host do digna. Planeje memória e espaço em disco adicionais para elas; consulte a
    [seção \[duckdb\]](#duckdb-section).

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

Esta seção configura o compartilhamento de recursos entre origens (CORS) entre o dashboard e o backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | URLs do dashboard | As URLs a partir das quais o dashboard é servido. Requisições do navegador vindas de qualquer outra origem são rejeitadas |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Obrigatório, para que o navegador envie o cookie de sessão em cada requisição |

!!! info "A seção [app] é opcional"

    A partir da Release 2026.11, as duas chaves, e a seção `[app]` inteira, podem ser omitidas. Essa é a
    configuração correta quando um proxy reverso serve o dashboard e o backend sob uma única origem: o
    navegador então não faz requisições entre origens, e nenhuma é permitida por padrão.

#### Seção [repo]

Esta seção configura a conexão com o banco de dados PostgreSQL:

```toml
[repo]
DIGNA_REPO_HOST = "localhost"
DIGNA_REPO_PORT = 5432
DIGNA_REPO_DB = "postgres"
DIGNA_REPO_SCHEMA = "dignarepo"
DIGNA_REPO_USER = "digna_user"
DIGNA_REPO_PASSWORD = "YourSecurePassword123!"
DIGNA_REPO_SSLMODE = "prefer"
DIGNA_REPO_NUM_CONNS = 16
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` or IP | Hostname/IP do servidor PostgreSQL |
| `DIGNA_REPO_PORT` | `5432` (default) | Porta do PostgreSQL |
| `DIGNA_REPO_DB` | `postgres` | Nome do banco de dados |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Schema criado anteriormente |
| `DIGNA_REPO_USER` | `digna_user` | Usuário criado na configuração do PostgreSQL |
| `DIGNA_REPO_PASSWORD` | Your password | Senha definida durante a criação do schema |
| `DIGNA_REPO_SSLMODE` | `prefer` (padrão) | Opcional. Modo SSL do PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` ou `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (padrão) | Opcional. Número de conexões que o digna mantém abertas com o repositório |

#### Seção [base]

Esta seção contém configurações de segurança, cookies e inspeção:

```toml
[base]
DIGNA_FERNET_KEY = "DU4a0yJ-OqvbKCL4hNQn_CsknH-V1vWmHZqBUl-AY44="
DIGNA_COOKIE_DOMAIN = "localhost"
DIGNA_COOKIE_SECURE = false
DIGNA_COOKIE_HTTPONLY = true
DIGNA_TOKEN_EXPIRES_IN = 86400
DIGNA_MAX_WORKERS = 4
DIGNA_FRONTEND_BASEURL = "http://localhost/"
DIGNA_SOURCE_QUERY_TIMEOUT_SEC = 3600
DIGNA_SOURCE_LOGIN_TIMEOUT_SEC = 30
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_FERNET_KEY` | Valor mostrado acima | Chave da criptografia usada pelas releases anteriores. Ela precisa estar presente; mantenha o valor mostrado |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Host pelo qual o dashboard é acessado. `""` não define nenhum domínio, o que é o correto atrás de um proxy que serve o dashboard e o backend sob uma única origem |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Deve ser `true` sempre que o digna for servido por HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Mantém o cookie de sessão fora do alcance de scripts |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 horas) | Tempo de expiração da sessão em segundos |
| `DIGNA_MAX_WORKERS` | Number of CPU cores - 1 | Número de inspeções que podem ser executadas ao mesmo tempo |
| `DIGNA_FRONTEND_BASEURL` | URL do dashboard | Obrigatório. Usado nos links das mensagens de notificação, portanto deve ser uma URL que os destinatários consigam abrir |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (padrão) | Opcional. Segundos durante os quais uma única consulta a um banco de dados de origem pode ser executada antes de ser abortada; `0` desativa o timeout |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (padrão) | Opcional. Segundos de espera por uma conexão com um banco de dados de origem; `0` espera indefinidamente |

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
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` ou `DEBUG` | `INFO` para produção, `DEBUG` para resolução de problemas. `TRACE`, `WARN` e `ERROR` também são aceitos |
| `DIGNA_LOGGING_DIR` | `logs` (padrão) | Opcional. Diretório dos arquivos de log rotativos, relativo ao diretório de trabalho |
| `DIGNA_LOGGING_MAX_FILES` | `30` (padrão) | Opcional. Número de arquivos de log rotacionados a manter |

!!! warning "Mantenha o diretório de logs ao executar como serviço"

    Um serviço do Windows não tem console, então os arquivos de log são o único registro do que o serviço
    faz. Não defina `DIGNA_LOGGING_DIR` como uma string vazia, o que desativa os arquivos de log.

#### Seção [duckdb] (Opcional) {: #duckdb-section }

Novidade da Release 2026.11. Esta seção define os recursos do **digna Engine**, que faz o profiling
dos dados dentro do digna para as conexões de banco de dados cujo local de profiling é **digna Engine**, e
executa verificações de integridade referencial entre fontes de dados em conexões de banco de dados diferentes. Consulte
[Profiling Location](../../../platform/profiling/profiling_location.md).

A seção é opcional. Sem ela, valem os padrões abaixo.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (padrão) | Memória, em MB, que uma execução do digna Engine pode usar. Até `DIGNA_MAX_WORKERS` execuções podem estar ativas ao mesmo tempo |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Padrão: o diretório temporário da conta que executa o digna (`%TEMP%`) | Diretório para arquivos temporários quando os dados não cabem na memória |

!!! tip "Dimensionando o digna Engine"

    Planeje até `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` de memória no host do digna,
    além do que o próprio digna usa, e espaço livre em disco suficiente no diretório temporário
    para comportar a maior data inspecionada das fontes de dados que usam o digna Engine.
    Aponte `DIGNA_DUCKDB_TEMP_DIRECTORY` para um disco com esse espaço, com permissão de escrita para a
    conta que executa o digna:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Você só precisa desta seção se pelo menos uma conexão de banco de dados usar o digna Engine, ou se uma
    verificação de integridade referencial comparar fontes de dados em conexões diferentes.

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
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Corrija tudo o que for informado como FAILED e execute o comando novamente antes de continuar. Um WARNING em **Unknown keys** lista chaves do `config.toml` que o digna não lê; elas não têm efeito, então remova-as ou corrija a grafia. A lista completa de opções está na [referência da CLI](../../../cli/Command_Line_Interface_202611.md).

### Passo 3: Inicializar o Repositório

1. Abra o Prompt de Comando
2. Navegue até o diretório de instalação do digna (onde `config.toml` e o executável `digna` estão localizados)
3. Execute o teste de conexão:

```bash
digna repo check
```

Em um schema novo, o comando se conecta e então informa que ainda não há nenhum repositório instalado:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Neste ponto, esse é o resultado esperado: ele confirma que o digna alcança o PostgreSQL e o schema. Já um erro de conexão ou de autenticação aponta para a seção `[repo]` ou para a configuração do PostgreSQL.

### Passo 4: Instalar o Schema do Repositório

No mesmo diretório, execute:

```bash
digna repo upgrade
```

Este comando instala as tabelas necessárias no schema do repositório e termina com:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade instala e atualiza"

    A partir da Release 2026.11, `repo upgrade` instala um novo repositório e atualiza um existente.
    `repo install` continua funcionando como outro nome para o mesmo comando.

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
- `--address` — Nome do host/IP do servidor (padrão `127.0.0.1`)
- `--port` — Porta do servidor (padrão `8000`)

Quando o servidor estiver no ar, ele exibe o endereço em que está escutando:

```text
Server running on http://127.0.0.1:8082
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
do padrão. A lista completa de opções está na [referência da CLI](../../../cli/Command_Line_Interface_202611.md).

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

Esta seção atualiza uma instalação da Release 2026.06 para a Release 2026.11.

!!! warning "Atualização a Partir de uma Release Anterior à 2026.06"

    Primeiro, execute as etapas de atualização da Release 2026.06: [Atualizando para uma Nova Release](../Release%202026.06/installation_guide_digna_windows_2026_06.md#upgrading-to-a-new-release). Depois, continue com as etapas abaixo.

### Antes de Atualizar

**É Obrigatório Criar um Backup do Repositório do digna**

Antes de atualizar o digna, faça backup do seu repositório (PostgreSQL) para proteger contra perda de dados.
Um backup garante que você possa recuperar caso a atualização encontre problemas inesperados.

**Solicitando o Arquivo de Licença para a Release 2026.11**

A Release 2026.11 precisa de um novo `license.toml`. Solicite-o à equipe do digna antes de começar e
deixe-o pronto para o [Passo 7](#step-7-replace-the-license-file).

### Processo de Atualização

#### Passo 1: Parar o Serviço digna {: #step-1-stop-the-digna-service }

Abra um Prompt de Comando como Administrador e pare o serviço com o executável `digna` da
sua instalação atual:

```bash
cd C:\path\to\digna
digna windows stop
```

O serviço continua registrado. O novo executável ocupa o lugar do antigo no mesmo
diretório, então o registro continua apontando para o arquivo certo.

Se o digna estiver em execução em primeiro plano, pressione ++ctrl+c++ na janela do Prompt de Comando.

#### Passo 2: Fazer Backup da Instalação Atual {: #step-2-backup-current-installation }

No diretório de instalação do digna, renomeie o executável e a pasta do dashboard da sua
instalação atual, para que a nova release possa ser implantada ao lado deles:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

Mantenha `digna_old.exe` até verificar a atualização, e `dashboard_old` até restaurar dele os seus
arquivos de configuração (veja o Passo 4). Depois, você pode excluir ambos.

#### Passo 3: Extrair e Implantar a Nova Versão {: #step-3-extract-and-deploy-new-version }

1. Extraia o novo arquivo ZIP de instalação do digna
2. Copie o novo executável `digna` e a pasta `dashboard` para o seu diretório de instalação


!!! warning "Importante"

    Nem o `config.toml` nem o `dashboard/dashboard_config.toml` são incluídos no ZIP de
    instalação — a equipe do digna nunca distribui nenhum dos dois arquivos. Por isso, sua
    configuração existente não é afetada pela atualização, e as cópias nas pastas renomeadas
    `*_old` são as únicas que você tem.

#### Passo 4: Restaurar Seus Arquivos de Configuração {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

A Release 2026.11 não exige nenhuma alteração no `config.toml`: um arquivo que funciona com a Release 2026.06
continua funcionando. Duas alterações são opcionais:

- Adicione uma [seção `[duckdb]`](#duckdb-section) se as conexões de banco de dados forem usar o digna Engine
  e os padrões dele não forem adequados ao seu host.
- Omita a seção `[app]` se um proxy reverso servir o dashboard e o backend sob uma única
  origem.

!!! warning "Configurações que o digna não lê"

    Versões anteriores deste guia mostravam algumas configurações que o digna não lê. Elas não têm
    efeito, e o `config check` as lista em **Unknown keys** no Passo 6. Remova-as ou
    corrija-as:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` e
      `digna_LOGGING_BACKUP_COUNT` não existem. Remova-as.
    - Os nomes das configurações diferenciam maiúsculas de minúsculas. O digna lê `DIGNA_REPO_HOST`, não `digna_REPO_HOST`.
      Escreva todos os nomes em maiúsculas, como em [Configuração do Backend](#backend-configuration).

!!! warning "Logon único: mantenha [[oidc_clients]]"

    O digna lê os provedores de logon único como uma lista de entradas `[[oidc_clients]]`, cada uma com seu
    próprio `DIGNA_OIDC_KEY`. Se você alterou seus provedores para seções `[oidc_clients.<key>]`, como uma
    versão anterior deste guia mostrava, volte à forma anterior. O `config check` informa
    `OIDC config(s)` como FAILED enquanto essa forma estiver em uso:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Repita a entrada para cada provedor e mantenha cada `DIGNA_OIDC_KEY` igual ao `key` definido em
    `dashboard_config.toml`. Apenas as instalações que usam logon único são afetadas.

#### Passo 5: Recarregar o Servidor Web {: #step-5-reload-the-web-server }

O dashboard é um conjunto de arquivos estáticos, então seu servidor web — e o navegador — podem
ainda estar servindo a versão anterior. Recarregue ou reinicie o servidor web que hospeda a pasta
`dashboard` e, em seguida, recarregue a página com uma atualização forçada (++ctrl+f5++).

#### Passo 6: Validar a Configuração {: #step-6-validate-the-configuration }

Confirme que o `config.toml` está completo antes de mexer no repositório:

```bash
digna config check
```

Todas as seções devem informar OK. Corrija tudo o que for informado como FAILED, remova as chaves listadas em
**Unknown keys** e execute o comando novamente antes de continuar.

#### Passo 7: Substituir o Arquivo de Licença {: #step-7-replace-the-license-file }

Normalmente, um arquivo de licença continua valendo de uma release para a seguinte. A Release 2026.11 é uma
exceção: ela adiciona dois módulos licenciados, o digna Data Reconciliation e o digna Agentic, e uma licença
emitida antes da 2026.11 não os contém. Copie o `license.toml` que a equipe do digna forneceu para a
Release 2026.11 para o diretório de instalação, substituindo o antigo:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Não mantenha a licença anterior"

    Com a licença anterior, o digna ainda inicia, mas o digna Data Reconciliation e o digna
    MCP Server permanecem desativados. Todo comando que verifica a licença — `user`,
    `inspection`, `repo` — é interrompido antes de mexer no repositório quando a verificação falha.
    Verifique a nova licença antes de prosseguir:

    ```bash
    digna license check
    ```

#### Passo 8: Atualizar o Schema do Repositório {: #step-8-upgrade-the-repository-schema }

No diretório de instalação do digna, execute:

```bash
digna repo upgrade
```

A Release 2026.11 gerencia o schema do repositório com migrações versionadas. A primeira atualização a partir
de uma release anterior leva o schema à última versão do mecanismo anterior, registra isso como ponto de
partida e, em seguida, aplica as migrações da Release 2026.11. Ela termina com:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Todos os dados existentes são preservados. Para ver o estado do repositório a qualquer momento, execute
`digna repo check`: ele lista a última migração aplicada e as migrações pendentes.

!!! warning "O digna não inicia com um repositório desatualizado"

    A partir da Release 2026.11, o servidor se recusa a iniciar enquanto o repositório precisar de uma
    atualização, e informa isso, por exemplo:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Execute `repo upgrade` antes de iniciar o servidor ou o serviço.

#### Passo 9: Reiniciar Serviços {: #step-9-restart-services }

Se o digna for executado como serviço do Windows, inicie-o novamente:

```bash
cd C:\path\to\digna
digna windows start
```

Se estiver executando manualmente, reinicie o servidor:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Se estiver usando IIS ou Tomcat, reinicie o respectivo servidor web.

#### Passo 10: Verificar a Atualização {: #step-10-verify-the-upgrade }

1. Confirme a release do novo executável:

    ```bash
    digna version
    ```

    A primeira linha deve ser `Release: 2026.11`.

2. Acesse o digna dashboard e verifique se a interface carrega corretamente.
3. Verifique os arquivos no diretório `logs` da instalação em busca de erros.
4. Teste suas conexões de banco de dados — consulte
   [Testar uma Conexão](../../../databases/overview.md#testing-a-connection). Após uma atualização
   a partir de uma release anterior à 2026.06, converta primeiro para ODBC todas as conexões que ainda
   não o usavam.

Para começar a usar os novos módulos, consulte [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Conectar um Agente de IA](../../../platform/agentic/connect_ai_agent.md) para o digna MCP Server e
[Profiling Location](../../../platform/profiling/profiling_location.md) para o digna Engine.
