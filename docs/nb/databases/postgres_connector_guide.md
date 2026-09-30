---
title: PostgreSQL-connector – databaseintegrasjon | digna-dokumentasjon
description: Konfigurer digna til å koble til PostgreSQL over ODBC med en DSN-løs tilkoblingsstreng. Dekker psqlODBC-driveren, de nødvendige ODBC-egenskapene, SSL-moduser og tilkoblingsinnstillingene på digna-siden.
image: /assets/logo_square.png
---


# Kildeconnector for PostgreSQL

Denne veiledningen beskriver hvordan du konfigurerer *digna* til å koble til PostgreSQL over **ODBC**, med en
**DSN-løs** tilkoblingsstreng.

*digna*-siden av oppsettet er den samme for alle teknologier — hvor tilkoblinger opprettes,
hvordan egenskapsverdier krypteres, hvordan en tilkobling testes og hva profileringsmodusene
betyr. Den er beskrevet i [Oversikt over databasetilkoblinger](overview.md). Denne siden dekker det
som er spesifikt for PostgreSQL.

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Installer PostgreSQL ODBC-driveren (**psqlODBC**) på maskinen som kjører *digna*-backend,
i henhold til leverandørens offisielle installasjonsveiledning.

Driveren registrerer seg under et navn som varierer mellom plattformer og pakker — vanligvis
**PostgreSQL Unicode(x64)** på Windows og **PostgreSQL ODBC Driver(UNICODE)** på Linux. Les av
det nøyaktige navnet på verten din som beskrevet i
[Installer ODBC-driveren på digna-verten](overview.md#install-the-driver), og bruk det navnet
for egenskapen `DRIVER` nedenfor.

---

## 2. ODBC-egenskaper {: #2-odbc-properties }

!!! important "Et eksempel, ikke en spesifikasjon"

    Settet nedenfor er én kombinasjon som er kjent for å fungere. Egenskapene tilhører
    psqlODBC-driveren, så navnene, standardverdiene og de godtatte verdiene varierer mellom
    driverversjoner og plattformer, og det serveren din krever — særlig SSL — kan også være annerledes.
    Bruk dette som et utgangspunkt og sjekk dokumentasjonen for driverversjonen du har
    installert.

Legg til følgende egenskaper i skjermbildet **Add DB Connection**:

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Må samsvare med drivernavnet som er registrert på *digna*-verten |
| `SERVER` | `db.example.com` | Servernavn eller IP-adresse |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Databasen som inneholder kildeskjemaene. Det er den eneste databasen denne tilkoblingen kan profilere |
| `UID` | `digna_source_user` | Databasebruker |
| `PWD` | `<password>` | Kryss av for **Encrypted** |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` eller `verify-full` — må godtas av serveren |

Den resulterende tilkoblingsstrengen ser slik ut:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Alle andre psqlODBC-alternativer kan legges til som en ekstra egenskap — for eksempel
`ReadOnly=1` for en skrivebeskyttet sesjon, eller `ConnSettings` for å kjøre `SET`-setninger ved
tilkobling.

---

## 3. *digna*-konfigurasjon {: #3-digna-configuration }

I skjermbildet **Add DB Connection** oppgir du følgende:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Merknader om PostgreSQL {: #4-notes-on-postgresql }

- **`SSLMode` må samsvare med serveren.** En server konfigurert med `hostssl` avviser
  `SSLMode=disable`, og `verify-ca` eller `verify-full` krever i tillegg at rotsertifikatet er
  tilgjengelig for driveren på *digna*-verten. Hvis du måtte velge en bestemt modus da du
  testet driveren, bruker du den samme her.
- **Én tilkobling ser én database.** *digna* tilbyr skjemaene i databasen som er angitt i
  `DATABASE`, fordi PostgreSQL bare rapporterer den gjeldende databasen som en katalog. Kildetabeller
  i en annen database trenger sin egen tilkobling.
- **Profileringsmoduser.** *Permanent* oppretter arbeidstabellene i **Work Schema**, så brukeren
  trenger `CREATE` på det skjemaet. *Session* bruker `CREATE TEMPORARY TABLE` og rører ikke
  **Work Schema**. *Standard* trenger bare lesetilgang.

---

## 5. Verifisere driveren (valgfritt) {: #5-verifying-the-driver-optional }

Det er ikke nødvendig å konfigurere en ODBC-datakilde for en DSN-løs tilkobling, men driverens
egen dialogboks er en praktisk måte å bekrefte at driveren fungerer og at serveren godtar
legitimasjonen og SSL-modusen din, før du legger dem inn i *digna*.

#### Trinn 1
![Trinn 1](images/postgres/create_odbc_data_source_step1.png)

#### Trinn 2 – Test tilkoblingen

Klikk på knappen **Test Connection**.

![Trinn 2](images/postgres/create_odbc_data_source_step2.png)

Verdiene du la inn her, er nøyaktig de verdiene egenskapene i
[avsnitt 2](#2-odbc-properties) skal ha.
