# Kildeconnector for Hive

Denne veiledningen beskriver hvordan du konfigurerer *digna* til å koble til Apache Hive over **ODBC**, med en
**DSN-løs** tilkoblingsstreng.

*digna*-siden av oppsettet er den samme for alle teknologier — hvor tilkoblinger opprettes,
hvordan egenskapsverdier krypteres, hvordan en tilkobling testes og hva profileringsmodusene
betyr. Den er beskrevet i [Oversikt over databasetilkoblinger](overview.md). Denne siden dekker det
som er spesifikt for Hive.

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Installer **Cloudera ODBC Driver for Apache Hive** på maskinen som kjører *digna*-backend,
i henhold til leverandørens offisielle installasjonsveiledning.

Les av det nøyaktige registrerte drivernavnet på verten din som beskrevet i
[Installer ODBC-driveren på digna-verten](overview.md#install-the-driver).

---

## 2. ODBC-egenskaper {: #2-odbc-properties }

!!! important "Et eksempel, ikke en spesifikasjon"

    Settet nedenfor er én kombinasjon som er kjent for å fungere. Egenskapene tilhører
    Cloudera Hive-driveren, så navnene, standardverdiene og de godtatte verdiene varierer mellom
    driverversjoner og plattformer, og hva HiveServer2 godtar, avhenger helt av hvordan clusteret er
    sikret — autentiseringsmekanisme, transportmodus, TLS, gateway. Bruk dette som et
    utgangspunkt og sjekk dokumentasjonen for driverversjonen du har installert.

Legg til følgende egenskaper i skjermbildet **Add DB Connection**:

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Må samsvare med drivernavnet som er registrert på *digna*-verten |
| `HOST` | `hive.example.com` | Vertsnavn eller IP-adresse for HiveServer2 |
| `PORT` | `10000` | HiveServer2-port; `10001` for HTTP-transport |

Den resulterende tilkoblingsstrengen ser slik ut:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Autentisering

En usikret HiveServer2 godtar de tre egenskapene ovenfor som de er. Der autentisering
er aktivert, legger du til:

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `AuthMech` | `3` | `0` ingen autentisering, `2` bare brukernavn, `3` brukernavn og passord, `1` Kerberos |
| `UID` | `digna_source_user` | Påkrevd for `AuthMech` `2` og `3` |
| `PWD` | `<password>` | Påkrevd for `AuthMech` `3`. Kryss av for **Encrypted** |

For Kerberos (`AuthMech=1`) trenger *digna*-verten i tillegg en gyldig billett (ticket) eller keytab, samt
egenskapene `KrbHostFQDN`, `KrbServiceName` og `KrbRealm` som driveren dokumenterer.

### Transport og TLS

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `ThriftTransport` | `2` | `0` binær (standard, port 10000), `1` SASL, `2` HTTP (port 10001, og det en Knox-gateway forventer) |
| `HTTPPath` | `cliservice` | Med `ThriftTransport=2` |
| `SSL` | `1` | Der HiveServer2 er sikret med TLS |
| `Schema` | `dignadata` | Hive-databasen sesjonen starter i. Valgfritt — *digna* kvalifiserer spørringene sine |

---

## 3. *digna*-konfigurasjon {: #3-digna-configuration }

I skjermbildet **Add DB Connection** oppgir du følgende:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Merknader om Hive {: #4-notes-on-hive }

- **Kataloger kommer fra driveren.** Hive har ingen egen katalog, så *digna* bruker det
  driveren rapporterer — vanligvis én enkelt oppføring kalt `HIVE` — og viser Hive-databasene som
  skjemaer under den.
- **Work Schema er en Hive-database.** For *Permanent*-profilering trenger brukeren rett til å
  opprette og slette tabeller i den, og den underliggende lagringsplasseringen må være skrivbar.
- **Profileringsmoduser.** *Permanent* oppretter arbeidstabellene i **Work Schema**. *Session* bruker
  `CREATE TEMPORARY TABLE`, som krever en HiveServer2 som støtter midlertidige tabeller, og
  rører ikke **Work Schema**. *Standard* trenger bare lesetilgang og er modusen du bør velge
  på et cluster der *digna* ikke har skrivetilgang i det hele tatt.
- **Profilering er et sett med spørringer, ikke en skanning.** All statistikk beregnes av HiveServer2, så
  køen som *digna*-brukeren sender jobber til, bør ha nok kapasitet for inspeksjonsvinduet.

---

## 5. Verifisere driveren (valgfritt) {: #5-verifying-the-driver-optional }

Det er ikke nødvendig å konfigurere en ODBC-datakilde for en DSN-løs tilkobling, men driverens
egen dialogboks er en praktisk måte å bekrefte at driveren, transportmodusen og
legitimasjonen din fungerer, før du legger dem inn i *digna*.

#### Trinn 1
![Trinn 1](images/hive/create_odbc_data_source_step1.png)

Feltene **Host**, **Port**, **Database**, **Mechanism** og **Thrift Transport** her tilsvarer
egenskapene `HOST`, `PORT`, `Schema`, `AuthMech` og `ThriftTransport` i
[avsnitt 2](#2-odbc-properties).

#### Trinn 2 – Test tilkoblingen

Oppgi passordet og klikk på knappen **Test**.

![Trinn 2](images/hive/create_odbc_data_source_step2.png)

Etter en vellykket test klikker du på knappen **OK**.