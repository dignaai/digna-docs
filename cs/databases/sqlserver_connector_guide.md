# Zdrojový konektor pro MS SQL Server

Tento návod popisuje, jak nakonfigurovat *digna* pro připojení k Microsoft SQL Server přes
**ODBC** pomocí **DSN-less** připojovacího řetězce.

Strana nastavení týkající se *digna* je stejná pro všechny technologie — kde se připojení
vytvářejí, jak se šifrují hodnoty vlastností, jak se připojení testuje a co znamenají režimy
profilování. Je popsána v [Přehledu databázových připojení](overview.md). Tato stránka
pokrývá to, co je specifické pro SQL Server.

!!! note "Azure Synapse Analytics"

    Synapse se rovněž konfiguruje jako připojení SQL Server, s jiným názvem hostitele a
    několika dalšími specifiky — viz [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Instalace ovladače ODBC {: #1-install-the-odbc-driver }

Nainstalujte **ODBC Driver 18 for SQL Server** na počítač, na kterém běží backend *digna*,
podle [instalačního návodu společnosti Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

Ovladač dodávaný s Windows pod prostým názvem **SQL Server** také funguje, ale je dávno
zastaralý a nepodporuje moderní nastavení TLS ani ověřování Azure. Používejte jej pouze tam,
kde instalace aktuálního ovladače nepřichází v úvahu.

Přesný registrovaný název ovladače zjistěte na svém hostiteli podle postupu v
[Instalace ovladače ODBC na hostitele digna](overview.md#install-the-driver).

---

## 2. Vlastnosti ODBC {: #2-odbc-properties }

!!! important "Příklad, nikoli specifikace"

    Níže uvedená sada je jedna kombinace, o které je známo, že funguje. Vlastnosti patří
    ovladači Microsoft ODBC, takže jejich názvy, výchozí hodnoty a přípustné hodnoty se liší
    mezi verzemi ovladače — například Driver 18 ve výchozím stavu šifruje, zatímco Driver 17
    nikoli — i mezi platformami. Použijte ji jako výchozí bod a řiďte se dokumentací
    nainstalované verze ovladače.

Na obrazovce **Add DB Connection** přidejte následující vlastnosti:

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Musí odpovídat názvu ovladače registrovanému na hostiteli *digna* |
| `SERVER` | `sql.example.com` | Název serveru nebo IP adresa. Pojmenované instance: `host\instance`; jiný než výchozí port: `host,1433` |
| `PORT` | `1433` | Vynechte, pokud je port již součástí `SERVER` |
| `DATABASE` | `digna_source_db` | Databáze obsahující zdrojová schémata. Je to jediná databáze, kterou toto připojení může profilovat |
| `UID` | `digna_source_user` | Uživatel databáze |
| `PWD` | `<password>` | Zaškrtněte **Encrypted** |

Výsledný připojovací řetězec vypadá takto:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Šifrování s ODBC Driver 18

Driver 18 ve výchozím stavu šifruje připojení a ověřuje certifikát serveru. U serveru s
certifikátem, kterému váš hostitel *digna* nedůvěřuje — typicky u certifikátu podepsaného sám
sebou — připojení selže s chybou řetězu certifikátů. Přidejte:

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `Encrypt` | `yes` | Výchozí v Driver 18; nastavte na `no` pouze tehdy, když server nepodporuje TLS |
| `TrustServerCertificate` | `yes` | Přeskočí ověření certifikátu. Praktické v testovacích prostředích; v produkci raději nainstalujte certifikát |

### Ověřování Windows

Chcete-li se místo SQL loginu připojit jako účet, pod kterým běží služba *digna*, odstraňte
`UID` a `PWD` a přidejte:

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `Trusted_Connection` | `yes` | Servisní účet *digna* potřebuje oprávnění k databázi |

---

## 3. Konfigurace *digna* {: #3-digna-configuration }

Na obrazovce **Add DB Connection** zadejte následující:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Poznámky k MS SQL Server {: #4-notes-on-ms-sql-server }

- **Jedno připojení vidí jednu databázi.** *digna* nabízí schémata databáze uvedené v
  `DATABASE`, protože SQL Server hlásí jako katalog pouze aktuální databázi. Zdrojové tabulky v
  jiné databázi potřebují vlastní připojení.
- **Režimy profilování.** *Permanent* vytváří pracovní tabulky ve **Work Schema**, takže
  uživatel tam potřebuje oprávnění `CREATE TABLE`. *Session* používá lokální dočasné tabulky
  (`#wt_…`) v `tempdb` a **Work Schema** nepoužívá. *Standard* potřebuje pouze přístup pro
  čtení.
- **`SERVER` nese instanci i port.** U pojmenované instance vyžaduje `host\instance`
  dostupnost služby SQL Server Browser; `host,port` se tomu vyhne.

---

## 5. Ověření ovladače (volitelné) {: #5-verifying-the-driver-optional }

Konfigurace zdroje dat ODBC není pro DSN-less připojení nutná, ale vlastní průvodce ovladače je
pohodlný způsob, jak ověřit, že ovladač funguje a že server přijímá vaše přihlašovací údaje,
ještě než je zadáte do *digna*.

#### Krok 1
![Krok 1](images/sqlserver/create_odbc_data_source_step1.png)

Klikněte na tlačítko **Next >**.

#### Krok 2
![Krok 2](images/sqlserver/create_odbc_data_source_step2.png)

Zvolte metodu ověřování (např. uživatelské jméno a heslo)
a zadejte požadované údaje.

Klikněte na tlačítko **Next >**.

#### Krok 3
![Krok 3](images/sqlserver/create_odbc_data_source_step3.png)

Zvolte nastavení kompatibilní s ANSI a poté klikněte na tlačítko **Next >**.

#### Krok 4
![Krok 4](images/sqlserver/create_odbc_data_source_step4.png)

Můžete ponechat výchozí nastavení nebo zvolit možnosti protokolování podle potřeby
a kliknout na tlačítko **Finish**.

#### Krok 5
![Krok 5](images/sqlserver/create_odbc_data_source_step5.png)

Nyní klikněte na tlačítko **Test datasource**.

#### Krok 6
![Krok 6](images/sqlserver/create_odbc_data_source_step6.png)

Obrazovka s potvrzením úspěchu ukazuje, že ovladač i přihlašovací údaje fungují. Hodnoty, které
jste zadali, jsou přesně ty hodnoty, které přebírají vlastnosti v
[sekci 2](#2-odbc-properties).