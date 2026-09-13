# Connettore sorgente per MS SQL Server

Questa guida descrive come configurare *digna* per connettersi a Microsoft SQL Server tramite
**ODBC**, usando una stringa di connessione **senza DSN**.

La parte digna della configurazione è identica per ogni tecnologia: dove si creano le
connessioni, come vengono cifrati i valori delle proprietà, come si testa una connessione e cosa
significano le modalità di profilazione. È descritta in
[Panoramica delle connessioni ai database](overview.md). Questa pagina copre ciò che è specifico
di SQL Server.

!!! note "Azure Synapse Analytics"

    Anche Synapse si configura come una connessione SQL Server, con un nome host diverso e
    qualche considerazione in più — vedi [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Installare il driver ODBC {: #1-install-the-odbc-driver }

Installa **ODBC Driver 18 for SQL Server** sulla macchina che esegue il backend di *digna*,
seguendo [la guida di installazione di Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

Anche il driver distribuito con Windows sotto il nome semplice **SQL Server** funziona, ma è da
tempo superato e non supporta né le impostazioni TLS moderne né l'autenticazione Azure. Usalo
solo dove non è possibile installare il driver attuale.

Leggi il nome esatto del driver registrato sul tuo host come descritto in
[Installare il driver ODBC sull'host digna](overview.md#install-the-driver).

---

## 2. Proprietà ODBC {: #2-odbc-properties }

!!! important "Un esempio, non una specifica"

    L'insieme qui sotto è una combinazione che è noto funzionare. Le proprietà appartengono al
    driver ODBC Microsoft, quindi i loro nomi, i valori predefiniti e i valori accettati variano
    tra versioni del driver — Driver 18 cifra per impostazione predefinita, cosa che Driver 17
    non faceva — e tra piattaforme. Usalo come punto di partenza e consulta la documentazione
    della versione del driver che hai installato.

Aggiungi le seguenti proprietà nella schermata **Add DB Connection**:

| Chiave | Valore di esempio | Note |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Deve corrispondere al nome del driver registrato sull'host *digna* |
| `SERVER` | `sql.example.com` | Nome del server o indirizzo IP. Istanze denominate: `host\instance`; porta non predefinita: `host,1433` |
| `PORT` | `1433` | Ometti quando la porta fa già parte di `SERVER` |
| `DATABASE` | `digna_source_db` | Database che contiene gli schemi sorgente. È l'unico database che questa connessione può profilare |
| `UID` | `digna_source_user` | Utente del database |
| `PWD` | `<password>` | Spunta **Encrypted** |

La stringa di connessione risultante è simile a questa:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Cifratura con ODBC Driver 18

Driver 18 cifra le connessioni per impostazione predefinita e convalida il certificato del
server. Contro un server con un certificato di cui il tuo host *digna* non si fida —
tipicamente un certificato autofirmato — la connessione fallisce con un errore di catena di
certificati. Aggiungi:

| Chiave | Valore di esempio | Note |
|---|---|---|
| `Encrypt` | `yes` | Predefinito in Driver 18; imposta `no` solo se il server non supporta TLS |
| `TrustServerCertificate` | `yes` | Salta la convalida del certificato. Comodo negli ambienti di test; in produzione è preferibile installare il certificato |

### Autenticazione Windows

Per connetterti con l'account che esegue il servizio *digna* anziché con un login SQL, rimuovi
`UID` e `PWD` e aggiungi:

| Chiave | Valore di esempio | Note |
|---|---|---|
| `Trusted_Connection` | `yes` | L'account di servizio *digna* deve avere i diritti sul database |

---

## 3. Configurazione di *digna* {: #3-digna-configuration }

Nella schermata **Add DB Connection**, indica quanto segue:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Note su MS SQL Server {: #4-notes-on-ms-sql-server }

- **Una connessione vede un database.** *digna* offre gli schemi del database indicato in
  `DATABASE`, perché SQL Server segnala solo il database corrente come catalogo. Le tabelle
  sorgente in un altro database richiedono una connessione propria.
- **Modalità di profilazione.** *Permanent* crea le tabelle di lavoro in **Work Schema**, quindi
  l'utente ha bisogno di `CREATE TABLE` lì. *Session* usa tabelle temporanee locali (`#wt_…`) in
  `tempdb` e non tocca **Work Schema**. *Standard* richiede solo accesso in lettura.
- **`SERVER` porta con sé istanza e porta.** Con un'istanza denominata, `host\instance` richiede
  che il servizio SQL Server Browser sia raggiungibile; `host,port` lo evita.

---

## 5. Verificare il driver (facoltativo) {: #5-verifying-the-driver-optional }

Configurare un'origine dati ODBC non è necessario per una connessione senza DSN, ma la procedura
guidata del driver è un modo comodo per confermare che il driver funziona e che il server
accetta le tue credenziali prima di inserirle in *digna*.

#### Passo 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Fai clic sul pulsante **Next >**.

#### Passo 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Scegli il metodo di autenticazione (per es. nome utente e password)
e fornisci i dati richiesti.

Fai clic sul pulsante **Next >**.

#### Passo 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Scegli le impostazioni conformi ad ANSI, poi fai clic sul pulsante **Next >**.

#### Passo 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Puoi lasciare le impostazioni predefinite oppure scegliere le opzioni di registrazione secondo
le tue esigenze e fare clic sul pulsante **Finish**.

#### Passo 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Ora fai clic sul pulsante **Test datasource**.

#### Passo 6
![Step 6](images/sqlserver/create_odbc_data_source_step6.png)

Una schermata di successo conferma che il driver e le credenziali funzionano. I valori inseriti
sono esattamente quelli che assumono le proprietà della [sezione 2](#2-odbc-properties).