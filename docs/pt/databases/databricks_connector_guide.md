---
title: Conector Databricks com Unity Catalog – Integração de Banco de Dados | Documentação digna
description: Configure o digna para conectar-se ao Databricks com Unity Catalog usando o conector Python nativo ou o driver ODBC. Suporta autenticação por token e conectividade flexível.
image: /assets/logo_square.png
---

# Source Connector for Databricks - with Unity Catalog

Este guia descreve como configurar o *digna* para conectar-se ao Databricks usando o conector Python nativo ou o driver ODBC.

Refere-se à tela **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> ⚠️ Para outros métodos de autenticação, por favor utilize o driver ODBC.

### Personal Access Token (PAT)

Para autenticar usando um personal access token, consulte a documentação oficial do Databricks:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Forneça as seguintes informações na tela **"Create a Database Connection"**:

```
Technology:      Databricks
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Name of the catalog to use. 
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

O driver ODBC suporta uma gama mais ampla de opções de autenticação e conectividade. Esta seção foca na autenticação por token usando o **Simba Spark ODBC Driver**.

### 1. Install the ODBC Driver

Instale o **Simba Spark ODBC Driver** seguindo o guia de instalação oficial do fornecedor.

### 2. Configure the ODBC Data Source

Siga estes passos para configurar uma nova data source ODBC usando um Personal Access Token:

#### Etapa 1
![Etapa 1](images/databricks/create_odbc_data_source_step1.png)

#### Etapa 2
![Etapa 2](images/databricks/create_odbc_data_source_step2.png)

#### Etapa 3
![Etapa 3](images/databricks/create_odbc_data_source_step3.png)

#### Etapa 4
![Etapa 4](images/databricks/create_odbc_data_source_step4.png)

#### Etapa 5 – Testar a conexão

Clique no botão **TEST**. Uma conexão bem-sucedida deve ser semelhante a esta:

![Etapa 5](images/databricks/create_odbc_data_source_step5.png)

---

Agora você pode configurar o *digna* para usar a conexão ODBC, seja com um **DSN (Data Source Name)** ou uma configuração **DSN-less**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Na tela **"Create a Database Connection"**, forneça o seguinte:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 O `DSN` deve corresponder ao nome definido na configuração do seu driver ODBC.

---

### B. DSN-less Configuration

#### *digna* Configuration

Na tela **"Create a Database Connection"**, forneça o seguinte:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name = "Driver",          value = "{Simba Spark ODBC Driver}"
name = "Host",            value = "xxxxxxxxxxxxxxxxxxx.databricks.com"
name = "Port",            value = "443"
name = "HTTPPath",        value = "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
name = "SSL",             value = "1"
name = "ThriftTransport", value = "2"
name = "AuthMech",        value = "3"
name = "UID",             value = "token"
name = "PWD",             value = "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```