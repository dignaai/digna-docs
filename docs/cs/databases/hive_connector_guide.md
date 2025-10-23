---
title: Konektor Apache Hive – Integrace databáze | dokumentace digna
description: Nakonfigurujte digna pro připojení k Apache Hive pomocí nativního ovladače PyHive nebo ODBC ovladače Cloudera. Podporuje ověřování pomocí hesla a nastavení přes DSN nebo bez DSN.
image: /assets/logo_square.png
---


# Zdrojový konektor pro Hive

Tento průvodce popisuje, jak nakonfigurovat *digna* pro připojení k Hive buď pomocí nativního Python konektoru, nebo pomocí ODBC ovladače.

Odkazuje na obrazovku **"Vytvořit připojení k databázi"**.

![Vytvořit připojení k databázi](images/data_source_config_input_mask.png)

---

## Nativní Python ovladač

**Knihovna:** `PyHive`  
**Podporované ověřování:** Pouze ověřování pomocí hesla

> ⚠️ Pro jiné metody ověřování použijte prosím ODBC ovladač.

### Konfigurace *digna* (nativní ovladač)

Zadejte následující informace v obrazovce **"Vytvořit připojení k databázi"**:

```
Technology:      Apache Hive
Host Address:    Název serveru nebo IP adresa
Host Port:       Číslo portu, např. 10000
Database Name:   Schema obsahující zdrojová data
Schema Name:     Schema obsahující zdrojová data
User Name:       Uživatelské jméno databáze
User Password:   Heslo pro uživatele
Use ODBC:        Zakázáno (výchozí)
```

---

## ODBC ovladač

ODBC ovladač může podporovat širší škálu možností ověřování a konektivity. Tato sekce se zaměřuje na ověřování pomocí hesla s ovladačem **Cloudera ODBC Driver for Apache Hive**.

### 1. Instalace ODBC ovladače

Nainstalujte **Cloudera ODBC Driver for Apache Hive** (nebo podobný) podle oficiálního instalačního návodu dodavatele.

### 2. Konfigurace ODBC datového zdroje

Postupujte podle těchto kroků pro konfiguraci nového ODBC datového zdroje s ověřováním pomocí hesla:

#### Krok 1
![Krok 1](images/hive/create_odbc_data_source_step1.png)


#### Krok 2 – Test připojení

Zadejte heslo a klikněte na tlačítko **Test**.

![Krok 2](images/hive/create_odbc_data_source_step2.png)

Po úspěšném testu klikněte na tlačítko **OK**.

---

Nyní můžete nakonfigurovat *digna*, aby používalo ODBC připojení, buď s **DSN (Data Source Name)**, nebo v nastavení **bez DSN**.

---

### A. Konfigurace založená na DSN

#### Konfigurace *digna*

V obrazovce **"Vytvořit připojení k databázi"** zadejte následující:

```
Technology:      Apache Hive
Database Name:   Schema obsahující zdrojová data (shodné se Schema Name)
Schema Name:     Schema obsahující zdrojová data
Use ODBC:        Povoleno
```

#### Vlastnosti ODBC

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{vaše heslo v složených závorkách}"
```

> 🔹 Hodnota `DSN` musí odpovídat jménu definovanému ve vaší konfiguraci ODBC ovladače.

---

### B. Konfigurace bez DSN

#### Konfigurace *digna*

V obrazovce **"Vytvořit připojení k databázi"** zadejte následující:

```
Technology:      Apache Hive
Database Name:   Schema obsahující zdrojová data (shodné se Schema Name)
Schema Name:     Schema obsahující zdrojová data
Use ODBC:        Povoleno
```

#### Vlastnosti ODBC

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "název vašeho serveru nebo IP adresa"
name: "PORT",       value: "Číslo portu, např. 10000"
name: "Schema",     value: "Schema obsahující zdrojová data"
name: "UID",        value: "váš hive uživatel"
name: "PWD",        value: "vaše hive heslo"
name: "AuthMech",   value: "3"
```