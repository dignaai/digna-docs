# Conector de Origem para Azure Synapse Analytics

Este guia descreve como configurar o *digna* para se conectar ao Azure Synapse Analytics via
**ODBC**, usando uma connection string **sem DSN**. Tanto pools SQL serverless quanto dedicados
são suportados.

O lado do *digna* na configuração é o mesmo para todas as tecnologias — onde as conexões são
criadas, como os valores das propriedades são criptografados, como uma conexão é testada e o que
significam os modos de perfilamento. Isso está descrito na
[Visão Geral das Conexões de Banco de Dados](overview.md). Esta página cobre o que é específico
do Azure Synapse.

!!! note "Tecnologia"

    O Synapse usa o dialeto do SQL Server, então a conexão é criada com **Technology:
    SQL Server**. Veja [MS SQL Server](sqlserver_connector_guide.md) para um servidor
    on-premises.

---

## 1. Instalar o Driver ODBC {: #1-install-the-odbc-driver }

Instale o **ODBC Driver 18 for SQL Server** na máquina que executa o backend do *digna*,
seguindo o [guia de instalação da Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server),
e leia no seu host o nome exato do driver registrado, conforme descrito em
[Instalar o Driver ODBC no Host do digna](overview.md#install-the-driver).

---

## 2. Propriedades ODBC {: #2-odbc-properties }

!!! important "Um exemplo, não uma especificação"

    O conjunto abaixo é uma combinação que comprovadamente funciona. As propriedades pertencem
    ao driver ODBC da Microsoft, portanto seus nomes, valores padrão e valores aceitos variam
    entre versões do driver e plataformas, e o que o workspace exige depende de como ele está
    configurado — tipo de pool, método de autenticação, firewall. Use isto como ponto de
    partida e consulte a documentação da versão do driver que você instalou.

Adicione as seguintes propriedades na tela **Add DB Connection**:

| Key | Valor de exemplo | Observações |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Deve corresponder ao nome do driver registrado no host do *digna* |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Nome do workspace mais o sufixo do endpoint — veja abaixo |
| `DATABASE` | `dignadata` | Banco de dados que contém os schemas de origem. É o único banco de dados que esta conexão pode perfilar |
| `UID` | `sqladminuser` | Login SQL |
| `PWD` | `<password>` | Marque **Encrypted** |

A connection string resultante fica assim:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### O Valor de `SERVER`

Pegue o nome do workspace do Synapse e acrescente o sufixo do endpoint:

| Pool | `SERVER` |
|---|---|
| **Pool SQL serverless** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Pool SQL dedicado** | `<workspace>.sql.azuresynapse.net` |

!!! warning "É fácil esquecer a parte `-ondemand`"

    Sem ela, o nome é resolvido para o endpoint dedicado, e a conexão falha ou acessa
    silenciosamente um pool diferente do pretendido. Ambos os endpoints são exibidos na página
    de visão geral do workspace no portal do Azure.

### Firewall

O firewall do workspace do Synapse deve permitir o endereço de saída do host do *digna*.
Adicione-o em **Networking** no workspace antes de testar a conexão — um endereço bloqueado
aparece como timeout de conexão, e não como erro de autenticação.

### Autenticação com Microsoft Entra ID

Em vez de um login SQL, o driver pode se autenticar no Entra ID. Substitua `UID`/`PWD` pelo
método de autenticação que o seu workspace espera, por exemplo:

| Key | Valor de exemplo | Observações |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | `UID` passa a receber o ID do aplicativo (cliente) e `PWD` o client secret |
| `Authentication` | `ActiveDirectoryMSI` | Identidade gerenciada do host do *digna*, sem necessidade de credenciais |

---

## 3. Configuração do *digna* {: #3-digna-configuration }

Na tela **Add DB Connection**, informe o seguinte:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Observações sobre o Azure Synapse {: #4-notes-on-azure-synapse }

- **Pools serverless suportam apenas o perfilamento *Standard*.** Um pool SQL serverless não
  pode criar tabelas em um banco de dados, então nem o perfilamento *Permanent* nem o *Session*
  podem ser executados. *Standard* calcula as métricas diretamente na origem, o que também é a
  opção mais barata, já que o serverless é cobrado por volume de dados processados.
- **Uma conexão enxerga um banco de dados.** O *digna* oferece os schemas do banco de dados
  indicado em `DATABASE`, porque o Synapse, assim como o SQL Server, informa apenas o banco de
  dados atual como catálogo.
- **A criptografia vem ativada por padrão** no Driver 18, e os endpoints do Synapse apresentam
  certificados públicos válidos, portanto nenhuma propriedade `Encrypt` ou
  `TrustServerCertificate` é necessária.
- **Um endpoint serverless pode estar sendo retomado após inatividade** na primeira conexão. Se
  o teste de conexão expirar em um pool que ficou sem uso por algum tempo, tente novamente.

---

## 5. Verificar o Driver (opcional) {: #5-verifying-the-driver-optional }

Configurar uma fonte de dados ODBC não é necessário para uma conexão sem DSN, mas o assistente
do próprio driver é uma forma prática de confirmar que o driver funciona e que o workspace
aceita suas credenciais antes de inseri-las no *digna*.

#### Passo 1
![Passo 1](images/azure_synapse/create_odbc_data_source_step1.png)

Preencha o campo "Server".
Use o nome do workspace do Synapse e acrescente ".sql.azuresynapse.net".  
**Atenção**: se você quiser se conectar usando um pool SQL serverless, não deixe de incluir
"-ondemand", como mostrado na captura de tela acima.

Clique no botão **Next >**.

#### Passo 2
![Passo 2](images/azure_synapse/create_odbc_data_source_step2.png)

Escolha o método de autenticação (por exemplo, nome de usuário e senha)
e informe os dados necessários.

Clique no botão **Next >**.

#### Passo 3
![Passo 3](images/azure_synapse/create_odbc_data_source_step3.png)

Escolha as configurações compatíveis com ANSI e clique no botão **Next >**.

#### Passo 4
![Passo 4](images/azure_synapse/create_odbc_data_source_step4.png)

Você pode manter as configurações padrão ou escolher as opções necessárias
e clicar no botão **Finish**.

#### Passo 5
![Passo 5](images/azure_synapse/create_odbc_data_source_step5.png)

Agora clique no botão **Test datasource**.

#### Passo 6
![Passo 6](images/azure_synapse/create_odbc_data_source_step6.png)

Uma tela de sucesso confirma que o driver, o endpoint e as credenciais funcionam. Os valores
que você inseriu são exatamente os valores que as propriedades da [seção 2](#2-odbc-properties)
recebem.