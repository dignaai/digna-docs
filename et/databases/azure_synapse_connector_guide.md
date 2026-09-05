# Allika liides Azure Synapse Analyticsi jaoks

See juhend kirjeldab, kuidas seadistada *digna* ühenduma Azure Synapse Analyticsiga kas natiivse Pythoni ühenduri või ODBC-draiveri abil.
See toetab nii serverless kui ka pühendatud SQL-puule.

See viitab ekraanile **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Supported Authentication:** Ainult paroolipõhine autentimine

> Muude autentimismeetodite puhul kasutage palun ODBC-draiverit.

### *digna* konfiguratsioon (natiivne draiver)

Sisestage järgmine info ekraanil **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC-draiver võib toetada laiemat valikut autentimis- ja ühendusvõimalusi. See jaotis keskendub paroolipõhisele autentimisele, kasutades draiverit **ODBC Driver 18 for SQL Server**.

### 1. Installige ODBC-draiver

Installige draiver **ODBC Driver 18 for SQL Server** (või sarnane) vastavalt tootja ametlikule paigaldusjuhisele.

### 2. Konfigureerige ODBC andmeallikas

Järgige neid samme, et konfigureerida uus ODBC andmeallikas, kasutades paroolipõhist autentimist:

#### Step 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Täitke väli "Server".
Kasutage synapse tööruumi nime ja lisage sellele ".sql.azuresynapse.net".   
**Tähelepanu**, kui soovite ühenduda serverless SQL-puuliga, siis lisage kindlasti "-ondemand", nagu alloleval ekraanipildil näidatud.

Klikkige nuppu **Next >**.

#### Step 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Valige autentimismeetod (nt kasutajanimi ja parool)
ja sisestage vajalikud andmed.

Klikkige nuppu **Next >**.

#### Step 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Valige ANSI-sobivad seaded ja seejärel klikkige nuppu **Next >**.

#### Step 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Võite jätta vaikeväärtused või valida vajalikud valikud 
ja klikkida seejärel nuppu **Finish**. 

#### Step 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Nüüd klikkige nuppu ** Test datasource **.

#### Step 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Kui saate edukusekraani, on ODBC õigesti konfigureeritud.

---

Nüüd saate seadistada *digna* kasutama ODBC-ühendust kas **DSN (Data Source Name)** abil või **DSN-less** seadistusega.

---

### A. DSN-põhine konfiguratsioon

#### *digna* konfiguratsioon

Ekraanil **"Create a Database Connection"** sisestage järgmised andmed:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC omadused

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> `DSN` peab vastama teie ODBC draiveri konfigureerimisel määratud nimele.

---

### B. DSN-less konfiguratsioon

#### *digna* konfiguratsioon

Ekraanil **"Create a Database Connection"** sisestage järgmised andmed:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC omadused

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Märkus** SERVER-i atribuudi kohta:  
Kasutage synapse tööruumi nime ja lisage sellele ".sql.azuresynapse.net". Kui soovite ühenduda serverless SQL-puuliga, siis lisage kindlasti "-ondemand", nagu alloleval ekraanipildil näidatud.