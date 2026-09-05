# Pokročilé plánování pomocí crontab

Tento průvodce ukazuje, jak plánovat úlohy v *digna* pomocí **crontab výrazů**.  
Na rozdíl od standardních vzorů (denně, týdně, měsíčně) vám crontab dává plnou flexibilitu pro definování vlastních rozvrhů.

---

## Interaktivní ukázka

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Co se naučíte

- Jak otevřít sekci **Scheduling** v dashboardu  
- Jak vytvořit novou úlohu pomocí **crontab výrazu**  
- Jak nastavit plán, který poběží pouze o **víkendech v 10:00**  

---

## Příklad: Plán na víkend

Chcete-li naplánovat úlohu tak, aby běžela každou **sobotu a neděli v 10:00**, použijte následující výraz:


- `0` → minuta (v celou hodinu)  
- `10` → hodina (10:00)  
- `*` → každý den v měsíci  
- `*` → každý měsíc  
- `sat,sun` → pouze v soboty a neděle  

---

## Proč používat crontab?

- Vytvořit plány mimo standardní denní, týdenní nebo měsíční vzory  
- Definovat přesné časy běhu (konkrétní dny, hodiny nebo intervaly)  
- Užitečné pro víkendové úlohy, kontroly mimo špičku nebo časté monitorování  

---