---
title: Azure Synapse priključek – integracija baze podatkov | digna dokumentacija
description: Konfigurirajte *digna*, da se poveže z Azure Synapse Analytics z uporabo bodisi nativnega Python gonilnika ali ODBC gonilnika. Podpira tako brezstrežne (serverless) kot namensko dodeljene SQL poole.
image: /assets/logo_square.png
---


# Priključek vira za Azure Synapse Analytics

Ta vodič pojasnjuje, kako povežete *digna* z Azure Synapse Analytics z uporabo bodisi nativnega Python gonilnika ali ODBC gonilnika. Podpira tako brezstrežne (serverless) kot namensko dodeljene SQL poole.

Ta dokument se nanaša na zaslon **"Create a Database Connection"**.

![Ustvari povezavo do baze podatkov](images/data_source_config_input_mask.png)

---

## Nativni Python gonilnik

**Knjžnica:** `pymssql`  
**Podprte metode overjanja:** samo overjanje z geslom

> ⚠️ Za druge metode overjanja uporabite ODBC gonilnik.

### Konfiguracija *digna* (nativni gonilnik)

Na zaslonu **"Create a Database Connection"** vnesite naslednje podatke:

```
Tehnologija:     MS SQL Server
Naslov gostitelja: <synapse-workspace>[-ondemand].sql.azuresynapse.net
Vrata gostitelja:  Številka vrat, npr. 1433
Ime baze podatkov: Ime baze podatkov
Ime sheme:         Shema, ki vsebuje izvorne podatke
Uporabniško ime:   Uporabniško ime baze podatkov
Geslo uporabnika:  Geslo uporabnika
Uporabi ODBC:      Onemogočeno (privzeto)
```

---

## ODBC gonilnik

ODBC gonilnik lahko podpira širši nabor možnosti overjanja in povezovanja. Ta razdelek se osredotoča na overjanje z geslom z uporabo **ODBC Driver 18 for SQL Server**.

### 1. Namestite ODBC gonilnik

Namestite **ODBC Driver 18 for SQL Server** (ali podoben) tako, da sledite uradnim navodilom dobavitelja.

### 2. Konfigurirajte ODBC vir podatkov

Za konfiguracijo novega ODBC vira podatkov z overjanjem na osnovi gesla sledite tem korakom:

#### Korak 1
![Korak 1](images/azure_synapse/create_odbc_data_source_step1.png)

Izpolnite polje "Server".  
Uporabite ime Synapse delovnega prostora in dodajte končnico ".sql.azuresynapse.net".  
Pozor: če se želite povezati z brezstrežnim (serverless) SQL poolom, poskrbite, da na koncu dodate "-ondemand", kot je prikazano na spodnjem posnetku zaslona.

Kliknite **Next >**.

#### Korak 2
![Korak 2](images/azure_synapse/create_odbc_data_source_step2.png)

Izberite metodo overjanja (npr. uporabniško ime in geslo) in vnesite zahtevane podatke.

Kliknite **Next >**.

#### Korak 3
![Korak 3](images/azure_synapse/create_odbc_data_source_step3.png)

Izberite nastavitve skladnosti z ANSI, nato kliknite **Next >**.

#### Korak 4
![Korak 4](images/azure_synapse/create_odbc_data_source_step4.png)

Lahko pustite privzete nastavitve ali prilagodite možnosti po potrebi in nato kliknite **Finish**.

#### Korak 5
![Korak 5](images/azure_synapse/create_odbc_data_source_step5.png)

Zdaj kliknite **Preizkusi vir podatkov**.

#### Korak 6
![Korak 6](images/azure_synapse/create_odbc_data_source_step6.png)

Če prejmete zaslon o uspehu, je ODBC pravilno konfiguriran.

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC povezavo bodisi z **DSN (Data Source Name)** ali z **DSN-less** nastavitvijo.

---

### A. Konfiguracija na osnovi DSN

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Tehnologija:     MS SQL Server
Ime baze podatkov: Ime baze podatkov, ki vsebuje izvorno shemo
Ime sheme:         Shema, ki vsebuje izvorne podatke
Uporabi ODBC:      Omogočeno
```

#### ODBC lastnosti

```
name: "DSN",      value: "azure-synopse-serverless-1"
name: "UID",      value: "vaše_uporabniško_ime_baze"
name: "PWD",      value: "vaše_geslo_baze"
name: "DATABASE", value: "ime_baze_podatkov_s_shemo_izvora"
```

> 🔹 `DSN` se mora ujemati z imenom, definiranim v konfiguraciji vašega ODBC gonilnika.

---

### B. Konfiguracija brez DSN (DSN-less)

#### Konfiguracija *digna*

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Tehnologija:     MS SQL Server
Ime baze podatkov: Shema, ki vsebuje izvorne podatke (enako kot Schema Name)
Ime sheme:         Shema, ki vsebuje izvorne podatke
Uporabi ODBC:      Omogočeno
```

#### ODBC lastnosti

```
name: "DRIVER",   value: "ODBC Driver 18 for SQL Server"
name: "SERVER",   value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",      value: "vaše_uporabniško_ime_baze"
name: "PWD",      value: "vaše_geslo_baze"
name: "DATABASE", value: "ime_baze_podatkov_s_shemo_izvora"
```

Opomba: glede lastnosti SERVER: uporabite ime Synapse delovnega prostora in dodajte končnico ".sql.azuresynapse.net". Če se povezujete z brezstrežnim (serverless) SQL poolom, poskrbite, da na koncu dodate "-ondemand", kot je prikazano na posnetku zaslona.