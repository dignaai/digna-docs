---
title: MS SQL Server jungtis – Duomenų bazės integracija | digna dokumentacija
description: Konfigūruokite digna prisijungimui prie Microsoft SQL Server naudodami pymssql Python tvarkyklę arba SQL Server ODBC tvarkyklę. Palaikoma autentifikacija su slaptažodžiu per DSN arba be DSN.
image: /assets/logo_square.png
---


# Šaltinio jungtis MS SQL Server

Šiame vadove aprašyta, kaip konfigūruoti *digna* prisijungimui prie SQL Server, naudojant arba natyvų Python jungtį, arba ODBC tvarkyklę.

Jame nurodoma sąsaja **„Sukurti duomenų bazės ryšį“**.

![Sukurti duomenų bazės ryšį](images/data_source_config_input_mask.png)

---

## Natyvus Python tvarkyklė

**Biblioteka:** `pymssql`  
**Palaikoma autentifikacija:** Tik slaptažodžiu pagrįsta autentifikacija

> ⚠️ Kitoms autentifikacijos metodikoms naudokite ODBC tvarkyklę.

### *digna* konfigūracija (natyvi tvarkyklė)

Pateikite šią informaciją sąsajoje **„Sukurti duomenų bazės ryšį“**:

```
Technologija:     MS SQL Server
Serverio adresas: Serverio pavadinimas arba IP adresas
Serverio portas:  Porto numeris, pvz. 1433
Duomenų bazė:    Duomenų bazės pavadinimas
Schemа:           Schema, kurioje yra šaltinio duomenys
Vartotojo vardas: Duomenų bazės vartotojo vardas
Vartotojo slaptažodis: Slaptažodis vartotojui
Naudoti ODBC:     Išjungta (numatytoji)
```

---

## ODBC tvarkyklė

ODBC tvarkyklė gali palaikyti platesnį autentifikacijos ir ryšio galimybių spektrą. Ši skiltis orientuota į slaptažodžiu pagrįstą autentifikaciją, naudojant tvarkyklę **SQL Server**.

### 1. Įdiekite ODBC tvarkyklę

Įdiekite tvarkyklę **SQL Server** (ar panašią) sekdami tiekėjo oficialų diegimo vadovą.

### 2. Konfigūruokite ODBC duomenų šaltinį

Atlikite šiuos veiksmus, kad konfigūruotumėte naują ODBC duomenų šaltinį, naudojant slaptažodžiu pagrįstą autentifikaciją:

#### 1 veiksmas
![1 veiksmas](images/sqlserver/create_odbc_data_source_step1.png)

Spustelėkite mygtuką **Next >**.

#### 2 veiksmas
![2 veiksmas](images/sqlserver/create_odbc_data_source_step2.png)

Pasirinkite autentifikacijos metodą (pvz., vartotojo vardas ir slaptažodis)
ir pateikite reikiamus duomenis.

Spustelėkite mygtuką **Next >**.

#### 3 veiksmas
![3 veiksmas](images/sqlserver/create_odbc_data_source_step3.png)

Pasirinkite ANSI suderinamus nustatymus, tada spustelėkite mygtuką **Next >**.

#### 4 veiksmas
![4 veiksmas](images/sqlserver/create_odbc_data_source_step4.png)

Galite palikti numatytuosius nustatymus arba pasirinkti žurnalo (logging) parinktis pagal poreikį
ir spustelėkite mygtuką **Finish**.

#### 5 veiksmas
![5 veiksmas](images/sqlserver/create_odbc_data_source_step5.png)

Dabar spustelėkite mygtuką **Test datasource**.

#### 6 veiksmas
![6 veiksmas](images/sqlserver/create_odbc_data_source_step6.png)

Kai gausite sėkmės ekraną, ODBC yra sukonfigūruota teisingai.

---

Dabar galite konfigūruoti *digna* naudoti ODBC ryšį — arba per **DSN (Data Source Name)**, arba be **DSN**.

---

### A. Konfigūracija su DSN

#### *digna* konfigūracija

Sąsajoje **„Sukurti duomenų bazės ryšį“** nurodykite šiuos laukus:

```
Technologija:     MS SQL Server
Duomenų bazė:    Duomenų bazė, kurioje yra šaltinio schema
Schema:           Schema, kurioje yra šaltinio duomenys
Naudoti ODBC:     Įjungta
```

#### ODBC savybės

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "jūsų duomenų bazės vartotojas"
name: "PWD",        value: "jūsų duomenų bazės slaptažodis"
name: "DATABASE",   value: "duomenų bazės pavadinimas, kuriame yra šaltinio duomenų schema"
```

> 🔹 `DSN` turi atitikti vardą, nurodytą jūsų ODBC tvarkyklės konfigūracijoje.

---

### B. Konfigūracija be DSN

#### *digna* konfigūracija

Sąsajoje **„Sukurti duomenų bazės ryšį“** nurodykite šiuos laukus:

```
Technologija:     MS SQL Server
Duomenų bazė:    Schema, kurioje yra šaltinio duomenys (tas pats kaip Schema)
Schema:           Schema, kurioje yra šaltinio duomenys
Naudoti ODBC:     Įjungta
```

#### ODBC savybės

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "jūsų serverio pavadinimas arba IP adresas"
name: "UID",        value: "jūsų duomenų bazės vartotojas"
name: "PWD",        value: "jūsų duomenų bazės slaptažodis"
name: "DATABASE",   value: "duomenų bazės pavadinimas, kuriame yra šaltinio duomenų schema"
```