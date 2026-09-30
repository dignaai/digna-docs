# Conector sursă pentru MS SQL Server

Acest ghid descrie cum să configurați *digna* pentru a se conecta la Microsoft SQL Server prin
**ODBC**, folosind un șir de conexiune **fără DSN** (DSN-less).

Partea *digna* a configurării este aceeași pentru orice tehnologie — unde se creează conexiunile,
cum sunt criptate valorile proprietăților, cum se testează o conexiune și ce înseamnă modurile de
profilare. Aceasta este descrisă în [Prezentarea conexiunilor la baze de date](overview.md). Această
pagină acoperă ceea ce este specific SQL Server.

!!! note "Azure Synapse Analytics"

    Și Synapse se configurează ca o conexiune SQL Server, cu un alt nume de gazdă și câteva
    aspecte suplimentare — consultați [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Instalați driverul ODBC {: #1-install-the-odbc-driver }

Instalați **ODBC Driver 18 for SQL Server** pe mașina care rulează backend-ul *digna*, urmând
[ghidul de instalare Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

Driverul livrat cu Windows sub numele simplu **SQL Server** funcționează și el, dar este de mult
depășit și nu acceptă nici setările TLS moderne, nici autentificarea Azure. Folosiți-l doar acolo
unde instalarea driverului actual nu este posibilă.

Citiți numele exact al driverului înregistrat de pe gazda dvs., așa cum este descris în
[Instalați driverul ODBC pe gazda digna](overview.md#install-the-driver).

---

## 2. Proprietăți ODBC {: #2-odbc-properties }

!!! important "Un exemplu, nu o specificație"

    Setul de mai jos este o combinație despre care se știe că funcționează. Proprietățile aparțin
    driverului ODBC Microsoft, astfel încât numele, valorile implicite și valorile acceptate diferă
    între versiunile de driver — de exemplu, Driver 18 criptează implicit, spre deosebire de
    Driver 17 — și între platforme. Folosiți-l ca punct de plecare și consultați documentația
    versiunii de driver pe care ați instalat-o.

Adăugați următoarele proprietăți în ecranul **Add DB Connection**:

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Trebuie să corespundă numelui driverului înregistrat pe gazda *digna* |
| `SERVER` | `sql.example.com` | Numele serverului sau adresa IP. Instanțe cu nume: `host\instance`; un port non-implicit: `host,1433` |
| `PORT` | `1433` | Omiteți atunci când portul face deja parte din `SERVER` |
| `DATABASE` | `digna_source_db` | Baza de date care conține schemele sursă. Este singura bază de date pe care această conexiune o poate profila |
| `UID` | `digna_source_user` | Utilizatorul bazei de date |
| `PWD` | `<password>` | Bifați **Encrypted** |

Șirul de conexiune rezultat arată astfel:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Criptarea cu ODBC Driver 18

Driver 18 criptează implicit conexiunile și validează certificatul serverului. Pentru un server cu
un certificat în care gazda *digna* nu are încredere — de obicei un certificat autosemnat —
conectarea eșuează cu o eroare de lanț de certificate. Adăugați:

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `Encrypt` | `yes` | Implicit în Driver 18; setați `no` doar dacă serverul nu poate folosi TLS |
| `TrustServerCertificate` | `yes` | Omite validarea certificatului. Comod în mediile de test; în producție preferați instalarea certificatului |

### Autentificare Windows

Pentru a vă conecta cu contul care rulează serviciul *digna* în loc de un login SQL, eliminați
`UID` și `PWD` și adăugați:

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `Trusted_Connection` | `yes` | Contul de serviciu *digna* are nevoie de drepturile pe baza de date |

---

## 3. Configurația *digna* {: #3-digna-configuration }

În ecranul **Add DB Connection**, furnizați următoarele:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Note despre MS SQL Server {: #4-notes-on-ms-sql-server }

- **O conexiune vede o singură bază de date.** *digna* oferă schemele bazei de date numite în
  `DATABASE`, deoarece SQL Server raportează ca și catalog doar baza de date curentă. Tabelele
  sursă dintr-o altă bază de date au nevoie de propria conexiune.
- **Moduri de profilare.** *Permanent* creează tabelele de lucru în **Work Schema**, deci
  utilizatorul are nevoie de `CREATE TABLE` acolo. *Session* folosește tabele temporare locale
  (`#wt_…`) în `tempdb` și nu atinge **Work Schema**. *Standard* necesită doar acces de citire.
- **`SERVER` conține instanța și portul.** Cu o instanță cu nume, `host\instance` necesită ca
  serviciul SQL Server Browser să fie accesibil; `host,port` evită acest lucru.

---

## 5. Verificarea driverului (opțional) {: #5-verifying-the-driver-optional }

Configurarea unei surse de date ODBC nu este necesară pentru o conexiune fără DSN, dar asistentul
propriu al driverului este o modalitate comodă de a confirma că driverul funcționează și că
serverul acceptă acreditările înainte de a le introduce în *digna*.

#### Pasul 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Faceți clic pe butonul **Next >**.

#### Pasul 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Alegeți metoda de autentificare (de ex. nume de utilizator și parolă)
și furnizați datele necesare.

Faceți clic pe butonul **Next >**.

#### Pasul 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Alegeți setările conforme ANSI, apoi faceți clic pe butonul **Next >**.

#### Pasul 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Puteți păstra setările implicite sau alege opțiunile de logging necesare
și faceți clic pe butonul **Finish**.

#### Pasul 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Acum faceți clic pe butonul **Test datasource**.

#### Pasul 6
![Step 6](images/sqlserver/create_odbc_data_source_step6.png)

Un ecran de succes confirmă că driverul și acreditările funcționează. Valorile introduse sunt
exact valorile pe care le iau proprietățile din [secțiunea 2](#2-odbc-properties).