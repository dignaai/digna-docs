# Zdrojový konektor pro Netezza

Tento návod popisuje, jak nakonfigurovat *digna* pro připojení k Netezza přes **ODBC** pomocí
**DSN-less** připojovacího řetězce.

Strana nastavení týkající se *digna* je stejná pro všechny technologie — kde se připojení
vytvářejí, jak se šifrují hodnoty vlastností, jak se připojení testuje a co znamenají režimy
profilování. Je popsána v [Přehledu databázových připojení](overview.md). Tato stránka
pokrývá to, co je specifické pro Netezza.

---

## 1. Instalace ovladače ODBC {: #1-install-the-odbc-driver }

Nainstalujte ovladač ODBC **NetezzaSQL** (součást klientských nástrojů IBM Netezza) na počítač,
na kterém běží backend *digna*, podle oficiálního instalačního návodu dodavatele.

Přesný registrovaný název ovladače zjistěte na svém hostiteli podle postupu v
[Instalace ovladače ODBC na hostitele digna](overview.md#install-the-driver).

---

## 2. Vlastnosti ODBC {: #2-odbc-properties }

!!! important "Příklad, nikoli specifikace"

    Níže uvedená sada je jedna kombinace, o které je známo, že funguje. Vlastnosti patří
    ovladači NetezzaSQL, takže jejich názvy, výchozí hodnoty a přípustné hodnoty se liší mezi
    verzemi klienta a platformami a appliance zabezpečená pomocí TLS potřebuje více vlastností,
    než je zde uvedeno. Použijte ji jako výchozí bod a řiďte se dokumentací nainstalované
    verze klienta.

Na obrazovce **Add DB Connection** přidejte následující vlastnosti:

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Musí odpovídat názvu ovladače registrovanému na hostiteli *digna*. Složené závorky jsou obvyklý způsob zápisu tohoto názvu |
| `SERVER` | `netezza.example.com` | Název serveru nebo IP adresa |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Databáze, ve které relace začíná |
| `UID` | `ADMIN` | Uživatel databáze |
| `PWD` | `<password>` | Zaškrtněte **Encrypted** |

Výsledný připojovací řetězec vypadá takto:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

V závislosti na verzi ovladače, nastavení a bezpečnostních požadavcích mohou být potřeba další
vlastnosti — například `SecurityLevel` a `CaCertFile` pro appliance zabezpečenou pomocí TLS.
Každou volbu, kterou nabízejí dialogy ovladače *Advanced*, *SSL* a *Driver*, lze přidat jako
vlastnost.

---

## 3. Konfigurace *digna* {: #3-digna-configuration }

Na obrazovce **Add DB Connection** zadejte následující:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Poznámky k Netezza {: #4-notes-on-netezza }

- **Platí katalogy i schémata.** *digna* uvádí databáze, které uživatel smí vidět (z
  `_V_DATABASE`), jako katalogy a pod nimi jejich schémata (z `_V_SCHEMA`), takže jedno
  připojení může obsluhovat zdroje ve více databázích. `DATABASE` určuje pouze, kde relace
  začíná.
- **Identifikátory jsou psány velkými písmeny**, pokud nebyly vytvořeny v uvozovkách, a proto
  výše uvedené příklady používají `TEST` a `ADMIN`.
- **Režimy profilování.** *Permanent* vytváří pracovní tabulky ve **Work Schema**, takže
  uživatel tam potřebuje oprávnění `CREATE TABLE`. *Session* používá `CREATE TEMPORARY TABLE`
  a **Work Schema** nepoužívá. *Standard* potřebuje pouze přístup pro čtení.

---

## 5. Ověření ovladače (volitelné) {: #5-verifying-the-driver-optional }

Konfigurace zdroje dat ODBC není pro DSN-less připojení nutná, ale vlastní dialog ovladače je
pohodlný způsob, jak ověřit, že ovladač a vaše přihlašovací údaje fungují, ještě než je
zadáte do *digna*.

#### Krok 1
![Krok 1](images/netezza/create_odbc_data_source_step1.png)

Pole na kartě **DSN Options** odpovídají jedna ku jedné vlastnostem v
[sekci 2](#2-odbc-properties). V závislosti na ovladači Netezza, nastavení a bezpečnostních
požadavcích můžete potřebovat vyplnit také karty **Advanced DSN Options**, **SSL DSN Options**
nebo **Driver Options**; pro nejjednodušší nastavení stačí **DSN Options**.

Klikněte na tlačítko **Test Connection**.

#### Krok 2
![Krok 2](images/netezza/create_odbc_data_source_step2.png)

Jakmile se zobrazí obrazovka s potvrzením úspěchu, ovladač funguje a hodnoty jsou správné.