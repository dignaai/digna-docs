# Conector sursă pentru Oracle

Acest ghid descrie cum să configurați *digna* pentru a se conecta la Oracle Database prin **ODBC**,
folosind un șir de conexiune **fără DSN** (DSN-less).

Partea *digna* a configurării este aceeași pentru orice tehnologie — unde se creează conexiunile,
cum sunt criptate valorile proprietăților, cum se testează o conexiune și ce înseamnă modurile de
profilare. Aceasta este descrisă în [Prezentarea conexiunilor la baze de date](overview.md). Această
pagină acoperă ceea ce este specific Oracle.

---

## 1. Instalați driverul ODBC {: #1-install-the-odbc-driver }

Driverul Oracle ODBC face parte din **Oracle Client** (pachetul „ODBC” al Instant Client este
suficient). Instalați-l pe mașina care rulează backend-ul *digna*, urmând ghidul oficial de
instalare al furnizorului.

Driverul se înregistrează ca **Oracle in `<OracleHomeName>`** — de exemplu
`Oracle in OraDB21Home1` sau `Oracle in instantclient_21_13`. Numele home-ului diferă de la o
instalare la alta, așa că citiți numele exact de pe gazda dvs., așa cum este descris în
[Instalați driverul ODBC pe gazda digna](overview.md#install-the-driver).

---

## 2. Proprietăți ODBC {: #2-odbc-properties }

!!! important "Un exemplu, nu o specificație"

    Setul de mai jos este o combinație despre care se știe că funcționează. Proprietățile aparțin
    driverului Oracle ODBC, astfel încât numele, valorile implicite și valorile acceptate diferă
    între versiunile de client, iar numele driverului în special depinde de Oracle home-ul de pe
    gazda dvs. Folosiți-l ca punct de plecare și consultați documentația versiunii de client pe
    care ați instalat-o.

Adăugați următoarele proprietăți în ecranul **Add DB Connection**:

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Trebuie să corespundă numelui driverului înregistrat pe gazda *digna* |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Baza de date la care vă conectați — vezi mai jos |
| `UID` | `DIGNA_SOURCE_USER` | Utilizatorul bazei de date |
| `PWD` | `<password>` | Bifați **Encrypted** |

Șirul de conexiune rezultat arată astfel:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### Valoarea `DBQ`

`DBQ` acceptă trei forme. Ele sunt echivalente pentru *digna*; diferă prin ceea ce trebuie
configurat pe gazda *digna*:

| Formă | Exemplu | Necesită |
|---|---|---|
| **Connect descriptor complet** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Nimic — totul se află în proprietate. Recomandat |
| **Alias TNS** | `DIGNA_SOURCE` | Aliasul trebuie să existe în `tnsnames.ora` al Oracle Client de pe gazda *digna* |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Un Oracle Client care acceptă Easy Connect (12c și ulterior) |

!!! tip "Preferați descriptorul complet"

    Un alias TNS mută jumătate din definiția conexiunii într-un fișier de pe gazda *digna*, unde
    este ușor de uitat atunci când gazda este reconstruită sau *digna* este mutată. Descriptorul
    complet păstrează conexiunea autonomă — ceea ce reprezintă scopul unei configurări fără DSN.

Rețineți că parantezele dintr-un descriptor nu pun probleme într-un șir de conexiune, dar dacă
parola conține `;`, încadrați-o între acolade: `PWD={p@ss;word}`.

---

## 3. Configurația *digna* {: #3-digna-configuration }

În ecranul **Add DB Connection**, furnizați următoarele:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Note despre Oracle {: #4-notes-on-oracle }

- **Schemele sunt utilizatori.** *digna* listează utilizatorii Oracle ca scheme, deci schema sursă
  este proprietarul tabelelor — `DIGNA_SOURCE_USER` în exemplul de mai sus. Utilizatorul conexiunii
  are nevoie de `SELECT` pe acele tabele, fie direct, fie printr-un rol.
- **O conexiune vede o singură bază de date.** Catalogul oferit de *digna* este baza de date la
  care este atașată conexiunea, deci `DBQ` decide ce serviciu și, prin urmare, ce bază de date este
  profilată.
- **Identificatorii sunt case-sensitive odată puși între ghilimele.** *digna* pune între ghilimele
  numele pe care le citește din dicționarul de date, adică ceea ce stochează Oracle — majuscule
  pentru obiectele create fără ghilimele.
- **Moduri de profilare.** *Permanent* creează tabelele de lucru în **Work Schema**, deci
  utilizatorul are nevoie de `CREATE TABLE` acolo și de o cotă pe tablespace. *Session* folosește
  un tabel temporar privat (`ORA$PTT_…`, Oracle 18c și ulterior) și nu atinge **Work Schema**.
  *Standard* necesită doar acces de citire.

---

## 5. Verificarea driverului (opțional) {: #5-verifying-the-driver-optional }

Configurarea unei surse de date ODBC nu este necesară pentru o conexiune fără DSN, dar dialogul
propriu al driverului este o modalitate comodă de a confirma că Oracle Client, numele serviciului
și acreditările funcționează înainte de a le introduce în *digna*.

#### Pasul 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

**TNS Service Name** oferit aici provine din `tnsnames.ora` al instalării Oracle Client — acolo
este definit aliasul și, odată cu el, gazda, portul și numele serviciului. În *digna* puteți
folosi aliasul ca `DBQ` sau, în schimb, descriptorul complet.

#### Pasul 2 – Testați conexiunea

Faceți clic pe butonul **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Introduceți parola și faceți clic pe butonul **OK**.

![Step 3](images/oracle/create_odbc_data_source_step3.png)

Un mesaj de succes confirmă că driverul și acreditările funcționează.