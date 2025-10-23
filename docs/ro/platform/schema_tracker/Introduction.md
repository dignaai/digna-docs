---
title: Data Schema Tracker – Monitorizează evoluția schemei | digna Documentație
description: Aflați cum Data Schema Tracker de la digna monitorizează modificările coloanelor, actualizările tipurilor de date și schema drift. Primiți alerte pentru schimbări intenționate și neintenționate pentru a preveni eșecuri ETL și erori în dashboard-uri.
---

# Data Schema Tracker – Monitorizează evoluția schemei

## Purpose
Monitorizează și trimite alerte privind evoluția schemei.

## Technical Features
- Monitorează:
  - Adăugarea sau eliminarea coloanelor
  - Modificări ale tipurilor de date
- Trimite alerte atât pentru schimbările intenționate, cât și pentru cele neintenționate ale schemei  
- Previne **silent schema drift** care poate întrerupe pipeline-urile ETL sau dashboard-urile  

## Example Use Cases
- Identificarea modificărilor de tip de date (de ex., `INT` → `VARCHAR`) care pot provoca erori în etapele ulterioare  
- Avertizarea inginerilor de date înainte ca pipeline-urile să eșueze din cauza nepotrivirilor de schemă  

## Value
Menține echipele în controlul **seturilor de date care evoluează rapid**.