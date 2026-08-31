---
title: digna Release 2026.06 | Python SDK, Docker Deployment & Enhanced Validation Management
description: Afla noutățile din digna Release 2026.06. Această versiune introduce noul **digna Python SDK**, suport oficial pentru **Docker deployment**, o experiență de dashboard reproiectată și capabilități extinse de import/export pentru regulile de validare a datelor.
keywords: digna Release 2026.06, digna Python SDK, digna Docker support, data quality automation, data profiling, validation rule import export, digna dashboard, data observability platform, Python API, metadata automation
image: /assets/logo_square.png
---

# Jurnal de modificări – Release 2026.06  

Cu Release 2026.06, digna face un pas important înainte în automatizare, extensibilitate și uzabilitatea platformei.  
Această versiune introduce noul **digna Python SDK**, suport oficial pentru **Docker deployment**, o experiență de dashboard reîmprospătată și portabilitate extinsă pentru gestionarea regulilor de validare.

---

## 🚀 Funcționalități noi  

### digna Python SDK – Automatizează totul cu Python  
- Instalare:
  ```bash
  pip install digna-sdk
  ```
- Gestionează și automatizează digna programatic folosind Python  
- Creează și configurează proiecte prin cod  
- Declanșează execuții de inspecție și monitorizare  
- Gestionează seturi de date, reguli și configurații programatic  
- Profilează tabele și extrage informații despre metadate  
- Exportă rezultatele de profilare și de calitate a datelor către depozite și sisteme externe  
- Integrează cu notebook-uri, instrumente de orchestrare și pipeline-uri CI/CD  

**Impact:** Permite infrastructură ca cod (infrastructure-as-code) completă și automatizare profundă a fluxurilor de lucru pentru calitatea datelor și observabilitate folosind Python.

---

### Docker Support – Implementare și operare simplificate  
- Suport oficial pentru imagine Docker a digna  
- Configurare rapidă și consecventă în toate mediile  
- Onboarding simplificat pentru dezvoltare, test și producție  
- Integrare facilă cu Kubernetes și platforme de containere  
- Portabilitate și reproductibilitate îmbunătățite ale implementărilor  

**Impact:** Face digna mai ușor de implementat și operat în arhitecturi cloud-native moderne.

---

### QueryMode – Strategie flexibilă de executare SQL

Configurează strategia de execuție a interogărilor: **Single** sau **Combined** mode

**Single Mode**: Fiecare statistică este calculată printr-o singură interogare SQL dedicată

  - Ideal pentru surse de date mari unde constrângerile de memorie sunt o problemă
  - Previne epuizarea resurselor cauzată de interogări combinate (out of memory, limite de spool)
  - Număr mai mare de interogări, dar consum de memorie per interogare mai mic

**Combined Mode**: Toate statisticile sunt calculate într-o singură interogare SQL

  - Reduce numărul total de interogări și overhead-ul de rețea
  - Optimizează performanța când sursele de date sunt gestionabile în memorie
  - Mai eficient pentru execuții frecvente și paralele

**Impact:** Oferă utilizatorilor control granular asupra execuției interogărilor pentru a echilibra performanța, utilizarea resurselor și siguranța memoriei în funcție de caracteristicile surselor de date.


---

### Experiență reproiectată a dashboardului  
- Design UI/UX modernizat și îmbunătățit  
- Navigare și structură mai clară  
- Vizibilitate mai bună a rezultatelor de monitorizare și a insight-urilor despre calitatea datelor  
- Citire îmbunătățită a alertelor, statisticilor și dashboardurilor  
- Acces mai rapid la informațiile operaționale cheie  

**Impact:** Îmbunătățește utilizabilitatea și productivitatea zilnică pentru toți utilizatorii.

---

### Import & Export extins pentru regulile de validare  
- Funcționalitate îmbunătățită de import/export pentru regulile de validare  
- Migrare mai ușoară între medii și proiecte  
- Reutilizare facilă a seturilor de reguli standardizate  
- Guvernanță și management al ciclului de viață al regulilor îmbunătățite  
- Colaborare simplificată între echipe  

**Impact:** Permite guvernanță scalabilă și consistentă a calității datelor în întreaga organizație.

---

## 🧪 Îmbunătățiri ale platformei  

- Integrare completă a SDK-ului Python pentru automatizare  
- Implementare containerizată prin Docker  
- UX îmbunătățit prin dashboard reproiectat  
- Portabilitate extinsă a logicii de validare  

---

## 🎯 Cine beneficiază de această versiune  

- Data Engineers: automatizare, utilizare SDK, integrare în pipeline-uri  
- Platform Teams: implementare simplificată prin Docker  
- Data Governance Teams: managementul regulilor de validare reutilizabile  
- Analytics Teams: vizibilitate îmbunătățită a insight-urilor și uzabilitate  

---

## 🛠 Actualizări CLI  
- Suport adăugat pentru integrarea SDK-ului  
- Fluxuri de import/export îmbunătățite  
- Îmbunătățiri generale de stabilitate și performanță