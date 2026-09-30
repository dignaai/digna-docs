---
title: Azure Synapse konektor – integracija baze podatkov | digna Dokumentacija
description: Konfigurirajte digna za povezavo z Azure Synapse Analytics prek ODBC z nizom za povezavo brez DSN. Podpira serverless in namenske (dedicated) bazene SQL, z zahtevanimi lastnostmi ODBC in nastavitvami povezave na strani digna.
image: /assets/logo_square.png
---


# Izvorni konektor za Azure Synapse Analytics

Ta vodič opisuje, kako konfigurirati *digna* za povezavo z Azure Synapse Analytics prek
**ODBC** z nizom za povezavo **brez DSN** (DSN-less). Podprti so tako serverless kot namenski
(dedicated) bazeni SQL.

Stran nastavitve *digna* je enaka za vse tehnologije — kje se ustvarjajo povezave, kako se
šifrirajo vrednosti lastnosti, kako se povezava testira in kaj pomenijo načini profiliranja.
Opisana je v [Pregled povezav z bazami podatkov](overview.md). Ta stran zajema, kar je
specifično za Azure Synapse.

!!! note "Tehnologija"

    Synapse uporablja narečje SQL Server, zato se povezava ustvari s **Technology:
    SQL Server**. Za lokalni strežnik glejte [MS SQL Server](sqlserver_connector_guide.md).

---

## 1. Namestite gonilnik ODBC {: #1-install-the-odbc-driver }

Na računalnik, na katerem teče zaledje *digna*, namestite **ODBC Driver 18 for SQL Server** po
[Microsoftovih navodilih za namestitev](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
in na svojem gostitelju preberite natančno registrirano ime gonilnika, kot je opisano v
[Namestite gonilnik ODBC na gostitelja digna](overview.md#install-the-driver).

---

## 2. Lastnosti ODBC {: #2-odbc-properties }

!!! important "Primer, ne specifikacija"

    Spodnji nabor je ena kombinacija, za katero je znano, da deluje. Lastnosti pripadajo
    Microsoftovemu gonilniku ODBC, zato se njihova imena, privzete vrednosti in sprejete
    vrednosti razlikujejo med različicami gonilnika in platformami, kaj zahteva delovni prostor
    (workspace), pa je odvisno od njegove konfiguracije — tip bazena, metoda avtentikacije,
    požarni zid. Uporabite to kot izhodišče in preverite dokumentacijo različice gonilnika, ki ste
    jo namestili.

Na zaslonu **Add DB Connection** dodajte naslednje lastnosti:

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Mora se ujemati z imenom gonilnika, registriranim na gostitelju *digna* |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Ime delovnega prostora in pripona končne točke — glejte spodaj |
| `DATABASE` | `dignadata` | Baza podatkov, ki vsebuje izvorne sheme. To je edina baza podatkov, ki jo ta povezava lahko profilira |
| `UID` | `sqladminuser` | Prijava SQL |
| `PWD` | `<password>` | Označite **Encrypted** |

Nastali niz za povezavo je videti takole:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### Vrednost `SERVER`

Vzemite ime delovnega prostora Synapse in dodajte pripono končne točke:

| Bazen | `SERVER` |
|---|---|
| **Serverless SQL pool** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Dedicated SQL pool** | `<workspace>.sql.azuresynapse.net` |

!!! warning "Del `-ondemand` je lahko spregledati"

    Brez njega se ime razreši v namensko končno točko, povezava pa bodisi ne uspe bodisi brez
    opozorila doseže drug bazen, kot je bil predviden. Obe končni točki sta prikazani na strani s
    pregledom delovnega prostora v portalu Azure.

### Požarni zid

Požarni zid delovnega prostora Synapse mora dovoliti odhodni naslov gostitelja *digna*. Dodajte
ga pod **Networking** v delovnem prostoru, preden testirate povezavo — blokiran naslov se pokaže
kot potek časa povezave in ne kot napaka avtentikacije.

### Avtentikacija z Microsoft Entra ID

Namesto prijave SQL se lahko gonilnik avtenticira z Entra ID. `UID`/`PWD` zamenjajte z metodo
avtentikacije, ki jo pričakuje vaš delovni prostor, na primer:

| Ključ | Primer vrednosti | Opombe |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | `UID` nato sprejme ID aplikacije (odjemalca), `PWD` pa skrivnost odjemalca |
| `Authentication` | `ActiveDirectoryMSI` | Upravljana identiteta (managed identity) gostitelja *digna*, poverilnice niso potrebne |

---

## 3. Konfiguracija *digna* {: #3-digna-configuration }

Na zaslonu **Add DB Connection** vnesite naslednje:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Opombe o Azure Synapse {: #4-notes-on-azure-synapse }

- **Serverless bazeni podpirajo samo profiliranje *Standard*.** Serverless SQL pool ne more
  ustvarjati tabel v bazi podatkov, zato ni mogoče izvajati niti profiliranja *Permanent* niti
  *Session*. *Standard* izračuna metrike neposredno na viru, kar je tudi cenejša možnost, saj
  se serverless obračunava po količini obdelanih podatkov.
- **Ena povezava vidi eno bazo podatkov.** *digna* ponudi sheme baze podatkov, navedene v
  `DATABASE`, ker Synapse, tako kot SQL Server, kot katalog sporoči samo trenutno bazo podatkov.
- **Šifriranje je privzeto vklopljeno** v Driver 18, končne točke Synapse pa predstavijo
  veljavne javne certifikate, zato lastnost `Encrypt` ali `TrustServerCertificate` ni potrebna.
- **Serverless končna točka se lahko ob prvi povezavi prebuja iz mirovanja.** Če test povezave
  poteče pri bazenu, ki nekaj časa ni bil uporabljen, poskusite znova.

---

## 5. Preverjanje gonilnika (neobvezno) {: #5-verifying-the-driver-optional }

Konfiguriranje vira podatkov ODBC za povezavo brez DSN ni potrebno, vendar je gonilnikov lastni
čarovnik priročen način, da preverite, ali gonilnik deluje in ali delovni prostor sprejme vaše
poverilnice, preden jih vnesete v *digna*.

#### 1. korak
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Izpolnite polje "Server".
Uporabite ime delovnega prostora Synapse in ga razširite z ".sql.azuresynapse.net".  
**Pozor**, če se želite povezati prek serverless SQL pool, ne pozabite vključiti
"-ondemand", kot je prikazano na zgornjem posnetku zaslona.

Kliknite gumb **Next >**.

#### 2. korak
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Izberite metodo avtentikacije (npr. uporabniško ime in geslo)
in vnesite zahtevane podatke.

Kliknite gumb **Next >**.

#### 3. korak
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Izberite nastavitve, skladne z ANSI, nato kliknite gumb **Next >**.

#### 4. korak
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Lahko pustite privzete nastavitve ali izberete možnosti po potrebi
in kliknete gumb **Finish**.

#### 5. korak
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Zdaj kliknite gumb **Test datasource**.

#### 6. korak
![Step 6](images/azure_synapse/create_odbc_data_source_step6.png)

Zaslon o uspehu potrdi, da gonilnik, končna točka in poverilnice delujejo. Vrednosti, ki ste jih
vnesli, so natanko vrednosti, ki jih sprejmejo lastnosti v [razdelku 2](#2-odbc-properties).
