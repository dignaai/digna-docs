---
title: MS SQL Server Bağlayıcısı – Veritabanı Entegrasyonu | digna Dokümantasyonu
description: digna'nın pymssql Python sürücüsü veya SQL Server ODBC sürücüsü kullanarak Microsoft SQL Server'a bağlanacak şekilde yapılandırılmasını sağlayın. DSN veya DSN'siz kurulumlarla parola tabanlı kimlik doğrulamayı destekler.
image: /assets/logo_square.png
---


# MS SQL Server için Kaynak Bağlayıcı

Bu kılavuz, *digna*'nın SQL Server'a yerel Python bağlayıcısı veya ODBC sürücüsü kullanarak nasıl bağlanacağının yapılandırılmasını açıklar.

Bu kılavuz **"Create a Database Connection"** ekranına atıfta bulunur.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Yerel Python Sürücüsü

**Kütüphane:** `pymssql`  
**Desteklenen Kimlik Doğrulama:** Yalnızca parola tabanlı kimlik doğrulama

> ⚠️ Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### *digna* Yapılandırması (Yerel Sürücü)

Şu bilgileri **"Create a Database Connection"** ekranında sağlayın:

```
Technology:      MS SQL Server
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Sürücüsü

ODBC sürücüsü daha geniş bir kimlik doğrulama ve bağlantı seçenekleri yelpazesini destekleyebilir. Bu bölüm, parola tabanlı kimlik doğrulamasına odaklanır ve **SQL Server** sürücüsünü kullanır.

### 1. ODBC Sürücüsünü Yükleyin

Tedarikçinin resmi kurulum kılavuzunu izleyerek **SQL Server** (veya benzeri) sürücüsünü yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Parola tabanlı kimlik doğrulama kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

**Next >** düğmesine tıklayın.

#### Adım 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Kimlik doğrulama yöntemini seçin (ör. kullanıcı adı ve parola) ve gerekli bilgileri girin.

**Next >** düğmesine tıklayın.

#### Adım 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

ANSI uyumlu ayarları seçin, ardından **Next >** düğmesine tıklayın.

#### Adım 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Varsayılan ayarları bırakabilir veya ihtiyaç duyduğunuzda kayıt (logging) seçeneklerini seçip **Finish** düğmesine tıklayabilirsiniz.

#### Adım 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Şimdi **Test datasource** düğmesine tıklayın.

#### Adım 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

Başarı ekranını aldığınızda ODBC düzgün şekilde yapılandırılmış demektir.

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde yapılandırabilirsiniz; bu ya bir **DSN (Data Source Name)** ile ya da **DSN'siz** bir kurulumla yapılabilir.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında şu bilgileri sağlayın:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Özellikleri

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 `DSN` ODBC sürücü yapılandırmanızda tanımlanan ad ile eşleşmelidir.

---

### B. DSN'siz Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında şu bilgileri sağlayın:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Özellikleri

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```