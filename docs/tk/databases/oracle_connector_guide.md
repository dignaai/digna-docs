---
title: Oracle Bağlayıcı – Veritabanı Entegrasyonu | digna Dokümantasyonu
description: python-oracledb sürücüsü veya Oracle ODBC sürücüsü kullanarak digna'yı Oracle'a bağlayacak şekilde yapılandırın. DSN veya DSN'siz kurulumlarla parola tabanlı kimlik doğrulamayı destekler.
image: /assets/logo_square.png
---


# Oracle için Kaynak Bağlayıcı

Bu kılavuz, *digna*'yı Oracle veritabanına yerel Python bağlantısı veya ODBC sürücüsü kullanarak nasıl bağlayacağınızı açıklar.

Bu, **"Create a Database Connection"** ekranına atıfta bulunur.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Yerel Python Sürücüsü

**Kütüphane:** `python-oracledb`  
**Desteklenen Kimlik Doğrulama:** Yalnızca parola tabanlı kimlik doğrulama

> ⚠️ Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### *digna* Yapılandırması (Yerel Sürücü)

**"Create a Database Connection"** ekranında aşağıdaki bilgileri sağlayın:

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

## ODBC Sürücüsü

ODBC sürücüsü daha geniş bir kimlik doğrulama ve bağlantı seçenekleri yelpazesini destekleyebilir. Bu bölüm, **Oracle in OraDB21Home1** sürücüsünü kullanarak parola tabanlı kimlik doğrulamaya odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Satıcının resmi kurulum kılavuzunu izleyerek **Oracle in OraDB21Home1** (veya benzeri) sürücüyü yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Parola tabanlı kimlik doğrulama kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Not:
TNS Service Name, oracle istemci kurulumunuzdaki tnsnames.ora dosyasında yapılandırılmalıdır. Bağlantı tanımlayıcısını (host, port, service name) burada sağlarsınız.

#### Adım 2 – Bağlantıyı test etme

**Test Connection** düğmesine tıklayın.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Parolayı girin ve **OK** düğmesine tıklayın.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde ya **DSN (Data Source Name)** ile ya da **DSN'siz** kurulumla yapılandırabilirsiniz.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri sağlayın:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Özellikleri

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> 🔹 `DSN`, ODBC sürücü yapılandırmanızda tanımlanan adla eşleşmelidir.

---

### B. DSN'siz Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri sağlayın:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Özellikleri

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```