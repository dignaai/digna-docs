# Veritabanı Bağlantılarına Genel Bakış

---

## İçindekiler

1. [Bağlantılar Nasıl Çalışır](#how-connections-work)
2. [Teknoloji Kılavuzları](#technology-guides)
3. [Ön Koşul: ODBC Sürücüsünü digna Ana Makinesine Kurun](#install-the-driver)
4. [Veritabanı Bağlantısı Oluşturma](#create-a-database-connection)
5. [ODBC Özellikleri](#odbc-properties)
6. [Özellik Değerlerini Şifreleme](#encrypting-property-values)
7. [Bir Bağlantıyı Test Etme](#testing-a-connection)
8. [Bağlantının Gördüğü Veritabanı](#which-database-the-connection-sees)
9. [Profil Oluşturma Modu ve Çalışma Şeması](#profiling-mode-and-work-schema)
10. [Bunun Yerine DSN Kullanma](#using-a-dsn-instead)
11. [Sorun Giderme](#troubleshooting)

---

## Bağlantılar Nasıl Çalışır {: #how-connections-work }

*digna* her kaynak teknolojiye **ODBC** üzerinden erişir. Bir bağlantı, anahtar/değer çiftleri
olarak girdiğiniz ODBC özelliklerinin bir listesidir. *digna* bağlantıyı açtığında bu çiftleri
bir bağlantı dizesinde birleştirir (`Key=Value`, `;` ile ayrılmış, listelediğiniz sırayla) ve
bunu *digna* ana makinesindeki ODBC sürücü yöneticisine iletir.

Özellikleri kendiniz girmeniz kurulumu **DSN'siz** kılar: bağlantı, sürücünün ihtiyaç duyduğu
her şeyi taşır, bu nedenle ana makinede herhangi bir ODBC veri kaynağının (DSN) kaydedilmesi
gerekmez. Bağlantı tanımı tamamen *digna* içinde bulunduğu ve onunla birlikte taşındığı için
*digna*'yı yapılandırmanın önerilen yolu budur.

### Neden ODBC {: #why-odbc }

Önceki sürümler, **Use ODBC** anahtarıyla seçilen, teknolojiye özel bir sürücü ile ODBC
arasında seçim sunuyordu. Release 2026.06 itibarıyla *digna* yalnızca ODBC üzerine kuruludur.
Tek ve standart bir arayüz, bir dizi özel sürücünün sunabileceğinden fazlasını sağlar:

- **Kimlik doğrulama**: kimlik doğrulama ODBC'nin bir parçasıdır, bu nedenle bir bağlantı
  sürücüsünün desteklediği her yöntemi kullanabilir: parolalar, token'lar ve PAT'ler, Kerberos
  ve Active Directory, MFA ve tarayıcı tabanlı çoklu oturum açma, bulut kimliği, istemci
  sertifikaları ve TLS. Yeni yöntemler bir *digna* sürümünü beklemeden sürücü güncellemesiyle
  gelir.
- **Veritabanı üreticileri tarafından bakımı yapılan sürücüler**: üreticinin kendi sürücüsü
  yeni sunucu sürümlerini ve güvenlik düzeltmelerini takip eder; siz de onu *digna*'dan
  bağımsız olarak kendi takviminize göre güncelleyebilirsiniz.
- **Her şeyi yapılandırmanın tek yolu**: her kaynak için farklı bir alan kümesi yerine, her
  teknoloji aynı arayüze, hassas değerlerin aynı şekilde şifrelenmesine ve aynı sorun giderme
  yöntemine sahip bir anahtar/değer özellikleri listesidir.
- **İnce ayar ve kapsam**: zaman aşımları, TLS ayarları, proxy'ler ve getirme boyutları gibi
  sürücü düzeyindeki seçenekler her kaynak için kullanılabilir ve uyumlu bir ODBC sürücüsüne
  sahip her teknoloji bağlanabilir; *digna*'nın özel bir kılavuz yayımlamadığı teknolojiler de
  buna dahildir.

!!! note "Arayüzde neler değişti"

    **Use ODBC** anahtarı ile ayrı ana makine, port, veritabanı, kullanıcı ve parola alanları
    artık mevcut değildir. Henüz ODBC kullanmayan bir bağlantının yeniden çalışabilmesi için
    ODBC özelliklerinin girilmesi gerekir; bkz.
    [Veritabanı Bağlantısı Oluşturma](#create-a-database-connection).

---

## Teknoloji Kılavuzları {: #technology-guides }

Özellik adları sürücüye göre farklılık gösterir ve her teknolojinin diğerlerinde bulunmayan bir
veya iki ayrıntısı vardır. Aşağıdaki kılavuzlar bu kısmı kapsar; bu sayfa ise hepsi için aynı
olan *digna* tarafını ele alır.

!!! important "Kılavuzlardaki özellik kümeleri örnektir"

    Her kılavuz çalıştığı bilinen bir kombinasyonu, yani *digna*'nın test edildiği kombinasyonu
    gösterir. Bu bir şartname değil, bir başlangıç noktasıdır: özellikler ODBC sürücüsüne
    aittir ve hangilerinin mevcut olduğu, nasıl adlandırıldıkları ve hangi değerleri kabul
    ettikleri sürücü sürümlerine ve üreticilere, Windows, Linux ve macOS arasında ve kaynak
    sunucunun nasıl yapılandırıldığına (kimlik doğrulama yöntemi, TLS, ağ geçidi, port) göre
    farklılık gösterir. Bir iki değeri ayarlamanız gerekebileceğini göz önünde bulundurun ve
    kurduğunuz sürücü sürümünün dokümantasyonunu esas alın.

| Teknoloji | Kılavuz | Bilinmesi gerekenler |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Sunucusuz havuzlar ana makine adında `-ondemand` gerektirir ve yalnızca *Standard* profil oluşturmayı destekler |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Token kimlik doğrulaması: `UID=token`, PAT `PWD` içinde |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Kataloglar bir sorgudan değil, sürücüden gelir |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Sürücü adı süslü parantez içindedir: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` ya tam bir bağlantı tanımlayıcısı ya da bir `tnsnames.ora` takma adı alır |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode`, sunucunun talep ettiğiyle eşleşmelidir |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Test edilen kimlik doğrulama yolu programatik erişim token'ıdır |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | *digna*'nın hangi şemaları görebileceğini `DATABASE` belirler |
| **Teradata** | [Teradata](teradata_connector_guide.md) | Ana makine `DBCNAME` içine yazılır; veritabanları şema işlevi görür |

---

## Ön Koşul: ODBC Sürücüsünü digna Ana Makinesine Kurun {: #install-the-driver }

*digna* kaynak bağlantılarını tarayıcıdan değil, **digna arka ucunu çalıştıran sunucudan**
açar. Bu nedenle ODBC sürücüsünün o makineye kurulması ve adının yerel sürücü yöneticisine
kaydedilmesi gerekir.

=== "Windows"

    Üreticinin 64 bit sürücüsünü kurun, ardından **ODBC Data Source Administrator (64-bit)**
    uygulamasını açın ve **Drivers** sekmesine geçin. Orada listelenen adlar, `Driver` özelliği
    için kullanabileceğiniz değerlerin tam olarak kendisidir.

=== "Linux"

    **unixODBC**'yi ve üreticinin sürücüsünü kurun, ardından kayıtlı sürücü adlarını listeleyin:

    ```bash
    odbcinst -q -d
    ```

    Köşeli parantez içinde yazdırılan adlar, `Driver` özelliği için kullanabileceğiniz
    değerlerdir. Bunlar `/etc/odbcinst.ini` dosyasından (veya `odbcinst -j` komutunun bildirdiği
    dosyadan) gelir.

=== "macOS"

    **unixODBC**'yi (örneğin `brew install unixodbc` ile) ve üreticinin sürücüsünü kurun,
    ardından kayıtlı sürücü adlarını listeleyin:

    ```bash
    odbcinst -q -d
    ```

!!! warning "Sürücü adı karakteri karakterine eşleşmelidir"

    `Driver` sürücü yöneticisine değiştirilmeden iletilir. Sürücü yöneticisi açısından
    `Simba Spark ODBC Driver` ve `Simba Spark ODBC Driver 64` farklı sürücülerdir; kayıtlı
    olmayan bir ad, ortada hiçbir DSN olmamasına rağmen *data source name not found* hatasına
    yol açar.

Kayıtlı bir ad yerine, yaygın sürücü yöneticilerinin tümü sürücü kitaplığının tam yolunu da
kabul eder; örneğin `Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. Bu, sürücü kurulu
olduğu halde kayıtlı olmadığında kullanışlıdır.

---

## Veritabanı Bağlantısı Oluşturma {: #create-a-database-connection }

**Admin Panel**'i açın, **Database Connections** sekmesine gidin ve **Add DB Connection**'a
tıklayın. Ekran beş bilgi ister:

| Alan | Açıklama |
|---|---|
| **Name** | Bağlantının adı. Bağlantıya diğer ekranlarda başvurmak için kullanılır. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake veya Hive. *digna*'nın ürettiği SQL lehçesini seçer, bu nedenle sürücüyle değil kaynakla eşleşmelidir. Azure Synapse Analytics bir **SQL Server** bağlantısıdır. |
| **ODBC Properties** | [ODBC Özellikleri](#odbc-properties) bölümünde açıklanan anahtar/değer çiftleri. |
| **Profiling Mode** | *Standard*, *Permanent* veya *Session*; bkz. [Profil Oluşturma Modu ve Çalışma Şeması](#profiling-mode-and-work-schema). |
| **Work Schema** | *Permanent* profil oluşturma için çalışma tablolarını barındıran şema. |

Bir bağlantı merkezi olarak yönetilir ve ardından bir veya daha fazla projeye atanır; böylece
aynı bağlantı birden çok projeye hizmet edebilir.

---

## ODBC Özellikleri {: #odbc-properties }

Her özellik için **Add Property**'ye tıklayın ve **Key**, **Value** alanlarını ve gizli
değerler için **Encrypted** onay kutusunu doldurun. Her teknoloji kılavuzu, o teknoloji için
sürücü sürümünüze ve sunucunuza uyarlayacağınız bir örnek küme listeler; bkz.
[yukarıdaki not](#technology-guides).

Sürücü ne olursa olsun, bir özellik kümesi aynı dört şeyi kapsar:

- **`Driver`**: [yukarıda](#install-the-driver) açıklandığı şekilde kayıtlı sürücü adı.
- **Sunucunun adresi**: anahtar sürücüye göre değişir: `SERVER`, `HOST`, `DBCNAME`,
  `Server` veya Oracle için `DBQ` bağlantı tanımlayıcısı.
- **Kimlik bilgileri**: genellikle `UID` ve `PWD`; Snowflake `UID` ile birlikte bir `token`
  kullanır, Databricks ise `token` değişmez kullanıcı adını ve `PWD` içinde kişisel erişim
  token'ını kullanır.
- **Üzerinde çalışılacak veritabanı veya katalog** (teknolojide varsa); bkz.
  [Bağlantının Gördüğü Veritabanı](#which-database-the-connection-sees).

Sürücünün belgelediği diğer her şey de aynı şekilde eklenebilir: bağlantı havuzu, soket zaman
aşımları, Kerberos ayarları, proxy ayarları. *digna* özellikleri yorumlamaz; yalnızca iletir.

!!! warning "Değerler kaçış karakteriyle işlenmez; noktalı virgül içeren her şeyi süslü paranteze alın"

    Özellikler `;` ile birleştirildiğinden, kendisi `;` içeren bir değer bağlantı dizesini
    yanlış yerden böler. Bu tür değerleri süslü parantez içine alın: `PWD={p@ss;word}`.
    Aynısı `=` veya baştaki boşluklar içeren değerler için de geçerlidir. Bazı sürücülerin
    geleneksel olarak `{NetezzaSQL}` veya `{SnowflakeDSIIDriver}` gibi süslü parantezle
    yazılmasının nedeni de budur.

---

## Özellik Değerlerini Şifreleme {: #encrypting-property-values }

Gizli bir değer tutan her özellik için **Encrypted** seçeneğini işaretleyin: `PWD`, `token`,
bir istemci gizli anahtarı. Değer bu durumda *digna* deposunda saklanmadan önce şifrelenir,
ekranda maskelenir ve yalnızca bağlantı dizesi oluşturulurken şifresi çözülür.

!!! tip "İpucu"

    Şifrelenmiş bir değer ne kullanıcı arayüzünde ne de API üzerinden geri okunabilir; yalnızca
    değiştirilebilir. Gizli bilgileri kendi parola yöneticinizde de saklayın.

Gizli olmayan özellikleri (sürücü adı, ana makine, port, veritabanı) şifrelemeden bırakmak en
iyisidir; böylece bağlantının bakımını daha sonra yapacak kişi için okunabilir kalırlar.

---

## Bir Bağlantıyı Test Etme {: #testing-a-connection }

Kaydetmeden **önce** *Add DB Connection* iletişim kutusunda **Test**'e tıklayın. Test, o anda
formda bulunan değerleri kullanır ve gerçek bir bağlantı kurar; bu nedenle bir incelemenin
karşılaşacağı sorunu tam olarak bildirir: yanlış bir sürücü adı, reddedilen bir parola,
erişilemeyen bir ana makine. Hiçbir şey saklanmaz: test bağlantısı başarılı da olsa başarısız
da olsa geri alınır.

Zaten var olan bir bağlantıyı yeniden test etmek için **Database Connections** sekmesinde
satırının üzerine gelin ve **fiş** simgesine tıklayın. Bu, bir parola değişikliğinden veya
güvenlik duvarı değişikliğinden sonra bir kaynağa erişilip erişilemediğini kontrol etmenin en
hızlı yoludur.

---

## Bağlantının Gördüğü Veritabanı {: #which-database-the-connection-sees }

Bir veri kaynağı eklediğinizde *digna*, bağlantının erişebildiği katalogları, şemaları ve
tabloları sunar. Bu erişimin ne kadar geniş olduğu teknolojiye bağlıdır:

| Teknoloji | Sunulan kataloglar |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Yalnızca bağlantının **geçerli** veritabanı |
| **Teradata**, **Netezza**, **Databricks** | Kullanıcının görmesine izin verilen tüm veritabanları veya kataloglar |
| **Hive**, **Impala** | Sürücü tarafından bildirilir |

!!! important "Bir bağlantı, bir veritabanı"

    PostgreSQL, SQL Server, Oracle ve Snowflake için özellikler kaynak şemaları barındıran
    veritabanını göstermelidir: `DATABASE=…`, `Database=…` veya Oracle'ın `DBQ` içindeki hizmet
    adı. Başka bir veritabanındaki tablolara bu bağlantı üzerinden erişilemez; onun için ikinci
    bir bağlantı ekleyin.

---

## Profil Oluşturma Modu ve Çalışma Şeması {: #profiling-mode-and-work-schema }

Profil oluşturma modu, *digna*'nın verileri nasıl işlediğini ve metrikleri nasıl hesapladığını
belirler:

- **Standard:** Metrikler, veriler kopyalanmadan doğrudan kaynak tablolar üzerinde hesaplanır.
- **Permanent:** İncelenen güne ait veriler kalıcı bir tabloya kopyalanır ve metrikler
  kopyalanan veriler üzerinde hesaplanır.
- **Session:** Veriler bir oturum tablosuna veya geçici tabloya kopyalanır ve metrikler bu
  geçici veriler üzerinde hesaplanır.

Mod, bağlantı kullanıcısının neleri yapabilmesi gerektiğini belirler:

| Mod | Yazılanlar | Bağlantı kullanıcısının ihtiyaç duyduğu haklar |
|---|---|---|
| **Standard** | hiçbir şey | Kaynak tablolarda okuma |
| **Permanent** | **Work Schema** içinde veri kaynağı başına bir tablo | **Work Schema** içinde tablo oluşturma ve silme |
| **Session** | veritabanının oturumla birlikte sildiği geçici bir tablo | Geçici tablo oluşturma; **Work Schema** kullanılmaz |

*Standard* yalnızca okuma yapar; bu da onu *digna*'ya salt okunur erişim verildiğinde
seçilecek mod yapar. **Work Schema** yalnızca *Permanent* için okunur, ancak mod daha sonra
değiştirilirse bağlantının çalışmaya devam etmesi için yine de doldurulmaya değer.

---

## Bunun Yerine DSN Kullanma {: #using-a-dsn-instead }

Bir DSN hâlâ çalışır; `DSN` yalnızca başka bir özelliktir:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

DSN, *digna* ana makinesinde, *digna* arka ucunu çalıştıran kullanıcı hesabı için ve *digna*
bir hizmet olarak çalıştığında **System DSN** olarak kaydedilmelidir. DSN'de yapılandırılan
her şey, ayrıca bir özellik olarak eklenerek geçersiz kılınabilir.

DSN'siz yöntem, ana makine tarafındaki bu durumdan kaçındığı için belgelenen varsayılandır:
bağlantı tamamen *digna* içinde tanımlanır ve yeni bir *digna* ana makinesinde sürücünün kurulu
olması yeterlidir, başka bir şeyin yapılandırılması gerekmez.

---

## Sorun Giderme {: #troubleshooting }

### Veri kaynağı adı bulunamadı / varsayılan sürücü belirtilmedi

**Belirtiler:**
- **Test** düğmesi, kurulum DSN'siz olmasına rağmen *data source name not found* ifadesini
  içeren bir hata bildiriyor

**Nedenler ve Çözümler:**
1. `Driver` değeri kayıtlı bir sürücü adıyla eşleşmiyor; bunu
   *ODBC Data Source Administrator (64-bit)* uygulamasının **Drivers** sekmesiyle veya
   `odbcinst -q -d` çıktısıyla karşılaştırın
2. Sürücü iş istasyonunuzda kurulu, ancak *digna* ana makinesinde kurulu değil
3. *digna* 64 bit iken sürücü 32 bit; 64 bit sürücüyü kurun
4. `Driver` özelliği tamamen eksik ve bir `DSN` de verilmemiş
5. Linux ve macOS'ta sürücü kurulu ancak kayıtlı değil; bunun yerine sürücü kitaplığının tam
   yolunu verin veya sürücüyü `odbcinst.ini` içinde kaydedin

---

### Bağlantı testi zaman aşımına uğruyor

**Belirtiler:**
- **Test** takılıyor ve yaklaşık yarım dakika sonra başarısız oluyor

**Nedenler ve Çözümler:**
1. Ana makineye veya porta *digna* ana makinesinden erişilemiyor; güvenlik duvarını ve bulut
   kaynakları için IP izin listesini kontrol edin
2. Ana makine adı doğru, ancak port başka bir hizmete ait
3. Kaynağın bir bağlantıyı kabul etmesi varsayılan 30 saniyeden uzun sürüyor; `config.toml`
   dosyasının `[base]` bölümündeki `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` değerini artırın (`0`
   süresiz bekler) ve arka ucu yeniden başlatın
4. Sunucusuz bir uç nokta boşta kalma durumundan devam ediyor; yeniden deneyin ve bu düzenli
   olarak oluyorsa oturum açma zaman aşımını yukarıdaki gibi artırın

---

### Kimlik bilgileri doğru olmasına rağmen kimlik doğrulama başarısız oluyor

**Belirtiler:**
- Sürücü geçersiz kimlik bilgileri bildiriyor, ancak aynı kullanıcı başka bir SQL istemcisinde
  çalışıyor

**Nedenler ve Çözümler:**
1. Parola `;` içeriyor; değeri süslü parantez içine alın: `{p@ss;word}`
2. Değere sondaki bir boşluk kopyalanmış
3. Sürücü belirli bir kimlik doğrulama mekanizması bekliyor; örneğin Hive ve Databricks
   sürücüleri için `AuthMech` veya Snowflake için `authenticator`
4. Değer şifrelenmiş olarak saklanmış ve ardından düzenlenmiş; şifrelenmiş değerler geri
   okunamaz, bu nedenle gizli değeri eksiksiz olarak yeniden girin
5. Bir token'ın süresi dolmuş; kişisel erişim token'ları ve programatik erişim token'ları bir
   son kullanma tarihiyle verilir

---

### Veri kaynağı ekranı beklenen veritabanını veya şemayı sunmuyor

**Belirtiler:**
- Bir veri kaynağı eklenirken kataloglar, şemalar veya tablolar eksik

**Nedenler ve Çözümler:**
1. Bağlantı farklı bir veritabanını gösteriyor; bkz.
   [Bağlantının Gördüğü Veritabanı](#which-database-the-connection-sees)
2. Bağlantı kullanıcısının şema veya veri sözlüğü üzerinde okuma hakları yok
3. **Technology** kaynakla eşleşmiyor, bu nedenle *digna* yanlış veri sözlüğünü sorguluyor
4. Snowflake için kullanıcıya varsayılan bir warehouse atanmamış ve `Warehouse` özelliği de
   verilmemiş, bu nedenle meta veri sorguları çalışamıyor

---

### Bağlantı testi başarılı olurken profil oluşturma başarısız oluyor

**Belirtiler:**
- **Test** başarılı oluyor, ancak çalışma tabloları oluşturulurken bir inceleme başarısız
  oluyor

**Nedenler ve Çözümler:**
1. *Permanent* profil oluşturma seçili ve bağlantı kullanıcısı **Work Schema** içinde tablo
   oluşturamıyor; hakları verin veya *Session* ya da *Standard* moduna geçin
2. *Permanent* profil oluşturma seçiliyken **Work Schema** boş veya var olmayan bir şemayı
   adlandırıyor
3. *Session* profil oluşturma seçili ve bağlantı kullanıcısı geçici tablo oluşturamıyor
4. Uzun süren bir profil oluşturma sorgusu sorgu zaman aşımına takılıyor; `config.toml`
   dosyasının `[base]` bölümündeki `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` değerini artırın
   (varsayılan 3600 saniye, `0` zaman aşımını devre dışı bırakır)

---

## En İyi Uygulamalar

**YAPIN:**

- Bağlantıyı yapılandırmadan önce sürücüyü *digna* ana makinesine kurun ve kaydedin
- Her parola ve token için **Encrypted** seçeneğini işaretleyin
- Kaydetmeden önce **Test**'e tıklayın ve bir parola değişikliğinden sonra yeniden test edin
- Bağlantıları kaynağa ve ortama göre adlandırın, örneğin `sales_dwh_prod`
- *digna*'ya özel bir veritabanı kullanıcısı verin; *Standard* profil oluşturmanın yeterli
  olduğu yerlerde salt okunur olsun
- Kaynak veritabanı başına bir bağlantı tutun ve ilkini değiştirmek yerine ikinci bir bağlantı
  ekleyin

**YAPMAYIN:**

- Gizli bilgileri şifrelenmemiş olarak saklamayın veya bir veritabanı kullanıcısını *digna* ile
  diğer araçlar arasında paylaşmayın
- 64 bit bir *digna* kurulumuyla 32 bit bir sürücü kullanmayın
- *digna* bir hizmet olarak çalıştığında bir User DSN'e güvenmeyin; görünür olmayacaktır
- `;` içeren bir değeri süslü parantez olmadan bir özelliğe koymayın
- **Work Schema**'yı kaynak verileri barındıran bir şemaya yönlendirmeyin

---

## Destek

Bir veritabanı bağlantısı konusunda yardıma mı ihtiyacınız var?

- **E-posta:** support@digna.ai
- **Dokümantasyon:** https://docs.digna.ai
- **Web sitesi:** https://www.digna.ai

---

**Sürüm:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**