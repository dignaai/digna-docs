---
title: Teradata Bağlayıcısı – Veritabanı Entegrasyonu | digna Dokümantasyonu
description: digna'yı teradatasql Python sürücüsü veya Teradata ODBC sürücüsü kullanarak Teradata'ya bağlanacak şekilde yapılandırın. DSN veya DSN'siz kurulumlarla parola tabanlı kimlik doğrulamayı destekler.
image: /assets/logo_square.png
---


# Teradata için Kaynak Bağlayıcı

Bu kılavuz, *digna*'yı Teradata'ya ya yerel Python bağlayıcısıyla ya da ODBC sürücüsüyle nasıl bağlayacağınızı açıklar.

Bu, **"Create a Database Connection"** ekranına atıfta bulunur.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Yerel Python Sürücüsü

**Kütüphane:** `teradatasql`  
**Desteklenen Kimlik Doğrulama:** Yalnızca parola tabanlı kimlik doğrulama

> Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### *digna* Yapılandırması (Yerel Sürücü)

**"Create a Database Connection"** ekranında aşağıdaki bilgileri sağlayın:

```
Technology:      Teradata
Host Address:    Sunucu adı veya IP adresi
Host Port:       Port numarası, örn. 1025
Database Name:   Veritabanı adı
Schema Name:     Veritabanı adı
User Name:       Veritabanı kullanıcı adı
User Password:   Kullanıcı parolası
Use ODBC:        Devre dışı (varsayılan)
```

---

## ODBC Sürücüsü

ODBC sürücüsü daha geniş bir kimlik doğrulama ve bağlantı seçenekleri yelpazesini destekleyebilir. Bu bölüm, sürücü **Teradata Database ODBC Driver 20.00** kullanarak parola tabanlı kimlik doğrulamasına odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Satıcının resmi kurulum kılavuzunu izleyerek **Teradata Database ODBC Driver 20.00** (veya benzeri) sürücüsünü yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Parola tabanlı kimlik doğrulama kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

**Test** düğmesine tıklayın.

#### Adım 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Kullanıcı adı ve parolayı girin.

**OK** düğmesine tıklayın. Başarı ekranını aldığınızda ODBC doğru şekilde yapılandırılmış demektir.

---

Şimdi *digna*'yı, **DSN (Data Source Name)** ile veya **DSN'siz** bir yapılandırmayla ODBC bağlantısını kullanacak şekilde yapılandırabilirsiniz.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri sağlayın:

```
Technology:      Teradata
Database Name:   Kaynak şemayı içeren veritabanı
Schema Name:     Kaynak verileri içeren şema
Use ODBC:        Etkin
```

#### ODBC Özellikleri

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "veritabanı kullanıcı adınız"
name: "PWD",        value: "veritabanı parolanız"
```

> `DSN`, ODBC sürücü yapılandırmanızda tanımlanan ad ile eşleşmelidir.

---

### B. DSN'siz Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri sağlayın:

```
Technology:      Teradata
Database Name:   Kaynak verileri içeren şema (Schema Name ile aynı)
Schema Name:     Kaynak verileri içeren şema
Use ODBC:        Etkin
```

#### ODBC Özellikleri

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "sunucu adınız veya IP adresiniz"
name: "UID",        value: "veritabanı kullanıcı adınız"
name: "PWD",        value: "veritabanı parolanız"
```