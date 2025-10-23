---
title: Conector MS SQL Server – Integração de Banco de Dados | Documentação digna
description: Configure o digna para conectar ao Microsoft SQL Server usando o driver Python pymssql ou o driver ODBC do SQL Server. Suporta autenticação por senha em configurações com DSN ou sem DSN.
image: /assets/logo_square.png
---


# Source Connector for MS SQL Server

Este guia descreve como configurar o *digna* para conectar ao SQL Server usando o conector Python nativo ou o driver ODBC.

Refere-se à tela **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Supported Authentication:** Autenticação baseada em senha apenas

> ⚠️ Para outros métodos de autenticação, por favor use o driver ODBC.

### *digna* Configuration (Native Driver)

Forneça as seguintes informações na tela **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    Nome do servidor ou endereço IP
Host Port:       Número da porta, ex.: 1433
Database Name:   Nome do banco de dados
Schema Name:     Schema que contém os dados de origem
User Name:       Nome do usuário do banco de dados
User Password:   Senha do usuário
Use ODBC:        Desabilitado (padrão)
```

---

## ODBC Driver

O driver ODBC pode suportar uma gama mais ampla de opções de autenticação e conectividade. Esta seção foca na autenticação por senha usando o driver **SQL Server**.

### 1. Instale o Driver ODBC

Instale o driver **SQL Server** (ou similar) seguindo o guia de instalação oficial do fornecedor.

### 2. Configure a Fonte de Dados ODBC

Siga estes passos para configurar uma nova fonte de dados ODBC usando autenticação por senha:

#### Step 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Clique no botão **Next >**.

#### Step 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Escolha o método de autenticação (ex.: nome de usuário e senha)
e forneça os dados necessários.

Clique no botão **Next >**.

#### Step 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Escolha as configurações compatíveis com ANSI e então clique no botão **Next >**.

#### Step 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Você pode manter as configurações padrão ou escolher opções de log conforme necessário
e clicar no botão **Finish**. 

#### Step 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Agora clique no botão **Test datasource**.

#### Step 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

Quando você receber a tela de sucesso, o ODBC está configurado corretamente.

---

Agora você pode configurar o *digna* para usar a conexão ODBC, seja com um **DSN (Data Source Name)** ou uma configuração **sem DSN**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Na tela **"Create a Database Connection"**, forneça o seguinte:

```
Technology:      MS SQL Server
Database Name:   Banco de dados que contém o schema de origem
Schema Name:     Schema que contém os dados de origem
Use ODBC:        Habilitado
```

#### ODBC Properties

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "seu usuário de banco de dados"
name: "PWD",        value: "sua senha de banco de dados"
name: "DATABASE",   value: "nome do banco de dados que contém o schema de dados de origem"

```

> 🔹 O `DSN` deve corresponder ao nome definido na configuração do seu driver ODBC.

---

### B. DSN-less Configuration

#### *digna* Configuration

Na tela **"Create a Database Connection"**, forneça o seguinte:

```
Technology:      MS SQL Server
Database Name:   Schema que contém os dados de origem (mesmo que Schema Name)
Schema Name:     Schema que contém os dados de origem
Use ODBC:        Habilitado
```

#### ODBC Properties

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "seu nome de servidor ou endereço IP"
name: "UID",        value: "seu usuário de banco de dados"
name: "PWD",        value: "sua senha de banco de dados"
name: "DATABASE",   value: "nome do banco de dados que contém o schema de dados de origem"
```