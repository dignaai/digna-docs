---
title: Referência da CLI digna 2024.11 – Comandos & Exemplos | Documentação digna
description: Referência completa para a CLI digna release 2024.11. Aprenda a gerenciar usuários, repositórios e dados com comandos como add-user, check-repo-connection, upgrade-repo, inspect, tls-status e mais.
image: /assets/logo_square.png
---

# digna CLI Reference 2024.11
**2024-11-03**

Esta página documenta o conjunto completo de comandos disponíveis na CLI ***digna*** release **2024.11**, incluindo exemplos de uso e opções.


---
## Noções Básicas da CLI

---

## Usando a opção `help`

A opção `--help` fornece informações sobre os comandos disponíveis e seu uso. Existem duas maneiras principais de usar essa opção:

1. **Exibindo a Ajuda Geral:**
   
   Use --help imediatamente após a palavra-chave ***dignacli***  
   ```bash
   dignacli --help
   ```

3.  **Obtendo Ajuda para Comandos Específicos:**  
  
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

  
## Usando o comando `check-repo-connection`

O comando check-repo-connection é uma utilidade dentro da ferramenta CLI ***digna*** projetada para testar a conectividade e o acesso a um repositório ***digna*** especificado. Este comando garante que a CLI consiga interagir com o repositório.
      
### Uso do Comando
```bash
dignacli check-repo-connection
```

Após a execução bem-sucedida, o comando exibe uma confirmação da conexão, juntamente com detalhes sobre o repositório: versão do repositório, Host, Banco de Dados e Schema.  
  
Se a conexão com o repositório não for bem-sucedida, verifique o arquivo config.toml para garantir que as configurações estejam corretas.

## Usando o comando ‘version’

Para verificar a versão instalada do *dignacli*, use a opção --version.  
  
### Uso do Comando
```bash
dignacli --version
```
  
### Exemplo de Saída
```bash
dignacli version 2024.11
```

## Usando opções de logging
  
Por padrão, a saída no console dos comandos da ***digna*** é projetada para ser minimalista. A maioria dos comandos oferece a possibilidade de fornecer informações adicionais, usando as seguintes opções:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
“verbose” e “debug” definem o nível de detalhe, enquanto a opção “logfile” permite redirecionar a saída para ser gravada em um arquivo em vez de exibida no console.

# Gerenciamento de Usuários

## Usando o comando ‘add-user’
  
O comando add-user na CLI ***digna*** é usado para adicionar um novo usuário ao sistema ***digna***.
  
### Uso do Comando
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumentos

- **USER_NAME**: O nome de usuário do novo usuário (obrigatório).
- **USER_FULL_NAME**: O nome completo do novo usuário (obrigatório).
- **USER_PASSWORD**: A senha do novo usuário (obrigatório).

### Opções

- `--is_superuser`, `-su`: Flag para designar o novo usuário como administrador.
- `--valid_until`, `-vu`: Define uma data de expiração para a conta do usuário no formato `YYYY-MM-DD HH:MI:SS`. Se não for definida, a conta não terá data de expiração.

### Exemplo

Para adicionar um novo usuário com o nome de usuário `jdoe`, nome completo `John Doe` e senha `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Para adicionar um novo usuário e definir uma data de expiração da conta:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Usando o comando `delete-user`
  
O comando `delete-user` na CLI ***digna*** é usado para remover um usuário existente do sistema ***digna***.
  
### Uso do Comando
```bash
dignacli delete-user USER_NAME
```
  
### Argumentos
- **USER_NAME**: O nome de usuário do usuário a ser excluído (obrigatório). Este é o único argumento requerido pelo comando.

### Exemplo
```bash
dignacli delete-user jdoe
```
  
A execução deste comando removerá o usuário `jdoe` do sistema ***digna***, revogando seu acesso e excluindo seus dados e permissões associados do repositório.

## Usando o comando `modify-user`

O comando `modify-user` na CLI ***digna*** é usado para atualizar os detalhes de um usuário existente no sistema ***digna***.

### Uso do Comando
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumentos
  
- **USER_NAME**: O nome de usuário do usuário a ser modificado (obrigatório).
- **USER_FULL_NAME**: O novo nome completo do usuário (obrigatório).
  
### Opções  
  
- `--is_superuser`, `-su`: Define o usuário como superusuário, concedendo privilégios elevados. Esta flag não requer um valor.  
- `--valid_until`, `-vu`: Define uma data de expiração para a conta do usuário no formato YYYY-MM-DD HH:MI:SS. Se não for fornecida, a conta permanece válida indefinidamente.  
  
### Exemplo
  
Para modificar o nome completo do usuário `jdoe` para “Johnathan Doe” e definir o usuário como superusuário:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Usando o comando `modify-user-pwd`
  
O comando `modify-user-pwd` na CLI ***digna*** é usado para alterar a senha de um usuário existente no sistema ***digna***.
  
### Uso do Comando
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumentos
  
- **USER_NAME**: O nome de usuário do usuário cuja senha será alterada (obrigatório).
- **USER_PWD**: A nova senha do usuário (obrigatório).
  
### Exemplo
  
Para alterar a senha do usuário `jdoe` para `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Usando o comando `list-users`

O comando `list-users` na CLI ***digna*** exibe uma lista de todos os usuários registrados no sistema ***digna***.

### Uso do Comando

```bash
dignacli list-users
```

A execução deste comando na CLI ***digna*** conectará ao repositório ***digna*** e listará todos os usuários, mostrando seu ID, nome de usuário, nome completo, status de superusuário e timestamps de expiração.

# Gerenciamento de Repositório

### Usando o comando `upgrade-repo`
  
O comando `upgrade-repo` na CLI ***digna*** é usado para atualizar ou inicializar o repositório ***digna***. Este comando é essencial para aplicar atualizações ou configurar a infraestrutura do repositório pela primeira vez.
  
### Uso do Comando

```bash
dignacli upgrade-repo [options]
```
  
### Opções
  
- `--simulation-mode`, `-s`: Quando habilitado, esta opção executa o comando em modo de simulação, imprimindo as instruções SQL que seriam executadas, mas não as executa de fato. Isto é útil para visualizar as mudanças sem modificar o repositório.  

  
### Exemplo
  
Para atualizar o repositório ***digna***, você pode executar o comando sem opções:
  
```bash
dignacli upgrade-repo
```  
Para executar a atualização em modo de simulação (para ver as instruções SQL sem aplicá-las):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Este comando é crucial para manter o sistema ***digna***, garantindo que o schema do banco de dados e outros componentes do repositório estejam atualizados com a versão mais recente do software.

## Usando o comando `encrypt`
  
O comando `encrypt` na CLI ***digna*** é usado para criptografar uma senha.
  
### Uso do Comando
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumentos
- **PASSWORD**: A senha que precisa ser criptografada (obrigatório).
  
### Exemplo
  
Para criptografar uma senha, você precisa fornecer a senha como argumento.   
Por exemplo, para criptografar a senha `mypassword123`, você usaria:
```bash
dignacli encrypt mypassword123
```
Este comando retorna a versão criptografada da senha fornecida, que pode então ser usada em contextos seguros. Se o argumento de senha não for fornecido, a CLI exibirá um erro indicando o argumento ausente.

## Usando o comando `generate-key`
  
O comando `generate-key` é usado para gerar uma chave Fernet, que é essencial para proteger senhas armazenadas no repositório ***digna***.
  
### Uso do Comando
```bash
dignacli generate-key
```
  
# Gerenciamento de Dados

## Usando o comando `clean-up`

O comando `clean-up` na CLI ***digna*** é usado para remover perfis, previsões e dados do sistema de semáforo (traffic light system) para uma ou mais fontes de dados dentro de um projeto especificado. Este comando é essencial para o gerenciamento do ciclo de vida dos dados, ajudando a manter um ambiente de dados organizado e eficiente ao limpar dados desatualizados ou desnecessários.

### Uso do Comando

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentos
  
- **PROJECT_NAME**: O nome do projeto do qual os dados serão removidos (obrigatório). Usar a palavra-chave all-projects neste argumento instruirá a ***digna*** a iterar sobre todos os projetos existentes e aplicar este comando.
- **FROM_DATE**: A data e hora de início para a remoção de dados. Formatos aceitos incluem %Y-%m-%d, %Y-%m-%dT%H:%M:%S, ou %Y-%m-%d %H:%M:%S (obrigatório).
- **TO_DATE**: A data e hora de término para a remoção de dados, seguindo os mesmos formatos de FROM_DATE (obrigatório).
  
### Opções
  
- `--table-name`, `-tn`: Limita a operação de limpeza a uma tabela específica dentro do projeto.
- `--table-filter`, `-tf`: Filtra para limitar a limpeza às tabelas que contenham a substring especificada em seus nomes.
- `--timing`, `-tm`: Exibe a duração do processo de limpeza após a conclusão.
- `--help`: Exibe informações de ajuda para o comando clean-up e sai.
  
### Exemplo
  
Para remover dados do projeto ProjectA entre 1 de janeiro de 2023 e 30 de junho de 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Para remover dados apenas de uma tabela específica chamada `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Este comando ajuda no gerenciamento do armazenamento de dados e garante que o repositório contenha apenas informações relevantes.

## Usando o comando `inspect`

O comando `inspect` na CLI ***digna*** é usado para criar perfis, previsões e dados do sistema de semáforo (traffic light system) para uma ou mais fontes de dados dentro de um projeto especificado. Este comando ajuda a analisar e monitorar os dados em um período definido.

### Uso do Comando

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentos
  
- **PROJECT_NAME**: O nome do projeto para o qual os dados serão inspecionados (obrigatório). Usar a palavra-chave all-projects neste argumento instruirá a ***digna*** a iterar sobre todos os projetos existentes e aplicar este comando.
- **FROM_DATE**: A data e hora de início para a inspeção de dados. Formatos aceitos incluem %Y-%m-%d, %Y-%m-%dT%H:%M:%S, ou %Y-%m-%d %H:%M:%S (obrigatório).
- **TO_DATE**: A data e hora de término para a inspeção de dados, seguindo os mesmos formatos de FROM_DATE (obrigatório).
  
### Opções

- `--table-name`, `-tn`: Limita a inspeção a uma tabela específica dentro do projeto.
- `--table-filter`, `-tf`: Filtra para inspecionar apenas tabelas que contenham a substring especificada em seus nomes.
- `--do-profile`: Aciona a recolha de perfis. O padrão é do-profile.
- `--no-do-profile`: Impede a recolha de perfis.
- `--do-prediction`: Aciona o recálculo de previsões. O padrão é do-prediction.
- `--no-do-prediction`: Impede o recálculo de previsões.
- `--do-alert-status`: Aciona o recálculo dos status de alerta. O padrão é do-alert-status.
- `--no-do-alert-status`: Impede o recálculo dos status de alerta.
- `--timing`, `-tm`: Exibe a duração do processo de inspeção após a conclusão.
  
### Exemplo
  
Para inspecionar dados do projeto `ProjectA` de 1 de janeiro de 2024 a 31 de janeiro de 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Para inspecionar apenas uma tabela específica e forçar o recálculo de previsões:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Este comando é útil para gerar perfis e previsões atualizados, monitorar a integridade dos dados e gerenciar sistemas de alerta dentro de um intervalo de tempo especificado para o projeto.

## Usando o comando `tls-status`

O comando `tls-status` na CLI ***digna*** é usado para consultar o status do Traffic Light System (TLS) para uma tabela específica dentro de um projeto em uma dada data. O Traffic Light System fornece insights sobre a saúde e qualidade dos dados, indicando quaisquer problemas ou alertas que possam exigir atenção.
  
### Uso do Comando
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumentos
  
- **PROJECT_NAME**: O nome do projeto para o qual o status TLS está sendo consultado (obrigatório).
- **TABLE_NAME**: A tabela específica dentro do projeto para a qual o status TLS é necessário (obrigatório).
- **DATE**: A data para a qual o status TLS está sendo consultado, tipicamente no formato %Y-%m-%d (obrigatório).
  
### Exemplo
  
Para verificar o status TLS de uma tabela chamada UserData no projeto ProjectA em 1 de julho de 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Este comando ajuda os usuários a monitorar e manter a qualidade dos dados, fornecendo um relatório claro e acionável de status baseado em critérios predefinidos.

## Usando o comando `list-projects`
  
O comando `list-projects` na CLI ***digna*** é usado para exibir uma lista de todos os projetos disponíveis no sistema ***digna***.
  
### Uso do Comando
  
```bash
dignacli list-projects
```

Este comando é especialmente útil para administradores e usuários que gerenciam múltiplos projetos, fornecendo uma visão rápida dos projetos disponíveis no repositório ***digna***.

## Usando o comando `list-ds`

O comando `list-ds` na CLI ***digna*** é usado para exibir uma lista de todas as fontes de dados disponíveis dentro de um projeto especificado. Este comando é útil para entender os ativos de dados disponíveis para análise e gerenciamento no sistema ***digna***.

### Uso do Comando
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumentos
- **PROJECT_NAME**: O nome do projeto cujas fontes de dados estão sendo listadas (obrigatório).
  
### Exemplo
  
Para listar todas as fontes de dados no projeto chamado `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Este comando fornece aos usuários uma visão geral das fontes de dados disponíveis em um projeto, ajudando-os a navegar e gerenciar o panorama de dados de forma mais eficaz.