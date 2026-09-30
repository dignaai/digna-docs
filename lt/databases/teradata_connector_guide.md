# Teradata šaltinio jungtis

Šiame vadove aprašyta, kaip sukonfigūruoti *digna* prisijungimą prie Teradata per **ODBC**,
naudojant ryšio eilutę **be DSN** (DSN-less).

*digna* pusės nustatymas yra vienodas visoms technologijoms — kur kuriami ryšiai, kaip
šifruojamos savybių reikšmės, kaip testuojamas ryšys ir ką reiškia profiliavimo režimai. Tai
aprašyta [Duomenų bazių ryšių apžvalgoje](overview.md). Šiame puslapyje aprašoma tai, kas būdinga
Teradata.

---

## 1. Įdiekite ODBC tvarkyklę {: #1-install-the-odbc-driver }

Įdiekite **ODBC Driver for Teradata** kompiuteryje, kuriame veikia *digna* backend, laikydamiesi
oficialaus gamintojo diegimo vadovo.

Tvarkyklė užsiregistruoja su versija pavadinime, pavyzdžiui,
**Teradata Database ODBC Driver 20.00**. Nuskaitykite tikslų užregistruotą pavadinimą savo
serveryje, kaip aprašyta skyriuje [ODBC tvarkyklės diegimas digna serveryje](overview.md#install-the-driver).

---

## 2. ODBC savybės {: #2-odbc-properties }

!!! important "Pavyzdys, o ne specifikacija"

    Toliau pateiktas rinkinys yra vienas žinomai veikiantis derinys. Savybės priklauso
    Teradata ODBC tvarkyklei, todėl jų pavadinimai, numatytosios reikšmės ir priimamos reikšmės
    skiriasi tarp tvarkyklės versijų — versija yra paties tvarkyklės pavadinimo dalis — ir tarp
    platformų. Naudokite tai kaip atspirties tašką ir patikrinkite įdiegtos tvarkyklės versijos
    dokumentaciją.

Ekrane **Add DB Connection** pridėkite šias savybes:

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Turi sutapti su tvarkyklės pavadinimu, užregistruotu *digna* serveryje |
| `DBCNAME` | `teradata.example.com` | Serverio pavadinimas arba IP adresas. Taip Teradata vadina serverio savybę |
| `UID` | `digna_source_user` | Duomenų bazės vartotojas |
| `PWD` | `<password>` | Pažymėkite **Encrypted** |

Gauta ryšio eilutė atrodo taip:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Naudingos papildomos savybės:

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `MechanismName` | `TD2` | Prisijungimo mechanizmas. `TD2` yra Teradata numatytasis; katalogo tarnybos (directory) autentifikacijai naudokite `LDAP` |
| `DefaultDatabase` | `dad` | Duomenų bazė, kurioje pradedamas seansas |
| `CharacterSet` | `UTF8` | Nustatykite, kai numatytasis seanso simbolių rinkinys sugadintų ne ASCII duomenis |

---

## 3. *digna* konfigūracija {: #3-digna-configuration }

Ekrane **Add DB Connection** nurodykite:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Pastabos apie Teradata {: #4-notes-on-teradata }

- **Teradata duomenų bazė yra katalogas, o ne schema.** *digna* duomenų bazes, kurias vartotojas
  gali matyti (iš `DBC.DatabasesV`), išvardija kaip katalogus, o schemos lygmuo netaikomas.
  Pridėdami duomenų šaltinį, pasirinkite duomenų bazę kaip katalogą; schema pažymima kaip
  *netaikoma* (not applicable).
- **Vienas ryšys pasiekia kiekvieną leidžiamą duomenų bazę**, todėl vienas ryšys gali aptarnauti
  šaltinius keliose duomenų bazėse — skirtingai nei technologijose, kuriose ryšys susietas su
  viena duomenų baze.
- **Work Schema yra duomenų bazė.** *Permanent* profiliavimui nurodykite Teradata duomenų bazę,
  kurioje laikomos darbinės lentelės, ir suteikite vartotojui teisę `CREATE TABLE` bei `PERM`
  vietos skyrimą joje — duomenų bazė su nuline perm vieta negali turėti lentelės.
- **Profiliavimo režimai.** *Permanent* kuria lenteles schemoje **Work Schema**. *Session*
  naudoja `VOLATILE` lentelę, kuriai reikia `SPOOL` vietos, bet nereikia perm vietos ir teisių
  **Work Schema**. *Standard* reikia tik skaitymo prieigos.

---

## 5. Tvarkyklės patikrinimas (neprivaloma) {: #5-verifying-the-driver-optional }

Ryšiui be DSN ODBC duomenų šaltinio konfigūruoti nereikia, tačiau pačios tvarkyklės dialogo
langas yra patogus būdas patvirtinti, kad tvarkyklė ir jūsų prisijungimo duomenys veikia, prieš
įvedant juos į *digna*.

#### 1 žingsnis
![1 žingsnis](images/teradata/create_odbc_data_source_step1.png)

Čia esantis laukas **Name or IP address** atitinka savybę `DBCNAME` iš
[2 skyriaus](#2-odbc-properties).

Spustelėkite mygtuką **Test**.

#### 2 žingsnis
![2 žingsnis](images/teradata/create_odbc_data_source_step2.png)

Įveskite vartotojo vardą ir slaptažodį, tada spustelėkite mygtuką **OK**. Sėkmės ekranas
patvirtina, kad tvarkyklė ir prisijungimo duomenys veikia.