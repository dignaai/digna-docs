# Oracle için Kaynak Bağlayıcı

Bu kılavuz, *digna*'yı yerel Python bağlayıcısı veya ODBC sürücüsü kullanarak Oracle veritabanına nasıl bağlanacak şekilde yapılandıracağınızı açıklar.

Bu, **"Create a Database Connection"** ekranına atıfta bulunur.

![Veritabanı bağlantısı oluştur](images/data_source_config_input_mask.png)

---

## Yerel Python Sürücüsü

**Kütüphane:** `python-oracledb`  
**Desteklenen Kimlik Doğrulama:** Yalnızca parola tabanlı kimlik doğrulama

> Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### *digna* Yapılandırması (Yerel Sürücü)

Aşağıdaki bilgileri **"Create a Database Connection"** ekranında sağlayın:

```
Teknoloji:        Oracle
Sunucu Adresi:    Sunucu adı veya IP adresi
Sunucu Portu:     Port numarası, örn. 1521
Veritabanı Adı:   Örnek adı, servis adı
Şema Adı:         Kaynak veriyi içeren şema
Kullanıcı Adı:    Veritabanı kullanıcı adı
Kullanıcı Parolası: Kullanıcının parolası
ODBC Kullanımı:   Devre Dışı (varsayılan)
```

---

## ODBC Sürücüsü

ODBC sürücüsü, daha geniş bir kimlik doğrulama ve bağlantı seçenekleri yelpazesini destekleyebilir. Bu bölüm, **Oracle in OraDB21Home1** sürücüsünü kullanarak parola tabanlı kimlik doğrulamaya odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

**Oracle in OraDB21Home1** (veya benzeri) sürücüsünü satıcının resmi kurulum kılavuzunu izleyerek yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Parola tabanlı kimlik doğrulama kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Adım 1](images/oracle/create_odbc_data_source_step1.png)

Not:
TNS Service Name, Oracle istemci kurulumunuzdaki tnsnames.ora dosyasında yapılandırılmalıdır. Bağlantı tanımlayıcısını (host, port, servis adı) burada sağlarsınız.

#### Adım 2 – Bağlantıyı test et

**Test Connection** düğmesine tıklayın.

![Adım 2](images/oracle/create_odbc_data_source_step2.png)

Parolayı girin ve **OK** düğmesine tıklayın.

![Adım 2](images/oracle/create_odbc_data_source_step3.png)

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde yapılandırabilirsiniz; ya bir **DSN (Data Source Name)** ile ya da **DSN'siz** bir kurulumla.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri sağlayın:

```
Teknoloji:        Oracle
Veritabanı Adı:   Kaynağın şemasını içeren veritabanı
Şema Adı:         Kaynak veriyi içeren şema
ODBC Kullanımı:   Etkin
```

#### ODBC Özellikleri

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "Oracle kullanıcı adınız"
name: "PWD",            value: "{şifreniz süslü parantez içinde}"
```

> `DSN`, ODBC sürücü yapılandırmanızda tanımlı olan ad ile eşleşmelidir.

---

### B. DSN'siz Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri sağlayın:

```
Teknoloji:        Oracle
Veritabanı Adı:   Kaynak veriyi içeren şema (Schema Name ile aynıdır)
Şema Adı:         Kaynak veriyi içeren şema
ODBC Kullanımı:   Etkin
```

#### ODBC Özellikleri

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "Oracle kullanıcı adınız"
name: "PWD",        value: "Oracle parolanız"
```