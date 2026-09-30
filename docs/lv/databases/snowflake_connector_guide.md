---
title: Snowflake konektors — datubāzes integrācija | digna dokumentācija
description: Konfigurējiet digna savienojumu ar Snowflake caur ODBC ar savienojuma virkni bez DSN. Aptver Snowflake ODBC draiveri, programmatic access tokenus, noliktavas un lomas izvēli un digna puses savienojuma iestatījumus.
image: /assets/logo_square.png
---


# Avota konektors Snowflake

Šajā ceļvedī aprakstīts, kā konfigurēt *digna* savienojumu ar Snowflake caur **ODBC**,
izmantojot savienojuma virkni **bez DSN** (DSN-less).

Iestatīšanas *digna* puse ir vienāda katrai tehnoloģijai — kur tiek veidoti savienojumi,
kā tiek šifrētas rekvizītu vērtības, kā tiek testēts savienojums un ko nozīmē profilēšanas
režīmi. Tā ir aprakstīta lapā [Datubāzu savienojumu pārskats](overview.md). Šī lapa aptver to,
kas raksturīgs tieši Snowflake.

---

## 1. Instalēt ODBC draiveri {: #1-install-the-odbc-driver }

Instalējiet **Snowflake ODBC Driver** datorā, kurā darbojas *digna* backend, sekojot
[Snowflake instalēšanas ceļvedim](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

Draiveris reģistrējas kā **SnowflakeDSIIDriver**. Nolasiet precīzu reģistrēto nosaukumu savā
resursdatorā, kā aprakstīts sadaļā [Instalēt ODBC draiveri digna resursdatorā](overview.md#install-the-driver).

---

## 2. ODBC rekvizīti {: #2-odbc-properties }

Snowflake tiek sasniegts ar **programmatic access token (PAT)** — autentifikācijas veidu, ar kuru
*digna* ir pārbaudīta, un to, ko Snowflake pieprasa kontiem, kuros pieteikšanās tikai ar paroli
ir bloķēta.

!!! important "Piemērs, nevis specifikācija"

    Tālāk norādītā kopa ir viena kombinācija, par kuru zināms, ka tā darbojas. Rekvizīti pieder
    Snowflake ODBC draiverim, tāpēc to nosaukumi, noklusējuma vērtības un pieņemtās vērtības
    atšķiras starp draivera versijām un platformām, un to, kādas autentifikācijas opcijas jūsu
    konts atļauj, nosaka konta drošības politika. Izmantojiet to kā sākumpunktu un pārbaudiet
    jūsu instalētās draivera versijas dokumentāciju.

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Jāatbilst draivera nosaukumam, kas reģistrēts *digna* resursdatorā |
| `Server` | `<account>.snowflakecomputing.com` | Konta identifikators plus sufikss, piem. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Snowflake lietotājs, kuram pieder tokens |
| `Database` | `TEST` | Datubāze, kurā atrodas avota shēmas. Tā ir vienīgā datubāze, ko šis savienojums var profilēt |
| `Schema` | `PUBLIC` | Sesijas noklusējuma shēma |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Izvēlas tokena autentifikāciju |
| `token` | `<programmatic access token>` | Atzīmējiet **Encrypted** |

Iegūtā savienojuma virkne izskatās šādi:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Noliktava un loma

Vaicājumiem nepieciešama noliktava (warehouse). Ja *digna* lietotājam ir noklusējuma noliktava un
noklusējuma loma, sesija tās izmanto, un nekas nav jākonfigurē. Pretējā gadījumā pievienojiet:

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Noliktava, kas izpilda profilēšanas vaicājumus |
| `Role` | `DIGNA_READER` | Loma, kuras tiesības izmanto sesija |

!!! tip "Piešķiriet digna savu noliktavu"

    Atsevišķa, neliela noliktava ar automātisku apturēšanu (auto-suspend) padara profilēšanas
    izmaksas pārskatāmas un novērš to, ka *digna* konkurē ar interaktīviem lietotājiem par skaitļošanas resursiem.

### Paroles autentifikācija

Ja konts to joprojām atļauj, tokena vietā var izmantot paroli — noņemiet `authenticator`
un `token` un pievienojiet:

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `PWD` | `<password>` | Atzīmējiet **Encrypted** |

---

## 3. *digna* konfigurācija {: #3-digna-configuration }

Ekrānā **Add DB Connection** norādiet šādus datus:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Piezīmes par Snowflake {: #4-notes-on-snowflake }

- **Tokeniem beidzas derīgums.** Programmatic access token tiek izsniegts ar noteiktu derīguma
  laiku, un profilēšana apstājas dienā, kad tas beidzas. Izveidojot tokenu, pierakstiet derīguma
  beigu datumu un ievadiet jauno tokenu rekvizītā `token` — šifrētas vērtības var aizstāt, bet
  nevar nolasīt atpakaļ.
- **Viens savienojums redz vienu datubāzi.** *digna* piedāvā tās datubāzes shēmas, kas norādīta
  `Database`, jo Snowflake kā katalogu norāda tikai pašreizējo datubāzi. Avota tabulām citā
  datubāzē nepieciešams savs savienojums.
- **Identifikatori ir lielajiem burtiem**, ja vien tie nav izveidoti pēdiņās. *digna* izmanto
  nosaukumus tā, kā tos norāda Snowflake.
- **Profilēšanas režīmi.** *Permanent* izveido darba tabulas shēmā **Work Schema**, tāpēc lomai
  tur nepieciešamas tiesības `CREATE TABLE`. *Session* izmanto `CREATE TEMPORARY TABLE` un neskar
  **Work Schema**. *Standard* nepieciešama tikai lasīšanas piekļuve — un nekādas rakstīšanas tiesības.

---

## 5. Draivera pārbaude (pēc izvēles) {: #5-verifying-the-driver-optional }

Savienojumam bez DSN nav jākonfigurē ODBC datu avots, taču paša draivera dialogs ir ērts veids,
kā pārliecināties, ka draiveris, konta URL un jūsu akreditācijas dati darbojas, pirms tos
ievadāt *digna*.

#### 1. solis
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Piezīmes:

- **Server** vērtība sastāv no jūsu Snowflake konta identifikatora, kam seko
  `.snowflakecomputing.com`.
- Šeit ievadītie **Database**, **Schema** un **Warehouse** atbilst rekvizītiem `Database`,
  `Schema` un `Warehouse` [2. sadaļā](#2-odbc-properties).

#### 2. solis – Testēt savienojumu

Noklikšķiniet uz pogas **TEST**. Veiksmīgs savienojums izskatās šādi:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)
