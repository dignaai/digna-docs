# digna CLI Reference 2025.09
**2025-09-29**

Bu sayfa, ***digna*** CLI sürümü **2025.09** için kullanılabilir tüm komutları, kullanım örneklerini ve seçenekleri belgelemektedir.

---

## CLI Temelleri

---

### help
`--help` seçeneği, kullanılabilir komutlar ve bunların kullanımı hakkında bilgi sağlar. Bu seçeneği kullanmanın iki ana yolu vardır:

1. **Genel Yardımı Görüntüleme:**
   
    `--help` seçeneğini ***digna*** kelimesini takip edecek şekilde kullanın.  
   ```bash
   dignacli --help
   ```

2. **Belirli Komutlar İçin Yardım Alma:**  
  
    Belirli bir komut hakkında ayrıntılı bilgi almak için o komuta `--help` ekleyin.  
    Örneğin, `add-user` komutu ile ilgili yardımı almak için çalıştırın:
     ```bash
     dignacli add-user --help
     ```

     ### çıktı:
      
     - **Komut Açıklaması:** Komutun ne yaptığını ayrıntılı olarak açıklar.  
     - **Sözdizimi:** Gerekli ve isteğe bağlı argümanlar dahil olmak üzere tam sözdizimini gösterir.  
     - **Seçenekler:** Komuta özgü seçenekleri ve açıklamalarını listeler.  
     - **Örnekler:** Komutun etkili bir şekilde nasıl çalıştırılacağına dair örnekler sağlar.

### check-config

check-config komutu, ***digna*** bileşenlerinin config.toml içinde gerekli yapılandırma öğelerini bulup bulamadığını test etmek için tasarlanmış bir yardımcı programdır.

#### Seçenekler

- `--configpath`, `-cp`: Yapılandırmayı içeren dosya veya dizin. İhmal edilirse ../config.toml kullanılacaktır.
      
#### Komut Kullanımı
```bash
dignacli check-config
```

Başarılı yürütme durumunda, komut yapılandırmanın eksiksiz olduğuna dair bir onay çıktısı verir.  
  
Eğer yapılandırma eksik görünüyorsa, eksik yapılandırma öğeleri listelenecektir.

  
### check-repo-connection

check-repo-connection komutu, belirtilen bir ***digna*** deposuna bağlantı ve erişimi test etmek için tasarlanmış bir yardımcı programdır. Bu komut, CLI'nin depoyla etkileşim kurabildiğini doğrular.
      
#### Komut Kullanımı
```bash
dignacli check-repo-connection
```

Başarılı yürütme durumunda, komut bağlantının doğrulandığına dair bir onay ve depoya ait ayrıntıları çıktı olarak verir: Repository version, Host, Database ve Schema.  
  
Eğer depo bağlantısı başarısız olursa, doğru yapılandırma ayarları için config.toml dosyasını kontrol edin.


### version

Yüklü *dignacli* sürümünü kontrol etmek için --version seçeneğini kullanın.  
  
#### Komut Kullanımı
```bash
dignacli --version
```
  
#### Örnek Çıktı
```bash
dignacli version 2025.09
```

### logging options
  
Varsayılan olarak, ***digna*** komutlarının konsol çıktısı minimalist olacak şekilde tasarlanmıştır. Çoğu komut, aşağıdaki seçenekleri kullanarak ek bilgi sağlama olanağı sunar:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” ve “debug” ayrıntı düzeyini tanımlarken, “logfile” seçeneği çıktının konsol yerine bir dosyaya yönlendirilmesini sağlar.

## Kullanıcı Yönetimi

### add-user
  
add-user komutu, ***digna*** CLI içinde yeni bir kullanıcı eklemek için kullanılır.
  
#### Komut Kullanımı
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argümanlar

- **USER_NAME**: Yeni kullanıcı için kullanıcı adı (zorunlu).
- **USER_FULL_NAME**: Yeni kullanıcının tam adı (zorunlu).
- **USER_PASSWORD**: Yeni kullanıcı için parola (zorunlu).

#### Seçenekler

- `--is_superuser`, `-su`: Yeni kullanıcıyı yönetici olarak atamak için bayrak.
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir geçerlilik sonu tarihi belirler. Ayarlanmazsa, hesabın bir sona erme tarihi olmaz.

#### Örnek

Kullanıcı adı `jdoe`, tam adı `John Doe` ve parolası `password123` olan yeni bir kullanıcı eklemek için:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Bir kullanıcı ekleyip hesap sonlandırma tarihi ayarlamak için:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
`delete-user` komutu, ***digna*** CLI içinde mevcut bir kullanıcıyı sistemden silmek için kullanılır.
  
#### Komut Kullanımı
```bash
dignacli delete-user USER_NAME
```
  
#### Argümanlar
- **USER_NAME**: Silinecek kullanıcının kullanıcı adı (zorunlu). Bu, komut tarafından gereken tek argümandır.

#### Örnek
```bash
dignacli delete-user jdoe
```
  
Bu komut `jdoe` kullanıcısını ***digna*** sisteminden kaldıracak, erişimini iptal edecek ve depodaki ilgili veri ve izinlerini silecektir.

### modify-user

`modify-user` komutu, ***digna*** CLI içinde mevcut bir kullanıcının bilgilerini güncellemek için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argümanlar
  
- **USER_NAME**: Güncellenecek kullanıcının kullanıcı adı (zorunlu).
- **USER_FULL_NAME**: Kullanıcı için yeni tam ad (zorunlu).
  
#### Seçenekler  
  
- `--is_superuser`, `-su`: Kullanıcıyı süper kullanıcı olarak ayarlar, yükseltilmiş ayrıcalıklar verir. Bu bayrak bir değer gerektirmez.  
- `--valid_until`, `-vu`: Kullanıcı hesabı için YYYY-MM-DD HH:MI:SS formatında bir son geçerlilik tarihi ayarlar. Sağlanmazsa, hesap süresiz geçerli kalır.  
  
#### Örnek
  
`jdoe` kullanıcısının tam adını “Johnathan Doe” olarak değiştirmek ve kullanıcıyı süper kullanıcı yapmak için:
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
  
- **USER_NAME**: Parolası değiştirilecek kullanıcının kullanıcı adı (zorunlu).
- **USER_PWD**: Kullanıcı için yeni parola (zorunlu).
  
#### Örnek
  
`jdoe` kullanıcısının parolasını `newpassword123` olarak değiştirmek için:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

`list-users` komutu, ***digna*** CLI içinde sisteme kayıtlı tüm kullanıcıların bir listesini gösterir.

#### Komut Kullanımı

```bash
dignacli list-users
```

Bu komutu çalıştırmak, ***digna*** deposuna bağlanarak tüm kullanıcıları ID, kullanıcı adı, tam ad, süper kullanıcı durumu ve sona erme zaman damgalarını göstererek listeleyecektir.

## Depo Yönetimi

### upgrade-repo
  
`upgrade-repo` komutu, ***digna*** deposunu yükseltmek veya başlatmak için kullanılan bir komuttur. Bu komut, güncellemeleri uygulamak veya depo altyapısını ilk kez kurmak için gereklidir.
  
#### Komut Kullanımı

```bash
dignacli upgrade-repo [options]
```
  
#### Seçenekler
  
- `--simulation-mode`, `-s`: Etkinleştirildiğinde, komut simülasyon modunda çalışır; yürütülecek SQL ifadelerini yazdırır ancak bunları gerçek olarak yürütmez. Bu, değişiklikleri uygulamadan önizlemek için kullanışlıdır.  

  
#### Örnek
  
***digna*** deposunu yükseltmek için herhangi bir seçenek olmadan komutu çalıştırabilirsiniz:
  
```bash
dignacli upgrade-repo
```  
Yükseltmeyi simülasyon modunda çalıştırmak (SQL ifadelerini görmek ama uygulamamak) için:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Bu komut, veri tabanı şeması ve diğer depo bileşenlerinin yazılımın en son sürümüyle uyumlu olmasını sağlayarak ***digna*** sisteminin bakımında kritik öneme sahiptir.

### encrypt
  
`encrypt` komutu, ***digna*** CLI içinde bir parolayı şifrelemek için kullanılır.
  
#### Komut Kullanımı
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argümanlar
- **PASSWORD**: Şifrelenmesi gereken parola (zorunlu).
  
#### Örnek
  
Bir parolayı şifrelemek için parola argümanı verilmelidir.   
Örneğin, `mypassword123` parolasını şifrelemek için:
```bash
dignacli encrypt mypassword123
```
Bu komut, verilen parolanın şifrelenmiş halini çıktı olarak verir; bu çıktı daha sonra güvenli bağlamlarda kullanılabilir. Parola argümanı sağlanmazsa, CLI eksik argüman olduğunu belirten bir hata gösterir.

### generate-key
  
`generate-key` komutu, ***digna*** deposunda saklanan parolaları korumak için gerekli olan bir Fernet anahtarı üretmek için kullanılır.
  
#### Komut Kullanımı
```bash
dignacli generate-key
```
  
## Veri Yönetimi

### clean-up

`clean-up` komutu, belirtilen bir proje içindeki bir veya daha fazla veri kaynağı için profil, tahmin ve trafik ışığı sistemi verilerini kaldırmak için kullanılır. Bu komut, veri yaşam döngüsü yönetimi için önemlidir ve eski veya gereksiz verilerin temizlenmesine yardımcı olur.

#### Komut Kullanımı

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: Verilerin kaldırılacağı projenin adı (zorunlu). Bu argümanda all-projects anahtar kelimesi kullanılırsa, ***digna*** mevcut tüm projeleri yineleyerek bu komutu uygular.
- **FROM_DATE**: Verilerin kaldırılmasına başlanacak tarih ve saat. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (zorunlu).
- **TO_DATE**: Verilerin kaldırılmasının sona ereceği tarih ve saat; FROM_DATE ile aynı formatları kabul eder (zorunlu).
  
#### Seçenekler
  
- `--table-name`, `-tn`: Temizleme işlemini projedeki belirli bir tabloyla sınırlamak için.
- `--table-filter`, `-tf`: Adında belirtilen alt dizgiyi içeren tablolarla sınırlamak için filtre.
- `--timing`, `-tm`: Temizleme işleminden sonra işlem süresini gösterir.
- `--help`: clean-up komutu için yardım bilgilerini görüntüler ve çıkar.
  
#### Örnek
  
ProjectA projesinden 1 Ocak 2023 ile 30 Haziran 2023 arasındaki verileri kaldırmak için:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Sadece `Table1` adlı belirli bir tablodan veri kaldırmak için:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Bu komut, veri depolamayı yönetmeye ve depoda yalnızca ilgili bilgilerin kalmasını sağlamaya yardımcı olur.

### remove-orphans
  
`remove-orphans` komutu, ***digna*** deposunda temizlik (house-keeping) işlemleri için kullanılır.  
Bir kullanıcı projeleri veya veri kaynaklarını sildiğinde, profiller ve tahminler depoda kalabilir. Bu komut ile bu tür yetim (orphan) satırlar depodan kaldırılacaktır.
  
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

Bu komut, özellikle birden çok projeyi yöneten yöneticiler ve kullanıcılar için yararlıdır; ***digna*** deposundaki mevcut projelerin hızlı bir genel görünümünü sağlar.

### list-ds

`list-ds` komutu, belirtilen bir proje içindeki mevcut tüm veri kaynaklarının bir listesini görüntülemek için kullanılır. Bu komut, analiz ve yönetim için kullanılabilecek veri varlıklarını anlamakta faydalıdır.

#### Komut Kullanımı
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının listelendiği projenin adı (zorunlu).
  
#### Örnek
  
`ProjectA` adlı projedeki tüm veri kaynaklarını listelemek için:
  
```bash
dignacli list-ds ProjectA
```
  
Bu komut, bir projede mevcut veri kaynaklarının genel bir görünümünü sağlayarak verilerle daha etkili gezinme ve yönetim imkanı sunar.


### inspect

`inspect` komutu, belirtilen bir proje içindeki bir veya daha fazla veri kaynağı için profil, tahmin ve trafik ışığı sistemi verileri oluşturmak için kullanılır. Bu komut, belirli bir dönem boyunca verileri analiz etmeye ve izlemeye yardımcı olur. İnceleme tamamlandığında hesaplanan trafik ışığı sisteminin değeri döndürülür:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Komut Kullanımı

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: İncelenecek verilerin ait olduğu projenin adı (zorunlu). Bu argümanda all-projects anahtar kelimesi kullanılırsa, ***digna*** mevcut tüm projeleri yineleyerek bu komutu uygular.
- **FROM_DATE**: Veri incelemesine başlanacak tarih ve saat. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (zorunlu).
- **TO_DATE**: Veri incelemesinin sona ereceği tarih ve saat; FROM_DATE ile aynı formatları kabul eder (zorunlu).
  
#### Seçenekler

- `--table-name`, `-tn`: İncelemeyi projedeki belirli bir tabloyla sınırlamak için.
- `--table-filter`, `-tf`: Adında belirtilen alt dizgiyi içeren tabloları incelemek için filtre.
- `--enable_notification`, `-en`: Uyarı durumunda bildirim gönderimini etkinleştirir.
- `--bypass-backend`, `-bb`: Backend'i atlayıp incelemeyi doğrudan CLI'den çalıştırır (sadece test amaçlı!).

  
#### Örnek
  
`ProjectA` projesi için 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri incelemek için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Sadece belirli bir tabloyu incelemek ve tahminlerin yeniden hesaplanmasını zorlamak için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Bu komut, güncellenmiş profiller ve tahminler oluşturmak, veri bütünlüğünü izlemek ve belirtilen proje zaman dilimi içinde uyarı sistemlerini yönetmek için faydalıdır.

### inspect-async

`inspect-async` komutu, belirtilen bir proje içindeki bir veya daha fazla veri kaynağı için profil, tahmin ve trafik ışığı sistemi verileri oluşturmak için kullanılır. Bu komut, belirli bir dönem boyunca verileri analiz etmeye ve izlemeye yardımcı olur. `inspect-async` komutunun aksine, bu komut incelemenin tamamlanmasını beklemez. Bunun yerine gönderilen inceleme isteği için bir istek kimliği (request id) döner. İnceleme sürecinin ilerlemesini sorgulamak için `inspect-status` komutunu kullanın.

#### Komut Kullanımı

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: İncelenecek verilerin ait olduğu projenin adı (zorunlu). Bu argümanda all-projects anahtar kelimesi kullanılırsa, ***digna*** mevcut tüm projeleri yineleyerek bu komutu uygular.
- **FROM_DATE**: Veri incelemesine başlanacak tarih ve saat. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (zorunlu).
- **TO_DATE**: Veri incelemesinin sona ereceği tarih ve saat; FROM_DATE ile aynı formatları kabul eder (zorunlu).
  
#### Seçenekler

- `--table-name`, `-tn`: İncelemeyi projedeki belirli bir tabloyla sınırlamak için.
- `--table-filter`, `-tf`: Adında belirtilen alt dizgiyi içeren tabloları incelemek için filtre.
- `--enable_notification`, `-en`: Uyarı durumunda bildirim gönderimini etkinleştirir.

  
#### Örnek
  
`ProjectA` projesi için 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri asenkron olarak incelemek için:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

`inspect-status` komutu, asenkron bir incelemenin ilerlemesini istek kimliğine (request ID) göre kontrol etmek için kullanılır.

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

`inspect-cancel` komutu, istek kimliğine göre incelemeleri iptal etmek veya mevcut tüm istekleri iptal etmek için kullanılır.

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

`export-ds` komutu, ***digna*** deposundan veri kaynaklarının bir dışa aktarmasını oluşturmak için kullanılır. Varsayılan olarak, belirtilen bir projedeki tüm veri kaynakları dışa aktarılır.

#### Komut Kullanımı
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının dışa aktarılacağı projenin adı.

#### Seçenekler

- `--table_name`, `-tn`: Bir projeden belirli bir veri kaynağını dışa aktarmak için.
- `--exportfile`, `-ef`: Dışa aktarma için dosya adını belirtir.
    
#### Örnek
  
`ProjectA` adlı projeden tüm veri kaynaklarını dışa aktarmak için:
  
```bash
dignacli export-ds ProjectA
```
  
Bu komut, `ProjectA` içindeki tüm veri kaynaklarını başka bir projeye veya ***digna*** deposuna aktarılabilecek bir JSON dokümanı olarak dışa aktarır.


### import-ds

`import-ds` komutu, veri kaynaklarını hedef bir projeye içe aktarmak ve bir içe aktarma raporu oluşturmak için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının içe aktarılacağı projenin adı.
- **EXPORT_FILE**: İçe aktarılacak veri kaynakları dışa aktarım dosyasının adı.

#### Seçenekler

- `--output-file`, `-o`: İçe aktarma raporunun kaydedileceği dosya (belirtilmezse, tablo halinde terminale yazdırılır).
- `--output-format`, `-f`: İçe aktarma raporunun kaydedileceği format (json, csv).
    
#### Örnek
  
`my_export.json` dışa aktarma dosyasındaki tüm veri kaynaklarını `ProjectB` içine aktarmak için:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
İçe aktarmanın ardından bu komut, içe aktarılan ve atlanan nesnelerin bir raporunu da gösterecektir. Yalnızca yeni veri kaynakları `ProjectB`'ye aktarılacaktır. Hangi nesnelerin aktarılacağını ve hangilerinin atlanacağını öğrenmek için `plan-import-ds` komutunu kullanabilirsiniz.

### plan-import-ds

`plan-import-ds` komutu, veri kaynaklarını hedef bir projeye içe aktarmadan önce analiz etmek ve bir içe aktarma raporu oluşturmak için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının içe aktarılacağı proje için planın oluşturulacağı proje adı.
- **EXPORT_FILE**: İçe aktarım öncesinde analiz edilecek dışa aktarma dosyasının adı.

#### Seçenekler

- `--output-file`, `-o`: İçe aktarma raporunun kaydedileceği dosya (belirtilmezse, tablo halinde terminale yazdırılır).
- `--output-format`, `-f`: İçe aktarma raporunun kaydedileceği format (json, csv).
    
#### Örnek
  
`my_export.json` dışa aktarma dosyasından `ProjectB`'ye aktarılırken hangi veri kaynaklarının aktarılacağını ve hangilerinin atlanacağını kontrol etmek için:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Bu komut yalnızca aktarılacak ve atlanacak nesnelerin bir içe aktarma planını gösterir.