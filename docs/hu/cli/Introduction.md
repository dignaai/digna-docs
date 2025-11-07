## A parancssori felület (CLI) célja

A ***digna*** parancssori felülete (CLI) egy erőteljes eszköz, amelyet az ***digna*** platformal való interakciók egyszerűsítésére terveztek. Szöveges felületet biztosít, amely lehetővé teszi a felhasználók számára, hogy grafikus felület nélkül hatékonyan végezzenek el széles körű feladatokat.

### Fő jellemzők:

- **Hatékonyság és rugalmasság:** A CLI lehetővé teszi a parancsok gyors végrehajtását, növelve a termelékenységet.
- **Automatizálás:** Támogatja a szkriptelést az ismétlődő feladatok automatizálásához.
- **Távoli hozzáférés:** Kezelje az ***digna*** erőforrásokat bárhonnan.
- **Konzisztencia és megbízhatóság:** Dokumentált, verziókövetett parancsokkal biztosít megbízható működést.
- **Skálázhatóság:** Nagy volumenű műveletek kezelésére alkalmas vállalati feladatokhoz.
- **Tanulás és szakértelem:** Mélyebb megértést nyújt az ***digna*** funkcionalitásáról.
- **Integráció más eszközökkel:** Zökkenőmentesen integrálható olyan automatizáló eszközökkel, mint a Control-M, UC4, AutomateNOW!

---

## Telepítési útmutató Windows rendszeren

A kezdéshez kövesse az alábbi lépéseket a szükséges fájlok kicsomagolásához, a *dignacli* mappa telepítéséhez és az ***digna*** repository-hoz való kapcsolódás konfigurálásához. Győződjön meg róla, hogy rendelkezik a repository hitelesítő adataival és minden szükséges konfigurációs információval, mielőtt elkezdi.

1. **A ***digna*** CLI kicsomagolása:**
   - Szerezze be a `.zip` fájlt, amely az ***digna*** CLI-t tartalmazza.
   - Csomagolja ki a fájlt a kívánt könyvtárba.

2. **A `dignacli` mappa telepítése:**
   - Másolja a `dignacli` mappát a kívánt telepítési helyre (pl. `C:\Program Files\***digna***`).

3. **A `config.toml` konfigurálása:**
   - Ellenőrizze, hogy a `dignacli` mappában megtalálható-e a `config.toml`.
   - Ha szükséges, nevezze át a `config_template.toml` fájlt `config.toml`-ra, és konfigurálja a mellékelt dokumentáció szerint.