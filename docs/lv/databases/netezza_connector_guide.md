---
title: Netezza konektors — datubāzes integrācija | digna dokumentācija
description: Konfigurējiet digna savienojumu ar Netezza caur ODBC ar savienojuma virkni bez DSN. Aptver NetezzaSQL draiveri, nepieciešamos ODBC rekvizītus un digna puses savienojuma iestatījumus.
image: /assets/logo_square.png
---


# Avota konektors Netezza

Šajā ceļvedī aprakstīts, kā konfigurēt *digna* savienojumu ar Netezza caur **ODBC**,
izmantojot savienojuma virkni **bez DSN** (DSN-less).

Iestatīšanas *digna* puse ir vienāda katrai tehnoloģijai — kur tiek veidoti savienojumi,
kā tiek šifrētas rekvizītu vērtības, kā tiek testēts savienojums un ko nozīmē profilēšanas
režīmi. Tā ir aprakstīta lapā [Datubāzu savienojumu pārskats](overview.md). Šī lapa aptver to,
kas raksturīgs tieši Netezza.

---

## 1. Instalēt ODBC draiveri {: #1-install-the-odbc-driver }

Instalējiet **NetezzaSQL** ODBC draiveri (daļa no IBM Netezza klienta rīkiem) datorā,
kurā darbojas *digna* backend, sekojot piegādātāja oficiālajam instalēšanas ceļvedim.

Nolasiet precīzu reģistrēto draivera nosaukumu savā resursdatorā, kā aprakstīts sadaļā
[Instalēt ODBC draiveri digna resursdatorā](overview.md#install-the-driver).

---

## 2. ODBC rekvizīti {: #2-odbc-properties }

!!! important "Piemērs, nevis specifikācija"

    Tālāk norādītā kopa ir viena kombinācija, par kuru zināms, ka tā darbojas. Rekvizīti pieder
    NetezzaSQL draiverim, tāpēc to nosaukumi, noklusējuma vērtības un pieņemtās vērtības
    atšķiras starp klienta versijām un platformām, un ar TLS aizsargātai iekārtai (appliance)
    nepieciešams vairāk nekā šeit parādītie rekvizīti. Izmantojiet to kā sākumpunktu un
    pārbaudiet jūsu instalētās klienta versijas dokumentāciju.

Ekrānā **Add DB Connection** pievienojiet šādus rekvizītus:

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Jāatbilst draivera nosaukumam, kas reģistrēts *digna* resursdatorā. Figūriekavas ir ierastais veids, kā rakstīt šo nosaukumu |
| `SERVER` | `netezza.example.com` | Servera nosaukums vai IP adrese |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Datubāze, kurā sākas sesija |
| `UID` | `ADMIN` | Datubāzes lietotājs |
| `PWD` | `<password>` | Atzīmējiet **Encrypted** |

Iegūtā savienojuma virkne izskatās šādi:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

Atkarībā no jūsu draivera versijas, iestatījumiem un drošības prasībām var būt nepieciešami
papildu rekvizīti — piemēram, `SecurityLevel` un `CaCertFile` ar TLS aizsargātai iekārtai. Katru
opciju, ko piedāvā draivera dialogi *Advanced*, *SSL* un *Driver*, var pievienot kā rekvizītu.

---

## 3. *digna* konfigurācija {: #3-digna-configuration }

Ekrānā **Add DB Connection** norādiet šādus datus:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Piezīmes par Netezza {: #4-notes-on-netezza }

- **Tiek izmantoti gan katalogi, gan shēmas.** *digna* uzskaita datubāzes, ko lietotājs drīkst
  redzēt (no `_V_DATABASE`), kā katalogus un to shēmas (no `_V_SCHEMA`) zem tiem, tāpēc viens
  savienojums var apkalpot avotus vairāk nekā vienā datubāzē. `DATABASE` nosaka tikai to, kur
  sākas sesija.
- **Identifikatori ir lielajiem burtiem**, ja vien tie nav izveidoti pēdiņās, tāpēc iepriekš
  minētajos piemēros izmantoti `TEST` un `ADMIN`.
- **Profilēšanas režīmi.** *Permanent* izveido darba tabulas shēmā **Work Schema**, tāpēc
  lietotājam tur nepieciešamas tiesības `CREATE TABLE`. *Session* izmanto `CREATE TEMPORARY TABLE`
  un neskar **Work Schema**. *Standard* nepieciešama tikai lasīšanas piekļuve.

---

## 5. Draivera pārbaude (pēc izvēles) {: #5-verifying-the-driver-optional }

Savienojumam bez DSN nav jākonfigurē ODBC datu avots, taču paša draivera dialogs ir ērts veids,
kā pārliecināties, ka draiveris un jūsu akreditācijas dati darbojas, pirms tos ievadāt *digna*.

#### 1. solis
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Lauki cilnē **DSN Options** viens pret vienu atbilst rekvizītiem
[2. sadaļā](#2-odbc-properties). Atkarībā no jūsu Netezza draivera, iestatījumiem un drošības
prasībām var būt nepieciešams aizpildīt arī cilnes **Advanced DSN Options**, **SSL DSN Options**
vai **Driver Options**; vienkāršākajai iestatīšanai pietiek ar **DSN Options**.

Noklikšķiniet uz pogas **Test Connection**.

#### 2. solis
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Kad redzat veiksmes ekrānu, draiveris darbojas un vērtības ir pareizas.
