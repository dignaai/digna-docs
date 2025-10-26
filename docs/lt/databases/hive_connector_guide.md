---
title: Apache Hive jungtis – Duomenų bazės integracija | digna dokumentacija
description: Konfigūruokite digna prisijungimui prie Apache Hive naudojant gimtąjį PyHive tvarkyklę arba Cloudera ODBC tvarkyklę. Palaikomas autentifikavimas slaptažodžiu ir DSN arba be DSN nustatymai.
image: /assets/logo_square.png
---


# Šaltinio jungtis Hive

Šiame vadove aprašyta, kaip konfigūruoti *digna* prisijungimui prie Hive naudojant arba gimtąją Python jungtį, arba ODBC tvarkyklę.

Jis nurodo ekraną **"Create a Database Connection"**.

![Sukurti duomenų bazės ryšį](images/data_source_config_input_mask.png)

---

## Gimtasis Python tvarkyklė

**Biblioteka:** `PyHive`  
**Palaikomas autentifikavimas:** Tik slaptažodžiu pagrįstas autentifikavimas

> ⚠️ Kitų autentifikavimo metodų atveju naudokite ODBC tvarkyklę.

### *digna* konfigūracija (gimtasis tvarkyklė)

Pateikite šią informaciją ekrane **"Create a Database Connection"**:

```
Technologija:     Apache Hive
Serverio adresas: Serverio pavadinimas arba IP adresas
Portas:           Porto numeris, pvz. 10000
Duomenų bazės pavadinimas: Schema, kurioje yra šaltinio duomenys
Schemos pavadinimas:      Schema, kurioje yra šaltinio duomenys
Vartotojo vardas:        Duomenų bazės vartotojo vardas
Vartotojo slaptažodis:   Vartotojo slaptažodis
Naudoti ODBC:     Išjungta (numatyta)
```

---

## ODBC tvarkyklė

ODBC tvarkyklė gali palaikyti platesnį autentifikavimo ir ryšio parinkčių spektrą. Šiame skyriuje dėmesys skiriamas autentifikavimui slaptažodžiu naudojant tvarkyklę **Cloudera ODBC Driver for Apache Hive**.

### 1. Įdiekite ODBC tvarkyklę

Įdiekite **Cloudera ODBC Driver for Apache Hive** (ar panašią) vadovaudamiesi tiekėjo oficialiu diegimo vadovu.

### 2. Konfigūruokite ODBC duomenų šaltinį

Atlikite šiuos veiksmus, kad sukonfigūruotumėte naują ODBC duomenų šaltinį, naudojant autentifikavimą slaptažodžiu:

#### Žingsnis 1
![Žingsnis 1](images/hive/create_odbc_data_source_step1.png)


#### Žingsnis 2 – Patikrinkite ryšį

Įveskite slaptažodį ir spauskite mygtuką **Test**.

![Žingsnis 2](images/hive/create_odbc_data_source_step2.png)

Po sėkmingo testo spauskite mygtuką **OK**.

---

Dabar galite sukonfigūruoti *digna* naudoti ODBC ryšį arba su **DSN (Data Source Name)**, arba be **DSN**.

---

### A. Konfigūracija su DSN

#### *digna* konfigūracija

Ekrane **"Create a Database Connection"** pateikite šią informaciją:

```
Technologija:     Apache Hive
Duomenų bazės pavadinimas: Schema, kurioje yra šaltinio duomenys (tas pats kaip Schemos pavadinimas)
Schemos pavadinimas:      Schema, kurioje yra šaltinio duomenys
Naudoti ODBC:     Įjungta
```

#### ODBC savybės

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{jūsų slaptažodis figūrinėse skliausteliuose}"
```

> 🔹 `DSN` turi atitikti pavadinimą, nurodytą jūsų ODBC tvarkyklės konfigūracijoje.

---

### B. Konfigūracija be DSN

#### *digna* konfigūracija

Ekrane **"Create a Database Connection"** pateikite šią informaciją:

```
Technologija:     Apache Hive
Duomenų bazės pavadinimas: Schema, kurioje yra šaltinio duomenys (tas pats kaip Schemos pavadinimas)
Schemos pavadinimas:      Schema, kurioje yra šaltinio duomenys
Naudoti ODBC:     Įjungta
```

#### ODBC savybės

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "jūsų serverio pavadinimas arba IP adresas"
name: "PORT",       value: "Porto numeris, pvz. 10000"
name: "Schema",     value: "Schema, kurioje yra šaltinio duomenys"
name: "UID",        value: "jūsų hive vartotojas'"
name: "PWD",        value: "jūsų hive slaptažodis"
name: "AuthMech",   value: "3"
```