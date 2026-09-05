# digna CLI Reference 2025.09
**2025-09-29**

Tato stránka dokumentuje úplnou sadu příkazů dostupných v CLI nástroji ***digna*** verze **2025.09**, včetně příkladů použití a možností.

---

## Základy CLI

---

### help
Možnost `--help` poskytuje informace o dostupných příkazech a jejich použití. Existují dva hlavní způsoby, jak tuto možnost použít:

1. **Zobrazení obecné nápovědy:**
   
    Použijte --help bezprostředně za klíčovým slovem ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Získání nápovědy ke konkrétním příkazům:**  
  
    Pro podrobné informace o konkrétním příkazu přidejte `--help` za název příkazu.
    Například pro nápovědu k příkazu `add-user` spusťte:
     ```bash
     dignacli add-user --help
     ```

     ### výstup:
      
     - **Popis příkazu:** Nabízí detailní popis toho, co příkaz dělá.  
     - **Syntax:** Zobrazuje přesnou syntaxi včetně povinných a volitelných argumentů.  
     - **Možnosti:** Uvádí jakékoliv volby specifické pro příkaz společně s jejich vysvětlením.  
     - **Příklady:** Poskytuje příklady, jak příkaz efektivně použít.

### check-config

Příkaz check-config je nástroj v CLI ***digna*** určený k otestování konfigurace ***digna***. Tento příkaz ověřuje, že komponenty ***digna*** najdou potřebné konfigurační prvky v souboru config.toml.

#### Možnosti

- `--configpath`, `-cp`: Soubor nebo adresář, který obsahuje konfiguraci. Pokud není uvedeno, použije se ../config.toml.
      
#### Použití příkazu
```bash
dignacli check-config
```

Po úspěšném provedení příkaz vypíše potvrzení o úplnosti konfigurace.  
  
Pokud se konfigurace jeví jako neúplná, budou vypsány chybějící konfigurační prvky.

  
### check-repo-connection

Příkaz check-repo-connection je nástroj v CLI ***digna*** určený k otestování konektivity a přístupu ke specifikovanému repozitáři ***digna***. Tento příkaz zajišťuje, že CLI může s repozitářem komunikovat.
      
#### Použití příkazu
```bash
dignacli check-repo-connection
```

Po úspěšném provedení příkaz vypíše potvrzení o připojení spolu s informacemi o repozitáři: verze repozitáře, hostitel, databáze a schéma.  
  
Pokud se připojení k repozitáři nezdaří, zkontrolujte soubor config.toml kvůli správným konfiguračním nastavením.


### version

Pro zjištění nainstalované verze *dignacli* použijte volbu --version.  
  
#### Použití příkazu
```bash
dignacli --version
```
  
#### Příklad výstupu
```bash
dignacli version 2025.09
```

### možnosti logování
  
Výchozí výstup příkazů ***digna*** do konzole je navržen jako minimalistický. Většina příkazů však nabízí možnost poskytnout další informace pomocí následujících voleb:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ a „debug“ určují úroveň detailů, zatímco přepínač „logfile“ umožňuje přesměrovat výstup do souboru místo do konzole.

## Správa uživatelů

### add-user
  
Příkaz add-user v CLI ***digna*** slouží k přidání nového uživatele do systému ***digna***.
  
#### Použití příkazu
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenty

- **USER_NAME**: Uživatelské jméno nového uživatele (povinné).
- **USER_FULL_NAME**: Celé jméno nového uživatele (povinné).
- **USER_PASSWORD**: Heslo pro nového uživatele (povinné).

#### Možnosti

- `--is_superuser`, `-su`: Příznak, který označí nového uživatele jako administrátora.
- `--valid_until`, `-vu`: Nastaví datum vypršení platnosti uživatelského účtu ve formátu `YYYY-MM-DD HH:MI:SS`. Pokud není nastaveno, účet nemá datum vypršení.

#### Příklad

Pro přidání nového uživatele s uživatelským jménem `jdoe`, jménem `John Doe` a heslem `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Pro přidání nového uživatele a nastavení data vypršení účtu:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Příkaz `delete-user` v CLI ***digna*** slouží k odstranění existujícího uživatele ze systému ***digna***.
  
#### Použití příkazu
```bash
dignacli delete-user USER_NAME
```
  
#### Argumenty
- **USER_NAME**: Uživatelské jméno uživatele, který má být smazán (povinné). Toto je jediný argument vyžadovaný příkazem.

#### Příklad
```bash
dignacli delete-user jdoe
```
  
Provedením tohoto příkazu bude uživatel `jdoe` odstraněn ze systému ***digna***, bude mu odňat přístup a jeho související data a oprávnění v repozitáři budou smazána.

### modify-user

Příkaz `modify-user` v CLI ***digna*** slouží k aktualizaci údajů existujícího uživatele v systému ***digna***.

#### Použití příkazu
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenty
  
- **USER_NAME**: Uživatelské jméno uživatele, který má být upraven (povinné).
- **USER_FULL_NAME**: Nové celé jméno uživatele (povinné).
  
#### Možnosti  
  
- `--is_superuser`, `-su`: Nastaví uživatele jako superuživatele, čímž mu udělí zvýšená oprávnění. Tento přepínač nevyžaduje hodnotu.  
- `--valid_until`, `-vu`: Nastaví datum vypršení platnosti uživatelského účtu ve formátu YYYY-MM-DD HH:MI:SS. Pokud není uvedeno, účet zůstává platný neomezeně.  
  
#### Příklad
  
Pro změnu celého jména uživatele `jdoe` na „Johnathan Doe“ a nastavení uživatele jako superuživatele:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Příkaz `modify-user-pwd` v CLI ***digna*** slouží ke změně hesla pro existujícího uživatele v systému ***digna***.
  
#### Použití příkazu
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumenty
  
- **USER_NAME**: Uživatelské jméno uživatele, jehož heslo se má změnit (povinné).
- **USER_PWD**: Nové heslo pro uživatele (povinné).
  
#### Příklad
  
Pro změnu hesla uživatele `jdoe` na `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Příkaz `list-users` v CLI ***digna*** zobrazí seznam všech uživatelů registrovaných v systému ***digna***.

#### Použití příkazu

```bash
dignacli list-users
```

Spuštěním tohoto příkazu se CLI připojí k repozitáři ***digna*** a vypíše všechny uživatele, zobrazí jejich ID, uživatelské jméno, celé jméno, status superuživatele a časy vypršení platnosti.

## Správa repozitáře

### upgrade-repo
  
Příkaz `upgrade-repo` v CLI ***digna*** slouží k aktualizaci nebo inicializaci repozitáře ***digna***. Tento příkaz je nezbytný pro aplikaci aktualizací nebo pro prvotní nastavení infrastruktury repozitáře.
  
#### Použití příkazu

```bash
dignacli upgrade-repo [options]
```
  
#### Možnosti
  
- `--simulation-mode`, `-s`: Pokud je povoleno, spustí příkaz v simulačním režimu, který vytiskne SQL příkazy, které by byly vykonány, ale skutečně je neprovede. To je užitečné pro nahlédnutí do změn bez jejich aplikace.  

  
#### Příklad
  
Pro aktualizaci repozitáře ***digna*** můžete spustit příkaz bez voleb:
  
```bash
dignacli upgrade-repo
```  
Pro spuštění upgradu v simulačním režimu (zobrazení SQL příkazů bez jejich aplikace):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Tento příkaz je klíčový pro udržování systému ***digna***, zajišťuje, že schéma databáze a další komponenty repozitáře jsou aktuální s nejnovější verzí softwaru.

### encrypt
  
Příkaz `encrypt` v CLI ***digna*** slouží k zašifrování hesla.
  
#### Použití příkazu
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenty
- **PASSWORD**: Heslo, které je třeba zašifrovat (povinné).
  
#### Příklad
  
Pro zašifrování hesla je třeba heslo uvést jako argument.   
Například pro zašifrování hesla `mypassword123` použijte:
```bash
dignacli encrypt mypassword123
```
Tento příkaz vypíše zašifrovanou verzi zadaného hesla, kterou lze následně použít v zabezpečených kontextech. Pokud argument hesla není poskytnut, CLI zobrazí chybu s informací o chybějícím argumentu.

### generate-key
  
Příkaz `generate-key` slouží k vygenerování Fernet klíče, který je nezbytný pro zabezpečení hesel uložených v repozitáři ***digna***.
  
#### Použití příkazu
```bash
dignacli generate-key
```
  
## Správa dat

### clean-up

Příkaz `clean-up` v CLI ***digna*** slouží k odstranění profilů, predikcí a dat systému semaforu (traffic light system) pro jeden nebo více datových zdrojů v rámci zadaného projektu. Tento příkaz je důležitý pro řízení životního cyklu dat a pomáhá udržovat organizované a efektivní prostředí odstraněním zastaralých nebo nepotřebných dat.

#### Použití příkazu

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Název projektu, z něhož mají být data odstraněna (povinné). Použití klíčového slova all-projects v tomto argumentu instruuje ***digna***, aby iterovalo přes všechny existující projekty a tento příkaz aplikovalo.
- **FROM_DATE**: Počáteční datum a čas pro odstranění dat. Přijatelné formáty zahrnují %Y-%m-%d, %Y-%m-%dT%H:%M:%S nebo %Y-%m-%d %H:%M:%S (povinné).
- **TO_DATE**: Konečné datum a čas pro odstranění dat, ve stejných formátech jako FROM_DATE (povinné).
  
#### Možnosti
  
- `--table-name`, `-tn`: Omezení čistění na konkrétní tabulku v projektu.
- `--table-filter`, `-tf`: Filtr pro omezení čištění na tabulky obsahující zadaný podřetězec v názvu.
- `--timing`, `-tm`: Zobrazí délku trvání procesu čištění po jeho dokončení.
- `--help`: Zobrazí nápovědu pro příkaz clean-up a ukončí.
  
#### Příklad
  
Pro odstranění dat z projektu ProjectA mezi 1. lednem 2023 a 30. červnem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Pro odstranění dat pouze z konkrétní tabulky s názvem `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Tento příkaz pomáhá spravovat úložiště dat a zajišťuje, že repozitář obsahuje pouze relevantní informace.

### remove-orphans
  
Příkaz `remove-orphans` v CLI ***digna*** slouží pro údržbu repozitáře ***digna***.  
Když uživatel smaže projekty nebo datové zdroje, profily a predikce zůstanou v repozitáři. Tento příkaz odstraní takové „sirotčí“ řádky z repozitáře.
  
#### Použití příkazu
  
```bash
dignacli list-projects
```

### list-projects
  
Příkaz `list-projects` v CLI ***digna*** slouží k zobrazení seznamu všech dostupných projektů v systému ***digna***.
  
#### Použití příkazu
  
```bash
dignacli list-projects
```

Tento příkaz je zvláště užitečný pro administrátory a uživatele spravující více projektů, protože poskytuje rychlý přehled dostupných projektů v repozitáři ***digna***.

### list-ds

Příkaz `list-ds` v CLI ***digna*** slouží k zobrazení seznamu všech dostupných datových zdrojů v rámci zadaného projektu. Tento příkaz je užitečný pro orientaci v datových aktivech, která jsou k dispozici pro analýzu a správu v systému ***digna***.

#### Použití příkazu
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenty
- **PROJECT_NAME**: Název projektu, pro který se datové zdroje vypisují (povinné).
  
#### Příklad
  
Pro zobrazení všech datových zdrojů v projektu s názvem `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Tento příkaz poskytuje uživatelům přehled datových zdrojů dostupných v projektu, což jim pomáhá lépe se orientovat a spravovat datové prostředí.


### inspect

Příkaz `inspect` v CLI ***digna*** slouží k vytvoření profilů, predikcí a dat systému semaforu (traffic light system) pro jeden nebo více datových zdrojů v rámci zadaného projektu. Tento příkaz pomáhá analyzovat a monitorovat data za definované období. Po dokončení inspekce je vrácena hodnota vypočteného systému semaforu:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Použití příkazu

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Název projektu, jehož data mají být inspektována (povinné). Použití klíčového slova all-projects v tomto argumentu instruuje ***digna***, aby iterovalo přes všechny existující projekty a tento příkaz aplikovalo.
- **FROM_DATE**: Počáteční datum a čas pro inspekci dat. Přijatelné formáty zahrnují %Y-%m-%d, %Y-%m-%dT%H:%M:%S nebo %Y-%m-%d %H:%M:%S (povinné).
- **TO_DATE**: Konečné datum a čas pro inspekci dat, ve stejných formátech jako FROM_DATE (povinné).
  
#### Možnosti

- `--table-name`, `-tn`: Omezuje inspekci na konkrétní tabulku v projektu.
- `--table-filter`, `-tf`: Filtr pro inspekci pouze tabulek obsahujících zadaný podřetězec v názvu.
- `--enable_notification`, `-en`: Povolit odesílání notifikací v případě alertů.
- `--bypass-backend`, `-bb`: Obcházet backend a spustit inspekci přímo z CLI (pouze pro testovací účely!).

  
#### Příklad
  
Pro inspekci dat projektu `ProjectA` od 1. ledna 2024 do 31. ledna 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Pro inspekci pouze konkrétní tabulky a vynucení přepočtu predikcí:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Tento příkaz je užitečný pro generování aktualizovaných profilů a predikcí, monitorování integrity dat a správu systémů alertů v rámci zadaného časového rozmezí projektu.

### inspect-async

Příkaz `inspect-async` v CLI ***digna*** slouží k vytvoření profilů, predikcí a dat systému semaforu (traffic light system) pro jeden nebo více datových zdrojů v rámci zadaného projektu. Tento příkaz pomáhá analyzovat a monitorovat data za definované období. Na rozdíl od příkazu `inspect` tento příkaz nečeká na dokončení inspekce.
Místo toho vrací ID požadavku pro odeslaný požadavek na inspekci. Pro zjištění průběhu inspekce použijte příkaz `inspect-status`.

#### Použití příkazu

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Název projektu, jehož data mají být inspektována (povinné). Použití klíčového slova all-projects v tomto argumentu instruuje ***digna***, aby iterovalo přes všechny existující projekty a tento příkaz aplikovalo.
- **FROM_DATE**: Počáteční datum a čas pro inspekci dat. Přijatelné formáty zahrnují %Y-%m-%d, %Y-%m-%dT%H:%M:%S nebo %Y-%m-%d %H:%M:%S (povinné).
- **TO_DATE**: Konečné datum a čas pro inspekci dat, ve stejných formátech jako FROM_DATE (povinné).
  
#### Možnosti

- `--table-name`, `-tn`: Omezuje inspekci na konkrétní tabulku v projektu.
- `--table-filter`, `-tf`: Filtr pro inspekci pouze tabulek obsahujících zadaný podřetězec v názvu.
- `--enable_notification`, `-en`: Povolit odesílání notifikací v případě alertů.

  
#### Příklad
  
Pro asynchronní inspekci dat projektu `ProjectA` od 1. ledna 2024 do 31. ledna 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Příkaz `inspect-status` v CLI ***digna*** slouží ke kontrole průběhu asynchronní inspekce na základě ID požadavku.

#### Použití příkazu

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenty
  
- **REQUEST_ID**: ID požadavku vrácené příkazem `inspect-async` 
  
#### Příklad
  
Pro kontrolu průběhu inspekce s ID požadavku 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Příkaz `inspect-cancel` v CLI ***digna*** slouží k zrušení inspekcí na základě ID požadavku, nebo lze použít k zrušení všech aktuálních požadavků.

#### Použití příkazu

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenty
  
- **REQUEST_ID**: ID požadavku vrácené příkazem `inspect-async` 
  
#### Příklad
  
Pro zrušení inspekce s ID požadavku 12345:
  
```bash
dignacli inspect-cancel 12345
```

Pro zrušení všech požadavků, které jsou právě spuštěné nebo čekající:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Příkaz `export-ds` v CLI ***digna*** slouží k vytvoření exportu datových zdrojů z repozitáře ***digna***. Ve výchozím nastavení budou exportovány všechny datové zdroje z daného projektu.

#### Použití příkazu
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenty
- **PROJECT_NAME**: Název projektu, ze kterého budou datové zdroje exportovány.

#### Možnosti

- `--table_name`, `-tn`: Exportovat konkrétní datový zdroj z projektu.
- `--exportfile`, `-ef`: Určit název souboru pro export.
    
#### Příklad
  
Pro export všech datových zdrojů z projektu s názvem `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Tento příkaz exportuje všechny datové zdroje z `ProjectA` jako JSON dokument, který lze importovat do jiného projektu nebo repozitáře ***digna***.


### import-ds

Příkaz `import-ds` v CLI ***digna*** slouží k importu datových zdrojů do cílového projektu a k vytvoření importního reportu.

#### Použití příkazu
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenty
- **PROJECT_NAME**: Název projektu, do kterého budou datové zdroje importovány.
- **EXPORT_FILE**: Název souboru s exportem datových zdrojů, který má být importován.

#### Možnosti

- `--output-file`, `-o`: Soubor pro uložení importního reportu (pokud není zadán, tiskne se do terminálu v tabulární podobě).
- `--output-format`, `-f`: Formát pro uložení importního reportu (json, csv).
    
#### Příklad
  
Pro import všech datových zdrojů ze souboru `my_export.json` do `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po importu tento příkaz také zobrazí report o importovaných a přeskočených objektech. Do `ProjectB` budou importovány pouze nové datové zdroje. Pro zjištění, které objekty by byly importovány a které přeskočeny, můžete použít příkaz `plan-import-ds`.

### plan-import-ds

Příkaz `plan-import-ds` v CLI ***digna*** slouží k naplánování importu datových zdrojů do cílového projektu a vytvoření importního reportu (bez skutečného provedení importu).

#### Použití příkazu
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenty
- **PROJECT_NAME**: Název projektu, do kterého by datové zdroje byly importovány.
- **EXPORT_FILE**: Název souboru s exportem datových zdrojů, který má být analyzován před importem.

#### Možnosti

- `--output-file`, `-o`: Soubor pro uložení importního reportu (pokud není zadán, tiskne se do terminálu v tabulární podobě).
- `--output-format`, `-f`: Formát pro uložení importního reportu (json, csv).
    
#### Příklad
  
Pro kontrolu, které datové zdroje by byly importovány a které by byly přeskočeny ze souboru `my_export.json` při importu do `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Tento příkaz zobrazí pouze plán importu objektů, které by byly importovány a přeskočeny.