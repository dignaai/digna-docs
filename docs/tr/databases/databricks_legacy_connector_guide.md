---
title: Databricks Bağlayıcı (Legacy, Unity Catalog olmadan) | digna Dokümantasyonu
description: Native Python bağlayıcısı veya Simba Spark ODBC sürücüsü kullanarak Unity Catalog olmadan Databricks'e bağlanmak için digna'yı yapılandırın. Token tabanlı kimlik doğrulamayı ve esnek bağlantı seçeneklerini destekler.
image: /assets/logo_square.png
---

# Databricks İçin Kaynak Bağlayıcı - Unity Catalog olmadan

Bu kılavuz, *digna*'yı Databricks'e ya native Python bağlayıcısı ya da ODBC sürücüsü üzerinden bağlayacak şekilde nasıl yapılandıracağınızı açıklar.

Bu, **"Create a Database Connection"** ekranına atıfta bulunmaktadır.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Yerel (Native) Python Sürücüsü

**Kütüphane:** `databricks-sql-connector`  
**Desteklenen Kimlik Doğrulama:** Yalnızca Kişisel Erişim Jetonu (PAT)

> Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### Kişisel Erişim Jetonu (PAT)

Kişisel erişim jetonu kullanarak kimlik doğrulaması yapmak için resmi Databricks dokümantasyonuna bakın:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Yapılandırması (Yerel Sürücü)

**"Create a Database Connection"** ekranında aşağıdaki bilgileri sağlayın:

```
Teknoloji:       Databricks (Legacy)
Host Adresi:     Databricks ana bilgisayar adı, örn. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Portu:      443
Veritabanı Adı:  Unity Catalog olmadan databricks için bu parametre kullanılmıyor
Şema Adı:        Kaynak veriyi içeren şema
Kullanıcı Adı:   Databricks tarafından sağlanan HTTP Path, örn. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
Kullanıcı Parolası: Kişisel Erişim Jetonu, örn. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
ODBC Kullanımı:  Devre Dışı (varsayılan)
```

---

## ODBC Sürücüsü

ODBC sürücüsü, daha geniş bir kimlik doğrulama ve bağlantı seçenekleri yelpazesini destekler. Bu bölüm, **Simba Spark ODBC Driver** kullanarak token tabanlı kimlik doğrulamaya odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Satıcının resmi kurulum kılavuzunu takip ederek **Simba Spark ODBC Driver**'ı yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Kişisel Erişim Jetonu kullanarak yeni bir ODBC veri kaynağı yapılandırmak için aşağıdaki adımları izleyin:

#### Adım 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Adım 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Adım 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Adım 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Adım 5 – Bağlantıyı Test Etme

**TEST** düğmesine tıklayın. Başarılı bir bağlantı şu şekilde görünmelidir:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde yapılandırabilirsiniz; ya bir **DSN (Data Source Name)** ile ya da **DSN-less** bir yapı ile.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

"Create a Database Connection" ekranında aşağıdakileri sağlayın:

```
Teknoloji:       Databricks (Legacy)
Veritabanı Adı:  Unity Catalog olmadan databricks için bu parametre kullanılmıyor
Şema Adı:        Kaynak veriyi içeren şema
ODBC Kullanımı:  Etkin
```

#### ODBC Özellikleri

```
name: "DSN",    value: "*digna*data_databricks"
```

> `DSN`, ODBC sürücü yapılandırmanızda tanımladığınız isimle eşleşmelidir.

---

### B. DSN-less Yapılandırma

#### *digna* Yapılandırması

"Create a Database Connection" ekranında aşağıdakileri sağlayın:

```
Teknoloji:       Databricks (Legacy)
Veritabanı Adı:  Unity Catalog olmadan databricks için bu parametre kullanılmıyor
Şema Adı:        Kaynak veriyi içeren şema
ODBC Kullanımı:  Etkin
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