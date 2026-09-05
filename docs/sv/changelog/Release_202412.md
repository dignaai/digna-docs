---
title: digna Release 2024.12 | Ändringslogg & Nya funktioner
description: Upptäck nyheterna i digna Release 2024.12. Denna version introducerar en inbyggd schemaläggare, PDF-rapportering, flexibla anpassade kolumntyper, dynamiska platshållare i snapshot-frågor och smartare tröskeloptimering för bättre anomaliupptäckt och datakvalitetsövervakning.
keywords: digna Release 2024.12, digna ändringslogg, release notes, inbyggd schemaläggare, PDF-rapporter, custom column type, snapshot query placeholders, tröskeloptimering, data observability, datakvalitetsövervakning, anomaliupptäckt
image: /assets/logo_square.png
---



# Ändringslogg – Release 2024.12

Release 2024.12 levererar ett nytt set funktioner och förbättringar som gör digna mer automatiserat, flexibelt och redo för verksamheten.  
Denna version förbättrar schemaläggning, rapportering, fråga-hantering och precisionen i anomaliupptäckten.  

---

## Nya funktioner

### Inbyggd schemaläggare
Inspektioner är inte längre beroende av enbart kommandorad eller API-anrop.  
Med den **nya digna Scheduler** kan inspektioner köras automatiskt vid angivna tidpunkter.  

- Stöder **Cron expressions** för återkommande scheman (dagligen, veckovis eller anpassade intervall).  
- Erbjuder precis kontroll via **offsets**, **startdatum** och **slutdatum**.  
- Gör det möjligt för team att säkerställa att alla kritiska datakällor inspekteras konsekvent och utan manuellt arbete.  

---

### Rapporter i PDF-format
Team kan nu enkelt dela resultat med intressenter via **PDF-exporter**.  

- Diagram, mått och anomaliresultat kan exporteras i ett professionellt PDF-format.  
- Rapporter kombinerar **visualiseringar** och **underliggande data** för både tekniska och affärsorienterade användare.  
- Eliminera behovet av externa verktyg för rapportskapande.  

---

### Ny kolumntyp: `CUSTOM`
För större flexibilitet introducerar digna en ny kolumntyp: **`CUSTOM`**.  

- Användare kan definiera exakt vilka **statistik och mått** som ska tillämpas på specifika attribut.  
- Perfekt för specialfall som inte passar in i standardkategorier som NUMERICAL eller CATEGORICAL.  
- Hjälper till att hålla analyser fokuserade och resultat relevanta för affärssammanhanget.  

---

### Nya platshållare i snapshot-frågor
Snapshot-frågor blir enklare och mindre felbenägna med **dynamiska platshållare**.  

- Token som `#date+n#` eller `#date-n#` justerar automatiskt datum i frågorna.  
- Exempel:  
  - `#date+1#` → i morgon  
  - `#date-2#` → för två dagar sedan  
- Eliminerar manuella datumberäkningar och säkerställer konsistens mellan team.  

---

### Tröskeloptimering
Anomali-trösklar är nu mer intelligenta och kontextmedvetna.  

- För mått som **NULL COUNT** begränsas lägre tröskelvärden automatiskt till **0**.  
- Förhindrar ogiltiga eller meningslösa tröskelvärden.  
- Resulterar i färre falska positiva och mer tillförlitlig anomaliupptäckt.  

---

## Allmänna förbättringar
- Förfinade **UI-komponenter** i vyerna för projekt- och attributkonfiguration.  
- Förbättrad **dashboard-prestanda** för stora datamängder.  
- Förbättrad **loggning och felmeddelanden** för felsökning.  

---

## Sammanfattning
Release 2024.12 stärker digna som en plattform för **datakvalitet, anomaliupptäckt och observability**.  
Med automatisering via schemaläggning, delbara PDF-rapporter, anpassningsbara kolumner, förenklade snapshot-frågor och smartare trösklar blir digna ännu mer värdefullt för både tekniska användare och affärsintressenter.