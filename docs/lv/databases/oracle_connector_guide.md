---
title: Oracle konektors — datubāzes integrācija | digna dokumentācija
description: Konfigurējiet digna savienojumu ar Oracle caur ODBC ar savienojuma virkni bez DSN. Aptver Oracle ODBC draiveri, DBQ savienojuma deskriptoru, TNS aizstājvārdus un digna puses savienojuma iestatījumus.
image: /assets/logo_square.png
---


# Avota konektors Oracle

Šajā ceļvedī aprakstīts, kā konfigurēt *digna* savienojumu ar Oracle Database caur **ODBC**,
izmantojot savienojuma virkni **bez DSN** (DSN-less).

Iestatīšanas *digna* puse ir vienāda katrai tehnoloģijai — kur tiek veidoti savienojumi,
kā tiek šifrētas rekvizītu vērtības, kā tiek testēts savienojums un ko nozīmē profilēšanas
režīmi. Tā ir aprakstīta lapā [Datubāzu savienojumu pārskats](overview.md). Šī lapa aptver to,
kas raksturīgs tieši Oracle.

---

## 1. Instalēt ODBC draiveri {: #1-install-the-odbc-driver }

Oracle ODBC draiveris ir daļa no **Oracle Client** (pietiek ar Instant Client pakotni "ODBC").
Instalējiet to datorā, kurā darbojas *digna* backend, sekojot piegādātāja oficiālajam
instalēšanas ceļvedim.

Draiveris reģistrējas kā **Oracle in `<OracleHomeName>`** — piemēram,
`Oracle in OraDB21Home1` vai `Oracle in instantclient_21_13`. Home nosaukums katrā instalācijā
atšķiras, tāpēc nolasiet precīzu nosaukumu savā resursdatorā, kā aprakstīts sadaļā
[Instalēt ODBC draiveri digna resursdatorā](overview.md#install-the-driver).

---

## 2. ODBC rekvizīti {: #2-odbc-properties }

!!! important "Piemērs, nevis specifikācija"

    Tālāk norādītā kopa ir viena kombinācija, par kuru zināms, ka tā darbojas. Rekvizīti pieder
    Oracle ODBC draiverim, tāpēc to nosaukumi, noklusējuma vērtības un pieņemtās vērtības
    atšķiras starp klienta versijām, un īpaši draivera nosaukums ir atkarīgs no Oracle home jūsu
    resursdatorā. Izmantojiet to kā sākumpunktu un pārbaudiet jūsu instalētās klienta versijas dokumentāciju.

Ekrānā **Add DB Connection** pievienojiet šādus rekvizītus:

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Jāatbilst draivera nosaukumam, kas reģistrēts *digna* resursdatorā |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Datubāze, ar kuru savienoties — skatiet tālāk |
| `UID` | `DIGNA_SOURCE_USER` | Datubāzes lietotājs |
| `PWD` | `<password>` | Atzīmējiet **Encrypted** |

Iegūtā savienojuma virkne izskatās šādi:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### `DBQ` vērtība

`DBQ` pieņem trīs formas. *digna* tās ir līdzvērtīgas; tās atšķiras ar to, kas jākonfigurē
*digna* resursdatorā:

| Forma | Piemērs | Nepieciešams |
|---|---|---|
| **Pilns savienojuma deskriptors** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Nekas — viss ir rekvizītā. Ieteicams |
| **TNS aizstājvārds** | `DIGNA_SOURCE` | Aizstājvārdam jābūt Oracle Client failā `tnsnames.ora` *digna* resursdatorā |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Oracle Client, kas atbalsta Easy Connect (12c un jaunāks) |

!!! tip "Dodiet priekšroku pilnam deskriptoram"

    TNS aizstājvārds pārvieto pusi savienojuma definīcijas uz failu *digna* resursdatorā, kur to
    ir viegli aizmirst, kad resursdators tiek pārbūvēts vai *digna* tiek pārvietota. Pilns
    deskriptors saglabā savienojumu pašpietiekamu — un tieši tā ir iestatīšanas bez DSN jēga.

Ievērojiet, ka deskriptora iekavas savienojuma virknē netraucē, taču, ja jūsu parole satur `;`,
ietveriet to figūriekavās: `PWD={p@ss;word}`.

---

## 3. *digna* konfigurācija {: #3-digna-configuration }

Ekrānā **Add DB Connection** norādiet šādus datus:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Piezīmes par Oracle {: #4-notes-on-oracle }

- **Shēmas ir lietotāji.** *digna* uzskaita Oracle lietotājus kā shēmas, tāpēc avota shēma ir
  tabulu īpašnieks — iepriekš minētajā piemērā `DIGNA_SOURCE_USER`. Savienojuma lietotājam
  nepieciešamas `SELECT` tiesības šīm tabulām, vai nu tieši, vai caur lomu.
- **Viens savienojums redz vienu datubāzi.** Katalogs, ko piedāvā *digna*, ir datubāze, kurai
  savienojums ir pievienots, tāpēc `DBQ` nosaka, kurš pakalpojums un līdz ar to kura datubāze
  tiek profilēta.
- **Identifikatori pēdiņās ir reģistrjutīgi.** *digna* ievieto pēdiņās nosaukumus, ko tā nolasa
  no datu vārdnīcas, un tie ir tādi, kā tos glabā Oracle — lielajiem burtiem objektiem, kas
  izveidoti bez pēdiņām.
- **Profilēšanas režīmi.** *Permanent* izveido darba tabulas shēmā **Work Schema**, tāpēc
  lietotājam tur nepieciešamas tiesības `CREATE TABLE` un kvota tabulu telpā (tablespace).
  *Session* izmanto privātu pagaidu tabulu (`ORA$PTT_…`, Oracle 18c un jaunāka) un neskar
  **Work Schema**. *Standard* nepieciešama tikai lasīšanas piekļuve.

---

## 5. Draivera pārbaude (pēc izvēles) {: #5-verifying-the-driver-optional }

Savienojumam bez DSN nav jākonfigurē ODBC datu avots, taču paša draivera dialogs ir ērts veids,
kā pārliecināties, ka Oracle Client, pakalpojuma nosaukums un jūsu akreditācijas dati darbojas,
pirms tos ievadāt *digna*.

#### 1. solis
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Šeit piedāvātais **TNS Service Name** nāk no jūsu Oracle Client instalācijas faila
`tnsnames.ora` — tur ir definēts aizstājvārds un līdz ar to resursdators, ports un pakalpojuma
nosaukums. *digna* varat izmantot aizstājvārdu kā `DBQ` vai tā vietā pilnu deskriptoru.

#### 2. solis – Testēt savienojumu

Noklikšķiniet uz pogas **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Norādiet paroli un noklikšķiniet uz pogas **OK**.

![Step 3](images/oracle/create_odbc_data_source_step3.png)

Veiksmes ziņojums apstiprina, ka draiveris un akreditācijas dati darbojas.
