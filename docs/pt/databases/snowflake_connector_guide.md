---
title: Snowflake Connector – Integração de Banco de Dados | digna Documentation
description: Configure o digna para conectar ao Snowflake usando o conector Python nativo ou o driver ODBC do Snowflake. Suporta autenticação por senha com configurações com DSN ou sem DSN.
image: /assets/logo_square.png
---


# Conector de Origem para Snowflake

Este guia descreve como configurar o *digna* para conectar ao Snowflake usando o conector Python nativo ou o driver ODBC.

Refere-se à tela **"Criar uma Conexão de Banco de Dados"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Driver Python Nativo

**Biblioteca:** `snowflake-connector-python`  
**Autenticação Suportada:** Somente autenticação baseada em senha

> Para outros métodos de autenticação, por favor use o driver ODBC.

### Configuração do *digna* (Driver Nativo)

Forneça as seguintes informações na tela **"Criar uma Conexão de Banco de Dados"**:

```
Technology:      Snowflake
Host Address:    Nome da conta Snowflake
Host Port:       Não é necessário
Database Name:   Banco de dados que contém o esquema de origem
Schema Name:     Esquema que contém os dados de origem
User Name:       Nome de usuário e warehouse no formato "user<@>warehouse"
User Password:   Senha do usuário
Use ODBC:        Desabilitado (padrão)
```

---

## Driver ODBC

O driver ODBC pode suportar uma gama mais ampla de opções de autenticação e conectividade. Esta seção foca na autenticação baseada em senha usando o **SnowflakeDSIIDriver**.

### 1. Instale o Driver ODBC

Instale o **SnowflakeDSIIDriver** seguindo o guia de instalação oficial do fornecedor.

### 2. Configure a Fonte de Dados ODBC

Siga estes passos para configurar uma nova fonte de dados ODBC usando autenticação baseada em senha:

#### Passo 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Observações:
- Se você não fornecer valores para Database, Schema e Warehouse, então será necessário fornecê-los como propriedades ODBC durante a configuração da fonte de dados do *digna*.
- O valor para "Server" consiste no nome da sua conta do Snowflake seguido por ".snowflakecomputing.com"

#### Passo 2 – Teste a conexão

Clique no botão **TEST**. Uma conexão bem-sucedida deve ser assim:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Agora você pode configurar o *digna* para usar a conexão ODBC, seja com um **DSN (Data Source Name)** ou uma configuração **sem DSN**.

---

### A. Configuração baseada em DSN

#### Configuração do *digna*

Na tela **"Criar uma Conexão de Banco de Dados"**, forneça o seguinte:

```
Technology:      Snowflake
Database Name:   Banco de dados que contém o esquema de origem
Schema Name:     Esquema que contém os dados de origem
Use ODBC:        Habilitado
```

#### Propriedades ODBC

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{sua senha entre chaves}"

opcionalmente:
name: "Database",       value: "Banco de dados que contém o esquema de origem"
name: "Schema",         value: "Esquema que contém os dados de origem"
name: "Warehouse",      value: "Warehouse a ser usado para a execução dos SQLs"
```

> O `DSN` deve corresponder ao nome definido na configuração do seu driver ODBC.

---

### B. Configuração sem DSN

#### Configuração do *digna*

Na tela **"Criar uma Conexão de Banco de Dados"**, forneça o seguinte:

```
Technology:      Snowflake
Database Name:   Esquema que contém os dados de origem (mesmo que Schema Name)
Schema Name:     Esquema que contém os dados de origem
Use ODBC:        Habilitado
```

#### Propriedades ODBC

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Banco de dados que contém o esquema de origem"
name: "Schema",     value: "Esquema que contém os dados de origem"
name: "Warehouse",  value: "Warehouse a ser usado para a execução dos SQLs"
```