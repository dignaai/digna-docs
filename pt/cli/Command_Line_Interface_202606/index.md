# Referência da CLI digna 2026.06
**2026-09-05**

Esta página documenta o conjunto completo de comandos disponíveis na versão **2026.06** da CLI do ***digna***, incluindo exemplos de uso e opções.

O executável se chama `digna`.

---

## Noções Básicas da CLI

---

### Visão Geral e Sintaxe

A CLI da versão **2026.06** usa uma hierarquia de comandos estruturada e baseada em categorias:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` e `serve` são comandos únicos, sem subcomando:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Opções Globais

As opções globais a seguir se aplicam a todos os comandos:

- `--help`, `-h`: Exibe informações de ajuda sobre a CLI ou sobre uma categoria de comandos ou subcomando específico.
- `--stacktrace`: Em caso de falha, exibe a cadeia completa de erros em vez de apenas a mensagem de nível mais alto.

`--stacktrace` é uma opção global no sentido estrito: ela precisa ser informada **antes** da categoria de comando, e não depois dela.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

Não existe um flag `--version`. Em vez disso, use o comando [`version`](#version).

### Pré-requisitos

A maioria dos comandos precisa de um `config.toml` legível e válido; alguns exigem, além disso, uma licença válida.
A tabela a seguir registra o que cada categoria de comandos carrega antes de fazer qualquer coisa:

| Categoria de comandos | Precisa de `config.toml` | Precisa de licença válida |
|---|---|---|
| `version` | não | não |
| `config check` | não (é justamente sobre isso que o comando informa) | não |
| `license check` | não | ela *é* a verificação |
| `crypt` | sim | não |
| `serve` | sim | não |
| `project` | sim | não |
| `user` | sim | sim |
| `inspection` | sim | sim |
| `repo` | sim | sim |

Onde uma licença é exigida, tanto sua assinatura quanto sua data de expiração são verificadas, e o comando é abortado antes de tocar no repositório se qualquer uma das duas falhar.

### Códigos de Saída

- `0`: o comando foi bem-sucedido.
- `1`: o comando falhou. A mensagem de erro é gravada em stderr, prefixada com `Error: `.

### help

A opção `--help` fornece informações sobre as categorias de comandos, os subcomandos e as opções disponíveis:

1. **Exibindo a ajuda geral:**
   ```bash
   digna --help
   ```

2. **Obtendo ajuda para categorias e comandos específicos:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **A saída inclui:**
   - **Descrição do Comando:** Resumo da finalidade do comando.
   - **Sintaxe:** Argumentos obrigatórios e opcionais.
   - **Opções:** Flags e parâmetros específicos do comando.

### version

O comando `version` imprime a versão instalada do ***digna***. Ele não lê nenhuma configuração e não valida nenhuma licença, portanto também funciona em uma instalação cujo `config.toml` ou cuja licença esteja ausente ou inválida.

A versão da release é independente da versão do schema do repositório informada por [`repo check`](#repo-check).

#### Uso do Comando
```bash
digna version
```

#### Exemplo de Saída
```text
2026.06
```

---

## Gerenciamento de Configuração

---

### config check

O comando `config check` valida o arquivo de configuração (`config.toml`), verificando se todas as seções e configurações obrigatórias estão presentes e formatadas corretamente. Cada seção é validada isoladamente, de modo que uma seção `[app]` quebrada não oculte o estado de `[repo]`.

As seções informadas são:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — opcional; uma chave ausente passa na verificação, uma lista presente porém malformada falha

O comando deliberadamente não carrega a configuração da aplicação da mesma forma que os outros comandos, para que possa diagnosticar um `config.toml` que impediria completamente o ***digna*** de iniciar.

#### Uso do Comando
```bash
digna config check [OPTIONS]
```

#### Opções
- `--configpath`, `-c`: Caminho para o arquivo de configuração ou para um diretório que contenha `config.toml` (o padrão é `./config.toml`).
- `--json`: Emite o relatório de validação em JSON. Tem precedência sobre `--quiet`.
- `--quiet`, `-q`: Suprime o relatório e se baseia exclusivamente no código de saída.

#### Exemplo
```bash
digna config check
```

Validar um arquivo de configuração específico e formatar a saída como JSON:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Exemplo de Saída
```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: FAILED
    missing field `aes_gcm_key`
 - OIDC config(s): OK

Overall: FAILED
```

Um arquivo ausente ou um erro de sintaxe TOML não deixa nada a ser validado seção por seção e é relatado como um único erro em vez de um relatório, independentemente de `--quiet` ou `--json`.

---

## Gerenciamento de Repositório

---

### repo check

O comando `repo check` testa a conexão com o banco de dados e verifica a instalação e a versão do repositório. Ele falha se o schema configurado não existir, ou se existir mas não contiver um repositório do ***digna***.

A versão informada é a versão do schema do repositório, que é versionado separadamente da release do ***digna*** impressa por [`version`](#version).

#### Uso do Comando
```bash
digna repo check
```

#### Exemplo de Saída
```text
Repo version 3.0.0 installed
```

### repo install

O comando `repo install` instala um novo repositório do ***digna*** no schema configurado em `config.toml`, criando todas as sequences, tabelas, índices, constraints e registros iniciais necessários.

O schema em si **não** é criado por este comando — ele precisa existir previamente. O comando também se recusa a executar se já houver um repositório instalado nesse schema, e aponta para [`repo upgrade`](#repo-upgrade) se a versão instalada for mais antiga.

#### Uso do Comando
```bash
digna repo install
```

#### Exemplo de Saída
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

O comando `repo upgrade` aplica migrações do schema do banco de dados para levar um repositório existente até a versão esperada pela release instalada. As atualizações são aplicadas um salto de versão por vez, ao longo de um caminho de upgrade fixo, e cada salto concluído é registrado no repositório.

Se o repositório já estiver na versão esperada, o comando informa que nenhuma atualização é necessária e não faz alteração alguma.

#### Uso do Comando
```bash
digna repo upgrade
```

#### Exemplo de Saída
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Gerenciamento de Criptografia

---

### crypt gen-key

O comando `crypt gen-key` gera uma nova chave de criptografia AES-GCM, para uso como chave de criptografia em `config.toml`. Um `config.toml` carregável já precisa estar presente, ainda que a chave gerada não dependa dele.

#### Uso do Comando
```bash
digna crypt gen-key
```

#### Exemplo de Saída
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

O comando `crypt encrypt` criptografa uma string (como a senha de um banco de dados) usando a chave AES-GCM configurada em `config.toml` e imprime o texto cifrado.

#### Uso do Comando
```bash
digna crypt encrypt <VALUE>
```

#### Argumentos
- **VALUE**: A string em texto simples a ser criptografada (obrigatório).

#### Exemplo
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

O comando `crypt decrypt` descriptografa uma string criptografada com AES-GCM usando a chave configurada em `config.toml` e imprime o texto simples.

#### Uso do Comando
```bash
digna crypt decrypt <VALUE>
```

#### Argumentos
- **VALUE**: A string cifrada a ser descriptografada (obrigatório).

#### Exemplo
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Gerenciamento de Usuários

---

### user add

O comando `user add` cria uma nova conta de usuário no repositório do ***digna***. O comando falha se já existir um usuário com o endereço de e-mail informado.

#### Uso do Comando
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argumentos
- **EMAIL**: O endereço de e-mail do usuário (obrigatório).
- **PASSWORD**: A senha inicial do usuário (obrigatório).
- **DISPLAY_NAME**: O nome de exibição completo do usuário (obrigatório).

#### Opções
- `--admin`, `-a`: Cria o usuário com privilégios de administrador (superusuário).

#### Exemplo
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Para criar uma conta de administrador:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Exemplo de Saída
```text
User created with ID: 42
```

### user list

O comando `user list` lista todos os usuários registrados em formato tabular, com ID, e-mail, nome de exibição e indicador de administrador.

#### Uso do Comando
```bash
digna user list
```

#### Exemplo de Saída
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

O comando `user modify` atualiza o nome de exibição e os privilégios de administrador de uma conta de usuário existente, identificada pelo endereço de e-mail.

Tanto o nome de exibição quanto o indicador de administrador são sempre gravados. `--admin` é um interruptor, não um valor: **omiti-lo revoga os privilégios de administrador**, portanto informe-o sempre que o usuário deva mantê-los ou obtê-los.

#### Uso do Comando
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argumentos
- **EMAIL**: O e-mail do usuário a ser modificado (obrigatório).
- **DISPLAY_NAME**: O nome de exibição atualizado (obrigatório).

#### Opções
- `--admin`, `-a`: Concede privilégios de administrador. Omita para revogá-los.
- `--valid-until`, `-v`: Aceito por compatibilidade, mas **atualmente não aplicado**. Informá-lo exibe um aviso e não altera nada.

#### Exemplo
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Exemplo de Saída
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

O comando `user modify-pwd` atualiza a senha de uma conta de usuário existente.

#### Uso do Comando
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argumentos
- **EMAIL**: O e-mail do usuário cuja senha deve ser atualizada (obrigatório).
- **PASSWORD**: A nova senha (obrigatório).

#### Exemplo
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

O comando `user delete` remove uma conta de usuário do sistema.

#### Uso do Comando
```bash
digna user delete <EMAIL>
```

#### Argumentos
- **EMAIL**: O e-mail do usuário a ser excluído (obrigatório).

#### Exemplo
```bash
digna user delete jdoe@example.com
```

---

## Gerenciamento de Projetos e Fontes de Dados

---

### project list

O comando `project list` lista todos os projetos disponíveis no repositório, mostrando seu ID, nome e descrição.

#### Uso do Comando
```bash
digna project list
```

#### Exemplo de Saída
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

O comando `project list-ds` lista todas as fontes de dados associadas a um determinado projeto, exibindo seu ID, nome, tipo, schema e nome da tabela.

#### Uso do Comando
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argumentos
- **PROJECT_NAME**: O nome do projeto cujas fontes de dados devem ser listadas (obrigatório). O nome precisa corresponder exatamente.

#### Exemplo
```bash
digna project list-ds ProjectA
```

#### Exemplo de Saída
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

O comando `project export-ds` exporta as fontes de dados de um projeto para um documento JSON.

Se nem `--table-name` nem `--table-id` forem informados, todas as fontes de dados do projeto são exportadas.

#### Uso do Comando
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argumentos
- **PROJECT_NAME**: O nome do projeto do qual exportar as fontes de dados (obrigatório).

#### Opções
- `--table-name`, `-n`: Nomes das fontes de dados a exportar. Vários nomes podem ser informados, separados por espaços.
- `--table-id`, `-i`: IDs das fontes de dados a exportar. Vários IDs podem ser informados, separados por espaços.
- `--exportfile`, `-f`: Caminho no qual salvar as fontes de dados exportadas (padrão: `data_sources_export.json`).

#### Exemplo
Para exportar todas as fontes de dados de `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Para exportar tabelas específicas:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Exemplo de Saída
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

O comando `project import-ds` importa fontes de dados de um arquivo de exportação para um projeto de destino e informa, objeto a objeto, o que foi criado, atualizado ou ignorado.

#### Uso do Comando
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumentos
- **PROJECT_NAME**: Nome do projeto de destino para o qual importar (obrigatório).
- **EXPORT_FILE**: Caminho para o arquivo JSON de exportação (obrigatório).

#### Opções
- `--output-file`, `-o`: Arquivo no qual gravar o relatório de importação. Sem ele, o relatório vai para stdout.
- `--output-format`, `-f`: Formato do relatório de importação — `table`, `json` ou `csv` (padrão: `table`).

#### Exemplo
```bash
digna project import-ds ProjectB my_export.json
```

Para obter um relatório legível por máquina:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

O relatório abrange quatro níveis de objeto — fonte de dados, definição do conjunto de dados, atributo e regra de validação — cada um com sua ação de importação, o resultado, o ID do objeto resultante e eventuais informações adicionais.

### project plan-import-ds

O comando `project plan-import-ds` prevê uma importação de fontes de dados para um projeto de destino, mostrando quais objetos seriam criados, atualizados ou ignorados, sem alterar nada. Ele recebe o mesmo arquivo de exportação e as mesmas opções de relatório que [`project import-ds`](#project-import-ds), e acrescenta um número de etapa por objeto planejado.

#### Uso do Comando
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumentos
- **PROJECT_NAME**: Nome do projeto de destino (obrigatório).
- **EXPORT_FILE**: Caminho para o arquivo de exportação (obrigatório).

#### Opções
- `--output-file`, `-o`: Arquivo no qual gravar o plano de importação. Sem ele, o plano vai para stdout.
- `--output-format`, `-f`: Formato do plano de importação — `table`, `json` ou `csv` (padrão: `table`).

#### Exemplo
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Gerenciamento de Inspeções

---

### inspection run

O comando `inspection run` cria uma solicitação de inspeção para um projeto e um intervalo de datas e então — dependendo das opções informadas — espera por ela, retorna imediatamente ou a executa no próprio processo.

Os três modos de execução são:

- **Padrão (sem flag)**: a solicitação é enfileirada para o backend, e a CLI a consulta a cada dois segundos, imprimindo o progresso das tarefas até que a inspeção alcance um estado final. É necessário um `digna serve` em execução; caso contrário, nada retira a solicitação da fila.
- **`--async-mode`**: a solicitação é enfileirada e seu ID é impresso imediatamente. Use [`inspection status`](#inspection-status) para acompanhá-la.
- **`--bypass-backend`**: a inspeção é executada pelo próprio processo da CLI e não é enfileirada, portanto nenhum servidor em execução é necessário.

`--async-mode` e `--bypass-backend` são mutuamente exclusivos.

Em todos os modos, o comando termina com um código de saída diferente de zero se a inspeção não tiver sido concluída com sucesso.

#### Uso do Comando
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argumentos
- **PROJECT_NAME**: O nome do projeto de destino (obrigatório). O nome precisa corresponder exatamente.
- **START_DATE**: Data inicial do intervalo de datas no formato `YYYY-MM-DD` (obrigatório).
- **END_DATE**: Data final do intervalo de datas no formato `YYYY-MM-DD` (obrigatório).

#### Opções
- `--table-name`: Restringe a inspeção a uma única fonte de dados do projeto, informada pelo nome da fonte de dados. Sem essa opção, todas as fontes de dados do projeto são inspecionadas.
- `--async-mode`: Enfileira a inspeção e imprime o ID da solicitação em vez de esperar por ela. Não pode ser combinada com `--bypass-backend`.
- `--bypass-backend`: Executa a inspeção diretamente no processo da CLI em vez de enfileirá-la para o backend. Não pode ser combinada com `--async-mode`.

#### Exemplo
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Para enviar uma inspeção assíncrona:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Para inspecionar uma única fonte de dados:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Exemplo de Saída
Modo padrão:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Modo assíncrono:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

O comando `inspection status` consulta o estado e o progresso das tarefas de uma solicitação de inspeção pelo ID da solicitação.

#### Uso do Comando
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argumentos
- **INSPECTION_REQUEST_ID**: O ID numérico da solicitação de inspeção (obrigatório).

#### Exemplo
```bash
digna inspection status 1024
```

#### Exemplo de Saída
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

O comando `inspection abort` solicita o cancelamento de solicitações de inspeção em execução ou pendentes. Ele registra um evento de parada para cada solicitação afetada; quem age sobre ele é o backend, portanto um aborto é um pedido de parada, e não um encerramento imediato.

#### Uso do Comando
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argumentos
- **INSPECTION_REQUEST_ID**: O ID da solicitação de inspeção a abortar. Obrigatório, a menos que `--killall` seja informado.

#### Opções
- `--killall`: Aborta todas as solicitações de inspeção em execução e pendentes. Tem precedência sobre um ID de solicitação informado junto com ela.

#### Exemplo
Para abortar uma solicitação específica:
```bash
digna inspection abort 1024
```

Para abortar todas as inspeções ativas e enfileiradas:
```bash
digna inspection abort --killall
```

#### Exemplo de Saída
`--killall` informa o que fez; abortar uma única solicitação não produz saída e sinaliza o sucesso por meio do código de saída.
```text
All running and pending inspections have been aborted.
```

---

## Gerenciamento de Licenças

---

### license check

O comando `license check` valida o `license.toml`, verificando sua assinatura contra a chave pública distribuída com a instalação e conferindo que ele não expirou. Ele não lê nenhuma configuração da aplicação, portanto também funciona antes que o `config.toml` esteja configurado.

#### Uso do Comando
```bash
digna license check
```

#### Exemplo de Saída
```text
License is valid
```

Uma assinatura inválida e uma licença expirada são relatadas como erros distintos, ambos com código de saída 1.

---

## Servidor e Serviços em Segundo Plano

---

### serve

O comando `serve` inicia o servidor da API REST do ***digna*** junto com o agendador de inspeções e o gerenciador de inspeções em segundo plano. Na inicialização, ele também marca como falha qualquer inspeção que o repositório ainda registre como em execução, já que nada pode ter sobrevivido de um processo anterior.

O comando é executado em primeiro plano até ser interrompido.

#### Uso do Comando
```bash
digna serve [OPTIONS]
```

#### Opções
- `--address`: Endereço de rede ao qual associar o servidor da API (padrão: `127.0.0.1`).
- `--port`: Número da porta na qual escutar (padrão: `8000`).

#### Exemplo
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Exemplo de Saída
```text
Server running on http://0.0.0.0:8000
```