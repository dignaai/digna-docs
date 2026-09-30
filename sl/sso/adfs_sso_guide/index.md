# Nastavite SSO z AD FS

Active Directory Federation Services je lokalna (on-premises) možnost: žetone izdajajo vaši lastni strežniki, discovery URL pa je vaše lastno ime gostitelja. AD FS podpira OpenID Connect od različice **Windows Server 2016** naprej.

Ta vodič zajema **AD FS stran**: ustvarjanje skupine aplikacij in zbiranje vrednosti, ki jih potrebuje digna. Digna stran — `dashboard_config.toml`, testiranje in odpravljanje težav — je enaka za vse ponudnike in je opisana v [Pregled Single Sign-On](overview.md).

---

## Preden začnete

| Zahteva | Opombe |
|---|---|
| **Različica AD FS** | Windows Server 2016 ali novejši — starejše različice ne podpirajo OIDC |
| **Dostop** | Lokalni skrbnik na strežniku AD FS |
| **Ime storitve federacije** | npr. `adfs.yourdomain.com` |
| **digna redirect URI** | URL, na katerega se uporabniki vrnejo po prijavi, npr. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. korak: Ustvarite skupino aplikacij

1. Na strežniku AD FS odprite **AD FS Management**
2. Z desno tipko miške kliknite **Application Groups** in izberite **Add Application Group**
3. Kot ime vnesite `digna`
4. Pod **Standalone applications** — ali **Client-Server applications**, odvisno od vaše različice — izberite **Server application accessing a web API**
5. Kliknite **Next**

---

## 2. korak: Konfigurirajte strežniško aplikacijo

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS ustvari GUID. Kopirajte ga — postane `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: vnesite svoj digna callback URL in kliknite **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Kliknite **Next**

!!! warning "Kliknite Add, ne samo Next"

    Polje za redirect URI ima svoj gumb **Add**. Če vnesete URI in kliknete **Next**, ne da bi pritisnili **Add**, se URI zavrže, čarovnik pa vas na to ne opozori. Preden nadaljujete, preverite, da se URI prikaže na seznamu pod poljem.

---

## 3. korak: Ustvarite deljeno skrivnost

1. Označite **Generate a shared secret**
2. Kopirajte ustvarjeno skrivnost → postane `DIGNA_OIDC_CLIENT_SECRET`
3. Kliknite **Next**

!!! warning "Skrivnost je prikazana samo enkrat"

    AD FS prikaže deljeno skrivnost samo na tej strani čarovnika in je ne more prikazati znova. Če jo izgubite, jo pozneje ponastavite v lastnostih skupine aplikacij.

---

## 4. korak: Konfigurirajte spletni API

1. **Identifier**: vnesite isti identifikator odjemalca iz 2. koraka in kliknite **Add**
2. Kliknite **Next**
3. Izberite **Access Control Policy** — *Permit everyone* je najpreprostejše izhodišče; za produkcijo dostop omejite na skupino
4. Kliknite **Next**

---

## 5. korak: Dodelite dovoljene obsege

V koraku **Configure Application Permissions** označite:

- `openid`
- `profile`
- `email`

Nato kliknite **Next** in dokončajte čarovnika.

!!! warning "openid ni privzeto označen"

    AD FS v nekaterih različicah vnaprej izbere samo `user_impersonation`. Brez `openid` končna točka za žetone vrne dostopni žeton OAuth namesto žetona ID, digna pa uporabnika ne more identificirati.

---

## 6. korak: Preverite končno točko discovery

Vstavite ime svoje storitve federacije:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Na primer:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Odprite ga v brskalniku. Dokument JSON potrjuje, da je OIDC omogočen in da je ime gostitelja pravilno.

!!! note "Zaledje mora zaupati certifikatu"

    Za AD FS je pogosta interna overitelj certifikatov (CA). Računalnik, na katerem teče digna zaledje, sam izvede odhodni klic HTTPS na ta URL, zato mora biti izdajateljski CA v shrambi zaupanja tega računalnika — ne le v brskalnikih ljudi, ki se prijavljajo.

---

## 7. korak: Konfigurirajte digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Login with Active Directory"
```

### `config.toml`

```toml
[oidc_clients.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

Vrednost `key` se mora v obeh datotekah ujemati — tukaj `adfs`.

---

## 8. korak: Testirajte

Znova zaženite zaledje in spletni strežnik, nato odprite nadzorno ploščo. Za celoten kontrolni seznam si oglejte [Testiranje prijave](overview.md#testing-login).

---

## Odpravljanje težav z AD FS

### MSIS9611: The Client Is Not Allowed to Access the Resource

Identifikator spletnega API-ja iz 4. koraka se ne ujema z identifikatorjem odjemalca ali pa obsegi iz 5. koraka niso bili dodeljeni. Oboje lahko uredite v lastnostih skupine aplikacij.

### MSIS9602: Invalid redirect_uri

URI je bil vnesen, ne pa dodan z gumbom **Add**, ali pa se razlikuje od `DIGNA_OIDC_REDIRECT_URI`. Preverite **Application Groups → digna → digna backend → Properties**.

### Žeton ID ni vrnjen

V dovoljenjih aplikacije manjka obseg `openid`.

### Zaledje ne doseže discovery URL-ja

Bodisi DNS na gostitelju zaledja ne razreši imena storitve federacije bodisi certifikatu AD FS tam ni zaupano. Preizkusite z `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` neposredno s strežnika digna.

### Dogodki, ki jih preverite

Strežnik AD FS beleži napake v **Applications and Services Logs → AD FS → Admin** v pregledovalniku dogodkov (Event Viewer), običajno z natančnejšim razlogom, kot ga prikaže brskalnik.

---

## Povezane vsebine

- [Pregled Single Sign-On](overview.md) — referenca konfiguracije, testiranje in splošno odpravljanje težav
- [Microsoft: AD FS OpenID Connect scenarios](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)