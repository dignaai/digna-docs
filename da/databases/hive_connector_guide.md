# Kildeconnector til Hive

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til
Apache Hive over **ODBC** med en **DSN-løs** forbindelsesstreng.

*digna*-delen af opsætningen er den samme for alle teknologier — hvor forbindelser oprettes,
hvordan egenskabsværdier krypteres, hvordan en forbindelse testes, og hvad profileringstilstandene
betyder. Den er beskrevet i [Oversigt over databaseforbindelser](overview.md). Denne side dækker
det, der er specifikt for Hive.

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Installer **Cloudera ODBC Driver for Apache Hive** på den maskine, der kører *digna*-backend,
efter leverandørens officielle installationsvejledning.

Aflæs det nøjagtige registrerede drivernavn på din vært som beskrevet i
[Installer ODBC-driveren på digna-værten](overview.md#install-the-driver).

---

## 2. ODBC-egenskaber {: #2-odbc-properties }

!!! important "Et eksempel, ikke en specifikation"

    Sættet nedenfor er én kombination, der vides at virke. Egenskaberne tilhører Cloudera
    Hive-driveren, så deres navne, standardværdier og accepterede værdier varierer mellem
    driverversioner og platforme, og hvad HiveServer2 accepterer, afhænger helt af, hvordan
    clusteren er sikret — autentificeringsmekanisme, transporttilstand, TLS, gateway. Brug dette
    som udgangspunkt, og tjek dokumentationen for den driverversion, du har installeret.

Tilføj følgende egenskaber på skærmen **Add DB Connection**:

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Skal matche det drivernavn, der er registreret på *digna*-værten |
| `HOST` | `hive.example.com` | HiveServer2-værtsnavn eller IP-adresse |
| `PORT` | `10000` | HiveServer2-port; `10001` for HTTP-transport |

Den resulterende forbindelsesstreng ser sådan ud:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Autentificering

En usikret HiveServer2 accepterer de tre egenskaber ovenfor, som de er. Hvor autentificering er
aktiveret, skal du tilføje:

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `AuthMech` | `3` | `0` ingen autentificering, `2` kun brugernavn, `3` brugernavn og adgangskode, `1` Kerberos |
| `UID` | `digna_source_user` | Påkrævet for `AuthMech` `2` og `3` |
| `PWD` | `<password>` | Påkrævet for `AuthMech` `3`. Sæt flueben i **Encrypted** |

For Kerberos (`AuthMech=1`) skal *digna*-værten desuden have en gyldig ticket eller keytab samt
egenskaberne `KrbHostFQDN`, `KrbServiceName` og `KrbRealm`, som driveren dokumenterer.

### Transport og TLS

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `ThriftTransport` | `2` | `0` binær (standard, port 10000), `1` SASL, `2` HTTP (port 10001, og det en Knox-gateway forventer) |
| `HTTPPath` | `cliservice` | Med `ThriftTransport=2` |
| `SSL` | `1` | Hvor HiveServer2 er sikret med TLS |
| `Schema` | `dignadata` | Hive-database, som sessionen starter i. Valgfri — *digna* kvalificerer sine forespørgsler |

---

## 3. *digna*-konfiguration {: #3-digna-configuration }

Angiv følgende på skærmen **Add DB Connection**:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Bemærkninger om Hive {: #4-notes-on-hive }

- **Kataloger kommer fra driveren.** Hive har ikke sit eget katalog, så *digna* bruger det,
  driveren rapporterer — normalt en enkelt post med navnet `HIVE` — og viser Hive-databaserne
  som skemaer under den.
- **Work Schema er en Hive-database.** Ved *Permanent*-profilering skal brugeren have ret til at
  oprette og slette tabeller i den, og den underliggende lagerplacering skal være skrivbar.
- **Profileringstilstande.** *Permanent* opretter arbejdstabellerne i **Work Schema**. *Session*
  bruger `CREATE TEMPORARY TABLE`, hvilket kræver en HiveServer2, der understøtter midlertidige
  tabeller, og rører ikke **Work Schema**. *Standard* kræver kun læseadgang og er den tilstand,
  du skal vælge på en cluster, hvor *digna* slet ikke har skriveadgang.
- **Profilering er en række forespørgsler, ikke en scanning.** Hver statistik beregnes af
  HiveServer2, så den kø, som *digna*s bruger sender til, bør have tilstrækkelig kapacitet til
  inspektionsvinduet.

---

## 5. Verificering af driveren (valgfrit) {: #5-verifying-the-driver-optional }

Det er ikke nødvendigt at konfigurere en ODBC-datakilde for en DSN-løs forbindelse, men
driverens egen dialog er en bekvem måde at bekræfte, at driveren, transporttilstanden og dine
legitimationsoplysninger virker, før du indtaster dem i *digna*.

#### Trin 1
![Trin 1](images/hive/create_odbc_data_source_step1.png)

Felterne **Host**, **Port**, **Database**, **Mechanism** og **Thrift Transport** her svarer til
egenskaberne `HOST`, `PORT`, `Schema`, `AuthMech` og `ThriftTransport` i
[afsnit 2](#2-odbc-properties).

#### Trin 2 – Test forbindelsen

Angiv adgangskoden, og klik på knappen **Test**.

![Trin 2](images/hive/create_odbc_data_source_step2.png)

Efter en vellykket test skal du klikke på knappen **OK**.