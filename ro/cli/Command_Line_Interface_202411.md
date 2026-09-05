# digna CLI Reference 2024.11
**2024-11-03**

Această pagină documentează setul complet de comenzi disponibile în CLI-ul ***digna***, release **2024.11**, inclusiv exemple de utilizare și opțiuni.


---
## CLI Basics

---

## Using `help` Option

Opțiunea `--help` furnizează informații despre comenzile disponibile și modul lor de utilizare. Există două modalități principale de a folosi această opțiune:

1. **Afișarea ajutorului general:**
   
    Folosiți --help imediat după cuvântul cheie ***dignacli***  
   ```bash
   dignacli --help
   ```

3.  **Obținerea ajutorului pentru comenzi specifice:**  
  
    Pentru informații detaliate despre o comandă anume, adăugați `--help` la sfârșitul acelei comenzi.
    De exemplu, pentru a obține ajutor pentru comanda `add-user`, rulați:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Descrierea comenzii:** Oferă o descriere detaliată a funcționalității comenzii.  
     - **Sintaxă:** Afișează sintaxa exactă, inclusiv argumentele obligatorii și opționale.  
     - **Opțiuni:** Listează opțiunile specifice comenzii, împreună cu explicațiile lor.  
     - **Exemple:** Oferă exemple despre cum să executați comanda eficient.

  
## Using `check-repo-connection` Command

Comanda check-repo-connection este un utilitar din CLI-ul ***digna*** conceput pentru a testa conectivitatea și accesul la un repository ***digna*** specific. Această comandă asigură că CLI-ul poate interacționa cu repository-ul.
      
### Command Usage
```bash
dignacli check-repo-connection
```

La executarea cu succes, comanda afișează o confirmare a conexiunii, împreună cu detalii despre repository: versiunea repository-ului, Host, Baza de date și Schema.  
  
Dacă conexiunea la repository nu este reușită, verificați fișierul config.toml pentru setările corecte de configurare.

## Using ‘version’ command

Pentru a verifica versiunea instalată a *dignacli*, folosiți opțiunea --version.  
  
### Command Usage
```bash
dignacli --version
```
  
### Example Output
```bash
dignacli version 2024.11
```

## Using logging options
  
Implicit, output-ul în consolă al comenzilor ***digna*** este conceput să fie minimalist. Majoritatea comenzilor oferă posibilitatea de a furniza informații suplimentare, folosind următoarele opțiuni:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose” și „debug” definesc nivelul de detaliu, în timp ce comutatorul „logfile” permite redirecționarea output-ului pentru a fi scris într-un fișier în loc de fereastra consolei.

# User Management

## Using ‘add-user’ command
  
Comanda add-user din CLI-ul ***digna*** este folosită pentru a adăuga un utilizator nou în sistemul ***digna***.
  
### Command Usage
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Arguments

- **USER_NAME**: Numele de utilizator pentru utilizatorul nou (obligatoriu).
- **USER_FULL_NAME**: Numele complet al utilizatorului nou (obligatoriu).
- **USER_PASSWORD**: Parola pentru utilizatorul nou (obligatoriu).

### Options

- `--is_superuser`, `-su`: Flag pentru a desemna utilizatorul nou ca administrator.
- `--valid_until`, `-vu`: Setează o dată de expirare pentru contul utilizatorului în formatul `YYYY-MM-DD HH:MI:SS`. Dacă nu este setat, contul nu are dată de expirare.

### Example

Pentru a adăuga un utilizator nou cu username-ul `jdoe`, numele complet `John Doe` și parola `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Pentru a adăuga un utilizator nou și a seta o dată de expirare a contului:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Using `delete-user` command
  
Comanda `delete-user` din CLI-ul ***digna*** este folosită pentru a elimina un utilizator existent din sistemul ***digna***.
  
### Command Usage
```bash
dignacli delete-user USER_NAME
```
  
### Arguments
- **USER_NAME**: Numele de utilizator al contului care urmează a fi șters (obligatoriu). Acesta este singurul argument necesar comenzii.

### Example
```bash
dignacli delete-user jdoe
```
  
Executarea acestei comenzi va elimina utilizatorul `jdoe` din sistemul ***digna***, revocându-i accesul și ștergând datele și permisiunile asociate din repository.

## Using `modify-user` Command

Comanda `modify-user` din CLI-ul ***digna*** este folosită pentru a actualiza detaliile unui utilizator existent în sistemul ***digna***.

### Command Usage
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Arguments
  
- **USER_NAME**: Numele de utilizator al contului care urmează a fi modificat (obligatoriu).
- **USER_FULL_NAME**: Noul nume complet pentru utilizator (obligatoriu).
  
### Options  
  
- `--is_superuser`, `-su`: Setează utilizatorul ca superuser, acordând privilegii elevate. Acest flag nu necesită o valoare.  
- `--valid_until`, `-vu`: Setează o dată de expirare pentru cont în formatul YYYY-MM-DD HH:MI:SS. Dacă nu este furnizată, contul rămâne valabil pe termen nelimitat.  
  
### Example
  
Pentru a modifica numele complet al utilizatorului `jdoe` în „Johnathan Doe” și a seta utilizatorul ca superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Using `modify-user-pwd` Command
  
Comanda `modify-user-pwd` din CLI-ul ***digna*** este folosită pentru a schimba parola unui utilizator existent în sistemul ***digna***.
  
### Command Usage
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Arguments
  
- **USER_NAME**: Numele de utilizator al contului a cărui parolă trebuie schimbată (obligatoriu).
- **USER_PWD**: Noua parolă pentru utilizator (obligatoriu).
  
### Example
  
Pentru a schimba parola utilizatorului `jdoe` în `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Using `list-users` Command

Comanda `list-users` din CLI-ul ***digna*** afișează o listă cu toți utilizatorii înregistrați în sistemul ***digna***.

### Command Usage

```bash
dignacli list-users
```

Executarea acestei comenzi în CLI-ul ***digna*** se va conecta la repository-ul ***digna*** și va lista toți utilizatorii, afișând ID-ul, username-ul, numele complet, statutul de superuser și timestamp-urile de expirare.

# Repository Management

### Using `upgrade-repo` Command
  
Comanda `upgrade-repo` din CLI-ul ***digna*** este folosită pentru a face upgrade sau pentru a inițializa repository-ul ***digna***. Această comandă este esențială pentru aplicarea actualizărilor sau pentru configurarea infrastructurii repository-ului pentru prima dată.
  
### Command Usage

```bash
dignacli upgrade-repo [options]
```
  
### Options
  
- `--simulation-mode`, `-s`: Când este activată, această opțiune rulează comanda în modul de simulare, afișând instrucțiunile SQL care ar fi executate, dar fără a le rula efectiv. Acest lucru este util pentru a previzualiza schimbările fără a modifica repository-ul.  

  
### Example
  
Pentru a face upgrade repository-ului ***digna***, puteți rula comanda fără opțiuni:
  
```bash
dignacli upgrade-repo
```  
Pentru a rula upgrade-ul în modul de simulare (pentru a vedea instrucțiunile SQL fără a le aplica):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Această comandă este crucială pentru întreținerea sistemului ***digna***, asigurând că schema bazei de date și alte componente ale repository-ului sunt actualizate la cea mai recentă versiune a software-ului.

## Using `encrypt` Command
  
Comanda `encrypt` din CLI-ul ***digna*** este folosită pentru a cripta o parolă.
  
### Command Usage
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Arguments
- **PASSWORD**: Parola care trebuie criptată (obligatoriu).
  
### Example
  
Pentru a cripta o parolă, trebuie să furnizați parola ca argument.   
De exemplu, pentru a cripta parola `mypassword123`, ați folosi:
```bash
dignacli encrypt mypassword123
```
Această comandă va afișa versiunea criptată a parolei furnizate, care poate fi apoi utilizată în contexte securizate. Dacă argumentul parolei nu este furnizat, CLI-ul va afișa o eroare indicând argumentul lipsă.

## Using `generate-key` Command
  
Comanda `generate-key` este folosită pentru a genera o cheie Fernet, esențială pentru securizarea parolelor stocate în repository-ul ***digna***.
  
### Command Usage
```bash
dignacli generate-key
```
  
# Data Management

## Using `clean-up` Command

Comanda `clean-up` din CLI-ul ***digna*** este folosită pentru a elimina profile, predicții și date ale sistemului de semaforizare (traffic light system) pentru una sau mai multe surse de date dintr-un proiect specificat. Această comandă este esențială pentru managementul ciclului de viață al datelor, ajutând la menținerea unui mediu de date organizat și eficient prin curățarea datelor învechite sau inutile.

### Command Usage

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Arguments
  
- **PROJECT_NAME**: Numele proiectului din care se vor elimina datele (obligatoriu). Folosirea cuvântului cheie all-projects în acest argument indică ***digna*** să itereze peste toate proiectele existente și să aplice comanda.
- **FROM_DATE**: Data și ora de început pentru ștergerea datelor. Formatele acceptate includ %Y-%m-%d, %Y-%m-%dT%H:%M:%S sau %Y-%m-%d %H:%M:%S (obligatoriu).
- **TO_DATE**: Data și ora de sfârșit pentru ștergerea datelor, urmând aceleași formate ca FROM_DATE (obligatoriu).
  
### Options
  
- `--table-name`, `-tn`: Limitează operațiunea de clean-up la un anumit tabel din proiect.
- `--table-filter`, `-tf`: Filtrează pentru a limita clean-up-ul la tabele care conțin substring-ul specificat în nume.
- `--timing`, `-tm`: Afișează durata procesului de clean-up după finalizare.
- `--help`: Afișează informații de ajutor pentru comanda clean-up și iese.
  
### Example
  
Pentru a elimina date din proiectul ProjectA între 1 ianuarie 2023 și 30 iunie 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Pentru a elimina date doar dintr-un tabel specific numit `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Această comandă contribuie la gestionarea spațiului de stocare a datelor și la asigurarea faptului că repository-ul conține doar informații relevante.

## Using `inspect` Command

Comanda `inspect` din CLI-ul ***digna*** este folosită pentru a crea profile, predicții și date ale sistemului de semaforizare pentru una sau mai multe surse de date dintr-un proiect specificat. Această comandă ajută la analizarea și monitorizarea datelor pe o perioadă definită.

### Command Usage

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Arguments
  
- **PROJECT_NAME**: Numele proiectului pentru care se vor inspecta datele (obligatoriu). Folosirea cuvântului cheie all-projects în acest argument indică ***digna*** să itereze peste toate proiectele existente și să aplice comanda.
- **FROM_DATE**: Data și ora de început pentru inspecția datelor. Formatele acceptate includ %Y-%m-%d, %Y-%m-%dT%H:%M:%S sau %Y-%m-%d %H:%M:%S (obligatoriu).
- **TO_DATE**: Data și ora de sfârșit pentru inspecția datelor, urmând aceleași formate ca FROM_DATE (obligatoriu).
  
### Options

- `--table-name`, `-tn`: Limitează inspecția la un anumit tabel din proiect.
- `--table-filter`, `-tf`: Filtrează pentru a inspecta doar tabele care conțin substring-ul specificat în nume.
- `--do-profile`: Declanșează recollectarea profilelor. Implicit este do-profile.
- `--no-do-profile`: Previne recollectarea profilelor.
- `--do-prediction`: Declanșează recalcularea predicțiilor. Implicit este do-prediction.
- `--no-do-prediction`: Previne recalcularea predicțiilor.
- `--do-alert-status`: Declanșează recalcularea stării alertelor. Implicit este do-alert-status.
- `--no-do-alert-status`: Previne recalcularea stării alertelor.
- `--timing`, `-tm`: Afișează durata procesului de inspecție după finalizare.
  
### Example
  
Pentru a inspecta datele pentru proiectul `ProjectA` din 1 ianuarie 2024 până în 31 ianuarie 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Pentru a inspecta doar un tabel specific și a forța recalcularea predicțiilor:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Această comandă este utilă pentru generarea de profile și predicții actualizate, monitorizarea integrității datelor și gestionarea sistemelor de alertă într-un interval de timp specificat pentru proiect.

## Using `tls-status` Command

Comanda `tls-status` din CLI-ul ***digna*** este folosită pentru a interoga starea Traffic Light System (TLS) pentru un tabel specific dintr-un proiect la o anumită dată. Sistemul de semaforizare oferă informații despre sănătatea și calitatea datelor, indicând eventualele probleme sau alerte care necesită atenție.
  
### Command Usage
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Arguments
  
- **PROJECT_NAME**: Numele proiectului pentru care se interoghează starea TLS (obligatoriu).
- **TABLE_NAME**: Tabelul specific din proiect pentru care este necesară starea TLS (obligatoriu).
- **DATE**: Data pentru care se interoghează starea TLS, de obicei în formatul %Y-%m-%d (obligatoriu).
  
### Example
  
Pentru a verifica starea TLS pentru un tabel numit UserData în proiectul ProjectA la 1 iulie 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Această comandă ajută utilizatorii să monitorizeze și să mențină calitatea datelor oferind un raport clar și acționabil pe baza criteriilor prestabilite.

## Using `list-projects` Command
  
Comanda `list-projects` din CLI-ul ***digna*** este folosită pentru a afișa o listă cu toate proiectele disponibile în sistemul ***digna***.
  
### Command Usage
  
```bash
dignacli list-projects
```

Această comandă este deosebit de utilă pentru administratori și utilizatori care gestionează mai multe proiecte, oferind o privire rapidă asupra proiectelor disponibile în repository-ul ***digna***.

## Using `list-ds` Command

Comanda `list-ds` din CLI-ul ***digna*** este folosită pentru a afișa o listă cu toate sursele de date disponibile într-un proiect specificat. Această comandă este utilă pentru înțelegerea activelor de date disponibile pentru analiză și gestionare în sistemul ***digna***.

### Command Usage
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Arguments
- **PROJECT_NAME**: Numele proiectului pentru care se listează sursele de date (obligatoriu).
  
### Example
  
Pentru a lista toate sursele de date din proiectul numit `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Această comandă oferă utilizatorilor o imagine de ansamblu asupra surselor de date disponibile într-un proiect, ajutându-i să navigheze și să gestioneze mai eficient peisajul de date.