---
title: digna CLI atsauce – Ievads | digna dokumentācija
description: Ievads digna komandrindas saskarnē (CLI) — teksta rīks digna resursu automatizēšanai un pārvaldīšanai, tostarp instalēšanas pamati operētājsistēmā Windows.
keywords: digna cli, digna komandrinda, digna automatizācija, digna skriptēšana, cli atsauce, dignacli instalēšana
image: /assets/logo_square.png
---

## Komandu rindas interfeisa (CLI) mērķis

The ***digna*** Command Line Interface (CLI) ir jaudīgs rīks, kas izstrādāts, lai vienkāršotu mijiedarbību ar ***digna*** platformu. Tas nodrošina teksta saskarni, kas ļauj lietotājiem efektīvi veikt plašu uzdevumu spektru, bez nepieciešamības pēc grafiskas lietotāja saskarnes.

### Galvenās funkcijas:

- **Efektivitāte un elastība:** CLI nodrošina ātru komandu izpildi, uzlabojot produktivitāti.
- **Automatizācija:** Atbalsta skriptu izmantošanu, lai automatizētu atkārtojošos uzdevumus.
- **Attālā piekļuve:** Pārvaldiet ***digna*** resursus no jebkuras vietas.
- **Konsekvence un uzticamība:** Nodrošina uzticamu darbību ar dokumentētām, versiju kontrolētām komandām.
- **Mērogojamība:** Spēj apstrādāt plaša mēroga operācijas uzņēmuma vajadzībām.
- **Mācīšanās un pārvaldīšana:** Nodrošina dziļāku izpratni par ***digna*** funkcionalitāti.
- **Integrācija ar citiem rīkiem:** Vienmērīgi integrējas ar automatizācijas rīkiem, piemēram, Control-M, UC4, AutomateNOW!

---

## Windows instalācijas norādījumi

Lai sāktu, izpildiet tālāk norādītās darbības, lai izsaiņotu nepieciešamos failus, izvietotu *dignacli* mapi un konfigurētu savienojumu ar ***digna*** repozitoriju. Pirms sākat, pārliecinieties, ka jums ir repozitorija piekļuves dati un visi nepieciešamie konfigurācijas parametri.

1. **Izsaiņošana ***digna*** CLI:**
   - Iegūstiet `.zip` failu, kas satur ***digna*** CLI.
   - Atveriet arhīvu uz vēlamo direktoriju.

2. **`dignacli` mapes izvietošana:**
   - Kopējiet `dignacli` mapi uz izvēlēto instalācijas atrašanās vietu (piem., `C:\Program Files\***digna***`).

3. **`config.toml` konfigurēšana:**
   - Pārbaudiet, vai `dignacli` mapē ir `config.toml`.
   - Pārdēvējiet `config_template.toml` par `config.toml`, ja nepieciešams, un konfigurējiet to, izmantojot sniegto dokumentāciju.