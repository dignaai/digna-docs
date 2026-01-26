---
title: digna CLI Reference 2026.01 – Příkazy a příklady | digna Dokumentace
description: Kompletní reference pro digna CLI verzi 2026.01. Naučte se spravovat uživatele, repozitáře a data pomocí příkazů jako add-user, check-config, check-repo-connection, inspect, inspect-async a dalších.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202601/
image: /assets/logo_square.png
---

# digna CLI Reference 2026.01
**2026-01-15**

Tato stránka dokumentuje kompletní sadu příkazů dostupných v CLI nástroji ***digna*** verze **2026.01**, včetně ukázkového použití a voleb.

---

## CLI Základy

---

### help
Volba `--help` poskytuje informace o dostupných příkazech a jejich použití. Existují dva hlavní způsoby, jak tuto volbu použít:

1. **Zobrazení obecné nápovědy:**
   
    Použijte `--help` ihned za klíčovým slovem ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Získání nápovědy pro konkrétní příkaz:**  
  
    Pro podrobné informace o konkrétním příkazu připojte `--help` za tento příkaz.
    Například pro nápovědu k příkazu `add-user` spusťte:
     ```bash
     dignacli add-user --help
     ```

     ### výstup:
      
     - **Popis příkazu:** Nabízí podrobný popis toho, co příkaz dělá.  
     - **Syntaxe:** Ukazuje přesnou syntaxi včetně povinných a volitelných argumentů.  
     - **Volby:** Vypisuje jakékoli volby specifické pro příkaz spolu s jejich vysvětlením.  
     - **Příklady:** Poskytuje příklady, jak příkaz efektivně spustit.

### check-config

Příkaz `check-config` je nástroj v CLI ***digna*** určený k otestování konfigurace ***digna***. Tento příkaz ověřuje, že komponenty ***digna*** dokáží najít potřebné konfigurační prvky v souboru config.toml.

#### Volby

- `--configpath`, `-cp`: Soubor nebo adresář obsahující konfiguraci. Pokud není zadáno, použije se ../config.toml.
      
#### Použití příkazu
```bash
dignacli check-config
```

Po úspěšném provedení příkaz vypíše potvrzení o úplnosti konfigurace.  
  
Pokud se konfigurace jeví jako neúplná, budou vypsány chybějící konfigurační položky.

  
### check-repo-connection

Příkaz `check-repo-connection` je nástroj v CLI ***digna*** určený k otestování konektivity a přístupu ke zadanému repozitáři ***digna***. Tento příkaz ověřuje, že CLI může s repozitářem komunikovat.
      
#### Použití příkazu
```bash
dignacli check-repo-connection
```

Po úspěšném provedení příkaz vypíše potvrzení o navázaném spojení spolu s detaily o repozitáři: verze repozitáře, Host, Databáze a Schema.  
  
Pokud připojení k repozitáři selže, zkontrolujte soubor config.toml pro správná konfiguracní nastavení.


### version

Pro kontrolu nainstalované verze *dignacli* použijte volbu `--version`.  
  
#### Použití příkazu
```bash
dignacli --version
```
  
#### Ukázkový výstup
```bash
dignacli version 2026.01
```

### možnosti logování
  
Ve výchozím nastavení je výstup příkazů ***digna*** do konzole navržen jako minimalistický. Většina příkazů nabízí možnost poskytnout dodatečné informace pomocí následujících voleb:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ a „debug“ definují úroveň podrobností, zatímco přepínač „logfile“ umožňuje přesměrovat výstup do souboru místo do konzolového okna.

## Správa uživatelů

### add-user
  
Příkaz `add-user` v CLI ***digna*** se používá k přidání nového uživatele do systému ***digna***.
  
#### Použití příkazu
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenty

- **USER_NAME**: Uživatelské jméno pro nového uživatele (povinné).
- **USER_FULL_NAME**: Celé jméno nového uživatele (povinné).
- **USER_PASSWORD**: Heslo pro nového uživatele (povinné).

#### Volby

- `--is_superuser`, `-su`: Příznak označující nového uživatele jako administrátora.
- `--valid_until`, `-vu`: Nastaví datum vypršení platnosti uživatelského účtu ve formátu `YYYY-MM-DD HH:MI:SS`. Pokud není nastaveno, účet nemá datum vypršení.

#### Příklad

Pro přidání nového uživatele s uživatelským jménem `jdoe`, celým jménem `John Doe` a heslem `password123`:

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
- **USER_NAME**: Uživatelské jméno uživatele, který má být smazán (povinné). Toto je jediný požadovaný argument příkazu.

#### Příklad
```bash
dignacli delete-user jdoe
```
  
Spuštěním tohoto příkazu bude uživatel `jdoe` odstraněn ze systému ***digna***, zruší se mu přístup a budou smazána jeho přidružená data a oprávnění z repozitáře.

### modify-user

Příkaz `modify-user` v CLI ***digna*** slouží k aktualizaci údajů existujícího uživatele v systému ***digna***.

#### Použití příkazu
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenty
  
- **USER_NAME**: Uživatelské jméno uživatele, který má být upraven (povinné).
- **USER_FULL_NAME**: Nové celé jméno uživatele (povinné).
  
#### Volby  
  
- `--is_superuser`, `-su`: Nastaví uživatele jako superuživatele, čímž uděluje zvýšená oprávnění. Tento přepínač nevyžaduje hodnotu.  
- `--valid_until`, `-vu`: Nastaví datum vypršení platnosti účtu ve formátu YYYY-MM-DD HH:MI:SS. Pokud není zadáno, účet zůstává platný na dobu neurčitou.  
  
#### Příklad
  
Pro změnu celého jména uživatele `jdoe` na „Johnathan Doe“ a nastavení uživatele jako superuživatele:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Příkaz `modify-user-pwd` v CLI ***digna*** se používá ke změně hesla existujícího uživatele v systému ***digna***.
  
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

Spuštěním tohoto příkazu se CLI připojí k repozitáři ***digna*** a vypíše všechny uživatele, zobrazí jejich ID, uživatelské jméno, celé jméno, stav superuživatele a časová razítka expirace.

## Správa repozitáře

### upgrade-repo
  
Příkaz `upgrade-repo` v CLI ***digna*** se používá k upgradování nebo inicializaci repozitáře ***digna***. Tento příkaz je zásadní pro aplikaci aktualizací nebo pro prvotní nastavení infrastruktury repozitáře.
  
#### Použití příkazu

```bash
dignacli upgrade-repo [options]
```
  
#### Volby
  
- `--simulation-mode`, `-s`: Po zapnutí tento režim spustí příkaz v simulačním módu, který vytiskne SQL příkazy, jež by byly provedeny, ale ve skutečnosti je neprovede. To je užitečné pro náhled změn bez provedení úprav v repozitáři.  

  
#### Příklad
  
Pro upgrade repozitáře ***digna*** můžete spustit příkaz bez voleb:
  
```bash
dignacli upgrade-repo
```  
Pro spuštění upgradu v simulačním režimu (zobrazit SQL příkazy bez jejich aplikace):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Tento příkaz je klíčový pro udržení systému ***digna***, zajišťuje, že schéma databáze a další komponenty repozitáře jsou aktuální s nejnovější verzí softwaru.

### encrypt
  
Příkaz `encrypt` v CLI ***digna*** slouží k zašifrování hesla.
  
#### Použití příkazu
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenty
- **PASSWORD**: Heslo, které je třeba zašifrovat (povinné).
  
#### Příklad
  
Pro zašifrování hesla je nutné zadat heslo jako argument.   
Například pro zašifrování hesla `mypassword123` použijte:
```bash
dignacli encrypt mypassword123
```
Tento příkaz vypíše zašifrovanou verzi zadaného hesla, která může být následně použita v zabezpečených kontextech. Pokud argument hesla nebude poskytnut, CLI zobrazí chybu indikující chybějící argument.

### generate-key
  
Příkaz `generate-key` se používá k vygenerování Fernet klíče, který je nezbytný pro zabezpečení hesel uložených v repozitáři ***digna***.
  
#### Použití příkazu
```bash
dignacli generate-key
```
  
## Správa dat

### clean-up

Příkaz `clean-up` v CLI ***digna*** slouží k odstranění profilů, predikcí a dat systému semaforu (traffic light system) pro jeden nebo více datových zdrojů v rámci zadaného projektu. Tento příkaz je důležitý pro řízení životního cyklu dat a pomáhá udržovat přehledné a efektivní datové prostředí odstraněním zastaralých nebo nepotřebných dat.

#### Použití příkazu

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Název projektu, ze kterého mají být data odstraněna (povinné). Použití klíčového slova all-projects v tomto argumentu instruuje ***digna***, aby iteroval přes všechny existující projekty a aplikoval příkaz.
- **FROM_DATE**: Počáteční datum a čas pro odstranění dat. Přijatelné formáty zahrnují %Y-%m-%d, %Y-%m-%dT%H:%M:%S nebo %Y-%m-%d %H:%M:%S (povinné).
- **TO_DATE**: Konečné datum a čas pro odstranění dat, v témže formátu jako FROM_DATE (povinné).
  
#### Volby
  
- `--table-name`, `-tn`: Omezuje operaci clean-up na konkrétní tabulku v projektu.
- `--table-filter`, `-tf`: Filtruje operaci clean-up tak, aby zahrnovala pouze tabulky obsahující zadaný podřetězec v názvu.
- `--timing`, `-tm`: Po dokončení zobrazí dobu trvání procesu clean-up.
- `--help`: Zobrazí nápovědu pro příkaz clean-up a ukončí se.
  
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
  
Příkaz `remove-orphans` v CLI ***digna*** slouží k údržbě repozitáře ***digna***.  
Když uživatel smaže projekty nebo datové zdroje, profily a predikce zůstanou v repozitáři. Tento příkaz odstraní takové osiřelé záznamy z repozitáře.
  
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

Tento příkaz je zvláště užitečný pro administrátory a uživatele spravující více projektů, poskytuje rychlý přehled dostupných projektů v repozitáři ***digna***.

### list-ds

Příkaz `list-ds` v CLI ***digna*** slouží k zobrazení seznamu všech dostupných datových zdrojů v rámci zadaného projektu. Tento příkaz je užitečný pro získání přehledu o datech dostupných pro analýzu a správu v systému ***digna***.

#### Použití příkazu
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenty
- **PROJECT_NAME**: Název projektu, pro který se vypisují datové zdroje (povinné).
  
#### Příklad
  
Pro výpis všech datových zdrojů v projektu s názvem `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Tento příkaz poskytuje uživatelům přehled o datových zdrojích dostupných v projektu, což jim pomáhá efektivněji se orientovat a spravovat datovou krajinu.


### inspect

Příkaz `inspect` v CLI ***digna*** slouží k vytvoření profilů, predikcí a dat semaforu (traffic light system) pro jeden nebo více datových zdrojů v rámci zadaného projektu. Tento příkaz pomáhá analyzovat a monitorovat data za definované období. Po dokončení inspekce je vrácena hodnota vypočteného semaforu:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Použití příkazu

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Název projektu, pro který mají být data inspektována (povinné). Použití klíčového slova all-projects v tomto argumentu instruuje ***digna***, aby prošla všechny existující projekty a aplikovala příkaz.
- **FROM_DATE**: Počáteční datum a čas pro inspekci dat. Přijatelné formáty zahrnují %Y-%m-%d, %Y-%m-%dT%H:%M:%S nebo %Y-%m-%d %H:%M:%S (povinné).
- **TO_DATE**: Konečné datum a čas pro inspekci dat, v témže formátu jako FROM_DATE (povinné).
  
#### Volby

- `--table-name`, `-tn`: Omezuje inspekci na konkrétní tabulku v projektu.
- `--table-filter`, `-tf`: Filtruje tak, aby se inspekce vztahovala pouze na tabulky obsahující zadaný podřetězec v názvu.
- `--enable_notification`, `-en`: Povolí odesílání notifikací v případě alertů.
- `--bypass-backend`, `-bb`: Obchází backend a spustí inspekci přímo z CLI (pouze pro testovací účely!).

  
#### Příklad
  
Pro inspekci dat projektu `ProjectA` od 1. ledna 2024 do 31. ledna 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Pro inspekci pouze konkrétní tabulky a vynucení přepočtu predikcí:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Tento příkaz je užitečný pro generování aktualizovaných profilů a predikcí, monitorování integrity dat a správu alertů v rámci zadaného časového okna projektu.

### inspect-async

Příkaz `inspect-async` v CLI ***digna*** slouží k vytvoření profilů, predikcí a dat semaforu pro jeden nebo více datových zdrojů v rámci zadaného projektu. Tento příkaz pomáhá analyzovat a monitorovat data za definované období. Na rozdíl od příkazu `inspect` tento příkaz nečeká na dokončení inspekce. Místo toho vrátí ID požadavku pro odeslanou asynchronní inspekční žádost. Pro sledování průběhu inspekce použijte příkaz `inspect-status`.

#### Použití příkazu

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Název projektu, pro který mají být data inspektována (povinné). Použití klíčového slova all-projects v tomto argumentu instruuje ***digna***, aby prošla všechny existující projekty a aplikovala příkaz.
- **FROM_DATE**: Počáteční datum a čas pro inspekci dat. Přijatelné formáty zahrnují %Y-%m-%d, %Y-%m-%dT%H:%M:%S nebo %Y-%m-%d %H:%M:%S (povinné).
- **TO_DATE**: Konečné datum a čas pro inspekci dat, v témže formátu jako FROM_DATE (povinné).
  
#### Volby

- `--table-name`, `-tn`: Omezuje inspekci na konkrétní tabulku v projektu.
- `--table-filter`, `-tf`: Filtruje tak, aby se inspekce vztahovala pouze na tabulky obsahující zadaný podřetězec v názvu.
- `--enable_notification`, `-en`: Povolí odesílání notifikací v případě alertů.

  
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

Příkaz `inspect-cancel` v CLI ***digna*** slouží k zrušení inspekcí na základě ID požadavku nebo k zrušení všech aktuálních požadavků.

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

Pro zrušení všech požadavků, které jsou aktuálně spuštěné nebo čekající:
  
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

#### Volby

- `--table_name`, `-tn`: Exportovat konkrétní datový zdroj z projektu.
- `--exportfile`, `-ef`: Určit název souboru pro export.
    
#### Příklad
  
Pro export všech datových zdrojů z projektu s názvem `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Tento příkaz exportuje všechny datové zdroje z `ProjectA` jako JSON dokument, který lze importovat do jiného projektu nebo repozitáře ***digna***.


### import-ds

Příkaz `import-ds` v CLI ***digna*** slouží k importu datových zdrojů do cílového projektu a k vytvoření importní zprávy.

#### Použití příkazu
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenty
- **PROJECT_NAME**: Název projektu, do kterého budou datové zdroje importovány.
- **EXPORT_FILE**: Název souboru s exportem datových zdrojů, který bude importován.

#### Volby

- `--output-file`, `-o`: Soubor pro uložení importní zprávy (pokud není specifikováno, tiskne se do terminálu v tabulární podobě).
- `--output-format`, `-f`: Formát uložení importní zprávy (json, csv).
    
#### Příklad
  
Pro import všech datových zdrojů ze souboru exportu `my_export.json` do `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po importu tento příkaz také zobrazí zprávu o importovaných a přeskočených objektech. Do `ProjectB` budou importovány pouze nové datové zdroje. Chcete‑li zjistit, které objekty by byly importovány a které přeskočeny, můžete použít příkaz `plan-import-ds`.

### plan-import-ds

Příkaz `plan-import-ds` v CLI ***digna*** slouží k analýze exportu datových zdrojů před vlastním importem a vytvoření importní zprávy.

#### Použití příkazu
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenty
- **PROJECT_NAME**: Název projektu, do kterého by byly datové zdroje importovány.
- **EXPORT_FILE**: Název souboru s exportem datových zdrojů, který bude analyzován před importem.

#### Volby

- `--output-file`, `-o`: Soubor pro uložení importní zprávy (pokud není specifikováno, tiskne se do terminálu v tabulární podobě).
- `--output-format`, `-f`: Formát uložení importní zprávy (json, csv).
    
#### Příklad
  
Pro zjištění, které datové zdroje by byly importovány a které by byly přeskočeny ze souboru `my_export.json` při importu do `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Tento příkaz pouze zobrazí plán importu objektů, které budou importovány a které přeskočeny.