---
title: PostgreSQL Bağlayıcısı – Veritabanı Entegrasyonu | digna Belgeleri
description: digna'yı psycopg Python sürücüsü veya PostgreSQL ODBC sürücüsünü kullanarak PostgreSQL'e bağlanacak şekilde yapılandırın. DSN veya DSN'siz kurulumlarla parola tabanlı kimlik doğrulamayı destekler.
image: /assets/logo_square.png
---


# PostgreSQL için Kaynak Bağlayıcı

Bu kılavuz, *digna*'yı yerel Python bağlayıcısı veya ODBC sürücüsünü kullanarak Postgres'e nasıl bağlanacak şekilde yapılandıracağınızı açıklar.

Ekran **"Create a Database Connection"**'a atıfta bulunmaktadır.

![Veritabanı bağlantısı oluştur](images/data_source_config_input_mask.png)

---

## Yerel Python Sürücüsü

**Kütüphane:** `psycopg`  
**Desteklenen Kimlik Doğrulama:** Yalnızca parola tabanlı kimlik doğrulama

> ⚠️ Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### *digna* Yapılandırması (Yerel Sürücü)

**"Create a Database Connection"** ekranında aşağıdaki bilgileri sağlayın:

```
Technology:      Postgres
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 5432
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Sürücüsü

ODBC sürücüsü daha geniş bir kimlik doğrulama ve bağlantı seçenekleri yelpazesini destekleyebilir. Bu bölüm, sürücü **PostgreSQL Unicode(x64)** kullanılarak parola tabanlı kimlik doğrulamaya odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Vendorsanın resmi kurulum kılavuzunu takip ederek **PostgreSQL Unicode(x64)** (veya benzeri) sürücüyü yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Parola tabanlı kimlik doğrulamayı kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Adım 1](images/postgres/create_odbc_data_source_step1.png)

Not: Veritabanı kurulumunuz belirli bir "SSLMode" seçmenizi gerektiriyorsa, lütfen DSN'siz bir yapılandırma tanımlarken de bunu kullanın.

#### Adım 2 – Bağlantıyı test edin

**Test Connection** düğmesine tıklayın.

![Adım 2](images/postgres/create_odbc_data_source_step2.png)

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde, ya **DSN (Data Source Name)** ile ya da **DSN'siz** bir kurulumla yapılandırabilirsiniz.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri sağlayın:

```
Technology:      PostgreSQL
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Özellikleri

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 `DSN`, ODBC sürücü yapılandırmanızda tanımlı olan ad ile eşleşmelidir.

---

### B. DSN'siz Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri sağlayın:

```
Technology:      PostgreSQL
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Özellikleri

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```