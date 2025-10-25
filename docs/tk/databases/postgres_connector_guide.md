---
title: PostgreSQL Connector – Veritabanı Entegrasyonu | digna Belgeleri
description: digna'nın psycopg Python sürücüsü veya PostgreSQL ODBC sürücüsünü kullanarak PostgreSQL'e bağlanacak şekilde nasıl yapılandırılacağını açıklayın. DSN veya DSN'siz kurulumlarla parola tabanlı kimlik doğrulamasını destekler.
image: /assets/logo_square.png
---


# PostgreSQL Kaynak Bağlayıcısı

Bu kılavuz, *digna*'yı yerel Python bağlayıcısı veya ODBC sürücüsü kullanarak Postgres'e bağlanacak şekilde nasıl yapılandıracağınızı açıklar.

Bu, **"Veritabanı Bağlantısı Oluştur"** ekranına atıfta bulunur.

![Veritabanı bağlantısı oluştur](images/data_source_config_input_mask.png)

---

## Yerel Python Sürücüsü

**Kütüphane:** `psycopg`  
**Desteklenen Kimlik Doğrulama:** Yalnızca parola tabanlı kimlik doğrulama

> ⚠️ Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### *digna* Yapılandırması (Yerel Sürücü)

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdaki bilgileri girin:

```
Technology:      Postgres
Host Address:    Sunucu adı veya IP adresi
Host Port:       Port numarası, örn. 5432
Database Name:   Veritabanı adı
Schema Name:     Kaynak veriyi içeren şema
User Name:       Veritabanı kullanıcı adı
User Password:   Kullanıcı parolası
Use ODBC:        Devre Dışı (varsayılan)
```

---

## ODBC Sürücüsü

ODBC sürücüsü, daha geniş bir kimlik doğrulama ve bağlantı seçenekleri yelpazesini destekleyebilir. Bu bölüm, **PostgreSQL Unicode(x64)** sürücüsünü kullanarak parola tabanlı kimlik doğrulamaya odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Tedarikçinin resmi kurulum kılavuzunu izleyerek **PostgreSQL Unicode(x64)** (veya benzeri) sürücüyü yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Parola tabanlı kimlik doğrulama kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Adım 1](images/postgres/create_odbc_data_source_step1.png)

Not: Veritabanı yapılandırmanız belirli bir "SSLMode" seçmenizi gerektiriyorsa, lütfen DSN'siz yapılandırma tanımlarken de bunu kullandığınızdan emin olun.

#### Adım 2 – Bağlantıyı test et

**Bağlantıyı Test Et** düğmesine tıklayın.

![Adım 2](images/postgres/create_odbc_data_source_step2.png)

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde yapılandırabilirsiniz; ya bir **DSN (Veri Kaynağı Adı)** ile ya da **DSN'siz** bir kurulumla.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdakileri sağlayın:

```
Technology:      PostgreSQL
Database Name:   Kaynak şemayı içeren veritabanı
Schema Name:     Kaynak veriyi içeren şema
Use ODBC:        Etkin
```

#### ODBC Özellikleri

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 `DSN`, ODBC sürücü yapılandırmanızda tanımlanan isimle eşleşmelidir.

---

### B. DSN'siz Yapılandırma

#### *digna* Yapılandırması

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdakileri sağlayın:

```
Technology:      PostgreSQL
Database Name:   Kaynak veriyi içeren şema (Schema Name ile aynı)
Schema Name:     Kaynak veriyi içeren şema
Use ODBC:        Etkin
```

#### ODBC Özellikleri

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "sunucu adınız veya IP adresiniz"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres veya veritabanınızın başka bir adı"
name: "UID",        value: "Postgres kullanıcı adınız'
name: "PWD",        value: "Postgres parolanız"
name: "SSLMode",    value: "require"
```