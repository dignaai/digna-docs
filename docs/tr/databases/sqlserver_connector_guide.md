---
title: MS SQL Server Bağlayıcısı – Veritabanı Entegrasyonu | digna Dokümantasyonu
description: digna'yı DSN'siz bir bağlantı dizesiyle ODBC üzerinden Microsoft SQL Server'a bağlanacak şekilde yapılandırın. Microsoft ODBC sürücüsünü, gerekli ODBC özelliklerini, şifreleme ayarlarını ve digna tarafındaki bağlantı ayarlarını kapsar.
image: /assets/logo_square.png
---


# MS SQL Server için Kaynak Bağlayıcısı

Bu kılavuz, *digna*'nın **DSN'siz** bir bağlantı dizesi kullanarak **ODBC** üzerinden
Microsoft SQL Server'a bağlanacak şekilde nasıl yapılandırılacağını açıklar.

Kurulumun *digna* tarafı her teknoloji için aynıdır: bağlantıların nerede oluşturulduğu,
özellik değerlerinin nasıl şifrelendiği, bir bağlantının nasıl test edildiği ve profil oluşturma
modlarının ne anlama geldiği. Bunlar [Veritabanı Bağlantılarına Genel Bakış](overview.md)
sayfasında açıklanmıştır. Bu sayfa SQL Server'a özgü konuları ele alır.

!!! note "Azure Synapse Analytics"

    Synapse da farklı bir ana makine adı ve birkaç ek husus ile bir SQL Server bağlantısı olarak
    yapılandırılır; bkz. [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. ODBC Sürücüsünü Kurun {: #1-install-the-odbc-driver }

[Microsoft'un kurulum kılavuzunu](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
izleyerek *digna* arka ucunu çalıştıran makineye **ODBC Driver 18 for SQL Server**'ı kurun.

Windows ile birlikte yalnızca **SQL Server** adıyla gelen sürücü de çalışır, ancak uzun
zamandır yerini yenilerine bırakmıştır ve ne modern TLS ayarlarını ne de Azure kimlik
doğrulamasını destekler. Bunu yalnızca güncel sürücüyü kurmanın mümkün olmadığı durumlarda
kullanın.

Kayıtlı sürücü adının tamamını
[ODBC Sürücüsünü digna Ana Makinesine Kurun](overview.md#install-the-driver) bölümünde
açıklandığı şekilde ana makinenizden okuyun.

---

## 2. ODBC Özellikleri {: #2-odbc-properties }

!!! important "Bir örnek, bir şartname değil"

    Aşağıdaki küme, çalıştığı bilinen bir kombinasyondur. Özellikler Microsoft ODBC sürücüsüne
    aittir; bu nedenle adları, varsayılan değerleri ve kabul edilen değerleri sürücü
    sürümlerine (örneğin Driver 18, Driver 17'nin aksine varsayılan olarak şifreleme yapar) ve
    platformlara göre farklılık gösterir. Bunu bir başlangıç noktası olarak kullanın ve
    kurduğunuz sürücü sürümünün dokümantasyonunu kontrol edin.

**Add DB Connection** ekranında aşağıdaki özellikleri ekleyin:

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | *digna* ana makinesinde kayıtlı sürücü adıyla eşleşmelidir |
| `SERVER` | `sql.example.com` | Sunucu adı veya IP adresi. Adlandırılmış örnekler: `host\instance`; varsayılan olmayan bir port: `host,1433` |
| `PORT` | `1433` | Port zaten `SERVER` içinde yer alıyorsa kullanmayın |
| `DATABASE` | `digna_source_db` | Kaynak şemaları barındıran veritabanı. Bu bağlantının profilini oluşturabileceği tek veritabanıdır |
| `UID` | `digna_source_user` | Veritabanı kullanıcısı |
| `PWD` | `<password>` | **Encrypted** seçeneğini işaretleyin |

Ortaya çıkan bağlantı dizesi şöyle görünür:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### ODBC Driver 18 ile şifreleme

Driver 18 bağlantıları varsayılan olarak şifreler ve sunucu sertifikasını doğrular. *digna*
ana makinenizin güvenmediği bir sertifikaya (genellikle kendinden imzalı bir sertifika) sahip
bir sunucuya bağlanırken bağlantı bir sertifika zinciri hatasıyla başarısız olur. Şunları
ekleyin:

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `Encrypt` | `yes` | Driver 18'de varsayılandır; yalnızca sunucu TLS kullanamıyorsa `no` olarak ayarlayın |
| `TrustServerCertificate` | `yes` | Sertifika doğrulamasını atlar. Test ortamlarında pratiktir; üretimde sertifikayı kurmayı tercih edin |

### Windows Kimlik Doğrulaması

Bir SQL oturum açma bilgisi yerine *digna* hizmetini çalıştıran hesapla bağlanmak için `UID`
ve `PWD` özelliklerini kaldırın ve şunu ekleyin:

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `Trusted_Connection` | `yes` | *digna* hizmet hesabının veritabanı haklarına ihtiyacı vardır |

---

## 3. *digna* Yapılandırması {: #3-digna-configuration }

**Add DB Connection** ekranında aşağıdakileri girin:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. MS SQL Server ile İlgili Notlar {: #4-notes-on-ms-sql-server }

- **Bir bağlantı bir veritabanını görür.** *digna*, `DATABASE` içinde adı verilen veritabanının
  şemalarını sunar, çünkü SQL Server katalog olarak yalnızca geçerli veritabanını bildirir.
  Başka bir veritabanındaki kaynak tablolar için ayrı bir bağlantı gerekir.
- **Profil oluşturma modları.** *Permanent* çalışma tablolarını **Work Schema** içinde
  oluşturur, bu nedenle kullanıcının orada `CREATE TABLE` yetkisine ihtiyacı vardır. *Session*
  `tempdb` içinde yerel geçici tablolar (`#wt_…`) kullanır ve **Work Schema**'ya dokunmaz.
  *Standard* yalnızca okuma erişimi gerektirir.
- **`SERVER` örneği ve portu taşır.** Adlandırılmış bir örnekte `host\instance`, SQL Server
  Browser hizmetine erişilebilmesini gerektirir; `host,port` bu gereksinimi ortadan kaldırır.

---

## 5. Sürücüyü Doğrulama (isteğe bağlı) {: #5-verifying-the-driver-optional }

DSN'siz bir bağlantı için bir ODBC veri kaynağı yapılandırmak gerekli değildir; ancak sürücünün
kendi sihirbazı, bunları *digna*'ya girmeden önce sürücünün çalıştığını ve sunucunun kimlik
bilgilerinizi kabul ettiğini doğrulamanın pratik bir yoludur.

#### Adım 1
![Adım 1](images/sqlserver/create_odbc_data_source_step1.png)

**Next >** düğmesine tıklayın.

#### Adım 2
![Adım 2](images/sqlserver/create_odbc_data_source_step2.png)

Kimlik doğrulama yöntemini seçin (ör. kullanıcı adı ve parola)
ve gerekli bilgileri girin.

**Next >** düğmesine tıklayın.

#### Adım 3
![Adım 3](images/sqlserver/create_odbc_data_source_step3.png)

ANSI uyumlu ayarları seçin ve ardından **Next >** düğmesine tıklayın.

#### Adım 4
![Adım 4](images/sqlserver/create_odbc_data_source_step4.png)

Varsayılan ayarları bırakabilir veya gerektiği gibi günlük kaydı seçeneklerini
belirleyebilirsiniz; ardından **Finish** düğmesine tıklayın.

#### Adım 5
![Adım 5](images/sqlserver/create_odbc_data_source_step5.png)

Şimdi **Test datasource** düğmesine tıklayın.

#### Adım 6
![Adım 6](images/sqlserver/create_odbc_data_source_step6.png)

Bir başarı ekranı, sürücünün ve kimlik bilgilerinin çalıştığını doğrular. Girdiğiniz değerler,
[bölüm 2](#2-odbc-properties) içindeki özelliklerin aldığı değerlerin tam olarak aynısıdır.
