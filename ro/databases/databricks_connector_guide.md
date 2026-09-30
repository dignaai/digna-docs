# Conector sursă pentru Databricks

Acest ghid descrie cum să configurați *digna* pentru a se conecta la Databricks prin **ODBC**,
folosind un șir de conexiune **fără DSN** (DSN-less).

Partea *digna* a configurării este aceeași pentru orice tehnologie — unde se creează conexiunile,
cum sunt criptate valorile proprietăților, cum se testează o conexiune și ce înseamnă modurile de
profilare. Aceasta este descrisă în [Prezentarea conexiunilor la baze de date](overview.md). Această
pagină acoperă ceea ce este specific Databricks.

!!! note "Unity Catalog este obligatoriu"

    *digna* citește cataloagele disponibile din `system.information_schema.catalogs`, deci
    workspace-ul trebuie să aibă Unity Catalog activat. Versiunile *digna* anterioare ofereau o
    tehnologie separată „Databricks Legacy” pentru workspace-urile fără Unity Catalog; aceasta nu
    mai este disponibilă.

---

## 1. Instalați driverul ODBC {: #1-install-the-odbc-driver }

Instalați **Databricks ODBC Driver** pe mașina care rulează backend-ul *digna*, urmând
[ghidul de instalare Databricks](https://docs.databricks.com/aws/en/integrations/odbc/).

În funcție de versiune, driverul se înregistrează ca **Simba Spark ODBC Driver** sau ca
**Databricks ODBC Driver**. Citiți numele exact înregistrat de pe gazda dvs., așa cum este descris
în [Instalați driverul ODBC pe gazda digna](overview.md#install-the-driver).

---

## 2. Colectați detaliile conexiunii {: #2-gather-the-connection-details }

Toate valorile provin din SQL warehouse-ul (sau clusterul) pe care doriți ca *digna* să îl
folosească. Deschideți-l în workspace-ul Databricks și accesați **Connection details**:

| Câmp Databricks | Folosit ca |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, de obicei `443` |
| **HTTP path** | `HTTPPath` |

Pentru autentificare, creați un **personal access token** — consultați
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Token-urile aparțin unui utilizator sau unui service principal, iar acel principal are nevoie de
`USE CATALOG`, `USE SCHEMA` și `SELECT` pe datele sursă.

---

## 3. Proprietăți ODBC {: #3-odbc-properties }

!!! important "Un exemplu, nu o specificație"

    Setul de mai jos este o combinație despre care se știe că funcționează. Proprietățile aparțin
    driverului Databricks/Simba, astfel încât numele, valorile implicite și valorile acceptate
    diferă între versiunile de driver — driverul a fost redenumit și opțiunile sale de
    autentificare extinse de mai multe ori — și între platforme. Folosiți-l ca punct de plecare și
    consultați documentația versiunii de driver pe care ați instalat-o.

Adăugați următoarele proprietăți în ecranul **Add DB Connection**:

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Trebuie să corespundă numelui driverului înregistrat pe gazda *digna* |
| `Host` | `<workspace>.cloud.databricks.com` | Server hostname al warehouse-ului, de ex. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | HTTP path al warehouse-ului sau clusterului |
| `SSL` | `1` | Endpoint-urile Databricks acceptă doar TLS |
| `ThriftTransport` | `2` | Transport HTTP, cel folosit de endpoint-urile SQL |
| `AuthMech` | `3` | Autentificare cu token |
| `UID` | `token` | Cuvântul literal `token`, nu un nume de utilizator |
| `PWD` | `dapi…` | Personal access token-ul. Bifați **Encrypted** |
| `UseNativeQuery` | `1` | Transmite nemodificat SQL-ul generat de *digna* — vezi mai jos |

Șirul de conexiune rezultat arată astfel:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Păstrați `UseNativeQuery=1`"

    Cu `UseNativeQuery=0` — valoarea implicită a driverului — driverul rescrie SQL-ul primit în
    ceea ce consideră a fi sintaxă ODBC portabilă. *digna* generează deja SQL Databricks, astfel
    încât rescrierea poate modifica ghilimelele backtick și literalii de dată, iar profilarea eșuează
    apoi pe instrucțiuni care sunt valide în forma în care au fost scrise.

### OAuth în loc de token

Pentru un service principal cu autentificare OAuth machine-to-machine, înlocuiți `AuthMech`,
`UID` și `PWD` cu:

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Client credentials |
| `Auth_Client_ID` | `<application id>` | Service principal |
| `Auth_Client_Secret` | `<client secret>` | Bifați **Encrypted** |

---

## 4. Configurația *digna* {: #4-digna-configuration }

În ecranul **Add DB Connection**, furnizați următoarele:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Note despre Databricks {: #5-notes-on-databricks }

- **Warehouse-ul trebuie să ruleze**, sau să poată porni, atunci când *digna* se conectează. Un
  warehouse care repornește dintr-o stare oprită poate avea nevoie de mai mult timp decât
  timeout-ul conexiunii — dacă testul eșuează la prima încercare după o perioadă de inactivitate,
  reîncercați.
- **Cataloagele provin din workspace.** Spre deosebire de majoritatea tehnologiilor, o conexiune
  Databricks ajunge la fiecare catalog pe care principalul are voie să îl vadă, astfel încât o
  singură conexiune poate deservi surse din mai multe cataloage.
- **Moduri de profilare.** *Permanent* creează tabelele de lucru în **Work Schema** din catalogul
  sursei, deci principalul are nevoie de `CREATE TABLE` acolo. *Session* folosește
  `CREATE TEMPORARY TABLE` și nu atinge **Work Schema**. *Standard* necesită doar acces de citire.
- **Warehouse-urile serverless funcționează** în același mod; diferă doar `HTTPPath`.

---

## 6. Verificarea driverului (opțional) {: #6-verifying-the-driver-optional }

Configurarea unei surse de date ODBC nu este necesară pentru o conexiune fără DSN, dar dialogul
propriu al driverului este o modalitate comodă de a confirma că driverul, warehouse-ul și token-ul
funcționează înainte de a le introduce în *digna*.

#### Pasul 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Pasul 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Pasul 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Pasul 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Pasul 5 – Testați conexiunea

Faceți clic pe butonul **TEST**. O conexiune reușită ar trebui să arate astfel:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

Gazda, HTTP path și token-ul introduse aici sunt exact valorile pe care le iau proprietățile din
[secțiunea 3](#3-odbc-properties).