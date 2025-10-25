---
title: Netezza Bağlayıcısı – Veritabanı Entegrasyonu | digna Dokümantasyonu
description: digna'yı NetezzaSQL ODBC sürücüsünü kullanarak Netezza'ya bağlanacak şekilde yapılandırma. DSN veya DSN-less kurulumlarla parola tabanlı kimlik doğrulamayı destekler.
image: /assets/logo_square.png
---


# Netezza için Kaynak Bağlayıcı

Bu kılavuz, *digna*'yı ODBC sürücüsünü kullanarak Netezza'ya bağlanacak şekilde nasıl yapılandıracağınızı açıklamaktadır.

Ekran **"Veritabanı Bağlantısı Oluştur"** öğesine atıfta bulunmaktadır.

![Veritabanı bağlantısı oluştur](images/data_source_config_input_mask.png)

---

## ODBC Sürücüsü

ODBC sürücüsü çeşitli kimlik doğrulama ve bağlantı seçeneklerini destekleyebilir. Bu bölüm, sürücü **NetezzaSQL** kullanılarak parola tabanlı kimlik doğrulamaya odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Satıcının resmi kurulum kılavuzunu izleyerek **NetezzaSQL** (veya benzeri) sürücüyü yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Parola tabanlı kimlik doğrulamayı kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Adım 1](images/netezza/create_odbc_data_source_step1.png)

Netezza sürücünüze, kurulum ve güvenlik gereksinimlerinize bağlı olarak **Advanced DSN Options**, **SSL DSN Options** veya **Driver Options** sekmelerinde ek bilgiler sağlamanız gerekebilir. En temel kurulum için **DSN Options** bölümüne bilgi girmek genellikle yeterlidir.

**Test Connection** düğmesine tıklayın.

#### Adım 2
![Adım 2](images/netezza/create_odbc_data_source_step2.png)

Başarı ekranını gördüğünüzde, ODBC doğru şekilde yapılandırılmış demektir.

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde yapılandırabilirsiniz; ister **DSN (Data Source Name)** ile ister **DSN-less** bir yapı ile.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdakileri sağlayın:

```
Teknoloji:       Netezza
Veritabanı Adı:  Kaynak şemayı içeren veritabanı
Şema Adı:        Kaynak veriyi içeren şema
ODBC Kullanımı:  Etkin
```

#### ODBC Özellikleri

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "veritabanı kullanıcı adınız"
name: "PWD",        value: "veritabanı parolanız"
```

> 🔹 `DSN`, ODBC sürücü yapılandırmanızda tanımlanan ad ile eşleşmelidir.

---

### B. DSN-less Yapılandırma

#### *digna* Yapılandırması

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdakileri sağlayın:

```
Teknoloji:       Netezza
Veritabanı Adı:  Kaynak veriyi içeren şema (Şema Adı ile aynı)
Şema Adı:        Kaynak veriyi içeren şema
ODBC Kullanımı:  Etkin
```

#### ODBC Özellikleri

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "sunucu adınız veya IP adresi"
name: "PORT",       value: "Port numarası, örn. 5480"
name: "DATABASE",   value: "kaynak veri şemasını içeren veritabanının adı"
name: "UID",        value: "veritabanı kullanıcı adınız"
name: "PWD",        value: "veritabanı parolanız"
```