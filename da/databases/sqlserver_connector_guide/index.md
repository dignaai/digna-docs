# Source Connector for MS SQL Server

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til SQL Server ved enten at bruge den native Python-connector eller ODBC-driveren.

Den henviser til skærmen **"Opret en databaseforbindelse"**.

![Opret en databaseforbindelse](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Understøttet autentificering:** Kun adgangskodebaseret autentificering

> For andre autentificeringsmetoder, brug venligst ODBC-driveren.

### *digna* konfiguration (native driver)

Angiv følgende oplysninger i skærmen **"Opret en databaseforbindelse"**:

```
Teknologi:        MS SQL Server
Hostadresse:      Servernavn eller IP-adresse
Hostport:         Portnummer, f.eks. 1433
Databasenavn:     Databasenavn
Skema:            Skemaet der indeholder kilde-dataene
Brugernavn:       Databasenavn (brugerkonto)
Adgangskode:      Adgangskode til brugeren
Brug ODBC:        Deaktiveret (standard)
```

---

## ODBC-driver

ODBC-driveren kan understøtte et bredere udvalg af autentificerings- og tilslutningsmuligheder. Dette afsnit fokuserer på adgangskodebaseret autentificering ved brug af driveren **SQL Server**.

### 1. Installer ODBC-driveren

Installer driveren **SQL Server** (eller en lignende) ved at følge leverandørens officielle installationsvejledning.

### 2. Konfigurer ODBC-datakilden

Følg disse trin for at konfigurere en ny ODBC-datakilde ved brug af adgangskodebaseret autentificering:

#### Trin 1
![Trin 1](images/sqlserver/create_odbc_data_source_step1.png)

Klik på knappen **Næste >**.

#### Trin 2
![Trin 2](images/sqlserver/create_odbc_data_source_step2.png)

Vælg autentificeringsmetode (fx brugernavn og adgangskode)
og angiv de krævede oplysninger.

Klik på knappen **Næste >**.

#### Trin 3
![Trin 3](images/sqlserver/create_odbc_data_source_step3.png)

Vælg de ANSI-kompatible indstillinger og klik derefter på knappen **Næste >**.

#### Trin 4
![Trin 4](images/sqlserver/create_odbc_data_source_step4.png)

Du kan beholde standardindstillingerne eller vælge logningsmuligheder efter behov
og klik derefter på knappen **Udfør**. 

#### Trin 5
![Trin 5](images/sqlserver/create_odbc_data_source_step5.png)

Klik nu på knappen **Test datakilde**.

#### Trin 6
![Trin 6](images/sqlserver/create_odbc_data_source_step6.png)

Når du får succesmeddelelsen, er ODBC konfigureret korrekt.

---

Nu kan du konfigurere *digna* til at bruge ODBC-forbindelsen, enten med en **DSN (Data Source Name)** eller en **DSN-less** opsætning.

---

### A. DSN-baseret konfiguration

#### *digna* konfiguration

I skærmen **"Opret en databaseforbindelse"** angiver du følgende:

```
Teknologi:        MS SQL Server
Databasenavn:     Databasen der indeholder kilde-skemaet
Skema:            Skemaet der indeholder kilde-dataene
Brug ODBC:        Aktiveret
```

#### ODBC-egenskaber

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "din databasebruger"
name: "PWD",        value: "din databaseadgangskode"
name: "DATABASE",   value: "navnet på databasen, der indeholder kilde-data-skemaet"
```

> `DSN` skal matche navnet defineret i din ODBC-driverkonfiguration.

---

### B. DSN-less konfiguration

#### *digna* konfiguration

I skærmen **"Opret en databaseforbindelse"** angiver du følgende:

```
Teknologi:        MS SQL Server
Databasenavn:     Skemaet der indeholder kilde-dataene (samme som Skema)
Skema:            Skemaet der indeholder kilde-dataene
Brug ODBC:        Aktiveret
```

#### ODBC-egenskaber

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "dit servernavn eller IP-adresse"
name: "UID",        value: "din databasebruger"
name: "PWD",        value: "din databaseadgangskode"
name: "DATABASE",   value: "navnet på databasen, der indeholder kilde-data-skemaet"
```