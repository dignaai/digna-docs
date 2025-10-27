---
title: digna CLI Referansı 2024.11 – Komutlar & Örnekler | digna Dokümantasyonu
description: digna CLI sürümü 2024.11 için eksiksiz referans. add-user, check-repo-connection, upgrade-repo, inspect, tls-status ve daha fazlası gibi komutlarla kullanıcıları, depoları ve verileri nasıl yöneteceğinizi öğrenin.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202411/
image: /assets/logo_square.png
---

# digna CLI Referansı 2024.11
**2024-11-03**

Bu sayfa, ***digna*** CLI sürümü **2024.11** içinde kullanılabilen tüm komutları, kullanım örneklerini ve seçenekleri belgelemektedir.


---
## CLI Temelleri

---

## `help` Seçeneğinin Kullanımı

`--help` seçeneği, kullanılabilir komutlar ve bunların kullanımı hakkında bilgi sağlar. Bu seçeneği kullanmanın iki ana yolu vardır:

1. **Genel Yardımı Görüntüleme:**
   
   `--help` seçeneğini ***dignacli*** komutundan hemen sonra kullanın.  
   ```bash
   dignacli --help
   ```

2. **Belirli Komutlar İçin Yardım Alma:**  
  
   Belirli bir komut hakkında ayrıntılı bilgi almak için o komuta `--help` ekleyin.  
   Örneğin, `add-user` komutu ile ilgili yardım almak için:
   ```bash
   dignacli add-user --help
   ```

   ### çıktı:
      
   - **Komut Açıklaması:** Komutun ne yaptığını ayrıntılı olarak açıklar.  
   - **Sözdizimi:** Gerekli ve isteğe bağlı argümanlar dahil olmak üzere kesin sözdizimini gösterir.  
   - **Seçenekler:** Komuta özgü seçenekleri ve açıklamalarını listeler.  
   - **Örnekler:** Komutun etkili bir şekilde nasıl çalıştırılacağını gösteren örnekler sağlar.

  
## `check-repo-connection` Komutunun Kullanımı

check-repo-connection komutu, ***digna*** CLI aracında belirli bir ***digna*** deposuna bağlantı ve erişimi test etmek için kullanılan bir yardımcı programdır. Bu komut, CLI'nin depoyla etkileşime girebildiğinden emin olur.
      
### Komut Kullanımı
```bash
dignacli check-repo-connection
```

Başarılı çalıştırma sonrasında komut, bağlantının onayını ve depoyla ilgili bilgileri çıktılar: Depo sürümü, Host, Veritabanı ve Şema.  
  
Eğer depo bağlantısı başarılı değilse, config.toml dosyasındaki yapılandırma ayarlarını kontrol edin.

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

## Günlükleme (logging) Seçeneklerinin Kullanımı
  
Varsayılan olarak, ***digna*** komutlarının konsol çıktısı minimal olacak şekilde tasarlanmıştır. Çoğu komut aşağıdaki seçenekleri kullanarak ek bilgi sağlama olanağı sunar:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” ve “debug” detay seviyesini tanımlar, oysa “logfile” anahtarı çıktıyı konsol yerine bir dosyaya yönlendirmeye olanak tanır.

# Kullanıcı Yönetimi

## `add-user` Komutunun Kullanımı
  
add-user komutu, ***digna*** CLI'de ***digna*** sistemine yeni bir kullanıcı eklemek için kullanılır.
  
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
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir sona erme tarihi belirler. Belirtilmezse hesap süresiz olur.

### Örnek

Kullanıcı adı `jdoe`, tam adı `John Doe` ve parolası `password123` olan yeni bir kullanıcı eklemek için:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Hesap sona erme tarihi belirleyerek yeni bir kullanıcı eklemek için:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## `delete-user` Komutunun Kullanımı
  
`delete-user` komutu, ***digna*** CLI'de mevcut bir kullanıcıyı ***digna*** sisteminden kaldırmak için kullanılır.
  
### Komut Kullanımı
```bash
dignacli delete-user USER_NAME
```
  
### Argümanlar
- **USER_NAME**: Silinecek kullanıcının kullanıcı adı (zorunlu). Bu, komutun gerektirdiği tek argümandır.

### Örnek
```bash
dignacli delete-user jdoe
```
  
Bu komut çalıştırıldığında `jdoe` kullanıcısı ***digna*** sisteminden kaldırılacak, erişimi iptal edilecek ve depo içindeki ilgili veri ve izinleri silinecektir.

## `modify-user` Komutunun Kullanımı

`modify-user` komutu, ***digna*** CLI'de mevcut bir kullanıcının bilgilerini güncellemek için kullanılır.

### Komut Kullanımı
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argümanlar
  
- **USER_NAME**: Güncellenecek kullanıcının kullanıcı adı (zorunlu).
- **USER_FULL_NAME**: Kullanıcının yeni tam adı (zorunlu).
  
### Seçenekler  
  
- `--is_superuser`, `-su`: Kullanıcıyı süper kullanıcı olarak ayarlar; yükseltilmiş ayrıcalıklar verir. Bu bayrak bir değere ihtiyaç duymaz.  
- `--valid_until`, `-vu`: Kullanıcı hesabı için YYYY-MM-DD HH:MI:SS formatında bir sona erme tarihi belirler. Verilmezse hesap süresiz geçerli kalır.  
  
### Örnek
  
`jdoe` kullanıcısının tam adını “Johnathan Doe” olarak değiştirmek ve kullanıcıyı süper kullanıcı yapmak için:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## `modify-user-pwd` Komutunun Kullanımı
  
`modify-user-pwd` komutu, ***digna*** CLI'de mevcut bir kullanıcının parolasını değiştirmek için kullanılır.
  
### Komut Kullanımı
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argümanlar
  
- **USER_NAME**: Parolası değiştirilecek kullanıcının kullanıcı adı (zorunlu).
- **USER_PWD**: Kullanıcı için yeni parola (zorunlu).
  
### Örnek
  
`jdoe` kullanıcısının parolasını `newpassword123` olarak değiştirmek için:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## `list-users` Komutunun Kullanımı

`list-users` komutu, ***digna*** CLI'de ***digna*** sistemine kayıtlı tüm kullanıcıların bir listesini gösterir.

### Komut Kullanımı

```bash
dignacli list-users
```

Bu komutu çalıştırmak, ***digna*** deposuna bağlanır ve tüm kullanıcıları; ID, kullanıcı adı, tam ad, süper kullanıcı durumu ve sona erme zaman damgalarını göstererek listeler.

# Depo Yönetimi

### `upgrade-repo` Komutunun Kullanımı
  
`upgrade-repo` komutu, ***digna*** CLI'de ***digna*** deposunu yükseltmek veya başlatmak için kullanılır. Bu komut, güncellemeleri uygulamak veya depo altyapısını ilk kez kurmak için gereklidir.
  
### Komut Kullanımı

```bash
dignacli upgrade-repo [options]
```
  
### Seçenekler
  
- `--simulation-mode`, `-s`: Etkinleştirildiğinde komut simülasyon modunda çalışır; çalıştırılacak SQL ifadelerini yazdırır ancak bunları gerçekte çalıştırmaz. Değişiklikleri uygulamadan önce önizleme için faydalıdır.  

  
### Örnek
  
***digna*** deposunu yükseltmek için komutu herhangi bir seçenek olmadan çalıştırabilirsiniz:
  
```bash
dignacli upgrade-repo
```  
Yükseltmeyi simülasyon modunda çalıştırmak (SQL ifadelerini görüntülemek için):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Bu komut, veritabanı şemasının ve depo bileşenlerinin yazılımın en son sürümüyle uyumlu olmasını sağlayarak ***digna*** sisteminin bakımında kritik öneme sahiptir.

## `encrypt` Komutunun Kullanımı
  
`encrypt` komutu, ***digna*** CLI'de bir parolayı şifrelemek için kullanılır.
  
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
Bu komut, verilen parolanın şifrelenmiş halini çıktılar; bu çıktı daha güvenli bağlamlarda kullanılabilir. Eğer parola argümanı verilmezse, CLI eksik argüman olduğunu belirten bir hata gösterir.

## `generate-key` Komutunun Kullanımı
  
`generate-key` komutu, ***digna*** deposunda saklanan parolaları güvence altına almak için gerekli olan bir Fernet anahtarı oluşturmak için kullanılır.
  
### Komut Kullanımı
```bash
dignacli generate-key
```
  
# Veri Yönetimi

## `clean-up` Komutunun Kullanımı

`clean-up` komutu, ***digna*** CLI'de bir proje içindeki bir veya daha fazla veri kaynağı için profilleri, tahminleri ve Trafik Lambası Sistemi verilerini kaldırmak için kullanılır. Bu komut, veri yaşam döngüsü yönetimi için önemlidir; eski veya gereksiz verileri temizleyerek düzenli ve verimli bir veri ortamı sağlamaya yardımcı olur.

### Komut Kullanımı

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argümanlar
  
- **PROJECT_NAME**: Verilerin kaldırılacağı proje adı (zorunlu). Bu argümana all-projects anahtar sözcüğü verilirse ***digna*** mevcut tüm projeler üzerinde iterasyon yaparak bu komutu uygular.
- **FROM_DATE**: Veri silme işleminin başlangıç tarih ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (zorunlu).
- **TO_DATE**: Veri silme işleminin bitiş tarih ve saati; FROM_DATE ile aynı formatları takip eder (zorunlu).
  
### Seçenekler
  
- `--table-name`, `-tn`: Temizleme işlemini proje içindeki belirli bir tablo ile sınırlamak için.
- `--table-filter`, `-tf`: Tablo adlarında belirtilen alt diziyi içeren tablolarla sınırlamak için filtre uygular.
- `--timing`, `-tm`: Temizleme tamamlandıktan sonra işlem süresini gösterir.
- `--help`: clean-up komutu için yardım bilgisi gösterir ve çıkar.
  
### Örnek
  
ProjectA projesinden 1 Ocak 2023 ile 30 Haziran 2023 arasındaki verileri silmek için:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Sadece `Table1` adlı belirli bir tablodan veri silmek için:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Bu komut, depolama yönetimine yardımcı olur ve deponun yalnızca ilgili bilgileri içermesini sağlar.

## `inspect` Komutunun Kullanımı

`inspect` komutu, ***digna*** CLI'de bir proje içindeki bir veya daha fazla veri kaynağı için profiller, tahminler ve Trafik Lambası Sistemi verilerini oluşturmak için kullanılır. Bu komut, belirli bir dönem boyunca verilerin analiz edilmesine ve izlenmesine yardımcı olur.

### Komut Kullanımı

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argümanlar
  
- **PROJECT_NAME**: İncelemenin yapılacağı proje adı (zorunlu). Bu argümana all-projects anahtar sözcüğü verilirse ***digna*** mevcut tüm projeler üzerinde iterasyon yaparak bu komutu uygular.
- **FROM_DATE**: İncelemenin başlayacağı tarih ve saat. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (zorunlu).
- **TO_DATE**: İncelemenin biteceği tarih ve saat; FROM_DATE ile aynı formatları takip eder (zorunlu).
  
### Seçenekler

- `--table-name`, `-tn`: İncelemeyi proje içindeki belirli bir tablo ile sınırlamak için.
- `--table-filter`, `-tf`: Adında belirtilen alt dizeyi içeren tabloları incelemek için filtre uygular.
- `--do-profile`: Profillerin yeniden toplanmasını tetikler. Varsayılan do-profile'dır.
- `--no-do-profile`: Profillerin yeniden toplanmasını engeller.
- `--do-prediction`: Tahminlerin yeniden hesaplanmasını tetikler. Varsayılan do-prediction'dır.
- `--no-do-prediction`: Tahminlerin yeniden hesaplanmasını engeller.
- `--do-alert-status`: Alarm durumlarının yeniden hesaplanmasını tetikler. Varsayılan do-alert-status'dur.
- `--no-do-alert-status`: Alarm durumlarının yeniden hesaplanmasını engeller.
- `--timing`, `-tm`: İnceleme tamamlandıktan sonra işlem süresini gösterir.
  
### Örnek
  
ProjectA projesi için 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri incelemek için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Sadece belirli bir tabloyu incelemek ve tahminlerin yeniden hesaplanmasını zorlamak için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Bu komut, güncellenmiş profiller ve tahminler oluşturmak, veri bütünlüğünü izlemek ve belirli bir proje zaman aralığında alarm sistemlerini yönetmek için faydalıdır.

## `tls-status` Komutunun Kullanımı

`tls-status` komutu, ***digna*** CLI'de belirli bir proje içindeki bir tablonun belirli bir tarihteki Trafik Lambası Sistemi (TLS) durumunu sorgulamak için kullanılır. Trafik Lambası Sistemi, verinin sağlığı ve kalitesi hakkında bilgiler sunar; potansiyel sorunlar veya dikkat gerektiren uyarılar hakkında fikir verir.
  
### Komut Kullanımı
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argümanlar
  
- **PROJECT_NAME**: TLS durumunun sorgulandığı proje adı (zorunlu).
- **TABLE_NAME**: TLS durumunun gerekli olduğu proje içindeki tablo adı (zorunlu).
- **DATE**: TLS durumunun sorgulandığı tarih, genellikle %Y-%m-%d formatında (zorunlu).
  
### Örnek
  
ProjectA projesinde UserData adlı tablonun 1 Temmuz 2024 tarihindeki TLS durumunu kontrol etmek için:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Bu komut, önceden tanımlanmış kriterlere dayalı olarak net ve eyleme geçirilebilir bir durum raporu sağlayarak kullanıcıların veri kalitesini izlemesine ve korumasına yardımcı olur.

## `list-projects` Komutunun Kullanımı
  
`list-projects` komutu, ***digna*** CLI'de mevcut tüm projelerin listesini görüntülemek için kullanılır.
  
### Komut Kullanımı
  
```bash
dignacli list-projects
```

Bu komut, birden çok proje yöneten yöneticiler ve kullanıcılar için özellikle faydalıdır; ***digna*** deposunda bulunabilecek projelerin hızlı bir özetini sağlar.

## `list-ds` Komutunun Kullanımı

`list-ds` komutu, ***digna*** CLI'de belirli bir proje içindeki mevcut tüm veri kaynaklarının listesini görüntülemek için kullanılır. Bu komut, analiz ve yönetim için kullanılabilir veri varlıklarını anlamaya yardımcı olur.

### Komut Kullanımı
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının listeleneceği proje adı (zorunlu).
  
### Örnek
  
ProjectA adlı projedeki tüm veri kaynaklarını listelemek için:
  
```bash
dignacli list-ds ProjectA
```
  
Bu komut, kullanıcıların bir projedeki veri kaynaklarına genel bir bakış elde etmelerini sağlar ve veri ortamını daha etkin yönetmelerine yardımcı olur.