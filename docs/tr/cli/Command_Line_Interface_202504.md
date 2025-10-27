---
title: digna CLI Reference 2025.04 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2025.04. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, and more.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202504/
image: /assets/logo_square.png
---

# digna CLI Reference 2025.04
**2025-04-01**

Bu sayfa, ***digna*** CLI sürümü **2025.04**’te kullanılabilir tüm komutları, kullanım örnekleri ve seçenekleri ile belgelendirir.

---

## CLI Temelleri

---

## `help` Seçeneğinin Kullanımı

`--help` seçeneği, kullanılabilir komutlar ve bunların kullanımı hakkında bilgi sağlar. Bu seçeneğin iki ana kullanım şekli vardır:

1. **Genel Yardımı Görüntüleme:**
   
   `dignacli` anahtar kelimesinden hemen sonra `--help` kullanın.  
   ```bash
   dignacli --help
   ```

2. **Belirli Bir Komut İçin Yardım Alma:**  
  
   Belirli bir komut hakkında ayrıntılı bilgi almak için o komuta `--help` ekleyin.  
   Örneğin, `add-user` komutu için yardım almak üzere şu komutu çalıştırın:
   ```bash
   dignacli add-user --help
   ```

   ### çıktı:
      
   - **Komut Açıklaması:** Komutun ne yaptığını ayrıntılı olarak açıklar.  
   - **Sözdizimi:** Gerekli ve isteğe bağlı argümanlar da dahil olmak üzere tam sözdizimini gösterir.  
   - **Seçenekler:** Komuta özgü seçenekleri ve açıklamalarını listeler.  
   - **Örnekler:** Komutun etkili bir şekilde nasıl çalıştırılacağına dair örnekler sağlar.

  
## `check-repo-connection` Komutunun Kullanımı

`check-repo-connection` komutu, ***digna*** CLI aracında belirtilen bir ***digna*** deposuna erişimi ve bağlantıyı test etmek için kullanılan bir yardımcı programdır. Bu komut, CLI'nın depoyla etkileşime girebildiğini doğrular.
      
#### Komut Kullanımı
```bash
dignacli check-repo-connection
```

Başarılı yürütme durumunda komut bağlantıyı onaylayan bir çıktı verir ve depo hakkında şu bilgileri gösterir: Repository version, Host, Database ve Schema.  
  
Eğer depo bağlantısı başarılı değilse, config.toml dosyasındaki yapılandırma ayarlarının doğru olduğundan emin olun.

## `version` komutunun Kullanımı

Yüklü *dignacli* sürümünü kontrol etmek için `--version` seçeneğini kullanın.  
  
#### Komut Kullanımı
```bash
dignacli --version
```
  
#### Örnek Çıktı
```bash
dignacli version 2025.04
```

## Günlükleme (logging) Seçeneklerinin Kullanımı
  
Varsayılan olarak, ***digna*** komutlarının konsol çıktısı minimalist olacak şekilde tasarlanmıştır. Çoğu komut ek bilgi sağlama olanağı sunar; aşağıdaki seçenekler kullanılabilir:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” ve “debug” detay seviyesini belirlerken, “logfile” anahtarı çıktıyı konsol yerine bir dosyaya yönlendirmeye olanak tanır.

## Kullanıcı Yönetimi

### `add-user` Komutunun Kullanımı
  
`add-user` komutu, ***digna*** CLI içinde yeni bir kullanıcı eklemek için kullanılır.
  
#### Komut Kullanımı
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argümanlar

- **USER_NAME**: Yeni kullanıcı için kullanıcı adı (zorunlu).
- **USER_FULL_NAME**: Yeni kullanıcının tam adı (zorunlu).
- **USER_PASSWORD**: Yeni kullanıcı için parola (zorunlu).

#### Seçenekler

- `--is_superuser`, `-su`: Yeni kullanıcıyı yönetici olarak işaretlemek için bayrak.
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir son geçerlilik tarihi belirler. Belirtilmezse hesap için son geçerlilik tarihi yoktur.

#### Örnek

Kullanıcı adı `jdoe`, tam adı `John Doe` ve parolası `password123` olan yeni bir kullanıcı eklemek için:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Bir kullanıcı ekleyip hesap son geçerlilik tarihini ayarlamak için:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### `delete-user` Komutunun Kullanımı
  
`delete-user` komutu, ***digna*** CLI içinde mevcut bir kullanıcıyı sistemden kaldırmak için kullanılır.
  
#### Komut Kullanımı
```bash
dignacli delete-user USER_NAME
```
  
##### Argümanlar
- **USER_NAME**: Silinecek kullanıcının kullanıcı adı (zorunlu). Bu komutun gerektirdiği tek argümandır.

#### Örnek
```bash
dignacli delete-user jdoe
```
  
Bu komut `jdoe` kullanıcısını ***digna*** sisteminden kaldırır, erişimini iptal eder ve depodaki ilişkili verileri ve izinleri siler.

### `modify-user` Komutunun Kullanımı

`modify-user` komutu, ***digna*** CLI içinde mevcut bir kullanıcının bilgilerini güncellemek için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argümanlar
  
- **USER_NAME**: Bilgileri değiştirilecek kullanıcının kullanıcı adı (zorunlu).
- **USER_FULL_NAME**: Kullanıcı için yeni tam ad (zorunlu).
  
#### Seçenekler  
  
- `--is_superuser`, `-su`: Kullanıcıyı süper kullanıcı olarak ayarlar; yükseltilmiş ayrıcalıklar verir. Bu bayrak bir değer gerektirmez.  
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir son geçerlilik tarihi belirler. Belirtilmezse hesap süresiz geçerli kalır.  
  
#### Örnek
  
`jdoe` kullanıcısının tam adını “Johnathan Doe” olarak değiştirmek ve kullanıcıyı süper kullanıcı yapmak için:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### `modify-user-pwd` Komutunun Kullanımı
  
`modify-user-pwd` komutu, ***digna*** CLI içinde mevcut bir kullanıcının parolasını değiştirmek için kullanılır.
  
#### Komut Kullanımı
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argümanlar
  
- **USER_NAME**: Parolası değiştirilecek kullanıcının kullanıcı adı (zorunlu).
- **USER_PWD**: Kullanıcı için yeni parola (zorunlu).
  
#### Örnek
  
`jdoe` kullanıcısının parolasını `newpassword123` olarak değiştirmek için:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### `list-users` Komutunun Kullanımı

`list-users` komutu, ***digna*** CLI içinde kayıtlı tüm kullanıcıların bir listesini gösterir.

#### Komut Kullanımı

```bash
dignacli list-users
```

Bu komutu çalıştırmak, ***digna*** deposuna bağlanır ve tüm kullanıcıları ID, kullanıcı adı, tam ad, süper kullanıcı durumu ve son geçerlilik zaman damgası ile listeler.

## Repository Yönetimi

### `upgrade-repo` Komutunun Kullanımı
  
`upgrade-repo` komutu, ***digna*** CLI içinde ***digna*** deposunu yükseltmek veya başlatmak için kullanılır. Bu komut, güncellemeleri uygulamak veya depo altyapısını ilk kez kurmak için gereklidir.
  
#### Komut Kullanımı

```bash
dignacli upgrade-repo [options]
```
  
#### Seçenekler
  
- `--simulation-mode`, `-s`: Etkinleştirildiğinde komut simülasyon modunda çalışır; yürütülecek SQL ifadelerini yazdırır ancak bunları gerçek anlamda çalıştırmaz. Depoda değişiklik yapmadan önizleme yapmak için faydalıdır.  

  
#### Örnek
  
***digna*** deposunu yükseltmek için seçenek belirtmeden komutu çalıştırabilirsiniz:
  
```bash
dignacli upgrade-repo
```  
Yükseltmeyi simülasyon modunda çalıştırmak (SQL ifadelerini görmek ama uygulamamak) için:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Bu komut, ***digna*** sisteminin bakımında kritik öneme sahiptir ve veritabanı şeması ile diğer depo bileşenlerinin yazılımın en son sürümü ile uyumlu olmasını sağlar.

### `encrypt` Komutunun Kullanımı
  
`encrypt` komutu, ***digna*** CLI içinde bir parolayı şifrelemek için kullanılır.
  
#### Komut Kullanımı
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argümanlar
- **PASSWORD**: Şifrelenmesi gereken parola (zorunlu).
  
#### Örnek
  
Bir parolayı şifrelemek için parola argüman olarak sağlanmalıdır.  
Örneğin, `mypassword123` parolasını şifrelemek için:
```bash
dignacli encrypt mypassword123
```
Bu komut verilen parolanın şifrelenmiş halini çıktı olarak verir; bu şifrelenmiş değer daha sonra güvenli bağlamlarda kullanılabilir. Parola argümanı sağlanmazsa CLI, eksik argüman hatası gösterecektir.

## `generate-key` Komutunun Kullanımı
  
`generate-key` komutu, ***digna*** deposunda saklanan parolaları güvence altına almak için gerekli olan bir Fernet anahtarı oluşturmak için kullanılır.
  
#### Komut Kullanımı
```bash
dignacli generate-key
```
  
## Veri Yönetimi

## `clean-up` Komutunun Kullanımı

`clean-up` komutu, ***digna*** CLI içinde belirtilen bir proje kapsamında bir veya daha fazla veri kaynağı için profil, tahmin ve trafik ışığı sistemi verilerini silmek için kullanılır. Bu komut, veri yaşam döngüsü yönetimi için önemlidir ve güncel olmayan veya gereksiz verilerin temizlenmesine yardımcı olur.

#### Komut Kullanımı

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: Verilerin silineceği projenin adı (zorunlu). Bu argümana all-projects anahtar kelimesi verilirse ***digna*** mevcut tüm projeler üzerinde yineleme yapar ve komutu uygular.
- **FROM_DATE**: Veri silme için başlangıç tarih ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (zorunlu).
- **TO_DATE**: Veri silme için bitiş tarih ve saati; FROM_DATE ile aynı formatları kabul eder (zorunlu).
  
#### Seçenekler
  
- `--table-name`, `-tn`: Temizleme işlemini proje içindeki belirli bir tablo ile sınırlar.
- `--table-filter`, `-tf`: İsimlerinde belirtilen alt dizeyi içeren tablolarla sınırlamak için filtre uygular.
- `--timing`, `-tm`: Tamamlandıktan sonra temizleme sürecinin süre bilgisini gösterir.
- `--help`: clean-up komutu için yardım bilgisini gösterir ve çıkar.
  
#### Örnek
  
ProjectA projesinden 1 Ocak 2023 ile 30 Haziran 2023 arasındaki verileri silmek için:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Sadece `Table1` adlı belirli bir tablodan veri silmek için:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Bu komut, veri depolamayı yönetmeye ve deponun yalnızca ilgili bilgileri içermesini sağlamaya yardımcı olur.

## `list-projects` Komutunun Kullanımı
  
`list-projects` komutu, ***digna*** CLI içinde mevcut tüm projelerin bir listesini görüntülemek için kullanılır.
  
#### Komut Kullanımı
  
```bash
dignacli list-projects
```

Bu komut, birden fazla projeyi yöneten yöneticiler ve kullanıcılar için özellikle yararlıdır; ***digna*** deposundaki mevcut projelere hızlı bir bakış sağlar.

## `list-ds` Komutunun Kullanımı

`list-ds` komutu, belirtilen bir proje içindeki mevcut veri kaynaklarının listesini görüntülemek için kullanılır. Bu komut, analiz ve yönetim için kullanılabilir veri varlıklarını anlamaya yardımcı olur.

#### Komut Kullanımı
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının listelendiği proje adı (zorunlu).
  
#### Örnek
  
`ProjectA` adlı projedeki tüm veri kaynaklarını listelemek için:
  
```bash
dignacli list-ds ProjectA
```
  
Bu komut, bir projede mevcut veri kaynakları hakkında genel bir bakış sağlayarak veri ortamını daha etkin yönetmeye yardımcı olur.


## `inspect` Komutunun Kullanımı

`inspect` komutu, ***digna*** CLI içinde belirtilen bir proje için bir veya daha fazla veri kaynağı adına profiller, tahminler ve trafik ışığı sistemi verileri oluşturmak için kullanılır. Bu komut, belirli bir dönem boyunca veri analiz ve izleme yapmaya yardımcı olur.

#### Komut Kullanımı

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: İncelenecek verilerin ait olduğu proje adı (zorunlu). Bu argümana all-projects anahtar kelimesi verilirse ***digna*** mevcut tüm projelerde yineleme yapar ve komutu uygular.
- **FROM_DATE**: Veri incelemesi için başlangıç tarih ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (zorunlu).
- **TO_DATE**: Veri incelemesi için bitiş tarih ve saati; FROM_DATE ile aynı formatları kabul eder (zorunlu).
  
#### Seçenekler

- `--table-name`, `-tn`: İncelemeyi proje içindeki belirli bir tablo ile sınırlar.
- `--table-filter`, `-tf`: İsimlerinde belirtilen alt dizeyi içeren tabloları incelemek için filtre uygular.
- `--do-profile`: Profil yeniden toplanmasını tetikler. Varsayılan do-profile’dur.
- `--no-do-profile`: Profil yeniden toplanmasını engeller.
- `--do-prediction`: Tahminlerin yeniden hesaplanmasını tetikler. Varsayılan do-prediction’dur.
- `--no-do-prediction`: Tahminlerin yeniden hesaplanmasını engeller.
- `--do-alert-status`: Uyarı durumlarının yeniden hesaplanmasını tetikler. Varsayılan do-alert-status’dur.
- `--no-do-alert-status`: Uyarı durumlarının yeniden hesaplanmasını engeller.
- `--iterative`: İncelemeyi günlük iterasyonlar kullanarak tetikler. Varsayılan iterative’dir.
- `--no-iterative`: Tüm dönemi tek seferde incelemeyi tetikler.
- `--enable_notification`, `-en`: Uyarı durumunda bildirim gönderimini etkinleştirir.
- `--timing`, `-tm`: İnceleme tamamlandıktan sonra sürenin gösterilmesini sağlar.
  
#### Örnek
  
`ProjectA` projesinin 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verilerini incelemek için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Sadece belirli bir tabloyu incelemek ve tahminlerin yeniden hesaplanmasını zorlamak için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Bu komut, güncellenmiş profiller ve tahminler oluşturmak, veri bütünlüğünü izlemek ve belirtilen proje zaman aralığında uyarı sistemlerini yönetmek için kullanışlıdır.

## `tls-status` Komutunun Kullanımı

`tls-status` komutu, ***digna*** CLI içinde belirli bir proje ve tablo için Trafik Işık Sistemi (TLS) durumunu belirtilen tarih için sorgulamak amacıyla kullanılır. Trafik Işık Sistemi, verinin sağlığı ve kalitesi hakkında uyarı veya sorunlara işaret eden bilgiler sağlar.
  
#### Komut Kullanımı
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argümanlar
  
- **PROJECT_NAME**: TLS durumunun sorgulandığı proje adı (zorunlu).
- **TABLE_NAME**: TLS durumu istenen proje içindeki belirli tablo (zorunlu).
- **DATE**: TLS durumunun sorgulandığı tarih; genellikle %Y-%m-%d formatında (zorunlu).
  
#### Örnek
  
`ProjectA` projesinde `UserData` adlı tablonun 1 Temmuz 2024 tarihindeki TLS durumunu kontrol etmek için:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Bu komut, önceden tanımlanmış kriterlere dayalı olarak net ve eyleme geçirilebilir bir durum raporu sağlayarak veri kalitesinin izlenmesine ve korunmasına yardımcı olur.

## `inspect-async` Komutunun Kullanımı

`inspect-async` komutu, ***digna*** CLI içinde arka uca belirli bir proje için bir veya daha fazla veri kaynağı üzerinde incelemenin eşzamansız (asenkron) olarak yapılmasını talep etmek için kullanılır. Eğer PROJECT_NAME all-projects olarak ayarlanırsa, inceleme tüm mevcut projeler üzerinde yineleme yapar. Komut, incelemenin ilerlemesini takip etmek için kullanılabilecek bir istek kimliği (request id) döndürür.

#### Komut Kullanımı

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: İncelenecek verilerin ait olduğu proje adı (zorunlu). Bu argümana all-projects anahtar kelimesi verilirse ***digna*** mevcut tüm projeler üzerinde yineleme yapar ve komutu uygular.
- **FROM_DATE**: Veri incelemesi için başlangıç tarih ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (zorunlu).
- **TO_DATE**: Veri incelemesi için bitiş tarih ve saati; FROM_DATE ile aynı formatları kabul eder (zorunlu).
  
#### Seçenekler

- `--table-name`, `-tn`: İncelemeyi proje içindeki belirli bir tablo ile sınırlar.
- `--table-filter`, `-tf`: İsimlerinde belirtilen alt dizeyi içeren tabloları incelemek için filtre uygular.

  
#### Örnek
  
`ProjectA` için 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri eşzamansız olarak incelemek için:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## `inspect-status` Komutunun Kullanımı

`inspect-status` komutu, eşzamansız bir incelemenin ilerlemesini istek kimliğine (request ID) göre kontrol etmek için kullanılır.

#### Komut Kullanımı

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argümanlar
  
- **REQUEST_ID**: `inspect-async` komutu tarafından döndürülen istek kimliği 
  
#### Seçenekler

- `--report_level`, `-rl`: Rapor seviyesini ayarlar: 'task' veya 'step' [varsayılan: task]
  
#### Örnek
  
İstek kimliği 12345 olan bir incelemenin ayrıntılı adım seviyesindeki ilerlemesini kontrol etmek için:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## `export-ds` Komutunun Kullanımı

`export-ds` komutu, ***digna*** CLI içinde veri kaynaklarının ***digna*** deposundan dışa aktarılmasını sağlamak için kullanılır. Varsayılan olarak belirtilen projedeki tüm veri kaynakları dışa aktarılır.

#### Komut Kullanımı
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının dışa aktarılacağı proje adı.

#### Seçenekler

- `--table_name`, `-tn`: Bir projeden belirli bir veri kaynağını dışa aktarır.
- `--exportfile`, `-ef`: Dışa aktarım için dosya adını belirtir.
    
#### Örnek
  
`ProjectA` projesindeki tüm veri kaynaklarını dışa aktarmak için:
  
```bash
dignacli export-ds ProjectA
```
  
Bu komut, `ProjectA` içindeki tüm veri kaynaklarını başka bir projeye veya ***digna*** deposuna aktarılabilecek JSON belgesi olarak dışa aktarır.


## `import-ds` Komutunun Kullanımı

`import-ds` komutu, ***digna*** CLI içinde veri kaynaklarını hedef bir projeye içe aktarmak ve bir içe aktarma raporu oluşturmak için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının içe aktarılacağı proje adı.
- **EXPORT_FILE**: İçe aktarılacak veri kaynakları dışa aktarım dosyasının adı.

#### Seçenekler

- `--output-file`, `-o`: İçe aktarma raporunun kaydedileceği dosya (belirtilmezse terminalde tablo şeklinde yazdırılır).
- `--output-format`, `-f`: İçe aktarma raporunun kaydedileceği format (json, csv).
    
#### Örnek
  
`my_export.json` dışa aktarım dosyasındaki tüm veri kaynaklarını `ProjectB` projesine içe aktarmak için:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
İçe aktarma sonrası bu komut, içe aktarılan ve atlanan nesnelerin bir raporunu da gösterir. Yalnızca yeni veri kaynakları `ProjectB` içine aktarılacaktır. Hangi nesnelerin içe aktarılacağını ve hangilerinin atlanacağını görmek için `plan-import-ds` komutunu kullanabilirsiniz.

## `plan-import-ds` Komutunun Kullanımı

`plan-import-ds` komutu, ***digna*** CLI içinde veri kaynaklarının hedef bir projeye içe aktarılmadan önce hangi nesnelerin içe aktarılacağını ve hangilerinin atlanacağını analiz etmek için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının içe aktarılacağı proje adı (analiz edilecek hedef proje).
- **EXPORT_FILE**: İçe aktarım öncesi analiz edilecek dışa aktarım dosyasının adı.

#### Seçenekler

- `--output-file`, `-o`: İçe aktarma planı raporunun kaydedileceği dosya (belirtilmezse terminalde tablo şeklinde yazdırılır).
- `--output-format`, `-f`: Raporun kaydedileceği format (json, csv).
    
#### Örnek
  
`my_export.json` dosyasından `ProjectB` projesine hangi veri kaynaklarının içe alınacağını ve hangilerinin atlanacağını kontrol etmek için:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Bu komut yalnızca içe aktarılacak ve atlanacak nesnelerin bir planını gösterir.