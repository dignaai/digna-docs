# Avota konektors Azure Synapse Analytics

Šajā ceļvedī aprakstīts, kā konfigurēt *digna* savienojumu ar Azure Synapse Analytics caur
**ODBC**, izmantojot savienojuma virkni **bez DSN** (DSN-less). Tiek atbalstīti gan serverless,
gan dedicated SQL pūli.

Iestatīšanas *digna* puse ir vienāda katrai tehnoloģijai — kur tiek veidoti savienojumi,
kā tiek šifrētas rekvizītu vērtības, kā tiek testēts savienojums un ko nozīmē profilēšanas
režīmi. Tā ir aprakstīta lapā [Datubāzu savienojumu pārskats](overview.md). Šī lapa aptver to,
kas raksturīgs tieši Azure Synapse.

!!! note "Tehnoloģija"

    Synapse izmanto SQL Server dialektu, tāpēc savienojums tiek izveidots ar **Technology:
    SQL Server**. Lokālam serverim skatiet [MS SQL Server](sqlserver_connector_guide.md).

---

## 1. Instalēt ODBC draiveri {: #1-install-the-odbc-driver }

Instalējiet **ODBC Driver 18 for SQL Server** datorā, kurā darbojas *digna* backend,
sekojot [Microsoft instalēšanas ceļvedim](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server),
un nolasiet precīzu reģistrēto draivera nosaukumu savā resursdatorā, kā aprakstīts sadaļā
[Instalēt ODBC draiveri digna resursdatorā](overview.md#install-the-driver).

---

## 2. ODBC rekvizīti {: #2-odbc-properties }

!!! important "Piemērs, nevis specifikācija"

    Tālāk norādītā kopa ir viena kombinācija, par kuru zināms, ka tā darbojas. Rekvizīti pieder
    Microsoft ODBC draiverim, tāpēc to nosaukumi, noklusējuma vērtības un pieņemtās vērtības
    atšķiras starp draivera versijām un platformām, un tas, ko pieprasa darbvieta (workspace), ir
    atkarīgs no tās konfigurācijas — pūla tipa, autentifikācijas metodes, ugunsmūra. Izmantojiet
    to kā sākumpunktu un pārbaudiet jūsu instalētās draivera versijas dokumentāciju.

Ekrānā **Add DB Connection** pievienojiet šādus rekvizītus:

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Jāatbilst draivera nosaukumam, kas reģistrēts *digna* resursdatorā |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Darbvietas nosaukums plus gala punkta sufikss — skatiet tālāk |
| `DATABASE` | `dignadata` | Datubāze, kurā atrodas avota shēmas. Tā ir vienīgā datubāze, ko šis savienojums var profilēt |
| `UID` | `sqladminuser` | SQL pieteikumvārds |
| `PWD` | `<password>` | Atzīmējiet **Encrypted** |

Iegūtā savienojuma virkne izskatās šādi:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### `SERVER` vērtība

Ņemiet Synapse darbvietas nosaukumu un pievienojiet gala punkta sufiksu:

| Pūls | `SERVER` |
|---|---|
| **Serverless SQL pool** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Dedicated SQL pool** | `<workspace>.sql.azuresynapse.net` |

!!! warning "Daļu `-ondemand` ir viegli palaist garām"

    Bez tās nosaukums tiek atrisināts uz dedicated gala punktu, un savienojums vai nu neizdodas,
    vai bez brīdinājuma sasniedz citu pūlu, nekā paredzēts. Abi gala punkti ir redzami darbvietas
    pārskata lapā Azure portālā.

### Ugunsmūris

Synapse darbvietas ugunsmūrim jāatļauj *digna* resursdatora izejošā adrese. Pirms savienojuma
testēšanas pievienojiet to darbvietas sadaļā **Networking** — bloķēta adrese izpaužas kā
savienojuma taimauts, nevis autentifikācijas kļūda.

### Microsoft Entra ID autentifikācija

SQL pieteikumvārda vietā draiveris var autentificēties pret Entra ID. Aizstājiet `UID`/`PWD` ar
autentifikācijas metodi, ko sagaida jūsu darbvieta, piemēram:

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | Tad `UID` satur lietotnes (klienta) ID un `PWD` — klienta slepeno atslēgu |
| `Authentication` | `ActiveDirectoryMSI` | *digna* resursdatora pārvaldītā identitāte (managed identity), akreditācijas dati nav nepieciešami |

---

## 3. *digna* konfigurācija {: #3-digna-configuration }

Ekrānā **Add DB Connection** norādiet šādus datus:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Piezīmes par Azure Synapse {: #4-notes-on-azure-synapse }

- **Serverless pūli atbalsta tikai *Standard* profilēšanu.** Serverless SQL pūls nevar izveidot
  tabulas datubāzē, tāpēc nevar darboties ne *Permanent*, ne *Session* profilēšana. *Standard*
  aprēķina metrikas tieši avotā, un tas ir arī lētākais variants, jo par serverless tiek
  maksāts pēc apstrādāto datu apjoma.
- **Viens savienojums redz vienu datubāzi.** *digna* piedāvā tās datubāzes shēmas, kas norādīta
  `DATABASE`, jo Synapse, tāpat kā SQL Server, kā katalogu norāda tikai pašreizējo datubāzi.
- **Šifrēšana pēc noklusējuma ir ieslēgta** Driver 18, un Synapse gala punkti izmanto derīgus
  publiskos sertifikātus, tāpēc rekvizīti `Encrypt` vai `TrustServerCertificate` nav nepieciešami.
- **Serverless gala punkts pirmajā savienojumā var atsākt darbu pēc dīkstāves.** Ja savienojuma
  testam iestājas taimauts pūlā, kas kādu laiku nav izmantots, mēģiniet vēlreiz.

---

## 5. Draivera pārbaude (pēc izvēles) {: #5-verifying-the-driver-optional }

Savienojumam bez DSN nav jākonfigurē ODBC datu avots, taču paša draivera vednis ir ērts veids,
kā pārliecināties, ka draiveris darbojas un darbvieta pieņem jūsu akreditācijas datus, pirms tos
ievadāt *digna*.

#### 1. solis
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Aizpildiet lauku "Server".
Izmantojiet Synapse darbvietas nosaukumu un papildiniet to ar ".sql.azuresynapse.net".  
**Uzmanību**: ja vēlaties savienoties, izmantojot serverless SQL pūlu, noteikti iekļaujiet
"-ondemand", kā parādīts ekrānuzņēmumā iepriekš.

Noklikšķiniet uz pogas **Next >**.

#### 2. solis
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Izvēlieties autentifikācijas metodi (piem., lietotājvārds un parole)
un norādiet nepieciešamos datus.

Noklikšķiniet uz pogas **Next >**.

#### 3. solis
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Izvēlieties ANSI atbilstošos iestatījumus, pēc tam noklikšķiniet uz pogas **Next >**.

#### 4. solis
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Varat atstāt noklusējuma iestatījumus vai izvēlēties opcijas pēc vajadzības
un noklikšķināt uz pogas **Finish**.

#### 5. solis
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Tagad noklikšķiniet uz pogas **Test datasource**.

#### 6. solis
![Step 6](images/azure_synapse/create_odbc_data_source_step6.png)

Veiksmes ekrāns apstiprina, ka draiveris, gala punkts un akreditācijas dati darbojas. Ievadītās
vērtības ir tieši tās, ko pieņem rekvizīti [2. sadaļā](#2-odbc-properties).