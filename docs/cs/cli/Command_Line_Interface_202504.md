---
title: digna CLI Reference 2025.04 – Příkazy & Příklady | digna Dokumentace
description: Kompletní referenční přehled pro digna CLI verzi 2025.04. Naučte se spravovat uživatele, repozitáře a data pomocí příkazů jako add-user, check-repo-connection, upgrade-repo, inspect a dalších.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202504/
image: /assets/logo_square.png
---

# digna CLI Reference 2025.04
**2025-04-01**

Tato stránka dokumentuje kompletní sadu příkazů dostupných v CLI nástroji ***digna*** verze **2025.04**, včetně ukázek použití a možností.

---

## Základy CLI

---

## Použití volby `--help`

Volba `--help` poskytuje informace o dostupných příkazech a jejich použití. Existují dva hlavní způsoby použití této volby:

1. **Zobrazení obecné nápovědy:**
   
    Použijte --help bezprostředně po klíčovém slovu ***dignacli***
   ```bash
   dignacli --help
   ```

2. **Získání nápovědy pro konkrétní příkaz:**  
  
    Pro podrobné informace o konkrétním příkazu připojte `--help` k tomuto příkazu.
    Například pro získání nápovědy k příkazu `add-user` spusťte:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Popis příkazu:** Nabízí podrobný popis toho, co příkaz dělá.  
     - **Syntaxe:** Ukazuje přesnou syntaxi včetně povinných a volitelných argumentů.  
     - **Možnosti:** Vypisuje možnosti specifické pro příkaz spolu s jejich vysvětlením.  
     - **Příklady:** Poskytuje příklady, jak příkaz efektivně spustit.

  
## Použití příkazu `check-repo-connection`

Příkaz check-repo-connection je nástroj v rámci CLI ***digna*** určený k otestování konektivity a přístupu k určenému repozitáři ***digna***. Tento příkaz ověřuje, že CLI může s repozitářem komunikovat.
      
#### Použití příkazu
```bash
dignacli check-repo-connection
```

Po úspěšném provedení příkaz vypíše potvrzení o připojení spolu s informacemi o repozitáři: verze repozitáře, hostitel, databáze a schéma.  
  
Pokud připojení k repozitáři není úspěšné, zkontrolujte soubor config.toml kvůli správnému nastavení konfigurace.

## Použití příkazu `--version`

Pro zjištění nainstalované verze *dignacli* použijte volbu --version.  
  
#### Použití příkazu
```bash
dignacli --version
```
  
#### Příklad výstupu
```bash
dignacli version 2025.04
```

## Použití možností logování
  
Ve výchozím nastavení je výstup do konzole příkazů ***digna*** navržen jako minimalistický. Většina příkazů nabízí možnost poskytnout další informace pomocí následujících voleb:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ a „debug“ určují úroveň detailu, zatímco přepínač „logfile“ umožňuje přesměrovat výstup do souboru namísto konzolového okna.

## Správa uživatelů

### Použití příkazu `add-user`
  
Příkaz add-user v CLI ***digna*** slouží k přidání nového uživatele do systému ***digna***.
  
#### Použití příkazu
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumenty

- **USER_NAME**: Uživatelské jméno nového uživatele (povinné).
- **USER_FULL_NAME**: Plné jméno nového uživatele (povinné).
- **USER_PASSWORD**: Heslo pro nového uživatele (povinné).

#### Možnosti

- `--is_superuser`, `-su`: Přepínač k označení nového uživatele jako administrátora.
- `--valid_until`, `-vu`: Nastaví datum vypršení platnosti uživatelského účtu ve formátu `YYYY-MM-DD HH:MI:SS`. Pokud není nastaveno, účet nemá datum vypršení.

#### Příklad

Pro přidání nového uživatele s uživatelským jménem `jdoe`, plným jménem `John Doe` a heslem `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Pro přidání nového uživatele a nastavení data vypršení účtu:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Použití příkazu `delete-user`
  
Příkaz `delete-user` v CLI ***digna*** slouží k odstranění existujícího uživatele ze systému ***digna***.
  
#### Použití příkazu
```bash
dignacli delete-user USER_NAME
```
  
##### Argumenty
- **USER_NAME**: Uživatelské jméno uživatele, který má být smazán (povinné). Toto je jediný argument vyžadovaný příkazem.

#### Příklad
```bash
dignacli delete-user jdoe
```
  
Provedením tohoto příkazu bude uživatel `jdoe` odstraněn ze systému ***digna***, bude mu odebrán přístup a jeho související data a oprávnění v repozitáři budou smazány.

### Použití příkazu `modify-user`

Příkaz `modify-user` v CLI ***digna*** slouží k aktualizaci údajů existujícího uživatele v systému ***digna***.

#### Použití příkazu
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumenty
  
- **USER_NAME**: Uživatelské jméno uživatele, který má být upraven (povinné).
- **USER_FULL_NAME**: Nové celé jméno uživatele (povinné).
  
#### Možnosti  
  
- `--is_superuser`, `-su`: Nastaví uživatele jako superuživatele, čímž udělí zvýšená oprávnění. Tento přepínač nevyžaduje hodnotu.  
- `--valid_until`, `-vu`: Nastaví datum vypršení platnosti uživatelského účtu ve formátu YYYY-MM-DD HH:MI:SS. Pokud není poskytnuto, účet zůstane platný neomezeně.  
  
#### Příklad
  
Pro změnu plného jména uživatele `jdoe` na „Johnathan Doe“ a nastavení uživatele jako superuživatele:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Použití příkazu `modify-user-pwd`
  
Příkaz `modify-user-pwd` v CLI ***digna*** slouží ke změně hesla existujícího uživatele v systému ***digna***.
  
#### Použití příkazu
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumenty
  
- **USER_NAME**: Uživatelské jméno uživatele, jehož heslo má být změněno (povinné).
- **USER_PWD**: Nové heslo pro uživatele (povinné).
  
#### Příklad
  
Pro změnu hesla uživatele `jdoe` na `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Použití příkazu `list-users`

Příkaz `list-users` v CLI ***digna*** zobrazí seznam všech uživatelů registrovaných v systému ***digna***.

#### Použití příkazu

```bash
dignacli list-users
```

Spuštěním tohoto příkazu se CLI připojí k repozitáři ***digna*** a vypíše všechny uživatele, zobrazí jejich ID, uživatelské jméno, plné jméno, stav superuživatele a časy vypršení platnosti.

## Správa repozitáře

### Použití příkazu `upgrade-repo`
  
Příkaz `upgrade-repo` v CLI ***digna*** slouží k aktualizaci nebo inicializaci repozitáře ***digna***. Tento příkaz je nezbytný pro aplikaci aktualizací nebo pro první nastavení infrastruktury repozitáře.
  
#### Použití příkazu

```bash
dignacli upgrade-repo [options]
```
  
#### Možnosti
  
- `--simulation-mode`, `-s`: Po zapnutí spustí příkaz v režimu simulace, který vypíše SQL příkazy, které by byly vykonány, ale skutečně je neprovede. To je užitečné pro náhled změn bez jejich aplikace.  

  
#### Příklad
  
Pro aktualizaci repozitáře ***digna*** můžete spustit příkaz bez voleb:
  
```bash
dignacli upgrade-repo
```  
Pro spuštění aktualizace v režimu simulace (zobrazí SQL příkazy bez jejich aplikace):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Tento příkaz je klíčový pro udržování systému ***digna***, zajišťuje, že schéma databáze a další komponenty repozitáře jsou aktuální s nejnovější verzí softwaru.

### Použití příkazu `encrypt`
  
Příkaz `encrypt` v CLI ***digna*** slouží k zašifrování hesla.
  
#### Použití příkazu
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenty
- **PASSWORD**: Heslo, které má být zašifrováno (povinné).
  
#### Příklad
  
Pro zašifrování hesla musíte poskytnout heslo jako argument.   
Například pro zašifrování hesla `mypassword123` použijte:
```bash
dignacli encrypt mypassword123
```
Tento příkaz vypíše zašifrovanou verzi poskytnutého hesla, kterou lze následně použít v bezpečných kontextech. Pokud není argument hesla poskytnut, CLI zobrazí chybu s informací o chybějícím argumentu.

## Použití příkazu `generate-key`
  
Příkaz `generate-key` slouží k vygenerování klíče Fernet, který je nezbytný pro zabezpečení hesel uložených v repozitáři ***digna***.
  
#### Použití příkazu
```bash
dignacli generate-key
```
  
## Správa dat

## Použití příkazu `clean-up`

Příkaz `clean-up` v CLI ***digna*** slouží k odstranění profilů, predikcí a dat systému semaforů (traffic light system) pro jeden nebo více datových zdrojů v rámci zadaného projektu. Tento příkaz je důležitý pro řízení životního cyklu dat a pomáhá udržovat přehledné a efektivní prostředí odstraněním zastaralých nebo nepotřebných dat.

#### Použití příkazu

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Název projektu, ze kterého mají být data odstraněna (povinné). Použití klíčového slova all-projects v tomto argumentu instruuje ***digna***, aby iterovalo přes všechny existující projekty a aplikovalo tento příkaz.
- **FROM_DATE**: Počáteční datum a čas pro odstranění dat. Přijatelné formáty zahrnují %Y-%m-%d, %Y-%m-%dT%H:%M:%S nebo %Y-%m-%d %H:%M:%S (povinné).
- **TO_DATE**: Konečné datum a čas pro odstranění dat, v souladu se stejnými formáty jako FROM_DATE (povinné).
  
#### Možnosti
  
- `--table-name`, `-tn`: Omezuje operaci clean-up na konkrétní tabulku v rámci projektu.
- `--table-filter`, `-tf`: Filtruje a omezuje clean-up na tabulky obsahující zadaný podřetězec v názvu.
- `--timing`, `-tm`: Po dokončení zobrazí dobu trvání procesu clean-up.
- `--help`: Zobrazí nápovědu k příkazu clean-up a ukončí se.
  
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

## Použití příkazu `list-projects`
  
Příkaz `list-projects` v CLI ***digna*** se používá k zobrazení seznamu všech dostupných projektů v systému ***digna***.
  
#### Použití příkazu
  
```bash
dignacli list-projects
```

Tento příkaz je zvláště užitečný pro administrátory a uživatele spravující více projektů, poskytuje rychlý přehled o dostupných projektech v repozitáři ***digna***.

## Použití příkazu `list-ds`

Příkaz `list-ds` v CLI ***digna*** slouží k zobrazení seznamu všech dostupných datových zdrojů v rámci zadaného projektu. Tento příkaz je užitečný pro pochopení datových aktiv dostupných pro analýzu a správu v systému ***digna***.

#### Použití příkazu
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenty
- **PROJECT_NAME**: Název projektu, pro který se vypisují datové zdroje (povinné).
  
#### Příklad
  
Pro vypsání všech datových zdrojů v projektu s názvem `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Tento příkaz poskytuje uživatelům přehled o datových zdrojích v projektu a usnadňuje orientaci a správu datového prostředí.


## Použití příkazu `inspect`

Příkaz `inspect` v CLI ***digna*** slouží k vytvoření profilů, predikcí a dat systému semaforů (traffic light system) pro jeden nebo více datových zdrojů v rámci zadaného projektu. Tento příkaz pomáhá analyzovat a monitorovat data v definovaném časovém období.

#### Použití příkazu

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Název projektu, pro který mají být data inspektována (povinné). Použití klíčového slova all-projects v tomto argumentu instruuje ***digna***, aby iterovalo přes všechny existující projekty a aplikovalo tento příkaz.
- **FROM_DATE**: Počáteční datum a čas pro inspekci dat. Přijatelné formáty zahrnují %Y-%m-%d, %Y-%m-%dT%H:%M:%S nebo %Y-%m-%d %H:%M:%S (povinné).
- **TO_DATE**: Konečné datum a čas pro inspekci dat, v souladu se stejnými formáty jako FROM_DATE (povinné).
  
#### Možnosti

- `--table-name`, `-tn`: Omezuje inspekci na konkrétní tabulku v rámci projektu.
- `--table-filter`, `-tf`: Filtruje inspekci pouze na tabulky obsahující zadaný podřetězec v názvech.
- `--do-profile`: Spouští znovu sběr profilů. Výchozí je do-profile.
- `--no-do-profile`: Zabraňuje opětovnému sběru profilů.
- `--do-prediction`: Spouští přepočet predikcí. Výchozí je do-prediction.
- `--no-do-prediction`: Zabraňuje přepočtu predikcí.
- `--do-alert-status`: Spouští přepočet stavů alertů. Výchozí je do-alert-status.
- `--no-do-alert-status`: Zabraňuje přepočtu stavů alertů.
- `--iterative`: Spouští inspekci období pomocí denních iterací. Výchozí je iterative.
- `--no-iterative`: Spouští inspekci celého období najednou.
- `--enable_notification`, `-en`: Povolit odesílání notifikací v případě alertů.
- `--timing`, `-tm`: Po dokončení zobrazí dobu trvání inspekčního procesu.
  
#### Příklad
  
Pro inspekci dat projektu `ProjectA` od 1. ledna 2024 do 31. ledna 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Pro inspekci pouze konkrétní tabulky a vynucení přepočtu predikcí:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Tento příkaz je užitečný pro generování aktualizovaných profilů a predikcí, sledování integrity dat a správu systému alertů v rámci zadaného časového úseku projektu.

## Použití příkazu `tls-status`

Příkaz `tls-status` v CLI ***digna*** slouží k dotazu na stav Traffic Light System (TLS) pro konkrétní tabulku v projektu ke zvolenému datu. Systém semaforů poskytuje přehled o zdraví a kvalitě dat, indikující případné problémy nebo alerty, které vyžadují pozornost.
  
#### Použití příkazu
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumenty
  
- **PROJECT_NAME**: Název projektu, pro který se dotazujete na stav TLS (povinné).
- **TABLE_NAME**: Konkrétní tabulka v projektu, pro kterou se požaduje stav TLS (povinné).
- **DATE**: Datum, pro které se dotazujete na stav TLS, obvykle ve formátu %Y-%m-%d (povinné).
  
#### Příklad
  
Pro zjištění stavu TLS pro tabulku UserData v projektu ProjectA k 1. červenci 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Tento příkaz pomáhá uživatelům monitorovat a udržovat kvalitu dat tím, že poskytuje jasnou a akční zprávu o stavu na základě předdefinovaných kritérií.

## Použití příkazu `inspect-async`

Příkaz `inspect-async` v CLI ***digna*** slouží k zadání backendu, aby asynchronně provedl inspekci pro jeden nebo více datových zdrojů v daném projektu. Pokud je project_name nastaveno na all-projects, inspekce projde všechny dostupné projekty a provede inspekci. Vrací ID požadavku, které lze použít pro sledování průběhu inspekce.

#### Použití příkazu

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Název projektu, pro který mají být data inspektována (povinné). Použití klíčového slova all-projects v tomto argumentu instruuje ***digna***, aby iterovalo přes všechny existující projekty a aplikovalo tento příkaz.
- **FROM_DATE**: Počáteční datum a čas pro inspekci dat. Přijatelné formáty zahrnují %Y-%m-%d, %Y-%m-%dT%H:%M:%S nebo %Y-%m-%d %H:%M:%S (povinné).
- **TO_DATE**: Konečné datum a čas pro inspekci dat, v souladu se stejnými formáty jako FROM_DATE (povinné).
  
#### Možnosti

- `--table-name`, `-tn`: Omezuje inspekci na konkrétní tabulku v rámci projektu.
- `--table-filter`, `-tf`: Filtruje inspekci pouze na tabulky obsahující zadaný podřetězec v názvech.

  
#### Příklad
  
Pro asynchronní inspekci dat projektu `ProjectA` od 1. ledna 2024 do 31. ledna 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Použití příkazu `inspect-status`

Příkaz `inspect-status` v CLI ***digna*** se používá ke kontrole průběhu asynchronní inspekce na základě ID požadavku.

#### Použití příkazu

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumenty
  
- **REQUEST_ID**: ID požadavku vrácené příkazem `inspect-async` 
  
#### Možnosti

- `--report_level`, `-rl`: Nastaví úroveň reportu: 'task' nebo 'step' [výchozí: task]
  
#### Příklad
  
Pro kontrolu průběhu inspekce s ID požadavku 12345 na detailní úrovni kroků:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Použití příkazu `export-ds`

Příkaz `export-ds` v CLI ***digna*** slouží k vytvoření exportu datových zdrojů z repozitáře ***digna***. Ve výchozím nastavení budou exportovány všechny datové zdroje z daného projektu.

#### Použití příkazu
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenty
- **PROJECT_NAME**: Název projektu, ze kterého budou datové zdroje exportovány.

#### Možnosti

- `--table_name`, `-tn`: Exportovat konkrétní datový zdroj z projektu.
- `--exportfile`, `-ef`: Určit jméno souboru pro export.
    
#### Příklad
  
Pro export všech datových zdrojů z projektu s názvem `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Tento příkaz exportuje všechny datové zdroje z `ProjectA` jako JSON dokument, který lze importovat do jiného projektu nebo repozitáře ***digna***.


## Použití příkazu `import-ds`

Příkaz `import-ds` v CLI ***digna*** slouží k importu datových zdrojů do cílového projektu a vytvoření importní zprávy.

#### Použití příkazu
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenty
- **PROJECT_NAME**: Název projektu, do kterého budou datové zdroje importovány.
- **EXPORT_FILE**: Název souboru exportu datových zdrojů, který se má importovat.

#### Možnosti

- `--output-file`, `-o`: Soubor pro uložení importní zprávy (pokud není zadán, vytiskne se do terminálu v tabulární formě).
- `--output-format`, `-f`: Formát pro uložení importní zprávy (json, csv).
    
#### Příklad
  
Pro import všech datových zdrojů ze souboru exportu `my_export.json` do projektu `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po importu tento příkaz také zobrazí zprávu o importovaných a přeskočených objektech. Do `ProjectB` budou importovány pouze nové datové zdroje. Pro zjištění, které objekty by byly importovány a které přeskočeny, můžete použít příkaz `plan-import-ds`.

## Použití příkazu `plan-import-ds`

Příkaz `plan-import-ds` v CLI ***digna*** slouží k analýze importu datových zdrojů do cílového projektu a vytvoření plánu importu (reportu), aniž by import skutečně provedl.

#### Použití příkazu
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenty
- **PROJECT_NAME**: Název projektu, do kterého by byly datové zdroje importovány.
- **EXPORT_FILE**: Název souboru exportu datových zdrojů, který má být analyzován před importem.

#### Možnosti

- `--output-file`, `-o`: Soubor pro uložení importní zprávy (pokud není zadán, vytiskne se do terminálu v tabulární formě).
- `--output-format`, `-f`: Formát pro uložení importní zprávy (json, csv).
    
#### Příklad
  
Pro zkontrolování, které datové zdroje by byly importovány a které by byly přeskočeny ze souboru exportu `my_export.json` při importu do `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Tento příkaz zobrazí pouze plán importu objektů, které budou importovány a které přeskočeny.