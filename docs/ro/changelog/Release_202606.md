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

## Urmăriți prezentarea versiunii

<!--YOUTUBE EMBED START--><div style="position: relative; padding-bottom: 56.25%; height: 0; width: 100%;"><iframe src="https://www.youtube-nocookie.com/embed/g6ZQl9pc4vg" title="What&#39;s New in digna | The Major Release of 2026" frameborder="0" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div><!--YOUTUBE EMBED END-->

*[What's New in digna | The Major Release of 2026](https://www.youtube.com/watch?v=g6ZQl9pc4vg) — o prezentare a acestei versiuni pe canalul de YouTube digna.*

---

## Funcționalități noi  

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

### Model de predicție configurabil

Modelul din spatele detectării anomaliilor cântărește acum explicații concurente pentru fiecare serie – un tipar combinat cu o interpretare a celor mai recente observații – și le îmbină prognozele în funcție de cât de puternic este susținută fiecare. O singură valoare extremă nu se mai poate propaga în predicțiile următoare.

Îl controlează două setări din noua filă **Model** a sursei de date, fiecare de la `0.0` la `1.0`, cu `0.5` ca valoare implicită:

- **Break Sensitivity** – cât de repede un salt la un nou nivel sau o tendință care se inversează este acceptat ca schimbare reală, în loc să fie tratat drept valori aberante
- **Model Complexity** – câtă structură caută modelul, de la efecte calendaristice și o singură schimbare de nivel până la cicluri necunoscute, efecte ale zilelor lunii și resetări lunare

Ambele pot fi readuse oricând la valorile implicite. Consultați [Setările modelului](../platform/data_anomalies/how_it_works.md#model-settings) pentru a vedea cum acționează fiecare.

**Impact:** Oferă utilizatorilor control asupra modelului de predicție însuși, alături de setările existente Sensitivity și Memory pentru banda de toleranță, aflate acum în fila **Thresholds**.

---

### Controlul notificărilor de anomalii

- Filă nouă **Notifications** în setările de anomalii ale sursei de date:
  - **Minimum Alerts** – de câte verificări eșuate (nu și de cele incerte) are nevoie o inspecție înainte să fie trimisă o notificare (implicit `1`)
  - **Pause After Notification (Days)** – cât timp rămâne silențios un abonament după ce a trimis o notificare despre sursa de date (implicit `0`, fără pauză)

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

## Îmbunătățiri ale platformei  

- Integrare completă a SDK-ului Python pentru automatizare  
- Implementare containerizată prin Docker  
- UX îmbunătățit prin dashboard reproiectat  
- Portabilitate extinsă a logicii de validare  

---

## Cine beneficiază de această versiune  

- Data Engineers: automatizare, utilizare SDK, integrare în pipeline-uri  
- Platform Teams: implementare simplificată prin Docker  
- Data Governance Teams: managementul regulilor de validare reutilizabile  
- Analytics Teams: vizibilitate îmbunătățită a insight-urilor și uzabilitate  

---

## Actualizări CLI  
- Suport adăugat pentru integrarea SDK-ului  
- Fluxuri de import/export îmbunătățite  
- Îmbunătățiri generale de stabilitate și performanță