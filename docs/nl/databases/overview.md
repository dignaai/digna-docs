---
title: Overzicht databaseverbindingen – DSN-loze ODBC-configuratie | digna Documentatie
description: Hoe databaseverbindingen in digna werken. Elke brontechnologie wordt via ODBC benaderd met een DSN-loze connection string, opgebouwd uit ODBC-properties. Behandelt de installatie van de driver op de digna-host, het scherm Add DB Connection, versleuteling van properties, het testen van verbindingen, probleemoplossing en links naar de gidsen per technologie.
image: /assets/logo_square.png
keywords:
  - digna databaseverbinding
  - dsn-loze odbc
  - odbc connection string
  - odbc-driver instellen
  - unixodbc
  - odbc-properties
  - configuratie van databronnen
lang: nl
robots: index, follow
og_title: digna databaseverbindingen – DSN-loze ODBC-configuratie
og_description: Configureer een digna-bronverbinding via ODBC zonder DSN. Installatie van de driver, ODBC-properties, versleuteling, testen en probleemoplossing.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Overzicht databaseverbindingen

---

## Inhoudsopgave

1. [Hoe verbindingen werken](#how-connections-work)
2. [Gidsen per technologie](#technology-guides)
3. [Vereiste: installeer de ODBC-driver op de digna-host](#install-the-driver)
4. [Een databaseverbinding aanmaken](#create-a-database-connection)
5. [ODBC-properties](#odbc-properties)
6. [Property-waarden versleutelen](#encrypting-property-values)
7. [Een verbinding testen](#testing-a-connection)
8. [Welke database de verbinding ziet](#which-database-the-connection-sees)
9. [Profiling Mode en Work Schema](#profiling-mode-and-work-schema)
10. [In plaats daarvan een DSN gebruiken](#using-a-dsn-instead)
11. [Problemen oplossen](#troubleshooting)

---

## Hoe verbindingen werken {: #how-connections-work }

*digna* benadert elke brontechnologie via **ODBC**. Een verbinding is een lijst ODBC-properties
die je als key/value-paren invoert. Wanneer *digna* de verbinding opent, voegt het die paren
samen tot een connection string — `Key=Value`, gescheiden door `;`, in de volgorde waarin je ze
hebt opgegeven — en geeft die door aan de ODBC-driver manager op de *digna*-host.

Doordat je de properties zelf invoert, is de configuratie **DSN-loos**: de verbinding bevat
alles wat de driver nodig heeft, dus er hoeft geen ODBC-databron (DSN) op de host te worden
geregistreerd. Dit is de aanbevolen manier om *digna* te configureren, omdat de definitie van de
verbinding volledig in *digna* staat en ermee meeverhuist.

### Waarom ODBC {: #why-odbc }

Eerdere releases boden een keuze tussen een driver per technologie en ODBC, geselecteerd met een
schakelaar **Use ODBC**. Vanaf Release 2026.06 bouwt *digna* uitsluitend op ODBC. Eén
standaardinterface biedt je meer dan een set op maat gemaakte drivers:

- **Authenticatie** — authenticatie maakt deel uit van ODBC, dus een verbinding kan alles
  gebruiken wat de driver ondersteunt: wachtwoorden, tokens en PAT's, Kerberos en Active
  Directory, MFA en single sign-on via de browser, cloudidentiteit, clientcertificaten en TLS.
  Nieuwe methoden komen beschikbaar met een driver-update, in plaats van te wachten op een
  *digna*-release.
- **Drivers die door de databaseleveranciers worden onderhouden** — de eigen driver van de
  leverancier volgt nieuwe serverversies en beveiligingsfixes, en je kunt hem volgens je eigen
  planning bijwerken, onafhankelijk van *digna*.
- **Eén manier om alles te configureren** — elke technologie is een lijst key/value-properties,
  met dezelfde interface, dezelfde versleuteling van gevoelige waarden en dezelfde
  probleemoplossing, in plaats van een andere set velden per bron.
- **Afstemming en bereik** — opties op driverniveau zoals time-outs, TLS-instellingen, proxy's en
  fetch sizes zijn voor elke bron beschikbaar, en elke technologie met een conforme ODBC-driver
  kan worden verbonden, ook technologieën waarvoor *digna* geen eigen gids publiceert.

!!! note "Wat er in de interface is veranderd"

    De schakelaar **Use ODBC** en de aparte velden voor host, poort, database, gebruiker en
    wachtwoord bestaan niet meer. Een verbinding die nog geen ODBC gebruikt, heeft ODBC-properties
    nodig voordat ze weer werkt — zie
    [Een databaseverbinding aanmaken](#create-a-database-connection).

---

## Gidsen per technologie {: #technology-guides }

De namen van de properties verschillen per driver, en elke technologie heeft een of twee details
die de andere niet hebben. De onderstaande gidsen behandelen dat deel; deze pagina behandelt de
*digna*-kant, die voor alle technologieën gelijk is.

!!! important "De property-sets in de gidsen zijn voorbeelden"

    Elke gids toont één combinatie waarvan bekend is dat ze werkt — de combinatie waartegen
    *digna* wordt getest. Het is een startpunt, geen specificatie: de properties horen bij de
    ODBC-driver, en welke er bestaan, hoe ze heten en welke waarden ze accepteren, verschilt per
    driverversie en leverancier, tussen Windows, Linux en macOS, en met de configuratie van de
    bronserver — authenticatiemethode, TLS, gateway, poort. Reken erop dat je een of twee waarden
    moet aanpassen, en beschouw de documentatie van de geïnstalleerde driverversie als leidend.

| Technologie | Gids | Goed om te weten |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Serverless pools hebben `-ondemand` in de hostnaam nodig en ondersteunen alleen *Standard* profiling |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Tokenauthenticatie: `UID=token`, PAT in `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Catalogs komen van de driver, niet uit een query |
| **Netezza** | [Netezza](netezza_connector_guide.md) | De drivernaam staat tussen accolades: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` accepteert een volledige connect descriptor of een alias uit `tnsnames.ora` |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` moet overeenkomen met wat de server eist |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Programmatic access token is het geteste authenticatiepad |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` bepaalt welke schema's *digna* kan zien |
| **Teradata** | [Teradata](teradata_connector_guide.md) | De host gaat in `DBCNAME`; databases fungeren als schema's |

---

## Vereiste: installeer de ODBC-driver op de digna-host {: #install-the-driver }

*digna* opent bronverbindingen vanaf de **server waarop de digna-backend draait**, niet vanuit de
browser. De ODBC-driver moet daarom op die machine zijn geïnstalleerd, en de naam ervan moet bij
de lokale driver manager zijn geregistreerd.

=== "Windows"

    Installeer de 64-bits driver van de leverancier, open daarna **ODBC Data Source
    Administrator (64-bit)** en ga naar het tabblad **Drivers**. De namen die daar staan, zijn
    precies de waarden die je voor de property `Driver` kunt gebruiken.

=== "Linux"

    Installeer **unixODBC** en de driver van de leverancier, en toon daarna de geregistreerde
    drivernamen:

    ```bash
    odbcinst -q -d
    ```

    De namen tussen vierkante haken zijn de waarden die je voor de property `Driver` kunt
    gebruiken. Ze komen uit `/etc/odbcinst.ini` (of het bestand dat `odbcinst -j` meldt).

=== "macOS"

    Installeer **unixODBC** (bijvoorbeeld met `brew install unixodbc`) en de driver van de
    leverancier, en toon daarna de geregistreerde drivernamen:

    ```bash
    odbcinst -q -d
    ```

!!! warning "De drivernaam moet teken voor teken overeenkomen"

    `Driver` wordt ongewijzigd aan de driver manager doorgegeven. `Simba Spark ODBC Driver` en
    `Simba Spark ODBC Driver 64` zijn voor de driver manager verschillende drivers, en een naam
    die niet is geregistreerd geeft de fout *data source name not found*, ook al is er geen DSN
    in het spel.

In plaats van een geregistreerde naam accepteren alle gangbare driver managers ook het volledige
pad naar de driverbibliotheek, bijvoorbeeld
`Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. Dat is handig als de driver wel is
geïnstalleerd maar niet geregistreerd.

---

## Een databaseverbinding aanmaken {: #create-a-database-connection }

Open het **Admin Panel**, ga naar het tabblad **Database Connections** en klik
**Add DB Connection**. Het scherm vraagt om vijf dingen:

| Veld | Beschrijving |
|---|---|
| **Name** | Naam van de verbinding. Deze wordt gebruikt om in andere schermen naar de verbinding te verwijzen. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake of Hive. Dit bepaalt het SQL-dialect dat *digna* genereert, dus het moet overeenkomen met de bron — niet met de driver. Azure Synapse Analytics is een **SQL Server**-verbinding. |
| **ODBC Properties** | De key/value-paren die worden beschreven in [ODBC-properties](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* of *Session* — zie [Profiling Mode en Work Schema](#profiling-mode-and-work-schema). |
| **Work Schema** | Schema dat de werktabellen voor *Permanent* profiling bevat. |

Een verbinding wordt centraal beheerd en daarna aan een of meer projecten toegewezen, zodat
dezelfde verbinding meerdere projecten kan bedienen.

---

## ODBC-properties {: #odbc-properties }

Klik voor elke property op **Add Property** en vul **Key**, **Value** en, voor geheimen, het
selectievakje **Encrypted** in. Elke gids per technologie geeft een voorbeeldset voor die
technologie, die je aanpast aan je driverversie en server — zie
[de opmerking hierboven](#technology-guides).

Welke driver het ook is, een property-set omvat altijd dezelfde vier dingen:

- **`Driver`** — de geregistreerde drivernaam, zoals [hierboven](#install-the-driver) beschreven.
- **Het adres van de server** — de key verschilt per driver: `SERVER`, `HOST`, `DBCNAME`,
  `Server`, of voor Oracle de connect descriptor `DBQ`.
- **Inloggegevens** — meestal `UID` en `PWD`; Snowflake gebruikt `UID` plus een `token`, en
  Databricks gebruikt de letterlijke gebruiker `token` plus het personal access token in `PWD`.
- **De database of catalog waarin gewerkt wordt**, als de technologie die kent — zie
  [Welke database de verbinding ziet](#which-database-the-connection-sees).

Alles wat de driver verder documenteert, kun je op dezelfde manier toevoegen — connection
pooling, socket-time-outs, Kerberos-instellingen, proxy-instellingen. *digna* interpreteert de
properties niet; het geeft ze alleen door.

!!! warning "Waarden worden niet ge-escaped — zet alles met een puntkomma tussen accolades"

    Omdat de properties met `;` worden samengevoegd, zou een waarde die zelf `;` bevat de
    connection string op de verkeerde plek splitsen. Zet zulke waarden tussen accolades:
    `PWD={p@ss;word}`. Hetzelfde geldt voor waarden met `=` of spaties aan het begin. Daarom
    worden sommige drivers ook gewoonlijk tussen accolades geschreven, zoals `{NetezzaSQL}` of
    `{SnowflakeDSIIDriver}`.

---

## Property-waarden versleutelen {: #encrypting-property-values }

Vink **Encrypted** aan voor elke property die een geheim bevat — `PWD`, `token`, een client
secret. De waarde wordt dan versleuteld voordat ze in de *digna*-repository wordt opgeslagen,
wordt op het scherm gemaskeerd en wordt pas ontsleuteld wanneer de connection string wordt
samengesteld.

!!! tip "Tip"

    Een versleutelde waarde kan niet worden teruggelezen, niet in de UI en niet via de API — ze
    kan alleen worden vervangen. Bewaar geheimen daarom ook in je eigen wachtwoordmanager.

Properties die niet geheim zijn — de drivernaam, host, poort, database — laat je het best
onversleuteld, zodat ze leesbaar blijven voor wie de verbinding later beheert.

---

## Een verbinding testen {: #testing-a-connection }

Klik in het dialoogvenster *Add DB Connection* op **Test** **voordat** je opslaat. De test
gebruikt de waarden die op dat moment in het formulier staan en maakt echt verbinding, dus hij
meldt precies waar een inspectie op zou stuiten — een verkeerde drivernaam, een geweigerd
wachtwoord, een onbereikbare host. Er wordt niets opgeslagen: de testverbinding wordt
teruggedraaid, of ze nu slaagt of mislukt.

Voor een bestaande verbinding beweeg je de muis over de rij in het tabblad
**Database Connections** en klik je op het **stekker**-pictogram om opnieuw te testen. Dat is de
snelste manier om na een wachtwoordwijziging of een firewallwijziging te controleren of een bron
bereikbaar is.

---

## Welke database de verbinding ziet {: #which-database-the-connection-sees }

Wanneer je een databron toevoegt, biedt *digna* de catalogs, schema's en tabellen aan die de
verbinding kan bereiken. Hoe ver dat reikt, hangt af van de technologie:

| Technologie | Aangeboden catalogs |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Alleen de **huidige** database van de verbinding |
| **Teradata**, **Netezza**, **Databricks** | Alle databases of catalogs die de gebruiker mag zien |
| **Hive**, **Impala** | Door de driver gemeld |

!!! important "Eén verbinding, één database"

    Voor PostgreSQL, SQL Server, Oracle en Snowflake moeten de properties verwijzen naar de
    database die de bronschema's bevat — `DATABASE=…`, `Database=…` of de servicenaam binnen de
    `DBQ` van Oracle. Tabellen in een andere database zijn via die verbinding niet bereikbaar;
    voeg daarvoor een tweede verbinding toe.

---

## Profiling Mode en Work Schema {: #profiling-mode-and-work-schema }

De profiling mode bepaalt hoe *digna* data verwerkt en metrics berekent:

- **Standard:** metrics worden direct op de brontabellen berekend, zonder de data te kopiëren.
- **Permanent:** de data van de geïnspecteerde dag wordt naar een permanente tabel gekopieerd, en
  metrics worden op de gekopieerde data berekend.
- **Session:** de data wordt naar een sessie- of tijdelijke tabel gekopieerd, en metrics worden
  op deze tijdelijke data berekend.

De mode bepaalt wat de verbindingsgebruiker mag doen:

| Mode | Schrijft | Rechten die de verbindingsgebruiker nodig heeft |
|---|---|---|
| **Standard** | niets | Leesrechten op de brontabellen |
| **Permanent** | een tabel per databron in **Work Schema** | Tabellen aanmaken en verwijderen in **Work Schema** |
| **Session** | een tijdelijke tabel die de database met de sessie verwijdert | Tijdelijke tabellen aanmaken — **Work Schema** wordt niet gebruikt |

*Standard* leest alleen, waardoor het de aangewezen mode is wanneer *digna* alleen-lezen toegang
krijgt. **Work Schema** wordt alleen bij *Permanent* gelezen, maar het loont om het toch in te
vullen, zodat de verbinding blijft werken als de mode later wordt gewijzigd.

---

## In plaats daarvan een DSN gebruiken {: #using-a-dsn-instead }

Een DSN werkt nog steeds — `DSN` is gewoon nog een property:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

De DSN moet op de *digna*-host zijn geregistreerd, voor hetzelfde gebruikersaccount dat de
*digna*-backend draait, en als **System DSN** wanneer *digna* als service draait. Alles wat in de
DSN is geconfigureerd, kun je overschrijven door het ook als property toe te voegen.

DSN-loos is de gedocumenteerde standaard omdat het die toestand op de host vermijdt: de
verbinding is volledig in *digna* beschreven, en op een nieuwe *digna*-host hoeft alleen de
driver te worden geïnstalleerd, zonder verdere configuratie.

---

## Problemen oplossen {: #troubleshooting }

### Data source name not found / no default driver specified

**Symptomen:**
- De knop **Test** meldt een fout met *data source name not found*, ook al is de configuratie
  DSN-loos

**Oorzaken en oplossingen:**
1. De waarde van `Driver` komt niet overeen met een geregistreerde drivernaam — vergelijk die met
   het tabblad **Drivers** van *ODBC Data Source Administrator (64-bit)*, of met `odbcinst -q -d`
2. De driver is op je werkstation geïnstalleerd, maar niet op de *digna*-host
3. De driver is 32-bits terwijl *digna* 64-bits is — installeer de 64-bits driver
4. De property `Driver` ontbreekt helemaal, en er is ook geen `DSN` opgegeven
5. Op Linux en macOS is de driver geïnstalleerd maar niet geregistreerd — geef in plaats daarvan
   het volledige pad naar de driverbibliotheek op, of registreer hem in `odbcinst.ini`

---

### De verbindingstest loopt af op een time-out

**Symptomen:**
- **Test** blijft hangen en mislukt na ongeveer een halve minuut

**Oorzaken en oplossingen:**
1. Host of poort is niet bereikbaar vanaf de *digna*-host — controleer de firewall en, voor
   cloudbronnen, de IP-allowlist
2. De hostnaam klopt, maar de poort hoort bij een andere service
3. De bron heeft meer dan de standaard 30 seconden nodig om een verbinding te accepteren — verhoog
   `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` in de sectie `[base]` van `config.toml` (`0` wacht
   onbeperkt) en herstart de backend
4. Een serverless endpoint ontwaakt uit inactiviteit — probeer het opnieuw, en verhoog de
   login-time-out zoals hierboven als dit regelmatig gebeurt

---

### Authenticatie mislukt hoewel de inloggegevens kloppen

**Symptomen:**
- De driver meldt ongeldige inloggegevens, maar dezelfde gebruiker werkt in een andere SQL-client

**Oorzaken en oplossingen:**
1. Het wachtwoord bevat `;` — zet de waarde tussen accolades: `{p@ss;word}`
2. Er is een spatie aan het eind mee gekopieerd in de waarde
3. De driver verwacht een specifiek authenticatiemechanisme — bijvoorbeeld `AuthMech` voor de
   Hive- en Databricks-drivers, of `authenticator` voor Snowflake
4. De waarde is versleuteld opgeslagen en daarna bewerkt — versleutelde waarden kunnen niet
   worden teruggelezen, dus voer het geheim opnieuw volledig in
5. Een token is verlopen — personal access tokens en programmatic access tokens worden met een
   vervaldatum uitgegeven

---

### Het databronscherm biedt de verwachte database of het verwachte schema niet aan

**Symptomen:**
- Catalogs, schema's of tabellen ontbreken bij het toevoegen van een databron

**Oorzaken en oplossingen:**
1. De verbinding verwijst naar een andere database — zie
   [Welke database de verbinding ziet](#which-database-the-connection-sees)
2. De verbindingsgebruiker heeft geen leesrechten op het schema of op de data dictionary
3. **Technology** komt niet overeen met de bron, waardoor *digna* de verkeerde data dictionary
   bevraagt
4. Voor Snowflake is aan de gebruiker geen standaard-warehouse toegewezen en is geen property
   `Warehouse` opgegeven, waardoor metadataqueries niet kunnen draaien

---

### Profiling mislukt terwijl de verbindingstest slaagt

**Symptomen:**
- **Test** slaagt, maar een inspectie mislukt bij het aanmaken van werktabellen

**Oorzaken en oplossingen:**
1. *Permanent* profiling is geselecteerd en de verbindingsgebruiker kan geen tabellen aanmaken in
   **Work Schema** — ken de rechten toe, of schakel over naar *Session* of *Standard*
2. **Work Schema** is leeg of noemt een schema dat niet bestaat, terwijl *Permanent* profiling
   is geselecteerd
3. *Session* profiling is geselecteerd en de verbindingsgebruiker mag geen tijdelijke tabellen
   aanmaken
4. Een langlopende profiling-query loopt tegen de query-time-out aan — verhoog
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` in de sectie `[base]` van `config.toml` (standaard 3600
   seconden, `0` schakelt de time-out uit)

---

## Best practices

**WEL:**

- Installeer en registreer de driver op de *digna*-host voordat je de verbinding configureert
- Vink **Encrypted** aan voor elk wachtwoord en elk token
- Klik **Test** voordat je opslaat, en test opnieuw na een wachtwoordwijziging
- Geef verbindingen een naam naar bron en omgeving, bijvoorbeeld `sales_dwh_prod`
- Geef *digna* een eigen databasegebruiker, met alleen leesrechten als *Standard* profiling
  volstaat
- Houd één verbinding per brondatabase aan, en voeg een tweede toe in plaats van de eerste om te
  zetten

**NIET:**

- Geheimen onversleuteld opslaan, of één databasegebruiker delen tussen *digna* en andere tools
- Een 32-bits driver gebruiken met een 64-bits *digna*-installatie
- Vertrouwen op een User DSN wanneer *digna* als service draait — die is dan niet zichtbaar
- Een waarde met `;` zonder accolades in een property zetten
- **Work Schema** laten verwijzen naar een schema dat brondata bevat

---

## Ondersteuning

Hulp nodig bij een databaseverbinding?

- **E-mail:** support@digna.ai
- **Documentatie:** https://docs.digna.ai
- **Website:** https://www.digna.ai

---

**Release:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
