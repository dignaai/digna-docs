---
title: Konektor Databricks – integrace databáze | Dokumentace digna
description: Nakonfigurujte digna pro připojení k Databricks s Unity Catalog přes ODBC pomocí DSN-less připojovacího řetězce. Zahrnuje ovladač Databricks ODBC, osobní přístupové tokeny, HTTP path a nastavení připojení na straně digna.
image: /assets/logo_square.png
---

# Zdrojový konektor pro Databricks

Tento návod popisuje, jak nakonfigurovat *digna* pro připojení k Databricks přes **ODBC**
pomocí **DSN-less** připojovacího řetězce.

Strana nastavení týkající se *digna* je stejná pro všechny technologie — kde se připojení
vytvářejí, jak se šifrují hodnoty vlastností, jak se připojení testuje a co znamenají režimy
profilování. Je popsána v [Přehledu databázových připojení](overview.md). Tato stránka
pokrývá to, co je specifické pro Databricks.

!!! note "Unity Catalog je povinný"

    *digna* načítá dostupné katalogy z `system.information_schema.catalogs`, takže workspace
    musí mít povolený Unity Catalog. Dřívější verze *digna* nabízely pro workspace bez Unity
    Catalog samostatnou technologii „Databricks Legacy“; ta už není k dispozici.

---

## 1. Instalace ovladače ODBC {: #1-install-the-odbc-driver }

Nainstalujte **Databricks ODBC Driver** na počítač, na kterém běží backend *digna*, podle
[instalačního návodu Databricks](https://docs.databricks.com/aws/en/integrations/odbc/).

V závislosti na verzi se ovladač registruje jako **Simba Spark ODBC Driver** nebo jako
**Databricks ODBC Driver**. Přesný registrovaný název zjistěte na svém hostiteli podle postupu v
[Instalace ovladače ODBC na hostitele digna](overview.md#install-the-driver).

---

## 2. Získání údajů pro připojení {: #2-gather-the-connection-details }

Všechny hodnoty pocházejí ze SQL warehouse (nebo clusteru), který má *digna* používat. Otevřete
jej ve workspace Databricks a přejděte na **Connection details**:

| Pole v Databricks | Použije se jako |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, obvykle `443` |
| **HTTP path** | `HTTPPath` |

Pro ověřování vytvořte **osobní přístupový token** (personal access token) — viz
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Tokeny patří uživateli nebo service principalu a tento principal potřebuje na zdrojových datech
oprávnění `USE CATALOG`, `USE SCHEMA` a `SELECT`.

---

## 3. Vlastnosti ODBC {: #3-odbc-properties }

!!! important "Příklad, nikoli specifikace"

    Níže uvedená sada je jedna kombinace, o které je známo, že funguje. Vlastnosti patří
    ovladači Databricks/Simba, takže jejich názvy, výchozí hodnoty a přípustné hodnoty se liší
    mezi verzemi ovladače — ovladač byl vícekrát přejmenován a jeho možnosti ověřování
    rozšířeny — i mezi platformami. Použijte ji jako výchozí bod a řiďte se dokumentací
    nainstalované verze ovladače.

Na obrazovce **Add DB Connection** přidejte následující vlastnosti:

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Musí odpovídat názvu ovladače registrovanému na hostiteli *digna* |
| `Host` | `<workspace>.cloud.databricks.com` | Server hostname warehouse, např. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | HTTP path warehouse nebo clusteru |
| `SSL` | `1` | Endpointy Databricks fungují pouze přes TLS |
| `ThriftTransport` | `2` | Transport HTTP, který SQL endpointy používají |
| `AuthMech` | `3` | Ověřování tokenem |
| `UID` | `token` | Doslova slovo `token`, nikoli uživatelské jméno |
| `PWD` | `dapi…` | Osobní přístupový token. Zaškrtněte **Encrypted** |
| `UseNativeQuery` | `1` | Předává SQL z *digna* beze změny — viz níže |

Výsledný připojovací řetězec vypadá takto:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Ponechte `UseNativeQuery=1`"

    Při `UseNativeQuery=0` — výchozí hodnotě ovladače — ovladač přepisuje příchozí SQL do
    syntaxe, kterou považuje za přenositelnou syntaxi ODBC. *digna* už generuje Databricks SQL,
    takže přepis může změnit uvozování pomocí zpětných apostrofů a datumové literály a
    profilování pak selže na příkazech, které jsou v původní podobě platné.

### OAuth místo tokenu

Pro service principal s ověřováním OAuth machine-to-machine nahraďte `AuthMech`, `UID` a
`PWD` těmito vlastnostmi:

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Client credentials |
| `Auth_Client_ID` | `<application id>` | Service principal |
| `Auth_Client_Secret` | `<client secret>` | Zaškrtněte **Encrypted** |

---

## 4. Konfigurace *digna* {: #4-digna-configuration }

Na obrazovce **Add DB Connection** zadejte následující:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Poznámky k Databricks {: #5-notes-on-databricks }

- **Warehouse musí běžet** nebo se musí dát spustit, když se *digna* připojuje. Warehouse,
  který se probouzí ze zastaveného stavu, může potřebovat déle, než je časový limit připojení
  — pokud test po období nečinnosti selže napoprvé, zkuste to znovu.
- **Katalogy pocházejí z workspace.** Na rozdíl od většiny technologií dosáhne jedno připojení
  Databricks na všechny katalogy, které principal smí vidět, takže jediné připojení může
  obsluhovat zdroje napříč katalogy.
- **Režimy profilování.** *Permanent* vytváří pracovní tabulky ve **Work Schema** uvnitř
  katalogu zdroje, takže principal tam potřebuje oprávnění `CREATE TABLE`. *Session* používá
  `CREATE TEMPORARY TABLE` a **Work Schema** nepoužívá. *Standard* potřebuje pouze přístup pro
  čtení.
- **Serverless warehouse fungují** stejně; liší se pouze `HTTPPath`.

---

## 6. Ověření ovladače (volitelné) {: #6-verifying-the-driver-optional }

Konfigurace zdroje dat ODBC není pro DSN-less připojení nutná, ale vlastní dialog ovladače je
pohodlný způsob, jak ověřit, že ovladač, warehouse i token fungují, ještě než je zadáte do
*digna*.

#### Krok 1
![Krok 1](images/databricks/create_odbc_data_source_step1.png)

#### Krok 2
![Krok 2](images/databricks/create_odbc_data_source_step2.png)

#### Krok 3
![Krok 3](images/databricks/create_odbc_data_source_step3.png)

#### Krok 4
![Krok 4](images/databricks/create_odbc_data_source_step4.png)

#### Krok 5 – Otestování připojení

Klikněte na tlačítko **TEST**. Úspěšné připojení by mělo vypadat takto:

![Krok 5](images/databricks/create_odbc_data_source_step5.png)

Host, HTTP path a token, které zde zadáte, jsou přesně ty hodnoty, které přebírají vlastnosti v
[sekci 3](#3-odbc-properties).
