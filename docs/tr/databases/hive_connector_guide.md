---
title: Apache Hive Bağlayıcısı – Veritabanı Entegrasyonu | digna Dokümantasyonu
description: digna'yı yerel PyHive sürücüsü veya Cloudera ODBC sürücüsünü kullanarak Apache Hive'a bağlanacak şekilde yapılandırın. Parola tabanlı kimlik doğrulamayı ve DSN veya DSN-less kurulumlarını destekler.
image: /assets/logo_square.png
---


# Hive İçin Kaynak Bağlayıcı

Bu rehber, *digna*'yı Hive'e yerel Python bağlayıcısı veya ODBC sürücüsü ile nasıl bağlayacağınızı açıklar.

Bu, **"Create a Database Connection"** ekranına atıfta bulunur.

![Veritabanı bağlantısı oluştur](images/data_source_config_input_mask.png)

---

## Yerel Python Sürücüsü

**Kütüphane:** `PyHive`  
**Desteklenen Kimlik Doğrulama:** Sadece parola tabanlı kimlik doğrulama

> Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### *digna* Yapılandırması (Yerel Sürücü)

**"Create a Database Connection"** ekranında aşağıdaki bilgileri sağlayın:

```
Technology:      Apache Hive
Host Address:    Sunucu adı veya IP adresi
Host Port:       Port numarası, örn. 10000
Database Name:   Kaynak veriyi içeren şema
Schema Name:     Kaynak veriyi içeren şema
User Name:       Veritabanı kullanıcı adı
User Password:   Kullanıcının parolası
Use ODBC:        Devre dışı (varsayılan)
```

---

## ODBC Sürücüsü

ODBC sürücüsü daha geniş bir kimlik doğrulama ve bağlantı seçenekleri yelpazesini destekleyebilir. Bu bölüm, **Cloudera ODBC Driver for Apache Hive** sürücüsünü kullanarak parola tabanlı kimlik doğrulamaya odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Tedarikçinin resmi kurulum kılavuzunu izleyerek **Cloudera ODBC Driver for Apache Hive** (veya benzer bir sürücü) yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Parola tabanlı kimlik doğrulama kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Adım 1](images/hive/create_odbc_data_source_step1.png)


#### Adım 2 – Bağlantıyı Test Etme

Parolayı girin ve **Test** düğmesine tıklayın.

![Adım 2](images/hive/create_odbc_data_source_step2.png)

Başarılı bir testten sonra **OK** düğmesine tıklayın.

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde, **DSN (Data Source Name)** ile veya **DSN-less** yapılandırma ile ayarlayabilirsiniz.

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
name: "PWD",            value: "{şifreniz süslü parantez içinde}"
```

> `DSN`, ODBC sürücü yapılandırmanızda tanımlı olan ad ile eşleşmelidir.

---

### B. DSN-less Yapılandırma

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
name: "UID",        value: "hive kullanıcı adınız'"
name: "PWD",        value: "hive parolanız"
name: "AuthMech",   value: "3"
```