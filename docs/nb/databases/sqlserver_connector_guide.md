---
title: MS SQL Server-connector – databaseintegrasjon | digna-dokumentasjon
description: Konfigurer digna til å koble til Microsoft SQL Server over ODBC med en DSN-løs tilkoblingsstreng. Dekker Microsofts ODBC-driver, de nødvendige ODBC-egenskapene, krypteringsinnstillinger og tilkoblingsinnstillingene på digna-siden.
image: /assets/logo_square.png
---


# Kildeconnector for MS SQL Server

Denne veiledningen beskriver hvordan du konfigurerer *digna* til å koble til Microsoft SQL Server over **ODBC**,
med en **DSN-løs** tilkoblingsstreng.

*digna*-siden av oppsettet er den samme for alle teknologier — hvor tilkoblinger opprettes,
hvordan egenskapsverdier krypteres, hvordan en tilkobling testes og hva profileringsmodusene
betyr. Den er beskrevet i [Oversikt over databasetilkoblinger](overview.md). Denne siden dekker det
som er spesifikt for SQL Server.

!!! note "Azure Synapse Analytics"

    Synapse konfigureres også som en SQL Server-tilkobling, med et annet vertsnavn og noen
    ekstra hensyn — se [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Installer **ODBC Driver 18 for SQL Server** på maskinen som kjører *digna*-backend,
i henhold til [Microsofts installasjonsveiledning](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

Driveren som følger med Windows under det enkle navnet **SQL Server**, fungerer også, men den er
for lengst erstattet og støtter verken moderne TLS-innstillinger eller Azure-autentisering. Bruk den bare
der det ikke er mulig å installere den gjeldende driveren.

Les av det nøyaktige registrerte drivernavnet på verten din som beskrevet i
[Installer ODBC-driveren på digna-verten](overview.md#install-the-driver).

---

## 2. ODBC-egenskaper {: #2-odbc-properties }

!!! important "Et eksempel, ikke en spesifikasjon"

    Settet nedenfor er én kombinasjon som er kjent for å fungere. Egenskapene tilhører
    Microsofts ODBC-driver, så navnene, standardverdiene og de godtatte verdiene varierer mellom
    driverversjoner — Driver 18 krypterer for eksempel som standard, noe Driver 17 ikke gjorde — og mellom
    plattformer. Bruk dette som et utgangspunkt og sjekk dokumentasjonen for driverversjonen
    du har installert.

Legg til følgende egenskaper i skjermbildet **Add DB Connection**:

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Må samsvare med drivernavnet som er registrert på *digna*-verten |
| `SERVER` | `sql.example.com` | Servernavn eller IP-adresse. Navngitte instanser: `host\instance`; en port som ikke er standard: `host,1433` |
| `PORT` | `1433` | Utelates når porten allerede er en del av `SERVER` |
| `DATABASE` | `digna_source_db` | Databasen som inneholder kildeskjemaene. Det er den eneste databasen denne tilkoblingen kan profilere |
| `UID` | `digna_source_user` | Databasebruker |
| `PWD` | `<password>` | Kryss av for **Encrypted** |

Den resulterende tilkoblingsstrengen ser slik ut:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Kryptering med ODBC Driver 18

Driver 18 krypterer tilkoblinger som standard og validerer serversertifikatet. Mot en
server med et sertifikat som *digna*-verten ikke stoler på — typisk et selvsignert sertifikat —
feiler tilkoblingen med en feil i sertifikatkjeden. Legg til:

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `Encrypt` | `yes` | Standard i Driver 18; sett til `no` bare hvis serveren ikke støtter TLS |
| `TrustServerCertificate` | `yes` | Hopper over sertifikatvalidering. Praktisk i testmiljøer; i produksjon bør du heller installere sertifikatet |

### Windows-autentisering

For å koble til som kontoen som kjører *digna*-tjenesten i stedet for med en SQL-pålogging, fjerner du
`UID` og `PWD` og legger til:

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `Trusted_Connection` | `yes` | Tjenestekontoen for *digna* trenger databaserettighetene |

---

## 3. *digna*-konfigurasjon {: #3-digna-configuration }

I skjermbildet **Add DB Connection** oppgir du følgende:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Merknader om MS SQL Server {: #4-notes-on-ms-sql-server }

- **Én tilkobling ser én database.** *digna* tilbyr skjemaene i databasen som er angitt i
  `DATABASE`, fordi SQL Server bare rapporterer den gjeldende databasen som en katalog. Kildetabeller
  i en annen database trenger sin egen tilkobling.
- **Profileringsmoduser.** *Permanent* oppretter arbeidstabellene i **Work Schema**, så brukeren
  trenger `CREATE TABLE` der. *Session* bruker lokale midlertidige tabeller (`#wt_…`) i `tempdb` og
  rører ikke **Work Schema**. *Standard* trenger bare lesetilgang.
- **`SERVER` inneholder instans og port.** Med en navngitt instans krever `host\instance` at
  tjenesten SQL Server Browser kan nås; `host,port` unngår det.

---

## 5. Verifisere driveren (valgfritt) {: #5-verifying-the-driver-optional }

Det er ikke nødvendig å konfigurere en ODBC-datakilde for en DSN-løs tilkobling, men driverens
egen veiviser er en praktisk måte å bekrefte at driveren fungerer og at serveren godtar
legitimasjonen din, før du legger den inn i *digna*.

#### Trinn 1
![Trinn 1](images/sqlserver/create_odbc_data_source_step1.png)

Klikk på knappen **Next >**.

#### Trinn 2
![Trinn 2](images/sqlserver/create_odbc_data_source_step2.png)

Velg autentiseringsmetode (f.eks. brukernavn og passord)
og oppgi de nødvendige opplysningene.

Klikk på knappen **Next >**.

#### Trinn 3
![Trinn 3](images/sqlserver/create_odbc_data_source_step3.png)

Velg de ANSI-kompatible innstillingene, og klikk deretter på knappen **Next >**.

#### Trinn 4
![Trinn 4](images/sqlserver/create_odbc_data_source_step4.png)

Du kan beholde standardinnstillingene eller velge loggingsalternativer etter behov,
og klikke på knappen **Finish**.

#### Trinn 5
![Trinn 5](images/sqlserver/create_odbc_data_source_step5.png)

Klikk nå på knappen **Test datasource**.

#### Trinn 6
![Trinn 6](images/sqlserver/create_odbc_data_source_step6.png)

Et bekreftelsesskjermbilde viser at driveren og legitimasjonen fungerer. Verdiene du la inn, er
nøyaktig de verdiene egenskapene i [avsnitt 2](#2-odbc-properties) skal ha.
