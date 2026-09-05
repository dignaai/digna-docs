# digna CLI Reference 2026.04
**2026-04-08**

Bu sayfa, ***digna*** CLI sürümü **2026.04**'te kullanılabilir tüm komutları, kullanım örneklerini ve seçeneklerini belgelendirir.

---

## CLI Temelleri

---

### help
`--help` seçeneği, kullanılabilir komutlar ve bunların kullanımı hakkında bilgi sağlar. Bu seçeneği kullanmanın iki temel yolu vardır:

1. **Genel Yardımı Görüntüleme:**
   
    `--help` seçeneğini `dignacli` anahtar kelimesinden hemen sonra kullanın.  
   ```bash
   dignacli --help
   ```

2. **Belirli Komutlar İçin Yardım Alma:**  
  
    Belirli bir komut hakkında ayrıntılı bilgi almak için o komuta `--help` ekleyin.  
    Örneğin, `add-user` komutu hakkında yardım almak için şu komutu çalıştırın:
     ```bash
     dignacli add-user --help
     ```

     ### çıktı:
      
     - **Komut Açıklaması:** Komutun ne yaptığını ayrıntılı olarak açıklar.  
     - **Söz Dizimi:** Gerekli ve isteğe bağlı argümanlar dahil olmak üzere tam söz dizimini gösterir.  
     - **Seçenekler:** Komuta özgü seçenekleri ve açıklamalarını listeler.  
     - **Örnekler:** Komutun etkin bir şekilde nasıl çalıştırılacağını gösteren örnekler sağlar.

### check-config

`check-config` komutu, ***digna*** CLI aracının içinde bulunan ve ***digna*** yapılandırmasını test etmek için tasarlanmış bir yardımcı programdır. Bu komut, ***digna*** bileşenlerinin config.toml içindeki gerekli yapılandırma öğelerini bulabildiğini doğrular.

#### Seçenekler

- `--configpath`, `-cp`: Yapılandırmayı içeren dosya veya dizin. Atlanırsa ../config.toml kullanılacaktır.
      
#### Komut Kullanımı
```bash
dignacli check-config
```

Başarılı yürütme sonucunda komut, yapılandırmanın tamamlandığına dair bir onay çıktısı üretir.  
  
Eğer yapılandırma eksik görünüyorsa, eksik yapılandırma öğeleri listelenecektir.

  
### check-repo-connection

`check-repo-connection` komutu, ***digna*** CLI aracında belirtilen bir ***digna*** deposuna bağlantıyı ve erişimi test etmek için kullanılan bir yardımcı programdır. Bu komut, CLI'nın depoyla etkileşime girebildiğini doğrular.
      
#### Komut Kullanımı
```bash
dignacli check-repo-connection
```

Başarılı yürütme sonucunda komut, depoya başarılı bağlantıya ilişkin bir onay ile birlikte depo hakkında şu bilgileri çıktı olarak verir: Repository version, Host, Database ve Schema.  
  
Eğer depo bağlantısı başarılı değilse, doğru yapılandırma ayarları için config.toml dosyasını kontrol edin.


### version

Yüklü *dignacli* sürümünü kontrol etmek için `--version` seçeneğini kullanın.  
  
#### Komut Kullanımı
```bash
dignacli --version
```
  
#### Örnek Çıktı
```bash
dignacli version 2026.04
```

### günlükleme seçenekleri
  
Varsayılan olarak, ***digna*** komutlarının konsol çıktısı minimaldir. Çoğu komut, aşağıdaki seçenekleri kullanarak ek bilgi sağlama olanağı sunar:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” ve “debug” detay seviyesini tanımlarken, “logfile” anahtarı çıktının konsol penceresi yerine bir dosyaya yönlendirilmesine olanak tanır.

## Kullanıcı Yönetimi

### add-user
  
`add-user` komutu, ***digna*** CLI içinde yeni bir kullanıcı eklemek için kullanılır.
  
#### Komut Kullanımı
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argümanlar

- **USER_NAME**: Yeni kullanıcı için kullanıcı adı (gerekli).
- **USER_FULL_NAME**: Yeni kullanıcının tam adı (gerekli).
- **USER_PASSWORD**: Yeni kullanıcı için parola (gerekli).

#### Seçenekler

- `--is_superuser`, `-su`: Yeni kullanıcıyı yönetici (superuser) olarak belirler.
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir son kullanma tarihi belirler. Belirtilmezse hesapın bir son kullanma tarihi yoktur.

#### Örnek

Kullanıcı adı `jdoe`, tam adı `John Doe` ve parolası `password123` olan yeni bir kullanıcı eklemek için:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Bir kullanıcı ekleyip hesap son kullanma tarihi ayarlamak için:
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
- **USER_NAME**: Silinecek kullanıcının kullanıcı adı (gerekli). Bu, komut tarafından gerekli olan tek argümandır.

#### Örnek
```bash
dignacli delete-user jdoe
```
  
Bu komut `jdoe` kullanıcısını ***digna*** sisteminden kaldıracak, erişimini iptal edecek ve depodaki ilişkili verilerini ve izinlerini silecektir.

### modify-user

`modify-user` komutu, ***digna*** CLI içinde mevcut bir kullanıcının bilgilerini güncellemek için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argümanlar
  
- **USER_NAME**: Güncellenecek kullanıcının kullanıcı adı (gerekli).
- **USER_FULL_NAME**: Kullanıcı için yeni tam ad (gerekli).
  
#### Seçenekler  
  
- `--is_superuser`, `-su`: Kullanıcıyı superuser olarak ayarlar, yükseltilmiş ayrıcalıklar verir. Bu bayrak bir değer gerektirmez.  
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir son kullanma tarihi belirler. Sağlanmazsa hesap süresiz olarak geçerli kalır.  
  
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
- **USER_PWD**: Kullanıcı için yeni parola (gerekli).
  
#### Örnek
  
`jdoe` kullanıcısının parolasını `newpassword123` yapmak için:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

`list-users` komutu, ***digna*** CLI içinde ***digna*** sistemine kayıtlı tüm kullanıcıların listesini görüntüler.

#### Komut Kullanımı

```bash
dignacli list-users
```

Bu komutu çalıştırmak, ***digna*** deposuna bağlanır ve tüm kullanıcıları listeleyerek ID, kullanıcı adı, tam ad, superuser durumu ve son kullanma zaman damgalarını gösterir.

## Depo Yönetimi

### upgrade-repo
  
`upgrade-repo` komutu, ***digna*** CLI içinde ***digna*** deposunu yükseltmek veya başlatmak için kullanılır. Bu komut, güncellemeleri uygulamak veya depoyu ilk kez kurmak için gereklidir.
  
#### Komut Kullanımı

```bash
dignacli upgrade-repo [options]
```
  
#### Seçenekler
  
- `--simulation-mode`, `-s`: Etkinleştirildiğinde, komutu simülasyon modunda çalıştırır; çalıştırılacak SQL ifadelerini yazdırır ancak bunları gerçekten yürütmez. Bu, değişiklikleri uygulamadan önce önizleme yapmak için kullanışlıdır.  

  
#### Örnek
  
***digna*** deposunu yükseltmek için herhangi bir seçenek olmadan komutu çalıştırabilirsiniz:
  
```bash
dignacli upgrade-repo
```  
Yükseltmeyi simülasyon modunda çalıştırmak (SQL ifadelerini uygulamadan görmek) için:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Bu komut, ***digna*** sisteminin bakımında kritik öneme sahiptir ve veritabanı şemasının ve diğer depo bileşenlerinin yazılımın en son sürümüyle uyumlu olmasını sağlar.

### encrypt
  
`encrypt` komutu, ***digna*** CLI içinde bir parolayı şifrelemek için kullanılır.
  
#### Komut Kullanımı
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argümanlar
- **PASSWORD**: Şifrelenmesi gereken parola (gerekli).
  
#### Örnek
  
Bir parolayı şifrelemek için parola argümanını sağlamanız gerekir.  
Örneğin, `mypassword123` parolasını şifrelemek için:
```bash
dignacli encrypt mypassword123
```
Bu komut, verilen parolanın şifrelenmiş halini çıktılayacak ve daha sonra güvenli bağlamlarda kullanılabilir. Eğer parola argümanı sağlanmazsa, CLI eksik argümanı belirten bir hata gösterir.

### generate-key
  
`generate-key` komutu, ***digna*** deposunda saklanan parolaları güvence altına almak için gerekli olan bir Fernet anahtarı oluşturmak için kullanılır.
  
#### Komut Kullanımı
```bash
dignacli generate-key
```
  
## Veri Yönetimi

### clean-up

`clean-up` komutu, ***digna*** CLI içinde belirli bir proje kapsamında bir veya daha fazla veri kaynağı için profilleri, tahminleri ve trafik ışığı sistemi verilerini kaldırmak için kullanılır. Bu komut, veri yaşam döngüsü yönetimi için önemlidir ve güncel olmayan veya gereksiz verileri temizleyerek düzenli ve verimli bir veri ortamının korunmasına yardımcı olur.

#### Komut Kullanımı

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: Verinin kaldırılacağı projenin adı (gerekli). Bu argümanda all-projects anahtar kelimesini kullanmak, ***digna***'nın mevcut tüm projeler üzerinde yineleme yapmasını ve bu komutu uygulamasını sağlar.
- **FROM_DATE**: Veri kaldırma işlemi için başlangıç tarih ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (gerekli).
- **TO_DATE**: Veri kaldırma işlemi için bitiş tarih ve saati; FROM_DATE ile aynı formatları takip eder (gerekli).
  
#### Seçenekler
  
- `--table-name`, `-tn`: Temizleme işlemini projedeki belirli bir tabloyla sınırlar.
- `--table-filter`, `-tf`: Tablo adlarında belirtilen alt dizeyi içeren tablolarla sınırlamak için filtre uygular.
- `--timing`, `-tm`: İşlem tamamlandıktan sonra temizleme süresini görüntüler.
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
  
`remove-orphans` komutu, ***digna*** deposunda bakım/temizlik için kullanılır.  
Bir kullanıcı projeleri veya veri kaynaklarını sildiğinde, profiller ve tahminler depoda kalır. Bu komut ile bu tür yetim (orphan) satırlar depodan kaldırılacaktır.
  
#### Komut Kullanımı
  
```bash
dignacli list-projects
```

### list-projects
  
`list-projects` komutu, ***digna*** CLI içinde mevcut tüm projelerin bir listesini görüntülemek için kullanılır.
  
#### Komut Kullanımı
  
```bash
dignacli list-projects
```

Bu komut, birden çok projeyi yöneten yönetici ve kullanıcılar için özellikle yararlıdır; ***digna*** deposunda mevcut projelerin hızlı bir özetini sağlar.

### list-ds

`list-ds` komutu, ***digna*** CLI içinde belirtilen bir projedeki mevcut tüm veri kaynaklarının listesini görüntülemek için kullanılır. Bu komut, analiz ve yönetim için mevcut veri varlıklarını anlamada faydalıdır.

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
  
Bu komut, bir projede kullanılabilir veri kaynaklarının genel bir görünümünü sağlayarak veri ortamını daha etkili yönetmeye yardımcı olur.


### inspect

`inspect` komutu, ***digna*** CLI içinde belirli bir proje kapsamında bir veya daha fazla veri kaynağı için profiller, tahminler ve trafik ışığı sistemi verileri oluşturmak için kullanılır. Bu komut, tanımlı bir dönem boyunca verileri analiz etmeye ve izlemeye yardımcı olur. Denetim tamamlandıktan sonra hesaplanan trafik ışığı sisteminin değeri döndürülür:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Komut Kullanımı

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: İncelenecek verinin ait olduğu proje adı (gerekli). Bu argümanda all-projects anahtar kelimesini kullanmak, ***digna***'nın mevcut tüm projeler üzerinde yineleme yapmasını ve bu komutu uygulamasını sağlar.
- **FROM_DATE**: Veri incelemesi için başlangıç tarih ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (gerekli).
- **TO_DATE**: Veri incelemesi için bitiş tarih ve saati; FROM_DATE ile aynı formatları takip eder (gerekli).
  
#### Seçenekler

- `--table-name`, `-tn`: İncelemeyi projedeki belirli bir tabloyla sınırlar.
- `--table-filter`, `-tf`: Adında belirtilen alt dizeyi içeren tabloları incelemek için filtre uygular.
- `--enable_notification`, `-en`: Uyarı durumlarında bildirim gönderimini etkinleştirir.
- `--bypass-backend`, `-bb`: Backend'i atlayıp incelemeyi doğrudan CLI'dan çalıştırır (sadece test amaçlı!).

  
#### Örnek
  
`ProjectA` projesi için 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri incelemek için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Sadece belirli bir tabloyu incelemek ve tahminlerin yeniden hesaplanmasını zorlamak için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Bu komut, güncellenmiş profiller ve tahminler oluşturmak, veri bütünlüğünü izlemek ve belirlenen proje zaman aralığında uyarı sistemlerini yönetmek için kullanışlıdır.

### inspect-async

`inspect-async` komutu, ***digna*** CLI içinde belirli bir proje kapsamında bir veya daha fazla veri kaynağı için profiller, tahminler ve trafik ışığı sistemi verileri oluşturmak için kullanılır. Bu komut, tanımlı bir dönem boyunca verileri analiz etmeye ve izlemeye yardımcı olur. In contrast to the `inspect-async` command, this does not wait for the completion of the inspection. Bunun yerine, gönderilen inceleme isteği için bir istek kimliği döndürür. İnceleme sürecinin ilerlemesini sorgulamak için `inspect-status` komutunu kullanın.

#### Komut Kullanımı

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: İncelenecek verinin ait olduğu proje adı (gerekli). Bu argümanda all-projects anahtar kelimesini kullanmak, ***digna***'nın mevcut tüm projeler üzerinde yineleme yapmasını ve bu komutu uygulamasını sağlar.
- **FROM_DATE**: Veri incelemesi için başlangıç tarih ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (gerekli).
- **TO_DATE**: Veri incelemesi için bitiş tarih ve saati; FROM_DATE ile aynı formatları takip eder (gerekli).
  
#### Seçenekler

- `--table-name`, `-tn`: İncelemeyi projedeki belirli bir tabloyla sınırlar.
- `--table-filter`, `-tf`: Adında belirtilen alt dizeyi içeren tabloları incelemek için filtre uygular.
- `--enable_notification`, `-en`: Uyarı durumlarında bildirim gönderimini etkinleştirir.

  
#### Örnek
  
`ProjectA` projesi için 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri asenkron şekilde incelemek için:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  

### inspect-status

`inspect-status` komutu, asenkron bir incelemenin ilerlemesini istek kimliğine göre kontrol etmek için kullanılır.

#### Komut Kullanımı

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argümanlar
  
- **REQUEST_ID**: `inspect-async` komutu tarafından döndürülen istek kimliği
  
#### Örnek
  
İstek kimliği 12345 olan bir incelemenin ilerlemesini kontrol etmek için:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

`inspect-cancel` komutu, istek kimliğine göre incelemeleri iptal etmek için veya tüm mevcut istekleri iptal etmek için kullanılabilir.

#### Komut Kullanımı

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argümanlar
  
- **REQUEST_ID**: `inspect-async` komutu tarafından döndürülen istek kimliği 
  
#### Örnek
  
İstek kimliği 12345 olan incelemeyi iptal etmek için:
  
```bash
dignacli inspect-cancel 12345
```

Şu anda çalışan veya beklemede olan tüm istekleri iptal etmek için:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

`export-ds` komutu, ***digna*** CLI içinde ***digna*** deposundan veri kaynaklarının bir dışa aktarımını oluşturmak için kullanılır. Varsayılan olarak, belirli bir projedeki tüm veri kaynakları dışa aktarılır.

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
  
`ProjectA` adlı projeden tüm veri kaynaklarını dışa aktarmak için:
  
```bash
dignacli export-ds ProjectA
```
  
Bu komut, `ProjectA`'daki tüm veri kaynaklarını başka bir projeye veya ***digna*** deposuna içe aktarılabilecek bir JSON belgesi olarak dışa aktarır.


### import-ds

`import-ds` komutu, ***digna*** CLI içinde veri kaynaklarını hedef bir projeye içe aktarmak ve bir içe aktarma raporu oluşturmak için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının içe aktarılacağı projenin adı.
- **EXPORT_FILE**: İçe aktarılacak veri kaynakları dışa aktarım dosyasının dosya adı.

#### Seçenekler

- `--output-file`, `-o`: İçe aktarma raporunun kaydedileceği dosya (belirtilmezse tablo halinde terminale yazdırılır).
- `--output-format`, `-f`: İçe aktarma raporunun kaydedileceği format (json, csv).
    
#### Örnek
  
`my_export.json` dışa aktarma dosyasındaki tüm veri kaynaklarını `ProjectB`'ye içe aktarmak için:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
İçe aktarma sonrası bu komut, içe aktarılan ve atlanan nesnelerin bir raporunu da gösterecektir. Sadece yeni veri kaynakları `ProjectB`'ye içe aktarılacaktır. Hangi nesnelerin içe aktarılacağını ve hangilerinin atlanacağını öğrenmek için `plan-import-ds` komutunu kullanabilirsiniz.

### plan-import-ds

`plan-import-ds` komutu, ***digna*** CLI içinde veri kaynaklarını hedef bir projeye içe aktarmadan önce analiz etmek ve bir içe aktarma planı raporu oluşturmak için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının içe aktarılacağı proje adı (inceleme yapılacak hedef).
- **EXPORT_FILE**: İçe aktarılmadan önce analiz edilecek dışa aktarım dosyasının dosya adı.

#### Seçenekler

- `--output-file`, `-o`: İçe aktarma plan raporunun kaydedileceği dosya (belirtilmezse tablo halinde terminale yazdırılır).
- `--output-format`, `-f`: İçe aktarma plan raporunun kaydedileceği format (json, csv).
    
#### Örnek
  
`my_export.json` dışa aktarma dosyasından `ProjectB`'ye içe aktarılırken hangi veri kaynaklarının içe alınacağını ve hangilerinin atlanacağını kontrol etmek için:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Bu komut yalnızca içe alınacak ve atlanacak nesnelerin bir içe aktarma planını gösterir.