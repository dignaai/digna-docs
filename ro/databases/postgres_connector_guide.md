# Conector sursă pentru PostgreSQL

Acest ghid descrie cum să configurați *digna* pentru a se conecta la PostgreSQL prin **ODBC**,
folosind un șir de conexiune **fără DSN** (DSN-less).

Partea *digna* a configurării este aceeași pentru orice tehnologie — unde se creează conexiunile,
cum sunt criptate valorile proprietăților, cum se testează o conexiune și ce înseamnă modurile de
profilare. Aceasta este descrisă în [Prezentarea conexiunilor la baze de date](overview.md). Această
pagină acoperă ceea ce este specific PostgreSQL.

---

## 1. Instalați driverul ODBC {: #1-install-the-odbc-driver }

Instalați driverul ODBC pentru PostgreSQL (**psqlODBC**) pe mașina care rulează backend-ul *digna*,
urmând ghidul oficial de instalare al furnizorului.

Driverul se înregistrează sub un nume care diferă în funcție de platformă și pachet — de obicei
**PostgreSQL Unicode(x64)** pe Windows și **PostgreSQL ODBC Driver(UNICODE)** pe Linux. Citiți
numele exact de pe gazda dvs., așa cum este descris în
[Instalați driverul ODBC pe gazda digna](overview.md#install-the-driver), și folosiți acel nume
pentru proprietatea `DRIVER` de mai jos.

---

## 2. Proprietăți ODBC {: #2-odbc-properties }

!!! important "Un exemplu, nu o specificație"

    Setul de mai jos este o combinație despre care se știe că funcționează. Proprietățile aparțin
    driverului psqlODBC, astfel încât numele, valorile implicite și valorile acceptate diferă între
    versiunile de driver și platforme, iar cerințele serverului dvs. — în special SSL — pot fi și ele
    diferite. Folosiți-l ca punct de plecare și consultați documentația versiunii de driver pe care
    ați instalat-o.

Adăugați următoarele proprietăți în ecranul **Add DB Connection**:

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Trebuie să corespundă numelui driverului înregistrat pe gazda *digna* |
| `SERVER` | `db.example.com` | Numele serverului sau adresa IP |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Baza de date care conține schemele sursă. Este singura bază de date pe care această conexiune o poate profila |
| `UID` | `digna_source_user` | Utilizatorul bazei de date |
| `PWD` | `<password>` | Bifați **Encrypted** |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` sau `verify-full` — trebuie să fie acceptat de server |

Șirul de conexiune rezultat arată astfel:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Orice altă opțiune psqlODBC poate fi adăugată ca proprietate suplimentară — de exemplu
`ReadOnly=1` pentru o sesiune doar în citire, sau `ConnSettings` pentru a rula instrucțiuni `SET`
la conectare.

---

## 3. Configurația *digna* {: #3-digna-configuration }

În ecranul **Add DB Connection**, furnizați următoarele:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Note despre PostgreSQL {: #4-notes-on-postgresql }

- **`SSLMode` trebuie să corespundă serverului.** Un server configurat cu `hostssl` respinge
  `SSLMode=disable`, iar `verify-ca` sau `verify-full` necesită în plus ca certificatul rădăcină să
  fie disponibil driverului pe gazda *digna*. Dacă a trebuit să alegeți un anumit mod la testarea
  driverului, folosiți-l pe același aici.
- **O conexiune vede o singură bază de date.** *digna* oferă schemele bazei de date numite în
  `DATABASE`, deoarece PostgreSQL raportează ca și catalog doar baza de date curentă. Tabelele sursă
  dintr-o altă bază de date au nevoie de propria conexiune.
- **Moduri de profilare.** *Permanent* creează tabelele de lucru în **Work Schema**, deci utilizatorul
  are nevoie de `CREATE` pe acea schemă. *Session* folosește `CREATE TEMPORARY TABLE` și nu atinge
  **Work Schema**. *Standard* necesită doar acces de citire.

---

## 5. Verificarea driverului (opțional) {: #5-verifying-the-driver-optional }

Configurarea unei surse de date ODBC nu este necesară pentru o conexiune fără DSN, dar dialogul
propriu al driverului este o modalitate comodă de a confirma că driverul funcționează și că serverul
acceptă acreditările și modul SSL înainte de a le introduce în *digna*.

#### Pasul 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

#### Pasul 2 – Testați conexiunea

Faceți clic pe butonul **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

Valorile introduse aici sunt exact valorile pe care le iau proprietățile din
[secțiunea 2](#2-odbc-properties).