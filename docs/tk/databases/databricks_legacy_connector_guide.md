---
title: Databricks Bağlayıcısı (Eski, Unity Catalog Olmadan) | digna Dokümantasyonu
description: Unity Catalog olmadan native Python connector veya Simba Spark ODBC sürücüsü kullanarak *digna*'yı Databricks'e bağlayacak şekilde yapılandırma. Token tabanlı kimlik doğrulamasını ve esnek bağlantı seçeneklerini destekler.
image: /assets/logo_square.png
---

# Databricks için Kaynak Bağlayıcı - Unity Catalog Olmadan

Bu kılavuz, *digna*'yı Databricks'e native Python connector veya ODBC sürücüsü kullanarak nasıl yapılandıracağınızı açıklar.

It refers to the screen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> ⚠️ Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### Personal Access Token (PAT)

Kişisel erişim token'ı ile kimlik doğrulama yapmak için resmi Databricks dokümantasyonuna bakın:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Yapılandırması (Native Sürücü)

Aşağıdaki bilgileri **"Create a Database Connection"** ekranına girin:

```
Technology:      Databricks (Legacy)
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC sürücüsü, daha geniş bir kimlik doğrulama ve bağlantı seçenekleri yelpazesini destekler. Bu bölüm, **Simba Spark ODBC Driver** kullanarak token tabanlı kimlik doğrulamasına odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Sağlayıcının resmi kurulum kılavuzunu takip ederek **Simba Spark ODBC Driver**'ı yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Kişisel Erişim Token'ı kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Adım 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Adım 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Adım 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Adım 5 – Bağlantıyı test et

**TEST** düğmesine tıklayın. Başarılı bağlantı şöyle görünmelidir:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde yapılandırabilirsiniz; ya bir **DSN (Data Source Name)** ile ya da **DSN'siz** bir kurulum ile.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri girin:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 `DSN` ODBC sürücü yapılandırmanızda tanımlı olan ad ile eşleşmelidir.

---

### B. DSN'siz Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri girin:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

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