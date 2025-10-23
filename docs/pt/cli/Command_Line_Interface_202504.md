---
title: Referência da CLI digna 2025.04 – Comandos & Exemplos | Documentação digna
description: Referência completa da CLI digna versão 2025.04. Aprenda a gerenciar usuários, repositórios e dados com comandos como add-user, check-repo-connection, upgrade-repo, inspect e outros.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202504/
image: /assets/logo_square.png
---

# digna CLI Reference 2025.04
**2025-04-01**

Esta página documenta o conjunto completo de comandos disponíveis na CLI ***digna***, release **2025.04**, incluindo exemplos de uso e opções.

---

## CLI Basics

---

## Using `help` Option

A opção `--help` fornece informações sobre os comandos disponíveis e seu uso. Existem duas formas principais de utilizar esta opção:

1. **Exibir Ajuda Geral:**
   
    Use --help imediatamente após a palavra-chave ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Obter Ajuda para Comandos Específicos:**  
  
    Para informações detalhadas sobre um comando específico, acrescente `--help` a esse comando.
    Por exemplo, para obter ajuda sobre o comando `add-user`, execute:
     ```bash
     dignacli add-user --help
     ```

     ### saída:
      
     - **Descrição do Comando:** Oferece uma descrição detalhada do que o comando faz.  
     - **Sintaxe:** Mostra a sintaxe exata, incluindo argumentos obrigatórios e opcionais.  
     - **Opções:** Lista quaisquer opções específicas do comando, juntamente com suas explicações.  
     - **Exemplos:** Fornece exemplos de como executar o comando de forma eficaz.

  
## Using `check-repo-connection` Command

O comando check-repo-connection é uma utilidade dentro da CLI ***digna*** projetada para testar a conectividade e o acesso a um repositório ***digna*** especificado. Este comando garante que a CLI consegue interagir com o repositório.
      
#### Command Usage
```bash
dignacli check-repo-connection
```

Após a execução bem-sucedida, o comando apresenta uma confirmação da conexão, juntamente com detalhes sobre o repositório: versão do repositório, Host, Database e Schema.  
  
Se a conexão com o repositório não for bem-sucedida, verifique o arquivo config.toml para garantir que as configurações estejam corretas.

## Using ‘version’ command

Para verificar a versão instalada do *dignacli*, use a opção --version.  
  
#### Command Usage
```bash
dignacli --version
```
  
#### Example Output
```bash
dignacli version 2025.04
```

## Using logging options
  
Por padrão, a saída no console dos comandos da ***digna*** é projetada para ser minimalista. A maioria dos comandos oferece a possibilidade de fornecer informações adicionais, usando as seguintes opções:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” e “debug” definem o nível de detalhe, enquanto a opção “logfile” permite redirecionar a saída para ser gravada em um arquivo em vez de exibida na janela do console.

## User Management

### Using ‘add-user’ command
  
O comando add-user na CLI ***digna*** é usado para adicionar um novo usuário ao sistema ***digna***.
  
#### Command Usage
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Arguments

- **USER_NAME**: O nome de usuário para o novo usuário (obrigatório).
- **USER_FULL_NAME**: O nome completo do novo usuário (obrigatório).
- **USER_PASSWORD**: A senha do novo usuário (obrigatório).

#### Options

- `--is_superuser`, `-su`: Flag para designar o novo usuário como administrador.
- `--valid_until`, `-vu`: Define uma data de expiração para a conta do usuário no formato `YYYY-MM-DD HH:MI:SS`. Se não definida, a conta não terá data de expiração.

#### Example

Para adicionar um novo usuário com nome de usuário `jdoe`, nome completo `John Doe` e senha `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Para adicionar um novo usuário e definir uma data de expiração da conta:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Using `delete-user` command
  
O comando `delete-user` na CLI ***digna*** é usado para remover um usuário existente do sistema ***digna***.
  
#### Command Usage
```bash
dignacli delete-user USER_NAME
```
  
##### Arguments
- **USER_NAME**: O nome de usuário do usuário a ser deletado (obrigatório). Este é o único argumento exigido pelo comando.

#### Example
```bash
dignacli delete-user jdoe
```
  
A execução deste comando removerá o usuário `jdoe` do sistema ***digna***, revogando seu acesso e excluindo seus dados e permissões associados do repositório.

### Using `modify-user` Command

O comando `modify-user` na CLI ***digna*** é usado para atualizar os detalhes de um usuário existente no sistema ***digna***.

#### Command Usage
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Arguments
  
- **USER_NAME**: O nome de usuário do usuário a ser modificado (obrigatório).
- **USER_FULL_NAME**: O novo nome completo para o usuário (obrigatório).
  
#### Options  
  
- `--is_superuser`, `-su`: Define o usuário como superusuário, concedendo privilégios elevados. Esta flag não requer valor.  
- `--valid_until`, `-vu`: Define uma data de expiração para a conta do usuário no formato YYYY-MM-DD HH:MI:SS. Se não fornecida, a conta permanece válida indefinidamente.  
  
#### Example
  
Para modificar o nome completo do usuário `jdoe` para “Johnathan Doe” e tornar o usuário superusuário:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Using `modify-user-pwd` Command
  
O comando `modify-user-pwd` na CLI ***digna*** é usado para alterar a senha de um usuário existente no sistema ***digna***.
  
#### Command Usage
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Arguments
  
- **USER_NAME**: O nome de usuário do usuário cuja senha será alterada (obrigatório).
- **USER_PWD**: A nova senha do usuário (obrigatório).
  
#### Example
  
Para alterar a senha do usuário `jdoe` para `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Using `list-users` Command

O comando `list-users` na CLI ***digna*** exibe uma lista de todos os usuários registrados no sistema ***digna***.

#### Command Usage

```bash
dignacli list-users
```

A execução deste comando na CLI ***digna*** irá conectar-se ao repositório ***digna*** e listar todos os usuários, mostrando seu ID, nome de usuário, nome completo, status de superusuário e timestamps de expiração.

## Repository Management

### Using `upgrade-repo` Command
  
O comando `upgrade-repo` na CLI ***digna*** é usado para atualizar ou inicializar o repositório ***digna***. Este comando é essencial para aplicar atualizações ou configurar a infraestrutura do repositório pela primeira vez.
  
#### Command Usage

```bash
dignacli upgrade-repo [options]
```
  
#### Options
  
- `--simulation-mode`, `-s`: Quando habilitado, esta opção executa o comando em modo de simulação, que imprime as instruções SQL que seriam executadas, mas não as aplica de fato. Isso é útil para visualizar as alterações sem modificar o repositório.  

  
#### Example
  
Para atualizar o repositório ***digna***, você pode executar o comando sem opções:
  
```bash
dignacli upgrade-repo
```  
Para executar a atualização em modo de simulação (para ver as instruções SQL sem aplicá-las):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Este comando é crucial para manter o sistema ***digna***, garantindo que o schema do banco de dados e outros componentes do repositório estejam atualizados com a versão mais recente do software.

### Using `encrypt` Command
  
O comando `encrypt` na CLI ***digna*** é usado para criptografar uma senha.
  
#### Command Usage
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Arguments
- **PASSWORD**: A senha que precisa ser criptografada (obrigatório).
  
#### Example
  
Para criptografar uma senha, você precisa fornecer a senha como argumento.   
Por exemplo, para criptografar a senha `mypassword123`, você usaria:
```bash
dignacli encrypt mypassword123
```
Este comando retorna a versão criptografada da senha fornecida, que pode então ser usada em contextos seguros. Se o argumento da senha não for fornecido, a CLI exibirá um erro indicando o argumento ausente.

## Using `generate-key` Command
  
O comando `generate-key` é usado para gerar uma chave Fernet, essencial para proteger senhas armazenadas no repositório ***digna***.
  
#### Command Usage
```bash
dignacli generate-key
```
  
## Data Management

## Using `clean-up` Command

O comando `clean-up` na CLI ***digna*** é usado para remover perfis, previsões e dados do sistema de semáforo (Traffic Light System) para uma ou mais fontes de dados dentro de um projeto especificado. Este comando é essencial para o gerenciamento do ciclo de vida dos dados, ajudando a manter um ambiente de dados organizado e eficiente ao limpar dados desatualizados ou desnecessários.

#### Command Usage

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: O nome do projeto do qual os dados serão removidos (obrigatório). Usar a palavra-chave all-projects neste argumento instrui a ***digna*** a iterar sobre todos os projetos existentes e aplicar este comando.
- **FROM_DATE**: A data e hora de início para a remoção de dados. Formatos aceitáveis incluem %Y-%m-%d, %Y-%m-%dT%H:%M:%S, ou %Y-%m-%d %H:%M:%S (obrigatório).
- **TO_DATE**: A data e hora de término para a remoção de dados, seguindo os mesmos formatos de FROM_DATE (obrigatório).
  
#### Options
  
- `--table-name`, `-tn`: Limita a operação de limpeza a uma tabela específica dentro do projeto.
- `--table-filter`, `-tf`: Filtra para limitar a limpeza às tabelas que contenham a substring especificada em seus nomes.
- `--timing`, `-tm`: Exibe a duração do processo de limpeza após a conclusão.
- `--help`: Exibe informações de ajuda para o comando clean-up e encerra.
  
#### Example
  
Para remover dados do projeto ProjectA entre 1 de janeiro de 2023 e 30 de junho de 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Para remover dados somente de uma tabela específica chamada `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Este comando ajuda a gerenciar o armazenamento de dados e a garantir que o repositório contenha apenas informações relevantes.

## Using `list-projects` Command
  
O comando `list-projects` na CLI ***digna*** é usado para exibir uma lista de todos os projetos disponíveis no sistema ***digna***.
  
#### Command Usage
  
```bash
dignacli list-projects
```

Este comando é especialmente útil para administradores e usuários que gerenciam múltiplos projetos, fornecendo uma visão rápida dos projetos disponíveis no repositório ***digna***.

## Using `list-ds` Command

O comando `list-ds` na CLI ***digna*** é usado para exibir uma lista de todas as fontes de dados disponíveis dentro de um projeto especificado. Este comando é útil para entender os ativos de dados disponíveis para análise e gerenciamento no sistema ***digna***.

#### Command Usage
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Arguments
- **PROJECT_NAME**: O nome do projeto para o qual as fontes de dados estão sendo listadas (obrigatório).
  
#### Example
  
Para listar todas as fontes de dados no projeto chamado `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Este comando fornece aos usuários uma visão geral das fontes de dados disponíveis em um projeto, ajudando-os a navegar e gerenciar o panorama de dados de forma mais eficaz.


## Using `inspect` Command

O comando `inspect` na CLI ***digna*** é usado para criar perfis, previsões e dados do sistema de semáforo (Traffic Light System) para uma ou mais fontes de dados dentro de um projeto especificado. Este comando ajuda a analisar e monitorar os dados ao longo de um período definido.

#### Command Usage

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: O nome do projeto cujos dados serão inspecionados (obrigatório). Usar a palavra-chave all-projects neste argumento instrui a ***digna*** a iterar sobre todos os projetos existentes e aplicar este comando.
- **FROM_DATE**: A data e hora de início para a inspeção de dados. Formatos aceitáveis incluem %Y-%m-%d, %Y-%m-%dT%H:%M:%S, ou %Y-%m-%d %H:%M:%S (obrigatório).
- **TO_DATE**: A data e hora de término para a inspeção de dados, seguindo os mesmos formatos de FROM_DATE (obrigatório).
  
#### Options

- `--table-name`, `-tn`: Limita a inspeção a uma tabela específica dentro do projeto.
- `--table-filter`, `-tf`: Filtra para inspecionar apenas tabelas que contenham a substring especificada em seus nomes.
- `--do-profile`: Aciona a recolha/recoleta de perfis. O padrão é do-profile.
- `--no-do-profile`: Impede a recolha/recoleta de perfis.
- `--do-prediction`: Aciona o recálculo de previsões. O padrão é do-prediction.
- `--no-do-prediction`: Impede o recálculo de previsões.
- `--do-alert-status`: Aciona o recálculo dos status de alerta. O padrão é do-alert-status.
- `--no-do-alert-status`: Impede o recálculo dos status de alerta.
- `--iterative`: Aciona a inspeção do período usando iterações diárias. O padrão é iterative.
- `--no-iterative`: Aciona a inspeção de todo o período de uma só vez.
- `--enable_notification`, `-en`: Habilita o envio de notificações em caso de alertas.
- `--timing`, `-tm`: Exibe a duração do processo de inspeção após a conclusão.
  
#### Example
  
Para inspecionar dados do projeto `ProjectA` de 1 de janeiro de 2024 a 31 de janeiro de 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Para inspecionar apenas uma tabela específica e forçar o recálculo de previsões:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Este comando é útil para gerar perfis e previsões atualizadas, monitorar a integridade dos dados e gerenciar sistemas de alerta dentro de um intervalo de tempo especificado para o projeto.

## Using `tls-status` Command

O comando `tls-status` na CLI ***digna*** é usado para consultar o status do Traffic Light System (TLS) para uma tabela específica dentro de um projeto em uma data determinada. O Traffic Light System fornece insights sobre a saúde e qualidade dos dados, indicando quaisquer problemas ou alertas que possam precisar de atenção.
  
#### Command Usage
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Arguments
  
- **PROJECT_NAME**: O nome do projeto para o qual o status do TLS está sendo consultado (obrigatório).
- **TABLE_NAME**: A tabela específica dentro do projeto para a qual o status do TLS é necessário (obrigatório).
- **DATE**: A data para a qual o status do TLS está sendo consultado, tipicamente no formato %Y-%m-%d (obrigatório).
  
#### Example
  
Para verificar o status do TLS para uma tabela chamada UserData no projeto ProjectA em 1 de julho de 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Este comando ajuda os usuários a monitorar e manter a qualidade dos dados, fornecendo um relatório claro e acionável com base em critérios predefinidos.

## Using `inspect-async` Command

O comando `inspect-async` na CLI ***digna*** é usado para instruir o backend a realizar assincronamente a inspeção para uma ou mais fontes de dados de um dado projeto. Se project_name for definido como all-projects, a inspeção irá iterar sobre todos os projetos disponíveis e executar a inspeção. Ele retorna um id de requisição que pode ser usado para rastrear o progresso da inspeção.

#### Command Usage

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: O nome do projeto cujos dados serão inspecionados (obrigatório). Usar a palavra-chave all-projects neste argumento instrui a ***digna*** a iterar sobre todos os projetos existentes e aplicar este comando.
- **FROM_DATE**: A data e hora de início para a inspeção de dados. Formatos aceitáveis incluem %Y-%m-%d, %Y-%m-%dT%H:%M:%S, ou %Y-%m-%d %H:%M:%S (obrigatório).
- **TO_DATE**: A data e hora de término para a inspeção de dados, seguindo os mesmos formatos de FROM_DATE (obrigatório).
  
#### Options

- `--table-name`, `-tn`: Limita a inspeção a uma tabela específica dentro do projeto.
- `--table-filter`, `-tf`: Filtra para inspecionar apenas tabelas que contenham a substring especificada em seus nomes.

  
#### Example
  
Para inspecionar dados do projeto `ProjectA` de 1 de janeiro de 2024 a 31 de janeiro de 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Using `inspect-status` Command

O comando `inspect-status` na CLI ***digna*** é usado para verificar o progresso de uma inspeção assíncrona com base no ID da requisição.

#### Command Usage

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Arguments
  
- **REQUEST_ID**: O id da requisição retornado pelo comando `inspect-async` 
  
#### Options

- `--report_level`, `-rl`: Define o nível do relatório: 'task' ou 'step' [default: task]
  
#### Example
  
Para verificar o progresso de uma inspeção com request ID 12345 no nível detalhado de passos:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Using `export-ds` Command

O comando `export-ds` na CLI ***digna*** é usado para criar uma exportação de fontes de dados do repositório ***digna***. Por padrão, todas as fontes de dados de um dado projeto serão exportadas.

#### Command Usage
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Arguments
- **PROJECT_NAME**: O nome do projeto do qual as fontes de dados serão exportadas.

#### Options

- `--table_name`, `-tn`: Exporta uma fonte de dados específica de um projeto.
- `--exportfile`, `-ef`: Especifica o nome do arquivo para a exportação.
    
#### Example
  
Para exportar todas as fontes de dados do projeto chamado `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Este comando exporta todas as fontes de dados de `ProjectA` como um documento JSON que pode ser importado para outro projeto ou repositório ***digna***.


## Using `import-ds` Command

O comando `import-ds` na CLI ***digna*** é usado para importar fontes de dados para um projeto alvo e criar um relatório de importação.

#### Command Usage
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME**: O nome do projeto para o qual as fontes de dados serão importadas.
- **EXPORT_FILE**: O nome do arquivo da exportação de fontes de dados a ser importado.

#### Options

- `--output-file`, `-o`: Arquivo para salvar o relatório de importação (se não especificado, imprime no terminal em forma tabular).
- `--output-format`, `-f`: Formato para salvar o relatório de importação (json, csv).
    
#### Example
  
Para importar todas as fontes de dados do arquivo de exportação `my_export.json` para `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Após a importação, este comando também exibirá um relatório dos objetos importados e pulados. Somente novas fontes de dados serão importadas para `ProjectB`. Para descobrir quais objetos seriam importados e pulados, você pode usar o comando `plan-import-ds`.

## Using `plan-import-ds` Command

O comando `plan-import-ds` na CLI ***digna*** é usado para analisar uma exportação de fontes de dados em relação a um projeto alvo e gerar um plano/relatório de importação.

#### Command Usage
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME**: O nome do projeto para o qual as fontes de dados seriam importadas.
- **EXPORT_FILE**: O nome do arquivo da exportação de fontes de dados a ser analisado antes da importação.

#### Options

- `--output-file`, `-o`: Arquivo para salvar o relatório de importação (se não especificado, imprime no terminal em forma tabular).
- `--output-format`, `-f`: Formato para salvar o relatório de importação (json, csv).
    
#### Example
  
Para verificar quais fontes de dados seriam importadas e quais seriam puladas a partir do arquivo de exportação `my_export.json` ao importar para `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Este comando exibirá apenas um plano de importação dos objetos a serem importados e pulados.