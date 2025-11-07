## Formål med Kommandolinjegrænsefladen (CLI)

Den ***digna*** Command Line Interface (CLI) er et kraftfuldt værktøj designet til at strømline interaktioner med ***digna***-platformen. Den giver en tekstbaseret grænseflade, som gør det muligt for brugere at udføre en bred vifte af opgaver effektivt, uden behov for en grafisk brugerflade.

### Nøglefunktioner:

- **Effektivitet og fleksibilitet:** CLI'en muliggør hurtig udførelse af kommandoer, hvilket øger produktiviteten.
- **Automatisering:** Understøtter scripting til at automatisere gentagne opgaver.
- **Fjernadgang:** Administrer ***digna***-ressourcer fra hvor som helst.
- **Konsistens og pålidelighed:** Sikrer pålidelige operationer med dokumenterede, versionskontrollerede kommandoer.
- **Skalerbarhed:** Håndterer operationer i stor skala til virksomhedens opgaver.
- **Læring og mestring:** Giver en dybere forståelse af funktionaliteten i ***digna***.
- **Integration med andre værktøjer:** Integreres problemfrit med automatiseringsværktøjer som Control-M, UC4 og AutomateNOW!

---

## Installationsvejledning til Windows

For at komme i gang, følg nedenstående trin for at udpakke de nødvendige filer, deployere `dignacli`-mappen og konfigurere din forbindelse til ***digna***-repositoryet. Sørg for at have dine repository-legitimationsoplysninger og eventuelle nødvendige konfigurationsdetaljer klar, inden du begynder.

1. **Udpakning af ***digna*** CLI:**
   - Hent `.zip`-filen, der indeholder ***digna*** CLI'en.
   - Udpak filen til den ønskede mappe.

2. **Deployering af `dignacli`-mappen:**
   - Kopiér `dignacli`-mappen til dit foretrukne installationssted (f.eks. `C:\Program Files\***digna***`).

3. **Konfigurering af `config.toml`:**
   - Kontrollér, om `config.toml` findes i `dignacli`.
   - Omdøb `config_template.toml` til `config.toml`, hvis nødvendigt, og konfigurer den ved hjælp af den medfølgende dokumentation.