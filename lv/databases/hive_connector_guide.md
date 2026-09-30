# Avota konektors Hive

Šajā ceļvedī aprakstīts, kā konfigurēt *digna* savienojumu ar Apache Hive caur **ODBC**,
izmantojot savienojuma virkni **bez DSN** (DSN-less).

Iestatīšanas *digna* puse ir vienāda katrai tehnoloģijai — kur tiek veidoti savienojumi,
kā tiek šifrētas rekvizītu vērtības, kā tiek testēts savienojums un ko nozīmē profilēšanas
režīmi. Tā ir aprakstīta lapā [Datubāzu savienojumu pārskats](overview.md). Šī lapa aptver to,
kas raksturīgs tieši Hive.

---

## 1. Instalēt ODBC draiveri {: #1-install-the-odbc-driver }

Instalējiet **Cloudera ODBC Driver for Apache Hive** datorā, kurā darbojas *digna*
backend, sekojot piegādātāja oficiālajam instalēšanas ceļvedim.

Nolasiet precīzu reģistrēto draivera nosaukumu savā resursdatorā, kā aprakstīts sadaļā
[Instalēt ODBC draiveri digna resursdatorā](overview.md#install-the-driver).

---

## 2. ODBC rekvizīti {: #2-odbc-properties }

!!! important "Piemērs, nevis specifikācija"

    Tālāk norādītā kopa ir viena kombinācija, par kuru zināms, ka tā darbojas. Rekvizīti pieder
    Cloudera Hive draiverim, tāpēc to nosaukumi, noklusējuma vērtības un pieņemtās vērtības
    atšķiras starp draivera versijām un platformām, un tas, ko pieņem HiveServer2, pilnībā ir
    atkarīgs no klastera aizsardzības — autentifikācijas mehānisma, transporta režīma, TLS,
    vārtejas. Izmantojiet to kā sākumpunktu un pārbaudiet jūsu instalētās draivera versijas dokumentāciju.

Ekrānā **Add DB Connection** pievienojiet šādus rekvizītus:

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Jāatbilst draivera nosaukumam, kas reģistrēts *digna* resursdatorā |
| `HOST` | `hive.example.com` | HiveServer2 resursdatora nosaukums vai IP adrese |
| `PORT` | `10000` | HiveServer2 ports; `10001` HTTP transportam |

Iegūtā savienojuma virkne izskatās šādi:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Autentifikācija

Neaizsargāts HiveServer2 pieņem trīs iepriekš minētos rekvizītus tādus, kādi tie ir. Ja
autentifikācija ir iespējota, pievienojiet:

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `AuthMech` | `3` | `0` bez autentifikācijas, `2` tikai lietotājvārds, `3` lietotājvārds un parole, `1` Kerberos |
| `UID` | `digna_source_user` | Nepieciešams `AuthMech` `2` un `3` |
| `PWD` | `<password>` | Nepieciešams `AuthMech` `3`. Atzīmējiet **Encrypted** |

Kerberos gadījumā (`AuthMech=1`) *digna* resursdatoram papildus nepieciešama derīga biļete vai
keytab, kā arī draivera dokumentētie rekvizīti `KrbHostFQDN`, `KrbServiceName` un `KrbRealm`.

### Transports un TLS

| Atslēga | Vērtības piemērs | Piezīmes |
|---|---|---|
| `ThriftTransport` | `2` | `0` binārais (noklusējums, ports 10000), `1` SASL, `2` HTTP (ports 10001, un to sagaida Knox vārteja) |
| `HTTPPath` | `cliservice` | Kopā ar `ThriftTransport=2` |
| `SSL` | `1` | Ja HiveServer2 ir aizsargāts ar TLS |
| `Schema` | `dignadata` | Hive datubāze, kurā sākas sesija. Nav obligāti — *digna* kvalificē savus vaicājumus |

---

## 3. *digna* konfigurācija {: #3-digna-configuration }

Ekrānā **Add DB Connection** norādiet šādus datus:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Piezīmes par Hive {: #4-notes-on-hive }

- **Katalogi nāk no draivera.** Hive nav sava kataloga, tāpēc *digna* izmanto to, ko norāda
  draiveris — parasti vienu ierakstu ar nosaukumu `HIVE` — un zem tā uzskaita Hive datubāzes
  kā shēmas.
- **Work Schema ir Hive datubāze.** *Permanent* profilēšanai lietotājam nepieciešamas tiesības
  tajā izveidot un dzēst tabulas, un pamatā esošajai krātuves vietai jābūt rakstāmai.
- **Profilēšanas režīmi.** *Permanent* izveido darba tabulas shēmā **Work Schema**. *Session*
  izmanto `CREATE TEMPORARY TABLE`, kam nepieciešams HiveServer2 ar pagaidu tabulu atbalstu,
  un neskar **Work Schema**. *Standard* nepieciešama tikai lasīšanas piekļuve, un tas ir režīms,
  kas jāizvēlas klasterī, kurā *digna* vispār nav rakstīšanas piekļuves.
- **Profilēšana ir vaicājumu kopa, nevis skenēšana.** Katru statistiku aprēķina HiveServer2,
  tāpēc rindai (queue), kurā *digna* lietotājs iesniedz vaicājumus, jābūt pietiekamai kapacitātei
  inspekcijas laika logam.

---

## 5. Draivera pārbaude (pēc izvēles) {: #5-verifying-the-driver-optional }

Savienojumam bez DSN nav jākonfigurē ODBC datu avots, taču paša draivera dialogs ir ērts veids,
kā pārliecināties, ka draiveris, transporta režīms un jūsu akreditācijas dati darbojas, pirms
tos ievadāt *digna*.

#### 1. solis
![Step 1](images/hive/create_odbc_data_source_step1.png)

Šeit redzamie lauki **Host**, **Port**, **Database**, **Mechanism** un **Thrift Transport**
atbilst rekvizītiem `HOST`, `PORT`, `Schema`, `AuthMech` un `ThriftTransport`
[2. sadaļā](#2-odbc-properties).

#### 2. solis – Testēt savienojumu

Norādiet paroli un noklikšķiniet uz pogas **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Pēc veiksmīga testa noklikšķiniet uz pogas **OK**.