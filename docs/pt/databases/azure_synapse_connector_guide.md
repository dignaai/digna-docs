---
title: Conector do Azure Synapse – Integração de Banco de Dados | Documentação digna
description: Configure o *digna* para conectar ao Azure Synapse Analytics usando o driver nativo Python ou o driver ODBC. Suporta pools SQL serverless e dedicados.
image: /assets/logo_square.png
canonical_url: https://docs.digna.ai/databases/azure_synapse_connector_guide/
---


# Source Connector for Azure Synapse Analytics

Este guia descreve como configurar o *digna* para se conectar ao Azure Synapse Analytics usando o conector nativo em Python ou o driver ODBC.
Suporta tanto pools SQL serverless quanto dedicados.

Refere-se à tela **"Create a Database Connection"**.

![Criar uma conexão de banco de dados](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Supported Authentication:** Autenticação baseada em senha apenas

> ⚠️ Para outros métodos de autenticação, utilize o driver ODBC.

### *digna* Configuration (Native Driver)

Forneça as seguintes informações na tela **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Número da porta, p.ex. 1433
Database Name:   Nome do banco de dados
Schema Name:     Esquema que contém os dados de origem
User Name:       Nome do usuário do banco de dados
User Password:   Senha do usuário
Use ODBC:        Disabled (padrão)
```

---

## ODBC Driver

O driver ODBC pode oferecer uma gama mais ampla de opções de autenticação e conectividade. Esta seção foca na autenticação baseada em senha usando o driver **ODBC Driver 18 for SQL Server**.

### 1. Instale o ODBC Driver

Instale o driver **ODBC Driver 18 for SQL Server** (ou similar) seguindo o guia oficial de instalação do fornecedor.

### 2. Configure a Fonte de Dados ODBC

Siga estes passos para configurar uma nova fonte de dados ODBC usando autenticação baseada em senha:

#### Step 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Preencha o campo "Server".
Use o nome do workspace do Synapse e acrescente ".sql.azuresynapse.net".  
**Atenção**, se desejar conectar usando um pool SQL serverless, certifique-se de incluir "-ondemand" conforme mostrado na captura de tela abaixo.

Clique no botão **Next >**.

#### Step 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Escolha o método de autenticação (por exemplo, nome de usuário e senha)
e forneça os dados requeridos.

Clique no botão **Next >**.

#### Step 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Escolha as configurações compatíveis com ANSI e clique no botão **Next >**.

#### Step 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Você pode manter as configurações padrão ou escolher opções conforme necessário 
e clicar no botão **Finish**. 

#### Step 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Agora clique no botão **Test datasource**.

#### Step 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Quando aparecer a tela de sucesso, o ODBC está configurado corretamente.

---

Agora você pode configurar o *digna* para usar a conexão ODBC, seja com **DSN (Data Source Name)** ou em configuração **sem DSN (DSN-less)**.

---

### A. Configuração baseada em DSN

#### *digna* Configuration

Na tela **"Create a Database Connection"**, forneça o seguinte:

```
Technology:      MS SQL Server
Database Name:   Banco de dados que contém o esquema de origem
Schema Name:     Esquema que contém os dados de origem
Use ODBC:        Enabled
```

#### Propriedades ODBC

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "seu usuário do banco de dados"
name: "PWD",        value: "sua senha do banco de dados"
name: "DATABASE",   value: "nome do banco de dados que contém o esquema dos dados de origem"
```

> 🔹 O `DSN` deve corresponder ao nome definido na configuração do seu driver ODBC.

---

### B. Configuração sem DSN (DSN-less)

#### *digna* Configuration

Na tela **"Create a Database Connection"**, forneça o seguinte:

```
Technology:      MS SQL Server
Database Name:   Esquema que contém os dados de origem (mesmo que Schema Name)
Schema Name:     Esquema que contém os dados de origem
Use ODBC:        Enabled
```

#### Propriedades ODBC

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "seu usuário do banco de dados"
name: "PWD",        value: "sua senha do banco de dados"
name: "DATABASE",   value: "nome do banco de dados que contém o esquema dos dados de origem"
```

**Observação** sobre a propriedade SERVER:  
Use o nome do workspace do Synapse e acrescente ".sql.azuresynapse.net". Se quiser conectar usando um pool SQL serverless, certifique-se de incluir "-ondemand" conforme mostrado na captura de tela abaixo.