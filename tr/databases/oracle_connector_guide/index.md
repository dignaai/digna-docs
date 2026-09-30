# Oracle için Kaynak Bağlayıcısı

Bu kılavuz, *digna*'nın **DSN'siz** bir bağlantı dizesi kullanarak **ODBC** üzerinden Oracle
Database'e bağlanacak şekilde nasıl yapılandırılacağını açıklar.

Kurulumun *digna* tarafı her teknoloji için aynıdır: bağlantıların nerede oluşturulduğu,
özellik değerlerinin nasıl şifrelendiği, bir bağlantının nasıl test edildiği ve profil oluşturma
modlarının ne anlama geldiği. Bunlar [Veritabanı Bağlantılarına Genel Bakış](overview.md)
sayfasında açıklanmıştır. Bu sayfa Oracle'a özgü konuları ele alır.

---

## 1. ODBC Sürücüsünü Kurun {: #1-install-the-odbc-driver }

Oracle ODBC sürücüsü **Oracle Client**'ın bir parçasıdır (Instant Client "ODBC" paketi
yeterlidir). Üreticinin resmi kurulum kılavuzunu izleyerek bunu *digna* arka ucunu çalıştıran
makineye kurun.

Sürücü kendini **Oracle in `<OracleHomeName>`** olarak kaydeder; örneğin
`Oracle in OraDB21Home1` veya `Oracle in instantclient_21_13`. Home adı kuruluma göre
değişir, bu nedenle tam adı
[ODBC Sürücüsünü digna Ana Makinesine Kurun](overview.md#install-the-driver) bölümünde
açıklandığı şekilde ana makinenizden okuyun.

---

## 2. ODBC Özellikleri {: #2-odbc-properties }

!!! important "Bir örnek, bir şartname değil"

    Aşağıdaki küme, çalıştığı bilinen bir kombinasyondur. Özellikler Oracle ODBC sürücüsüne
    aittir; bu nedenle adları, varsayılan değerleri ve kabul edilen değerleri istemci
    sürümlerine göre farklılık gösterir; özellikle sürücü adı ana makinenizdeki Oracle home'a
    bağlıdır. Bunu bir başlangıç noktası olarak kullanın ve kurduğunuz istemci sürümünün
    dokümantasyonunu kontrol edin.

**Add DB Connection** ekranında aşağıdaki özellikleri ekleyin:

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | *digna* ana makinesinde kayıtlı sürücü adıyla eşleşmelidir |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Bağlanılacak veritabanı; aşağıya bakın |
| `UID` | `DIGNA_SOURCE_USER` | Veritabanı kullanıcısı |
| `PWD` | `<password>` | **Encrypted** seçeneğini işaretleyin |

Ortaya çıkan bağlantı dizesi şöyle görünür:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### `DBQ` değeri

`DBQ` üç biçim kabul eder. Bunlar *digna* için eşdeğerdir; *digna* ana makinesinde nelerin
yapılandırılması gerektiği bakımından farklılık gösterirler:

| Biçim | Örnek | Gereksinim |
|---|---|---|
| **Tam bağlantı tanımlayıcısı** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Hiçbir şey; her şey özelliğin içindedir. Önerilir |
| **TNS takma adı** | `DIGNA_SOURCE` | Takma ad, *digna* ana makinesindeki Oracle Client'ın `tnsnames.ora` dosyasında bulunmalıdır |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Easy Connect'i destekleyen bir Oracle Client (12c ve üzeri) |

!!! tip "Tam tanımlayıcıyı tercih edin"

    Bir TNS takma adı, bağlantı tanımının yarısını *digna* ana makinesindeki bir dosyaya taşır;
    ana makine yeniden kurulduğunda veya *digna* taşındığında bu dosya kolayca unutulur. Tam
    tanımlayıcı, bağlantıyı kendi kendine yeterli tutar; DSN'siz bir kurulumun amacı da budur.

Bir tanımlayıcıdaki parantezlerin bağlantı dizesi içinde sorun yaratmadığını unutmayın; ancak
parolanız `;` içeriyorsa onu süslü paranteze alın: `PWD={p@ss;word}`.

---

## 3. *digna* Yapılandırması {: #3-digna-configuration }

**Add DB Connection** ekranında aşağıdakileri girin:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Oracle ile İlgili Notlar {: #4-notes-on-oracle }

- **Şemalar kullanıcılardır.** *digna* Oracle kullanıcılarını şema olarak listeler, bu nedenle
  kaynak şema tabloların sahibidir; yukarıdaki örnekte `DIGNA_SOURCE_USER`. Bağlantı
  kullanıcısının bu tablolar üzerinde doğrudan veya bir rol aracılığıyla `SELECT` yetkisine
  ihtiyacı vardır.
- **Bir bağlantı bir veritabanını görür.** *digna*'nın sunduğu katalog, bağlantının bağlı
  olduğu veritabanıdır; bu nedenle hangi hizmetin ve dolayısıyla hangi veritabanının profilinin
  oluşturulacağını `DBQ` belirler.
- **Tanımlayıcılar tırnak içine alındığında büyük/küçük harfe duyarlıdır.** *digna* veri
  sözlüğünden okuduğu adları, yani Oracle'ın sakladığı biçimi (tırnaksız nesneler için büyük
  harf) tırnak içine alır.
- **Profil oluşturma modları.** *Permanent* çalışma tablolarını **Work Schema** içinde
  oluşturur, bu nedenle kullanıcının orada `CREATE TABLE` yetkisine ve tablespace üzerinde bir
  kotaya ihtiyacı vardır. *Session* özel bir geçici tablo (`ORA$PTT_…`, Oracle 18c ve üzeri)
  kullanır ve **Work Schema**'ya dokunmaz. *Standard* yalnızca okuma erişimi gerektirir.

---

## 5. Sürücüyü Doğrulama (isteğe bağlı) {: #5-verifying-the-driver-optional }

DSN'siz bir bağlantı için bir ODBC veri kaynağı yapılandırmak gerekli değildir; ancak sürücünün
kendi iletişim kutusu, bunları *digna*'ya girmeden önce Oracle Client'ın, hizmet adının ve
kimlik bilgilerinizin çalıştığını doğrulamanın pratik bir yoludur.

#### Adım 1
![Adım 1](images/oracle/create_odbc_data_source_step1.png)

Burada sunulan **TNS Service Name**, Oracle Client kurulumunuzun `tnsnames.ora` dosyasından
gelir; takma ad ve onunla birlikte ana makine, port ve hizmet adı orada tanımlanır. *digna*'da
takma adı `DBQ` olarak ya da bunun yerine tam tanımlayıcıyı kullanabilirsiniz.

#### Adım 2 – Bağlantıyı test edin

**Test Connection** düğmesine tıklayın.

![Adım 2](images/oracle/create_odbc_data_source_step2.png)

Parolayı girin ve **OK** düğmesine tıklayın.

![Adım 3](images/oracle/create_odbc_data_source_step3.png)

Bir başarı mesajı, sürücünün ve kimlik bilgilerinin çalıştığını doğrular.