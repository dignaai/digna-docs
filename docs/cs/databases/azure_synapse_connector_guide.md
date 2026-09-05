---
title: Konektor Azure Synapse – Integrace databáze | dokumentace digna
description: Nakonfigurujte digna pro připojení k Azure Synapse Analytics pomocí nativního Python konektoru nebo ODBC ovladače. Podporuje jak serverless, tak dedikované SQL pooly.
image: /assets/logo_square.png
---


# Source Connector for Azure Synapse Analytics

Tento návod popisuje, jak nakonfigurovat *digna* pro připojení k Azure Synapse Analytics pomocí buď nativního Python konektoru, nebo ODBC ovladače.
Podporuje jak serverless, tak dedikované SQL pooly.

Odkazuje na obrazovku **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Supported Authentication:** Pouze ověřování pomocí hesla

> Pro jiné metody ověřování použijte prosím ODBC ovladač.

### *digna* Configuration (Native Driver)

Zadejte následující informace na obrazovce **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC ovladač může podporovat širší škálu možností ověřování a konektivity. Tato sekce se zaměřuje na ověřování pomocí hesla s ovladačem **ODBC Driver 18 for SQL Server**.

### 1. Instalace ODBC ovladače

Nainstalujte ovladač **ODBC Driver 18 for SQL Server** (nebo obdobný) podle oficiální instalační příručky dodavatele.

### 2. Konfigurace ODBC datového zdroje

Postupujte podle těchto kroků pro konfiguraci nového ODBC datového zdroje pomocí ověřování pomocí hesla:

#### Krok 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Vyplňte pole "Server".
Použijte název Synapse workspace a doplňte ho o ".sql.azuresynapse.net".  
**Pozor**, pokud se chcete připojit pomocí serverless SQL poolu, nezapomeňte zahrnout "-ondemand", jak je uvedeno na obrázku níže.

Klikněte na tlačítko **Next >**.

#### Krok 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Vyberte metodu ověřování (např. uživatelské jméno a heslo)
a zadejte požadovaná data.

Klikněte na tlačítko **Next >**.

#### Krok 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Zvolte nastavení kompatibilní s ANSI a poté klikněte na tlačítko **Next >**.

#### Krok 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Můžete ponechat výchozí nastavení nebo zvolit požadované volby
a kliknout na tlačítko **Finish**.

#### Krok 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Nyní klikněte na tlačítko ** Test datasource **.

#### Krok 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Když se zobrazí obrazovka úspěchu, ODBC je správně nakonfigurován.

---

Nyní můžete nakonfigurovat *digna*, aby používala ODBC připojení, buď s **DSN (Data Source Name)**, nebo bez DSN (DSN-less).

---

### A. Konfigurace založená na DSN

#### *digna* Configuration

Na obrazovce **"Create a Database Connection"** zadejte následující:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> `DSN` musí odpovídat názvu definovanému ve vaší konfiguraci ODBC ovladače.

---

### B. Konfigurace bez DSN (DSN-less)

#### *digna* Configuration

Na obrazovce **"Create a Database Connection"** zadejte následující:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Poznámka** k vlastnosti SERVER:  
Použijte název Synapse workspace a doplňte ho o ".sql.azuresynapse.net". Pokud se chcete připojit pomocí serverless SQL poolu, nezapomeňte zahrnout "-ondemand", jak je uvedeno na obrázku níže.