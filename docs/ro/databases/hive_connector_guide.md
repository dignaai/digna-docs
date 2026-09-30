---
title: Conector Apache Hive – Integrare bază de date | Documentația digna
description: Configurați digna pentru a se conecta la Apache Hive prin ODBC cu un șir de conexiune fără DSN. Acoperă driverul Cloudera Hive ODBC, mecanismele de autentificare, modurile de transport și setările de conexiune din digna.
image: /assets/logo_square.png
---


# Conector sursă pentru Hive

Acest ghid descrie cum să configurați *digna* pentru a se conecta la Apache Hive prin **ODBC**,
folosind un șir de conexiune **fără DSN** (DSN-less).

Partea *digna* a configurării este aceeași pentru orice tehnologie — unde se creează conexiunile,
cum sunt criptate valorile proprietăților, cum se testează o conexiune și ce înseamnă modurile de
profilare. Aceasta este descrisă în [Prezentarea conexiunilor la baze de date](overview.md). Această
pagină acoperă ceea ce este specific Hive.

---

## 1. Instalați driverul ODBC {: #1-install-the-odbc-driver }

Instalați **Cloudera ODBC Driver for Apache Hive** pe mașina care rulează backend-ul *digna*,
urmând ghidul oficial de instalare al furnizorului.

Citiți numele exact al driverului înregistrat de pe gazda dvs., așa cum este descris în
[Instalați driverul ODBC pe gazda digna](overview.md#install-the-driver).

---

## 2. Proprietăți ODBC {: #2-odbc-properties }

!!! important "Un exemplu, nu o specificație"

    Setul de mai jos este o combinație despre care se știe că funcționează. Proprietățile aparțin
    driverului Cloudera Hive, astfel încât numele, valorile implicite și valorile acceptate diferă
    între versiunile de driver și platforme, iar ce acceptă HiveServer2 depinde în întregime de
    modul în care este securizat clusterul — mecanismul de autentificare, modul de transport, TLS,
    gateway. Folosiți-l ca punct de plecare și consultați documentația versiunii de driver pe care
    ați instalat-o.

Adăugați următoarele proprietăți în ecranul **Add DB Connection**:

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Trebuie să corespundă numelui driverului înregistrat pe gazda *digna* |
| `HOST` | `hive.example.com` | Numele gazdei sau adresa IP a HiveServer2 |
| `PORT` | `10000` | Portul HiveServer2; `10001` pentru transport HTTP |

Șirul de conexiune rezultat arată astfel:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Autentificare

Un HiveServer2 nesecurizat acceptă cele trei proprietăți de mai sus așa cum sunt. Acolo unde
autentificarea este activată, adăugați:

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `AuthMech` | `3` | `0` fără autentificare, `2` doar nume de utilizator, `3` nume de utilizator și parolă, `1` Kerberos |
| `UID` | `digna_source_user` | Necesar pentru `AuthMech` `2` și `3` |
| `PWD` | `<password>` | Necesar pentru `AuthMech` `3`. Bifați **Encrypted** |

Pentru Kerberos (`AuthMech=1`), gazda *digna* are nevoie în plus de un ticket valid sau de un
keytab, precum și de proprietățile `KrbHostFQDN`, `KrbServiceName` și `KrbRealm` documentate de
driver.

### Transport și TLS

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `ThriftTransport` | `2` | `0` binar (implicit, portul 10000), `1` SASL, `2` HTTP (portul 10001, și ceea ce așteaptă un gateway Knox) |
| `HTTPPath` | `cliservice` | Cu `ThriftTransport=2` |
| `SSL` | `1` | Acolo unde HiveServer2 este securizat cu TLS |
| `Schema` | `dignadata` | Baza de date Hive în care pornește sesiunea. Opțional — *digna* își califică interogările |

---

## 3. Configurația *digna* {: #3-digna-configuration }

În ecranul **Add DB Connection**, furnizați următoarele:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Note despre Hive {: #4-notes-on-hive }

- **Cataloagele provin de la driver.** Hive nu are un catalog propriu, astfel încât *digna* preia
  ceea ce raportează driverul — de obicei o singură intrare numită `HIVE` — și listează bazele de
  date Hive ca scheme sub aceasta.
- **Work Schema este o bază de date Hive.** Pentru profilarea *Permanent*, utilizatorul are nevoie
  de dreptul de a crea și șterge tabele în ea, iar locația de stocare subiacentă trebuie să permită
  scrierea.
- **Moduri de profilare.** *Permanent* creează tabelele de lucru în **Work Schema**. *Session*
  folosește `CREATE TEMPORARY TABLE`, ceea ce necesită un HiveServer2 care acceptă tabele temporare,
  și nu atinge **Work Schema**. *Standard* necesită doar acces de citire și este modul de ales pe un
  cluster unde *digna* nu are deloc acces de scriere.
- **Profilarea este un set de interogări, nu o scanare.** Fiecare statistică este calculată de
  HiveServer2, deci coada în care trimite interogări utilizatorul *digna* ar trebui să aibă
  suficientă capacitate pentru fereastra de inspecție.

---

## 5. Verificarea driverului (opțional) {: #5-verifying-the-driver-optional }

Configurarea unei surse de date ODBC nu este necesară pentru o conexiune fără DSN, dar dialogul
propriu al driverului este o modalitate comodă de a confirma că driverul, modul de transport și
acreditările funcționează înainte de a le introduce în *digna*.

#### Pasul 1
![Step 1](images/hive/create_odbc_data_source_step1.png)

Câmpurile **Host**, **Port**, **Database**, **Mechanism** și **Thrift Transport** de aici sunt
proprietățile `HOST`, `PORT`, `Schema`, `AuthMech` și `ThriftTransport` din
[secțiunea 2](#2-odbc-properties).

#### Pasul 2 – Testați conexiunea

Introduceți parola și faceți clic pe butonul **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

După un test reușit, faceți clic pe butonul **OK**.
