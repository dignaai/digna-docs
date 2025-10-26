---
title: Netezza jungtis – Duomenų bazės integracija | digna dokumentacija
description: Sukonfigūruokite digna, kad prisijungtų prie Netezza naudojant NetezzaSQL ODBC tvarkyklę. Palaikomas prisijungimas su slaptažodžiu, naudojant DSN arba be DSN, kad būtų užtikrintas lankstus ryšys.
image: /assets/logo_square.png
---


# Netezza šaltinio jungtis

Šiame vadove aprašoma, kaip sukonfigūruoti *digna*, kad jis prisijungtų prie Netezza naudojant ODBC tvarkyklę.

Jame nurodoma ekranas **"Sukurti duomenų bazės ryšį"**.

![Sukurti duomenų bazės ryšį](images/data_source_config_input_mask.png)

---

## ODBC tvarkyklė

ODBC tvarkyklė gali palaikyti įvairias autentifikacijos ir prisijungimo parinktis. Ši skiltis orientuota į prisijungimą su slaptažodžiu naudojant tvarkyklę **NetezzaSQL**.

### 1. Įdiekite ODBC tvarkyklę

Įdiekite tvarkyklę **NetezzaSQL** (ar panašią) vadovaudamiesi tiekėjo oficialiu diegimo vadovu.

### 2. Konfigūruokite ODBC duomenų šaltinį

Atlikite šiuos veiksmus, kad sukonfigūruotumėte naują ODBC duomenų šaltinį, naudojant prisijungimą su slaptažodžiu:

#### Žingsnis 1
![Žingsnis 1](images/netezza/create_odbc_data_source_step1.png)

Priklausomai nuo jūsų Netezza tvarkyklės, diegimo ir saugumo reikalavimų, gali prireikti taip pat pateikti duomenis skiltyse **Advanced DSN Options**, **SSL DSN Options** arba **Driver Options**. Paprasčiausiam konfigūravimui pakanka nurodyti informaciją skiltyje **DSN Options**.

Spustelėkite mygtuką **Test Connection**.

#### Žingsnis 2
![Žingsnis 2](images/netezza/create_odbc_data_source_step2.png)

Kai gaunate sėkmės ekraną, ODBC yra tinkamai sukonfigūruota.

---

Dabar galite sukonfigūruoti *digna*, kad naudotų ODBC ryšį, arba per **DSN (Data Source Name)**, arba naudojant **be DSN** (DSN-less) konfigūraciją.

---

### A. Konfigūracija su DSN

#### *digna* konfigūracija

Ekrane **"Sukurti duomenų bazės ryšį"** nurodykite šią informaciją:

```
Technology:      Netezza
Database Name:   Duomenų bazė, kurioje yra šaltinio schema
Schema Name:     Schema, kurioje yra šaltinio duomenys
Use ODBC:        Enabled
```

#### ODBC savybės

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "jūsų duomenų bazės vartotojas"
name: "PWD",        value: "jūsų duomenų bazės slaptažodis"
```

> 🔹 `DSN` turi atitikti pavadinimą, nurodytą jūsų ODBC tvarkyklės konfigūracijoje.

---

### B. DSN-less konfigūracija

#### *digna* konfigūracija

Ekrane **"Sukurti duomenų bazės ryšį"** nurodykite šią informaciją:

```
Technology:      Netezza
Database Name:   Schema, kurioje yra šaltinio duomenys (tas pats, kaip Schema Name)
Schema Name:     Schema, kurioje yra šaltinio duomenys
Use ODBC:        Enabled
```

#### ODBC savybės

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "jūsų serverio pavadinimas arba IP adresas"
name: "PORT",       value: "Porto numeris, pvz., 5480"
name: "DATABASE",   value: "duomenų bazės pavadinimas, kuriame yra šaltinio duomenų schema"
name: "UID",        value: "jūsų duomenų bazės vartotojas"
name: "PWD",        value: "jūsų duomenų bazės slaptažodis"
```