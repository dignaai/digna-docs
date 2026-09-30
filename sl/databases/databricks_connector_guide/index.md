# Izvorni konektor za Databricks

Ta vodič opisuje, kako konfigurirati *digna* za povezavo z Databricks prek **ODBC** z nizom za
povezavo **brez DSN** (DSN-less).

Stran nastavitve *digna* je enaka za vse tehnologije — kje se ustvarjajo povezave, kako se
šifrirajo vrednosti lastnosti, kako se povezava testira in kaj pomenijo načini profiliranja.
Opisana je v [Pregled povezav z bazami podatkov](overview.md). Ta stran zajema, kar je
specifično za Databricks.

!!! note "Unity Catalog je obvezen"

    *digna* razpoložljive kataloge bere iz `system.information_schema.catalogs`, zato mora imeti
    delovni prostor omogočen Unity Catalog. Prejšnje izdaje *digna* so za delovne prostore brez
    Unity Catalog ponujale ločeno tehnologijo "Databricks Legacy"; ta ni več na voljo.

---

## 1. Namestite gonilnik ODBC {: #1-install-the-odbc-driver }

Na računalnik, na katerem teče zaledje *digna*, namestite **Databricks ODBC Driver** po
[navodilih za namestitev Databricks](https://docs.databricks.com/aws/en/integrations/odbc/).

Glede na različico se gonilnik registrira kot **Simba Spark ODBC Driver** ali kot
**Databricks ODBC Driver**. Na svojem gostitelju preberite natančno registrirano ime, kot je
opisano v [Namestite gonilnik ODBC na gostitelja digna](overview.md#install-the-driver).

---

## 2. Zberite podatke za povezavo {: #2-gather-the-connection-details }

Vse vrednosti prihajajo iz skladišča SQL (SQL warehouse) ali gruče, ki naj jo *digna*
uporablja. Odprite ga v delovnem prostoru Databricks in pojdite na **Connection details**:

| Polje Databricks | Uporabi se kot |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, običajno `443` |
| **HTTP path** | `HTTPPath` |

Za avtentikacijo ustvarite **osebni dostopni žeton** (personal access token) — glejte
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Žetoni pripadajo uporabniku ali service principalu, ta pa potrebuje `USE CATALOG`,
`USE SCHEMA` in `SELECT` na izvornih podatkih.

---

## 3. Lastnosti ODBC {: #3-odbc-properties }

!!! important "Primer, ne specifikacija"

    Spodnji nabor je ena kombinacija, za katero je znano, da deluje. Lastnosti pripadajo
    gonilniku Databricks/Simba, zato se njihova imena, privzete vrednosti in sprejete vrednosti
    razlikujejo med različicami gonilnika — gonilnik je bil večkrat preimenovan, njegove možnosti
    avtentikacije pa razširjene — in med platformami. Uporabite to kot izhodišče in preverite
    dokumentacijo različice gonilnika, ki ste jo namestili.

Na zaslonu **Add DB Connection** dodajte naslednje lastnosti:

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Mora se ujemati z imenom gonilnika, registriranim na gostitelju *digna* |
| `Host` | `<workspace>.cloud.databricks.com` | Server hostname skladišča, npr. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | HTTP path skladišča ali gruče |
| `SSL` | `1` | Končne točke Databricks delujejo samo s TLS |
| `ThriftTransport` | `2` | Transport HTTP, ki ga uporabljajo končne točke SQL |
| `AuthMech` | `3` | Avtentikacija z žetonom |
| `UID` | `token` | Dobesedna beseda `token`, ne uporabniško ime |
| `PWD` | `dapi…` | Osebni dostopni žeton. Označite **Encrypted** |
| `UseNativeQuery` | `1` | SQL iz *digna* posreduje nespremenjen — glejte spodaj |

Nastali niz za povezavo je videti takole:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Ohranite `UseNativeQuery=1`"

    Z `UseNativeQuery=0` — privzeto vrednostjo gonilnika — gonilnik dohodni SQL prepiše v to,
    kar šteje za prenosljivo sintakso ODBC. *digna* že ustvarja Databricks SQL, zato lahko
    prepis spremeni navajanje z obrnjenimi narekovaji (backtick) in datumske literale,
    profiliranje pa nato ne uspe pri stavkih, ki so v izvirni obliki veljavni.

### OAuth namesto žetona

Za service principal z avtentikacijo OAuth machine-to-machine zamenjajte `AuthMech`,
`UID` in `PWD` z:

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Client credentials |
| `Auth_Client_ID` | `<application id>` | Service principal |
| `Auth_Client_Secret` | `<client secret>` | Označite **Encrypted** |

---

## 4. Konfiguracija *digna* {: #4-digna-configuration }

Na zaslonu **Add DB Connection** vnesite naslednje:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Opombe o Databricks {: #5-notes-on-databricks }

- **Skladišče mora teči** ali se mora lahko zagnati, ko se *digna* poveže. Skladišče, ki se
  prebuja iz zaustavljenega stanja, lahko potrebuje več časa, kot znaša časovna omejitev
  povezave — če test ob prvem poskusu po obdobju mirovanja ne uspe, poskusite znova.
- **Katalogi prihajajo iz delovnega prostora.** Za razliko od večine tehnologij ena povezava
  Databricks doseže vsak katalog, ki ga principal sme videti, zato lahko ena sama povezava
  služi virom v več katalogih.
- **Načini profiliranja.** *Permanent* ustvari delovne tabele v **Work Schema** znotraj
  kataloga vira, zato principal tam potrebuje `CREATE TABLE`. *Session* uporablja
  `CREATE TEMPORARY TABLE` in se **Work Schema** ne dotika. *Standard* potrebuje samo dostop za
  branje.
- **Serverless skladišča delujejo** na enak način; razlikuje se samo `HTTPPath`.

---

## 6. Preverjanje gonilnika (neobvezno) {: #6-verifying-the-driver-optional }

Konfiguriranje vira podatkov ODBC za povezavo brez DSN ni potrebno, vendar je gonilnikovo
lastno pogovorno okno priročen način, da preverite, ali gonilnik, skladišče in žeton delujejo,
preden jih vnesete v *digna*.

#### 1. korak
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### 2. korak
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### 3. korak
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### 4. korak
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### 5. korak – Testirajte povezavo

Kliknite gumb **TEST**. Uspešna povezava bi morala biti videti takole:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

Gostitelj, HTTP path in žeton, vneseni tukaj, so natanko vrednosti, ki jih sprejmejo lastnosti v
[razdelku 3](#3-odbc-properties).