---
title: Azure Synapse Bağlayıcısı – Veritabanı Entegrasyonu | digna Dokümantasyonu
description: digna'yı, yerel Python sürücüsü veya ODBC sürücüsü kullanarak Azure Synapse Analytics'e bağlanacak şekilde yapılandırın. Hem sunucusuz hem de özel SQL havuzlarını destekler.
image: /assets/logo_square.png
---


# Azure Synapse Analytics İçin Kaynak Bağlayıcı

Bu kılavuz, *digna*'yı yerel Python bağlayıcısı veya ODBC sürücüsü kullanarak Azure Synapse Analytics'e bağlanacak şekilde nasıl yapılandıracağınızı açıklar.
Hem sunucusuz hem de özel SQL havuzlarını destekler.

Bu kılavuz **"Veritabanı Bağlantısı Oluştur"** ekranına atıfta bulunur.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Yerel Python Sürücüsü

**Kütüphane:** `pymssql`  
**Desteklenen Kimlik Doğrulama:** Sadece parola tabanlı kimlik doğrulama

> Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### *digna* Yapılandırması (Yerel Sürücü)

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdaki bilgileri sağlayın:

```
Teknoloji:        MS SQL Server
Host Adresi:      <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Portu:       Port numarası, örn. 1433
Veritabanı Adı:   Veritabanı adı
Şema Adı:         Kaynak veriyi içeren şema
Kullanıcı Adı:    Veritabanı kullanıcı adı
Kullanıcı Parolası: Kullanıcının parolası
ODBC Kullan:      Devre Dışı (varsayılan)
```

---

## ODBC Sürücüsü

ODBC sürücüsü daha geniş bir kimlik doğrulama ve bağlantı seçenekleri yelpazesini destekleyebilir. Bu bölüm, **ODBC Driver 18 for SQL Server** sürücüsünü kullanarak parola tabanlı kimlik doğrulamaya odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Satıcının resmi kurulum kılavuzunu izleyerek **ODBC Driver 18 for SQL Server** (veya benzeri) sürücüsünü yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Parola tabanlı kimlik doğrulamayı kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

"Server" alanını doldurun.
Synapse çalışma alanı adını kullanın ve sonuna ".sql.azuresynapse.net" ekleyin.  
**Dikkat**, sunucusuz bir SQL havuzu ile bağlanmak istiyorsanız, aşağıdaki ekran görüntüsünde gösterildiği gibi "-ondemand" eklediğinizden emin olun.

**Next >** düğmesine tıklayın.

#### Adım 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Kimlik doğrulama yöntemini seçin (ör. kullanıcı adı ve parola) ve gerekli bilgileri girin.

**Next >** düğmesine tıklayın.

#### Adım 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

ANSI uyumlu ayarları seçin, ardından **Next >** düğmesine tıklayın.

#### Adım 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Varsayılan ayarları bırakabilir veya ihtiyaca göre seçenekler belirleyebilirsiniz ve **Finish** düğmesine tıklayın.

#### Adım 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Şimdi **Test datasource** butonuna tıklayın.

#### Adım 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Başarı ekranını aldığınızda, ODBC düzgün şekilde yapılandırılmış demektir.

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde yapılandırabilirsiniz; ya bir **DSN (Data Source Name)** ile ya da **DSN'siz (DSN-less)** bir kurulumla.

---

### A. DSN-Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdakileri sağlayın:

```
Teknoloji:        MS SQL Server
Veritabanı Adı:   Kaynak şemayı içeren veritabanı
Şema Adı:         Kaynak veriyi içeren şema
ODBC Kullan:      Etkin
```

#### ODBC Özellikleri

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "veritabanı kullanıcı adınız"
name: "PWD",        value: "veritabanı parolanız"
name: "DATABASE",   value: "kaynak verinin şemasını içeren veritabanı adı"
```

> `DSN`, ODBC sürücü yapılandırmanızda tanımlı olan adla eşleşmelidir.

---

### B. DSN'siz Yapılandırma

#### *digna* Yapılandırması

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdakileri sağlayın:

```
Teknoloji:        MS SQL Server
Veritabanı Adı:   Kaynak veriyi içeren şema (Şema Adı ile aynı)
Şema Adı:         Kaynak veriyi içeren şema
ODBC Kullan:      Etkin
```

#### ODBC Özellikleri

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "veritabanı kullanıcı adınız"
name: "PWD",        value: "veritabanı parolanız"
name: "DATABASE",   value: "kaynak verinin şemasını içeren veritabanı adı"
```

**Not** SERVER özelliği ile ilgili:  
Synapse çalışma alanı adını kullanın ve sonuna ".sql.azuresynapse.net" ekleyin. Sunucusuz bir SQL havuzu ile bağlanmak istiyorsanız, aşağıdaki ekran görüntüsünde gösterildiği gibi "-ondemand" eklediğinizden emin olun.