---
title: digna CLI Başvuru 2024.12 – Komutlar & Örnekler | digna Dokümantasyonu
description: digna CLI sürümü 2024.12 için eksiksiz başvuru. add-user, check-repo-connection, upgrade-repo, inspect ve daha fazlası gibi komutlarla kullanıcıları, depoları ve verileri nasıl yöneteceğinizi öğrenin.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202412/
image: /assets/logo_square.png
---


# digna CLI Başvuru 2024.12
**2024-12-09**

Bu sayfa, ***digna*** CLI sürümü **2024.12**'de kullanılabilen tüm komutları, kullanım örneklerini ve seçeneklerini belgelendirir.

---


**2024-12-09**


---

## CLI Temelleri

---

## `help` Seçeneğinin Kullanımı

`--help` seçeneği, mevcut komutlar ve bunların kullanımı hakkında bilgi sağlar. Bu seçeneği kullanmanın iki temel yolu vardır:

1. **Genel Yardımı Görüntüleme:**
   
    `dignacli` anahtar kelimesinden hemen sonra `--help` kullanın.  
   ```bash
   dignacli --help
   ```

2. **Belirli Komutlar İçin Yardım Alma:**  
  
    Belirli bir komut hakkında ayrıntılı bilgi almak için o komuta `--help` ekleyin.  
    Örneğin, `add-user` komutu için yardım almak amacıyla çalıştırın:
     ```bash
     dignacli add-user --help
     ```

     ### çıktı:
      
     - **Komut Açıklaması:** Komutun ne yaptığını ayrıntılı olarak açıklar.  
     - **Sözdizimi:** Gerekli ve isteğe bağlı argümanları içerecek şekilde tam sözdizimini gösterir.  
     - **Seçenekler:** Komuta özgü seçenekleri ve açıklamalarını listeler.  
     - **Örnekler:** Komutun etkin bir şekilde nasıl çalıştırılacağına dair örnekler sağlar.

  
## `check-repo-connection` Komutunun Kullanımı

`check-repo-connection` komutu, ***digna*** CLI aracında belirli bir ***digna*** repository ile bağlantı ve erişimi test etmek için kullanılan bir yardımcı araçtır. Bu komut, CLI'nin repository ile etkileşime girebildiğini doğrular.
      
### Komut Kullanımı
```bash
dignacli check-repo-connection
```

Başarılı çalıştırma durumunda komut, bağlantının doğrulandığını ve repository hakkında Repository version, Host, Database ve Schema bilgilerini çıktılar.  
  
Eğer repository bağlantısı başarılı değilse, doğru yapılandırma ayarları için config.toml dosyasını kontrol edin.

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

## Kayıt (logging) Seçeneklerinin Kullanımı
  
Varsayılan olarak, ***digna*** komutlarının konsol çıktısı minimalist olacak şekilde tasarlanmıştır. Çoğu komut, aşağıdaki seçenekleri kullanarak ek bilgiler sağlama olanağı sunar:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” ve “debug” ayrıntı düzeyini tanımlar, oysa “logfile” anahtarı çıktıyı konsol penceresi yerine bir dosyaya yönlendirmeye olanak tanır.

# Kullanıcı Yönetimi

## `add-user` Komutunun Kullanımı
  
`add-user` komutu, ***digna*** CLI içinde yeni bir kullanıcıyı ***digna*** sistemine eklemek için kullanılır.
  
### Komut Kullanımı
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argümanlar

- **USER_NAME**: Yeni kullanıcı için kullanıcı adı (gerekli).
- **USER_FULL_NAME**: Yeni kullanıcının tam adı (gerekli).
- **USER_PASSWORD**: Yeni kullanıcı için parola (gerekli).

### Seçenekler

- `--is_superuser`, `-su`: Yeni kullanıcıyı yönetici olarak atamak için bayrak.
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir sonlanma tarihi belirler. Ayarlanmazsa hesap için sonlanma tarihi yoktur.

### Örnek

Kullanıcı adı `jdoe`, tam adı `John Doe` ve parolası `password123` olan yeni bir kullanıcı eklemek için:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Hesap sonlanma tarihi belirleyerek yeni bir kullanıcı eklemek için:
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
- **USER_NAME**: Silinecek kullanıcının kullanıcı adı (gerekli). Bu komutun gerektirdiği tek argümandır.

### Örnek
```bash
dignacli delete-user jdoe
```
  
Bu komut çalıştırıldığında `jdoe` kullanıcısı ***digna*** sisteminden kaldırılır, erişimi iptal edilir ve repository'deki ilişkili verileri ve izinleri silinir.

## `modify-user` Komutunun Kullanımı

`modify-user` komutu, ***digna*** CLI içinde mevcut bir kullanıcının bilgilerini güncellemek için kullanılır.

### Komut Kullanımı
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argümanlar
  
- **USER_NAME**: Düzenlenecek kullanıcının kullanıcı adı (gerekli).
- **USER_FULL_NAME**: Kullanıcının yeni tam adı (gerekli).
  
### Seçenekler  
  
- `--is_superuser`, `-su`: Kullanıcıyı süper kullanıcı olarak ayarlar, yükseltilmiş ayrıcalıklar verir. Bu bayrak bir değer gerektirmez.  
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir sonlanma tarihi belirler. Verilmezse hesap süresiz geçerli kalır.  
  
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
  
- **USER_NAME**: Parolası değiştirilecek kullanıcının kullanıcı adı (gerekli).
- **USER_PWD**: Kullanıcının yeni parolası (gerekli).
  
### Örnek
  
`jdoe` kullanıcısının parolasını `newpassword123` olarak değiştirmek için:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## `list-users` Komutunun Kullanımı

`list-users` komutu, ***digna*** CLI içinde ***digna*** sistemine kayıtlı tüm kullanıcıları listelemek için kullanılır.

### Komut Kullanımı

```bash
dignacli list-users
```

Bu komutu çalıştırmak, ***digna*** repository'sine bağlanarak tüm kullanıcıları listeler; ID, kullanıcı adı, tam ad, süper kullanıcı durumu ve sonlanma zaman damgalarını gösterir.

# Repository Yönetimi

### `upgrade-repo` Komutunun Kullanımı
  
`upgrade-repo` komutu, ***digna*** CLI içinde ***digna*** repository'sini yükseltmek veya başlatmak için kullanılır. Bu komut, güncellemeleri uygulamak veya repository altyapısını ilk kez kurmak için gereklidir.
  
### Komut Kullanımı

```bash
dignacli upgrade-repo [options]
```
  
### Seçenekler
  
- `--simulation-mode`, `-s`: Etkinleştirildiğinde komut simülasyon modunda çalışır; çalıştırılacak SQL ifadelerini yazdırır ancak bunları gerçekten uygulamaz. Repository üzerinde değişiklik yapmadan değişiklikleri önizlemek için faydalıdır.  

  
### Örnek
  
***digna*** repository'sini yükseltmek için herhangi bir seçenek olmadan komutu çalıştırabilirsiniz:
  
```bash
dignacli upgrade-repo
```  
Yükseltmeyi simülasyon modunda çalıştırmak (SQL ifadelerini görmek ancak uygulamamak) için:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Bu komut, ***digna*** sisteminin bakımında kritik öneme sahiptir; veritabanı şemasının ve diğer repository bileşenlerinin yazılımın en son sürümüyle uyumlu olmasını sağlar.

## `encrypt` Komutunun Kullanımı
  
`encrypt` komutu, ***digna*** CLI içinde bir parolayı şifrelemek için kullanılır.
  
### Komut Kullanımı
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argümanlar
- **PASSWORD**: Şifrelenmesi gereken parola (gerekli).
  
### Örnek
  
Bir parolayı şifrelemek için parolayı argüman olarak vermeniz gerekir.   
Örneğin, `mypassword123` parolasını şifrelemek için:
```bash
dignacli encrypt mypassword123
```
Bu komut, verilen parolanın şifrelenmiş halini çıktı olarak verir; bu çıktı daha sonra güvenli bağlamlarda kullanılabilir. Parola argümanı verilmezse CLI eksik argüman olduğunu belirten bir hata gösterir.

## `generate-key` Komutunun Kullanımı
  
`generate-key` komutu, ***digna*** repository'sinde saklanan parolaları güvence altına almak için gerekli olan bir Fernet anahtarı üretmek için kullanılır.
  
### Komut Kullanımı
```bash
dignacli generate-key
```
  
# Veri Yönetimi

## `clean-up` Komutunun Kullanımı

`clean-up` komutu, ***digna*** CLI içinde belirli bir proje kapsamında bir veya birden fazla veri kaynağı için profilleri, tahminleri ve Trafik Işık Sistemi verilerini kaldırmak için kullanılır. Bu komut, veri yaşam döngüsü yönetimi için önemlidir ve eski veya gereksiz verileri temizleyerek düzenli ve verimli bir veri ortamı sürdürmeye yardımcı olur.

### Komut Kullanımı

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argümanlar
  
- **PROJECT_NAME**: Verilerin kaldırılacağı projenin adı (gerekli). Bu argümana all-projects anahtar kelimesi verilirse ***digna*** mevcut tüm projeler üzerinde yineleme yapar ve komutu uygular.
- **FROM_DATE**: Veri kaldırma için başlangıç tarih ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (gerekli).
- **TO_DATE**: Veri kaldırma için bitiş tarih ve saati, FROM_DATE ile aynı formatları takip eder (gerekli).
  
### Seçenekler
  
- `--table-name`, `-tn`: Temizleme işlemini proje içindeki belirli bir tabloyla sınırlamak için.
- `--table-filter`, `-tf`: Tablo adlarında belirtilen alt dizeyi içeren tablolarla sınırlamak için filtre uygular.
- `--timing`, `-tm`: Temizleme işleminin tamamlanmasının ardından geçen süreyi gösterir.
- `--help`: clean-up komutu için yardım bilgilerini gösterir ve çıkar.
  
### Örnek
  
ProjectA projesinden 1 Ocak 2023 ile 30 Haziran 2023 arasındaki verileri kaldırmak için:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Yalnızca `Table1` adlı belirli bir tablodan veri kaldırmak için:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Bu komut, veri depolamayı yönetmeye ve repository'nin yalnızca ilgili bilgileri içermesini sağlamaya yardımcı olur.

## `inspect` Komutunun Kullanımı

`inspect` komutu, ***digna*** CLI içinde belirli bir proje kapsamında bir veya birden fazla veri kaynağı için profiller, tahminler ve Trafik Işık Sistemi verileri oluşturmak için kullanılır. Bu komut, belirli bir süre boyunca veri analizine ve izlemeye yardımcı olur.

### Komut Kullanımı

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argümanlar
  
- **PROJECT_NAME**: İncelenecek verilerin ait olduğu projenin adı (gerekli). Bu argümana all-projects anahtar kelimesi verilirse ***digna*** mevcut tüm projeler üzerinde yineleme yapar ve komutu uygular.
- **FROM_DATE**: Veri incelemesi için başlangıç tarih ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (gerekli).
- **TO_DATE**: Veri incelemesi için bitiş tarih ve saati, FROM_DATE ile aynı formatları takip eder (gerekli).
  
### Seçenekler

- `--table-name`, `-tn`: İncelemeyi proje içindeki belirli bir tabloyla sınırlamak için.
- `--table-filter`, `-tf`: İsimlerinde belirtilen alt dizeyi içeren tabloları incelemek için filtre uygular.
- `--do-profile`: Profillerin yeniden toplanmasını tetikler. Varsayılan do-profile'dır.
- `--no-do-profile`: Profillerin yeniden toplanmasını engeller.
- `--do-prediction`: Tahminlerin yeniden hesaplanmasını tetikler. Varsayılan do-prediction'dır.
- `--no-do-prediction`: Tahminlerin yeniden hesaplanmasını engeller.
- `--do-alert-status`: Uyarı durumlarının yeniden hesaplanmasını tetikler. Varsayılan do-alert-status'tur.
- `--no-do-alert-status`: Uyarı durumlarının yeniden hesaplanmasını engeller.
- `--iterative`: Belirtilen dönemi günlük iterasyonlar kullanarak incelemeyi tetikler. Varsayılan iterative'dir.
- `--no-iterative`: Tüm dönemin tek seferde incelenmesini tetikler.
- `--timing`, `-tm`: İncelemenin tamamlanmasının ardından geçen süreyi gösterir.
  
### Örnek
  
`ProjectA` projesi için 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri incelemek için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Yalnızca belirli bir tabloyu incelemek ve tahminlerin yeniden hesaplanmasını zorlamak için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Bu komut, güncel profiller ve tahminler oluşturmak, veri bütünlüğünü izlemek ve belirtilen proje zaman aralığında uyarı sistemlerini yönetmek için faydalıdır.

## `tls-status` Komutunun Kullanımı

`tls-status` komutu, ***digna*** CLI içinde bir proje içindeki belirli bir tablonun belirli bir tarihte Trafik Işık Sistemi (TLS) durumunu sorgulamak için kullanılır. Trafik Işık Sistemi, verinin sağlığı ve kalitesi hakkında, dikkat edilmesi gereken sorun veya uyarıları gösteren bilgiler sağlar.
  
### Komut Kullanımı
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argümanlar
  
- **PROJECT_NAME**: TLS durumunun sorgulandığı projenin adı (gerekli).
- **TABLE_NAME**: TLS durumunun gerektiği proje içindeki belirli tablo (gerekli).
- **DATE**: TLS durumunun sorgulandığı tarih, genellikle %Y-%m-%d formatında (gerekli).
  
### Örnek
  
`ProjectA` projesinde `UserData` adlı tablonun 1 Temmuz 2024 tarihindeki TLS durumunu kontrol etmek için:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Bu komut, önceden tanımlanmış kriterlere göre açık ve uygulanabilir bir durum raporu sağlayarak kullanıcıların veri kalitesini izlemelerine ve sürdürmelerine yardımcı olur.

## `list-projects` Komutunun Kullanımı
  
`list-projects` komutu, ***digna*** CLI içinde mevcut tüm projelerin listesini göstermek için kullanılır.
  
### Komut Kullanımı
  
```bash
dignacli list-projects
```

Bu komut, birden çok proje yöneten yöneticiler ve kullanıcılar için özellikle yararlıdır; ***digna*** repository'sindeki mevcut projelere hızlı bir genel bakış sağlar.

## `list-ds` Komutunun Kullanımı

`list-ds` komutu, ***digna*** CLI içinde belirli bir proje kapsamındaki mevcut tüm veri kaynaklarını listelemek için kullanılır. Bu komut, analiz ve yönetim için kullanılabilecek veri varlıklarını anlamaya yardımcı olur.

### Komut Kullanımı
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının listelendiği projenin adı (gerekli).
  
### Örnek
  
`ProjectA` adlı projedeki tüm veri kaynaklarını listelemek için:
  
```bash
dignacli list-ds ProjectA
```
  
Bu komut, bir projedeki kullanılabilir veri kaynakları hakkında kullanıcıya genel bir bakış sağlayarak veri alanını daha etkili yönetmelerine yardımcı olur.