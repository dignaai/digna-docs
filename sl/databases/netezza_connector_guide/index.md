# Povezovalnik vira za Netezza

Ta vodnik opisuje, kako konfigurirati *digna*, da se poveže z Netezza z uporabo ODBC gonilnika.

Navaja se zaslon **"Ustvari povezavo do baze podatkov"**.

![Ustvari povezavo do baze podatkov](images/data_source_config_input_mask.png)

---

## ODBC gonilnik

ODBC gonilnik lahko podpira različne možnosti overjanja in povezljivosti. Ta razdelek se osredotoča na overjanje z geslom z gonilnikom **NetezzaSQL**.

### 1. Namestite ODBC gonilnik

Namestite gonilnik **NetezzaSQL** (ali podoben) tako, da sledite uradnemu navodilu za namestitev proizvajalca.

### 2. Konfigurirajte ODBC podatkovni vir

Sledite tem korakom za konfiguracijo novega ODBC podatkovnega vira z uporabo overjanja z geslom:

#### Korak 1
![Korak 1](images/netezza/create_odbc_data_source_step1.png)

Glede na vaš Netezza gonilnik, zahteve za namestitev in varnost, boste morda morali vnesti podatke tudi na zavihkih **Advanced DSN Options**, **SSL DSN Options** ali **Driver Options**. Za najbolj preprosto nastavitev je dovolj vnesti podatke v **DSN Options**.

Kliknite gumb **Preizkusi povezavo**.

#### Korak 2
![Korak 2](images/netezza/create_odbc_data_source_step2.png)

Ko se prikaže zaslon z obvestilom o uspehu, je ODBC pravilno konfiguriran.

---

Zdaj lahko *digna* konfigurirate za uporabo ODBC povezave, bodisi s **DSN (Data Source Name)** ali v **DSN-less** načinu.

---

### A. Konfiguracija na osnovi DSN

#### Konfiguracija *digna*

Na zaslonu **"Ustvari povezavo do baze podatkov"** vnesite naslednje:

```
Technology:      Netezza
Database Name:   Baza podatkov, ki vsebuje izvorno shemo
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Omogočeno
```

#### ODBC lastnosti

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "vaš uporabnik baze podatkov"
name: "PWD",        value: "vaše geslo za bazo podatkov"
```

> Vrednost `DSN` mora ustrezati imenu, definiranemu v vaši konfiguraciji ODBC gonilnika.

---

### B. DSN-less konfiguracija

#### Konfiguracija *digna*

Na zaslonu **"Ustvari povezavo do baze podatkov"** vnesite naslednje:

```
Technology:      Netezza
Database Name:   Shema, ki vsebuje izvorne podatke (enako kot Schema Name)
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Omogočeno
```

#### ODBC lastnosti

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "ime vašega strežnika ali IP naslov"
name: "PORT",       value: "Številka vrat, npr. 5480"
name: "DATABASE",   value: "ime baze podatkov, ki vsebuje shemo z izvornih podatki"
name: "UID",        value: "vaš uporabnik baze podatkov"
name: "PWD",        value: "vaše geslo za bazo podatkov"
```