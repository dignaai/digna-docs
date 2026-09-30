---
title: Pregled povezav z bazami podatkov – nastavitev ODBC brez DSN | digna Dokumentacija
description: Kako delujejo povezave z bazami podatkov v digna. Vsaka izvorna tehnologija je dosegljiva prek ODBC z nizom za povezavo brez DSN, sestavljenim iz lastnosti ODBC. Zajema namestitev gonilnika na gostitelja digna, zaslon Add DB Connection, šifriranje lastnosti, testiranje povezave, odpravljanje težav in povezave do vodičev za posamezne tehnologije.
image: /assets/logo_square.png
keywords:
  - digna povezava z bazo podatkov
  - odbc brez dsn
  - niz za povezavo odbc
  - nastavitev gonilnika odbc
  - unixodbc
  - lastnosti odbc
  - konfiguracija vira podatkov
lang: en
robots: index, follow
og_title: digna Database Connections – DSN-less ODBC Setup
og_description: Configure a digna source connection over ODBC without a DSN. Driver installation, ODBC properties, encryption, testing and troubleshooting.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Pregled povezav z bazami podatkov

---

## Vsebina

1. [Kako delujejo povezave](#how-connections-work)
2. [Vodiči za tehnologije](#technology-guides)
3. [Predpogoj: namestite gonilnik ODBC na gostitelja digna](#install-the-driver)
4. [Ustvarite povezavo z bazo podatkov](#create-a-database-connection)
5. [Lastnosti ODBC](#odbc-properties)
6. [Šifriranje vrednosti lastnosti](#encrypting-property-values)
7. [Testiranje povezave](#testing-a-connection)
8. [Katero bazo podatkov vidi povezava](#which-database-the-connection-sees)
9. [Način profiliranja in delovna shema](#profiling-mode-and-work-schema)
10. [Uporaba DSN](#using-a-dsn-instead)
11. [Odpravljanje težav](#troubleshooting)

---

## Kako delujejo povezave {: #how-connections-work }

*digna* dostopa do vsake izvorne tehnologije prek **ODBC**. Povezava je seznam lastnosti ODBC,
ki jih vnesete kot pare ključ/vrednost. Ko *digna* odpre povezavo, te pare združi v niz za
povezavo — `Key=Value`, ločeno z `;`, v vrstnem redu, v katerem ste jih navedli — in ga preda
upravitelju gonilnikov ODBC na gostitelju *digna*.

Ker lastnosti vnesete sami, je nastavitev **brez DSN** (DSN-less): povezava vsebuje vse, kar
gonilnik potrebuje, zato na gostitelju ni treba registrirati nobenega vira podatkov ODBC (DSN).
To je priporočen način konfiguracije *digna*, saj definicija povezave v celoti živi v *digna* in
se premika skupaj z njo.

### Zakaj ODBC {: #why-odbc }

Prejšnje različice so ponujale izbiro med gonilnikom za posamezno tehnologijo in ODBC, ki se je
izbirala s stikalom **Use ODBC**. Od Release 2026.06 *digna* temelji izključno na ODBC. En sam
standardni vmesnik vam ponuja več kot nabor namenskih gonilnikov:

- **Avtentikacija** — avtentikacija je del ODBC, zato lahko povezava uporablja karkoli, kar
  podpira njen gonilnik: gesla, žetone in PAT, Kerberos in Active Directory, MFA in enotno
  prijavo v brskalniku, oblačno identiteto, odjemalske certifikate in TLS. Nove metode pridejo s
  posodobitvijo gonilnika, namesto da bi čakali na izdajo *digna*.
- **Gonilniki, ki jih vzdržujejo proizvajalci baz podatkov** — proizvajalčev lastni gonilnik
  sledi novim različicam strežnika in varnostnim popravkom, posodobite pa ga lahko po lastnem
  urniku, neodvisno od *digna*.
- **En način za konfiguracijo vsega** — vsaka tehnologija je seznam lastnosti ključ/vrednost, z
  istim vmesnikom, istim šifriranjem občutljivih vrednosti in istim odpravljanjem težav, namesto
  različnega nabora polj za vsak vir.
- **Prilagajanje in doseg** — možnosti na ravni gonilnika, kot so časovne omejitve, nastavitve
  TLS, posredniški strežniki in velikosti pridobivanja (fetch size), so na voljo za vsak vir,
  povežete pa lahko katero koli tehnologijo z ustreznim gonilnikom ODBC, vključno s tistimi, za
  katere *digna* ne objavlja namenskega vodiča.

!!! note "Kaj se je spremenilo v vmesniku"

    Stikalo **Use ODBC** in ločena polja za gostitelja, vrata, bazo podatkov, uporabnika in
    geslo ne obstajajo več. Za povezavo, ki še ne uporablja ODBC, morate vnesti lastnosti ODBC,
    preden bo znova delovala — glejte
    [Ustvarite povezavo z bazo podatkov](#create-a-database-connection).

---

## Vodiči za tehnologije {: #technology-guides }

Imena lastnosti se razlikujejo glede na gonilnik, vsaka tehnologija pa ima eno ali dve
podrobnosti, ki jih druge nimajo. Spodnji vodiči zajemajo ta del; ta stran zajema stran *digna*,
ki je enaka za vse.

!!! important "Nabori lastnosti v vodičih so primeri"

    Vsak vodič prikazuje eno kombinacijo, za katero je znano, da deluje — tisto, s katero je
    *digna* testirana. To je izhodišče, ne specifikacija: lastnosti pripadajo gonilniku ODBC,
    katere obstajajo, kako se imenujejo in katere vrednosti sprejemajo, pa se razlikuje med
    različicami gonilnikov in proizvajalci, med Windows, Linux in macOS ter glede na to, kako je
    konfiguriran izvorni strežnik — metoda avtentikacije, TLS, prehod, vrata. Pričakujte, da
    boste morali prilagoditi vrednost ali dve, za merodajno pa štejte dokumentacijo različice
    gonilnika, ki ste jo namestili.

| Tehnologija | Vodič | Dobro je vedeti |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Serverless bazeni potrebujejo `-ondemand` v imenu gostitelja in podpirajo samo profiliranje *Standard* |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Avtentikacija z žetonom: `UID=token`, PAT v `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Katalogi prihajajo iz gonilnika, ne iz poizvedbe |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Ime gonilnika je v zavitih oklepajih: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` sprejme celoten opisnik povezave (connect descriptor) ali vzdevek iz `tnsnames.ora` |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` se mora ujemati s tem, kar zahteva strežnik |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Programmatic access token je testirana pot avtentikacije |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` določa, katere sheme vidi *digna* |
| **Teradata** | [Teradata](teradata_connector_guide.md) | Gostitelj gre v `DBCNAME`; baze podatkov delujejo kot sheme |

---

## Predpogoj: namestite gonilnik ODBC na gostitelja digna {: #install-the-driver }

*digna* odpira povezave z viri s **strežnika, na katerem teče zaledje digna**, ne iz brskalnika.
Gonilnik ODBC mora biti zato nameščen na tem računalniku, njegovo ime pa registrirano pri
lokalnem upravitelju gonilnikov.

=== "Windows"

    Namestite proizvajalčev 64-bitni gonilnik, nato odprite **ODBC Data Source Administrator
    (64-bit)** in preklopite na zavihek **Drivers**. Tam navedena imena so natanko vrednosti,
    ki jih lahko uporabite za lastnost `Driver`.

=== "Linux"

    Namestite **unixODBC** in proizvajalčev gonilnik, nato izpišite registrirana imena
    gonilnikov:

    ```bash
    odbcinst -q -d
    ```

    Imena, izpisana v oglatih oklepajih, so vrednosti, ki jih lahko uporabite za lastnost
    `Driver`. Prihajajo iz `/etc/odbcinst.ini` (ali iz datoteke, ki jo navede `odbcinst -j`).

=== "macOS"

    Namestite **unixODBC** (na primer z `brew install unixodbc`) in proizvajalčev gonilnik,
    nato izpišite registrirana imena gonilnikov:

    ```bash
    odbcinst -q -d
    ```

!!! warning "Ime gonilnika se mora ujemati znak za znakom"

    `Driver` se upravitelju gonilnikov preda nespremenjen. `Simba Spark ODBC Driver` in
    `Simba Spark ODBC Driver 64` sta za upravitelja gonilnikov različna gonilnika, ime, ki ni
    registrirano, pa povzroči napako *data source name not found*, čeprav DSN sploh ni
    vpleten.

Namesto registriranega imena vsi običajni upravitelji gonilnikov sprejmejo tudi celotno pot do
knjižnice gonilnika, na primer `Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. To je
uporabno, kadar je gonilnik nameščen, ni pa registriran.

---

## Ustvarite povezavo z bazo podatkov {: #create-a-database-connection }

Odprite **Admin Panel**, pojdite na zavihek **Database Connections** in kliknite
**Add DB Connection**. Zaslon zahteva pet podatkov:

| Polje | Opis |
|---|---|
| **Name** | Ime povezave. Uporablja se za sklicevanje na povezavo na drugih zaslonih. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake ali Hive. Določa narečje SQL, ki ga ustvarja *digna*, zato se mora ujemati z virom — ne z gonilnikom. Azure Synapse Analytics je povezava **SQL Server**. |
| **ODBC Properties** | Pari ključ/vrednost, opisani v [Lastnosti ODBC](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* ali *Session* — glejte [Način profiliranja in delovna shema](#profiling-mode-and-work-schema). |
| **Work Schema** | Shema, ki vsebuje delovne tabele za profiliranje *Permanent*. |

Povezava se upravlja centralno in se nato dodeli enemu ali več projektom, tako da lahko ista
povezava služi več projektom.

---

## Lastnosti ODBC {: #odbc-properties }

Za vsako lastnost kliknite **Add Property** in izpolnite **Key**, **Value** ter za skrivnosti
potrditveno polje **Encrypted**. Vsak vodič za tehnologijo navaja primer nabora za to
tehnologijo, ki ga prilagodite svoji različici gonilnika in strežniku — glejte
[opombo zgoraj](#technology-guides).

Ne glede na gonilnik nabor lastnosti zajema iste štiri stvari:

- **`Driver`** — registrirano ime gonilnika, kot je opisano [zgoraj](#install-the-driver).
- **Naslov strežnika** — ključ se razlikuje glede na gonilnik: `SERVER`, `HOST`, `DBCNAME`,
  `Server` ali, pri Oracle, opisnik povezave `DBQ`.
- **Poverilnice** — običajno `UID` in `PWD`; Snowflake uporablja `UID` in `token`,
  Databricks pa dobesednega uporabnika `token` in osebni dostopni žeton v `PWD`.
- **Baza podatkov ali katalog, v katerem se dela**, kjer ga tehnologija ima — glejte
  [Katero bazo podatkov vidi povezava](#which-database-the-connection-sees).

Vse drugo, kar dokumentira gonilnik, lahko dodate na enak način — združevanje povezav
(connection pooling), časovne omejitve vtičnic, nastavitve Kerberos, nastavitve posredniškega
strežnika. *digna* lastnosti ne tolmači; samo posreduje jih naprej.

!!! warning "Vrednosti se ne ubežijo — vse s podpičjem zavijte v zavite oklepaje"

    Ker so lastnosti združene z `;`, bi vrednost, ki sama vsebuje `;`, razdelila niz za
    povezavo na napačnem mestu. Takšne vrednosti zavijte v zavite oklepaje: `PWD={p@ss;word}`.
    Enako velja za vrednosti z `=` ali presledki na začetku. Zato se nekateri gonilniki po
    ustaljeni praksi pišejo v zavitih oklepajih, kot npr. `{NetezzaSQL}` ali
    `{SnowflakeDSIIDriver}`.

---

## Šifriranje vrednosti lastnosti {: #encrypting-property-values }

Označite **Encrypted** za vsako lastnost, ki vsebuje skrivnost — `PWD`, `token`, skrivnost
odjemalca. Vrednost se nato šifrira, preden se shrani v repozitorij *digna*, na zaslonu je
zakrita, dešifrira pa se šele, ko se sestavi niz za povezavo.

!!! tip "Nasvet"

    Šifrirane vrednosti ni mogoče znova prebrati, niti v uporabniškem vmesniku niti prek API —
    mogoče jo je samo zamenjati. Skrivnosti hranite tudi v svojem upravitelju gesel.

Lastnosti, ki niso skrivne — ime gonilnika, gostitelj, vrata, baza podatkov — je najbolje
pustiti nešifrirane, da ostanejo berljive za tistega, ki bo povezavo pozneje vzdrževal.

---

## Testiranje povezave {: #testing-a-connection }

V pogovornem oknu *Add DB Connection* kliknite **Test**, **preden** shranite. Test uporabi
vrednosti, ki so trenutno v obrazcu, in izvede dejansko povezavo, zato poroča natanko to, na
kar bi naletela inšpekcija — napačno ime gonilnika, zavrnjeno geslo, nedosegljivega gostitelja.
Nič se ne shrani: testna povezava se razveljavi (rollback), ne glede na to, ali uspe ali ne.

Za povezavo, ki že obstaja, se na zavihku **Database Connections** z miško postavite nad njeno
vrstico in kliknite ikono **vtiča**, da jo znova testirate. To je najhitrejši način, da
preverite, ali je vir dosegljiv po menjavi gesla ali spremembi požarnega zidu.

---

## Katero bazo podatkov vidi povezava {: #which-database-the-connection-sees }

Ko dodate vir podatkov, *digna* ponudi kataloge, sheme in tabele, ki jih povezava doseže. Kako
daleč to seže, je odvisno od tehnologije:

| Tehnologija | Ponujeni katalogi |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Samo **trenutna** baza podatkov povezave |
| **Teradata**, **Netezza**, **Databricks** | Vse baze podatkov ali katalogi, ki jih uporabnik sme videti |
| **Hive**, **Impala** | Sporoči jih gonilnik |

!!! important "Ena povezava, ena baza podatkov"

    Pri PostgreSQL, SQL Server, Oracle in Snowflake morajo lastnosti kazati na bazo podatkov, ki
    vsebuje izvorne sheme — `DATABASE=…`, `Database=…` ali ime storitve v Oraclovem `DBQ`.
    Tabele v drugi bazi podatkov prek te povezave niso dosegljive; zanjo dodajte drugo
    povezavo.

---

## Način profiliranja in delovna shema {: #profiling-mode-and-work-schema }

Način profiliranja določa, kako *digna* obdeluje podatke in izračunava metrike:

- **Standard:** Metrike se izračunajo neposredno na izvornih tabelah, brez kopiranja podatkov.
- **Permanent:** Podatki za pregledovani dan se kopirajo v trajno tabelo, metrike pa se
  izračunajo na kopiranih podatkih.
- **Session:** Podatki se kopirajo v sejno ali začasno tabelo, metrike pa se izračunajo na teh
  začasnih podatkih.

Način določa, kaj mora uporabnik povezave smeti početi:

| Način | Zapisuje | Pravice, ki jih potrebuje uporabnik povezave |
|---|---|---|
| **Standard** | nič | Branje izvornih tabel |
| **Permanent** | tabelo za vsak vir podatkov v **Work Schema** | Ustvarjanje in brisanje tabel v **Work Schema** |
| **Session** | začasno tabelo, ki jo baza podatkov izbriše skupaj s sejo | Ustvarjanje začasnih tabel — **Work Schema** se ne uporablja |

*Standard* samo bere, zato je to način, ki ga izberete, kadar ima *digna* dostop samo za
branje. **Work Schema** se bere samo pri *Permanent*, vendar jo je vseeno vredno izpolniti, da
povezava deluje naprej, če se način pozneje spremeni.

---

## Uporaba DSN {: #using-a-dsn-instead }

DSN še vedno deluje — `DSN` je le še ena lastnost:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

DSN mora biti registriran na gostitelju *digna*, za isti uporabniški račun, pod katerim teče
zaledje *digna*, in kot **System DSN**, kadar *digna* teče kot storitev. Vse, kar je
konfigurirano v DSN, lahko preglasite tako, da to dodate tudi kot lastnost.

Brez DSN je dokumentirana privzeta možnost, ker se izogne temu stanju na strani gostitelja:
povezava je v celoti opisana v *digna*, nov gostitelj *digna* pa potrebuje nameščen gonilnik,
konfigurirati pa ni treba ničesar.

---

## Odpravljanje težav {: #troubleshooting }

### Data source name not found / no default driver specified

**Simptomi:**
- Gumb **Test** sporoči napako, ki omenja *data source name not found*, čeprav je nastavitev
  brez DSN

**Vzroki in rešitve:**
1. Vrednost `Driver` se ne ujema z imenom registriranega gonilnika — primerjajte jo z zavihkom
   **Drivers** v *ODBC Data Source Administrator (64-bit)* ali z `odbcinst -q -d`
2. Gonilnik je nameščen na vaši delovni postaji, ne pa na gostitelju *digna*
3. Gonilnik je 32-bitni, *digna* pa je 64-bitna — namestite 64-bitni gonilnik
4. Lastnost `Driver` v celoti manjka, prav tako ni bil podan `DSN`
5. Na Linux in macOS je gonilnik nameščen, ni pa registriran — namesto tega navedite celotno
   pot do knjižnice gonilnika ali ga registrirajte v `odbcinst.ini`

---

### Test povezave poteče

**Simptomi:**
- **Test** obvisi in nato po približno pol minute ne uspe

**Vzroki in rešitve:**
1. Gostitelj ali vrata niso dosegljivi z gostitelja *digna* — preverite požarni zid in pri
   oblačnih virih seznam dovoljenih naslovov IP
2. Ime gostitelja je pravilno, vrata pa pripadajo drugi storitvi
3. Vir potrebuje več kot privzetih 30 sekund, da sprejme povezavo — povečajte
   `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` v razdelku `[base]` datoteke `config.toml` (`0` čaka
   neomejeno) in znova zaženite zaledje
4. Serverless končna točka se prebuja iz mirovanja — poskusite znova, in če se to redno
   dogaja, povečajte časovno omejitev prijave, kot je opisano zgoraj

---

### Avtentikacija ne uspe, čeprav so poverilnice pravilne

**Simptomi:**
- Gonilnik sporoči neveljavne poverilnice, isti uporabnik pa deluje v drugem odjemalcu SQL

**Vzroki in rešitve:**
1. Geslo vsebuje `;` — vrednost zavijte v zavite oklepaje: `{p@ss;word}`
2. V vrednost je bil skopiran presledek na koncu
3. Gonilnik pričakuje določen mehanizem avtentikacije — na primer `AuthMech` za gonilnika
   Hive in Databricks ali `authenticator` za Snowflake
4. Vrednost je bila shranjena šifrirano in nato urejena — šifriranih vrednosti ni mogoče znova
   prebrati, zato skrivnost znova vnesite v celoti
5. Žeton je potekel — osebni dostopni žetoni in programmatic access tokens se izdajajo z
   datumom poteka

---

### Zaslon za vir podatkov ne ponudi pričakovane baze podatkov ali sheme

**Simptomi:**
- Ko dodajate vir podatkov, manjkajo katalogi, sheme ali tabele

**Vzroki in rešitve:**
1. Povezava kaže na drugo bazo podatkov — glejte
   [Katero bazo podatkov vidi povezava](#which-database-the-connection-sees)
2. Uporabnik povezave nima pravic za branje sheme ali podatkovnega slovarja
3. **Technology** se ne ujema z virom, zato *digna* poizveduje po napačnem podatkovnem
   slovarju
4. Pri Snowflake uporabniku ni dodeljeno privzeto skladišče (warehouse) in lastnost
   `Warehouse` ni bila podana, zato poizvedb po metapodatkih ni mogoče izvesti

---

### Profiliranje ne uspe, čeprav test povezave uspe

**Simptomi:**
- **Test** uspe, inšpekcija pa ne uspe pri ustvarjanju delovnih tabel

**Vzroki in rešitve:**
1. Izbrano je profiliranje *Permanent*, uporabnik povezave pa ne more ustvarjati tabel v
   **Work Schema** — dodelite pravice ali preklopite na *Session* ali *Standard*
2. **Work Schema** je prazna ali navaja shemo, ki ne obstaja, izbrano pa je profiliranje
   *Permanent*
3. Izbrano je profiliranje *Session*, uporabnik povezave pa ne sme ustvarjati začasnih tabel
4. Dolgotrajna poizvedba profiliranja doseže časovno omejitev poizvedbe — povečajte
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` v razdelku `[base]` datoteke `config.toml` (privzeto 3600
   sekund, `0` onemogoči časovno omejitev)

---

## Priporočene prakse

**NAREDITE:**

- Namestite in registrirajte gonilnik na gostitelju *digna*, preden konfigurirate povezavo
- Označite **Encrypted** za vsako geslo in žeton
- Pred shranjevanjem kliknite **Test** in po menjavi gesla povezavo znova testirajte
- Povezave poimenujte po viru in okolju, na primer `sales_dwh_prod`
- *digna* dodelite namenskega uporabnika baze podatkov, samo za branje, kjer zadošča
  profiliranje *Standard*
- Za vsako izvorno bazo podatkov imejte eno povezavo in raje dodajte drugo, kot da bi prvo
  preklapljali

**NE:**

- Ne shranjujte skrivnosti nešifriranih in ne delite enega uporabnika baze podatkov med *digna*
  in drugimi orodji
- Ne uporabljajte 32-bitnega gonilnika s 64-bitno namestitvijo *digna*
- Ne zanašajte se na User DSN, kadar *digna* teče kot storitev — ne bo viden
- Ne vnašajte vrednosti, ki vsebuje `;`, v lastnost brez zavitih oklepajev
- Ne usmerite **Work Schema** na shemo, ki vsebuje izvorne podatke

---

## Podpora

Potrebujete pomoč pri povezavi z bazo podatkov?

- **E-pošta:** support@digna.ai
- **Dokumentacija:** https://docs.digna.ai
- **Spletna stran:** https://www.digna.ai

---

**Izdaja:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
