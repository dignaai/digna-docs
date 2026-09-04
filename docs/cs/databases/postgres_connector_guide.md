---
title: Konektor PostgreSQL – integrace databáze | Dokumentace digna
description: Nakonfigurujte digna tak, aby se připojil k PostgreSQL pomocí nativního Python ovladače psycopg nebo PostgreSQL ODBC ovladače. Podporuje ověřování pomocí hesla v konfiguracích s DSN nebo bez DSN.
image: /assets/logo_square.png
---


# Zdrojový konektor pro PostgreSQL

Tento návod popisuje, jak nakonfigurovat *digna* pro připojení k Postgresu pomocí buď nativního Python konektoru nebo ODBC ovladače.

Odkazuje na obrazovku **"Create a Database Connection"**.

![Vytvoření připojení k databázi](images/data_source_config_input_mask.png)

---

## Nativní Python ovladač

**Knihovna:** `psycopg`  
**Podporované ověřování:** Pouze ověřování pomocí hesla

> Pro jiné metody ověřování použijte prosím ODBC ovladač.

### Konfigurace *digna* (nativní ovladač)

Zadejte na obrazovce **"Create a Database Connection"** následující informace:

```
Technology:      Postgres
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 5432
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC ovladač

ODBC ovladač může podporovat širší škálu možností ověřování a konektivity. Tato sekce se zaměřuje na ověřování pomocí hesla s ovladačem **PostgreSQL Unicode(x64)**.

### 1. Instalace ODBC ovladače

Nainstalujte **PostgreSQL Unicode(x64)** (nebo obdobný) podle oficiální instalační příručky dodavatele.

### 2. Konfigurace ODBC zdroje dat

Postupujte podle těchto kroků pro konfiguraci nového ODBC zdroje dat s ověřováním pomocí hesla:

#### Krok 1
![Krok 1](images/postgres/create_odbc_data_source_step1.png)

Poznámka: Pokud vaše konfigurace databáze vyžaduje zadání konkrétního "SSLMode", ujistěte se, že jej použijete i při definování DSN-less konfigurace.

#### Krok 2 – Otestujte připojení

Klikněte na tlačítko **Test Connection**.

![Krok 2](images/postgres/create_odbc_data_source_step2.png)

---

Nyní můžete nakonfigurovat *digna*, aby používalo ODBC připojení, buď s **DSN (Data Source Name)**, nebo v konfiguraci **bez DSN (DSN-less)**.

---

### A. Konfigurace založená na DSN

#### Konfigurace *digna*

Na obrazovce **"Create a Database Connection"** zadejte následující:

```
Technology:      PostgreSQL
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Vlastnosti ODBC

```
name: "DSN",    value: "PostgreSQL35W"
```

> `DSN` musí odpovídat názvu definovanému ve vaší konfiguraci ODBC ovladače.

---

### B. Konfigurace bez DSN (DSN-less)

#### Konfigurace *digna*

Na obrazovce **"Create a Database Connection"** zadejte následující:

```
Technology:      PostgreSQL
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Vlastnosti ODBC

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```