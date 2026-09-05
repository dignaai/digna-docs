# Jurnal de modificări – Versiunea 2026.04  

Cu Versiunea 2026.04, digna își extinde semnificativ capabilitățile în domeniul analitic și al validării datelor.  
Această versiune introduce analiză avansată de serii temporale, componente reutilizabile pentru validare și standardizare centralizată a valorilor.

---

## Funcționalități noi  

### Analytics Chart – Analiză de serii temporale fără Data Science  
- Nou: **Analytics Chart** pentru analiză interactivă a seriilor temporale  
- Metode analitice integrate:
    - Regresie liniară, cuadratică și cubică  
    - Regresie pe segmente (piecewise) cu puncte de cotitură configurabile  
    - Tehnici de smoothing  
    - Analiză a cuantilelor  
- Identificare automată a trendurilor, sezonalității și a schimbărilor de pattern  
- Analiză a reziduurilor pentru o înțelegere mai profundă a deviațiilor  
- Seriile temporale sunt calculate automat pentru fiecare set de date  

**Impact:** Permite utilizatorilor să înțeleagă comportamente complexe ale datelor în timp fără a necesita expertiză în data science sau instrumente externe.

---

### Enumerations – Definire centralizată a valorilor permise  
- Definire de seturi reutilizabile de valori permise (de ex., țări, state, coduri de stare)  
- Validarea valorilor coloanelor în raport cu enumerations predefinite în **digna Data Validation**  
- Reutilizarea enumerations în proiecte și surse de date diferite  
- Utilizare universală prin `#ENUM:MY_ENUM#`  
- Toate verificările sunt executate **direct în baza de date sursă**  

**Impact:** Asigură valori consistente și standardizate ale datelor la nivel organizațional.

---

### Validation Rule Templates – Logică reutilizabilă pentru calitatea datelor  
- Definire de reguli de validare reutilizabile (de ex., verificări pentru spații albe, NOT NULL, verificări de format)  
- Aplicarea șabloanelor pe multiple seturi de date  
- Asigurarea unei logici consistente a regulilor între proiecte  
- Reducerea duplicărilor și a configurării manuale  
- Toate verificările sunt executate **direct în baza de date sursă**  

**Impact:** Permite validarea scalabilă și high-performance a datelor fără a le muta.

---

### Condiții de relevanță la nivel de statistică  
- Definirea condițiilor de relevanță pe **nivel de coloană pentru fiecare statistică**  
- Extinde conceptul de condiții de relevanță pentru anomalii  
- Controlul momentului în care o statistică trebuie considerată relevantă  
- Reducerea zgomotului prin excluderea situațiilor non-critice  

**Impact:** Îmbunătățește calitatea semnalelor concentrându-se doar pe deviațiile semnificative.

---

## Capabilități extinse pentru Data Analytics & Validation  

Cu această versiune, digna extinde atât înțelegerea datelor, cât și standardizarea validării datelor:

- Interpretare avansată a **seriilor temporale** fără cunoștințe de data science  
- Definire centralizată a **valorilor permise prin enumerations**  
- Logică de **validare reutilizabilă prin șabloane**  
- Control granular asupra **relevanței statisticilor și alertelor**  

Împreună, aceste capabilități permit organizațiilor nu doar să detecteze probleme, ci și să **înțeleagă, standardizeze și controleze calitatea datelor**.

---

## Cine beneficiază de această versiune  

- **Data Engineers:** Logică de validare reutilizabilă și control îmbunătățit asupra comportamentului de monitorizare  
- **Echipe de Calitate și Guvernanță a Datelor:** Reguli standardizate și validare consistentă a datelor între sisteme  
- **Echipe Analytics & BI:** Înțelegere mai bună a trendurilor și deviațiilor  
- **Platform Owners:** Creștere a adopției prin analiză simplificată și validare scalabilă  

---

## Actualizări CLI  
- Nicio modificare  

---