---
title: Conector Teradata – Integração de Banco de Dados | Documentação digna
description: Configure o digna para se conectar ao Teradata via ODBC com uma connection string sem DSN. Abrange o driver ODBC do Teradata, a propriedade DBCNAME, os mecanismos de logon e as configurações de conexão do lado do digna.
image: /assets/logo_square.png
---


# Conector de Origem para Teradata

Este guia descreve como configurar o *digna* para se conectar ao Teradata via **ODBC**, usando
uma connection string **sem DSN**.

O lado do *digna* na configuração é o mesmo para todas as tecnologias — onde as conexões são
criadas, como os valores das propriedades são criptografados, como uma conexão é testada e o que
significam os modos de perfilamento. Isso está descrito na
[Visão Geral das Conexões de Banco de Dados](overview.md). Esta página cobre o que é específico
do Teradata.

---

## 1. Instalar o Driver ODBC {: #1-install-the-odbc-driver }

Instale o **ODBC Driver for Teradata** na máquina que executa o backend do *digna*, seguindo o
guia de instalação oficial do fornecedor.

O driver se registra com a versão no nome, por exemplo
**Teradata Database ODBC Driver 20.00**. Leia no seu host o nome exato registrado, conforme
descrito em [Instalar o Driver ODBC no Host do digna](overview.md#install-the-driver).

---

## 2. Propriedades ODBC {: #2-odbc-properties }

!!! important "Um exemplo, não uma especificação"

    O conjunto abaixo é uma combinação que comprovadamente funciona. As propriedades pertencem
    ao driver ODBC do Teradata, portanto seus nomes, valores padrão e valores aceitos variam
    entre versões do driver — a versão faz parte do próprio nome do driver — e entre
    plataformas. Use isto como ponto de partida e consulte a documentação da versão do driver
    que você instalou.

Adicione as seguintes propriedades na tela **Add DB Connection**:

| Key | Valor de exemplo | Observações |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Deve corresponder ao nome do driver registrado no host do *digna* |
| `DBCNAME` | `teradata.example.com` | Nome do servidor ou endereço IP. É o nome que o próprio Teradata dá à propriedade do host |
| `UID` | `digna_source_user` | Usuário do banco de dados |
| `PWD` | `<password>` | Marque **Encrypted** |

A connection string resultante fica assim:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Propriedades adicionais úteis:

| Key | Valor de exemplo | Observações |
|---|---|---|
| `MechanismName` | `TD2` | Mecanismo de logon. `TD2` é o padrão do Teradata; use `LDAP` para autenticação por diretório |
| `DefaultDatabase` | `dad` | Banco de dados em que a sessão começa |
| `CharacterSet` | `UTF8` | Defina-o quando o conjunto de caracteres padrão da sessão corromperia dados não ASCII |

---

## 3. Configuração do *digna* {: #3-digna-configuration }

Na tela **Add DB Connection**, informe o seguinte:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Observações sobre o Teradata {: #4-notes-on-teradata }

- **Um banco de dados Teradata é um catálogo, não um schema.** O *digna* lista os bancos de
  dados que o usuário pode ver (de `DBC.DatabasesV`) como catálogos, e o nível de schema não se
  aplica. Ao adicionar uma fonte de dados, escolha o banco de dados como catálogo; o schema é
  informado como *not applicable*.
- **Uma conexão alcança todos os bancos de dados permitidos**, então uma única conexão pode
  atender a origens em vários bancos de dados — ao contrário das tecnologias em que a conexão
  fica presa a um único banco de dados.
- **O Work Schema é um banco de dados.** Para o perfilamento *Permanent*, indique o banco de
  dados Teradata que contém as tabelas de trabalho e dê ao usuário permissões de `CREATE TABLE`,
  além de uma alocação de espaço `PERM` nele — um banco de dados com zero de perm space não pode
  conter uma tabela.
- **Modos de perfilamento.** *Permanent* cria tabelas em **Work Schema**. *Session* usa uma
  tabela `VOLATILE`, que precisa de espaço `SPOOL`, mas não de perm space nem de permissões em
  **Work Schema**. *Standard* precisa apenas de acesso de leitura.

---

## 5. Verificar o Driver (opcional) {: #5-verifying-the-driver-optional }

Configurar uma fonte de dados ODBC não é necessário para uma conexão sem DSN, mas o diálogo do
próprio driver é uma forma prática de confirmar que o driver e suas credenciais funcionam antes
de inseri-los no *digna*.

#### Passo 1
![Passo 1](images/teradata/create_odbc_data_source_step1.png)

O campo **Name or IP address** aqui corresponde à propriedade `DBCNAME` da
[seção 2](#2-odbc-properties).

Clique no botão **Test**.

#### Passo 2
![Passo 2](images/teradata/create_odbc_data_source_step2.png)

Informe o nome de usuário e a senha e clique no botão **OK**. Uma tela de sucesso confirma que
o driver e as credenciais funcionam.
