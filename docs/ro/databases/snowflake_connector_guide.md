---
title: Conector Snowflake – Integrare bază de date | Documentația digna
description: Configurați digna pentru a se conecta la Snowflake prin ODBC cu un șir de conexiune fără DSN. Acoperă driverul Snowflake ODBC, programmatic access token-urile, alegerea warehouse-ului și a rolului și setările de conexiune din digna.
image: /assets/logo_square.png
---


# Conector sursă pentru Snowflake

Acest ghid descrie cum să configurați *digna* pentru a se conecta la Snowflake prin **ODBC**,
folosind un șir de conexiune **fără DSN** (DSN-less).

Partea *digna* a configurării este aceeași pentru orice tehnologie — unde se creează conexiunile,
cum sunt criptate valorile proprietăților, cum se testează o conexiune și ce înseamnă modurile de
profilare. Aceasta este descrisă în [Prezentarea conexiunilor la baze de date](overview.md). Această
pagină acoperă ceea ce este specific Snowflake.

---

## 1. Instalați driverul ODBC {: #1-install-the-odbc-driver }

Instalați **Snowflake ODBC Driver** pe mașina care rulează backend-ul *digna*, urmând
[ghidul de instalare Snowflake](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

Driverul se înregistrează ca **SnowflakeDSIIDriver**. Citiți numele exact înregistrat de pe gazda
dvs., așa cum este descris în [Instalați driverul ODBC pe gazda digna](overview.md#install-the-driver).

---

## 2. Proprietăți ODBC {: #2-odbc-properties }

Snowflake este accesat cu un **programmatic access token (PAT)** — calea de autentificare pe care
este verificată *digna* și cea pe care Snowflake o impune pentru conturile pe care autentificarea
doar cu parolă este blocată.

!!! important "Un exemplu, nu o specificație"

    Setul de mai jos este o combinație despre care se știe că funcționează. Proprietățile aparțin
    driverului Snowflake ODBC, astfel încât numele, valorile implicite și valorile acceptate diferă
    între versiunile de driver și platforme, iar opțiunile de autentificare permise de contul dvs.
    sunt stabilite de politica de securitate a contului. Folosiți-l ca punct de plecare și
    consultați documentația versiunii de driver pe care ați instalat-o.

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Trebuie să corespundă numelui driverului înregistrat pe gazda *digna* |
| `Server` | `<account>.snowflakecomputing.com` | Identificatorul contului plus sufixul, de ex. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Utilizatorul Snowflake căruia îi aparține token-ul |
| `Database` | `TEST` | Baza de date care conține schemele sursă. Este singura bază de date pe care această conexiune o poate profila |
| `Schema` | `PUBLIC` | Schema implicită a sesiunii |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Selectează autentificarea cu token |
| `token` | `<programmatic access token>` | Bifați **Encrypted** |

Șirul de conexiune rezultat arată astfel:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Warehouse și rol

Interogările au nevoie de un warehouse. Dacă utilizatorul *digna* are un warehouse implicit și un
rol implicit, sesiunea le preia și nu trebuie configurat nimic. În caz contrar, adăugați:

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Warehouse-ul care rulează interogările de profilare |
| `Role` | `DIGNA_READER` | Rolul ale cărui permisiuni le folosește sesiunea |

!!! tip "Oferiți digna propriul warehouse"

    Un warehouse separat, mic, cu suspendare automată, menține vizibil costul profilării și
    împiedică *digna* să concureze cu utilizatorii interactivi pentru resursele de calcul.

### Autentificare cu parolă

Acolo unde contul încă o permite, o parolă funcționează în locul token-ului — eliminați
`authenticator` și `token` și adăugați:

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `PWD` | `<password>` | Bifați **Encrypted** |

---

## 3. Configurația *digna* {: #3-digna-configuration }

În ecranul **Add DB Connection**, furnizați următoarele:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Note despre Snowflake {: #4-notes-on-snowflake }

- **Token-urile expiră.** Un programmatic access token este emis cu o durată de valabilitate, iar
  profilarea se oprește în ziua în care acesta expiră. Notați data de expirare când îl creați și
  reintroduceți noul token în proprietatea `token` — valorile criptate pot fi înlocuite, dar nu pot
  fi citite înapoi.
- **O conexiune vede o singură bază de date.** *digna* oferă schemele bazei de date numite în
  `Database`, deoarece Snowflake raportează ca și catalog doar baza de date curentă. Tabelele sursă
  dintr-o altă bază de date au nevoie de propria conexiune.
- **Identificatorii sunt scriși cu majuscule**, cu excepția cazului în care au fost creați între
  ghilimele. *digna* folosește numele așa cum le raportează Snowflake.
- **Moduri de profilare.** *Permanent* creează tabelele de lucru în **Work Schema**, deci rolul are
  nevoie de `CREATE TABLE` acolo. *Session* folosește `CREATE TEMPORARY TABLE` și nu atinge
  **Work Schema**. *Standard* necesită doar acces de citire — și nicio permisiune de scriere.

---

## 5. Verificarea driverului (opțional) {: #5-verifying-the-driver-optional }

Configurarea unei surse de date ODBC nu este necesară pentru o conexiune fără DSN, dar dialogul
propriu al driverului este o modalitate comodă de a confirma că driverul, URL-ul contului și
acreditările funcționează înainte de a le introduce în *digna*.

#### Pasul 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Note:

- Valoarea pentru **Server** constă din identificatorul contului Snowflake urmat de
  `.snowflakecomputing.com`.
- **Database**, **Schema** și **Warehouse** introduse aici corespund proprietăților `Database`,
  `Schema` și `Warehouse` din [secțiunea 2](#2-odbc-properties).

#### Pasul 2 – Testați conexiunea

Faceți clic pe butonul **TEST**. O conexiune reușită ar trebui să arate astfel:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)
