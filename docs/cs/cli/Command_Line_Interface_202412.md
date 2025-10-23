---
title: digna CLI Reference 2024.12 – Commands & Examples | digna Documentation
description: Kompletní reference pro vydání digna CLI 2024.12. Naučte se spravovat uživatele, repozitáře a data pomocí příkazů jako add-user, check-repo-connection, upgrade-repo, inspect a dalších.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202412/
image: /assets/logo_square.png
---


# digna CLI Reference 2024.12
**2024-12-09**

Tato stránka dokumentuje kompletní sadu příkazů dostupných v ***digna*** CLI verze **2024.12**, včetně ukázek použití a možností.

---


**2024-12-09**


---

## Základy CLI

---

## Použití volby `--help`

Volba `--help` poskytuje informace o dostupných příkazech a jejich použití. Existují dva hlavní způsoby, jak tuto volbu použít:

1. **Zobrazení obecné nápovědy:**
   
    Použijte –help bezprostředně za klíčovým slovem ***digna***cl  
   ```bash
   dignacli --help

3.  **Získání nápovědy pro konkrétní příkazy:**  
  
    Pro podrobné informace o konkrétním příkazu přidejte `--help` za tento příkaz.
    Například pro získání nápovědy k příkazu `add-user` spusťte:
     ```bash
     dignacli add-user --help
     ```

     ### výstup:
      
     - **Popis příkazu:** Nabízí podrobný popis toho, co příkaz dělá.  
     - **Syntaxe:** Ukazuje přesnou syntaxi, včetně povinných a volitelných argumentů.  
     - **Možnosti:** Vypisuje jakékoli volby specifické pro příkaz spolu s jejich vysvětlením.  
     - **Příklady:** Poskytuje příklady, jak příkaz efektivně spustit.

  
## Použití příkazu `check-repo-connection`

Příkaz check-repo-connection je nástroj v rámci ***digna*** CLI určený k otestování konektivity a přístupu k určenému repozitáři ***digna***. Tento příkaz ověřuje, zda může CLI komunikovat s repozitářem.
      
### Použití příkazu
```bash
dignacli check-repo-connection
```

Po úspěšném provedení příkaz vypíše potvrzení o připojení spolu s podrobnostmi o repozitáři: verze repozitáře, Host, Databáze a Schema.  
  
Pokud připojení k repozitáři není úspěšné, zkontrolujte konfigurační soubor config.toml, zda jsou v něm správná nastavení.

## Použití příkazu ‘version’

Pro zjištění nainstalované verze *dignacli* použijte volbu --version.  
  
### Použití příkazu
```bash
dignacli --version
```
  
### Příklad výstupu
```bash
dignacli version 2024.12
```

## Použití možností logování
  
Ve výchozím nastavení je výstup příkazů ***digna*** do konzole navržen jako minimalistický. Většina příkazů nabízí možnost poskytnout další informace pomocí následujících voleb:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ a „debug“ určují úroveň podrobností, zatímco přepínač „logfile“ umožňuje přesměrovat výstup do souboru místo do konzolového okna.

# Správa uživatelů

## Použití příkazu ‘add-user’
  
Příkaz add-user v ***digna*** CLI slouží k přidání nového uživatele do systému ***digna***.
  
### Použití příkazu
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenty

- **USER_NAME**: Uživatelské jméno nového uživatele (povinné).
- **USER_FULL_NAME**: Celé jméno nového uživatele (povinné).
- **USER_PASSWORD**: Heslo nového uživatele (povinné).

### Volby

- `--is_superuser`, `-su`: Příznak k označení nového uživatele jako administrátora.
- `--valid_until`, `-vu`: Nastaví datum vypršení platnosti účtu ve formátu `YYYY-MM-DD HH:MI:SS`. Pokud není nastaveno, účet nemá datum vypršení.

### Příklad

Pro přidání nového uživatele s uživatelským jménem `jdoe`, celým jménem `John Doe` a heslem `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Pro přidání nového uživatele a nastavení data vypršení platnosti účtu:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Použití příkazu `delete-user`
  
Příkaz `delete-user` v ***digna*** CLI slouží k odstranění existujícího uživatele ze systému ***digna***.
  
### Použití příkazu
```bash
dignacli delete-user USER_NAME
```
  
### Argumenty
- **USER_NAME**: Uživatelské jméno uživatele, který má být smazán (povinné). Toto je jediný požadovaný argument příkazu.

### Příklad
```bash
dignacli delete-user jdoe
```
  
Provedením tohoto příkazu bude uživatel `jdoe` odstraněn ze systému ***digna***, zruší se jeho přístup a budou odstraněna jeho související data a oprávnění z repozitáře.

## Použití příkazu `modify-user`

Příkaz `modify-user` v ***digna*** CLI slouží k aktualizaci údajů existujícího uživatele v systému ***digna***.

### Použití příkazu
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenty
  
- **USER_NAME**: Uživatelské jméno uživatele, který má být upraven (povinné).
- **USER_FULL_NAME**: Nové celé jméno uživatele (povinné).
  
### Volby  
  
- `--is_superuser`, `-su`: Nastaví uživatele jako superuživatele, čímž mu udělí rozšířená oprávnění. Tento přepínač nevyžaduje hodnotu.  
- `--valid_until`, `-vu`: Nastaví datum vypršení platnosti účtu ve formátu YYYY-MM-DD HH:MI:SS. Pokud není uvedeno, zůstává účet platný na dobu neurčitou.  
  
### Příklad
  
Pro změnu celého jména uživatele `jdoe` na „Johnathan Doe“ a nastavení uživatele jako superuživatele:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Použití příkazu `modify-user-pwd`
  
Příkaz `modify-user-pwd` v ***digna*** CLI slouží ke změně hesla existujícího uživatele v systému ***digna***.
  
### Použití příkazu
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumenty
  
- **USER_NAME**: Uživatelské jméno uživatele, jehož heslo se má změnit (povinné).
- **USER_PWD**: Nové heslo uživatele (povinné).
  
### Příklad
  
Pro změnu hesla uživatele `jdoe` na `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Použití příkazu `list-users`

Příkaz `list-users` v ***digna*** CLI zobrazí seznam všech uživatelů registrovaných v systému ***digna***.

### Použití příkazu

```bash
dignacli list-users
```

Spuštěním tohoto příkazu v ***digna*** CLI se CLI připojí k repozitáři ***digna*** a vypíše všechny uživatele, zobrazí jejich ID, uživatelské jméno, celé jméno, stav superuživatele a časová razítka vypršení platnosti.

# Správa repozitáře

### Použití příkazu `upgrade-repo`
  
Příkaz `upgrade-repo` v ***digna*** CLI slouží k upgradu nebo inicializaci repozitáře ***digna***. Tento příkaz je nezbytný pro aplikaci aktualizací nebo pro prvotní nastavení infrastruktury repozitáře.
  
### Použití příkazu

```bash
dignacli upgrade-repo [options]
```
  
### Volby
  
- `--simulation-mode`, `-s`: Pokud je povoleno, tento přepínač spustí příkaz v simulačním režimu, který vytiskne SQL příkazy, které by byly vykonány, ale skutečně je neprovede. To je užitečné pro náhled změn bez provedení úprav v repozitáři.  

  
### Příklad
  
Pro upgrade repozitáře ***digna*** můžete spustit příkaz bez jakýchkoli voleb:
  
```bash
dignacli upgrade-repo
```  
Pro spuštění upgradu v simulačním režimu (zobrazení SQL příkazů bez jejich aplikace):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Tento příkaz je klíčový pro údržbu systému ***digna*** a zajišťuje, že schéma databáze a další komponenty repozitáře jsou aktuální s nejnovější verzí softwaru.

## Použití příkazu `encrypt`
  
Příkaz `encrypt` v ***digna*** CLI slouží k zašifrování hesla.
  
### Použití příkazu
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenty
- **PASSWORD**: Heslo, které je třeba zašifrovat (povinné).
  
### Příklad
  
Pro zašifrování hesla musíte heslo předat jako argument.   
Například pro zašifrování hesla `mypassword123` použijte:
```bash
dignacli encrypt mypassword123
```
Tento příkaz vypíše zašifrovanou verzi předaného hesla, kterou lze následně použít v zabezpečených kontextech. Pokud argument s heslem není poskytnut, CLI zobrazí chybu oznamující chybějící argument.

## Použití příkazu `generate-key`
  
Příkaz `generate-key` se používá k vygenerování Fernet klíče, který je nezbytný pro zabezpečení hesel uložených v repozitáři ***digna***.
  
### Použití příkazu
```bash
dignacli generate-key
```
  
# Správa dat

## Použití příkazu `clean-up`

Příkaz `clean-up` v ***digna*** CLI slouží k odstranění profilů, predikcí a dat systému semaforů (traffic light system) pro jeden nebo více datových zdrojů v rámci zadaného projektu. Tento příkaz je důležitý pro řízení životního cyklu dat a pomáhá udržovat přehledné a efektivní prostředí odstraněním zastaralých nebo nepotřebných dat.

### Použití příkazu

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenty
  
- **PROJECT_NAME**: Název projektu, ze kterého se mají data odstranit (povinné). Použitím klíčového slova all-projects v tomto argumentu se ***digna*** přikáže iterovat přes všechny existující projekty a tento příkaz aplikovat.
- **FROM_DATE**: Počáteční datum a čas pro odstranění dat. Přijatelné formáty zahrnují %Y-%m-%d, %Y-%m-%dT%H:%M:%S nebo %Y-%m-%d %H:%M:%S (povinné).
- **TO_DATE**: Koncové datum a čas pro odstranění dat, následující stejné formáty jako FROM_DATE (povinné).
  
### Volby
  
- `--table-name`, `-tn`: Omezuje operaci clean-up na konkrétní tabulku v rámci projektu.
- `--table-filter`, `-tf`: Filtruje tak, aby se clean-up týkal pouze tabulek obsahujících zadaný podřetězec v názvu.
- `--timing`, `-tm`: Po dokončení zobrazí dobu trvání procesu clean-up.
- `--help`: Zobrazí nápovědu pro příkaz clean-up a ukončí.
  
### Příklad
  
Pro odstranění dat z projektu ProjectA mezi 1. lednem 2023 a 30. červnem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Pro odstranění dat pouze z konkrétní tabulky s názvem `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Tento příkaz pomáhá spravovat úložiště dat a zabezpečuje, že repozitář obsahuje pouze relevantní informace.

## Použití příkazu `inspect`

Příkaz `inspect` v ***digna*** CLI slouží k vytvoření profilů, predikcí a dat systému semaforů (traffic light system) pro jeden nebo více datových zdrojů v rámci zadaného projektu. Tento příkaz pomáhá analyzovat a monitorovat data během definovaného období.

### Použití příkazu

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenty
  
- **PROJECT_NAME**: Název projektu, pro který se mají data inspektovat (povinné). Použitím klíčového slova all-projects v tomto argumentu se ***digna*** přikáže iterovat přes všechny existující projekty a tento příkaz aplikovat.
- **FROM_DATE**: Počáteční datum a čas pro inspekci dat. Přijatelné formáty zahrnují %Y-%m-%d, %Y-%m-%dT%H:%M:%S nebo %Y-%m-%d %H:%M:%S (povinné).
- **TO_DATE**: Koncové datum a čas pro inspekci dat, následující stejné formáty jako FROM_DATE (povinné).
  
### Volby

- `--table-name`, `-tn`: Omezuje inspekci na konkrétní tabulku v rámci projektu.
- `--table-filter`, `-tf`: Filtruje tak, aby se inspekce týkala pouze tabulek obsahujících zadaný podřetězec v názvu.
- `--do-profile`: Spouští opětovné sbírání profilů. Výchozí je do-profile.
- `--no-do-profile`: Zabraňuje opětovnému sbírání profilů.
- `--do-prediction`: Spouští přepočet predikcí. Výchozí je do-prediction.
- `--no-do-prediction`: Zabraňuje přepočtu predikcí.
- `--do-alert-status`: Spouští přepočet stavů alertů. Výchozí je do-alert-status.
- `--no-do-alert-status`: Zabraňuje přepočtu stavů alertů.
- `--iterative`: Spouští inspekci období pomocí denních iterací. Výchozí je iterative.
- `--no-iterative`: Spouští inspekci celého období najednou.
- `--timing`, `-tm`: Po dokončení zobrazí dobu trvání procesu inspekce.
  
### Příklad
  
Pro inspekci dat projektu `ProjectA` od 1. ledna 2024 do 31. ledna 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Pro inspekci pouze konkrétní tabulky a vynucení přepočtu predikcí:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Tento příkaz je užitečný pro generování aktualizovaných profilů a predikcí, sledování integrity dat a správu alert systémů v rámci zadaného časového rozsahu projektu.

## Použití příkazu `tls-status`

Příkaz `tls-status` v ***digna*** CLI slouží k dotazu na stav Traffic Light System (TLS) pro konkrétní tabulku v projektu k danému datu. Traffic Light System poskytuje přehled o zdravotním stavu a kvalitě dat a indikuje případné problémy nebo alerty, které vyžadují pozornost.
  
### Použití příkazu
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenty
  
- **PROJECT_NAME**: Název projektu, pro který se dotaz provádí (povinné).
- **TABLE_NAME**: Konkrétní tabulka v projektu, pro kterou je potřeba stav TLS (povinné).
- **DATE**: Datum, pro které se stav TLS dotazuje, obvykle ve formátu %Y-%m-%d (povinné).
  
### Příklad
  
Pro kontrolu stavu TLS pro tabulku UserData v projektu ProjectA k 1. červenci 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Tento příkaz pomáhá uživatelům sledovat a udržovat kvalitu dat tím, že poskytuje jasnou a akční zprávu o stavu na základě předdefinovaných kritérií.

## Použití příkazu `list-projects`
  
Příkaz `list-projects` v ***digna*** CLI slouží k zobrazení seznamu všech dostupných projektů v systému ***digna***.
  
### Použití příkazu
  
```bash
dignacli list-projects
```

Tento příkaz je zvláště užitečný pro administrátory a uživatele spravující více projektů, poskytuje rychlý přehled dostupných projektů v repozitáři ***digna***.

## Použití příkazu `list-ds`

Příkaz `list-ds` v ***digna*** CLI slouží k zobrazení seznamu všech dostupných datových zdrojů v rámci zadaného projektu. Tento příkaz je užitečný pro orientaci v datových aktivech dostupných pro analýzu a správu v systému ***digna***.

### Použití příkazu
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumenty
- **PROJECT_NAME**: Název projektu, pro který se datové zdroje vypisují (povinné).
  
### Příklad
  
Pro vypsání všech datových zdrojů v projektu s názvem `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Tento příkaz poskytuje uživatelům přehled datových zdrojů dostupných v projektu a pomáhá jim efektivněji se orientovat a spravovat datové prostředí.