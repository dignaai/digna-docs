---
title: digna CLI Reference 2025.04 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2025.04. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, and more.
image: /assets/logo_square.png
---

# digna CLI Reference 2025.04
**2025-04-01**

Această pagină documentează setul complet de comenzi disponibile în CLI-ul ***digna***, release **2025.04**, inclusiv exemple de utilizare și opțiuni.

---

## CLI Basics

---

## Using `help` Option

Opțiunea `--help` oferă informații despre comenzile disponibile și despre modul lor de utilizare. Există două moduri principale de a folosi această opțiune:

1. **Afișarea ajutorului general:**
   
    Folosiți `--help` imediat după cuvântul cheie `dignacli`  
   ```bash
   dignacli --help
   ```

2. **Obținerea ajutorului pentru comenzi specifice:**  
  
    Pentru informații detaliate despre o comandă anume, adăugați `--help` la sfârșitul comenzii respective.  
    De exemplu, pentru a obține ajutor pentru comanda `add-user`, rulați:
     ```bash
     dignacli add-user --help
     ```

     ### ieșire:
      
     - **Descrierea comenzii:** Oferă o descriere detaliată a funcționalității comenzii.  
     - **Sintaxă:** Afișează sintaxa exactă, incluzând argumentele obligatorii și opționale.  
     - **Opțiuni:** Listează opțiunile specifice comenzii, împreună cu explicațiile lor.  
     - **Exemple:** Oferă exemple despre cum să executați comanda în mod eficient.

  
## Using `check-repo-connection` Command

Comanda `check-repo-connection` este un utilitar din CLI-ul ***digna*** conceput pentru a testa conectivitatea și accesul la un depozit ***digna*** specific. Această comandă se asigură că CLI-ul poate interacționa cu depozitul.
      
#### Command Usage
```bash
dignacli check-repo-connection
```

La executare cu succes, comanda afișează o confirmare a conexiunii, împreună cu detalii despre depozit: versiunea Repository, Host, Database și Schema.  
  
Dacă conexiunea la depozit nu reușește, verificați fișierul config.toml pentru setările corecte de configurare.

## Using ‘version’ command

Pentru a verifica versiunea instalată a *dignacli*, folosiți opțiunea `--version`.  
  
#### Command Usage
```bash
dignacli --version
```
  
#### Example Output
```bash
dignacli version 2025.04
```

## Using logging options
  
În mod implicit, ieșirea în consolă a comenzilor ***digna*** este concepută să fie minimală. Majoritatea comenzilor oferă posibilitatea de a furniza informații suplimentare, folosind următoarele opțiuni:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose” și „debug” definesc nivelul de detaliu, în timp ce comutatorul „logfile” permite redirecționarea ieșirii către un fișier în loc de fereastra consolă.

## User Management

### Using ‘add-user’ command
  
Comanda `add-user` din CLI-ul ***digna*** este folosită pentru a adăuga un utilizator nou în sistemul ***digna***.
  
#### Command Usage
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Arguments

- **USER_NAME**: Numele de utilizator pentru noul utilizator (obligatoriu).
- **USER_FULL_NAME**: Numele complet al noului utilizator (obligatoriu).
- **USER_PASSWORD**: Parola pentru noul utilizator (obligatoriu).

#### Options

- `--is_superuser`, `-su`: Flag pentru a desemna noul utilizator ca admin.
- `--valid_until`, `-vu`: Setează o dată de expirare pentru contul utilizatorului în formatul `YYYY-MM-DD HH:MI:SS`. Dacă nu este setat, contul nu are dată de expirare.

#### Example

Pentru a adăuga un utilizator nou cu username `jdoe`, numele complet `John Doe` și parola `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Pentru a adăuga un utilizator nou și a seta o dată de expirare a contului:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Using `delete-user` command
  
Comanda `delete-user` din CLI-ul ***digna*** este folosită pentru a elimina un utilizator existent din sistemul ***digna***.
  
#### Command Usage
```bash
dignacli delete-user USER_NAME
```
  
##### Arguments
- **USER_NAME**: Numele de utilizator al celui care urmează a fi șters (obligatoriu). Acesta este singurul argument necesar comenzii.

#### Example
```bash
dignacli delete-user jdoe
```
  
Executarea acestei comenzi va elimina utilizatorul `jdoe` din sistemul ***digna***, revocându-i accesul și ștergând datele și permisiunile asociate din depozit.

### Using `modify-user` Command

Comanda `modify-user` din CLI-ul ***digna*** este folosită pentru a actualiza detaliile unui utilizator existent în sistemul ***digna***.

#### Command Usage
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Arguments
  
- **USER_NAME**: Numele de utilizator al utilizatorului care urmează a fi modificat (obligatoriu).
- **USER_FULL_NAME**: Noul nume complet pentru utilizator (obligatoriu).
  
#### Options  
  
- `--is_superuser`, `-su`: Setează utilizatorul ca superuser, acordând privilegii sporite. Acest flag nu necesită valoare.  
- `--valid_until`, `-vu`: Setează o dată de expirare pentru contul utilizatorului în formatul YYYY-MM-DD HH:MI:SS. Dacă nu este furnizată, contul rămâne valabil pe termen nelimitat.  
  
#### Example
  
Pentru a modifica numele complet al utilizatorului `jdoe` în „Johnathan Doe” și a seta utilizatorul ca superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Using `modify-user-pwd` Command
  
Comanda `modify-user-pwd` din CLI-ul ***digna*** este folosită pentru a schimba parola unui utilizator existent în sistemul ***digna***.
  
#### Command Usage
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Arguments
  
- **USER_NAME**: Numele de utilizator al utilizatorului a cărui parolă urmează a fi schimbată (obligatoriu).
- **USER_PWD**: Noua parolă pentru utilizator (obligatoriu).
  
#### Example
  
Pentru a schimba parola utilizatorului `jdoe` în `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Using `list-users` Command

Comanda `list-users` din CLI-ul ***digna*** afișează o listă cu toți utilizatorii înregistrați în sistemul ***digna***.

#### Command Usage

```bash
dignacli list-users
```

Executând această comandă în CLI-ul ***digna*** se va conecta la depozitul ***digna*** și va lista toți utilizatorii, afișând ID-ul, username-ul, numele complet, statutul de superuser și timpii de expirare.

## Repository Management

### Using `upgrade-repo` Command
  
Comanda `upgrade-repo` din CLI-ul ***digna*** este folosită pentru a actualiza sau inițializa depozitul ***digna***. Această comandă este esențială pentru aplicarea actualizărilor sau pentru configurarea infrastructurii depozitului pentru prima dată.
  
#### Command Usage

```bash
dignacli upgrade-repo [options]
```
  
#### Options
  
- `--simulation-mode`, `-s`: Când este activată, această opțiune rulează comanda în modul de simulare, care afișează instrucțiunile SQL care ar fi executate, dar nu le execută efectiv. Acest lucru este util pentru previzualizarea modificărilor fără a face schimbări în depozit.  

  
#### Example
  
Pentru a actualiza depozitul ***digna***, puteți rula comanda fără opțiuni:
  
```bash
dignacli upgrade-repo
```  
Pentru a rula actualizarea în modul de simulare (pentru a vedea instrucțiunile SQL fără a le aplica):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Această comandă este crucială pentru întreținerea sistemului ***digna***, asigurând că schema bazei de date și celelalte componente ale depozitului sunt la zi cu cea mai recentă versiune a software-ului.

### Using `encrypt` Command
  
Comanda `encrypt` din CLI-ul ***digna*** este folosită pentru a cripta o parolă.
  
#### Command Usage
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Arguments
- **PASSWORD**: Parola care trebuie criptată (obligatoriu).
  
#### Example
  
Pentru a cripta o parolă, trebuie să furnizați parola ca argument.   
De exemplu, pentru a cripta parola `mypassword123`, ați folosi:
```bash
dignacli encrypt mypassword123
```
Această comandă afișează versiunea criptată a parolei furnizate, care poate fi utilizată apoi în contexte securizate. Dacă argumentul parolei nu este furnizat, CLI-ul va afișa o eroare indicând lipsa argumentului.

## Using `generate-key` Command
  
Comanda `generate-key` este folosită pentru a genera o cheie Fernet, esențială pentru securizarea parolelor stocate în depozitul ***digna***.
  
#### Command Usage
```bash
dignacli generate-key
```
  
## Data Management

## Using `clean-up` Command

Comanda `clean-up` din CLI-ul ***digna*** este folosită pentru a elimina profile, predicții și date ale sistemului de semafor (traffic light system) pentru una sau mai multe surse de date din cadrul unui proiect specificat. Această comandă este esențială pentru gestionarea ciclului de viață al datelor, ajutând la menținerea unui mediu de date organizat și eficient prin curățarea datelor învechite sau inutile.

#### Command Usage

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: Numele proiectului din care se vor elimina datele (obligatoriu). Utilizarea cuvântului cheie `all-projects` în acest argument instruiește pe ***digna*** să itereze prin toate proiectele existente și să aplice această comandă.
- **FROM_DATE**: Data și ora de început pentru eliminarea datelor. Formatele acceptate includ %Y-%m-%d, %Y-%m-%dT%H:%M:%S sau %Y-%m-%d %H:%M:%S (obligatoriu).
- **TO_DATE**: Data și ora de sfârșit pentru eliminarea datelor, urmând aceleași formate ca FROM_DATE (obligatoriu).
  
#### Options
  
- `--table-name`, `-tn`: Limitează operațiunea de curățare la un tabel specific din proiect.
- `--table-filter`, `-tf`: Filtrează pentru a limita curățarea la tabele care conțin substring-ul specificat în numele lor.
- `--timing`, `-tm`: Afișează durata procesului de curățare după finalizare.
- `--help`: Afișează informații de ajutor pentru comanda clean-up și iese.
  
#### Example
  
Pentru a șterge date din proiectul ProjectA între 1 ianuarie 2023 și 30 iunie 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Pentru a șterge date doar dintr-un tabel specific numit `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Această comandă ajută la gestionarea stocării datelor și la asigurarea că depozitul conține doar informațiile relevante.

## Using `list-projects` Command
  
Comanda `list-projects` din CLI-ul ***digna*** este folosită pentru a afișa o listă cu toate proiectele disponibile în sistemul ***digna***.
  
#### Command Usage
  
```bash
dignacli list-projects
```

Această comandă este deosebit de utilă pentru administratori și utilizatori care gestionează mai multe proiecte, oferind o vedere rapidă asupra proiectelor disponibile în depozitul ***digna***.

## Using `list-ds` Command

Comanda `list-ds` din CLI-ul ***digna*** este folosită pentru a afișa o listă cu toate sursele de date disponibile într-un proiect specificat. Această comandă este utilă pentru înțelegerea activelor de date disponibile pentru analiză și gestionare în sistemul ***digna***.

#### Command Usage
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Arguments
- **PROJECT_NAME**: Numele proiectului pentru care se listează sursele de date (obligatoriu).
  
#### Example
  
Pentru a lista toate sursele de date din proiectul numit `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Această comandă oferă utilizatorilor o privire de ansamblu asupra surselor de date disponibile într-un proiect, ajutându-i să navigheze și să gestioneze mai eficient peisajul de date.


## Using `inspect` Command

Comanda `inspect` din CLI-ul ***digna*** este folosită pentru a crea profile, predicții și date pentru sistemul de semafor (traffic light system) pentru una sau mai multe surse de date din cadrul unui proiect specificat. Această comandă ajută la analizarea și monitorizarea datelor pe o perioadă definită.

#### Command Usage

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: Numele proiectului pentru care se vor inspecta datele (obligatoriu). Utilizarea cuvântului cheie `all-projects` în acest argument instruiește pe ***digna*** să itereze prin toate proiectele existente și să aplice această comandă.
- **FROM_DATE**: Data și ora de început pentru inspectarea datelor. Formatele acceptate includ %Y-%m-%d, %Y-%m-%dT%H:%M:%S sau %Y-%m-%d %H:%M:%S (obligatoriu).
- **TO_DATE**: Data și ora de sfârșit pentru inspectarea datelor, urmând aceleași formate ca FROM_DATE (obligatoriu).
  
#### Options

- `--table-name`, `-tn`: Limitează inspectarea la un tabel specific din proiect.
- `--table-filter`, `-tf`: Filtrează pentru a inspecta doar tabele care conțin substring-ul specificat în numele lor.
- `--do-profile`: Declanșează recollectarea profilelor. Implicit este do-profile.
- `--no-do-profile`: Previne recollectarea profilelor.
- `--do-prediction`: Declanșează recalcularea predicțiilor. Implicit este do-prediction.
- `--no-do-prediction`: Previne recalcularea predicțiilor.
- `--do-alert-status`: Declanșează recalcularea stării alertelor. Implicit este do-alert-status.
- `--no-do-alert-status`: Previne recalcularea stării alertelor.
- `--iterative`: Declanșează inspectarea unei perioade folosind iterații zilnice. Implicit este iterative.
- `--no-iterative`: Declanșează inspectarea întregii perioade dintr-o singură execuție.
- `--enable_notification`, `-en`: Activează trimiterea notificărilor în caz de alerte.
- `--timing`, `-tm`: Afișează durata procesului de inspectare după finalizare.
  
#### Example
  
Pentru a inspecta datele pentru proiectul `ProjectA` din 1 ianuarie 2024 până pe 31 ianuarie 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Pentru a inspecta doar un tabel specific și a forța recalcularea predicțiilor:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Această comandă este utilă pentru generarea de profile și predicții actualizate, monitorizarea integrității datelor și gestionarea sistemelor de alertă într-un interval de timp specificat.

## Using `tls-status` Command

Comanda `tls-status` din CLI-ul ***digna*** este folosită pentru a interoga starea Traffic Light System (TLS) pentru un tabel specific dintr-un proiect la o dată dată. Sistemul de semafor oferă informații despre sănătatea și calitatea datelor, indicând eventuale probleme sau alerte care necesită atenție.
  
#### Command Usage
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Arguments
  
- **PROJECT_NAME**: Numele proiectului pentru care se interoghează starea TLS (obligatoriu).
- **TABLE_NAME**: Tabelul specific din proiect pentru care se dorește starea TLS (obligatoriu).
- **DATE**: Data pentru care se interoghează starea TLS, de obicei în formatul %Y-%m-%d (obligatoriu).
  
#### Example
  
Pentru a verifica starea TLS pentru un tabel numit `UserData` în proiectul `ProjectA` la data de 1 iulie 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Această comandă ajută utilizatorii să monitorizeze și să mențină calitatea datelor, oferind un raport clar și acționabil bazat pe criterii predefinite.

## Using `inspect-async` Command

Comanda `inspect-async` din CLI-ul ***digna*** este folosită pentru a transmite backend-ului instrucțiunea de a efectua asincron inspectarea pentru una sau mai multe surse de date dintr-un proiect dat. Dacă `project_name` este setat la `all-projects`, inspectarea va itera prin toate proiectele disponibile și va efectua inspectarea. Comanda returnează un request id care poate fi folosit pentru a urmări progresul inspectării.

#### Command Usage

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: Numele proiectului pentru care se vor inspecta datele (obligatoriu). Utilizarea cuvântului cheie `all-projects` în acest argument instruiește pe ***digna*** să itereze prin toate proiectele existente și să aplice această comandă.
- **FROM_DATE**: Data și ora de început pentru inspectarea datelor. Formatele acceptate includ %Y-%m-%d, %Y-%m-%dT%H:%M:%S sau %Y-%m-%d %H:%M:%S (obligatoriu).
- **TO_DATE**: Data și ora de sfârșit pentru inspectarea datelor, urmând aceleași formate ca FROM_DATE (obligatoriu).
  
#### Options

- `--table-name`, `-tn`: Limitează inspectarea la un tabel specific din proiect.
- `--table-filter`, `-tf`: Filtrează pentru a inspecta doar tabele care conțin substring-ul specificat în numele lor.

  
#### Example
  
Pentru a inspecta datele pentru proiectul `ProjectA` din 1 ianuarie 2024 până pe 31 ianuarie 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Using `inspect-status` Command

Comanda `inspect-status` din CLI-ul ***digna*** este folosită pentru a verifica progresul unei inspectări asincrone pe baza request ID-ului.

#### Command Usage

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Arguments
  
- **REQUEST_ID**: Request id returnat de comanda `inspect-async` 
  
#### Options

- `--report_level`, `-rl`: Setează nivelul raportului: 'task' sau 'step' [default: task]
  
#### Example
  
Pentru a verifica progresul unei inspectări cu request ID 12345 la nivel detaliat de pași:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Using `export-ds` Command

Comanda `export-ds` din CLI-ul ***digna*** este folosită pentru a crea un export al surselor de date din depozitul ***digna***. În mod implicit, toate sursele de date dintr-un proiect dat vor fi exportate.

#### Command Usage
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Arguments
- **PROJECT_NAME**: Numele proiectului din care vor fi exportate sursele de date.

#### Options

- `--table_name`, `-tn`: Exportă o sursă de date particulară dintr-un proiect.
- `--exportfile`, `-ef`: Specifică numele fișierului pentru export.
    
#### Example
  
Pentru a exporta toate sursele de date din proiectul numit `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Această comandă exportă toate sursele de date din `ProjectA` ca un document JSON care poate fi importat într-un alt proiect sau depozit ***digna***.


## Using `import-ds` Command

Comanda `import-ds` din CLI-ul ***digna*** este folosită pentru a importa surse de date într-un proiect țintă și pentru a crea un raport de import.

#### Command Usage
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME**: Numele proiectului în care vor fi importate sursele de date.
- **EXPORT_FILE**: Numele fișierului exportat al surselor de date care urmează a fi importat.

#### Options

- `--output-file`, `-o`: Fișier în care se salvează raportul de import (dacă nu este specificat, se afișează în terminal în formă tabelară).
- `--output-format`, `-f`: Formatul pentru salvarea raportului de import (json, csv).
    
#### Example
  
Pentru a importa toate sursele de date din fișierul de export `my_export.json` în `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
După import, această comandă va afișa și un raport al obiectelor importate și celor sărite. Doar sursele de date noi vor fi importate în `ProjectB`. Pentru a afla care obiecte ar fi importate și care ar fi sărite, puteți folosi comanda `plan-import-ds`.

## Using `plan-import-ds` Command

Comanda `plan-import-ds` din CLI-ul ***digna*** este folosită pentru a analiza importul surselor de date într-un proiect țintă și pentru a crea un raport de planificare a importului.

#### Command Usage
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME**: Numele proiectului în care ar fi importate sursele de date.
- **EXPORT_FILE**: Numele fișierului exportat al surselor de date care urmează a fi analizat înainte de import.

#### Options

- `--output-file`, `-o`: Fișier în care se salvează raportul de import (dacă nu este specificat, se afișează în terminal în formă tabelară).
- `--output-format`, `-f`: Formatul pentru salvarea raportului de import (json, csv).
    
#### Example
  
Pentru a verifica ce surse de date ar fi importate și care ar fi sărite din fișierul de export `my_export.json` când sunt importate în `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Această comandă va afișa doar un plan de import al obiectelor care vor fi importate și a celor care vor fi sărite.