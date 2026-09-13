# Connettore sorgente per Oracle

Questa guida descrive come configurare *digna* per connettersi a Oracle Database tramite
**ODBC**, usando una stringa di connessione **senza DSN**.

La parte digna della configurazione è identica per ogni tecnologia: dove si creano le
connessioni, come vengono cifrati i valori delle proprietà, come si testa una connessione e cosa
significano le modalità di profilazione. È descritta in
[Panoramica delle connessioni ai database](overview.md). Questa pagina copre ciò che è specifico
di Oracle.

---

## 1. Installare il driver ODBC {: #1-install-the-odbc-driver }

Il driver ODBC di Oracle fa parte del **client Oracle** (è sufficiente il pacchetto «ODBC» di
Instant Client). Installalo sulla macchina che esegue il backend di *digna*, seguendo la guida
di installazione ufficiale del fornitore.

Il driver si registra come **Oracle in `<OracleHomeName>`** — per esempio
`Oracle in OraDB21Home1` oppure `Oracle in instantclient_21_13`. Il nome della home varia da
installazione a installazione, quindi leggi il nome esatto sul tuo host come descritto in
[Installare il driver ODBC sull'host digna](overview.md#install-the-driver).

---

## 2. Proprietà ODBC {: #2-odbc-properties }

!!! important "Un esempio, non una specifica"

    L'insieme qui sotto è una combinazione che è noto funzionare. Le proprietà appartengono al
    driver ODBC di Oracle, quindi i loro nomi, i valori predefiniti e i valori accettati variano
    tra versioni del client, e il nome del driver in particolare dipende dalla home Oracle
    presente sul tuo host. Usalo come punto di partenza e consulta la documentazione della
    versione del client che hai installato.

Aggiungi le seguenti proprietà nella schermata **Add DB Connection**:

| Chiave | Valore di esempio | Note |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Deve corrispondere al nome del driver registrato sull'host *digna* |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Il database a cui connettersi — vedi sotto |
| `UID` | `DIGNA_SOURCE_USER` | Utente del database |
| `PWD` | `<password>` | Spunta **Encrypted** |

La stringa di connessione risultante è simile a questa:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### Il valore di `DBQ`

`DBQ` accetta tre forme. Per *digna* sono equivalenti; differiscono per ciò che deve essere
configurato sull'host *digna*:

| Forma | Esempio | Richiede |
|---|---|---|
| **Descrittore di connessione completo** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Nulla: tutto è nella proprietà. Consigliato |
| **Alias TNS** | `DIGNA_SOURCE` | L'alias deve esistere nel `tnsnames.ora` del client Oracle sull'host *digna* |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Un client Oracle che supporti Easy Connect (12c e successivi) |

!!! tip "Preferisci il descrittore completo"

    Un alias TNS sposta metà della definizione della connessione in un file sull'host *digna*,
    dove è facile dimenticarlo quando l'host viene ricostruito o *digna* viene spostato. Il
    descrittore completo mantiene la connessione autosufficiente — che è poi il senso di
    un'installazione senza DSN.

Nota che le parentesi di un descrittore non creano problemi all'interno di una stringa di
connessione, ma se la tua password contiene `;`, racchiudila tra parentesi graffe:
`PWD={p@ss;word}`.

---

## 3. Configurazione di *digna* {: #3-digna-configuration }

Nella schermata **Add DB Connection**, indica quanto segue:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Note su Oracle {: #4-notes-on-oracle }

- **Gli schemi sono utenti.** *digna* elenca gli utenti Oracle come schemi, quindi lo schema
  sorgente è il proprietario delle tabelle: `DIGNA_SOURCE_USER` nell'esempio qui sopra. L'utente
  della connessione ha bisogno di `SELECT` su quelle tabelle, direttamente o tramite un ruolo.
- **Una connessione vede un database.** Il catalogo offerto da *digna* è il database a cui la
  connessione è agganciata, quindi `DBQ` decide quale servizio, e perciò quale database, viene
  profilato.
- **Gli identificatori distinguono maiuscole e minuscole una volta tra virgolette.** *digna* mette
  tra virgolette i nomi che legge dal dizionario dati, cioè ciò che Oracle memorizza: maiuscolo
  per gli oggetti non tra virgolette.
- **Modalità di profilazione.** *Permanent* crea le tabelle di lavoro in **Work Schema**, quindi
  l'utente ha bisogno di `CREATE TABLE` lì e di una quota sul tablespace. *Session* usa una
  tabella temporanea privata (`ORA$PTT_…`, Oracle 18c e successivi) e non tocca **Work Schema**.
  *Standard* richiede solo accesso in lettura.

---

## 5. Verificare il driver (facoltativo) {: #5-verifying-the-driver-optional }

Configurare un'origine dati ODBC non è necessario per una connessione senza DSN, ma la finestra
di dialogo del driver è un modo comodo per confermare che il client Oracle, il nome del servizio
e le tue credenziali funzionano prima di inserirli in *digna*.

#### Passo 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Il **TNS Service Name** offerto qui proviene dal `tnsnames.ora` della tua installazione client
Oracle: è lì che sono definiti l'alias e, con esso, host, porta e nome del servizio. In *digna*
puoi usare l'alias come `DBQ`, oppure il descrittore completo.

#### Passo 2 – Testare la connessione

Fai clic sul pulsante **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Indica la password e fai clic sul pulsante **OK**.

![Step 3](images/oracle/create_odbc_data_source_step3.png)

Un messaggio di successo conferma che il driver e le credenziali funzionano.