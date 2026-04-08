---
title: Referință digna CLI 2026.04 – Comenzi & Exemple | digna Documentation
description: Referință completă pentru digna CLI versiunea 2026.04
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202604/
image: /assets/logo_square.png
---

# digna CLI Reference 2026.04
**2026-04-08**

Această pagină documentează setul complet de comenzi disponibile în CLI-ul ***digna*** versiunea **2026.04**, incluzând exemple de utilizare și opțiuni.

---

## Noțiuni de bază CLI

---

### help
Opțiunea `--help` oferă informații despre comenzile disponibile și despre modul lor de utilizare. Există două moduri principale de a folosi această opțiune:

1. **Afișarea ajutorului general:**
   
    Folosiți `--help` imediat după cuvântul cheie `dignacli`  
   ```bash
   dignacli --help
   ```

2. **Obținerea de ajutor pentru comenzi specifice:**  
  
    Pentru informații detaliate despre o comandă anume, adăugați `--help` după acea comandă.
    De exemplu, pentru a obține ajutor privind comanda `add-user`, rulați:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Descrierea comenzii:** Oferă o descriere detaliată a ceea ce face comanda.  
     - **Sintaxă:** Arată sintaxa exactă, incluzând argumentele obligatorii și opționale.  
     - **Opțiuni:** Listează orice opțiuni specifice comenzii, împreună cu explicațiile acestora.  
     - **Exemple:** Oferă exemple de cum să executați comanda în mod eficient.

### check-config

Comanda `check-config` este un utilitar din instrumentul CLI ***digna*** conceput pentru a testa configurația ***digna***. Această comandă verifică dacă componentele ***digna*** pot găsi elementele de configurație necesare în fișierul `config.toml`.

#### Opțiuni

- `--configpath`, `-cp`: Fișier sau director care conține configurația. Dacă este omis, se va folosi `../config.toml`.
      
#### Utilizare comandă
```bash
dignacli check-config
```

La executarea cu succes, comanda afișează o confirmare a completitudinii configurației.  
  
Dacă configurația pare incompletă, elementele lipsă de configurare vor fi listate.

  
### check-repo-connection

Comanda `check-repo-connection` este un utilitar din CLI-ul ***digna*** conceput pentru a testa conectivitatea și accesul la un depozit (repository) ***digna*** specificat. Această comandă verifică dacă CLI-ul poate interacționa cu repository-ul.
      
#### Utilizare comandă
```bash
dignacli check-repo-connection
```

La executarea cu succes, comanda afișează o confirmare a conexiunii, împreună cu detalii despre repository: versiunea Repository, Host, Bază de date și Schema.  
  
Dacă conexiunea la repository nu este reușită, verificați fișierul `config.toml` pentru setările corecte de configurare.


### version

Pentru a verifica versiunea instalată a *dignacli*, folosiți opțiunea `--version`.  
  
#### Utilizare comandă
```bash
dignacli --version
```
  
#### Exemplu de output
```bash
dignacli version 2026.04
```

### opțiuni de logare
  
Implicit, output-ul în consolă al comenzilor ***digna*** este proiectat să fie minimalistic. Majoritatea comenzilor oferă posibilitatea de a furniza informații suplimentare, folosind următoarele opțiuni:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose” și „debug” definesc nivelul de detaliu, pe când comutatorul „logfile” permite redirecționarea output-ului pentru a fi scris într-un fișier în loc de fereastra consolei.

## Administrare utilizatori

### add-user
  
Comanda `add-user` din CLI-ul ***digna*** este folosită pentru a adăuga un utilizator nou în sistemul ***digna***.
  
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
- `--valid_until`, `-vu`: Setează o dată de expirare pentru contul utilizatorului în formatul `YYYY-MM-DD HH:MI:SS`. Dacă nu este setată, contul nu are dată de expirare.

#### Exemplu

Pentru a adăuga un utilizator nou cu username-ul `jdoe`, numele complet `John Doe` și parola `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Pentru a adăuga un utilizator nou și a seta o dată de expirare a contului:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Comanda `delete-user` din CLI-ul ***digna*** este folosită pentru a elimina un utilizator existent din sistemul ***digna***.
  
#### Utilizare comandă
```bash
dignacli delete-user USER_NAME
```
  
#### Argumente
- **USER_NAME**: Numele de utilizator al contului care va fi șters (obligatoriu). Acesta este singurul argument necesar comenzii.

#### Exemplu
```bash
dignacli delete-user jdoe
```
  
Executând această comandă se va elimina utilizatorul `jdoe` din sistemul ***digna***, revocându-i accesul și ștergând datele și permisiunile asociate din repository.

### modify-user

Comanda `modify-user` din CLI-ul ***digna*** este folosită pentru a actualiza detaliile unui utilizator existent în sistemul ***digna***.

#### Utilizare comandă
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumente
  
- **USER_NAME**: Numele de utilizator al contului care va fi modificat (obligatoriu).
- **USER_FULL_NAME**: Noul nume complet pentru utilizator (obligatoriu).
  
#### Opțiuni  
  
- `--is_superuser`, `-su`: Setează utilizatorul ca superuser, acordând privilegii ridicate. Acest flag nu necesită o valoare.  
- `--valid_until`, `-vu`: Setează o dată de expirare pentru contul utilizatorului în formatul YYYY-MM-DD HH:MI:SS. Dacă nu este furnizată, contul rămâne valabil pe termen nelimitat.  
  
#### Exemplu
  
Pentru a modifica numele complet al utilizatorului `jdoe` în „Johnathan Doe” și a seta utilizatorul ca superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Comanda `modify-user-pwd` din CLI-ul ***digna*** este folosită pentru a schimba parola unui utilizator existent în sistemul ***digna***.
  
#### Utilizare comandă
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumente
  
- **USER_NAME**: Numele de utilizator al contului al cărui parolă urmează să fie schimbată (obligatoriu).
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

Executând această comandă în CLI-ul ***digna*** se va conecta la repository-ul ***digna*** și va lista toți utilizatorii, afișând ID-ul, username-ul, numele complet, statutul de superuser și timpii de expirare.

## Administrare repository

### upgrade-repo
  
Comanda `upgrade-repo` din CLI-ul ***digna*** este folosită pentru a actualiza sau inițializa repository-ul ***digna***. Această comandă este esențială pentru aplicarea actualizărilor sau pentru configurarea infrastructurii repository-ului pentru prima dată.
  
#### Utilizare comandă

```bash
dignacli upgrade-repo [options]
```
  
#### Opțiuni
  
- `--simulation-mode`, `-s`: Când este activată, această opțiune rulează comanda în mod simulare, afișând instrucțiunile SQL care ar fi executate, dar fără a le aplica efectiv. Acest mod este util pentru previzualizarea modificărilor fără a face modificări în repository.  

  
#### Exemplu
  
Pentru a actualiza repository-ul ***digna***, puteți rula comanda fără opțiuni:
  
```bash
dignacli upgrade-repo
```  
Pentru a rula upgrade-ul în mod simulare (pentru a vedea instrucțiunile SQL fără a le aplica):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Această comandă este crucială pentru întreținerea sistemului ***digna***, asigurând că schema bazei de date și alte componente ale repository-ului sunt actualizate la cea mai recentă versiune a software-ului.

### encrypt
  
Comanda `encrypt` din CLI-ul ***digna*** este folosită pentru a cripta o parolă.
  
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
Această comandă afișează versiunea criptată a parolei furnizate, care poate fi apoi folosită în contexte securizate. Dacă argumentul cu parola nu este furnizat, CLI-ul va afișa o eroare indicând argumentul lipsă.

### generate-key
  
Comanda `generate-key` este folosită pentru a genera o cheie Fernet, esențială pentru securizarea parolelor stocate în repository-ul ***digna***.
  
#### Utilizare comandă
```bash
dignacli generate-key
```
  
## Managementul datelor

### clean-up

Comanda `clean-up` din CLI-ul ***digna*** este folosită pentru a elimina profile, predicții și date ale sistemului de semaforizare (traffic light system) pentru una sau mai multe surse de date dintr-un proiect specificat. Această comandă este esențială pentru managementul ciclului de viață al datelor, ajutând la menținerea unui mediu de date organizat și eficient prin curățarea datelor învechite sau inutile.

#### Utilizare comandă

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Numele proiectului din care urmează să fie eliminate datele (obligatoriu). Utilizarea cuvântului cheie `all-projects` în acest argument indică lui ***digna*** să itereze peste toate proiectele existente și să aplice comanda.
- **FROM_DATE**: Data și ora de început pentru eliminarea datelor. Formatele acceptate includ %Y-%m-%d, %Y-%m-%dT%H:%M:%S sau %Y-%m-%d %H:%M:%S (obligatoriu).
- **TO_DATE**: Data și ora de sfârșit pentru eliminarea datelor, urmând aceleași formate ca pentru FROM_DATE (obligatoriu).
  
#### Opțiuni
  
- `--table-name`, `-tn`: Limitează operațiunea de clean-up la un tabel specific din proiect.
- `--table-filter`, `-tf`: Filtrează pentru a limita clean-up-ul la tabele care conțin subșirul specificat în numele lor.
- `--timing`, `-tm`: Afișează durata temporară a procesului de clean-up după finalizare.
- `--help`: Afișează informații de ajutor pentru comanda clean-up și iese.
  
#### Exemplu
  
Pentru a elimina date din proiectul `ProjectA` între 1 ianuarie 2023 și 30 iunie 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Pentru a elimina date doar dintr-un tabel specific numit `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Această comandă ajută la gestionarea stocării datelor și la asigurarea faptului că repository-ul conține doar informații relevante.

### remove-orphans
  
Comanda `remove-orphans` din CLI-ul ***digna*** este folosită pentru activități de întreținere în repository-ul ***digna***.  
Când un utilizator șterge proiecte sau surse de date, profilele și predicțiile pot rămâne în repository. Cu această comandă, astfel de rânduri orfane vor fi eliminate din repository.
  
#### Utilizare comandă
  
```bash
dignacli list-projects
```

### list-projects
  
Comanda `list-projects` din CLI-ul ***digna*** este folosită pentru a afișa o listă a tuturor proiectelor disponibile în sistemul ***digna***.
  
#### Utilizare comandă
  
```bash
dignacli list-projects
```

Această comandă este deosebit de utilă pentru administratori și utilizatori care gestionează mai multe proiecte, oferind o privire rapidă asupra proiectelor disponibile în repository-ul ***digna***.

### list-ds

Comanda `list-ds` din CLI-ul ***digna*** este folosită pentru a afișa o listă a tuturor surselor de date disponibile într-un proiect specificat. Această comandă este utilă pentru înțelegerea activelor de date disponibile pentru analiză și gestionare în sistemul ***digna***.

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
  
Această comandă oferă utilizatorilor o imagine de ansamblu a surselor de date disponibile într-un proiect, ajutându-i să navigheze și să gestioneze mai eficient peisajul de date.


### inspect

Comanda `inspect` din CLI-ul ***digna*** este folosită pentru a crea profile, predicții și date pentru sistemul de semaforizare (traffic light system) pentru una sau mai multe surse de date dintr-un proiect specificat. Această comandă ajută la analizarea și monitorizarea datelor pe o perioadă definită. După finalizarea inspecției, este returnată valoarea sistemului de semaforizare calculat:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Utilizare comandă

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Numele proiectului pentru care urmează să fie inspectate datele (obligatoriu). Utilizarea cuvântului cheie `all-projects` în acest argument indică lui ***digna*** să itereze peste toate proiectele existente și să aplice comanda.
- **FROM_DATE**: Data și ora de început pentru inspecția datelor. Formatele acceptate includ %Y-%m-%d, %Y-%m-%dT%H:%M:%S sau %Y-%m-%d %H:%M:%S (obligatoriu).
- **TO_DATE**: Data și ora de sfârșit pentru inspecția datelor, urmând aceleași formate ca pentru FROM_DATE (obligatoriu).
  
#### Opțiuni

- `--table-name`, `-tn`: Limitează inspecția la un tabel specific din proiect.
- `--table-filter`, `-tf`: Filtrează pentru a inspecta doar tabele care conțin subșirul specificat în numele lor.
- `--enable_notification`, `-en`: Activează trimiterea de notificări în caz de alerte.
- `--bypass-backend`, `-bb`: Sari peste backend și rulează inspecția direct din CLI (doar pentru scopuri de testare!).

  
#### Exemplu
  
Pentru a inspecta date pentru proiectul `ProjectA` din 1 ianuarie 2024 până la 31 ianuarie 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Pentru a inspecta doar un tabel specific și a forța recalcularea predicțiilor:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Această comandă este utilă pentru generarea de profile și predicții actualizate, monitorizarea integrității datelor și gestionarea sistemelor de alertă într-un interval de timp specificat pentru proiect.

### inspect-async

Comanda `inspect-async` din CLI-ul ***digna*** este folosită pentru a crea profile, predicții și date pentru sistemul de semaforizare (traffic light system) pentru una sau mai multe surse de date dintr-un proiect specificat. Această comandă ajută la analizarea și monitorizarea datelor pe o perioadă definită. Spre deosebire de comanda `inspect`, aceasta nu așteaptă finalizarea inspecției.
În schimb, returnează un ID de cerere (request id) pentru solicitarea de inspecție trimisă. Pentru a interoga progresul procesului de inspecție, folosiți comanda `inspect-status`.

#### Utilizare comandă

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumente
  
- **PROJECT_NAME**: Numele proiectului pentru care urmează să fie inspectate datele (obligatoriu). Utilizarea cuvântului cheie `all-projects` în acest argument indică lui ***digna*** să itereze peste toate proiectele existente și să aplice comanda.
- **FROM_DATE**: Data și ora de început pentru inspecția datelor. Formatele acceptate includ %Y-%m-%d, %Y-%m-%dT%H:%M:%S sau %Y-%m-%d %H:%M:%S (obligatoriu).
- **TO_DATE**: Data și ora de sfârșit pentru inspecția datelor, urmând aceleași formate ca pentru FROM_DATE (obligatoriu).
  
#### Opțiuni

- `--table-name`, `-tn`: Limitează inspecția la un tabel specific din proiect.
- `--table-filter`, `-tf`: Filtrează pentru a inspecta doar tabele care conțin subșirul specificat în numele lor.
- `--enable_notification`, `-en`: Activează trimiterea de notificări în caz de alerte.

  
#### Exemplu
  
Pentru a inspecta date pentru proiectul `ProjectA` din 1 ianuarie 2024 până la 31 ianuarie 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Comanda `inspect-status` din CLI-ul ***digna*** este folosită pentru a verifica progresul unei inspecții asincrone pe baza ID-ului cererii.

#### Utilizare comandă

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumente
  
- **REQUEST_ID**: ID-ul cererii returnat de comanda `inspect-async` 
  
#### Exemplu
  
Pentru a verifica progresul unei inspecții cu ID-ul cererii 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Comanda `inspect-cancel` din CLI-ul ***digna*** este folosită pentru a anula inspecții pe baza ID-ului cererii sau poate fi utilizată pentru a anula toate cererile curente.

#### Utilizare comandă

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumente
  
- **REQUEST_ID**: ID-ul cererii returnat de comanda `inspect-async` 
  
#### Exemplu
  
Pentru a anula inspecția cu ID-ul cererii 12345:
  
```bash
dignacli inspect-cancel 12345
```

Pentru a anula toate cererile care sunt în curs de rulare sau în așteptare:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Comanda `export-ds` din CLI-ul ***digna*** este folosită pentru a crea un export al surselor de date din repository-ul ***digna***. Implicit, toate sursele de date dintr-un proiect dat vor fi exportate.

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

Comanda `import-ds` din CLI-ul ***digna*** este folosită pentru a importa surse de date într-un proiect țintă și pentru a crea un raport de import.

#### Utilizare comandă
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumente
- **PROJECT_NAME**: Numele proiectului în care vor fi importate sursele de date.
- **EXPORT_FILE**: Numele fișierului export al surselor de date care urmează să fie importat.

#### Opțiuni

- `--output-file`, `-o`: Fișier în care se salvează raportul de import (dacă nu este specificat, se afișează în terminal în format tabular).
- `--output-format`, `-f`: Formatul în care se salvează raportul de import (json, csv).
    
#### Exemplu
  
Pentru a importa toate sursele de date din fișierul de export `my_export.json` în `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
După import, această comandă va afișa și un raport al obiectelor importate și sărite. Vor fi importate doar sursele de date noi în `ProjectB`. Pentru a afla ce obiecte ar fi importate și ce obiecte ar fi sărite, puteți folosi comanda `plan-import-ds`.

### plan-import-ds

Comanda `plan-import-ds` din CLI-ul ***digna*** este folosită pentru a analiza un fișier de export înainte de import și pentru a crea un raport de import planificat.

#### Utilizare comandă
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumente
- **PROJECT_NAME**: Numele proiectului în care ar fi importate sursele de date.
- **EXPORT_FILE**: Numele fișierului export al surselor de date care urmează să fie analizat înainte de import.

#### Opțiuni

- `--output-file`, `-o`: Fișier în care se salvează raportul de import (dacă nu este specificat, se afișează în terminal în format tabular).
- `--output-format`, `-f`: Formatul în care se salvează raportul de import (json, csv).
    
#### Exemplu
  
Pentru a verifica ce surse de date ar fi importate și care ar fi sărite din fișierul de export `my_export.json` dacă ar fi importat în `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Această comandă va afișa doar un plan de import al obiectelor care ar fi importate și cele care ar fi sărite.