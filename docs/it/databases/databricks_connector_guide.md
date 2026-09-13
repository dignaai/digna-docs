---
title: Connettore Databricks – Integrazione database | digna Documentazione
description: Configura digna per connettersi a Databricks con Unity Catalog tramite ODBC e una stringa di connessione senza DSN. Copre il driver ODBC di Databricks, i token di accesso personale, il percorso HTTP e le impostazioni di connessione lato digna.
image: /assets/logo_square.png
---

# Connettore sorgente per Databricks

Questa guida descrive come configurare *digna* per connettersi a Databricks tramite **ODBC**,
usando una stringa di connessione **senza DSN**.

La parte digna della configurazione è identica per ogni tecnologia: dove si creano le
connessioni, come vengono cifrati i valori delle proprietà, come si testa una connessione e cosa
significano le modalità di profilazione. È descritta in
[Panoramica delle connessioni ai database](overview.md). Questa pagina copre ciò che è specifico
di Databricks.

!!! note "Unity Catalog è obbligatorio"

    *digna* legge i cataloghi disponibili da `system.information_schema.catalogs`, quindi il
    workspace deve avere Unity Catalog abilitato. Le versioni precedenti di *digna* offrivano
    una tecnologia separata «Databricks Legacy» per i workspace senza Unity Catalog; non è più
    disponibile.

---

## 1. Installare il driver ODBC {: #1-install-the-odbc-driver }

Installa il **Databricks ODBC Driver** sulla macchina che esegue il backend di *digna*, seguendo
[la guida di installazione di Databricks](https://docs.databricks.com/aws/en/integrations/odbc/).

A seconda della versione, il driver si registra come **Simba Spark ODBC Driver** oppure come
**Databricks ODBC Driver**. Leggi il nome esatto registrato sul tuo host come descritto in
[Installare il driver ODBC sull'host digna](overview.md#install-the-driver).

---

## 2. Raccogliere i dati di connessione {: #2-gather-the-connection-details }

Tutti i valori provengono dal warehouse SQL (o dal cluster) che vuoi far usare a *digna*. Aprilo
nel workspace Databricks e vai in **Connection details**:

| Campo Databricks | Usato come |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, normalmente `443` |
| **HTTP path** | `HTTPPath` |

Per l'autenticazione, crea un **token di accesso personale** — vedi
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
I token appartengono a un utente o a un service principal, e quel principal ha bisogno di
`USE CATALOG`, `USE SCHEMA` e `SELECT` sui dati sorgente.

---

## 3. Proprietà ODBC {: #3-odbc-properties }

!!! important "Un esempio, non una specifica"

    L'insieme qui sotto è una combinazione che è noto funzionare. Le proprietà appartengono al
    driver Databricks/Simba, quindi i loro nomi, i valori predefiniti e i valori accettati
    variano tra versioni del driver — il driver è stato rinominato e le sue opzioni di
    autenticazione ampliate più di una volta — e tra piattaforme. Usalo come punto di partenza e
    consulta la documentazione della versione del driver che hai installato.

Aggiungi le seguenti proprietà nella schermata **Add DB Connection**:

| Chiave | Valore di esempio | Note |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Deve corrispondere al nome del driver registrato sull'host *digna* |
| `Host` | `<workspace>.cloud.databricks.com` | Nome host del server del warehouse, per es. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | Percorso HTTP del warehouse o del cluster |
| `SSL` | `1` | Gli endpoint Databricks sono solo TLS |
| `ThriftTransport` | `2` | Trasporto HTTP, che è quello parlato dagli endpoint SQL |
| `AuthMech` | `3` | Autenticazione tramite token |
| `UID` | `token` | La parola letterale `token`, non un nome utente |
| `PWD` | `dapi…` | Il token di accesso personale. Spunta **Encrypted** |
| `UseNativeQuery` | `1` | Passa l'SQL di *digna* senza modifiche — vedi sotto |

La stringa di connessione risultante è simile a questa:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Mantieni `UseNativeQuery=1`"

    Con `UseNativeQuery=0` — il valore predefinito del driver — il driver riscrive l'SQL in
    arrivo in quella che ritiene sintassi ODBC portabile. *digna* genera già SQL per Databricks,
    quindi la riscrittura può alterare l'uso dei backtick e i letterali di data, e la
    profilazione fallisce allora su istruzioni che sarebbero valide così come sono scritte.

### OAuth al posto di un token

Per un service principal con autenticazione OAuth machine-to-machine, sostituisci `AuthMech`,
`UID` e `PWD` con:

| Chiave | Valore di esempio | Note |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Credenziali client |
| `Auth_Client_ID` | `<application id>` | Service principal |
| `Auth_Client_Secret` | `<client secret>` | Spunta **Encrypted** |

---

## 4. Configurazione di *digna* {: #4-digna-configuration }

Nella schermata **Add DB Connection**, indica quanto segue:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Note su Databricks {: #5-notes-on-databricks }

- **Il warehouse deve essere in esecuzione**, o in grado di avviarsi, quando *digna* si connette.
  Un warehouse che riparte da uno stato arrestato può impiegare più del timeout di connessione:
  se il test fallisce al primo tentativo dopo un periodo di inattività, riprova.
- **I cataloghi vengono dal workspace.** A differenza della maggior parte delle tecnologie, una
  connessione Databricks raggiunge ogni catalogo che il principal è autorizzato a vedere, così
  che una sola connessione può servire sorgenti distribuite su più cataloghi.
- **Modalità di profilazione.** *Permanent* crea le tabelle di lavoro in **Work Schema**
  all'interno del catalogo della sorgente, quindi il principal ha bisogno di `CREATE TABLE` lì.
  *Session* usa `CREATE TEMPORARY TABLE` e non tocca **Work Schema**. *Standard* richiede solo
  accesso in lettura.
- **I warehouse serverless funzionano** allo stesso modo; cambia solo `HTTPPath`.

---

## 6. Verificare il driver (facoltativo) {: #6-verifying-the-driver-optional }

Configurare un'origine dati ODBC non è necessario per una connessione senza DSN, ma la finestra
di dialogo del driver è un modo comodo per confermare che il driver, il warehouse e il token
funzionano prima di inserirli in *digna*.

#### Passo 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Passo 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Passo 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Passo 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Passo 5 – Testare la connessione

Fai clic sul pulsante **TEST**. Una connessione riuscita dovrebbe apparire così:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

L'host, il percorso HTTP e il token inseriti qui sono esattamente i valori che assumono le
proprietà della [sezione 3](#3-odbc-properties).
