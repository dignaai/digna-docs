---
title: PostgreSQL-connector – Databaseintegration | digna-dokumentation
description: Konfigurer digna til at oprette forbindelse til PostgreSQL over ODBC med en DSN-løs forbindelsesstreng. Dækker psqlODBC-driveren, de nødvendige ODBC-egenskaber, SSL-tilstande og forbindelsesindstillingerne på digna-siden.
image: /assets/logo_square.png
---


# Kildeconnector til PostgreSQL

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til
PostgreSQL over **ODBC** med en **DSN-løs** forbindelsesstreng.

*digna*-delen af opsætningen er den samme for alle teknologier — hvor forbindelser oprettes,
hvordan egenskabsværdier krypteres, hvordan en forbindelse testes, og hvad profileringstilstandene
betyder. Den er beskrevet i [Oversigt over databaseforbindelser](overview.md). Denne side dækker
det, der er specifikt for PostgreSQL.

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Installer PostgreSQL ODBC-driveren (**psqlODBC**) på den maskine, der kører *digna*-backend,
efter leverandørens officielle installationsvejledning.

Driveren registrerer sig under et navn, der varierer efter platform og pakke — typisk
**PostgreSQL Unicode(x64)** på Windows og **PostgreSQL ODBC Driver(UNICODE)** på Linux. Aflæs
det nøjagtige navn på din vært som beskrevet i
[Installer ODBC-driveren på digna-værten](overview.md#install-the-driver), og brug det navn til
egenskaben `DRIVER` nedenfor.

---

## 2. ODBC-egenskaber {: #2-odbc-properties }

!!! important "Et eksempel, ikke en specifikation"

    Sættet nedenfor er én kombination, der vides at virke. Egenskaberne tilhører
    psqlODBC-driveren, så deres navne, standardværdier og accepterede værdier varierer mellem
    driverversioner og platforme, og det, din server kræver — især SSL — kan også variere. Brug
    dette som udgangspunkt, og tjek dokumentationen for den driverversion, du har installeret.

Tilføj følgende egenskaber på skærmen **Add DB Connection**:

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Skal matche det drivernavn, der er registreret på *digna*-værten |
| `SERVER` | `db.example.com` | Servernavn eller IP-adresse |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Databasen, der indeholder kildeskemaerne. Det er den eneste database, denne forbindelse kan profilere |
| `UID` | `digna_source_user` | Databasebruger |
| `PWD` | `<password>` | Sæt flueben i **Encrypted** |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` eller `verify-full` — skal accepteres af serveren |

Den resulterende forbindelsesstreng ser sådan ud:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Enhver anden psqlODBC-indstilling kan tilføjes som en ekstra egenskab — for eksempel
`ReadOnly=1` for en skrivebeskyttet session eller `ConnSettings` for at køre `SET`-sætninger,
når forbindelsen oprettes.

---

## 3. *digna*-konfiguration {: #3-digna-configuration }

Angiv følgende på skærmen **Add DB Connection**:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Bemærkninger om PostgreSQL {: #4-notes-on-postgresql }

- **`SSLMode` skal matche serveren.** En server, der er konfigureret med `hostssl`, afviser
  `SSLMode=disable`, og `verify-ca` eller `verify-full` kræver desuden, at rodcertifikatet er
  tilgængeligt for driveren på *digna*-værten. Hvis du skulle vælge en bestemt tilstand, da du
  testede driveren, så brug den samme her.
- **Én forbindelse ser én database.** *digna* tilbyder skemaerne i den database, der er angivet i
  `DATABASE`, fordi PostgreSQL kun rapporterer den aktuelle database som katalog. Kildetabeller i
  en anden database kræver deres egen forbindelse.
- **Profileringstilstande.** *Permanent* opretter arbejdstabellerne i **Work Schema**, så
  brugeren skal have `CREATE` på det skema. *Session* bruger `CREATE TEMPORARY TABLE` og rører
  ikke **Work Schema**. *Standard* kræver kun læseadgang.

---

## 5. Verificering af driveren (valgfrit) {: #5-verifying-the-driver-optional }

Det er ikke nødvendigt at konfigurere en ODBC-datakilde for en DSN-løs forbindelse, men
driverens egen dialog er en bekvem måde at bekræfte, at driveren virker, og at serveren
accepterer dine legitimationsoplysninger og din SSL-tilstand, før du indtaster dem i *digna*.

#### Trin 1
![Trin 1](images/postgres/create_odbc_data_source_step1.png)

#### Trin 2 – Test forbindelsen

Klik på knappen **Test Connection**.

![Trin 2](images/postgres/create_odbc_data_source_step2.png)

De værdier, du indtastede her, er præcis de værdier, egenskaberne i
[afsnit 2](#2-odbc-properties) skal have.
