---
title: Azure Synapse-connector – databaseintegrasjon | digna-dokumentasjon
description: Konfigurer digna til å koble til Azure Synapse Analytics over ODBC med en DSN-løs tilkoblingsstreng. Støtter serverless og dedikerte SQL-pooler, med de nødvendige ODBC-egenskapene og tilkoblingsinnstillingene på digna-siden.
image: /assets/logo_square.png
---


# Kildeconnector for Azure Synapse Analytics

Denne veiledningen beskriver hvordan du konfigurerer *digna* til å koble til Azure Synapse Analytics over
**ODBC**, med en **DSN-løs** tilkoblingsstreng. Både serverless og dedikerte SQL-pooler
støttes.

*digna*-siden av oppsettet er den samme for alle teknologier — hvor tilkoblinger opprettes,
hvordan egenskapsverdier krypteres, hvordan en tilkobling testes og hva profileringsmodusene
betyr. Den er beskrevet i [Oversikt over databasetilkoblinger](overview.md). Denne siden dekker det
som er spesifikt for Azure Synapse.

!!! note "Teknologi"

    Synapse bruker SQL Server-dialekten, så tilkoblingen opprettes med **Technology:
    SQL Server**. Se [MS SQL Server](sqlserver_connector_guide.md) for en lokal server (on-premises).

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Installer **ODBC Driver 18 for SQL Server** på maskinen som kjører *digna*-backend,
i henhold til [Microsofts installasjonsveiledning](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server),
og les av det nøyaktige registrerte drivernavnet på verten din som beskrevet i
[Installer ODBC-driveren på digna-verten](overview.md#install-the-driver).

---

## 2. ODBC-egenskaper {: #2-odbc-properties }

!!! important "Et eksempel, ikke en spesifikasjon"

    Settet nedenfor er én kombinasjon som er kjent for å fungere. Egenskapene tilhører
    Microsofts ODBC-driver, så navnene, standardverdiene og de godtatte verdiene varierer mellom
    driverversjoner og plattformer, og hva arbeidsområdet krever, avhenger av hvordan det er konfigurert —
    pooltype, autentiseringsmetode, brannmur. Bruk dette som et utgangspunkt og sjekk
    dokumentasjonen for driverversjonen du har installert.

Legg til følgende egenskaper i skjermbildet **Add DB Connection**:

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Må samsvare med drivernavnet som er registrert på *digna*-verten |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Navnet på arbeidsområdet pluss endepunktsuffikset — se nedenfor |
| `DATABASE` | `dignadata` | Databasen som inneholder kildeskjemaene. Det er den eneste databasen denne tilkoblingen kan profilere |
| `UID` | `sqladminuser` | SQL-pålogging |
| `PWD` | `<password>` | Kryss av for **Encrypted** |

Den resulterende tilkoblingsstrengen ser slik ut:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### Verdien for `SERVER`

Ta navnet på Synapse-arbeidsområdet og legg til endepunktsuffikset:

| Pool | `SERVER` |
|---|---|
| **Serverless SQL pool** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Dedicated SQL pool** | `<workspace>.sql.azuresynapse.net` |

!!! warning "Delen `-ondemand` er lett å overse"

    Uten den peker navnet på det dedikerte endepunktet, og tilkoblingen feiler enten eller
    når i stillhet en annen pool enn tiltenkt. Begge endepunktene vises på oversiktssiden
    for arbeidsområdet i Azure-portalen.

### Brannmur

Brannmuren for Synapse-arbeidsområdet må tillate den utgående adressen til *digna*-verten. Legg den til
under **Networking** i arbeidsområdet før du tester tilkoblingen — en blokkert adresse viser seg
som et tidsavbrudd for tilkoblingen, ikke som en autentiseringsfeil.

### Microsoft Entra ID-autentisering

I stedet for en SQL-pålogging kan driveren autentisere mot Entra ID. Erstatt `UID`/`PWD` med
autentiseringsmetoden arbeidsområdet ditt forventer, for eksempel:

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | `UID` tar da applikasjons-ID-en (klient-ID) og `PWD` client secret |
| `Authentication` | `ActiveDirectoryMSI` | Administrert identitet (managed identity) for *digna*-verten, ingen legitimasjon nødvendig |

---

## 3. *digna*-konfigurasjon {: #3-digna-configuration }

I skjermbildet **Add DB Connection** oppgir du følgende:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Merknader om Azure Synapse {: #4-notes-on-azure-synapse }

- **Serverless pooler støtter bare *Standard*-profilering.** En serverless SQL pool kan ikke opprette
  tabeller i en database, så verken *Permanent*- eller *Session*-profilering kan kjøres. *Standard*
  beregner metrikkene direkte på kilden, noe som også er det billigste alternativet, siden
  serverless faktureres per mengde behandlede data.
- **Én tilkobling ser én database.** *digna* tilbyr skjemaene i databasen som er angitt i
  `DATABASE`, fordi Synapse, i likhet med SQL Server, bare rapporterer den gjeldende databasen som en katalog.
- **Kryptering er slått på som standard** i Driver 18, og Synapse-endepunkter presenterer gyldige offentlige
  sertifikater, så ingen `Encrypt`- eller `TrustServerCertificate`-egenskap er nødvendig.
- **Et serverless-endepunkt kan våkne fra inaktiv tilstand** ved første tilkobling. Hvis tilkoblingstesten
  får tidsavbrudd mot en pool som ikke har vært brukt på en stund, prøv igjen.

---

## 5. Verifisere driveren (valgfritt) {: #5-verifying-the-driver-optional }

Det er ikke nødvendig å konfigurere en ODBC-datakilde for en DSN-løs tilkobling, men driverens
egen veiviser er en praktisk måte å bekrefte at driveren fungerer og at arbeidsområdet godtar
legitimasjonen din, før du legger den inn i *digna*.

#### Trinn 1
![Trinn 1](images/azure_synapse/create_odbc_data_source_step1.png)

Fyll ut feltet "Server".
Bruk navnet på Synapse-arbeidsområdet og legg til ".sql.azuresynapse.net".  
**Obs:** Hvis du vil koble til via en serverless SQL pool, må du passe på å ta med
"-ondemand" som vist i skjermbildet ovenfor.

Klikk på knappen **Next >**.

#### Trinn 2
![Trinn 2](images/azure_synapse/create_odbc_data_source_step2.png)

Velg autentiseringsmetode (f.eks. brukernavn og passord)
og oppgi de nødvendige opplysningene.

Klikk på knappen **Next >**.

#### Trinn 3
![Trinn 3](images/azure_synapse/create_odbc_data_source_step3.png)

Velg de ANSI-kompatible innstillingene, og klikk deretter på knappen **Next >**.

#### Trinn 4
![Trinn 4](images/azure_synapse/create_odbc_data_source_step4.png)

Du kan beholde standardinnstillingene eller velge alternativer etter behov,
og klikke på knappen **Finish**.

#### Trinn 5
![Trinn 5](images/azure_synapse/create_odbc_data_source_step5.png)

Klikk nå på knappen **Test datasource**.

#### Trinn 6
![Trinn 6](images/azure_synapse/create_odbc_data_source_step6.png)

Et bekreftelsesskjermbilde viser at driveren, endepunktet og legitimasjonen fungerer. Verdiene
du la inn, er nøyaktig de verdiene egenskapene i [avsnitt 2](#2-odbc-properties) skal ha.
