# Conector de Origem para Oracle

Este guia descreve como configurar o *digna* para se conectar ao Oracle Database via **ODBC**,
usando uma connection string **sem DSN**.

O lado do *digna* na configuração é o mesmo para todas as tecnologias — onde as conexões são
criadas, como os valores das propriedades são criptografados, como uma conexão é testada e o que
significam os modos de perfilamento. Isso está descrito na
[Visão Geral das Conexões de Banco de Dados](overview.md). Esta página cobre o que é específico
do Oracle.

---

## 1. Instalar o Driver ODBC {: #1-install-the-odbc-driver }

O driver ODBC do Oracle faz parte do **Oracle Client** (o pacote "ODBC" do Instant Client é
suficiente). Instale-o na máquina que executa o backend do *digna*, seguindo o guia de
instalação oficial do fornecedor.

O driver se registra como **Oracle in `<OracleHomeName>`** — por exemplo,
`Oracle in OraDB21Home1` ou `Oracle in instantclient_21_13`. O nome do home difere a cada
instalação, então leia no seu host o nome exato, conforme descrito em
[Instalar o Driver ODBC no Host do digna](overview.md#install-the-driver).

---

## 2. Propriedades ODBC {: #2-odbc-properties }

!!! important "Um exemplo, não uma especificação"

    O conjunto abaixo é uma combinação que comprovadamente funciona. As propriedades pertencem
    ao driver ODBC do Oracle, portanto seus nomes, valores padrão e valores aceitos variam entre
    versões do cliente, e o nome do driver, em particular, depende do Oracle home no seu host.
    Use isto como ponto de partida e consulte a documentação da versão do cliente que você
    instalou.

Adicione as seguintes propriedades na tela **Add DB Connection**:

| Key | Valor de exemplo | Observações |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Deve corresponder ao nome do driver registrado no host do *digna* |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | O banco de dados ao qual se conectar — veja abaixo |
| `UID` | `DIGNA_SOURCE_USER` | Usuário do banco de dados |
| `PWD` | `<password>` | Marque **Encrypted** |

A connection string resultante fica assim:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### O Valor de `DBQ`

`DBQ` aceita três formas. Para o *digna* elas são equivalentes; elas diferem no que precisa ser
configurado no host do *digna*:

| Forma | Exemplo | Requer |
|---|---|---|
| **Connect descriptor completo** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Nada — tudo está na propriedade. Recomendado |
| **Alias TNS** | `DIGNA_SOURCE` | O alias deve existir no `tnsnames.ora` do Oracle Client no host do *digna* |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Um Oracle Client que suporte Easy Connect (12c e posteriores) |

!!! tip "Prefira o descriptor completo"

    Um alias TNS move metade da definição da conexão para um arquivo no host do *digna*, onde é
    fácil esquecê-lo quando o host é reconstruído ou o *digna* é movido. O descriptor completo
    mantém a conexão autossuficiente — que é justamente o objetivo de uma configuração sem DSN.

Os parênteses de um descriptor não causam problema dentro de uma connection string, mas, se a
sua senha contiver `;`, coloque-a entre chaves: `PWD={p@ss;word}`.

---

## 3. Configuração do *digna* {: #3-digna-configuration }

Na tela **Add DB Connection**, informe o seguinte:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Observações sobre o Oracle {: #4-notes-on-oracle }

- **Schemas são usuários.** O *digna* lista os usuários do Oracle como schemas, então o schema
  de origem é o proprietário das tabelas — `DIGNA_SOURCE_USER` no exemplo acima. O usuário da
  conexão precisa de `SELECT` nessas tabelas, diretamente ou por meio de uma role.
- **Uma conexão enxerga um banco de dados.** O catálogo que o *digna* oferece é o banco de dados
  ao qual a conexão está ligada, então `DBQ` define qual serviço e, portanto, qual banco de
  dados é perfilado.
- **Identificadores diferenciam maiúsculas de minúsculas quando estão entre aspas.** O *digna*
  coloca entre aspas os nomes que lê do dicionário de dados, que é o que o Oracle armazena —
  maiúsculas para objetos sem aspas.
- **Modos de perfilamento.** *Permanent* cria as tabelas de trabalho em **Work Schema**, então o
  usuário precisa de `CREATE TABLE` ali e de uma cota no tablespace. *Session* usa uma tabela
  temporária privada (`ORA$PTT_…`, Oracle 18c e posteriores) e não utiliza **Work Schema**.
  *Standard* precisa apenas de acesso de leitura.

---

## 5. Verificar o Driver (opcional) {: #5-verifying-the-driver-optional }

Configurar uma fonte de dados ODBC não é necessário para uma conexão sem DSN, mas o diálogo do
próprio driver é uma forma prática de confirmar que o Oracle Client, o service name e suas
credenciais funcionam antes de inseri-los no *digna*.

#### Passo 1
![Passo 1](images/oracle/create_odbc_data_source_step1.png)

O **TNS Service Name** oferecido aqui vem do `tnsnames.ora` da sua instalação do Oracle Client —
é lá que o alias e, com ele, o host, a porta e o service name são definidos. No *digna*, você
pode usar o alias como `DBQ` ou, em vez disso, o descriptor completo.

#### Passo 2 – Testar a Conexão

Clique no botão **Test Connection**.

![Passo 2](images/oracle/create_odbc_data_source_step2.png)

Informe a senha e clique no botão **OK**.

![Passo 3](images/oracle/create_odbc_data_source_step3.png)

Uma mensagem de sucesso confirma que o driver e as credenciais funcionam.