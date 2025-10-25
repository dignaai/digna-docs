## A parancssori felület (CLI) célja

A ***digna*** parancssori felülete (CLI) egy erőteljes eszköz, amelyet az ***digna*** platformmal való interakciók hatékonyabbá tételére fejlesztettek. Szöveges felületet biztosít, amely lehetővé teszi a felhasználók számára, hogy grafikus felhasználói felület nélkül is széles körű feladatokat hajtsanak végre hatékonyan.

### Főbb jellemzők:

- **Hatékonyság és rugalmasság:** A CLI gyors parancsvégrehajtást tesz lehetővé és növeli a termelékenységet.
- **Automatizálás:** Támogatja a szkriptek használatát az ismétlődő feladatok automatizálásához.
- **Távoli hozzáférés:** Kezelje az ***digna*** erőforrásokat bárhonnan.
- **Konzisztencia és megbízhatóság:** Megbízható műveleteket biztosít dokumentált, verziókövetett parancsokkal.
- **Skálázhatóság:** Nagyméretű műveletek kezelésére alkalmas vállalati feladatokhoz.
- **Tanulás és jártasság:** Mélyebb megértést ad az ***digna*** funkcionalitásáról.
- **Integráció más eszközökkel:** Zökkenőmentesen integrálódik olyan automatizálási eszközökkel, mint a Control-M, UC4, AutomateNOW!

---

## Telepítési útmutató Windows rendszeren

A kezdéshez kövesse az alábbi lépéseket a szükséges fájlok kicsomagolásához, a *dignacli* mappa elhelyezéséhez és az ***digna*** repository-hoz való csatlakozás konfigurálásához. Győződjön meg róla, hogy rendelkezik a repository bejelentkezési adataival és az esetlegesen szükséges konfigurációs részletekkel, mielőtt elkezdi.

1. *****digna*** CLI kicsomagolása:**
   - Töltse le a `.zip` fájlt, amely az ***digna*** CLI-t tartalmazza.
   - Csomagolja ki a fájlt a kívánt könyvtárba.

2. **`dignacli`-mappa elhelyezése:**
   - Másolja a `dignacli` mappát a kívánt telepítési helyre (f. e. `C:\Program Files\***digna***`).

3. **`config.toml` konfigurálása:**
   - Ellenőrizze, hogy a `config.toml` megtalálható-e a `dignacli` mappában.
   - Szükség esetén nevezze át a `config_template.toml` fájlt `config.toml`-ra, majd konfigurálja azt a mellékelt dokumentációnak megfelelően.