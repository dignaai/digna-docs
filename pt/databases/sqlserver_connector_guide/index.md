# Conector de Origem para MS SQL Server

Este guia descreve como configurar o *digna* para se conectar ao Microsoft SQL Server via
**ODBC**, usando uma connection string **sem DSN**.

O lado do *digna* na configuração é o mesmo para todas as tecnologias — onde as conexões são
criadas, como os valores das propriedades são criptografados, como uma conexão é testada e o que
significam os modos de perfilamento. Isso está descrito na
[Visão Geral das Conexões de Banco de Dados](overview.md). Esta página cobre o que é específico
do SQL Server.

!!! note "Azure Synapse Analytics"

    O Synapse também é configurado como uma conexão SQL Server, com um nome de host diferente e
    algumas considerações adicionais — veja [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Instalar o Driver ODBC {: #1-install-the-odbc-driver }

Instale o **ODBC Driver 18 for SQL Server** na máquina que executa o backend do *digna*,
seguindo o [guia de instalação da Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

O driver que acompanha o Windows com o nome simples **SQL Server** também funciona, mas está há
muito tempo obsoleto e não suporta nem configurações modernas de TLS nem autenticação do Azure.
Use-o apenas quando não for possível instalar o driver atual.

Leia no seu host o nome exato do driver registrado, conforme descrito em
[Instalar o Driver ODBC no Host do digna](overview.md#install-the-driver).

---

## 2. Propriedades ODBC {: #2-odbc-properties }

!!! important "Um exemplo, não uma especificação"

    O conjunto abaixo é uma combinação que comprovadamente funciona. As propriedades pertencem
    ao driver ODBC da Microsoft, portanto seus nomes, valores padrão e valores aceitos variam
    entre versões do driver — o Driver 18, por exemplo, criptografa por padrão, enquanto o
    Driver 17 não — e entre plataformas. Use isto como ponto de partida e consulte a
    documentação da versão do driver que você instalou.

Adicione as seguintes propriedades na tela **Add DB Connection**:

| Key | Valor de exemplo | Observações |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Deve corresponder ao nome do driver registrado no host do *digna* |
| `SERVER` | `sql.example.com` | Nome do servidor ou endereço IP. Instâncias nomeadas: `host\instance`; uma porta não padrão: `host,1433` |
| `PORT` | `1433` | Omita quando a porta já fizer parte de `SERVER` |
| `DATABASE` | `digna_source_db` | Banco de dados que contém os schemas de origem. É o único banco de dados que esta conexão pode perfilar |
| `UID` | `digna_source_user` | Usuário do banco de dados |
| `PWD` | `<password>` | Marque **Encrypted** |

A connection string resultante fica assim:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Criptografia com o ODBC Driver 18

O Driver 18 criptografa as conexões por padrão e valida o certificado do servidor. Contra um
servidor com um certificado em que o host do *digna* não confia — normalmente um certificado
autoassinado —, a conexão falha com um erro de cadeia de certificados. Adicione:

| Key | Valor de exemplo | Observações |
|---|---|---|
| `Encrypt` | `yes` | Padrão no Driver 18; defina como `no` apenas se o servidor não suportar TLS |
| `TrustServerCertificate` | `yes` | Ignora a validação do certificado. Prático em ambientes de teste; em produção, prefira instalar o certificado |

### Autenticação do Windows

Para se conectar com a conta que executa o serviço do *digna* em vez de um login SQL, remova
`UID` e `PWD` e adicione:

| Key | Valor de exemplo | Observações |
|---|---|---|
| `Trusted_Connection` | `yes` | A conta de serviço do *digna* precisa das permissões no banco de dados |

---

## 3. Configuração do *digna* {: #3-digna-configuration }

Na tela **Add DB Connection**, informe o seguinte:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Observações sobre o MS SQL Server {: #4-notes-on-ms-sql-server }

- **Uma conexão enxerga um banco de dados.** O *digna* oferece os schemas do banco de dados
  indicado em `DATABASE`, porque o SQL Server informa apenas o banco de dados atual como
  catálogo. Tabelas de origem em outro banco de dados precisam de uma conexão própria.
- **Modos de perfilamento.** *Permanent* cria as tabelas de trabalho em **Work Schema**, então o
  usuário precisa de `CREATE TABLE` ali. *Session* usa tabelas temporárias locais (`#wt_…`) no
  `tempdb` e não utiliza **Work Schema**. *Standard* precisa apenas de acesso de leitura.
- **`SERVER` inclui a instância e a porta.** Com uma instância nomeada, `host\instance` exige
  que o serviço SQL Server Browser esteja acessível; `host,port` evita isso.

---

## 5. Verificar o Driver (opcional) {: #5-verifying-the-driver-optional }

Configurar uma fonte de dados ODBC não é necessário para uma conexão sem DSN, mas o assistente
do próprio driver é uma forma prática de confirmar que o driver funciona e que o servidor
aceita suas credenciais antes de inseri-las no *digna*.

#### Passo 1
![Passo 1](images/sqlserver/create_odbc_data_source_step1.png)

Clique no botão **Next >**.

#### Passo 2
![Passo 2](images/sqlserver/create_odbc_data_source_step2.png)

Escolha o método de autenticação (por exemplo, nome de usuário e senha)
e informe os dados necessários.

Clique no botão **Next >**.

#### Passo 3
![Passo 3](images/sqlserver/create_odbc_data_source_step3.png)

Escolha as configurações compatíveis com ANSI e clique no botão **Next >**.

#### Passo 4
![Passo 4](images/sqlserver/create_odbc_data_source_step4.png)

Você pode manter as configurações padrão ou escolher as opções de log necessárias
e clicar no botão **Finish**.

#### Passo 5
![Passo 5](images/sqlserver/create_odbc_data_source_step5.png)

Agora clique no botão **Test datasource**.

#### Passo 6
![Passo 6](images/sqlserver/create_odbc_data_source_step6.png)

Uma tela de sucesso confirma que o driver e as credenciais funcionam. Os valores que você
inseriu são exatamente os valores que as propriedades da [seção 2](#2-odbc-properties) recebem.