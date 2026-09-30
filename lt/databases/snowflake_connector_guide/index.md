# Snowflake šaltinio jungtis

Šiame vadove aprašyta, kaip sukonfigūruoti *digna* prisijungimą prie Snowflake per **ODBC**,
naudojant ryšio eilutę **be DSN** (DSN-less).

*digna* pusės nustatymas yra vienodas visoms technologijoms — kur kuriami ryšiai, kaip
šifruojamos savybių reikšmės, kaip testuojamas ryšys ir ką reiškia profiliavimo režimai. Tai
aprašyta [Duomenų bazių ryšių apžvalgoje](overview.md). Šiame puslapyje aprašoma tai, kas būdinga
Snowflake.

---

## 1. Įdiekite ODBC tvarkyklę {: #1-install-the-odbc-driver }

Įdiekite **Snowflake ODBC Driver** kompiuteryje, kuriame veikia *digna* backend, laikydamiesi
[Snowflake diegimo vadovo](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

Tvarkyklė užsiregistruoja kaip **SnowflakeDSIIDriver**. Nuskaitykite tikslų užregistruotą
pavadinimą savo serveryje, kaip aprašyta skyriuje [ODBC tvarkyklės diegimas digna serveryje](overview.md#install-the-driver).

---

## 2. ODBC savybės {: #2-odbc-properties }

Prie Snowflake jungiamasi naudojant **programinės prieigos žetoną (PAT, programmatic access
token)** — tai autentifikacijos būdas, su kuriuo *digna* patikrinta, ir būdas, kurio Snowflake
reikalauja paskyrose, kuriose prisijungimas vien slaptažodžiu užblokuotas.

!!! important "Pavyzdys, o ne specifikacija"

    Toliau pateiktas rinkinys yra vienas žinomai veikiantis derinys. Savybės priklauso
    Snowflake ODBC tvarkyklei, todėl jų pavadinimai, numatytosios reikšmės ir priimamos reikšmės
    skiriasi tarp tvarkyklės versijų ir platformų, o tai, kokias autentifikacijos parinktis
    leidžia jūsų paskyra, nulemia paskyros saugumo politika. Naudokite tai kaip atspirties tašką
    ir patikrinkite įdiegtos tvarkyklės versijos dokumentaciją.

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Turi sutapti su tvarkyklės pavadinimu, užregistruotu *digna* serveryje |
| `Server` | `<account>.snowflakecomputing.com` | Paskyros identifikatorius ir priesaga, pvz. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Snowflake vartotojas, kuriam priklauso žetonas |
| `Database` | `TEST` | Duomenų bazė, kurioje yra šaltinio schemos. Tai vienintelė duomenų bazė, kurią šis ryšys gali profiliuoti |
| `Schema` | `PUBLIC` | Numatytoji seanso schema |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Pasirenka autentifikaciją žetonu |
| `token` | `<programmatic access token>` | Pažymėkite **Encrypted** |

Gauta ryšio eilutė atrodo taip:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Warehouse ir rolė

Užklausoms reikia warehouse. Jei *digna* vartotojas turi numatytąjį warehouse ir numatytąją rolę,
seansas juos perima, ir nieko konfigūruoti nereikia. Priešingu atveju pridėkite:

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Warehouse, kuriame vykdomos profiliavimo užklausos |
| `Role` | `DIGNA_READER` | Rolė, kurios teises naudoja seansas |

!!! tip "Skirkite digna atskirą warehouse"

    Atskiras, mažas, automatiškai sustabdomas warehouse leidžia matyti profiliavimo kainą ir
    neleidžia *digna* konkuruoti dėl skaičiavimo išteklių su interaktyviais vartotojais.

### Autentifikacija slaptažodžiu

Kai paskyra tai dar leidžia, vietoje žetono galima naudoti slaptažodį — pašalinkite
`authenticator` ir `token` ir pridėkite:

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `PWD` | `<password>` | Pažymėkite **Encrypted** |

---

## 3. *digna* konfigūracija {: #3-digna-configuration }

Ekrane **Add DB Connection** nurodykite:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Pastabos apie Snowflake {: #4-notes-on-snowflake }

- **Žetonų galiojimas baigiasi.** Programinės prieigos žetonas išduodamas su galiojimo trukme, ir
  profiliavimas sustoja tą dieną, kai jis nustoja galioti. Kurdami žetoną užsirašykite galiojimo
  pabaigos datą ir įveskite naują žetoną savybėje `token` — užšifruotas reikšmes galima pakeisti,
  bet ne perskaityti atgal.
- **Vienas ryšys mato vieną duomenų bazę.** *digna* siūlo `Database` nurodytos duomenų bazės
  schemas, nes Snowflake kaip katalogą praneša tik dabartinę duomenų bazę. Šaltinio lentelėms
  kitoje duomenų bazėje reikia atskiro ryšio.
- **Identifikatoriai rašomi didžiosiomis raidėmis**, nebent jie buvo sukurti kabutėse. *digna*
  naudoja pavadinimus taip, kaip juos praneša Snowflake.
- **Profiliavimo režimai.** *Permanent* kuria darbines lenteles schemoje **Work Schema**, todėl
  rolei ten reikia teisės `CREATE TABLE`. *Session* naudoja `CREATE TEMPORARY TABLE` ir
  **Work Schema** neliečia. *Standard* reikia tik skaitymo prieigos — ir jokių rašymo teisių.

---

## 5. Tvarkyklės patikrinimas (neprivaloma) {: #5-verifying-the-driver-optional }

Ryšiui be DSN ODBC duomenų šaltinio konfigūruoti nereikia, tačiau pačios tvarkyklės dialogo
langas yra patogus būdas patvirtinti, kad tvarkyklė, paskyros URL ir jūsų prisijungimo duomenys
veikia, prieš įvedant juos į *digna*.

#### 1 žingsnis
![1 žingsnis](images/snowflake/create_odbc_data_source_step1.png)

Pastabos:

- Lauko **Server** reikšmę sudaro jūsų Snowflake paskyros identifikatorius, po kurio eina
  `.snowflakecomputing.com`.
- Čia įvesti **Database**, **Schema** ir **Warehouse** atitinka savybes `Database`,
  `Schema` ir `Warehouse` iš [2 skyriaus](#2-odbc-properties).

#### 2 žingsnis – Išbandykite ryšį

Spustelėkite mygtuką **TEST**. Sėkmingas ryšys turėtų atrodyti taip:

![2 žingsnis](images/snowflake/create_odbc_data_source_step2.png)