# Izvorni konektor za Snowflake

Ta vodič opisuje, kako konfigurirati *digna* za povezavo s Snowflake prek **ODBC** z nizom za
povezavo **brez DSN** (DSN-less).

Stran nastavitve *digna* je enaka za vse tehnologije — kje se ustvarjajo povezave, kako se
šifrirajo vrednosti lastnosti, kako se povezava testira in kaj pomenijo načini profiliranja.
Opisana je v [Pregled povezav z bazami podatkov](overview.md). Ta stran zajema, kar je
specifično za Snowflake.

---

## 1. Namestite gonilnik ODBC {: #1-install-the-odbc-driver }

Na računalnik, na katerem teče zaledje *digna*, namestite **Snowflake ODBC Driver** po
[navodilih za namestitev Snowflake](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

Gonilnik se registrira kot **SnowflakeDSIIDriver**. Na svojem gostitelju preberite natančno
registrirano ime, kot je opisano v [Namestite gonilnik ODBC na gostitelja digna](overview.md#install-the-driver).

---

## 2. Lastnosti ODBC {: #2-odbc-properties }

Do Snowflake dostopate s **programmatic access token (PAT)** — to je pot avtentikacije, s
katero je *digna* preverjena, in tista, ki jo Snowflake zahteva za račune, na katerih je
prijava samo z geslom blokirana.

!!! important "Primer, ne specifikacija"

    Spodnji nabor je ena kombinacija, za katero je znano, da deluje. Lastnosti pripadajo
    gonilniku Snowflake ODBC, zato se njihova imena, privzete vrednosti in sprejete vrednosti
    razlikujejo med različicami gonilnika in platformami, katere možnosti avtentikacije vaš
    račun dovoljuje, pa določa varnostna politika računa. Uporabite to kot izhodišče in
    preverite dokumentacijo različice gonilnika, ki ste jo namestili.

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Mora se ujemati z imenom gonilnika, registriranim na gostitelju *digna* |
| `Server` | `<account>.snowflakecomputing.com` | Identifikator računa in pripona, npr. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Uporabnik Snowflake, ki mu pripada žeton |
| `Database` | `TEST` | Baza podatkov, ki vsebuje izvorne sheme. To je edina baza podatkov, ki jo ta povezava lahko profilira |
| `Schema` | `PUBLIC` | Privzeta shema seje |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Izbere avtentikacijo z žetonom |
| `token` | `<programmatic access token>` | Označite **Encrypted** |

Nastali niz za povezavo je videti takole:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Skladišče in vloga

Poizvedbe potrebujejo skladišče (warehouse). Če ima uporabnik *digna* privzeto skladišče in
privzeto vlogo, ju seja prevzame in ničesar ni treba konfigurirati. V nasprotnem primeru
dodajte:

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Skladišče, ki izvaja poizvedbe profiliranja |
| `Role` | `DIGNA_READER` | Vloga, katere dodeljene pravice uporablja seja |

!!! tip "digna dodelite lastno skladišče"

    Ločeno, majhno skladišče s samodejno zaustavitvijo ohranja stroške profiliranja pregledne
    in preprečuje, da bi *digna* z interaktivnimi uporabniki tekmovala za računske vire.

### Avtentikacija z geslom

Kjer račun to še dovoljuje, namesto žetona deluje geslo — odstranite `authenticator` in
`token` ter dodajte:

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `PWD` | `<password>` | Označite **Encrypted** |

---

## 3. Konfiguracija *digna* {: #3-digna-configuration }

Na zaslonu **Add DB Connection** vnesite naslednje:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Opombe o Snowflake {: #4-notes-on-snowflake }

- **Žetoni potečejo.** Programmatic access token se izda z omejeno življenjsko dobo, profiliranje
  pa se ustavi na dan, ko poteče. Ob ustvarjanju si zabeležite datum poteka in novi žeton znova
  vnesite v lastnost `token` — šifrirane vrednosti je mogoče zamenjati, ne pa znova prebrati.
- **Ena povezava vidi eno bazo podatkov.** *digna* ponudi sheme baze podatkov, navedene v
  `Database`, ker Snowflake kot katalog sporoči samo trenutno bazo podatkov. Izvorne tabele v
  drugi bazi podatkov potrebujejo svojo povezavo.
- **Identifikatorji so z velikimi črkami**, razen če so bili ustvarjeni v narekovajih. *digna*
  uporablja imena tako, kot jih sporoči Snowflake.
- **Načini profiliranja.** *Permanent* ustvari delovne tabele v **Work Schema**, zato vloga tam
  potrebuje `CREATE TABLE`. *Session* uporablja `CREATE TEMPORARY TABLE` in se
  **Work Schema** ne dotika. *Standard* potrebuje samo dostop za branje — in sploh nobenih
  pravic za pisanje.

---

## 5. Preverjanje gonilnika (neobvezno) {: #5-verifying-the-driver-optional }

Konfiguriranje vira podatkov ODBC za povezavo brez DSN ni potrebno, vendar je gonilnikovo
lastno pogovorno okno priročen način, da preverite, ali gonilnik, URL računa in vaše
poverilnice delujejo, preden jih vnesete v *digna*.

#### 1. korak
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Opombe:

- Vrednost za **Server** je sestavljena iz identifikatorja vašega računa Snowflake, ki mu sledi
  `.snowflakecomputing.com`.
- **Database**, **Schema** in **Warehouse**, vneseni tukaj, ustrezajo lastnostim `Database`,
  `Schema` in `Warehouse` v [razdelku 2](#2-odbc-properties).

#### 2. korak – Testirajte povezavo

Kliknite gumb **TEST**. Uspešna povezava bi morala biti videti takole:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)