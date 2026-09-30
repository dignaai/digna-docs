# PostgreSQL için Kaynak Bağlayıcısı

Bu kılavuz, *digna*'nın **DSN'siz** bir bağlantı dizesi kullanarak **ODBC** üzerinden
PostgreSQL'e bağlanacak şekilde nasıl yapılandırılacağını açıklar.

Kurulumun *digna* tarafı her teknoloji için aynıdır: bağlantıların nerede oluşturulduğu,
özellik değerlerinin nasıl şifrelendiği, bir bağlantının nasıl test edildiği ve profil oluşturma
modlarının ne anlama geldiği. Bunlar [Veritabanı Bağlantılarına Genel Bakış](overview.md)
sayfasında açıklanmıştır. Bu sayfa PostgreSQL'e özgü konuları ele alır.

---

## 1. ODBC Sürücüsünü Kurun {: #1-install-the-odbc-driver }

PostgreSQL ODBC sürücüsünü (**psqlODBC**), üreticinin resmi kurulum kılavuzunu izleyerek
*digna* arka ucunu çalıştıran makineye kurun.

Sürücü kendini platforma ve pakete göre değişen bir adla kaydeder; Windows'ta genellikle
**PostgreSQL Unicode(x64)**, Linux'ta ise **PostgreSQL ODBC Driver(UNICODE)**. Tam adı
[ODBC Sürücüsünü digna Ana Makinesine Kurun](overview.md#install-the-driver) bölümünde
açıklandığı şekilde ana makinenizden okuyun ve aşağıdaki `DRIVER` özelliği için bu adı kullanın.

---

## 2. ODBC Özellikleri {: #2-odbc-properties }

!!! important "Bir örnek, bir şartname değil"

    Aşağıdaki küme, çalıştığı bilinen bir kombinasyondur. Özellikler psqlODBC sürücüsüne aittir;
    bu nedenle adları, varsayılan değerleri ve kabul edilen değerleri sürücü sürümlerine ve
    platformlara göre farklılık gösterir. Sunucunuzun talep ettikleri, özellikle SSL, de
    farklı olabilir. Bunu bir başlangıç noktası olarak kullanın ve kurduğunuz sürücü sürümünün
    dokümantasyonunu kontrol edin.

**Add DB Connection** ekranında aşağıdaki özellikleri ekleyin:

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | *digna* ana makinesinde kayıtlı sürücü adıyla eşleşmelidir |
| `SERVER` | `db.example.com` | Sunucu adı veya IP adresi |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Kaynak şemaları barındıran veritabanı. Bu bağlantının profilini oluşturabileceği tek veritabanıdır |
| `UID` | `digna_source_user` | Veritabanı kullanıcısı |
| `PWD` | `<password>` | **Encrypted** seçeneğini işaretleyin |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` veya `verify-full`; sunucu tarafından kabul edilmelidir |

Ortaya çıkan bağlantı dizesi şöyle görünür:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Diğer tüm psqlODBC seçenekleri ek bir özellik olarak eklenebilir; örneğin salt okunur bir
oturum için `ReadOnly=1` veya bağlantı sırasında `SET` ifadelerini çalıştırmak için
`ConnSettings`.

---

## 3. *digna* Yapılandırması {: #3-digna-configuration }

**Add DB Connection** ekranında aşağıdakileri girin:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. PostgreSQL ile İlgili Notlar {: #4-notes-on-postgresql }

- **`SSLMode` sunucuyla eşleşmelidir.** `hostssl` ile yapılandırılmış bir sunucu
  `SSLMode=disable` değerini reddeder; `verify-ca` veya `verify-full` ise ayrıca kök sertifikanın
  *digna* ana makinesindeki sürücü tarafından erişilebilir olmasını gerektirir. Sürücüyü test
  ederken belirli bir mod seçmeniz gerektiyse burada da aynısını kullanın.
- **Bir bağlantı bir veritabanını görür.** *digna*, `DATABASE` içinde adı verilen veritabanının
  şemalarını sunar, çünkü PostgreSQL katalog olarak yalnızca geçerli veritabanını bildirir.
  Başka bir veritabanındaki kaynak tablolar için ayrı bir bağlantı gerekir.
- **Profil oluşturma modları.** *Permanent* çalışma tablolarını **Work Schema** içinde
  oluşturur, bu nedenle kullanıcının o şema üzerinde `CREATE` yetkisine ihtiyacı vardır.
  *Session* `CREATE TEMPORARY TABLE` kullanır ve **Work Schema**'ya dokunmaz. *Standard*
  yalnızca okuma erişimi gerektirir.

---

## 5. Sürücüyü Doğrulama (isteğe bağlı) {: #5-verifying-the-driver-optional }

DSN'siz bir bağlantı için bir ODBC veri kaynağı yapılandırmak gerekli değildir; ancak sürücünün
kendi iletişim kutusu, bunları *digna*'ya girmeden önce sürücünün çalıştığını ve
sunucunun kimlik bilgilerinizi ve SSL modunuzu kabul ettiğini doğrulamanın pratik bir yoludur.

#### Adım 1
![Adım 1](images/postgres/create_odbc_data_source_step1.png)

#### Adım 2 – Bağlantıyı test edin

**Test Connection** düğmesine tıklayın.

![Adım 2](images/postgres/create_odbc_data_source_step2.png)

Burada girdiğiniz değerler, [bölüm 2](#2-odbc-properties) içindeki özelliklerin aldığı
değerlerin tam olarak aynısıdır.