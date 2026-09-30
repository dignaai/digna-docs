---
title: Databricks konektors — datubāzes integrācija | digna dokumentācija
description: Konfigurējiet digna savienojumu ar Databricks ar Unity Catalog caur ODBC ar savienojuma virkni bez DSN. Aptver Databricks ODBC draiveri, personīgās piekļuves tokenus, HTTP ceļu un digna puses savienojuma iestatījumus.
image: /assets/logo_square.png
---

# Avota konektors Databricks

Šajā ceļvedī aprakstīts, kā konfigurēt *digna* savienojumu ar Databricks caur **ODBC**,
izmantojot savienojuma virkni **bez DSN** (DSN-less).

Iestatīšanas *digna* puse ir vienāda katrai tehnoloģijai — kur tiek veidoti savienojumi,
kā tiek šifrētas rekvizītu vērtības, kā tiek testēts savienojums un ko nozīmē profilēšanas
režīmi. Tā ir aprakstīta lapā [Datubāzu savienojumu pārskats](overview.md). Šī lapa aptver to,
kas raksturīgs tieši Databricks.

!!! note "Nepieciešams Unity Catalog"

    *digna* nolasa pieejamos katalogus no `system.information_schema.catalogs`, tāpēc darbvietā
    (workspace) jābūt iespējotam Unity Catalog. Iepriekšējos *digna* izlaidumos bija pieejama
    atsevišķa tehnoloģija "Databricks Legacy" darbvietām bez Unity Catalog; tā vairs nav
    pieejama.

---

## 1. Instalēt ODBC draiveri {: #1-install-the-odbc-driver }

Instalējiet **Databricks ODBC Driver** datorā, kurā darbojas *digna* backend, sekojot
[Databricks instalēšanas ceļvedim](https://docs.databricks.com/aws/en/integrations/odbc/).

Atkarībā no versijas draiveris reģistrējas kā **Simba Spark ODBC Driver** vai kā
**Databricks ODBC Driver**. Nolasiet precīzu reģistrēto nosaukumu savā resursdatorā, kā aprakstīts sadaļā
[Instalēt ODBC draiveri digna resursdatorā](overview.md#install-the-driver).

---

## 2. Savākt savienojuma datus {: #2-gather-the-connection-details }

Visas vērtības nāk no SQL noliktavas (warehouse) vai klastera, ko vēlaties, lai *digna* izmantotu.
Atveriet to Databricks darbvietā un dodieties uz **Connection details**:

| Databricks lauks | Tiek izmantots kā |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, parasti `443` |
| **HTTP path** | `HTTPPath` |

Autentifikācijai izveidojiet **personīgās piekļuves tokenu** (personal access token) — skatiet
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Tokeni pieder lietotājam vai servisa principālim (service principal), un šim principālim avota
datos nepieciešamas tiesības `USE CATALOG`, `USE SCHEMA` un `SELECT`.

---

## 3. ODBC rekvizīti {: #3-odbc-properties }

!!! important "Piemērs, nevis specifikācija"

    Tālāk norādītā kopa ir viena kombinācija, par kuru zināms, ka tā darbojas. Rekvizīti pieder
    Databricks/Simba draiverim, tāpēc to nosaukumi, noklusējuma vērtības un pieņemtās vērtības
    atšķiras starp draivera versijām — draiveris ir vairākkārt pārdēvēts un tā autentifikācijas
    opcijas paplašinātas — un starp platformām. Izmantojiet to kā sākumpunktu un pārbaudiet jūsu
    instalētās draivera versijas dokumentāciju.

Ekrānā **Add DB Connection** pievienojiet šādus rekvizītus:

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Jāatbilst draivera nosaukumam, kas reģistrēts *digna* resursdatorā |
| `Host` | `<workspace>.cloud.databricks.com` | Noliktavas servera resursdatora nosaukums, piem. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | Noliktavas vai klastera HTTP ceļš |
| `SSL` | `1` | Databricks gala punkti darbojas tikai ar TLS |
| `ThriftTransport` | `2` | HTTP transports, ko izmanto SQL gala punkti |
| `AuthMech` | `3` | Tokena autentifikācija |
| `UID` | `token` | Burtiski vārds `token`, nevis lietotājvārds |
| `PWD` | `dapi…` | Personīgās piekļuves tokens. Atzīmējiet **Encrypted** |
| `UseNativeQuery` | `1` | Nodod *digna* SQL nemainītu — skatiet tālāk |

Iegūtā savienojuma virkne izskatās šādi:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Saglabājiet `UseNativeQuery=1`"

    Ar `UseNativeQuery=0` — draivera noklusējumu — draiveris pārraksta ienākošo SQL tajā, ko tas
    uzskata par pārnesamu ODBC sintaksi. *digna* jau ģenerē Databricks SQL, tāpēc pārrakstīšana
    var mainīt apostrofu (backtick) pēdiņas un datumu literāļus, un profilēšana tad neizdodas ar
    priekšrakstiem, kas oriģinālajā formā ir derīgi.

### OAuth tokena vietā

Servisa principālim ar OAuth machine-to-machine autentifikāciju aizstājiet `AuthMech`,
`UID` un `PWD` ar:

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Klienta akreditācijas dati (client credentials) |
| `Auth_Client_ID` | `<application id>` | Servisa principālis |
| `Auth_Client_Secret` | `<client secret>` | Atzīmējiet **Encrypted** |

---

## 4. *digna* konfigurācija {: #4-digna-configuration }

Ekrānā **Add DB Connection** norādiet šādus datus:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Piezīmes par Databricks {: #5-notes-on-databricks }

- **Noliktavai jādarbojas** vai jāspēj startēt, kad *digna* savienojas. Noliktavai, kas atsāk
  darbu no apturēta stāvokļa, var būt nepieciešams vairāk laika nekā savienojuma taimauts — ja
  tests neizdodas pirmajā mēģinājumā pēc dīkstāves, mēģiniet vēlreiz.
- **Katalogi nāk no darbvietas.** Atšķirībā no vairuma tehnoloģiju viens Databricks savienojums
  sasniedz katru katalogu, ko principālim ir atļauts redzēt, tāpēc viens savienojums var
  apkalpot avotus vairākos katalogos.
- **Profilēšanas režīmi.** *Permanent* izveido darba tabulas shēmā **Work Schema** avota
  katalogā, tāpēc principālim tur nepieciešamas tiesības `CREATE TABLE`. *Session* izmanto
  `CREATE TEMPORARY TABLE` un neskar **Work Schema**. *Standard* nepieciešama tikai lasīšanas
  piekļuve.
- **Serverless noliktavas darbojas** tādā pašā veidā; atšķiras tikai `HTTPPath`.

---

## 6. Draivera pārbaude (pēc izvēles) {: #6-verifying-the-driver-optional }

Savienojumam bez DSN nav jākonfigurē ODBC datu avots, taču paša draivera dialogs ir ērts veids,
kā pārliecināties, ka draiveris, noliktava un tokens darbojas, pirms tos ievadāt *digna*.

#### 1. solis
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### 2. solis
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### 3. solis
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### 4. solis
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### 5. solis – Testēt savienojumu

Noklikšķiniet uz pogas **TEST**. Veiksmīgs savienojums izskatās šādi:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

Šeit ievadītais resursdators, HTTP ceļš un tokens ir tieši tās vērtības, ko pieņem rekvizīti
[3. sadaļā](#3-odbc-properties).
