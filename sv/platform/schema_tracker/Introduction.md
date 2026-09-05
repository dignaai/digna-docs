# Data Schema Tracker – Övervaka schemats utveckling
<h1 style="display:none;">AI-driven modul för metadata-observabilitet och datakvalitet – digna Data Schema Tracker</h1>

---

## Syfte

The **Data Schema Tracker** håller dig informerad om hur dina databasscheman utvecklas.  
Den övervakar kontinuerligt **tabellscheman, kolumner och datatyper** för att upptäcka **schemadrift** — avsiktliga eller oavsiktliga strukturella förändringar som kan störa pipelines, ETL-jobb eller BI-instrumentpaneler.

Genom att säkerställa transparens i schemautvecklingen hjälper digna organisationer att bibehålla **förtroende för datakvaliteten**, upprätthålla **observabilitet i datasystemen** och undvika kostsamma produktionsincidenter orsakade av oupptäckta schemaändringar.

---

## Teknisk översikt

### Vad den övervakar

- **Tillagda eller borttagna kolumner** – Upptäcker nyligen introducerade, bytta namn på eller borttagna kolumner.  
- **Ändringar av datatyp** – Identifierar ändringar såsom `INT → VARCHAR` eller `DATE → TIMESTAMP`.  
- **Tabell- och vyändringar** – Spårar skapande, namnändring eller borttagning av tabeller och vyer.  
- **Skillnader mellan miljöer** – Jämför schemaversioner mellan Dev, Test och Production.

### Detektion & avisering

- Skannar **databasmetadata** eller **systemkataloger** direkt i din dataplattaform.  
- Jämför varje schema-ögonblicksbild med den tidigare kända versionen som lagras i digna’s observability schema.  
- Genererar **realtidslarm** i instrumentpanelen, via API eller externa notifieringskanaler (e-post, Slack, webhook).  
- Loggar varje schemaversion för **historisk spårning och revisionsberedskap**.

---

## Arkitektur och körning

- **Körning i databasen:** digna körs helt inom din miljö och frågar metadata-vyer utan att extrahera någon användardata.  
- **Lättviktig skanning:** får endast åtkomst till strukturell information — aldrig användardata.  
- **Centraliserad lagring:** schemametadata och poster om drift lagras i digna observability-schema för visualisering och analys.  
- **Automatisering:** stödjer schemalagda eller händelsebaserade skanningar via digna Core eller externa orkestreringsverktyg.  

---

## Exempel på användningsfall

| Användningsfall | Beskrivning |
|-----------------|-------------|
| **Övervakning av ETL-stabilitet** | Upptäck ändringar i upstream-strukturen innan pipelines fallerar på grund av schemaavvikelser. |
| **Business Intelligence-tillförlitlighet** | Förhindra trasiga instrumentpaneler orsakade av omdöpta eller saknade kolumner. |
| **Datalagerstyrning** | Behåll en granskningsbar historik över schemautveckling för efterlevnad och påverkananalys. |
| **Översyn av integrationer** | Säkerställ att data lake- och datalager-scheman förblir synkroniserade efter strukturella uppdateringar. |

---

## Fördelar

| Område | Fördel |
|--------|--------|
| **Datakvalitet** | Förhindrar oupptäckt schemadrift som kan korrumpera eller ogiltigförklara datapipelines. |
| **Observabilitet** | Lägg till strukturell övervakning till den övergripande observabiliteten i dataekosystemet. |
| **Efterlevnad** | Behåll versionerad schemahistorik för revision, spårbarhet och förändringskontroll. |
| **Förebyggande** | Upptäcker strukturella problem innan de eskalerar till rapporterings- eller produktionsfel. |

---

## Så fungerar det

1. **Snapshot Collection** – digna tar en ögonblicksbild av den aktuella schemametadatan.  
2. **Jämförelse** – den nya ögonblicksbilden jämförs