---
title: Netezza-connector – databaseintegrasjon | digna-dokumentasjon
description: Konfigurer digna til å koble til Netezza over ODBC med en DSN-løs tilkoblingsstreng. Dekker NetezzaSQL-driveren, de nødvendige ODBC-egenskapene og tilkoblingsinnstillingene på digna-siden.
image: /assets/logo_square.png
---


# Kildeconnector for Netezza

Denne veiledningen beskriver hvordan du konfigurerer *digna* til å koble til Netezza over **ODBC**, med en
**DSN-løs** tilkoblingsstreng.

*digna*-siden av oppsettet er den samme for alle teknologier — hvor tilkoblinger opprettes,
hvordan egenskapsverdier krypteres, hvordan en tilkobling testes og hva profileringsmodusene
betyr. Den er beskrevet i [Oversikt over databasetilkoblinger](overview.md). Denne siden dekker det
som er spesifikt for Netezza.

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Installer ODBC-driveren **NetezzaSQL** (en del av IBM Netezza-klientverktøyene) på maskinen
som kjører *digna*-backend, i henhold til leverandørens offisielle installasjonsveiledning.

Les av det nøyaktige registrerte drivernavnet på verten din som beskrevet i
[Installer ODBC-driveren på digna-verten](overview.md#install-the-driver).

---

## 2. ODBC-egenskaper {: #2-odbc-properties }

!!! important "Et eksempel, ikke en spesifikasjon"

    Settet nedenfor er én kombinasjon som er kjent for å fungere. Egenskapene tilhører
    NetezzaSQL-driveren, så navnene, standardverdiene og de godtatte verdiene varierer mellom
    klientversjoner og plattformer, og en TLS-sikret appliance trenger flere egenskaper enn dem som vises
    her. Bruk dette som et utgangspunkt og sjekk dokumentasjonen for klientversjonen du har
    installert.

Legg til følgende egenskaper i skjermbildet **Add DB Connection**:

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Må samsvare med drivernavnet som er registrert på *digna*-verten. Krøllparentesene er den vanlige måten å skrive dette navnet på |
| `SERVER` | `netezza.example.com` | Servernavn eller IP-adresse |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Databasen sesjonen starter i |
| `UID` | `ADMIN` | Databasebruker |
| `PWD` | `<password>` | Kryss av for **Encrypted** |

Den resulterende tilkoblingsstrengen ser slik ut:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

Avhengig av driverversjon, oppsett og sikkerhetskrav kan flere egenskaper være
nødvendige — for eksempel `SecurityLevel` og `CaCertFile` for en TLS-sikret appliance. Alle alternativer
som driverens dialogbokser *Advanced*, *SSL* og *Driver* tilbyr, kan legges til som en egenskap.

---

## 3. *digna*-konfigurasjon {: #3-digna-configuration }

I skjermbildet **Add DB Connection** oppgir du følgende:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Merknader om Netezza {: #4-notes-on-netezza }

- **Både kataloger og skjemaer gjelder.** *digna* viser databasene brukeren har lov til å se (fra
  `_V_DATABASE`) som kataloger, og skjemaene deres (fra `_V_SCHEMA`) under dem, så én tilkobling
  kan betjene kilder i mer enn én database. `DATABASE` avgjør bare hvor sesjonen
  starter.
- **Identifikatorer skrives med store bokstaver** med mindre de ble opprettet i anførselstegn, og det er derfor
  eksemplene ovenfor bruker `TEST` og `ADMIN`.
- **Profileringsmoduser.** *Permanent* oppretter arbeidstabellene i **Work Schema**, så brukeren trenger
  `CREATE TABLE` der. *Session* bruker `CREATE TEMPORARY TABLE` og rører ikke
  **Work Schema**. *Standard* trenger bare lesetilgang.

---

## 5. Verifisere driveren (valgfritt) {: #5-verifying-the-driver-optional }

Det er ikke nødvendig å konfigurere en ODBC-datakilde for en DSN-løs tilkobling, men driverens
egen dialogboks er en praktisk måte å bekrefte at driveren og legitimasjonen din fungerer, før du
legger dem inn i *digna*.

#### Trinn 1
![Trinn 1](images/netezza/create_odbc_data_source_step1.png)

Feltene i **DSN Options** tilsvarer én til én egenskapene i
[avsnitt 2](#2-odbc-properties). Avhengig av Netezza-driveren, oppsettet og sikkerhetskravene
kan du også trenge opplysninger i fanene **Advanced DSN Options**, **SSL DSN Options** eller
**Driver Options**; for det enkleste oppsettet er **DSN Options** tilstrekkelig.

Klikk på knappen **Test Connection**.

#### Trinn 2
![Trinn 2](images/netezza/create_odbc_data_source_step2.png)

Når du får bekreftelsesskjermbildet, fungerer driveren og verdiene er riktige.
