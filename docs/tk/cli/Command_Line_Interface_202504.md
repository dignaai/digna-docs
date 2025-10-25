---
title: digna CLI Reference 2025.04 – Komutlar & Örnekler | digna Documentation
description: digna CLI sürümü 2025.04 için eksiksiz referans. add-user, check-repo-connection, upgrade-repo, inspect ve daha fazlası gibi komutlarla kullanıcıları, repository'leri ve verileri nasıl yöneteceğinizi öğrenin.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202504/
image: /assets/logo_square.png
---

# digna CLI Reference 2025.04
**2025-04-01**

Bu sayfa, ***digna*** CLI sürümü **2025.04**'te kullanılabilir tüm komutların kullanım örnekleri ve seçenekleriyle birlikte tam dökümantasyonunu sunar.

---

## CLI Temelleri

---

## `help` Seçeneğini Kullanma

`--help` seçeneği, kullanılabilir komutlar ve bunların kullanımı hakkında bilgi sağlar. Bu seçeneği kullanmanın iki temel yolu vardır:

1. **Genel Yardımı Görüntüleme:**
   
    `***digna***` anahtar kelimesinin hemen ardından `--help` kullanın.  
   ```bash
   dignacli --help

2. **Belirli Komutlar İçin Yardım Alma:**  
  
    Belirli bir komut hakkında ayrıntılı bilgi almak için o komuta `--help` ekleyin.  
    Örneğin, `add-user` komutu için yardım almak istiyorsanız şunu çalıştırın:
     ```bash
     dignacli add-user --help
     ```

     ### çıktı:
      
     - **Komut Açıklaması:** Komutun ne yaptığını detaylı olarak açıklar.  
     - **Sözdizimi:** Gerekli ve isteğe bağlı argümanlar dahil olmak üzere tam sözdizimini gösterir.  
     - **Seçenekler:** Komuta özgü seçenekleri ve bunların açıklamalarını listeler.  
     - **Örnekler:** Komutun etkili bir şekilde nasıl çalıştırılacağına dair örnekler sağlar.

  
## `check-repo-connection` Komutunun Kullanımı

`check-repo-connection` komutu, ***digna*** CLI aracında belirtilen bir ***digna*** repository'sine bağlantı ve erişimi test etmek için kullanılan bir araçtır. Bu komut, CLI'nin repository ile etkileşime girebildiğini doğrular.
      
#### Komut Kullanımı
```bash
dignacli check-repo-connection
```

Başarılı yürütme halinde komut, bağlantı onayının yanı sıra repository hakkında şu bilgileri çıktı olarak verir: Repository sürümü, Host, Database ve Schema.  
  
Eğer repository bağlantısı başarılı değilse, config.toml dosyasındaki yapılandırma ayarlarını kontrol edin.

## `version` Komutunun Kullanımı

Yüklü *dignacli* sürümünü kontrol etmek için `--version` seçeneğini kullanın.  
  
#### Komut Kullanımı
```bash
dignacli --version
```
  
#### Örnek Çıktı
```bash
dignacli version 2025.04
```

## Loglama Seçeneklerini Kullanma
  
Varsayılan olarak, ***digna*** komutlarının konsol çıktısı minimal düzeyde olacak şekilde tasarlanmıştır. Çoğu komut, ek bilgi sağlama olanağı sunar; aşağıdaki seçenekler kullanılabilir:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
“verbose” ve “debug” ayrıntı düzeyini tanımlar; “logfile” anahtarı ise çıktının konsol penceresi yerine bir dosyaya yönlendirilmesine olanak tanır.

## Kullanıcı Yönetimi

### `add-user` Komutunun Kullanımı
  
***digna*** CLI içindeki `add-user` komutu, ***digna*** sistemine yeni bir kullanıcı eklemek için kullanılır.
  
#### Komut Kullanımı
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argümanlar

- **USER_NAME**: Yeni kullanıcı için kullanıcı adı (zorunlu).
- **USER_FULL_NAME**: Yeni kullanıcının tam adı (zorunlu).
- **USER_PASSWORD**: Yeni kullanıcı için parola (zorunlu).

#### Seçenekler

- `--is_superuser`, `-su`: Yeni kullanıcıyı yönetici (superuser) olarak atamak için bayrak.
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir son geçerlilik tarihi belirler. Belirtilmezse hesap için bir sona erme tarihi yoktur.

#### Örnek

Kullanıcı adı `jdoe`, tam adı `John Doe` ve parolası `password123` olan yeni bir kullanıcı eklemek için:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Hesap son geçerlilik tarihi belirleyerek yeni bir kullanıcı eklemek için:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### `delete-user` Komutunun Kullanımı
  
`delete-user` komutu, ***digna*** CLI'da var olan bir kullanıcıyı ***digna*** sisteminden kaldırmak için kullanılır.
  
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
  
Bu komut `jdoe` kullanıcısını ***digna*** sisteminden kaldırır; erişimini iptal eder ve repository'deki ilgili veri ve izinlerini siler.

### `modify-user` Komutunun Kullanımı

`modify-user` komutu, ***digna*** CLI'da mevcut bir kullanıcının bilgilerini güncellemek için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argümanlar
  
- **USER_NAME**: Güncellenecek kullanıcının kullanıcı adı (zorunlu).
- **USER_FULL_NAME**: Kullanıcının yeni tam adı (zorunlu).
  
#### Seçenekler  
  
- `--is_superuser`, `-su`: Kullanıcıyı superuser olarak ayarlar; yükseltilmiş ayrıcalık verir. Bu bayrak bir değer gerektirmez.  
- `--valid_until`, `-vu`: Kullanıcı hesabı için YYYY-MM-DD HH:MI:SS formatında bir son geçerlilik tarihi belirler. Verilmezse hesap süresiz geçerli kalır.  
  
#### Örnek
  
`jdoe` kullanıcısının tam adını “Johnathan Doe” olarak değiştirmek ve kullanıcıyı superuser yapmak için:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### `modify-user-pwd` Komutunun Kullanımı
  
`modify-user-pwd` komutu, ***digna*** CLI'da mevcut bir kullanıcının parolasını değiştirmek için kullanılır.
  
#### Komut Kullanımı
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argümanlar
  
- **USER_NAME**: Parolası değiştirilecek kullanıcının kullanıcı adı (zorunlu).
- **USER_PWD**: Kullanıcının yeni parolası (zorunlu).
  
#### Örnek
  
`jdoe` kullanıcısının parolasını `newpassword123` olarak değiştirmek için:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### `list-users` Komutunun Kullanımı

`list-users` komutu, ***digna*** CLI'da ***digna*** sistemine kayıtlı tüm kullanıcıları listeler.

#### Komut Kullanımı

```bash
dignacli list-users
```

Bu komutu çalıştırmak repository'ye bağlanır ve kullanıcıların ID'si, kullanıcı adı, tam adı, superuser durumu ve son geçerlilik zaman damgalarını göstererek tüm kullanıcıları listeler.

## Repository Yönetimi

### `upgrade-repo` Komutunun Kullanımı
  
`upgrade-repo` komutu, ***digna*** CLI'da ***digna*** repository'sini yükseltmek veya başlatmak için kullanılır. Bu komut, güncellemeleri uygulamak veya repository altyapısını ilk kez kurmak için gereklidir.
  
#### Komut Kullanımı

```bash
dignacli upgrade-repo [options]
```
  
#### Seçenekler
  
- `--simulation-mode`, `-s`: Etkinleştirildiğinde komut simülasyon modunda çalışır; çalıştırılacak SQL ifadelerini yazdırır ancak bunları gerçekten yürütmez. Değişiklikleri uygulamadan önce önizleme yapmak için kullanışlıdır.  

  
#### Örnek
  
***digna*** repository'sini yükseltmek için herhangi bir seçenek olmadan komutu çalıştırabilirsiniz:
  
```bash
dignacli upgrade-repo
```  
Yükseltmeyi simülasyon modunda çalıştırmak (SQL ifadelerini görmek ama uygulamamak) için:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Bu komut, veritabanı şeması ve diğer repository bileşenlerinin yazılımın en son sürümüyle uyumlu olmasını sağlayarak ***digna*** sisteminin bakımında kritik öneme sahiptir.

### `encrypt` Komutunun Kullanımı
  
`encrypt` komutu, ***digna*** CLI'da bir parolayı şifrelemek için kullanılır.
  
#### Komut Kullanımı
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argümanlar
- **PASSWORD**: Şifrelenmesi gereken parola (zorunlu).
  
#### Örnek
  
Bir parolayı şifrelemek için parolayı argüman olarak vermeniz gerekir.   
Örneğin, `mypassword123` parolasını şifrelemek için:
```bash
dignacli encrypt mypassword123
```
Bu komut, sağlanan parolanın şifrelenmiş halini çıktı olarak verir; daha sonra güvenli bağlamlarda kullanılabilir. Parola argümanı verilmezse, CLI eksik argümanı belirten bir hata gösterir.

## `generate-key` Komutunun Kullanımı
  
`generate-key` komutu, Fernet anahtarı oluşturmak için kullanılır; bu anahtar ***digna*** repository'sinde saklanan parolaların güvenliğini sağlamada gereklidir.
  
#### Komut Kullanımı
```bash
dignacli generate-key
```
  
## Veri Yönetimi

## `clean-up` Komutunun Kullanımı

`clean-up` komutu, ***digna*** CLI'da belirli bir proje içindeki bir veya daha fazla veri kaynağı için profilleri, tahminleri ve trafik ışığı sistemi verilerini kaldırmak için kullanılır. Bu komut, veri yaşam döngüsü yönetimi için önemlidir ve eski veya gereksiz verileri temizleyerek düzenli ve verimli bir veri ortamının korunmasına yardımcı olur.

#### Komut Kullanımı

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: Verilerin kaldırılacağı proje adı (zorunlu). Bu argümana all-projects anahtar kelimesi verildiğinde ***digna*** tüm mevcut projeler üzerinde yineleme yaparak komutu uygular.
- **FROM_DATE**: Veri kaldırma için başlangıç tarih ve zamanı. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (zorunlu).
- **TO_DATE**: Veri kaldırma için bitiş tarih ve zamanı; FROM_DATE ile aynı formatları kabul eder (zorunlu).
  
#### Seçenekler
  
- `--table-name`, `-tn`: Temizleme işlemini projedeki belirli bir tabloyla sınırlar.
- `--table-filter`, `-tf`: Tablo adlarında belirtilen alt dizeyi içeren tablolarla sınırlamak için filtre uygular.
- `--timing`, `-tm`: İşlem tamamlandıktan sonra temizleme süresini gösterir.
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
  
Bu komut, veri depolamayı yönetmeye yardımcı olur ve repository'de yalnızca ilgili bilgilerin tutulmasını sağlar.

## `list-projects` Komutunun Kullanımı
  
`list-projects` komutu, ***digna*** CLI'da sistemdeki tüm mevcut projelerin listesini göstermek için kullanılır.
  
#### Komut Kullanımı
  
```bash
dignacli list-projects
```

Bu komut, birden çok projeyi yöneten yöneticiler ve kullanıcılar için özellikle yararlıdır; repository'deki mevcut projelerin hızlı bir genel görünümünü sağlar.

## `list-ds` Komutunun Kullanımı

`list-ds` komutu, belirtilen bir proje içindeki tüm mevcut veri kaynaklarının listesini görüntülemek için kullanılır. Bu komut, analiz ve yönetim için kullanılabilecek veri varlıklarını anlamaya yardımcı olur.

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
  
Bu komut, bir projedeki mevcut veri kaynaklarının genel görünümünü sağlayarak veri ortamını daha etkin yönetmeye yardımcı olur.


## `inspect` Komutunun Kullanımı

`inspect` komutu, ***digna*** CLI'da belirli bir proje içindeki bir veya daha fazla veri kaynağı için profiller, tahminler ve trafik ışığı sistemi verileri oluşturmak için kullanılır. Bu komut, belirli bir dönem boyunca veri analizine ve izlemeye yardımcı olur.

#### Komut Kullanımı

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: Denetlenecek verilerin ait olduğu proje adı (zorunlu). Bu argümana all-projects anahtar kelimesi verildiğinde ***digna*** mevcut tüm projeler üzerinde yineleme yapar.
- **FROM_DATE**: Veri incelemesi için başlangıç tarih ve zamanı. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (zorunlu).
- **TO_DATE**: Veri incelemesi için bitiş tarih ve zamanı; FROM_DATE ile aynı formatları kabul eder (zorunlu).
  
#### Seçenekler

- `--table-name`, `-tn`: İncelemeyi projedeki belirli bir tabloyla sınırlar.
- `--table-filter`, `-tf`: İsimlerinde belirtilen alt dizeyi içeren tabloları incelemek için filtre uygular.
- `--do-profile`: Profillerin yeniden toplanmasını tetikler. Varsayılan: do-profile.
- `--no-do-profile`: Profillerin yeniden toplanmasını engeller.
- `--do-prediction`: Tahminlerin yeniden hesaplanmasını tetikler. Varsayılan: do-prediction.
- `--no-do-prediction`: Tahminlerin yeniden hesaplanmasını engeller.
- `--do-alert-status`: Uyarı durumlarının yeniden hesaplanmasını tetikler. Varsayılan: do-alert-status.
- `--no-do-alert-status`: Uyarı durumlarının yeniden hesaplanmasını engeller.
- `--iterative`: Belirtilen dönemin günlük yinelemelerle incelenmesini tetikler. Varsayılan: iterative.
- `--no-iterative`: Belirtilen dönemin tek seferde incelenmesini sağlar.
- `--enable_notification`, `-en`: Uyarı durumunda bildirim gönderimini etkinleştirir.
- `--timing`, `-tm`: İnceleme işlemi tamamlandıktan sonra süresini gösterir.
  
#### Örnek
  
`ProjectA` projesi için 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri incelemek için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Sadece belirli bir tabloyu incelemek ve tahminlerin yeniden hesaplanmasını zorlamak için:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Bu komut, güncellenmiş profiller ve tahminler oluşturmak, veri bütünlüğünü izlemek ve belirtilen proje zaman aralığında uyarı sistemlerini yönetmek için kullanışlıdır.

## `tls-status` Komutunun Kullanımı

`tls-status` komutu, ***digna*** CLI'da belirli bir tarihte bir proje içindeki bir tablo için Trafik Işıkları Sistemi (TLS) durumunu sorgulamak için kullanılır. Trafik Işıkları Sistemi, verinin sağlığı ve kalitesi hakkında bilgi sağlar; dikkat gerektiren sorunları veya uyarıları gösterir.
  
#### Komut Kullanımı
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argümanlar
  
- **PROJECT_NAME**: TLS durumu sorgulanan proje adı (zorunlu).
- **TABLE_NAME**: TLS durumu alınacak proje içindeki tablo adı (zorunlu).
- **DATE**: TLS durumunun sorgulanacağı tarih; genellikle %Y-%m-%d formatında (zorunlu).
  
#### Örnek
  
`ProjectA` projesinde `UserData` adlı tablonun 1 Temmuz 2024 tarihindeki TLS durumunu kontrol etmek için:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Bu komut, önceden tanımlanmış kriterlere dayanarak verinin kalitesi hakkında net ve uygulanabilir bir durum raporu sağlayarak kullanıcıların veri kalitesini izlemelerine yardımcı olur.

## `inspect-async` Komutunun Kullanımı

`inspect-async` komutu, ***digna*** CLI'da backend'e belirtilen proje için bir veya daha fazla veri kaynağının incelemesini asenkron olarak gerçekleştirmesini talep etmek için kullanılır. project_name all-projects olarak ayarlanırsa, inceleme mevcut tüm projeler üzerinde yineleme yapar. Komut, incelemenin ilerlemesini takip etmek için kullanılabilecek bir istek kimliği (request id) döndürür.

#### Komut Kullanımı

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argümanlar
  
- **PROJECT_NAME**: İncelemeye tabi tutulacak proje adı (zorunlu). all-projects anahtar kelimesi kullanıldığında ***digna*** mevcut tüm projeler üzerinde yineleme yapar.
- **FROM_DATE**: İncelemenin başlangıç tarih ve zamanı. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (zorunlu).
- **TO_DATE**: İncelemenin bitiş tarih ve zamanı; FROM_DATE ile aynı formatları kabul eder (zorunlu).
  
#### Seçenekler

- `--table-name`, `-tn`: İncelemeyi projedeki belirli bir tabloyla sınırlar.
- `--table-filter`, `-tf`: İsimlerinde belirtilen alt dizeyi içeren tabloları incelemek için filtre uygular.

  
#### Örnek
  
`ProjectA` projesi için 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verilerin asenkron olarak incelenmesini talep etmek için:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## `inspect-status` Komutunun Kullanımı

`inspect-status` komutu, `inspect-async` ile başlatılan bir asenkron incelemenin ilerlemesini istek kimliğine (request ID) göre kontrol etmek için kullanılır.

#### Komut Kullanımı

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argümanlar
  
- **REQUEST_ID**: `inspect-async` komutu tarafından döndürülen istek kimliği.
  
#### Seçenekler

- `--report_level`, `-rl`: Rapor seviyesini ayarlar: 'task' veya 'step' [varsayılan: task]
  
#### Örnek
  
İstek kimliği 12345 olan bir incelemenin ayrıntılı adım (step) seviyesindeki ilerlemesini kontrol etmek için:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## `export-ds` Komutunun Kullanımı

`export-ds` komutu, ***digna*** CLI'da repository'den veri kaynaklarının dışa aktarımını oluşturmak için kullanılır. Varsayılan olarak, belirtilen bir projedeki tüm veri kaynakları dışa aktarılır.

#### Komut Kullanımı
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının dışa aktarılacağı proje adı.

#### Seçenekler

- `--table_name`, `-tn`: Projedeki belirli bir veri kaynağını dışa aktarmak için.
- `--exportfile`, `-ef`: Dışa aktarım için dosya adını belirtir.
    
#### Örnek
  
`ProjectA` projesindeki tüm veri kaynaklarını dışa aktarmak için:
  
```bash
dignacli export-ds ProjectA
```
  
Bu komut, `ProjectA` içindeki tüm veri kaynaklarını başka bir proje veya ***digna*** repository'sine aktarılabilecek JSON dokümanı olarak dışa aktarır.


## `import-ds` Komutunun Kullanımı

`import-ds` komutu, ***digna*** CLI'da veri kaynaklarını hedef bir projeye içe aktarmak ve bir içe aktarım raporu oluşturmak için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının içe aktarılacağı proje adı.
- **EXPORT_FILE**: İçe aktarılacak veri kaynakları dışa aktarım dosyasının adı.

#### Seçenekler

- `--output-file`, `-o`: İçe aktarım raporunun kaydedileceği dosya (belirtilmezse, terminalde tablo halinde yazdırılır).
- `--output-format`, `-f`: İçe aktarım raporunun kaydedileceği format (json, csv).
    
#### Örnek
  
`my_export.json` dışa aktarım dosyasındaki tüm veri kaynaklarını `ProjectB` içine aktarmak için:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
İçe aktarmadan sonra, bu komut ayrıca içe aktarılan ve atlanan nesnelerin bir raporunu gösterir. Yalnızca yeni veri kaynakları `ProjectB`'ye aktarılır. Hangi nesnelerin içe aktarılacağını ve hangilerinin atlanacağını görmek için `plan-import-ds` komutunu kullanabilirsiniz.

## `plan-import-ds` Komutunun Kullanımı

`plan-import-ds` komutu, ***digna*** CLI'da hedef projeye veri kaynakları içe aktarılmadan önce hangi nesnelerin içe aktarılacağını ve hangilerinin atlanacağını analiz etmek için kullanılır.

#### Komut Kullanımı
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının içe aktarılacağı proje adı.
- **EXPORT_FILE**: İçe aktarım öncesi analiz edilecek dışa aktarım dosyasının adı.

#### Seçenekler

- `--output-file`, `-o`: İçe aktarım plan raporunun kaydedileceği dosya (belirtilmezse, terminalde tablo halinde yazdırılır).
- `--output-format`, `-f`: Plan raporunun kaydedileceği format (json, csv).
    
#### Örnek
  
`my_export.json` dışa aktarım dosyasından `ProjectB`'ye aktarılacak ve atlanacak veri kaynaklarını kontrol etmek için:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Bu komut yalnızca içe aktarılacak ve atlanacak nesnelerin bir planını gösterir.