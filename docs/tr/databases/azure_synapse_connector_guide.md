---
title: Azure Synapse Bağlayıcısı – Veritabanı Entegrasyonu | digna Dokümantasyonu
description: digna'yı DSN'siz bir bağlantı dizesiyle ODBC üzerinden Azure Synapse Analytics'e bağlanacak şekilde yapılandırın. Gerekli ODBC özellikleri ve digna tarafındaki bağlantı ayarlarıyla sunucusuz ve ayrılmış SQL havuzlarını destekler.
image: /assets/logo_square.png
---


# Azure Synapse Analytics için Kaynak Bağlayıcısı

Bu kılavuz, *digna*'nın **DSN'siz** bir bağlantı dizesi kullanarak **ODBC** üzerinden Azure
Synapse Analytics'e bağlanacak şekilde nasıl yapılandırılacağını açıklar. Hem sunucusuz hem de
ayrılmış SQL havuzları desteklenir.

Kurulumun *digna* tarafı her teknoloji için aynıdır: bağlantıların nerede oluşturulduğu,
özellik değerlerinin nasıl şifrelendiği, bir bağlantının nasıl test edildiği ve profil oluşturma
modlarının ne anlama geldiği. Bunlar [Veritabanı Bağlantılarına Genel Bakış](overview.md)
sayfasında açıklanmıştır. Bu sayfa Azure Synapse'e özgü konuları ele alır.

!!! note "Teknoloji"

    Synapse SQL Server lehçesini kullanır, bu nedenle bağlantı **Technology: SQL Server** ile
    oluşturulur. Şirket içi bir sunucu için bkz. [MS SQL Server](sqlserver_connector_guide.md).

---

## 1. ODBC Sürücüsünü Kurun {: #1-install-the-odbc-driver }

[Microsoft'un kurulum kılavuzunu](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
izleyerek *digna* arka ucunu çalıştıran makineye **ODBC Driver 18 for SQL Server**'ı kurun ve
kayıtlı sürücü adının tamamını
[ODBC Sürücüsünü digna Ana Makinesine Kurun](overview.md#install-the-driver) bölümünde
açıklandığı şekilde ana makinenizden okuyun.

---

## 2. ODBC Özellikleri {: #2-odbc-properties }

!!! important "Bir örnek, bir şartname değil"

    Aşağıdaki küme, çalıştığı bilinen bir kombinasyondur. Özellikler Microsoft ODBC sürücüsüne
    aittir; bu nedenle adları, varsayılan değerleri ve kabul edilen değerleri sürücü
    sürümlerine ve platformlara göre farklılık gösterir. Çalışma alanının gerektirdikleri de
    nasıl yapılandırıldığına (havuz türü, kimlik doğrulama yöntemi, güvenlik duvarı) bağlıdır.
    Bunu bir başlangıç noktası olarak kullanın ve kurduğunuz sürücü sürümünün dokümantasyonunu
    kontrol edin.

**Add DB Connection** ekranında aşağıdaki özellikleri ekleyin:

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | *digna* ana makinesinde kayıtlı sürücü adıyla eşleşmelidir |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Çalışma alanı adı ile uç nokta soneki; aşağıya bakın |
| `DATABASE` | `dignadata` | Kaynak şemaları barındıran veritabanı. Bu bağlantının profilini oluşturabileceği tek veritabanıdır |
| `UID` | `sqladminuser` | SQL oturum açma bilgisi |
| `PWD` | `<password>` | **Encrypted** seçeneğini işaretleyin |

Ortaya çıkan bağlantı dizesi şöyle görünür:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### `SERVER` değeri

Synapse çalışma alanının adını alın ve uç nokta sonekini ekleyin:

| Havuz | `SERVER` |
|---|---|
| **Sunucusuz SQL havuzu** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Ayrılmış SQL havuzu** | `<workspace>.sql.azuresynapse.net` |

!!! warning "`-ondemand` kısmı kolayca gözden kaçabilir"

    Bu kısım olmadan ad ayrılmış uç noktaya çözümlenir ve bağlantı ya başarısız olur ya da fark
    edilmeden amaçlanandan farklı bir havuza ulaşır. Her iki uç nokta da Azure portalındaki
    çalışma alanı genel bakış sayfasında gösterilir.

### Güvenlik duvarı

Synapse çalışma alanı güvenlik duvarı, *digna* ana makinesinin giden adresine izin vermelidir.
Bağlantıyı test etmeden önce bu adresi çalışma alanında **Networking** altına ekleyin; engellenen
bir adres, kimlik doğrulama hatası olarak değil bağlantı zaman aşımı olarak görünür.

### Microsoft Entra ID kimlik doğrulaması

Sürücü, bir SQL oturum açma bilgisi yerine Entra ID'ye karşı kimlik doğrulaması yapabilir.
`UID`/`PWD` yerine çalışma alanınızın beklediği kimlik doğrulama yöntemini kullanın, örneğin:

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | Bu durumda `UID` uygulama (istemci) kimliğini, `PWD` ise istemci gizli anahtarını alır |
| `Authentication` | `ActiveDirectoryMSI` | *digna* ana makinesinin yönetilen kimliği, kimlik bilgisi gerekmez |

---

## 3. *digna* Yapılandırması {: #3-digna-configuration }

**Add DB Connection** ekranında aşağıdakileri girin:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Azure Synapse ile İlgili Notlar {: #4-notes-on-azure-synapse }

- **Sunucusuz havuzlar yalnızca *Standard* profil oluşturmayı destekler.** Sunucusuz bir SQL
  havuzu bir veritabanında tablo oluşturamaz, bu nedenle ne *Permanent* ne de *Session* profil
  oluşturma çalışabilir. *Standard* metrikleri doğrudan kaynak üzerinde hesaplar; sunucusuz
  hizmet işlenen veri başına faturalandırıldığından bu aynı zamanda daha ucuz seçenektir.
- **Bir bağlantı bir veritabanını görür.** *digna*, `DATABASE` içinde adı verilen veritabanının
  şemalarını sunar, çünkü Synapse da SQL Server gibi katalog olarak yalnızca geçerli
  veritabanını bildirir.
- **Driver 18'de şifreleme varsayılan olarak açıktır** ve Synapse uç noktaları geçerli genel
  sertifikalar sunar, bu nedenle `Encrypt` veya `TrustServerCertificate` özelliğine gerek
  yoktur.
- **Sunucusuz bir uç nokta**, ilk bağlantıda **boşta kalma durumundan devam edebilir**. Bir
  süredir kullanılmayan bir havuzda bağlantı testi zaman aşımına uğrarsa yeniden deneyin.

---

## 5. Sürücüyü Doğrulama (isteğe bağlı) {: #5-verifying-the-driver-optional }

DSN'siz bir bağlantı için bir ODBC veri kaynağı yapılandırmak gerekli değildir; ancak sürücünün
kendi sihirbazı, bunları *digna*'ya girmeden önce sürücünün çalıştığını ve çalışma alanının
kimlik bilgilerinizi kabul ettiğini doğrulamanın pratik bir yoludur.

#### Adım 1
![Adım 1](images/azure_synapse/create_odbc_data_source_step1.png)

"Server" alanını doldurun.
Synapse çalışma alanının adını kullanın ve sonuna ".sql.azuresynapse.net" ekleyin.  
**Dikkat**: sunucusuz bir SQL havuzu kullanarak bağlanmak istiyorsanız, yukarıdaki ekran
görüntüsünde gösterildiği gibi "-ondemand" kısmını eklediğinizden emin olun.

**Next >** düğmesine tıklayın.

#### Adım 2
![Adım 2](images/azure_synapse/create_odbc_data_source_step2.png)

Kimlik doğrulama yöntemini seçin (ör. kullanıcı adı ve parola)
ve gerekli bilgileri girin.

**Next >** düğmesine tıklayın.

#### Adım 3
![Adım 3](images/azure_synapse/create_odbc_data_source_step3.png)

ANSI uyumlu ayarları seçin ve ardından **Next >** düğmesine tıklayın.

#### Adım 4
![Adım 4](images/azure_synapse/create_odbc_data_source_step4.png)

Varsayılan ayarları bırakabilir veya gerektiği gibi seçenekleri belirleyebilirsiniz;
ardından **Finish** düğmesine tıklayın.

#### Adım 5
![Adım 5](images/azure_synapse/create_odbc_data_source_step5.png)

Şimdi **Test datasource** düğmesine tıklayın.

#### Adım 6
![Adım 6](images/azure_synapse/create_odbc_data_source_step6.png)

Bir başarı ekranı sürücünün, uç noktanın ve kimlik bilgilerinin çalıştığını doğrular.
Girdiğiniz değerler, [bölüm 2](#2-odbc-properties) içindeki özelliklerin aldığı değerlerin
tam olarak aynısıdır.
