# Izvorni konektor za PostgreSQL

Ta vodič opisuje, kako konfigurirati *digna* za povezavo s PostgreSQL prek **ODBC** z nizom za
povezavo **brez DSN** (DSN-less).

Stran nastavitve *digna* je enaka za vse tehnologije — kje se ustvarjajo povezave, kako se
šifrirajo vrednosti lastnosti, kako se povezava testira in kaj pomenijo načini profiliranja.
Opisana je v [Pregled povezav z bazami podatkov](overview.md). Ta stran zajema, kar je
specifično za PostgreSQL.

---

## 1. Namestite gonilnik ODBC {: #1-install-the-odbc-driver }

Na računalnik, na katerem teče zaledje *digna*, namestite gonilnik PostgreSQL ODBC
(**psqlODBC**) po uradnih navodilih proizvajalca za namestitev.

Gonilnik se registrira pod imenom, ki se razlikuje glede na platformo in paket — običajno
**PostgreSQL Unicode(x64)** v sistemu Windows in **PostgreSQL ODBC Driver(UNICODE)** v sistemu
Linux. Na svojem gostitelju preberite natančno ime, kot je opisano v
[Namestite gonilnik ODBC na gostitelja digna](overview.md#install-the-driver), in to ime
uporabite za spodnjo lastnost `DRIVER`.

---

## 2. Lastnosti ODBC {: #2-odbc-properties }

!!! important "Primer, ne specifikacija"

    Spodnji nabor je ena kombinacija, za katero je znano, da deluje. Lastnosti pripadajo
    gonilniku psqlODBC, zato se njihova imena, privzete vrednosti in sprejete vrednosti
    razlikujejo med različicami gonilnika in platformami, tudi zahteve vašega strežnika — zlasti
    glede SSL — so lahko drugačne. Uporabite to kot izhodišče in preverite dokumentacijo
    različice gonilnika, ki ste jo namestili.

Na zaslonu **Add DB Connection** dodajte naslednje lastnosti:

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Mora se ujemati z imenom gonilnika, registriranim na gostitelju *digna* |
| `SERVER` | `db.example.com` | Ime strežnika ali naslov IP |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Baza podatkov, ki vsebuje izvorne sheme. To je edina baza podatkov, ki jo ta povezava lahko profilira |
| `UID` | `digna_source_user` | Uporabnik baze podatkov |
| `PWD` | `<password>` | Označite **Encrypted** |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` ali `verify-full` — strežnik ga mora sprejeti |

Nastali niz za povezavo je videti takole:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Vsako nadaljnjo možnost psqlODBC lahko dodate kot dodatno lastnost — na primer `ReadOnly=1`
za sejo samo za branje ali `ConnSettings` za izvajanje stavkov `SET` ob vzpostavitvi
povezave.

---

## 3. Konfiguracija *digna* {: #3-digna-configuration }

Na zaslonu **Add DB Connection** vnesite naslednje:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Opombe o PostgreSQL {: #4-notes-on-postgresql }

- **`SSLMode` se mora ujemati s strežnikom.** Strežnik, konfiguriran s `hostssl`, zavrne
  `SSLMode=disable`, `verify-ca` ali `verify-full` pa dodatno zahtevata, da je korenski
  certifikat na voljo gonilniku na gostitelju *digna*. Če ste morali pri testiranju gonilnika
  izbrati določen način, uporabite istega tudi tukaj.
- **Ena povezava vidi eno bazo podatkov.** *digna* ponudi sheme baze podatkov, navedene v
  `DATABASE`, ker PostgreSQL kot katalog sporoči samo trenutno bazo podatkov. Izvorne tabele v
  drugi bazi podatkov potrebujejo svojo povezavo.
- **Načini profiliranja.** *Permanent* ustvari delovne tabele v **Work Schema**, zato uporabnik
  potrebuje `CREATE` na tej shemi. *Session* uporablja `CREATE TEMPORARY TABLE` in se
  **Work Schema** ne dotika. *Standard* potrebuje samo dostop za branje.

---

## 5. Preverjanje gonilnika (neobvezno) {: #5-verifying-the-driver-optional }

Konfiguriranje vira podatkov ODBC za povezavo brez DSN ni potrebno, vendar je gonilnikovo
lastno pogovorno okno priročen način, da preverite, ali gonilnik deluje in ali strežnik sprejme
vaše poverilnice in način SSL, preden jih vnesete v *digna*.

#### 1. korak
![Step 1](images/postgres/create_odbc_data_source_step1.png)

#### 2. korak – Testirajte povezavo

Kliknite gumb **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

Vrednosti, ki ste jih vnesli tukaj, so natanko vrednosti, ki jih sprejmejo lastnosti v
[razdelku 2](#2-odbc-properties).