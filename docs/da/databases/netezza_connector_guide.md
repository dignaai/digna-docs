---
title: Netezza-connector – Databaseintegration | digna-dokumentation
description: Konfigurer digna til at oprette forbindelse til Netezza over ODBC med en DSN-løs forbindelsesstreng. Dækker NetezzaSQL-driveren, de nødvendige ODBC-egenskaber og forbindelsesindstillingerne på digna-siden.
image: /assets/logo_square.png
---


# Kildeconnector til Netezza

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til
Netezza over **ODBC** med en **DSN-løs** forbindelsesstreng.

*digna*-delen af opsætningen er den samme for alle teknologier — hvor forbindelser oprettes,
hvordan egenskabsværdier krypteres, hvordan en forbindelse testes, og hvad profileringstilstandene
betyder. Den er beskrevet i [Oversigt over databaseforbindelser](overview.md). Denne side dækker
det, der er specifikt for Netezza.

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Installer **NetezzaSQL**-ODBC-driveren (en del af IBM Netezza-klientværktøjerne) på den maskine,
der kører *digna*-backend, efter leverandørens officielle installationsvejledning.

Aflæs det nøjagtige registrerede drivernavn på din vært som beskrevet i
[Installer ODBC-driveren på digna-værten](overview.md#install-the-driver).

---

## 2. ODBC-egenskaber {: #2-odbc-properties }

!!! important "Et eksempel, ikke en specifikation"

    Sættet nedenfor er én kombination, der vides at virke. Egenskaberne tilhører
    NetezzaSQL-driveren, så deres navne, standardværdier og accepterede værdier varierer mellem
    klientversioner og platforme, og en TLS-sikret appliance kræver mere end de egenskaber, der
    vises her. Brug dette som udgangspunkt, og tjek dokumentationen for den klientversion, du
    har installeret.

Tilføj følgende egenskaber på skærmen **Add DB Connection**:

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Skal matche det drivernavn, der er registreret på *digna*-værten. De krøllede parenteser er den sædvanlige måde at skrive dette navn på |
| `SERVER` | `netezza.example.com` | Servernavn eller IP-adresse |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Databasen, som sessionen starter i |
| `UID` | `ADMIN` | Databasebruger |
| `PWD` | `<password>` | Sæt flueben i **Encrypted** |

Den resulterende forbindelsesstreng ser sådan ud:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

Afhængigt af din driverversion, opsætning og dine sikkerhedskrav kan der være brug for flere
egenskaber — for eksempel `SecurityLevel` og `CaCertFile` for en TLS-sikret appliance. Alle
indstillinger, som driverens dialoger *Advanced*, *SSL* og *Driver* tilbyder, kan tilføjes som
en egenskab.

---

## 3. *digna*-konfiguration {: #3-digna-configuration }

Angiv følgende på skærmen **Add DB Connection**:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Bemærkninger om Netezza {: #4-notes-on-netezza }

- **Både kataloger og skemaer gælder.** *digna* viser de databaser, brugeren må se (fra
  `_V_DATABASE`), som kataloger og deres skemaer (fra `_V_SCHEMA`) under dem, så én forbindelse
  kan betjene kilder i mere end én database. `DATABASE` afgør kun, hvor sessionen starter.
- **Identifikatorer skrives med store bogstaver**, medmindre de er oprettet i anførselstegn,
  hvilket er grunden til, at eksemplerne ovenfor bruger `TEST` og `ADMIN`.
- **Profileringstilstande.** *Permanent* opretter arbejdstabellerne i **Work Schema**, så
  brugeren skal have `CREATE TABLE` der. *Session* bruger `CREATE TEMPORARY TABLE` og rører ikke
  **Work Schema**. *Standard* kræver kun læseadgang.

---

## 5. Verificering af driveren (valgfrit) {: #5-verifying-the-driver-optional }

Det er ikke nødvendigt at konfigurere en ODBC-datakilde for en DSN-løs forbindelse, men
driverens egen dialog er en bekvem måde at bekræfte, at driveren og dine
legitimationsoplysninger virker, før du indtaster dem i *digna*.

#### Trin 1
![Trin 1](images/netezza/create_odbc_data_source_step1.png)

Felterne i **DSN Options** svarer én til én til egenskaberne i
[afsnit 2](#2-odbc-properties). Afhængigt af din Netezza-driver, opsætning og dine
sikkerhedskrav kan du også få brug for at udfylde fanerne **Advanced DSN Options**,
**SSL DSN Options** eller **Driver Options**; til den enkleste opsætning er **DSN Options**
tilstrækkelig.

Klik på knappen **Test Connection**.

#### Trin 2
![Trin 2](images/netezza/create_odbc_data_source_step2.png)

Når du får bekræftelsesskærmen, virker driveren, og værdierne er korrekte.
