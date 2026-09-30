---
title: PostgreSQL jungtis – duomenų bazės integracija | digna dokumentacija
description: Sukonfigūruokite digna prisijungimą prie PostgreSQL per ODBC naudojant ryšio eilutę be DSN. Apima psqlODBC tvarkyklę, reikalingas ODBC savybes, SSL režimus ir digna pusės ryšio nustatymus.
image: /assets/logo_square.png
---


# PostgreSQL šaltinio jungtis

Šiame vadove aprašyta, kaip sukonfigūruoti *digna* prisijungimą prie PostgreSQL per **ODBC**,
naudojant ryšio eilutę **be DSN** (DSN-less).

*digna* pusės nustatymas yra vienodas visoms technologijoms — kur kuriami ryšiai, kaip
šifruojamos savybių reikšmės, kaip testuojamas ryšys ir ką reiškia profiliavimo režimai. Tai
aprašyta [Duomenų bazių ryšių apžvalgoje](overview.md). Šiame puslapyje aprašoma tai, kas būdinga
PostgreSQL.

---

## 1. Įdiekite ODBC tvarkyklę {: #1-install-the-odbc-driver }

Įdiekite PostgreSQL ODBC tvarkyklę (**psqlODBC**) kompiuteryje, kuriame veikia *digna* backend,
laikydamiesi oficialaus gamintojo diegimo vadovo.

Tvarkyklė užsiregistruoja pavadinimu, kuris skiriasi priklausomai nuo platformos ir paketo —
dažniausiai **PostgreSQL Unicode(x64)** Windows sistemoje ir **PostgreSQL ODBC Driver(UNICODE)**
Linux sistemoje. Nuskaitykite tikslų pavadinimą savo serveryje, kaip aprašyta skyriuje
[ODBC tvarkyklės diegimas digna serveryje](overview.md#install-the-driver), ir naudokite jį
toliau nurodytai savybei `DRIVER`.

---

## 2. ODBC savybės {: #2-odbc-properties }

!!! important "Pavyzdys, o ne specifikacija"

    Toliau pateiktas rinkinys yra vienas žinomai veikiantis derinys. Savybės priklauso
    psqlODBC tvarkyklei, todėl jų pavadinimai, numatytosios reikšmės ir priimamos reikšmės
    skiriasi tarp tvarkyklės versijų ir platformų, o tai, ko reikalauja jūsų serveris — ypač
    SSL, — taip pat gali skirtis. Naudokite tai kaip atspirties tašką ir patikrinkite įdiegtos
    tvarkyklės versijos dokumentaciją.

Ekrane **Add DB Connection** pridėkite šias savybes:

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Turi sutapti su tvarkyklės pavadinimu, užregistruotu *digna* serveryje |
| `SERVER` | `db.example.com` | Serverio pavadinimas arba IP adresas |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Duomenų bazė, kurioje yra šaltinio schemos. Tai vienintelė duomenų bazė, kurią šis ryšys gali profiliuoti |
| `UID` | `digna_source_user` | Duomenų bazės vartotojas |
| `PWD` | `<password>` | Pažymėkite **Encrypted** |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` arba `verify-full` — serveris turi jį priimti |

Gauta ryšio eilutė atrodo taip:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Bet kurią kitą psqlODBC parinktį galima pridėti kaip papildomą savybę — pavyzdžiui,
`ReadOnly=1` tik skaitymo seansui arba `ConnSettings`, kad prisijungiant būtų vykdomi `SET`
sakiniai.

---

## 3. *digna* konfigūracija {: #3-digna-configuration }

Ekrane **Add DB Connection** nurodykite:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Pastabos apie PostgreSQL {: #4-notes-on-postgresql }

- **`SSLMode` turi atitikti serverį.** Serveris, sukonfigūruotas su `hostssl`, atmeta
  `SSLMode=disable`, o `verify-ca` ar `verify-full` papildomai reikalauja, kad šakninis
  sertifikatas būtų prieinamas tvarkyklei *digna* serveryje. Jei testuodami tvarkyklę turėjote
  pasirinkti konkretų režimą, naudokite tą patį ir čia.
- **Vienas ryšys mato vieną duomenų bazę.** *digna* siūlo `DATABASE` nurodytos duomenų bazės
  schemas, nes PostgreSQL kaip katalogą praneša tik dabartinę duomenų bazę. Šaltinio lentelėms
  kitoje duomenų bazėje reikia atskiro ryšio.
- **Profiliavimo režimai.** *Permanent* kuria darbines lenteles schemoje **Work Schema**, todėl
  vartotojui reikia teisės `CREATE` šiai schemai. *Session* naudoja `CREATE TEMPORARY TABLE` ir
  **Work Schema** neliečia. *Standard* reikia tik skaitymo prieigos.

---

## 5. Tvarkyklės patikrinimas (neprivaloma) {: #5-verifying-the-driver-optional }

Ryšiui be DSN ODBC duomenų šaltinio konfigūruoti nereikia, tačiau pačios tvarkyklės dialogo
langas yra patogus būdas patvirtinti, kad tvarkyklė veikia, o serveris priima jūsų prisijungimo
duomenis ir SSL režimą, prieš įvedant juos į *digna*.

#### 1 žingsnis
![1 žingsnis](images/postgres/create_odbc_data_source_step1.png)

#### 2 žingsnis – Išbandykite ryšį

Spustelėkite mygtuką **Test Connection**.

![2 žingsnis](images/postgres/create_odbc_data_source_step2.png)

Čia įvestos reikšmės yra būtent tos reikšmės, kurias priima savybės iš
[2 skyriaus](#2-odbc-properties).
