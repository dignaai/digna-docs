# Zdrojový konektor pro Teradata

Tento návod popisuje, jak nakonfigurovat *digna* pro připojení k Teradata přes **ODBC** pomocí
**DSN-less** připojovacího řetězce.

Strana nastavení týkající se *digna* je stejná pro všechny technologie — kde se připojení
vytvářejí, jak se šifrují hodnoty vlastností, jak se připojení testuje a co znamenají režimy
profilování. Je popsána v [Přehledu databázových připojení](overview.md). Tato stránka
pokrývá to, co je specifické pro Teradata.

---

## 1. Instalace ovladače ODBC {: #1-install-the-odbc-driver }

Nainstalujte **ODBC Driver for Teradata** na počítač, na kterém běží backend *digna*, podle
oficiálního instalačního návodu dodavatele.

Ovladač se registruje s verzí v názvu, například **Teradata Database ODBC Driver 20.00**.
Přesný registrovaný název zjistěte na svém hostiteli podle postupu v
[Instalace ovladače ODBC na hostitele digna](overview.md#install-the-driver).

---

## 2. Vlastnosti ODBC {: #2-odbc-properties }

!!! important "Příklad, nikoli specifikace"

    Níže uvedená sada je jedna kombinace, o které je známo, že funguje. Vlastnosti patří
    ovladači Teradata ODBC, takže jejich názvy, výchozí hodnoty a přípustné hodnoty se liší
    mezi verzemi ovladače — verze je přímo součástí názvu ovladače — i mezi platformami.
    Použijte ji jako výchozí bod a řiďte se dokumentací nainstalované verze ovladače.

Na obrazovce **Add DB Connection** přidejte následující vlastnosti:

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Musí odpovídat názvu ovladače registrovanému na hostiteli *digna* |
| `DBCNAME` | `teradata.example.com` | Název serveru nebo IP adresa. Vlastní název Teradata pro vlastnost hostitele |
| `UID` | `digna_source_user` | Uživatel databáze |
| `PWD` | `<password>` | Zaškrtněte **Encrypted** |

Výsledný připojovací řetězec vypadá takto:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Užitečné doplňkové vlastnosti:

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `MechanismName` | `TD2` | Mechanismus přihlášení. `TD2` je výchozí v Teradata; pro ověřování přes adresářovou službu použijte `LDAP` |
| `DefaultDatabase` | `dad` | Databáze, ve které relace začíná |
| `CharacterSet` | `UTF8` | Nastavte tam, kde by výchozí znaková sada relace poškodila data mimo ASCII |

---

## 3. Konfigurace *digna* {: #3-digna-configuration }

Na obrazovce **Add DB Connection** zadejte následující:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Poznámky k Teradata {: #4-notes-on-teradata }

- **Databáze Teradata je katalog, nikoli schéma.** *digna* uvádí databáze, které uživatel smí
  vidět (z `DBC.DatabasesV`), jako katalogy a úroveň schématu se neuplatňuje. Při přidávání
  zdroje dat zvolte databázi jako katalog; schéma se zobrazí jako *not applicable*.
- **Jedno připojení dosáhne na všechny povolené databáze**, takže jediné připojení může
  obsluhovat zdroje napříč databázemi — na rozdíl od technologií, kde je připojení vázáno na
  jednu databázi.
- **Work Schema je databáze.** Pro profilování *Permanent* uveďte databázi Teradata, která
  obsahuje pracovní tabulky, a dejte uživateli oprávnění `CREATE TABLE` a v ní i přidělený
  prostor `PERM` — databáze s nulovým perm prostorem nemůže obsahovat žádnou tabulku.
- **Režimy profilování.** *Permanent* vytváří tabulky ve **Work Schema**. *Session* používá
  tabulku `VOLATILE`, která potřebuje prostor `SPOOL`, ale žádný perm prostor ani oprávnění ve
  **Work Schema**. *Standard* potřebuje pouze přístup pro čtení.

---

## 5. Ověření ovladače (volitelné) {: #5-verifying-the-driver-optional }

Konfigurace zdroje dat ODBC není pro DSN-less připojení nutná, ale vlastní dialog ovladače je
pohodlný způsob, jak ověřit, že ovladač a vaše přihlašovací údaje fungují, ještě než je
zadáte do *digna*.

#### Krok 1
![Krok 1](images/teradata/create_odbc_data_source_step1.png)

Pole **Name or IP address** zde odpovídá vlastnosti `DBCNAME` v
[sekci 2](#2-odbc-properties).

Klikněte na tlačítko **Test**.

#### Krok 2
![Krok 2](images/teradata/create_odbc_data_source_step2.png)

Zadejte uživatelské jméno a heslo a poté klikněte na tlačítko **OK**. Obrazovka s potvrzením
úspěchu ukazuje, že ovladač i přihlašovací údaje fungují.