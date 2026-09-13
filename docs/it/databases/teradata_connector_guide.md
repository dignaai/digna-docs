---
title: Connettore Teradata – Integrazione database | digna Documentazione
description: Configura digna per connettersi a Teradata tramite ODBC con una stringa di connessione senza DSN. Copre il driver ODBC di Teradata, la proprietà DBCNAME, i meccanismi di accesso e le impostazioni di connessione lato digna.
image: /assets/logo_square.png
---


# Connettore sorgente per Teradata

Questa guida descrive come configurare *digna* per connettersi a Teradata tramite **ODBC**,
usando una stringa di connessione **senza DSN**.

La parte digna della configurazione è identica per ogni tecnologia: dove si creano le
connessioni, come vengono cifrati i valori delle proprietà, come si testa una connessione e cosa
significano le modalità di profilazione. È descritta in
[Panoramica delle connessioni ai database](overview.md). Questa pagina copre ciò che è specifico
di Teradata.

---

## 1. Installare il driver ODBC {: #1-install-the-odbc-driver }

Installa l'**ODBC Driver for Teradata** sulla macchina che esegue il backend di *digna*,
seguendo la guida di installazione ufficiale del fornitore.

Il driver si registra con la propria versione nel nome, per esempio
**Teradata Database ODBC Driver 20.00**. Leggi il nome esatto registrato sul tuo host come
descritto in [Installare il driver ODBC sull'host digna](overview.md#install-the-driver).

---

## 2. Proprietà ODBC {: #2-odbc-properties }

!!! important "Un esempio, non una specifica"

    L'insieme qui sotto è una combinazione che è noto funzionare. Le proprietà appartengono al
    driver ODBC di Teradata, quindi i loro nomi, i valori predefiniti e i valori accettati
    variano tra versioni del driver — la versione fa parte del nome stesso del driver — e tra
    piattaforme. Usalo come punto di partenza e consulta la documentazione della versione del
    driver che hai installato.

Aggiungi le seguenti proprietà nella schermata **Add DB Connection**:

| Chiave | Valore di esempio | Note |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Deve corrispondere al nome del driver registrato sull'host *digna* |
| `DBCNAME` | `teradata.example.com` | Nome del server o indirizzo IP. Il nome che Teradata dà alla proprietà dell'host |
| `UID` | `digna_source_user` | Utente del database |
| `PWD` | `<password>` | Spunta **Encrypted** |

La stringa di connessione risultante è simile a questa:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Proprietà aggiuntive utili:

| Chiave | Valore di esempio | Note |
|---|---|---|
| `MechanismName` | `TD2` | Meccanismo di accesso. `TD2` è il valore predefinito di Teradata; usa `LDAP` per l'autenticazione tramite directory |
| `DefaultDatabase` | `dad` | Database in cui la sessione inizia |
| `CharacterSet` | `UTF8` | Impostalo quando il set di caratteri predefinito della sessione danneggerebbe dati non ASCII |

---

## 3. Configurazione di *digna* {: #3-digna-configuration }

Nella schermata **Add DB Connection**, indica quanto segue:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Note su Teradata {: #4-notes-on-teradata }

- **Un database Teradata è un catalogo, non uno schema.** *digna* elenca come cataloghi i
  database che l'utente può vedere (da `DBC.DatabasesV`), e il livello dello schema non si
  applica. Quando aggiungi una sorgente dati, scegli il database come catalogo; lo schema viene
  segnalato come *non applicabile*.
- **Una connessione raggiunge ogni database consentito**, così una sola connessione può servire
  sorgenti distribuite su più database — a differenza delle tecnologie in cui la connessione è
  vincolata a un unico database.
- **Work Schema è un database.** Per la profilazione *Permanent*, indica il database Teradata
  che contiene le tabelle di lavoro e concedi all'utente i diritti di `CREATE TABLE` più
  un'allocazione di spazio `PERM` al suo interno: un database senza spazio perm non può ospitare
  una tabella.
- **Modalità di profilazione.** *Permanent* crea le tabelle in **Work Schema**. *Session* usa una
  tabella `VOLATILE`, che richiede spazio `SPOOL` ma nessuno spazio perm e nessun diritto in
  **Work Schema**. *Standard* richiede solo accesso in lettura.

---

## 5. Verificare il driver (facoltativo) {: #5-verifying-the-driver-optional }

Configurare un'origine dati ODBC non è necessario per una connessione senza DSN, ma la finestra
di dialogo del driver è un modo comodo per confermare che il driver e le tue credenziali
funzionano prima di inserirli in *digna*.

#### Passo 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Il campo **Name or IP address** corrisponde qui alla proprietà `DBCNAME` della
[sezione 2](#2-odbc-properties).

Fai clic sul pulsante **Test**.

#### Passo 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Indica nome utente e password, poi fai clic sul pulsante **OK**. Una schermata di successo
conferma che il driver e le credenziali funzionano.
