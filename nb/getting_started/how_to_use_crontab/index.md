# Avansert planlegging med crontab

Denne veiledningen viser hvordan du planlegger jobber i *digna* ved å bruke **crontab-uttrykk**.  
I motsetning til standardmønstrene (daglig, ukentlig, månedlig) gir crontab deg full fleksibilitet til å definere egendefinerte tidsplaner.

---

## Interaktiv demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Dette vil du lære

- Hvordan åpne **Scheduling**-seksjonen i dashbordet  
- Hvordan opprette en ny jobb ved å bruke et **crontab-uttrykk**  
- Hvordan sette en tidsplan som kun kjører i **helgene kl. 10:00**  

---

## Eksempel: Helgeplan

For å planlegge en jobb som kjører hver **lørdag og søndag kl. 10:00**, bruk følgende uttrykk:


- `0` → minutt (på hel time)  
- `10` → time (kl. 10)  
- `*` → hver dag i måneden  
- `*` → hver måned  
- `sat,sun` → kun på lørdager og søndager  

---

## Hvorfor bruke crontab?

- Opprett tidsplaner utover standard daglige, ukentlige eller månedlige mønstre  
- Definer nøyaktige kjøretidspunkter (spesifikke dager, klokkeslett eller intervaller)  
- Nyttig for helgejobber, kontroller utenom arbeidstid eller hyppig overvåking  

---