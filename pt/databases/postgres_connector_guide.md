# Conector de Origem para PostgreSQL

Este guia descreve como configurar o *digna* para se conectar ao PostgreSQL via **ODBC**, usando
uma connection string **sem DSN**.

O lado do *digna* na configuração é o mesmo para todas as tecnologias — onde as conexões são
criadas, como os valores das propriedades são criptografados, como uma conexão é testada e o que
significam os modos de perfilamento. Isso está descrito na
[Visão Geral das Conexões de Banco de Dados](overview.md). Esta página cobre o que é específico
do PostgreSQL.

---

## 1. Instalar o Driver ODBC {: #1-install-the-odbc-driver }

Instale o driver ODBC do PostgreSQL (**psqlODBC**) na máquina que executa o backend do
*digna*, seguindo o guia de instalação oficial do fornecedor.

O driver se registra com um nome que varia conforme a plataforma e o pacote — geralmente
**PostgreSQL Unicode(x64)** no Windows e **PostgreSQL ODBC Driver(UNICODE)** no Linux. Leia no
seu host o nome exato, conforme descrito em
[Instalar o Driver ODBC no Host do digna](overview.md#install-the-driver), e use esse nome na
propriedade `DRIVER` abaixo.

---

## 2. Propriedades ODBC {: #2-odbc-properties }

!!! important "Um exemplo, não uma especificação"

    O conjunto abaixo é uma combinação que comprovadamente funciona. As propriedades pertencem
    ao driver psqlODBC, portanto seus nomes, valores padrão e valores aceitos variam entre
    versões do driver e plataformas, e o que o seu servidor exige — SSL em particular — também
    pode variar. Use isto como ponto de partida e consulte a documentação da versão do driver
    que você instalou.

Adicione as seguintes propriedades na tela **Add DB Connection**:

| Key | Valor de exemplo | Observações |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Deve corresponder ao nome do driver registrado no host do *digna* |
| `SERVER` | `db.example.com` | Nome do servidor ou endereço IP |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Banco de dados que contém os schemas de origem. É o único banco de dados que esta conexão pode perfilar |
| `UID` | `digna_source_user` | Usuário do banco de dados |
| `PWD` | `<password>` | Marque **Encrypted** |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` ou `verify-full` — deve ser aceito pelo servidor |

A connection string resultante fica assim:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Qualquer outra opção do psqlODBC pode ser adicionada como propriedade adicional — por exemplo,
`ReadOnly=1` para uma sessão somente leitura, ou `ConnSettings` para executar instruções `SET`
no momento da conexão.

---

## 3. Configuração do *digna* {: #3-digna-configuration }

Na tela **Add DB Connection**, informe o seguinte:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Observações sobre o PostgreSQL {: #4-notes-on-postgresql }

- **`SSLMode` deve corresponder ao servidor.** Um servidor configurado com `hostssl` rejeita
  `SSLMode=disable`, e `verify-ca` ou `verify-full` também exigem que o certificado raiz esteja
  disponível para o driver no host do *digna*. Se você teve que escolher um modo específico ao
  testar o driver, use o mesmo aqui.
- **Uma conexão enxerga um banco de dados.** O *digna* oferece os schemas do banco de dados
  indicado em `DATABASE`, porque o PostgreSQL informa apenas o banco de dados atual como
  catálogo. Tabelas de origem em outro banco de dados precisam de uma conexão própria.
- **Modos de perfilamento.** *Permanent* cria as tabelas de trabalho em **Work Schema**, então o
  usuário precisa de `CREATE` nesse schema. *Session* usa `CREATE TEMPORARY TABLE` e não utiliza
  **Work Schema**. *Standard* precisa apenas de acesso de leitura.

---

## 5. Verificar o Driver (opcional) {: #5-verifying-the-driver-optional }

Configurar uma fonte de dados ODBC não é necessário para uma conexão sem DSN, mas o diálogo do
próprio driver é uma forma prática de confirmar que o driver funciona e que o servidor aceita
suas credenciais e o modo SSL antes de inseri-los no *digna*.

#### Passo 1
![Passo 1](images/postgres/create_odbc_data_source_step1.png)

#### Passo 2 – Testar a Conexão

Clique no botão **Test Connection**.

![Passo 2](images/postgres/create_odbc_data_source_step2.png)

Os valores que você inseriu aqui são exatamente os valores que as propriedades da
[seção 2](#2-odbc-properties) recebem.