# Netezza için Kaynak Bağlayıcı

Bu kılavuz, *digna*'yı ODBC sürücüsü kullanarak Netezza'ya bağlanacak şekilde nasıl yapılandıracağınızı açıklar.

Bu belge **"Veritabanı Bağlantısı Oluştur"** ekranına atıfta bulunur.

![Veritabanı bağlantısı oluştur](images/data_source_config_input_mask.png)

---

## ODBC Sürücüsü

ODBC sürücüsü çeşitli kimlik doğrulama ve bağlantı seçeneklerini destekleyebilir. Bu bölüm, sürücü **NetezzaSQL** kullanılarak parola tabanlı kimlik doğrulamaya odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Satıcının resmi kurulum kılavuzunu izleyerek **NetezzaSQL** (veya benzeri) sürücüyü yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Parola tabanlı kimlik doğrulama kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Adım 1](images/netezza/create_odbc_data_source_step1.png)

Netezza sürücünüze, kurulum ve güvenlik gereksinimlerinize bağlı olarak, **Advanced DSN Options**, **SSL DSN Options** veya **Driver Options** sekmelerinde de veri sağlamanız gerekebilir. En basit kurulum için **DSN Options** sekmesine veri sağlamak yeterlidir.

**Test Connection** düğmesine tıklayın.

#### Adım 2
![Adım 2](images/netezza/create_odbc_data_source_step2.png)

Başarı ekranını aldığınızda, ODBC doğru şekilde yapılandırılmış demektir.

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde yapılandırabilirsiniz; bu ya **DSN (Data Source Name)** ile ya da **DSN-less** bir kurulumla yapılabilir.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdakileri sağlayın:

```
Technology:      Netezza
Database Name:   Kaynak şemayı içeren veritabanı
Schema Name:     Kaynak veriyi içeren şema
Use ODBC:        Etkin
```

#### ODBC Özellikleri

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "veritabanı kullanıcı adınız"
name: "PWD",        value: "veritabanı parolanız"
```

> `DSN`, ODBC sürücü yapılandırmanızda tanımlı olan ad ile eşleşmelidir.

---

### B. DSN-less Yapılandırma

#### *digna* Yapılandırması

**"Veritabanı Bağlantısı Oluştur"** ekranında aşağıdakileri sağlayın:

```
Technology:      Netezza
Database Name:   Kaynağı içeren veritabanın adı (Schema Name ile aynı)
Schema Name:     Kaynak veriyi içeren şema
Use ODBC:        Etkin
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