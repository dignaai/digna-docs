---
title: digna CLI Reference 2025.09 – Komutlar & Örnekler | digna Documentation
description: digna CLI sürümü 2025.109 için eksiksiz referans. add-user, check-config, check-repo-connection, inspect, inspect-async ve diğer komutlarla kullanıcıları, depoları ve verileri nasıl yöneteceğinizi öğrenin.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202509/
image: /assets/logo_square.png
---

# digna CLI Reference 2025.09
**2025-09-29**

Bu sayfa, ***digna*** CLI sürümü **2025.09** ile kullanılabilen tüm komutları, kullanım örneklerini ve seçeneklerini belgeler.

---

## CLI Temelleri

---

### help
`--help` seçeneği mevcut komutlar ve kullanım hakkında bilgi sağlar. Bu seçeneği kullanmanın iki ana yolu vardır:

1. **Genel Yardımı Görüntüleme:**
   
    `***digna***` kelimesinin hemen ardından `--help` kullanın  
   ```bash
   dignacli --help
   ```

2. **Belirli Komutlar İçin Yardım Alma:**  
  
    Belirli bir komut hakkında ayrıntılı bilgi almak için o komuta `--help` ekleyin.  
    Örneğin `add-user` komutu için yardım almak istiyorsanız şu komutu çalıştırın:
     ```bash
     dignacli add-user --help
     ```

     ### çıktı:
      
     - **Komut Açıklaması:** Komutun ne yaptığını detaylı şekilde açıklar.  
     - **Sözdizimi:** Gerekli ve isteğe bağlı argümanlar dahil tam sözdizimini gösterir.  
     - **Seçenekler:** Komuta özel seçenekleri ve açıklamalarını listeler.  
     - **Örnekler:** Komutun etkili şekilde nasıl çalıştırılacağını gösteren örnekler sağlar.

### check-config

check-config komutu, ***digna*** CLI aracında ***digna*** yapılandırmasını test etmek için kullanılan bir yardımcıdır. Bu komut, ***digna*** bileşenlerinin config.toml içinde gereken yapılandırma öğelerini bulabildiğinden emin olur.

#### Seçenekler

- `--configpath`, `-cp`: Yapılandırmayı içeren dosya veya dizin. Atlanırsa ../config.toml kullanılacaktır.
      
#### Komut Kullanımı
```bash
dignacli check-config
```

Başarılı çalıştırma durumunda, komut yapılandırmanın eksiksiz olduğunu doğrulayan bir çıktı verir.  
  
Yapılandırma eksik görünüyorsa, eksik yapılandırma öğeleri listelenecektir.

  
### check-repo-connection

check-repo-connection komutu, ***digna*** CLI aracında belirtilen bir ***digna*** deposuna bağlantı ve erişimi test etmek için kullanılan bir yardımcıdır. Bu komut, CLI'nın depo ile etkileşime girebildiğinden emin olur.
      
#### Komut Kullanımı
```bash
dignacli check-repo-connection
```

Başarılı çalıştırma durumunda, komut bağlantının doğrulandığını ve depo hakkında aşağıdaki bilgileri çıktılar: Repository version, Host, Database ve Schema.  
  
Depo bağlantısı başarılı değilse, doğru yapılandırma ayarlarının config.toml dosyasında bulunduğundan emin olun.


### version

Yüklü *dignacli* sürümünü kontrol etmek için `--version` seçeneğini kullanın.  
  
#### Komut Kullanımı
```bash
dignacli --version
```
  
#### Örnek Çıktı
```bash
dignacli version 2025.09
```

### günlükleme seçenekleri
  
Varsayılan olarak, ***digna*** komutlarının konsol çıktısı minimalist olacak şekilde tasarlanmıştır. Çoğu komut, aşağıdaki seçenekleri kullanarak ek bilgi sağlama olanağı sunar:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” ve “debug” detay seviyesini belirlerken, “logfile” anahtarı çıktının konsol yerine bir dosyaya akıtılmasını sağlar.

## Kullanıcı Yönetimi

### add-user
  
add-user komutu, ***digna*** CLI içinde ***digna*** sistemine yeni bir kullanıcı eklemek için kullanılır.
  
#### Komut Kullanımı
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argümanlar

- **USER_NAME**: Yeni kullanıcı için kullanıcı adı (gerekli).
- **USER_FULL_NAME**: Yeni kullanıcının tam adı (gerekli).
- **USER_PASSWORD**: Yeni kullanıcı için parola (gerekli).

#### Seçenekler

- `--is_superuser`, `-su`: Yeni kullanıcıyı yönetici (superuser) olarak atamak için bayrak.
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir sona erme tarihi belirler. Belirtilmezse hesapın sona erme tarihi yoktur.

#### Örnek

Kullanıcı adı `jdoe`, tam adı `John Doe` ve parolası `password123` olan yeni bir kullanıcı eklemek için:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Bir kullanıcı ekleyip hesap sona erme tarihi belirlemek için:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
`delete-user` komutu, ***digna*** CLI içinde mevcut bir kullanıcıyı ***digna*** sisteminden kaldırmak için kullanılır.
  
#### Komut Kullanımı
```bash
dignacli delete-user USER_NAME
```
  
#### Argümanlar
- **USER_NAME**: Silinecek kullanıcının kullanıcı adı (gerekli). Bu, komutun gerektirdiği tek argümandır.

#### Örnek
```bash
dignacli delete-user jdoe
```
  
Bu komut çalıştırıldığında, `jdoe` kullanıcısı ***digna*** sisteminden kaldırılır; erişimi iptal edilir ve depo içindeki ilişkili veri ve izinleri silinir.

### modify-user

`modify-user` komutu, ***digna*** CLI içinde mevcut bir kullanıcının bilgilerini güncellemek için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argümanlar
  
- **USER_NAME**: Güncellenecek kullanıcının kullanıcı adı (gerekli).
- **USER_FULL_NAME**: Kullanıcının yeni tam adı (gerekli).
  
#### Seçenekler  
  
- `--is_superuser`, `-su`: Kullanıcıyı superuser olarak ayarlar, yükseltilmiş ayrıcalık verir. Bu bayrak bir değer gerektirmez.  
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir sona erme tarihi belirler. Sağlanmazsa hesap süresiz geçerli kalır.  
  
#### Örnek
  
`jdoe` kullanıcısının tam adını “Johnathan Doe” olarak değiştirmek ve kullanıcıyı superuser yapmak için:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
`modify-user-pwd` komutu, ***digna*** CLI içinde mevcut bir kullanıcının parolasını değiştirmek için kullanılır.
  
#### Komut Kullanımı
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argümanlar
  
- **USER_NAME**: Parolası değiştirilecek kullanıcının kullanıcı adı (gerekli).
- **USER_PWD**: Kullanıcının yeni parolası (gerekli).
  
#### Örnek
  
`jdoe` kullanıcısının parolasını `newpassword123` olarak değiştirmek için:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

`list-users` komutu, ***digna*** CLI içinde sisteme kayıtlı tüm kullanıcıların listesini görüntüler.

#### Komut Kullanımı

```bash
dignacli list-users
```

Bu komut çalıştırıldığında ***digna*** deposuna bağlanır ve tüm kullanıcıları ID, kullanıcı adı, tam adı, superuser durumu ve sona erme zaman damgaları ile birlikte listeler.

## Depo Yönetimi

### upgrade-repo
  
`upgrade-repo` komutu, ***digna*** CLI içinde ***digna*** deposunu yükseltmek veya başlatmak için kullanılır. Bu komut, güncellemeleri uygulamak veya depo altyapısını ilk kez kurmak için gereklidir.
  
#### Komut Kullanımı

```bash
dignacli upgrade-repo [options]
```
  
#### Seçenekler
  
- `--simulation-mode`, `-s`: Etkinleştirildiğinde komut simülasyon modunda çalıştırılır; yürütülecek SQL ifadelerini yazdırır, ancak bunları gerçekten çalıştırmaz. Bu, değişiklikleri uygulamadan önizlemek için faydalıdır.  

  
#### Örnek
  
***digna*** deposunu yükseltmek için seçeneksiz çalıştırabilirsiniz:
  
```bash
dignacli upgrade-repo
```  
Yükseltmeyi simülasyon modunda çalıştırmak (SQL ifadelerini görüp uygulamamak) için:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Bu komut, ***digna*** sisteminin bakımında kritik öneme sahiptir ve veri tabanı şeması ile diğer depo bileşenlerinin yazılımın en son sürümüyle uyumlu olmasını sağlar.

### encrypt
  
`encrypt` komutu, ***digna*** CLI içinde bir parolayı şifrelemek için kullanılır.
  
#### Komut Kullanımı
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argümanlar
- **PASSWORD**: Şifrelenmesi gereken parola (gerekli).
  
#### Örnek
  
Bir parolayı şifrelemek için parolayı argüman olarak sağlamanız gerekir.   
Örneğin, `mypassword123` parolasını şifrelemek için:
```bash
dignacli encrypt mypassword123
```
Bu komut, sağlanan parolanın şifrelenmiş halini çıktılar; bu sonuç daha güvenli bağlamlarda kullanılabilir. Parola argümanı sağlanmazsa CLI eksik argümanı belirten bir hata gösterir.

### generate-key
  
`generate-key` komutu, Fernet anahtarı üretmek için kullanılır; bu anahtar ***digna*** deposunda saklanan parolaların güvenliği için gereklidir.
  
#### Komut Kullanımı
```bash
dignacli generate-key
```
  
## Veri Yönetimi

### clean-up

`clean-up` komutu, ***digna*** CLI içinde belirtilen proje kapsamındaki bir veya birden fazla veri kaynağı için profilleri, tahminleri ve trafik ışığı sistemi verilerini kaldırmak için kullanılır. Bu komut, veri yaşam döngüsü yönetimi için önemlidir; eski veya gereksiz verileri temizleyerek düzenli ve verimli bir veri ortamı sağlar.

#### Komut Kullanımı

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: Verilerin kaldırılacağı projenin adı (gerekli). Bu argümana all-projects anahtar kelimesi verildiğinde ***digna*** mevcut tüm projeler üzerinde yineleme yapar ve komutu uygular.
- **FROM_DATE**: Veri kaldırma işleminin başlangıç tarih ve zamanı. Kabul edilebilir formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (gerekli).
- **TO_DATE**: Veri kaldırma işleminin bitiş tarih ve zamanı, FROM_DATE ile aynı formatları kullanır (gerekli).
  
#### Seçenekler
  
- `--table-name`, `-tn`: Temizleme işlemini proje içindeki belirli bir tabloyla sınırlar.
- `--table-filter`, `-tf`: İsimlerinde belirtilen alt dizeyi içeren tablolara göre filtre uygular.
- `--timing`, `-tm`: Temizleme işlemi tamamlandıktan sonra süre bilgisini gösterir.
- `--help`: clean-up komutu için yardım bilgisi gösterir ve çıkar.
  
#### Örnek
  
ProjectA projesinden 1 Ocak 2023 ile 30 Haziran 2023 arasındaki verileri kaldırmak için:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Sadece `Table1` adlı belirli bir tablodan veri kaldırmak için:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Bu komut, veri depolamayı yönetmeye ve deponun yalnızca ilgili bilgileri içermesini sağlamaya yardımcı olur.

### remove-orphans
  
`remove-orphans` komutu, ***digna*** CLI içinde depo için bakım amaçlı kullanılır.  
Bir kullanıcı projeleri veya veri kaynaklarını sildiğinde, profiller ve tahminler depoda kalmaya devam edebilir. Bu komutla, bu tür yetim (orphan) satırlar depodan kaldırılır.
  
#### Komut Kullanımı
  
```bash
dignacli list-projects
```

### list-projects
  
`list-projects` komutu, ***digna*** CLI içinde mevcut tüm projelerin listesini görüntülemek için kullanılır.
  
#### Komut Kullanımı
  
```bash
dignacli list-projects
```

Bu komut, çoklu projeyi yöneten yöneticiler ve kullanıcılar için özellikle faydalıdır; ***digna*** deposunda mevcut projelerin hızlı bir özetini sağlar.

### list-ds

`list-ds` komutu, belirtilen bir proje içindeki mevcut tüm veri kaynaklarını listelemek için ***digna*** CLI içinde kullanılır. Bu komut, analiz ve yönetim için mevcut veri varlıklarını anlamaya yardımcı olur.

#### Komut Kullanımı
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının listelendiği projenin adı (gerekli).
  
#### Örnek
  
`ProjectA` adlı projedeki tüm veri kaynaklarını listelemek için:
  
```bash
dignacli list-ds ProjectA
```
  
Bu komut, bir projede mevcut veri kaynaklarına genel bir bakış sağlayarak veriyi daha etkili yönetme ve gezinme imkanı sunar.


### inspect

`inspect` komutu, ***digna*** CLI içinde belirtilen proje kapsamındaki bir veya birden fazla veri kaynağı için profiller, tahminler ve trafik ışığı sistemi verileri oluşturmak için kullanılır. Bu komut, tanımlanan bir dönem boyunca verileri analiz etmeye ve izlemeye yardımcı olur. Denetleme tamamlandığında hesaplanan trafik ışığı sistemi değeri döndürülür:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Komut Kullanımı

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: Denetlenecek verilerin ait olduğu projenin adı (gerekli). Bu argümana all-projects anahtar kelimesi verildiğinde ***digna*** mevcut tüm projeler üzerinde yineleme yapar ve komutu uygular.
- **FROM_DATE**: Veri denetiminin başlangıç tarih ve zamanı. Kabul edilebilir formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (gerekli).
- **TO_DATE**: Veri denetiminin bitiş tarih ve zamanı, FROM_DATE ile aynı formatları kullanır (gerekli).
  
#### Seçenekler

- `--table-name`, `-tn`: Denetimi proje içindeki belirli bir tabloyla sınırlar.
- `--table-filter`, `-tf`: İsimlerinde belirtilen alt dizeyi içeren tablolarda denetim uygular.
- `--enable_notification`, `-en`: Uyarı durumunda bildirim gönderimini etkinleştirir.
- `--bypass-backend`, `-bb`: Backend'i devre dışı bırakarak denetimi doğrudan CLI'dan çalıştırır (sadece test amaçlı!).

  
#### Örnek
  
`ProjectA` projesindeki 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri denetlemek için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Sadece belirli bir tabloyu denetlemek ve tahminlerin yeniden hesaplanmasını zorlamak için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Bu komut, güncellenmiş profiller ve tahminler oluşturmak, veri bütünlüğünü izlemek ve belirlenen proje zaman aralığı içinde uyarı sistemlerini yönetmek için faydalıdır.

### inspect-async

`inspect-async` komutu, ***digna*** CLI içinde belirtilen proje kapsamındaki bir veya birden fazla veri kaynağı için profiller, tahminler ve trafik ışığı sistemi verileri oluşturmak için kullanılır. Bu komut, tanımlanan bir dönem boyunca verileri analiz etmeye ve izlemeye yardımcı olur. `inspect-async` komutunun aksine, bu komut denetlemenin tamamlanmasını beklemez.  
Bunun yerine gönderilen denetim isteği için bir request id döndürür. Denetim sürecinin ilerlemesini sorgulamak için `inspect-status` komutunu kullanın.

#### Komut Kullanımı

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: Denetlenecek verilerin ait olduğu projenin adı (gerekli). Bu argümana all-projects anahtar kelimesi verildiğinde ***digna*** mevcut tüm projeler üzerinde yineleme yapar ve komutu uygular.
- **FROM_DATE**: Veri denetiminin başlangıç tarih ve zamanı. Kabul edilebilir formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (gerekli).
- **TO_DATE**: Veri denetiminin bitiş tarih ve zamanı, FROM_DATE ile aynı formatları kullanır (gerekli).
  
#### Seçenekler

- `--table-name`, `-tn`: Denetimi proje içindeki belirli bir tabloyla sınırlar.
- `--table-filter`, `-tf`: İsimlerinde belirtilen alt dizeyi içeren tablolarda denetim uygular.
- `--enable_notification`, `-en`: Uyarı durumunda bildirim gönderimini etkinleştirir.

  
#### Örnek
  
`ProjectA` projesindeki 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri asenkron olarak denetlemek için:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

`inspect-status` komutu, ***digna*** CLI içinde asenkron bir denetimin ilerlemesini request ID bazında kontrol etmek için kullanılır.

#### Komut Kullanımı

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argümanlar
  
- **REQUEST_ID**: `inspect-async` komutu tarafından döndürülen request id
  
#### Örnek
  
Request ID'si 12345 olan bir denetimin ilerlemesini kontrol etmek için:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

`inspect-cancel` komutu, ***digna*** CLI içinde request ID bazında denetimleri iptal etmek veya tüm mevcut istekleri iptal etmek için kullanılır.

#### Komut Kullanımı

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argümanlar
  
- **REQUEST_ID**: `inspect-async` komutu tarafından döndürülen request id 
  
#### Örnek
  
Request ID'si 12345 olan denetimi iptal etmek için:
  
```bash
dignacli inspect-cancel 12345
```

Şu anda çalışmakta veya beklemede olan tüm istekleri iptal etmek için:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

`export-ds` komutu, ***digna*** CLI içinde veri kaynaklarının bir dışa aktarımını oluşturmak için kullanılır. Varsayılan olarak, verilen bir projedeki tüm veri kaynakları dışa aktarılır.

#### Komut Kullanımı
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının dışa aktarılacağı projenin adı.

#### Seçenekler

- `--table_name`, `-tn`: Bir projeden belirli bir veri kaynağını dışa aktarır.
- `--exportfile`, `-ef`: Dışa aktarım için dosya adını belirtir.
    
#### Örnek
  
`ProjectA` projesindeki tüm veri kaynaklarını dışa aktarmak için:
  
```bash
dignacli export-ds ProjectA
```
  
Bu komut `ProjectA` içindeki tüm veri kaynaklarını başka bir projeye veya ***digna*** deposuna aktarılabilecek bir JSON belgesi olarak dışa aktarır.


### import-ds

`import-ds` komutu, ***digna*** CLI içinde veri kaynaklarını hedef bir projeye aktarmak ve bir import raporu oluşturmak için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının içe aktarılacağı projenin adı.
- **EXPORT_FILE**: İçe aktarılacak veri kaynakları dışa aktarım dosyasının adı.

#### Seçenekler

- `--output-file`, `-o`: İçe aktarma raporunun kaydedileceği dosya (belirtilmezse terminalde tablo halinde yazdırılır).
- `--output-format`, `-f`: İçe aktarma raporunun kaydedileceği format (json, csv).
    
#### Örnek
  
`my_export.json` dışa aktarım dosyasındaki tüm veri kaynaklarını `ProjectB`'ye aktarmak için:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
İçe aktarma sonrası, bu komut ayrıca içe aktarılan ve atlanan nesnelerin bir raporunu gösterir. Sadece yeni veri kaynakları `ProjectB`'ye aktarılacaktır. Hangi nesnelerin aktarılacağını ve hangilerinin atlanacağını öğrenmek için `plan-import-ds` komutunu kullanabilirsiniz.

### plan-import-ds

`plan-import-ds` komutu, ***digna*** CLI içinde bir dışa aktarım dosyasının hedef projeye alınması durumunda hangi veri kaynaklarının aktarılacağını ve hangilerinin atlanacağını analiz eden bir plan oluşturmak için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının içe aktarılacağı proje adı (analiz edilmek istenen hedef).
- **EXPORT_FILE**: İçe aktarma öncesinde analiz edilecek dışa aktarım dosyasının adı.

#### Seçenekler

- `--output-file`, `-o`: İçe aktarma plan raporunun kaydedileceği dosya (belirtilmezse terminalde tablo halinde yazdırılır).
- `--output-format`, `-f`: İçe aktarma plan raporunun kaydedileceği format (json, csv).
    
#### Örnek
  
`my_export.json` dışa aktarım dosyasındaki hangi veri kaynaklarının `ProjectB`'ye aktarılacağını ve hangilerinin atlanacağını kontrol etmek için:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Bu komut yalnızca aktarılacak ve atlanacak nesnelerin bir içe aktarma planını gösterir.