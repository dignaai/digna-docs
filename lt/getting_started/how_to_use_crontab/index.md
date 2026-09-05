# Išplėstinis planavimas su Crontab

Šis vadovas parodo, kaip *digna* suplanuoti užduotis naudojant **crontab išraiškas**.  
Skirtingai nei standartiniai šablonai (kasdien, kas savaitę, kas mėnesį), crontab suteikia pilną lankstumą kuriant pasirinktinius grafikus.

---

## Interaktyvi demonstracija

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Ko išmoksite

- Kaip atidaryti **Scheduling** skyrių dashboard'e  
- Kaip sukurti naują užduotį naudojant **crontab išraišką**  
- Kaip nustatyti tvarkaraštį, kuris vykdomas tik **savaitgaliais 10:00**  

---

## Pavyzdys: savaitgalio tvarkaraštis

Norėdami suplanuoti užduotį, kuri vykdoma kiekvieną **šeštadienį ir sekmadienį 10:00**, naudokite šią išraišką:


- `0` → minutė (pilna valanda)  
- `10` → valanda (10:00)  
- `*` → kiekvieną mėnesio dieną  
- `*` → kiekvieną mėnesį  
- `sat,sun` → tik šeštadieniais ir sekmadieniais  

---

## Kodėl naudoti Crontab?

- Kurkite grafikus, viršijančius standartinius kasdienius, kas savaitę ar kas mėnesį modelius  
- Nustatykite tikslius vykdymo laikus (konkretūs dienos laikai, valandos ar intervalai)  
- Naudinga savaitgalio užduotims, ne darbo valandų patikroms arba dažnam stebėjimui  

---