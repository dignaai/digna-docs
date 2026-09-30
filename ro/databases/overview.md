# Prezentarea conexiunilor la baze de date

---

## Cuprins

1. [Cum funcționează conexiunile](#how-connections-work)
2. [Ghiduri pe tehnologii](#technology-guides)
3. [Cerință prealabilă: instalați driverul ODBC pe gazda digna](#install-the-driver)
4. [Creați o conexiune la baza de date](#create-a-database-connection)
5. [Proprietăți ODBC](#odbc-properties)
6. [Criptarea valorilor proprietăților](#encrypting-property-values)
7. [Testarea unei conexiuni](#testing-a-connection)
8. [Ce bază de date vede conexiunea](#which-database-the-connection-sees)
9. [Modul de profilare și Work Schema](#profiling-mode-and-work-schema)
10. [Utilizarea unui DSN în schimb](#using-a-dsn-instead)
11. [Depanare](#troubleshooting)

---

## Cum funcționează conexiunile {: #how-connections-work }

*digna* accesează fiecare tehnologie sursă prin **ODBC**. O conexiune este o listă de proprietăți
ODBC pe care le introduceți ca perechi cheie/valoare. Când *digna* deschide conexiunea, unește
aceste perechi într-un șir de conexiune — `Key=Value`, separate prin `;`, în ordinea în care le-ați
listat — și îl transmite managerului de drivere ODBC de pe gazda *digna*.

Faptul că introduceți singur proprietățile este ceea ce face configurarea **fără DSN** (DSN-less):
conexiunea conține tot ce are nevoie driverul, deci nu trebuie înregistrată nicio sursă de date
ODBC (DSN) pe gazdă. Aceasta este modalitatea recomandată de configurare a *digna*, deoarece
definiția conexiunii se află în întregime în *digna* și se mută odată cu aceasta.

### De ce ODBC {: #why-odbc }

Versiunile anterioare ofereau o alegere între un driver specific fiecărei tehnologii și ODBC,
selectată cu un comutator **Use ODBC**. Începând cu Release 2026.06, *digna* se bazează doar pe
ODBC. O singură interfață standard vă oferă mai mult decât un set de drivere dedicate:

- **Autentificare** — autentificarea face parte din ODBC, astfel încât o conexiune poate folosi
  orice acceptă driverul său: parole, token-uri și PAT-uri, Kerberos și Active Directory, MFA și
  single sign-on în browser, identitate cloud, certificate client și TLS. Metodele noi vin odată
  cu o actualizare a driverului, fără a aștepta o versiune *digna*.
- **Drivere întreținute de furnizorii bazelor de date** — driverul propriu al furnizorului ține
  pasul cu noile versiuni de server și cu remedierile de securitate, iar dvs. îl puteți actualiza
  după propriul program, independent de *digna*.
- **O singură modalitate de a configura totul** — fiecare tehnologie este o listă de proprietăți
  cheie/valoare, cu aceeași interfață, aceeași criptare a valorilor sensibile și aceeași depanare,
  în loc de un set diferit de câmpuri pentru fiecare sursă.
- **Reglaj și acoperire** — opțiunile la nivel de driver, precum timeout-uri, setări TLS, proxy-uri
  și dimensiuni de fetch, sunt disponibile pentru fiecare sursă, iar orice tehnologie cu un driver
  ODBC conform poate fi conectată, inclusiv cele pentru care *digna* nu publică un ghid dedicat.

!!! note "Ce s-a schimbat în interfață"

    Comutatorul **Use ODBC** și câmpurile separate pentru gazdă, port, bază de date, utilizator și
    parolă nu mai există. O conexiune care nu folosește deja ODBC are nevoie de introducerea
    proprietăților ODBC înainte de a funcționa din nou — consultați
    [Creați o conexiune la baza de date](#create-a-database-connection).

---

## Ghiduri pe tehnologii {: #technology-guides }

Numele proprietăților diferă de la un driver la altul, iar fiecare tehnologie are unul sau două
detalii pe care celelalte nu le au. Ghidurile de mai jos acoperă acea parte; această pagină
acoperă partea *digna*, care este aceeași pentru toate.

!!! important "Seturile de proprietăți din ghiduri sunt exemple"

    Fiecare ghid prezintă o combinație despre care se știe că funcționează — cea pe care este
    testată *digna*. Este un punct de plecare, nu o specificație: proprietățile aparțin driverului
    ODBC, iar care dintre ele există, cum se numesc și ce valori acceptă diferă între versiunile de
    driver și furnizori, între Windows, Linux și macOS, și în funcție de modul în care este
    configurat serverul sursă — metoda de autentificare, TLS, gateway, port. Așteptați-vă să ajustați
    una sau două valori și considerați documentația versiunii de driver instalate ca referință.

| Tehnologie | Ghid | Bine de știut |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Pool-urile serverless necesită `-ondemand` în numele gazdei și acceptă doar profilarea *Standard* |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Autentificare cu token: `UID=token`, PAT în `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Cataloagele provin de la driver, nu dintr-o interogare |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Numele driverului este între acolade: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` acceptă fie un connect descriptor complet, fie un alias `tnsnames.ora` |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` trebuie să corespundă cerințelor serverului |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Programmatic access token este calea de autentificare testată |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` decide ce scheme poate vedea *digna* |
| **Teradata** | [Teradata](teradata_connector_guide.md) | Gazda se trece în `DBCNAME`; bazele de date funcționează ca scheme |

---

## Cerință prealabilă: instalați driverul ODBC pe gazda digna {: #install-the-driver }

*digna* deschide conexiunile sursă de pe **serverul care rulează backend-ul digna**, nu din
browser. Prin urmare, driverul ODBC trebuie instalat pe acea mașină, iar numele său trebuie
înregistrat la managerul local de drivere.

=== "Windows"

    Instalați driverul pe 64 de biți al furnizorului, apoi deschideți
    **ODBC Data Source Administrator (64-bit)** și treceți la fila **Drivers**. Numele listate
    acolo sunt exact valorile pe care le puteți folosi pentru proprietatea `Driver`.

=== "Linux"

    Instalați **unixODBC** și driverul furnizorului, apoi listați numele driverelor înregistrate:

    ```bash
    odbcinst -q -d
    ```

    Numele afișate între paranteze drepte sunt valorile pe care le puteți folosi pentru
    proprietatea `Driver`. Ele provin din `/etc/odbcinst.ini` (sau din fișierul raportat de
    `odbcinst -j`).

=== "macOS"

    Instalați **unixODBC** (de exemplu cu `brew install unixodbc`) și driverul furnizorului, apoi
    listați numele driverelor înregistrate:

    ```bash
    odbcinst -q -d
    ```

!!! warning "Numele driverului trebuie să corespundă caracter cu caracter"

    `Driver` este transmis nemodificat managerului de drivere. `Simba Spark ODBC Driver` și
    `Simba Spark ODBC Driver 64` sunt drivere diferite din punctul de vedere al managerului de
    drivere, iar un nume care nu este înregistrat produce o eroare *data source name not found*,
    chiar dacă nu este implicat niciun DSN.

În locul unui nume înregistrat, toți managerii de drivere uzuali acceptă și calea completă către
biblioteca driverului, de exemplu `Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. Acest
lucru este util atunci când driverul este instalat, dar nu este înregistrat.

---

## Creați o conexiune la baza de date {: #create-a-database-connection }

Deschideți **Admin Panel**, accesați fila **Database Connections** și faceți clic pe
**Add DB Connection**. Ecranul solicită cinci lucruri:

| Câmp | Descriere |
|---|---|
| **Name** | Numele conexiunii. Este folosit pentru a face referire la conexiune în alte ecrane. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake sau Hive. Selectează dialectul SQL generat de *digna*, deci trebuie să corespundă sursei — nu driverului. Azure Synapse Analytics este o conexiune **SQL Server**. |
| **ODBC Properties** | Perechile cheie/valoare descrise în [Proprietăți ODBC](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* sau *Session* — consultați [Modul de profilare și Work Schema](#profiling-mode-and-work-schema). |
| **Work Schema** | Schema care conține tabelele de lucru pentru profilarea *Permanent*. |

O conexiune este administrată centralizat și apoi atribuită unuia sau mai multor proiecte, astfel
încât aceeași conexiune poate deservi mai multe proiecte.

---

## Proprietăți ODBC {: #odbc-properties }

Faceți clic pe **Add Property** pentru fiecare proprietate și completați **Key**, **Value** și,
pentru secrete, caseta de selectare **Encrypted**. Fiecare ghid de tehnologie listează un set
exemplu pentru acea tehnologie, pe care îl adaptați versiunii driverului și serverului dvs. —
consultați [nota de mai sus](#technology-guides).

Indiferent de driver, un set de proprietăți acoperă aceleași patru lucruri:

- **`Driver`** — numele driverului înregistrat, așa cum este descris [mai sus](#install-the-driver).
- **Adresa serverului** — cheia diferă în funcție de driver: `SERVER`, `HOST`, `DBCNAME`,
  `Server` sau, pentru Oracle, connect descriptor-ul `DBQ`.
- **Acreditările** — de obicei `UID` și `PWD`; Snowflake folosește `UID` plus un `token`, iar
  Databricks folosește utilizatorul literal `token` plus personal access token-ul în `PWD`.
- **Baza de date sau catalogul de lucru**, acolo unde tehnologia are unul — consultați
  [Ce bază de date vede conexiunea](#which-database-the-connection-sees).

Orice altceva documentat de driver poate fi adăugat în același mod — connection pooling,
timeout-uri de socket, setări Kerberos, setări de proxy. *digna* nu interpretează proprietățile;
doar le transmite mai departe.

!!! warning "Valorile nu sunt escapate — puneți între acolade orice conține punct și virgulă"

    Deoarece proprietățile sunt unite cu `;`, o valoare care conține ea însăși `;` ar împărți șirul
    de conexiune în locul greșit. Încadrați astfel de valori între acolade: `PWD={p@ss;word}`.
    Același lucru este valabil pentru valorile cu `=` sau cu spații la început. Acesta este și
    motivul pentru care unele drivere se scriu prin convenție între acolade, ca în `{NetezzaSQL}`
    sau `{SnowflakeDSIIDriver}`.

---

## Criptarea valorilor proprietăților {: #encrypting-property-values }

Bifați **Encrypted** pentru fiecare proprietate care conține un secret — `PWD`, `token`, un client
secret. Valoarea este apoi criptată înainte de a fi stocată în repository-ul *digna*, mascată pe
ecran și decriptată doar atunci când este asamblat șirul de conexiune.

!!! tip "Sfat"

    O valoare criptată nu poate fi citită înapoi, nici în interfață, nici prin API — poate fi doar
    înlocuită. Păstrați secretele și în propriul manager de parole.

Proprietățile care nu sunt secrete — numele driverului, gazda, portul, baza de date — este mai bine
să rămână necriptate, astfel încât să rămână lizibile pentru cine va întreține conexiunea ulterior.

---

## Testarea unei conexiuni {: #testing-a-connection }

Faceți clic pe **Test** în dialogul *Add DB Connection* **înainte** de salvare. Testul folosește
valorile aflate în acel moment în formular și realizează o conectare reală, deci raportează exact
ce ar întâlni o inspecție — un nume de driver greșit, o parolă respinsă, o gazdă inaccesibilă. Nu
se stochează nimic: conexiunea de test este anulată (rollback), fie că reușește, fie că eșuează.

Pentru o conexiune care există deja, treceți cu mouse-ul peste rândul ei din fila
**Database Connections** și faceți clic pe pictograma **plug** (ștecher) pentru a o retesta. Este
cea mai rapidă modalitate de a verifica dacă o sursă este accesibilă după o rotire a parolei sau o
modificare a firewall-ului.

---

## Ce bază de date vede conexiunea {: #which-database-the-connection-sees }

Când adăugați o sursă de date, *digna* oferă cataloagele, schemele și tabelele pe care le poate
accesa conexiunea. Cât de departe ajunge aceasta depinde de tehnologie:

| Tehnologie | Cataloage oferite |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Doar baza de date **curentă** a conexiunii |
| **Teradata**, **Netezza**, **Databricks** | Toate bazele de date sau cataloagele pe care utilizatorul are voie să le vadă |
| **Hive**, **Impala** | Raportate de driver |

!!! important "O conexiune, o bază de date"

    Pentru PostgreSQL, SQL Server, Oracle și Snowflake, proprietățile trebuie să indice baza de date
    care conține schemele sursă — `DATABASE=…`, `Database=…` sau numele serviciului din `DBQ` la
    Oracle. Tabelele dintr-o altă bază de date nu sunt accesibile prin acea conexiune; adăugați o a
    doua conexiune pentru ea.

---

## Modul de profilare și Work Schema {: #profiling-mode-and-work-schema }

Modul de profilare determină modul în care *digna* procesează datele și calculează metricile:

- **Standard:** Metricile sunt calculate direct pe tabelele sursă, fără copierea datelor.
- **Permanent:** Datele pentru ziua inspectată sunt copiate într-un tabel permanent, iar metricile
  sunt calculate pe datele copiate.
- **Session:** Datele sunt copiate într-un tabel de sesiune sau temporar, iar metricile sunt
  calculate pe aceste date temporare.

Modul decide ce trebuie să aibă voie să facă utilizatorul conexiunii:

| Mod | Scrie | Drepturile necesare utilizatorului conexiunii |
|---|---|---|
| **Standard** | nimic | Citire pe tabelele sursă |
| **Permanent** | un tabel pentru fiecare sursă de date în **Work Schema** | Crearea și ștergerea tabelelor în **Work Schema** |
| **Session** | un tabel temporar pe care baza de date îl șterge odată cu sesiunea | Crearea de tabele temporare — **Work Schema** nu este folosită |

*Standard* doar citește, ceea ce îl face modul de ales atunci când *digna* primește acces doar în
citire. **Work Schema** este citită doar pentru *Permanent*, dar merită completată oricum, astfel
încât conexiunea să funcționeze în continuare dacă modul este schimbat ulterior.

---

## Utilizarea unui DSN în schimb {: #using-a-dsn-instead }

Un DSN funcționează în continuare — `DSN` este doar o altă proprietate:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

DSN-ul trebuie înregistrat pe gazda *digna*, pentru același cont de utilizator care rulează
backend-ul *digna*, și ca **System DSN** atunci când *digna* rulează ca serviciu. Tot ce este
configurat în DSN poate fi suprascris adăugându-l și ca proprietate.

Varianta fără DSN este cea implicită documentată, deoarece evită această stare pe partea gazdei:
conexiunea este descrisă complet în *digna*, iar o nouă gazdă *digna* are nevoie doar de driverul
instalat, fără nicio configurare.

---

## Depanare {: #troubleshooting }

### Data source name not found / no default driver specified

**Simptome:**
- Butonul **Test** raportează o eroare care menționează *data source name not found*, deși
  configurarea este fără DSN

**Cauze și soluții:**
1. Valoarea `Driver` nu corespunde unui nume de driver înregistrat — comparați-o cu fila
   **Drivers** din *ODBC Data Source Administrator (64-bit)* sau cu `odbcinst -q -d`
2. Driverul este instalat pe stația dvs. de lucru, dar nu pe gazda *digna*
3. Driverul este pe 32 de biți, în timp ce *digna* este pe 64 de biți — instalați driverul pe 64
   de biți
4. Proprietatea `Driver` lipsește cu totul și nu a fost specificat nici un `DSN`
5. Pe Linux și macOS, driverul este instalat, dar nu este înregistrat — specificați în schimb calea
   completă către biblioteca driverului sau înregistrați-l în `odbcinst.ini`

---

### Testul conexiunii expiră (timeout)

**Simptome:**
- **Test** se blochează și apoi eșuează după aproximativ o jumătate de minut

**Cauze și soluții:**
1. Gazda sau portul nu sunt accesibile de pe gazda *digna* — verificați firewall-ul și, pentru
   sursele cloud, lista de IP-uri permise
2. Numele gazdei este corect, dar portul aparține unui alt serviciu
3. Sursa are nevoie de mai mult decât cele 30 de secunde implicite pentru a accepta o conexiune —
   măriți `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` în secțiunea `[base]` din `config.toml` (`0` așteaptă
   nelimitat) și reporniți backend-ul
4. Un endpoint serverless își reia activitatea după inactivitate — reîncercați, iar dacă se
   întâmplă în mod obișnuit, măriți timeout-ul de login ca mai sus

---

### Autentificarea eșuează, deși acreditările sunt corecte

**Simptome:**
- Driverul raportează acreditări invalide, dar același utilizator funcționează într-un alt client
  SQL

**Cauze și soluții:**
1. Parola conține `;` — încadrați valoarea între acolade: `{p@ss;word}`
2. Un spațiu final a fost copiat în valoare
3. Driverul așteaptă un anumit mecanism de autentificare — de exemplu `AuthMech` pentru driverele
   Hive și Databricks, sau `authenticator` pentru Snowflake
4. Valoarea a fost stocată criptat și apoi editată — valorile criptate nu pot fi citite înapoi,
   deci reintroduceți secretul integral
5. Un token a expirat — personal access token-urile și programmatic access token-urile sunt emise
   cu o dată de expirare

---

### Ecranul sursei de date nu oferă baza de date sau schema așteptată

**Simptome:**
- Cataloage, scheme sau tabele lipsesc atunci când se adaugă o sursă de date

**Cauze și soluții:**
1. Conexiunea indică o altă bază de date — consultați
   [Ce bază de date vede conexiunea](#which-database-the-connection-sees)
2. Utilizatorul conexiunii nu are drepturi de citire pe schemă sau pe dicționarul de date
3. **Technology** nu corespunde sursei, astfel încât *digna* interoghează dicționarul de date greșit
4. Pentru Snowflake, utilizatorului nu i-a fost atribuit un warehouse implicit și nu a fost
   specificată proprietatea `Warehouse`, deci interogările de metadate nu pot rula

---

### Profilarea eșuează, deși testul conexiunii reușește

**Simptome:**
- **Test** trece, dar o inspecție eșuează la crearea tabelelor de lucru

**Cauze și soluții:**
1. Este selectată profilarea *Permanent*, iar utilizatorul conexiunii nu poate crea tabele în
   **Work Schema** — acordați drepturile sau treceți la *Session* ori *Standard*
2. **Work Schema** este goală sau numește o schemă care nu există, în timp ce este selectată
   profilarea *Permanent*
3. Este selectată profilarea *Session*, iar utilizatorul conexiunii nu poate crea tabele temporare
4. O interogare de profilare de lungă durată atinge timeout-ul interogării — măriți
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` în secțiunea `[base]` din `config.toml` (implicit 3600 de
   secunde, `0` dezactivează timeout-ul)

---

## Bune practici

**RECOMANDAT:**

- Instalați și înregistrați driverul pe gazda *digna* înainte de a configura conexiunea
- Bifați **Encrypted** pentru fiecare parolă și token
- Faceți clic pe **Test** înainte de salvare și retestați după o rotire a parolei
- Denumiți conexiunile după sursă și mediu, de exemplu `sales_dwh_prod`
- Oferiți *digna* un utilizator de bază de date dedicat, doar în citire acolo unde profilarea
  *Standard* este suficientă
- Păstrați o conexiune pentru fiecare bază de date sursă și adăugați una nouă în loc să o
  modificați pe prima

**DE EVITAT:**

- Stocarea secretelor necriptate sau partajarea unui utilizator de bază de date între *digna* și
  alte instrumente
- Utilizarea unui driver pe 32 de biți cu o instalare *digna* pe 64 de biți
- Bazarea pe un User DSN atunci când *digna* rulează ca serviciu — acesta nu va fi vizibil
- Introducerea unei valori care conține `;` într-o proprietate fără acolade
- Setarea **Work Schema** pe o schemă care conține date sursă

---

## Suport

Aveți nevoie de ajutor cu o conexiune la baza de date?

- **E-mail:** support@digna.ai
- **Documentație:** https://docs.digna.ai
- **Website:** https://www.digna.ai

---

**Release:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**