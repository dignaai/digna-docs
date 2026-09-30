---
title: Apache Hive Bağlayıcısı – Veritabanı Entegrasyonu | digna Dokümantasyonu
description: digna'yı DSN'siz bir bağlantı dizesiyle ODBC üzerinden Apache Hive'a bağlanacak şekilde yapılandırın. Cloudera Hive ODBC sürücüsünü, kimlik doğrulama mekanizmalarını, aktarım modlarını ve digna tarafındaki bağlantı ayarlarını kapsar.
image: /assets/logo_square.png
---


# Hive için Kaynak Bağlayıcısı

Bu kılavuz, *digna*'nın **DSN'siz** bir bağlantı dizesi kullanarak **ODBC** üzerinden Apache
Hive'a bağlanacak şekilde nasıl yapılandırılacağını açıklar.

Kurulumun *digna* tarafı her teknoloji için aynıdır: bağlantıların nerede oluşturulduğu,
özellik değerlerinin nasıl şifrelendiği, bir bağlantının nasıl test edildiği ve profil oluşturma
modlarının ne anlama geldiği. Bunlar [Veritabanı Bağlantılarına Genel Bakış](overview.md)
sayfasında açıklanmıştır. Bu sayfa Hive'a özgü konuları ele alır.

---

## 1. ODBC Sürücüsünü Kurun {: #1-install-the-odbc-driver }

Üreticinin resmi kurulum kılavuzunu izleyerek *digna* arka ucunu çalıştıran makineye
**Cloudera ODBC Driver for Apache Hive**'ı kurun.

Kayıtlı sürücü adının tamamını
[ODBC Sürücüsünü digna Ana Makinesine Kurun](overview.md#install-the-driver) bölümünde
açıklandığı şekilde ana makinenizden okuyun.

---

## 2. ODBC Özellikleri {: #2-odbc-properties }

!!! important "Bir örnek, bir şartname değil"

    Aşağıdaki küme, çalıştığı bilinen bir kombinasyondur. Özellikler Cloudera Hive sürücüsüne
    aittir; bu nedenle adları, varsayılan değerleri ve kabul edilen değerleri sürücü
    sürümlerine ve platformlara göre farklılık gösterir. HiveServer2'nin neyi kabul ettiği ise
    tamamen kümenin nasıl güvence altına alındığına (kimlik doğrulama mekanizması, aktarım modu,
    TLS, ağ geçidi) bağlıdır. Bunu bir başlangıç noktası olarak kullanın ve kurduğunuz sürücü
    sürümünün dokümantasyonunu kontrol edin.

**Add DB Connection** ekranında aşağıdaki özellikleri ekleyin:

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | *digna* ana makinesinde kayıtlı sürücü adıyla eşleşmelidir |
| `HOST` | `hive.example.com` | HiveServer2 ana makine adı veya IP adresi |
| `PORT` | `10000` | HiveServer2 portu; HTTP aktarımı için `10001` |

Ortaya çıkan bağlantı dizesi şöyle görünür:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Kimlik doğrulama

Güvenliği yapılandırılmamış bir HiveServer2, yukarıdaki üç özelliği olduğu gibi kabul eder.
Kimlik doğrulamanın etkin olduğu durumlarda şunları ekleyin:

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `AuthMech` | `3` | `0` kimlik doğrulama yok, `2` yalnızca kullanıcı adı, `3` kullanıcı adı ve parola, `1` Kerberos |
| `UID` | `digna_source_user` | `AuthMech` `2` ve `3` için gereklidir |
| `PWD` | `<password>` | `AuthMech` `3` için gereklidir. **Encrypted** seçeneğini işaretleyin |

Kerberos (`AuthMech=1`) için *digna* ana makinesinin ayrıca geçerli bir bilete veya keytab
dosyasına ve sürücünün belgelediği `KrbHostFQDN`, `KrbServiceName` ve `KrbRealm`
özelliklerine ihtiyacı vardır.

### Aktarım ve TLS

| Anahtar | Örnek değer | Notlar |
|---|---|---|
| `ThriftTransport` | `2` | `0` ikili (varsayılan, port 10000), `1` SASL, `2` HTTP (port 10001; bir Knox ağ geçidinin beklediği mod) |
| `HTTPPath` | `cliservice` | `ThriftTransport=2` ile birlikte |
| `SSL` | `1` | HiveServer2'nin TLS ile korunduğu durumlarda |
| `Schema` | `dignadata` | Oturumun başladığı Hive veritabanı. İsteğe bağlıdır; *digna* sorgularını tam nitelikli adlarla yazar |

---

## 3. *digna* Yapılandırması {: #3-digna-configuration }

**Add DB Connection** ekranında aşağıdakileri girin:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Hive ile İlgili Notlar {: #4-notes-on-hive }

- **Kataloglar sürücüden gelir.** Hive'ın kendine ait bir kataloğu yoktur, bu nedenle *digna*
  sürücünün bildirdiğini (normalde `HIVE` adlı tek bir giriş) alır ve Hive veritabanlarını
  bunun altında şema olarak listeler.
- **Work Schema bir Hive veritabanıdır.** *Permanent* profil oluşturma için kullanıcının bu
  veritabanında tablo oluşturma ve silme hakkına sahip olması ve alttaki depolama konumunun
  yazılabilir olması gerekir.
- **Profil oluşturma modları.** *Permanent* çalışma tablolarını **Work Schema** içinde
  oluşturur. *Session* `CREATE TEMPORARY TABLE` kullanır; bu, geçici tabloları destekleyen bir
  HiveServer2 gerektirir ve **Work Schema**'ya dokunmaz. *Standard* yalnızca okuma erişimi
  gerektirir ve *digna*'nın hiç yazma erişimi olmayan bir kümede seçilecek moddur.
- **Profil oluşturma bir tarama değil, bir dizi sorgudur.** Her istatistik HiveServer2
  tarafından hesaplanır, bu nedenle *digna* kullanıcısının iş gönderdiği kuyruğun inceleme
  penceresi için yeterli kapasitesi olmalıdır.

---

## 5. Sürücüyü Doğrulama (isteğe bağlı) {: #5-verifying-the-driver-optional }

DSN'siz bir bağlantı için bir ODBC veri kaynağı yapılandırmak gerekli değildir; ancak sürücünün
kendi iletişim kutusu, bunları *digna*'ya girmeden önce sürücünün, aktarım modunun ve kimlik
bilgilerinizin çalıştığını doğrulamanın pratik bir yoludur.

#### Adım 1
![Adım 1](images/hive/create_odbc_data_source_step1.png)

Buradaki **Host**, **Port**, **Database**, **Mechanism** ve **Thrift Transport** alanları,
[bölüm 2](#2-odbc-properties) içindeki `HOST`, `PORT`, `Schema`, `AuthMech` ve
`ThriftTransport` özellikleridir.

#### Adım 2 – Bağlantıyı test edin

Parolayı girin ve **Test** düğmesine tıklayın.

![Adım 2](images/hive/create_odbc_data_source_step2.png)

Başarılı bir testten sonra **OK** düğmesine tıklayın.
