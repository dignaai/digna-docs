---
title: Conector Apache Hive – Integração de Banco de Dados | Documentação digna
description: Configure o digna para conectar-se ao Apache Hive usando o driver nativo PyHive ou o driver ODBC da Cloudera. Suporta autenticação baseada em senha e configurações com DSN ou sem DSN.
image: /assets/logo_square.png
---


# Conector de Origem para Hive

Este guia descreve como configurar o *digna* para conectar-se ao Hive usando o conector nativo em Python ou o driver ODBC.

Refere-se à tela **"Create a Database Connection"**.

![Criar uma conexão com o banco de dados](images/data_source_config_input_mask.png)

---

## Driver Python Nativo

**Library:** `PyHive`  
**Autenticação Suportada:** apenas autenticação baseada em senha

> ⚠️ Para outros métodos de autenticação, por favor use o driver ODBC.

### Configuração do *digna* (Driver Nativo)

Forneça as seguintes informações na tela **"Create a Database Connection"**:

```
Technology:      Apache Hive
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 10000
Database Name:   Schema that contains the source data
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## Driver ODBC

O driver ODBC pode oferecer uma gama mais ampla de opções de autenticação e conectividade. Esta seção foca na autenticação baseada em senha usando o driver **Cloudera ODBC Driver for Apache Hive**.

### 1. Instale o Driver ODBC

Instale o **Cloudera ODBC Driver for Apache Hive** (ou similar) seguindo o guia de instalação oficial do fornecedor.

### 2. Configure a Fonte de Dados ODBC

Siga estes passos para configurar uma nova fonte de dados ODBC usando autenticação baseada em senha:

#### Etapa 1
![Etapa 1](images/hive/create_odbc_data_source_step1.png)


#### Etapa 2 – Testar a conexão

Forneça a senha e clique no botão **Testar**.

![Etapa 2](images/hive/create_odbc_data_source_step2.png)

Após um teste bem-sucedido, clique no botão **OK**.

---

Agora você pode configurar o *digna* para usar a conexão ODBC, seja com **DSN (Data Source Name)** ou com uma configuração **sem DSN**.

---

### A. Configuração Baseada em DSN

#### Configuração do *digna*

Na tela **"Create a Database Connection"**, forneça o seguinte:

```
Technology:      Apache Hive
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Propriedades ODBC

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{your password in curly braces}"
```

> 🔹 O `DSN` deve corresponder ao nome definido na configuração do seu driver ODBC.

---

### B. Configuração Sem DSN

#### Configuração do *digna*

Na tela **"Create a Database Connection"**, forneça o seguinte:

```
Technology:      Apache Hive
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Propriedades ODBC

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 10000"
name: "Schema",     value: "Schema that contains the source data"
name: "UID",        value: "your hive user'
name: "PWD",        value: "your hive password"
name: "AuthMech",   value: "3"
```