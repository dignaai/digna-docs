---
title: digna CLI Referansı 2024.12 – Komutlar & Örnekler | digna Dokümantasyonu
description: digna CLI sürümü 2024.12 için tam referans. add-user, check-repo-connection, upgrade-repo, inspect ve diğer komutlarla kullanıcıları, depoları ve verileri nasıl yöneteceğinizi öğrenin.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202412/
image: /assets/logo_square.png
---


# digna CLI Referansı 2024.12
**2024-12-09**

Bu sayfa, ***digna*** CLI sürümü **2024.12**'de kullanılabilen tüm komutları, kullanım örnekleri ve seçenekleriyle birlikte belgelemektedir.

---


**2024-12-09**


---

## CLI Temelleri

---

## `help` Seçeneğinin Kullanımı

`--help` seçeneği, kullanılabilir komutlar ve bunların kullanımına ilişkin bilgi sağlar. Bu seçeneğin iki ana kullanım şekli vardır:

1. **Genel Yardımı Görüntüleme:**
   
    `--help` seçeneğini ***digna*** komutundan hemen sonra kullanın.  
   ```bash
   dignacli --help
   ```

2. **Belirli Komut İçin Yardım Alma:**  
  
    Belirli bir komut hakkında detaylı bilgi almak için o komuta `--help` ekleyin.  
    Örneğin `add-user` komutu için yardım almak isterseniz:
     ```bash
     dignacli add-user --help
     ```

     ### çıktı:
      
     - **Komut Açıklaması:** Komutun ne yaptığını ayrıntılı şekilde açıklar.  
     - **Sözdizimi:** Gerekli ve isteğe bağlı argümanlar dahil olmak üzere kesin sözdizimini gösterir.  
     - **Seçenekler:** Komuta özgü seçenekleri ve açıklamalarını listeler.  
     - **Örnekler:** Komutun etkili şekilde nasıl çalıştırılacağını gösteren örnekler sunar.

  
## `check-repo-connection` Komutunun Kullanımı

check-repo-connection komutu, ***digna*** CLI aracında belirtilen bir ***digna*** deposuna bağlantı ve erişimi test etmek için kullanılan bir yardımcıdır. Bu komut, CLI'nin depoyla etkileşime geçip geçemediğini doğrular.
      
### Komut Kullanımı
```bash
dignacli check-repo-connection
```

Başarılı çalıştırma durumunda komut bağlantı onayını ve depo hakkında aşağıdaki bilgileri çıktılar: Depo sürümü, Host, Veritabanı ve Şema.  
  
Eğer depo bağlantısı başarılı değilse, doğru yapılandırma ayarları için config.toml dosyasını kontrol edin.

## `version` Komutunun Kullanımı

Yüklü *dignacli* sürümünü kontrol etmek için `--version` seçeneğini kullanın.  
  
### Komut Kullanımı
```bash
dignacli --version
```
  
### Örnek Çıktı
```bash
dignacli version 2024.12
```

## Günlükleme (logging) Seçeneklerinin Kullanımı
  
Varsayılan olarak, ***digna*** komutlarının konsol çıktısı minimal düzeyde olacak şekilde tasarlanmıştır. Çoğu komut ek bilgi sağlamayı mümkün kılar; bunun için aşağıdaki seçenekler kullanılır:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
“verbose” ve “debug” detay seviyesini belirlerken, “logfile” anahtarı çıktının konsol yerine bir dosyaya yönlendirilmesine olanak tanır.

# Kullanıcı Yönetimi

## `add-user` Komutunun Kullanımı
  
add-user komutu, ***digna*** CLI'de sisteme yeni bir kullanıcı eklemek için kullanılır.
  
### Komut Kullanımı
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argümanlar

- **USER_NAME**: Yeni kullanıcı için kullanıcı adı (gereklidir).
- **USER_FULL_NAME**: Yeni kullanıcının tam adı (gereklidir).
- **USER_PASSWORD**: Yeni kullanıcı için parola (gereklidir).

### Seçenekler

- `--is_superuser`, `-su`: Yeni kullanıcıyı yönetici olarak atamak için bayrak.
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir son geçerlilik tarihi belirler. Belirtilmezse hesapın son kullanma tarihi olmaz.

### Örnek

Kullanıcı adı `jdoe`, tam adı `John Doe` ve parolası `password123` olan yeni bir kullanıcı eklemek için:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Hesap son geçerlilik tarihini de ayarlamak için:
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
- **USER_NAME**: Silinecek kullanıcının kullanıcı adı (gereklidir). Bu komutun gerektirdiği tek argümandır.

### Örnek
```bash
dignacli delete-user jdoe
```
  
Bu komut çalıştırıldığında `jdoe` kullanıcısı ***digna*** sisteminden kaldırılacak; erişimi iptal edilecek ve depo içindeki ilişkili verileri ile izinleri silinecektir.

## `modify-user` Komutunun Kullanımı

`modify-user` komutu, ***digna*** CLI'de mevcut bir kullanıcının bilgilerini güncellemek için kullanılır.

### Komut Kullanımı
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argümanlar
  
- **USER_NAME**: Değiştirilecek kullanıcının kullanıcı adı (gereklidir).
- **USER_FULL_NAME**: Kullanıcının yeni tam adı (gereklidir).
  
### Seçenekler  
  
- `--is_superuser`, `-su`: Kullanıcıyı yetkili kullanıcı (superuser) olarak belirler; bu bayrak bir değer gerektirmez.  
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir son geçerlilik tarihi belirler. Sağlanmazsa hesap süresiz olarak geçerli kalır.  
  
### Örnek
  
`jdoe` kullanıcısının tam adını “Johnathan Doe” olarak değiştirmek ve kullanıcıyı superuser yapmak için:
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
  
- **USER_NAME**: Parolası değiştirilecek kullanıcının kullanıcı adı (gereklidir).
- **USER_PWD**: Kullanıcının yeni parolası (gereklidir).
  
### Örnek
  
`jdoe` kullanıcısının parolasını `newpassword123` olarak değiştirmek için:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## `list-users` Komutunun Kullanımı

`list-users` komutu, ***digna*** CLI'de kayıtlı tüm kullanıcıları listelemek için kullanılır.

### Komut Kullanımı

```bash
dignacli list-users
```

Bu komutu çalıştırdığınızda ***digna*** deposuna bağlanılır ve kullanıcıların ID, kullanıcı adı, tam adı, superuser durumu ve son geçerlilik zaman damgalarını gösteren bir liste sunulur.

# Depo (Repository) Yönetimi

### `upgrade-repo` Komutunun Kullanımı
  
`upgrade-repo` komutu, ***digna*** CLI'de ***digna*** deposunu yükseltmek veya başlatmak için kullanılır. Bu komut, güncellemeleri uygulamak veya depo altyapısını ilk kez kurmak için gereklidir.
  
### Komut Kullanımı

```bash
dignacli upgrade-repo [options]
```
  
### Seçenekler
  
- `--simulation-mode`, `-s`: Etkinleştirildiğinde komut simülasyon modunda çalışır; yürütülecek SQL ifadelerini yazdırır ancak gerçek uygulama yapmaz. Değişiklikleri uygulamadan önce önizleme yapmak için faydalıdır.  

  
### Örnek
  
***digna*** deposunu yükseltmek için herhangi bir seçenek olmadan komutu çalıştırabilirsiniz:
  
```bash
dignacli upgrade-repo
```  
Yükseltmeyi simülasyon modunda çalıştırmak (SQL ifadelerini görmek ancak uygulamamak) için:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Bu komut, veritabanı şeması ve diğer depo bileşenlerinin yazılımın en son sürümüyle uyumlu olmasını sağlayarak ***digna*** sisteminin bakımında kritik öneme sahiptir.

## `encrypt` Komutunun Kullanımı
  
`encrypt` komutu, ***digna*** CLI'de bir parolayı şifrelemek için kullanılır.
  
### Komut Kullanımı
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argümanlar
- **PASSWORD**: Şifrelenmesi gereken parola (gereklidir).
  
### Örnek
  
Bir parolayı şifrelemek için parolayı argüman olarak vermeniz gerekir.  
Örneğin `mypassword123` parolasını şifrelemek için:
```bash
dignacli encrypt mypassword123
```
Bu komut, verilen parolanın şifrelenmiş halini çıktılar; daha sonra güvenli bağlamlarda kullanılabilir. Parola argümanı sağlanmazsa CLI eksik argüman olduğunu belirten bir hata gösterir.

## `generate-key` Komutunun Kullanımı
  
`generate-key` komutu, ***digna*** deposunda saklanan parolaları güvence altına almak için gerekli olan bir Fernet anahtarı oluşturmak için kullanılır.
  
### Komut Kullanımı
```bash
dignacli generate-key
```
  
# Veri Yönetimi

## `clean-up` Komutunun Kullanımı

`clean-up` komutu, ***digna*** CLI'de bir veya daha fazla veri kaynağı için bir projede profil, tahmin (prediction) ve Trafik Işık Sistemi (Traffic Light System) verilerini temizlemek için kullanılır. Bu komut, veri yaşam döngüsü yönetimi için önemlidir ve eski veya gereksiz verileri temizleyerek düzenli ve verimli bir veri ortamı sağlamaya yardımcı olur.

### Komut Kullanımı

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argümanlar
  
- **PROJECT_NAME**: Verilerin silineceği projenin adı (gereklidir). Bu argümana all-projects anahtar kelimesi verildiğinde ***digna*** tüm mevcut projelerde yineleme yaparak bu komutu uygular.
- **FROM_DATE**: Veri temizliği için başlangıç tarih ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (gereklidir).
- **TO_DATE**: Veri temizliği için bitiş tarih ve saati, FROM_DATE ile aynı formatları takip eder (gereklidir).
  
### Seçenekler
  
- `--table-name`, `-tn`: Temizleme işlemini proje içindeki belirli bir tablo ile sınırlar.
- `--table-filter`, `-tf`: Tablo adlarında belirtilen alt dizeyi içeren tablolara temizlemeyi sınırlar.
- `--timing`, `-tm`: Temizleme işlemi tamamlandıktan sonra süre bilgisini gösterir.
- `--help`: clean-up komutu için yardım bilgisini gösterir ve çıkar.
  
### Örnek
  
ProjectA projesinden 1 Ocak 2023 ile 30 Haziran 2023 arasındaki verileri silmek için:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Sadece `Table1` adlı belirli bir tablodan veri silmek için:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Bu komut, veri depolamayı yönetmeye ve deponun yalnızca ilgili bilgileri içermesini sağlamaya yardımcı olur.

## `inspect` Komutunun Kullanımı

`inspect` komutu, ***digna*** CLI'de bir veya daha fazla veri kaynağı için bir projede profil, tahminler ve Trafik Işık Sistemi verilerini oluşturmak için kullanılır. Bu komut, belirli bir dönem içinde veriyi analiz etmeye ve izlemeye yardımcı olur.

### Komut Kullanımı

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argümanlar
  
- **PROJECT_NAME**: İncelenecek verilerin ait olduğu proje adı (gereklidir). Bu argümana all-projects anahtar kelimesi verildiğinde ***digna*** tüm mevcut projelerde yineleme yaparak bu komutu uygular.
- **FROM_DATE**: Veri incelemesi için başlangıç tarih ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (gereklidir).
- **TO_DATE**: Veri incelemesi için bitiş tarih ve saati, FROM_DATE ile aynı formatları takip eder (gereklidir).
  
### Seçenekler

- `--table-name`, `-tn`: İncelemeyi proje içindeki belirli bir tablo ile sınırlar.
- `--table-filter`, `-tf`: Adlarında belirtilen alt dizeyi içeren tablolara incelemeyi sınırlar.
- `--do-profile`: Profillerin yeniden toplanmasını tetikler. Varsayılan do-profile'dır.
- `--no-do-profile`: Profillerin yeniden toplanmasını engeller.
- `--do-prediction`: Tahminlerin yeniden hesaplanmasını tetikler. Varsayılan do-prediction'dır.
- `--no-do-prediction`: Tahminlerin yeniden hesaplanmasını engeller.
- `--do-alert-status`: Uyarı durumlarının yeniden hesaplanmasını tetikler. Varsayılan do-alert-status'tur.
- `--no-do-alert-status`: Uyarı durumlarının yeniden hesaplanmasını engeller.
- `--iterative`: Belirtilen dönemin günlük yinelemelerle incelenmesini tetikler. Varsayılan iterative'dir.
- `--no-iterative`: Belirtilen dönemin tek seferde incelenmesini sağlar.
- `--timing`, `-tm`: İnceleme işlemi tamamlandıktan sonra sürenin gösterilmesini sağlar.
  
### Örnek
  
ProjectA projesi için 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri incelemek için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Sadece belirli bir tabloyu incelemek ve tahminlerin yeniden hesaplanmasını zorlamak için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Bu komut, güncellenmiş profiller ve tahminler oluşturmak, veri bütünlüğünü izlemek ve belirli bir proje zaman aralığı içinde uyarı sistemlerini yönetmek için faydalıdır.

## `tls-status` Komutunun Kullanımı

`tls-status` komutu, ***digna*** CLI'de belirli bir proje içindeki bir tablonun belirli bir tarihteki Trafik Işık Sistemi (TLS) durumunu sorgulamak için kullanılır. Trafik Işık Sistemi, verinin sağlık ve kalite durumu hakkında içgörü sağlar ve dikkat gerektiren sorunlar veya uyarılar hakkında bilgi verir.
  
### Komut Kullanımı
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argümanlar
  
- **PROJECT_NAME**: TLS durumunun sorgulandığı proje adı (gereklidir).
- **TABLE_NAME**: TLS durumunun gerektiği belirli tablo (gereklidir).
- **DATE**: TLS durumunun sorgulandığı tarih, genellikle %Y-%m-%d formatındadır (gereklidir).
  
### Örnek
  
ProjectA projesinde UserData adlı tablonun 1 Temmuz 2024 tarihindeki TLS durumunu kontrol etmek için:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Bu komut, önceden tanımlanmış kriterlere dayalı olarak açık ve uygulanabilir bir durum raporu sağlayarak kullanıcıların veri kalitesini izlemesine ve sürdürmesine yardımcı olur.

## `list-projects` Komutunun Kullanımı
  
`list-projects` komutu, ***digna*** CLI'de sistemde mevcut tüm projelerin listesini görüntülemek için kullanılır.
  
### Komut Kullanımı
  
```bash
dignacli list-projects
```

Bu komut, birden fazla projeyi yöneten yöneticiler ve kullanıcılar için özellikle faydalıdır; ***digna*** deposundaki mevcut projelerin hızlı bir özetini sunar.

## `list-ds` Komutunun Kullanımı

`list-ds` komutu, ***digna*** CLI'de belirli bir proje içindeki tüm veri kaynaklarını listelemek için kullanılır. Bu komut, analiz ve yönetim için mevcut veri varlıklarını anlamaya yardımcı olur.

### Komut Kullanımı
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının listelendiği proje adı (gereklidir).
  
### Örnek
  
ProjectA adlı projedeki tüm veri kaynaklarını listelemek için:
  
```bash
dignacli list-ds ProjectA
```
  
Bu komut, bir projenin sahip olduğu veri kaynaklarına genel bir bakış sağlayarak veri ortamını daha etkili yönetmelerine yardımcı olur.