# Source Connector for Teradata

Tento průvodce popisuje, jak nakonfigurovat *digna* pro připojení k Teradata buď pomocí nativního Python konektoru, nebo ODBC driveru.

Odkazuje na obrazovku **"Vytvoření připojení k databázi"**.

![Vytvoření připojení k databázi](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Knihovna:** `teradatasql`  
**Podporovaná autentizace:** Pouze autentizace pomocí hesla

> Pro jiné metody autentizace použijte prosím ODBC driver.

### *digna* konfigurace (nativní driver)

Do obrazovky **"Vytvoření připojení k databázi"** zadejte následující informace:

```
Technologie:      Teradata
Adresa serveru:   Název serveru nebo IP adresa
Port:             Číslo portu, např. 1025
Název databáze:   Název databáze
Název schématu:   Název schématu
Uživatelské jméno: Uživatelské jméno databáze
Uživatelské heslo: Heslo pro uživatele
Použít ODBC:      Zakázáno (výchozí)
```

---

## ODBC Driver

ODBC driver může podporovat širší škálu možností autentizace a konektivity. Tato sekce se zaměřuje na autentizaci pomocí hesla s ovladačem **Teradata Database ODBC Driver 20.00**.

### 1. Instalace ODBC driveru

Nainstalujte ovladač **Teradata Database ODBC Driver 20.00** (nebo podobný) podle oficiální instalační příručky dodavatele.

### 2. Konfigurace ODBC datového zdroje

Postupujte podle těchto kroků pro konfiguraci nového ODBC datového zdroje s autentizací pomocí hesla:

#### Krok 1
![Krok 1](images/teradata/create_odbc_data_source_step1.png)

Klikněte na tlačítko **Test**.

#### Krok 2
![Krok 2](images/teradata/create_odbc_data_source_step2.png)

Zadejte uživatelské jméno a heslo.

Klikněte na tlačítko **OK**.  
Po zobrazení potvrzující obrazovky je ODBC správně nakonfigurováno.

---

Nyní můžete nakonfigurovat *digna*, aby používalo ODBC připojení, buď s **DSN (Data Source Name)**, nebo v nastavení **DSN-less**.

---

### A. Konfigurace založená na DSN

#### *digna* konfigurace

Do obrazovky **"Vytvoření připojení k databázi"** zadejte následující:

```
Technologie:      Teradata
Název databáze:   Databáze, která obsahuje zdrojové schéma
Název schématu:   Schéma, které obsahuje zdrojová data
Použít ODBC:      Povolen
```

#### Vlastnosti ODBC

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "váš uživatel databáze"
name: "PWD",        value: "vaše databázové heslo"
```

> Hodnota `DSN` musí odpovídat názvu definovanému v konfiguraci vašeho ODBC driveru.

---

### B. Konfigurace bez DSN

#### *digna* konfigurace

Do obrazovky **"Vytvoření připojení k databázi"** zadejte následující:

```
Technologie:      Teradata
Název databáze:   Schéma, které obsahuje zdrojová data (stejné jako Název schématu)
Název schématu:   Schéma, které obsahuje zdrojová data
Použít ODBC:      Povolen
```

#### Vlastnosti ODBC

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "název vašeho serveru nebo IP adresa"
name: "UID",        value: "váš uživatel databáze"
name: "PWD",        value: "vaše databázové heslo"
```