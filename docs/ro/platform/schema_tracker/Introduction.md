---
title: Data Schema Tracker – Monitorizarea evoluției schemei | Documentația digna
description: Aflați cum digna Data Schema Tracker monitorizează modificările coloanelor, actualizările tipurilor de date și derivația schemei. Detectați și primiți alerte pentru modificările intenționate sau neintenționate ale schemei pentru a preveni eșecuri ETL, dashboard-uri nefuncționale și pierderea observabilității datelor.
image: /assets/logo_square.png
keywords:
  - monitorizare schemă date
  - detectare schema drift
  - monitorizare evoluție schemă
  - observabilitate metadate
  - observabilitate date
  - calitatea datelor
  - monitorizare structură date
  - metadata baze de date
  - stabilitate pipeline ETL
  - digna data schema tracker
lang: en
robots: index, follow
og_title: Data Schema Tracker – Monitorizarea evoluției schemei | Documentația digna
og_description: digna Data Schema Tracker monitorizează derivația schemei, modificările tipurilor de date și actualizările coloanelor. Primiți alerte înainte ca pipeline-urile ETL sau dashboard-urile să eșueze din cauza modificărilor neașteptate ale structurii.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Schema Tracker – Monitor Schema Evolution
<h1 style="display:none;">Modul AI pentru observabilitatea metadatelor și calitatea datelor – digna Data Schema Tracker</h1>

---

## Scop

The **Data Schema Tracker** vă ține la curent cu modul în care evoluează structurile bazei de date.  
Monitorizează continuu **schemele tabelelor, coloanele și tipurile de date** pentru a detecta **schema drift** — modificări structurale intenționate sau neintenționate care pot perturba pipeline-urile, job-urile ETL sau dashboard-urile BI.

Prin asigurarea transparenței în evoluția schemei, digna ajută organizațiile să mențină **încrederea în calitatea datelor**, să susțină **observabilitatea sistemelor de date** și să evite incidente costisitoare în producție cauzate de modificări ale schemei nedetectate.

---

## Prezentare tehnică

### Ce monitorizează

- **Coloane adăugate sau eliminate** – Detectează coloane introduse recent, redenumite sau șterse.  
- **Modificări ale tipurilor de date** – Identifică schimbări precum `INT → VARCHAR` sau `DATE → TIMESTAMP`.  
- **Modificări ale tabelelor și view-urilor** – Urmărește crearea, redenumirea sau eliminarea tabelelor și view-urilor.  
- **Diferențe între medii** – Compară versiuni ale schemei între mediile Dev, Test și Production.  

### Detectare și alertare

- Scanează **metadata bazei de date** sau **catalogele de sistem** direct în platforma dvs. de date.  
- Compară fiecare snapshot al schemei cu versiunea anterioară cunoscută, stocată în schema de observabilitate a digna.  
- Generează **alerte în timp real** în dashboard, prin API sau prin canale externe de notificare (email, Slack, webhook).  
- Înregistrează fiecare versiune a schemei pentru **urmărire istorică și pregătire pentru audit**.

---

## Arhitectură și execuție

- **Executare în baza de date:** digna rulează integral în mediul dvs., interogând vizualizările de metadata fără a extrage niciun fel de date utilizator.  
- **Scanare ușoară:** accesează numai informații structurale — niciodată datele utilizatorilor.  
- **Stocare centralizată:** metadatele schemei și înregistrările de drift sunt stocate în schema de observabilitate digna pentru vizualizare și analiză.  
- **Automatizare:** suportă scanări programate sau bazate pe evenimente prin digna Core sau instrumente externe de orchestrare.  

---

## Exemple de cazuri de utilizare

| Caz de utilizare | Descriere |
|------------------|-----------|
| **Monitorizare stabilitate ETL** | Detectați schimbările de structură în upstream înainte ca pipeline-urile să eșueze din cauza nepotrivirilor de schemă. |
| **Fiabilitate Business Intelligence** | Preveniți dashboard-urile rupte cauzate de coloane redenumite sau lipsă. |
| **Guvernanță Data Warehouse** | Mențineți un istoric audibil al evoluției schemei pentru conformitate și analiză de impact. |
| **Supraveghere integrare** | Asigurați-vă că schemele din data lake și data warehouse rămân sincronizate după actualizări structurale. |

---

## Beneficii

| Domeniu | Beneficiu |
|---------|----------|
| **Calitatea datelor** | Previne derivația schemei nedetectată care poate corupe sau invalida pipeline-urile de date. |
| **Observabilitate** | Adaugă monitorizare structurală la observabilitatea generală a ecosistemelor de date. |
| **Conformitate** | Menține istoricul versionat al schemei pentru audit, trasabilitate și control al schimbărilor. |
| **Prevenție** | Detectează probleme structurale înainte ca acestea să se transforme în erori de raportare sau producție. |

---

## Cum funcționează

1. **Colectare instantanee (snapshot)** – digna capturează metadatele curente ale schemei.  
2. **Comparare** – noua captura este comparată