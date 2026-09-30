---
title: Conector Netezza – Integração de Banco de Dados | Documentação digna
description: Configure o digna para se conectar ao Netezza via ODBC com uma connection string sem DSN. Abrange o driver NetezzaSQL, as propriedades ODBC necessárias e as configurações de conexão do lado do digna.
image: /assets/logo_square.png
---


# Conector de Origem para Netezza

Este guia descreve como configurar o *digna* para se conectar ao Netezza via **ODBC**, usando
uma connection string **sem DSN**.

O lado do *digna* na configuração é o mesmo para todas as tecnologias — onde as conexões são
criadas, como os valores das propriedades são criptografados, como uma conexão é testada e o que
significam os modos de perfilamento. Isso está descrito na
[Visão Geral das Conexões de Banco de Dados](overview.md). Esta página cobre o que é específico
do Netezza.

---

## 1. Instalar o Driver ODBC {: #1-install-the-odbc-driver }

Instale o driver ODBC **NetezzaSQL** (parte das ferramentas de cliente do IBM Netezza) na
máquina que executa o backend do *digna*, seguindo o guia de instalação oficial do fornecedor.

Leia no seu host o nome exato do driver registrado, conforme descrito em
[Instalar o Driver ODBC no Host do digna](overview.md#install-the-driver).

---

## 2. Propriedades ODBC {: #2-odbc-properties }

!!! important "Um exemplo, não uma especificação"

    O conjunto abaixo é uma combinação que comprovadamente funciona. As propriedades pertencem
    ao driver NetezzaSQL, portanto seus nomes, valores padrão e valores aceitos variam entre
    versões do cliente e plataformas, e um appliance protegido por TLS precisa de mais do que as
    propriedades mostradas aqui. Use isto como ponto de partida e consulte a documentação da
    versão do cliente que você instalou.

Adicione as seguintes propriedades na tela **Add DB Connection**:

| Key | Valor de exemplo | Observações |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Deve corresponder ao nome do driver registrado no host do *digna*. As chaves são a forma usual de escrever esse nome |
| `SERVER` | `netezza.example.com` | Nome do servidor ou endereço IP |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Banco de dados em que a sessão começa |
| `UID` | `ADMIN` | Usuário do banco de dados |
| `PWD` | `<password>` | Marque **Encrypted** |

A connection string resultante fica assim:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

Dependendo da versão do driver, da configuração e dos requisitos de segurança, outras
propriedades podem ser necessárias — por exemplo, `SecurityLevel` e `CaCertFile` para um
appliance protegido por TLS. Toda opção oferecida pelos diálogos *Advanced*, *SSL* e *Driver*
do driver pode ser adicionada como propriedade.

---

## 3. Configuração do *digna* {: #3-digna-configuration }

Na tela **Add DB Connection**, informe o seguinte:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Observações sobre o Netezza {: #4-notes-on-netezza }

- **Catálogos e schemas se aplicam.** O *digna* lista os bancos de dados que o usuário pode ver
  (de `_V_DATABASE`) como catálogos e seus schemas (de `_V_SCHEMA`) abaixo deles, de modo que
  uma conexão pode atender a origens em mais de um banco de dados. `DATABASE` define apenas
  onde a sessão começa.
- **Os identificadores ficam em maiúsculas**, a menos que tenham sido criados entre aspas, e é
  por isso que os exemplos acima usam `TEST` e `ADMIN`.
- **Modos de perfilamento.** *Permanent* cria as tabelas de trabalho em **Work Schema**, então o
  usuário precisa de `CREATE TABLE` ali. *Session* usa `CREATE TEMPORARY TABLE` e não utiliza
  **Work Schema**. *Standard* precisa apenas de acesso de leitura.

---

## 5. Verificar o Driver (opcional) {: #5-verifying-the-driver-optional }

Configurar uma fonte de dados ODBC não é necessário para uma conexão sem DSN, mas o diálogo do
próprio driver é uma forma prática de confirmar que o driver e suas credenciais funcionam antes
de inseri-los no *digna*.

#### Passo 1
![Passo 1](images/netezza/create_odbc_data_source_step1.png)

Os campos em **DSN Options** correspondem um a um às propriedades da
[seção 2](#2-odbc-properties). Dependendo do seu driver Netezza, da configuração e dos
requisitos de segurança, você também pode precisar de dados nas abas **Advanced DSN Options**,
**SSL DSN Options** ou **Driver Options**; para a configuração mais simples, **DSN Options** é
suficiente.

Clique no botão **Test Connection**.

#### Passo 2
![Passo 2](images/netezza/create_odbc_data_source_step2.png)

Quando a tela de sucesso aparecer, o driver está funcionando e os valores estão corretos.
