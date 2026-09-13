---
title: Connettore Azure Synapse – Integrazione database | digna Documentazione
description: Configura digna per connettersi ad Azure Synapse Analytics tramite ODBC con una stringa di connessione senza DSN. Supporta pool SQL serverless e dedicati, con le proprietà ODBC necessarie e le impostazioni di connessione lato digna.
image: /assets/logo_square.png
---


# Connettore sorgente per Azure Synapse Analytics

Questa guida descrive come configurare *digna* per connettersi ad Azure Synapse Analytics
tramite **ODBC**, usando una stringa di connessione **senza DSN**. Sono supportati sia i pool
SQL serverless sia quelli dedicati.

La parte digna della configurazione è identica per ogni tecnologia: dove si creano le
connessioni, come vengono cifrati i valori delle proprietà, come si testa una connessione e cosa
significano le modalità di profilazione. È descritta in
[Panoramica delle connessioni ai database](overview.md). Questa pagina copre ciò che è specifico
di Azure Synapse.

!!! note "Tecnologia"

    Synapse parla il dialetto di SQL Server, quindi la connessione si crea con **Technology:
    SQL Server**. Per un server on-premise vedi [MS SQL Server](sqlserver_connector_guide.md).

---

## 1. Installare il driver ODBC {: #1-install-the-odbc-driver }

Installa **ODBC Driver 18 for SQL Server** sulla macchina che esegue il backend di *digna*,
seguendo [la guida di installazione di Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server),
e leggi il nome esatto del driver registrato sul tuo host come descritto in
[Installare il driver ODBC sull'host digna](overview.md#install-the-driver).

---

## 2. Proprietà ODBC {: #2-odbc-properties }

!!! important "Un esempio, non una specifica"

    L'insieme qui sotto è una combinazione che è noto funzionare. Le proprietà appartengono al
    driver ODBC Microsoft, quindi i loro nomi, i valori predefiniti e i valori accettati variano
    tra versioni del driver e piattaforme, e ciò che il workspace richiede dipende da come è
    configurato: tipo di pool, metodo di autenticazione, firewall. Usalo come punto di partenza
    e consulta la documentazione della versione del driver che hai installato.

Aggiungi le seguenti proprietà nella schermata **Add DB Connection**:

| Chiave | Valore di esempio | Note |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Deve corrispondere al nome del driver registrato sull'host *digna* |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Nome del workspace più il suffisso dell'endpoint — vedi sotto |
| `DATABASE` | `dignadata` | Database che contiene gli schemi sorgente. È l'unico database che questa connessione può profilare |
| `UID` | `sqladminuser` | Login SQL |
| `PWD` | `<password>` | Spunta **Encrypted** |

La stringa di connessione risultante è simile a questa:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### Il valore di `SERVER`

Prendi il nome del workspace Synapse e aggiungi il suffisso dell'endpoint:

| Pool | `SERVER` |
|---|---|
| **Pool SQL serverless** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Pool SQL dedicato** | `<workspace>.sql.azuresynapse.net` |

!!! warning "La parte `-ondemand` sfugge facilmente"

    Senza di essa il nome viene risolto verso l'endpoint dedicato, e la connessione fallisce
    oppure raggiunge silenziosamente un pool diverso da quello previsto. Entrambi gli endpoint
    sono mostrati nella pagina di panoramica del workspace nel portale di Azure.

### Firewall

Il firewall del workspace Synapse deve consentire l'indirizzo in uscita dell'host *digna*.
Aggiungilo in **Networking** nel workspace prima di testare la connessione: un indirizzo
bloccato si manifesta come timeout di connessione anziché come errore di autenticazione.

### Autenticazione con Microsoft Entra ID

Anziché un login SQL, il driver può autenticarsi verso Entra ID. Sostituisci `UID`/`PWD` con il
metodo di autenticazione che il tuo workspace si aspetta, per esempio:

| Chiave | Valore di esempio | Note |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | `UID` assume allora l'ID applicazione (client) e `PWD` il client secret |
| `Authentication` | `ActiveDirectoryMSI` | Identità gestita dell'host *digna*, nessuna credenziale necessaria |

---

## 3. Configurazione di *digna* {: #3-digna-configuration }

Nella schermata **Add DB Connection**, indica quanto segue:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Note su Azure Synapse {: #4-notes-on-azure-synapse }

- **I pool serverless supportano solo la profilazione *Standard*.** Un pool SQL serverless non
  può creare tabelle in un database, quindi non possono essere eseguite né la profilazione
  *Permanent* né quella *Session*. *Standard* calcola le metriche direttamente sulla sorgente,
  ed è anche l'opzione più economica, dato che il serverless viene fatturato in base ai dati
  elaborati.
- **Una connessione vede un database.** *digna* offre gli schemi del database indicato in
  `DATABASE`, perché Synapse, come SQL Server, segnala solo il database corrente come catalogo.
- **La cifratura è attiva per impostazione predefinita** in Driver 18 e gli endpoint Synapse
  presentano certificati pubblici validi, quindi non serve alcuna proprietà `Encrypt` o
  `TrustServerCertificate`.
- **Un endpoint serverless può riattivarsi dall'inattività** alla prima connessione. Se il test
  di connessione va in timeout su un pool inutilizzato da un po', riprova.

---

## 5. Verificare il driver (facoltativo) {: #5-verifying-the-driver-optional }

Configurare un'origine dati ODBC non è necessario per una connessione senza DSN, ma la procedura
guidata del driver è un modo comodo per confermare che il driver funziona e che il workspace
accetta le tue credenziali prima di inserirle in *digna*.

#### Passo 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Compila il campo «Server».
Usa il nome del workspace Synapse ed estendilo con «.sql.azuresynapse.net».  
**Attenzione**: se vuoi connetterti usando un pool SQL serverless, assicurati di includere
«-ondemand» come mostrato nello screenshot qui sopra.

Fai clic sul pulsante **Next >**.

#### Passo 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Scegli il metodo di autenticazione (per es. nome utente e password)
e fornisci i dati richiesti.

Fai clic sul pulsante **Next >**.

#### Passo 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Scegli le impostazioni conformi ad ANSI, poi fai clic sul pulsante **Next >**.

#### Passo 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Puoi lasciare le impostazioni predefinite oppure scegliere le opzioni secondo le tue esigenze
e fare clic sul pulsante **Finish**.

#### Passo 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Ora fai clic sul pulsante **Test datasource**.

#### Passo 6
![Step 6](images/azure_synapse/create_odbc_data_source_step6.png)

Una schermata di successo conferma che il driver, l'endpoint e le credenziali funzionano. I
valori inseriti sono esattamente quelli che assumono le proprietà della
[sezione 2](#2-odbc-properties).
