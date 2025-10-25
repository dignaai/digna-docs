---
title: Snowflake Bağlayıcısı – Veritabanı Entegrasyonu | digna Documentation
description: digna'yı Python bağlayıcısı veya Snowflake ODBC sürücüsü kullanarak Snowflake'e bağlanacak şekilde yapılandırın. DSN veya DSN'siz kurulumlarla parola tabanlı kimlik doğrulamayı destekler.
image: /assets/logo_square.png
---


# Snowflake için Kaynak Bağlayıcı

Bu kılavuz, *digna*'yı yerel Python bağlayıcısı veya ODBC sürücüsü kullanarak Snowflake'e nasıl bağlayacağınızı açıklar.

Bu belge **"Create a Database Connection"** ekranına atıfta bulunur.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Yerel Python Sürücüsü

**Kütüphane:** `snowflake-connector-python`  
**Desteklenen Kimlik Doğrulama:** Yalnızca parola tabanlı kimlik doğrulama

> ⚠️ Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### *digna* Yapılandırması (Yerel Sürücü)

**"Create a Database Connection"** ekranında aşağıdaki bilgileri sağlayın:

```
Technology:      Snowflake
Host Address:    Snowflake hesap adı
Host Port:       Gerekli değil
Database Name:   Kaynak şemayı içeren veritabanı
Schema Name:     Kaynak veriyi içeren şema
User Name:       "user<@>warehouse" formatında kullanıcı adı ve warehouse
User Password:   Kullanıcı için parola
Use ODBC:        Devre dışı (varsayılan)
```

---

## ODBC Sürücüsü

ODBC sürücüsü daha geniş bir kimlik doğrulama ve bağlantı seçenekleri yelpazesini destekleyebilir. Bu bölüm, **SnowflakeDSIIDriver** kullanarak parola tabanlı kimlik doğrulamaya odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Vendor'un resmi kurulum kılavuzunu izleyerek **SnowflakeDSIIDriver**'ı yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Parola tabanlı kimlik doğrulama kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Notlar: 
- Database, Schema ve Warehouse için değer sağlamazsanız, bunları *digna* veri kaynağı yapılandırması sırasında ODBC özellikleri olarak sağlamanız gerekecektir.
- "Server" değeri, snowflake hesap adınızın sonuna ".snowflakecomputing.com" eklenmesiyle oluşur.

#### Adım 2 – Bağlantıyı test edin

**TEST** düğmesine tıklayın. Başarılı bir bağlantı şöyle görünmelidir:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde yapılandırabilirsiniz; ya bir **DSN (Data Source Name)** ile ya da **DSN'siz** bir kurulumla.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri sağlayın:

```
Technology:      Snowflake
Database Name:   Kaynak şemayı içeren veritabanı
Schema Name:     Kaynak veriyi içeren şema
Use ODBC:        Etkin
```

#### ODBC Özellikleri

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{parolanız süslü parantez içinde}"

isteğe bağlı olarak:
name: "Database",       value: "Kaynak şemayı içeren veritabanı"
name: "Schema",         value: "Kaynak veriyi içeren şema"
name: "Warehouse",      value: "SQL'lerin yürütülmesi için kullanılacak warehouse"
```

> 🔹 `DSN`, ODBC sürücü yapılandırmanızda tanımlı olan ad ile eşleşmelidir.

---

### B. DSN'siz Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri sağlayın:

```
Technology:      Snowflake
Database Name:   Kaynak veriyi içeren şema (Schema Name ile aynı)
Schema Name:     Kaynak veriyi içeren şema
Use ODBC:        Etkin
```

#### ODBC Özellikleri

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Kaynak şemayı içeren veritabanı"
name: "Schema",     value: "Kaynak veriyi içeren şema"
name: "Warehouse",  value: "SQL'lerin yürütülmesi için kullanılacak warehouse"
```