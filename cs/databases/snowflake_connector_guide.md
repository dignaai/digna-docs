# Zdrojový konektor pro Snowflake

Tento návod popisuje, jak nakonfigurovat *digna* pro připojení ke Snowflake přes **ODBC**
pomocí **DSN-less** připojovacího řetězce.

Strana nastavení týkající se *digna* je stejná pro všechny technologie — kde se připojení
vytvářejí, jak se šifrují hodnoty vlastností, jak se připojení testuje a co znamenají režimy
profilování. Je popsána v [Přehledu databázových připojení](overview.md). Tato stránka
pokrývá to, co je specifické pro Snowflake.

---

## 1. Instalace ovladače ODBC {: #1-install-the-odbc-driver }

Nainstalujte **Snowflake ODBC Driver** na počítač, na kterém běží backend *digna*, podle
[instalačního návodu Snowflake](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

Ovladač se registruje jako **SnowflakeDSIIDriver**. Přesný registrovaný název zjistěte na svém
hostiteli podle postupu v [Instalace ovladače ODBC na hostitele digna](overview.md#install-the-driver).

---

## 2. Vlastnosti ODBC {: #2-odbc-properties }

K Snowflake se připojuje pomocí **programového přístupového tokenu (PAT)** — to je způsob
ověřování, vůči kterému je *digna* ověřena, a zároveň ten, který Snowflake vyžaduje u účtů, na
kterých je přihlášení pouze heslem zablokováno.

!!! important "Příklad, nikoli specifikace"

    Níže uvedená sada je jedna kombinace, o které je známo, že funguje. Vlastnosti patří
    ovladači Snowflake ODBC, takže jejich názvy, výchozí hodnoty a přípustné hodnoty se liší
    mezi verzemi ovladače a platformami a o tom, které možnosti ověřování váš účet povoluje,
    rozhoduje bezpečnostní politika účtu. Použijte ji jako výchozí bod a řiďte se dokumentací
    nainstalované verze ovladače.

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Musí odpovídat názvu ovladače registrovanému na hostiteli *digna* |
| `Server` | `<account>.snowflakecomputing.com` | Identifikátor účtu plus přípona, např. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Uživatel Snowflake, kterému token patří |
| `Database` | `TEST` | Databáze obsahující zdrojová schémata. Je to jediná databáze, kterou toto připojení může profilovat |
| `Schema` | `PUBLIC` | Výchozí schéma relace |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Zvolí ověřování tokenem |
| `token` | `<programmatic access token>` | Zaškrtněte **Encrypted** |

Výsledný připojovací řetězec vypadá takto:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Warehouse a role

Dotazy potřebují warehouse. Pokud má uživatel *digna* výchozí warehouse a výchozí roli, relace
je převezme a není třeba nic konfigurovat. V opačném případě přidejte:

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Warehouse, ve kterém běží dotazy profilování |
| `Role` | `DIGNA_READER` | Role, jejíž oprávnění relace používá |

!!! tip "Dejte digna vlastní warehouse"

    Samostatný, malý warehouse s automatickým pozastavením udržuje náklady na profilování
    přehledné a zabraňuje tomu, aby *digna* soupeřila o výpočetní výkon s interaktivními
    uživateli.

### Ověřování heslem

Pokud to účet stále povoluje, funguje místo tokenu i heslo — odstraňte `authenticator` a
`token` a přidejte:

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `PWD` | `<password>` | Zaškrtněte **Encrypted** |

---

## 3. Konfigurace *digna* {: #3-digna-configuration }

Na obrazovce **Add DB Connection** zadejte následující:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Poznámky ke Snowflake {: #4-notes-on-snowflake }

- **Tokeny vyprší.** Programový přístupový token se vydává s omezenou platností a profilování
  se zastaví v den, kdy platnost skončí. Při vytváření si poznamenejte datum vypršení a nový
  token znovu zadejte do vlastnosti `token` — šifrované hodnoty lze nahradit, ale nelze je
  zpětně přečíst.
- **Jedno připojení vidí jednu databázi.** *digna* nabízí schémata databáze uvedené v
  `Database`, protože Snowflake hlásí jako katalog pouze aktuální databázi. Zdrojové tabulky v
  jiné databázi potřebují vlastní připojení.
- **Identifikátory jsou psány velkými písmeny**, pokud nebyly vytvořeny v uvozovkách. *digna*
  používá názvy tak, jak je Snowflake hlásí.
- **Režimy profilování.** *Permanent* vytváří pracovní tabulky ve **Work Schema**, takže role
  tam potřebuje oprávnění `CREATE TABLE`. *Session* používá `CREATE TEMPORARY TABLE` a
  **Work Schema** nepoužívá. *Standard* potřebuje pouze přístup pro čtení — a vůbec žádná
  oprávnění k zápisu.

---

## 5. Ověření ovladače (volitelné) {: #5-verifying-the-driver-optional }

Konfigurace zdroje dat ODBC není pro DSN-less připojení nutná, ale vlastní dialog ovladače je
pohodlný způsob, jak ověřit, že ovladač, URL účtu i vaše přihlašovací údaje fungují, ještě než
je zadáte do *digna*.

#### Krok 1
![Krok 1](images/snowflake/create_odbc_data_source_step1.png)

Poznámky:

- Hodnota pro **Server** se skládá z identifikátoru vašeho účtu Snowflake, za kterým následuje
  `.snowflakecomputing.com`.
- **Database**, **Schema** a **Warehouse** zadané zde odpovídají vlastnostem `Database`,
  `Schema` a `Warehouse` v [sekci 2](#2-odbc-properties).

#### Krok 2 – Otestování připojení

Klikněte na tlačítko **TEST**. Úspěšné připojení by mělo vypadat takto:

![Krok 2](images/snowflake/create_odbc_data_source_step2.png)