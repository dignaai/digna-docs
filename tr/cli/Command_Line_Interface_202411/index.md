# digna CLI Reference 2024.11
**2024-11-03**

Bu sayfa, ***digna*** CLI sürümü **2024.11**'de kullanılabilen tüm komutları, kullanım örnekleri ve seçenekleriyle birlikte belgelendirir.


---
## CLI Temelleri

---

## `help` Seçeneğinin Kullanımı

`--help` seçeneği, mevcut komutlar ve bunların kullanımı hakkında bilgi sağlar. Bu seçeneğin kullanılmasına dair iki ana yol vardır:

1. **Genel Yardımı Görüntüleme:**
   
    `--help`'i ***dignacli*** anahtar kelimesinden hemen sonra kullanın.  
   ```bash
   dignacli --help
   ```

3.  **Belirli Komutlar İçin Yardım Alma:**  
  
    Belirli bir komut hakkında ayrıntılı bilgi almak için `--help`'i o komuta ekleyin.  
    Örneğin, `add-user` komutu hakkında yardım almak için şu komutu çalıştırın:
     ```bash
     dignacli add-user --help
     ```

     ### çıktı:
      
     - **Komut Açıklaması:** Komutun ne yaptığını ayrıntılı şekilde açıklar.  
     - **Sözdizimi:** Gerekli ve isteğe bağlı argümanlar da dahil olmak üzere tam sözdizimini gösterir.  
     - **Seçenekler:** Komuta özgü seçenekleri ve bunların açıklamalarını listeler.  
     - **Örnekler:** Komutun etkili şekilde nasıl çalıştırılacağına dair örnekler sağlar.

  
## `check-repo-connection` Komutunun Kullanımı

check-repo-connection komutu, ***digna*** CLI aracında belirtilen ***digna*** repository'sine erişim ve bağlantıyı test etmek için kullanılan bir yardımcı araçtır. Bu komut, CLI'nın repository ile etkileşime girebildiğini doğrular.
      
### Komut Kullanımı
```bash
dignacli check-repo-connection
```

Başarılı yürütme durumunda komut, bağlantının doğrulandığını ve repository hakkında Repository version, Host, Database ve Schema gibi bilgileri çıktılar.  
  
Eğer repository bağlantısı başarılı değilse, doğru yapılandırma ayarları için config.toml dosyasını kontrol edin.

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

## Logging Seçeneklerinin Kullanımı
  
Varsayılan olarak, ***digna*** komutlarının konsol çıktısı minimal olacak şekilde tasarlanmıştır. Çoğu komut, aşağıdaki seçenekleri kullanarak ek bilgi sağlama imkânı sunar:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” ve “debug” ayrıntı düzeyini belirlerken, “logfile” anahtarı çıktıyı konsol penceresi yerine bir dosyaya yönlendirmeye olanak tanır.

# Kullanıcı Yönetimi

## `add-user` Komutunun Kullanımı
  
add-user komutu, ***digna*** CLI içinde ***digna*** sistemine yeni bir kullanıcı eklemek için kullanılır.
  
### Komut Kullanımı
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argümanlar

- **USER_NAME**: Yeni kullanıcı için kullanıcı adı (zorunlu).
- **USER_FULL_NAME**: Yeni kullanıcının tam adı (zorunlu).
- **USER_PASSWORD**: Yeni kullanıcı için parola (zorunlu).

### Seçenekler

- `--is_superuser`, `-su`: Yeni kullanıcıyı yönetici (admin) olarak belirtme bayrağı.
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir son geçerlilik tarihi ayarlar. Ayarlanmazsa hesap süresiz geçerlidir.

### Örnek

`jdoe` kullanıcı adı, `John Doe` tam adı ve `password123` parolası ile yeni bir kullanıcı eklemek için:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Bir kullanıcı ekleyip hesap son kullanma tarihini ayarlamak için:
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
  
Bu komut çalıştırıldığında `jdoe` kullanıcısı ***digna*** sisteminden kaldırılacak, erişimi iptal edilecek ve repository'deki ilgili verileri ve izinleri silinecektir.

## `modify-user` Komutunun Kullanımı

`modify-user` komutu, ***digna*** CLI içinde mevcut bir kullanıcının bilgilerini güncellemek için kullanılır.

### Komut Kullanımı
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argümanlar
  
- **USER_NAME**: Değiştirilecek kullanıcının kullanıcı adı (zorunlu).
- **USER_FULL_NAME**: Kullanıcı için yeni tam ad (zorunlu).
  
### Seçenekler  
  
- `--is_superuser`, `-su`: Kullanıcıyı superuser olarak ayarlar, yükseltilmiş yetkiler verir. Bu bayrak bir değer gerektirmez.  
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir son geçerlilik tarihi ayarlar. Sağlanmazsa hesap süresiz geçerli kalır.  
  
### Örnek
  
`jdoe` kullanıcısının tam adını “Johnathan Doe” olarak değiştirmek ve kullanıcıyı superuser olarak ayarlamak için:
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
- **USER_PWD**: Kullanıcı için yeni parola (zorunlu).
  
### Örnek
  
`jdoe` kullanıcısının parolasını `newpassword123` olarak değiştirmek için:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## `list-users` Komutunun Kullanımı

`list-users` komutu, ***digna*** CLI içinde ***digna*** sistemine kayıtlı tüm kullanıcıların listesini gösterir.

### Komut Kullanımı

```bash
dignacli list-users
```

Bu komutu çalıştırmak, ***digna*** repository'sine bağlanacak ve tüm kullanıcıları ID, kullanıcı adı, tam ad, superuser durumu ve son geçerlilik zaman damgalarını göstererek listeleyecektir.

# Repository Yönetimi

### `upgrade-repo` Komutunun Kullanımı
  
`upgrade-repo` komutu, ***digna*** CLI içinde ***digna*** repository'sini yükseltmek veya başlatmak için kullanılır. Bu komut, güncellemeleri uygulamak veya repository altyapısını ilk kez kurmak için gereklidir.
  
### Komut Kullanımı

```bash
dignacli upgrade-repo [options]
```
  
### Seçenekler
  
- `--simulation-mode`, `-s`: Etkinleştirildiğinde, bu seçenek komutu simülasyon modunda çalıştırır; yürütülecek SQL ifadelerini yazdırır ancak bunları gerçekten çalıştırmaz. Bu, repository üzerinde herhangi bir değişiklik yapmadan değişiklikleri önizlemek için kullanışlıdır.  

  
### Örnek
  
***digna*** repository'sini yükseltmek için, komutu herhangi bir seçenek olmadan çalıştırabilirsiniz:
  
```bash
dignacli upgrade-repo
```  
Yükseltmeyi simülasyon modunda çalıştırmak (SQL ifadelerini görmek ama uygulamamak) için:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Bu komut, ***digna*** sisteminin bakımında kritik öneme sahiptir ve veritabanı şeması ile diğer repository bileşenlerinin yazılımın en son sürümüyle uyumlu olmasını sağlar.

## `encrypt` Komutunun Kullanımı
  
`encrypt` komutu, ***digna*** CLI içinde bir parolayı şifrelemek için kullanılır.
  
### Komut Kullanımı
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argümanlar
- **PASSWORD**: Şifrelenmesi gereken parola (zorunlu).
  
### Örnek
  
Bir parolayı şifrelemek için parola argümanı sağlanmalıdır.   
Örneğin, `mypassword123` parolasını şifrelemek için:
```bash
dignacli encrypt mypassword123
```
Bu komut, sağlanan parolanın şifrelenmiş halini çıktılar; bu çıktı daha sonra güvenli ortamlarda kullanılabilir. Parola argümanı sağlanmazsa, CLI eksik argüman olduğunu belirten bir hata gösterir.

## `generate-key` Komutunun Kullanımı
  
`generate-key` komutu, ***digna*** repository'sinde saklanan parolaları güvence altına almak için gerekli olan bir Fernet anahtarı üretmek için kullanılır.
  
### Komut Kullanımı
```bash
dignacli generate-key
```
  
# Veri Yönetimi

## `clean-up` Komutunun Kullanımı

`clean-up` komutu, ***digna*** CLI içinde belirli bir proje kapsamında bir veya daha fazla veri kaynağı için profilleri, tahminleri ve trafik ışığı sistemi verilerini kaldırmak için kullanılır. Bu komut, veri yaşam döngüsü yönetimi için önemlidir ve eski ya da gereksiz verileri temizleyerek düzenli ve verimli bir veri ortamı sağlanmasına yardımcı olur.

### Komut Kullanımı

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argümanlar
  
- **PROJECT_NAME**: Verilerin kaldırılacağı projenin adı (zorunlu). Bu argümana all-projects anahtar kelimesini kullanmak, ***digna***'nın mevcut tüm projeler üzerinde yineleme yapmasını ve bu komutu uygulamasını sağlar.
- **FROM_DATE**: Veri kaldırma işleminin başlayacağı tarih ve saat. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (zorunlu).
- **TO_DATE**: Veri kaldırma işleminin biteceği tarih ve saat; FROM_DATE ile aynı formatları takip eder (zorunlu).
  
### Seçenekler
  
- `--table-name`, `-tn`: Temizleme işlemini proje içindeki belirli bir tabloyla sınırlamak için kullanılır.
- `--table-filter`, `-tf`: İsimlerinde belirtilen alt dizeyi içeren tablolara temizleme işlemini sınırlamak için filtre uygular.
- `--timing`, `-tm`: Tamamlandıktan sonra temizleme sürecinin süre bilgisini gösterir.
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
  
Bu komut, veri depolamayı yönetmeye ve repository'de yalnızca ilgili bilgilerin bulunmasını sağlamaya yardımcı olur.

## `inspect` Komutunun Kullanımı

`inspect` komutu, ***digna*** CLI içinde belirli bir proje kapsamındaki bir veya daha fazla veri kaynağı için profiller, tahminler ve trafik ışığı sistemi verileri oluşturmak için kullanılır. Bu komut, belirtilen dönem boyunca verilerin analiz edilmesine ve izlenmesine yardımcı olur.

### Komut Kullanımı

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argümanlar
  
- **PROJECT_NAME**: İncelemenin yapılacağı projenin adı (zorunlu). Bu argümana all-projects anahtar kelimesi kullanıldığında, ***digna*** mevcut tüm projeler üzerinde yineleme yapar ve bu komutu uygular.
- **FROM_DATE**: Veri incelemesinin başlayacağı tarih ve saat. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (zorunlu).
- **TO_DATE**: Veri incelemesinin biteceği tarih ve saat; FROM_DATE ile aynı formatları takip eder (zorunlu).
  
### Seçenekler

- `--table-name`, `-tn`: İncelemeyi proje içindeki belirli bir tabloyla sınırlamak için kullanılır.
- `--table-filter`, `-tf`: İsimlerinde belirtilen alt dizeyi içeren tablolara inceleme uygulamak için filtre uygular.
- `--do-profile`: Profillerin yeniden toplanmasını tetikler. Varsayılan do-profile'dır.
- `--no-do-profile`: Profillerin yeniden toplanmasını engeller.
- `--do-prediction`: Tahminlerin yeniden hesaplanmasını tetikler. Varsayılan do-prediction'dır.
- `--no-do-prediction`: Tahminlerin yeniden hesaplanmasını engeller.
- `--do-alert-status`: Alarm durumlarının yeniden hesaplanmasını tetikler. Varsayılan do-alert-status'dur.
- `--no-do-alert-status`: Alarm durumlarının yeniden hesaplanmasını engeller.
- `--timing`, `-tm`: Tamamlandıktan sonra inceleme sürecinin süresini gösterir.
  
### Örnek
  
`ProjectA` projesindeki verileri 1 Ocak 2024 ile 31 Ocak 2024 arasında incelemek için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Sadece belirli bir tabloyu incelemek ve tahminlerin yeniden hesaplanmasını zorlamak için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Bu komut, güncellenmiş profiller ve tahminler oluşturmak, veri bütünlüğünü izlemek ve belirli bir proje zaman aralığındaki alarm sistemlerini yönetmek için kullanışlıdır.

## `tls-status` Komutunun Kullanımı

`tls-status` komutu, ***digna*** CLI içinde belirli bir proje ve tarihte bir tablo için Traffic Light System (TLS) durumunu sorgulamak için kullanılır. Trafik Işık Sistemi, verinin sağlığı ve kalitesi hakkında içgörüler sağlayarak dikkat edilmesi gereken sorunları veya uyarıları gösterir.
  
### Komut Kullanımı
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argümanlar
  
- **PROJECT_NAME**: TLS durumunun sorgulandığı proje adı (zorunlu).
- **TABLE_NAME**: Proje içindeki TLS durumu istenen tablo (zorunlu).
- **DATE**: TLS durumunun sorgulandığı tarih, genellikle %Y-%m-%d formatında (zorunlu).
  
### Örnek
  
1 Temmuz 2024 tarihinde ProjectA projesindeki UserData adlı tablonun TLS durumunu kontrol etmek için:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Bu komut, önceden tanımlanmış kriterlere dayalı olarak açık ve uygulanabilir bir durum raporu sağlayarak kullanıcıların veri kalitesini izlemesine ve sürdürmesine yardımcı olur.

## `list-projects` Komutunun Kullanımı
  
`list-projects` komutu, ***digna*** CLI içinde mevcut tüm projelerin bir listesini görüntülemek için kullanılır.
  
### Komut Kullanımı
  
```bash
dignacli list-projects
```

Bu komut, birden fazla proje yöneten yöneticiler ve kullanıcılar için özellikle yararlıdır; ***digna*** repository'sindeki mevcut projelerin hızlı bir genel görünümünü sağlar.

## `list-ds` Komutunun Kullanımı

`list-ds` komutu, ***digna*** CLI içinde belirli bir proje kapsamında mevcut tüm veri kaynaklarının bir listesini görüntülemek için kullanılır. Bu komut, analiz ve yönetim için kullanılabilir veri varlıklarını anlamada faydalıdır.

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
  
Bu komut, bir projedeki mevcut veri kaynaklarına genel bir bakış sunar ve kullanıcıların veri ortamını daha etkili yönetip gezinmesine yardımcı olur.