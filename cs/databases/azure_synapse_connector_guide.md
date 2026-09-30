# Zdrojový konektor pro Azure Synapse Analytics

Tento návod popisuje, jak nakonfigurovat *digna* pro připojení k Azure Synapse Analytics přes
**ODBC** pomocí **DSN-less** připojovacího řetězce. Podporovány jsou serverless i dedicated SQL
pooly.

Strana nastavení týkající se *digna* je stejná pro všechny technologie — kde se připojení
vytvářejí, jak se šifrují hodnoty vlastností, jak se připojení testuje a co znamenají režimy
profilování. Je popsána v [Přehledu databázových připojení](overview.md). Tato stránka
pokrývá to, co je specifické pro Azure Synapse.

!!! note "Technologie"

    Synapse používá dialekt SQL Server, proto se připojení vytváří s **Technology:
    SQL Server**. Pro on-premises server viz [MS SQL Server](sqlserver_connector_guide.md).

---

## 1. Instalace ovladače ODBC {: #1-install-the-odbc-driver }

Nainstalujte **ODBC Driver 18 for SQL Server** na počítač, na kterém běží backend *digna*,
podle [instalačního návodu společnosti Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
a zjistěte přesný registrovaný název ovladače na svém hostiteli podle postupu v
[Instalace ovladače ODBC na hostitele digna](overview.md#install-the-driver).

---

## 2. Vlastnosti ODBC {: #2-odbc-properties }

!!! important "Příklad, nikoli specifikace"

    Níže uvedená sada je jedna kombinace, o které je známo, že funguje. Vlastnosti patří
    ovladači Microsoft ODBC, takže jejich názvy, výchozí hodnoty a přípustné hodnoty se liší
    mezi verzemi ovladače a platformami a to, co workspace vyžaduje, závisí na jeho konfiguraci
    — typu poolu, metodě ověřování a firewallu. Použijte ji jako výchozí bod a řiďte se
    dokumentací nainstalované verze ovladače.

Na obrazovce **Add DB Connection** přidejte následující vlastnosti:

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Musí odpovídat názvu ovladače registrovanému na hostiteli *digna* |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Název workspace plus přípona endpointu — viz níže |
| `DATABASE` | `dignadata` | Databáze obsahující zdrojová schémata. Je to jediná databáze, kterou toto připojení může profilovat |
| `UID` | `sqladminuser` | SQL login |
| `PWD` | `<password>` | Zaškrtněte **Encrypted** |

Výsledný připojovací řetězec vypadá takto:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### Hodnota `SERVER`

Vezměte název workspace Synapse a připojte k němu příponu endpointu:

| Pool | `SERVER` |
|---|---|
| **Serverless SQL pool** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Dedicated SQL pool** | `<workspace>.sql.azuresynapse.net` |

!!! warning "Část `-ondemand` se snadno přehlédne"

    Bez ní se název přeloží na dedicated endpoint a připojení buď selže, nebo se bez upozornění
    dostane k jinému poolu, než bylo zamýšleno. Oba endpointy jsou zobrazeny na stránce
    přehledu workspace na portálu Azure.

### Firewall

Firewall workspace Synapse musí povolit odchozí adresu hostitele *digna*. Přidejte ji v části
**Networking** ve workspace ještě před testováním připojení — blokovaná adresa se projeví jako
vypršení časového limitu připojení, nikoli jako chyba ověřování.

### Ověřování pomocí Microsoft Entra ID

Místo SQL loginu se ovladač může ověřovat vůči Entra ID. Nahraďte `UID`/`PWD` metodou
ověřování, kterou váš workspace očekává, například:

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | `UID` pak obsahuje ID aplikace (klienta) a `PWD` tajný klíč klienta |
| `Authentication` | `ActiveDirectoryMSI` | Spravovaná identita hostitele *digna*, nejsou potřeba žádné přihlašovací údaje |

---

## 3. Konfigurace *digna* {: #3-digna-configuration }

Na obrazovce **Add DB Connection** zadejte následující:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Poznámky k Azure Synapse {: #4-notes-on-azure-synapse }

- **Serverless pooly podporují pouze profilování *Standard*.** Serverless SQL pool nemůže v
  databázi vytvářet tabulky, takže nelze spustit profilování *Permanent* ani *Session*.
  *Standard* počítá metriky přímo na zdroji, což je zároveň levnější varianta, protože
  serverless se účtuje podle objemu zpracovaných dat.
- **Jedno připojení vidí jednu databázi.** *digna* nabízí schémata databáze uvedené v
  `DATABASE`, protože Synapse stejně jako SQL Server hlásí jako katalog pouze aktuální databázi.
- **Šifrování je ve Driver 18 ve výchozím stavu zapnuté** a endpointy Synapse předkládají
  platné veřejné certifikáty, takže vlastnost `Encrypt` ani `TrustServerCertificate` není
  potřeba.
- **Serverless endpoint se může při prvním připojení probouzet z nečinnosti.** Pokud test
  připojení vyprší u poolu, který se nějakou dobu nepoužíval, zkuste to znovu.

---

## 5. Ověření ovladače (volitelné) {: #5-verifying-the-driver-optional }

Konfigurace zdroje dat ODBC není pro DSN-less připojení nutná, ale vlastní průvodce ovladače je
pohodlný způsob, jak ověřit, že ovladač funguje a že workspace přijímá vaše přihlašovací údaje,
ještě než je zadáte do *digna*.

#### Krok 1
![Krok 1](images/azure_synapse/create_odbc_data_source_step1.png)

Vyplňte pole „Server“.
Použijte název workspace Synapse a doplňte ho o „.sql.azuresynapse.net“.  
**Pozor**, pokud se chcete připojit pomocí serverless SQL poolu, nezapomeňte uvést
„-ondemand“, jak je vidět na snímku obrazovky výše.

Klikněte na tlačítko **Next >**.

#### Krok 2
![Krok 2](images/azure_synapse/create_odbc_data_source_step2.png)

Zvolte metodu ověřování (např. uživatelské jméno a heslo)
a zadejte požadované údaje.

Klikněte na tlačítko **Next >**.

#### Krok 3
![Krok 3](images/azure_synapse/create_odbc_data_source_step3.png)

Zvolte nastavení kompatibilní s ANSI a poté klikněte na tlačítko **Next >**.

#### Krok 4
![Krok 4](images/azure_synapse/create_odbc_data_source_step4.png)

Můžete ponechat výchozí nastavení nebo zvolit možnosti podle potřeby
a kliknout na tlačítko **Finish**.

#### Krok 5
![Krok 5](images/azure_synapse/create_odbc_data_source_step5.png)

Nyní klikněte na tlačítko **Test datasource**.

#### Krok 6
![Krok 6](images/azure_synapse/create_odbc_data_source_step6.png)

Obrazovka s potvrzením úspěchu ukazuje, že ovladač, endpoint i přihlašovací údaje fungují.
Hodnoty, které jste zadali, jsou přesně ty hodnoty, které přebírají vlastnosti v
[sekci 2](#2-odbc-properties).