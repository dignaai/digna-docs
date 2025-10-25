## A parancssori felület (CLI) célja

***digna*** parancssori felülete (CLI) erőteljes eszköz, amely a ***digna*** platformmal való interakciók egyszerűsítésére készült. Grafikus felhasználói felület nélkül lehetővé teszi, hogy a felhasználók szöveges felületen keresztül hatékonyan végezzenek el széles körű feladatokat.

### Főbb jellemzők:

- **Hatékonyság és rugalmasság:** A CLI gyors parancsvégrehajtást tesz lehetővé, növelve a termelékenységet.
- **Automatizálás:** Támogatja az ismétlődő feladatok automatizálását szkripteléssel.
- **Távoli elérés:** Kezelje a ***digna*** erőforrásokat bárhonnan.
- **Következetesség és megbízhatóság:** Dokumentált, verziókezelés alatt álló parancsokkal megbízható műveleteket biztosít.
- **Skálázhatóság:** Nagy volumenű vállalati feladatok kezelésére alkalmas.
- **Tanulás és szakosodás:** Lehetővé teszi a ***digna*** funkcionalitásának mélyebb megismerését.
- **Integráció más eszközökkel:** Zökkenőmentes integrációt biztosít automatizációs eszközökkel, mint a Control-M, UC4 és AutomateNOW!.

---

## Telepítési utasítások Windowshoz

A kezdéshez csomagolja ki a szükséges fájlokat, helyezze el a *dignacli* mappát, és konfigurálja a ***digna*** repository kapcsolatát az alábbi lépések szerint. A megkezdés előtt tartsa kéznél a repository hitelesítési adatait és a szükséges konfigurációs részleteket.

1. **`***digna*** CLI` kicsomagolása:**
   - Szerezze be a ***digna*** CLI-t tartalmazó `.zip` fájlt.
   - Csomagolja ki a fájlt a kívánt könyvtárba.

2. **`dignacli` mappa elhelyezése:**
   - Másolja a `dignacli` mappát a kívánt telepítési helyre (pl. `C:\Program Files\***digna***`).

3. **`config.toml` konfigurálása:**
   - Ellenőrizze, hogy a `dignacli` könyvtárban található-e `config.toml` fájl.
   - Ha szükséges, nevezze át a `config_template.toml` fájlt `config.toml`-ra, és konfigurálja a mellékelt dokumentáció szerint.