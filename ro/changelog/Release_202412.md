# Jurnal de modificări – Lansare 2024.12

Lansarea 2024.12 aduce un set nou de funcționalități și îmbunătățiri care fac digna mai automatizată, flexibilă și pregătită pentru mediul de business.  
Această versiune îmbunătățește programarea, raportarea, gestionarea interogărilor și acuratețea detectării anomaliilor.  

---

## Funcționalități noi

### Scheduler încorporat
Inspecțiile nu mai depind exclusiv de linia de comandă sau apeluri API.  
Cu noul **digna Scheduler**, inspecțiile pot fi executate automat la ore definite.  

- Acceptă **expresii Cron** pentru programări recurente (zilnic, săptămânal sau intervale personalizate).  
- Oferă control precis prin **offset-uri**, **date de început** și **date de sfârșit**.  
- Permite echipelor să se asigure că toate sursele critice de date sunt inspectate constant și fără efort manual.  

---

### Rapoarte în format PDF
Echipele pot partaja acum rezultatele cu părțile interesate prin **exporturi PDF**.  

- Graficele, metricile și rezultatele anomaliilor pot fi exportate într-un format PDF profesional.  
- Rapoartele combină **vizualizările** și **datele subiacente** pentru a servi atât utilizatorilor tehnici, cât și celor de business.  
- Elimină necesitatea unor instrumente externe pentru crearea rapoartelor.  

---

### Tip nou de coloană: `CUSTOM`
Pentru a oferi mai multă flexibilitate, digna introduce un nou tip de coloană **`CUSTOM`**.  

- Utilizatorii pot defini exact ce **statistici și metrici** se aplică anumitor atribute.  
- Perfect pentru cazuri speciale care nu se încadrează în categoriile standard precum NUMERICAL sau CATEGORICAL.  
- Ajută la menținerea analizelor concentrate și a rezultatelor relevante pentru contextul de afaceri.  

---

### Placeholder-e noi în interogările snapshot
Interogările snapshot sunt acum mai simple și mai puțin predispuse la erori datorită **placeholder-elor dinamice**.  

- Token-uri precum `#date+n#` sau `#date-n#` ajustează automat datele în interogări.  
- Exemplu:  
  - `#date+1#` → mâine  
  - `#date-2#` → acum două zile  
- Elimină calculele manuale ale datelor și asigură consistența între echipe.  

---

### Optimizarea pragurilor
Pragurile pentru anomalii sunt acum mai inteligente și sensibile la context.  

- Pentru metrici precum **NULL COUNT**, pragurile inferioare sunt automat limitate la **0**.  
- Previne praguri invalide sau lipsite de sens.  
- Rezultă într-un număr mai mic de alarme false și o detectare a anomaliilor mai fiabilă.  

---

## Îmbunătățiri generale
- Componente **UI** rafinate în vizualizările de configurare a proiectelor și a atributelor.  
- Performanță îmbunătățită a **dashboard-ului** pentru volume mari de date.  
- Îmbunătățiri ale logging-ului și ale mesajelor de eroare pentru depanare.  

---

## Rezumat
Lansarea 2024.12 întărește digna ca platformă pentru **calitatea datelor, detectarea anomaliilor și observabilitate**.  
Prin automatizare prin programare, rapoarte PDF partajabile, coloane personalizabile, interogări snapshot simplificate și praguri mai inteligente, digna devine și mai valoroasă atât pentru utilizatorii tehnici, cât și pentru părțile interesate din business.