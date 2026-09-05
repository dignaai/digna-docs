# digna CLI Referansı 2026.01
**2026-01-15**

Bu sayfa, ***digna*** CLI sürümü **2026.01** ile kullanılabilen tüm komutları, kullanım örneklerini ve seçeneklerini belgelemektedir.

---

## CLI Temelleri

---

### help
`--help` seçeneği, kullanılabilir komutlar ve bunların kullanımı hakkında bilgi sağlar. Bu seçeneği kullanmanın iki ana yolu vardır:

1. **Genel Yardımı Görüntüleme:**
   
    `--help` seçeneğini ***dignacli*** ifadesinin hemen ardından kullanın.  
   ```bash
   dignacli --help
   ```

2. **Belirli Bir Komut İçin Yardım Alma:**  
  
    Belirli bir komut hakkında ayrıntılı bilgi almak için o komuta `--help` ekleyin.  
    Örneğin, `add-user` komutu ile ilgili yardım almak için çalıştırın:
     ```bash
     dignacli add-user --help
     ```

     ### çıktı:
      
     - **Komut Açıklaması:** Komutun ne yaptığına dair ayrıntılı açıklama.  
     - **Sözdizimi:** Gerekli ve isteğe bağlı argümanlar dahil olmak üzere kesin sözdizimini gösterir.  
     - **Seçenekler:** Komuta özgü seçenekleri ve açıklamalarını listeler.  
     - **Örnekler:** Komutun etkili şekilde nasıl çalıştırılacağına dair örnekler sağlar.

### check-config

`check-config` komutu, ***digna*** CLI aracında ***digna*** yapılandırmasını test etmek için kullanılan bir yardımcı programdır. Bu komut, ***digna*** bileşenlerinin config.toml dosyasında ihtiyaç duyulan yapılandırma öğelerini bulabildiğini doğrular.

#### Seçenekler

- `--configpath`, `-cp`: Yapılandırmayı içeren dosya veya dizin. Belirtilmezse ../config.toml kullanılacaktır.
      
#### Komut Kullanımı
```bash
dignacli check-config
```

Başarılı bir yürütme sonucunda komut, yapılandırmanın tamamlandığına dair bir onay çıktısı verir.  
  
Yapılandırma eksik görünüyorsa, eksik yapılandırma öğeleri listelenecektir.

  
### check-repo-connection

`check-repo-connection` komutu, ***digna*** CLI aracında belirtilen bir ***digna*** deposuna bağlantı ve erişimi test etmek için kullanılan bir yardımcı programdır. Bu komut, CLI'nın depoyla etkileşim kurabildiğini doğrular.
      
#### Komut Kullanımı
```bash
dignacli check-repo-connection
```

Başarılı yürütme sonucunda komut, bağlantının doğrulandığına dair onay ile birlikte depo hakkında şu bilgileri verir: Repository version, Host, Database ve Schema.  
  
Depo bağlantısı başarılı değilse, doğru yapılandırma ayarları için config.toml dosyasını kontrol edin.


### version

Yüklü *dignacli* sürümünü kontrol etmek için `--version` seçeneğini kullanın.  
  
#### Komut Kullanımı
```bash
dignacli --version
```
  
#### Örnek Çıktı
```bash
dignacli version 2026.01
```

### logging options
  
Varsayılan olarak, ***digna*** komutlarının konsol çıktısı minimalist olacak şekilde tasarlanmıştır. Çoğu komut, ek bilgi sağlamaya olanak tanır; bunun için aşağıdaki seçenekler kullanılır:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” ve “debug” detay seviyesini belirlerken, “logfile” seçeneği çıktının konsol yerine bir dosyaya yönlendirilmesini sağlar.

## Kullanıcı Yönetimi

### add-user
  
`add-user` komutu, ***digna*** CLI içinde yeni bir kullanıcı eklemek için kullanılır.
  
#### Komut Kullanımı
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argümanlar

- **USER_NAME**: Yeni kullanıcı için kullanıcı adı (gereklidir).
- **USER_FULL_NAME**: Yeni kullanıcının tam adı (gereklidir).
- **USER_PASSWORD**: Yeni kullanıcı için parola (gereklidir).

#### Seçenekler

- `--is_superuser`, `-su`: Yeni kullanıcıyı yönetici olarak atamak için işaret.
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir sona erme tarihi belirler. Belirtilmezse hesapın bir sona erme tarihi olmaz.

#### Örnek

Kullanıcı adı `jdoe`, tam adı `John Doe` ve parolası `password123` olan yeni bir kullanıcı eklemek için:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Hesap sona erme tarihi belirleyerek yeni bir kullanıcı eklemek için:
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
- **USER_NAME**: Silinecek kullanıcının kullanıcı adı (gereklidir). Bu komutun gerektirdiği tek argümandır.

#### Örnek
```bash
dignacli delete-user jdoe
```
  
Bu komut `jdoe` kullanıcısını ***digna*** sisteminden kaldırır; erişimi iptal edilir ve depo içindeki ilişkili veri ve izinler silinir.

### modify-user

`modify-user` komutu, ***digna*** CLI içinde mevcut bir kullanıcının bilgilerini güncellemek için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argümanlar
  
- **USER_NAME**: Değiştirilecek kullanıcının kullanıcı adı (gereklidir).
- **USER_FULL_NAME**: Kullanıcının yeni tam adı (gereklidir).
  
#### Seçenekler  
  
- `--is_superuser`, `-su`: Kullanıcıyı süper kullanıcı olarak ayarlar, yükseltilmiş ayrıcalıklar verir. Bu bayrak bir değer gerektirmez.  
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir sona erme tarihi belirler. Sağlanmazsa, hesap süresiz geçerli kalır.  
  
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
  
- **USER_NAME**: Parolası değiştirilecek kullanıcının kullanıcı adı (gereklidir).
- **USER_PWD**: Kullanıcının yeni parolası (gereklidir).
  
#### Örnek
  
`jdoe` kullanıcısının parolasını `newpassword123` olarak değiştirmek için:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

`list-users` komutu, ***digna*** CLI içinde sisteme kayıtlı tüm kullanıcıları listelemek için kullanılır.

#### Komut Kullanımı

```bash
dignacli list-users
```

Bu komutu çalıştırmak, ***digna*** deposuna bağlanır ve kullanıcıların ID, kullanıcı adı, tam adı, süper kullanıcı durumu ve sona erme zaman damgalarını gösterir.

## Depo Yönetimi

### upgrade-repo
  
`upgrade-repo` komutu, ***digna*** CLI içinde ***digna*** deposunu yükseltmek veya başlatmak için kullanılır. Bu komut, güncellemeleri uygulamak veya depo altyapısını ilk kez kurmak için gereklidir.
  
#### Komut Kullanımı

```bash
dignacli upgrade-repo [options]
```
  
#### Seçenekler
  
- `--simulation-mode`, `-s`: Etkinleştirildiğinde, komut simülasyon modunda çalışır; yürütülecek SQL ifadelerini yazdırır ancak bunları gerçekten çalıştırmaz. Değişiklikleri uygulamadan önizlemek için faydalıdır.  

  
#### Örnek
  
***digna*** deposunu yükseltmek için, seçenek olmadan komutu çalıştırabilirsiniz:
  
```bash
dignacli upgrade-repo
```  
Yükseltmeyi simülasyon modunda çalıştırmak (SQL ifadelerini uygulamadan görmek) için:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Bu komut, ***digna*** sisteminin bakımında kritik öneme sahiptir; veritabanı şeması ve diğer depo bileşenlerinin yazılımın en son sürümüyle güncel olmasını sağlar.

### encrypt
  
`encrypt` komutu, ***digna*** CLI içinde bir parolayı şifrelemek için kullanılır.
  
#### Komut Kullanımı
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argümanlar
- **PASSWORD**: Şifrelenmesi gereken parola (gereklidir).
  
#### Örnek
  
Bir parolayı şifrelemek için parolayı argüman olarak vermeniz gerekir.   
Örneğin, `mypassword123` parolasını şifrelemek için:
```bash
dignacli encrypt mypassword123
```
Bu komut, verilen parolanın şifrelenmiş halini çıktılar; bu çıktı daha sonra güvenli ortamlarda kullanılabilir. Parola argümanı sağlanmazsa CLI eksik argüman hatası gösterecektir.

### generate-key
  
`generate-key` komutu, Fernet anahtarı üretmek için kullanılır; bu anahtar ***digna*** deposunda saklanan parolaların güvenliği için gereklidir.
  
#### Komut Kullanımı
```bash
dignacli generate-key
```
  
## Veri Yönetimi

### clean-up

`clean-up` komutu, ***digna*** CLI içinde bir veya daha fazla veri kaynağı için bir projeye ait profil, tahmin ve trafik ışığı sistemi verilerini silmek için kullanılır. Bu komut, veri yaşam döngüsü yönetimi açısından eski veya gereksiz verilerin temizlenmesine yardımcı olarak düzenli ve verimli bir veri ortamı sağlar.

#### Komut Kullanımı

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: Verilerin silineceği projenin adı (gereklidir). Bu argümanda all-projects anahtar kelimesi kullanılırsa, ***digna*** mevcut tüm projeler üzerinde yineleme yapar ve komutu uygular.
- **FROM_DATE**: Veri silimine başlanacak tarih ve saat. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (gereklidir).
- **TO_DATE**: Veri siliminin biteceği tarih ve saat; FROM_DATE ile aynı formatlar kullanılır (gereklidir).
  
#### Seçenekler
  
- `--table-name`, `-tn`: Temizleme işlemini proje içindeki belirli bir tabloyla sınırlar.
- `--table-filter`, `-tf`: İsimlerinde belirtilen alt dizeyi içeren tablolara temizleme uygulamak için filtre.
- `--timing`, `-tm`: İşlem tamamlandıktan sonra clean-up süresini gösterir.
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
  
`remove-orphans` komutu, ***digna*** deposunda temizlik işlemleri için kullanılır.  
Bir kullanıcı projeleri veya veri kaynaklarını sildiğinde, profiller ve tahminler depoda kalabilir. Bu komut ile böyle yetim (orphan) satırlar depodan kaldırılır.
  
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

Bu komut, birden fazla proje yöneten yönetici ve kullanıcılar için özellikle yararlıdır; ***digna*** deposunda mevcut projelerin hızlı bir genel görünümünü sağlar.

### list-ds

`list-ds` komutu, belirli bir proje içindeki mevcut veri kaynaklarının listesini görüntülemek için kullanılır. Bu komut, analiz ve yönetim için kullanılabilir veri varlıklarını anlamada faydalıdır.

#### Komut Kullanımı
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynakları listelenecek projenin adı (gereklidir).
  
#### Örnek
  
`ProjectA` adlı projedeki tüm veri kaynaklarını listelemek için:
  
```bash
dignacli list-ds ProjectA
```
  
Bu komut, bir projedeki kullanılabilir veri kaynaklarının genel görünümünü sağlar ve kullanıcıların veri ortamında daha etkili gezinmesine ve yönetmesine yardımcı olur.


### inspect

`inspect` komutu, ***digna*** CLI içinde bir veya daha fazla veri kaynağı için profil, tahmin ve trafik ışığı sistemi verilerini oluşturmak amacıyla kullanılır. Bu komut, belirli bir dönem içinde veriyi analiz etmeye ve izlemeye yardımcı olur. İnceleme tamamlandıktan sonra hesaplanan trafik ışığı sistemi değeri döndürülür:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Komut Kullanımı

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: İncelenecek verilerin ait olduğu proje adı (gereklidir). Bu argümanda all-projects anahtar kelimesi kullanılırsa, ***digna*** mevcut tüm projeler üzerinde yineleme yapar ve komutu uygular.
- **FROM_DATE**: Veri incelemesine başlanacak tarih ve saat. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (gereklidir).
- **TO_DATE**: Veri incelemesinin biteceği tarih ve saat; FROM_DATE ile aynı formatlar kullanılır (gereklidir).
  
#### Seçenekler

- `--table-name`, `-tn`: İncelemeyi proje içindeki belirli bir tablo ile sınırlar.
- `--table-filter`, `-tf`: İsimlerinde belirtilen alt dizeyi içeren tablolarda inceleme yapmak için filtre.
- `--enable_notification`, `-en`: Uyarı durumunda bildirim gönderilmesini etkinleştirir.
- `--bypass-backend`, `-bb`: Backend’i atlayarak incelemeyi doğrudan CLI üzerinden çalıştırır (sadece test amaçlı!).

  
#### Örnek
  
`ProjectA` projesi için 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri incelemek için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Sadece belirli bir tabloyu incelemek ve tahminlerin yeniden hesaplanmasını zorlamak için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Bu komut, güncellenmiş profiller ve tahminler oluşturmak, veri bütünlüğünü izlemek ve belirli bir proje zaman aralığında uyarı sistemlerini yönetmek için faydalıdır.

### inspect-async

`inspect-async` komutu, ***digna*** CLI içinde bir veya daha fazla veri kaynağı için profil, tahmin ve trafik ışığı sistemi verilerini oluşturmak amacıyla kullanılır. Bu komut, belirli bir dönem içinde veriyi analiz etmeye ve izlemeye yardımcı olur. `inspect-async` komutunun eşzamanlı (senkron) sürümünün aksine, bu komut incelemenin tamamlanmasını beklemez. Bunun yerine gönderilen inceleme isteği için bir istek kimliği (request id) döndürür. İncelemenin ilerlemesini sorgulamak için `inspect-status` komutunu kullanın.

#### Komut Kullanımı

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: İncelenecek verilerin ait olduğu proje adı (gereklidir). Bu argümanda all-projects anahtar kelimesi kullanılırsa, ***digna*** mevcut tüm projeler üzerinde yineleme yapar ve komutu uygular.
- **FROM_DATE**: Veri incelemesine başlanacak tarih ve saat. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (gereklidir).
- **TO_DATE**: Veri incelemesinin biteceği tarih ve saat; FROM_DATE ile aynı formatlar kullanılır (gereklidir).
  
#### Seçenekler

- `--table-name`, `-tn`: İncelemeyi proje içindeki belirli bir tablo ile sınırlar.
- `--table-filter`, `-tf`: İsimlerinde belirtilen alt dizeyi içeren tablolarda inceleme yapmak için filtre.
- `--enable_notification`, `-en`: Uyarı durumunda bildirim gönderilmesini etkinleştirir.

  
#### Örnek
  
`ProjectA` projesi için 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri asenkron olarak incelemek için:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

`inspect-status` komutu, ***digna*** CLI içinde asenkron bir incelemenin ilerlemesini istek kimliğine göre kontrol etmek için kullanılır.

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

`inspect-cancel` komutu, ***digna*** CLI içinde istek kimliğine göre incelemeleri iptal etmek için veya tüm mevcut istekleri iptal etmek için kullanılabilir.

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

`export-ds` komutu, ***digna*** CLI içinde ***digna*** deposundan veri kaynaklarının bir dışa aktarımını oluşturmak için kullanılır. Varsayılan olarak, verilen bir projedeki tüm veri kaynakları dışa aktarılır.

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
  
Bu komut, `ProjectA` içindeki tüm veri kaynaklarını başka bir projeye veya ***digna*** deposuna aktarılabilecek JSON belgesi olarak dışa aktarır.


### import-ds

`import-ds` komutu, ***digna*** CLI içinde veri kaynaklarını hedef bir projeye içe aktarmak ve bir içe aktarma raporu oluşturmak için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının içe aktarılacağı projenin adı.
- **EXPORT_FILE**: İçe aktarılacak veri kaynakları dışa aktarım dosyasının adı.

#### Seçenekler

- `--output-file`, `-o`: İçe aktarma raporunun kaydedileceği dosya (belirtilmezse, tablo biçiminde terminale yazdırılır).
- `--output-format`, `-f`: İçe aktarma raporunun kaydedileceği format (json, csv).
    
#### Örnek
  
`my_export.json` dışa aktarım dosyasındaki tüm veri kaynaklarını `ProjectB`'ye içe aktarmak için:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
İçe aktarma sonrasında bu komut, içe aktarılan ve atlanan nesnelerin bir raporunu da gösterir. Sadece yeni veri kaynakları `ProjectB`'ye içe aktarılacaktır. Hangi nesnelerin içe aktarılacağını ve hangilerinin atlanacağını önceden görmek için `plan-import-ds` komutunu kullanabilirsiniz.

### plan-import-ds

`plan-import-ds` komutu, ***digna*** CLI içinde bir dışa aktarım dosyasının hedef projeye içe aktarılmadan önce hangi veri kaynaklarının içe aktarılacağını ve hangilerinin atlanacağını analiz etmek için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının içe aktarılacağı proje olarak değerlendirilecek hedef projenin adı.
- **EXPORT_FILE**: İçe aktarım öncesinde analiz edilecek dışa aktarım dosyasının adı.

#### Seçenekler

- `--output-file`, `-o`: İçe aktarma planı raporunun kaydedileceği dosya (belirtilmezse, tablo biçiminde terminale yazdırılır).
- `--output-format`, `-f`: Raporun kaydedileceği format (json, csv).
    
#### Örnek
  
`my_export.json` dışa aktarım dosyasından `ProjectB`'ye hangi veri kaynaklarının içe aktarılacağını ve hangilerinin atlanacağını kontrol etmek için:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Bu komut yalnızca içe aktarılacak ve atlanacak nesnelerin bir planını gösterir.