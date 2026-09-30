# Oversikt over databasetilkoblinger

---

## Innholdsfortegnelse

1. [Slik fungerer tilkoblinger](#how-connections-work)
2. [Veiledninger per teknologi](#technology-guides)
3. [Forutsetning: Installer ODBC-driveren på digna-verten](#install-the-driver)
4. [Opprett en databasetilkobling](#create-a-database-connection)
5. [ODBC-egenskaper](#odbc-properties)
6. [Kryptering av egenskapsverdier](#encrypting-property-values)
7. [Teste en tilkobling](#testing-a-connection)
8. [Hvilken database tilkoblingen ser](#which-database-the-connection-sees)
9. [Profiling Mode og Work Schema](#profiling-mode-and-work-schema)
10. [Bruke en DSN i stedet](#using-a-dsn-instead)
11. [Feilsøking](#troubleshooting)

---

## Slik fungerer tilkoblinger {: #how-connections-work }

*digna* når alle kildeteknologier over **ODBC**. En tilkobling er en liste med ODBC-egenskaper
som du legger inn som nøkkel/verdi-par. Når *digna* åpner tilkoblingen, setter den sammen parene
til en tilkoblingsstreng — `Key=Value`, skilt med `;`, i den rekkefølgen du oppga dem —
og sender den til ODBC-driverbehandleren (driver manager) på *digna*-verten.

Det at du selv legger inn egenskapene, er det som gjør oppsettet **DSN-løst**: tilkoblingen
inneholder alt driveren trenger, så ingen ODBC-datakilde (DSN) må registreres på verten.
Dette er den anbefalte måten å konfigurere *digna* på, fordi tilkoblingsdefinisjonen ligger
helt i *digna* og følger med den.

### Hvorfor ODBC {: #why-odbc }

Tidligere versjoner lot deg velge mellom en teknologispesifikk driver og ODBC via en
**Use ODBC**-bryter. Fra og med Release 2026.06 bygger *digna* utelukkende på ODBC. Ett enkelt,
standardisert grensesnitt gir deg mer enn en samling spesiallagde drivere kan:

- **Autentisering** — autentisering er en del av ODBC, så en tilkobling kan bruke alt driveren
  støtter: passord, tokens og PAT-er, Kerberos og Active Directory, MFA og nettleserbasert
  single sign-on, skyidentitet, klientsertifikater og TLS. Nye metoder kommer med en
  driveroppdatering, i stedet for å vente på en ny *digna*-versjon.
- **Drivere vedlikeholdt av databaseleverandørene** — leverandørens egen driver følger nye
  serverversjoner og sikkerhetsrettelser, og du kan oppdatere den etter din egen tidsplan,
  uavhengig av *digna*.
- **Én måte å konfigurere alt på** — alle teknologier er en liste med nøkkel/verdi-egenskaper, med
  samme grensesnitt, samme kryptering av sensitive verdier og samme feilsøking, i stedet for
  et eget sett med felter for hver kilde.
- **Finjustering og rekkevidde** — innstillinger på drivernivå som tidsavbrudd, TLS-innstillinger,
  proxyer og fetch-størrelser er tilgjengelige for alle kilder, og enhver teknologi med en
  kompatibel ODBC-driver kan kobles til, også de som *digna* ikke publiserer en egen
  veiledning for.

!!! note "Hva som er endret i grensesnittet"

    **Use ODBC**-bryteren og de separate feltene for host, port, database, bruker og passord
    finnes ikke lenger. En tilkobling som ikke allerede bruker ODBC, må få ODBC-egenskapene sine
    lagt inn før den fungerer igjen — se
    [Opprett en databasetilkobling](#create-a-database-connection).

---

## Veiledninger per teknologi {: #technology-guides }

Egenskapsnavnene varierer fra driver til driver, og hver teknologi har en eller to detaljer
som de andre ikke har. Veiledningene nedenfor dekker den delen; denne siden dekker
*digna*-siden, som er den samme for alle.

!!! important "Egenskapssettene i veiledningene er eksempler"

    Hver veiledning viser én kombinasjon som er kjent for å fungere — den *digna* er testet mot.
    Det er et utgangspunkt, ikke en spesifikasjon: egenskapene tilhører ODBC-driveren, og
    hvilke som finnes, hva de heter og hvilke verdier de godtar, varierer mellom
    driverversjoner og leverandører, mellom Windows, Linux og macOS, og med hvordan kildeserveren
    er konfigurert — autentiseringsmetode, TLS, gateway, port. Regn med å måtte justere en
    verdi eller to, og betrakt dokumentasjonen for driverversjonen du har installert som
    den gjeldende kilden.

| Teknologi | Veiledning | Verdt å vite |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Serverless pools krever `-ondemand` i vertsnavnet og støtter bare *Standard*-profilering |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Token-autentisering: `UID=token`, PAT i `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Kataloger kommer fra driveren, ikke fra en spørring |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Drivernavnet står i krøllparenteser: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` tar enten en fullstendig connect descriptor eller et `tnsnames.ora`-alias |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` må samsvare med det serveren krever |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Programmatic access token er den testede autentiseringsmetoden |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` avgjør hvilke skjemaer *digna* kan se |
| **Teradata** | [Teradata](teradata_connector_guide.md) | Verten angis i `DBCNAME`; databaser fungerer som skjemaer |

---

## Forutsetning: Installer ODBC-driveren på digna-verten {: #install-the-driver }

*digna* åpner kildetilkoblinger fra **serveren som kjører digna-backend**, ikke fra
nettleseren. ODBC-driveren må derfor være installert på den maskinen, og navnet dens må være
registrert hos den lokale driverbehandleren.

=== "Windows"

    Installer leverandørens 64-biters driver, åpne deretter **ODBC Data Source Administrator (64-bit)**
    og gå til fanen **Drivers**. Navnene som står oppført der, er nøyaktig de verdiene du kan
    bruke for egenskapen `Driver`.

=== "Linux"

    Installer **unixODBC** og leverandørens driver, og list deretter opp de registrerte drivernavnene:

    ```bash
    odbcinst -q -d
    ```

    Navnene i hakeparenteser er verdiene du kan bruke for egenskapen `Driver`. De
    kommer fra `/etc/odbcinst.ini` (eller filen som `odbcinst -j` viser).

=== "macOS"

    Installer **unixODBC** (for eksempel med `brew install unixodbc`) og leverandørens driver,
    og list deretter opp de registrerte drivernavnene:

    ```bash
    odbcinst -q -d
    ```

!!! warning "Drivernavnet må samsvare tegn for tegn"

    `Driver` sendes uendret til driverbehandleren. `Simba Spark ODBC Driver` og
    `Simba Spark ODBC Driver 64` er to forskjellige drivere for driverbehandleren,
    og et navn som ikke er registrert, gir feilen *data source name not found*,
    selv om ingen DSN er involvert.

I stedet for et registrert navn godtar alle vanlige driverbehandlere også den fullstendige
banen til driverbiblioteket, for eksempel `Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`.
Det er nyttig når driveren er installert, men ikke registrert.

---

## Opprett en databasetilkobling {: #create-a-database-connection }

Åpne **Admin Panel**, gå til fanen **Database Connections** og klikk
**Add DB Connection**. Skjermbildet ber om fem ting:

| Felt | Beskrivelse |
|---|---|
| **Name** | Navnet på tilkoblingen. Det brukes til å referere til tilkoblingen i andre skjermbilder. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake eller Hive. Den bestemmer hvilken SQL-dialekt *digna* genererer, så den må samsvare med kilden — ikke med driveren. Azure Synapse Analytics er en **SQL Server**-tilkobling. |
| **ODBC Properties** | Nøkkel/verdi-parene beskrevet under [ODBC-egenskaper](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* eller *Session* — se [Profiling Mode og Work Schema](#profiling-mode-and-work-schema). |
| **Work Schema** | Skjemaet som inneholder arbeidstabellene ved *Permanent*-profilering. |

En tilkobling administreres sentralt og tildeles deretter ett eller flere prosjekter, så den
samme tilkoblingen kan betjene flere prosjekter.

---

## ODBC-egenskaper {: #odbc-properties }

Klikk **Add Property** for hver egenskap, og fyll ut **Key**, **Value** og, for hemmeligheter,
avkrysningsboksen **Encrypted**. Hver teknologiveiledning viser et eksempelsett for den
aktuelle teknologien, som du tilpasser til driverversjonen og serveren din — se
[merknaden ovenfor](#technology-guides).

Uansett driver dekker et egenskapssett de samme fire tingene:

- **`Driver`** — det registrerte drivernavnet, som beskrevet [ovenfor](#install-the-driver).
- **Serverens adresse** — nøkkelen varierer fra driver til driver: `SERVER`, `HOST`, `DBCNAME`,
  `Server`, eller, for Oracle, connect descriptoren i `DBQ`.
- **Legitimasjon** — vanligvis `UID` og `PWD`; Snowflake bruker `UID` pluss en `token`, og
  Databricks bruker den bokstavelige brukeren `token` pluss personal access token i `PWD`.
- **Databasen eller katalogen det skal arbeides i**, der teknologien har en slik — se
  [Hvilken database tilkoblingen ser](#which-database-the-connection-sees).

Alt annet som driveren dokumenterer, kan legges til på samme måte — connection pooling,
socket-tidsavbrudd, Kerberos-innstillinger, proxyinnstillinger. *digna* tolker ikke
egenskapene; den sender dem bare videre.

!!! warning "Verdier escapes ikke — sett krøllparenteser rundt alt med semikolon"

    Siden egenskapene settes sammen med `;`, vil en verdi som selv inneholder `;`, dele
    tilkoblingsstrengen på feil sted. Sett slike verdier i krøllparenteser: `PWD={p@ss;word}`.
    Det samme gjelder verdier med `=` eller innledende mellomrom. Dette er også grunnen til at
    noen drivere tradisjonelt skrives i krøllparenteser, som `{NetezzaSQL}` eller `{SnowflakeDSIIDriver}`.

---

## Kryptering av egenskapsverdier {: #encrypting-property-values }

Kryss av for **Encrypted** for hver egenskap som inneholder en hemmelighet — `PWD`, `token`, en client secret.
Verdien krypteres da før den lagres i *digna*-repositoriet, maskeres i
skjermbildet og dekrypteres først når tilkoblingsstrengen settes sammen.

!!! tip "Tips"

    En kryptert verdi kan ikke leses tilbake, verken i brukergrensesnittet eller via API-et — den kan bare
    erstattes. Oppbevar hemmeligheter også i din egen passordbehandler.

Egenskaper som ikke er hemmelige — drivernavn, vert, port, database — bør helst være
ukrypterte, slik at de forblir lesbare for den som vedlikeholder tilkoblingen senere.

---

## Teste en tilkobling {: #testing-a-connection }

Klikk **Test** i dialogboksen *Add DB Connection* **før** du lagrer. Testen bruker verdiene
som står i skjemaet, og utfører en ekte tilkobling, så den rapporterer nøyaktig det en inspeksjon
ville støtt på — et feil drivernavn, et avvist passord, en vert som ikke kan nås. Ingenting lagres:
testtilkoblingen rulles tilbake enten den lykkes eller mislykkes.

For en tilkobling som allerede finnes, holder du markøren over raden i fanen **Database Connections** og
klikker på **plugg**-ikonet for å teste den på nytt. Det er den raskeste måten å sjekke om en kilde kan
nås etter et passordbytte eller en brannmurendring.

---

## Hvilken database tilkoblingen ser {: #which-database-the-connection-sees }

Når du legger til en datakilde, tilbyr *digna* katalogene, skjemaene og tabellene som
tilkoblingen kan nå. Hvor langt det rekker, avhenger av teknologien:

| Teknologi | Kataloger som tilbys |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Bare tilkoblingens **gjeldende** database |
| **Teradata**, **Netezza**, **Databricks** | Alle databaser eller kataloger brukeren har lov til å se |
| **Hive**, **Impala** | Rapporteres av driveren |

!!! important "Én tilkobling, én database"

    For PostgreSQL, SQL Server, Oracle og Snowflake må egenskapene peke på databasen
    som inneholder kildeskjemaene — `DATABASE=…`, `Database=…`, eller tjenestenavnet i
    Oracles `DBQ`. Tabeller i en annen database kan ikke nås gjennom den tilkoblingen; legg til en
    ny tilkobling for den.

---

## Profiling Mode og Work Schema {: #profiling-mode-and-work-schema }

Profileringsmodusen bestemmer hvordan *digna* behandler data og beregner metrikker:

- **Standard:** Metrikker beregnes direkte på kildetabellene uten at dataene kopieres.
- **Permanent:** Data for den inspiserte dagen kopieres til en permanent tabell, og metrikker
  beregnes på de kopierte dataene.
- **Session:** Data kopieres til en sesjonstabell eller midlertidig tabell, og metrikker beregnes på
  disse midlertidige dataene.

Modusen avgjør hva tilkoblingsbrukeren må ha lov til å gjøre:

| Modus | Skriver | Rettigheter tilkoblingsbrukeren trenger |
|---|---|---|
| **Standard** | ingenting | Lesetilgang til kildetabellene |
| **Permanent** | én tabell per datakilde i **Work Schema** | Opprette og slette tabeller i **Work Schema** |
| **Session** | en midlertidig tabell som databasen sletter sammen med sesjonen | Opprette midlertidige tabeller — **Work Schema** brukes ikke |

*Standard* leser bare, noe som gjør den til modusen du bør velge når *digna* får
skrivebeskyttet tilgang. **Work Schema** leses bare ved *Permanent*, men det lønner seg å fylle det ut likevel, slik at
tilkoblingen fortsetter å fungere hvis modusen endres senere.

---

## Bruke en DSN i stedet {: #using-a-dsn-instead }

En DSN fungerer fortsatt — `DSN` er bare enda en egenskap:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

DSN-en må være registrert på *digna*-verten, for den samme brukerkontoen som kjører *digna*-backend,
og som en **System DSN** når *digna* kjører som en tjeneste. Alt som er konfigurert
i DSN-en, kan overstyres ved også å legge det til som en egenskap.

DSN-løst er den dokumenterte standarden fordi det unngår slik tilstand på verten: tilkoblingen er
fullstendig beskrevet i *digna*, og en ny *digna*-vert trenger bare at driveren er installert, uten
noen konfigurasjon.

---

## Feilsøking {: #troubleshooting }

### Data source name not found / no default driver specified

**Symptomer:**
- **Test**-knappen rapporterer en feil som nevner *data source name not found*, selv om
  oppsettet er DSN-løst

**Årsaker og løsninger:**
1. `Driver`-verdien samsvarer ikke med et registrert drivernavn — sammenlign den med fanen **Drivers**
   i *ODBC Data Source Administrator (64-bit)*, eller med `odbcinst -q -d`
2. Driveren er installert på arbeidsstasjonen din, men ikke på *digna*-verten
3. Driveren er 32-biters mens *digna* er 64-biters — installer 64-biters driveren
4. Egenskapen `Driver` mangler helt, og ingen `DSN` er oppgitt heller
5. På Linux og macOS er driveren installert, men ikke registrert — oppgi den fullstendige banen til
   driverbiblioteket i stedet, eller registrer den i `odbcinst.ini`

---

### Tilkoblingstesten får tidsavbrudd

**Symptomer:**
- **Test** henger og feiler deretter etter omtrent et halvt minutt

**Årsaker og løsninger:**
1. Verten eller porten kan ikke nås fra *digna*-verten — sjekk brannmuren og, for skykilder,
   IP-tillatelseslisten
2. Vertsnavnet er riktig, men porten tilhører en annen tjeneste
3. Kilden trenger lenger enn standard 30 sekunder for å godta en tilkobling — øk
   `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` i `[base]`-seksjonen i `config.toml` (`0` venter
   på ubestemt tid) og start backend på nytt
4. Et serverless-endepunkt våkner fra inaktiv tilstand — prøv igjen, og hvis det skjer jevnlig, øk
   innloggingstidsavbruddet som beskrevet ovenfor

---

### Autentiseringen feiler selv om legitimasjonen er riktig

**Symptomer:**
- Driveren rapporterer ugyldig legitimasjon, men den samme brukeren fungerer i en annen SQL-klient

**Årsaker og løsninger:**
1. Passordet inneholder `;` — sett verdien i krøllparenteser: `{p@ss;word}`
2. Et avsluttende mellomrom ble kopiert inn i verdien
3. Driveren forventer en bestemt autentiseringsmekanisme — for eksempel `AuthMech` for
   Hive- og Databricks-driverne, eller `authenticator` for Snowflake
4. Verdien ble lagret kryptert og deretter redigert — krypterte verdier kan ikke leses tilbake, så
   legg inn hemmeligheten på nytt i sin helhet
5. Et token har utløpt — personal access tokens og programmatic access tokens utstedes med
   en utløpsdato

---

### Datakildeskjermbildet tilbyr ikke forventet database eller skjema

**Symptomer:**
- Kataloger, skjemaer eller tabeller mangler når en datakilde legges til

**Årsaker og løsninger:**
1. Tilkoblingen peker på en annen database — se
   [Hvilken database tilkoblingen ser](#which-database-the-connection-sees)
2. Tilkoblingsbrukeren mangler lesetilgang til skjemaet eller til datakatalogen (data dictionary)
3. **Technology** samsvarer ikke med kilden, så *digna* spør mot feil datakatalog
4. For Snowflake er ingen standard warehouse tildelt brukeren, og ingen `Warehouse`-egenskap er
   oppgitt, så metadataspørringer kan ikke kjøres

---

### Profileringen feiler mens tilkoblingstesten lykkes

**Symptomer:**
- **Test** går gjennom, men en inspeksjon feiler når arbeidstabeller opprettes

**Årsaker og løsninger:**
1. *Permanent*-profilering er valgt, og tilkoblingsbrukeren kan ikke opprette tabeller i
   **Work Schema** — gi rettighetene, eller bytt til *Session* eller *Standard*
2. **Work Schema** er tomt eller angir et skjema som ikke finnes, mens *Permanent*-profilering
   er valgt
3. *Session*-profilering er valgt, og tilkoblingsbrukeren har ikke lov til å opprette midlertidige tabeller
4. En langvarig profileringsspørring når tidsavbruddet for spørringer — øk
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` i `[base]`-seksjonen i `config.toml` (standard 3600
   sekunder, `0` slår av tidsavbruddet)

---

## Beste praksis

**GJØR:**

- Installer og registrer driveren på *digna*-verten før du konfigurerer tilkoblingen
- Kryss av for **Encrypted** for hvert passord og token
- Klikk **Test** før du lagrer, og test på nytt etter et passordbytte
- Gi tilkoblinger navn etter kilde og miljø, for eksempel `sales_dwh_prod`
- Gi *digna* en egen databasebruker, med skrivebeskyttet tilgang der *Standard*-profilering er nok
- Ha én tilkobling per kildedatabase, og legg heller til en ny enn å bytte om den første

**IKKE:**

- Lagre hemmeligheter ukryptert, eller del én databasebruker mellom *digna* og andre verktøy
- Bruk en 32-biters driver med en 64-biters *digna*-installasjon
- Stol på en User DSN når *digna* kjører som en tjeneste — den vil ikke være synlig
- Legg inn en verdi som inneholder `;` i en egenskap uten krøllparenteser
- La **Work Schema** peke på et skjema som inneholder kildedata

---

## Støtte

Trenger du hjelp med en databasetilkobling?

- **E-post:** support@digna.ai
- **Dokumentasjon:** https://docs.digna.ai
- **Nettsted:** https://www.digna.ai

---

**Release:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**