# digna CLI Reference 2024.11
**2024-11-03**

Tato stránka dokumentuje kompletní sadu příkazů dostupných v CLI nástroji ***digna***, vydání **2024.11**, včetně ukázkového použití a dostupných možností.


---
## Základy CLI

---

## Použití volby `--help`

Volba `--help` poskytuje informace o dostupných příkazech a způsobu jejich použití. Existují dva hlavní způsoby, jak tuto volbu použít:

1. **Zobrazení obecné nápovědy:**
   
   Zadejte `--help` bezprostředně za příkazem ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Získání nápovědy ke konkrétním příkazům:**  
  
   Pro detailní informace o konkrétním příkazu připojte `--help` k tomuto příkazu.  
   Například pro nápovědu k příkazu `add-user` spusťte:
   ```bash
   dignacli add-user --help
   ```

   ### výstup:
      
   - **Popis příkazu:** Podrobný popis toho, co příkaz provádí.  
   - **Syntaxe:** Ukazuje přesnou syntaxi včetně povinných a nepovinných argumentů.  
   - **Možnosti:** Seznam možností specifických pro příkaz spolu s jejich vysvětlením.  
   - **Příklady:** Ukazuje příklady, jak příkaz efektivně použít.

  
## Použití příkazu `check-repo-connection`

Příkaz `check-repo-connection` je nástroj v CLI ***digna*** určený k otestování konektivity a přístupu k určenému repozitáři ***digna***. Tento příkaz ověřuje, že CLI může s repozitářem komunikovat.
      
### Použití příkazu
```bash
dignacli check-repo-connection
```

Po úspěšném spuštění příkaz vypíše potvrzení o připojení spolu s detaily o repozitáři: verze repozitáře, hostitel, databáze a schéma.  
  
Pokud připojení k repozitáři není úspěšné, zkontrolujte soubor config.toml pro správná konfigurační nastavení.

## Použití příkazu `--version`

Pro zjištění nainstalované verze *dignacli* použijte volbu `--version`.  
  
### Použití příkazu
```bash
dignacli --version
```
  
### Příklad výstupu
```bash
dignacli version 2024.11
```

## Volby pro logování
  
Výstup příkazů ***digna*** v konzoli je ve výchozím nastavení minimalistický. Většina příkazů umožňuje zobrazit další informace pomocí následujících voleb:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
Volby „verbose“ a „debug“ určují úroveň detailu, zatímco přepínač „logfile“ umožňuje přesměrovat výstup do souboru místo na konzoli.

# Správa uživatelů

## Použití příkazu `add-user`
  
Příkaz `add-user` v CLI ***digna*** slouží k přidání nového uživatele do systému ***digna***.
  
### Použití příkazu
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenty

- **USER_NAME**: Uživatelské jméno nového uživatele (povinné).
- **USER_FULL_NAME**: Celé jméno nového uživatele (povinné).
- **USER_PASSWORD**: Heslo pro nového uživatele (povinné).

### Možnosti

- `--is_superuser`, `-su`: Příznak, který označí nového uživatele jako administrátora.
- `--valid_until`, `-vu`: Nastaví datum vypršení účtu ve formátu `YYYY-MM-DD HH:MI:SS`. Pokud není nastaveno, účet nemá datum vypršení platnosti.

### Příklad

Chcete-li přidat nového uživatele s uživatelským jménem `jdoe`, celým jménem `John Doe` a heslem `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Pro přidání nového uživatele a nastavení data vypršení účtu:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Použití příkazu `delete-user`
  
Příkaz `delete-user` v CLI ***digna*** slouží k odstranění existujícího uživatele ze systému ***digna***.
  
### Použití příkazu
```bash
dignacli delete-user USER_NAME
```
  
### Argumenty
- **USER_NAME**: Uživatelské jméno uživatele, který má být smazán (povinné). Toto je jediný argument požadovaný příkazem.

### Příklad
```bash
dignacli delete-user jdoe
```
  
Spuštěním tohoto příkazu bude uživatel `jdoe` odstraněn ze systému ***digna***, jeho přístup bude zrušen a související data a oprávnění v repozitáři budou smazána.

## Použití příkazu `modify-user`

Příkaz `modify-user` v CLI ***digna*** slouží k aktualizaci údajů existujícího uživatele v systému ***digna***.

### Použití příkazu
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenty
  
- **USER_NAME**: Uživatelské jméno uživatele, který má být upraven (povinné).
- **USER_FULL_NAME**: Nové celé jméno uživatele (povinné).
  
### Možnosti  
  
- `--is_superuser`, `-su`: Nastaví uživatele jako superuživatele, čímž mu udělí vyšší oprávnění. Tento přepínač nevyžaduje hodnotu.  
- `--valid_until`, `-vu`: Nastaví datum vypršení účtu ve formátu YYYY-MM-DD HH:MI:SS. Pokud není uvedeno, účet zůstává platný bez omezení.  
  
### Příklad
  
Pro změnu celého jména uživatele `jdoe` na „Johnathan Doe“ a nastavení uživatele jako superuživatele:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Použití příkazu `modify-user-pwd`
  
Příkaz `modify-user-pwd` v CLI ***digna*** slouží ke změně hesla existujícího uživatele v systému ***digna***.
  
### Použití příkazu
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumenty
  
- **USER_NAME**: Uživatelské jméno uživatele, jehož heslo má být změněno (povinné).
- **USER_PWD**: Nové heslo uživatele (povinné).
  
### Příklad
  
Pro změnu hesla uživatele `jdoe` na `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Použití příkazu `list-users`

Příkaz `list-users` v CLI ***digna*** zobrazí seznam všech uživatelů registrovaných v systému ***digna***.

### Použití příkazu

```bash
dignacli list-users
```

Spuštěním tohoto příkazu se CLI připojí k repozitáři ***digna*** a vypíše všechny uživatele, zobrazí jejich ID, uživatelské jméno, celé jméno, stav superuživatele a časové razítko vypršení platnosti.

# Správa repozitáře

### Použití příkazu `upgrade-repo`
  
Příkaz `upgrade-repo` v CLI ***digna*** se používá k aktualizaci nebo inicializaci repozitáře ***digna***. Tento příkaz je nezbytný pro aplikaci aktualizací nebo pro prvotní nastavení infrastruktury repozitáře.
  
### Použití příkazu

```bash
dignacli upgrade-repo [options]
```
  
### Možnosti
  
- `--simulation-mode`, `-s`: Po zapnutí poběží příkaz v simulačním režimu, který vytiskne SQL dotazy, jež by byly vykonány, ale skutečně je neprovede. To je užitečné pro nahlédnutí do změn bez jejich aplikace.  

  
### Příklad
  
Pro aktualizaci repozitáře ***digna*** spusťte příkaz bez voleb:
  
```bash
dignacli upgrade-repo
```  
Pro spuštění upgradu v simulačním režimu (zobrazí SQL dotazy bez jejich aplikace):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Tento příkaz je klíčový pro udržení systému ***digna*** tím, že zajistí, aby schéma databáze a další komponenty repozitáře odpovídaly nejnovější verzi softwaru.

## Použití příkazu `encrypt`
  
Příkaz `encrypt` v CLI ***digna*** slouží k zašifrování hesla.
  
### Použití příkazu
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenty
- **PASSWORD**: Heslo, které má být zašifrováno (povinné).
  
### Příklad
  
Pro zašifrování hesla je potřeba heslo předat jako argument.   
Například pro zašifrování hesla `mypassword123` použijte:
```bash
dignacli encrypt mypassword123
```
Tento příkaz vypíše zašifrovanou verzi zadaného hesla, kterou lze následně použít v zabezpečených kontextech. Pokud argument hesla chybí, CLI zobrazí chybu oznamující chybějící argument.

## Použití příkazu `generate-key`
  
Příkaz `generate-key` slouží k vygenerování Fernet klíče, který je nezbytný pro zabezpečení hesel uložených v repozitáři ***digna***.
  
### Použití příkazu
```bash
dignacli generate-key
```
  
# Správa dat

## Použití příkazu `clean-up`

Příkaz `clean-up` v CLI ***digna*** slouží k odstranění profilů, predikcí a dat systému semaforu (traffic light system) pro jeden nebo více datových zdrojů v rámci zadaného projektu. Tento příkaz je důležitý pro správu životního cyklu dat a pomáhá udržovat pořádek a efektivitu odstraněním zastaralých či nepotřebných dat.

### Použití příkazu

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenty
  
- **PROJECT_NAME**: Název projektu, ze kterého mají být data odstraněna (povinné). Použití klíčového slova `all-projects` v tomto argumentu způsobí, že ***digna*** iteruje přes všechny existující projekty a aplikuje tento příkaz.
- **FROM_DATE**: Počáteční datum a čas pro odstranění dat. Přijatelné formáty zahrnují %Y-%m-%d, %Y-%m-%dT%H:%M:%S nebo %Y-%m-%d %H:%M:%S (povinné).
- **TO_DATE**: Konečné datum a čas pro odstranění dat, se stejnými formáty jako FROM_DATE (povinné).
  
### Možnosti
  
- `--table-name`, `-tn`: Omezuje operaci čistky na konkrétní tabulku v projektu.
- `--table-filter`, `-tf`: Filtr, který omezuje čištění na tabulky obsahující zadaný podřetězec v názvu.
- `--timing`, `-tm`: Po dokončení zobrazí délku trvání procesu čištění.
- `--help`: Zobrazí nápovědu pro příkaz clean-up a ukončí se.
  
### Příklad
  
Pro odstranění dat z projektu ProjectA mezi 1. lednem 2023 a 30. červnem 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Pro odstranění dat pouze z konkrétní tabulky pojmenované `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Tento příkaz pomáhá řídit využití úložiště a zajišťuje, že repozitář obsahuje pouze relevantní informace.

## Použití příkazu `inspect`

Příkaz `inspect` v CLI ***digna*** slouží k vytvoření profilů, predikcí a dat pro systém semaforu (traffic light system) pro jeden nebo více datových zdrojů v zadaném projektu. Tento příkaz pomáhá analyzovat a monitorovat data za definované období.

### Použití příkazu

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenty
  
- **PROJECT_NAME**: Název projektu, pro který mají být data prozkoumána (povinné). Použití klíčového slova `all-projects` v tomto argumentu způsobí, že ***digna*** projde všechny existující projekty a aplikuje tento příkaz.
- **FROM_DATE**: Počáteční datum a čas pro inspekci dat. Přijatelné formáty zahrnují %Y-%m-%d, %Y-%m-%dT%H:%M:%S nebo %Y-%m-%d %H:%M:%S (povinné).
- **TO_DATE**: Konečné datum a čas pro inspekci dat, se stejnými formáty jako FROM_DATE (povinné).
  
### Možnosti

- `--table-name`, `-tn`: Omezuje inspekci na konkrétní tabulku v projektu.
- `--table-filter`, `-tf`: Filtr pro inspekci pouze těch tabulek, které obsahují zadaný podřetězec v názvu.
- `--do-profile`: Spustí znovu sběr profilů. Výchozí chování je do-profile.
- `--no-do-profile`: Zabrání opětovnému sběru profilů.
- `--do-prediction`: Spustí přepočet predikcí. Výchozí chování je do-prediction.
- `--no-do-prediction`: Zabrání přepočtu predikcí.
- `--do-alert-status`: Spustí přepočet stavů alertů. Výchozí chování je do-alert-status.
- `--no-do-alert-status`: Zabrání přepočtu stavů alertů.
- `--timing`, `-tm`: Po dokončení zobrazí dobu trvání inspekce.
  
### Příklad
  
Pro inspekci dat projektu `ProjectA` od 1. ledna 2024 do 31. ledna 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Pro inspekci pouze konkrétní tabulky a vynucení přepočtu predikcí:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Tento příkaz je užitečný pro generování aktualizovaných profilů a predikcí, monitorování integrity dat a správu systémů alertů v rámci zvoleného časového období projektu.

## Použití příkazu `tls-status`

Příkaz `tls-status` v CLI ***digna*** slouží k dotazu na stav Traffic Light System (TLS) pro konkrétní tabulku v projektu k danému datu. Systém semaforu poskytuje přehled o zdraví a kvalitě dat a upozorňuje na případné problémy nebo alerty, které vyžadují pozornost.
  
### Použití příkazu
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenty
  
- **PROJECT_NAME**: Název projektu, pro který se dotaz provádí (povinné).
- **TABLE_NAME**: Konkrétní tabulka v projektu, pro kterou je potřeba stav TLS (povinné).
- **DATE**: Datum, pro které se stav TLS dotazuje, obvykle ve formátu %Y-%m-%d (povinné).
  
### Příklad
  
Pro kontrolu stavu TLS pro tabulku UserData v projektu ProjectA k datu 1. července 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Tento příkaz pomáhá uživatelům monitorovat a udržovat kvalitu dat tím, že poskytuje jasné a akční informace založené na předdefinovaných kritériích.

## Použití příkazu `list-projects`
  
Příkaz `list-projects` v CLI ***digna*** slouží k zobrazení seznamu všech dostupných projektů v systému ***digna***.
  
### Použití příkazu
  
```bash
dignacli list-projects
```

Tento příkaz je obzvlášť užitečný pro administrátory a uživatele spravující více projektů, poskytuje rychlý přehled dostupných projektů v repozitáři ***digna***.

## Použití příkazu `list-ds`

Příkaz `list-ds` v CLI ***digna*** slouží k zobrazení seznamu všech dostupných datových zdrojů v rámci zvoleného projektu. Tento příkaz je užitečný pro orientaci v datových aktivech, která jsou k dispozici pro analýzu a správu v systému ***digna***.

### Použití příkazu
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumenty
- **PROJECT_NAME**: Název projektu, pro který se datové zdroje vypisují (povinné).
  
### Příklad
  
Pro výpis všech datových zdrojů v projektu `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Tento příkaz poskytuje uživatelům přehled o datových zdrojích v projektu a pomáhá jim efektivněji se orientovat a spravovat datové prostředí.