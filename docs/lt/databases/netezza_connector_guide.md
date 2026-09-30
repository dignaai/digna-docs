---
title: Netezza jungtis – duomenų bazės integracija | digna dokumentacija
description: Sukonfigūruokite digna prisijungimą prie Netezza per ODBC naudojant ryšio eilutę be DSN. Apima NetezzaSQL tvarkyklę, reikalingas ODBC savybes ir digna pusės ryšio nustatymus.
image: /assets/logo_square.png
---


# Netezza šaltinio jungtis

Šiame vadove aprašyta, kaip sukonfigūruoti *digna* prisijungimą prie Netezza per **ODBC**,
naudojant ryšio eilutę **be DSN** (DSN-less).

*digna* pusės nustatymas yra vienodas visoms technologijoms — kur kuriami ryšiai, kaip
šifruojamos savybių reikšmės, kaip testuojamas ryšys ir ką reiškia profiliavimo režimai. Tai
aprašyta [Duomenų bazių ryšių apžvalgoje](overview.md). Šiame puslapyje aprašoma tai, kas būdinga
Netezza.

---

## 1. Įdiekite ODBC tvarkyklę {: #1-install-the-odbc-driver }

Įdiekite **NetezzaSQL** ODBC tvarkyklę (IBM Netezza kliento įrankių dalį) kompiuteryje, kuriame
veikia *digna* backend, laikydamiesi oficialaus gamintojo diegimo vadovo.

Nuskaitykite tikslų užregistruotos tvarkyklės pavadinimą savo serveryje, kaip aprašyta skyriuje
[ODBC tvarkyklės diegimas digna serveryje](overview.md#install-the-driver).

---

## 2. ODBC savybės {: #2-odbc-properties }

!!! important "Pavyzdys, o ne specifikacija"

    Toliau pateiktas rinkinys yra vienas žinomai veikiantis derinys. Savybės priklauso
    NetezzaSQL tvarkyklei, todėl jų pavadinimai, numatytosios reikšmės ir priimamos reikšmės
    skiriasi tarp kliento versijų ir platformų, o TLS apsaugotam įrenginiui (appliance) reikia
    daugiau savybių nei čia parodyta. Naudokite tai kaip atspirties tašką ir patikrinkite
    įdiegtos kliento versijos dokumentaciją.

Ekrane **Add DB Connection** pridėkite šias savybes:

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Turi sutapti su tvarkyklės pavadinimu, užregistruotu *digna* serveryje. Riestiniai skliaustai yra įprastas šio pavadinimo rašymo būdas |
| `SERVER` | `netezza.example.com` | Serverio pavadinimas arba IP adresas |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Duomenų bazė, kurioje pradedamas seansas |
| `UID` | `ADMIN` | Duomenų bazės vartotojas |
| `PWD` | `<password>` | Pažymėkite **Encrypted** |

Gauta ryšio eilutė atrodo taip:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

Priklausomai nuo tvarkyklės versijos, nustatymo ir saugumo reikalavimų, gali prireikti papildomų
savybių — pavyzdžiui, `SecurityLevel` ir `CaCertFile` TLS apsaugotam įrenginiui. Kiekvieną
parinktį, kurią siūlo tvarkyklės dialogo langai *Advanced*, *SSL* ir *Driver*, galima pridėti
kaip savybę.

---

## 3. *digna* konfigūracija {: #3-digna-configuration }

Ekrane **Add DB Connection** nurodykite:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Pastabos apie Netezza {: #4-notes-on-netezza }

- **Taikomi ir katalogai, ir schemos.** *digna* duomenų bazes, kurias vartotojas gali matyti (iš
  `_V_DATABASE`), išvardija kaip katalogus, o jų schemas (iš `_V_SCHEMA`) — po jais, todėl vienas
  ryšys gali aptarnauti šaltinius daugiau nei vienoje duomenų bazėje. `DATABASE` nulemia tik tai,
  kur pradedamas seansas.
- **Identifikatoriai rašomi didžiosiomis raidėmis**, nebent jie buvo sukurti kabutėse, todėl
  aukščiau pateiktuose pavyzdžiuose naudojami `TEST` ir `ADMIN`.
- **Profiliavimo režimai.** *Permanent* kuria darbines lenteles schemoje **Work Schema**, todėl
  vartotojui ten reikia teisės `CREATE TABLE`. *Session* naudoja `CREATE TEMPORARY TABLE` ir
  **Work Schema** neliečia. *Standard* reikia tik skaitymo prieigos.

---

## 5. Tvarkyklės patikrinimas (neprivaloma) {: #5-verifying-the-driver-optional }

Ryšiui be DSN ODBC duomenų šaltinio konfigūruoti nereikia, tačiau pačios tvarkyklės dialogo
langas yra patogus būdas patvirtinti, kad tvarkyklė ir jūsų prisijungimo duomenys veikia, prieš
įvedant juos į *digna*.

#### 1 žingsnis
![1 žingsnis](images/netezza/create_odbc_data_source_step1.png)

Laukai skirtuke **DSN Options** vienas prie vieno atitinka savybes iš
[2 skyriaus](#2-odbc-properties). Priklausomai nuo jūsų Netezza tvarkyklės, nustatymo ir saugumo
reikalavimų, gali prireikti duomenų ir skirtukuose **Advanced DSN Options**, **SSL DSN Options**
arba **Driver Options**; paprasčiausiam nustatymui pakanka **DSN Options**.

Spustelėkite mygtuką **Test Connection**.

#### 2 žingsnis
![2 žingsnis](images/netezza/create_odbc_data_source_step2.png)

Kai pamatote sėkmės ekraną, tvarkyklė veikia, o reikšmės yra teisingos.
