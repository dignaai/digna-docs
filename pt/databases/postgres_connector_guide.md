# Conector de Origem para PostgreSQL

Este guia descreve como configurar o *digna* para se conectar ao Postgres usando tanto o conector nativo em Python quanto o driver ODBC.

Refere-se à tela **"Create a Database Connection"**.

![Criar uma conexão de banco de dados](images/data_source_config_input_mask.png)

---

## Driver Python Nativo

**Biblioteca:** `psycopg`  
**Autenticação Suportada:** Somente autenticação baseada em senha

> Para outros métodos de autenticação, use o driver ODBC.

### Configuração do *digna* (Driver Nativo)

Forneça as seguintes informações na tela **"Create a Database Connection"**:

```
Tecnologia:      Postgres
Endereço do Host:    Nome do servidor ou endereço IP
Porta do Host:       Número da porta, ex.: 5432
Nome do Banco:   Nome do banco de dados
Nome do Schema:     Schema que contém os dados de origem
Nome do Usuário:       Nome do usuário do banco de dados
Senha do Usuário:   Senha do usuário
Usar ODBC:        Desabilitado (padrão)
```

---

## Driver ODBC

O driver ODBC pode oferecer uma gama mais ampla de opções de autenticação e conectividade. Esta seção foca na autenticação baseada em senha usando o driver **PostgreSQL Unicode(x64)**.

### 1. Instale o Driver ODBC

Instale o **PostgreSQL Unicode(x64)** (ou similar) seguindo o guia de instalação oficial do fornecedor.

### 2. Configure a Fonte de Dados ODBC

Siga estes passos para configurar uma nova fonte de dados ODBC usando autenticação por senha:

#### Passo 1
![Passo 1](images/postgres/create_odbc_data_source_step1.png)

Observação: Se a configuração do seu banco de dados exigir que você escolha um "SSLMode" específico, certifique-se de também usar esse mesmo valor ao definir uma configuração sem DSN.

#### Passo 2 – Teste a conexão

Clique no botão **Test Connection**.

![Passo 2](images/postgres/create_odbc_data_source_step2.png)

---

Agora você pode configurar o *digna* para usar a conexão ODBC, seja com uma **DSN (Data Source Name)** ou uma configuração **DSN-less**.

---

### A. Configuração baseada em DSN

#### Configuração do *digna*

Na tela **"Create a Database Connection"**, forneça o seguinte:

```
Technology:      PostgreSQL
Database Name:   Banco de dados que contém o schema de origem
Schema Name:     Schema que contém os dados de origem
Use ODBC:        Enabled
```

#### Propriedades ODBC

```
name: "DSN",    value: "PostgreSQL35W"
```

> O `DSN` deve corresponder ao nome definido na configuração do seu driver ODBC.

---

### B. Configuração sem DSN

#### Configuração do *digna*

Na tela **"Create a Database Connection"**, forneça o seguinte:

```
Technology:      PostgreSQL
Database Name:   Schema que contém os dados de origem (igual ao Schema Name)
Schema Name:     Schema que contém os dados de origem
Use ODBC:        Enabled
```

#### Propriedades ODBC

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```