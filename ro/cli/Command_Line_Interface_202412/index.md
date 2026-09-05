# digna CLI Reference 2024.12
**2024-12-09**

Această pagină documentează setul complet de comenzi disponibile în CLI-ul ***digna***, release **2024.12**, incluzând exemple de utilizare și opțiuni.

---


**2024-12-09**


---

## Bazele CLI-ului

---

## Utilizarea opțiunii `help`

Opțiunea `--help` oferă informații despre comenzile disponibile și modul lor de utilizare. Există două modalități principale de a folosi această opțiune:

1. **Afișarea ajutorului general:**
   
    Folosiți --help imediat după cuvântul cheie ***digna***cl  
   ```bash
   dignacli --help
   ```

3.  **Obținerea de ajutor pentru comenzi specifice:**  
  
    Pentru informații detaliate despre o comandă specifică, adăugați `--help` la acea comandă.
    De exemplu, pentru a obține ajutor pentru comanda `add-user`, rulați:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Descrierea comenzii:** Oferă o descriere detaliată a ceea ce face comanda.  
     - **Sintaxă:** Afișează sintaxa exactă, incluzând argumentele obligatorii și opționale.  
     - **Opțiuni:** Listează orice opțiuni specifice comenzii, împreună cu explicațiile lor.  
     - **Exemple:** Furnizează exemple despre cum să executați comanda eficient.

  
## Utilizarea comenzii `check-repo-connection`

Comanda check-repo-connection este un utilitar din cadrul CLI-ului ***digna*** conceput pentru a testa conectivitatea și accesul la un depozit ***digna*** specificat. Această comandă se asigură că CLI-ul poate interacționa cu depozitul.
      
### Utilizare comandă
```bash
dignacli check-repo-connection
```

La executarea cu succes, comanda afișează o confirmare a conexiunii, împreună cu detalii despre depozit: versiunea depozitului, Host, Bază de date și Schema.  
  
Dacă conexiunea la depozit nu reușește, verificați fișierul config.toml pentru setările corecte de configurare.

## Utilizarea comenzii `version`

Pentru a verifica versiunea instalată a *dignacli*, folosiți opțiunea --version.  
  
### Utilizare comandă
```bash
dignacli --version
```
  
### Exemplu de ieșire
```bash
dignacli version 2024.12
```

## Utilizarea opțiunilor de logare
  
Implicit, ieșirea în consolă a comenzilor ***digna*** este proiectată să fie minimală. Majoritatea comenzilor oferă posibilitatea de a furniza informații suplimentare, folosind următoarele opțiuni:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose” și „debug” definesc nivelul de detaliu, în timp ce comutatorul „logfile” permite redirecționarea ieșirii pentru a fi scrisă într-un fișier în loc de fereastra consolei.

# Managementul utilizatorilor

## Utilizarea comenzii `add-user`
  
Comanda add-user din CLI-ul ***digna*** este folosită pentru a adăuga un utilizator nou în sistemul ***digna***.
  
### Utilizare comandă
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumente

- **USER_NAME**: Numele de utilizator pentru utilizatorul nou (obligatoriu).
- **USER_FULL_NAME**: Numele complet al utilizatorului nou (obligatoriu).
- **USER_PASSWORD**: Parola pentru utilizatorul nou (obligatoriu).

### Opțiuni

- `--is_superuser`, `-su`: Flag pentru a desemna utilizatorul nou ca administrator.
- `--valid_until`, `-vu`: Setează o dată de expirare pentru contul utilizatorului în formatul `YYYY-MM-DD HH:MI:SS`. Dacă nu este setată, contul nu are dată de expirare.

### Exemplu

Pentru a adăuga un utilizator nou cu numele de utilizator `jdoe`, numele complet `John Doe` și parola `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Pentru a adăuga un utilizator nou și a seta o dată de expirare a contului:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Utilizarea comenzii `delete-user`
  
Comanda `delete-user` din CLI-ul ***digna*** este folosită pentru a elimina un utilizator existent din sistemul ***digna***.
  
### Utilizare comandă
```bash
dignacli delete-user USER_NAME
```
  
### Argumente
- **USER_NAME**: Numele de utilizator al utilizatorului care urmează să fie șters (obligatoriu). Acesta este singurul argument necesar comenzii.

### Exemplu
```bash
dignacli delete-user jdoe
```
  
Executarea acestei comenzi va elimina utilizatorul `jdoe` din sistemul ***digna***, revocându-i accesul și ștergând datele și permisiunile asociate din depozit.

## Utilizarea comenzii `modify-user`

Comanda `modify-user` din CLI-ul ***digna*** este folosită pentru a actualiza detaliile unui utilizator existent în sistemul ***digna***.

### Utilizare comandă
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumente
  
- **USER_NAME**: Numele de utilizator al utilizatorului care urmează să fie modificat (obligatoriu).
- **USER_FULL_NAME**: Noul nume complet pentru utilizator (obligatoriu).
  
### Opțiuni  
  
- `--is_superuser`, `-su`: Setează utilizatorul ca superuser, acordând privilegii ridicate. Acest flag nu necesită o valoare.  
- `--valid_until`, `-vu`: Setează o dată de expirare pentru contul utilizatorului în formatul YYYY-MM-DD HH:MI:SS. Dacă nu este furnizată, contul rămâne valabil pe termen nelimitat.  
  
### Exemplu
  
Pentru a modifica numele complet al utilizatorului `jdoe` în „Johnathan Doe” și a seta utilizatorul ca superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Utilizarea comenzii `modify-user-pwd`
  
Comanda `modify-user-pwd` din CLI-ul ***digna*** este folosită pentru a schimba parola unui utilizator existent în sistemul ***digna***.
  
### Utilizare comandă
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumente
  
- **USER_NAME**: Numele de utilizator al utilizatorului a cărui parolă trebuie schimbată (obligatoriu).
- **USER_PWD**: Noua parolă pentru utilizator (obligatoriu).
  
### Exemplu
  
Pentru a schimba parola utilizatorului `jdoe` în `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Utilizarea comenzii `list-users`

Comanda `list-users` din CLI-ul ***digna*** afișează o listă cu toți utilizatorii înregistrați în sistemul ***digna***.

### Utilizare comandă

```bash
dignacli list-users
```

Executarea acestei comenzi în CLI-ul ***digna*** se va conecta la depozitul ***digna*** și va lista toți utilizatorii, afișând ID-ul lor, numele de utilizator, numele complet, statutul de superuser și timestamp-urile de expirare.

# Managementul depozitelor

### Utilizarea comenzii `upgrade-repo`
  
Comanda `upgrade-repo` din CLI-ul ***digna*** este folosită pentru a actualiza sau inițializa depozitul ***digna***. Această comandă este esențială pentru aplicarea actualizărilor sau pentru configurarea infrastructurii depozitului pentru prima dată.
  
### Utilizare comandă

```bash
dignacli upgrade-repo [options]
```
  
### Opțiuni
  
- `--simulation-mode`, `-s`: Când este activată, această opțiune rulează comanda în modul de simulare, care afișează instrucțiunile SQL care ar fi executate, dar nu le execută efectiv. Acest lucru este util pentru previzualizarea modificărilor fără a face modificări în depozit.  

  
### Exemplu
  
Pentru a actualiza depozitul ***digna***, puteți rula comanda fără opțiuni:
  
```bash
dignacli upgrade-repo
```  
Pentru a rula upgrade-ul în modul de simulare (pentru a vedea instrucțiunile SQL fără a le aplica):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Această comandă este crucială pentru menținerea sistemului ***digna***, asigurând că schema bazei de date și celelalte componente ale depozitului sunt actualizate la ultima versiune a software-ului.

## Utilizarea comenzii `encrypt`
  
Comanda `encrypt` din CLI-ul ***digna*** este folosită pentru a cripta o parolă.
  
### Utilizare comandă
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumente
- **PASSWORD**: Parola care trebuie criptată (obligatoriu).
  
### Exemplu
  
Pentru a cripta o parolă, trebuie să furnizați parola ca argument.   
De exemplu, pentru a cripta parola `mypassword123`, ați folosi:
```bash
dignacli encrypt mypassword123
```
Această comandă va returna versiunea criptată a parolei furnizate, care poate fi folosită apoi în contexte securizate. Dacă argumentul pentru parolă nu este furnizat, CLI-ul va afișa o eroare indicând argumentul lipsă.

## Utilizarea comenzii `generate-key`
  
Comanda `generate-key` este folosită pentru a genera o cheie Fernet, esențială pentru securizarea parolelor stocate în depozitul ***digna***.
  
### Utilizare comandă
```bash
dignacli generate-key
```
  
# Managementul datelor

## Utilizarea comenzii `clean-up`

Comanda `clean-up` din CLI-ul ***digna*** este folosită pentru a elimina profile, predicții și date ale sistemului de semaforizare pentru unul sau mai multe surse de date dintr-un proiect specificat. Această comandă este esențială pentru gestionarea ciclului de viață al datelor, ajutând la menținerea unui mediu de date organizat și eficient prin curățarea datelor învechite sau inutile.

### Utilizare comandă

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumente
  
- **PROJECT_NAME**: Numele proiectului din care se vor elimina datele (obligatoriu). Folosirea cuvântului cheie all-projects în acest argument indică ***digna*** să itereze peste toate proiectele existente și să aplice această comandă.
- **FROM_DATE**: Data și ora de început pentru eliminarea datelor. Formatele acceptate includ %Y-%m-%d, %Y-%m-%dT%H:%M:%S sau %Y-%m-%d %H:%M:%S (obligatoriu).
- **TO_DATE**: Data și ora de sfârșit pentru eliminarea datelor, urmând aceleași formate ca FROM_DATE (obligatoriu).
  
### Opțiuni
  
- `--table-name`, `-tn`: Limitează operațiunea de clean-up la un tabel specific din proiect.
- `--table-filter`, `-tf`: Filtrează pentru a limita clean-up-ul la tabele care conțin substring-ul specificat în numele lor.
- `--timing`, `-tm`: Afișează durata procesului de clean-up după finalizare.
- `--help`: Afișează informații de ajutor pentru comanda clean-up și se oprește.
  
### Exemplu
  
Pentru a elimina date din proiectul ProjectA între 1 ianuarie 2023 și 30 iunie 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Pentru a elimina date doar dintr-un tabel specific numit `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Această comandă ajută la gestionarea stocării datelor și asigură că depozitul conține doar informațiile relevante.

## Utilizarea comenzii `inspect`

Comanda `inspect` din CLI-ul ***digna*** este folosită pentru a crea profile, predicții și date ale sistemului de semaforizare pentru una sau mai multe surse de date dintr-un proiect specificat. Această comandă ajută la analizarea și monitorizarea datelor pe o perioadă definită.

### Utilizare comandă

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumente
  
- **PROJECT_NAME**: Numele proiectului pentru care se vor inspecta datele (obligatoriu). Folosirea cuvântului cheie all-projects în acest argument indică ***digna*** să itereze peste toate proiectele existente și să aplice această comandă.
- **FROM_DATE**: Data și ora de început pentru inspecția datelor. Formatele acceptate includ %Y-%m-%d, %Y-%m-%dT%H:%M:%S sau %Y-%m-%d %H:%M:%S (obligatoriu).
- **TO_DATE**: Data și ora de sfârșit pentru inspecția datelor, urmând aceleași formate ca FROM_DATE (obligatoriu).
  
### Opțiuni

- `--table-name`, `-tn`: Limitează inspecția la un tabel specific din proiect.
- `--table-filter`, `-tf`: Filtrează pentru a inspecta doar tabelele care conțin substring-ul specificat în numele lor.
- `--do-profile`: Declanșează recollectarea profilelor. Implicit este do-profile.
- `--no-do-profile`: Previne recollectarea profilelor.
- `--do-prediction`: Declanșează recalcularea predicțiilor. Implicit este do-prediction.
- `--no-do-prediction`: Previne recalcularea predicțiilor.
- `--do-alert-status`: Declanșează recalcularea stărilor de alertă. Implicit este do-alert-status.
- `--no-do-alert-status`: Previne recalcularea stărilor de alertă.
- `--iterative`: Declanșează inspecția unei perioade folosind iterații zilnice. Implicit este iterative.
- `--no-iterative`: Declanșează inspecția întregii perioade dintr-o singură dată.
- `--timing`, `-tm`: Afișează durata procesului de inspecție după finalizare.
  
### Exemplu
  
Pentru a inspecta datele pentru proiectul `ProjectA` din 1 ianuarie 2024 până pe 31 ianuarie 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Pentru a inspecta doar un tabel specific și a forța recalcularea predicțiilor:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Această comandă este utilă pentru generarea de profile și predicții actualizate, monitorizarea integrității datelor și gestionarea sistemelor de alertă într-un interval de timp specificat pentru proiect.

## Utilizarea comenzii `tls-status`

Comanda `tls-status` din CLI-ul ***digna*** este folosită pentru a interoga starea Traffic Light System (TLS) pentru un tabel specific dintr-un proiect într-o anumită dată. Sistemul de semaforizare oferă informații despre sănătatea și calitatea datelor, indicând eventualele probleme sau alerte care necesită atenție.
  
### Utilizare comandă
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumente
  
- **PROJECT_NAME**: Numele proiectului pentru care se interoghează starea TLS (obligatoriu).
- **TABLE_NAME**: Tabelul specific din proiect pentru care este necesară starea TLS (obligatoriu).
- **DATE**: Data pentru care se interoghează starea TLS, de obicei în formatul %Y-%m-%d (obligatoriu).
  
### Exemplu
  
Pentru a verifica starea TLS pentru un tabel numit UserData în proiectul ProjectA la data de 1 iulie 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Această comandă ajută utilizatorii să monitorizeze și să mențină calitatea datelor oferind un raport clar și acționabil bazat pe criterii predefinite.

## Utilizarea comenzii `list-projects`
  
Comanda `list-projects` din CLI-ul ***digna*** este folosită pentru a afișa o listă cu toate proiectele disponibile în sistemul ***digna***.
  
### Utilizare comandă
  
```bash
dignacli list-projects
```

Această comandă este deosebit de utilă pentru administratori și utilizatori care gestionează mai multe proiecte, oferind o privire rapidă asupra proiectelor disponibile în depozitul ***digna***.

## Utilizarea comenzii `list-ds`

Comanda `list-ds` din CLI-ul ***digna*** este folosită pentru a afișa o listă cu toate sursele de date disponibile într-un proiect specificat. Această comandă este utilă pentru înțelegerea activelor de date disponibile pentru analiză și gestionare în sistemul ***digna***.

### Utilizare comandă
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumente
- **PROJECT_NAME**: Numele proiectului pentru care se listează sursele de date (obligatoriu).
  
### Exemplu
  
Pentru a lista toate sursele de date din proiectul numit `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Această comandă oferă utilizatorilor o imagine de ansamblu asupra surselor de date disponibile într-un proiect, ajutându-i să navigheze și să gestioneze mai eficient peisajul de date.