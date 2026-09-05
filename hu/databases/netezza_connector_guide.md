# Netezza forráskapcsoló

Ez az útmutató leírja, hogyan konfigurálja a *digna*-t a Netezza-hez való csatlakozáshoz az ODBC-illesztőprogram használatával.

A következő képernyőre hivatkozik: **„Adatbázis-kapcsolat létrehozása”**.

![Adatbázis-kapcsolat létrehozása](images/data_source_config_input_mask.png)

---

## ODBC-illesztőprogram

Az ODBC-illesztőprogram különféle hitelesítési és csatlakozási lehetőségeket támogathat. Ez a rész a jelszó alapú hitelesítésre összpontosít a **NetezzaSQL** illesztőprogram használatával.

### 1. Telepítse az ODBC-illesztőprogramot

Telepítse a **NetezzaSQL** (vagy hasonló) illesztőprogramot a gyártó hivatalos telepítési útmutatójának megfelelően.

### 2. Az ODBC adatforrás konfigurálása

Kövesse az alábbi lépéseket egy új ODBC adatforrás konfigurálásához jelszó alapú hitelesítéssel:

#### 1. lépés
![1. lépés](images/netezza/create_odbc_data_source_step1.png)

A Netezza-illesztőprogramtól, a telepítési és biztonsági követelményektől függően előfordulhat, hogy adatokat kell megadnia az **Advanced DSN Options**, **SSL DSN Options** vagy **Driver Options** lapokon is. A legegyszerűbb beállításhoz elegendő adatok megadása a **DSN Options** lapon.

Kattintson a **Test Connection** gombra.

#### 2. lépés
![2. lépés](images/netezza/create_odbc_data_source_step2.png)

Ha megjelenik a sikeres csatlakozás képernyője, az ODBC megfelelően van konfigurálva.

---

Most konfigurálhatja a *digna*-t az ODBC-kapcsolat használatára, akár **DSN (Data Source Name)**, akár **DSN-less** beállítással.

---

### A. DSN-alapú konfiguráció

#### *digna* konfiguráció

A **„Create a Database Connection”** képernyőn adja meg a következőket:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> A `DSN`-nek meg kell egyeznie az ODBC illesztőprogram konfigurációjában definiált névvel.

---

### B. DSN nélküli konfiguráció

#### *digna* konfiguráció

A **„Create a Database Connection”** képernyőn adja meg a következőket:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```