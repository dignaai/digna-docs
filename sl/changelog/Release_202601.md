# Changelog – Release 2026.01  

Z izdajo Release 2026.01 digna predstavlja pomembne izboljšave v modeliranju podatkovnih virov, upravljanju povezav in uporabnosti pregledov.  
Ta izdaja povečuje prilagodljivost v vseh modulih in občutno širi področje **kakovosti podatkov in preverjanja**.

---

## Nove funkcije  

### Globalne povezave do baz podatkov  
- Povezave do baz podatkov so zdaj konfigurirane na **globalni ravni**.  
- Globalne povezave je mogoče ponovno uporabiti v **vseh projektih**, kar poenostavlja konfiguracijo in vzdrževanje.  
- **Vpliv:** Zmanjšuje operativno obremenitev in zagotavlja dosledno povezljivost v različnih okoljih.

### Več konfiguracij povezav virov na projekt  
- Projekti lahko zdaj sklicujejo **več konfiguracij povezav virov**.  
- Omogoča bolj prilagodljive nastavitve za kompleksne podatkovne pokrajine projektov.  
- **Vpliv:** Podpira realistično podjetniško arhitekturo z heterogenimi viri podatkov.

### Logični podatkovni viri  
- Podatkovni viri zdaj predstavljajo **logično plast** znotraj projekta.  
- Vsak podatkovni vir je lahko podprt z:
    - **tabelo v bazi podatkov**
    - **pogledom v bazi podatkov**
    - **poizvedbo SQL po meri**  
- Ta ločitev izboljšuje ponovno uporabo, jasnost in modeliranje pregledov v različnih modulih.  
- **Vpliv:** Loči inšpekcije in pravila kakovosti podatkov od fizičnega shranjevanja, kar izboljšuje vzdrževanje in ponovno uporabo.

### Pogoj relevantnosti anomalije  
- Zdaj je mogoče definirati **pogoj relevantnosti anomalije**, da se nadzoruje ocenjevanje stanja anomalij na ravni nabora podatkov.  
- Statistike se izračunavajo neodvisno od tega, ali je pogoj nastavljen ali izpolnjen.  
- Če pogoj **ni izpolnjen**, **digna Data Anomalies** ne podaja statusa anomalije (green / yellow / red).  
- **Primer:** Izključite nabor podatkov iz ocenjevanja anomalij, ko je število zapisov manjše od 10.  
- **Vpliv:** Zagotavlja, da se anomalije ocenjujejo le v relevantnih poslovnih kontekstih.

### Konfiguracija obvestil po modulih  
- Obvestila je zdaj mogoče konfigurirati **po posameznih modulih** neposredno v digna.  
- Omogoča neodvisen nadzor obnašanja alarmiranja za **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** in druge module.  
- **Vpliv:** Omogoča natančne strategije obveščanja, usklajene z odgovornostmi ekip in kritičnostjo.

### Izvoz rezultatov pregledov (CSV)  
- Uporabniki lahko zdaj **prenesejo rezultate pregledov kot CSV datoteke**.  
- Omogoča analizo brez povezave, poročanje in integracijo z zunanjimi orodji.  
- **Vpliv:** Poenostavlja revizije, poročanje in nadaljnjo analizo kakovosti podatkov.

---

## Razširjene zmogljivosti Data Validation  

Z to izdajo **digna Data Validation** zdaj podpira obsežen nabor pravil kakovosti podatkov:

- **Pravila preverjanja na ravni vrstic**  
- **Preverjanja unikatnosti za več stolpcev**  
- **Preverjanje referenčne celovitosti med podatkovnimi viri**

Skupaj ta preverjanja omogočajo uveljavljanje **strukturnih in relacijskih pravil kakovosti podatkov** v kompleksnih podatkovnih pokrajinah.

### Preverjanja unikatnosti za več stolpcev
- Uvedena so **preverjanja unikatnosti** za nastavljiv **nabor stolpcev**.  
- Omogoča preverjanje sestavljenih ključev in poslovnih omejitev unikatnosti.  
- **Vpliv:** Odkrije podvojene poslovne entitete, ki jih ni mogoče identificirati z enostavnimi preverjanji po posameznem stolpcu.

### Preverjanje referenčne celovitosti
- Uvedena so **preverjanja referenčne celovitosti** za validacijo odnosov med podatkovnimi viri.  
- Zagotavlja, da vrednosti tujih ključev v izvornih podatkovnih virih obstajajo v referenciranih ciljnih podatkovnih virih.  
- Pomaga zgodaj odkriti osirotele zapise, prekinjene povezave in težave s konsistentnostjo podatkov.  
- Oblikovana so za delo z **logičnimi podatkovnimi viri**, vključno s pogledi in poizvedbami po meri.  
- **Primeri uporabe:** celovitost podatkovnega skladišča, regulativno poročanje, konsistentnost osnovnih podatkov in zanesljiva nadaljnja analitika.

---

## Kdo ima koristi od te izdaje  

- **Data Engineers:** bolj prilagodljivo modeliranje podatkovnih virov in ponovno uporabne povezave do baz podatkov  
- **Data Quality & Governance Teams:** razširjeno področje preverjanj, vključno s pravili relacijske celovitosti  
- **Analytics & BI Teams:** čistejši vhodi in izvozljivi rezultati pregledov  
- **Platform Owners:** zmanjšana kompleksnost konfiguracije in izboljšano operativno vzdrževanje

---

## CLI posodobitve  
- Brez sprememb

---