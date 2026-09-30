---
title: Conector Azure Synapse – Integrare bază de date | Documentația digna
description: Configurați digna pentru a se conecta la Azure Synapse Analytics prin ODBC cu un șir de conexiune fără DSN. Acceptă pool-uri SQL serverless și dedicate, cu proprietățile ODBC necesare și setările de conexiune din digna.
image: /assets/logo_square.png
---


# Conector sursă pentru Azure Synapse Analytics

Acest ghid descrie cum să configurați *digna* pentru a se conecta la Azure Synapse Analytics prin
**ODBC**, folosind un șir de conexiune **fără DSN** (DSN-less). Sunt acceptate atât pool-urile SQL
serverless, cât și cele dedicate.

Partea *digna* a configurării este aceeași pentru orice tehnologie — unde se creează conexiunile,
cum sunt criptate valorile proprietăților, cum se testează o conexiune și ce înseamnă modurile de
profilare. Aceasta este descrisă în [Prezentarea conexiunilor la baze de date](overview.md). Această
pagină acoperă ceea ce este specific Azure Synapse.

!!! note "Tehnologie"

    Synapse folosește dialectul SQL Server, astfel încât conexiunea se creează cu **Technology:
    SQL Server**. Consultați [MS SQL Server](sqlserver_connector_guide.md) pentru un server
    on-premises.

---

## 1. Instalați driverul ODBC {: #1-install-the-odbc-driver }

Instalați **ODBC Driver 18 for SQL Server** pe mașina care rulează backend-ul *digna*, urmând
[ghidul de instalare Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server),
și citiți numele exact al driverului înregistrat de pe gazda dvs., așa cum este descris în
[Instalați driverul ODBC pe gazda digna](overview.md#install-the-driver).

---

## 2. Proprietăți ODBC {: #2-odbc-properties }

!!! important "Un exemplu, nu o specificație"

    Setul de mai jos este o combinație despre care se știe că funcționează. Proprietățile aparțin
    driverului ODBC Microsoft, astfel încât numele, valorile implicite și valorile acceptate diferă
    între versiunile de driver și platforme, iar cerințele workspace-ului depind de modul în care
    este configurat — tipul de pool, metoda de autentificare, firewall-ul. Folosiți-l ca punct de
    plecare și consultați documentația versiunii de driver pe care ați instalat-o.

Adăugați următoarele proprietăți în ecranul **Add DB Connection**:

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Trebuie să corespundă numelui driverului înregistrat pe gazda *digna* |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Numele workspace-ului plus sufixul endpoint-ului — vezi mai jos |
| `DATABASE` | `dignadata` | Baza de date care conține schemele sursă. Este singura bază de date pe care această conexiune o poate profila |
| `UID` | `sqladminuser` | Login SQL |
| `PWD` | `<password>` | Bifați **Encrypted** |

Șirul de conexiune rezultat arată astfel:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### Valoarea `SERVER`

Luați numele workspace-ului Synapse și adăugați sufixul endpoint-ului:

| Pool | `SERVER` |
|---|---|
| **Serverless SQL pool** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Dedicated SQL pool** | `<workspace>.sql.azuresynapse.net` |

!!! warning "Partea `-ondemand` este ușor de omis"

    Fără ea, numele se rezolvă la endpoint-ul dedicat, iar conexiunea fie eșuează, fie ajunge în
    mod silențios la un alt pool decât cel intenționat. Ambele endpoint-uri sunt afișate pe pagina
    de prezentare generală a workspace-ului în portalul Azure.

### Firewall

Firewall-ul workspace-ului Synapse trebuie să permită adresa de ieșire a gazdei *digna*. Adăugați-o
sub **Networking** în workspace înainte de a testa conexiunea — o adresă blocată apare ca un
timeout de conexiune, nu ca o eroare de autentificare.

### Autentificare Microsoft Entra ID

În locul unui login SQL, driverul se poate autentifica prin Entra ID. Înlocuiți `UID`/`PWD` cu
metoda de autentificare pe care o așteaptă workspace-ul dvs., de exemplu:

| Cheie | Valoare exemplu | Note |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | `UID` primește atunci ID-ul aplicației (client), iar `PWD` client secret-ul |
| `Authentication` | `ActiveDirectoryMSI` | Identitatea gestionată (managed identity) a gazdei *digna*, fără acreditări |

---

## 3. Configurația *digna* {: #3-digna-configuration }

În ecranul **Add DB Connection**, furnizați următoarele:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Note despre Azure Synapse {: #4-notes-on-azure-synapse }

- **Pool-urile serverless acceptă doar profilarea *Standard*.** Un serverless SQL pool nu poate
  crea tabele într-o bază de date, deci nu poate rula nici profilarea *Permanent*, nici *Session*.
  *Standard* calculează metricile direct pe sursă, ceea ce este și opțiunea mai ieftină, deoarece
  serverless este facturat în funcție de datele procesate.
- **O conexiune vede o singură bază de date.** *digna* oferă schemele bazei de date numite în
  `DATABASE`, deoarece Synapse, ca și SQL Server, raportează ca și catalog doar baza de date
  curentă.
- **Criptarea este activată implicit** în Driver 18, iar endpoint-urile Synapse prezintă
  certificate publice valide, deci nu este necesară nicio proprietate `Encrypt` sau
  `TrustServerCertificate`.
- **Un endpoint serverless își poate relua activitatea după inactivitate** la prima conectare. Dacă
  testul conexiunii expiră pe un pool care nu a fost folosit de ceva timp, reîncercați.

---

## 5. Verificarea driverului (opțional) {: #5-verifying-the-driver-optional }

Configurarea unei surse de date ODBC nu este necesară pentru o conexiune fără DSN, dar asistentul
propriu al driverului este o modalitate comodă de a confirma că driverul funcționează și că
workspace-ul acceptă acreditările înainte de a le introduce în *digna*.

#### Pasul 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Completați câmpul „Server”.
Folosiți numele workspace-ului Synapse și extindeți-l cu „.sql.azuresynapse.net”.  
**Atenție**: dacă doriți să vă conectați folosind un serverless SQL pool, asigurați-vă că includeți
„-ondemand”, așa cum se arată în captura de ecran de mai sus.

Faceți clic pe butonul **Next >**.

#### Pasul 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Alegeți metoda de autentificare (de ex. nume de utilizator și parolă)
și furnizați datele necesare.

Faceți clic pe butonul **Next >**.

#### Pasul 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Alegeți setările conforme ANSI, apoi faceți clic pe butonul **Next >**.

#### Pasul 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Puteți păstra setările implicite sau alege opțiunile necesare
și faceți clic pe butonul **Finish**.

#### Pasul 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Acum faceți clic pe butonul **Test datasource**.

#### Pasul 6
![Step 6](images/azure_synapse/create_odbc_data_source_step6.png)

Un ecran de succes confirmă că driverul, endpoint-ul și acreditările funcționează. Valorile
introduse sunt exact valorile pe care le iau proprietățile din [secțiunea 2](#2-odbc-properties).
