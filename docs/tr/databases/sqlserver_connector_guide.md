---
title: MS SQL Server Bağlayıcısı – Veritabanı Entegrasyonu | digna Belgeleri
description: pymssql Python sürücüsü veya SQL Server ODBC sürücüsü kullanarak digna'yı Microsoft SQL Server'a bağlanacak şekilde yapılandırın. DSN veya DSN'siz kurulumlarla parola tabanlı kimlik doğrulamayı destekler.
image: /assets/logo_square.png
---


# MS SQL Server için Kaynak Bağlayıcı

Bu kılavuz, *digna*'yı hem yerel Python bağlayıcısı hem de ODBC sürücüsü kullanarak SQL Server'a nasıl bağlayacağınızı açıklar.

Bu belge **"Veritabanı Bağlantısı Oluştur"** ekranına atıfta bulunur.

![Veritabanı bağlantısı oluştur](images/data_source_config_input_mask.png)

---

## Yerel Python Sürücüsü

**Kütüphane:** `pymssql`  
**Desteklenen Kimlik Doğrulama:** Sadece parola tabanlı kimlik doğrulama

> ⚠️ Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### *digna* Yapılandırması (Yerel Sürücü)

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdaki bilgileri sağlayın:

```
Technology:      MS SQL Server
Host Address:    Sunucu adı veya IP adresi
Host Port:       Port numarası, örn. 1433
Database Name:   Veritabanı adı
Schema Name:     Kaynak veriyi içeren şema
User Name:       Veritabanı kullanıcı adı
User Password:   Kullanıcı şifresi
Use ODBC:        Devre Dışı (varsayılan)
```

---

## ODBC Sürücüsü

ODBC sürücüsü daha geniş kimlik doğrulama ve bağlantı seçeneklerini destekleyebilir. Bu bölüm, **SQL Server** sürücüsünü kullanarak parola tabanlı kimlik doğrulamaya odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Tedarikçinin resmi kurulum kılavuzunu izleyerek **SQL Server** (veya benzeri) sürücüsünü yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Parola tabanlı kimlik doğrulama kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Adım 1](images/sqlserver/create_odbc_data_source_step1.png)

**Next >** düğmesine tıklayın.

#### Adım 2
![Adım 2](images/sqlserver/create_odbc_data_source_step2.png)

Kimlik doğrulama yöntemini (ör. kullanıcı adı ve parola) seçin
ve gerekli bilgileri girin.

**Next >** düğmesine tıklayın.

#### Adım 3
![Adım 3](images/sqlserver/create_odbc_data_source_step3.png)

ANSI uyumlu ayarları seçin, ardından **Next >** düğmesine tıklayın.

#### Adım 4
![Adım 4](images/sqlserver/create_odbc_data_source_step4.png)

Varsayılan ayarları bırakabilir veya gerektiğinde günlükleme seçeneklerini belirleyip
**Finish** düğmesine tıklayabilirsiniz.

#### Adım 5
![Adım 5](images/sqlserver/create_odbc_data_source_step5.png)

Şimdi ** Test datasource ** düğmesine tıklayın.

#### Adım 6
![Adım 6](images/sqlserver/create_odbc_data_source_step6.png)

Başarı ekranını aldığınızda, ODBC düzgün şekilde yapılandırılmış demektir.

---

Artık digna'yı ODBC bağlantısını kullanacak şekilde, ya bir **DSN (Data Source Name)** ile ya da **DSN'siz** yapılandırarak ayarlayabilirsiniz.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdakileri sağlayın:

```
Technology:      MS SQL Server
Database Name:   Kaynak şemayı içeren veritabanı
Schema Name:     Kaynak veriyi içeren şema
Use ODBC:        Etkin
```

#### ODBC Özellikleri

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "veritabanı kullanıcı adınız"
name: "PWD",        value: "veritabanı şifreniz"
name: "DATABASE",   value: "kaynak veri şemasını içeren veritabanının adı"
```

> 🔹 `DSN`, ODBC sürücü yapılandırmanızda tanımladığınız adla eşleşmelidir.

---

### B. DSN'siz Yapılandırma

#### *digna* Yapılandırması

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdakileri sağlayın:

```
Technology:      MS SQL Server
Database Name:   Kaynak veriyi içeren şema (Schema Name ile aynı)
Schema Name:     Kaynak veriyi içeren şema
Use ODBC:        Etkin
```

#### ODBC Özellikleri

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "sunucu adınız veya IP adresiniz"
name: "UID",        value: "veritabanı kullanıcı adınız"
name: "PWD",        value: "veritabanı şifreniz"
name: "DATABASE",   value: "kaynak veri şemasını içeren veritabanının adı"
```