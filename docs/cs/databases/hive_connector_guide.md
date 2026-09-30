---
title: Konektor Apache Hive – integrace databáze | Dokumentace digna
description: Nakonfigurujte digna pro připojení k Apache Hive přes ODBC pomocí DSN-less připojovacího řetězce. Zahrnuje ovladač Cloudera Hive ODBC, mechanismy ověřování, režimy transportu a nastavení připojení na straně digna.
image: /assets/logo_square.png
---


# Zdrojový konektor pro Hive

Tento návod popisuje, jak nakonfigurovat *digna* pro připojení k Apache Hive přes **ODBC**
pomocí **DSN-less** připojovacího řetězce.

Strana nastavení týkající se *digna* je stejná pro všechny technologie — kde se připojení
vytvářejí, jak se šifrují hodnoty vlastností, jak se připojení testuje a co znamenají režimy
profilování. Je popsána v [Přehledu databázových připojení](overview.md). Tato stránka
pokrývá to, co je specifické pro Hive.

---

## 1. Instalace ovladače ODBC {: #1-install-the-odbc-driver }

Nainstalujte **Cloudera ODBC Driver for Apache Hive** na počítač, na kterém běží backend
*digna*, podle oficiálního instalačního návodu dodavatele.

Přesný registrovaný název ovladače zjistěte na svém hostiteli podle postupu v
[Instalace ovladače ODBC na hostitele digna](overview.md#install-the-driver).

---

## 2. Vlastnosti ODBC {: #2-odbc-properties }

!!! important "Příklad, nikoli specifikace"

    Níže uvedená sada je jedna kombinace, o které je známo, že funguje. Vlastnosti patří
    ovladači Cloudera Hive, takže jejich názvy, výchozí hodnoty a přípustné hodnoty se liší
    mezi verzemi ovladače a platformami a to, co HiveServer2 přijme, zcela závisí na tom, jak
    je cluster zabezpečen — mechanismus ověřování, režim transportu, TLS, brána. Použijte ji
    jako výchozí bod a řiďte se dokumentací nainstalované verze ovladače.

Na obrazovce **Add DB Connection** přidejte následující vlastnosti:

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Musí odpovídat názvu ovladače registrovanému na hostiteli *digna* |
| `HOST` | `hive.example.com` | Název hostitele nebo IP adresa HiveServer2 |
| `PORT` | `10000` | Port HiveServer2; `10001` pro transport HTTP |

Výsledný připojovací řetězec vypadá takto:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Ověřování

Nezabezpečený HiveServer2 přijme výše uvedené tři vlastnosti tak, jak jsou. Pokud je ověřování
zapnuté, přidejte:

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `AuthMech` | `3` | `0` bez ověřování, `2` pouze uživatelské jméno, `3` uživatelské jméno a heslo, `1` Kerberos |
| `UID` | `digna_source_user` | Povinné pro `AuthMech` `2` a `3` |
| `PWD` | `<password>` | Povinné pro `AuthMech` `3`. Zaškrtněte **Encrypted** |

Pro Kerberos (`AuthMech=1`) potřebuje hostitel *digna* navíc platný ticket nebo keytab a také
vlastnosti `KrbHostFQDN`, `KrbServiceName` a `KrbRealm`, které popisuje dokumentace ovladače.

### Transport a TLS

| Klíč | Příklad hodnoty | Poznámky |
|---|---|---|
| `ThriftTransport` | `2` | `0` binární (výchozí, port 10000), `1` SASL, `2` HTTP (port 10001, a to, co očekává brána Knox) |
| `HTTPPath` | `cliservice` | S `ThriftTransport=2` |
| `SSL` | `1` | Pokud je HiveServer2 zabezpečen pomocí TLS |
| `Schema` | `dignadata` | Databáze Hive, ve které relace začíná. Volitelné — *digna* své dotazy plně kvalifikuje |

---

## 3. Konfigurace *digna* {: #3-digna-configuration }

Na obrazovce **Add DB Connection** zadejte následující:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Poznámky k Hive {: #4-notes-on-hive }

- **Katalogy pocházejí z ovladače.** Hive nemá vlastní katalog, takže *digna* přebírá to, co
  hlásí ovladač — obvykle jedinou položku s názvem `HIVE` — a pod ní uvádí databáze Hive jako
  schémata.
- **Work Schema je databáze Hive.** Pro profilování *Permanent* potřebuje uživatel oprávnění v
  ní vytvářet a odstraňovat tabulky a do příslušného úložiště musí být možné zapisovat.
- **Režimy profilování.** *Permanent* vytváří pracovní tabulky ve **Work Schema**. *Session*
  používá `CREATE TEMPORARY TABLE`, což vyžaduje HiveServer2 s podporou dočasných tabulek, a
  **Work Schema** nepoužívá. *Standard* potřebuje pouze přístup pro čtení a je to režim, který
  zvolíte na clusteru, kde *digna* nemá vůbec žádný přístup pro zápis.
- **Profilování je sada dotazů, nikoli skenování.** Každou statistiku počítá HiveServer2, takže
  fronta, do které uživatel *digna* odesílá dotazy, by měla mít dostatečnou kapacitu pro okno
  inspekce.

---

## 5. Ověření ovladače (volitelné) {: #5-verifying-the-driver-optional }

Konfigurace zdroje dat ODBC není pro DSN-less připojení nutná, ale vlastní dialog ovladače je
pohodlný způsob, jak ověřit, že ovladač, režim transportu i vaše přihlašovací údaje fungují,
ještě než je zadáte do *digna*.

#### Krok 1
![Krok 1](images/hive/create_odbc_data_source_step1.png)

Pole **Host**, **Port**, **Database**, **Mechanism** a **Thrift Transport** zde odpovídají
vlastnostem `HOST`, `PORT`, `Schema`, `AuthMech` a `ThriftTransport` v
[sekci 2](#2-odbc-properties).

#### Krok 2 – Otestování připojení

Zadejte heslo a klikněte na tlačítko **Test**.

![Krok 2](images/hive/create_odbc_data_source_step2.png)

Po úspěšném testu klikněte na tlačítko **OK**.
