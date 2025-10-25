---
title: Povezovalec Netezza – integracija baze podatkov | digna dokumentacija
description: Konfiguracija digna za povezavo z Netezza z uporabo ODBC gonilnika NetezzaSQL. Podpira preverjanje pristnosti z geslom z nastavitvami DSN ali brez DSN.
image: /assets/logo_square.png
---


# Povezovalec vira za Netezza

Ta vodnik opisuje, kako konfigurirati *digna* za povezavo z Netezza z uporabo ODBC gonilnika.

Slika se nanaša na zaslon **"Ustvari povezavo z bazo podatkov"**.

![Veritabanı bağlantısı oluştur](images/data_source_config_input_mask.png)

---

## ODBC gonilnik

ODBC gonilnik lahko podpira različne možnosti preverjanja pristnosti in povezovanja. Ta razdelek se osredotoča na preverjanje pristnosti z geslom z uporabo gonilnika **NetezzaSQL**.

### 1. Namestite ODBC gonilnik

Namestite gonilnik **NetezzaSQL** (ali soroden), tako kot je opisano v uradnem namestitvenem vodniku dobavitelja.

### 2. Konfigurirajte ODBC vir podatkov

Za konfiguracijo novega ODBC vira podatkov z overjanjem na osnovi gesla sledite tem korakom:

#### Korak 1
![Adım 1](images/netezza/create_odbc_data_source_step1.png)

Gonilnik Netezza vam morda zahteva dodatne informacije v zavihkih **Advanced DSN Options**, **SSL DSN Options** ali **Driver Options**, odvisno od vaše namestitve in varnostnih zahtev. Za osnovno namestitev je običajno dovolj vnesti informacije v razdelku **DSN Options**.

Kliknite na gumb **Test Connection**.

#### Korak 2
![Adım 2](images/netezza/create_odbc_data_source_step2.png)

Ko se prikaže zaslon o uspehu, je ODBC pravilno konfiguriran.

---

Zdaj lahko *digna* konfigurirate za uporabo ODBC povezave; bodisi z **DSN (Data Source Name)** ali z nastavitevjo **brez DSN** (DSN-less).

---

### A. Konfiguracija z DSN

#### *digna* konfiguracija

**"Ustvari povezavo z bazo podatkov"** zaslonu zagotovite naslednje:

```
Tehnologija:      Netezza
Ime baze podatkov: Baza podatkov, ki vsebuje izvorno shemo
Ime sheme:         Shema, ki vsebuje izvorne podatke
Uporaba ODBC:      Omogočeno
```

#### ODBC lastnosti

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "vaše uporabniško ime za bazo"
name: "PWD",        value: "vaše geslo za bazo"
```

> 🔹 `DSN` mora ustrezati imenu, definiranim v nastavitvah vašega ODBC gonilnika.

---

### B. Konfiguracija brez DSN

#### *digna* konfiguracija

Na zaslonu **"Ustvari povezavo z bazo podatkov"** zagotovite:

```
Tehnologija:       Netezza
Ime baze podatkov: Shema, ki vsebuje izvorne podatke (enako kot Ime sheme)
Ime sheme:         Shema, ki vsebuje izvorne podatke
Uporaba ODBC:      Omogočeno
```

#### ODBC lastnosti

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "ime strežnika ali IP naslov"
name: "PORT",       value: "številka vrat, npr. 5480"
name: "DATABASE",   value: "ime baze podatkov, ki vsebuje izvorno shemo"
name: "UID",        value: "vaše uporabniško ime za bazo"
name: "PWD",        value: "vaše geslo za bazo"
```