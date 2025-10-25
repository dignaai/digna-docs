---
title: Databricks Bağlayıcısı Unity Catalog ile – Veritabanı Entegrasyonu | digna Dokümantasyonu
description: digna'yı, yerel Python konektörü veya ODBC sürücüsü kullanarak Unity Catalog ile Databricks'e bağlanacak şekilde yapılandırın. Token tabanlı kimlik doğrulamayı ve esnek bağlantı seçeneklerini destekler.
image: /assets/logo_square.png
---

# Databricks Kaynak Bağlayıcısı - Unity Catalog ile

Bu rehber, *digna*'yı Databricks'e ya yerel Python konektörü ya da ODBC sürücüsü kullanarak bağlanacak şekilde nasıl yapılandıracağınızı açıklar.

It refers to the screen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Yerel Python Sürücüsü

**Kütüphane:** `databricks-sql-connector`  
**Desteklenen Kimlik Doğrulama:** Sadece Personal Access Token (PAT)

> ⚠️ Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### Kişisel Erişim Token'ı (PAT)

Kişisel erişim token'ı kullanarak kimlik doğrulaması yapmak için resmi Databricks dokümantasyonuna bakın:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Yapılandırması (Yerel Sürücü)

**"Create a Database Connection"** ekranına aşağıdaki bilgileri girin:

```
Technology:      Databricks
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Name of the catalog to use. 
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Sürücüsü

ODBC sürücüsü daha geniş bir kimlik doğrulama ve bağlantı seçeneği yelpazesini destekler. Bu bölüm, **Simba Spark ODBC Driver** kullanarak token tabanlı kimlik doğrulamasına odaklanır.

### 1. ODBC Sürücüyü Yükleyin

Satıcının resmi kurulum kılavuzunu izleyerek **Simba Spark ODBC Driver**'ı yükleyin.

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

**TEST** düğmesine tıklayın. Başarılı bir bağlantı şöyle görünmelidir:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde, ya **DSN (Data Source Name)** ile ya da **DSN-less** yapılandırmasıyla ayarlayabilirsiniz.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranına aşağıdakileri girin:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Özellikleri

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 `DSN`, ODBC sürücü yapılandırmanızda tanımlanan ad ile eşleşmelidir.

---

### B. DSN-less Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranına aşağıdakileri girin:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Özellikleri

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