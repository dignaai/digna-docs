# Virni konektor za Teradata

Ta vodnik opisuje, kako konfigurirati *digna* za povezavo s Teradata z uporabo bodisi izvornega Python konektorja bodisi ODBC gonilnika.

Navaja se zaslon **"Ustvari povezavo z bazo podatkov"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Izvorni Python gonilnik

**Knjižnica:** `teradatasql`  
**Podprta avtentikacija:** Samo avtentikacija z geslom

> Za druge metode avtentikacije uporabite ODBC gonilnik.

### Konfiguracija *digna* (izvorni gonilnik)

Na zaslonu **"Ustvari povezavo z bazo podatkov"** vnesite naslednje podatke:

```
Technology:      Teradata
Host Address:    Ime strežnika ali IP naslov
Host Port:       Številka vrat, npr. 1025
Database Name:   Ime baze podatkov
Schema Name:     Ime baze podatkov
User Name:       Uporabniško ime baze podatkov
User Password:   Geslo uporabnika
Use ODBC:        Onemogočeno (privzeto)
```

---

## ODBC gonilnik

ODBC gonilnik lahko podpira širši nabor možnosti avtentikacije in povezljivosti. Ta razdelek se osredotoča na prijavo z geslom z uporabo gonilnika **Teradata Database ODBC Driver 20.00**.

### 1. Namestitev ODBC gonilnika

Namestite gonilnik **Teradata Database ODBC Driver 20.00** (ali podoben) po uradnem navodilu dobavitelja.

### 2. Konfiguracija ODBC vira podatkov

Sledite tem korakom za konfiguracijo novega ODBC vira podatkov z avtentikacijo z geslom:

#### Korak 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Kliknite gumb **Preizkusi**.

#### Korak 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Vnesite uporabniško ime in geslo.

Kliknite gumb **V redu**.
Ko prejmete zaslon s potrditvijo uspeha, je ODBC pravilno konfiguriran.

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC povezavo, bodisi z **DSN (Data Source Name)** ali brez DSN.

---

### A. Konfiguracija z DSN

#### Konfiguracija *digna*

Na zaslonu **"Ustvari povezavo z bazo podatkov"** vnesite naslednje:

```
Technology:      Teradata
Database Name:   Baza podatkov, ki vsebuje izvorno shemo
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Omogočeno
```

#### ODBC lastnosti

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "vaš uporabnik baze podatkov"
name: "PWD",        value: "vaše geslo za bazo podatkov"
```

> Vrednost `DSN` se mora ujemati z imenom, definiranim v konfiguraciji vašega ODBC gonilnika.

---

### B. Konfiguracija brez DSN

#### Konfiguracija *digna*

Na zaslonu **"Ustvari povezavo z bazo podatkov"** vnesite naslednje:

```
Technology:      Teradata
Database Name:   Shema, ki vsebuje izvorne podatke (enako kot Schema Name)
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Omogočeno
```

#### ODBC lastnosti

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "ime vašega strežnika ali IP naslov"
name: "UID",        value: "vaš uporabnik baze podatkov"
name: "PWD",        value: "vaše geslo za bazo podatkov"
```