# Oracle šaltinio jungtis

Šiame vadove aprašoma, kaip konfigūruoti *digna*, kad ji prisijungtų prie Oracle DB, naudojant arba natyvų Python jungiklį, arba ODBC tvarkyklę.

Tai nurodo ekraną **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natyvus Python tvarkyklė

**Biblioteka:** `python-oracledb`  
**Palaikomas autentifikavimas:** Tik slaptažodžiu pagrįstas autentifikavimas

> Kitiems autentifikavimo metodams naudokite ODBC tvarkyklę.

### *digna* konfigūracija (natyvus tvarkyklė)

Pateikite šią informaciją ekrane **"Create a Database Connection"**:

```
Technology:      Oracle
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1521
Database Name:   Instance name, service name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC tvarkyklė

ODBC tvarkyklė gali palaikyti platesnį autentifikavimo ir prisijungimo parinkčių spektrą. Šiame skyriuje dėmesys skiriamas slaptažodžiu pagrįstam autentifikavimui naudojant tvarkyklę **Oracle in OraDB21Home1**.

### 1. Įdiekite ODBC tvarkyklę

Įdiekite **Oracle in OraDB21Home1** (ar panašią) vadovaudamiesi tiekėjo oficialiu diegimo vadovu.

### 2. Konfigūruokite ODBC duomenų šaltinį

Atlikite šiuos veiksmus, kad sukonfigūruotumėte naują ODBC duomenų šaltinį, naudojant slaptažodžiu pagrįstą autentifikavimą:

#### 1 veiksmas
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Pastaba:
TNS Service Name turi būti sukonfigūruotas jūsų oracle kliento diegimo tnsnames.ora faile. Čia pateikiamas ryšio aprašas (host, port, service name).

#### 2 veiksmas – patikrinkite ryšį

Spustelėkite **Test Connection** mygtuką.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Įveskite slaptažodį ir spustelėkite **OK** mygtuką.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Dabar galite konfigūruoti *digna*, kad naudotų ODBC ryšį, arba su **DSN (Data Source Name)**, arba be DSN (**DSN-less**).

---

### A. DSN pagrįsta konfigūracija

#### *digna* konfigūracija

Ekrane **"Create a Database Connection"** nurodykite šiuos laukus:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC savybės

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> `DSN` turi atitikti pavadinimą, nurodytą jūsų ODBC tvarkyklės konfigūracijoje.

---

### B. DSN-less konfigūracija

#### *digna* konfigūracija

Ekrane **"Create a Database Connection"** nurodykite šiuos laukus:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC savybės

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```