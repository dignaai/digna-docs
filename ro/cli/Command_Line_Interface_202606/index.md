# Referință CLI digna 2026.06
**2026-09-05**

Această pagină documentează setul complet de comenzi disponibile în versiunea **2026.06** a CLI ***digna***, inclusiv exemple de utilizare și opțiuni.

Executabilul se numește `digna`.

---

## Noțiuni de bază despre CLI

---

### Prezentare generală și sintaxă

CLI-ul versiunii **2026.06** folosește o ierarhie de comenzi structurată, bazată pe categorii:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` și `serve` sunt comenzi de sine stătătoare, fără subcomandă:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Opțiuni globale

Următoarele opțiuni globale se aplică tuturor comenzilor:

- `--help`, `-h`: Afișează informații de ajutor despre CLI sau despre o anumită categorie de comenzi ori subcomandă.
- `--stacktrace`: În caz de eroare, afișează întregul lanț de erori în loc de doar mesajul de nivel superior.

`--stacktrace` este o opțiune globală în sens strict: trebuie indicată **înainte** de categoria de comandă, nu după ea.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

Nu există un indicator `--version`. Folosiți în schimb comanda [`version`](#version).

### Cerințe preliminare

Majoritatea comenzilor au nevoie de un fișier `config.toml` lizibil și valid; unele necesită în plus o licență valabilă.
Tabelul următor consemnează ce încarcă fiecare categorie de comenzi înainte de a face orice altceva:

| Categorie de comenzi | Necesită `config.toml` | Necesită licență valabilă |
|---|---|---|
| `version` | nu | nu |
| `config check` | nu (tocmai acesta este obiectul raportării comenzii) | nu |
| `license check` | nu | ea *este* verificarea |
| `crypt` | da | nu |
| `serve` | da | nu |
| `project` | da | nu |
| `user` | da | da |
| `inspection` | da | da |
| `repo` | da | da |

Acolo unde este necesară o licență, se verifică atât semnătura, cât și data de expirare a acesteia, iar comanda se oprește înainte de a atinge repository-ul dacă oricare dintre ele eșuează.

### Coduri de ieșire

- `0`: comanda a reușit.
- `1`: comanda a eșuat. Mesajul de eroare este scris în stderr, precedat de prefixul `Error: `.

### help

Opțiunea `--help` oferă informații despre categoriile de comenzi, subcomenzile și opțiunile disponibile:

1. **Afișarea ajutorului general:**
   ```bash
   digna --help
   ```

2. **Obținerea ajutorului pentru categorii și comenzi specifice:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **Rezultatul include:**
   - **Descrierea comenzii:** Rezumat al scopului comenzii.
   - **Sintaxa:** Argumentele obligatorii și cele opționale.
   - **Opțiunile:** Indicatorii și parametrii specifici comenzii.

### version

Comanda `version` afișează versiunea instalată a ***digna***. Nu citește nicio configurație și nu validează nicio licență, așa că funcționează și pe o instalare al cărei fișier `config.toml` sau a cărei licență lipsește ori este invalidă.

Versiunea produsului este independentă de versiunea schemei repository-ului raportată de [`repo check`](#repo-check).

#### Utilizarea comenzii
```bash
digna version
```

#### Exemplu de ieșire
```text
2026.06
```

---

## Gestionarea configurației

---

### config check

Comanda `config check` validează fișierul de configurare (`config.toml`), verificând dacă toate secțiunile și setările obligatorii sunt prezente și corect formatate. Fiecare secțiune este validată separat, astfel încât o secțiune `[app]` defectă să nu ascundă starea secțiunii `[repo]`.

Secțiunile raportate sunt:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — opțională; o cheie absentă trece verificarea, iar o listă prezentă, dar formată greșit, nu o trece

Comanda nu încarcă în mod deliberat configurația aplicației așa cum o fac celelalte comenzi, pentru a putea diagnostica un fișier `config.toml` care ar împiedica pornirea aplicației ***digna***.

#### Utilizarea comenzii
```bash
digna config check [OPTIONS]
```

#### Opțiuni
- `--configpath`, `-c`: Calea către fișierul de configurare sau către un director care conține `config.toml` (implicit `./config.toml`).
- `--json`: Emite raportul de validare în format JSON. Are prioritate față de `--quiet`.
- `--quiet`, `-q`: Suprimă raportul și se bazează exclusiv pe codul de ieșire.

#### Exemplu
```bash
digna config check
```

Validarea unui anumit fișier de configurare și formatarea rezultatului ca JSON:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Exemplu de ieșire
```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: FAILED
    missing field `aes_gcm_key`
 - OIDC config(s): OK

Overall: FAILED
```

Un fișier lipsă sau o eroare de sintaxă TOML nu lasă nimic de validat secțiune cu secțiune și este raportat ca o singură eroare în loc de un raport, indiferent de `--quiet` sau `--json`.

---

## Gestionarea repository-ului

---

### repo check

Comanda `repo check` testează conexiunea la baza de date și verifică instalarea și versiunea repository-ului. Eșuează dacă schema configurată nu există sau dacă există, dar nu conține un repository ***digna***.

Versiunea raportată este versiunea schemei repository-ului, care este versionată separat de versiunea ***digna*** afișată de [`version`](#version).

#### Utilizarea comenzii
```bash
digna repo check
```

#### Exemplu de ieșire
```text
Repo version 3.0.0 installed
```

### repo install

Comanda `repo install` instalează un nou repository ***digna*** în schema configurată în `config.toml`, creând toate secvențele, tabelele, indecșii, constrângerile și înregistrările inițiale necesare.

Schema propriu-zisă **nu** este creată de această comandă — ea trebuie să existe în prealabil. Comanda refuză de asemenea să ruleze dacă în acea schemă este deja instalat un repository și indică [`repo upgrade`](#repo-upgrade) dacă versiunea instalată este una mai veche.

#### Utilizarea comenzii
```bash
digna repo install
```

#### Exemplu de ieșire
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

Comanda `repo upgrade` aplică migrări ale schemei bazei de date pentru a aduce un repository existent la versiunea așteptată de ediția instalată. Actualizările sunt aplicate câte un salt de versiune pe rând, de-a lungul unei căi de actualizare fixe, iar fiecare salt finalizat este consemnat în repository.

Dacă repository-ul se află deja la versiunea așteptată, comanda raportează că nu este necesară nicio actualizare și nu face nicio modificare.

#### Utilizarea comenzii
```bash
digna repo upgrade
```

#### Exemplu de ieșire
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Gestionarea criptării

---

### crypt gen-key

Comanda `crypt gen-key` generează o nouă cheie de criptare AES-GCM, destinată utilizării ca cheie de criptare în `config.toml`. Trebuie să existe deja un fișier `config.toml` care poate fi încărcat, chiar dacă cheia generată nu depinde de el.

#### Utilizarea comenzii
```bash
digna crypt gen-key
```

#### Exemplu de ieșire
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

Comanda `crypt encrypt` criptează un șir de caractere (de exemplu o parolă de bază de date) folosind cheia AES-GCM configurată în `config.toml` și afișează textul cifrat.

#### Utilizarea comenzii
```bash
digna crypt encrypt <VALUE>
```

#### Argumente
- **VALUE**: Șirul de caractere în clar care trebuie criptat (obligatoriu).

#### Exemplu
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

Comanda `crypt decrypt` decriptează un șir de caractere criptat cu AES-GCM folosind cheia configurată în `config.toml` și afișează textul în clar.

#### Utilizarea comenzii
```bash
digna crypt decrypt <VALUE>
```

#### Argumente
- **VALUE**: Șirul cifrat care trebuie decriptat (obligatoriu).

#### Exemplu
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Gestionarea utilizatorilor

---

### user add

Comanda `user add` creează un cont de utilizator nou în repository-ul ***digna***. Comanda eșuează dacă există deja un utilizator cu adresa de e-mail indicată.

#### Utilizarea comenzii
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argumente
- **EMAIL**: Adresa de e-mail a utilizatorului (obligatoriu).
- **PASSWORD**: Parola inițială a utilizatorului (obligatoriu).
- **DISPLAY_NAME**: Numele complet afișat al utilizatorului (obligatoriu).

#### Opțiuni
- `--admin`, `-a`: Creează utilizatorul cu privilegii de administrator (superutilizator).

#### Exemplu
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Pentru a crea un cont de administrator:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Exemplu de ieșire
```text
User created with ID: 42
```

### user list

Comanda `user list` listează toți utilizatorii înregistrați în format tabelar, cu ID, e-mail, nume afișat și indicatorul de administrator.

#### Utilizarea comenzii
```bash
digna user list
```

#### Exemplu de ieșire
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

Comanda `user modify` actualizează numele afișat și privilegiile de administrator ale unui cont de utilizator existent, identificat după adresa de e-mail.

Atât numele afișat, cât și indicatorul de administrator sunt scrise de fiecare dată. `--admin` este un comutator, nu o valoare: **omiterea lui revocă privilegiile de administrator**, așa că indicați-l ori de câte ori utilizatorul trebuie să le păstreze sau să le primească.

#### Utilizarea comenzii
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argumente
- **EMAIL**: Adresa de e-mail a utilizatorului de modificat (obligatoriu).
- **DISPLAY_NAME**: Numele afișat actualizat (obligatoriu).

#### Opțiuni
- `--admin`, `-a`: Acordă privilegii de administrator. Omiteți-l pentru a le revoca.
- `--valid-until`, `-v`: Acceptat din motive de compatibilitate, dar **momentan neaplicat**. Indicarea lui afișează un avertisment și nu schimbă nimic.

#### Exemplu
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Exemplu de ieșire
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

Comanda `user modify-pwd` actualizează parola unui cont de utilizator existent.

#### Utilizarea comenzii
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argumente
- **EMAIL**: Adresa de e-mail a utilizatorului a cărui parolă trebuie actualizată (obligatoriu).
- **PASSWORD**: Noua parolă (obligatoriu).

#### Exemplu
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

Comanda `user delete` elimină un cont de utilizator din sistem.

#### Utilizarea comenzii
```bash
digna user delete <EMAIL>
```

#### Argumente
- **EMAIL**: Adresa de e-mail a utilizatorului de șters (obligatoriu).

#### Exemplu
```bash
digna user delete jdoe@example.com
```

---

## Gestionarea proiectelor și a surselor de date

---

### project list

Comanda `project list` listează toate proiectele disponibile în repository, afișând ID-ul, numele și descrierea acestora.

#### Utilizarea comenzii
```bash
digna project list
```

#### Exemplu de ieșire
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

Comanda `project list-ds` listează toate sursele de date asociate unui proiect dat, afișând ID-ul, numele, tipul, schema și numele tabelei acestora.

#### Utilizarea comenzii
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argumente
- **PROJECT_NAME**: Numele proiectului ale cărui surse de date trebuie listate (obligatoriu). Numele trebuie să corespundă exact.

#### Exemplu
```bash
digna project list-ds ProjectA
```

#### Exemplu de ieșire
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

Comanda `project export-ds` exportă sursele de date ale unui proiect într-un document JSON.

Dacă nu se indică nici `--table-name`, nici `--table-id`, sunt exportate toate sursele de date ale proiectului.

#### Utilizarea comenzii
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argumente
- **PROJECT_NAME**: Numele proiectului din care se exportă sursele de date (obligatoriu).

#### Opțiuni
- `--table-name`, `-n`: Numele surselor de date de exportat. Se pot indica mai multe nume, separate prin spații.
- `--table-id`, `-i`: ID-urile surselor de date de exportat. Se pot indica mai multe ID-uri, separate prin spații.
- `--exportfile`, `-f`: Calea în care se salvează sursele de date exportate (implicit: `data_sources_export.json`).

#### Exemplu
Pentru a exporta toate sursele de date din `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Pentru a exporta anumite tabele:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Exemplu de ieșire
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

Comanda `project import-ds` importă surse de date dintr-un fișier de export într-un proiect țintă și raportează, pentru fiecare obiect, ce a fost creat, actualizat sau omis.

#### Utilizarea comenzii
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumente
- **PROJECT_NAME**: Numele proiectului țintă în care se importă (obligatoriu).
- **EXPORT_FILE**: Calea către fișierul JSON de export (obligatoriu).

#### Opțiuni
- `--output-file`, `-o`: Fișierul în care se scrie raportul de import. Fără el, raportul este trimis la stdout.
- `--output-format`, `-f`: Formatul raportului de import — `table`, `json` sau `csv` (implicit: `table`).

#### Exemplu
```bash
digna project import-ds ProjectB my_export.json
```

Pentru a obține un raport care poate fi citit automat:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

Raportul acoperă patru niveluri de obiecte — sursa de date, definiția setului de date, atributul și regula de validare — fiecare cu acțiunea sa de import, rezultatul, ID-ul obiectului rezultat și eventualele informații suplimentare.

### project plan-import-ds

Comanda `project plan-import-ds` prezintă în avans un import de surse de date într-un proiect țintă, arătând ce obiecte ar fi create, actualizate sau omise, fără a modifica nimic. Preia același fișier de export și aceleași opțiuni de raportare ca [`project import-ds`](#project-import-ds) și adaugă un număr de pas pentru fiecare obiect planificat.

#### Utilizarea comenzii
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumente
- **PROJECT_NAME**: Numele proiectului țintă (obligatoriu).
- **EXPORT_FILE**: Calea către fișierul de export (obligatoriu).

#### Opțiuni
- `--output-file`, `-o`: Fișierul în care se scrie planul de import. Fără el, planul este trimis la stdout.
- `--output-format`, `-f`: Formatul planului de import — `table`, `json` sau `csv` (implicit: `table`).

#### Exemplu
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Gestionarea inspecțiilor

---

### inspection run

Comanda `inspection run` creează o cerere de inspecție pentru un proiect și un interval de date, iar apoi — în funcție de opțiunile indicate — fie o așteaptă, fie se încheie imediat, fie o execută în propriul proces.

Cele trei moduri de execuție sunt:

- **Implicit (fără indicator)**: cererea este pusă în coadă pentru backend, iar CLI-ul o interoghează la fiecare două secunde, afișând progresul sarcinilor până când inspecția ajunge într-o stare finală. Este necesar un `digna serve` în execuție, altfel nimic nu preia cererea.
- **`--async-mode`**: cererea este pusă în coadă, iar ID-ul ei este afișat imediat. Folosiți [`inspection status`](#inspection-status) pentru a o urmări.
- **`--bypass-backend`**: inspecția este executată chiar de procesul CLI și nu este pusă în coadă, deci nu este nevoie de un server în execuție.

`--async-mode` și `--bypass-backend` se exclud reciproc.

În toate modurile, comanda se încheie cu un cod de ieșire diferit de zero dacă inspecția nu s-a finalizat cu succes.

#### Utilizarea comenzii
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argumente
- **PROJECT_NAME**: Numele proiectului țintă (obligatoriu). Numele trebuie să corespundă exact.
- **START_DATE**: Data de început a intervalului, în formatul `YYYY-MM-DD` (obligatoriu).
- **END_DATE**: Data de sfârșit a intervalului, în formatul `YYYY-MM-DD` (obligatoriu).

#### Opțiuni
- `--table-name`: Restrânge inspecția la o singură sursă de date a proiectului, indicată prin numele sursei de date. Fără ea, sunt inspectate toate sursele de date ale proiectului.
- `--async-mode`: Pune inspecția în coadă și afișează ID-ul cererii în loc să o aștepte. Nu poate fi combinată cu `--bypass-backend`.
- `--bypass-backend`: Rulează inspecția direct în procesul CLI în loc să o pună în coadă pentru backend. Nu poate fi combinată cu `--async-mode`.

#### Exemplu
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Pentru a trimite o inspecție asincronă:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Pentru a inspecta o singură sursă de date:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Exemplu de ieșire
Modul implicit:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Modul asincron:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

Comanda `inspection status` interoghează starea și progresul sarcinilor unei cereri de inspecție după ID-ul cererii.

#### Utilizarea comenzii
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argumente
- **INSPECTION_REQUEST_ID**: ID-ul numeric al cererii de inspecție (obligatoriu).

#### Exemplu
```bash
digna inspection status 1024
```

#### Exemplu de ieșire
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

Comanda `inspection abort` solicită anularea cererilor de inspecție în execuție sau în așteptare. Ea consemnează un eveniment de oprire pentru fiecare cerere vizată; backend-ul este cel care acționează pe baza lui, deci o întrerupere este o cerere de oprire, nu o oprire imediată.

#### Utilizarea comenzii
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argumente
- **INSPECTION_REQUEST_ID**: ID-ul cererii de inspecție care trebuie întreruptă. Obligatoriu, cu excepția cazului în care se indică `--killall`.

#### Opțiuni
- `--killall`: Întrerupe toate cererile de inspecție aflate în execuție și în așteptare. Are prioritate față de un ID de cerere indicat alături de ea.

#### Exemplu
Pentru a întrerupe o anumită cerere:
```bash
digna inspection abort 1024
```

Pentru a întrerupe toate inspecțiile active și cele din coadă:
```bash
digna inspection abort --killall
```

#### Exemplu de ieșire
`--killall` raportează ce a făcut; întreruperea unei singure cereri nu produce niciun rezultat afișat și semnalează succesul prin codul său de ieșire.
```text
All running and pending inspections have been aborted.
```

---

## Gestionarea licențelor

---

### license check

Comanda `license check` validează fișierul `license.toml`, verificându-i semnătura cu ajutorul cheii publice livrate împreună cu instalarea și controlând că nu a expirat. Nu citește nicio configurație a aplicației, deci funcționează și înainte ca `config.toml` să fie configurat.

#### Utilizarea comenzii
```bash
digna license check
```

#### Exemplu de ieșire
```text
License is valid
```

O semnătură invalidă și o licență expirată sunt raportate ca erori distincte, ambele cu codul de ieșire 1.

---

## Server și servicii de fundal

---

### serve

Comanda `serve` lansează serverul REST API al aplicației ***digna***, împreună cu planificatorul de inspecții și managerul de inspecții care rulează în fundal. La pornire, marchează de asemenea ca eșuată orice inspecție pe care repository-ul o mai consemnează ca fiind în execuție, întrucât nimic nu poate să fi supraviețuit dintr-un proces anterior.

Comanda rulează în prim-plan până când este oprită.

#### Utilizarea comenzii
```bash
digna serve [OPTIONS]
```

#### Opțiuni
- `--address`: Adresa de rețea la care se leagă serverul API (implicit: `127.0.0.1`).
- `--port`: Numărul portului pe care se ascultă (implicit: `8000`).

#### Exemplu
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Exemplu de ieșire
```text
Server running on http://0.0.0.0:8000
```