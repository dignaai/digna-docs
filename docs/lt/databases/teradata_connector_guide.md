---
title: Teradata jungtis – Duomenų bazės integracija | digna dokumentacija
description: Konfigūruokite digna prisijungimui prie Teradata, naudojant teradatasql Python draiverį arba Teradata ODBC draiverį. Palaiko autentifikaciją slaptažodžiu su DSN arba be DSN.
image: /assets/logo_square.png
---


# Teradata šaltinio jungtis

Šiame vadove aprašoma, kaip sukonfigūruoti *digna* prisijungimui prie Teradata, naudojant arba vietinį Python jungtuką (connector), arba ODBC draiverį.

Jis nurodo ekraną **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Vietinis Python draiveris

**Library:** `teradatasql`  
**Palaikoma autentifikacija:** Tik autentifikacija slaptažodžiu

> Kitoms autentifikacijos metodikoms naudokite ODBC draiverį.

### *digna* konfigūracija (vietinis draiveris)

Pateikite šią informaciją ekrane **"Create a Database Connection"**:

```
Technology:      Teradata
Host Address:    Serverio pavadinimas arba IP adresas
Host Port:       Porto numeris, pvz., 1025
Database Name:   Duomenų bazės pavadinimas
Schema Name:     Schemos pavadinimas
User Name:       Duomenų bazės vartotojo vardas
User Password:   Vartotojo slaptažodis
Use ODBC:        Išjungta (numatyta)
```

---

## ODBC draiveris

ODBC draiveris gali palaikyti platesnį autentifikacijos ir ryšio parinkčių spektrą. Ši skiltis orientuota į autentifikaciją slaptažodžiu, naudojant draiverį **Teradata Database ODBC Driver 20.00**.

### 1. Įdiekite ODBC draiverį

Įdiekite draiverį **Teradata Database ODBC Driver 20.00** (ar panašų), vadovaudamiesi tiekėjo oficialiu diegimo gidu.

### 2. Konfigūruokite ODBC duomenų šaltinį

Atlikite šiuos veiksmus, kad sukonfigūruotumėte naują ODBC duomenų šaltinį, naudojant autentifikaciją slaptažodžiu:

#### Step 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Spustelėkite mygtuką **Test**.

#### Step 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Įveskite vartotojo vardą ir slaptažodį.

Spustelėkite mygtuką **OK**. Kai pasirodys sėkmės pranešimas, ODBC yra tinkamai sukonfigūruotas.

---

Dabar galite sukonfigūruoti *digna* naudoti ODBC ryšį, arba per **DSN (Data Source Name)**, arba be **DSN**.

---

### A. DSN pagrindu

#### *digna* konfigūracija

Ekrane **"Create a Database Connection"** pateikite šią informaciją:

```
Technology:      Teradata
Database Name:   Duomenų bazė, kurioje yra šaltinio schema
Schema Name:     Schema, kurioje yra šaltinio duomenys
Use ODBC:        Įjungta
```

#### ODBC nuostatos

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "jūsų duomenų bazės vartotojas"
name: "PWD",        value: "jūsų duomenų bazės slaptažodis"
```

> `DSN` turi sutapti su vardu, nurodytu jūsų ODBC draiverio konfigūracijoje.

---

### B. Konfigūracija be DSN

#### *digna* konfigūracija

Ekrane **"Create a Database Connection"** pateikite šią informaciją:

```
Technology:      Teradata
Database Name:   Schema, kurioje yra šaltinio duomenys (ta pati kaip Schema Name)
Schema Name:     Schema, kurioje yra šaltinio duomenys
Use ODBC:        Įjungta
```

#### ODBC nuostatos

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "jūsų serverio pavadinimas arba IP adresas"
name: "UID",        value: "jūsų duomenų bazės vartotojas"
name: "PWD",        value: "jūsų duomenų bazės slaptažodis"
```