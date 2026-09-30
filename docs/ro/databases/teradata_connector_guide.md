---
title: Conector Teradata – Integrare bază de date | Documentația digna
description: Configurați digna pentru a se conecta la Teradata prin ODBC cu un șir de conexiune fără DSN. Acoperă driverul Teradata ODBC, proprietatea DBCNAME, mecanismele de logon și setările de conexiune din digna.
image: /assets/logo_square.png
---


# Conector sursă pentru Teradata

Acest ghid descrie cum să configurați *digna* pentru a se conecta la Teradata prin **ODBC**,
folosind un șir de conexiune **fără DSN** (DSN-less).

Partea *digna* a configurării este aceeași pentru orice tehnologie — unde se creează conexiunile,
cum sunt criptate valorile proprietăților, cum se testează o conexiune și ce înseamnă modurile de
profilare. Aceasta este descrisă în [Prezentarea conexiunilor la baze de date](overview.md). Această
pagină acoperă ceea ce este specific Teradata.

---

## 1. Instalați driverul ODBC {: #1-install-the-odbc-driver }

Instalați **ODBC Driver for Teradata** pe mașina care rulează backend-ul *digna*, urmând ghidul
oficial de instalare al furnizorului.

Driverul se înregistrează cu versiunea inclusă în nume, de exemplu
**Teradata Database ODBC Driver 20.00**. Citiți numele exact înregistrat de pe gazda dvs., așa cum
este descris în [Instalați driverul ODBC pe gazda digna](overview.md#install-the-driver).

---

## 2. Proprietăți ODBC {: #2-odbc-properties }

!!! important "Un exemplu, nu o specificație"

    Setul de mai jos este o combinație despre care se știe că funcționează. Proprietățile aparțin
    driverului Teradata ODBC, astfel încât numele, valorile implicite și valorile acceptate diferă
    între versiunile de driver — versiunea face parte chiar din numele driverului — și între
    platforme. Folosiți-l ca punct de plecare și consultați documentația versiunii de driver pe
    care ați instalat-o.

Adăugați următoarele proprietăți în ecranul **Add DB Connection**:

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Trebuie să corespundă numelui driverului înregistrat pe gazda *digna* |
| `DBCNAME` | `teradata.example.com` | Numele serverului sau adresa IP. Denumirea proprie Teradata pentru proprietatea gazdei |
| `UID` | `digna_source_user` | Utilizatorul bazei de date |
| `PWD` | `<password>` | Bifați **Encrypted** |

Șirul de conexiune rezultat arată astfel:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Proprietăți suplimentare utile:

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `MechanismName` | `TD2` | Mecanismul de logon. `TD2` este implicit în Teradata; folosiți `LDAP` pentru autentificarea prin director |
| `DefaultDatabase` | `dad` | Baza de date în care pornește sesiunea |
| `CharacterSet` | `UTF8` | Setați-o acolo unde setul de caractere implicit al sesiunii ar deteriora datele non-ASCII |

---

## 3. Configurația *digna* {: #3-digna-configuration }

În ecranul **Add DB Connection**, furnizați următoarele:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Note despre Teradata {: #4-notes-on-teradata }

- **O bază de date Teradata este un catalog, nu o schemă.** *digna* listează bazele de date pe care
  utilizatorul le poate vedea (din `DBC.DatabasesV`) ca și cataloage, iar nivelul de schemă nu se
  aplică. Când adăugați o sursă de date, alegeți baza de date ca și catalog; schema este raportată
  ca *not applicable*.
- **O conexiune ajunge la fiecare bază de date permisă**, astfel încât o singură conexiune poate
  deservi surse din mai multe baze de date — spre deosebire de tehnologiile la care conexiunea este
  legată de o singură bază de date.
- **Work Schema este o bază de date.** Pentru profilarea *Permanent*, indicați baza de date Teradata
  care conține tabelele de lucru și acordați utilizatorului drepturi `CREATE TABLE`, plus o alocare
  de spațiu `PERM` în ea — o bază de date cu spațiu perm zero nu poate conține un tabel.
- **Moduri de profilare.** *Permanent* creează tabele în **Work Schema**. *Session* folosește un
  tabel `VOLATILE`, care necesită spațiu `SPOOL`, dar nu spațiu perm și nici drepturi în
  **Work Schema**. *Standard* necesită doar acces de citire.

---

## 5. Verificarea driverului (opțional) {: #5-verifying-the-driver-optional }

Configurarea unei surse de date ODBC nu este necesară pentru o conexiune fără DSN, dar dialogul
propriu al driverului este o modalitate comodă de a confirma că driverul și acreditările
funcționează înainte de a le introduce în *digna*.

#### Pasul 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Câmpul **Name or IP address** de aici este proprietatea `DBCNAME` din
[secțiunea 2](#2-odbc-properties).

Faceți clic pe butonul **Test**.

#### Pasul 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Introduceți numele de utilizator și parola, apoi faceți clic pe butonul **OK**. Un ecran de succes
confirmă că driverul și acreditările funcționează.
