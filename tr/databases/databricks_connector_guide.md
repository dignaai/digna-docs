# Databricks için Kaynak Bağlayıcısı

Bu kılavuz, *digna*'nın **DSN'siz** bir bağlantı dizesi kullanarak **ODBC** üzerinden
Databricks'e bağlanacak şekilde nasıl yapılandırılacağını açıklar.

Kurulumun *digna* tarafı her teknoloji için aynıdır: bağlantıların nerede oluşturulduğu,
özellik değerlerinin nasıl şifrelendiği, bir bağlantının nasıl test edildiği ve profil oluşturma
modlarının ne anlama geldiği. Bunlar [Veritabanı Bağlantılarına Genel Bakış](overview.md)
sayfasında açıklanmıştır. Bu sayfa Databricks'e özgü konuları ele alır.

!!! note "Unity Catalog gereklidir"

    *digna* kullanılabilir katalogları `system.information_schema.catalogs` üzerinden okur, bu
    nedenle çalışma alanında Unity Catalog etkin olmalıdır. Önceki *digna* sürümleri, Unity
    Catalog içermeyen çalışma alanları için ayrı bir "Databricks Legacy" teknolojisi sunuyordu;
    bu teknoloji artık kullanılamaz.

---

## 1. ODBC Sürücüsünü Kurun {: #1-install-the-odbc-driver }

[Databricks'in kurulum kılavuzunu](https://docs.databricks.com/aws/en/integrations/odbc/)
izleyerek *digna* arka ucunu çalıştıran makineye **Databricks ODBC Driver**'ı kurun.

Sürüme bağlı olarak sürücü kendini **Simba Spark ODBC Driver** veya **Databricks ODBC Driver**
olarak kaydeder. Kayıtlı adın tamamını
[ODBC Sürücüsünü digna Ana Makinesine Kurun](overview.md#install-the-driver) bölümünde
açıklandığı şekilde ana makinenizden okuyun.

---

## 2. Bağlantı Bilgilerini Toplayın {: #2-gather-the-connection-details }

Tüm değerler, *digna*'nın kullanmasını istediğiniz SQL warehouse'tan (veya kümeden) gelir.
Databricks çalışma alanında bunu açın ve **Connection details** bölümüne gidin:

| Databricks alanı | Kullanıldığı yer |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, normalde `443` |
| **HTTP path** | `HTTPPath` |

Kimlik doğrulama için bir **kişisel erişim token'ı** oluşturun; bkz.
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Token'lar bir kullanıcıya veya hizmet sorumlusuna aittir ve bu sorumlunun kaynak veriler
üzerinde `USE CATALOG`, `USE SCHEMA` ve `SELECT` yetkilerine ihtiyacı vardır.

---

## 3. ODBC Özellikleri {: #3-odbc-properties }

!!! important "Bir örnek, bir şartname değil"

    Aşağıdaki küme, çalıştığı bilinen bir kombinasyondur. Özellikler Databricks/Simba
    sürücüsüne aittir; bu nedenle adları, varsayılan değerleri ve kabul edilen değerleri sürücü
    sürümlerine (sürücü birden fazla kez yeniden adlandırılmış ve kimlik doğrulama seçenekleri
    genişletilmiştir) ve platformlara göre farklılık gösterir. Bunu bir başlangıç noktası olarak
    kullanın ve kurduğunuz sürücü sürümünün dokümantasyonunu kontrol edin.

**Add DB Connection** ekranında aşağıdaki özellikleri ekleyin:

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | *digna* ana makinesinde kayıtlı sürücü adıyla eşleşmelidir |
| `Host` | `<workspace>.cloud.databricks.com` | Warehouse'un sunucu ana makine adı, ör. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | Warehouse'un veya kümenin HTTP yolu |
| `SSL` | `1` | Databricks uç noktaları yalnızca TLS kullanır |
| `ThriftTransport` | `2` | SQL uç noktalarının kullandığı HTTP aktarımı |
| `AuthMech` | `3` | Token kimlik doğrulaması |
| `UID` | `token` | Bir kullanıcı adı değil, harfi harfine `token` kelimesi |
| `PWD` | `dapi…` | Kişisel erişim token'ı. **Encrypted** seçeneğini işaretleyin |
| `UseNativeQuery` | `1` | *digna*'nın SQL'ini değiştirmeden iletir; aşağıya bakın |

Ortaya çıkan bağlantı dizesi şöyle görünür:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "`UseNativeQuery=1` değerini koruyun"

    Sürücünün varsayılanı olan `UseNativeQuery=0` ile sürücü, gelen SQL'i taşınabilir ODBC
    sözdizimi olduğunu düşündüğü biçime yeniden yazar. *digna* zaten Databricks SQL ürettiği
    için bu yeniden yazma ters tırnak kullanımını ve tarih değişmezlerini değiştirebilir;
    bunun sonucunda profil oluşturma, yazıldığı haliyle geçerli olan ifadelerde başarısız olur.

### Token yerine OAuth

Makineden makineye OAuth kimlik doğrulaması kullanan bir hizmet sorumlusu için `AuthMech`,
`UID` ve `PWD` yerine şunları kullanın:

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | İstemci kimlik bilgileri |
| `Auth_Client_ID` | `<application id>` | Hizmet sorumlusu |
| `Auth_Client_Secret` | `<client secret>` | **Encrypted** seçeneğini işaretleyin |

---

## 4. *digna* Yapılandırması {: #4-digna-configuration }

**Add DB Connection** ekranında aşağıdakileri girin:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Databricks ile İlgili Notlar {: #5-notes-on-databricks }

- ***digna* bağlandığında warehouse çalışıyor olmalı** veya başlayabilmelidir. Durdurulmuş
  bir durumdan devam eden bir warehouse bağlantı zaman aşımından daha uzun sürebilir; boşta
  geçen bir süreden sonraki ilk denemede test başarısız olursa yeniden deneyin.
- **Kataloglar çalışma alanından gelir.** Çoğu teknolojinin aksine, tek bir Databricks
  bağlantısı sorumlunun görmesine izin verilen her kataloğa erişir; böylece tek bir bağlantı
  birden çok katalogdaki kaynaklara hizmet edebilir.
- **Profil oluşturma modları.** *Permanent* çalışma tablolarını kaynağın kataloğu içindeki
  **Work Schema**'da oluşturur, bu nedenle sorumlunun orada `CREATE TABLE` yetkisine ihtiyacı
  vardır. *Session* `CREATE TEMPORARY TABLE` kullanır ve **Work Schema**'ya dokunmaz.
  *Standard* yalnızca okuma erişimi gerektirir.
- **Sunucusuz warehouse'lar** da aynı şekilde **çalışır**; yalnızca `HTTPPath` farklıdır.

---

## 6. Sürücüyü Doğrulama (isteğe bağlı) {: #6-verifying-the-driver-optional }

DSN'siz bir bağlantı için bir ODBC veri kaynağı yapılandırmak gerekli değildir; ancak sürücünün
kendi iletişim kutusu, bunları *digna*'ya girmeden önce sürücünün, warehouse'un ve token'ın
çalıştığını doğrulamanın pratik bir yoludur.

#### Adım 1
![Adım 1](images/databricks/create_odbc_data_source_step1.png)

#### Adım 2
![Adım 2](images/databricks/create_odbc_data_source_step2.png)

#### Adım 3
![Adım 3](images/databricks/create_odbc_data_source_step3.png)

#### Adım 4
![Adım 4](images/databricks/create_odbc_data_source_step4.png)

#### Adım 5 – Bağlantıyı test edin

**TEST** düğmesine tıklayın. Başarılı bir bağlantı şöyle görünmelidir:

![Adım 5](images/databricks/create_odbc_data_source_step5.png)

Burada girilen ana makine, HTTP yolu ve token, [bölüm 3](#3-odbc-properties) içindeki
özelliklerin aldığı değerlerin tam olarak aynısıdır.