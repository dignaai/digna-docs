---
title: MS SQL Server konektor – integracija baze podatkov | digna Dokumentacija
description: Konfigurirajte digna za povezavo z Microsoft SQL Server prek ODBC z nizom za povezavo brez DSN. Zajema Microsoftov gonilnik ODBC, zahtevane lastnosti ODBC, nastavitve šifriranja in nastavitve povezave na strani digna.
image: /assets/logo_square.png
---


# Izvorni konektor za MS SQL Server

Ta vodič opisuje, kako konfigurirati *digna* za povezavo z Microsoft SQL Server prek **ODBC** z
nizom za povezavo **brez DSN** (DSN-less).

Stran nastavitve *digna* je enaka za vse tehnologije — kje se ustvarjajo povezave, kako se
šifrirajo vrednosti lastnosti, kako se povezava testira in kaj pomenijo načini profiliranja.
Opisana je v [Pregled povezav z bazami podatkov](overview.md). Ta stran zajema, kar je
specifično za SQL Server.

!!! note "Azure Synapse Analytics"

    Tudi Synapse se konfigurira kot povezava SQL Server, z drugačnim imenom gostitelja in nekaj
    dodatnimi posebnostmi — glejte [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Namestite gonilnik ODBC {: #1-install-the-odbc-driver }

Na računalnik, na katerem teče zaledje *digna*, namestite **ODBC Driver 18 for SQL Server** po
[Microsoftovih navodilih za namestitev](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

Deluje tudi gonilnik, ki je priložen sistemu Windows pod preprostim imenom **SQL Server**,
vendar je že dolgo zastarel in ne podpira niti sodobnih nastavitev TLS niti avtentikacije Azure.
Uporabite ga samo tam, kjer namestitev trenutnega gonilnika ni mogoča.

Na svojem gostitelju preberite natančno registrirano ime gonilnika, kot je opisano v
[Namestite gonilnik ODBC na gostitelja digna](overview.md#install-the-driver).

---

## 2. Lastnosti ODBC {: #2-odbc-properties }

!!! important "Primer, ne specifikacija"

    Spodnji nabor je ena kombinacija, za katero je znano, da deluje. Lastnosti pripadajo
    Microsoftovemu gonilniku ODBC, zato se njihova imena, privzete vrednosti in sprejete
    vrednosti razlikujejo med različicami gonilnika — Driver 18 na primer privzeto šifrira, česar
    Driver 17 ni počel — in med platformami. Uporabite to kot izhodišče in preverite
    dokumentacijo različice gonilnika, ki ste jo namestili.

Na zaslonu **Add DB Connection** dodajte naslednje lastnosti:

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Mora se ujemati z imenom gonilnika, registriranim na gostitelju *digna* |
| `SERVER` | `sql.example.com` | Ime strežnika ali naslov IP. Poimenovane instance: `host\instance`; nestandardna vrata: `host,1433` |
| `PORT` | `1433` | Izpustite, če so vrata že del `SERVER` |
| `DATABASE` | `digna_source_db` | Baza podatkov, ki vsebuje izvorne sheme. To je edina baza podatkov, ki jo ta povezava lahko profilira |
| `UID` | `digna_source_user` | Uporabnik baze podatkov |
| `PWD` | `<password>` | Označite **Encrypted** |

Nastali niz za povezavo je videti takole:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Šifriranje z ODBC Driver 18

Driver 18 privzeto šifrira povezave in preverja certifikat strežnika. Pri strežniku s
certifikatom, ki mu vaš gostitelj *digna* ne zaupa — običajno samopodpisan certifikat —
povezava ne uspe z napako v verigi certifikatov. Dodajte:

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `Encrypt` | `yes` | Privzeto v Driver 18; nastavite na `no` samo, če strežnik ne podpira TLS |
| `TrustServerCertificate` | `yes` | Preskoči preverjanje certifikata. Priročno v testnih okoljih; v produkciji raje namestite certifikat |

### Windows Authentication

Če se želite povezati kot račun, pod katerim teče storitev *digna*, namesto s prijavo SQL,
odstranite `UID` in `PWD` ter dodajte:

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `Trusted_Connection` | `yes` | Storitveni račun *digna* potrebuje pravice v bazi podatkov |

---

## 3. Konfiguracija *digna* {: #3-digna-configuration }

Na zaslonu **Add DB Connection** vnesite naslednje:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Opombe o MS SQL Server {: #4-notes-on-ms-sql-server }

- **Ena povezava vidi eno bazo podatkov.** *digna* ponudi sheme baze podatkov, navedene v
  `DATABASE`, ker SQL Server kot katalog sporoči samo trenutno bazo podatkov. Izvorne tabele v
  drugi bazi podatkov potrebujejo svojo povezavo.
- **Načini profiliranja.** *Permanent* ustvari delovne tabele v **Work Schema**, zato uporabnik
  tam potrebuje `CREATE TABLE`. *Session* uporablja lokalne začasne tabele (`#wt_…`) v
  `tempdb` in se **Work Schema** ne dotika. *Standard* potrebuje samo dostop za branje.
- **`SERVER` vsebuje instanco in vrata.** Pri poimenovani instanci `host\instance` zahteva, da
  je storitev SQL Server Browser dosegljiva; `host,port` se temu izogne.

---

## 5. Preverjanje gonilnika (neobvezno) {: #5-verifying-the-driver-optional }

Konfiguriranje vira podatkov ODBC za povezavo brez DSN ni potrebno, vendar je gonilnikov lastni
čarovnik priročen način, da preverite, ali gonilnik deluje in ali strežnik sprejme vaše
poverilnice, preden jih vnesete v *digna*.

#### 1. korak
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Kliknite gumb **Next >**.

#### 2. korak
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Izberite metodo avtentikacije (npr. uporabniško ime in geslo)
in vnesite zahtevane podatke.

Kliknite gumb **Next >**.

#### 3. korak
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Izberite nastavitve, skladne z ANSI, nato kliknite gumb **Next >**.

#### 4. korak
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Lahko pustite privzete nastavitve ali izberete možnosti beleženja po potrebi
in kliknete gumb **Finish**.

#### 5. korak
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Zdaj kliknite gumb **Test datasource**.

#### 6. korak
![Step 6](images/sqlserver/create_odbc_data_source_step6.png)

Zaslon o uspehu potrdi, da gonilnik in poverilnice delujejo. Vrednosti, ki ste jih vnesli, so
natanko vrednosti, ki jih sprejmejo lastnosti v [razdelku 2](#2-odbc-properties).
