# Kildeconnector for Snowflake

Denne veiledningen beskriver hvordan du konfigurerer *digna* til å koble til Snowflake over **ODBC**, med en
**DSN-løs** tilkoblingsstreng.

*digna*-siden av oppsettet er den samme for alle teknologier — hvor tilkoblinger opprettes,
hvordan egenskapsverdier krypteres, hvordan en tilkobling testes og hva profileringsmodusene
betyr. Den er beskrevet i [Oversikt over databasetilkoblinger](overview.md). Denne siden dekker det
som er spesifikt for Snowflake.

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Installer **Snowflake ODBC Driver** på maskinen som kjører *digna*-backend, i henhold til
[Snowflakes installasjonsveiledning](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

Driveren registrerer seg som **SnowflakeDSIIDriver**. Les av det nøyaktige registrerte navnet på
verten din som beskrevet i [Installer ODBC-driveren på digna-verten](overview.md#install-the-driver).

---

## 2. ODBC-egenskaper {: #2-odbc-properties }

Snowflake nås med et **programmatic access token (PAT)** — autentiseringsmetoden
*digna* er verifisert mot, og den Snowflake krever for kontoer der
innlogging med bare passord er blokkert.

!!! important "Et eksempel, ikke en spesifikasjon"

    Settet nedenfor er én kombinasjon som er kjent for å fungere. Egenskapene tilhører
    Snowflake ODBC-driveren, så navnene, standardverdiene og de godtatte verdiene varierer mellom
    driverversjoner og plattformer, og hvilke autentiseringsalternativer kontoen din tillater, bestemmes av
    kontoens sikkerhetspolicy. Bruk dette som et utgangspunkt og sjekk dokumentasjonen for
    driverversjonen du har installert.

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Må samsvare med drivernavnet som er registrert på *digna*-verten |
| `Server` | `<account>.snowflakecomputing.com` | Kontoidentifikator pluss suffikset, f.eks. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Snowflake-brukeren tokenet tilhører |
| `Database` | `TEST` | Databasen som inneholder kildeskjemaene. Det er den eneste databasen denne tilkoblingen kan profilere |
| `Schema` | `PUBLIC` | Standardskjemaet for sesjonen |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Velger token-autentisering |
| `token` | `<programmatic access token>` | Kryss av for **Encrypted** |

Den resulterende tilkoblingsstrengen ser slik ut:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Warehouse og rolle

Spørringer trenger et warehouse. Hvis *digna*-brukeren har et standard warehouse og en standardrolle,
bruker sesjonen disse, og ingenting må konfigureres. Ellers legger du til:

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Warehouse som kjører profileringsspørringene |
| `Role` | `DIGNA_READER` | Rollen hvis rettigheter sesjonen bruker |

!!! tip "Gi digna sitt eget warehouse"

    Et eget, lite warehouse med automatisk suspendering holder profileringskostnadene synlige og hindrer
    at *digna* konkurrerer med interaktive brukere om beregningskapasitet.

### Passordautentisering

Der kontoen fortsatt tillater det, fungerer et passord i stedet for tokenet — fjern `authenticator`
og `token` og legg til:

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `PWD` | `<password>` | Kryss av for **Encrypted** |

---

## 3. *digna*-konfigurasjon {: #3-digna-configuration }

I skjermbildet **Add DB Connection** oppgir du følgende:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Merknader om Snowflake {: #4-notes-on-snowflake }

- **Tokens utløper.** Et programmatic access token utstedes med en levetid, og profileringen stopper
  den dagen det utløper. Noter utløpsdatoen når du oppretter det, og legg inn det nye tokenet i
  egenskapen `token` — krypterte verdier kan erstattes, men ikke leses tilbake.
- **Én tilkobling ser én database.** *digna* tilbyr skjemaene i databasen som er angitt i
  `Database`, fordi Snowflake bare rapporterer den gjeldende databasen som en katalog. Kildetabeller i
  en annen database trenger sin egen tilkobling.
- **Identifikatorer skrives med store bokstaver** med mindre de ble opprettet i anførselstegn. *digna* bruker navnene slik
  Snowflake rapporterer dem.
- **Profileringsmoduser.** *Permanent* oppretter arbeidstabellene i **Work Schema**, så rollen trenger
  `CREATE TABLE` der. *Session* bruker `CREATE TEMPORARY TABLE` og rører ikke
  **Work Schema**. *Standard* trenger bare lesetilgang — og ingen skriverettigheter i det hele tatt.

---

## 5. Verifisere driveren (valgfritt) {: #5-verifying-the-driver-optional }

Det er ikke nødvendig å konfigurere en ODBC-datakilde for en DSN-løs tilkobling, men driverens
egen dialogboks er en praktisk måte å bekrefte at driveren, konto-URL-en og
legitimasjonen din fungerer, før du legger dem inn i *digna*.

#### Trinn 1
![Trinn 1](images/snowflake/create_odbc_data_source_step1.png)

Merknader:

- Verdien for **Server** består av Snowflake-kontoidentifikatoren din etterfulgt av
  `.snowflakecomputing.com`.
- **Database**, **Schema** og **Warehouse** som legges inn her, tilsvarer egenskapene `Database`,
  `Schema` og `Warehouse` i [avsnitt 2](#2-odbc-properties).

#### Trinn 2 – Test tilkoblingen

Klikk på knappen **TEST**. En vellykket tilkobling skal se slik ut:

![Trinn 2](images/snowflake/create_odbc_data_source_step2.png)