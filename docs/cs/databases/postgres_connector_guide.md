---
title: Konektor PostgreSQL – integrace databáze | Dokumentace digna
description: Nakonfigurujte digna pro připojení k PostgreSQL přes ODBC pomocí DSN-less připojovacího řetězce. Zahrnuje ovladač psqlODBC, povinné vlastnosti ODBC, režimy SSL a nastavení připojení na straně digna.
image: /assets/logo_square.png
---


# Zdrojový konektor pro PostgreSQL

Tento návod popisuje, jak nakonfigurovat *digna* pro připojení k PostgreSQL přes **ODBC**
pomocí **DSN-less** připojovacího řetězce.

Strana nastavení týkající se *digna* je stejná pro všechny technologie — kde se připojení
vytvářejí, jak se šifrují hodnoty vlastností, jak se připojení testuje a co znamenají režimy
profilování. Je popsána v [Přehledu databázových připojení](overview.md). Tato stránka
pokrývá to, co je specifické pro PostgreSQL.

---

## 1. Instalace ovladače ODBC {: #1-install-the-odbc-driver }

Nainstalujte ovladač PostgreSQL ODBC (**psqlODBC**) na počítač, na kterém běží backend *digna*,
podle oficiálního instalačního návodu dodavatele.

Ovladač se registruje pod názvem, který se liší podle platformy a balíčku — obvykle
**PostgreSQL Unicode(x64)** ve Windows a **PostgreSQL ODBC Driver(UNICODE)** v Linuxu. Přesný
název zjistěte na svém hostiteli podle postupu v
[Instalace ovladače ODBC na hostitele digna](overview.md#install-the-driver) a tento název
použijte pro vlastnost `DRIVER` níže.

---

## 2. Vlastnosti ODBC {: #2-odbc-properties }

!!! important "Příklad, nikoli specifikace"

    Níže uvedená sada je jedna kombinace, o které je známo, že funguje. Vlastnosti patří
    ovladači psqlODBC, takže jejich názvy, výchozí hodnoty a přípustné hodnoty se liší mezi
    verzemi ovladače a platformami a také požadavky vašeho serveru — zejména na SSL — se mohou
    lišit. Použijte ji jako výchozí bod a řiďte se dokumentací nainstalované verze ovladače.

Na obrazovce **Add DB Connection** přidejte následující vlastnosti:

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Musí odpovídat názvu ovladače registrovanému na hostiteli *digna* |
| `SERVER` | `db.example.com` | Název serveru nebo IP adresa |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Databáze obsahující zdrojová schémata. Je to jediná databáze, kterou toto připojení může profilovat |
| `UID` | `digna_source_user` | Uživatel databáze |
| `PWD` | `<password>` | Zaškrtněte **Encrypted** |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` nebo `verify-full` — server jej musí akceptovat |

Výsledný připojovací řetězec vypadá takto:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Jakoukoli další volbu psqlODBC lze přidat jako další vlastnost — například `ReadOnly=1` pro
relaci pouze pro čtení nebo `ConnSettings` pro spuštění příkazů `SET` při připojení.

---

## 3. Konfigurace *digna* {: #3-digna-configuration }

Na obrazovce **Add DB Connection** zadejte následující:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Poznámky k PostgreSQL {: #4-notes-on-postgresql }

- **`SSLMode` musí odpovídat serveru.** Server nakonfigurovaný s `hostssl` odmítne
  `SSLMode=disable` a `verify-ca` nebo `verify-full` navíc vyžadují, aby byl kořenový
  certifikát dostupný ovladači na hostiteli *digna*. Pokud jste při testování ovladače museli
  zvolit konkrétní režim, použijte zde stejný.
- **Jedno připojení vidí jednu databázi.** *digna* nabízí schémata databáze uvedené v
  `DATABASE`, protože PostgreSQL hlásí jako katalog pouze aktuální databázi. Zdrojové tabulky v
  jiné databázi potřebují vlastní připojení.
- **Režimy profilování.** *Permanent* vytváří pracovní tabulky ve **Work Schema**, takže
  uživatel potřebuje na tomto schématu oprávnění `CREATE`. *Session* používá
  `CREATE TEMPORARY TABLE` a **Work Schema** nepoužívá. *Standard* potřebuje pouze přístup pro
  čtení.

---

## 5. Ověření ovladače (volitelné) {: #5-verifying-the-driver-optional }

Konfigurace zdroje dat ODBC není pro DSN-less připojení nutná, ale vlastní dialog ovladače je
pohodlný způsob, jak ověřit, že ovladač funguje a že server přijímá vaše přihlašovací údaje a
režim SSL, ještě než je zadáte do *digna*.

#### Krok 1
![Krok 1](images/postgres/create_odbc_data_source_step1.png)

#### Krok 2 – Otestování připojení

Klikněte na tlačítko **Test Connection**.

![Krok 2](images/postgres/create_odbc_data_source_step2.png)

Hodnoty, které zde zadáte, jsou přesně ty hodnoty, které přebírají vlastnosti v
[sekci 2](#2-odbc-properties).
