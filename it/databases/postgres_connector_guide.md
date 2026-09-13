# Connettore sorgente per PostgreSQL

Questa guida descrive come configurare *digna* per connettersi a PostgreSQL tramite **ODBC**,
usando una stringa di connessione **senza DSN**.

La parte digna della configurazione è identica per ogni tecnologia: dove si creano le
connessioni, come vengono cifrati i valori delle proprietà, come si testa una connessione e cosa
significano le modalità di profilazione. È descritta in
[Panoramica delle connessioni ai database](overview.md). Questa pagina copre ciò che è specifico
di PostgreSQL.

---

## 1. Installare il driver ODBC {: #1-install-the-odbc-driver }

Installa il driver ODBC di PostgreSQL (**psqlODBC**) sulla macchina che esegue il backend di
*digna*, seguendo la guida di installazione ufficiale del fornitore.

Il driver si registra con un nome che varia per piattaforma e pacchetto: di solito
**PostgreSQL Unicode(x64)** su Windows e **PostgreSQL ODBC Driver(UNICODE)** su Linux. Leggi il
nome esatto sul tuo host come descritto in
[Installare il driver ODBC sull'host digna](overview.md#install-the-driver), e usa quel nome per
la proprietà `DRIVER` qui sotto.

---

## 2. Proprietà ODBC {: #2-odbc-properties }

!!! important "Un esempio, non una specifica"

    L'insieme qui sotto è una combinazione che è noto funzionare. Le proprietà appartengono al
    driver psqlODBC, quindi i loro nomi, i valori predefiniti e i valori accettati variano tra
    versioni del driver e piattaforme, e anche ciò che il tuo server richiede — SSL in
    particolare — può essere diverso. Usalo come punto di partenza e consulta la documentazione
    della versione del driver che hai installato.

Aggiungi le seguenti proprietà nella schermata **Add DB Connection**:

| Chiave | Valore di esempio | Note |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Deve corrispondere al nome del driver registrato sull'host *digna* |
| `SERVER` | `db.example.com` | Nome del server o indirizzo IP |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Database che contiene gli schemi sorgente. È l'unico database che questa connessione può profilare |
| `UID` | `digna_source_user` | Utente del database |
| `PWD` | `<password>` | Spunta **Encrypted** |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` o `verify-full` — deve essere accettato dal server |

La stringa di connessione risultante è simile a questa:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Qualsiasi altra opzione di psqlODBC può essere aggiunta come proprietà ulteriore — per esempio
`ReadOnly=1` per una sessione in sola lettura, oppure `ConnSettings` per eseguire istruzioni
`SET` alla connessione.

---

## 3. Configurazione di *digna* {: #3-digna-configuration }

Nella schermata **Add DB Connection**, indica quanto segue:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Note su PostgreSQL {: #4-notes-on-postgresql }

- **`SSLMode` deve corrispondere al server.** Un server configurato con `hostssl` rifiuta
  `SSLMode=disable`, e `verify-ca` o `verify-full` richiedono inoltre che il certificato radice
  sia disponibile al driver sull'host *digna*. Se durante il test del driver hai dovuto
  scegliere una modalità specifica, usa la stessa qui.
- **Una connessione vede un database.** *digna* offre gli schemi del database indicato in
  `DATABASE`, perché PostgreSQL segnala solo il database corrente come catalogo. Le tabelle
  sorgente in un altro database richiedono una connessione propria.
- **Modalità di profilazione.** *Permanent* crea le tabelle di lavoro in **Work Schema**, quindi
  l'utente ha bisogno di `CREATE` su quello schema. *Session* usa `CREATE TEMPORARY TABLE` e non
  tocca **Work Schema**. *Standard* richiede solo accesso in lettura.

---

## 5. Verificare il driver (facoltativo) {: #5-verifying-the-driver-optional }

Configurare un'origine dati ODBC non è necessario per una connessione senza DSN, ma la finestra
di dialogo del driver è un modo comodo per confermare che il driver funziona e che il server
accetta le tue credenziali e la tua modalità SSL prima di inserirle in *digna*.

#### Passo 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

#### Passo 2 – Testare la connessione

Fai clic sul pulsante **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

I valori inseriti qui sono esattamente quelli che assumono le proprietà della
[sezione 2](#2-odbc-properties).