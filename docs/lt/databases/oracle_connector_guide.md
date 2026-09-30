---
title: Oracle jungtis – duomenų bazės integracija | digna dokumentacija
description: Sukonfigūruokite digna prisijungimą prie Oracle per ODBC naudojant ryšio eilutę be DSN. Apima Oracle ODBC tvarkyklę, DBQ prisijungimo aprašą, TNS pseudonimus ir digna pusės ryšio nustatymus.
image: /assets/logo_square.png
---


# Oracle šaltinio jungtis

Šiame vadove aprašyta, kaip sukonfigūruoti *digna* prisijungimą prie Oracle Database per **ODBC**,
naudojant ryšio eilutę **be DSN** (DSN-less).

*digna* pusės nustatymas yra vienodas visoms technologijoms — kur kuriami ryšiai, kaip
šifruojamos savybių reikšmės, kaip testuojamas ryšys ir ką reiškia profiliavimo režimai. Tai
aprašyta [Duomenų bazių ryšių apžvalgoje](overview.md). Šiame puslapyje aprašoma tai, kas būdinga
Oracle.

---

## 1. Įdiekite ODBC tvarkyklę {: #1-install-the-odbc-driver }

Oracle ODBC tvarkyklė yra **Oracle Client** dalis (pakanka Instant Client „ODBC“ paketo).
Įdiekite ją kompiuteryje, kuriame veikia *digna* backend, laikydamiesi oficialaus gamintojo
diegimo vadovo.

Tvarkyklė užsiregistruoja kaip **Oracle in `<OracleHomeName>`** — pavyzdžiui,
`Oracle in OraDB21Home1` arba `Oracle in instantclient_21_13`. Oracle home pavadinimas kiekviename
diegime skiriasi, todėl nuskaitykite tikslų pavadinimą savo serveryje, kaip aprašyta skyriuje
[ODBC tvarkyklės diegimas digna serveryje](overview.md#install-the-driver).

---

## 2. ODBC savybės {: #2-odbc-properties }

!!! important "Pavyzdys, o ne specifikacija"

    Toliau pateiktas rinkinys yra vienas žinomai veikiantis derinys. Savybės priklauso Oracle
    ODBC tvarkyklei, todėl jų pavadinimai, numatytosios reikšmės ir priimamos reikšmės skiriasi
    tarp kliento versijų, o ypač tvarkyklės pavadinimas priklauso nuo Oracle home jūsų serveryje.
    Naudokite tai kaip atspirties tašką ir patikrinkite įdiegtos kliento versijos dokumentaciją.

Ekrane **Add DB Connection** pridėkite šias savybes:

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Turi sutapti su tvarkyklės pavadinimu, užregistruotu *digna* serveryje |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Duomenų bazė, prie kurios jungiamasi — žr. toliau |
| `UID` | `DIGNA_SOURCE_USER` | Duomenų bazės vartotojas |
| `PWD` | `<password>` | Pažymėkite **Encrypted** |

Gauta ryšio eilutė atrodo taip:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### Reikšmė `DBQ`

`DBQ` priima tris formas. *digna* jos lygiavertės; jos skiriasi tuo, ką reikia sukonfigūruoti
*digna* serveryje:

| Forma | Pavyzdys | Reikalauja |
|---|---|---|
| **Pilnas prisijungimo aprašas** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Nieko — viskas yra savybėje. Rekomenduojama |
| **TNS pseudonimas** | `DIGNA_SOURCE` | Pseudonimas turi būti apibrėžtas *digna* serverio Oracle Client faile `tnsnames.ora` |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Oracle Client, palaikantis Easy Connect (12c ir naujesni) |

!!! tip "Rinkitės pilną aprašą"

    TNS pseudonimas perkelia pusę ryšio apibrėžimo į failą *digna* serveryje, kur jį lengva
    pamiršti, kai serveris perkuriamas ar *digna* perkeliama. Pilnas aprašas išlaiko ryšį
    savarankišką — o tai ir yra nustatymo be DSN esmė.

Atkreipkite dėmesį, kad skliaustai apraše ryšio eilutėje netrukdo, tačiau jei jūsų slaptažodyje
yra `;`, apgaubkite jį riestiniais skliaustais: `PWD={p@ss;word}`.

---

## 3. *digna* konfigūracija {: #3-digna-configuration }

Ekrane **Add DB Connection** nurodykite:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Pastabos apie Oracle {: #4-notes-on-oracle }

- **Schemos yra vartotojai.** *digna* Oracle vartotojus išvardija kaip schemas, todėl šaltinio
  schema yra lentelių savininkas — aukščiau pateiktame pavyzdyje `DIGNA_SOURCE_USER`. Ryšio
  vartotojui reikia teisės `SELECT` šioms lentelėms tiesiogiai arba per rolę.
- **Vienas ryšys mato vieną duomenų bazę.** Katalogas, kurį siūlo *digna*, yra duomenų bazė, prie
  kurios prijungtas ryšys, todėl `DBQ` nulemia, kuri paslauga, o kartu ir kuri duomenų bazė, yra
  profiliuojama.
- **Identifikatoriai kabutėse skiria didžiąsias ir mažąsias raides.** *digna* rašo kabutėse
  pavadinimus, kuriuos nuskaito iš duomenų žodyno, t. y. tai, ką saugo Oracle — objektams be
  kabučių didžiosiomis raidėmis.
- **Profiliavimo režimai.** *Permanent* kuria darbines lenteles schemoje **Work Schema**, todėl
  vartotojui ten reikia teisės `CREATE TABLE` ir kvotos lentelių erdvėje (tablespace). *Session*
  naudoja privačią laikinąją lentelę (`ORA$PTT_…`, Oracle 18c ir naujesni) ir **Work Schema**
  neliečia. *Standard* reikia tik skaitymo prieigos.

---

## 5. Tvarkyklės patikrinimas (neprivaloma) {: #5-verifying-the-driver-optional }

Ryšiui be DSN ODBC duomenų šaltinio konfigūruoti nereikia, tačiau pačios tvarkyklės dialogo
langas yra patogus būdas patvirtinti, kad Oracle Client, paslaugos pavadinimas ir jūsų
prisijungimo duomenys veikia, prieš įvedant juos į *digna*.

#### 1 žingsnis
![1 žingsnis](images/oracle/create_odbc_data_source_step1.png)

Čia siūlomas **TNS Service Name** paimamas iš jūsų Oracle Client diegimo failo `tnsnames.ora` —
būtent ten apibrėžiamas pseudonimas, o kartu ir serveris, prievadas bei paslaugos pavadinimas.
*digna* galite naudoti pseudonimą kaip `DBQ` arba vietoje jo pilną aprašą.

#### 2 žingsnis – Išbandykite ryšį

Spustelėkite mygtuką **Test Connection**.

![2 žingsnis](images/oracle/create_odbc_data_source_step2.png)

Įveskite slaptažodį ir spustelėkite mygtuką **OK**.

![3 žingsnis](images/oracle/create_odbc_data_source_step3.png)

Sėkmės pranešimas patvirtina, kad tvarkyklė ir prisijungimo duomenys veikia.
