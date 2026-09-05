# Snowflake için Kaynak Bağlayıcı

Bu kılavuz, *digna*'yı Snowflake'e yerel Python bağlayıcısı veya ODBC sürücüsü kullanarak nasıl bağlayacağınızı açıklar.

Bu, **"Veritabanı Bağlantısı Oluştur"** ekranına atıfta bulunur.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Yerel Python Sürücüsü

**Kütüphane:** `snowflake-connector-python`  
**Desteklenen Kimlik Doğrulama:** Yalnızca parola tabanlı kimlik doğrulama

> Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### *digna* Yapılandırması (Yerel Sürücü)

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdaki bilgileri sağlayın:

```
Technology:      Snowflake
Host Address:    Snowflake hesap adı
Host Port:       Gerekli değil
Database Name:   Kaynak şemayı içeren veritabanı
Schema Name:     Kaynak veriyi içeren şema
User Name:       "user<@>warehouse" formatında kullanıcı adı ve warehouse
User Password:   Kullanıcı parolası
Use ODBC:        Devre Dışı (varsayılan)
```

---

## ODBC Sürücüsü

ODBC sürücüsü, daha geniş bir kimlik doğrulama ve bağlantı seçenekleri yelpazesini destekleyebilir. Bu bölüm, **SnowflakeDSIIDriver** kullanarak parola tabanlı kimlik doğrulamaya odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Vendor'ın resmi yükleme kılavuzunu izleyerek **SnowflakeDSIIDriver**'ı yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Parola tabanlı kimlik doğrulama kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Notlar:
- Database, Schema ve Warehouse için değer sağlamazsanız, bunları *digna* veri kaynağı yapılandırması sırasında ODBC özellikleri olarak sağlamanız gerekecektir.
- "Server" değeri, Snowflake hesap adınızın sonuna ".snowflakecomputing.com" eklenmesiyle oluşur.

#### Adım 2 – Bağlantıyı test etme

**TEST** düğmesine tıklayın. Başarılı bir bağlantı şöyle görünmelidir:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde yapılandırabilirsiniz; ya **DSN (Data Source Name)** ile ya da **DSN'siz** bir kurulumla.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdakileri sağlayın:

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

isteğe bağlı:
name: "Database",       value: "Kaynak şemayı içeren veritabanı"
name: "Schema",         value: "Kaynak veriyi içeren şema"
name: "Warehouse",      value: "SQL'lerin yürütülmesi için kullanılacak warehouse"
```

> `DSN`, ODBC sürücü yapılandırmanızda tanımladığınız adla eşleşmelidir.

---

### B. DSN'siz Yapılandırma

#### *digna* Yapılandırması

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdakileri sağlayın:

```
Technology:      Snowflake
Database Name:   Kaynak veriyi içeren şema (Schema Name ile aynı)
Schema Name:     Kaynak veriyi içeren şema
Use ODBC:        Etkin
```

#### ODBC Özellikleri

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com"
name: "UID",        value: "your snowflake user"
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Kaynak şemayı içeren veritabanı"
name: "Schema",     value: "Kaynak veriyi içeren şema"
name: "Warehouse",  value: "SQL'lerin yürütülmesi için kullanılacak warehouse"
```