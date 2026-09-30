---
title: Teradata konektors — datubāzes integrācija | digna dokumentācija
description: Konfigurējiet digna savienojumu ar Teradata caur ODBC ar savienojuma virkni bez DSN. Aptver Teradata ODBC draiveri, rekvizītu DBCNAME, pieteikšanās mehānismus un digna puses savienojuma iestatījumus.
image: /assets/logo_square.png
---


# Avota konektors Teradata

Šajā ceļvedī aprakstīts, kā konfigurēt *digna* savienojumu ar Teradata caur **ODBC**,
izmantojot savienojuma virkni **bez DSN** (DSN-less).

Iestatīšanas *digna* puse ir vienāda katrai tehnoloģijai — kur tiek veidoti savienojumi,
kā tiek šifrētas rekvizītu vērtības, kā tiek testēts savienojums un ko nozīmē profilēšanas
režīmi. Tā ir aprakstīta lapā [Datubāzu savienojumu pārskats](overview.md). Šī lapa aptver to,
kas raksturīgs tieši Teradata.

---

## 1. Instalēt ODBC draiveri {: #1-install-the-odbc-driver }

Instalējiet **ODBC Driver for Teradata** datorā, kurā darbojas *digna* backend,
sekojot piegādātāja oficiālajam instalēšanas ceļvedim.

Draiveris reģistrējas ar versiju nosaukumā, piemēram,
**Teradata Database ODBC Driver 20.00**. Nolasiet precīzu reģistrēto nosaukumu savā resursdatorā,
kā aprakstīts sadaļā [Instalēt ODBC draiveri digna resursdatorā](overview.md#install-the-driver).

---

## 2. ODBC rekvizīti {: #2-odbc-properties }

!!! important "Piemērs, nevis specifikācija"

    Tālāk norādītā kopa ir viena kombinācija, par kuru zināms, ka tā darbojas. Rekvizīti pieder
    Teradata ODBC draiverim, tāpēc to nosaukumi, noklusējuma vērtības un pieņemtās vērtības
    atšķiras starp draivera versijām — versija ir daļa no paša draivera nosaukuma — un starp
    platformām. Izmantojiet to kā sākumpunktu un pārbaudiet jūsu instalētās draivera versijas dokumentāciju.

Ekrānā **Add DB Connection** pievienojiet šādus rekvizītus:

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Jāatbilst draivera nosaukumam, kas reģistrēts *digna* resursdatorā |
| `DBCNAME` | `teradata.example.com` | Servera nosaukums vai IP adrese. Teradata paša nosaukums resursdatora rekvizītam |
| `UID` | `digna_source_user` | Datubāzes lietotājs |
| `PWD` | `<password>` | Atzīmējiet **Encrypted** |

Iegūtā savienojuma virkne izskatās šādi:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Noderīgi papildu rekvizīti:

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `MechanismName` | `TD2` | Pieteikšanās mehānisms. `TD2` ir Teradata noklusējums; direktorija autentifikācijai izmantojiet `LDAP` |
| `DefaultDatabase` | `dad` | Datubāze, kurā sākas sesija |
| `CharacterSet` | `UTF8` | Iestatiet to, ja noklusējuma sesijas rakstzīmju kopa sabojātu ne-ASCII datus |

---

## 3. *digna* konfigurācija {: #3-digna-configuration }

Ekrānā **Add DB Connection** norādiet šādus datus:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Piezīmes par Teradata {: #4-notes-on-teradata }

- **Teradata datubāze ir katalogs, nevis shēma.** *digna* uzskaita datubāzes, ko lietotājs drīkst
  redzēt (no `DBC.DatabasesV`), kā katalogus, un shēmas līmenis netiek izmantots. Pievienojot
  datu avotu, izvēlieties datubāzi kā katalogu; shēma tiek norādīta kā *not applicable*.
- **Viens savienojums sasniedz katru atļauto datubāzi**, tāpēc viens savienojums var apkalpot
  avotus vairākās datubāzēs — atšķirībā no tehnoloģijām, kurās savienojums ir piesaistīts vienai datubāzei.
- **Work Schema ir datubāze.** *Permanent* profilēšanai norādiet Teradata datubāzi, kurā atrodas
  darba tabulas, un piešķiriet lietotājam tajā tiesības `CREATE TABLE` un `PERM` vietas
  piešķīrumu — datubāzē ar nulles perm vietu nevar glabāt tabulu.
- **Profilēšanas režīmi.** *Permanent* izveido tabulas shēmā **Work Schema**. *Session* izmanto
  `VOLATILE` tabulu, kurai nepieciešama `SPOOL` vieta, bet nav nepieciešama perm vieta un tiesības
  **Work Schema**. *Standard* nepieciešama tikai lasīšanas piekļuve.

---

## 5. Draivera pārbaude (pēc izvēles) {: #5-verifying-the-driver-optional }

Savienojumam bez DSN nav jākonfigurē ODBC datu avots, taču paša draivera dialogs ir ērts veids,
kā pārliecināties, ka draiveris un jūsu akreditācijas dati darbojas, pirms tos ievadāt *digna*.

#### 1. solis
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Lauks **Name or IP address** šeit ir rekvizīts `DBCNAME`
[2. sadaļā](#2-odbc-properties).

Noklikšķiniet uz pogas **Test**.

#### 2. solis
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Norādiet lietotājvārdu un paroli, pēc tam noklikšķiniet uz pogas **OK**. Veiksmes ekrāns
apstiprina, ka draiveris un akreditācijas dati darbojas.
