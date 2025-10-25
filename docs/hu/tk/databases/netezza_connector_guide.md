---
title: Netezza csatlakozó – Adatbázis-integráció | digna dokumentáció
description: A digna konfigurálása Netezza-hez való csatlakozáshoz a NetezzaSQL ODBC-illesztőprogram használatával. Támogatja a jelszó alapú hitelesítést DSN vagy DSN-less beállításokkal.
image: /assets/logo_square.png
---


# Netezza forrás csatlakozó

Ez az útmutató azt ismerteti, hogyan konfigurálja a *digna*-t, hogy ODBC-illesztőprogramon keresztül csatlakozzon Netezza-hez.

A képernyő az "Adatbázis-kapcsolat létrehozása" képernyőre utal.

![Adatbázis-kapcsolat létrehozása](images/data_source_config_input_mask.png)

---

## ODBC illesztőprogram

Az ODBC-illesztőprogram különböző hitelesítési és kapcsolódási lehetőségeket támogathat. Ez a rész a jelszó alapú hitelesítésre összpontosít, az NetezzaSQL illesztőprogram használatával.

### 1. ODBC illesztőprogram telepítése

Telepítse a gyártó hivatalos telepítési útmutatója szerint a **NetezzaSQL** (vagy hasonló) illesztőprogramot.

### 2. ODBC adatforrás konfigurálása

Új ODBC adatforrás konfigurálásához jelszó alapú hitelesítéshez kövesse az alábbi lépéseket:

#### 1. lépés
![1. lépés](images/netezza/create_odbc_data_source_step1.png)

Előfordulhat, hogy a Netezza illesztőprogram esetén a telepítési és biztonsági követelmények függvényében további beállításokat kell megadnia az **Advanced DSN Options**, **SSL DSN Options** vagy **Driver Options** fülön. Az alap telepítéshez általában elegendő a **DSN Options** szekció kitöltése.

Kattintson a "Test Connection" gombra.

#### 2. lépés
![2. lépés](images/netezza/create_odbc_data_source_step2.png)

Ha megjelenik a siker képernyő, az ODBC megfelelően konfigurálva van.

---

Most már konfigurálhatja a *digna*-t úgy, hogy az ODBC-kapcsolatot használja; akár **DSN (Data Source Name)**-nel, akár **DSN-less** beállítással.

---

### A. DSN alapú konfiguráció

#### *digna* konfigurációja

Az "Adatbázis-kapcsolat létrehozása" képernyőn adja meg a következőket:

```
Technológia:     Netezza
Adatbázis neve:  Az a adatbázis, amely a forrás sémát tartalmazza
Séma neve:       A forrás adatokat tartalmazó séma
ODBC használat:  Engedélyezve
```

#### ODBC tulajdonságai

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "adatbázis felhasználóneve"
name: "PWD",        value: "adatbázis jelszava"
```

> 🔹 `DSN`-nek meg kell egyeznie az ODBC-illesztőprogram konfigurációjában megadott névvel.

---

### B. DSN-less konfiguráció

#### *digna* konfigurációja

Az "Adatbázis-kapcsolat létrehozása" képernyőn adja meg a következőket:

```
Technológia:     Netezza
Adatbázis neve:  A forrás adatokat tartalmazó séma (ugyanaz, mint a séma neve)
Séma neve:       A forrás adatokat tartalmazó séma
ODBC használat:  Engedélyezve
```

#### ODBC tulajdonságai

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "szerver neve vagy IP-címe"
name: "PORT",       value: "Port száma, pl. 5480"
name: "DATABASE",   value: "annak az adatbázisnak a neve, amely a forrás sémát tartalmazza"
name: "UID",        value: "adatbázis felhasználóneve"
name: "PWD",        value: "adatbázis jelszava"
```