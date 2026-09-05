# Data Anomalies – Automated Detection
<h1 style="display:none;">Modul, pogonjen z AI za kakovost in observabilnost podatkov – digna Data Anomalies</h1>

---

## Namen

Modul **Data Anomalies** samodejno identificira nepravilnosti v vaših podatkovnih naborih — brez pisanja pravil.  
Neprekinjeno spremlja **kakovost dostave podatkov**, uči se, kako izgleda "normalno", in zaznava odstopanja v realnem času.

Z uporabo odkrivanja, ki ga poganja AI, digna prepozna *tihe napake v podatkih*, kot so manjkajoči, podvojeni ali poškodovani zapisi, ki lahko izkrivijo poročila, ML modele in dashboards.

---

## Tehnični pregled

### Analizirane metrike

digna neprekinjeno profilira naslednje vidike vaših podatkov:

- **Obseg zapisov** – skupno število vrstic, dnevno ali po batch serijah  
- **Manjkajoče vrednosti** – zaznavanje null ali praznih polj  
- **Porazdelitve in histogrami** – spremljanje sprememb oblike podatkov  
- **Razponi vrednosti** – samodejna identifikacija vrednosti izven pričakovanih meja ali ekstremnih vrednosti  
- **Enoličnost** – preverjanje podvojenih ključev ali ponovljenih vnosov  

### Pametno zaznavanje anomalij

- Uporablja **učenje iz zgodovine** za dinamično določanje pričakovanih meja  
- Zaznava odstopanja v **volumnu, porazdelitvah vrednosti ali logičnih razmerjih**  
- Uporablja AI za samodejno prilagajanje pragov glede na čas dneva ali sezonske vzorce  
- Ločuje **statistična nihanja** od pravih anomalij  
- Ustvari podrobne metrike in ocene zaupanja za vsak nabor podatkov in stolpec  

---

## Scenariji zaznavanja

Spodaj so primeri realnih težav, ki jih modul **Data Anomalies** samodejno ujame:

| Scenario | Description |
|-----------|--------------|
| **Volume drops or spikes** | Izguba polovice dnevnih transakcij, podvojeni batch naloži ali nenaden skok volumna podatkov |
| **Missing or null values** | Ekstrakcije podatkov so zaključene, vendar kritični stolpci ostanejo prazni |
| **Distribution drifts** | Povprečen znesek nakupa ali število transakcij na regijo se nepričakovano spremeni |
| **Column swaps** | Stolpci, kot sta *first_name* in *last_name*, so med ETL postopkom pomotoma zamenjani |
| **Unexpected categorical values** | npr. “Zurich” se pojavi na seznamu avstrijskih mest |
| **Sudden uniqueness loss** | Prej enolični ID-ji začnejo duplicirati zaradi napak pri zgornjih join operacijah |

---

## Arhitektura in izvajanje

- **Izvajanje v bazi podatkov:** Vsa logika zaznavanja anomalij se izvaja *znotraj pogona baze podatkov* (Teradata, Snowflake, Databricks, PostgreSQL itd.)  
- **Brez premikanja podatkov:** digna bere samo metrike, surovih podatkov nikoli ne prenaša zunaj  
- **Inkrementalne posodobitve:** Pri vsaki izvedbi se analizira le nov segment podatkov za večjo učinkovitost  
- **Konfigurabilna frekvenca pregledov:** Na uro, dnevno ali sproženo s strani zgornjih procesov  
- **Shranjevanje rezultatov:** Metrike in zastavice anomalij se zapišejo nazaj v digna observability schema za vizualizacijo in opozarjanje  

---

## Koristi

| Področje | Korist |
|------|----------|
| **Avtomatizacija** | Odpravlja na stotine ročno napisanih SQL poizvedb ali pravil |
| **Natančnost** | Zaznava težave, ki jih statični pragovi pogosto spregledajo |
| **Razširljivost** | Učinkovito spremlja milijone zapisov na tabelo |
| **Integracija** | Deluje nemoteno z *digna Data Analytics* za analizo trendov |
| **Skladnost** | Zagotavlja kontinuiran nadzor nad **kakovostjo in observabilnostjo podatkov** |
| **Transparentnost** | Nudi ocene zaupanja, časovne žige in kode razlogov za vsako anomalijo |

---

## Kako se digna uči "normalnega"

1. **Faza profiliranja:** digna zbira metrike iz zgodovinskih podatkovnih naborov.  
2. **Faza učenja:** AI modeli identificirajo ponavljajoče se vzorce (sezonske, tedenske, dnevne).  
3. **Faza spremljanja:** Prihodnji podatkovni nabori se primerjajo z dinamično naučenimi mejnami.  
4. **Faza opozarjanja:** Odstopanja, ki presegajo statistične meje zaupanja, se prijavijo kot anomalije.  

Vsi modeli so pojasnjivi, deterministični in optimizirani za obsege podatkov v podjetjih.

---

## Primeri uporabe

- Spremljanje kakovosti podatkov v **bančnih transakcijskih sistemih**  
- Zaznavanje napak pri nalaganju v **ETL ali podatkovne skladiščne opravke**  
- Prepoznavanje nenavadnih aktivnosti strank v **telekomunikacijskih zapisih**  
- Spremljanje konsistentnosti kliničnih podatkov v **podatkovnih cevovodih zdravstvene analitike**  
- Preprečevanje okvarjenih nadzornih plošč v **BI in poročilnih okoljih**

---

## Pogosta vprašanja

**Does Data Anomalies require predefined rules?**  
Ne — modul se avtomatično uči iz vedenja podatkov.

**Can I still define specific thresholds if needed?**  
Da. digna omogoča kombiniranje zaznavanja na osnovi AI in na osnovi pravil (prek *Data Validation*).

**How are false positives minimized?**  
Modul uporablja adaptivno učenje in statistično ocenjevanje zaupanja, da zanemari normalne sezonske variacije.

**Where does computation happen?**  
Vse obdelave potekajo znotraj vaše baze podatkov — digna nikoli ne izvleče surovih podatkov.

**Is it suitable for sensitive or regulated data?**  
Da. digna deluje popolnoma on-premises ali v zasebnem oblaku in spoštuje evropske standarde skladnosti.