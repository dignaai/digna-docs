---
title: MS SQL Server Connector – Database Integration | digna Documentation
description: Nakonfigurujte digna pro připojení k Microsoft SQL Serveru pomocí Python ovladače pymssql nebo ODBC ovladače SQL Server. Podporuje ověřování založené na hesle s DSN nebo DSN-less nastavením.
image: /assets/logo_square.png
---


# Source Connector for MS SQL Server

Tento průvodce popisuje, jak nakonfigurovat *digna* pro připojení k SQL Serveru buď pomocí nativního Python konektoru, nebo pomocí ODBC ovladače.

Odkazuje na obrazovku **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Supported Authentication:** Pouze ověřování založené na hesle

> ⚠️ Pro jiné metody ověřování prosím použijte ODBC ovladač.

### *digna* Configuration (Native Driver)

Zadejte následující informace v obrazovce **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    Název serveru nebo IP adresa
Host Port:       Číslo portu, např. 1433
Database Name:   Název databáze
Schema Name:     Schéma, které obsahuje zdrojová data
User Name:       Uživatelské jméno databáze
User Password:   Heslo pro uživatele
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC ovladač může podporovat širší škálu možností ověřování a konektivity. Tato sekce se zaměřuje na ověřování založené na hesle pomocí ovladače **SQL Server**.

### 1. Install the ODBC Driver

Nainstalujte ovladač **SQL Server** (nebo podobný) podle oficiální instalační příručky dodavatele.

### 2. Configure the ODBC Data Source

Postupujte podle následujících kroků pro konfiguraci nového ODBC data source s ověřováním založeným na hesle:

#### Step 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Klikněte na tlačítko **Next >**.

#### Step 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Vyberte metodu ověřování (např. uživatelské jméno a heslo) a zadejte požadovaná data.

Klikněte na tlačítko **Next >**.

#### Step 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Zvolte nastavení kompatibilní s ANSI a poté klikněte na tlačítko **Next >**.

#### Step 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Můžete ponechat výchozí nastavení nebo podle potřeby zvolit možnosti logování a kliknout na tlačítko **Finish**.

#### Step 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Nyní klikněte na tlačítko ** Test datasource **.

#### Step 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

Když obdržíte obrazovku s úspěchem, ODBC je správně nakonfigurováno.

---

Nyní můžete nakonfigurovat *digna*, aby používalo ODBC připojení, buď s **DSN (Data Source Name)** nebo v **DSN-less** režimu.

---

### A. DSN-Based Configuration

#### *digna* Configuration

V obrazovce **"Create a Database Connection"** zadejte následující:

```
Technology:      MS SQL Server
Database Name:   Databáze, která obsahuje zdrojové schéma
Schema Name:     Schéma, které obsahuje zdrojová data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

> 🔹 The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less Configuration

#### *digna* Configuration

V obrazovce **"Create a Database Connection"** zadejte následující:

```
Technology:      MS SQL Server
Database Name:   Schéma, které obsahuje zdrojová data (stejné jako Schema Name)
Schema Name:     Schéma, které obsahuje zdrojová data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```