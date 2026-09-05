# Změny – Vydání 2025.09  

S vydáním 2025.09 představuje digna novou **modulární architekturu** a spouští **pět specializovaných modulů** pro kvalitu dat a observability.  
Toto vydání rovněž posiluje ověřování a vylepšuje zpracování notifikací v celé platformě.  

---

## Nové funkce  

### Modulární architektura  
- digna nyní používá **modulární architekturu**.  
- Zákazníci si mohou povolit pouze moduly, které potřebují, a přidávat další podle rostoucích požadavků.  
- Dřívější funkcionalita je nyní součástí **digna Data Anomalies**.  

### Nové moduly  
- **digna Data Anomalies** – detekce odchylek v objemech dat, rozděleních a chybějících hodnotách poháněná AI.  
- **digna Data Analytics** – vyhodnocování metrik observability v časových řadách pro detekci dlouhodobých trendů a volatility.  
- **digna Data Timeliness** – sledování očekávaných časů příchodu dat, jak pomocí AI, tak na základě pravidel.  
- **digna Data Validation** – kontrola záznamů na úrovni pravidel pro zajištění souladu s obchodními pravidly.  
- **digna Data Schema Tracker** – detekce změn schématu (úpravy DDL) v monitorovaných databázích.  

### MFA přes OIDC  
- Podpora **vícefaktorového ověřování (MFA)** přes OIDC Single Sign-On.  
- Zajišťuje podnikové zabezpečení pro všechna uživatelská přihlášení.  

### E-mailová upozornění pro jednotlivé moduly  
- Notifikace jsou nyní odesílány **po modulech**, což usnadňuje oddělení upozornění z Data Anomalies, Data Analytics a dalších modulů.  

---

## Aktualizace CLI  

- **Nový příkaz: `inspect-cancel`** – zruší inspekce podle ID požadavku nebo ukončí všechny aktivní požadavky.  
- **Nový příkaz: `check-config`** – ověří konfigurační soubory před spuštěním.  
- **Nový příkaz: `remove-orphans`** – vyčistí opuštěné záznamy v repozitáři.  
- **Vylepšený příkaz `inspect`** – nová volba `--bypass-backend` (`-bb`) a standardizované návratové kódy (`0 = OK, 1 = INFO, 2 = WARNING`).  


## Dokumentace  
- Nové návody:  
  - Průvodce integrací Single Sign-On