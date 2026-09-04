---
title: digna Release 2026.01 | Surse de date logice, Conexiuni globale & Validare avansată a datelor
description: Află noutățile din digna Release 2026.01. Această versiune introduce conexiuni globale la baze de date, surse de date logice, condiții de relevanță pentru anomalii, exporturi CSV și validare avansată a datelor, inclusiv verificări de integritate referențială.
keywords: digna Release 2026.01, digna changelog, digna datasource, digna database connections, digna Data Anomalies, digna Data Validation, validare integritate referențială, reguli calitate date, observabilitate date, digna CSV export
image: /assets/logo_square.png
---

# Jurnal de modificări – Release 2026.01  

Cu Release 2026.01, digna introduce îmbunătățiri majore în modelarea surselor de date, gestionarea conexiunilor și ușurința utilizării inspecțiilor.  
Această versiune mărește flexibilitatea în toate modulele și extinde semnificativ acoperirea pentru **calitatea și validarea datelor**.

---

## Caracteristici noi  

### Conexiuni globale la baze de date  
- Conexiunile la baze de date sunt acum configurate la nivel **global**.  
- Conexiunile globale pot fi reutilizate în **toate proiectele**, simplificând configurarea și întreținerea.  
- **Impact:** Reduce povara operațională și asigură conectivitate consistentă între medii.

### Conexiuni multiple sursă per proiect  
- Proiectele pot face referire acum la **multiple configurații de conexiuni sursă**.  
- Permite configurații mai flexibile pentru peisaje de date complexe la nivel de proiect.  
- **Impact:** Suportă arhitecturi enterprise realiste cu surse de date eterogene.

### Surse de date logice  
- Sursele de date reprezintă acum un **strat logic** în cadrul unui proiect.  
- Fiecare sursă de date poate fi susținută de:
    - un **tabel din baza de date**
    - o **vizualizare din baza de date**
    - o **instruire SQL personalizată**  
- Această separare îmbunătățește reutilizarea, claritatea și modelarea inspecțiilor în toate modulele.  
- **Impact:** Decuplează inspecțiile și regulile de calitate a datelor de stocarea fizică, îmbunătățind mentenanța și reutilizarea.

### Condiție de relevanță a anomaliilor  
- O **Condiție de relevanță a anomaliilor** poate fi definită acum pentru a controla evaluarea stării anomaliilor la nivel de set de date.  
- Statisticile sunt calculate independent de faptul dacă condiția este setată sau îndeplinită.  
- Dacă condiția **nu este îndeplinită**, **digna Data Anomalies** nu oferă stare de anomalie (verde / galben / roșu).  
- **Exemplu:** Excluderea setului de date din evaluarea anomaliilor când numărul de înregistrări este sub 10.  
- **Impact:** Asigură că anomaliile sunt evaluate doar în contexte de business relevante.

### Configurare notificări pe modul  
- Notificările pot fi acum configurate **pe modul** direct în digna.  
- Permite control independent al comportamentului de alertare pentru **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** și alte module.  
- **Impact:** Activează strategii de alertare precise, aliniate cu responsabilitățile echipelor și criticitatea.

### Export rezultate inspecție (CSV)  
- Utilizatorii pot **descărca rezultatele inspecțiilor ca fișiere CSV**.  
- Permite analiză offline, generare de rapoarte și integrare cu instrumente externe.  
- **Impact:** Simplifică auditările, raportarea și analiza calității datelor în aval.

---

## Capacități extinse de validare a datelor  

Cu această versiune, **digna Data Validation** suportă acum un set cuprinzător de reguli de calitate a datelor:

- **Reguli de validare la nivel de rând**  
- **Verificări de unicitate pe mai multe coloane**  
- **Validare a integrității referențiale între surse de date**

Împreună, aceste verificări permit aplicarea **regulilor structurale și relaționale de calitate a datelor** în peisaje de date complexe.

### Verificări de unicitate pentru coloane multiple
- Introduse **Verificări de Unicitate** pentru un **set configurabil de coloane**.  
- Permite validarea cheilor compuse și a constrângerilor de unicitate la nivel de business.  
- **Impact:** Detectează entități de business duplicate care nu pot fi identificate cu verificări pe o singură coloană.

### Verificări de integritate referențială
- Introduse **Verificări de Integritate Referențială** pentru a valida relațiile între sursele de date.  
- Asigură că **valorile cheilor externe** dintr-o sursă sursă există în sursa țintă referențiată.  
- Ajută la detectarea înregistrărilor orfane, a relațiilor rupte și a problemelor de consistență a datelor din timp.  
- Conceput pentru a funcționa cu **surse de date logice**, inclusiv vizualizări și SQL personalizat.  
- **Cazuri de utilizare:** integritatea data warehouse-ului, raportare reglementară, consistența master data și analize fiabile în aval.

---

## Cui îi este folositoare această versiune  

- **Data Engineers:** Modelare mai flexibilă a surselor de date și conexiuni reutilizabile la baze de date  
- **Echipe Calitate & Guvernanță a Datelor:** Acoperire extinsă a validărilor, inclusiv reguli de integritate relațională  
- **Echipele de analiză și BI:** Date de intrare mai curate și rezultate ale inspecțiilor exportabile  
- **Proprietari de platformă:** Complexitate redusă a configurației și mentenanță operațională îmbunătățită

---

## Actualizări CLI  
- Nicio modificare

---