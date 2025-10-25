## A parancssori felület (CLI) célja

A ***digna*** Command Line Interface (CLI) egy hatékony eszköz, amely az interakciók egyszerűsítésére szolgál a ***digna*** platformmal. Szövegalapú felületet biztosít, amely lehetővé teszi a felhasználók számára, hogy grafikus felület nélkül hatékonyan végezzenek el számos feladatot.

### Főbb jellemzők:

- **Hatékonyság és rugalmasság:** A CLI gyors parancsvégrehajtást tesz lehetővé, növelve a produktivitást.
- **Automatizálás:** Támogatja a scripteket az ismétlődő feladatok automatizálásához.
- **Távoli elérés:** Kezelje a ***digna*** erőforrásokat bárhonnan.
- **Következetesség és megbízhatóság:** Dokumentált, verziókövetett parancsokkal biztosít megbízható működést.
- **Skálázhatóság:** Nagy léptékű műveletek kezelésére alkalmas vállalati feladatokhoz.
- **Tanulás és elsajátítás:** Mélyebb megértést nyújt a ***digna*** funkcióiról.
- **Más eszközökkel való integráció:** Zökkenőmentesen integrálható automatizálási eszközökkel, mint a Control-M, UC4, AutomateNOW!

---

## Telepítési útmutató Windowshoz

A kezdethez kövesse az alábbi lépéseket a szükséges fájlok kicsomagolásához, a *dignacli* mappa telepítéséhez és a kapcsolódás konfigurálásához a ***digna*** repository-hoz. Győződjön meg róla, hogy rendelkezik a repository hitelesítő adataival és minden szükséges konfigurációs információval, mielőtt nekiáll.

1. **A ***digna*** CLI kicsomagolása:**
   - Szerezze be a `.zip` fájlt, amely az ***digna*** CLI-t tartalmazza.
   - Csomagolja ki a fájlt a kívánt könyvtárba.

2. **A `dignacli` mappa telepítése:**
   - Másolja a `dignacli` mappát a kívánt telepítési helyre (pl. `C:\Program Files\***digna***`).

3. **A `config.toml` konfigurálása:**
   - Ellenőrizze, hogy a `dignacli` mappában található-e `config.toml`.
   - Ha szükséges, nevezze át a `config_template.toml` fájlt `config.toml`-ra, és konfigurálja a mellékelt dokumentáció szerint.