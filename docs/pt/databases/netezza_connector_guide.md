---
title: Conector Netezza – Integração de Banco de Dados | Documentação digna
description: Configure o *digna* para conectar-se ao Netezza usando o driver ODBC NetezzaSQL. Suporta autenticação por senha com configurações com DSN ou sem DSN para conectividade flexível.
image: /assets/logo_square.png
---


# Conector de Origem para Netezza

Este guia descreve como configurar o *digna* para conectar-se ao Netezza usando o driver ODBC.

Refere-se à tela **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## ODBC Driver

O driver ODBC pode suportar várias opções de autenticação e conectividade. Esta seção foca na autenticação baseada em senha usando o driver **NetezzaSQL**.

### 1. Instalar o Driver ODBC

Instale o driver **NetezzaSQL** (ou similar) seguindo o guia oficial de instalação do fornecedor.

### 2. Configurar a Fonte de Dados ODBC

Siga estes passos para configurar uma nova fonte de dados ODBC usando autenticação baseada em senha:

#### Step 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Dependendo do seu driver Netezza, dos requisitos de instalação e segurança, pode ser necessário fornecer também dados nas abas **Advanced DSN Options**, **SSL DSN Options** ou **Driver Options**. Para a configuração mais simples, é suficiente fornecer os dados em **DSN Options**.

Clique no botão **Test Connection**.

#### Step 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Quando você receber a tela de sucesso, o ODBC estará configurado corretamente.

---

Agora você pode configurar o *digna* para usar a conexão ODBC, seja com um **DSN (Data Source Name)** ou uma configuração **DSN-less**.

---

### A. Configuração baseada em DSN

#### Configuração do *digna*

Na tela **"Create a Database Connection"**, forneça o seguinte:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Propriedades ODBC

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> O `DSN` deve corresponder ao nome definido na configuração do seu driver ODBC.

---

### B. Configuração sem DSN

#### Configuração do *digna*

Na tela **"Create a Database Connection"**, forneça o seguinte:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Propriedades ODBC

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```