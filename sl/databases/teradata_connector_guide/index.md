# Izvorni konektor za Teradata

Ta vodič opisuje, kako konfigurirati *digna* za povezavo s Teradata prek **ODBC** z nizom za
povezavo **brez DSN** (DSN-less).

Stran nastavitve *digna* je enaka za vse tehnologije — kje se ustvarjajo povezave, kako se
šifrirajo vrednosti lastnosti, kako se povezava testira in kaj pomenijo načini profiliranja.
Opisana je v [Pregled povezav z bazami podatkov](overview.md). Ta stran zajema, kar je
specifično za Teradata.

---

## 1. Namestite gonilnik ODBC {: #1-install-the-odbc-driver }

Na računalnik, na katerem teče zaledje *digna*, namestite **ODBC Driver for Teradata** po
uradnih navodilih proizvajalca za namestitev.

Gonilnik se registrira z različico v imenu, na primer
**Teradata Database ODBC Driver 20.00**. Na svojem gostitelju preberite natančno registrirano
ime, kot je opisano v [Namestite gonilnik ODBC na gostitelja digna](overview.md#install-the-driver).

---

## 2. Lastnosti ODBC {: #2-odbc-properties }

!!! important "Primer, ne specifikacija"

    Spodnji nabor je ena kombinacija, za katero je znano, da deluje. Lastnosti pripadajo
    gonilniku Teradata ODBC, zato se njihova imena, privzete vrednosti in sprejete vrednosti
    razlikujejo med različicami gonilnika — različica je del samega imena gonilnika — in med
    platformami. Uporabite to kot izhodišče in preverite dokumentacijo različice gonilnika, ki ste
    jo namestili.

Na zaslonu **Add DB Connection** dodajte naslednje lastnosti:

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Mora se ujemati z imenom gonilnika, registriranim na gostitelju *digna* |
| `DBCNAME` | `teradata.example.com` | Ime strežnika ali naslov IP. Teradatino lastno ime za lastnost gostitelja |
| `UID` | `digna_source_user` | Uporabnik baze podatkov |
| `PWD` | `<password>` | Označite **Encrypted** |

Nastali niz za povezavo je videti takole:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Uporabne dodatne lastnosti:

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `MechanismName` | `TD2` | Mehanizem prijave. `TD2` je privzeti mehanizem Teradata; za avtentikacijo prek imenika uporabite `LDAP` |
| `DefaultDatabase` | `dad` | Baza podatkov, v kateri se začne seja |
| `CharacterSet` | `UTF8` | Nastavite, kadar bi privzeti nabor znakov seje pokvaril podatke, ki niso ASCII |

---

## 3. Konfiguracija *digna* {: #3-digna-configuration }

Na zaslonu **Add DB Connection** vnesite naslednje:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Opombe o Teradata {: #4-notes-on-teradata }

- **Baza podatkov Teradata je katalog, ne shema.** *digna* navede baze podatkov, ki jih
  uporabnik sme videti (iz `DBC.DatabasesV`), kot kataloge, raven sheme pa ne velja. Ko dodate
  vir podatkov, izberite bazo podatkov kot katalog; shema je sporočena kot *not applicable*.
- **Ena povezava doseže vsako dovoljeno bazo podatkov**, zato lahko ena sama povezava služi
  virom v več bazah podatkov — za razliko od tehnologij, pri katerih je povezava vezana na eno
  bazo podatkov.
- **Work Schema je baza podatkov.** Za profiliranje *Permanent* navedite bazo podatkov
  Teradata, ki vsebuje delovne tabele, in uporabniku v njej dodelite pravice `CREATE TABLE` ter
  dodelitev prostora `PERM` — baza podatkov z ničelnim prostorom perm ne more vsebovati tabele.
- **Načini profiliranja.** *Permanent* ustvari tabele v **Work Schema**. *Session* uporablja
  tabelo `VOLATILE`, ki potrebuje prostor `SPOOL`, ne pa prostora perm niti pravic v **Work
  Schema**. *Standard* potrebuje samo dostop za branje.

---

## 5. Preverjanje gonilnika (neobvezno) {: #5-verifying-the-driver-optional }

Konfiguriranje vira podatkov ODBC za povezavo brez DSN ni potrebno, vendar je gonilnikovo
lastno pogovorno okno priročen način, da preverite, ali gonilnik in vaše poverilnice delujejo,
preden jih vnesete v *digna*.

#### 1. korak
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Polje **Name or IP address** tukaj je lastnost `DBCNAME` v
[razdelku 2](#2-odbc-properties).

Kliknite gumb **Test**.

#### 2. korak
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Vnesite uporabniško ime in geslo, nato kliknite gumb **OK**. Zaslon o uspehu potrdi, da
gonilnik in poverilnice delujejo.