# Izmaiņu žurnāls – versija 2026.06  

Ar izlaidumu 2026.06 digna sper lielu soli uz priekšu automatizācijas, paplašināmības un platformas lietojamības jomā.  
Šī versija ievieš jauno **digna Python SDK**, oficiālu **Docker izvietošanas atbalstu**, pārdizainētu informācijas paneļa pieredzi un uzlabotu pārnēsājamību validācijas noteikumu pārvaldībā.

---

## Noskatieties laidiena prezentāciju

<!--YOUTUBE EMBED START--><div style="position: relative; padding-bottom: 56.25%; height: 0; width: 100%;"><iframe src="https://www.youtube-nocookie.com/embed/g6ZQl9pc4vg" title="What&#39;s New in digna | The Major Release of 2026" frameborder="0" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div><!--YOUTUBE EMBED END-->

*[What's New in digna | The Major Release of 2026](https://www.youtube.com/watch?v=g6ZQl9pc4vg) — ieskats šajā laidienā digna YouTube kanālā.*

---

## Jaunumi  

### digna Python SDK – Automatizējiet visu ar Python  
- Instalēšanai:
  ```bash
  pip install digna-sdk
  ```
- Programmatīvi pārvaldīt un automatizēt digna, izmantojot Python  
- Izveidot un konfigurēt projektus, izmantojot kodu  
- Aktivizēt inspekcijas un monitoringa izpildes  
- Programmatīvi pārvaldīt datu kopas, noteikumus un konfigurācijas  
- Profilēt tabulas un iegūt metadatu ieskatus  
- Eksportēt profilēšanas un datu kvalitātes rezultātus uz ārējām repozitorijām un sistēmām  
- Integrēt ar notebookiem, orkestrācijas rīkiem un CI/CD cauruļvadiem  

**Ietekme:** Iespējota pilnīga infrastruktūra-kā-kods un dziļa datu kvalitātes un novērošanas darba plūsmu automatizācija, izmantojot Python.

---

### Docker atbalsts – vienkāršota izvietošana un darbība  
- Oficiāls Docker attēla atbalsts digna  
- Ātra un konsekventa iestatīšana dažādās vidēs  
- Vienkāršota ieviešana izstrādes, testēšanas un produkcijas vidēs  
- Viegla integrācija ar Kubernetes un citiem konteineru platformu risinājumiem  
- Uzlabota izvietojumu pārnēsājamība un reproducējamība  

**Ietekme:** Padara digna vienkāršāku izvietošanai un pārvaldībai mūsdienu mākoņnatīvās arhitektūrās.

---

### QueryMode – elastīga SQL izpildes stratēģija

Konfigurējiet vaicājumu izpildes stratēģiju: **Single** vai **Combined** režīms

**Single režīms**: Katra statistika tiek aprēķināta ar vienu atsevišķu SQL vaicājumu

  - Ideāli lielām datu avotu vidēm, kur ir bažas par atmiņas ierobežojumiem  
  - Novērš kombinētā vaicājuma resursu izsīkšanu (piem., atmiņas izsīkšana, spool ierobežojumi)  
  - Lielāks vaicājumu skaits, bet mazāks atmiņas patēriņš uz vaicājumu

**Combined režīms**: Visas statistikas tiek aprēķinātas vienā SQL vaicājumā

  - Samazina kopējo vaicājumu skaitu un tīkla režiju  
  - Optimizē veiktspēju, ja datu avoti ir pārvaldāmi atmiņā  
  - Efektīvāks biežām, paralēlām izpildēm

**Ietekme:** Lietotājiem tiek dota smalkāka kontrole pār vaicājumu izpildi, ļaujot balansēt veiktspēju, resursu patēriņu un atmiņas drošību atkarībā no datu avotu īpašībām.

---

### Konfigurējams prognozēšanas modelis

Modelis, uz kura balstās anomāliju noteikšana, tagad ir konfigurējams. Septiņi parametri nosaka, kā prognoze tiek pielāgota:

- Break Sensitivity
- Outlier Sensitivity
- Memory
- Ridge Strength
- Gap Tolerance
- Outlier Correction
- Plausible Range Tightness

Noklusējuma vērtības ir piemērotas lielākajai daļai rindu, un katru parametru jebkurā brīdī var atjaunot uz tā noklusējuma vērtību.

**Ietekme:** Dod lietotājiem kontroli pār pašu prognozēšanas modeli līdzās esošajiem pielaides joslas iestatījumiem Sensitivity un Memory. Lai saņemtu norādes, kad pievērsties kādam parametram un kā to iestatīt, sazinieties ar digna.

---

### Pārdizainēta informācijas paneļa pieredze  
- Modernizēta un uzlabota UI/UX dizains  
- Skaidrāka navigācija un struktūra  
- Labāka monitoringa rezultātu un datu kvalitātes ieskatu pārskatāmība  
- Uzlabota trauksmju, statistiku un paneļu lasāmība  
- Ātrāka piekļuve svarīgākajai operacionālajai informācijai  

**Ietekme:** Uzlabo lietojamību un ikdienas produktivitāti visiem lietotājiem.

---

### Paplašināta importēšana un eksportēšana validācijas noteikumiem  
- Uzlabota importēšanas/eksportēšanas funkcionalitāte validācijas noteikumiem  
- Vienkāršāka migrācija starp vidēm un projektiem  
- Uzlabota standarta noteikumu kopu atkārtota izmantošana  
- Labāka pārvaldība un noteikumu dzīves cikla kontrolēšana  
- Vienkāršota sadarbība starp komandām  

**Ietekme:** Iespējo mērogojamu un konsekventu datu kvalitātes pārvaldību visā organizācijā.

---

## Platformas uzlabojumi  

- Pilnīga Python SDK integrācija automatizācijai  
- Konteinerizēta izvietošana caur Docker  
- Uzlabota UX ar pārdizainētu informācijas paneli  
- Paplašināta validācijas loģikas pārnēsājamība  

---

## Kam šī versija noder  

- Datu inženieri: automatizācija, SDK izmantošana, cauruļvadu integrācija  
- Platformas komandas: vienkāršota izvietošana ar Docker  
- Datu pārvaldības komandas: atkārtoti izmantojama validācijas noteikumu pārvaldība  
- Analītikas komandas: uzlabota lietojamība un ieskatu redzamība  

---

## CLI atjauninājumi  
- Pievienota SDK integrācijas atbalsts  
- Uzlaboti importēšanas/eksportēšanas darbplūsmas  
- Vispārīgi stabilitātes un veiktspējas uzlabojumi