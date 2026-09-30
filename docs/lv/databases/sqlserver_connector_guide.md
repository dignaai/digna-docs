---
title: MS SQL Server konektors — datubāzes integrācija | digna dokumentācija
description: Konfigurējiet digna savienojumu ar Microsoft SQL Server caur ODBC ar savienojuma virkni bez DSN. Aptver Microsoft ODBC draiveri, nepieciešamos ODBC rekvizītus, šifrēšanas iestatījumus un digna puses savienojuma iestatījumus.
image: /assets/logo_square.png
---


# Avota konektors MS SQL Server

Šajā ceļvedī aprakstīts, kā konfigurēt *digna* savienojumu ar Microsoft SQL Server caur **ODBC**,
izmantojot savienojuma virkni **bez DSN** (DSN-less).

Iestatīšanas *digna* puse ir vienāda katrai tehnoloģijai — kur tiek veidoti savienojumi,
kā tiek šifrētas rekvizītu vērtības, kā tiek testēts savienojums un ko nozīmē profilēšanas
režīmi. Tā ir aprakstīta lapā [Datubāzu savienojumu pārskats](overview.md). Šī lapa aptver to,
kas raksturīgs tieši SQL Server.

!!! note "Azure Synapse Analytics"

    Arī Synapse tiek konfigurēts kā SQL Server savienojums, ar citu resursdatora nosaukumu un
    dažiem papildu apsvērumiem — skatiet [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Instalēt ODBC draiveri {: #1-install-the-odbc-driver }

Instalējiet **ODBC Driver 18 for SQL Server** datorā, kurā darbojas *digna* backend,
sekojot [Microsoft instalēšanas ceļvedim](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

Arī draiveris, kas tiek piegādāts kopā ar Windows ar vienkāršo nosaukumu **SQL Server**,
darbojas, taču tas sen ir novecojis un neatbalsta ne mūsdienīgus TLS iestatījumus, ne Azure
autentifikāciju. Izmantojiet to tikai tad, ja pašreizējā draivera instalēšana nav iespējama.

Nolasiet precīzu reģistrēto draivera nosaukumu savā resursdatorā, kā aprakstīts sadaļā
[Instalēt ODBC draiveri digna resursdatorā](overview.md#install-the-driver).

---

## 2. ODBC rekvizīti {: #2-odbc-properties }

!!! important "Piemērs, nevis specifikācija"

    Tālāk norādītā kopa ir viena kombinācija, par kuru zināms, ka tā darbojas. Rekvizīti pieder
    Microsoft ODBC draiverim, tāpēc to nosaukumi, noklusējuma vērtības un pieņemtās vērtības
    atšķiras starp draivera versijām — piemēram, Driver 18 pēc noklusējuma šifrē, bet Driver 17
    to nedarīja — un starp platformām. Izmantojiet to kā sākumpunktu un pārbaudiet jūsu instalētās
    draivera versijas dokumentāciju.

Ekrānā **Add DB Connection** pievienojiet šādus rekvizītus:

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Jāatbilst draivera nosaukumam, kas reģistrēts *digna* resursdatorā |
| `SERVER` | `sql.example.com` | Servera nosaukums vai IP adrese. Nosauktām instancēm: `host\instance`; nestandarta portam: `host,1433` |
| `PORT` | `1433` | Izlaidiet, ja ports jau ir daļa no `SERVER` |
| `DATABASE` | `digna_source_db` | Datubāze, kurā atrodas avota shēmas. Tā ir vienīgā datubāze, ko šis savienojums var profilēt |
| `UID` | `digna_source_user` | Datubāzes lietotājs |
| `PWD` | `<password>` | Atzīmējiet **Encrypted** |

Iegūtā savienojuma virkne izskatās šādi:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Šifrēšana ar ODBC Driver 18

Driver 18 pēc noklusējuma šifrē savienojumus un pārbauda servera sertifikātu. Ja servera
sertifikātam jūsu *digna* resursdators neuzticas — parasti tas ir pašparakstīts sertifikāts —,
savienošanās neizdodas ar sertifikātu ķēdes kļūdu. Pievienojiet:

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `Encrypt` | `yes` | Noklusējums Driver 18; iestatiet `no` tikai tad, ja serveris nevar izmantot TLS |
| `TrustServerCertificate` | `yes` | Izlaiž sertifikāta pārbaudi. Ērti testa vidēs; ražošanā labāk instalējiet sertifikātu |

### Windows autentifikācija

Lai savienotos ar kontu, ar kuru darbojas *digna* pakalpojums, nevis ar SQL pieteikumvārdu,
noņemiet `UID` un `PWD` un pievienojiet:

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `Trusted_Connection` | `yes` | *digna* pakalpojuma kontam nepieciešamas datubāzes tiesības |

---

## 3. *digna* konfigurācija {: #3-digna-configuration }

Ekrānā **Add DB Connection** norādiet šādus datus:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Piezīmes par MS SQL Server {: #4-notes-on-ms-sql-server }

- **Viens savienojums redz vienu datubāzi.** *digna* piedāvā tās datubāzes shēmas, kas norādīta
  `DATABASE`, jo SQL Server kā katalogu norāda tikai pašreizējo datubāzi. Avota tabulām citā
  datubāzē nepieciešams savs savienojums.
- **Profilēšanas režīmi.** *Permanent* izveido darba tabulas shēmā **Work Schema**, tāpēc
  lietotājam tur nepieciešamas tiesības `CREATE TABLE`. *Session* izmanto lokālas pagaidu tabulas
  (`#wt_…`) datubāzē `tempdb` un neskar **Work Schema**. *Standard* nepieciešama tikai lasīšanas piekļuve.
- **`SERVER` satur instanci un portu.** Nosauktai instancei `host\instance` gadījumā jābūt
  sasniedzamam pakalpojumam SQL Server Browser; `host,port` no tā izvairās.

---

## 5. Draivera pārbaude (pēc izvēles) {: #5-verifying-the-driver-optional }

Savienojumam bez DSN nav jākonfigurē ODBC datu avots, taču paša draivera vednis ir ērts veids,
kā pārliecināties, ka draiveris darbojas un serveris pieņem jūsu akreditācijas datus, pirms tos
ievadāt *digna*.

#### 1. solis
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Noklikšķiniet uz pogas **Next >**.

#### 2. solis
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Izvēlieties autentifikācijas metodi (piem., lietotājvārds un parole)
un norādiet nepieciešamos datus.

Noklikšķiniet uz pogas **Next >**.

#### 3. solis
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Izvēlieties ANSI atbilstošos iestatījumus, pēc tam noklikšķiniet uz pogas **Next >**.

#### 4. solis
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Varat atstāt noklusējuma iestatījumus vai izvēlēties žurnālošanas opcijas pēc vajadzības
un noklikšķināt uz pogas **Finish**.

#### 5. solis
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Tagad noklikšķiniet uz pogas **Test datasource**.

#### 6. solis
![Step 6](images/sqlserver/create_odbc_data_source_step6.png)

Veiksmes ekrāns apstiprina, ka draiveris un akreditācijas dati darbojas. Ievadītās vērtības ir
tieši tās, ko pieņem rekvizīti [2. sadaļā](#2-odbc-properties).
