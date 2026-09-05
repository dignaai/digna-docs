# Változásnapló – Kiadás 2026.04  

A 2026.04-es kiadással a digna jelentősen bővíti analitikai és adatvalidációs képességeit.  
Ez a verzió fejlett idősorelemzést, újrahasznosítható validációs komponenseket és az értékek központi szabványosítását vezeti be.

---

## Új funkciók  

### Analytics Chart – Idősorelemzés adattudományi háttér nélkül  
- Új **Analytics Chart** interaktív idősorelemzéshez  
- Beépített analitikai módszerek:
    - Lineáris, kvadratikus és köbös regresszió  
    - Szakaszos regresszió konfigurálható töréspontokkal  
    - Simítási technikák  
    - Kvantilis elemzés  
- Trendek, szezonalitás és mintaváltások automatikus felismerése  
- Reziduális elemzés a eltérések mélyebb megértéséhez  
- Az idősorok minden adatkészlethez automatikusan kiszámításra kerülnek  

**Hatás:** Lehetővé teszi a felhasználók számára, hogy összetett időbeli viselkedést értsenek meg adattudományi szakértelem vagy külső eszközök nélkül.

---

### Enumerations – Engedélyezett értékek központi meghatározása  
- Újrahasznosítható halmazok definiálása engedélyezett értékekre (pl. országok, államok, státuszkódok)  
- Oszlopértékek ellenőrzése előre definiált enumerációk ellen a **digna Data Validation**-ben  
- Enumerációk újrafelhasználása projektek és adatforrások között  
- Enumerációk használata bárhol a `#ENUM:MY_ENUM#` jelöléssel  
- Az összes ellenőrzés **közvetlenül a forrásadatbázisban** fut le  

**Hatás:** Biztosítja az egységes és standardizált adatértékeket a szervezeten belül.

---

### Validation Rule Templates – Újrahasznosítható adatminőségi logika  
- Újrahasznosítható validációs szabályok definiálása (pl. szóköz ellenőrzés, NOT NULL, formátumellenőrzés)  
- Sablonok alkalmazása több adatkészleten keresztül  
- Konzisztens szabálylogika biztosítása projektek között  
- Duplikáció és kézi konfiguráció csökkentése  
- Az összes ellenőrzés **közvetlenül a forrásadatbázisban** fut le  

**Hatás:** Skálázható és nagy teljesítményű adatvalidációt tesz lehetővé adatmozgatás nélkül.

---

### Statisztika-szintű relevanciafeltételek  
- Relevanciafeltételek megadása **oszlop szintjén minden statisztikához**  
- Kiterjeszti az anomália relevanciafeltételek koncepcióját  
- Szabályozza, mikor tekintendő egy statisztika relevánsnak  
- Zaj csökkentése a nem kritikus helyzetek kizárásával  

**Hatás:** Javítja a jelminőséget azáltal, hogy csak a lényeges eltérésekre fókuszál.

---

## Kiterjesztett Data Analytics & validációs képességek  

Ezzel a kiadással a digna bővíti mind az **adatmegértést**, mind az **adatvalidáció standardizálását**:

- Fejlett **idősor értelmezés** adattudományi ismeretek nélkül  
- Az **engedélyezett értékek központi definiálása** enumerációkon keresztül  
- Újrahasznosítható **validációs logika sablonokkal**  
- Finomhangolt kontroll a **statisztikák és riasztások relevanciája** felett  

Ezek a képességek együtt lehetővé teszik a szervezetek számára, hogy ne csak problémákat észleljenek, hanem azokat **megértsék, szabványosítsák és kontrollálják az adatminőséget**.

---

## Kik profitálnak ebből a kiadásból  

- Adatmérnökök: újrahasznosítható validációs logika és jobb kontroll a monitorozás viselkedése felett  
- Adatminőség- és kormányzási csapatok: szabványosított szabályok és konzisztens adatvalidáció rendszerek között  
- Analytics és BI csapatok: jobb rálátás a trendekre és eltérésekre  
- Platformtulajdonosok: megnövelt elfogadás egyszerűsített analitikával és skálázható validációval  

---

## CLI frissítések  
- Nincs változás  

---