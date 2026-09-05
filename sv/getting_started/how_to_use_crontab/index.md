# Avancerad schemaläggning med Crontab

Denna guide visar hur du schemalägger jobb i *digna* med **crontab-uttryck**.  
Till skillnad från standardmönstren (dagligt, veckovis eller månatligt) ger crontab dig full flexibilitet att definiera egna scheman.

---

## Interaktiv demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Vad du kommer att lära dig

- Hur du öppnar **Scheduling**-sektionen i dashboarden  
- Hur du skapar ett nytt jobb med ett **crontab-uttryck**  
- Hur du ställer in ett schema som endast körs **på helger kl. 10:00**  

---

## Exempel: Helgschema

För att schemalägga ett jobb så att det körs varje **lördag och söndag kl. 10:00**, använd följande uttryck:


- `0` → minut (på timmen)  
- `10` → timme (kl. 10:00)  
- `*` → varje dag i månaden  
- `*` → varje månad  
- `sat,sun` → endast lördagar och söndagar  

---

## Varför använda Crontab?

- Skapa scheman utöver standardmönster (dagligt, veckovis eller månatligt)  
- Definiera exakta körtider (specifika dagar, timmar eller intervaller)  
- Användbart för helgjobb, kontroller utanför arbetstid eller frekvent övervakning  

---