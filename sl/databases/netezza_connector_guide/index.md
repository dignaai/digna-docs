# Izvorni konektor za Netezza

Ta vodič opisuje, kako konfigurirati *digna* za povezavo z Netezza prek **ODBC** z nizom za
povezavo **brez DSN** (DSN-less).

Stran nastavitve *digna* je enaka za vse tehnologije — kje se ustvarjajo povezave, kako se
šifrirajo vrednosti lastnosti, kako se povezava testira in kaj pomenijo načini profiliranja.
Opisana je v [Pregled povezav z bazami podatkov](overview.md). Ta stran zajema, kar je
specifično za Netezza.

---

## 1. Namestite gonilnik ODBC {: #1-install-the-odbc-driver }

Na računalnik, na katerem teče zaledje *digna*, namestite gonilnik ODBC **NetezzaSQL** (del
odjemalskih orodij IBM Netezza) po uradnih navodilih proizvajalca za namestitev.

Na svojem gostitelju preberite natančno registrirano ime gonilnika, kot je opisano v
[Namestite gonilnik ODBC na gostitelja digna](overview.md#install-the-driver).

---

## 2. Lastnosti ODBC {: #2-odbc-properties }

!!! important "Primer, ne specifikacija"

    Spodnji nabor je ena kombinacija, za katero je znano, da deluje. Lastnosti pripadajo
    gonilniku NetezzaSQL, zato se njihova imena, privzete vrednosti in sprejete vrednosti
    razlikujejo med različicami odjemalca in platformami, naprava, zavarovana s TLS, pa
    potrebuje več lastnosti, kot jih je prikazanih tukaj. Uporabite to kot izhodišče in
    preverite dokumentacijo različice odjemalca, ki ste jo namestili.

Na zaslonu **Add DB Connection** dodajte naslednje lastnosti:

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Mora se ujemati z imenom gonilnika, registriranim na gostitelju *digna*. Zaviti oklepaji so običajen način zapisa tega imena |
| `SERVER` | `netezza.example.com` | Ime strežnika ali naslov IP |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Baza podatkov, v kateri se začne seja |
| `UID` | `ADMIN` | Uporabnik baze podatkov |
| `PWD` | `<password>` | Označite **Encrypted** |

Nastali niz za povezavo je videti takole:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

Glede na različico gonilnika, nastavitev in varnostne zahteve so lahko potrebne dodatne
lastnosti — na primer `SecurityLevel` in `CaCertFile` za napravo, zavarovano s TLS. Vsako
možnost, ki jo ponujajo gonilnikova pogovorna okna *Advanced*, *SSL* in *Driver*, lahko dodate
kot lastnost.

---

## 3. Konfiguracija *digna* {: #3-digna-configuration }

Na zaslonu **Add DB Connection** vnesite naslednje:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Opombe o Netezza {: #4-notes-on-netezza }

- **Veljajo tako katalogi kot sheme.** *digna* navede baze podatkov, ki jih uporabnik sme
  videti (iz `_V_DATABASE`), kot kataloge, pod njimi pa njihove sheme (iz `_V_SCHEMA`), zato
  lahko ena povezava služi virom v več kot eni bazi podatkov. `DATABASE` določa le, kje se seja
  začne.
- **Identifikatorji so z velikimi črkami**, razen če so bili ustvarjeni v narekovajih, zato
  zgornji primeri uporabljajo `TEST` in `ADMIN`.
- **Načini profiliranja.** *Permanent* ustvari delovne tabele v **Work Schema**, zato uporabnik
  tam potrebuje `CREATE TABLE`. *Session* uporablja `CREATE TEMPORARY TABLE` in se
  **Work Schema** ne dotika. *Standard* potrebuje samo dostop za branje.

---

## 5. Preverjanje gonilnika (neobvezno) {: #5-verifying-the-driver-optional }

Konfiguriranje vira podatkov ODBC za povezavo brez DSN ni potrebno, vendar je gonilnikovo
lastno pogovorno okno priročen način, da preverite, ali gonilnik in vaše poverilnice delujejo,
preden jih vnesete v *digna*.

#### 1. korak
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Polja v **DSN Options** se ena proti ena ujemajo z lastnostmi v
[razdelku 2](#2-odbc-properties). Glede na vaš gonilnik Netezza, nastavitev in varnostne
zahteve boste morda potrebovali tudi podatke na zavihkih **Advanced DSN Options**,
**SSL DSN Options** ali **Driver Options**; za najpreprostejšo nastavitev zadošča
**DSN Options**.

Kliknite gumb **Test Connection**.

#### 2. korak
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Ko se prikaže zaslon o uspehu, gonilnik deluje in vrednosti so pravilne.