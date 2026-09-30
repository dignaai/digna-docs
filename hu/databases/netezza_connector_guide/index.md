# Forráskonnektor Netezza-hoz

Ez az útmutató leírja, hogyan konfigurálhatja a *digna*-t a Netezza-hoz való csatlakozásra
**ODBC**-n keresztül, **DSN nélküli** kapcsolati karakterlánccal.

A beállítás *digna*-oldali része minden technológiánál ugyanaz — hol jönnek létre a
kapcsolatok, hogyan titkosíthatók a tulajdonságértékek, hogyan tesztelhető egy kapcsolat és mit
jelentenek a profilozási módok. Ezt az [Adatbázis-kapcsolatok áttekintése](overview.md) írja
le. Ez az oldal azt tárgyalja, ami a Netezza-ra jellemző.

---

## 1. Az ODBC illesztőprogram telepítése {: #1-install-the-odbc-driver }

Telepítse a **NetezzaSQL** ODBC illesztőprogramot (az IBM Netezza klienseszközök része) arra a
gépre, amely a *digna* backendet futtatja, a gyártó hivatalos telepítési útmutatója szerint.

Olvassa le a pontos regisztrált illesztőprogram-nevet a gépén, ahogyan az
[Az ODBC illesztőprogram telepítése a digna gépre](overview.md#install-the-driver) részben le
van írva.

---

## 2. ODBC tulajdonságok {: #2-odbc-properties }

!!! important "Példa, nem specifikáció"

    Az alábbi készlet egy olyan kombináció, amelyről ismert, hogy működik. A tulajdonságok a
    NetezzaSQL illesztőprogramhoz tartoznak, így nevük, alapértelmezett értékeik és az
    elfogadott értékek kliensverziónként és platformonként eltérnek, és egy TLS-sel védett
    appliance-hez több kell az itt bemutatott tulajdonságoknál. Használja ezt
    kiindulópontként, és nézze meg a telepített kliensverzió dokumentációját.

Adja hozzá a következő tulajdonságokat az **Add DB Connection** képernyőn:

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Egyeznie kell a *digna* gépen regisztrált illesztőprogram-névvel. A kapcsos zárójel a szokásos írásmódja ennek a névnek |
| `SERVER` | `netezza.example.com` | Szervernév vagy IP-cím |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Az adatbázis, amelyben a munkamenet indul |
| `UID` | `ADMIN` | Adatbázis-felhasználó |
| `PWD` | `<password>` | Jelölje be az **Encrypted** opciót |

Az így kapott kapcsolati karakterlánc így néz ki:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

Az illesztőprogram verziójától, a beállítástól és a biztonsági követelményektől függően további
tulajdonságokra lehet szükség — például `SecurityLevel` és `CaCertFile` egy TLS-sel védett
appliance esetén. Minden opció, amelyet az illesztőprogram *Advanced*, *SSL* és *Driver*
párbeszédablakai kínálnak, hozzáadható tulajdonságként.

---

## 3. *digna* konfiguráció {: #3-digna-configuration }

Az **Add DB Connection** képernyőn adja meg a következőket:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Megjegyzések a Netezza-hoz {: #4-notes-on-netezza }

- **Katalógusok és sémák egyaránt érvényesek.** A *digna* katalógusként listázza azokat az
  adatbázisokat, amelyeket a felhasználó láthat (a `_V_DATABASE` alapján), alattuk pedig a
  sémáikat (a `_V_SCHEMA` alapján), így egy kapcsolat több adatbázis forrásait is
  kiszolgálhatja. A `DATABASE` csak azt dönti el, hol indul a munkamenet.
- **Az azonosítók nagybetűsek**, hacsak nem idézőjelek között hozták létre őket, ezért
  használják a fenti példák a `TEST` és `ADMIN` neveket.
- **Profilozási módok.** A *Permanent* a munkatáblákat a **Work Schema**-ban hozza létre, ezért
  a felhasználónak ott `CREATE TABLE` jogosultság kell. A *Session* `CREATE TEMPORARY TABLE`-t
  használ, és nem érinti a **Work Schema**-t. A *Standard*-hoz csak olvasási hozzáférés
  szükséges.

---

## 5. Az illesztőprogram ellenőrzése (opcionális) {: #5-verifying-the-driver-optional }

ODBC adatforrás konfigurálása nem szükséges egy DSN nélküli kapcsolathoz, de az
illesztőprogram saját párbeszédablaka kényelmes módja annak, hogy megbizonyosodjon arról, hogy
az illesztőprogram és a hitelesítő adatai működnek, mielőtt megadná őket a *digna*-ban.

#### 1. lépés
![Step 1](images/netezza/create_odbc_data_source_step1.png)

A **DSN Options** mezői egy az egyben megfelelnek a [2. szakasz](#2-odbc-properties)
tulajdonságainak. A Netezza illesztőprogramtól, a beállítástól és a biztonsági
követelményektől függően az **Advanced DSN Options**, **SSL DSN Options** vagy
**Driver Options** füleken is szükség lehet adatokra; a legegyszerűbb beállításhoz a
**DSN Options** elegendő.

Kattintson a **Test Connection** gombra.

#### 2. lépés
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Amikor megjelenik a sikert jelző képernyő, az illesztőprogram működik, és az értékek helyesek.