---
title: Conector Apache Hive – Integração de Banco de Dados | Documentação digna
description: Configure o digna para se conectar ao Apache Hive via ODBC com uma connection string sem DSN. Abrange o driver ODBC Cloudera para Hive, mecanismos de autenticação, modos de transporte e as configurações de conexão do lado do digna.
image: /assets/logo_square.png
---


# Conector de Origem para Hive

Este guia descreve como configurar o *digna* para se conectar ao Apache Hive via **ODBC**,
usando uma connection string **sem DSN**.

O lado do *digna* na configuração é o mesmo para todas as tecnologias — onde as conexões são
criadas, como os valores das propriedades são criptografados, como uma conexão é testada e o que
significam os modos de perfilamento. Isso está descrito na
[Visão Geral das Conexões de Banco de Dados](overview.md). Esta página cobre o que é específico
do Hive.

---

## 1. Instalar o Driver ODBC {: #1-install-the-odbc-driver }

Instale o **Cloudera ODBC Driver for Apache Hive** na máquina que executa o backend do *digna*,
seguindo o guia de instalação oficial do fornecedor.

Leia no seu host o nome exato do driver registrado, conforme descrito em
[Instalar o Driver ODBC no Host do digna](overview.md#install-the-driver).

---

## 2. Propriedades ODBC {: #2-odbc-properties }

!!! important "Um exemplo, não uma especificação"

    O conjunto abaixo é uma combinação que comprovadamente funciona. As propriedades pertencem
    ao driver Cloudera para Hive, portanto seus nomes, valores padrão e valores aceitos variam
    entre versões do driver e plataformas, e o que o HiveServer2 aceita depende inteiramente de
    como o cluster está protegido — mecanismo de autenticação, modo de transporte, TLS, gateway.
    Use isto como ponto de partida e consulte a documentação da versão do driver que você
    instalou.

Adicione as seguintes propriedades na tela **Add DB Connection**:

| Key | Valor de exemplo | Observações |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Deve corresponder ao nome do driver registrado no host do *digna* |
| `HOST` | `hive.example.com` | Nome do host ou endereço IP do HiveServer2 |
| `PORT` | `10000` | Porta do HiveServer2; `10001` para transporte HTTP |

A connection string resultante fica assim:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Autenticação

Um HiveServer2 sem proteção aceita as três propriedades acima como estão. Onde a autenticação
estiver habilitada, adicione:

| Key | Valor de exemplo | Observações |
|---|---|---|
| `AuthMech` | `3` | `0` sem autenticação, `2` apenas nome de usuário, `3` nome de usuário e senha, `1` Kerberos |
| `UID` | `digna_source_user` | Obrigatório para `AuthMech` `2` e `3` |
| `PWD` | `<password>` | Obrigatório para `AuthMech` `3`. Marque **Encrypted** |

Para Kerberos (`AuthMech=1`), o host do *digna* também precisa de um ticket ou keytab válido,
além das propriedades `KrbHostFQDN`, `KrbServiceName` e `KrbRealm` documentadas pelo driver.

### Transporte e TLS

| Key | Valor de exemplo | Observações |
|---|---|---|
| `ThriftTransport` | `2` | `0` binário (o padrão, porta 10000), `1` SASL, `2` HTTP (porta 10001, e o que um gateway Knox espera) |
| `HTTPPath` | `cliservice` | Com `ThriftTransport=2` |
| `SSL` | `1` | Quando o HiveServer2 é protegido por TLS |
| `Schema` | `dignadata` | Banco de dados Hive em que a sessão começa. Opcional — o *digna* qualifica suas consultas |

---

## 3. Configuração do *digna* {: #3-digna-configuration }

Na tela **Add DB Connection**, informe o seguinte:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Observações sobre o Hive {: #4-notes-on-hive }

- **Os catálogos vêm do driver.** O Hive não tem catálogo próprio, então o *digna* usa o que o
  driver informa — normalmente uma única entrada chamada `HIVE` — e lista os bancos de dados
  Hive como schemas abaixo dela.
- **O Work Schema é um banco de dados Hive.** Para o perfilamento *Permanent*, o usuário precisa
  de permissão para criar e excluir tabelas nele, e o local de armazenamento subjacente deve
  permitir gravação.
- **Modos de perfilamento.** *Permanent* cria as tabelas de trabalho em **Work Schema**.
  *Session* usa `CREATE TEMPORARY TABLE`, o que exige um HiveServer2 que suporte tabelas
  temporárias, e não utiliza **Work Schema**. *Standard* precisa apenas de acesso de leitura e é
  o modo a escolher em um cluster onde o *digna* não tem nenhum acesso de gravação.
- **O perfilamento é um conjunto de consultas, não uma varredura.** Toda estatística é calculada
  pelo HiveServer2, então a fila para a qual o usuário do *digna* envia as consultas deve ter
  capacidade suficiente para a janela de inspeção.

---

## 5. Verificar o Driver (opcional) {: #5-verifying-the-driver-optional }

Configurar uma fonte de dados ODBC não é necessário para uma conexão sem DSN, mas o diálogo do
próprio driver é uma forma prática de confirmar que o driver, o modo de transporte e suas
credenciais funcionam antes de inseri-los no *digna*.

#### Passo 1
![Passo 1](images/hive/create_odbc_data_source_step1.png)

Os campos **Host**, **Port**, **Database**, **Mechanism** e **Thrift Transport** aqui
correspondem às propriedades `HOST`, `PORT`, `Schema`, `AuthMech` e `ThriftTransport` da
[seção 2](#2-odbc-properties).

#### Passo 2 – Testar a Conexão

Informe a senha e clique no botão **Test**.

![Passo 2](images/hive/create_odbc_data_source_step2.png)

Após um teste bem-sucedido, clique no botão **OK**.
