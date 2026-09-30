# Teradata için Kaynak Bağlayıcısı

Bu kılavuz, *digna*'nın **DSN'siz** bir bağlantı dizesi kullanarak **ODBC** üzerinden
Teradata'ya bağlanacak şekilde nasıl yapılandırılacağını açıklar.

Kurulumun *digna* tarafı her teknoloji için aynıdır: bağlantıların nerede oluşturulduğu,
özellik değerlerinin nasıl şifrelendiği, bir bağlantının nasıl test edildiği ve profil oluşturma
modlarının ne anlama geldiği. Bunlar [Veritabanı Bağlantılarına Genel Bakış](overview.md)
sayfasında açıklanmıştır. Bu sayfa Teradata'ya özgü konuları ele alır.

---

## 1. ODBC Sürücüsünü Kurun {: #1-install-the-odbc-driver }

Üreticinin resmi kurulum kılavuzunu izleyerek *digna* arka ucunu çalıştıran makineye
**ODBC Driver for Teradata**'yı kurun.

Sürücü kendini adında sürüm numarası bulunacak şekilde kaydeder; örneğin
**Teradata Database ODBC Driver 20.00**. Kayıtlı adın tamamını
[ODBC Sürücüsünü digna Ana Makinesine Kurun](overview.md#install-the-driver) bölümünde
açıklandığı şekilde ana makinenizden okuyun.

---

## 2. ODBC Özellikleri {: #2-odbc-properties }

!!! important "Bir örnek, bir şartname değil"

    Aşağıdaki küme, çalıştığı bilinen bir kombinasyondur. Özellikler Teradata ODBC sürücüsüne
    aittir; bu nedenle adları, varsayılan değerleri ve kabul edilen değerleri sürücü
    sürümlerine (sürüm, sürücü adının bir parçasıdır) ve platformlara göre farklılık gösterir.
    Bunu bir başlangıç noktası olarak kullanın ve kurduğunuz sürücü sürümünün dokümantasyonunu
    kontrol edin.

**Add DB Connection** ekranında aşağıdaki özellikleri ekleyin:

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | *digna* ana makinesinde kayıtlı sürücü adıyla eşleşmelidir |
| `DBCNAME` | `teradata.example.com` | Sunucu adı veya IP adresi. Teradata'nın ana makine özelliği için kullandığı ad |
| `UID` | `digna_source_user` | Veritabanı kullanıcısı |
| `PWD` | `<password>` | **Encrypted** seçeneğini işaretleyin |

Ortaya çıkan bağlantı dizesi şöyle görünür:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Faydalı ek özellikler:

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `MechanismName` | `TD2` | Oturum açma mekanizması. `TD2` Teradata varsayılanıdır; dizin kimlik doğrulaması için `LDAP` kullanın |
| `DefaultDatabase` | `dad` | Oturumun başladığı veritabanı |
| `CharacterSet` | `UTF8` | Varsayılan oturum karakter kümesinin ASCII dışı verileri bozacağı durumlarda bunu ayarlayın |

---

## 3. *digna* Yapılandırması {: #3-digna-configuration }

**Add DB Connection** ekranında aşağıdakileri girin:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Teradata ile İlgili Notlar {: #4-notes-on-teradata }

- **Bir Teradata veritabanı bir şema değil, bir katalogdur.** *digna*, kullanıcının
  görebildiği veritabanlarını (`DBC.DatabasesV` üzerinden) katalog olarak listeler ve şema
  düzeyi uygulanmaz. Bir veri kaynağı eklerken veritabanını katalog olarak seçin; şema
  *not applicable* olarak bildirilir.
- **Bir bağlantı izin verilen her veritabanına erişir**; bu nedenle, bağlantının tek bir
  veritabanına sabitlendiği teknolojilerin aksine, tek bir bağlantı birden çok veritabanındaki
  kaynaklara hizmet edebilir.
- **Work Schema bir veritabanıdır.** *Permanent* profil oluşturma için çalışma tablolarını
  barındıran Teradata veritabanını adlandırın ve kullanıcıya orada `CREATE TABLE` hakları ile
  bir `PERM` alan tahsisi verin; perm alanı sıfır olan bir veritabanı tablo barındıramaz.
- **Profil oluşturma modları.** *Permanent* tabloları **Work Schema** içinde oluşturur.
  *Session* bir `VOLATILE` tablo kullanır; bu, `SPOOL` alanı gerektirir ancak perm alanı ve
  **Work Schema** içinde hak gerektirmez. *Standard* yalnızca okuma erişimi gerektirir.

---

## 5. Sürücüyü Doğrulama (isteğe bağlı) {: #5-verifying-the-driver-optional }

DSN'siz bir bağlantı için bir ODBC veri kaynağı yapılandırmak gerekli değildir; ancak sürücünün
kendi iletişim kutusu, bunları *digna*'ya girmeden önce sürücünün ve kimlik bilgilerinizin
çalıştığını doğrulamanın pratik bir yoludur.

#### Adım 1
![Adım 1](images/teradata/create_odbc_data_source_step1.png)

Buradaki **Name or IP address** alanı, [bölüm 2](#2-odbc-properties) içindeki `DBCNAME`
özelliğidir.

**Test** düğmesine tıklayın.

#### Adım 2
![Adım 2](images/teradata/create_odbc_data_source_step2.png)

Kullanıcı adını ve parolayı girin, ardından **OK** düğmesine tıklayın. Bir başarı ekranı,
sürücünün ve kimlik bilgilerinin çalıştığını doğrular.