---
title: MS SQL Server jungtis – duomenų bazės integracija | digna dokumentacija
description: Sukonfigūruokite digna prisijungimą prie Microsoft SQL Server per ODBC naudojant ryšio eilutę be DSN. Apima Microsoft ODBC tvarkyklę, reikalingas ODBC savybes, šifravimo nustatymus ir digna pusės ryšio nustatymus.
image: /assets/logo_square.png
---


# MS SQL Server šaltinio jungtis

Šiame vadove aprašyta, kaip sukonfigūruoti *digna* prisijungimą prie Microsoft SQL Server per
**ODBC**, naudojant ryšio eilutę **be DSN** (DSN-less).

*digna* pusės nustatymas yra vienodas visoms technologijoms — kur kuriami ryšiai, kaip
šifruojamos savybių reikšmės, kaip testuojamas ryšys ir ką reiškia profiliavimo režimai. Tai
aprašyta [Duomenų bazių ryšių apžvalgoje](overview.md). Šiame puslapyje aprašoma tai, kas būdinga
SQL Server.

!!! note "Azure Synapse Analytics"

    Synapse taip pat konfigūruojamas kaip SQL Server ryšys, tik su kitu serverio pavadinimu ir
    keliais papildomais aspektais — žr. [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Įdiekite ODBC tvarkyklę {: #1-install-the-odbc-driver }

Įdiekite **ODBC Driver 18 for SQL Server** kompiuteryje, kuriame veikia *digna* backend,
laikydamiesi [Microsoft diegimo vadovo](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

Kartu su Windows pateikiama tvarkyklė paprastu pavadinimu **SQL Server** taip pat veikia, tačiau
ji seniai pasenusi ir nepalaiko nei šiuolaikinių TLS nustatymų, nei Azure autentifikacijos.
Naudokite ją tik tada, kai dabartinės tvarkyklės įdiegti neįmanoma.

Nuskaitykite tikslų užregistruotos tvarkyklės pavadinimą savo serveryje, kaip aprašyta skyriuje
[ODBC tvarkyklės diegimas digna serveryje](overview.md#install-the-driver).

---

## 2. ODBC savybės {: #2-odbc-properties }

!!! important "Pavyzdys, o ne specifikacija"

    Toliau pateiktas rinkinys yra vienas žinomai veikiantis derinys. Savybės priklauso
    Microsoft ODBC tvarkyklei, todėl jų pavadinimai, numatytosios reikšmės ir priimamos reikšmės
    skiriasi tarp tvarkyklės versijų — pavyzdžiui, Driver 18 pagal nutylėjimą šifruoja, o
    Driver 17 to nedarė — ir tarp platformų. Naudokite tai kaip atspirties tašką ir patikrinkite
    įdiegtos tvarkyklės versijos dokumentaciją.

Ekrane **Add DB Connection** pridėkite šias savybes:

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Turi sutapti su tvarkyklės pavadinimu, užregistruotu *digna* serveryje |
| `SERVER` | `sql.example.com` | Serverio pavadinimas arba IP adresas. Pavadintiems egzemplioriams: `host\instance`; nestandartiniam prievadui: `host,1433` |
| `PORT` | `1433` | Praleiskite, kai prievadas jau yra `SERVER` dalis |
| `DATABASE` | `digna_source_db` | Duomenų bazė, kurioje yra šaltinio schemos. Tai vienintelė duomenų bazė, kurią šis ryšys gali profiliuoti |
| `UID` | `digna_source_user` | Duomenų bazės vartotojas |
| `PWD` | `<password>` | Pažymėkite **Encrypted** |

Gauta ryšio eilutė atrodo taip:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Šifravimas su ODBC Driver 18

Driver 18 pagal nutylėjimą šifruoja ryšius ir tikrina serverio sertifikatą. Jungiantis prie
serverio, kurio sertifikatu jūsų *digna* serveris nepasitiki — paprastai savarankiškai pasirašyto
sertifikato, — prisijungimas nepavyksta su sertifikatų grandinės klaida. Pridėkite:

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `Encrypt` | `yes` | Numatytoji reikšmė Driver 18; nustatykite `no` tik tada, jei serveris nepalaiko TLS |
| `TrustServerCertificate` | `yes` | Praleidžia sertifikato tikrinimą. Patogu testavimo aplinkose; gamybinėje aplinkoje verčiau įdiekite sertifikatą |

### Windows autentifikacija

Norėdami jungtis paskyra, kuria veikia *digna* paslauga, o ne SQL prisijungimu, pašalinkite
`UID` ir `PWD` ir pridėkite:

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `Trusted_Connection` | `yes` | *digna* paslaugos paskyrai reikia duomenų bazės teisių |

---

## 3. *digna* konfigūracija {: #3-digna-configuration }

Ekrane **Add DB Connection** nurodykite:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Pastabos apie MS SQL Server {: #4-notes-on-ms-sql-server }

- **Vienas ryšys mato vieną duomenų bazę.** *digna* siūlo `DATABASE` nurodytos duomenų bazės
  schemas, nes SQL Server kaip katalogą praneša tik dabartinę duomenų bazę. Šaltinio lentelėms
  kitoje duomenų bazėje reikia atskiro ryšio.
- **Profiliavimo režimai.** *Permanent* kuria darbines lenteles schemoje **Work Schema**, todėl
  vartotojui ten reikia teisės `CREATE TABLE`. *Session* naudoja vietines laikinąsias lenteles
  (`#wt_…`) duomenų bazėje `tempdb` ir **Work Schema** neliečia. *Standard* reikia tik skaitymo
  prieigos.
- **`SERVER` nurodo egzempliorių ir prievadą.** Naudojant pavadintą egzempliorių, `host\instance`
  reikalauja, kad būtų pasiekiama paslauga SQL Server Browser; `host,port` to išvengia.

---

## 5. Tvarkyklės patikrinimas (neprivaloma) {: #5-verifying-the-driver-optional }

Ryšiui be DSN ODBC duomenų šaltinio konfigūruoti nereikia, tačiau pačios tvarkyklės vedlys yra
patogus būdas patvirtinti, kad tvarkyklė veikia ir kad serveris priima jūsų prisijungimo
duomenis, prieš įvedant juos į *digna*.

#### 1 žingsnis
![1 žingsnis](images/sqlserver/create_odbc_data_source_step1.png)

Spustelėkite mygtuką **Next >**.

#### 2 žingsnis
![2 žingsnis](images/sqlserver/create_odbc_data_source_step2.png)

Pasirinkite autentifikacijos metodą (pvz., vartotojo vardas ir slaptažodis)
ir pateikite reikiamus duomenis.

Spustelėkite mygtuką **Next >**.

#### 3 žingsnis
![3 žingsnis](images/sqlserver/create_odbc_data_source_step3.png)

Pasirinkite ANSI atitinkančius nustatymus ir spustelėkite mygtuką **Next >**.

#### 4 žingsnis
![4 žingsnis](images/sqlserver/create_odbc_data_source_step4.png)

Galite palikti numatytuosius nustatymus arba pasirinkti reikiamas žurnalo (logging) parinktis
ir spustelėti mygtuką **Finish**.

#### 5 žingsnis
![5 žingsnis](images/sqlserver/create_odbc_data_source_step5.png)

Dabar spustelėkite mygtuką **Test datasource**.

#### 6 žingsnis
![6 žingsnis](images/sqlserver/create_odbc_data_source_step6.png)

Sėkmės ekranas patvirtina, kad tvarkyklė ir prisijungimo duomenys veikia. Įvestos reikšmės yra
būtent tos reikšmės, kurias priima savybės iš [2 skyriaus](#2-odbc-properties).
