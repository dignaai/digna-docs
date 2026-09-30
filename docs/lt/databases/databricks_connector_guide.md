---
title: Databricks jungtis – duomenų bazės integracija | digna dokumentacija
description: Sukonfigūruokite digna prisijungimą prie Databricks su Unity Catalog per ODBC naudojant ryšio eilutę be DSN. Apima Databricks ODBC tvarkyklę, asmeninius prieigos žetonus, HTTP kelią ir digna pusės ryšio nustatymus.
image: /assets/logo_square.png
---

# Databricks šaltinio jungtis

Šiame vadove aprašyta, kaip sukonfigūruoti *digna* prisijungimą prie Databricks per **ODBC**,
naudojant ryšio eilutę **be DSN** (DSN-less).

*digna* pusės nustatymas yra vienodas visoms technologijoms — kur kuriami ryšiai, kaip
šifruojamos savybių reikšmės, kaip testuojamas ryšys ir ką reiškia profiliavimo režimai. Tai
aprašyta [Duomenų bazių ryšių apžvalgoje](overview.md). Šiame puslapyje aprašoma tai, kas būdinga
Databricks.

!!! note "Būtinas Unity Catalog"

    *digna* prieinamus katalogus nuskaito iš `system.information_schema.catalogs`, todėl darbo
    sritis (workspace) turi turėti įjungtą Unity Catalog. Ankstesnės *digna* versijos siūlė
    atskirą „Databricks Legacy“ technologiją darbo sritims be Unity Catalog; ji nebėra prieinama.

---

## 1. Įdiekite ODBC tvarkyklę {: #1-install-the-odbc-driver }

Įdiekite **Databricks ODBC Driver** kompiuteryje, kuriame veikia *digna* backend, laikydamiesi
[Databricks diegimo vadovo](https://docs.databricks.com/aws/en/integrations/odbc/).

Priklausomai nuo versijos, tvarkyklė užsiregistruoja kaip **Simba Spark ODBC Driver** arba kaip
**Databricks ODBC Driver**. Nuskaitykite tikslų užregistruotą pavadinimą savo serveryje, kaip
aprašyta skyriuje [ODBC tvarkyklės diegimas digna serveryje](overview.md#install-the-driver).

---

## 2. Surinkite ryšio duomenis {: #2-gather-the-connection-details }

Visos reikšmės paimamos iš SQL warehouse (arba klasterio), kurį turi naudoti *digna*. Atidarykite
jį Databricks darbo srityje ir eikite į **Connection details**:

| Databricks laukas | Naudojamas kaip |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, paprastai `443` |
| **HTTP path** | `HTTPPath` |

Autentifikacijai sukurkite **asmeninį prieigos žetoną** (personal access token) — žr.
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Žetonai priklauso vartotojui arba paslaugos subjektui (service principal), ir tam subjektui
šaltinio duomenims reikia teisių `USE CATALOG`, `USE SCHEMA` ir `SELECT`.

---

## 3. ODBC savybės {: #3-odbc-properties }

!!! important "Pavyzdys, o ne specifikacija"

    Toliau pateiktas rinkinys yra vienas žinomai veikiantis derinys. Savybės priklauso
    Databricks/Simba tvarkyklei, todėl jų pavadinimai, numatytosios reikšmės ir priimamos
    reikšmės skiriasi tarp tvarkyklės versijų — tvarkyklė ne kartą buvo pervadinta, o jos
    autentifikacijos parinktys išplėstos — ir tarp platformų. Naudokite tai kaip atspirties
    tašką ir patikrinkite įdiegtos tvarkyklės versijos dokumentaciją.

Ekrane **Add DB Connection** pridėkite šias savybes:

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Turi sutapti su tvarkyklės pavadinimu, užregistruotu *digna* serveryje |
| `Host` | `<workspace>.cloud.databricks.com` | Warehouse serverio pavadinimas, pvz. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | Warehouse arba klasterio HTTP kelias |
| `SSL` | `1` | Databricks galiniai taškai veikia tik per TLS |
| `ThriftTransport` | `2` | HTTP transportas, kurį naudoja SQL galiniai taškai |
| `AuthMech` | `3` | Autentifikacija žetonu |
| `UID` | `token` | Pažodžiui žodis `token`, o ne vartotojo vardas |
| `PWD` | `dapi…` | Asmeninis prieigos žetonas. Pažymėkite **Encrypted** |
| `UseNativeQuery` | `1` | Perduoda *digna* SQL nepakeistą — žr. toliau |

Gauta ryšio eilutė atrodo taip:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Palikite `UseNativeQuery=1`"

    Esant `UseNativeQuery=0` — tvarkyklės numatytajai reikšmei — tvarkyklė perrašo gaunamą SQL
    į, jos manymu, perkeliamą ODBC sintaksę. *digna* jau generuoja Databricks SQL, todėl
    perrašymas gali pakeisti kabučių (backtick) naudojimą ir datų literalus, ir tada
    profiliavimas nepavyksta su sakiniais, kurie parašyti yra teisingi.

### OAuth vietoje žetono

Paslaugos subjektui su OAuth mašina–mašina (machine-to-machine) autentifikacija pakeiskite
`AuthMech`, `UID` ir `PWD` šiomis savybėmis:

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Kliento kredencialai (client credentials) |
| `Auth_Client_ID` | `<application id>` | Paslaugos subjektas |
| `Auth_Client_Secret` | `<client secret>` | Pažymėkite **Encrypted** |

---

## 4. *digna* konfigūracija {: #4-digna-configuration }

Ekrane **Add DB Connection** nurodykite:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Pastabos apie Databricks {: #5-notes-on-databricks }

- **Warehouse turi veikti** arba galėti pasileisti, kai *digna* jungiasi. Warehouse, kuris
  atsibunda iš sustabdytos būsenos, gali užtrukti ilgiau nei ryšio laiko limitas — jei testas
  nepavyksta pirmu bandymu po neveiklumo laikotarpio, bandykite dar kartą.
- **Katalogai paimami iš darbo srities.** Skirtingai nei daugumoje technologijų, vienas
  Databricks ryšys pasiekia visus katalogus, kuriuos subjektui leidžiama matyti, todėl vienas
  ryšys gali aptarnauti šaltinius keliuose kataloguose.
- **Profiliavimo režimai.** *Permanent* kuria darbines lenteles schemoje **Work Schema** šaltinio
  kataloge, todėl subjektui ten reikia teisės `CREATE TABLE`. *Session* naudoja
  `CREATE TEMPORARY TABLE` ir **Work Schema** neliečia. *Standard* reikia tik skaitymo prieigos.
- **Serverless warehouse veikia** tokiu pat būdu; skiriasi tik `HTTPPath`.

---

## 6. Tvarkyklės patikrinimas (neprivaloma) {: #6-verifying-the-driver-optional }

Ryšiui be DSN ODBC duomenų šaltinio konfigūruoti nereikia, tačiau pačios tvarkyklės dialogo
langas yra patogus būdas patvirtinti, kad tvarkyklė, warehouse ir žetonas veikia, prieš įvedant
juos į *digna*.

#### 1 žingsnis
![1 žingsnis](images/databricks/create_odbc_data_source_step1.png)

#### 2 žingsnis
![2 žingsnis](images/databricks/create_odbc_data_source_step2.png)

#### 3 žingsnis
![3 žingsnis](images/databricks/create_odbc_data_source_step3.png)

#### 4 žingsnis
![4 žingsnis](images/databricks/create_odbc_data_source_step4.png)

#### 5 žingsnis – Išbandykite ryšį

Spustelėkite mygtuką **TEST**. Sėkmingas ryšys turėtų atrodyti taip:

![5 žingsnis](images/databricks/create_odbc_data_source_step5.png)

Čia įvesti serveris, HTTP kelias ir žetonas yra būtent tos reikšmės, kurias priima savybės iš
[3 skyriaus](#3-odbc-properties).
