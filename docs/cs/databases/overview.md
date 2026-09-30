---
title: Přehled databázových připojení – DSN-less nastavení ODBC | Dokumentace digna
description: Jak fungují databázová připojení v digna. Ke každé zdrojové technologii se přistupuje přes ODBC pomocí DSN-less připojovacího řetězce sestaveného z vlastností ODBC. Zahrnuje instalaci ovladače na hostitele digna, obrazovku Add DB Connection, šifrování vlastností, testování připojení, odstraňování problémů a odkazy na návody pro jednotlivé technologie.
image: /assets/logo_square.png
keywords:
  - digna databázové připojení
  - dsn-less odbc
  - odbc připojovací řetězec
  - nastavení ovladače odbc
  - unixodbc
  - vlastnosti odbc
  - konfigurace zdroje dat
lang: en
robots: index, follow
og_title: digna Database Connections – DSN-less ODBC Setup
og_description: Configure a digna source connection over ODBC without a DSN. Driver installation, ODBC properties, encryption, testing and troubleshooting.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Přehled databázových připojení

---

## Obsah

1. [Jak fungují připojení](#how-connections-work)
2. [Návody pro jednotlivé technologie](#technology-guides)
3. [Předpoklad: instalace ovladače ODBC na hostitele digna](#install-the-driver)
4. [Vytvoření databázového připojení](#create-a-database-connection)
5. [Vlastnosti ODBC](#odbc-properties)
6. [Šifrování hodnot vlastností](#encrypting-property-values)
7. [Testování připojení](#testing-a-connection)
8. [Kterou databázi připojení vidí](#which-database-the-connection-sees)
9. [Režim profilování a Work Schema](#profiling-mode-and-work-schema)
10. [Použití DSN](#using-a-dsn-instead)
11. [Odstraňování problémů](#troubleshooting)

---

## Jak fungují připojení {: #how-connections-work }

*digna* přistupuje ke každé zdrojové technologii přes **ODBC**. Připojení je seznam vlastností
ODBC, které zadáváte jako dvojice klíč/hodnota. Když *digna* připojení otevírá, spojí tyto
dvojice do připojovacího řetězce — `Key=Value`, oddělené `;`, v pořadí, v jakém jste je uvedli —
a předá jej správci ovladačů ODBC na hostiteli *digna*.

Právě to, že vlastnosti zadáváte sami, dělá nastavení **DSN-less**: připojení nese vše, co
ovladač potřebuje, takže na hostiteli není nutné registrovat žádný zdroj dat ODBC (DSN). Toto
je doporučený způsob konfigurace *digna*, protože definice připojení je celá uložena v *digna*
a přesouvá se spolu s ní.

### Proč ODBC {: #why-odbc }

Dřívější verze nabízely volbu mezi ovladačem specifickým pro technologii a ODBC, vybíranou
přepínačem **Use ODBC**. Od Release 2026.06 staví *digna* výhradně na ODBC. Jediné standardní
rozhraní vám dává víc, než dokáže sada ovladačů na míru:

- **Ověřování** — ověřování je součástí ODBC, takže připojení může používat cokoli, co jeho
  ovladač podporuje: hesla, tokeny a PAT, Kerberos a Active Directory, MFA a jednotné
  přihlášení v prohlížeči, cloudovou identitu, klientské certifikáty a TLS. Nové metody
  přicházejí s aktualizací ovladače a nemusí čekat na verzi *digna*.
- **Ovladače udržované dodavateli databází** — vlastní ovladač dodavatele drží krok s novými
  verzemi serveru a bezpečnostními opravami a můžete jej aktualizovat podle vlastního plánu,
  nezávisle na *digna*.
- **Jeden způsob konfigurace všeho** — každá technologie je seznam vlastností klíč/hodnota se
  stejným rozhraním, stejným šifrováním citlivých hodnot a stejným odstraňováním problémů,
  místo odlišné sady polí pro každý zdroj.
- **Ladění a dosah** — volby na úrovni ovladače, jako jsou časové limity, nastavení TLS, proxy
  a velikosti načítaných dávek, jsou dostupné pro každý zdroj a připojit lze jakoukoli
  technologii s vyhovujícím ovladačem ODBC, včetně těch, pro které *digna* nezveřejňuje
  samostatný návod.

!!! note "Co se v rozhraní změnilo"

    Přepínač **Use ODBC** a samostatná pole pro hostitele, port, databázi, uživatele a heslo
    už neexistují. Připojení, které dosud ODBC nepoužívá, potřebuje zadat vlastnosti ODBC, aby
    znovu fungovalo — viz
    [Vytvoření databázového připojení](#create-a-database-connection).

---

## Návody pro jednotlivé technologie {: #technology-guides }

Názvy vlastností se liší podle ovladače a každá technologie má jeden či dva detaily, které
ostatní nemají. Níže uvedené návody pokrývají tuto část; tato stránka pokrývá stranu *digna*,
která je pro všechny stejná.

!!! important "Sady vlastností v návodech jsou příklady"

    Každý návod ukazuje jednu kombinaci, o které je známo, že funguje — tu, vůči které je
    *digna* testována. Je to výchozí bod, nikoli specifikace: vlastnosti patří ovladači ODBC a
    to, které existují, jak se jmenují a jaké hodnoty přijímají, se liší mezi verzemi ovladače
    a dodavateli, mezi Windows, Linuxem a macOS a podle konfigurace zdrojového serveru —
    metody ověřování, TLS, brány, portu. Počítejte s tím, že bude třeba upravit jednu či dvě
    hodnoty, a za rozhodující považujte dokumentaci nainstalované verze ovladače.

| Technologie | Návod | Stojí za to vědět |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Serverless pooly potřebují `-ondemand` v názvu hostitele a podporují pouze profilování *Standard* |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Ověřování tokenem: `UID=token`, PAT v `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Katalogy pocházejí z ovladače, nikoli z dotazu |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Název ovladače je ve složených závorkách: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` přijímá buď úplný connect descriptor, nebo alias z `tnsnames.ora` |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` musí odpovídat požadavkům serveru |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Otestovaným způsobem ověřování je programový přístupový token |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` určuje, která schémata *digna* vidí |
| **Teradata** | [Teradata](teradata_connector_guide.md) | Hostitel se zadává do `DBCNAME`; databáze fungují jako schémata |

---

## Předpoklad: instalace ovladače ODBC na hostitele digna {: #install-the-driver }

*digna* otevírá zdrojová připojení ze **serveru, na kterém běží backend digna**, nikoli z
prohlížeče. Ovladač ODBC proto musí být nainstalován na tomto počítači a jeho název musí být
registrován u místního správce ovladačů.

=== "Windows"

    Nainstalujte 64bitový ovladač dodavatele, poté otevřete **ODBC Data Source Administrator
    (64-bit)** a přepněte na kartu **Drivers**. Názvy, které jsou tam uvedeny, jsou přesně ty
    hodnoty, které můžete použít pro vlastnost `Driver`.

=== "Linux"

    Nainstalujte **unixODBC** a ovladač dodavatele a poté vypište registrované názvy ovladačů:

    ```bash
    odbcinst -q -d
    ```

    Názvy vypsané v hranatých závorkách jsou hodnoty, které můžete použít pro vlastnost
    `Driver`. Pocházejí z `/etc/odbcinst.ini` (nebo ze souboru, který uvádí `odbcinst -j`).

=== "macOS"

    Nainstalujte **unixODBC** (například pomocí `brew install unixodbc`) a ovladač dodavatele a
    poté vypište registrované názvy ovladačů:

    ```bash
    odbcinst -q -d
    ```

!!! warning "Název ovladače se musí shodovat znak po znaku"

    `Driver` se předává správci ovladačů beze změny. `Simba Spark ODBC Driver` a
    `Simba Spark ODBC Driver 64` jsou z pohledu správce ovladačů různé ovladače a název, který
    není registrován, vyvolá chybu *data source name not found*, přestože se žádné DSN
    nepoužívá.

Místo registrovaného názvu všichni běžní správci ovladačů přijímají i úplnou cestu ke knihovně
ovladače, například `Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. To se hodí, když je
ovladač nainstalován, ale není registrován.

---

## Vytvoření databázového připojení {: #create-a-database-connection }

Otevřete **Admin Panel**, přejděte na kartu **Database Connections** a klikněte na
**Add DB Connection**. Obrazovka vyžaduje pět údajů:

| Pole | Popis |
|---|---|
| **Name** | Název připojení. Používá se k odkazování na připojení na dalších obrazovkách. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake nebo Hive. Určuje dialekt SQL, který *digna* generuje, takže musí odpovídat zdroji — nikoli ovladači. Azure Synapse Analytics je připojení typu **SQL Server**. |
| **ODBC Properties** | Dvojice klíč/hodnota popsané v části [Vlastnosti ODBC](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* nebo *Session* — viz [Režim profilování a Work Schema](#profiling-mode-and-work-schema). |
| **Work Schema** | Schéma, které obsahuje pracovní tabulky pro profilování *Permanent*. |

Připojení se spravuje centrálně a poté se přiřazuje jednomu nebo více projektům, takže stejné
připojení může sloužit několika projektům.

---

## Vlastnosti ODBC {: #odbc-properties }

Pro každou vlastnost klikněte na **Add Property** a vyplňte **Key**, **Value** a u tajných
hodnot zaškrtněte políčko **Encrypted**. Každý návod pro technologii uvádí vzorovou sadu pro
danou technologii, kterou přizpůsobíte své verzi ovladače a serveru — viz
[poznámku výše](#technology-guides).

Bez ohledu na ovladač pokrývá sada vlastností stejné čtyři věci:

- **`Driver`** — registrovaný název ovladače, jak je popsáno [výše](#install-the-driver).
- **Adresa serveru** — klíč se liší podle ovladače: `SERVER`, `HOST`, `DBCNAME`, `Server`
  nebo u Oracle connect descriptor `DBQ`.
- **Přihlašovací údaje** — obvykle `UID` a `PWD`; Snowflake používá `UID` plus `token` a
  Databricks používá doslovného uživatele `token` plus osobní přístupový token v `PWD`.
- **Databáze nebo katalog, se kterým se pracuje**, pokud jej technologie má — viz
  [Kterou databázi připojení vidí](#which-database-the-connection-sees).

Cokoli dalšího, co ovladač dokumentuje, lze přidat stejným způsobem — sdružování připojení
(connection pooling), časové limity soketů, nastavení Kerberos, nastavení proxy. *digna*
vlastnosti neinterpretuje; pouze je předává dál.

!!! warning "Hodnoty se neescapují — cokoli se středníkem uzavřete do složených závorek"

    Protože se vlastnosti spojují pomocí `;`, hodnota, která sama obsahuje `;`, by rozdělila
    připojovací řetězec na nesprávném místě. Takové hodnoty uzavřete do složených závorek:
    `PWD={p@ss;word}`. Totéž platí pro hodnoty s `=` nebo s mezerami na začátku. Proto se také
    některé ovladače obvykle zapisují ve složených závorkách, jako `{NetezzaSQL}` nebo
    `{SnowflakeDSIIDriver}`.

---

## Šifrování hodnot vlastností {: #encrypting-property-values }

Zaškrtněte **Encrypted** u každé vlastnosti, která obsahuje tajnou hodnotu — `PWD`, `token`,
tajný klíč klienta. Hodnota se pak před uložením do repozitáře *digna* zašifruje, na obrazovce
se zobrazí maskovaně a dešifruje se až při sestavování připojovacího řetězce.

!!! tip "Tip"

    Šifrovanou hodnotu nelze zpětně přečíst, ani v rozhraní, ani přes API — lze ji pouze
    nahradit. Tajné hodnoty si uchovávejte také ve vlastním správci hesel.

Vlastnosti, které nejsou tajné — název ovladače, hostitel, port, databáze — je nejlepší
ponechat nešifrované, aby zůstaly čitelné pro toho, kdo bude připojení později spravovat.

---

## Testování připojení {: #testing-a-connection }

V dialogu *Add DB Connection* klikněte na **Test** **před** uložením. Test použije hodnoty,
které jsou aktuálně ve formuláři, a provede skutečné připojení, takže nahlásí přesně to, na co
by narazila inspekce — chybný název ovladače, odmítnuté heslo, nedostupného hostitele. Nic se
neukládá: testovací připojení se vrátí zpět (rollback), ať uspěje, nebo selže.

U již existujícího připojení najeďte myší na jeho řádek na kartě **Database Connections** a
kliknutím na ikonu **zástrčky** jej otestujte znovu. To je nejrychlejší způsob, jak ověřit, zda
je zdroj dostupný po změně hesla nebo úpravě firewallu.

---

## Kterou databázi připojení vidí {: #which-database-the-connection-sees }

Když přidáváte zdroj dat, *digna* nabízí katalogy, schémata a tabulky, na které připojení
dosáhne. Jak daleko tento dosah sahá, závisí na technologii:

| Technologie | Nabízené katalogy |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Pouze **aktuální** databáze připojení |
| **Teradata**, **Netezza**, **Databricks** | Všechny databáze nebo katalogy, které uživatel smí vidět |
| **Hive**, **Impala** | Podle hlášení ovladače |

!!! important "Jedno připojení, jedna databáze"

    U PostgreSQL, SQL Server, Oracle a Snowflake musí vlastnosti ukazovat na databázi, která
    obsahuje zdrojová schémata — `DATABASE=…`, `Database=…` nebo název služby uvnitř `DBQ` u
    Oracle. Tabulky v jiné databázi nejsou přes toto připojení dostupné; přidejte pro ni druhé
    připojení.

---

## Režim profilování a Work Schema {: #profiling-mode-and-work-schema }

Režim profilování určuje, jak *digna* zpracovává data a počítá metriky:

- **Standard:** Metriky se počítají přímo na zdrojových tabulkách bez kopírování dat.
- **Permanent:** Data za inspektovaný den se zkopírují do trvalé tabulky a metriky se počítají
  na zkopírovaných datech.
- **Session:** Data se zkopírují do tabulky relace nebo dočasné tabulky a metriky se počítají
  na těchto dočasných datech.

Režim rozhoduje o tom, co musí mít uživatel připojení povoleno:

| Režim | Zapisuje | Oprávnění, která uživatel připojení potřebuje |
|---|---|---|
| **Standard** | nic | Čtení zdrojových tabulek |
| **Permanent** | jednu tabulku na zdroj dat ve **Work Schema** | Vytváření a odstraňování tabulek ve **Work Schema** |
| **Session** | dočasnou tabulku, kterou databáze odstraní spolu s relací | Vytváření dočasných tabulek — **Work Schema** se nepoužívá |

*Standard* pouze čte, a proto je to režim, který zvolíte, když má *digna* přidělen přístup
pouze pro čtení. **Work Schema** se čte jen u režimu *Permanent*, ale i tak stojí za to jej
vyplnit, aby připojení fungovalo i v případě, že se režim později změní.

---

## Použití DSN {: #using-a-dsn-instead }

DSN stále funguje — `DSN` je jen další vlastnost:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

DSN musí být registrováno na hostiteli *digna*, pro stejný uživatelský účet, pod kterým běží
backend *digna*, a jako **System DSN**, pokud *digna* běží jako služba. Vše, co je nakonfigurováno
v DSN, lze přepsat tím, že to přidáte i jako vlastnost.

DSN-less je zdokumentovaná výchozí volba, protože se vyhýbá tomuto stavu na straně hostitele:
připojení je plně popsáno v *digna* a nový hostitel *digna* potřebuje pouze nainstalovaný
ovladač, bez jakékoli konfigurace.

---

## Odstraňování problémů {: #troubleshooting }

### Data source name not found / no default driver specified

**Příznaky:**
- Tlačítko **Test** hlásí chybu zmiňující *data source name not found*, přestože je nastavení
  DSN-less

**Příčiny a řešení:**
1. Hodnota `Driver` neodpovídá žádnému registrovanému názvu ovladače — porovnejte ji s kartou
   **Drivers** v *ODBC Data Source Administrator (64-bit)* nebo s výstupem `odbcinst -q -d`
2. Ovladač je nainstalován na vaší pracovní stanici, ale ne na hostiteli *digna*
3. Ovladač je 32bitový, zatímco *digna* je 64bitová — nainstalujte 64bitový ovladač
4. Vlastnost `Driver` úplně chybí a nebylo zadáno ani `DSN`
5. V Linuxu a macOS je ovladač nainstalován, ale není registrován — zadejte místo toho úplnou
   cestu ke knihovně ovladače, nebo jej registrujte v `odbcinst.ini`

---

### Test připojení vyprší

**Příznaky:**
- **Test** se zasekne a přibližně po půl minutě selže

**Příčiny a řešení:**
1. Hostitel nebo port není z hostitele *digna* dostupný — zkontrolujte firewall a u cloudových
   zdrojů seznam povolených IP adres
2. Název hostitele je správný, ale port patří jiné službě
3. Zdroj potřebuje k přijetí připojení déle než výchozích 30 sekund — zvyšte
   `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` v sekci `[base]` souboru `config.toml` (`0` čeká
   neomezeně) a restartujte backend
4. Serverless endpoint se probouzí z nečinnosti — zkuste to znovu, a pokud se to děje
   pravidelně, zvyšte časový limit přihlášení, jak je uvedeno výše

---

### Ověření selže, přestože jsou přihlašovací údaje správné

**Příznaky:**
- Ovladač hlásí neplatné přihlašovací údaje, ale stejný uživatel funguje v jiném SQL klientovi

**Příčiny a řešení:**
1. Heslo obsahuje `;` — uzavřete hodnotu do složených závorek: `{p@ss;word}`
2. Do hodnoty se zkopírovala mezera na konci
3. Ovladač očekává konkrétní mechanismus ověřování — například `AuthMech` u ovladačů Hive a
   Databricks nebo `authenticator` u Snowflake
4. Hodnota byla uložena šifrovaně a poté upravena — šifrované hodnoty nelze zpětně přečíst,
   proto tajnou hodnotu zadejte znovu celou
5. Platnost tokenu vypršela — osobní přístupové tokeny a programové přístupové tokeny se
   vydávají s datem vypršení

---

### Obrazovka zdroje dat nenabízí očekávanou databázi nebo schéma

**Příznaky:**
- Při přidávání zdroje dat chybějí katalogy, schémata nebo tabulky

**Příčiny a řešení:**
1. Připojení ukazuje na jinou databázi — viz
   [Kterou databázi připojení vidí](#which-database-the-connection-sees)
2. Uživatel připojení nemá oprávnění ke čtení schématu nebo datového slovníku
3. **Technology** neodpovídá zdroji, takže *digna* dotazuje nesprávný datový slovník
4. U Snowflake nemá uživatel přiřazen výchozí warehouse a nebyla zadána vlastnost `Warehouse`,
   takže dotazy na metadata nelze spustit

---

### Profilování selže, zatímco test připojení uspěje

**Příznaky:**
- **Test** projde, ale inspekce selže při vytváření pracovních tabulek

**Příčiny a řešení:**
1. Je zvoleno profilování *Permanent* a uživatel připojení nemůže vytvářet tabulky ve
   **Work Schema** — udělte oprávnění, nebo přepněte na *Session* či *Standard*
2. **Work Schema** je prázdné nebo uvádí schéma, které neexistuje, zatímco je zvoleno
   profilování *Permanent*
3. Je zvoleno profilování *Session* a uživatel připojení nesmí vytvářet dočasné tabulky
4. Dlouho běžící dotaz profilování narazí na časový limit dotazu — zvyšte
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` v sekci `[base]` souboru `config.toml` (výchozí hodnota
   3600 sekund, `0` časový limit vypíná)

---

## Osvědčené postupy

**CO DĚLAT:**

- Před konfigurací připojení nainstalujte a registrujte ovladač na hostiteli *digna*
- Zaškrtněte **Encrypted** u každého hesla a tokenu
- Před uložením klikněte na **Test** a po změně hesla test zopakujte
- Pojmenovávejte připojení podle zdroje a prostředí, například `sales_dwh_prod`
- Dejte *digna* vyhrazeného uživatele databáze, s přístupem pouze pro čtení tam, kde stačí
  profilování *Standard*
- Pro každou zdrojovou databázi mějte jedno připojení a raději přidejte druhé, než abyste
  přepínali to první

**CO NEDĚLAT:**

- Neukládejte tajné hodnoty nešifrované a nesdílejte jednoho uživatele databáze mezi *digna* a
  jinými nástroji
- Nepoužívejte 32bitový ovladač s 64bitovou instalací *digna*
- Nespoléhejte na User DSN, když *digna* běží jako služba — nebude viditelné
- Nevkládejte do vlastnosti hodnotu obsahující `;` bez složených závorek
- Nesměrujte **Work Schema** na schéma, které obsahuje zdrojová data

---

## Podpora

Potřebujete pomoc s databázovým připojením?

- **E-mail:** support@digna.ai
- **Dokumentace:** https://docs.digna.ai
- **Web:** https://www.digna.ai

---

**Release:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
