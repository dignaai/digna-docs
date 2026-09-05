# Data Timeliness – On-Time Delivery Monitoring
<h1 style="display:none;">Modul Data Timeliness alimentat de AI pentru Calitatea Datelor și Observabilitate – digna</h1>

---

## Scop

Modulul **Data Timeliness** se asigură că **datele sosesc la timp** - de fiecare dată.  
Monitorizează continuu programele de livrare și detectează automat când seturi de date, tabele sau fișiere sunt **întârziate, lipsă sau incomplete**.  

Prin combinarea învățării AI cu programe definite de utilizator, *digna* permite organizațiilor să prevină erorile în aval și să respecte țintele stricte de **SLA (Service Level Agreement)** pentru atât **Calitatea Datelor**, cât și **observabilitatea pipeline-urilor de date**.

---

## Prezentare tehnică

### Moduri duale de monitorizare
- **Tipare de sosire învățate de AI**  
  digna învață automat ritmul natural al livrărilor tale de date — zilnic, la oră sau declanșate de evenimente — analizând timestamp-urile istorice și timpii de finalizare.  
  Se adaptează la schimbări din calendare business, weekenduri sau vârfuri de sfârșit de lună.

- **Programe definite de utilizator**  
  Utilizatorii pot defini explicit orele de livrare așteptate (de ex., *în fiecare zi lucrătoare înainte de 7:30 AM*).  
  digna compară timpul efectiv de sosire cu programul planificat și generează alerte când datele sunt întârziate sau lipsesc.

### Mecanism de detectare
- Evaluează **timestamp-urile din metadata**, **numărul de înregistrări** și **freshness-ul tabelelor**  
- Detectează **job-uri ETL blocate**, **extracții eșuate** și **arrivări parțiale de fișiere**  
- Se integrează cu *Data Anomalies* și *Data Validation* pentru perspective combinate

---

## Scenarii de detectare

| Scenario | Descriere |
|-----------|--------------|
| **Sosire întârziată a datelor** | Feed zilnic de date de piață întârziat cu două ore, cauzând rapoarte care nu respectă SLA-urile |
| **Încărcare lipsă** | Un tabel sau o partiție programată nu este actualizată pentru data curentă |
| **Întârziere din dependențe în lanț** | Întârzierea unui job upstream afectează reîmprospătarea pipeline-ului downstream |
| **Schimbare de pattern în weekend** | Modelul AI se adaptează automat când nu se așteaptă date duminica |

---

## Arhitectură și execuție

- **Execuție în baza de date:** digna rulează verificările de timeliness direct în baza ta de date sau data warehouse.  
- **Acces metadata ușor:** citește timestamp-urile job-urilor, numărul de înregistrări și informațiile despre partiții — nu sunt necesare extrageri de date.  
- **Frecvență configurabilă:** programează monitorizarea per dataset, schemă sau pipeline.  
- **Alerte cross-module:** rezultatele pot declanșa avertizări vizuale în *Inspection Hub* sau notificări prin email, Slack sau API.  

---

## Exemple de cazuri de utilizare

- **Feed-uri piețe financiare:** detectează întârzierile în actualizările de prețuri sau tranzacții.  
- **Încărcări în Data Warehouse:** monitorizează când job-urile ETL nocturne se termină mai târziu decât era de așteptat.  
- **Partajarea datelor între echipe:** asigură că livrările departamentale de date au loc înainte de cutoff-urile zilnice.  
- **Raportare regulatorie:** confirmă că depunerile includ cel mai recent snapshot disponibil al datelor.  

---

## Beneficii

| Domeniu | Beneficiu |
|------|----------|
| **Continuitate business** | Previne întreruperile operaționale cauzate de date întârziate sau lipsă |
| **Calitatea datelor** | Îmbunătățește fiabilitatea și consistența pipeline-urilor de date |
| **Conformitate** | Asigură respectarea SLA-urilor și transparență pentru audit |
| **Automatizare** | AI elimină urmărirea manuală a programelor |
| **Integrare** | Funcționează perfect cu *Data Analytics* pentru a vizualiza tendințele de timeliness în timp |

---

## Cum învață digna timpii de livrare așteptați

1. **Analiză istorică:** digna observă timpii și duratele încărcărilor anterioare.  
2. **Modelare AI:** Machine learning creează o bază dinamică pentru sosirea așteptată.  
3. **Monitorizare:** Fiecare livrare nouă este comparată cu baza de referință.  
4. **Alertare:** Abaterile declanșează alerte cu metrici contextuale și scoruri de încredere.  

Această abordare de învățare continuă se adaptează la procesele în evoluție, menținând în același timp un nivel scăzut de false positive.

---

## Întrebări frecvente

**Pot defini propriile ore de livrare?**  
Da. digna suportă atât programe fixe definite de utilizator, cât și pattern-uri învățate de AI.

**Se poate integra cu ETL-ul meu sau cu un tool de orchestrare?**  
Da. digna se integrează cu instrumente precum Airflow, dbt, Informatica sau scheduler-e custom.

**Unde are loc calculul?**  
Toată analiza rulează în cadrul bazei tale de date sau cloud warehouse — nu se folosește niciun serviciu extern.

**Ce se întâmplă când datele întârzie?**  
digna generează alerte în dashboard, în Inspection Hub și prin API/webhooks pentru a notifica echipele de operațiuni instant.

---


**digna Data Timeliness** ajută la asigurarea **încrederii în date**, combinând **detecție asistată de AI**, **execuție on-premises** și **observabilitate a datelor** — toate în mediul tău controlat.