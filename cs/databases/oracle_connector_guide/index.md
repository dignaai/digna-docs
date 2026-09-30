# Zdrojový konektor pro Oracle

Tento návod popisuje, jak nakonfigurovat *digna* pro připojení k Oracle Database přes **ODBC**
pomocí **DSN-less** připojovacího řetězce.

Strana nastavení týkající se *digna* je stejná pro všechny technologie — kde se připojení
vytvářejí, jak se šifrují hodnoty vlastností, jak se připojení testuje a co znamenají režimy
profilování. Je popsána v [Přehledu databázových připojení](overview.md). Tato stránka
pokrývá to, co je specifické pro Oracle.

---

## 1. Instalace ovladače ODBC {: #1-install-the-odbc-driver }

Ovladač Oracle ODBC je součástí **Oracle Client** (stačí balíček „ODBC“ z Instant Client).
Nainstalujte jej na počítač, na kterém běží backend *digna*, podle oficiálního instalačního
návodu dodavatele.

Ovladač se registruje jako **Oracle in `<OracleHomeName>`** — například
`Oracle in OraDB21Home1` nebo `Oracle in instantclient_21_13`. Název home se liší podle
instalace, proto přesný název zjistěte na svém hostiteli podle postupu v
[Instalace ovladače ODBC na hostitele digna](overview.md#install-the-driver).

---

## 2. Vlastnosti ODBC {: #2-odbc-properties }

!!! important "Příklad, nikoli specifikace"

    Níže uvedená sada je jedna kombinace, o které je známo, že funguje. Vlastnosti patří
    ovladači Oracle ODBC, takže jejich názvy, výchozí hodnoty a přípustné hodnoty se liší mezi
    verzemi klienta a zejména název ovladače závisí na Oracle home na vašem hostiteli. Použijte
    ji jako výchozí bod a řiďte se dokumentací nainstalované verze klienta.

Na obrazovce **Add DB Connection** přidejte následující vlastnosti:

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Musí odpovídat názvu ovladače registrovanému na hostiteli *digna* |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Databáze, ke které se připojuje — viz níže |
| `UID` | `DIGNA_SOURCE_USER` | Uživatel databáze |
| `PWD` | `<password>` | Zaškrtněte **Encrypted** |

Výsledný připojovací řetězec vypadá takto:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### Hodnota `DBQ`

`DBQ` přijímá tři formy. Pro *digna* jsou rovnocenné; liší se v tom, co musí být nakonfigurováno
na hostiteli *digna*:

| Forma | Příklad | Vyžaduje |
|---|---|---|
| **Úplný connect descriptor** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Nic — vše je ve vlastnosti. Doporučeno |
| **Alias TNS** | `DIGNA_SOURCE` | Alias musí existovat v `tnsnames.ora` klienta Oracle na hostiteli *digna* |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Oracle Client s podporou Easy Connect (12c a novější) |

!!! tip "Dejte přednost úplnému descriptoru"

    Alias TNS přesouvá polovinu definice připojení do souboru na hostiteli *digna*, na který se
    snadno zapomene při přestavbě hostitele nebo přesunu *digna*. Úplný descriptor udržuje
    připojení soběstačné — a právě o to v DSN-less nastavení jde.

Závorky v descriptoru uvnitř připojovacího řetězce nevadí, ale pokud vaše heslo obsahuje `;`,
uzavřete jej do složených závorek: `PWD={p@ss;word}`.

---

## 3. Konfigurace *digna* {: #3-digna-configuration }

Na obrazovce **Add DB Connection** zadejte následující:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Poznámky k Oracle {: #4-notes-on-oracle }

- **Schémata jsou uživatelé.** *digna* uvádí uživatele Oracle jako schémata, takže zdrojovým
  schématem je vlastník tabulek — v příkladu výše `DIGNA_SOURCE_USER`. Uživatel připojení
  potřebuje na těchto tabulkách oprávnění `SELECT`, buď přímo, nebo prostřednictvím role.
- **Jedno připojení vidí jednu databázi.** Katalog, který *digna* nabízí, je databáze, ke které
  je připojení připojeno, takže `DBQ` určuje, která služba, a tedy která databáze, se
  profiluje.
- **Identifikátory v uvozovkách rozlišují velikost písmen.** *digna* uvozuje názvy, které čte
  z datového slovníku, tedy tak, jak je Oracle ukládá — velkými písmeny u objektů vytvořených
  bez uvozovek.
- **Režimy profilování.** *Permanent* vytváří pracovní tabulky ve **Work Schema**, takže
  uživatel tam potřebuje oprávnění `CREATE TABLE` a kvótu na tablespace. *Session* používá
  privátní dočasnou tabulku (`ORA$PTT_…`, Oracle 18c a novější) a **Work Schema** nepoužívá.
  *Standard* potřebuje pouze přístup pro čtení.

---

## 5. Ověření ovladače (volitelné) {: #5-verifying-the-driver-optional }

Konfigurace zdroje dat ODBC není pro DSN-less připojení nutná, ale vlastní dialog ovladače je
pohodlný způsob, jak ověřit, že Oracle Client, název služby i vaše přihlašovací údaje fungují,
ještě než je zadáte do *digna*.

#### Krok 1
![Krok 1](images/oracle/create_odbc_data_source_step1.png)

**TNS Service Name** nabízený zde pochází z `tnsnames.ora` vaší instalace Oracle Client — tam
je definován alias a s ním i host, port a název služby. V *digna* můžete jako `DBQ` použít
alias, nebo místo něj úplný descriptor.

#### Krok 2 – Otestování připojení

Klikněte na tlačítko **Test Connection**.

![Krok 2](images/oracle/create_odbc_data_source_step2.png)

Zadejte heslo a klikněte na tlačítko **OK**.

![Krok 3](images/oracle/create_odbc_data_source_step3.png)

Zpráva o úspěchu potvrzuje, že ovladač i přihlašovací údaje fungují.