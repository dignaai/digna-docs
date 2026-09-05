---
title: digna CLI Reference 2025.09 – Comenzi & Exemple | digna Documentation
description: Referință completă pentru digna CLI release 2025.109 Aflați cum să gestionați utilizatorii, repository-urile și datele cu comenzi precum add-user, check-config, check-repo-connection, inspect, inspect-async și altele.
image: /assets/logo_square.png
---

# digna CLI Reference 2025.09
**2025-09-29**

Această pagină documentează setul complet de comenzi disponibile în CLI-ul ***digna***, release **2025.09**, inclusiv exemple de utilizare și opțiuni.

---

## Bazele CLI-ului

---

### help
Opțiunea `--help` oferă informații despre comenzile disponibile și modul lor de utilizare. Există două moduri principale de a folosi această opțiune:

1. **Afișarea ajutorului general:**
   
    Folosiți --help imediat după cuvântul cheie ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Obținerea de ajutor pentru comenzi specifice:**  
  
    Pentru informații detaliate despre o comandă specifică, adăugați `--help` la sfârșitul comenzii.
    De exemplu, pentru a obține ajutor pentru comanda `add-user`, rulați:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Descrierea comenzii:** Oferă o descriere detaliată a ceea ce face comanda.  
     - **Sintaxă:** Afișează sintaxa exactă, inclusiv argumentele obligatorii și opționale.  
     - **Opțiuni:** Listează orice opțiuni specifice comenzii, împreună cu explicațiile lor.  
     - **Exemple:** Oferă exemple despre cum să executați comanda eficient.

### check-config

Comanda check-config este o utilitate din cadrul CLI-ului ***digna*** concepută pentru a testa configurația ***digna***. Această comandă verifică dacă componentele ***digna*** pot găsi elementele de configurare necesare în config.toml.

#### Opțiuni

- `--configpath`, `-cp`: Fișier sau director care conține configurația. Dacă este omis, va fi folosit ../config.toml.
      
#### Utilizare comandă
```bash
dignacli check-config
```

La execuție cu succes, comanda afișează o confirmare a completitudinii configurației.  
  
Dacă configurația pare incompletă, vor fi listate elementele de configurare lipsă.

  
### check-repo-connection

Comanda check-repo-connection este o utilitate din cadrul CLI-ului ***digna*** concepută pentru a testa conectivitatea și accesul la un repository ***digna*** specificat. Această comandă verifică dacă CLI-ul poate interacționa cu repository-ul.
      
#### Utilizare comandă
```bash
dignacli check-repo-connection
```

La execuție cu succes, comanda afișează o confirmare a conexiunii, împreună cu detalii despre repository: versiunea repository-ului, Host, Database și Schema.  
  
Dacă conexiunea la repository nu reușește, verificați fișierul config.toml pentru setările corecte de configurare.


### version

Pentru a verifica versiunea instalată a *dignacli*, folosiți opțiunea --version.  
  
#### Utilizare comandă
```bash
dignacli --version
```
  
#### Exemplu de output
```bash
dignacli version 2025.09
```

### opțiuni de logging
  
Implicit, output-ul în consolă al comenzilor ***digna*** este conceput pentru a fi minimalistic. Majoritatea comenzilor oferă posibilitatea de a furniza informații suplimentare, folosind următoarele opțiuni:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose” și „debug” definesc nivelul de detaliu, în timp ce comutatorul „logfile” permite redirecționarea output-ului pentru a fi scris într-un fișier în loc de fereastra consolei.

## Managementul utilizatorilor

### add-user
  
Comanda add-user din CLI-ul ***digna*** este utilizată pentru a adăuga un utilizator nou în sistemul ***digna***.
  
#### Utilizare comandă
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumente

- **USER_NAME**: Numele de utilizator pentru noul utilizator (obligatoriu).
- **USER_FULL_NAME**: Numele complet al noului utilizator (obligatoriu).
- **USER_PASSWORD**: Parola pentru noul utilizator (obligatoriu).

#### Opțiuni

- `--is_superuser`, `-su`: Flag pentru a desemna noul utilizator ca administrator.
- `--valid_until`, `-vu`: Setează o dată de expirare pentru contul utilizatorului în formatul `YYYY-MM-DD HH:MI:SS`. Dacă nu este setat, contul nu are dată de expirare.

#### Exemplu

Pentru a adăuga un utilizator nou cu username `jdoe`, nume complet `John Doe` și parola `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Pentru a adăuga un utilizator nou și a seta o dată de expirare a contului:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Comanda `delete-user` din CLI-ul ***digna*** este utilizată pentru a elimina un utilizator existent din sistemul ***digna***.
  
#### Utilizare comandă
```bash
dignacli delete-user USER_NAME
```
  
#### Argumente
- **USER_NAME**: Numele de utilizator al utilizatorului ce urmează a fi șters (obligatoriu). Acesta este singurul argument cerut de comandă.

#### Exemplu
```bash
dignacli delete-user jdoe
```
  
Executarea acestei comenzi va elimina utilizatorul `jdoe` din sistemul ***digna***, revocându-i accesul și ștergând datele și permisiunile asociate din repository.

### modify-user

Comanda `modify-user` din CLI-ul ***digna*** este folosită pentru a actualiza detaliile unui utilizator existent în sistemul ***digna***.

#### Utilizare comandă
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumente
  
- **USER_NAME**: Numele de utilizator al utilizatorului care urmează a fi modificat (obligatoriu).
- **USER_FULL_NAME**: Noul nume complet pentru utilizator (obligatoriu).
  
#### Opțiuni  
  
- `--is_superuser`, `-su`: Setează utilizatorul ca superuser, acordând privilegii ridicate. Acest flag nu necesită o valoare.  
- `--valid_until`, `-vu`: Setează o dată de expirare pentru contul utilizatorului în formatul YYYY-MM-DD HH:MI:SS. Dacă nu este furnizată, contul rămâne valabil pe termen nelimitat.  
  
#### Exemplu
  
Pentru a modifica numele complet al utilizatorului `jdoe` în „Johnathan Doe” și pentru a-l seta ca superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Comanda `modify-user-pwd` din CLI-ul ***digna*** este utilizată pentru a schimba parola unui utilizator existent în sistemul ***digna***.
  
#### Utilizare comandă
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumente
  
- **USER_NAME**: Numele de utilizator al utilizatorului căruia i se va schimba parola (obligatoriu).
- **USER_PWD**: Noua parolă pentru utilizator (obligatoriu).
  
#### Exemplu
  
Pentru a schimba parola utilizatorului `jdoe` în `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Comanda `list-users` din CLI-ul ***digna*** afișează o listă a tuturor utilizatorilor înregistrați în sistemul ***digna***.

#### Utilizare comandă

```bash
dignacli list-users
```

Executând această comandă în CLI-ul ***digna*** se va conecta la repository-ul ***digna*** și va lista toți utilizatorii, afișând ID-ul, username-ul, numele complet, statutul de superuser și timestamp-urile de expirare.

## Managementul repository-ului

### upgrade-repo
  
Comanda `upgrade-repo` din CLI-ul ***digna*** este folosită pentru a actualiza sau inițializa repository-ul ***digna***. Această comandă este esențială pentru aplicarea actualizărilor sau pentru configurarea infrastructurii repository-ului pentru prima dată.
  
#### Utilizare comandă

```bash
dignacli upgrade-repo [options]
```
  
#### Opțiuni
  
- `--simulation-mode`, `-s`: Când este activată, această opțiune rulează comanda în modul de simulare, afișând instrucțiunile SQL care ar fi executate, dar fără a le rula efectiv. Este utilă pentru a previzualiza schimbările fără a modifica repository-ul.  

  
#### Exemplu
  
Pentru a actualiza repository-ul ***digna***, puteți rula comanda fără opțiuni:
  
```bash
dignacli upgrade-repo
```  
Pentru a rula upgrade-ul în modul de simulare (pentru a vedea instrucțiunile SQL fără a le aplica):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Această comandă este crucială pentru întreținerea sistemului ***digna***, asigurând că schema bazei de date și celelalte componente ale repository-ului sunt up-to-date cu ultima versiune a software-ului.

### encrypt
  
Comanda `encrypt` din CLI-ul ***digna*** este utilizată pentru a cripta o parolă.
  
#### Utilizare comandă
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumente
- **PASSWORD**: Parola care trebuie criptată (obligatoriu).
  
#### Exemplu
  
Pentru a cripta o parolă, trebuie să furnizați parola ca argument.   
De exemplu, pentru a cripta parola `mypassword123`, ați folosi:
```bash
dignacli encrypt mypassword123
```
Această comandă afișează versiunea criptată a parolei furnizate, care poate fi folosită în contexte securizate. Dacă argumentul parolei nu este furnizat, CLI-ul va afișa o eroare indicând argumentul lipsă.

### generate-key
  
Comanda `generate-key` este folosită pentru a genera o cheie Fernet, esențială pentru securizarea parolelor stocate în repository-ul ***digna***.
  
#### Utilizare comandă
```bash
dignacli generate-key
```
  
## Managementul datelor

### clean-up

Comanda `clean-up` din CLI-ul ***digna*** este utilizată pentru a elimina profile, predicții și date din sistemul de traffic light pentru una sau mai multe surse de date din cadrul unui proiect specificat. Această comandă este esențială pentru managementul ciclului de viață al datelor, ajutând la menținerea unui mediu de date organizat și eficient prin curățarea datelor vechi sau inutile.

#### Utilizare comandă

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Numele proiectului din care se vor elimina datele (obligatoriu). Utilizarea cuvântului cheie all-projects în acest argument indică lui ***digna*** să itereze prin toate proiectele existente și să aplice această comandă.
- **FROM_DATE**: Data și ora de început pentru ștergerea datelor. Formatele acceptate includ %Y-%m-%d, %Y-%m-%dT%H:%M:%S sau %Y-%m-%d %H:%M:%S (obligatoriu).
- **TO_DATE**: Data și ora de sfârșit pentru ștergerea datelor, urmând aceleași formate ca FROM_DATE (obligatoriu).
  
#### Opțiuni
  
- `--table-name`, `-tn`: Limitează operațiunea de clean-up la un anumit tabel din proiect.
- `--table-filter`, `-tf`: Filtrează pentru a limita clean-up-ul la tabele care conțin substring-ul specificat în numele lor.
- `--timing`, `-tm`: Afișează durata de timp a procesului de clean-up după finalizare.
- `--help`: Afișează informații de ajutor pentru comanda clean-up și iese.
  
#### Exemplu
  
Pentru a elimina date din proiectul ProjectA între 1 ianuarie 2023 și 30 iunie 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Pentru a elimina date doar dintr-un anumit tabel numit `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Această comandă ajută la gestionarea spațiului de stocare a datelor și la asigurarea faptului că repository-ul conține doar informații relevante.

### remove-orphans
  
Comanda `remove-orphans` din CLI-ul ***digna*** este folosită pentru mentenanță în repository-ul ***digna***.  
Când un utilizator șterge proiecte sau surse de date, profilele și predicțiile pot rămâne în repository. Cu această comandă, astfel de rânduri orfane vor fi eliminate din repository.
  
#### Utilizare comandă
  
```bash
dignacli list-projects
```

### list-projects
  
Comanda `list-projects` din CLI-ul ***digna*** este folosită pentru a afișa lista tuturor proiectelor disponibile în sistemul ***digna***.
  
#### Utilizare comandă
  
```bash
dignacli list-projects
```

Această comandă este deosebit de utilă pentru administratori și utilizatori care gestionează mai multe proiecte, oferind o privire rapidă asupra proiectelor disponibile în repository-ul ***digna***.

### list-ds

Comanda `list-ds` din CLI-ul ***digna*** este utilizată pentru a afișa lista tuturor surselor de date disponibile într-un proiect specificat. Această comandă este utilă pentru a înțelege activele de date disponibile pentru analiză și management în sistemul ***digna***.

#### Utilizare comandă
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumente
- **PROJECT_NAME**: Numele proiectului pentru care se listează sursele de date (obligatoriu).
  
#### Exemplu
  
Pentru a lista toate sursele de date din proiectul numit `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Această comandă oferă utilizatorilor o imagine de ansamblu asupra surselor de date disponibile într-un proiect, ajutându-i să navigheze și să gestioneze mai eficient peisajul de date.


### inspect

Comanda `inspect` din CLI-ul ***digna*** este utilizată pentru a crea profile, predicții și date pentru sistemul de traffic light pentru una sau mai multe surse de date din cadrul unui proiect specificat. Această comandă ajută la analizarea și monitorizarea datelor pe o perioadă definită. La finalizarea inspecției, este returnată valoarea sistemului de traffic light calculat:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Utilizare comandă

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Numele proiectului pentru care se vor inspecta datele (obligatoriu). Utilizarea cuvântului cheie all-projects în acest argument indică lui ***digna*** să parcurgă toate proiectele existente și să aplice această comandă.
- **FROM_DATE**: Data și ora de început pentru inspecția datelor. Formatele acceptate includ %Y-%m-%d, %Y-%m-%dT%H:%M:%S sau %Y-%m-%d %H:%M:%S (obligatoriu).
- **TO_DATE**: Data și ora de sfârșit pentru inspecția datelor, urmând aceleași formate ca FROM_DATE (obligatoriu).
  
#### Opțiuni

- `--table-name`, `-tn`: Limitează inspecția la un tabel specific din proiect.
- `--table-filter`, `-tf`: Filtrează pentru a inspecta doar tabele care conțin substring-ul specificat în numele lor.
- `--enable_notification`, `-en`: Activează trimiterea de notificări în cazul alertelor.
- `--bypass-backend`, `-bb`: Ocolește backend-ul și rulează inspecția direct din CLI (doar în scopuri de testare!).

  
#### Exemplu
  
Pentru a inspecta datele pentru proiectul `ProjectA` din 1 ianuarie 2024 până la 31 ianuarie 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Pentru a inspecta doar un tabel specific și a forța recalcularea predicțiilor:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Această comandă este utilă pentru generarea de profile și predicții actualizate, monitorizarea integrității datelor și gestionarea sistemelor de alertă într-un interval de timp specificat pentru un proiect.

### inspect-async

Comanda `inspect-async` din CLI-ul ***digna*** este utilizată pentru a crea profile, predicții și date pentru sistemul de traffic light pentru una sau mai multe surse de date din cadrul unui proiect specificat. Această comandă ajută la analizarea și monitorizarea datelor pe o perioadă definită. Spre deosebire de comanda `inspect`, aceasta nu așteaptă finalizarea inspecției.
În schimb, returnează request id-ul pentru cererea de inspecție trimisă. Pentru a interoga progresul procesului de inspecție, folosiți comanda `inspect-status`.

#### Utilizare comandă

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Numele proiectului pentru care se vor inspecta datele (obligatoriu). Utilizarea cuvântului cheie all-projects în acest argument indică lui ***digna*** să parcurgă toate proiectele existente și să aplice această comandă.
- **FROM_DATE**: Data și ora de început pentru inspecția datelor. Formatele acceptate includ %Y-%m-%d, %Y-%m-%dT%H:%M:%S sau %Y-%m-%d %H:%M:%S (obligatoriu).
- **TO_DATE**: Data și ora de sfârșit pentru inspecția datelor, urmând aceleași formate ca FROM_DATE (obligatoriu).
  
#### Opțiuni

- `--table-name`, `-tn`: Limitează inspecția la un tabel specific din proiect.
- `--table-filter`, `-tf`: Filtrează pentru a inspecta doar tabele care conțin substring-ul specificat în numele lor.
- `--enable_notification`, `-en`: Activează trimiterea de notificări în cazul alertelor.

  
#### Exemplu
  
Pentru a inspecta datele pentru proiectul `ProjectA` din 1 ianuarie 2024 până la 31 ianuarie 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Comanda `inspect-status` din CLI-ul ***digna*** este utilizată pentru a verifica progresul unei inspecții asincrone pe baza request ID-ului.

#### Utilizare comandă

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumente
  
- **REQUEST_ID**: Request id-ul returnat de comanda `inspect-async` 
  
#### Exemplu
  
Pentru a verifica progresul unei inspecții cu request ID 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Comanda `inspect-cancel` din CLI-ul ***digna*** este utilizată pentru a anula inspecțiile pe baza request ID-ului sau poate fi folosită pentru a anula toate cererile curente.

#### Utilizare comandă

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumente
  
- **REQUEST_ID**: Request id-ul returnat de comanda `inspect-async` 
  
#### Exemplu
  
Pentru a anula inspecția cu request ID 12345:
  
```bash
dignacli inspect-cancel 12345
```

Pentru a anula toate cererile care sunt în prezent în execuție sau în așteptare:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Comanda `export-ds` din CLI-ul ***digna*** este utilizată pentru a crea un export al surselor de date din repository-ul ***digna***. Implicit, toate sursele de date dintr-un proiect dat vor fi exportate.

#### Utilizare comandă
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumente
- **PROJECT_NAME**: Numele proiectului din care vor fi exportate sursele de date.

#### Opțiuni

- `--table_name`, `-tn`: Exportă o anumită sursă de date dintr-un proiect.
- `--exportfile`, `-ef`: Specifică numele fișierului pentru export.
    
#### Exemplu
  
Pentru a exporta toate sursele de date din proiectul numit `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Această comandă exportă toate sursele de date din `ProjectA` ca un document JSON care poate fi importat într-un alt proiect sau repository ***digna***.


### import-ds

Comanda `import-ds` din CLI-ul ***digna*** este utilizată pentru a importa surse de date într-un proiect țintă și pentru a crea un raport de import.

#### Utilizare comandă
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumente
- **PROJECT_NAME**: Numele proiectului în care vor fi importate sursele de date.
- **EXPORT_FILE**: Numele fișierului exportului de surse de date care urmează a fi importat.

#### Opțiuni

- `--output-file`, `-o`: Fișier în care se salvează raportul de import (dacă nu este specificat, se afișează în terminal în formă tabelară).
- `--output-format`, `-f`: Formatul în care se salvează raportul de import (json, csv).
    
#### Exemplu
  
Pentru a importa toate sursele de date din fișierul de export `my_export.json` în `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
După import, această comandă va afișa de asemenea un raport al obiectelor importate și a celor sărite. Vor fi importate doar sursele de date noi în `ProjectB`. Pentru a afla ce obiecte ar fi importate și care ar fi sărite, puteți folosi comanda `plan-import-ds`.

### plan-import-ds

Comanda `plan-import-ds` din CLI-ul ***digna*** este utilizată pentru a analiza un export de surse de date înainte de import și pentru a crea un raport de import planificat.

#### Utilizare comandă
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumente
- **PROJECT_NAME**: Numele proiectului în care ar urma să fie importate sursele de date.
- **EXPORT_FILE**: Numele fișierului exportului de surse de date care urmează a fi analizat înainte de import.

#### Opțiuni

- `--output-file`, `-o`: Fișier în care se salvează raportul de import planificat (dacă nu este specificat, se afișează în terminal în formă tabelară).
- `--output-format`, `-f`: Formatul în care se salvează raportul de import planificat (json, csv).
    
#### Exemplu
  
Pentru a verifica ce surse de date ar fi importate și care ar fi sărite din fișierul de export `my_export.json` când sunt importate în `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Această comandă va afișa doar un plan de import al obiectelor care ar fi importate și a celor care ar fi sărite.