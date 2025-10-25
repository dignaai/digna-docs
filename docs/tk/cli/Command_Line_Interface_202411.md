---
title: digna CLI Başvuru 2024.11 – Komutlar & Örnekler | digna Belgelendirme
description: digna CLI sürümü 2024.11 için eksiksiz başvuru. add-user, check-repo-connection, upgrade-repo, inspect, tls-status gibi komutlarla kullanıcıları, depoları ve verileri nasıl yöneteceğinizi öğrenin.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202411/
image: /assets/logo_square.png
---

# digna CLI Reference 2024.11
**2024-11-03**

Bu sayfa, ***digna*** CLI sürümü **2024.11** içinde kullanılabilen tüm komutları, kullanım örneklerini ve seçeneklerini belgelendirir.


---
## CLI Temelleri

---

## `help` Seçeneğinin Kullanımı

`--help` seçeneği, kullanılabilir komutlar ve bunların kullanımı hakkında bilgi sağlar. Bu seçeneğin iki ana kullanım şekli vardır:

1. **Genel Yardımı Görüntüleme:**
   
   `--help` seçeneğini ***digna*** komutunun hemen sonrasında kullanın.  
   ```bash
   dignacli --help
   ```

3.  **Belirli Komutlar İçin Yardım Alma:**  
  
    Belirli bir komut hakkında ayrıntılı bilgi için o komuta `--help` ekleyin.  
    Örneğin, `add-user` komutu hakkında yardım almak için şu komutu çalıştırın:
     ```bash
     dignacli add-user --help
     ```

     ### çıktı:
      
     - **Komut Açıklaması:** Komutun ne yaptığını ayrıntılı olarak açıklar.  
     - **Sözdizimi:** Gerekli ve isteğe bağlı argümanlar dahil olmak üzere tam sözdizimini gösterir.  
     - **Seçenekler:** Komuta özgü seçenekleri ve açıklamalarını listeler.  
     - **Örnekler:** Komutun etkili bir şekilde nasıl çalıştırılacağına dair örnekler sunar.

  
## `check-repo-connection` Komutunun Kullanımı

check-repo-connection komutu, ***digna*** CLI aracında belirtilen bir ***digna*** deposuna bağlantı ve erişimi test etmek için kullanılan bir yardımcı araçtır. Bu komut, CLI'nın depoyla etkileşime girebildiğini doğrular.
      
### Komut Kullanımı
```bash
dignacli check-repo-connection
```

Başarılı çalıştırıldığında, komut bağlantının onayını ve depo hakkında şu ayrıntıları çıktılar: Repository version, Host, Database ve Schema.  
  
Eğer depo bağlantısı başarılı olmazsa, doğru yapılandırma ayarları için config.toml dosyasını kontrol edin.

## `version` Komutunun Kullanımı

Yüklü *dignacli* sürümünü kontrol etmek için `--version` seçeneğini kullanın.  
  
### Komut Kullanımı
```bash
dignacli --version
```
  
### Örnek Çıktı
```bash
dignacli version 2024.11
```

## Günlükleme Seçeneklerinin Kullanımı
  
Varsayılan olarak, ***digna*** komutlarının konsol çıktısı minimal olacak şekilde tasarlanmıştır. Çoğu komut, aşağıdaki seçenekleri kullanarak ek bilgi sağlama olanağı sunar:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” ve “debug” ayrıntı düzeyini tanımlar, “logfile” anahtarı ise çıktının konsol penceresi yerine bir dosyaya yönlendirilmesine olanak tanır.

# Kullanıcı Yönetimi

## `add-user` Komutunun Kullanımı
  
add-user komutu, ***digna*** CLI içinde yeni bir kullanıcıyı ***digna*** sistemine eklemek için kullanılır.
  
### Komut Kullanımı
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argümanlar

- **USER_NAME**: Yeni kullanıcı için kullanıcı adı (zorunlu).
- **USER_FULL_NAME**: Yeni kullanıcının tam adı (zorunlu).
- **USER_PASSWORD**: Yeni kullanıcı için parola (zorunlu).

### Seçenekler

- `--is_superuser`, `-su`: Yeni kullanıcıyı yönetici olarak belirlemek için bayrak.
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir son geçerlilik tarihi belirler. Belirtilmezse hesap süresiz olur.

### Örnek

Kullanıcı adı `jdoe`, tam adı `John Doe` ve parolası `password123` olan yeni bir kullanıcı eklemek için:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Hesap son geçerlilik tarihi belirleyerek yeni bir kullanıcı eklemek için:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## `delete-user` Komutunun Kullanımı
  
`delete-user` komutu, ***digna*** CLI içinde mevcut bir kullanıcıyı ***digna*** sisteminden kaldırmak için kullanılır.
  
### Komut Kullanımı
```bash
dignacli delete-user USER_NAME
```
  
### Argümanlar
- **USER_NAME**: Silinecek kullanıcının kullanıcı adı (zorunlu). Bu komutun gerektirdiği tek argümandır.

### Örnek
```bash
dignacli delete-user jdoe
```
  
Bu komut çalıştırıldığında, `jdoe` kullanıcısı ***digna*** sisteminden kaldırılır; erişimi iptal edilir ve depo ile ilişkili verileri ve izinleri silinir.

## `modify-user` Komutunun Kullanımı

`modify-user` komutu, ***digna*** CLI içinde mevcut bir kullanıcının bilgilerini güncellemek için kullanılır.

### Komut Kullanımı
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argümanlar
  
- **USER_NAME**: Değiştirilecek kullanıcının kullanıcı adı (zorunlu).
- **USER_FULL_NAME**: Kullanıcının yeni tam adı (zorunlu).
  
### Seçenekler  
  
- `--is_superuser`, `-su`: Kullanıcıyı yükseltilmiş ayrıcalıklara sahip bir süper kullanıcı olarak ayarlar. Bu bayrağın değere ihtiyacı yoktur.  
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir son geçerlilik tarihi belirler. Belirtilmezse hesap süresiz olarak geçerli kalır.  
  
### Örnek
  
`jdoe` kullanıcısının tam adını “Johnathan Doe” olarak değiştirmek ve kullanıcıyı süper kullanıcı yapmak için:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## `modify-user-pwd` Komutunun Kullanımı
  
`modify-user-pwd` komutu, ***digna*** CLI içinde mevcut bir kullanıcının parolasını değiştirmek için kullanılır.
  
### Komut Kullanımı
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argümanlar
  
- **USER_NAME**: Parolası değiştirilecek kullanıcının kullanıcı adı (zorunlu).
- **USER_PWD**: Kullanıcının yeni parolası (zorunlu).
  
### Örnek
  
`jdoe` kullanıcısının parolasını `newpassword123` olarak değiştirmek için:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## `list-users` Komutunun Kullanımı

`list-users` komutu, ***digna*** CLI içinde ***digna*** sistemine kayıtlı tüm kullanıcıların listesini görüntüler.

### Komut Kullanımı

```bash
dignacli list-users
```

Bu komutu çalıştırmak, ***digna*** deposuna bağlanır ve tüm kullanıcıları ID, kullanıcı adı, tam adı, süper kullanıcı durumu ve son geçerlilik zaman damgalarını göstererek listeler.

# Depo Yönetimi

### `upgrade-repo` Komutunun Kullanımı
  
`upgrade-repo` komutu, ***digna*** CLI içinde ***digna*** deposunu yükseltmek veya başlatmak için kullanılır. Bu komut, güncellemeleri uygulamak veya depoyu ilk kez kurmak için gereklidir.
  
### Komut Kullanımı

```bash
dignacli upgrade-repo [options]
```
  
### Seçenekler
  
- `--simulation-mode`, `-s`: Etkinleştirildiğinde komut simülasyon modunda çalışır; yürütülecek SQL ifadelerini yazdırır ancak bunları gerçekten çalıştırmaz. Bu, değişiklikleri uygulamadan önce önizlemek için faydalıdır.  

  
### Örnek
  
***digna*** deposunu yükseltmek için seçenek olmadan komutu çalıştırabilirsiniz:
  
```bash
dignacli upgrade-repo
```  
Yükseltmeyi simülasyon modunda çalıştırmak (SQL ifadelerini uygulamadan görmek) için:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Bu komut, veritabanı şemasının ve diğer depo bileşenlerinin yazılımın en son sürümüyle uyumlu olmasını sağlayarak ***digna*** sisteminin bakımında kritik öneme sahiptir.

## `encrypt` Komutunun Kullanımı
  
`encrypt` komutu, ***digna*** CLI içinde bir parolayı şifrelemek için kullanılır.
  
### Komut Kullanımı
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argümanlar
- **PASSWORD**: Şifrelenmesi gereken parola (zorunlu).
  
### Örnek
  
Bir parolayı şifrelemek için parolayı argüman olarak vermeniz gerekir.   
Örneğin, `mypassword123` parolasını şifrelemek için:
```bash
dignacli encrypt mypassword123
```
Bu komut, sağlanan parolanın şifrelenmiş sürümünü çıktılar; bu sürüm daha sonra güvenli bağlamlarda kullanılabilir. Parola argümanı sağlanmazsa, CLI eksik argüman olduğunu belirten bir hata gösterir.

## `generate-key` Komutunun Kullanımı
  
`generate-key` komutu, ***digna*** deposunda saklanan parolaları güvence altına almak için gerekli olan bir Fernet anahtarı oluşturmak için kullanılır.
  
### Komut Kullanımı
```bash
dignacli generate-key
```
  
# Veri Yönetimi

## `clean-up` Komutunun Kullanımı

`clean-up` komutu, ***digna*** CLI içinde belirli bir proje kapsamında bir veya daha fazla veri kaynağı için profilleri, tahminleri ve Trafik Işık Sistemi verilerini (Traffic Light System - TLS) kaldırmak için kullanılır. Bu komut, veri yaşam döngüsü yönetimi için önemlidir ve eski veya gereksiz verilerin temizlenmesine yardımcı olur.

### Komut Kullanımı

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argümanlar
  
- **PROJECT_NAME**: Verilerin kaldırılağı proje adı (zorunlu). Bu argümana all-projects anahtar kelimesi verildiğinde, ***digna*** mevcut tüm projeler üzerinde yineleme yapar ve komutu uygular.
- **FROM_DATE**: Veri temizliği için başlangıç tarih ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (zorunlu).
- **TO_DATE**: Veri temizliği için bitiş tarih ve saati; FROM_DATE ile aynı formatları takip eder (zorunlu).
  
### Seçenekler
  
- `--table-name`, `-tn`: Temizleme işlemini proje içindeki belirli bir tablo ile sınırlar.
- `--table-filter`, `-tf`: İsimlerinde belirtilen alt dizeyi içeren tablolara temizlemeyi sınırlamak için filtre uygular.
- `--timing`, `-tm`: Tamamlandıktan sonra temizleme işleminin süre bilgisini gösterir.
- `--help`: clean-up komutu için yardım bilgilerini gösterir ve çıkar.
  
### Örnek
  
ProjectA projesinden 1 Ocak 2023 ile 30 Haziran 2023 arasındaki verileri kaldırmak için:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Sadece `Table1` adlı belirli bir tablodan veri kaldırmak için:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Bu komut, veri depolamayı yönetmeye ve deponun yalnızca ilgili bilgileri içermesini sağlamaya yardımcı olur.

## `inspect` Komutunun Kullanımı

`inspect` komutu, ***digna*** CLI içinde belirli bir proje kapsamındaki bir veya daha fazla veri kaynağı için profiller, tahminler ve Trafik Işık Sistemi verileri oluşturmak için kullanılır. Bu komut, belirli bir dönemde verilerin analiz edilmesine ve izlenmesine yardımcı olur.

### Komut Kullanımı

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argümanlar
  
- **PROJECT_NAME**: İncelemenin yapılacağı proje adı (zorunlu). Bu argümana all-projects anahtar kelimesi verildiğinde, ***digna*** mevcut tüm projeler üzerinde yineleme yapar ve komutu uygular.
- **FROM_DATE**: İncelemenin başlayacağı tarih ve saat. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (zorunlu).
- **TO_DATE**: İncelemenin biteceği tarih ve saat; FROM_DATE ile aynı formatları takip eder (zorunlu).
  
### Seçenekler

- `--table-name`, `-tn`: İncelemeyi proje içindeki belirli bir tablo ile sınırlar.
- `--table-filter`, `-tf`: İsimlerinde belirtilen alt dizeyi içeren tablolarda inceleme yapacak şekilde filtre uygular.
- `--do-profile`: Profillerin yeniden toplanmasını tetikler. Varsayılan do-profile'dır.
- `--no-do-profile`: Profillerin yeniden toplanmasını engeller.
- `--do-prediction`: Tahminlerin yeniden hesaplanmasını tetikler. Varsayılan do-prediction'dır.
- `--no-do-prediction`: Tahminlerin yeniden hesaplanmasını engeller.
- `--do-alert-status`: Uyarı durumlarının yeniden hesaplanmasını tetikler. Varsayılan do-alert-status'dur.
- `--no-do-alert-status`: Uyarı durumlarının yeniden hesaplanmasını engeller.
- `--timing`, `-tm`: Tamamlandıktan sonra inceleme işleminin süresini gösterir.
  
### Örnek
  
`ProjectA` projesi için 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri incelemek için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Yalnızca belirli bir tabloyu incelemek ve tahminlerin yeniden hesaplanmasını zorlamak için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Bu komut, güncellenmiş profiller ve tahminler oluşturmak, veri bütünlüğünü izlemek ve belirtilen proje zaman aralığı içinde uyarı sistemlerini yönetmek için kullanışlıdır.

## `tls-status` Komutunun Kullanımı

`tls-status` komutu, ***digna*** CLI içinde belirli bir tarihte bir proje içindeki belirli bir tablo için Trafik Işık Sistemi (TLS) durumunu sorgulamak için kullanılır. Trafik Işık Sistemi, verinin sağlığı ve kalitesi hakkında içgörüler sağlar ve dikkat gerektiren sorunları veya uyarıları gösterir.
  
### Komut Kullanımı
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argümanlar
  
- **PROJECT_NAME**: TLS durumu sorgulanan proje adı (zorunlu).
- **TABLE_NAME**: TLS durumu gereken proje içindeki tablo (zorunlu).
- **DATE**: TLS durumunun sorgulandığı tarih, genellikle %Y-%m-%d formatında (zorunlu).
  
### Örnek
  
`ProjectA` projesinde `UserData` adlı tablonun 1 Temmuz 2024 tarihindeki TLS durumunu kontrol etmek için:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Bu komut, önceden tanımlanmış kriterlere dayalı olarak açık ve uygulanabilir bir durum raporu sağlayarak kullanıcıların veri kalitesini izlemesine ve sürdürmesine yardımcı olur.

## `list-projects` Komutunun Kullanımı
  
`list-projects` komutu, ***digna*** CLI içinde mevcut tüm projelerin listesini görüntülemek için kullanılır.
  
### Komut Kullanımı
  
```bash
dignacli list-projects
```

Bu komut, birden çok projeyi yöneten yöneticiler ve kullanıcılar için özellikle kullanışlıdır; ***digna*** deposundaki mevcut projelerin hızlı bir özetini sağlar.

## `list-ds` Komutunun Kullanımı

`list-ds` komutu, ***digna*** CLI içinde belirli bir proje kapsamındaki mevcut tüm veri kaynaklarının listesini görüntülemek için kullanılır. Bu komut, analiz ve yönetim için mevcut veri varlıklarını anlamaya yardımcı olur.

### Komut Kullanımı
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının listelendiği proje adı (zorunlu).
  
### Örnek
  
`ProjectA` adlı projedeki tüm veri kaynaklarını listelemek için:
  
```bash
dignacli list-ds ProjectA
```
  
Bu komut, bir projedeki veri kaynaklarına genel bir bakış sağlar ve kullanıcıların veri ortamını daha etkin bir şekilde gezmelerine ve yönetmelerine yardımcı olur.