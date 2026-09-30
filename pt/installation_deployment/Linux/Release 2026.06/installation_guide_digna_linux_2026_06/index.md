# Guia de Instalação no Linux para o digna Release 2026.06

**Release:** 2026.06

**Última Atualização:** 5 de setembro de 2026


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
9. [Executando o digna como um Serviço systemd](#running-digna-as-a-systemd-service)
10. [Atualizando para uma Nova Release](#upgrading-to-a-new-release)

---

## Introdução {: #introduction }

### Sobre o digna

digna é uma plataforma abrangente guiada por IA, projetada para otimizar o gerenciamento da qualidade de dados em diversos ambientes de dados, como data warehouses, data lakes e lakehouses. Desenvolvida para ser altamente escalável e adaptável, digna resolve desafios modernos de dados por meio de automação, monitoramento em tempo real e detecção de anomalias.

O digna consiste em dois componentes principais:

- **digna**: o núcleo da aplicação, responsável por processar os dados e executar as verificações de qualidade. Reúne o backend e a interface de linha de comando em um único executável, substituindo os programas separados `dignabackend` e `dignacli` das versões anteriores.
- **dignadashboard**: Uma interface web hospedada em um servidor web, que fornece uma forma amigável de interagir com a plataforma digna e visualizar métricas de qualidade de dados.

### Novidades no Release 2026.06

Esta release traz capacidades de observabilidade de dados diretamente para o seu código, permitindo que desenvolvedores monitorem a qualidade dos dados na origem. Consulte as [notas de versão](http://docs.digna.ai/changelog/Release_202606/) para detalhes completos.

### Procurando Windows ou macOS?

Este guia cobre o Linux. Para outras plataformas, veja o [Guia de Instalação no Windows](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) ou o [Guia de Instalação no macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

### Quais Distribuições Este Guia Cobre?

As instruções foram escritas para as duas famílias de servidores mais comuns. Onde as duas diferem, os dois comandos são apresentados:

- **Família Debian** — Debian, Ubuntu. Gerenciador de pacotes: `apt`.
- **Família RHEL** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Gerenciador de pacotes: `dnf`.

Qualquer distribuição moderna com `systemd` funciona; apenas os nomes dos pacotes e alguns caminhos de configuração mudam.

---

## Requisitos do Sistema {: #system-requirements }

Antes de iniciar a instalação, verifique se seu sistema atende aos seguintes requisitos mínimos:

| Requisito | Especificação |
|---|---|
| **Sistema Operacional** | Ubuntu 22.04 LTS ou posterior, Debian 12 ou posterior, RHEL 9 / Rocky 9 / AlmaLinux 9 ou posterior |
| **Arquitetura** | x86_64 (amd64) ou arm64 |
| **Sistema de Inicialização** | systemd |
| **Memória (Configuração Mínima)** | 16 GB de RAM |
| **Espaço em Disco** | 10 GB de armazenamento disponível |
| **Banco de Dados** | PostgreSQL Server 12 ou superior |
| **Servidor Web** | nginx, Apache httpd ou equivalente |

### Opções de Instalação do Banco de Dados

**Se o PostgreSQL já estiver instalado:**
Você pode adicionar um novo banco de dados para o digna ao seu servidor PostgreSQL existente.

**Se for instalar o PostgreSQL na mesma máquina que o digna:**

!!! info "Especificações recomendadas"

    - **Memória**: 32 GB de RAM (em vez de 16 GB)
    - **Espaço em Disco**: 50 GB de armazenamento disponível (em vez de 10 GB)

    Essas especificações mais altas acomodam tanto o digna quanto o banco de dados PostgreSQL em execução simultaneamente.

### Verificando Sua Distribuição e Arquitetura

Vários comandos neste guia diferem entre as famílias Debian e RHEL. Para verificar qual você usa, execute:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` ou `ID=debian` — use os comandos `apt`.
- `ID=rhel`, `rocky`, `almalinux` ou `fedora` — use os comandos `dnf`.
- `x86_64` ou `aarch64` — a arquitetura do pacote de instalação de que você precisa.

---

## Pré-instalação {: #pre-installation-setup }

Antes de instalar o digna, certifique-se de que dois pré-requisitos principais estejam em vigor:

1. **PostgreSQL Server** – para armazenar métricas calculadas e dados de desempenho
2. **Servidor Web** – para hospedar o digna Dashboard

Se esses componentes ainda não estiverem configurados, siga as seções abaixo para instalá-los e configurá-los.

### Atualizando o Índice de Pacotes

Atualize suas listas de pacotes antes de instalar qualquer coisa:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Observação"

    Ao longo deste guia, o primeiro comando de cada par é para a **família Debian** e o segundo para a **família RHEL**. Execute apenas o que corresponde ao seu sistema.

---

## Configuração do Servidor PostgreSQL {: #postgresql-server-setup }

### Se Você Já Tem PostgreSQL

Se o PostgreSQL já estiver instalado e em execução na sua máquina local ou se você estiver usando um servidor PostgreSQL gerenciado remoto, você pode pular para a [próxima seção](#web-server-configuration).

### Instalando o PostgreSQL

#### Passo 1: Instalar o Pacote do Servidor

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Dica"

    Os pacotes da distribuição podem estar atrasados em relação à release atual do PostgreSQL. Se você precisar de uma versão mais recente específica, use o [repositório apt ou yum oficial do PostgreSQL](https://www.postgresql.org/download/linux/).

#### Passo 2: Inicializar o Cluster de Banco de Dados

Na **família Debian**, o pacote cria e inicia um cluster automaticamente — pule para o próximo passo.

Na **família RHEL**, o cluster precisa ser criado explicitamente:

```bash
sudo postgresql-setup --initdb
```

#### Passo 3: Iniciar e Habilitar o Serviço

```bash
sudo systemctl enable --now postgresql
```

Isto inicia o PostgreSQL imediatamente e o configura para iniciar novamente de forma automática na inicialização do sistema.

#### Passo 4: Verificar a Instalação

```bash
psql --version
sudo systemctl status postgresql
```

Você deverá ver a versão do PostgreSQL e um serviço `active (running)`.

#### Passo 5: Conectar-se ao Servidor

Um pacote PostgreSQL para Linux cria uma conta de sistema `postgres`, que é dona do cluster. Conecte-se por meio dela:

```bash
sudo -u postgres psql
```

!!! note "Observação — o Linux Difere do Windows Aqui"

    O instalador do Windows solicita a definição de uma senha para o superusuário `postgres` durante a instalação. Os pacotes para Linux não fazem isso. Em vez disso, as conexões locais são autenticadas por **peer authentication**: o usuário `postgres` do sistema operacional pode se conectar como o usuário `postgres` do banco de dados sem senha.

    É por isso que o comando acima usa `sudo -u postgres`. O backend do digna se conecta via TCP com nome de usuário e senha, então você criará um usuário explícito para o digna em [Instalação Inicial](#initial-installation).

#### Passo 6: Confirmar a Porta

A porta padrão do PostgreSQL é `5432`. Para confirmar a porta em que seu servidor está escutando:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Anote o valor — você precisará dele ao configurar o backend do digna.

#### Passo 7: Habilitar a Autenticação por Senha para o Usuário do digna

O digna se conecta ao PostgreSQL via TCP como `digna_user`, o que exige autenticação por senha em vez de peer authentication. Verifique se o seu `pg_hba.conf` permite isso.

Localize o arquivo:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Abra-o em um editor e confirme que as linhas TCP locais usam `scram-sha-256` (ou `md5` em servidores mais antigos) em vez de `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Recarregue o PostgreSQL após qualquer alteração:

```bash
sudo systemctl reload postgresql
```

!!! warning "Importante"

    Se o digna informar `FATAL: Ident authentication failed for user "digna_user"`, a causa é esta configuração.

#### Passo 8: Se o PostgreSQL Rodar em Outra Máquina

Para aceitar conexões de outro host, defina `listen_addresses` em `postgresql.conf` e adicione uma linha `host` correspondente à sua rede em `pg_hba.conf`:

```
listen_addresses = '*'
```

Em seguida, abra a porta no firewall e reinicie o serviço:

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## Configuração do Servidor Web {: #web-server-configuration }

O digna requer um servidor web para hospedar o dashboard. Escolha uma das seguintes opções:

- [nginx](#nginx-setup) — leve e recomendado
- [Apache httpd](#apache-setup) — alternativa amplamente utilizada

Você só precisa instalar e configurar **um** desses servidores.

Ambas as seções configuram duas coisas das quais o dashboard depende:

- **Fallback para single-page application**, para que atualizar a URL do dashboard no navegador não retorne 404
- **Um tipo MIME para `.md`**, para que arquivos Markdown sejam servidos corretamente

### Configuração do nginx {: #nginx-setup }

#### Visão Geral

O nginx é um servidor web leve e de alto desempenho, adequado para servir o dashboard estático do digna.

#### Instalação

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### Iniciando o nginx

```bash
sudo systemctl enable --now nginx
```

#### Verificar a Instalação

1. Abra seu navegador
2. Navegue para `http://localhost`
3. Você deverá ver a página de boas-vindas do nginx

#### Abrindo o Firewall

Se o servidor for acessado a partir de outras máquinas, permita o tráfego HTTP:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Configurando um Site para o Dashboard

O nginx inclui todos os arquivos do seu diretório `conf.d` em ambas as famílias de distribuição. Crie ali um arquivo de configuração dedicado para o digna:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Cole o seguinte, substituindo `/opt/digna/dashboard` pelo caminho real da sua pasta `dashboard` extraída:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
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

#### Desativar o Site Padrão

Apenas um server block pode ser o `default_server` de uma porta. Na **família Debian**, remova o site padrão do pacote para que ele não entre em conflito:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

Na **família RHEL**, comente ou exclua o bloco `server { ... }` dentro de `/etc/nginx/nginx.conf`.

#### Aplicar a Configuração

Teste a configuração para erros de sintaxe e então recarregue o nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Configuração do Apache httpd {: #apache-setup }

#### Visão Geral

O Apache httpd está disponível nos repositórios padrão de todas as distribuições suportadas. O pacote se chama `apache2` na família Debian e `httpd` na família RHEL.

#### Instalação

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Iniciando o Apache

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Verificar a Instalação

1. Abra seu navegador
2. Navegue para `http://localhost`
3. Você deverá ver a página padrão do Apache da sua distribuição

#### Obrigatório: Habilitar mod_rewrite

O dashboard requer reescrita de URL.

Na **família Debian**, habilite o módulo e reinicie:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

Na **família RHEL**, o `mod_rewrite` é carregado por padrão. Confirme:

```bash
httpd -M | grep rewrite
```

#### Obrigatório: Permitir Overrides via .htaccess

Abra o arquivo de configuração do seu document root:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Localize o bloco `<Directory>` que cobre o seu document root (`/var/www/html` em ambas as famílias) e altere:

```apache
AllowOverride None
```

para:

```apache
AllowOverride All
```

#### Obrigatório: Tipo MIME para Arquivos Markdown

No mesmo arquivo, adicione a linha a seguir para que arquivos Markdown sejam servidos corretamente:

```apache
AddType text/markdown .md
```

!!! warning "Importante"

    Sem essa configuração, arquivos `.md` podem não ser servidos corretamente.

#### Aplicar a Configuração

Verifique a configuração por erros de sintaxe e então reinicie o Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
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

Para executar isso a partir do shell em um único passo:

```bash
sudo -u postgres psql
```

Em seguida, cole os comandos no prompt `postgres=#` e digite `\q` para sair.

!!! tip "Boa prática"

    Use senhas fortes e complexas para os usuários do banco de dados. Evite credenciais fáceis de adivinhar.

---

### Passo 2: Extraia o Pacote de Instalação do digna

1. Localize o arquivo ZIP de instalação do digna fornecido a você
2. Extraia-o para o local de instalação desejado — por exemplo `/opt/digna`
3. Após a extração, você deverá ver os seguintes itens:
   - `dashboard/` — Interface web do dashboard
   - `digna` — Executável principal (backend + CLI combinados)

!!! info "Os arquivos de configuração e de licença não estão no pacote"

    Nem o `config.toml` nem o `dashboard/dashboard_config.toml` acompanham a instalação — você
    cria os dois, em [Configuração do Backend](#backend-configuration) e
    [Configuração do Dashboard](#dashboard-configuration). O `license.toml` também não acompanha;
    o digna o fornece separadamente, conforme descrito no Passo 3.

Para extrair pelo shell:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
```

!!! note "Observação"

    Se o `unzip` não estiver instalado, adicione-o com `sudo apt install -y unzip` ou `sudo dnf install -y unzip`.

#### Tornar o Executável Executável

Dependendo de como o arquivo foi transferido, o bit de execução pode não sobreviver à extração. Defina-o explicitamente:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Criar uma Conta de Serviço

Executar o backend como um usuário dedicado sem privilégios é recomendado para implantações em produção:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Observação"

    Na família RHEL, o caminho de shell equivalente é `/sbin/nologin`.

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
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
├── bin/                (service management scripts)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Configuração do Backend {: #backend-configuration }

### Passo 1: Criar e Editar o Arquivo de Configuração

O arquivo `config_template.toml` é fornecido no diretório de instalação do digna. Você só precisa renomeá-lo para `config.toml`.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Localização:** `/opt/digna/config.toml`

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

| Parâmetro | Valor | Observações |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | URL do frontend | Se o dashboard estiver em servidor diferente, inclua sua URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Necessário para CORS com credenciais |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Permite todos os métodos HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Permite todos os cabeçalhos |

!!! note "Observação"

    Se você servir o dashboard a partir do nginx ou do Apache na porta HTTP padrão, a origem a ser permitida é `http://localhost` — ou a URL pública do servidor quando o dashboard for acessado a partir de outras máquinas.

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

| Parâmetro | Valor | Observações |
|---|---|---|
| `digna_REPO_HOST` | `localhost` ou IP | Hostname/IP do servidor PostgreSQL |
| `digna_REPO_PORT` | `5432` (padrão) | Porta do PostgreSQL |
| `digna_REPO_DB` | `postgres` | Nome do banco de dados |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema criado anteriormente |
| `digna_REPO_USER` | `digna_user` | Usuário criado na configuração do PostgreSQL |
| `digna_REPO_PASSWORD` | Sua senha | Senha definida durante a criação do schema |

!!! tip "Boa prática"

    O `config.toml` contém uma senha de banco de dados em texto simples. Restrinja suas permissões para que apenas a conta de serviço possa lê-lo:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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

| Parâmetro | Valor | Observações |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Deve corresponder ao domínio do frontend |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (produção) | Use `true` para conexões HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Sempre habilitado por segurança |
| `digna_COOKIE_SAME_SITE` | `lax` | Ajuda a prevenir ataques CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 horas) | Tempo de expiração da sessão em segundos |
| `digna_MAX_WORKERS` | Número de cores da CPU - 1 | Número de tarefas de inspeção paralelas |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Atraso máximo, em segundos, que o agendador pode acrescentar antes de iniciar uma tarefa pendente |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Horário (formato 24 h `HH:MM`) em que a limpeza diária começa |

!!! tip "Dica"

    Para descobrir o número de núcleos de CPU disponíveis no seu servidor, execute `nproc`.

#### Seção [encryption]

Esta seção contém a chave usada para criptografar os valores sensíveis armazenados no repositório. Ela é **obrigatória** — `config check` informa a seção `[encryption]` como FAILED se a chave estiver ausente.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parâmetro | Valor | Observações |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Chave codificada em Base64 | Criptografa os valores sensíveis armazenados no repositório digna |

!!! warning "Proteja o config.toml"

    Esta chave é um valor fixo, idêntico em todas as instalações do digna, e é ela que
    descriptografa os valores sensíveis do seu repositório. Restrinja o `config.toml` à conta que
    executa o digna, mantenha o arquivo fora do controle de versão e de unidades compartilhadas e
    exclua-o de qualquer backup guardado com menos segurança que o próprio repositório.

#### Seção [logging]

Esta seção configura o comportamento de logging:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parâmetro | Valor | Observações |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` ou `DEBUG` | `INFO` para produção, `DEBUG` para resolução de problemas |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Número de backups diários de logs a reter |

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

Overall: OK
```

Corrija tudo o que for informado como FAILED e execute o comando novamente antes de continuar. A lista completa de opções está na [referência da CLI](../../../cli/Command_Line_Interface_202606.md).

### Passo 3: Inicializar o Repositório

1. Abra um terminal
2. Navegue até o diretório de instalação do digna (onde `config.toml` e o executável `digna` estão localizados)
3. Execute o teste de conexão:

```bash
cd /opt/digna
./digna repo check
```

Você deverá ver uma confirmação de que a conexão foi estabelecida (o repositório em si ainda não foi inicializado).

!!! note "Observação"

    No Linux, o diretório atual não está no seu PATH, então o executável é invocado como `./digna` em vez de `digna`. Para usar a forma curta em qualquer lugar, adicione um link simbólico:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Passo 4: Instalar o Schema do Repositório

No mesmo diretório, execute:

```bash
./digna repo install
```

Este comando instala as tabelas e o schema necessários no seu banco de dados PostgreSQL.

### Passo 5: Criar um Usuário Admin

O usuário admin é criado diretamente no schema do repositório, portanto o servidor ainda não precisa estar em execução. No diretório de instalação do digna, execute:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Exemplo:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Isto cria um usuário com o e-mail `admin@example.com` e privilégios administrativos completos.

!!! tip "Dica"

    Coloque a senha entre aspas simples. O `bash` e o `zsh` tratam caracteres como `!`, `$` e `*` de forma especial, e uma senha sem aspas contendo esses caracteres não será passada como digitada.

!!! tip "Boa prática"

    Use uma senha forte com mistura de maiúsculas, minúsculas, números e caracteres especiais.

### Passo 6: Iniciar o Servidor digna

No diretório de instalação do digna, inicie o servidor com:

```bash
./digna serve --address <host> --port <port>
```

**Parâmetros:**
- `--address` — Hostname/IP do servidor
- `--port` — Porta do servidor

Você deverá ver mensagens de inicialização confirmando que o servidor está em execução:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Dica"

    Se o dashboard for servido a partir de uma máquina diferente da do backend, abra também a porta da API no firewall:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "O servidor ocupa o terminal"

    `serve` roda em primeiro plano e continua até você pará-lo com ++ctrl+c++. Deixe-o rodando enquanto termina a configuração; para iniciá-lo automaticamente na inicialização do sistema, consulte [Executando o digna como um Serviço systemd](#running-digna-as-a-systemd-service).

---

## Configuração do Dashboard {: #dashboard-configuration }

### Passo 1: Fazer o Deploy do Dashboard no Servidor Web

O dashboard do digna lê sua própria configuração do arquivo `dashboard/dashboard_config.toml`. Esse arquivo não acompanha a instalação — você o cria no diretório `dashboard/`, junto com os arquivos do dashboard.

O conteúdo dele está descrito em [Single Sign-On](../../../sso/overview.md), que é também onde o arquivo é necessário: ele contém as opções de login que o dashboard oferece e, em implantações com múltiplas instâncias, a conexão com o backend.

Escolha seu servidor web e siga as etapas de implantação correspondentes.

#### Implantando no nginx

Se você seguiu a seção de [Configuração do nginx](#nginx-setup), o server block já aponta para sua pasta `dashboard` e nenhuma cópia é necessária.

1. **Confirme o caminho**
   - Abra `/etc/nginx/conf.d/digna.conf`
   - Verifique se `root` aponta para a sua pasta `dashboard` extraída

2. **Garanta que a pasta seja legível**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Recarregue o nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Teste a Instalação**
   - Abra seu navegador
   - Navegue para `http://localhost` (ou sua URL configurada)
   - Você deverá ver a página de login do digna dashboard

#### Implantando no Apache httpd

1. **Copie o Dashboard para o Document Root**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Adicione as Regras de Rewrite**

   Crie um arquivo `.htaccess` dentro da pasta implantada para que as rotas do dashboard sobrevivam a um refresh do navegador:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
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
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Acesse o Dashboard**
   - Abra seu navegador
   - Navegue para `http://localhost/digna`
   - Você deverá ver a página de login do digna dashboard

### Passo 2: SELinux (Apenas Família RHEL)

No RHEL, Rocky, AlmaLinux e Fedora, o SELinux fica no modo enforcing por padrão e impede que o servidor web leia arquivos fora dos locais esperados. Verifique se ele está ativo:

```bash
getenforce
```

Se o resultado for `Enforcing` e você estiver servindo o dashboard a partir de `/opt/digna/dashboard`, rotule o diretório para que o servidor web possa lê-lo:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Observação"

    Se o `semanage` não for encontrado, instale-o com `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Importante"

    Um dashboard que retorna **403 Forbidden** em um servidor RHEL recém-configurado quase sempre indica um problema de rotulagem do SELinux, e não de permissões de arquivo. Confirme com `sudo ausearch -m avc -ts recent`.

---

## Executando o digna como um Serviço systemd {: #running-digna-as-a-systemd-service }

### Por que Executar o digna como um Serviço?

Executar o backend do digna como um serviço systemd garante que ele:

- Inicie automaticamente quando a máquina for ligada
- Execute em segundo plano sem uma janela de terminal aberta
- Reinicie automaticamente se travar
- Possa ser gerenciado através do `systemctl`, o gerenciador de serviços padrão do Linux

### Arquivos de Gerenciamento do Serviço

Todos os arquivos necessários estão localizados no diretório de instalação do digna em: `bin/`

Os seguintes scripts shell estão disponíveis:

- `install_service.sh` — Registra o digna no systemd
- `uninstall_service.sh` — Remove o registro do serviço
- `start_service.sh` — Inicia o serviço registrado
- `stop_service.sh` — Para o serviço em execução

!!! warning "Privilégios de root necessários"

    Todos os scripts devem ser executados com `sudo`, pois registrar um serviço que inicia com o sistema grava um arquivo de unidade em `/etc/systemd/system`.

### Tornando os Scripts Executáveis

A extração pode não preservar o bit executável. Antes do primeiro uso:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Instalando o Serviço

1. **Abra um terminal**

2. **Navegue até a pasta bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Execute o script de instalação**
   ```bash
   sudo ./install_service.sh
   ```

O servidor digna agora está registrado no systemd com inicialização **automática** habilitada. O serviço não inicia imediatamente — veja a seção a seguir para iniciá-lo.

### Iniciando e Parando o Serviço

#### Para Iniciar o Serviço

1. Abra um terminal
2. Navegue para `/opt/digna/bin`
3. Execute:
   ```bash
   sudo ./start_service.sh
   ```

#### Para Parar o Serviço

1. Abra um terminal
2. Navegue para `/opt/digna/bin`
3. Execute:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Dica"

    Sempre pare o serviço antes de atualizar arquivos da aplicação.

### Gerenciando o Serviço com systemctl

Depois de registrado, o serviço também pode ser controlado com os comandos padrão do systemd, a partir de qualquer diretório:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Verificando o Serviço

Para confirmar que o serviço está registrado e em execução:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` significa que o serviço inicia com o sistema; `active` significa que ele está em execução agora.

### Visualizando os Logs do Serviço

O systemd captura tudo o que o backend escreve no console. Para ler:

```bash
sudo journalctl -u digna -n 100
```

Para acompanhar o log ao vivo enquanto reproduz um problema:

```bash
sudo journalctl -u digna -f
```

!!! tip "Dica"

    Esta é a forma mais rápida de diagnosticar um serviço que inicia e para imediatamente. Uma falha de conexão com o repositório ou a ausência do `license.toml` é informada aqui.

### Movendo o Serviço para um Novo Diretório

O arquivo de unidade armazena o caminho absoluto do executável, portanto mover a instalação exige registrar o serviço novamente:

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

O servidor digna agora está desregistrado do systemd.

---

## Atualizando para uma Nova Release {: #upgrading-to-a-new-release }

### Antes de Atualizar

**Verifique Primeiro Todas as Conexões de Banco de Dados**

A partir da Release 2026.06, o digna acessa cada tecnologia de origem por **ODBC**. As versões
anteriores ofereciam a escolha entre um driver próprio por tecnologia e ODBC, selecionada pelo
botão **Use ODBC**. A equipe do digna decidiu se apoiar apenas em ODBC, porque uma interface única
e padronizada oferece mais do que um conjunto de drivers sob medida:

- **Autenticação** — a autenticação faz parte do ODBC, então uma conexão pode usar tudo o que o
  seu driver suportar: senhas, tokens e PATs, Kerberos e Active Directory, MFA e logon único pelo
  navegador, identidades na nuvem, certificados de cliente e TLS. Novos métodos chegam com uma
  atualização do driver, em vez de esperar por uma versão do digna.
- **Drivers mantidos pelos fabricantes dos bancos de dados** — o driver do próprio fabricante
  acompanha as novas versões do servidor e as correções de segurança, e você pode atualizá-lo no
  seu próprio ritmo, independentemente do digna.
- **Uma única forma de configurar tudo** — cada tecnologia é uma lista de propriedades
  chave/valor, com a mesma interface, a mesma criptografia de valores sensíveis e a mesma solução
  de problemas, em vez de um conjunto de campos diferente por origem.
- **Ajuste e alcance** — opções do driver como tempos limite, configurações de TLS, proxies e
  tamanhos de leitura estão disponíveis para todas as origens, e qualquer tecnologia com um driver
  ODBC compatível pode ser conectada, inclusive aquelas para as quais o digna não publica um guia
  dedicado.

Na prática, isso significa que o botão **Use ODBC** e os campos separados de host, porta, banco de
dados, usuário e senha não existem mais. **Toda conexão que ainda não usa ODBC precisa ser
convertida para ODBC** — não há conversão automática, portanto planeje isso antes de atualizar:

1. Revise cada conexão de banco de dados definida na sua instalação e anote as que ainda não usam
   ODBC — cada uma precisará ser reconfigurada.
2. Instale o driver ODBC correspondente no host do digna — as conexões são abertas pelo servidor
   que executa o backend do digna, não pelo navegador. Consulte
   [Instalar o Driver ODBC no Host do digna](../../../databases/overview.md#install-the-driver).
3. Tenha as propriedades ODBC prontas para cada conexão afetada. Os
   [guias por tecnologia](../../../databases/overview.md#technology-guides) trazem, para cada
   origem, um conjunto de propriedades comprovado.

Após a atualização, converta cada conexão afetada para ODBC e teste-a pelo dashboard —
consulte [Criar uma Conexão de Banco de Dados](../../../databases/overview.md#create-a-database-connection)
e [Testar uma Conexão](../../../databases/overview.md#testing-a-connection).

!!! warning "Conexões Databricks Legacy"

    O conector Databricks Legacy foi removido nesta release. Migre essas conexões
    para o conector [Databricks](../../../databases/databricks_connector_guide.md).

**É Obrigatório Criar um Backup do Repositório do digna**

Antes de atualizar o digna, faça backup do seu repositório (PostgreSQL) para proteger contra perda de dados.
Um backup garante que você possa recuperar caso a atualização encontre problemas inesperados.

Para criar um backup a partir do shell:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Processo de Atualização

#### Passo 1: Parar o Serviço digna

Se o digna estiver em execução como serviço systemd, pare-o primeiro:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Se o digna estiver em execução em primeiro plano, pressione `Ctrl + C` na janela do terminal onde ele está rodando.

#### Passo 2: Fazer Backup da Instalação Atual

No diretório de instalação do digna, renomeie as pastas da instalação atual para que a nova release possa ser implantada ao lado delas:

```bash
cd /opt/digna
sudo mv dignabackend dignabackend_old
```
```bash
sudo mv dignacli dignacli_old
```
```bash
sudo mv dashboard dashboard_old
```

!!! info "dignabackend e dignacli não são mais usados"

    A partir da Release 2026.06, `dignabackend` e `dignacli` são substituídos pelo executável único `digna`, que reúne o backend e a CLI. Mantenha `dignabackend_old` e `dignacli_old` apenas até verificar a atualização — depois você pode excluir as duas pastas. Mantenha `dashboard_old` até restaurar dele os seus arquivos de configuração (veja o passo 4).

#### Passo 3: Extrair e Implantar a Nova Versão

1. Extraia o novo arquivo ZIP de instalação do digna
2. Copie o novo executável `digna` e a pasta `dashboard` para seu diretório de instalação
3. Restaure o bit de execução e a propriedade da conta de serviço:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Importante"

    Nem o `config.toml` nem o `dashboard/dashboard_config.toml` são incluídos no ZIP de
    instalação — a equipe do digna nunca distribui nenhum dos dois arquivos. Por isso, sua
    configuração existente não é afetada pela atualização, e as cópias nas pastas renomeadas
    `*_old` são as únicas que você tem.

#### Passo 4: Restaurar Seus Arquivos de Configuração

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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

    A release 2026.06 substitui a matriz de tabelas por uma tabela por provedor, nomeada a partir
    da chave do provedor. `DIGNA_OIDC_KEY` deixa de existir — a chave agora faz parte do cabeçalho
    da seção.

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

    Repita a seção para cada provedor e mantenha cada chave igual ao `key` definido em
    `dashboard_config.toml`. O `digna config check` informa `oidc_clients` como FAILED enquanto a
    forma antiga permanecer. Apenas as instalações que usam logon único são afetadas.

#### Passo 5: Recarregar o Servidor Web

O dashboard é um conjunto de arquivos estáticos, então seu servidor web — e o navegador — podem
ainda estar servindo a versão anterior. Recarregue ou reinicie o servidor web que hospeda a pasta
`dashboard` e, em seguida, recarregue a página com uma atualização forçada (++ctrl+f5++).

#### Passo 6: Validar a Configuração

Confirme que o `config.toml` atualizado está completo antes de mexer no repositório:

```bash
./digna config check
```

Todas as seções devem informar OK. Corrija tudo o que for informado como FAILED e execute o comando novamente antes de continuar.

#### Passo 7: Substituir o Arquivo de Licença

Cada release é licenciada separadamente. Copie o `license.toml` que a equipe do digna forneceu
para esta release para o diretório de instalação, substituindo o antigo:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Não mantenha a licença anterior"

    Um `license.toml` emitido para uma release anterior não cobre esta, e todo comando que
    verifica a licença — `user`, `inspection`, `repo` — é interrompido antes de mexer no
    repositório quando a verificação falha. Verifique-a antes de prosseguir:

    ```bash
    ./digna license check
    ```

#### Passo 8: Atualizar o Schema do Repositório

Navegue até o diretório de instalação do digna e execute:

```bash
cd /opt/digna
./digna repo upgrade
```

Isto atualiza o schema do PostgreSQL para a versão mais recente preservando todos os dados existentes.

#### Passo 9: Reiniciar Serviços

Se estiver rodando como serviço systemd:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Se estiver executando manualmente, reinicie o servidor:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Se estiver usando nginx ou Apache, recarregue o respectivo servidor web:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

Na família RHEL, reaplique a rotulagem do SELinux se o diretório `dashboard` tiver sido substituído:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Passo 10: Verificar a Atualização

1. Acesse o digna dashboard
2. Verifique se a interface carrega corretamente
3. Cheque os logs do servidor em busca de erros
4. Converta para ODBC todas as conexões que ainda não o usavam e depois teste todas as conexões
   — consulte [Testar uma Conexão](../../../databases/overview.md#testing-a-connection):

```bash
sudo journalctl -u digna -n 100
```