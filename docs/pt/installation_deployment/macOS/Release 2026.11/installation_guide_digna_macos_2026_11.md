---
title: Guia de Instalação no macOS – digna Release 2026.11 | digna Documentation
description: Guia passo a passo para instalar o digna Release 2026.11 no macOS — requisitos do sistema, configuração do Homebrew e PostgreSQL, configuração do nginx ou Apache, configuração do backend e do dashboard, execução do digna como serviço em segundo plano e atualização a partir da Release 2026.06.
keywords: digna macos installation, digna mac deployment guide, digna backend setup, digna dashboard installation, postgresql homebrew, nginx macos, digna launchd service, digna upgrade guide
image: /assets/logo_square.png
---

# Guia de Instalação no macOS para o digna Release 2026.11

**Release:** 2026.11

**Última Atualização:** 7 de novembro de 2026


---

## Sumário

1. [Introdução](#introduction)
2. [Requisitos do Sistema](#system-requirements)
3. [Pré-instalação](#pre-installation-setup)
4. [Configuração do Servidor PostgreSQL](#postgresql-server-setup)
5. [Configuração do Servidor Web](#web-server-configuration)
6. [Instalação Inicial](#initial-installation)
7. [Configuração do Backend](#backend-configuration)
8. [Configuração do Dashboard](#dashboard-configuration)
9. [Executando o digna como um Serviço em Segundo Plano](#running-digna-as-a-background-service)
10. [Atualizando para uma Nova Release](#upgrading-to-a-new-release)

---

## Introdução {: #introduction }

### Sobre o digna

digna é uma plataforma abrangente guiada por IA, projetada para otimizar o gerenciamento da qualidade de dados em diversos ambientes de dados, como data warehouses, data lakes e lakehouses. Desenvolvida para ser altamente escalável e adaptável, digna resolve desafios modernos de dados por meio de automação, monitoramento em tempo real e detecção de anomalias.

O digna consiste em dois componentes principais:

- **digna**: o núcleo da aplicação, responsável por processar os dados e executar as verificações de qualidade. Reúne o backend e a interface de linha de comando em um único executável, substituindo os programas separados `dignabackend` e `dignacli` das versões anteriores.
- **dignadashboard**: Uma interface web hospedada em um servidor web, que fornece uma forma amigável de interagir com a plataforma digna e visualizar métricas de qualidade de dados.

### Novidades no Release 2026.11

Esta release adiciona o digna Data Reconciliation, o digna Agentic com o digna MCP Server e o digna Engine, que pode fazer o profiling dos dados dentro do digna e verificar a integridade referencial entre diferentes tecnologias de banco de dados. Consulte as [notas de versão](../../../changelog/Release_202611.md) para detalhes completos.

Para uma instalação, a release traz um novo mecanismo de migração do repositório, uma seção `[duckdb]` opcional no `config.toml` para o digna Engine e um novo arquivo de licença. A [seção de atualização](#upgrading-to-a-new-release) aborda cada um deles.

### Procurando Windows ou Linux?

Este guia cobre o macOS. Para outras plataformas, veja o [Windows Installation Guide](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) ou o [Linux Installation Guide](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Requisitos do Sistema {: #system-requirements }

Antes de iniciar a instalação, verifique se seu sistema atende aos seguintes requisitos mínimos:

| Requisito | Especificação |
|---|---|
| **Sistema Operacional** | macOS 13 (Ventura) ou posterior |
| **Arquitetura** | Apple Silicon (arm64) ou Intel (x86_64) |
| **Memória (Configuração Mínima)** | 16 GB de RAM |
| **Espaço em Disco** | 10 GB de armazenamento disponível |
| **Banco de Dados** | PostgreSQL Server 12 ou superior |
| **Servidor Web** | nginx, Apache httpd ou equivalente |
| **Ferramentas de Linha de Comando** | Xcode Command Line Tools (requerido pelo Homebrew) |

!!! info "digna Engine"

    As conexões de banco de dados que usam o digna Engine como local de profiling passam pelo profiling no
    próprio host do digna. Planeje memória e espaço em disco adicionais para elas; consulte a
    [seção \[duckdb\]](#duckdb-section).

### Opções de Instalação do Banco de Dados

**Se o PostgreSQL já estiver instalado:**
Você pode adicionar um novo banco de dados para o digna ao seu servidor PostgreSQL existente.

**Se for instalar o PostgreSQL na mesma máquina que o digna:**

!!! info "Especificações recomendadas"

    - **Memória**: 32 GB de RAM (em vez de 16 GB)
    - **Espaço em Disco**: 50 GB de armazenamento disponível (em vez de 10 GB)

    Essas especificações mais altas acomodam tanto o digna quanto o banco de dados PostgreSQL em execução simultaneamente.

### Verificando Sua Arquitetura

Vários caminhos neste guia diferem entre Macs Apple Silicon e Intel. Para verificar qual você possui, abra o **Terminal** e execute:

```bash
uname -m
```

- `arm64` — Apple Silicon. O Homebrew instala em `/opt/homebrew`.
- `x86_64` — Intel. O Homebrew instala em `/usr/local`.

!!! tip "Dica"

    Em vez de codificar um caminho fixo, este guia usa `$(brew --prefix)`, que expande para o local correto em ambas as arquiteturas. Você pode copiar os comandos literalmente.

---

## Pré-instalação {: #pre-installation-setup }

Antes de instalar o digna, certifique-se de que três pré-requisitos principais estejam em vigor:

1. **Homebrew** – o gerenciador de pacotes utilizado para instalar os componentes abaixo
2. **PostgreSQL Server** – para armazenar métricas calculadas e dados de desempenho
3. **Servidor Web** – para hospedar o digna Dashboard

Se esses componentes ainda não estiverem configurados, siga as seções abaixo para instalá-los e configurá-los.

### Instalando o Homebrew

O Homebrew é o gerenciador de pacotes padrão para macOS e é usado ao longo deste guia para instalar PostgreSQL e nginx.

#### Passo 1: Verificar se o Homebrew já está instalado

Abra o **Terminal** (pressione `Cmd + Space`, digite `Terminal`, pressione Enter) e execute:

```bash
brew --version
```

Se um número de versão for retornado, pule para a seção [Configuração do Servidor PostgreSQL](#postgresql-server-setup).

#### Passo 2: Instalar o Homebrew

Se o comando não for encontrado, instale o Homebrew seguindo as instruções no [site oficial do Homebrew](https://brew.sh). O instalador também instala as Xcode Command Line Tools se elas não estiverem presentes.

#### Passo 3: Adicionar o Homebrew ao seu PATH

No Apple Silicon, o instalador imprime dois comandos para adicionar o Homebrew ao seu ambiente de shell. Execute-os conforme instruído e depois confirme:

```bash
brew --prefix
```

Isto deve imprimir `/opt/homebrew` no Apple Silicon ou `/usr/local` no Intel.

---

## Configuração do Servidor PostgreSQL {: #postgresql-server-setup }

### Se Você Já Tem PostgreSQL

Se o PostgreSQL já estiver instalado e em execução na sua máquina local ou se você estiver usando um servidor PostgreSQL gerenciado remoto, você pode pular para a [próxima seção](#web-server-configuration).

### Opções de Instalação

O macOS oferece duas maneiras simples de instalar o PostgreSQL. Escolha **uma**:

- [Homebrew](#postgresql-homebrew) — instalação via linha de comando, recomendada para implantações de servidor
- [Postgres.app](#postgresql-app) — instalação gráfica, conveniente para avaliação local

### Instalando PostgreSQL com Homebrew {: #postgresql-homebrew }

#### Passo 1: Instalar a fórmula do PostgreSQL

```bash
brew install postgresql@16
```

#### Passo 2: Adicionar o PostgreSQL ao seu PATH

As fórmulas versionadas do PostgreSQL são *keg-only*, o que significa que o Homebrew não vincula seus comandos ao seu PATH automaticamente. Adicione-os você mesmo:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Observação"

    Isto assume o shell `zsh` padrão usado pelo macOS. Se você usa `bash`, acrescente a mesma linha em `~/.bash_profile` em vez disso.

#### Passo 3: Iniciar o serviço PostgreSQL

```bash
brew services start postgresql@16
```

Isto inicia o PostgreSQL imediatamente e o configura para iniciar automaticamente quando você efetuar login.

#### Passo 4: Verificar a instalação

```bash
psql --version
```

Você deverá ver a versão do PostgreSQL se a instalação foi bem-sucedida.

#### Passo 5: Conectar-se ao servidor

```bash
psql postgres
```

!!! warning "Importante — o macOS difere do Windows aqui"

    O instalador do Windows solicita a criação de um superusuário `postgres` e uma senha. O Homebrew não faz isso. Em vez disso, ele cria um superusuário com o nome da sua **conta macOS**, sem senha, acessível somente a partir da máquina local.

    Isso significa que não existe a role `postgres` em uma instalação Homebrew nova. Use o nome da sua conta quando precisar de um superusuário e crie um usuário explícito para o digna conforme descrito em [Instalação Inicial](#initial-installation).

#### Passo 6: Confirmar a porta

A porta padrão do PostgreSQL é `5432`. Para confirmar a porta em que seu servidor está escutando:

```bash
psql postgres -c "SHOW port;"
```

Anote o valor — você precisará dele ao configurar o backend do digna.

### Instalando PostgreSQL com Postgres.app {: #postgresql-app }

Se preferir uma instalação gráfica:

1. Baixe o [Postgres.app](https://postgresapp.com) e arraste-o para a sua pasta **Applications**
2. Abra o app e clique em **Initialize** para criar um novo servidor
3. Siga as instruções do app para adicionar suas ferramentas de linha de comando ao PATH
4. Verifique a instalação:

```bash
psql --version
```

O Postgres.app também cria um superusuário com o nome da sua conta macOS.

---

## Configuração do Servidor Web {: #web-server-configuration }

O digna requer um servidor web para hospedar o dashboard. Escolha uma das seguintes opções:

- [nginx](#nginx-setup) — instalado via Homebrew, recomendado
- [Apache httpd](#apache-setup) — incluído no macOS

Você só precisa instalar e configurar **um** desses servidores.

Ambas as seções configuram duas coisas das quais o dashboard depende:

- **Fallback para single-page application**, para que atualizar a URL do dashboard no navegador não retorne 404
- **Um tipo MIME para `.md`**, para que arquivos Markdown sejam servidos corretamente

### Configuração do nginx {: #nginx-setup }

#### Visão Geral

O nginx é um servidor web leve e de alto desempenho, adequado para servir o dashboard estático do digna.

#### Instalação

```bash
brew install nginx
```

#### Iniciando o nginx

```bash
brew services start nginx
```

#### Verificar a Instalação

1. Abra seu navegador
2. Navegue para `http://localhost:8080`
3. Você deverá ver a página de boas-vindas do nginx

!!! note "Observação — porta padrão é 8080, não 80"

    O Homebrew configura o nginx para escutar na porta `8080` para que ele possa ser executado sem privilégios de administrador. No macOS, vincular a porta `80` ou qualquer outra abaixo de 1024 requer root.

    Para servir o dashboard na porta 80, altere `listen 8080;` para `listen 80;` na configuração abaixo e inicie o nginx com `sudo brew services start nginx` em vez disso.

#### Configurando um Site para o Dashboard

A configuração do nginx do Homebrew inclui todos os arquivos do diretório `servers`. Crie um arquivo de configuração dedicado para o digna lá:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Cole o seguinte, substituindo `/path/to/digna/dashboard` pelo caminho real da sua pasta `dashboard` extraída:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Importante"

    Sem a diretiva `try_files`, recarregar qualquer página do dashboard que não seja a URL raiz retorna 404. Isto é o equivalente no nginx ao módulo URL Rewrite exigido pelo IIS no Windows.

#### Aplicar a Configuração

Teste a configuração para erros de sintaxe e então recarregue o nginx:

```bash
nginx -t
brew services restart nginx
```

---

### Configuração do Apache httpd {: #apache-setup }

#### Visão Geral

O macOS inclui o Apache httpd, portanto não é necessária instalação. Ele vem desativado por padrão.

#### Iniciando o Apache

```bash
sudo apachectl start
```

#### Verificar a Instalação

1. Abra seu navegador
2. Navegue para `http://localhost`
3. Você deverá ver a mensagem "It works!"

#### Obrigatório: Habilitar mod_rewrite

O dashboard requer reescrita de URL. Abra a configuração do Apache:

```bash
sudo nano /etc/apache2/httpd.conf
```

Encontre a seguinte linha e remova o `#` inicial para descomentá-la:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Obrigatório: Permitir Overrides via .htaccess

No mesmo arquivo, localize o bloco `<Directory "/Library/WebServer/Documents">` e altere:

```apache
AllowOverride None
```

para:

```apache
AllowOverride All
```

#### Obrigatório: Tipo MIME para Arquivos Markdown

Ainda em `httpd.conf`, adicione a linha a seguir para que arquivos Markdown sejam servidos corretamente:

```apache
AddType text/markdown .md
```

!!! warning "Importante"

    Sem essa configuração, arquivos `.md` podem não ser servidos corretamente.

#### Aplicar a Configuração

Verifique a configuração por erros de sintaxe e então reinicie o Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Instalação Inicial {: #initial-installation }

### Passo 1: Configure o Repositório do digna

O repositório do digna armazena todas as métricas calculadas pelo digna. Ele atua como o banco de dados central para dados analíticos e de desempenho.

#### Criar Esquema e Usuário do Repositório

Abra seu cliente PostgreSQL (psql, pgAdmin ou similar) e execute os seguintes comandos SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Substitua os seguintes placeholders:**

- `<digna_repo_schema>` — O nome do schema desejado (por exemplo, `dignarepo`)
- `<digna_repo_user>` — O nome de usuário desejado (por exemplo, `digna_user`)
- `<digna_repo_password>` — Uma senha segura para este usuário

**Exemplo:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Para executar isso a partir do Terminal em um único passo:

```bash
psql postgres
```

Em seguida cole as instruções no prompt `postgres=#` e digite `\q` para sair.

!!! tip "Boa prática"

    Use senhas fortes e complexas para usuários de banco de dados. Evite credenciais facilmente adivinháveis.

---

### Passo 2: Extraia o Pacote de Instalação do digna

1. Localize o arquivo ZIP de instalação do digna fornecido a você
2. Extraia-o para o local de instalação desejado — por exemplo `/opt/digna` ou `~/digna`
3. Após a extração, você deverá ver os seguintes itens:
   - `dashboard/` — Interface web do dashboard
   - `digna` — Executável principal (backend + CLI combinados)

!!! info "Os arquivos de configuração e de licença não estão no pacote"

    Nem o `config.toml` nem o `dashboard/dashboard_config.toml` acompanham a instalação — você
    cria os dois, em [Configuração do Backend](#backend-configuration) e
    [Configuração do Dashboard](#dashboard-configuration). O `license.toml` também não acompanha;
    o digna o fornece separadamente, conforme descrito no Passo 3.

Para extrair pelo Terminal:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
```

#### Tornar o Executável Executável

Dependendo de como o arquivo foi transferido, o bit de execução pode não sobreviver à extração. Defina-o explicitamente:

```bash
cd /opt/digna
chmod +x digna
```

#### Se o macOS Bloquear a Aplicação

Arquivos baixados via navegador ou cliente de e-mail são marcados com um atributo de quarentena. Se o macOS relatar que o app *"cannot be opened because the developer cannot be verified"*, remova o atributo da pasta de instalação:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Alternativamente, abra **System Settings → Privacy & Security**, encontre o item bloqueado próximo ao final da página e clique em **Open Anyway**.

!!! note "Observação"

    Esta etapa só é necessária se o macOS realmente bloquear o executável. Pacotes transferidos por SSH ou de compartilhamentos internos normalmente não são colocados em quarentena.

### Passo 3: Instalar o Arquivo de Licença

!!! warning "Importante"

    O arquivo de licença **não** está incluído no pacote de instalação e será fornecido separadamente pela digna.

1. Localize o arquivo `license.toml` fornecido a você
2. Copie-o para o diretório raiz de instalação do digna (onde estão `config.toml` e o executável `digna`)

**Por que isso é importante:**
O arquivo de licença contém suas informações de cliente, data de expiração da licença e assinatura digital. **Não modifique este arquivo** — quaisquer alterações o invalidarão.

**Estrutura de diretórios após a configuração:**

```
/opt/digna/
├── config.toml         (arquivo de configuração)
├── license.toml        (SEU ARQUIVO DE LICENÇA - copie aqui)
├── digna               (executável principal)
├── bin/                (scripts de gerenciamento do serviço)
└── dashboard/          (interface web)
    └── (arquivos do dashboard)
```

---

## Configuração do Backend {: #backend-configuration }

### Passo 1: Criar e Editar o Arquivo de Configuração

O arquivo `config_template.toml` é fornecido no diretório de instalação do digna. Você só precisa renomeá-lo para `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Localização:** `/opt/digna/config.toml`

Abra `config.toml` em um editor de texto e configure cada seção abaixo.

#### Seção [app]

Esta seção configura o compartilhamento de recursos entre origens (CORS) entre o dashboard e o backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parâmetro | Valor | Observações |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | URLs do dashboard | As URLs a partir das quais o dashboard é servido. Requisições do navegador vindas de qualquer outra origem são rejeitadas |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Obrigatório, para que o navegador envie o cookie de sessão em cada requisição |

!!! note "Observação"

    Se você servir o dashboard a partir do nginx do Homebrew na porta padrão, a origem a ser permitida é `http://localhost:8080`.

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

| Parâmetro | Valor | Observações |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` ou IP | Hostname/IP do servidor PostgreSQL |
| `DIGNA_REPO_PORT` | `5432` (padrão) | Porta do PostgreSQL |
| `DIGNA_REPO_DB` | `postgres` | Nome do banco de dados |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Schema criado anteriormente |
| `DIGNA_REPO_USER` | `digna_user` | Usuário criado na configuração do PostgreSQL |
| `DIGNA_REPO_PASSWORD` | Sua senha | Senha definida durante a criação do schema |
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

| Parâmetro | Valor | Observações |
|---|---|---|
| `DIGNA_FERNET_KEY` | Valor mostrado acima | Chave da criptografia usada pelas releases anteriores. Ela precisa estar presente; mantenha o valor mostrado |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Host pelo qual o dashboard é acessado. `""` não define nenhum domínio, o que é o correto atrás de um proxy que serve o dashboard e o backend sob uma única origem |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Deve ser `true` sempre que o digna for servido por HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Mantém o cookie de sessão fora do alcance de scripts |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 horas) | Tempo de expiração da sessão em segundos |
| `DIGNA_MAX_WORKERS` | Número de cores da CPU - 1 | Número de inspeções que podem ser executadas ao mesmo tempo |
| `DIGNA_FRONTEND_BASEURL` | URL do dashboard | Obrigatório. Usado nos links das mensagens de notificação, portanto deve ser uma URL que os destinatários consigam abrir |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (padrão) | Opcional. Segundos durante os quais uma única consulta a um banco de dados de origem pode ser executada antes de ser abortada; `0` desativa o timeout |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (padrão) | Opcional. Segundos de espera por uma conexão com um banco de dados de origem; `0` espera indefinidamente |

!!! tip "Dica"

    Para descobrir o número de núcleos de CPU disponíveis no seu Mac, execute `sysctl -n hw.ncpu`.

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

| Parâmetro | Valor | Observações |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` ou `DEBUG` | `INFO` para produção, `DEBUG` para resolução de problemas. `TRACE`, `WARN` e `ERROR` também são aceitos |
| `DIGNA_LOGGING_DIR` | `logs` (padrão) | Opcional. Diretório dos arquivos de log rotativos, relativo ao diretório de trabalho |
| `DIGNA_LOGGING_MAX_FILES` | `30` (padrão) | Opcional. Número de arquivos de log rotacionados a manter |

#### Seção [duckdb] (Opcional) {: #duckdb-section }

Novidade da Release 2026.11. Esta seção define os recursos do **digna Engine**, que faz o profiling
dos dados dentro do digna para as conexões de banco de dados cujo local de profiling é **digna Engine**, e
executa verificações de integridade referencial entre fontes de dados em conexões de banco de dados diferentes. Consulte
[Profiling Location](../../../platform/profiling/profiling_location.md).

A seção é opcional. Sem ela, valem os padrões abaixo.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parâmetro | Valor | Observações |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (padrão) | Memória, em MB, que uma execução do digna Engine pode usar. Até `DIGNA_MAX_WORKERS` execuções podem estar ativas ao mesmo tempo |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Padrão: o diretório temporário do sistema (`$TMPDIR` da conta que executa o digna) | Diretório para arquivos temporários quando os dados não cabem na memória |

!!! tip "Dimensionando o digna Engine"

    Planeje até `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` de memória no host do digna,
    além do que o próprio digna usa, e espaço livre em disco suficiente no diretório temporário
    para comportar a maior data inspecionada das fontes de dados que usam o digna Engine.
    Aponte `DIGNA_DUCKDB_TEMP_DIRECTORY` para um disco com esse espaço, com permissão de escrita para a
    conta que executa o digna:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    Você só precisa desta seção se pelo menos uma conexão de banco de dados usar o digna Engine, ou se uma
    verificação de integridade referencial comparar fontes de dados em conexões diferentes.

---

### Passo 2: Validar a Configuração

Antes de inicializar o repositório, verifique se o `config.toml` está completo e bem formado. No diretório de instalação do digna, execute:

```bash
./digna config check
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

1. Abra o **Terminal**
2. Navegue até o diretório de instalação do digna (onde `config.toml` e o executável `digna` estão localizados)
3. Execute o teste de conexão:

```bash
cd /opt/digna
./digna repo check
```

Em um schema novo, o comando se conecta e então informa que ainda não há nenhum repositório instalado:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Neste ponto, esse é o resultado esperado: ele confirma que o digna alcança o PostgreSQL e o schema. Já um erro de conexão ou de autenticação aponta para a seção `[repo]` ou para a configuração do PostgreSQL.

!!! note "Observação"

    No macOS, comandos no diretório atual não estão no seu PATH, então o executável é invocado como `./digna` em vez de `digna`. Para usar a forma curta em qualquer lugar, adicione o diretório de instalação ao seu PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Passo 4: Instalar o Schema do Repositório

No mesmo diretório, execute:

```bash
./digna repo upgrade
```

Este comando instala as tabelas necessárias no schema do repositório e termina com:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade instala e atualiza"

    A partir da Release 2026.11, `repo upgrade` instala um novo repositório e atualiza um existente.
    `repo install` continua funcionando como outro nome para o mesmo comando.

### Passo 5: Criar um Usuário Admin

1. Abra uma nova janela do **Terminal**
2. Navegue até o diretório de instalação do digna
3. Execute o seguinte comando para criar um usuário admin:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Exemplo:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Isto cria um utilizador com o endereço de e-mail `admin@example.com` e privilégios administrativos completos.

!!! tip "Dica"

    Coloque a senha entre aspas simples. O `zsh` trata caracteres como `!`, `$` e `*` de forma especial, e uma senha não entre aspas contendo esses caracteres não será passada como digitada.

!!! tip "Boa prática"

    Use uma senha forte com mistura de maiúsculas, minúsculas, números e caracteres especiais.

---

### Passo 6: Iniciar o Servidor digna

No diretório de instalação do digna, inicie o servidor com:

```bash
./digna serve --address <host> --port <port>
```

**Parâmetros:**
- `--address` — Hostname/IP do servidor (padrão `127.0.0.1`)
- `--port` — Porta do servidor (padrão `8000`)

Quando o servidor estiver no ar, ele exibe o endereço em que está escutando:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Dica"

    A primeira vez que você iniciar o servidor, o macOS pode perguntar se deseja permitir que a aplicação aceite conexões de rede. Clique em **Allow**, caso contrário o dashboard não conseguirá atingir o backend.

!!! note "O servidor ocupa o terminal"

    `serve` roda em primeiro plano e continua até você pará-lo com ++ctrl+c++. Deixe-o rodando enquanto termina a configuração; para iniciá-lo automaticamente na inicialização, consulte [Executar o digna como Serviço em Segundo Plano](#running-digna-as-a-background-service).

## Configuração do Dashboard {: #dashboard-configuration }

### Passo 1: Fazer o Deploy do Dashboard no Servidor Web

O dashboard do digna lê sua própria configuração do arquivo `dashboard/dashboard_config.toml`. Esse arquivo não acompanha a instalação — você o cria no diretório `dashboard/`, junto com os arquivos do dashboard.

O conteúdo dele está descrito em [Single Sign-On](../../../sso/overview.md), que é também onde o arquivo é necessário: ele contém as opções de login que o dashboard oferece e, em implantações com múltiplas instâncias, a conexão com o backend.

Escolha seu servidor web e siga as etapas de implantação correspondentes.

#### Implantando no nginx

Se você seguiu a seção de [Configuração do nginx](#nginx-setup), o server block já aponta para sua pasta `dashboard` e nenhuma cópia é necessária.

1. **Confirme o caminho**
   - Abra `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Verifique se `root` aponta para a sua pasta `dashboard` extraída

2. **Garanta que a pasta seja legível**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Recarregue o nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Teste a Instalação**
   - Abra seu navegador
   - Navegue para `http://localhost:8080` (ou sua URL configurada)
   - Você deverá ver a página de login do digna dashboard

#### Implantando no Apache httpd

1. **Copie o Dashboard para o Document Root**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Adicione as Regras de Rewrite**

   Crie um arquivo `.htaccess` dentro da pasta implantada para que as rotas do dashboard sobrevivam a um refresh do navegador:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Cole o seguinte:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **Reinicie o Apache**
   ```bash
   sudo apachectl restart
   ```

4. **Acesse o Dashboard**
   - Abra seu navegador
   - Navegue para `http://localhost/digna`
   - Você deverá ver a página de login do digna dashboard

---

## Executando o digna como um Serviço em Segundo Plano {: #running-digna-as-a-background-service }

### Por que executar o digna como um serviço?

Executar o backend do digna como serviço em segundo plano garante que ele:

- Inicie automaticamente quando a máquina for ligada
- Execute em segundo plano sem uma janela do Terminal aberta
- Reinicie automaticamente se travar
- Possa ser gerenciado através do `launchctl`, o gerenciador de serviços do macOS

### Arquivos de Gerenciamento do Serviço

Todos os arquivos necessários estão localizados no diretório de instalação do digna em: `bin/`

Os seguintes scripts shell estão disponíveis:

- `install_service.sh` — Registra o digna no launchd
- `uninstall_service.sh` — Remove o registro do serviço
- `start_service.sh` — Inicia o serviço registrado
- `stop_service.sh` — Para o serviço em execução

!!! warning "Administrador requerido"

    Todos os scripts devem ser executados com `sudo`, pois registrar um serviço que inicia na inicialização grava em `/Library/LaunchDaemons`.

### Tornando os Scripts Executáveis

A extração pode não preservar o bit executável. Antes do primeiro uso:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Instalando o Serviço

1. **Abra o Terminal**

2. **Navegue até a pasta bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Execute o script de instalação**
   ```bash
   sudo ./install_service.sh
   ```

O servidor digna agora está registrado no launchd com inicialização **automática** habilitada. O serviço não inicia imediatamente — veja a seção a seguir para iniciá-lo.

### Iniciando e Parando o Serviço

#### Para Iniciar o Serviço

1. Abra o Terminal
2. Navegue para `/opt/digna/bin`
3. Execute:
   ```bash
   sudo ./start_service.sh
   ```

#### Para Parar o Serviço

1. Abra o Terminal
2. Navegue para `/opt/digna/bin`
3. Execute:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Dica"

    Sempre pare o serviço antes de atualizar arquivos da aplicação.

### Verificando o Serviço

Para confirmar que o serviço está registrado e em execução:

```bash
sudo launchctl list | grep digna
```

Uma linha começando com um ID de processo indica que o serviço está em execução. Um `-` na primeira coluna significa que está registrado mas parado.

### Movendo o Serviço para um Novo Diretório

O launchd armazena o caminho absoluto para o executável, portanto mover a instalação exige re-registrar o serviço:

1. **Desinstalar o serviço atual**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Mover os arquivos da aplicação**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Reinstalar o serviço**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Iniciar o serviço**
   ```bash
   sudo ./start_service.sh
   ```

### Desinstalando o Serviço

1. **Parar o serviço em execução**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Desinstalar o serviço**
   ```bash
   sudo ./uninstall_service.sh
   ```

O servidor digna agora está desregistrado do launchd.

---

## Atualizando para uma Nova Release {: #upgrading-to-a-new-release }

Esta seção atualiza uma instalação da Release 2026.06 para a Release 2026.11.

!!! warning "Atualização a Partir de uma Release Anterior à 2026.06"

    Primeiro, execute as etapas de atualização da Release 2026.06: [Atualizando para uma Nova Release](../Release%202026.06/installation_guide_digna_macos_2026_06.md#upgrading-to-a-new-release). Depois, continue com as etapas abaixo.

### Antes de Atualizar

**É Obrigatório Criar um Backup do Repositório do digna**

Antes de atualizar o digna, faça backup do seu repositório (PostgreSQL) para proteger contra perda de dados.
Um backup garante que você possa recuperar caso a atualização encontre problemas inesperados.

Para criar um backup a partir do Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Solicitando o Arquivo de Licença para a Release 2026.11**

A Release 2026.11 precisa de um novo `license.toml`. Solicite-o à equipe do digna antes de começar e
deixe-o pronto para o [Passo 7](#step-7-replace-the-license-file).

### Processo de Atualização

#### Passo 1: Parar o Serviço digna {: #step-1-stop-the-digna-service }

Se o digna estiver em execução como serviço em segundo plano, pare-o primeiro:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Se o digna estiver em execução em primeiro plano, pressione ++ctrl+c++ na janela do Terminal onde ele está rodando.

#### Passo 2: Fazer Backup da Instalação Atual {: #step-2-backup-current-installation }

No diretório de instalação do digna, renomeie o executável e a pasta do dashboard da sua
instalação atual, para que a nova release possa ser implantada ao lado deles:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

Mantenha `digna_old` até verificar a atualização, e `dashboard_old` até restaurar dele os seus
arquivos de configuração (veja o Passo 4). Depois, você pode excluir ambos.

#### Passo 3: Extrair e Implantar a Nova Versão {: #step-3-extract-and-deploy-new-version }

1. Extraia o novo arquivo ZIP de instalação do digna
2. Copie o novo executável `digna` e a pasta `dashboard` para seu diretório de instalação
3. Restaure o bit de execução e, se necessário, limpe o atributo de quarentena:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Importante"

    Nem o `config.toml` nem o `dashboard/dashboard_config.toml` são incluídos no ZIP de
    instalação — a equipe do digna nunca distribui nenhum dos dois arquivos. Por isso, sua
    configuração existente não é afetada pela atualização, e as cópias nas pastas renomeadas
    `*_old` são as únicas que você tem.

#### Passo 4: Restaurar Seus Arquivos de Configuração {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
`dashboard` e, em seguida, recarregue a página com uma atualização forçada (++cmd+shift+r++).

#### Passo 6: Validar a Configuração {: #step-6-validate-the-configuration }

Confirme que o `config.toml` está completo antes de mexer no repositório:

```bash
./digna config check
```

Todas as seções devem informar OK. Corrija tudo o que for informado como FAILED, remova as chaves listadas em
**Unknown keys** e execute o comando novamente antes de continuar.

#### Passo 7: Substituir o Arquivo de Licença {: #step-7-replace-the-license-file }

Normalmente, um arquivo de licença continua valendo de uma release para a seguinte. A Release 2026.11 é uma
exceção: ela adiciona dois módulos licenciados, o digna Data Reconciliation e o digna Agentic, e uma licença
emitida antes da 2026.11 não os contém. Copie o `license.toml` que a equipe do digna forneceu para a
Release 2026.11 para o diretório de instalação, substituindo o antigo:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Não mantenha a licença anterior"

    Com a licença anterior, o digna ainda inicia, mas o digna Data Reconciliation e o digna
    MCP Server permanecem desativados. Todo comando que verifica a licença — `user`,
    `inspection`, `repo` — é interrompido antes de mexer no repositório quando a verificação falha.
    Verifique a nova licença antes de prosseguir:

    ```bash
    ./digna license check
    ```

#### Passo 8: Atualizar o Schema do Repositório {: #step-8-upgrade-the-repository-schema }

No diretório de instalação do digna, execute:

```bash
cd /opt/digna
./digna repo upgrade
```

A Release 2026.11 gerencia o schema do repositório com migrações versionadas. A primeira atualização a partir
de uma release anterior leva o schema à última versão do mecanismo anterior, registra isso como ponto de
partida e, em seguida, aplica as migrações da Release 2026.11. Ela termina com:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Todos os dados existentes são preservados. Para ver o estado do repositório a qualquer momento, execute
`./digna repo check`: ele lista a última migração aplicada e as migrações pendentes.

!!! warning "O digna não inicia com um repositório desatualizado"

    A partir da Release 2026.11, o servidor se recusa a iniciar enquanto o repositório precisar de uma
    atualização, e informa isso, por exemplo:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Execute `repo upgrade` antes de iniciar o servidor ou o serviço.

#### Passo 9: Reiniciar Serviços {: #step-9-restart-services }

Se estiver rodando como serviço em segundo plano:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Se estiver executando manualmente, reinicie o servidor:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Se estiver usando nginx ou Apache, reinicie o respectivo servidor web:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Passo 10: Verificar a Atualização {: #step-10-verify-the-upgrade }

1. Confirme a release do novo executável:

    ```bash
    ./digna version
    ```

    A primeira linha deve ser `Release: 2026.11`.

2. Acesse o digna dashboard e verifique se a interface carrega corretamente.
3. Verifique a saída do servidor e os arquivos no diretório `logs` em busca de erros.
4. Teste suas conexões de banco de dados — consulte
   [Testar uma Conexão](../../../databases/overview.md#testing-a-connection). Após uma atualização
   a partir de uma release anterior à 2026.06, converta primeiro para ODBC todas as conexões que ainda
   não o usavam.

Para começar a usar os novos módulos, consulte [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Conectar um Agente de IA](../../../platform/agentic/connect_ai_agent.md) para o digna MCP Server e
[Profiling Location](../../../platform/profiling/profiling_location.md) para o digna Engine.
