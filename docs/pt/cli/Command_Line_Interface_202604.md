---
title: Referência da CLI digna 2026.04 – Comandos e Exemplos | Documentação digna
description: Referência completa da CLI digna versão 2026.04
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202604/
image: /assets/logo_square.png
---

# digna CLI Reference 2026.04
**2026-04-08**

Esta página documenta o conjunto completo de comandos disponíveis na CLI ***digna*** release **2026.04**, incluindo exemplos de uso e opções.

---

## Noções Básicas da CLI

---

### help
A opção `--help` fornece informações sobre os comandos disponíveis e seu uso. Existem duas formas principais de usar essa opção:

1. **Exibindo Ajuda Geral:**
   
    Use --help imediatamente após a palavra-chave ***digna***cl  
   ```bash
   dignacli --help
   ```

2. **Obtendo Ajuda para Comandos Específicos:**  
  
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

### check-config

O comando check-config é uma utilidade dentro da ferramenta CLI ***digna*** projetada para testar a configuração do ***digna***. Esse comando garante que os componentes do ***digna*** consigam localizar os elementos de configuração necessários no config.toml.

#### Opções

- `--configpath`, `-cp`: Arquivo ou diretório que contém a configuração. Se omitido, ../config.toml será utilizado.
      
#### Uso do Comando
```bash
dignacli check-config
```

Após a execução bem-sucedida, o comando exibe uma confirmação da completude da configuração.  
  
Se a configuração aparentar estar incompleta, os elementos de configuração faltantes serão listados.

  
### check-repo-connection

O comando check-repo-connection é uma utilidade dentro da CLI ***digna*** projetada para testar a conectividade e o acesso a um repositório especificado do ***digna***. Esse comando garante que a CLI consiga interagir com o repositório.
      
#### Uso do Comando
```bash
dignacli check-repo-connection
```

Após a execução bem-sucedida, o comando exibe uma confirmação da conexão, juntamente com detalhes sobre o repositório: versão do repositório, host, banco de dados e schema.  
  
Se a conexão com o repositório não for bem-sucedida, verifique o arquivo config.toml para as configurações corretas.


### version

Para verificar a versão instalada do *dignacli*, use a opção --version.  
  
#### Uso do Comando
```bash
dignacli --version
```
  
#### Exemplo de Saída
```bash
dignacli version 2026.04
```

### opções de logging
  
Por padrão, a saída no console dos comandos da ***digna*** é projetada para ser minimalista. A maioria dos comandos oferece a possibilidade de fornecer informações adicionais, usando as seguintes opções:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” e “debug” definem o nível de detalhamento, enquanto o interruptor “logfile” permite redirecionar a saída para ser gravada em um arquivo em vez de exibida na janela do console.

## Gerenciamento de Usuários

### add-user
  
O comando add-user na CLI ***digna*** é usado para adicionar um novo usuário ao sistema ***digna***.
  
#### Uso do Comando
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumentos

- **USER_NAME**: O nome de usuário para o novo usuário (obrigatório).
- **USER_FULL_NAME**: O nome completo do novo usuário (obrigatório).
- **USER_PASSWORD**: A senha do novo usuário (obrigatório).

#### Opções

- `--is_superuser`, `-su`: Flag para designar o novo usuário como administrador.
- `--valid_until`, `-vu`: Define uma data de expiração para a conta do usuário no formato `YYYY-MM-DD HH:MI:SS`. Se não for definido, a conta não terá data de expiração.

#### Exemplo

Para adicionar um novo usuário com nome de usuário `jdoe`, nome completo `John Doe` e senha `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Para adicionar um novo usuário e definir a data de expiração da conta:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
O comando `delete-user` na CLI ***digna*** é usado para remover um usuário existente do sistema ***digna***.
  
#### Uso do Comando
```bash
dignacli delete-user USER_NAME
```
  
#### Argumentos
- **USER_NAME**: O nome de usuário do usuário a ser excluído (obrigatório). Este é o único argumento exigido pelo comando.

#### Exemplo
```bash
dignacli delete-user jdoe
```
  
A execução deste comando removerá o usuário `jdoe` do sistema ***digna***, revogando seu acesso e excluindo seus dados e permissões associados do repositório.

### modify-user

O comando `modify-user` na CLI ***digna*** é usado para atualizar os detalhes de um usuário existente no sistema ***digna***.

#### Uso do Comando
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumentos
  
- **USER_NAME**: O nome de usuário do usuário a ser modificado (obrigatório).
- **USER_FULL_NAME**: O novo nome completo do usuário (obrigatório).
  
#### Opções  
  
- `--is_superuser`, `-su`: Define o usuário como superusuário, concedendo privilégios elevados. Esta flag não requer valor.  
- `--valid_until`, `-vu`: Define uma data de expiração para a conta do usuário no formato YYYY-MM-DD HH:MI:SS. Se não fornecida, a conta permanece válida indefinidamente.  
  
#### Exemplo
  
Para modificar o nome completo do usuário `jdoe` para “Johnathan Doe” e definir o usuário como superusuário:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
O comando `modify-user-pwd` na CLI ***digna*** é usado para alterar a senha de um usuário existente no sistema ***digna***.
  
#### Uso do Comando
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumentos
  
- **USER_NAME**: O nome de usuário do usuário cuja senha será alterada (obrigatório).
- **USER_PWD**: A nova senha do usuário (obrigatório).
  
#### Exemplo
  
Para alterar a senha do usuário `jdoe` para `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

O comando `list-users` na CLI ***digna*** exibe uma lista de todos os usuários registrados no sistema ***digna***.

#### Uso do Comando

```bash
dignacli list-users
```

A execução deste comando na CLI ***digna*** irá conectar-se ao repositório ***digna*** e listar todos os usuários, mostrando seu ID, nome de usuário, nome completo, status de superusuário e timestamps de expiração.

## Gerenciamento de Repositório

### upgrade-repo
  
O comando `upgrade-repo` na CLI ***digna*** é usado para atualizar ou inicializar o repositório ***digna***. Este comando é essencial para aplicar atualizações ou configurar a infraestrutura do repositório pela primeira vez.
  
#### Uso do Comando

```bash
dignacli upgrade-repo [options]
```
  
#### Opções
  
- `--simulation-mode`, `-s`: Quando ativada, essa opção executa o comando em modo de simulação, imprimindo as instruções SQL que seriam executadas, mas sem realmente executá-las. Isso é útil para pré-visualizar alterações sem fazer modificações no repositório.  

  
#### Exemplo
  
Para atualizar o repositório ***digna***, você pode executar o comando sem opções:
  
```bash
dignacli upgrade-repo
```  
Para executar a atualização em modo de simulação (para ver as instruções SQL sem aplicá-las):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Este comando é crucial para manter o sistema ***digna***, garantindo que o esquema do banco de dados e outros componentes do repositório estejam atualizados com a versão mais recente do software.

### encrypt
  
O comando `encrypt` na CLI ***digna*** é usado para criptografar uma senha.
  
#### Uso do Comando
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumentos
- **PASSWORD**: A senha que precisa ser criptografada (obrigatório).
  
#### Exemplo
  
Para criptografar uma senha, é necessário fornecer a senha como argumento.   
Por exemplo, para criptografar a senha `mypassword123`, você usaria:
```bash
dignacli encrypt mypassword123
```
Este comando retorna a versão criptografada da senha fornecida, que pode então ser usada em contextos seguros. Se o argumento da senha não for fornecido, a CLI exibirá um erro indicando o argumento ausente.

### generate-key
  
O comando `generate-key` é usado para gerar uma chave Fernet, que é essencial para proteger senhas armazenadas no repositório ***digna***.
  
#### Uso do Comando
```bash
dignacli generate-key
```
  
## Gerenciamento de Dados

### clean-up

O comando `clean-up` na CLI ***digna*** é usado para remover perfis, previsões e dados do sistema de semáforo para uma ou mais fontes de dados dentro de um projeto especificado. Este comando é essencial para o gerenciamento do ciclo de vida dos dados, ajudando a manter um ambiente de dados organizado e eficiente ao limpar dados antigos ou desnecessários.

#### Uso do Comando

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentos
  
- **PROJECT_NAME**: O nome do projeto do qual os dados serão removidos (obrigatório). Usar a palavra-chave all-projects neste argumento instrui o ***digna*** a iterar sobre todos os projetos existentes e aplicar este comando.
- **FROM_DATE**: A data e hora de início para a remoção de dados. Formatos aceitáveis incluem %Y-%m-%d, %Y-%m-%dT%H:%M:%S, ou %Y-%m-%d %H:%M:%S (obrigatório).
- **TO_DATE**: A data e hora de término para a remoção de dados, seguindo os mesmos formatos de FROM_DATE (obrigatório).
  
#### Opções
  
- `--table-name`, `-tn`: Limita a operação de limpeza a uma tabela específica dentro do projeto.
- `--table-filter`, `-tf`: Filtra para limitar a limpeza às tabelas que contêm a substring especificada em seus nomes.
- `--timing`, `-tm`: Exibe a duração do processo de limpeza após a conclusão.
- `--help`: Exibe informações de ajuda para o comando clean-up e sai.
  
#### Exemplo
  
Para remover dados do projeto ProjectA entre 1 de janeiro de 2023 e 30 de junho de 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Para remover dados apenas de uma tabela específica chamada `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Este comando ajuda a gerenciar o armazenamento de dados e garantir que o repositório contenha apenas informações relevantes.

### remove-orphans
  
O comando `remove-orphans` na CLI ***digna*** é usado para manutenção (house-keeping) no repositório ***digna***.  
Quando um usuário exclui projetos ou fontes de dados, os perfis e previsões permanecem no repositório. Com este comando, essas linhas órfãs serão removidas do repositório.
  
#### Uso do Comando
  
```bash
dignacli list-projects
```

### list-projects
  
O comando `list-projects` na CLI ***digna*** é usado para exibir uma lista de todos os projetos disponíveis dentro do sistema ***digna***.
  
#### Uso do Comando
  
```bash
dignacli list-projects
```

Este comando é especialmente útil para administradores e usuários que gerenciam múltiplos projetos, fornecendo uma visão rápida dos projetos disponíveis no repositório ***digna***.

### list-ds

O comando `list-ds` na CLI ***digna*** é usado para exibir uma lista de todas as fontes de dados disponíveis dentro de um projeto especificado. Este comando é útil para entender os ativos de dados disponíveis para análise e gestão no sistema ***digna***.

#### Uso do Comando
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentos
- **PROJECT_NAME**: O nome do projeto cujas fontes de dados estão sendo listadas (obrigatório).
  
#### Exemplo
  
Para listar todas as fontes de dados no projeto chamado `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Este comando fornece aos usuários uma visão geral das fontes de dados disponíveis em um projeto, ajudando-os a navegar e gerenciar o panorama de dados de forma mais eficaz.


### inspect

O comando `inspect` na CLI ***digna*** é usado para criar perfis, previsões e dados do sistema de semáforo para uma ou mais fontes de dados dentro de um projeto especificado. Este comando ajuda a analisar e monitorar dados ao longo de um período definido. Após a conclusão da inspeção, o valor do sistema de semáforo calculado é retornado:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Uso do Comando

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentos
  
- **PROJECT_NAME**: O nome do projeto cujos dados serão inspecionados (obrigatório). Usar a palavra-chave all-projects neste argumento instrui o ***digna*** a iterar sobre todos os projetos existentes e aplicar este comando.
- **FROM_DATE**: A data e hora de início para a inspeção de dados. Formatos aceitáveis incluem %Y-%m-%d, %Y-%m-%dT%H:%M:%S, ou %Y-%m-%d %H:%M:%S (obrigatório).
- **TO_DATE**: A data e hora de término para a inspeção de dados, seguindo os mesmos formatos de FROM_DATE (obrigatório).
  
#### Opções

- `--table-name`, `-tn`: Limita a inspeção a uma tabela específica dentro do projeto.
- `--table-filter`, `-tf`: Filtra para inspecionar apenas tabelas que contenham a substring especificada em seus nomes.
- `--enable_notification`, `-en`: Habilita o envio de notificações em caso de alertas.
- `--bypass-backend`, `-bb`: Desvia o backend e executa a inspeção diretamente pela CLI (apenas para fins de teste!).

  
#### Exemplo
  
Para inspecionar dados do projeto `ProjectA` de 1 de janeiro de 2024 a 31 de janeiro de 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Para inspecionar apenas uma tabela específica e forçar o recálculo de previsões:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Este comando é útil para gerar perfis e previsões atualizadas, monitorar a integridade dos dados e gerenciar sistemas de alerta dentro de um intervalo de tempo especificado do projeto.

### inspect-async

O comando `inspect-async` na CLI ***digna*** é usado para criar perfis, previsões e dados do sistema de semáforo para uma ou mais fontes de dados dentro de um projeto especificado. Este comando ajuda a analisar e monitorar dados ao longo de um período definido. Em contraste com o comando `inspect`, este não espera pela conclusão da inspeção.
Em vez disso, ele retorna o id da requisição para a solicitação de inspeção submetida. Para consultar o progresso do processo de inspeção, use o comando `inspect-status`.

#### Uso do Comando

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentos
  
- **PROJECT_NAME**: O nome do projeto cujos dados serão inspecionados (obrigatório). Usar a palavra-chave all-projects neste argumento instrui o ***digna*** a iterar sobre todos os projetos existentes e aplicar este comando.
- **FROM_DATE**: A data e hora de início para a inspeção de dados. Formatos aceitáveis incluem %Y-%m-%d, %Y-%m-%dT%H:%M:%S, ou %Y-%m-%d %H:%M:%S (obrigatório).
- **TO_DATE**: A data e hora de término para a inspeção de dados, seguindo os mesmos formatos de FROM_DATE (obrigatório).
  
#### Opções

- `--table-name`, `-tn`: Limita a inspeção a uma tabela específica dentro do projeto.
- `--table-filter`, `-tf`: Filtra para inspecionar apenas tabelas que contenham a substring especificada em seus nomes.
- `--enable_notification`, `-en`: Habilita o envio de notificações em caso de alertas.

  
#### Exemplo
  
Para inspecionar dados do projeto `ProjectA` de 1 de janeiro de 2024 a 31 de janeiro de 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

O comando `inspect-status` na CLI ***digna*** é usado para verificar o progresso de uma inspeção assíncrona com base no ID da requisição.

#### Uso do Comando

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumentos
  
- **REQUEST_ID**: O id da requisição retornado pelo comando `inspect-async` 
  
#### Exemplo
  
Para verificar o progresso de uma inspeção com o id de requisição 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

O comando `inspect-cancel` na CLI ***digna*** é usado para cancelar inspeções com base no ID da requisição ou pode ser usado para cancelar todas as requisições atuais.

#### Uso do Comando

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumentos
  
- **REQUEST_ID**: O id da requisição retornado pelo comando `inspect-async` 
  
#### Exemplo
  
Para cancelar a inspeção com id de requisição 12345:
  
```bash
dignacli inspect-cancel 12345
```

Para cancelar todas as requisições que estão atualmente em execução ou pendentes:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

O comando `export-ds` na CLI ***digna*** é usado para criar uma exportação de fontes de dados do repositório ***digna***. Por padrão, todas as fontes de dados de um determinado projeto serão exportadas.

#### Uso do Comando
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentos
- **PROJECT_NAME**: O nome do projeto do qual as fontes de dados serão exportadas.

#### Opções

- `--table_name`, `-tn`: Exporta uma fonte de dados específica de um projeto.
- `--exportfile`, `-ef`: Especifica o nome do arquivo para a exportação.
    
#### Exemplo
  
Para exportar todas as fontes de dados do projeto chamado `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Este comando exporta todas as fontes de dados de `ProjectA` como um documento JSON que pode ser importado para outro projeto ou repositório ***digna***.


### import-ds

O comando `import-ds` na CLI ***digna*** é usado para importar fontes de dados para um projeto alvo e criar um relatório de importação.

#### Uso do Comando
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentos
- **PROJECT_NAME**: O nome do projeto para o qual as fontes de dados serão importadas.
- **EXPORT_FILE**: O nome do arquivo da exportação de fontes de dados a ser importada.

#### Opções

- `--output-file`, `-o`: Arquivo para salvar o relatório de importação (se não especificado, imprime no terminal em formato tabular).
- `--output-format`, `-f`: Formato para salvar o relatório de importação (json, csv).
    
#### Exemplo
  
Para importar todas as fontes de dados do arquivo de exportação `my_export.json` para `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Após a importação, este comando também exibirá um relatório dos objetos importados e ignorados. Apenas novas fontes de dados serão importadas para `ProjectB`. Para descobrir quais objetos seriam importados e ignorados, você pode usar o comando `plan-import-ds`.

### plan-import-ds

O comando `plan-import-ds` na CLI ***digna*** é usado para analisar uma exportação de fontes de dados e gerar um plano de importação com relatório, sem efetuar a importação.

#### Uso do Comando
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentos
- **PROJECT_NAME**: O nome do projeto para o qual as fontes de dados seriam importadas.
- **EXPORT_FILE**: O nome do arquivo da exportação de fontes de dados a ser analisado antes da importação.

#### Opções

- `--output-file`, `-o`: Arquivo para salvar o relatório de importação (se não especificado, imprime no terminal em formato tabular).
- `--output-format`, `-f`: Formato para salvar o relatório de importação (json, csv).
    
#### Exemplo
  
Para verificar quais fontes de dados seriam importadas e quais seriam ignoradas do arquivo de exportação `my_export.json` ao importar para `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Este comando apenas mostrará um plano de importação dos objetos a serem importados e ignorados.