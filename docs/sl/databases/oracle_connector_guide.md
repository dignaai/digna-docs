---
title: Oracle konektor – integracija baze podatkov | digna Dokumentacija
description: Konfigurirajte digna za povezavo z Oracle prek ODBC z nizom za povezavo brez DSN. Zajema gonilnik Oracle ODBC, opisnik povezave DBQ, vzdevke TNS in nastavitve povezave na strani digna.
image: /assets/logo_square.png
---


# Izvorni konektor za Oracle

Ta vodič opisuje, kako konfigurirati *digna* za povezavo z Oracle Database prek **ODBC** z
nizom za povezavo **brez DSN** (DSN-less).

Stran nastavitve *digna* je enaka za vse tehnologije — kje se ustvarjajo povezave, kako se
šifrirajo vrednosti lastnosti, kako se povezava testira in kaj pomenijo načini profiliranja.
Opisana je v [Pregled povezav z bazami podatkov](overview.md). Ta stran zajema, kar je
specifično za Oracle.

---

## 1. Namestite gonilnik ODBC {: #1-install-the-odbc-driver }

Gonilnik Oracle ODBC je del **Oracle Client** (zadošča paket "ODBC" za Instant Client).
Namestite ga na računalnik, na katerem teče zaledje *digna*, po uradnih navodilih proizvajalca
za namestitev.

Gonilnik se registrira kot **Oracle in `<OracleHomeName>`** — na primer
`Oracle in OraDB21Home1` ali `Oracle in instantclient_21_13`. Ime domačega imenika (home) se
razlikuje od namestitve do namestitve, zato na svojem gostitelju preberite natančno ime, kot je
opisano v [Namestite gonilnik ODBC na gostitelja digna](overview.md#install-the-driver).

---

## 2. Lastnosti ODBC {: #2-odbc-properties }

!!! important "Primer, ne specifikacija"

    Spodnji nabor je ena kombinacija, za katero je znano, da deluje. Lastnosti pripadajo
    gonilniku Oracle ODBC, zato se njihova imena, privzete vrednosti in sprejete vrednosti
    razlikujejo med različicami odjemalca, ime gonilnika pa je še posebej odvisno od Oracle home
    na vašem gostitelju. Uporabite to kot izhodišče in preverite dokumentacijo različice
    odjemalca, ki ste jo namestili.

Na zaslonu **Add DB Connection** dodajte naslednje lastnosti:

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Mora se ujemati z imenom gonilnika, registriranim na gostitelju *digna* |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Baza podatkov, s katero se povežete — glejte spodaj |
| `UID` | `DIGNA_SOURCE_USER` | Uporabnik baze podatkov |
| `PWD` | `<password>` | Označite **Encrypted** |

Nastali niz za povezavo je videti takole:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### Vrednost `DBQ`

`DBQ` sprejme tri oblike. Za *digna* so enakovredne; razlikujejo se po tem, kaj mora biti
konfigurirano na gostitelju *digna*:

| Oblika | Primer | Zahteva |
|---|---|---|
| **Celoten opisnik povezave** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Nič — vse je v lastnosti. Priporočeno |
| **Vzdevek TNS** | `DIGNA_SOURCE` | Vzdevek mora obstajati v `tnsnames.ora` odjemalca Oracle Client na gostitelju *digna* |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Oracle Client, ki podpira Easy Connect (12c in novejši) |

!!! tip "Raje uporabite celoten opisnik"

    Vzdevek TNS premakne polovico definicije povezave v datoteko na gostitelju *digna*, kjer
    jo je lahko pozabiti, ko se gostitelj na novo postavi ali se *digna* premakne. Celoten
    opisnik ohrani povezavo samozadostno — kar je bistvo nastavitve brez DSN.

Upoštevajte, da so oklepaji v opisniku znotraj niza za povezavo v redu, če pa vaše geslo
vsebuje `;`, ga zavijte v zavite oklepaje: `PWD={p@ss;word}`.

---

## 3. Konfiguracija *digna* {: #3-digna-configuration }

Na zaslonu **Add DB Connection** vnesite naslednje:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Opombe o Oracle {: #4-notes-on-oracle }

- **Sheme so uporabniki.** *digna* navede uporabnike Oracle kot sheme, zato je izvorna shema
  lastnik tabel — v zgornjem primeru `DIGNA_SOURCE_USER`. Uporabnik povezave potrebuje
  `SELECT` na teh tabelah, bodisi neposredno bodisi prek vloge.
- **Ena povezava vidi eno bazo podatkov.** Katalog, ki ga ponudi *digna*, je baza podatkov, na
  katero je povezava priključena, zato `DBQ` določa, katera storitev in s tem katera baza
  podatkov se profilira.
- **Identifikatorji v narekovajih razlikujejo velike in male črke.** *digna* postavi v narekovaje
  imena, ki jih prebere iz podatkovnega slovarja, kar je tisto, kar hrani Oracle — velike črke
  za objekte brez narekovajev.
- **Načini profiliranja.** *Permanent* ustvari delovne tabele v **Work Schema**, zato uporabnik
  tam potrebuje `CREATE TABLE` in kvoto na tabličnem prostoru (tablespace). *Session* uporablja
  zasebno začasno tabelo (`ORA$PTT_…`, Oracle 18c in novejši) in se **Work Schema** ne
  dotika. *Standard* potrebuje samo dostop za branje.

---

## 5. Preverjanje gonilnika (neobvezno) {: #5-verifying-the-driver-optional }

Konfiguriranje vira podatkov ODBC za povezavo brez DSN ni potrebno, vendar je gonilnikovo
lastno pogovorno okno priročen način, da preverite, ali Oracle Client, ime storitve in vaše
poverilnice delujejo, preden jih vnesete v *digna*.

#### 1. korak
![Step 1](images/oracle/create_odbc_data_source_step1.png)

**TNS Service Name**, ki je ponujen tukaj, prihaja iz `tnsnames.ora` vaše namestitve Oracle
Client — tam je definiran vzdevek, z njim pa gostitelj, vrata in ime storitve. V *digna* lahko
kot `DBQ` uporabite vzdevek ali pa namesto njega celoten opisnik.

#### 2. korak – Testirajte povezavo

Kliknite gumb **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Vnesite geslo in kliknite gumb **OK**.

![Step 3](images/oracle/create_odbc_data_source_step3.png)

Sporočilo o uspehu potrdi, da gonilnik in poverilnice delujejo.
