# Azure Synapse Analytics šaltinio jungtis

Šiame vadove aprašyta, kaip sukonfigūruoti *digna* prisijungimą prie Azure Synapse Analytics per
**ODBC**, naudojant ryšio eilutę **be DSN** (DSN-less). Palaikomi ir serverless, ir dedicated SQL
telkiniai (pools).

*digna* pusės nustatymas yra vienodas visoms technologijoms — kur kuriami ryšiai, kaip
šifruojamos savybių reikšmės, kaip testuojamas ryšys ir ką reiškia profiliavimo režimai. Tai
aprašyta [Duomenų bazių ryšių apžvalgoje](overview.md). Šiame puslapyje aprašoma tai, kas būdinga
Azure Synapse.

!!! note "Technologija"

    Synapse naudoja SQL Server dialektą, todėl ryšys kuriamas su **Technology:
    SQL Server**. Vietiniam (on-premises) serveriui žr. [MS SQL Server](sqlserver_connector_guide.md).

---

## 1. Įdiekite ODBC tvarkyklę {: #1-install-the-odbc-driver }

Įdiekite **ODBC Driver 18 for SQL Server** kompiuteryje, kuriame veikia *digna* backend,
laikydamiesi [Microsoft diegimo vadovo](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server),
ir nuskaitykite tikslų užregistruotos tvarkyklės pavadinimą savo serveryje, kaip aprašyta skyriuje
[ODBC tvarkyklės diegimas digna serveryje](overview.md#install-the-driver).

---

## 2. ODBC savybės {: #2-odbc-properties }

!!! important "Pavyzdys, o ne specifikacija"

    Toliau pateiktas rinkinys yra vienas žinomai veikiantis derinys. Savybės priklauso
    Microsoft ODBC tvarkyklei, todėl jų pavadinimai, numatytosios reikšmės ir priimamos reikšmės
    skiriasi tarp tvarkyklės versijų ir platformų, o tai, ko reikalauja darbo sritis (workspace),
    priklauso nuo jos konfigūracijos — telkinio tipo, autentifikacijos metodo, ugniasienės.
    Naudokite tai kaip atspirties tašką ir patikrinkite įdiegtos tvarkyklės versijos dokumentaciją.

Ekrane **Add DB Connection** pridėkite šias savybes:

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Turi sutapti su tvarkyklės pavadinimu, užregistruotu *digna* serveryje |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Darbo srities pavadinimas ir galinio taško priesaga — žr. toliau |
| `DATABASE` | `dignadata` | Duomenų bazė, kurioje yra šaltinio schemos. Tai vienintelė duomenų bazė, kurią šis ryšys gali profiliuoti |
| `UID` | `sqladminuser` | SQL prisijungimas |
| `PWD` | `<password>` | Pažymėkite **Encrypted** |

Gauta ryšio eilutė atrodo taip:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### Reikšmė `SERVER`

Paimkite Synapse darbo srities pavadinimą ir pridėkite galinio taško priesagą:

| Telkinys | `SERVER` |
|---|---|
| **Serverless SQL pool** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Dedicated SQL pool** | `<workspace>.sql.azuresynapse.net` |

!!! warning "Dalį `-ondemand` lengva praleisti"

    Be jos pavadinimas nukreipiamas į dedicated galinį tašką, ir ryšys arba nepavyksta, arba
    tyliai pasiekia kitą telkinį nei numatyta. Abu galiniai taškai rodomi darbo srities apžvalgos
    puslapyje Azure portale.

### Ugniasienė

Synapse darbo srities ugniasienė turi leisti *digna* serverio išeinantį adresą. Prieš testuodami
ryšį, pridėkite jį darbo srities skiltyje **Networking** — užblokuotas adresas pasireiškia kaip
ryšio laiko limito viršijimas, o ne kaip autentifikacijos klaida.

### Microsoft Entra ID autentifikacija

Vietoje SQL prisijungimo tvarkyklė gali autentifikuotis per Entra ID. Pakeiskite `UID`/`PWD`
autentifikacijos metodu, kurio tikisi jūsų darbo sritis, pavyzdžiui:

| Raktas | Pavyzdinė reikšmė | Pastabos |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | Tada `UID` priima programos (kliento) ID, o `PWD` – kliento slaptumo raktą |
| `Authentication` | `ActiveDirectoryMSI` | *digna* serverio valdoma tapatybė (managed identity), prisijungimo duomenų nereikia |

---

## 3. *digna* konfigūracija {: #3-digna-configuration }

Ekrane **Add DB Connection** nurodykite:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Pastabos apie Azure Synapse {: #4-notes-on-azure-synapse }

- **Serverless telkiniai palaiko tik *Standard* profiliavimą.** Serverless SQL telkinys negali
  kurti lentelių duomenų bazėje, todėl negali veikti nei *Permanent*, nei *Session* profiliavimas.
  *Standard* skaičiuoja metrikas tiesiogiai šaltinyje, o tai ir pigesnis variantas, nes serverless
  apmokestinamas pagal apdorotų duomenų kiekį.
- **Vienas ryšys mato vieną duomenų bazę.** *digna* siūlo `DATABASE` nurodytos duomenų bazės
  schemas, nes Synapse, kaip ir SQL Server, kaip katalogą praneša tik dabartinę duomenų bazę.
- **Šifravimas įjungtas pagal nutylėjimą** Driver 18 tvarkyklėje, o Synapse galiniai taškai
  pateikia galiojančius viešus sertifikatus, todėl savybių `Encrypt` ar `TrustServerCertificate`
  nereikia.
- **Serverless galinis taškas gali atsibusti po neveiklumo** pirmojo prisijungimo metu. Jei ryšio
  testui baigiasi laikas telkinyje, kuris kurį laiką nebuvo naudojamas, bandykite dar kartą.

---

## 5. Tvarkyklės patikrinimas (neprivaloma) {: #5-verifying-the-driver-optional }

Ryšiui be DSN ODBC duomenų šaltinio konfigūruoti nereikia, tačiau pačios tvarkyklės vedlys yra
patogus būdas patvirtinti, kad tvarkyklė veikia ir kad darbo sritis priima jūsų prisijungimo
duomenis, prieš įvedant juos į *digna*.

#### 1 žingsnis
![1 žingsnis](images/azure_synapse/create_odbc_data_source_step1.png)

Užpildykite lauką „Server“.
Naudokite Synapse darbo srities pavadinimą ir papildykite jį „.sql.azuresynapse.net“.  
**Dėmesio**: jei norite jungtis naudodami serverless SQL telkinį, būtinai įtraukite
„-ondemand“, kaip parodyta ekrano nuotraukoje aukščiau.

Spustelėkite mygtuką **Next >**.

#### 2 žingsnis
![2 žingsnis](images/azure_synapse/create_odbc_data_source_step2.png)

Pasirinkite autentifikacijos metodą (pvz., vartotojo vardas ir slaptažodis)
ir pateikite reikiamus duomenis.

Spustelėkite mygtuką **Next >**.

#### 3 žingsnis
![3 žingsnis](images/azure_synapse/create_odbc_data_source_step3.png)

Pasirinkite ANSI atitinkančius nustatymus ir spustelėkite mygtuką **Next >**.

#### 4 žingsnis
![4 žingsnis](images/azure_synapse/create_odbc_data_source_step4.png)

Galite palikti numatytuosius nustatymus arba pasirinkti reikiamas parinktis
ir spustelėti mygtuką **Finish**.

#### 5 žingsnis
![5 žingsnis](images/azure_synapse/create_odbc_data_source_step5.png)

Dabar spustelėkite mygtuką **Test datasource**.

#### 6 žingsnis
![6 žingsnis](images/azure_synapse/create_odbc_data_source_step6.png)

Sėkmės ekranas patvirtina, kad tvarkyklė, galinis taškas ir prisijungimo duomenys veikia. Įvestos
reikšmės yra būtent tos reikšmės, kurias priima savybės iš [2 skyriaus](#2-odbc-properties).