# Izvorni konektor za Hive

Ta vodič opisuje, kako konfigurirati *digna* za povezavo z Apache Hive prek **ODBC** z nizom za
povezavo **brez DSN** (DSN-less).

Stran nastavitve *digna* je enaka za vse tehnologije — kje se ustvarjajo povezave, kako se
šifrirajo vrednosti lastnosti, kako se povezava testira in kaj pomenijo načini profiliranja.
Opisana je v [Pregled povezav z bazami podatkov](overview.md). Ta stran zajema, kar je
specifično za Hive.

---

## 1. Namestite gonilnik ODBC {: #1-install-the-odbc-driver }

Na računalnik, na katerem teče zaledje *digna*, namestite **Cloudera ODBC Driver for Apache
Hive** po uradnih navodilih proizvajalca za namestitev.

Na svojem gostitelju preberite natančno registrirano ime gonilnika, kot je opisano v
[Namestite gonilnik ODBC na gostitelja digna](overview.md#install-the-driver).

---

## 2. Lastnosti ODBC {: #2-odbc-properties }

!!! important "Primer, ne specifikacija"

    Spodnji nabor je ena kombinacija, za katero je znano, da deluje. Lastnosti pripadajo
    gonilniku Cloudera Hive, zato se njihova imena, privzete vrednosti in sprejete vrednosti
    razlikujejo med različicami gonilnika in platformami, kaj sprejme HiveServer2, pa je v celoti
    odvisno od tega, kako je gruča zavarovana — mehanizem avtentikacije, način transporta, TLS,
    prehod. Uporabite to kot izhodišče in preverite dokumentacijo različice gonilnika, ki ste jo
    namestili.

Na zaslonu **Add DB Connection** dodajte naslednje lastnosti:

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Mora se ujemati z imenom gonilnika, registriranim na gostitelju *digna* |
| `HOST` | `hive.example.com` | Ime gostitelja ali naslov IP strežnika HiveServer2 |
| `PORT` | `10000` | Vrata HiveServer2; `10001` za transport HTTP |

Nastali niz za povezavo je videti takole:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Avtentikacija

Nezavarovan HiveServer2 sprejme zgornje tri lastnosti takšne, kot so. Kjer je avtentikacija
omogočena, dodajte:

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `AuthMech` | `3` | `0` brez avtentikacije, `2` samo uporabniško ime, `3` uporabniško ime in geslo, `1` Kerberos |
| `UID` | `digna_source_user` | Obvezno za `AuthMech` `2` in `3` |
| `PWD` | `<password>` | Obvezno za `AuthMech` `3`. Označite **Encrypted** |

Za Kerberos (`AuthMech=1`) gostitelj *digna* dodatno potrebuje veljavno vstopnico (ticket) ali
keytab ter lastnosti `KrbHostFQDN`, `KrbServiceName` in `KrbRealm`, ki jih dokumentira
gonilnik.

### Transport in TLS

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `ThriftTransport` | `2` | `0` binarni (privzeto, vrata 10000), `1` SASL, `2` HTTP (vrata 10001, kar pričakuje prehod Knox) |
| `HTTPPath` | `cliservice` | Z `ThriftTransport=2` |
| `SSL` | `1` | Kjer je HiveServer2 zavarovan s TLS |
| `Schema` | `dignadata` | Baza podatkov Hive, v kateri se začne seja. Neobvezno — *digna* svoje poizvedbe v celoti kvalificira |

---

## 3. Konfiguracija *digna* {: #3-digna-configuration }

Na zaslonu **Add DB Connection** vnesite naslednje:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Opombe o Hive {: #4-notes-on-hive }

- **Katalogi prihajajo iz gonilnika.** Hive nima lastnega kataloga, zato *digna* vzame to, kar
  sporoči gonilnik — običajno en sam vnos z imenom `HIVE` — in pod njim navede baze podatkov
  Hive kot sheme.
- **Work Schema je baza podatkov Hive.** Za profiliranje *Permanent* uporabnik potrebuje pravico
  ustvarjanja in brisanja tabel v njej, osnovna lokacija shrambe pa mora biti zapisljiva.
- **Načini profiliranja.** *Permanent* ustvari delovne tabele v **Work Schema**. *Session*
  uporablja `CREATE TEMPORARY TABLE`, kar zahteva HiveServer2, ki podpira začasne tabele, in se
  **Work Schema** ne dotika. *Standard* potrebuje samo dostop za branje in je način, ki ga
  izberete v gruči, kjer *digna* nima nobenega dostopa za pisanje.
- **Profiliranje je nabor poizvedb, ne pregled podatkov.** Vsako statistiko izračuna
  HiveServer2, zato mora imeti čakalna vrsta, v katero pošilja uporabnik *digna*, dovolj
  zmogljivosti za časovno okno inšpekcije.

---

## 5. Preverjanje gonilnika (neobvezno) {: #5-verifying-the-driver-optional }

Konfiguriranje vira podatkov ODBC za povezavo brez DSN ni potrebno, vendar je gonilnikovo
lastno pogovorno okno priročen način, da preverite, ali gonilnik, način transporta in vaše
poverilnice delujejo, preden jih vnesete v *digna*.

#### 1. korak
![Step 1](images/hive/create_odbc_data_source_step1.png)

Polja **Host**, **Port**, **Database**, **Mechanism** in **Thrift Transport** tukaj ustrezajo
lastnostim `HOST`, `PORT`, `Schema`, `AuthMech` in `ThriftTransport` v
[razdelku 2](#2-odbc-properties).

#### 2. korak – Testirajte povezavo

Vnesite geslo in kliknite gumb **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Po uspešnem testu kliknite gumb **OK**.