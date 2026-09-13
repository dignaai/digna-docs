---
title: Connettore Apache Hive – Integrazione database | digna Documentazione
description: Configura digna per connettersi ad Apache Hive tramite ODBC con una stringa di connessione senza DSN. Copre il driver ODBC Cloudera per Hive, i meccanismi di autenticazione, le modalità di trasporto e le impostazioni di connessione lato digna.
image: /assets/logo_square.png
---


# Connettore sorgente per Hive

Questa guida descrive come configurare *digna* per connettersi ad Apache Hive tramite **ODBC**,
usando una stringa di connessione **senza DSN**.

La parte digna della configurazione è identica per ogni tecnologia: dove si creano le
connessioni, come vengono cifrati i valori delle proprietà, come si testa una connessione e cosa
significano le modalità di profilazione. È descritta in
[Panoramica delle connessioni ai database](overview.md). Questa pagina copre ciò che è specifico
di Hive.

---

## 1. Installare il driver ODBC {: #1-install-the-odbc-driver }

Installa il **Cloudera ODBC Driver for Apache Hive** sulla macchina che esegue il backend di
*digna*, seguendo la guida di installazione ufficiale del fornitore.

Leggi il nome esatto del driver registrato sul tuo host come descritto in
[Installare il driver ODBC sull'host digna](overview.md#install-the-driver).

---

## 2. Proprietà ODBC {: #2-odbc-properties }

!!! important "Un esempio, non una specifica"

    L'insieme qui sotto è una combinazione che è noto funzionare. Le proprietà appartengono al
    driver Cloudera per Hive, quindi i loro nomi, i valori predefiniti e i valori accettati
    variano tra versioni del driver e piattaforme, e ciò che HiveServer2 accetta dipende
    interamente da come è protetto il cluster: meccanismo di autenticazione, modalità di
    trasporto, TLS, gateway. Usalo come punto di partenza e consulta la documentazione della
    versione del driver che hai installato.

Aggiungi le seguenti proprietà nella schermata **Add DB Connection**:

| Chiave | Valore di esempio | Note |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Deve corrispondere al nome del driver registrato sull'host *digna* |
| `HOST` | `hive.example.com` | Nome host o indirizzo IP di HiveServer2 |
| `PORT` | `10000` | Porta di HiveServer2; `10001` per il trasporto HTTP |

La stringa di connessione risultante è simile a questa:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Autenticazione

Un HiveServer2 non protetto accetta le tre proprietà qui sopra così come sono. Dove
l'autenticazione è attiva, aggiungi:

| Chiave | Valore di esempio | Note |
|---|---|---|
| `AuthMech` | `3` | `0` nessuna autenticazione, `2` solo nome utente, `3` nome utente e password, `1` Kerberos |
| `UID` | `digna_source_user` | Necessario per `AuthMech` `2` e `3` |
| `PWD` | `<password>` | Necessario per `AuthMech` `3`. Spunta **Encrypted** |

Per Kerberos (`AuthMech=1`), l'host *digna* ha bisogno inoltre di un ticket o di un keytab
valido, oltre alle proprietà `KrbHostFQDN`, `KrbServiceName` e `KrbRealm` documentate dal driver.

### Trasporto e TLS

| Chiave | Valore di esempio | Note |
|---|---|---|
| `ThriftTransport` | `2` | `0` binario (predefinito, porta 10000), `1` SASL, `2` HTTP (porta 10001, ed è ciò che si aspetta un gateway Knox) |
| `HTTPPath` | `cliservice` | Con `ThriftTransport=2` |
| `SSL` | `1` | Dove HiveServer2 è protetto con TLS |
| `Schema` | `dignadata` | Database Hive in cui la sessione inizia. Facoltativo: *digna* qualifica le proprie query |

---

## 3. Configurazione di *digna* {: #3-digna-configuration }

Nella schermata **Add DB Connection**, indica quanto segue:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Note su Hive {: #4-notes-on-hive }

- **I cataloghi vengono dal driver.** Hive non ha un catalogo proprio, quindi *digna* prende ciò
  che il driver segnala — normalmente una sola voce chiamata `HIVE` — ed elenca i database Hive
  come schemi al di sotto.
- **Work Schema è un database Hive.** Per la profilazione *Permanent*, l'utente deve avere il
  diritto di creare ed eliminare tabelle al suo interno, e la posizione di archiviazione
  sottostante deve essere scrivibile.
- **Modalità di profilazione.** *Permanent* crea le tabelle di lavoro in **Work Schema**.
  *Session* usa `CREATE TEMPORARY TABLE`, che richiede un HiveServer2 con supporto per le
  tabelle temporanee, e non tocca **Work Schema**. *Standard* richiede solo accesso in lettura,
  ed è la modalità da scegliere su un cluster in cui *digna* non ha alcun accesso in scrittura.
- **La profilazione è un insieme di query, non una scansione.** Ogni statistica è calcolata da
  HiveServer2, quindi la coda a cui invia l'utente di *digna* deve avere capacità sufficiente
  per la finestra di ispezione.

---

## 5. Verificare il driver (facoltativo) {: #5-verifying-the-driver-optional }

Configurare un'origine dati ODBC non è necessario per una connessione senza DSN, ma la finestra
di dialogo del driver è un modo comodo per confermare che il driver, la modalità di trasporto e
le tue credenziali funzionano prima di inserirli in *digna*.

#### Passo 1
![Step 1](images/hive/create_odbc_data_source_step1.png)

I campi **Host**, **Port**, **Database**, **Mechanism** e **Thrift Transport** corrispondono qui
alle proprietà `HOST`, `PORT`, `Schema`, `AuthMech` e `ThriftTransport` della
[sezione 2](#2-odbc-properties).

#### Passo 2 – Testare la connessione

Indica la password e fai clic sul pulsante **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Dopo un test riuscito, fai clic sul pulsante **OK**.
