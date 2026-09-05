# Zdrojový konektor pro Netezza

Tento průvodce popisuje, jak nakonfigurovat *digna* pro připojení k Netezza pomocí ODBC ovladače.

Odkazuje na obrazovku **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## ODBC ovladač

ODBC ovladač může podporovat řadu možností ověřování a konektivity. Tato sekce se zaměřuje na ověřování pomocí hesla s ovladačem **NetezzaSQL**.

### 1. Nainstalujte ODBC ovladač

Nainstalujte ovladač **NetezzaSQL** (nebo podobný) podle oficiální instalační příručky dodavatele.

### 2. Konfigurujte ODBC datový zdroj

Postupujte podle těchto kroků pro konfiguraci nového ODBC datového zdroje s použitím ověřování pomocí hesla:

#### Krok 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

V závislosti na vašem Netezza ovladači, požadavcích na nastavení a zabezpečení možná budete muset také zadat údaje v záložkách **Advanced DSN Options**, **SSL DSN Options** nebo **Driver Options**. Pro nejjednodušší nastavení stačí zadat údaje v **DSN Options**.

Klikněte na tlačítko **Test Connection**.

#### Krok 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Po zobrazení obrazovky potvrzující úspěch je ODBC správně nakonfigurováno.

---

Nyní můžete nakonfigurovat *digna*, aby používalo ODBC připojení, buď s **DSN (Data Source Name)**, nebo v konfiguraci **bez DSN**.

---

### A. Konfigurace založená na DSN

#### *digna* konfigurace

Na obrazovce **"Create a Database Connection"** zadejte následující:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC vlastnosti

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> `DSN` musí odpovídat názvu definovanému ve vaší konfiguraci ODBC ovladače.

---

### B. Konfigurace bez DSN

#### *digna* konfigurace

Na obrazovce **"Create a Database Connection"** zadejte následující:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC vlastnosti

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```