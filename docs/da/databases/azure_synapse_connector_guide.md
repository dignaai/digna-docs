---
title: Azure Synapse-connector – Databaseintegration | digna-dokumentation
description: Konfigurer digna til at oprette forbindelse til Azure Synapse Analytics over ODBC med en DSN-løs forbindelsesstreng. Understøtter serverless og dedikerede SQL-pools med de nødvendige ODBC-egenskaber og forbindelsesindstillinger på digna-siden.
image: /assets/logo_square.png
---


# Kildeconnector til Azure Synapse Analytics

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til
Azure Synapse Analytics over **ODBC** med en **DSN-løs** forbindelsesstreng. Både serverless og
dedikerede SQL-pools understøttes.

*digna*-delen af opsætningen er den samme for alle teknologier — hvor forbindelser oprettes,
hvordan egenskabsværdier krypteres, hvordan en forbindelse testes, og hvad profileringstilstandene
betyder. Den er beskrevet i [Oversigt over databaseforbindelser](overview.md). Denne side dækker
det, der er specifikt for Azure Synapse.

!!! note "Teknologi"

    Synapse taler SQL Server-dialekten, så forbindelsen oprettes med **Technology:
    SQL Server**. Se [MS SQL Server](sqlserver_connector_guide.md) for en on-premises-server.

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Installer **ODBC Driver 18 for SQL Server** på den maskine, der kører *digna*-backend, efter
[Microsofts installationsvejledning](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server),
og aflæs det nøjagtige registrerede drivernavn på din vært som beskrevet i
[Installer ODBC-driveren på digna-værten](overview.md#install-the-driver).

---

## 2. ODBC-egenskaber {: #2-odbc-properties }

!!! important "Et eksempel, ikke en specifikation"

    Sættet nedenfor er én kombination, der vides at virke. Egenskaberne tilhører Microsofts
    ODBC-driver, så deres navne, standardværdier og accepterede værdier varierer mellem
    driverversioner og platforme, og hvad workspacet kræver, afhænger af, hvordan det er
    konfigureret — pooltype, autentificeringsmetode, firewall. Brug dette som udgangspunkt, og
    tjek dokumentationen for den driverversion, du har installeret.

Tilføj følgende egenskaber på skærmen **Add DB Connection**:

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Skal matche det drivernavn, der er registreret på *digna*-værten |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Workspacets navn plus endpoint-suffikset — se nedenfor |
| `DATABASE` | `dignadata` | Databasen, der indeholder kildeskemaerne. Det er den eneste database, denne forbindelse kan profilere |
| `UID` | `sqladminuser` | SQL-login |
| `PWD` | `<password>` | Sæt flueben i **Encrypted** |

Den resulterende forbindelsesstreng ser sådan ud:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### `SERVER`-værdien

Tag navnet på Synapse-workspacet, og tilføj endpoint-suffikset:

| Pool | `SERVER` |
|---|---|
| **Serverless SQL pool** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Dedicated SQL pool** | `<workspace>.sql.azuresynapse.net` |

!!! warning "Delen `-ondemand` er let at overse"

    Uden den peger navnet på det dedikerede endpoint, og forbindelsen fejler enten, eller den
    når ubemærket en anden pool end tilsigtet. Begge endpoints vises på workspacets
    oversigtsside i Azure-portalen.

### Firewall

Synapse-workspacets firewall skal tillade *digna*-værtens udgående adresse. Tilføj den under
**Networking** i workspacet, før du tester forbindelsen — en blokeret adresse viser sig som en
forbindelsestimeout og ikke som en autentificeringsfejl.

### Microsoft Entra ID-autentificering

I stedet for et SQL-login kan driveren autentificere mod Entra ID. Erstat `UID`/`PWD` med den
autentificeringsmetode, dit workspace forventer, for eksempel:

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | `UID` tager så applikations-ID'et (client ID) og `PWD` client secret |
| `Authentication` | `ActiveDirectoryMSI` | Managed identity for *digna*-værten, ingen legitimationsoplysninger nødvendige |

---

## 3. *digna*-konfiguration {: #3-digna-configuration }

Angiv følgende på skærmen **Add DB Connection**:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Bemærkninger om Azure Synapse {: #4-notes-on-azure-synapse }

- **Serverless pools understøtter kun *Standard*-profilering.** En serverless SQL pool kan ikke
  oprette tabeller i en database, så hverken *Permanent*- eller *Session*-profilering kan køre.
  *Standard* beregner metrikkerne direkte på kilden, hvilket også er den billigste løsning, da
  serverless faktureres efter mængden af behandlede data.
- **Én forbindelse ser én database.** *digna* tilbyder skemaerne i den database, der er angivet i
  `DATABASE`, fordi Synapse ligesom SQL Server kun rapporterer den aktuelle database som katalog.
- **Kryptering er slået til som standard** i Driver 18, og Synapse-endpoints præsenterer gyldige
  offentlige certifikater, så der er ikke brug for egenskaberne `Encrypt` eller
  `TrustServerCertificate`.
- **Et serverless-endpoint kan vågne fra inaktivitet** ved den første forbindelse. Hvis
  forbindelsestesten får timeout på en pool, der ikke har været brugt i et stykke tid, så prøv
  igen.

---

## 5. Verificering af driveren (valgfrit) {: #5-verifying-the-driver-optional }

Det er ikke nødvendigt at konfigurere en ODBC-datakilde for en DSN-løs forbindelse, men
driverens egen guide er en bekvem måde at bekræfte, at driveren virker, og at workspacet
accepterer dine legitimationsoplysninger, før du indtaster dem i *digna*.

#### Trin 1
![Trin 1](images/azure_synapse/create_odbc_data_source_step1.png)

Udfyld feltet "Server".
Brug navnet på Synapse-workspacet, og udvid det med ".sql.azuresynapse.net".  
**Bemærk**: Hvis du vil oprette forbindelse via en serverless SQL pool, skal du sørge for at
medtage "-ondemand" som vist på skærmbilledet ovenfor.

Klik på knappen **Next >**.

#### Trin 2
![Trin 2](images/azure_synapse/create_odbc_data_source_step2.png)

Vælg autentificeringsmetoden (f.eks. brugernavn og adgangskode),
og angiv de nødvendige oplysninger.

Klik på knappen **Next >**.

#### Trin 3
![Trin 3](images/azure_synapse/create_odbc_data_source_step3.png)

Vælg de ANSI-kompatible indstillinger, og klik derefter på knappen **Next >**.

#### Trin 4
![Trin 4](images/azure_synapse/create_odbc_data_source_step4.png)

Du kan beholde standardindstillingerne eller vælge indstillinger efter behov
og klikke på knappen **Finish**.

#### Trin 5
![Trin 5](images/azure_synapse/create_odbc_data_source_step5.png)

Klik nu på knappen **Test datasource**.

#### Trin 6
![Trin 6](images/azure_synapse/create_odbc_data_source_step6.png)

En bekræftelsesskærm viser, at driveren, endpointet og legitimationsoplysningerne virker. De
værdier, du indtastede, er præcis de værdier, egenskaberne i [afsnit 2](#2-odbc-properties) skal
have.
