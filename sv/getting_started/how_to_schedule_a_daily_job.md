# Hur du schemalägger ett dagligt jobb

Schemaläggning låter dig köra inspektioner automatiskt utan manuell inblandning.  
I denna guide lär du dig hur du skapar ett jobb som körs **en gång per dag**, vilket säkerställer att din data övervakas kontinuerligt.

---

## Interaktiv demo

Följ den interaktiva guiden för att se processen i praktiken:  

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/Ra9E19A0QfMpzKqm3Yhu?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a New Data Inspection Job" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Vad du kommer att lära dig

- Hur du får åtkomst till **Scheduling**-sektionen i digna-dashboarden  
- Hur du skapar ett nytt schemalagt jobb  
- Hur du konfigurerar det att köras **dagligen vid en bestämd tidpunkt**  
- Hur du väljer rätt projekt och datasource  
- Hur du aktiverar jobbet så att det körs automatiskt  

---

## Varför dagliga jobb är användbara

Daglig schemaläggning är den vanligaste inställningen i produktionsmiljöer. Det säkerställer:  

- **Färskhet** — dagens data valideras.  
- **Konsistens** — avvikelser upptäcks tidigt innan de sprids nedströms.  
- **Automatisering** — inget behov av att manuellt starta inspektioner.  

---

## Nästa steg

- Utforska [Hur du använder crontab-definitionen](how_to_use_crontab.md) för mer avancerade anpassade scheman.  
- Kombinera dagliga jobb med **alerting** för att få aviseringar när avvikelser upptäcks.