# Snowflake için Kaynak Bağlayıcısı

Bu kılavuz, *digna*'nın **DSN'siz** bir bağlantı dizesi kullanarak **ODBC** üzerinden
Snowflake'e bağlanacak şekilde nasıl yapılandırılacağını açıklar.

Kurulumun *digna* tarafı her teknoloji için aynıdır: bağlantıların nerede oluşturulduğu,
özellik değerlerinin nasıl şifrelendiği, bir bağlantının nasıl test edildiği ve profil oluşturma
modlarının ne anlama geldiği. Bunlar [Veritabanı Bağlantılarına Genel Bakış](overview.md)
sayfasında açıklanmıştır. Bu sayfa Snowflake'e özgü konuları ele alır.

---

## 1. ODBC Sürücüsünü Kurun {: #1-install-the-odbc-driver }

[Snowflake'in kurulum kılavuzunu](https://docs.snowflake.com/en/developer-guide/odbc/odbc)
izleyerek *digna* arka ucunu çalıştıran makineye **Snowflake ODBC Driver**'ı kurun.

Sürücü kendini **SnowflakeDSIIDriver** olarak kaydeder. Kayıtlı adın tamamını
[ODBC Sürücüsünü digna Ana Makinesine Kurun](overview.md#install-the-driver) bölümünde
açıklandığı şekilde ana makinenizden okuyun.

---

## 2. ODBC Özellikleri {: #2-odbc-properties }

Snowflake'e bir **programatik erişim token'ı (PAT)** ile erişilir; bu, *digna*'nın doğrulandığı
kimlik doğrulama yolu ve Snowflake'in yalnızca parolayla oturum açmanın engellendiği hesaplar
için şart koştuğu yoldur.

!!! important "Bir örnek, bir şartname değil"

    Aşağıdaki küme, çalıştığı bilinen bir kombinasyondur. Özellikler Snowflake ODBC sürücüsüne
    aittir; bu nedenle adları, varsayılan değerleri ve kabul edilen değerleri sürücü
    sürümlerine ve platformlara göre farklılık gösterir. Hesabınızın hangi kimlik doğrulama
    seçeneklerine izin verdiğine ise hesabın güvenlik politikası karar verir. Bunu bir
    başlangıç noktası olarak kullanın ve kurduğunuz sürücü sürümünün dokümantasyonunu kontrol
    edin.

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | *digna* ana makinesinde kayıtlı sürücü adıyla eşleşmelidir |
| `Server` | `<account>.snowflakecomputing.com` | Hesap tanımlayıcısı ile sonek, ör. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Token'ın ait olduğu Snowflake kullanıcısı |
| `Database` | `TEST` | Kaynak şemaları barındıran veritabanı. Bu bağlantının profilini oluşturabileceği tek veritabanıdır |
| `Schema` | `PUBLIC` | Oturumun varsayılan şeması |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Token kimlik doğrulamasını seçer |
| `token` | `<programmatic access token>` | **Encrypted** seçeneğini işaretleyin |

Ortaya çıkan bağlantı dizesi şöyle görünür:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Warehouse ve rol

Sorgular bir warehouse gerektirir. *digna* kullanıcısının varsayılan bir warehouse'u ve
varsayılan bir rolü varsa oturum bunları kullanır ve hiçbir şeyin yapılandırılması gerekmez.
Aksi takdirde şunları ekleyin:

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Profil oluşturma sorgularını çalıştıran warehouse |
| `Role` | `DIGNA_READER` | Oturumun yetkilerini kullandığı rol |

!!! tip "digna'ya kendi warehouse'unu verin"

    Ayrı, küçük ve otomatik askıya alınan bir warehouse, profil oluşturma maliyetini görünür
    tutar ve *digna*'nın işlem kapasitesi için etkileşimli kullanıcılarla rekabet etmesini
    önler.

### Parola ile kimlik doğrulama

Hesabın hâlâ izin verdiği durumlarda token yerine bir parola da kullanılabilir; `authenticator`
ve `token` özelliklerini kaldırın ve şunu ekleyin:

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `PWD` | `<password>` | **Encrypted** seçeneğini işaretleyin |

---

## 3. *digna* Yapılandırması {: #3-digna-configuration }

**Add DB Connection** ekranında aşağıdakileri girin:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Snowflake ile İlgili Notlar {: #4-notes-on-snowflake }

- **Token'ların süresi dolar.** Programatik erişim token'ı bir geçerlilik süresiyle verilir ve
  süresinin dolduğu gün profil oluşturma durur. Token'ı oluştururken son kullanma tarihini not
  edin ve yeni token'ı `token` özelliğine yeniden girin; şifrelenmiş değerler değiştirilebilir
  ancak geri okunamaz.
- **Bir bağlantı bir veritabanını görür.** *digna*, `Database` içinde adı verilen veritabanının
  şemalarını sunar, çünkü Snowflake katalog olarak yalnızca geçerli veritabanını bildirir.
  Başka bir veritabanındaki kaynak tablolar için ayrı bir bağlantı gerekir.
- **Tanımlayıcılar**, tırnak içinde oluşturulmadıkları sürece **büyük harflidir**. *digna*
  adları Snowflake'in bildirdiği şekilde kullanır.
- **Profil oluşturma modları.** *Permanent* çalışma tablolarını **Work Schema** içinde
  oluşturur, bu nedenle rolün orada `CREATE TABLE` yetkisine ihtiyacı vardır. *Session*
  `CREATE TEMPORARY TABLE` kullanır ve **Work Schema**'ya dokunmaz. *Standard* yalnızca okuma
  erişimi gerektirir ve hiçbir yazma yetkisine ihtiyaç duymaz.

---

## 5. Sürücüyü Doğrulama (isteğe bağlı) {: #5-verifying-the-driver-optional }

DSN'siz bir bağlantı için bir ODBC veri kaynağı yapılandırmak gerekli değildir; ancak sürücünün
kendi iletişim kutusu, bunları *digna*'ya girmeden önce sürücünün, hesap URL'sinin ve kimlik
bilgilerinizin çalıştığını doğrulamanın pratik bir yoludur.

#### Adım 1
![Adım 1](images/snowflake/create_odbc_data_source_step1.png)

Notlar:

- **Server** değeri, Snowflake hesap tanımlayıcınızın ardından gelen
  `.snowflakecomputing.com` kısmından oluşur.
- Burada girilen **Database**, **Schema** ve **Warehouse**, [bölüm 2](#2-odbc-properties)
  içindeki `Database`, `Schema` ve `Warehouse` özelliklerine karşılık gelir.

#### Adım 2 – Bağlantıyı test edin

**TEST** düğmesine tıklayın. Başarılı bir bağlantı şöyle görünmelidir:

![Adım 2](images/snowflake/create_odbc_data_source_step2.png)