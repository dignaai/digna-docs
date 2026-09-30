---
title: Visão Geral das Conexões de Banco de Dados – Configuração ODBC sem DSN | Documentação digna
description: Como as conexões de banco de dados funcionam no digna. Toda tecnologia de origem é acessada via ODBC com uma connection string sem DSN, construída a partir de propriedades ODBC. Abrange a instalação do driver no host do digna, a tela Add DB Connection, a criptografia de propriedades, o teste de conexão, a resolução de problemas e links para os guias por tecnologia.
image: /assets/logo_square.png
keywords:
  - conexão de banco de dados digna
  - odbc sem dsn
  - connection string odbc
  - configuração do driver odbc
  - unixodbc
  - propriedades odbc
  - configuração de fonte de dados
lang: pt
robots: index, follow
og_title: Conexões de Banco de Dados do digna – Configuração ODBC sem DSN
og_description: Configure uma conexão de origem do digna via ODBC sem DSN. Instalação do driver, propriedades ODBC, criptografia, testes e resolução de problemas.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Visão Geral das Conexões de Banco de Dados

---

## Sumário

1. [Como as Conexões Funcionam](#how-connections-work)
2. [Guias por Tecnologia](#technology-guides)
3. [Pré-requisito: Instalar o Driver ODBC no Host do digna](#install-the-driver)
4. [Criar uma Conexão de Banco de Dados](#create-a-database-connection)
5. [Propriedades ODBC](#odbc-properties)
6. [Criptografar Valores de Propriedades](#encrypting-property-values)
7. [Testar uma Conexão](#testing-a-connection)
8. [Qual Banco de Dados a Conexão Enxerga](#which-database-the-connection-sees)
9. [Modo de Perfilamento e Work Schema](#profiling-mode-and-work-schema)
10. [Usar um DSN](#using-a-dsn-instead)
11. [Resolução de Problemas](#troubleshooting)

---

## Como as Conexões Funcionam {: #how-connections-work }

O *digna* acessa todas as tecnologias de origem via **ODBC**. Uma conexão é uma lista de
propriedades ODBC que você insere como pares chave/valor. Quando o *digna* abre a conexão, ele
junta esses pares em uma connection string — `Key=Value`, separados por `;`, na ordem em que
você os listou — e a entrega ao gerenciador de drivers ODBC no host do *digna*.

É o fato de você mesmo inserir as propriedades que torna a configuração **sem DSN**: a conexão
carrega tudo o que o driver precisa, portanto nenhuma fonte de dados ODBC (DSN) precisa ser
registrada no host. Essa é a forma recomendada de configurar o *digna*, porque a definição da
conexão fica inteiramente no *digna* e se move junto com ele.

### Por Que ODBC {: #why-odbc }

Releases anteriores ofereciam a escolha entre um driver específico por tecnologia e ODBC,
selecionada com uma chave **Use ODBC**. A partir do Release 2026.06, o *digna* se baseia apenas
em ODBC. Uma interface única e padronizada oferece mais do que um conjunto de drivers sob
medida:

- **Autenticação** — a autenticação faz parte do ODBC, então uma conexão pode usar tudo o que o
  seu driver suporta: senhas, tokens e PATs, Kerberos e Active Directory, MFA e single sign-on
  pelo navegador, identidade em nuvem, certificados de cliente e TLS. Novos métodos chegam com
  uma atualização do driver, sem esperar por um release do *digna*.
- **Drivers mantidos pelos fornecedores dos bancos de dados** — o driver do próprio fornecedor
  acompanha novas versões do servidor e correções de segurança, e você pode atualizá-lo no seu
  próprio ritmo, independentemente do *digna*.
- **Uma única forma de configurar tudo** — toda tecnologia é uma lista de propriedades
  chave/valor, com a mesma interface, a mesma criptografia de valores sensíveis e a mesma
  resolução de problemas, em vez de um conjunto diferente de campos para cada origem.
- **Ajuste fino e alcance** — opções no nível do driver, como timeouts, configurações de TLS,
  proxies e tamanhos de fetch, estão disponíveis para todas as origens, e qualquer tecnologia com
  um driver ODBC compatível pode ser conectada, incluindo aquelas para as quais o *digna* não
  publica um guia dedicado.

!!! note "O que mudou na interface"

    A chave **Use ODBC** e os campos separados de host, porta, banco de dados, usuário e senha
    não existem mais. Uma conexão que ainda não usa ODBC precisa ter suas propriedades ODBC
    inseridas antes de voltar a funcionar — veja
    [Criar uma Conexão de Banco de Dados](#create-a-database-connection).

---

## Guias por Tecnologia {: #technology-guides }

Os nomes das propriedades diferem de driver para driver, e cada tecnologia tem um ou dois
detalhes que as outras não têm. Os guias abaixo cobrem essa parte; esta página cobre o lado do
*digna*, que é o mesmo para todas elas.

!!! important "Os conjuntos de propriedades dos guias são exemplos"

    Cada guia mostra uma combinação que comprovadamente funciona — aquela com a qual o *digna* é
    testado. É um ponto de partida, não uma especificação: as propriedades pertencem ao driver
    ODBC, e quais existem, como se chamam e quais valores aceitam varia entre versões e
    fornecedores de drivers, entre Windows, Linux e macOS, e conforme a configuração do servidor
    de origem — método de autenticação, TLS, gateway, porta. Conte com a necessidade de ajustar
    um ou dois valores e considere a documentação da versão do driver que você instalou como a
    referência oficial.

| Tecnologia | Guia | Vale a pena saber |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Pools serverless precisam de `-ondemand` no nome do host e suportam apenas o perfilamento *Standard* |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Autenticação por token: `UID=token`, PAT em `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Os catálogos vêm do driver, não de uma consulta |
| **Netezza** | [Netezza](netezza_connector_guide.md) | O nome do driver fica entre chaves: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` aceita um connect descriptor completo ou um alias do `tnsnames.ora` |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` deve corresponder ao que o servidor exige |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | O programmatic access token é o caminho de autenticação testado |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` define quais schemas o *digna* pode ver |
| **Teradata** | [Teradata](teradata_connector_guide.md) | O host vai em `DBCNAME`; os bancos de dados funcionam como schemas |

---

## Pré-requisito: Instalar o Driver ODBC no Host do digna {: #install-the-driver }

O *digna* abre as conexões de origem a partir do **servidor que executa o backend do digna**, e
não a partir do navegador. Portanto, o driver ODBC deve estar instalado nessa máquina, e seu
nome deve estar registrado no gerenciador de drivers local.

=== "Windows"

    Instale o driver de 64 bits do fornecedor, depois abra o **ODBC Data Source Administrator
    (64-bit)** e mude para a aba **Drivers**. Os nomes listados ali são exatamente os valores
    que você pode usar na propriedade `Driver`.

=== "Linux"

    Instale o **unixODBC** e o driver do fornecedor, depois liste os nomes de drivers
    registrados:

    ```bash
    odbcinst -q -d
    ```

    Os nomes exibidos entre colchetes são os valores que você pode usar na propriedade `Driver`.
    Eles vêm de `/etc/odbcinst.ini` (ou do arquivo indicado por `odbcinst -j`).

=== "macOS"

    Instale o **unixODBC** (por exemplo, com `brew install unixodbc`) e o driver do fornecedor,
    depois liste os nomes de drivers registrados:

    ```bash
    odbcinst -q -d
    ```

!!! warning "O nome do driver deve corresponder caractere por caractere"

    `Driver` é repassado ao gerenciador de drivers sem alterações. `Simba Spark ODBC Driver` e
    `Simba Spark ODBC Driver 64` são drivers diferentes para o gerenciador de drivers, e um nome
    que não está registrado produz um erro *data source name not found*, mesmo que nenhum DSN
    esteja envolvido.

Em vez de um nome registrado, todos os gerenciadores de drivers comuns também aceitam o caminho
completo para a biblioteca do driver, por exemplo
`Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. Isso é útil quando o driver está
instalado, mas não registrado.

---

## Criar uma Conexão de Banco de Dados {: #create-a-database-connection }

Abra o **Admin Panel**, vá para a aba **Database Connections** e clique em
**Add DB Connection**. A tela pede cinco informações:

| Campo | Descrição |
|---|---|
| **Name** | Nome da conexão. É usado para referenciar a conexão em outras telas. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake ou Hive. Define o dialeto SQL que o *digna* gera, portanto deve corresponder à origem — não ao driver. O Azure Synapse Analytics é uma conexão **SQL Server**. |
| **ODBC Properties** | Os pares chave/valor descritos em [Propriedades ODBC](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* ou *Session* — veja [Modo de Perfilamento e Work Schema](#profiling-mode-and-work-schema). |
| **Work Schema** | Schema que contém as tabelas de trabalho do perfilamento *Permanent*. |

Uma conexão é administrada centralmente e depois atribuída a um ou mais projetos, de modo que a
mesma conexão pode atender a vários projetos.

---

## Propriedades ODBC {: #odbc-properties }

Clique em **Add Property** para cada propriedade e preencha **Key**, **Value** e, para
segredos, a caixa de seleção **Encrypted**. Cada guia por tecnologia lista um conjunto de
exemplo para aquela tecnologia, que você adapta à versão do seu driver e ao seu servidor — veja
[a nota acima](#technology-guides).

Seja qual for o driver, um conjunto de propriedades cobre as mesmas quatro coisas:

- **`Driver`** — o nome registrado do driver, conforme descrito [acima](#install-the-driver).
- **O endereço do servidor** — a chave difere por driver: `SERVER`, `HOST`, `DBCNAME`,
  `Server` ou, no Oracle, o connect descriptor `DBQ`.
- **Credenciais** — geralmente `UID` e `PWD`; o Snowflake usa `UID` mais um `token`, e o
  Databricks usa o usuário literal `token` mais o personal access token em `PWD`.
- **O banco de dados ou catálogo de trabalho**, quando a tecnologia tem um — veja
  [Qual Banco de Dados a Conexão Enxerga](#which-database-the-connection-sees).

Qualquer outra opção documentada pelo driver pode ser adicionada da mesma forma — pool de
conexões, timeouts de socket, configurações de Kerberos, configurações de proxy. O *digna* não
interpreta as propriedades; apenas as repassa.

!!! warning "Os valores não são escapados — coloque entre chaves tudo o que tiver ponto e vírgula"

    Como as propriedades são unidas com `;`, um valor que contenha `;` dividiria a connection
    string no lugar errado. Coloque esses valores entre chaves: `PWD={p@ss;word}`.
    O mesmo vale para valores com `=` ou com espaços iniciais. É também por isso que alguns
    drivers costumam ser escritos entre chaves, como em `{NetezzaSQL}` ou
    `{SnowflakeDSIIDriver}`.

---

## Criptografar Valores de Propriedades {: #encrypting-property-values }

Marque **Encrypted** para toda propriedade que contenha um segredo — `PWD`, `token`, um client
secret. O valor é então criptografado antes de ser armazenado no repositório do *digna*,
mascarado na tela e descriptografado apenas quando a connection string é montada.

!!! tip "Dica"

    Um valor criptografado não pode ser lido de volta, nem na interface nem pela API — ele só
    pode ser substituído. Guarde os segredos também no seu próprio gerenciador de senhas.

Propriedades que não são secretas — o nome do driver, o host, a porta, o banco de dados — é
melhor deixar sem criptografia, para que continuem legíveis para quem mantiver a conexão
depois.

---

## Testar uma Conexão {: #testing-a-connection }

Clique em **Test** no diálogo *Add DB Connection* **antes** de salvar. O teste usa os valores
que estão no formulário no momento e faz uma conexão real, portanto relata exatamente o que uma
inspeção encontraria — um nome de driver errado, uma senha rejeitada, um host inacessível. Nada
é armazenado: a conexão de teste é revertida, quer tenha sucesso ou falhe.

Para uma conexão que já existe, passe o mouse sobre a linha dela na aba
**Database Connections** e clique no ícone de **plugue** para testá-la novamente. Essa é a
forma mais rápida de verificar se uma origem está acessível após uma troca de senha ou uma
alteração no firewall.

---

## Qual Banco de Dados a Conexão Enxerga {: #which-database-the-connection-sees }

Quando você adiciona uma fonte de dados, o *digna* oferece os catálogos, schemas e tabelas que a
conexão consegue alcançar. Até onde isso vai depende da tecnologia:

| Tecnologia | Catálogos oferecidos |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Apenas o banco de dados **atual** da conexão |
| **Teradata**, **Netezza**, **Databricks** | Todos os bancos de dados ou catálogos que o usuário tem permissão para ver |
| **Hive**, **Impala** | Informados pelo driver |

!!! important "Uma conexão, um banco de dados"

    Para PostgreSQL, SQL Server, Oracle e Snowflake, as propriedades devem apontar para o banco
    de dados que contém os schemas de origem — `DATABASE=…`, `Database=…` ou o service name
    dentro do `DBQ` do Oracle. Tabelas em outro banco de dados não são acessíveis por essa
    conexão; adicione uma segunda conexão para ele.

---

## Modo de Perfilamento e Work Schema {: #profiling-mode-and-work-schema }

O modo de perfilamento determina como o *digna* processa os dados e calcula as métricas:

- **Standard:** as métricas são calculadas diretamente nas tabelas de origem, sem copiar os
  dados.
- **Permanent:** os dados do dia inspecionado são copiados para uma tabela permanente, e as
  métricas são calculadas sobre os dados copiados.
- **Session:** os dados são copiados para uma tabela de sessão ou temporária, e as métricas são
  calculadas sobre esses dados temporários.

O modo define o que o usuário da conexão precisa ter permissão para fazer:

| Modo | Grava | Permissões necessárias para o usuário da conexão |
|---|---|---|
| **Standard** | nada | Leitura nas tabelas de origem |
| **Permanent** | uma tabela por fonte de dados em **Work Schema** | Criar e excluir tabelas em **Work Schema** |
| **Session** | uma tabela temporária que o banco de dados exclui junto com a sessão | Criar tabelas temporárias — **Work Schema** não é usado |

*Standard* apenas lê, o que o torna o modo a escolher quando o *digna* recebe acesso somente
leitura. **Work Schema** só é lido no modo *Permanent*, mas vale a pena preenchê-lo mesmo assim,
para que a conexão continue funcionando se o modo for alterado depois.

---

## Usar um DSN {: #using-a-dsn-instead }

Um DSN continua funcionando — `DSN` é apenas mais uma propriedade:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

O DSN deve estar registrado no host do *digna*, para a mesma conta de usuário que executa o
backend do *digna*, e como **System DSN** quando o *digna* é executado como serviço. Tudo o que
está configurado no DSN também pode ser sobrescrito adicionando-o como propriedade.

Sem DSN é o padrão documentado porque evita esse estado no host: a conexão fica totalmente
descrita no *digna*, e um novo host do *digna* precisa do driver instalado, mas de nada
configurado.

---

## Resolução de Problemas {: #troubleshooting }

### Data source name not found / no default driver specified

**Sintomas:**
- O botão **Test** relata um erro mencionando *data source name not found*, mesmo que a
  configuração seja sem DSN

**Causas e Soluções:**
1. O valor de `Driver` não corresponde a um nome de driver registrado — compare-o com a aba
   **Drivers** do *ODBC Data Source Administrator (64-bit)*, ou com `odbcinst -q -d`
2. O driver está instalado na sua estação de trabalho, mas não no host do *digna*
3. O driver é de 32 bits, enquanto o *digna* é de 64 bits — instale o driver de 64 bits
4. A propriedade `Driver` está totalmente ausente, e nenhum `DSN` foi informado
5. No Linux e no macOS, o driver está instalado, mas não registrado — informe o caminho
   completo para a biblioteca do driver ou registre-o em `odbcinst.ini`

---

### O teste de conexão expira

**Sintomas:**
- **Test** trava e depois falha após cerca de meio minuto

**Causas e Soluções:**
1. Host ou porta inacessível a partir do host do *digna* — verifique o firewall e, para origens
   em nuvem, a lista de IPs permitidos
2. O nome do host está correto, mas a porta pertence a outro serviço
3. A origem precisa de mais do que os 30 segundos padrão para aceitar uma conexão — aumente
   `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` na seção `[base]` de `config.toml` (`0` espera
   indefinidamente) e reinicie o backend
4. Um endpoint serverless está sendo retomado após inatividade — tente novamente e, se isso
   acontecer com frequência, aumente o timeout de login como acima

---

### A autenticação falha, embora as credenciais estejam corretas

**Sintomas:**
- O driver informa credenciais inválidas, mas o mesmo usuário funciona em outro cliente SQL

**Causas e Soluções:**
1. A senha contém `;` — coloque o valor entre chaves: `{p@ss;word}`
2. Um espaço no final foi copiado para o valor
3. O driver espera um mecanismo de autenticação específico — por exemplo, `AuthMech` para os
   drivers Hive e Databricks, ou `authenticator` para o Snowflake
4. O valor foi armazenado criptografado e depois editado — valores criptografados não podem ser
   lidos de volta, então insira novamente o segredo completo
5. Um token expirou — personal access tokens e programmatic access tokens são emitidos com uma
   data de expiração

---

### A tela de fonte de dados não oferece o banco de dados ou schema esperado

**Sintomas:**
- Catálogos, schemas ou tabelas estão faltando quando uma fonte de dados é adicionada

**Causas e Soluções:**
1. A conexão aponta para outro banco de dados — veja
   [Qual Banco de Dados a Conexão Enxerga](#which-database-the-connection-sees)
2. O usuário da conexão não tem permissão de leitura no schema ou no dicionário de dados
3. **Technology** não corresponde à origem, então o *digna* consulta o dicionário de dados errado
4. No Snowflake, nenhum warehouse padrão está atribuído ao usuário e nenhuma propriedade
   `Warehouse` foi informada, então as consultas de metadados não podem ser executadas

---

### O perfilamento falha, enquanto o teste de conexão é bem-sucedido

**Sintomas:**
- **Test** passa, mas uma inspeção falha quando as tabelas de trabalho são criadas

**Causas e Soluções:**
1. O perfilamento *Permanent* está selecionado e o usuário da conexão não pode criar tabelas em
   **Work Schema** — conceda as permissões ou mude para *Session* ou *Standard*
2. **Work Schema** está vazio ou indica um schema que não existe, enquanto o perfilamento
   *Permanent* está selecionado
3. O perfilamento *Session* está selecionado e o usuário da conexão não pode criar tabelas
   temporárias
4. Uma consulta de perfilamento demorada atinge o timeout de consulta — aumente
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` na seção `[base]` de `config.toml` (padrão de 3600
   segundos; `0` desativa o timeout)

---

## Boas Práticas

**FAÇA:**

- Instale e registre o driver no host do *digna* antes de configurar a conexão
- Marque **Encrypted** para toda senha e todo token
- Clique em **Test** antes de salvar e teste novamente após uma troca de senha
- Nomeie as conexões de acordo com a origem e o ambiente, por exemplo `sales_dwh_prod`
- Dê ao *digna* um usuário de banco de dados dedicado, somente leitura quando o perfilamento
  *Standard* for suficiente
- Mantenha uma conexão por banco de dados de origem e adicione uma segunda em vez de alterar a
  primeira

**NÃO FAÇA:**

- Armazenar segredos sem criptografia ou compartilhar um usuário de banco de dados entre o
  *digna* e outras ferramentas
- Usar um driver de 32 bits com uma instalação de 64 bits do *digna*
- Depender de um User DSN quando o *digna* é executado como serviço — ele não ficará visível
- Colocar em uma propriedade um valor que contenha `;` sem chaves
- Apontar **Work Schema** para um schema que contenha dados de origem

---

## Suporte

Precisa de ajuda com uma conexão de banco de dados?

- **E-mail:** support@digna.ai
- **Documentação:** https://docs.digna.ai
- **Site:** https://www.digna.ai

---

**Release:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
