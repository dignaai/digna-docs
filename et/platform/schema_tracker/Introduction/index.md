# Data Schema Tracker – Monitor Schema Evolution
<h1 style="display:none;">AI-Driven Module for Metadata Observability and Data Quality – digna Data Schema Tracker</h1>

---

## Eesmärk

The **Data Schema Tracker** hoiab sind kursis sellega, kuidas sinu andmebaasi struktuurid arenevad.  
See jälgib pidevalt **tabelite skeeme, veerge ja andmetüüpe**, et tuvastada **skeemi nihet** — kavandatud või ootamatuid strukturaalseid muudatusi, mis võivad katkestada torujuhtmeid, ETL-töövooge või BI-armatuurlaudu.

Tagades skeemi evolutsiooni läbipaistvuse, aitab digna organisatsioonidel säilitada **usaldust andmete kvaliteedi vastu**, tagada **andmesüsteemide observability** ja vältida kulukaid tootmiskahjustusi, mis tekivad avastamata skeemimuudatustest.

---

## Tehniline ülevaade

### Mida see jälgib

- **Lisatud või eemaldatud veerud** – tuvastab äsja lisatud, ümbernimetatud või kustutatud veerud.  
- **Andmetüüpide muutused** – identifitseerib muutusi nagu `INT → VARCHAR` või `DATE → TIMESTAMP`.  
- **Tabelite ja vaadete muutused** – jälgib tabelite ja vaadetega seotud loomist, ümbernimetamist või eemaldamist.  
- **Keskkondadevahelised erinevused** – võrdleb skeemiversioone Dev, Test ja Production keskkondade vahel.  

### Tuvastamine ja teavitamine

- Skaneerib **andmebaasi metaandmeid** või **süsteemi katalooge** otse sinu andmeplatvormis.  
- Võrdleb iga skeemi hetktõmmist eelnevalt teadaoleva versiooniga, mis on salvestatud digna observability skeemi.  
- Genereerib **reaalajas teavitusi** armatuurlaudas, API kaudu või välistes teavitusk kanalites (e-post, Slack, webhook).  
- Logib iga skeemi versiooni **ajalooliseks jälgimiseks ja auditi valmisolekuks**.

---

## Arhitektuur ja täitmine

- **Andmebaasis täidetav:** digna töötab täielikult sinu keskkonnas, pärides metaandmete vaateid ilma kasutajaandmeid välja toomata.  
- **Kerge skaneerimine:** pääseb ligi ainult struktuurilisele infole — mitte kunagi kasutajaandmetele.  
- **Tsentraliseeritud salvestus:** skeemi metaandmed ja nihelogid salvestatakse digna observability skeemi visualiseerimiseks ja analüüsiks.  
- **Automatiseerimine:** toetab ajastatud või sündmuspõhiseid skaneeringuid digna Core'i või väliste orkestreerimistööriistade kaudu.  

---

## Näited kasutusjuhtudest

| Kasutusjuhtum | Kirjeldus |
|-----------|--------------|
| **ETL stabiilsuse jälgimine** | Tuvasta ülesvoo struktuurimuutused enne, kui torud ebaõnnestuvad skeemi mittevastavuse tõttu. |
| **Ärianalüüsi töökindlus** | Vältida katkiseid armatuurlaudu, mis tekivad ümbernimetatud või puuduolevate veergude tõttu. |
| **Andmekogu valitsemine** | Säilita auditeeritav ajalugu skeemi evolutsioonist vastavuse ja mõjude analüüsi jaoks. |
| **Integratsiooni järelevalve** | Tagada, et andmejärv ja andmelao skeemid jäävad sünkroonis pärast struktuurivärskendusi. |

---

## Kasu

| Valdkond | Kasu |
|------|----------|
| **Andmete kvaliteet** | Vältib avastamata skeemi nihet, mis võib korruptsiooni või valideerimatuseni viia andmevoogudes. |
| **Observability** | Lisab struktuursed monitooringu võimalused andmeökosüsteemi üldisele observability’le. |
| **Vastavus** | Säilitab versioonitud skeemi ajaloo auditi, jälgitavuse ja muudatuste kontrolli jaoks. |
| **Ennetus** | Tuvastab struktuursed probleemid enne, kui need eskaleeruvad aruandluse või tootmise vigadeks. |

---

## Kuidas see töötab

1. **Hetktõmmise kogumine** – digna püüdab kinni praeguse skeemi metaandmed.  
2. **Võrdlus** – uus hetktõmmis võrreldakse