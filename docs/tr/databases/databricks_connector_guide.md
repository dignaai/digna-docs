---
title: Databricks Bağlayıcısı Unity Catalog ile – Veritabanı Entegrasyonu | digna Dokümantasyonu
description: digna'yı Databricks ile Unity Catalog kullanarak, yerel Python connector veya ODBC sürücüsü aracılığıyla bağlanacak şekilde yapılandırma. Token tabanlı kimlik doğrulamayı ve esnek bağlantı seçeneklerini destekler.
image: /assets/logo_square.png
---

# Databricks İçin Kaynak Bağlayıcı - Unity Catalog ile

Bu kılavuz, *digna*'yı Databricks'e ya yerel Python connector ya da ODBC sürücüsü kullanarak bağlayacak şekilde nasıl yapılandıracağınızı açıklar.

Bu belge **"Create a Database Connection"** ekranına atıfta bulunur.

![Veritabanı bağlantısı oluştur](images/data_source_config_input_mask.png)

---

## Yerel Python Sürücüsü

**Kütüphane:** `databricks-sql-connector`  
**Desteklenen Kimlik Doğrulama:** Yalnızca Personal Access Token (PAT)

> ⚠️ Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### Personal Access Token (PAT)

Kişisel erişim belirteci kullanarak kimlik doğrulamak için resmi Databricks dokümantasyonuna bakın:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Yapılandırması (Yerel Sürücü)

**"Create a Database Connection"** ekranında aşağıdaki bilgileri sağlayın:

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

ODBC sürücüsü daha geniş bir kimlik doğrulama ve bağlantı seçenekleri yelpazesini destekler. Bu bölüm, **Simba Spark ODBC Driver** kullanarak token tabanlı kimlik doğrulamaya odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Vendor'ın resmi kurulum kılavuzunu izleyerek **Simba Spark ODBC Driver**'ı yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Kişisel Erişim Belirteci (PAT) kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Adım 1](images/databricks/create_odbc_data_source_step1.png)

#### Adım 2
![Adım 2](images/databricks/create_odbc_data_source_step2.png)

#### Adım 3
![Adım 3](images/databricks/create_odbc_data_source_step3.png)

#### Adım 4
![Adım 4](images/databricks/create_odbc_data_source_step4.png)

#### Adım 5 – Bağlantıyı test etme

**TEST** düğmesine tıklayın. Başarılı bir bağlantı şu şekilde görünmelidir:

![Adım 5](images/databricks/create_odbc_data_source_step5.png)

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde yapılandırabilirsiniz; ya bir **DSN (Data Source Name)** ile ya da **DSN-less** bir kurulumla.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri sağlayın:

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

> 🔹 `DSN`, ODBC sürücü yapılandırmanızda tanımladığınız isimle eşleşmelidir.

---

### B. DSN-less Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri sağlayın:

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