---
title: Conector Netezza – Integrare bază de date | Documentația digna
description: Configurați digna pentru a se conecta la Netezza prin ODBC cu un șir de conexiune fără DSN. Acoperă driverul NetezzaSQL, proprietățile ODBC necesare și setările de conexiune din digna.
image: /assets/logo_square.png
---


# Conector sursă pentru Netezza

Acest ghid descrie cum să configurați *digna* pentru a se conecta la Netezza prin **ODBC**,
folosind un șir de conexiune **fără DSN** (DSN-less).

Partea *digna* a configurării este aceeași pentru orice tehnologie — unde se creează conexiunile,
cum sunt criptate valorile proprietăților, cum se testează o conexiune și ce înseamnă modurile de
profilare. Aceasta este descrisă în [Prezentarea conexiunilor la baze de date](overview.md). Această
pagină acoperă ceea ce este specific Netezza.

---

## 1. Instalați driverul ODBC {: #1-install-the-odbc-driver }

Instalați driverul ODBC **NetezzaSQL** (parte a instrumentelor client IBM Netezza) pe mașina care
rulează backend-ul *digna*, urmând ghidul oficial de instalare al furnizorului.

Citiți numele exact al driverului înregistrat de pe gazda dvs., așa cum este descris în
[Instalați driverul ODBC pe gazda digna](overview.md#install-the-driver).

---

## 2. Proprietăți ODBC {: #2-odbc-properties }

!!! important "Un exemplu, nu o specificație"

    Setul de mai jos este o combinație despre care se știe că funcționează. Proprietățile aparțin
    driverului NetezzaSQL, astfel încât numele, valorile implicite și valorile acceptate diferă
    între versiunile de client și platforme, iar un appliance securizat cu TLS are nevoie de mai
    mult decât proprietățile prezentate aici. Folosiți-l ca punct de plecare și consultați
    documentația versiunii de client pe care ați instalat-o.

Adăugați următoarele proprietăți în ecranul **Add DB Connection**:

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Trebuie să corespundă numelui driverului înregistrat pe gazda *digna*. Acoladele sunt modul obișnuit de a scrie acest nume |
| `SERVER` | `netezza.example.com` | Numele serverului sau adresa IP |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Baza de date în care pornește sesiunea |
| `UID` | `ADMIN` | Utilizatorul bazei de date |
| `PWD` | `<password>` | Bifați **Encrypted** |

Șirul de conexiune rezultat arată astfel:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

În funcție de versiunea driverului, de configurare și de cerințele de securitate, pot fi necesare
și alte proprietăți — de exemplu `SecurityLevel` și `CaCertFile` pentru un appliance securizat cu
TLS. Orice opțiune oferită de dialogurile *Advanced*, *SSL* și *Driver* ale driverului poate fi
adăugată ca proprietate.

---

## 3. Configurația *digna* {: #3-digna-configuration }

În ecranul **Add DB Connection**, furnizați următoarele:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Note despre Netezza {: #4-notes-on-netezza }

- **Se aplică atât cataloagele, cât și schemele.** *digna* listează bazele de date pe care
  utilizatorul le poate vedea (din `_V_DATABASE`) ca și cataloage, iar schemele lor (din
  `_V_SCHEMA`) sub acestea, astfel încât o conexiune poate deservi surse din mai multe baze de
  date. `DATABASE` decide doar unde pornește sesiunea.
- **Identificatorii sunt scriși cu majuscule**, cu excepția cazului în care au fost creați între
  ghilimele, motiv pentru care exemplele de mai sus folosesc `TEST` și `ADMIN`.
- **Moduri de profilare.** *Permanent* creează tabelele de lucru în **Work Schema**, deci
  utilizatorul are nevoie de `CREATE TABLE` acolo. *Session* folosește `CREATE TEMPORARY TABLE` și
  nu atinge **Work Schema**. *Standard* necesită doar acces de citire.

---

## 5. Verificarea driverului (opțional) {: #5-verifying-the-driver-optional }

Configurarea unei surse de date ODBC nu este necesară pentru o conexiune fără DSN, dar dialogul
propriu al driverului este o modalitate comodă de a confirma că driverul și acreditările
funcționează înainte de a le introduce în *digna*.

#### Pasul 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Câmpurile din **DSN Options** corespund unu-la-unu proprietăților din
[secțiunea 2](#2-odbc-properties). În funcție de driverul Netezza, de configurare și de cerințele
de securitate, este posibil să aveți nevoie și de date în filele **Advanced DSN Options**,
**SSL DSN Options** sau **Driver Options**; pentru cea mai simplă configurare, **DSN Options** este
suficient.

Faceți clic pe butonul **Test Connection**.

#### Pasul 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Când primiți ecranul de succes, driverul funcționează și valorile sunt corecte.
