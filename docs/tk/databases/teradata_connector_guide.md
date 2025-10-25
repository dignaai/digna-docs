---
title: Teradata Bağlayıcısı – Veritabanı Entegrasyonu | digna Belgeleri
description: digna'yı teradatasql Python sürücüsü veya Teradata ODBC sürücüsü kullanarak Teradata'ya bağlanacak şekilde yapılandırın. DSN veya DSN'siz kurulumlarla parola tabanlı kimlik doğrulamayı destekler.
image: /assets/logo_square.png
---


# Teradata İçin Kaynak Bağlayıcı

Bu kılavuz, *digna*'nın Teradata'ya ya yerel Python bağlantısı ya da ODBC sürücüsü kullanarak nasıl bağlanacağını yapılandırmayı açıklar.

Aşağıda **"Veritabanı Bağlantısı Oluştur"** ekranına atıfta bulunulmaktadır.

![Bir veritabanı bağlantısı oluştur](images/data_source_config_input_mask.png)

---

## Yerel Python Sürücüsü

**Kütüphane:** `teradatasql`  
**Desteklenen Kimlik Doğrulama:** Yalnızca parola tabanlı kimlik doğrulama

> ⚠️ Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### *digna* Yapılandırması (Yerel Sürücü)

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdaki bilgileri sağlayın:

```
Technology:      Teradata
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1025
Database Name:   Database name
Schema Name:     Database name
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Sürücüsü

ODBC sürücüsü daha geniş bir kimlik doğrulama ve bağlantı seçenekleri yelpazesini destekleyebilir. Bu bölüm, **Teradata Database ODBC Driver 20.00** sürücüsünü kullanarak parola tabanlı kimlik doğrulama üzerine odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Satıcının resmi kurulum kılavuzunu izleyerek **Teradata Database ODBC Driver 20.00** (veya benzeri) sürücüyü yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Parola tabanlı kimlik doğrulamayı kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Test düğmesine tıklayın.

#### Adım 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Kullanıcı adı ve parolayı girin.

OK düğmesine tıklayın.
Başarı ekranını aldığınızda ODBC doğru şekilde yapılandırılmıştır.

---

Şimdi *digna*'yı ODBC bağlantısını kullanacak şekilde, ya **DSN (Veri Kaynağı Adı)** ile ya da **DSN'siz** bir kurulumla yapılandırabilirsiniz.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdakileri sağlayın:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Özellikleri

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 `DSN`, ODBC sürücü yapılandırmanızda tanımlı olan adla eşleşmelidir.

---

### B. DSN'siz Yapılandırma

#### *digna* Yapılandırması

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdakileri sağlayın:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Özellikleri

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
