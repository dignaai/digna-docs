---
title: Referenční příručka digna CLI 2024.09 – Příkazy a příklady | Dokumentace digna
description: Kompletní reference pro vydání digna CLI 2024.09. Naučte se spravovat uživatele, repozitáře a data pomocí příkazů jako add-user, check-repo-connection, upgrade-repo, inspect, tls-status a dalších.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202408/
image: /assets/logo_square.png
---

# digna CLI Reference 2024.09
**2024-08-24**

---

## Základy CLI

---

### help

Možnost --help poskytuje informace o dostupných příkazech a jejich použití. Existují dva hlavní způsoby, jak tuto možnost použít:

1. **Zobrazení obecné nápovědy:**
   
    Použijte --help těsně za příkazem ***digna***
   bash
   dignacli --help

2.  **Nápověda pro konkrétní příkazy:**  
  
    Pro podrobné informace o konkrétním příkazu připojte k tomu příkazu --help.
    Například pro zobrazení nápovědy k příkazu add-user spusťte:
     bash
     dignacli add-user --help
     

     ### výstup:
      
     - **Popis příkazu:** Podrobný popis, co příkaz provádí.  
     - **Syntax:** Ukazuje přesnou syntaxi včetně povinných a volitelných argumentů.  
     - **Možnosti:** Seznam možností specifických pro příkaz spolu s jejich vysvětlením.  
     - **Příklady:** Ukázky, jak příkaz efektivně použít.

  
### check-repo-connection

Příkaz check-repo-connection je nástroj v rámci ***digna*** CLI určený k otestování konektivity a přístupu k určenému ***digna*** repozitáři. Tento příkaz ověřuje, že CLI dokáže s repozitářem komunikovat.
      
##### Použití příkazu
bash
dignacli check-repo-connection


Po úspěšném provedení příkaz vypíše potvrzení o připojení spolu s informacemi o repozitáři: verze repozitáře, hostitel, databáze a schéma.  
  
Pokud se připojení k repozitáři nezdaří, zkontrolujte soubor config.toml, zda obsahuje správná konfigurační nastavení.

### version

Pro zjištění nainstalované verze *dignacli* použijte volbu --version.  
  
#### Použití příkazu
bash
dignacli --version

  
#### Příklad výstupu
bash
dignacli version 2024.09


### možnosti protokolování
  
Ve výchozím nastavení je výstup příkazů ***digna*** do konzole navržen minimalisticky. Většina příkazů umožňuje zobrazit dodatečné informace pomocí následujících možností:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
„verbose“ a „debug“ určují úroveň podrobností, zatímco přepínač „logfile“ umožňuje přesměrovat výstup do souboru namísto konzole.

## Správa uživatelů

### add-user
  
Příkaz add-user v ***digna*** CLI slouží k přidání nového uživatele do systému ***digna***.
  
#### Použití příkazu
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argumenty

- **USER_NAME**: Uživatelské jméno nového uživatele (povinné).
- **USER_FULL_NAME**: Celé jméno nového uživatele (povinné).
- **USER_PASSWORD**: Heslo pro nového uživatele (povinné).

#### Možnosti

- --is_superuser, -su: Přepínač, kterým se novému uživateli udělí administrátorská práva.
- --valid_until, -vu: Nastaví datum vypršení platnosti účtu ve formátu YYYY-MM-DD HH:MI:SS. Pokud není nastaveno, účet nemá datum vypršení.

#### Příklad

Pro přidání nového uživatele s uživatelským jménem jdoe, celým jménem John Doe a heslem password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Pro přidání nového uživatele a nastavení data expirace účtu:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


### delete-user
  
Příkaz delete-user v ***digna*** CLI slouží k odstranění existujícího uživatele ze systému ***digna***.
  
##### Použití příkazu
bash
dignacli delete-user USER_NAME

  
#### Argumenty
- **USER_NAME**: Uživatelské jméno uživatele, který má být odstraněn (povinné). Toto je jediný povinný argument příkazu.

#### Příklad
bash
dignacli delete-user jdoe

  
Provedením tohoto příkazu bude uživatel jdoe odstraněn ze systému ***digna***, jeho přístup bude zrušen a související data a oprávnění v repozitáři budou smazána.

### modify-user

Příkaz modify-user v ***digna*** CLI slouží k aktualizaci údajů existujícího uživatele v systému ***digna***.

##### Použití příkazu
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argumenty
  
- **USER_NAME**: Uživatelské jméno uživatele, který má být upraven (povinné).
- **USER_FULL_NAME**: Nové celé jméno uživatele (povinné).
  
#### Možnosti  
  
- --is_superuser, -su: Nastaví uživatele jako superuživatele, čímž mu udělí zvýšená oprávnění. Tento přepínač nevyžaduje hodnotu.  
- --valid_until, -vu: Nastaví datum vypršení platnosti účtu ve formátu YYYY-MM-DD HH:MI:SS. Pokud není uvedeno, účet zůstane platný na neurčito.  
  
#### Příklad
  
Pro úpravu celého jména uživatele jdoe na „Johnathan Doe“ a nastavení uživatele jako superuživatele:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


### modify-user-pwd
  
Příkaz modify-user-pwd v ***digna*** CLI slouží ke změně hesla existujícího uživatele v systému ***digna***.
  
##### Použití příkazu
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argumenty
  
- **USER_NAME**: Uživatelské jméno uživatele, jehož heslo se má změnit (povinné).
- **USER_PWD**: Nové heslo pro uživatele (povinné).
  
#### Příklad
  
Pro změnu hesla uživatele jdoe na newpassword123:
bash
dignacli modify-user-pwd jdoe newpassword123


### list-users

Příkaz list-users v ***digna*** CLI zobrazí seznam všech uživatelů registrovaných v systému ***digna***.

##### Použití příkazu

bash
dignacli list-users


Spuštěním tohoto příkazu se ***digna*** CLI připojí k repozitáři ***digna*** a vypíše všechny uživatele, zobrazí jejich ID, uživatelské jméno, celé jméno, stav superuživatele a časová razítka expirace.

# Správa repozitáře

### upgrade-repo
  
Příkaz upgrade-repo v ***digna*** CLI slouží k upgradu nebo inicializaci repozitáře ***digna***. Tento příkaz je nezbytný pro aplikaci aktualizací nebo pro prvotní nastavení infrastruktury repozitáře.
  
#### Použití příkazu

bash
dignacli upgrade-repo [options]

  
#### Možnosti
  
- --simulation-mode, -s: Pokud je povoleno, příkaz poběží v simulačním režimu, který vypíše SQL příkazy, které by byly vykonány, ale skutečně je nespustí. To je užitečné pro náhled změn bez úprav repozitáře.  

  
#### Příklad
  
Pro upgrade repozitáře ***digna*** můžete spustit příkaz bez voleb:
  
bash
dignacli upgrade-repo
  
Pro spuštění upgradu v simulačním režimu (zobrazení SQL příkazů bez jejich aplikace):
  
bash
dignacli upgrade-repo --simulation-mode

  
Tento příkaz je klíčový pro udržování systému ***digna***, zajišťuje, že schéma databáze a další komponenty repozitáře jsou aktuální vůči nejnovější verzi softwaru.

### encrypt
  
Příkaz encrypt v ***digna*** CLI slouží k zašifrování hesla.
  
#### Použití příkazu
  
bash
dignacli encrypt <PASSWORD>

    
#### Argumenty
- **PASSWORD**: Heslo, které je potřeba zašifrovat (povinné).
  
#### Příklad
  
Pro zašifrování hesla je potřeba předat heslo jako argument.   
Například pro zašifrování hesla mypassword123 byste použili:
bash
dignacli encrypt mypassword123

Tento příkaz vypíše zašifrovanou verzi zadaného hesla, kterou lze následně použít v zabezpečených kontextech. Pokud argument hesla není poskytnut, CLI zobrazí chybu oznamující chybějící argument.

### generate-key
  
Příkaz generate-key slouží k vygenerování Fernet klíče, který je nezbytný pro zabezpečení hesel uložených v repozitáři ***digna***.
  
#### Použití příkazu
bash
dignacli generate-key

  
## Správa dat

### clean-up

Příkaz clean-up v ***digna*** CLI slouží k odstranění profilů, predikcí a dat systému Traffic Light pro jeden nebo více datových zdrojů v rámci zadaného projektu. Tento příkaz je důležitý pro správu životního cyklu dat a pomáhá udržovat organizované a efektivní prostředí odstraněním zastaralých nebo nepotřebných dat.

#### Použití příkazu

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumenty
  
- **PROJECT_NAME**: Název projektu, ze kterého mají být data odstraněna (povinné). Použití klíčového slova all-projects v tomto argumentu způsobí, že ***digna*** projde všechny existující projekty a aplikovat tento příkaz na každý z nich.
- **FROM_DATE**: Počáteční datum a čas pro odstranění dat. Přípustné formáty zahrnují %Y-%m-%d, %Y-%m-%dT%H:%M:%S nebo %Y-%m-%d %H:%M:%S (povinné).
- **TO_DATE**: Konečné datum a čas pro odstranění dat, podle stejných formátů jako FROM_DATE (povinné).
  
#### Možnosti
  
- --table-name, -tn: Omezuje operaci clean-up na konkrétní tabulku v projektu.
- --table-filter, -tf: Filtr pro omezení clean-up pouze na tabulky, které obsahují zadaný podřetězec v názvech.
- --timing, -tm: Po dokončení zobrazí dobu trvání procesu clean-up.
- --help: Zobrazí nápovědu pro příkaz clean-up a ukončí program.
  
#### Příklad
  
Pro odstranění dat z projektu ProjectA mezi 1. lednem 2023 a 30. červnem 2023:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Pro odstranění dat pouze z konkrétní tabulky s názvem Table1:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Tento příkaz pomáhá spravovat úložiště dat a zajišťuje, že repozitář obsahuje pouze relevantní informace.

### inspect

Příkaz inspect v ***digna*** CLI slouží k vytvoření profilů, predikcí a dat systému Traffic Light pro jeden nebo více datových zdrojů v rámci zadaného projektu. Tento příkaz pomáhá analyzovat a monitorovat data v definovaném časovém období.

#### Použití příkazu

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumenty
  
- **PROJECT_NAME**: Název projektu, pro který mají být data prozkoumána (povinné). Použití klíčového slova all-projects v tomto argumentu způsobí, že ***digna*** projde všechny existující projekty a aplikuje tento příkaz.
- **FROM_DATE**: Počáteční datum a čas pro inspekci dat. Přípustné formáty zahrnují %Y-%m-%d, %Y-%m-%dT%H:%M:%S nebo %Y-%m-%d %H:%M:%S (povinné).
- **TO_DATE**: Konečné datum a čas pro inspekci dat, podle stejných formátů jako FROM_DATE (povinné).
  
#### Možnosti

- --table-name, -tn: Omezuje inspekci na konkrétní tabulku v projektu.
- --table-filter, -tf: Filtr pro inspekci pouze tabulek, které obsahují zadaný podřetězec v názvech.
- --force-profile: Vynutí znovu sesbírání profilů. Výchozí chování je force-profile.
- --no-force-profile: Zamezí znovu sesbírání profilů.
- --force-prediction: Vynutí překalkulování predikcí. Výchozí chování je force-prediction.
- --no-force-prediction: Zamezí překalkulování predikcí.
- --force-alert-status: Vynutí překalkulování stavů alertů. Výchozí chování je force-alert-status.
- --no-force-alert-status: Zamezí překalkulování stavů alertů.
- --timing, -tm: Po dokončení zobrazí dobu trvání procesu inspekce.
- --alert-notification, -an: Odesílá notifikace alertů do přihlášených kanálů.
  
#### Příklad
  
Pro inspekci dat projektu ProjectA od 1. ledna 2024 do 31. ledna 2024:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Pro inspekci pouze konkrétní tabulky a vynucení překalkulování predikcí:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Tento příkaz je užitečný pro generování aktualizovaných profilů a predikcí, monitorování integritě dat a správu alert systému v rámci zadaného časového rámce projektu.

### tls-status

Příkaz tls-status v ***digna*** CLI slouží k dotazu na stav Traffic Light System (TLS) pro konkrétní tabulku v projektu k danému datu. Traffic Light System poskytuje přehled o stavu a kvalitě dat a ukazuje případné problémy nebo alerty, které vyžadují pozornost.
  
#### Použití příkazu
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Argumenty
  
- **PROJECT_NAME**: Název projektu, pro který se zjišťuje stav TLS (povinné).
- **TABLE_NAME**: Konkrétní tabulka v projektu, pro kterou je stav TLS požadován (povinné).
- **DATE**: Datum, pro které se stav TLS dotazuje, typicky ve formátu %Y-%m-%d (povinné).
  
#### Příklad
  
Pro zjištění stavu TLS pro tabulku UserData v projektu ProjectA k 1. červenci 2024:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Tento příkaz pomáhá uživatelům sledovat a udržovat kvalitu dat tím, že poskytuje jasnou a použitelnou zprávu o stavu na základě předdefinovaných kritérií.

### list-projects
  
Příkaz list-projects v ***digna*** CLI slouží k zobrazení seznamu všech dostupných projektů v systému ***digna***.
  
#### Použití příkazu
  
bash
dignacli list-projects


Tento příkaz je zvláště užitečný pro administrátory a uživatele spravující více projektů a poskytuje rychlý přehled dostupných projektů v repozitáři ***digna***.

### list-ds

Příkaz list-ds v ***digna*** CLI slouží k zobrazení seznamu všech dostupných datových zdrojů v rámci zadaného projektu. Tento příkaz je užitečný pro získání přehledu o datových aktivech dostupných k analýze a správě v systému ***digna***.

#### Použití příkazu
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argumenty
- **PROJECT_NAME**: Název projektu, pro který se zobrazují datové zdroje (povinné).
  
#### Příklad
  
Pro vypsání všech datových zdrojů v projektu s názvem ProjectA:
  
bash
dignacli list-ds ProjectA

  
Tento příkaz poskytuje uživatelům přehled datových zdrojů dostupných v projektu a usnadňuje navigaci a správu datového prostředí.