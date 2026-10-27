---
title: digna Release 2026.11 | Data Reconciliation, digna Agentic & digna Engine
description: Aflați noutățile din digna Release 2026.11. Această versiune introduce trei adăugiri majore - digna Data Reconciliation, digna Agentic cu digna MCP Server și digna Engine, care permite verificări de integritate referențială între tehnologii de baze de date diferite.
keywords: digna Release 2026.11, jurnal de modificări digna, digna Data Reconciliation, reconcilierea datelor, validare ETL, reconciliere sursă-țintă, digna Agentic, digna MCP Server, agenți AI calitatea datelor, digna Engine, integritate referențială între conexiuni, atribute de interogare, profilarea datelor, observabilitatea datelor
image: /assets/logo_square.png
---

# Jurnal de modificări – Release 2026.11  

Release 2026.11 este construit în jurul a trei adăugiri majore:

- **digna Data Reconciliation**: verifică dacă datele rămân consecvente pe măsură ce se deplasează între sisteme  
- **digna Agentic**: deschide digna către agenții AI prin digna MCP Server  
- **digna Engine**: profilează opțional datele în interiorul digna și permite verificări de integritate referențială între tehnologii de baze de date diferite  

digna Data Reconciliation și digna Agentic sunt livrate în versiune beta.

---

## Funcționalități noi  

### digna Data Reconciliation – Consecvență de la sursă la țintă  
Datele trec adesea prin mai multe sisteme înainte să ajungă într-un raport. digna Data Reconciliation compară o sursă de date **țintă** cu **sursele** din care a fost construită și emite o alertă atunci când acestea nu mai corespund.

- Se configurează ca reguli cu nume în noua filă **Data Reconciliation** a sursei de date țintă  
- Orice sursă de date din proiect care are Data Reconciliation activat poate fi o sursă  
- Cazurile de utilizare includ procedurile standard de reconciliere și validarea rezultatelor proceselor ETL  
- Două tipuri de reguli: **Exact** și **AI**  

**Reguli Exact – Reconcilierea ca regulă de calitate a datelor**: Definiți exact ce trebuie să corespundă între o sursă și o țintă, ca la o regulă de calitate a datelor.

  - Comparați o sursă de date sursă cu o sursă de date țintă  
  - Asociați o verificare a țintei cu o verificare a sursei după statistică și atribut, de ex. numărul de rânduri sau suma unei coloane de valori  
  - Permiteți o diferență cu o toleranță **absolute** (de ex. ± 10) sau una **relative** (de ex. ± 0,5 % din sursă)  
  - Cronologia afișează diferența din fiecare zi față de toleranță  

**Reguli AI – Reconcilierea ca observabilitate a datelor**: digna învață cum urmează o țintă sursele sale, la fel cum digna observă datele în celelalte module, și emite o alertă atunci când relația se rupe.

  - Combinați verificări din mai multe surse de date sursă cu verificările unei singure ținte  
  - Nu este nevoie să cunoașteți sau să descrieți logica dintre ele (join-uri, filtre, agregări)  
  - Un model învață din istoric cum urmează ținta sursele sale în aceeași zi  
  - Fiecare verificare a țintei este prezisă din valorile surselor din ziua respectivă, iar digna emite o alertă atunci când ținta iese din banda erorilor anterioare ale regulii  
  - Fiecare regulă are propriile **Model settings**: **Sensitivity**, **Memory** și **Model Complexity**  

Verificările de reconciliere apar în Dashboard cu o cronologie pentru fiecare regulă. Ele contează pentru starea generală a inspecției și declanșează notificări.

**Impact:** Acoperă ambele fețe ale reconcilierii. Regulile Exact impun controale cunoscute între sursă și țintă, iar regulile AI monitorizează fluxuri complexe, precum procesele ETL, astfel încât datele pierdute sau modificate pe parcurs sunt detectate fără SQL de reconciliere scris manual.

---

### digna Agentic – digna pentru agenți AI  
Prima versiune a digna Agentic. Agenții AI pot lucra acum cu digna, pot răspunde la întrebări de business despre datele dumneavoastră și vă pot ajuta să vă îmbunătățiți configurația.

**digna MCP Server**: Permite lui Claude și altor agenți AI să lucreze cu digna prin Model Context Protocol.

  - Gestionarea proiectelor, surselor de date, regulilor, programărilor de inspecție și abonamentelor  
  - Citirea stărilor inspecțiilor până la nivelul fiecărei verificări, pentru investigarea alertelor  

**Descrieri pentru surse de date și atribute**: Descrieți în limbaj simplu ce conține o sursă de date sau un atribut.

  - Agenții AI folosesc descrierile pentru a vă interpreta datele  
  - Puneți întrebări de business despre datele dumneavoastră, iar agenții AI le răspund pe baza a ceea ce monitorizează digna  
  - Dacă configurația actuală a digna nu poate răspunde la o întrebare, agentul AI sugerează, acolo unde este posibil, modificări ale sursei de date și ale atributelor sale, de ex. adăugarea unui nou set de date  

**Impact:** Vă permite să puneți întrebări de business despre datele dumneavoastră în limbaj simplu și le permite agenților AI să ajute la configurarea digna și la investigarea problemelor de calitate a datelor.

---

### digna Engine – Profilare acolo unde alegeți  
În mod implicit, digna profilează datele acolo unde se află, în baza de date sursă. digna Engine adaugă o opțiune: digna exportă datele din sursă și le profilează în interiorul digna Engine.

- Opțional, nu obligatoriu: profilarea în baza de date sursă rămâne disponibilă  
- Se selectează pentru fiecare conexiune la baza de date ca **locație de profilare**: **Source Database** sau **digna Engine**  
- Disponibil pentru toate tehnologiile sursă acceptate  

**Integritate referențială între conexiuni**: Unele verificări necesită exportarea datelor. digna Engine extinde **digna Data Validation** pentru aceste cazuri.

  - **Verificări de integritate referențială** între surse de date aflate pe **conexiuni diferite la baze de date**, inclusiv tehnologii de baze de date diferite (de ex. Oracle și PostgreSQL)  
  - Funcționează cu ambele locații de profilare: pentru Source Database, doar coloanele cheie sunt exportate în digna Engine  
  - Dashboardul arată când o verificare rulează pe două conexiuni  

**Impact:** Vă permite să alegeți unde sunt profilate datele și impune relațiile dintre sisteme care rulează pe tehnologii de baze de date diferite.

---

## Îmbunătățiri ale profilării  

Această versiune le oferă utilizatorilor și mai mult control asupra a ceea ce este profilat și cum.

### Atribute de interogare – Coloane definite de utilizator  
- Definiți coloane artificiale: o expresie SQL peste una sau mai multe coloane ale sursei de date  
- Fiecare atribut de interogare are propriul nume  
- Este profilat și verificat ca orice alt atribut  

### Categoria de coloană DATE  
- Nouă categorie **Date** pentru atribute  
- Metrici relative la data inspectată  

### Profilare la cerere  
- Profilați orice atribut pe baza instantaneului complet al unei singure date, fără a rula o inspecție  
- Ajută la setarea tipului de coloană al atributului: **Numerical**, **Categorical**, **Date** sau **Unspecified**  

---

## Cine beneficiază de această versiune  

- **Data Engineers:** Validarea rezultatelor ETL cu digna Data Reconciliation  
- **Echipe de Finanțe, Risc și Controlling:** Proceduri standard de reconciliere sub formă de reguli Exact în digna Data Reconciliation  
- **Echipe Calitate & Guvernanță a Datelor:** Integritate referențială între tehnologii de baze de date cu digna Engine  
- **Utilizatori de business:** Întrebări de business despre date, la care răspund agenții AI cu digna Agentic  
- **Echipe AI & Automatizare:** Agenți AI care lucrează cu digna prin digna Agentic  

---

## Actualizări CLI  
- Nicio modificare  

---
