---
title: Netezza Bağlayıcısı – Veritabanı Entegrasyonu | digna Dokümantasyonu
description: digna'yı DSN'siz bir bağlantı dizesiyle ODBC üzerinden Netezza'ya bağlanacak şekilde yapılandırın. NetezzaSQL sürücüsünü, gerekli ODBC özelliklerini ve digna tarafındaki bağlantı ayarlarını kapsar.
image: /assets/logo_square.png
---


# Netezza için Kaynak Bağlayıcısı

Bu kılavuz, *digna*'nın **DSN'siz** bir bağlantı dizesi kullanarak **ODBC** üzerinden
Netezza'ya bağlanacak şekilde nasıl yapılandırılacağını açıklar.

Kurulumun *digna* tarafı her teknoloji için aynıdır: bağlantıların nerede oluşturulduğu,
özellik değerlerinin nasıl şifrelendiği, bir bağlantının nasıl test edildiği ve profil oluşturma
modlarının ne anlama geldiği. Bunlar [Veritabanı Bağlantılarına Genel Bakış](overview.md)
sayfasında açıklanmıştır. Bu sayfa Netezza'ya özgü konuları ele alır.

---

## 1. ODBC Sürücüsünü Kurun {: #1-install-the-odbc-driver }

Üreticinin resmi kurulum kılavuzunu izleyerek *digna* arka ucunu çalıştıran makineye
**NetezzaSQL** ODBC sürücüsünü (IBM Netezza istemci araçlarının bir parçası) kurun.

Kayıtlı sürücü adının tamamını
[ODBC Sürücüsünü digna Ana Makinesine Kurun](overview.md#install-the-driver) bölümünde
açıklandığı şekilde ana makinenizden okuyun.

---

## 2. ODBC Özellikleri {: #2-odbc-properties }

!!! important "Bir örnek, bir şartname değil"

    Aşağıdaki küme, çalıştığı bilinen bir kombinasyondur. Özellikler NetezzaSQL sürücüsüne
    aittir; bu nedenle adları, varsayılan değerleri ve kabul edilen değerleri istemci
    sürümlerine ve platformlara göre farklılık gösterir. TLS ile korunan bir cihaz ise burada
    gösterilenlerden daha fazla özellik gerektirir. Bunu bir başlangıç noktası olarak kullanın
    ve kurduğunuz istemci sürümünün dokümantasyonunu kontrol edin.

**Add DB Connection** ekranında aşağıdaki özellikleri ekleyin:

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | *digna* ana makinesinde kayıtlı sürücü adıyla eşleşmelidir. Süslü parantezler bu adın olağan yazılış biçimidir |
| `SERVER` | `netezza.example.com` | Sunucu adı veya IP adresi |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Oturumun başladığı veritabanı |
| `UID` | `ADMIN` | Veritabanı kullanıcısı |
| `PWD` | `<password>` | **Encrypted** seçeneğini işaretleyin |

Ortaya çıkan bağlantı dizesi şöyle görünür:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

Sürücü sürümünüze, kurulumunuza ve güvenlik gereksinimlerinize bağlı olarak başka özellikler de
gerekebilir; örneğin TLS ile korunan bir cihaz için `SecurityLevel` ve `CaCertFile`. Sürücünün
*Advanced*, *SSL* ve *Driver* iletişim kutularının sunduğu her seçenek bir özellik olarak
eklenebilir.

---

## 3. *digna* Yapılandırması {: #3-digna-configuration }

**Add DB Connection** ekranında aşağıdakileri girin:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Netezza ile İlgili Notlar {: #4-notes-on-netezza }

- **Hem kataloglar hem de şemalar geçerlidir.** *digna*, kullanıcının görebildiği veritabanlarını
  (`_V_DATABASE` üzerinden) katalog olarak ve bunların şemalarını (`_V_SCHEMA` üzerinden)
  altlarında listeler; böylece tek bir bağlantı birden fazla veritabanındaki kaynaklara hizmet
  edebilir. `DATABASE` yalnızca oturumun nerede başlayacağını belirler.
- **Tanımlayıcılar**, tırnak içinde oluşturulmadıkları sürece **büyük harflidir**; yukarıdaki
  örneklerde `TEST` ve `ADMIN` kullanılmasının nedeni budur.
- **Profil oluşturma modları.** *Permanent* çalışma tablolarını **Work Schema** içinde
  oluşturur, bu nedenle kullanıcının orada `CREATE TABLE` yetkisine ihtiyacı vardır. *Session*
  `CREATE TEMPORARY TABLE` kullanır ve **Work Schema**'ya dokunmaz. *Standard* yalnızca okuma
  erişimi gerektirir.

---

## 5. Sürücüyü Doğrulama (isteğe bağlı) {: #5-verifying-the-driver-optional }

DSN'siz bir bağlantı için bir ODBC veri kaynağı yapılandırmak gerekli değildir; ancak sürücünün
kendi iletişim kutusu, bunları *digna*'ya girmeden önce sürücünün ve kimlik bilgilerinizin
çalıştığını doğrulamanın pratik bir yoludur.

#### Adım 1
![Adım 1](images/netezza/create_odbc_data_source_step1.png)

**DSN Options** içindeki alanlar, [bölüm 2](#2-odbc-properties) içindeki özelliklere birebir
karşılık gelir. Netezza sürücünüze, kurulumunuza ve güvenlik gereksinimlerinize bağlı olarak
**Advanced DSN Options**, **SSL DSN Options** veya **Driver Options** sekmelerinde de bilgi
girmeniz gerekebilir; en basit kurulum için **DSN Options** yeterlidir.

**Test Connection** düğmesine tıklayın.

#### Adım 2
![Adım 2](images/netezza/create_odbc_data_source_step2.png)

Başarı ekranını gördüğünüzde sürücü çalışıyor ve değerler doğru demektir.
