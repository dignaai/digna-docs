---
title: Databricks-liitin (Legacy, ilman Unity Catalog) | digna-dokumentaatio
description: Konfiguroi digna yhdistämään Databricksiin ilman Unity Catalogia käyttäen natiivista Python-liitintä tai Simba Spark ODBC -ajuria. Tukee token-pohjaista todennusta ja joustavia yhteysvaihtoehtoja.
image: /assets/logo_square.png
---

# Databricks-lähdeyhteys – ilman Unity Catalog

Tämä opas kuvaa, miten *digna* konfiguroidaan yhdistämään Databricksiin joko natiivilla Python-kirjastolla tai ODBC-ajurilla.

Se viittaa näyttöön **"Create a Database Connection"**.

![Luo tietokantayhteys](images/data_source_config_input_mask.png)

---

## Natiivinen Python-ajuri

**Kirjasto:** `databricks-sql-connector`  
**Tuettu todennus:** Personal Access Token (PAT) ainoastaan

> ⚠️ Muiden todennustapojen osalta käytä ODBC-ajuria.

### Personal Access Token (PAT)

Todentaaksesi henkilökohtaisella access tokenilla, katso Databricksin virallinen dokumentaatio:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna*-konfiguraatio (natiiviajuri)

Anna seuraavat tiedot **"Create a Database Connection"** -näytössä:

```
Technology:      Databricks (Legacy)
Host Address:    Databricks-isäntänimi, esim. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Tämä parametri ei ole käytössä databricksille ilman unity catalogia
Schema Name:     Skeema, joka sisältää lähdetiedot
User Name:       Databricksin tarjoama HTTP Path, esim. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, esim. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Pois päältä (oletus)
```

---

## ODBC-ajuri

ODBC-ajuri tukee laajempaa valikoimaa todennus- ja yhteysvaihtoehtoja. Tässä osiossa keskitytään token-pohjaiseen todennukseen käyttäen **Simba Spark ODBC Driver** -ajuria.

### 1. Asenna ODBC-ajuri

Asenna **Simba Spark ODBC Driver** noudattamalla toimittajan virallista asennusohjetta.

### 2. Konfiguroi ODBC-tietolähde

Tee seuraavat vaiheet konfiguroidaksesi uuden ODBC-tietolähteen käyttäen Personal Access Tokenia:

#### Vaihe 1
![Vaihe 1](images/databricks/create_odbc_data_source_step1.png)

#### Vaihe 2
![Vaihe 2](images/databricks/create_odbc_data_source_step2.png)

#### Vaihe 3
![Vaihe 3](images/databricks/create_odbc_data_source_step3.png)

#### Vaihe 4
![Vaihe 4](images/databricks/create_odbc_data_source_step4.png)

#### Vaihe 5 – testaa yhteys

Klikkaa **TEST**-painiketta. Onnistuneen yhteyden pitäisi näyttää tältä:

![Vaihe 5](images/databricks/create_odbc_data_source_step5.png)

---

Nyt voit konfiguroida *digna*:n käyttämään ODBC-yhteyttä joko **DSN:n (Data Source Name)** avulla tai **DSN-vapaalla** asetuksella.

---

### A. DSN-pohjainen konfiguraatio

#### *digna*-konfiguraatio

Anna **"Create a Database Connection"** -näytössä seuraavat tiedot:

```
Technology:      Databricks (Legacy)
Database Name:   Tämä parametri ei ole käytössä databricksille ilman unity catalogia
Schema Name:     Skeema, joka sisältää lähdetiedot
Use ODBC:        Päällä
```

#### ODBC-ominaisuudet

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 `DSN`-arvon on vastattava ODBC-ajurin konfiguraatiossa määriteltyä nimeä.

---

### B. DSN-vapaa konfiguraatio

#### *digna*-konfiguraatio

Anna **"Create a Database Connection"** -näytössä seuraavat tiedot:

```
Technology:      Databricks (Legacy)
Database Name:   Tämä parametri ei ole käytössä databricksille ilman unity catalogia
Schema Name:     Skeema, joka sisältää lähdetiedot
Use ODBC:        Päällä
```

#### ODBC-ominaisuudet

```
name = "Driver",          value = "{Simba Spark ODBC Driver}"
name = "Host",            value = "xxxxxxxxxxxxxxxxxxx.databricks.com"
name = "Port",            value = "443"
name = "HTTPPath",        value = "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
name = "SSL",             value = "1"
name = "ThriftTransport", value = "2"
name = "AuthMech",        value = "3"
name = "UID",             value = "token"
name = "PWD",             value = "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```