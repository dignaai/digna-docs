---
title: Conector Snowflake – Integração de Banco de Dados | Documentação digna
description: Configure o digna para se conectar ao Snowflake via ODBC com uma connection string sem DSN. Abrange o driver ODBC do Snowflake, programmatic access tokens, a seleção de warehouse e role e as configurações de conexão do lado do digna.
image: /assets/logo_square.png
---


# Conector de Origem para Snowflake

Este guia descreve como configurar o *digna* para se conectar ao Snowflake via **ODBC**, usando
uma connection string **sem DSN**.

O lado do *digna* na configuração é o mesmo para todas as tecnologias — onde as conexões são
criadas, como os valores das propriedades são criptografados, como uma conexão é testada e o que
significam os modos de perfilamento. Isso está descrito na
[Visão Geral das Conexões de Banco de Dados](overview.md). Esta página cobre o que é específico
do Snowflake.

---

## 1. Instalar o Driver ODBC {: #1-install-the-odbc-driver }

Instale o **Snowflake ODBC Driver** na máquina que executa o backend do *digna*, seguindo o
[guia de instalação do Snowflake](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

O driver se registra como **SnowflakeDSIIDriver**. Leia no seu host o nome exato registrado,
conforme descrito em [Instalar o Driver ODBC no Host do digna](overview.md#install-the-driver).

---

## 2. Propriedades ODBC {: #2-odbc-properties }

O Snowflake é acessado com um **programmatic access token (PAT)** — o caminho de autenticação
com o qual o *digna* é verificado e aquele que o Snowflake exige para contas em que o login
apenas com senha está bloqueado.

!!! important "Um exemplo, não uma especificação"

    O conjunto abaixo é uma combinação que comprovadamente funciona. As propriedades pertencem
    ao driver ODBC do Snowflake, portanto seus nomes, valores padrão e valores aceitos variam
    entre versões do driver e plataformas, e quais opções de autenticação a sua conta permite é
    definido pela política de segurança da conta. Use isto como ponto de partida e consulte a
    documentação da versão do driver que você instalou.

| Key | Valor de exemplo | Observações |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Deve corresponder ao nome do driver registrado no host do *digna* |
| `Server` | `<account>.snowflakecomputing.com` | Identificador da conta mais o sufixo, ex.: `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Usuário do Snowflake ao qual o token pertence |
| `Database` | `TEST` | Banco de dados que contém os schemas de origem. É o único banco de dados que esta conexão pode perfilar |
| `Schema` | `PUBLIC` | Schema padrão da sessão |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Seleciona a autenticação por token |
| `token` | `<programmatic access token>` | Marque **Encrypted** |

A connection string resultante fica assim:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Warehouse e Role

As consultas precisam de um warehouse. Se o usuário do *digna* tiver um warehouse padrão e uma
role padrão, a sessão os utiliza e nada precisa ser configurado. Caso contrário, adicione:

| Key | Valor de exemplo | Observações |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Warehouse que executa as consultas de perfilamento |
| `Role` | `DIGNA_READER` | Role cujas permissões a sessão usa |

!!! tip "Dê ao digna um warehouse próprio"

    Um warehouse separado, pequeno e com suspensão automática mantém o custo do perfilamento
    visível e evita que o *digna* concorra por capacidade de processamento com usuários
    interativos.

### Autenticação por Senha

Onde a conta ainda permitir, uma senha funciona no lugar do token — remova `authenticator` e
`token` e adicione:

| Key | Valor de exemplo | Observações |
|---|---|---|
| `PWD` | `<password>` | Marque **Encrypted** |

---

## 3. Configuração do *digna* {: #3-digna-configuration }

Na tela **Add DB Connection**, informe o seguinte:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Observações sobre o Snowflake {: #4-notes-on-snowflake }

- **Os tokens expiram.** Um programmatic access token é emitido com um prazo de validade, e o
  perfilamento para no dia em que ele vence. Anote a data de expiração ao criá-lo e insira o
  novo token na propriedade `token` — valores criptografados podem ser substituídos, mas não
  lidos de volta.
- **Uma conexão enxerga um banco de dados.** O *digna* oferece os schemas do banco de dados
  indicado em `Database`, porque o Snowflake informa apenas o banco de dados atual como
  catálogo. Tabelas de origem em outro banco de dados precisam de uma conexão própria.
- **Os identificadores ficam em maiúsculas**, a menos que tenham sido criados entre aspas. O
  *digna* usa os nomes conforme o Snowflake os informa.
- **Modos de perfilamento.** *Permanent* cria as tabelas de trabalho em **Work Schema**, então a
  role precisa de `CREATE TABLE` ali. *Session* usa `CREATE TEMPORARY TABLE` e não utiliza
  **Work Schema**. *Standard* precisa apenas de acesso de leitura — e de nenhuma permissão de
  gravação.

---

## 5. Verificar o Driver (opcional) {: #5-verifying-the-driver-optional }

Configurar uma fonte de dados ODBC não é necessário para uma conexão sem DSN, mas o diálogo do
próprio driver é uma forma prática de confirmar que o driver, a URL da conta e suas credenciais
funcionam antes de inseri-los no *digna*.

#### Passo 1
![Passo 1](images/snowflake/create_odbc_data_source_step1.png)

Observações:

- O valor de **Server** consiste no identificador da sua conta Snowflake seguido de
  `.snowflakecomputing.com`.
- **Database**, **Schema** e **Warehouse** inseridos aqui correspondem às propriedades
  `Database`, `Schema` e `Warehouse` da [seção 2](#2-odbc-properties).

#### Passo 2 – Testar a Conexão

Clique no botão **TEST**. Uma conexão bem-sucedida deve ter esta aparência:

![Passo 2](images/snowflake/create_odbc_data_source_step2.png)
