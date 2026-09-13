# Panoramica delle connessioni ai database

---

## Indice

1. [Come funzionano le connessioni](#how-connections-work)
2. [Guide per tecnologia](#technology-guides)
3. [Prerequisito: installare il driver ODBC sull'host digna](#install-the-driver)
4. [Creare una connessione al database](#create-a-database-connection)
5. [Proprietà ODBC](#odbc-properties)
6. [Cifrare i valori delle proprietà](#encrypting-property-values)
7. [Testare una connessione](#testing-a-connection)
8. [Quale database vede la connessione](#which-database-the-connection-sees)
9. [Modalità di profilazione e Work Schema](#profiling-mode-and-work-schema)
10. [Usare invece un DSN](#using-a-dsn-instead)
11. [Risoluzione dei problemi](#troubleshooting)

---

## Come funzionano le connessioni {: #how-connections-work }

*digna* raggiunge ogni tecnologia sorgente tramite **ODBC**. Una connessione è un elenco di
proprietà ODBC che inserisci come coppie chiave/valore. Quando *digna* apre la connessione,
unisce quelle coppie in una stringa di connessione — `Key=Value`, separate da `;`, nell'ordine
in cui le hai elencate — e la consegna al gestore di driver ODBC sull'host *digna*.

Inserire tu stesso le proprietà è ciò che rende la configurazione **senza DSN**: la connessione
porta con sé tutto ciò di cui il driver ha bisogno, quindi non occorre registrare alcuna origine
dati ODBC (DSN) sull'host. È il modo consigliato di configurare *digna*, perché la definizione
della connessione risiede interamente in *digna* e si sposta con esso.

### Perché ODBC {: #why-odbc }

Le versioni precedenti offrivano la scelta tra un driver per tecnologia e ODBC, selezionata con
un interruttore **Use ODBC**. Dalla release 2026.06, *digna* si basa esclusivamente su ODBC.
Un'unica interfaccia standard offre più di un insieme di driver su misura:

- **Autenticazione** — l'autenticazione fa parte di ODBC, quindi una connessione può usare tutto
  ciò che il suo driver supporta: password, token e PAT, Kerberos e Active Directory, MFA e
  single sign-on da browser, identità cloud, certificati client e TLS. I nuovi metodi arrivano
  con un aggiornamento del driver, senza attendere una release di *digna*.
- **Driver mantenuti dai produttori dei database** — il driver del produttore segue le nuove
  versioni del server e le correzioni di sicurezza, e puoi aggiornarlo secondo i tuoi tempi,
  indipendentemente da *digna*.
- **Un solo modo di configurare tutto** — ogni tecnologia è un elenco di proprietà
  chiave/valore, con la stessa interfaccia, la stessa cifratura dei valori sensibili e la stessa
  diagnostica, invece di un insieme di campi diverso per ogni sorgente.
- **Regolazione e portata** — le opzioni a livello di driver come timeout, impostazioni TLS,
  proxy e dimensioni di fetch sono disponibili per ogni sorgente, e qualsiasi tecnologia con un
  driver ODBC conforme può essere collegata, comprese quelle per cui *digna* non pubblica una
  guida dedicata.

!!! note "Cosa è cambiato nell'interfaccia"

    L'interruttore **Use ODBC** e i campi separati host, porta, database, utente e password non
    esistono più. Una connessione che non usa già ODBC ha bisogno che le sue proprietà ODBC
    vengano inserite prima di tornare a funzionare — vedi
    [Creare una connessione al database](#create-a-database-connection).

---

## Guide per tecnologia {: #technology-guides }

I nomi delle proprietà variano da driver a driver, e ogni tecnologia ha uno o due dettagli che
le altre non hanno. Le guide qui sotto coprono quella parte; questa pagina copre il lato
*digna*, che è lo stesso per tutte.

!!! important "Gli insiemi di proprietà nelle guide sono esempi"

    Ogni guida mostra una combinazione che è noto funzionare: quella su cui *digna* viene
    testato. È un punto di partenza, non una specifica: le proprietà appartengono al driver
    ODBC, e quali esistono, come si chiamano e quali valori accettano varia tra versioni e
    produttori di driver, tra Windows, Linux e macOS, e in base a come è configurato il server
    sorgente: metodo di autenticazione, TLS, gateway, porta. Aspettati di dover adattare
    qualche valore, e considera autorevole la documentazione della versione del driver che hai
    installato.

| Tecnologia | Guida | Da sapere |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | I pool serverless richiedono `-ondemand` nel nome host e supportano solo la profilazione *Standard* |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Autenticazione tramite token: `UID=token`, PAT in `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | I cataloghi vengono dal driver, non da una query |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Il nome del driver va tra parentesi graffe: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` accetta un descrittore di connessione completo oppure un alias di `tnsnames.ora` |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` deve corrispondere a ciò che il server richiede |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` decide quali schemi *digna* può vedere |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Il token di accesso programmatico è il percorso di autenticazione testato |
| **Teradata** | [Teradata](teradata_connector_guide.md) | L'host va in `DBCNAME`; i database fungono da schemi |

---

## Prerequisito: installare il driver ODBC sull'host digna {: #install-the-driver }

*digna* apre le connessioni sorgente dal **server che esegue il backend digna**, non dal
browser. Il driver ODBC deve quindi essere installato su quella macchina, e il suo nome
registrato presso il gestore di driver locale.

=== "Windows"

    Installa il driver a 64 bit del produttore, poi apri **Amministrazione origine dati ODBC
    (64 bit)** e passa alla scheda **Drivers**. I nomi elencati lì sono esattamente i valori che
    puoi usare per la proprietà `Driver`.

=== "Linux"

    Installa **unixODBC** e il driver del produttore, poi elenca i nomi dei driver registrati:

    ```bash
    odbcinst -q -d
    ```

    I nomi stampati tra parentesi quadre sono i valori che puoi usare per la proprietà `Driver`.
    Provengono da `/etc/odbcinst.ini` (o dal file indicato da `odbcinst -j`).

=== "macOS"

    Installa **unixODBC** (per esempio con `brew install unixodbc`) e il driver del produttore,
    poi elenca i nomi dei driver registrati:

    ```bash
    odbcinst -q -d
    ```

!!! warning "Il nome del driver deve corrispondere carattere per carattere"

    `Driver` viene passato invariato al gestore di driver. `Simba Spark ODBC Driver` e
    `Simba Spark ODBC Driver 64` sono driver diversi per il gestore, e un nome non registrato
    produce un errore *data source name not found* anche se non c'è di mezzo alcun DSN.

Invece di un nome registrato, tutti i gestori di driver comuni accettano anche il percorso
completo alla libreria del driver, per esempio
`Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. È utile quando il driver è installato ma
non registrato.

---

## Creare una connessione al database {: #create-a-database-connection }

Apri l'**Admin Panel**, vai alla scheda **Database Connections** e fai clic su
**Add DB Connection**. La schermata chiede cinque cose:

| Campo | Descrizione |
|---|---|
| **Name** | Nome della connessione. Serve a riferirsi alla connessione nelle altre schermate. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake o Hive. Seleziona il dialetto SQL che *digna* genera, quindi deve corrispondere alla sorgente, non al driver. Azure Synapse Analytics è una connessione **SQL Server**. |
| **ODBC Properties** | Le coppie chiave/valore descritte in [Proprietà ODBC](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* o *Session* — vedi [Modalità di profilazione e Work Schema](#profiling-mode-and-work-schema). |
| **Work Schema** | Schema che contiene le tabelle di lavoro per la profilazione *Permanent*. |

Una connessione viene amministrata centralmente e poi assegnata a uno o più progetti, così la
stessa connessione può servire più progetti.

---

## Proprietà ODBC {: #odbc-properties }

Fai clic su **Add Property** per ogni proprietà e compila **Key**, **Value** e, per i segreti,
la casella **Encrypted**. Ogni guida di tecnologia elenca un insieme di esempio per quella
tecnologia, che adatti alla tua versione del driver e al tuo server — vedi
[la nota qui sopra](#technology-guides).

Qualunque sia il driver, un insieme di proprietà copre le stesse quattro cose:

- **`Driver`** — il nome del driver registrato, come descritto [qui sopra](#install-the-driver).
- **L'indirizzo del server** — la chiave varia da driver a driver: `SERVER`, `HOST`, `DBCNAME`,
  `Server` oppure, per Oracle, il descrittore di connessione `DBQ`.
- **Le credenziali** — di solito `UID` e `PWD`; Snowflake usa `UID` più un `token`, e Databricks
  l'utente letterale `token` più il token di accesso personale in `PWD`.
- **Il database o il catalogo in cui lavorare**, quando la tecnologia ne ha uno — vedi
  [Quale database vede la connessione](#which-database-the-connection-sees).

Tutto ciò che il driver documenta può essere aggiunto allo stesso modo: pool di connessioni,
timeout dei socket, impostazioni Kerberos, impostazioni proxy. *digna* non interpreta le
proprietà; si limita a inoltrarle.

!!! warning "I valori non vengono sottoposti a escape: racchiudi tra graffe tutto ciò che contiene un punto e virgola"

    Poiché le proprietà vengono unite con `;`, un valore che contenga a sua volta `;`
    spezzerebbe la stringa di connessione nel punto sbagliato. Racchiudi quei valori tra
    parentesi graffe: `PWD={p@ss;word}`. Lo stesso vale per valori con `=` o con spazi iniziali.
    È anche il motivo per cui alcuni driver si scrivono per convenzione tra graffe, come
    `{NetezzaSQL}` o `{SnowflakeDSIIDriver}`.

---

## Cifrare i valori delle proprietà {: #encrypting-property-values }

Spunta **Encrypted** per ogni proprietà che contiene un segreto: `PWD`, `token`, un client
secret. Il valore viene allora cifrato prima di essere memorizzato nel repository di *digna*,
mascherato nella schermata e decifrato solo quando la stringa di connessione viene assemblata.

!!! tip "Suggerimento"

    Un valore cifrato non può essere riletto, né nell'interfaccia né tramite l'API: può solo
    essere sostituito. Conserva i segreti anche nel tuo gestore di password.

Le proprietà che non sono segrete — nome del driver, host, porta, database — è meglio lasciarle
non cifrate, così restano leggibili per chi manterrà la connessione in seguito.

---

## Testare una connessione {: #testing-a-connection }

Fai clic su **Test** nella finestra *Add DB Connection* **prima** di salvare. Il test usa i
valori attualmente presenti nel modulo ed esegue una connessione reale, quindi segnala
esattamente ciò che incontrerebbe un'ispezione: un nome di driver errato, una password
rifiutata, un host irraggiungibile. Non viene memorizzato nulla: la connessione di test viene
annullata sia in caso di successo sia in caso di errore.

Per una connessione già esistente, passa il mouse sulla sua riga nella scheda
**Database Connections** e fai clic sull'icona della **spina** per ritestarla. È il modo più
rapido per verificare se una sorgente è raggiungibile dopo una rotazione di password o una
modifica al firewall.

---

## Quale database vede la connessione {: #which-database-the-connection-sees }

Quando aggiungi una sorgente dati, *digna* offre i cataloghi, gli schemi e le tabelle che la
connessione può raggiungere. Fin dove arrivi dipende dalla tecnologia:

| Tecnologia | Cataloghi offerti |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Solo il database **corrente** della connessione |
| **Teradata**, **Netezza**, **Databricks** | Tutti i database o cataloghi che l'utente è autorizzato a vedere |
| **Hive**, **Impala** | Quelli segnalati dal driver |

!!! important "Una connessione, un database"

    Per PostgreSQL, SQL Server, Oracle e Snowflake, le proprietà devono puntare al database che
    contiene gli schemi sorgente — `DATABASE=…`, `Database=…`, oppure il nome del servizio
    all'interno del `DBQ` di Oracle. Le tabelle in un altro database non sono raggiungibili
    tramite quella connessione; aggiungine una seconda.

---

## Modalità di profilazione e Work Schema {: #profiling-mode-and-work-schema }

La modalità di profilazione determina come *digna* elabora i dati e calcola le metriche:

- **Standard:** le metriche sono calcolate direttamente sulle tabelle sorgente, senza copiare i
  dati.
- **Permanent:** i dati del giorno ispezionato vengono copiati in una tabella permanente e le
  metriche sono calcolate sui dati copiati.
- **Session:** i dati vengono copiati in una tabella di sessione o temporanea e le metriche sono
  calcolate su quei dati temporanei.

La modalità decide cosa deve essere consentito all'utente della connessione:

| Modalità | Scrive | Diritti necessari all'utente della connessione |
|---|---|---|
| **Standard** | nulla | Lettura sulle tabelle sorgente |
| **Permanent** | una tabella per sorgente dati in **Work Schema** | Creare ed eliminare tabelle in **Work Schema** |
| **Session** | una tabella temporanea che il database elimina con la sessione | Creare tabelle temporanee — **Work Schema** non viene usato |

*Standard* si limita a leggere, il che ne fa la modalità da scegliere quando a *digna* è
concesso un accesso in sola lettura. **Work Schema** viene letto solo per *Permanent*, ma vale
comunque la pena compilarlo perché la connessione continui a funzionare se la modalità viene
cambiata in seguito.

---

## Usare invece un DSN {: #using-a-dsn-instead }

Un DSN funziona ancora: `DSN` è semplicemente un'altra proprietà:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

Il DSN deve essere registrato sull'host *digna*, per lo stesso account utente che esegue il
backend di *digna*, e come **System DSN** quando *digna* viene eseguito come servizio. Tutto ciò
che è configurato nel DSN può essere sovrascritto aggiungendolo anche come proprietà.

La modalità senza DSN è l'impostazione predefinita documentata perché evita quello stato lato
host: la connessione è descritta interamente in *digna*, e un nuovo host *digna* ha bisogno del
driver installato, ma di nulla di configurato.

---

## Risoluzione dei problemi {: #troubleshooting }

### Nome dell'origine dati non trovato / nessun driver predefinito specificato

**Sintomi:**
- Il pulsante **Test** segnala un errore che menziona *data source name not found*, anche se la
  configurazione è senza DSN

**Cause e soluzioni:**
1. Il valore di `Driver` non corrisponde ad alcun nome di driver registrato: confrontalo con la
   scheda **Drivers** di *Amministrazione origine dati ODBC (64 bit)*, oppure con
   `odbcinst -q -d`
2. Il driver è installato sulla tua workstation ma non sull'host *digna*
3. Il driver è a 32 bit mentre *digna* è a 64 bit: installa il driver a 64 bit
4. La proprietà `Driver` manca del tutto, e non è stato indicato nemmeno un `DSN`
5. Su Linux e macOS il driver è installato ma non registrato: indica invece il percorso completo
   alla libreria del driver, oppure registralo in `odbcinst.ini`

---

### Il test di connessione va in timeout

**Sintomi:**
- **Test** si blocca e poi fallisce dopo circa mezzo minuto

**Cause e soluzioni:**
1. Host o porta irraggiungibili dall'host *digna*: controlla il firewall e, per le sorgenti
   cloud, l'elenco degli indirizzi IP consentiti
2. Il nome host è corretto, ma la porta appartiene a un altro servizio
3. La sorgente ha bisogno di più dei 30 secondi predefiniti per accettare una connessione: alza
   `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` nella sezione `[base]` di `config.toml` (`0` attende
   indefinitamente) e riavvia il backend
4. Un endpoint serverless si sta riattivando dall'inattività: riprova e, se accade di
   frequente, alza il timeout di login come sopra

---

### L'autenticazione fallisce anche se le credenziali sono corrette

**Sintomi:**
- Il driver segnala credenziali non valide, ma lo stesso utente funziona in un altro client SQL

**Cause e soluzioni:**
1. La password contiene `;`: racchiudi il valore tra graffe: `{p@ss;word}`
2. Uno spazio finale è stato copiato dentro il valore
3. Il driver si aspetta un meccanismo di autenticazione specifico, per esempio `AuthMech` per i
   driver Hive e Databricks, oppure `authenticator` per Snowflake
4. Il valore è stato memorizzato cifrato e poi modificato: i valori cifrati non possono essere
   riletti, quindi reinserisci il segreto per intero
5. Un token è scaduto: i token di accesso personale e quelli di accesso programmatico vengono
   emessi con una data di scadenza

---

### La schermata della sorgente dati non offre il database o lo schema previsto

**Sintomi:**
- Mancano cataloghi, schemi o tabelle quando si aggiunge una sorgente dati

**Cause e soluzioni:**
1. La connessione punta a un altro database — vedi
   [Quale database vede la connessione](#which-database-the-connection-sees)
2. All'utente della connessione mancano i diritti di lettura sullo schema o sul dizionario dati
3. **Technology** non corrisponde alla sorgente, quindi *digna* interroga il dizionario dati
   sbagliato
4. Per Snowflake non è assegnato alcun warehouse predefinito all'utente e non è stata indicata
   alcuna proprietà `Warehouse`, quindi le query sui metadati non possono essere eseguite

---

### La profilazione fallisce mentre il test di connessione riesce

**Sintomi:**
- **Test** passa, ma un'ispezione fallisce quando vengono create le tabelle di lavoro

**Cause e soluzioni:**
1. È selezionata la profilazione *Permanent* e l'utente della connessione non può creare tabelle
   in **Work Schema**: concedi i diritti, oppure passa a *Session* o *Standard*
2. **Work Schema** è vuoto o nomina uno schema inesistente, mentre è selezionata la profilazione
   *Permanent*
3. È selezionata la profilazione *Session* e l'utente della connessione non può creare tabelle
   temporanee
4. Una query di profilazione di lunga durata raggiunge il timeout delle query: alza
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` nella sezione `[base]` di `config.toml` (3600 secondi di
   default, `0` disattiva il timeout)

---

## Buone pratiche

**DA FARE:**

- Installare e registrare il driver sull'host *digna* prima di configurare la connessione
- Spuntare **Encrypted** per ogni password e ogni token
- Fare clic su **Test** prima di salvare, e ritestare dopo una rotazione di password
- Nominare le connessioni in base a sorgente e ambiente, per esempio `sales_dwh_prod`
- Dare a *digna* un utente di database dedicato, in sola lettura dove basta la profilazione
  *Standard*
- Mantenere una connessione per database sorgente, e aggiungerne una seconda anziché modificare
  la prima

**DA NON FARE:**

- Memorizzare segreti non cifrati, o condividere un utente di database tra *digna* e altri
  strumenti
- Usare un driver a 32 bit con un'installazione di *digna* a 64 bit
- Affidarsi a un DSN utente quando *digna* viene eseguito come servizio: non sarà visibile
- Inserire un valore che contiene `;` in una proprietà senza graffe
- Puntare **Work Schema** su uno schema che contiene dati sorgente

---

## Supporto

Hai bisogno di aiuto con una connessione al database?

- **E-mail:** support@digna.ai
- **Documentazione:** https://docs.digna.ai
- **Sito web:** https://www.digna.ai

---

**Release:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**