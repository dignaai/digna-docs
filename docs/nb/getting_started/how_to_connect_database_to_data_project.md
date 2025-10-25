---
title: Koble til en database | digna-dokumentasjon
description: Trinnvis veiledning for å koble en database til et eksisterende prosjekt i digna. Lær hvordan du konfigurerer tilkoblinger, oppgir legitimasjon og aktiverer sikker tilgang.
---

# Koble til en database

Denne veiledningen viser de minimale trinnene for å legge til en databaseforbindelse i prosjektet ditt.

## Interaktiv demo

<!--ARCADE EMBED START-->
<div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;">
  <iframe
    src="https://demo.arcade.software/NhlhDLqeW9wC5zaLlYPa?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true"
    title="Koble en database til et prosjekt"
    frameborder="0"
    loading="lazy"
    webkitallowfullscreen
    mozallowfullscreen
    allowfullscreen
    allow="clipboard-write"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;">
  </iframe>
</div>
<!--ARCADE EMBED END-->

---

### Trinn

1. **Åpne prosjektet ditt**  
   Fra venstremenyen, klikk på **Prosjekter** og velg målprosjektet.

2. **Legg til en tilkobling**  
   Gå til **Tilkoblinger** og klikk **Legg til tilkobling**.

3. **Velg databasenstype**  
   Velg databasen du vil koble til (f.eks. PostgreSQL, MySQL, SQL Server, Oracle, Snowflake, Teradata).

4. **Oppgi tilkoblingsdetaljer**  
   Fyll ut **Navn**, **Host**, **Port**, **Database/Service**, og **Credentials** (brukernavn/passord eller SSO, etter hva som er aktuelt).

5. **Test og lagre**  
   Klikk **Test**. Hvis vellykket, klikk **Lagre**. Tilkoblingen vil vises under **Tilkoblinger** for prosjektet.