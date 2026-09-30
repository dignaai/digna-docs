# Avota konektors PostgreSQL

Šajā ceļvedī aprakstīts, kā konfigurēt *digna* savienojumu ar PostgreSQL caur **ODBC**,
izmantojot savienojuma virkni **bez DSN** (DSN-less).

Iestatīšanas *digna* puse ir vienāda katrai tehnoloģijai — kur tiek veidoti savienojumi,
kā tiek šifrētas rekvizītu vērtības, kā tiek testēts savienojums un ko nozīmē profilēšanas
režīmi. Tā ir aprakstīta lapā [Datubāzu savienojumu pārskats](overview.md). Šī lapa aptver to,
kas raksturīgs tieši PostgreSQL.

---

## 1. Instalēt ODBC draiveri {: #1-install-the-odbc-driver }

Instalējiet PostgreSQL ODBC draiveri (**psqlODBC**) datorā, kurā darbojas *digna* backend,
sekojot piegādātāja oficiālajam instalēšanas ceļvedim.

Draiveris reģistrējas ar nosaukumu, kas atšķiras atkarībā no platformas un pakotnes — parasti
**PostgreSQL Unicode(x64)** operētājsistēmā Windows un **PostgreSQL ODBC Driver(UNICODE)**
Linux. Nolasiet precīzu nosaukumu savā resursdatorā, kā aprakstīts sadaļā
[Instalēt ODBC draiveri digna resursdatorā](overview.md#install-the-driver), un izmantojiet šo
nosaukumu tālāk norādītajam rekvizītam `DRIVER`.

---

## 2. ODBC rekvizīti {: #2-odbc-properties }

!!! important "Piemērs, nevis specifikācija"

    Tālāk norādītā kopa ir viena kombinācija, par kuru zināms, ka tā darbojas. Rekvizīti pieder
    psqlODBC draiverim, tāpēc to nosaukumi, noklusējuma vērtības un pieņemtās vērtības atšķiras
    starp draivera versijām un platformām, un arī tas, ko pieprasa jūsu serveris — īpaši SSL —,
    var atšķirties. Izmantojiet to kā sākumpunktu un pārbaudiet jūsu instalētās draivera versijas
    dokumentāciju.

Ekrānā **Add DB Connection** pievienojiet šādus rekvizītus:

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Jāatbilst draivera nosaukumam, kas reģistrēts *digna* resursdatorā |
| `SERVER` | `db.example.com` | Servera nosaukums vai IP adrese |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Datubāze, kurā atrodas avota shēmas. Tā ir vienīgā datubāze, ko šis savienojums var profilēt |
| `UID` | `digna_source_user` | Datubāzes lietotājs |
| `PWD` | `<password>` | Atzīmējiet **Encrypted** |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` vai `verify-full` — serverim tas jāpieņem |

Iegūtā savienojuma virkne izskatās šādi:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Jebkuru citu psqlODBC opciju var pievienot kā papildu rekvizītu — piemēram, `ReadOnly=1`
sesijai tikai lasīšanai vai `ConnSettings`, lai savienošanās brīdī izpildītu `SET` priekšrakstus.

---

## 3. *digna* konfigurācija {: #3-digna-configuration }

Ekrānā **Add DB Connection** norādiet šādus datus:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Piezīmes par PostgreSQL {: #4-notes-on-postgresql }

- **`SSLMode` jāatbilst serverim.** Serveris, kas konfigurēts ar `hostssl`, noraida
  `SSLMode=disable`, un `verify-ca` vai `verify-full` gadījumā draiverim *digna* resursdatorā
  papildus jābūt pieejamam saknes sertifikātam. Ja, testējot draiveri, bija jāizvēlas konkrēts
  režīms, izmantojiet to pašu arī šeit.
- **Viens savienojums redz vienu datubāzi.** *digna* piedāvā tās datubāzes shēmas, kas norādīta
  `DATABASE`, jo PostgreSQL kā katalogu norāda tikai pašreizējo datubāzi. Avota tabulām citā
  datubāzē nepieciešams savs savienojums.
- **Profilēšanas režīmi.** *Permanent* izveido darba tabulas shēmā **Work Schema**, tāpēc
  lietotājam šajā shēmā nepieciešamas tiesības `CREATE`. *Session* izmanto `CREATE TEMPORARY TABLE`
  un neskar **Work Schema**. *Standard* nepieciešama tikai lasīšanas piekļuve.

---

## 5. Draivera pārbaude (pēc izvēles) {: #5-verifying-the-driver-optional }

Savienojumam bez DSN nav jākonfigurē ODBC datu avots, taču paša draivera dialogs ir ērts veids,
kā pārliecināties, ka draiveris darbojas un serveris pieņem jūsu akreditācijas datus un SSL
režīmu, pirms tos ievadāt *digna*.

#### 1. solis
![Step 1](images/postgres/create_odbc_data_source_step1.png)

#### 2. solis – Testēt savienojumu

Noklikšķiniet uz pogas **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

Šeit ievadītās vērtības ir tieši tās, ko pieņem rekvizīti [2. sadaļā](#2-odbc-properties).