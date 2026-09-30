---
title: Teradata-connector – databaseintegrasjon | digna-dokumentasjon
description: Konfigurer digna til å koble til Teradata over ODBC med en DSN-løs tilkoblingsstreng. Dekker Teradata ODBC-driveren, egenskapen DBCNAME, påloggingsmekanismer og tilkoblingsinnstillingene på digna-siden.
image: /assets/logo_square.png
---


# Kildeconnector for Teradata

Denne veiledningen beskriver hvordan du konfigurerer *digna* til å koble til Teradata over **ODBC**, med en
**DSN-løs** tilkoblingsstreng.

*digna*-siden av oppsettet er den samme for alle teknologier — hvor tilkoblinger opprettes,
hvordan egenskapsverdier krypteres, hvordan en tilkobling testes og hva profileringsmodusene
betyr. Den er beskrevet i [Oversikt over databasetilkoblinger](overview.md). Denne siden dekker det
som er spesifikt for Teradata.

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Installer **ODBC Driver for Teradata** på maskinen som kjører *digna*-backend,
i henhold til leverandørens offisielle installasjonsveiledning.

Driveren registrerer seg med versjonsnummeret i navnet, for eksempel
**Teradata Database ODBC Driver 20.00**. Les av det nøyaktige registrerte navnet på verten din som
beskrevet i [Installer ODBC-driveren på digna-verten](overview.md#install-the-driver).

---

## 2. ODBC-egenskaper {: #2-odbc-properties }

!!! important "Et eksempel, ikke en spesifikasjon"

    Settet nedenfor er én kombinasjon som er kjent for å fungere. Egenskapene tilhører
    Teradata ODBC-driveren, så navnene, standardverdiene og de godtatte verdiene varierer mellom
    driverversjoner — versjonen er en del av selve drivernavnet — og mellom plattformer. Bruk dette
    som et utgangspunkt og sjekk dokumentasjonen for driverversjonen du har installert.

Legg til følgende egenskaper i skjermbildet **Add DB Connection**:

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Må samsvare med drivernavnet som er registrert på *digna*-verten |
| `DBCNAME` | `teradata.example.com` | Servernavn eller IP-adresse. Teradatas eget navn på vertsegenskapen |
| `UID` | `digna_source_user` | Databasebruker |
| `PWD` | `<password>` | Kryss av for **Encrypted** |

Den resulterende tilkoblingsstrengen ser slik ut:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Nyttige tilleggsegenskaper:

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `MechanismName` | `TD2` | Påloggingsmekanisme. `TD2` er Teradatas standard; bruk `LDAP` for katalogautentisering |
| `DefaultDatabase` | `dad` | Databasen sesjonen starter i |
| `CharacterSet` | `UTF8` | Angi denne der standardtegnsettet for sesjonen ville ødelagt ikke-ASCII-data |

---

## 3. *digna*-konfigurasjon {: #3-digna-configuration }

I skjermbildet **Add DB Connection** oppgir du følgende:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Merknader om Teradata {: #4-notes-on-teradata }

- **En Teradata-database er en katalog, ikke et skjema.** *digna* viser databasene brukeren har lov til å
  se (fra `DBC.DatabasesV`) som kataloger, og skjemanivået gjelder ikke. Når du legger til en
  datakilde, velger du databasen som katalog; skjemaet rapporteres som *not applicable*.
- **Én tilkobling når alle tillatte databaser**, så én enkelt tilkobling kan betjene kilder
  på tvers av databaser — i motsetning til teknologiene der tilkoblingen er låst til én database.
- **Work Schema er en database.** For *Permanent*-profilering angir du Teradata-databasen som
  inneholder arbeidstabellene, og gir brukeren `CREATE TABLE`-rettigheter pluss en `PERM`-plasstildeling
  i den — en database med null perm space kan ikke inneholde en tabell.
- **Profileringsmoduser.** *Permanent* oppretter tabeller i **Work Schema**. *Session* bruker en
  `VOLATILE`-tabell, som trenger `SPOOL`-plass, men ingen perm space og ingen rettigheter i **Work
  Schema**. *Standard* trenger bare lesetilgang.

---

## 5. Verifisere driveren (valgfritt) {: #5-verifying-the-driver-optional }

Det er ikke nødvendig å konfigurere en ODBC-datakilde for en DSN-løs tilkobling, men driverens
egen dialogboks er en praktisk måte å bekrefte at driveren og legitimasjonen din fungerer, før du
legger dem inn i *digna*.

#### Trinn 1
![Trinn 1](images/teradata/create_odbc_data_source_step1.png)

Feltet **Name or IP address** her tilsvarer egenskapen `DBCNAME` i
[avsnitt 2](#2-odbc-properties).

Klikk på knappen **Test**.

#### Trinn 2
![Trinn 2](images/teradata/create_odbc_data_source_step2.png)

Oppgi brukernavn og passord, og klikk deretter på knappen **OK**. Et bekreftelsesskjermbilde viser at
driveren og legitimasjonen fungerer.
