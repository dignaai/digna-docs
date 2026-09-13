# Connettore sorgente per Netezza

Questa guida descrive come configurare *digna* per connettersi a Netezza tramite **ODBC**, usando
una stringa di connessione **senza DSN**.

La parte digna della configurazione è identica per ogni tecnologia: dove si creano le
connessioni, come vengono cifrati i valori delle proprietà, come si testa una connessione e cosa
significano le modalità di profilazione. È descritta in
[Panoramica delle connessioni ai database](overview.md). Questa pagina copre ciò che è specifico
di Netezza.

---

## 1. Installare il driver ODBC {: #1-install-the-odbc-driver }

Installa il driver ODBC **NetezzaSQL** (parte degli strumenti client di IBM Netezza) sulla
macchina che esegue il backend di *digna*, seguendo la guida di installazione ufficiale del
fornitore.

Leggi il nome esatto del driver registrato sul tuo host come descritto in
[Installare il driver ODBC sull'host digna](overview.md#install-the-driver).

---

## 2. Proprietà ODBC {: #2-odbc-properties }

!!! important "Un esempio, non una specifica"

    L'insieme qui sotto è una combinazione che è noto funzionare. Le proprietà appartengono al
    driver NetezzaSQL, quindi i loro nomi, i valori predefiniti e i valori accettati variano tra
    versioni del client e piattaforme, e un'appliance protetta con TLS richiede più delle
    proprietà mostrate qui. Usalo come punto di partenza e consulta la documentazione della
    versione del client che hai installato.

Aggiungi le seguenti proprietà nella schermata **Add DB Connection**:

| Chiave | Valore di esempio | Note |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Deve corrispondere al nome del driver registrato sull'host *digna*. Le parentesi graffe sono il modo consueto di scrivere questo nome |
| `SERVER` | `netezza.example.com` | Nome del server o indirizzo IP |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Database in cui la sessione inizia |
| `UID` | `ADMIN` | Utente del database |
| `PWD` | `<password>` | Spunta **Encrypted** |

La stringa di connessione risultante è simile a questa:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

A seconda della versione del driver, dell'installazione e dei requisiti di sicurezza possono
servire altre proprietà — per esempio `SecurityLevel` e `CaCertFile` per un'appliance protetta
con TLS. Ogni opzione offerta dalle finestre *Advanced*, *SSL* e *Driver* del driver può essere
aggiunta come proprietà.

---

## 3. Configurazione di *digna* {: #3-digna-configuration }

Nella schermata **Add DB Connection**, indica quanto segue:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Note su Netezza {: #4-notes-on-netezza }

- **Valgono sia i cataloghi sia gli schemi.** *digna* elenca come cataloghi i database che
  l'utente può vedere (da `_V_DATABASE`) e sotto di essi i loro schemi (da `_V_SCHEMA`), così
  che una connessione può servire sorgenti in più di un database. `DATABASE` decide solo dove
  inizia la sessione.
- **Gli identificatori sono in maiuscolo**, a meno che non siano stati creati tra virgolette:
  per questo gli esempi qui sopra usano `TEST` e `ADMIN`.
- **Modalità di profilazione.** *Permanent* crea le tabelle di lavoro in **Work Schema**, quindi
  l'utente ha bisogno di `CREATE TABLE` lì. *Session* usa `CREATE TEMPORARY TABLE` e non tocca
  **Work Schema**. *Standard* richiede solo accesso in lettura.

---

## 5. Verificare il driver (facoltativo) {: #5-verifying-the-driver-optional }

Configurare un'origine dati ODBC non è necessario per una connessione senza DSN, ma la finestra
di dialogo del driver è un modo comodo per confermare che il driver e le tue credenziali
funzionano prima di inserirli in *digna*.

#### Passo 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

I campi in **DSN Options** corrispondono uno a uno alle proprietà della
[sezione 2](#2-odbc-properties). A seconda del driver Netezza, dell'installazione e dei
requisiti di sicurezza potresti aver bisogno di dati anche nelle schede
**Advanced DSN Options**, **SSL DSN Options** o **Driver Options**; per l'installazione più
semplice, **DSN Options** è sufficiente.

Fai clic sul pulsante **Test Connection**.

#### Passo 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Quando compare la schermata di successo, il driver funziona e i valori sono corretti.