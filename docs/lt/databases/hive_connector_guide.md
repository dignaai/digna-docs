---
title: Apache Hive jungtis – duomenų bazės integracija | digna dokumentacija
description: Sukonfigūruokite digna prisijungimą prie Apache Hive per ODBC naudojant ryšio eilutę be DSN. Apima Cloudera Hive ODBC tvarkyklę, autentifikacijos mechanizmus, transporto režimus ir digna pusės ryšio nustatymus.
image: /assets/logo_square.png
---


# Hive šaltinio jungtis

Šiame vadove aprašyta, kaip sukonfigūruoti *digna* prisijungimą prie Apache Hive per **ODBC**,
naudojant ryšio eilutę **be DSN** (DSN-less).

*digna* pusės nustatymas yra vienodas visoms technologijoms — kur kuriami ryšiai, kaip
šifruojamos savybių reikšmės, kaip testuojamas ryšys ir ką reiškia profiliavimo režimai. Tai
aprašyta [Duomenų bazių ryšių apžvalgoje](overview.md). Šiame puslapyje aprašoma tai, kas būdinga
Hive.

---

## 1. Įdiekite ODBC tvarkyklę {: #1-install-the-odbc-driver }

Įdiekite **Cloudera ODBC Driver for Apache Hive** kompiuteryje, kuriame veikia *digna* backend,
laikydamiesi oficialaus gamintojo diegimo vadovo.

Nuskaitykite tikslų užregistruotos tvarkyklės pavadinimą savo serveryje, kaip aprašyta skyriuje
[ODBC tvarkyklės diegimas digna serveryje](overview.md#install-the-driver).

---

## 2. ODBC savybės {: #2-odbc-properties }

!!! important "Pavyzdys, o ne specifikacija"

    Toliau pateiktas rinkinys yra vienas žinomai veikiantis derinys. Savybės priklauso
    Cloudera Hive tvarkyklei, todėl jų pavadinimai, numatytosios reikšmės ir priimamos reikšmės
    skiriasi tarp tvarkyklės versijų ir platformų, o tai, ką priima HiveServer2, visiškai
    priklauso nuo to, kaip apsaugotas klasteris — autentifikacijos mechanizmo, transporto
    režimo, TLS, šliuzo. Naudokite tai kaip atspirties tašką ir patikrinkite įdiegtos tvarkyklės
    versijos dokumentaciją.

Ekrane **Add DB Connection** pridėkite šias savybes:

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Turi sutapti su tvarkyklės pavadinimu, užregistruotu *digna* serveryje |
| `HOST` | `hive.example.com` | HiveServer2 serverio pavadinimas arba IP adresas |
| `PORT` | `10000` | HiveServer2 prievadas; `10001` HTTP transportui |

Gauta ryšio eilutė atrodo taip:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Autentifikacija

Neapsaugotas HiveServer2 priima tris aukščiau nurodytas savybes tokias, kokios jos yra. Kai
autentifikacija įjungta, pridėkite:

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `AuthMech` | `3` | `0` be autentifikacijos, `2` tik vartotojo vardas, `3` vartotojo vardas ir slaptažodis, `1` Kerberos |
| `UID` | `digna_source_user` | Būtina, kai `AuthMech` yra `2` ir `3` |
| `PWD` | `<password>` | Būtina, kai `AuthMech` yra `3`. Pažymėkite **Encrypted** |

Naudojant Kerberos (`AuthMech=1`), *digna* serveriui papildomai reikia galiojančio bilieto
(ticket) arba keytab, taip pat tvarkyklės dokumentacijoje aprašytų savybių `KrbHostFQDN`,
`KrbServiceName` ir `KrbRealm`.

### Transportas ir TLS

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `ThriftTransport` | `2` | `0` dvejetainis (numatytasis, prievadas 10000), `1` SASL, `2` HTTP (prievadas 10001, ir tai, ko tikisi Knox šliuzas) |
| `HTTPPath` | `cliservice` | Su `ThriftTransport=2` |
| `SSL` | `1` | Kai HiveServer2 apsaugotas TLS |
| `Schema` | `dignadata` | Hive duomenų bazė, kurioje pradedamas seansas. Neprivaloma — *digna* savo užklausose nurodo pilnus pavadinimus |

---

## 3. *digna* konfigūracija {: #3-digna-configuration }

Ekrane **Add DB Connection** nurodykite:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Pastabos apie Hive {: #4-notes-on-hive }

- **Katalogus pateikia tvarkyklė.** Hive neturi savo katalogo, todėl *digna* paima tai, ką
  praneša tvarkyklė — paprastai vieną įrašą pavadinimu `HIVE` — ir po juo išvardija Hive
  duomenų bazes kaip schemas.
- **Work Schema yra Hive duomenų bazė.** *Permanent* profiliavimui vartotojui reikia teisės kurti
  ir šalinti joje lenteles, o pagrindinė saugojimo vieta turi būti įrašoma.
- **Profiliavimo režimai.** *Permanent* kuria darbines lenteles schemoje **Work Schema**. *Session*
  naudoja `CREATE TEMPORARY TABLE`, kuriam reikia laikinąsias lenteles palaikančio HiveServer2,
  ir **Work Schema** neliečia. *Standard* reikia tik skaitymo prieigos, ir šį režimą verta rinktis
  klasteryje, kuriame *digna* visai neturi rašymo prieigos.
- **Profiliavimas yra užklausų rinkinys, o ne skenavimas.** Kiekvieną statistiką apskaičiuoja
  HiveServer2, todėl eilė, į kurią siunčia *digna* vartotojas, turėtų turėti pakankamai pajėgumų
  inspekcijos laikotarpiui.

---

## 5. Tvarkyklės patikrinimas (neprivaloma) {: #5-verifying-the-driver-optional }

Ryšiui be DSN ODBC duomenų šaltinio konfigūruoti nereikia, tačiau pačios tvarkyklės dialogo
langas yra patogus būdas patvirtinti, kad tvarkyklė, transporto režimas ir jūsų prisijungimo
duomenys veikia, prieš įvedant juos į *digna*.

#### 1 žingsnis
![1 žingsnis](images/hive/create_odbc_data_source_step1.png)

Čia esantys laukai **Host**, **Port**, **Database**, **Mechanism** ir **Thrift Transport** atitinka
savybes `HOST`, `PORT`, `Schema`, `AuthMech` ir `ThriftTransport` iš
[2 skyriaus](#2-odbc-properties).

#### 2 žingsnis – Išbandykite ryšį

Įveskite slaptažodį ir spustelėkite mygtuką **Test**.

![2 žingsnis](images/hive/create_odbc_data_source_step2.png)

Po sėkmingo testo spustelėkite mygtuką **OK**.
