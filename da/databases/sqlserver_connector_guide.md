# Kildeconnector til MS SQL Server

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til
Microsoft SQL Server over **ODBC** med en **DSN-løs** forbindelsesstreng.

*digna*-delen af opsætningen er den samme for alle teknologier — hvor forbindelser oprettes,
hvordan egenskabsværdier krypteres, hvordan en forbindelse testes, og hvad profileringstilstandene
betyder. Den er beskrevet i [Oversigt over databaseforbindelser](overview.md). Denne side dækker
det, der er specifikt for SQL Server.

!!! note "Azure Synapse Analytics"

    Synapse konfigureres også som en SQL Server-forbindelse, med et andet værtsnavn og nogle få
    ekstra forhold at tage højde for — se [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Installer **ODBC Driver 18 for SQL Server** på den maskine, der kører *digna*-backend, efter
[Microsofts installationsvejledning](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

Den driver, der følger med Windows under det enkle navn **SQL Server**, virker også, men den er
for længst afløst og understøtter hverken moderne TLS-indstillinger eller Azure-autentificering.
Brug den kun, hvor det ikke er muligt at installere den aktuelle driver.

Aflæs det nøjagtige registrerede drivernavn på din vært som beskrevet i
[Installer ODBC-driveren på digna-værten](overview.md#install-the-driver).

---

## 2. ODBC-egenskaber {: #2-odbc-properties }

!!! important "Et eksempel, ikke en specifikation"

    Sættet nedenfor er én kombination, der vides at virke. Egenskaberne tilhører Microsofts
    ODBC-driver, så deres navne, standardværdier og accepterede værdier varierer mellem
    driverversioner — Driver 18 krypterer for eksempel som standard, hvilket Driver 17 ikke
    gjorde — og mellem platforme. Brug dette som udgangspunkt, og tjek dokumentationen for den
    driverversion, du har installeret.

Tilføj følgende egenskaber på skærmen **Add DB Connection**:

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Skal matche det drivernavn, der er registreret på *digna*-værten |
| `SERVER` | `sql.example.com` | Servernavn eller IP-adresse. Navngivne instanser: `host\instance`; en ikke-standardport: `host,1433` |
| `PORT` | `1433` | Udelades, når porten allerede indgår i `SERVER` |
| `DATABASE` | `digna_source_db` | Databasen, der indeholder kildeskemaerne. Det er den eneste database, denne forbindelse kan profilere |
| `UID` | `digna_source_user` | Databasebruger |
| `PWD` | `<password>` | Sæt flueben i **Encrypted** |

Den resulterende forbindelsesstreng ser sådan ud:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Kryptering med ODBC Driver 18

Driver 18 krypterer forbindelser som standard og validerer servercertifikatet. Mod en server med
et certifikat, som din *digna*-vært ikke har tillid til — typisk et selvsigneret certifikat —
fejler forbindelsen med en fejl i certifikatkæden. Tilføj:

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `Encrypt` | `yes` | Standard i Driver 18; sæt kun til `no`, hvis serveren ikke kan håndtere TLS |
| `TrustServerCertificate` | `yes` | Springer certifikatvalideringen over. Praktisk i testmiljøer; installer hellere certifikatet i produktion |

### Windows-godkendelse

For at oprette forbindelse som den konto, der kører *digna*-tjenesten, i stedet for med et
SQL-login skal du fjerne `UID` og `PWD` og tilføje:

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `Trusted_Connection` | `yes` | *digna*-tjenestekontoen skal have databaserettighederne |

---

## 3. *digna*-konfiguration {: #3-digna-configuration }

Angiv følgende på skærmen **Add DB Connection**:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Bemærkninger om MS SQL Server {: #4-notes-on-ms-sql-server }

- **Én forbindelse ser én database.** *digna* tilbyder skemaerne i den database, der er angivet i
  `DATABASE`, fordi SQL Server kun rapporterer den aktuelle database som katalog. Kildetabeller i
  en anden database kræver deres egen forbindelse.
- **Profileringstilstande.** *Permanent* opretter arbejdstabellerne i **Work Schema**, så
  brugeren skal have `CREATE TABLE` der. *Session* bruger lokale midlertidige tabeller (`#wt_…`)
  i `tempdb` og rører ikke **Work Schema**. *Standard* kræver kun læseadgang.
- **`SERVER` indeholder instans og port.** Med en navngivet instans kræver `host\instance`, at
  tjenesten SQL Server Browser kan nås; `host,port` undgår det.

---

## 5. Verificering af driveren (valgfrit) {: #5-verifying-the-driver-optional }

Det er ikke nødvendigt at konfigurere en ODBC-datakilde for en DSN-løs forbindelse, men
driverens egen guide er en bekvem måde at bekræfte, at driveren virker, og at serveren
accepterer dine legitimationsoplysninger, før du indtaster dem i *digna*.

#### Trin 1
![Trin 1](images/sqlserver/create_odbc_data_source_step1.png)

Klik på knappen **Next >**.

#### Trin 2
![Trin 2](images/sqlserver/create_odbc_data_source_step2.png)

Vælg autentificeringsmetoden (f.eks. brugernavn og adgangskode),
og angiv de nødvendige oplysninger.

Klik på knappen **Next >**.

#### Trin 3
![Trin 3](images/sqlserver/create_odbc_data_source_step3.png)

Vælg de ANSI-kompatible indstillinger, og klik derefter på knappen **Next >**.

#### Trin 4
![Trin 4](images/sqlserver/create_odbc_data_source_step4.png)

Du kan beholde standardindstillingerne eller vælge logningsindstillinger efter behov
og klikke på knappen **Finish**.

#### Trin 5
![Trin 5](images/sqlserver/create_odbc_data_source_step5.png)

Klik nu på knappen **Test datasource**.

#### Trin 6
![Trin 6](images/sqlserver/create_odbc_data_source_step6.png)

En bekræftelsesskærm viser, at driveren og legitimationsoplysningerne virker. De værdier, du
indtastede, er præcis de værdier, egenskaberne i [afsnit 2](#2-odbc-properties) skal have.