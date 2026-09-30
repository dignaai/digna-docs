---
title: Teradata-connector – Databaseintegration | digna-dokumentation
description: Konfigurer digna til at oprette forbindelse til Teradata over ODBC med en DSN-løs forbindelsesstreng. Dækker Teradata ODBC-driveren, egenskaben DBCNAME, logon-mekanismer og forbindelsesindstillingerne på digna-siden.
image: /assets/logo_square.png
---


# Kildeconnector til Teradata

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til
Teradata over **ODBC** med en **DSN-løs** forbindelsesstreng.

*digna*-delen af opsætningen er den samme for alle teknologier — hvor forbindelser oprettes,
hvordan egenskabsværdier krypteres, hvordan en forbindelse testes, og hvad profileringstilstandene
betyder. Den er beskrevet i [Oversigt over databaseforbindelser](overview.md). Denne side dækker
det, der er specifikt for Teradata.

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Installer **ODBC Driver for Teradata** på den maskine, der kører *digna*-backend, efter
leverandørens officielle installationsvejledning.

Driveren registrerer sig med versionen i navnet, for eksempel
**Teradata Database ODBC Driver 20.00**. Aflæs det nøjagtige registrerede navn på din vært som
beskrevet i [Installer ODBC-driveren på digna-værten](overview.md#install-the-driver).

---

## 2. ODBC-egenskaber {: #2-odbc-properties }

!!! important "Et eksempel, ikke en specifikation"

    Sættet nedenfor er én kombination, der vides at virke. Egenskaberne tilhører Teradata
    ODBC-driveren, så deres navne, standardværdier og accepterede værdier varierer mellem
    driverversioner — versionen er en del af selve drivernavnet — og mellem platforme. Brug dette
    som udgangspunkt, og tjek dokumentationen for den driverversion, du har installeret.

Tilføj følgende egenskaber på skærmen **Add DB Connection**:

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Skal matche det drivernavn, der er registreret på *digna*-værten |
| `DBCNAME` | `teradata.example.com` | Servernavn eller IP-adresse. Teradatas eget navn for værtsegenskaben |
| `UID` | `digna_source_user` | Databasebruger |
| `PWD` | `<password>` | Sæt flueben i **Encrypted** |

Den resulterende forbindelsesstreng ser sådan ud:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Nyttige ekstra egenskaber:

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `MechanismName` | `TD2` | Logon-mekanisme. `TD2` er Teradatas standard; brug `LDAP` til katalogtjenestebaseret autentificering |
| `DefaultDatabase` | `dad` | Databasen, som sessionen starter i |
| `CharacterSet` | `UTF8` | Angiv denne, hvor sessionens standardtegnsæt ville ødelægge data uden for ASCII |

---

## 3. *digna*-konfiguration {: #3-digna-configuration }

Angiv følgende på skærmen **Add DB Connection**:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Bemærkninger om Teradata {: #4-notes-on-teradata }

- **En Teradata-database er et katalog, ikke et skema.** *digna* viser de databaser, brugeren må
  se (fra `DBC.DatabasesV`), som kataloger, og skemaniveauet gælder ikke. Når du tilføjer en
  datakilde, skal du vælge databasen som katalog; skemaet rapporteres som *not applicable*.
- **Én forbindelse når alle tilladte databaser**, så en enkelt forbindelse kan betjene kilder på
  tværs af databaser — i modsætning til de teknologier, hvor forbindelsen er låst til én database.
- **Work Schema er en database.** Ved *Permanent*-profilering skal du angive den
  Teradata-database, der indeholder arbejdstabellerne, og give brugeren `CREATE TABLE`-rettigheder
  samt en `PERM`-pladstildeling i den — en database med nul perm space kan ikke indeholde en tabel.
- **Profileringstilstande.** *Permanent* opretter tabeller i **Work Schema**. *Session* bruger en
  `VOLATILE`-tabel, som kræver `SPOOL`-plads, men ingen perm space og ingen rettigheder i **Work
  Schema**. *Standard* kræver kun læseadgang.

---

## 5. Verificering af driveren (valgfrit) {: #5-verifying-the-driver-optional }

Det er ikke nødvendigt at konfigurere en ODBC-datakilde for en DSN-løs forbindelse, men
driverens egen dialog er en bekvem måde at bekræfte, at driveren og dine
legitimationsoplysninger virker, før du indtaster dem i *digna*.

#### Trin 1
![Trin 1](images/teradata/create_odbc_data_source_step1.png)

Feltet **Name or IP address** her svarer til egenskaben `DBCNAME` i
[afsnit 2](#2-odbc-properties).

Klik på knappen **Test**.

#### Trin 2
![Trin 2](images/teradata/create_odbc_data_source_step2.png)

Angiv brugernavn og adgangskode, og klik derefter på knappen **OK**. En bekræftelsesskærm viser,
at driveren og legitimationsoplysningerne virker.
