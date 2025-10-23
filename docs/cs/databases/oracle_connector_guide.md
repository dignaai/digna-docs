---
title: Konektor Oracle – integrace databáze | digna Dokumentace
description: Nakonfigurujte digna pro připojení k Oracle pomocí python-oracledb nebo Oracle ODBC ovladače. Podporuje ověřování pomocí hesla s DSN i bez DSN.
image: /assets/logo_square.png
---


# Source Connector for Oracle

Tento návod popisuje, jak nakonfigurovat *digna* pro připojení k Oracle DB buď pomocí nativního Python konektoru, nebo pomocí ODBC ovladače.

Odkazuje na obrazovku **"Create a Database Connection"**.

![Vytvoření připojení k databázi](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `python-oracledb`  
**Supported Authentication:** Password-based authentication only

> ⚠️ Pro jiné metody ověřování použijte prosím ODBC ovladač.

### *digna* Configuration (Native Driver)

Zadejte následující informace na obrazovce **"Create a Database Connection"**:

```
Technology:      Oracle
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1521
Database Name:   Instance name, service name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC ovladač může podporovat širší škálu možností ověřování a konektivity. Tato sekce se zaměřuje na ověřování pomocí hesla s ovladačem **Oracle in OraDB21Home1**.

### 1. Install the ODBC Driver

Nainstalujte **Oracle in OraDB21Home1** (nebo podobný) podle oficiální instalační příručky dodavatele.

### 2. Configure the ODBC Data Source

Postupujte podle těchto kroků pro konfiguraci nového ODBC datového zdroje s ověřováním pomocí hesla:

#### Step 1
![Krok 1](images/oracle/create_odbc_data_source_step1.png)

Poznámka:
TNS Service Name musí být nakonfigurován v souboru tnsnames.ora vaší instalace Oracle klienta. Zde zadáte popis připojení (host, port, service name).

#### Step 2 – Test the connection

Klikněte na tlačítko **Test Connection**.

![Krok 2](images/oracle/create_odbc_data_source_step2.png)

Zadejte heslo a klikněte na tlačítko **OK**.

![Krok 2](images/oracle/create_odbc_data_source_step3.png)

---

Nyní můžete nakonfigurovat *digna*, aby používalo ODBC připojení, buď s **DSN (Data Source Name)** nebo v **DSN-less** režimu.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Na obrazovce **"Create a Database Connection"** zadejte následující:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> 🔹 `DSN` musí odpovídat názvu definovanému ve vaší konfiguraci ODBC ovladače.

---

### B. DSN-less Configuration

#### *digna* Configuration

Na obrazovce **"Create a Database Connection"** zadejte následující:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```