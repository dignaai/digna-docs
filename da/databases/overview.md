# Oversigt over databaseforbindelser

---

## Indholdsfortegnelse

1. [Sådan fungerer forbindelser](#how-connections-work)
2. [Vejledninger per teknologi](#technology-guides)
3. [Forudsætning: Installer ODBC-driveren på digna-værten](#install-the-driver)
4. [Opret en databaseforbindelse](#create-a-database-connection)
5. [ODBC-egenskaber](#odbc-properties)
6. [Kryptering af egenskabsværdier](#encrypting-property-values)
7. [Test af en forbindelse](#testing-a-connection)
8. [Hvilken database forbindelsen ser](#which-database-the-connection-sees)
9. [Profiling Mode og Work Schema](#profiling-mode-and-work-schema)
10. [Brug af en DSN i stedet](#using-a-dsn-instead)
11. [Fejlfinding](#troubleshooting)

---

## Sådan fungerer forbindelser {: #how-connections-work }

*digna* når alle kildeteknologier over **ODBC**. En forbindelse er en liste af ODBC-egenskaber,
som du indtaster som nøgle/værdi-par. Når *digna* åbner forbindelsen, sammensætter den parrene
til en forbindelsesstreng — `Key=Value`, adskilt af `;`, i den rækkefølge du har angivet dem —
og giver den videre til ODBC-driveradministratoren (driver manager) på *digna*-værten.

Det er, fordi du selv indtaster egenskaberne, at opsætningen er **DSN-løs**: forbindelsen
indeholder alt, hvad driveren har brug for, så der skal ikke registreres nogen ODBC-datakilde
(DSN) på værten. Dette er den anbefalede måde at konfigurere *digna* på, fordi
forbindelsesdefinitionen ligger helt i *digna* og flytter med den.

### Hvorfor ODBC {: #why-odbc }

Tidligere versioner gav mulighed for at vælge mellem en teknologispecifik driver og ODBC via en
**Use ODBC**-kontakt. Fra og med Release 2026.06 bygger *digna* udelukkende på ODBC. En enkelt,
standardiseret grænseflade giver dig mere, end en række specialbyggede drivere kan:

- **Autentificering** — autentificering er en del af ODBC, så en forbindelse kan bruge alt,
  hvad dens driver understøtter: adgangskoder, tokens og PAT'er, Kerberos og Active Directory,
  MFA og browserbaseret single sign-on, cloud-identitet, klientcertifikater og TLS. Nye metoder
  kommer med en driveropdatering i stedet for at vente på en ny *digna*-version.
- **Drivere vedligeholdt af databaseleverandørerne** — leverandørens egen driver følger nye
  serverversioner og sikkerhedsrettelser, og du kan opdatere den efter din egen tidsplan,
  uafhængigt af *digna*.
- **Én måde at konfigurere alt på** — alle teknologier er en liste af nøgle/værdi-egenskaber med
  den samme grænseflade, den samme kryptering af følsomme værdier og den samme fejlfinding i
  stedet for et forskelligt sæt felter for hver kilde.
- **Finjustering og rækkevidde** — indstillinger på driverniveau som timeouts, TLS-indstillinger,
  proxyer og fetch-størrelser er tilgængelige for alle kilder, og enhver teknologi med en
  kompatibel ODBC-driver kan tilsluttes, også dem, som *digna* ikke udgiver en særskilt
  vejledning for.

!!! note "Hvad der er ændret i brugerfladen"

    **Use ODBC**-kontakten og de separate felter til host, port, database, bruger og adgangskode
    findes ikke længere. En forbindelse, der ikke allerede bruger ODBC, skal have sine
    ODBC-egenskaber indtastet, før den virker igen — se
    [Opret en databaseforbindelse](#create-a-database-connection).

---

## Vejledninger per teknologi {: #technology-guides }

Egenskabernes navne er forskellige fra driver til driver, og hver teknologi har en eller to
detaljer, som de andre ikke har. Vejledningerne nedenfor dækker den del; denne side dækker
*digna*-delen, som er den samme for dem alle.

!!! important "Egenskabssættene i vejledningerne er eksempler"

    Hver vejledning viser én kombination, der vides at virke — den, som *digna* er testet med.
    Det er et udgangspunkt, ikke en specifikation: egenskaberne tilhører ODBC-driveren, og
    hvilke der findes, hvad de hedder, og hvilke værdier de accepterer, varierer mellem
    driverversioner og leverandører, mellem Windows, Linux og macOS og med, hvordan kildeserveren
    er konfigureret — autentificeringsmetode, TLS, gateway, port. Regn med at skulle justere en
    værdi eller to, og betragt dokumentationen for den driverversion, du har installeret, som
    den gældende kilde.

| Teknologi | Vejledning | Godt at vide |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Serverless pools kræver `-ondemand` i værtsnavnet og understøtter kun *Standard*-profilering |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Token-autentificering: `UID=token`, PAT i `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Kataloger kommer fra driveren, ikke fra en forespørgsel |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Drivernavnet står i krøllede parenteser: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` tager enten en fuld connect descriptor eller et `tnsnames.ora`-alias |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` skal matche det, serveren kræver |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Programmatic access token er den testede autentificeringsmetode |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` afgør, hvilke skemaer *digna* kan se |
| **Teradata** | [Teradata](teradata_connector_guide.md) | Værten angives i `DBCNAME`; databaser fungerer som skemaer |

---

## Forudsætning: Installer ODBC-driveren på digna-værten {: #install-the-driver }

*digna* åbner kildeforbindelser fra **den server, der kører digna-backend**, ikke fra browseren.
ODBC-driveren skal derfor være installeret på den maskine, og dens navn skal være registreret
hos den lokale driveradministrator.

=== "Windows"

    Installer leverandørens 64-bit driver, åbn derefter **ODBC Data Source Administrator (64-bit)**
    og skift til fanen **Drivers**. Navnene, der vises der, er præcis de værdier, du kan bruge
    til egenskaben `Driver`.

=== "Linux"

    Installer **unixODBC** og leverandørens driver, og vis derefter de registrerede drivernavne:

    ```bash
    odbcinst -q -d
    ```

    Navnene i kantede parenteser er de værdier, du kan bruge til egenskaben `Driver`. De
    kommer fra `/etc/odbcinst.ini` (eller den fil, som `odbcinst -j` angiver).

=== "macOS"

    Installer **unixODBC** (for eksempel med `brew install unixodbc`) og leverandørens driver,
    og vis derefter de registrerede drivernavne:

    ```bash
    odbcinst -q -d
    ```

!!! warning "Drivernavnet skal matche tegn for tegn"

    `Driver` sendes uændret til driveradministratoren. `Simba Spark ODBC Driver` og
    `Simba Spark ODBC Driver 64` er to forskellige drivere set fra driveradministratorens side,
    og et navn, der ikke er registreret, giver fejlen *data source name not found*, selv om der
    slet ikke er nogen DSN involveret.

I stedet for et registreret navn accepterer alle gængse driveradministratorer også den fulde sti
til driverbiblioteket, for eksempel `Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. Det
er nyttigt, når driveren er installeret, men ikke registreret.

---

## Opret en databaseforbindelse {: #create-a-database-connection }

Åbn **Admin Panel**, gå til fanen **Database Connections**, og klik på
**Add DB Connection**. Skærmen beder om fem ting:

| Felt | Beskrivelse |
|---|---|
| **Name** | Forbindelsens navn. Det bruges til at henvise til forbindelsen på andre skærme. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake eller Hive. Den vælger den SQL-dialekt, *digna* genererer, så den skal matche kilden — ikke driveren. Azure Synapse Analytics er en **SQL Server**-forbindelse. |
| **ODBC Properties** | Nøgle/værdi-parrene beskrevet under [ODBC-egenskaber](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* eller *Session* — se [Profiling Mode og Work Schema](#profiling-mode-and-work-schema). |
| **Work Schema** | Skema, der indeholder arbejdstabellerne ved *Permanent*-profilering. |

En forbindelse administreres centralt og tildeles derefter et eller flere projekter, så den
samme forbindelse kan betjene flere projekter.

---

## ODBC-egenskaber {: #odbc-properties }

Klik på **Add Property** for hver egenskab, og udfyld **Key**, **Value** og, for hemmeligheder,
afkrydsningsfeltet **Encrypted**. Hver teknologivejledning viser et eksempelsæt for den
pågældende teknologi, som du tilpasser til din driverversion og server — se
[bemærkningen ovenfor](#technology-guides).

Uanset driveren dækker et egenskabssæt de samme fire ting:

- **`Driver`** — det registrerede drivernavn, som beskrevet [ovenfor](#install-the-driver).
- **Serverens adresse** — nøglen varierer fra driver til driver: `SERVER`, `HOST`, `DBCNAME`,
  `Server` eller, for Oracle, `DBQ`-connect descriptoren.
- **Legitimationsoplysninger** — som regel `UID` og `PWD`; Snowflake bruger `UID` plus en
  `token`, og Databricks bruger den bogstavelige bruger `token` plus personal access token i `PWD`.
- **Den database eller det katalog, der skal arbejdes i**, hvor teknologien har et — se
  [Hvilken database forbindelsen ser](#which-database-the-connection-sees).

Alt andet, som driveren dokumenterer, kan tilføjes på samme måde — connection pooling,
socket-timeouts, Kerberos-indstillinger, proxyindstillinger. *digna* fortolker ikke
egenskaberne; den sender dem blot videre.

!!! warning "Værdier escapes ikke — sæt krøllede parenteser om alt med semikolon"

    Da egenskaberne sammensættes med `;`, vil en værdi, der selv indeholder `;`, dele
    forbindelsesstrengen det forkerte sted. Omslut sådanne værdier med krøllede parenteser:
    `PWD={p@ss;word}`. Det samme gælder værdier med `=` eller indledende mellemrum. Det er også
    grunden til, at nogle drivere traditionelt skrives i krøllede parenteser, som i `{NetezzaSQL}`
    eller `{SnowflakeDSIIDriver}`.

---

## Kryptering af egenskabsværdier {: #encrypting-property-values }

Sæt flueben i **Encrypted** for hver egenskab, der indeholder en hemmelighed — `PWD`, `token`,
en client secret. Værdien krypteres så, før den gemmes i *digna*-repositoriet, maskeres på
skærmen og dekrypteres først, når forbindelsesstrengen sammensættes.

!!! tip "Tip"

    En krypteret værdi kan ikke læses igen, hverken i brugerfladen eller via API'et — den kan
    kun erstattes. Gem også hemmeligheder i din egen adgangskodeadministrator.

Egenskaber, der ikke er hemmelige — drivernavn, vært, port, database — bør helst ikke
krypteres, så de forbliver læsbare for den, der senere vedligeholder forbindelsen.

---

## Test af en forbindelse {: #testing-a-connection }

Klik på **Test** i dialogen *Add DB Connection*, **før** du gemmer. Testen bruger de værdier,
der aktuelt står i formularen, og udfører en rigtig forbindelse, så den rapporterer præcis det,
en inspektion ville ramme — et forkert drivernavn, en afvist adgangskode, en utilgængelig vært.
Intet gemmes: testforbindelsen rulles tilbage, uanset om den lykkes eller mislykkes.

For en forbindelse, der allerede findes, skal du holde musen over dens række i fanen
**Database Connections** og klikke på **stik**-ikonet for at teste den igen. Det er den
hurtigste måde at kontrollere, om en kilde kan nås efter et adgangskodeskift eller en
firewallændring.

---

## Hvilken database forbindelsen ser {: #which-database-the-connection-sees }

Når du tilføjer en datakilde, tilbyder *digna* de kataloger, skemaer og tabeller, som
forbindelsen kan nå. Hvor langt det rækker, afhænger af teknologien:

| Teknologi | Tilbudte kataloger |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Kun forbindelsens **aktuelle** database |
| **Teradata**, **Netezza**, **Databricks** | Alle databaser eller kataloger, brugeren har lov til at se |
| **Hive**, **Impala** | Rapporteres af driveren |

!!! important "Én forbindelse, én database"

    For PostgreSQL, SQL Server, Oracle og Snowflake skal egenskaberne pege på den database, der
    indeholder kildeskemaerne — `DATABASE=…`, `Database=…` eller servicenavnet i Oracles `DBQ`.
    Tabeller i en anden database kan ikke nås via den forbindelse; tilføj en ekstra forbindelse
    til den.

---

## Profiling Mode og Work Schema {: #profiling-mode-and-work-schema }

Profileringstilstanden bestemmer, hvordan *digna* behandler data og beregner metrikker:

- **Standard:** Metrikker beregnes direkte på kildetabellerne uden at kopiere data.
- **Permanent:** Data for den inspicerede dag kopieres til en permanent tabel, og metrikker
  beregnes på de kopierede data.
- **Session:** Data kopieres til en sessions- eller midlertidig tabel, og metrikker beregnes på
  disse midlertidige data.

Tilstanden afgør, hvad forbindelsesbrugeren skal have lov til:

| Tilstand | Skriver | Rettigheder, forbindelsesbrugeren har brug for |
|---|---|---|
| **Standard** | intet | Læseadgang til kildetabellerne |
| **Permanent** | en tabel per datakilde i **Work Schema** | Oprette og slette tabeller i **Work Schema** |
| **Session** | en midlertidig tabel, som databasen sletter sammen med sessionen | Oprette midlertidige tabeller — **Work Schema** bruges ikke |

*Standard* læser kun, hvilket gør den til den tilstand, du skal vælge, når *digna* får
skrivebeskyttet adgang. **Work Schema** læses kun ved *Permanent*, men det er alligevel værd at
udfylde det, så forbindelsen fortsat virker, hvis tilstanden ændres senere.

---

## Brug af en DSN i stedet {: #using-a-dsn-instead }

En DSN virker stadig — `DSN` er blot endnu en egenskab:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

DSN'en skal være registreret på *digna*-værten, for den samme brugerkonto, som kører
*digna*-backend, og som **System DSN**, når *digna* kører som en tjeneste. Alt, hvad der er
konfigureret i DSN'en, kan tilsidesættes ved også at tilføje det som en egenskab.

DSN-løs er den dokumenterede standard, fordi den undgår denne tilstand på værtssiden:
forbindelsen er fuldt beskrevet i *digna*, og en ny *digna*-vært skal have driveren installeret,
men intet konfigureret.

---

## Fejlfinding {: #troubleshooting }

### Data source name not found / no default driver specified

**Symptomer:**
- Knappen **Test** rapporterer en fejl, der nævner *data source name not found*, selv om
  opsætningen er DSN-løs

**Årsager og løsninger:**
1. `Driver`-værdien matcher ikke et registreret drivernavn — sammenlign den med fanen **Drivers**
   i *ODBC Data Source Administrator (64-bit)* eller med `odbcinst -q -d`
2. Driveren er installeret på din arbejdsstation, men ikke på *digna*-værten
3. Driveren er 32-bit, mens *digna* er 64-bit — installer 64-bit-driveren
4. Egenskaben `Driver` mangler helt, og der er heller ikke angivet nogen `DSN`
5. På Linux og macOS er driveren installeret, men ikke registreret — angiv i stedet den fulde sti
   til driverbiblioteket, eller registrer den i `odbcinst.ini`

---

### Forbindelsestesten får timeout

**Symptomer:**
- **Test** hænger og fejler derefter efter cirka et halvt minut

**Årsager og løsninger:**
1. Vært eller port kan ikke nås fra *digna*-værten — kontroller firewallen og, for cloudkilder,
   IP-tilladelseslisten
2. Værtsnavnet er korrekt, men porten tilhører en anden tjeneste
3. Kilden har brug for mere end standardværdien på 30 sekunder til at acceptere en forbindelse —
   hæv `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` i sektionen `[base]` i `config.toml` (`0` venter
   uendeligt), og genstart backend
4. Et serverless-endpoint vågner fra inaktivitet — prøv igen, og hæv login-timeouten som ovenfor,
   hvis det sker regelmæssigt

---

### Autentificeringen fejler, selv om legitimationsoplysningerne er korrekte

**Symptomer:**
- Driveren rapporterer ugyldige legitimationsoplysninger, men den samme bruger virker i en anden
  SQL-klient

**Årsager og løsninger:**
1. Adgangskoden indeholder `;` — omslut værdien med krøllede parenteser: `{p@ss;word}`
2. Et mellemrum til sidst er blevet kopieret med ind i værdien
3. Driveren forventer en bestemt autentificeringsmekanisme — for eksempel `AuthMech` for Hive- og
   Databricks-driverne eller `authenticator` for Snowflake
4. Værdien blev gemt krypteret og derefter redigeret — krypterede værdier kan ikke læses igen, så
   indtast hemmeligheden igen i sin helhed
5. Et token er udløbet — personal access tokens og programmatic access tokens udstedes med en
   udløbsdato

---

### Datakildeskærmen tilbyder ikke den forventede database eller det forventede skema

**Symptomer:**
- Kataloger, skemaer eller tabeller mangler, når en datakilde tilføjes

**Årsager og løsninger:**
1. Forbindelsen peger på en anden database — se
   [Hvilken database forbindelsen ser](#which-database-the-connection-sees)
2. Forbindelsesbrugeren mangler læserettigheder til skemaet eller til datakataloget (data dictionary)
3. **Technology** matcher ikke kilden, så *digna* forespørger det forkerte datakatalog
4. For Snowflake er der ikke tildelt brugeren noget standard-warehouse, og der er ikke angivet
   nogen `Warehouse`-egenskab, så metadataforespørgsler kan ikke køre

---

### Profileringen fejler, mens forbindelsestesten lykkes

**Symptomer:**
- **Test** består, men en inspektion fejler, når arbejdstabeller oprettes

**Årsager og løsninger:**
1. *Permanent*-profilering er valgt, og forbindelsesbrugeren kan ikke oprette tabeller i
   **Work Schema** — tildel rettighederne, eller skift til *Session* eller *Standard*
2. **Work Schema** er tomt eller angiver et skema, der ikke findes, mens *Permanent*-profilering
   er valgt
3. *Session*-profilering er valgt, og forbindelsesbrugeren må ikke oprette midlertidige tabeller
4. En langvarig profileringsforespørgsel rammer query-timeouten — hæv
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` i sektionen `[base]` i `config.toml` (standard 3600
   sekunder, `0` deaktiverer timeouten)

---

## Bedste praksis

**GØR:**

- Installer og registrer driveren på *digna*-værten, før du konfigurerer forbindelsen
- Sæt flueben i **Encrypted** for hver adgangskode og hvert token
- Klik på **Test**, før du gemmer, og test igen efter et adgangskodeskift
- Navngiv forbindelser efter kilde og miljø, for eksempel `sales_dwh_prod`
- Giv *digna* en dedikeret databasebruger, skrivebeskyttet hvor *Standard*-profilering er nok
- Hav én forbindelse per kildedatabase, og tilføj hellere en ekstra end at omstille den første

**UNDLAD:**

- At gemme hemmeligheder ukrypteret eller dele én databasebruger mellem *digna* og andre værktøjer
- At bruge en 32-bit driver med en 64-bit *digna*-installation
- At stole på en User DSN, når *digna* kører som en tjeneste — den vil ikke være synlig
- At indsætte en værdi, der indeholder `;`, i en egenskab uden krøllede parenteser
- At lade **Work Schema** pege på et skema, der indeholder kildedata

---

## Support

Brug for hjælp til en databaseforbindelse?

- **E-mail:** support@digna.ai
- **Dokumentation:** https://docs.digna.ai
- **Websted:** https://www.digna.ai

---

**Release:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**