# Översikt över databasanslutningar

---

## Innehållsförteckning

1. [Så fungerar anslutningar](#how-connections-work)
2. [Guider per teknik](#technology-guides)
3. [Förutsättning: installera ODBC-drivrutinen på digna-värden](#install-the-driver)
4. [Skapa en databasanslutning](#create-a-database-connection)
5. [ODBC-egenskaper](#odbc-properties)
6. [Kryptera egenskapsvärden](#encrypting-property-values)
7. [Testa en anslutning](#testing-a-connection)
8. [Vilken databas anslutningen ser](#which-database-the-connection-sees)
9. [Profileringsläge och Work Schema](#profiling-mode-and-work-schema)
10. [Använda en DSN i stället](#using-a-dsn-instead)
11. [Felsökning](#troubleshooting)

---

## Så fungerar anslutningar {: #how-connections-work }

*digna* når varje källteknik via **ODBC**. En anslutning är en lista med ODBC-egenskaper
som du anger som nyckel/värde-par. När *digna* öppnar anslutningen fogas paren samman till en
anslutningssträng — `Key=Value`, separerade med `;`, i den ordning du listade dem —
och lämnas till ODBC-drivrutinshanteraren på *digna*-värden.

Att du själv anger egenskaperna är det som gör konfigurationen **DSN-lös**: anslutningen innehåller
allt som drivrutinen behöver, så ingen ODBC-datakälla (DSN) behöver registreras på värden.
Det är det rekommenderade sättet att konfigurera *digna*, eftersom anslutningsdefinitionen finns
helt i *digna* och följer med den.

### Varför ODBC {: #why-odbc }

Tidigare releaser erbjöd ett val mellan en teknikspecifik drivrutin och ODBC, via reglaget
**Use ODBC**. Från och med Release 2026.06 bygger *digna* enbart på ODBC. Ett enda standardiserat
gränssnitt ger dig mer än en uppsättning specialbyggda drivrutiner kan:

- **Autentisering** — autentisering är en del av ODBC, så en anslutning kan använda allt som dess
  drivrutin stöder: lösenord, token och PAT, Kerberos och Active Directory, MFA och
  webbläsarbaserad single sign-on, molnidentitet, klientcertifikat och TLS. Nya metoder kommer
  med en drivrutinsuppdatering, i stället för att vänta på en *digna*-release.
- **Drivrutiner som underhålls av databasleverantörerna** — leverantörens egen drivrutin följer nya serverversioner
  och säkerhetsrättningar, och du kan uppdatera den enligt ditt eget schema, oberoende av
  *digna*.
- **Ett sätt att konfigurera allt** — varje teknik är en lista med nyckel/värde-egenskaper, med
  samma gränssnitt, samma kryptering av känsliga värden och samma felsökning,
  i stället för en ny uppsättning fält per källa.
- **Finjustering och räckvidd** — alternativ på drivrutinsnivå som timeouts, TLS-inställningar, proxyservrar och
  fetch-storlekar finns för alla källor, och alla tekniker med en kompatibel ODBC-drivrutin kan
  anslutas, även sådana som *digna* inte publicerar någon egen guide för.

!!! note "Vad som har ändrats i gränssnittet"

    Reglaget **Use ODBC** och de separata fälten för värd, port, databas, användare och lösenord
    finns inte längre. En anslutning som inte redan använder ODBC måste få sina ODBC-egenskaper angivna
    innan den fungerar igen — se
    [Skapa en databasanslutning](#create-a-database-connection).

---

## Guider per teknik {: #technology-guides }

Egenskapsnamnen skiljer sig mellan drivrutiner, och varje teknik har en eller två detaljer som
de andra saknar. Guiderna nedan täcker den delen; denna sida täcker *digna*-sidan, som
är densamma för alla.

!!! important "Egenskapsuppsättningarna i guiderna är exempel"

    Varje guide visar en kombination som är känd för att fungera — den som *digna* testas mot.
    Den är en utgångspunkt, inte en specifikation: egenskaperna tillhör ODBC-drivrutinen, och
    vilka som finns, vad de heter och vilka värden de accepterar skiljer sig mellan drivrutinsversioner
    och leverantörer, mellan Windows, Linux och macOS, och beroende på hur källservern är
    konfigurerad — autentiseringsmetod, TLS, gateway, port. Räkna med att justera ett eller två värden,
    och se dokumentationen för den drivrutinsversion du installerat som den avgörande källan.

| Teknik | Guide | Bra att veta |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Serverlösa pooler kräver `-ondemand` i värdnamnet och stöder endast profileringsläget *Standard* |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Tokenautentisering: `UID=token`, PAT i `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Kataloger kommer från drivrutinen, inte från en fråga |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Drivrutinsnamnet står inom klammerparenteser: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` tar antingen en fullständig connect descriptor eller ett alias från `tnsnames.ora` |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` måste motsvara det som servern kräver |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Programmatic access token är den testade autentiseringsvägen |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` avgör vilka scheman *digna* kan se |
| **Teradata** | [Teradata](teradata_connector_guide.md) | Värden anges i `DBCNAME`; databaser fungerar som scheman |

---

## Förutsättning: installera ODBC-drivrutinen på digna-värden {: #install-the-driver }

*digna* öppnar källanslutningar från **servern som kör digna-backenden**, inte från
webbläsaren. ODBC-drivrutinen måste därför installeras på den maskinen, och dess namn måste
vara registrerat i den lokala drivrutinshanteraren.

=== "Windows"

    Installera leverantörens 64-bitarsdrivrutin, öppna sedan **ODBC Data Source Administrator (64-bit)**
    och växla till fliken **Drivers**. Namnen som listas där är exakt de värden du kan
    använda för egenskapen `Driver`.

=== "Linux"

    Installera **unixODBC** och leverantörens drivrutin, och lista sedan de registrerade drivrutinsnamnen:

    ```bash
    odbcinst -q -d
    ```

    Namnen inom hakparenteser är de värden du kan använda för egenskapen `Driver`. De
    kommer från `/etc/odbcinst.ini` (eller den fil som `odbcinst -j` anger).

=== "macOS"

    Installera **unixODBC** (till exempel med `brew install unixodbc`) och leverantörens drivrutin,
    och lista sedan de registrerade drivrutinsnamnen:

    ```bash
    odbcinst -q -d
    ```

!!! warning "Drivrutinsnamnet måste stämma tecken för tecken"

    `Driver` skickas oförändrat till drivrutinshanteraren. `Simba Spark ODBC Driver` och
    `Simba Spark ODBC Driver 64` är olika drivrutiner för drivrutinshanteraren,
    och ett namn som inte är registrerat ger felet *data source name not found*
    trots att ingen DSN är inblandad.

I stället för ett registrerat namn accepterar alla vanliga drivrutinshanterare även den fullständiga sökvägen till
drivrutinsbiblioteket, till exempel `Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. Det är
användbart när drivrutinen är installerad men inte registrerad.

---

## Skapa en databasanslutning {: #create-a-database-connection }

Öppna **Admin Panel**, gå till fliken **Database Connections** och klicka på
**Add DB Connection**. Skärmen frågar efter fem saker:

| Fält | Beskrivning |
|---|---|
| **Name** | Anslutningens namn. Det används för att referera till anslutningen på andra skärmar. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake eller Hive. Det väljer den SQL-dialekt som *digna* genererar, så det måste motsvara källan — inte drivrutinen. Azure Synapse Analytics är en **SQL Server**-anslutning. |
| **ODBC Properties** | Nyckel/värde-paren som beskrivs i [ODBC-egenskaper](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* eller *Session* — se [Profileringsläge och Work Schema](#profiling-mode-and-work-schema). |
| **Work Schema** | Schema som innehåller arbetstabellerna för profileringsläget *Permanent*. |

En anslutning administreras centralt och tilldelas sedan ett eller flera projekt, så samma
anslutning kan betjäna flera projekt.

---

## ODBC-egenskaper {: #odbc-properties }

Klicka på **Add Property** för varje egenskap och fyll i **Key**, **Value** och, för hemligheter,
kryssrutan **Encrypted**. Varje teknikguide listar en exempeluppsättning för den tekniken,
som du anpassar till din drivrutinsversion och server — se
[noteringen ovan](#technology-guides).

Oavsett drivrutin täcker en egenskapsuppsättning samma fyra saker:

- **`Driver`** — det registrerade drivrutinsnamnet, enligt beskrivningen [ovan](#install-the-driver).
- **Serverns adress** — nyckeln skiljer sig mellan drivrutiner: `SERVER`, `HOST`, `DBCNAME`,
  `Server`, eller, för Oracle, connect descriptorn i `DBQ`.
- **Inloggningsuppgifter** — oftast `UID` och `PWD`; Snowflake använder `UID` plus en `token`, och
  Databricks använder den bokstavliga användaren `token` plus den personliga åtkomsttoken i `PWD`.
- **Databasen eller katalogen som ska användas**, där tekniken har en sådan — se
  [Vilken databas anslutningen ser](#which-database-the-connection-sees).

Allt annat som drivrutinen dokumenterar kan läggas till på samma sätt — connection pooling, socket-timeouts,
Kerberos-inställningar, proxyinställningar. *digna* tolkar inte egenskaperna; den
skickar bara vidare dem.

!!! warning "Värden escapas inte — omge allt med semikolon med klammerparenteser"

    Eftersom egenskaperna fogas samman med `;` skulle ett värde som självt innehåller `;` dela
    anslutningssträngen på fel ställe. Omge sådana värden med klammerparenteser: `PWD={p@ss;word}`.
    Detsamma gäller värden med `=` eller inledande mellanslag. Det är också därför vissa drivrutiner
    av konvention skrivs inom klammerparenteser, som i `{NetezzaSQL}` eller `{SnowflakeDSIIDriver}`.

---

## Kryptera egenskapsvärden {: #encrypting-property-values }

Kryssa i **Encrypted** för varje egenskap som innehåller en hemlighet — `PWD`, `token`, en klienthemlighet.
Värdet krypteras då innan det lagras i *digna*-repositoryt, maskeras på
skärmen och dekrypteras först när anslutningssträngen sätts samman.

!!! tip "Tips"

    Ett krypterat värde kan inte läsas tillbaka, varken i gränssnittet eller via API:et — det kan bara
    ersättas. Förvara hemligheterna även i din egen lösenordshanterare.

Egenskaper som inte är hemliga — drivrutinsnamn, värd, port, databas — lämnas helst
okrypterade, så att de förblir läsbara för den som underhåller anslutningen senare.

---

## Testa en anslutning {: #testing-a-connection }

Klicka på **Test** i dialogrutan *Add DB Connection* **innan** du sparar. Testet använder de värden
som för närvarande finns i formuläret och gör en verklig anslutning, så det rapporterar exakt det som en inspektion
skulle stöta på — ett felaktigt drivrutinsnamn, ett avvisat lösenord, en värd som inte kan nås. Ingenting lagras:
testanslutningen rullas tillbaka oavsett om den lyckas eller misslyckas.

För en befintlig anslutning, håll muspekaren över dess rad på fliken **Database Connections** och
klicka på ikonen **plug** för att testa den igen. Det är det snabbaste sättet att kontrollera om en källa kan
nås efter ett lösenordsbyte eller en brandväggsändring.

---

## Vilken databas anslutningen ser {: #which-database-the-connection-sees }

När du lägger till en datakälla erbjuder *digna* de kataloger, scheman och tabeller som
anslutningen kan nå. Hur långt det räcker beror på tekniken:

| Teknik | Kataloger som erbjuds |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Endast anslutningens **aktuella** databas |
| **Teradata**, **Netezza**, **Databricks** | Alla databaser eller kataloger som användaren har behörighet att se |
| **Hive**, **Impala** | Rapporteras av drivrutinen |

!!! important "En anslutning, en databas"

    För PostgreSQL, SQL Server, Oracle och Snowflake måste egenskaperna peka på den databas
    som innehåller källschemana — `DATABASE=…`, `Database=…`, eller tjänstnamnet i
    Oracles `DBQ`. Tabeller i en annan databas kan inte nås via den anslutningen; lägg till en
    andra anslutning för den.

---

## Profileringsläge och Work Schema {: #profiling-mode-and-work-schema }

Profileringsläget avgör hur *digna* bearbetar data och beräknar mätvärden:

- **Standard:** Mätvärdena beräknas direkt på källtabellerna utan att data kopieras.
- **Permanent:** Data för den inspekterade dagen kopieras till en permanent tabell, och mätvärdena
  beräknas på de kopierade data.
- **Session:** Data kopieras till en sessions- eller temporär tabell, och mätvärdena beräknas på
  dessa temporära data.

Läget avgör vad anslutningens användare måste ha behörighet att göra:

| Läge | Skriver | Behörigheter som anslutningens användare behöver |
|---|---|---|
| **Standard** | ingenting | Läsbehörighet på källtabellerna |
| **Permanent** | en tabell per datakälla i **Work Schema** | Skapa och ta bort tabeller i **Work Schema** |
| **Session** | en temporär tabell som databasen tar bort när sessionen avslutas | Skapa temporära tabeller — **Work Schema** används inte |

*Standard* läser enbart, vilket gör det till läget att välja när *digna* får skrivskyddad
åtkomst. **Work Schema** läses endast för *Permanent*, men det är ändå värt att fylla i så att
anslutningen fortsätter att fungera om läget ändras senare.

---

## Använda en DSN i stället {: #using-a-dsn-instead }

En DSN fungerar fortfarande — `DSN` är bara ytterligare en egenskap:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

DSN:en måste vara registrerad på *digna*-värden, för samma användarkonto som kör *digna*-backenden,
och som **System DSN** när *digna* körs som en tjänst. Allt som är konfigurerat
i DSN:en kan åsidosättas genom att det även läggs till som en egenskap.

DSN-löst är det dokumenterade standardvalet eftersom det undviker detta tillstånd på värden: anslutningen är
helt beskriven i *digna*, och en ny *digna*-värd behöver ha drivrutinen installerad men inget
konfigurerat.

---

## Felsökning {: #troubleshooting }

### Data source name not found / no default driver specified

**Symtom:**
- Knappen **Test** rapporterar ett fel som nämner *data source name not found*, trots att
  konfigurationen är DSN-lös

**Orsaker och lösningar:**
1. Värdet för `Driver` matchar inte något registrerat drivrutinsnamn — jämför med fliken **Drivers**
   i *ODBC Data Source Administrator (64-bit)*, eller med `odbcinst -q -d`
2. Drivrutinen är installerad på din arbetsstation men inte på *digna*-värden
3. Drivrutinen är 32-bitars medan *digna* är 64-bitars — installera 64-bitarsdrivrutinen
4. Egenskapen `Driver` saknas helt, och ingen `DSN` har heller angetts
5. På Linux och macOS är drivrutinen installerad men inte registrerad — ange i stället den fullständiga sökvägen till
   drivrutinsbiblioteket, eller registrera den i `odbcinst.ini`

---

### Anslutningstestet får timeout

**Symtom:**
- **Test** hänger sig och misslyckas sedan efter ungefär en halv minut

**Orsaker och lösningar:**
1. Värd eller port kan inte nås från *digna*-värden — kontrollera brandväggen och, för molnkällor,
   listan över tillåtna IP-adresser
2. Värdnamnet är rätt men porten tillhör en annan tjänst
3. Källan behöver längre tid än standardvärdet 30 sekunder för att acceptera en anslutning — höj
   `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` i avsnittet `[base]` i `config.toml` (`0` väntar
   obegränsat) och starta om backenden
4. En serverlös endpoint vaknar från viloläge — försök igen, och om det händer regelbundet, höj
   inloggningstimeouten enligt ovan

---

### Autentiseringen misslyckas trots att inloggningsuppgifterna är korrekta

**Symtom:**
- Drivrutinen rapporterar ogiltiga inloggningsuppgifter, men samma användare fungerar i en annan SQL-klient

**Orsaker och lösningar:**
1. Lösenordet innehåller `;` — omge värdet med klammerparenteser: `{p@ss;word}`
2. Ett avslutande mellanslag har kopierats med i värdet
3. Drivrutinen förväntar sig en viss autentiseringsmekanism — till exempel `AuthMech` för
   drivrutinerna för Hive och Databricks, eller `authenticator` för Snowflake
4. Värdet lagrades krypterat och redigerades sedan — krypterade värden kan inte läsas tillbaka, så
   ange hemligheten på nytt i sin helhet
5. En token har gått ut — personliga åtkomsttoken och programmatic access tokens utfärdas med
   ett utgångsdatum

---

### Skärmen för datakällor erbjuder inte den förväntade databasen eller det förväntade schemat

**Symtom:**
- Kataloger, scheman eller tabeller saknas när en datakälla läggs till

**Orsaker och lösningar:**
1. Anslutningen pekar på en annan databas — se
   [Vilken databas anslutningen ser](#which-database-the-connection-sees)
2. Anslutningens användare saknar läsbehörighet på schemat eller på datakatalogen
3. **Technology** motsvarar inte källan, så *digna* frågar fel datakatalog
4. För Snowflake är inget standard-warehouse tilldelat användaren och ingen egenskap `Warehouse` har
   angetts, så metadatafrågor kan inte köras

---

### Profileringen misslyckas medan anslutningstestet lyckas

**Symtom:**
- **Test** lyckas, men en inspektion misslyckas när arbetstabeller skapas

**Orsaker och lösningar:**
1. Profileringsläget *Permanent* är valt och anslutningens användare kan inte skapa tabeller i
   **Work Schema** — bevilja behörigheterna, eller byt till *Session* eller *Standard*
2. **Work Schema** är tomt eller anger ett schema som inte finns, samtidigt som profileringsläget *Permanent*
   är valt
3. Profileringsläget *Session* är valt och anslutningens användare får inte skapa temporära tabeller
4. En långvarig profileringsfråga når frågetimeouten — höj
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` i avsnittet `[base]` i `config.toml` (standard 3600
   sekunder, `0` inaktiverar timeouten)

---

## Bästa praxis

**GÖR:**

- Installera och registrera drivrutinen på *digna*-värden innan du konfigurerar anslutningen
- Kryssa i **Encrypted** för varje lösenord och token
- Klicka på **Test** innan du sparar, och testa igen efter ett lösenordsbyte
- Namnge anslutningar efter källa och miljö, till exempel `sales_dwh_prod`
- Ge *digna* en dedikerad databasanvändare, skrivskyddad där profileringsläget *Standard* räcker
- Ha en anslutning per källdatabas, och lägg till en andra hellre än att ändra den första

**GÖR INTE:**

- Lagra hemligheter okrypterade, eller dela en databasanvändare mellan *digna* och andra verktyg
- Använda en 32-bitarsdrivrutin med en 64-bitars *digna*-installation
- Förlita dig på en User DSN när *digna* körs som en tjänst — den kommer inte att vara synlig
- Ange ett värde som innehåller `;` i en egenskap utan klammerparenteser
- Låta **Work Schema** peka på ett schema som innehåller källdata

---

## Support

Behöver du hjälp med en databasanslutning?

- **E-post:** support@digna.ai
- **Dokumentation:** https://docs.digna.ai
- **Webbplats:** https://www.digna.ai

---

**Release:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**