---
title: Apache Hive Bağlayıcı – Veritabanı Entegrasyonu | digna Belgelendirmesi
description: digna'yı yerel PyHive sürücüsü veya Cloudera ODBC sürücüsü kullanarak Apache Hive'a bağlanacak şekilde yapılandırma. Parola tabanlı kimlik doğrulamayı ve DSN veya DSN'siz kurulumları destekler.
image: /assets/logo_square.png
---


# Hive için Kaynak Bağlayıcısı

Bu kılavuz, *digna*'nın Hive'a yerel Python bağlayıcısı veya ODBC sürücüsü kullanarak nasıl bağlanacağını yapılandırmayı açıklar.

Bu, **"Create a Database Connection"** ekranına atıfta bulunur.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Yerel Python Sürücüsü

**Kütüphane:** `PyHive`  
**Desteklenen Kimlik Doğrulama:** Yalnızca parola tabanlı kimlik doğrulama

> ⚠️ Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### *digna* Yapılandırması (Yerel Sürücü)

Aşağıdaki bilgileri **"Create a Database Connection"** ekranında sağlayın:

```
Technology:      Apache Hive
Host Address:    Sunucu adı veya IP adresi
Host Port:       Port numarası, örn. 10000
Database Name:   Kaynak veriyi içeren şema
Schema Name:     Kaynak veriyi içeren şema
User Name:       Veritabanı kullanıcı adı
User Password:   Kullanıcı için parola
Use ODBC:        Devre Dışı (varsayılan)
```

---

## ODBC Sürücüsü

ODBC sürücüsü, daha geniş bir kimlik doğrulama ve bağlantı seçeneği yelpazesini destekleyebilir. Bu bölüm, sürücü **Cloudera ODBC Driver for Apache Hive** kullanılarak parola tabanlı kimlik doğrulamasına odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Üreticinin resmi kurulum kılavuzunu izleyerek **Cloudera ODBC Driver for Apache Hive** (veya benzeri) sürücüsünü yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Parola tabanlı kimlik doğrulama kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Adım 2 – Bağlantıyı test et

Parolayı girin ve **Test** düğmesine tıklayın.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Başarılı bir testten sonra **OK** düğmesine tıklayın.

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde yapılandırabilirsiniz; ya **DSN (Data Source Name)** ile ya da **DSN'siz** bir kurulumla.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri sağlayın:

```
Technology:      Apache Hive
Database Name:   Kaynak veriyi içeren şema (Schema Name ile aynı)
Schema Name:     Kaynak veriyi içeren şema
Use ODBC:        Etkin
```

#### ODBC Özellikleri

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{parolanız süslü parantez içinde}"
```

> 🔹 `DSN` ODBC sürücü yapılandırmanızda tanımlı olan ad ile eşleşmelidir.

---

### B. DSN'siz Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri sağlayın:

```
Technology:      Apache Hive
Database Name:   Kaynak veriyi içeren şema (Schema Name ile aynı)
Schema Name:     Kaynak veriyi içeren şema
Use ODBC:        Etkin
```

#### ODBC Özellikleri

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "sunucu adınız veya IP adresiniz"
name: "PORT",       value: "Port numarası, örn. 10000"
name: "Schema",     value: "Kaynak veriyi içeren şema"
name: "UID",        value: "your hive user'
name: "PWD",        value: "your hive password"
name: "AuthMech",   value: "3"
```