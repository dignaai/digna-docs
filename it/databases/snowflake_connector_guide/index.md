# Connettore sorgente per Snowflake

Questa guida descrive come configurare *digna* per connettersi a Snowflake tramite **ODBC**,
usando una stringa di connessione **senza DSN**.

La parte digna della configurazione è identica per ogni tecnologia: dove si creano le
connessioni, come vengono cifrati i valori delle proprietà, come si testa una connessione e cosa
significano le modalità di profilazione. È descritta in
[Panoramica delle connessioni ai database](overview.md). Questa pagina copre ciò che è specifico
di Snowflake.

---

## 1. Installare il driver ODBC {: #1-install-the-odbc-driver }

Installa lo **Snowflake ODBC Driver** sulla macchina che esegue il backend di *digna*, seguendo
[la guida di installazione di Snowflake](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

Il driver si registra come **SnowflakeDSIIDriver**. Leggi il nome esatto registrato sul tuo host
come descritto in [Installare il driver ODBC sull'host digna](overview.md#install-the-driver).

---

## 2. Proprietà ODBC {: #2-odbc-properties }

A Snowflake si arriva con un **token di accesso programmatico (PAT)**: il percorso di
autenticazione su cui *digna* è verificato, e quello che Snowflake richiede per gli account in
cui l'accesso con la sola password è bloccato.

!!! important "Un esempio, non una specifica"

    L'insieme qui sotto è una combinazione che è noto funzionare. Le proprietà appartengono al
    driver ODBC di Snowflake, quindi i loro nomi, i valori predefiniti e i valori accettati
    variano tra versioni del driver e piattaforme, e quali opzioni di autenticazione il tuo
    account consenta è deciso dalla policy di sicurezza dell'account. Usalo come punto di
    partenza e consulta la documentazione della versione del driver che hai installato.

| Chiave | Valore di esempio | Note |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Deve corrispondere al nome del driver registrato sull'host *digna* |
| `Server` | `<account>.snowflakecomputing.com` | Identificatore dell'account più il suffisso, per es. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Utente Snowflake a cui appartiene il token |
| `Database` | `TEST` | Database che contiene gli schemi sorgente. È l'unico database che questa connessione può profilare |
| `Schema` | `PUBLIC` | Schema predefinito della sessione |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Seleziona l'autenticazione tramite token |
| `token` | `<programmatic access token>` | Spunta **Encrypted** |

La stringa di connessione risultante è simile a questa:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Warehouse e ruolo

Le query hanno bisogno di un warehouse. Se l'utente *digna* ha un warehouse predefinito e un
ruolo predefinito, la sessione li eredita e non c'è nulla da configurare. Altrimenti aggiungi:

| Chiave | Valore di esempio | Note |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Warehouse che esegue le query di profilazione |
| `Role` | `DIGNA_READER` | Ruolo i cui privilegi vengono usati dalla sessione |

!!! tip "Dai a digna un warehouse dedicato"

    Un warehouse separato, piccolo e con sospensione automatica mantiene visibile il costo della
    profilazione ed evita che *digna* competa con gli utenti interattivi per la capacità di
    calcolo.

### Autenticazione con password

Dove l'account lo consente ancora, una password funziona al posto del token: rimuovi
`authenticator` e `token` e aggiungi:

| Chiave | Valore di esempio | Note |
|---|---|---|
| `PWD` | `<password>` | Spunta **Encrypted** |

---

## 3. Configurazione di *digna* {: #3-digna-configuration }

Nella schermata **Add DB Connection**, indica quanto segue:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Note su Snowflake {: #4-notes-on-snowflake }

- **I token scadono.** Un token di accesso programmatico viene emesso con una durata, e la
  profilazione si ferma il giorno in cui scade. Annota la data di scadenza quando lo crei e
  inserisci il nuovo token nella proprietà `token`: i valori cifrati possono essere sostituiti
  ma non riletti.
- **Una connessione vede un database.** *digna* offre gli schemi del database indicato in
  `Database`, perché Snowflake segnala solo il database corrente come catalogo. Le tabelle
  sorgente in un altro database richiedono una connessione propria.
- **Gli identificatori sono in maiuscolo**, a meno che non siano stati creati tra virgolette.
  *digna* usa i nomi così come Snowflake li segnala.
- **Modalità di profilazione.** *Permanent* crea le tabelle di lavoro in **Work Schema**, quindi
  il ruolo ha bisogno di `CREATE TABLE` lì. *Session* usa `CREATE TEMPORARY TABLE` e non tocca
  **Work Schema**. *Standard* richiede solo accesso in lettura — e nessun privilegio di
  scrittura.

---

## 5. Verificare il driver (facoltativo) {: #5-verifying-the-driver-optional }

Configurare un'origine dati ODBC non è necessario per una connessione senza DSN, ma la finestra
di dialogo del driver è un modo comodo per confermare che il driver, l'URL dell'account e le tue
credenziali funzionano prima di inserirli in *digna*.

#### Passo 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Note:

- Il valore di **Server** è composto dall'identificatore del tuo account Snowflake seguito da
  `.snowflakecomputing.com`.
- **Database**, **Schema** e **Warehouse** inseriti qui corrispondono alle proprietà `Database`,
  `Schema` e `Warehouse` della [sezione 2](#2-odbc-properties).

#### Passo 2 – Testare la connessione

Fai clic sul pulsante **TEST**. Una connessione riuscita dovrebbe apparire così:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)