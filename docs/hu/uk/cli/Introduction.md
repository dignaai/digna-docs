## A parancssori felület (CLI) célja

A parancssori felület (CLI) ***digna*** egy erőteljes eszköz, amely a ***digna*** platformmal való interakció optimalizálására készült. Szöveges felületet biztosít, amely lehetővé teszi a felhasználók számára, hogy széles körű feladatokat hatékonyan hajtsanak végre grafikus felhasználói felület nélkül.

### Főbb funkciók:

- **Hatékonyság és rugalmasság:** A CLI lehetővé teszi a parancsok gyors végrehajtását, növelve a termelékenységet.
- **Automatizálás:** Támogatja a szkriptezést az ismétlődő feladatok automatizálásához.
- **Távoli elérés:** Kezelje a ***digna*** erőforrásait bárhonnan.
- **Következetesség és megbízhatóság:** Dokumentált, verziókövetett parancsokkal biztosít megbízható működést.
- **Skálázhatóság:** Támogatja a vállalati szintű műveleteket.
- **Tanulás és elsajátítás:** Mélyebb betekintést nyújt a ***digna*** funkcionalitásába.
- **Integráció más eszközökkel:** Zökkenőmentesen integrálódik olyan automatizálási eszközökkel, mint a Control-M, UC4, AutomateNOW!

---

## Telepítési útmutató Windows rendszeren

A kezdéshez végezze el az alábbi lépéseket a szükséges fájlok kicsomagolásához, a *dignacli* mappa telepítéséhez és a kapcsolat beállításához a ***digna*** tárolóval. Győződjön meg róla, hogy rendelkezik a tároló hitelesítő adataival és minden szükséges konfigurációs részlettel a kezdés előtt.

1. **A ***digna*** CLI kicsomagolása:**
   - Szerezze be a `.zip` fájlt, amely a ***digna*** CLI-t tartalmazza.
   - Csomagolja ki a fájlt a kívánt mappába.

2. **A `dignacli` mappa telepítése:**
   - Másolja a `dignacli` mappát a kívánt telepítési helyre (például `C:\Program Files\***digna***`).

3. **A `config.toml` beállítása:**
   - Ellenőrizze, hogy a `config.toml` megtalálható-e a `dignacli` mappában.
   - Szükség esetén nevezze át a `config_template.toml` fájlt `config.toml`-ra, és állítsa be a mellékelt dokumentációnak megfelelően.