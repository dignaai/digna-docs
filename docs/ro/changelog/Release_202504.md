---
title: digna Lansare 2025.04 | Inspection Hub, Suport multi-limbă, Module Analytics
description: Află noutățile din digna Lansare 2025.04. Această versiune introduce Inspection Hub, suport multi-limbă (engleză, germană, poloneză), import/export de surse de date prin dignacli, prima versiune a Module Analytics și o experiență de dashboard îmbunătățită.
keywords: digna Lansare 2025.04, digna changelog, digna inspection hub, digna suport multi-limbă, digna module analytics, digna import export, digna CLI, note de lansare, observabilitatea datelor, monitorizarea calității datelor
image: /assets/logo_square.png
---

# Changelog – Lansare 2025.04

Cu Lansarea 2025.04, digna face un pas major înainte pentru a face gestionarea calității și observabilității datelor mai ușoară, mai transparentă pentru echipe și accesibilă utilizatorilor din întreaga lume.  
Această versiune combină **funcționalități noi puternice**, **îmbunătățiri ale automatizării fluxurilor de lucru** și **rafinamente ale experienței utilizator**.  

---

## Funcționalități noi

### Inspection Hub – Un nou centru de comandă
**Inspection Hub** este acum disponibil ca locul central pentru a gestiona toate job-urile de inspecție. În loc să sari între module diferite sau să te bazezi exclusiv pe execuția din linia de comandă, poți acum monitoriza și controla inspecțiile dintr-o singură interfață simplificată.  

Capabilități cheie includ:  
- Inspecții la cerere: Pornește job-uri noi instantaneu, ori de câte ori ai nevoie de rezultate proaspete.  
- Istoric al inspecțiilor: Vezi o cronologie a inspecțiilor — ce a fost rulat, cine a declanșat și când.  
- Urmărirea stării: Job-urile sunt clar marcate ca finalizate, în curs de desfășurare sau în așteptare.  
- Informații despre invoker: Verifică rapid dacă o inspecție a fost declanșată de un utilizator, de un scheduler sau de CLI.  
- Unelte de curățare: Șterge job-urile învechite sau inutile pentru a-ți menține spațiul de lucru curat.  
- Jurnale detaliate: Aprofundează fiecare job pentru a vedea cât a durat, ce surse au fost incluse și cum au fost aplicate pragurile.  

Inspection Hub oferă echipelor **vizibilitate și control end-to-end**, făcând gestionarea inspecțiilor mai ușoară în proiecte de mari dimensiuni.  

---

### Suport multi-limbă – digna îți vorbește limba
digna este acum pregătită pentru echipe internaționale odată cu introducerea **suportului multi-limbă**.  

În această versiune poți seta **limba preferată a interfeței** direct din Preferințele Utilizatorului. Limbile suportate includ:  
- Engleză (UK, US, CA, AU)  
- Germană (DE, AT, CH)  
- Poloneză (PL)  

Aceasta face digna mai ușor de utilizat pentru organizațiile multilingve și asigură o adoptare mai fluidă în rândul echipelor din regiuni diferite. Vor fi adăugate mai multe limbi în versiunile viitoare.  

---

### Import & Export al surselor de date – Configurare simplificată
Consistența între medii este esențială în implementările enterprise. Cu 2025.04, digna introduce **import/export al surselor de date** prin **dignacli**, instrumentul din linia de comandă pentru utilizatorii avansați.  

Beneficii:  
- Exportă o configurație de sursă de date o dată, apoi refolosește-o în Development, Test și Production.  
- Elimină reconfigurările manuale și evită erorile costisitoare.  
- Susține fluxuri automate de lucru și pipeline-uri CI/CD cu comenzi CLI simple (`export-ds` și `import-ds`).  
- Copiază rapid surse de date între proiecte pentru o colaborare mai ușoară.  

Această funcționalitate asigură că echipele pot implementa cu încredere, știind că configurațiile sunt consistente în fiecare mediu.  

---

### Module Analytics (v1) – De la detectare la înțelegere
digna a început ca o platformă pentru detectarea anomaliilor și monitorizarea calității datelor. Cu Lansarea 2025.04, evoluează mai departe cu **prima versiune a Module Analytics**.  

Module Analytics îi ajută pe utilizatori să **înțeleagă datele** în loc să reacționeze doar la probleme. Cu acest nou modul poți:  
- Urmări tendințele pe termen lung în seturile tale de date.  
- Detecta și monitoriza volatilitatea pentru a înțelege fluctuațiile.  
- Explora comportamentul datelor în timp pentru un context mai profund.  

De exemplu, digna poate evidenția automat că *„Numărul de rânduri a crescut cu 15.8% de la începutul anului.”*  
Fără interogări SQL, fără verificări manuale — doar **insight-uri acționabile dintr-o privire**.  

Aceasta este fundația călătoriei digna către analitică avansată a datelor, permițând echipelor de date să treacă de la monitorizare reactivă la una proactivă.  

---

### Îmbunătățiri ale dashboard-ului – O experiență mai fluidă
Dincolo de funcționalitățile majore, Lansarea 2025.04 include mai multe **rafinamente ale dashboard-ului** concepute pentru a face digna mai intuitivă și plăcută la utilizare:  
- Navigare mai rapidă între proiecte și inspecții.  
- Un layout mai curat pentru jurnalele de inspecție și trimiterea job-urilor.  
- Ajustări subtile de design care te ajută să găsești insight-urile mai rapid.  

Aceste îmbunătățiri se bazează direct pe feedback-ul clienților și demonstrează angajamentul nostru continuu de a face digna **o platformă construită pentru utilizare zilnică**.  

---

## Îmbunătățiri generale
- Optimizări de performanță pentru job-urile de inspecție pe seturi mari de date.  
- Tratare îmbunătățită a erorilor în dignacli pentru a oferi feedback mai clar.  
- Îmbunătățiri de stabilitate pentru proiectele cu multe job-uri simultane.  
- Rafinamente UI pentru filtrarea jurnalelor de job și gestionarea proiectelor.  

---

## Rezumat
Lansarea 2025.04 este despre **control, accesibilitate și insight**.  

- Noul **Inspection Hub** oferă utilizatorilor vizibilitate completă asupra job-urilor de inspecție.  
- **Suportul multi-limbă** asigură că digna poate fi folosită de echipe globale.  
- Funcționalitatea de **import/export** simplifică gestionarea configurațiilor între medii.  
- **Module Analytics (v1)** mută accentul de la detectare la înțelegere, cu urmărire de tendințe și volatilitate.  
- **Îmbunătățirile dashboard-ului** rafinează experiența generală a utilizatorului.  

Împreună, aceste actualizări fac digna mai puternică, mai prietenoasă și mai pregătită pentru utilizare internațională ca niciodată.