---
title: Oracle Connector – Database Integration | digna Documentation
description: Configure o digna para conectar ao Oracle usando o driver python-oracledb ou o driver ODBC da Oracle. Suporta autenticação por senha com configurações DSN ou sem DSN.
image: /assets/logo_square.png
---


# Source Connector for Oracle

Este guia descreve como configurar o *digna* para conectar ao Oracle DB usando o conector nativo em Python ou o driver ODBC.

Refere-se à tela **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `python-oracledb`  
**Supported Authentication:** Password-based authentication only

> ⚠️ Para outros métodos de autenticação, por favor use o driver ODBC.

### *digna* Configuration (Native Driver)

Forneça as seguintes informações na tela **"Create a Database Connection"**:

```
Technology:      Oracle
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1521
Database Name:   Instance name, service name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

O driver ODBC pode suportar uma gama mais ampla de opções de autenticação e conectividade. Esta seção foca na autenticação por senha usando o driver **Oracle in OraDB21Home1**.

### 1. Install the ODBC Driver

Instale o **Oracle in OraDB21Home1** (ou similar) seguindo o guia de instalação oficial do fornecedor.

### 2. Configure the ODBC Data Source

Siga estes passos para configurar um novo data source ODBC usando autenticação por senha:

#### Step 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Nota:
O TNS Service Name deve ser configurado no arquivo tnsnames.ora da sua instalação do cliente Oracle. É aí que você fornece o descritor de conexão (host, porta, service name).

#### Step 2 – Test the connection

Clique no botão **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Forneça a senha e clique no botão **OK**.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Agora você pode configurar o *digna* para usar a conexão ODBC, seja com um **DSN (Data Source Name)** ou uma configuração **DSN-less**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Na tela **"Create a Database Connection"**, forneça o seguinte:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> 🔹 O `DSN` deve corresponder ao nome definido na configuração do seu driver ODBC.

---

### B. DSN-less Configuration

#### *digna* Configuration

Na tela **"Create a Database Connection"**, forneça o seguinte:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```