---
title: Conector Teradata – Integração de Banco de Dados | Documentação digna
description: Configure o digna para conectar-se ao Teradata usando o driver Python teradatasql ou o driver ODBC da Teradata. Suporta autenticação baseada em senha com configurações com DSN ou sem DSN.
image: /assets/logo_square.png
---


# Source Connector for Teradata

Este guia descreve como configurar o *digna* para conectar-se ao Teradata usando o conector Python nativo ou o driver ODBC.

Refere-se à tela **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `teradatasql`  
**Supported Authentication:** Password-based authentication only

> ⚠️ Para outros métodos de autenticação, utilize o driver ODBC.

### *digna* Configuration (Native Driver)

Forneça as seguintes informações na tela **"Create a Database Connection"**:

```
Technology:      Teradata
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1025
Database Name:   Database name
Schema Name:     Database name
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

O driver ODBC pode oferecer uma gama mais ampla de opções de autenticação e conectividade. Esta seção foca na autenticação baseada em senha usando o driver **Teradata Database ODBC Driver 20.00**.

### 1. Install the ODBC Driver

Instale o driver **Teradata Database ODBC Driver 20.00** (ou similar) seguindo o guia de instalação oficial do fornecedor.

### 2. Configure the ODBC Data Source

Siga estes passos para configurar uma nova fonte de dados ODBC usando autenticação baseada em senha:

#### Step 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Clique no botão **Test**.

#### Step 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Informe o nome de usuário e a senha.

Clique no botão **OK**.
Quando você receber a tela de sucesso, o ODBC estará configurado corretamente.

---

Agora você pode configurar o *digna* para usar a conexão ODBC, seja com um **DSN (Data Source Name)** ou uma configuração **DSN-less**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Na tela **"Create a Database Connection"**, forneça o seguinte:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 O `DSN` deve corresponder ao nome definido na configuração do seu driver ODBC.

---

### B. DSN-less Configuration

#### *digna* Configuration

Na tela **"Create a Database Connection"**, forneça o seguinte:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
