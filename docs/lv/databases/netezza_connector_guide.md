---
title: Netezza savienotājs – datubāzes integrācija | digna dokumentācija
description: Konfigurējiet *digna*, lai savienotos ar Netezza, izmantojot NetezzaSQL ODBC draiveri. Atbalsta autentifikāciju ar paroli gan ar DSN, gan bez DSN elastīgai savienojamībai.
image: /assets/logo_square.png
---


# Avota savienotājs Netezza

Šis ceļvedis apraksta, kā konfigurēt *digna*, lai savienotos ar Netezza, izmantojot ODBC draiveri.

Tas attiecas uz ekrānu **"Izveidot datubāzes savienojumu"**.

![Izveidot datubāzes savienojumu](images/data_source_config_input_mask.png)

---

## ODBC draiveris

ODBC draiveris var atbalstīt dažādas autentifikācijas un savienošanās opcijas. Šī sadaļa fokusējas uz autentifikāciju, kas balstīta uz paroli, izmantojot draiveri **NetezzaSQL**.

### 1. Instalējiet ODBC draiveri

Instalējiet draiveri **NetezzaSQL** (vai līdzīgu), sekojot ražotāja oficiālajam instalācijas ceļvedim.

### 2. Konfigurējiet ODBC datu avotu

Veiciet šīs darbības, lai konfigurētu jaunu ODBC datu avotu, izmantojot autentifikāciju ar paroli:

#### 1. solis
![1. solis](images/netezza/create_odbc_data_source_step1.png)

Atkarībā no jūsu Netezza draivera, iestatīšanas un drošības prasībām, iespējams, būs jānorāda dati arī cilnēs **Advanced DSN Options**, **SSL DSN Options** vai **Driver Options**. Vienkāršākai konfigurācijai pietiek norādīt datus cilnē **DSN Options**.

Nospiediet pogu **Test Connection**.

#### 2. solis
![2. solis](images/netezza/create_odbc_data_source_step2.png)

Kad tiek parādīts veiksmes ekrāns, ODBC ir pareizi konfigurēts.

---

Tagad varat konfigurēt *digna*, lai izmantotu ODBC savienojumu, izmantojot vai nu **DSN (Data Source Name)**, vai **DSN-less** iestatījumu.

---

### A. DSN bāzes konfigurācija

#### Konfigurācija *digna*

Ekrānā **"Izveidot datubāzes savienojumu"**, norādiet sekojošo:

```
Tehnoloģija:           Netezza
Datubāzes nosaukums:   Datubāze, kas satur avota shēmu
Shēmas nosaukums:      Shēma, kas satur avota datus
Izmantot ODBC:         Ieslēgts
```

#### ODBC īpašības

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "jūsu datubāzes lietotājs"
name: "PWD",        value: "jūsu datubāzes parole"
```

> 🔹 `DSN` ir jāsakrīt ar nosaukumu, kas definēts jūsu ODBC draivera konfigurācijā.

---

### B. DSN-less konfigurācija

#### Konfigurācija *digna*

Ekrānā **"Izveidot datubāzes savienojumu"**, norādiet sekojošo:

```
Tehnoloģija:           Netezza
Datubāzes nosaukums:   Shēma, kas satur avota datus (tas pats, kas Shēmas nosaukums)
Shēmas nosaukums:      Shēma, kas satur avota datus
Izmantot ODBC:         Ieslēgts
```

#### ODBC īpašības

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "jūsu servera nosaukums vai IP adrese"
name: "PORT",       value: "Porta numurs, piem., 5480"
name: "DATABASE",   value: "datubāzes nosaukums, kas satur avota datu shēmu"
name: "UID",        value: "jūsu datubāzes lietotājs"
name: "PWD",        value: "jūsu datubāzes parole"
```