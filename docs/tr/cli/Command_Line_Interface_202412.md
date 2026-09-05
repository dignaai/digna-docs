---
title: digna CLI Referansı 2024.12 – Komutlar ve Örnekler | digna Dokümantasyonu
description: digna CLI sürümü 2024.12 için eksiksiz referans. add-user, check-repo-connection, upgrade-repo, inspect ve diğer komutlarla kullanıcıları, repository'leri ve veriyi nasıl yöneteceğinizi öğrenin.
image: /assets/logo_square.png
---


# digna CLI Referansı 2024.12
**2024-12-09**

Bu sayfa, ***digna*** CLI sürümü **2024.12**'de kullanılabilir tüm komutları, kullanım örneklerini ve seçeneklerini belgelemektedir.

---


**2024-12-09**


---

## CLI Temelleri

---

## `help` Seçeneğinin Kullanımı

`--help` seçeneği, kullanılabilir komutlar ve bunların kullanımı hakkında bilgi sağlar. Bu seçeneği kullanmanın iki ana yolu vardır:

1. **Genel Yardımı Görüntüleme:**
   
    `--help` öğesini ***digna*** anahtar kelimesinden hemen sonra kullanın  
   ```bash
   dignacli --help
   ```

3.  **Belirli Komutlar İçin Yardım Alma:**  
  
    Belirli bir komut hakkında ayrıntılı bilgi almak için o komuta `--help` ekleyin.  
    Örneğin, `add-user` komutu için yardım almak amacıyla şu komutu çalıştırın:
     ```bash
     dignacli add-user --help
     ```

     ### çıktı:
      
     - **Komut Açıklaması:** Komutun ne yaptığını detaylı şekilde açıklar.  
     - **Sözdizimi:** Gerekli ve isteğe bağlı argümanlar dahil olmak üzere tam sözdizimini gösterir.  
     - **Seçenekler:** Komuta özgü tüm seçenekleri ve açıklamalarını listeler.  
     - **Örnekler:** Komutun etkili şekilde nasıl çalıştırılacağına dair örnekler sağlar.

  
## `check-repo-connection` Komutunun Kullanımı

check-repo-connection komutu, ***digna*** CLI aracında belirlenen bir ***digna*** repository'sine erişim ve bağlantıyı test etmek için kullanılan bir yardımcı komuttur. Bu komut, CLI'nin repository ile etkileşime girebildiğini doğrular.
      
### Komut Kullanımı
```bash
dignacli check-repo-connection
```

Başarılı yürütme halinde, komut bağlantı onayını ve repository ile ilgili bilgileri (Repository versiyonu, Host, Database ve Schema) çıktı olarak verir.  
  
Eğer repository bağlantısı başarılı değilse, config.toml dosyasındaki yapılandırma ayarlarını kontrol edin.

## ‘version’ Komutunun Kullanımı

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
  
Varsayılan olarak, ***digna*** komutlarının konsol çıktısı minimal tutulmuştur. Çoğu komut, aşağıdaki seçenekleri kullanarak ek bilgi sağlamaya olanak tanır:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” ve “debug” ayrıntı düzeyini tanımlarken, “logfile” anahtarı çıktının konsol yerine bir dosyaya yönlendirilmesine olanak tanır.

# Kullanıcı Yönetimi

## `add-user` Komutunun Kullanımı
  
add-user komutu, ***digna*** CLI'de sisteme yeni bir kullanıcı eklemek için kullanılır.
  
### Komut Kullanımı
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argümanlar

- **USER_NAME**: Yeni kullanıcı için kullanıcı adı (zorunlu).
- **USER_FULL_NAME**: Yeni kullanıcının tam adı (zorunlu).
- **USER_PASSWORD**: Yeni kullanıcı için parola (zorunlu).

### Seçenekler

- `--is_superuser`, `-su`: Yeni kullanıcıyı yönetici olarak tanımlamak için bayrak.
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir son kullanma tarihi belirler. Belirtilmezse, hesabın bir son kullanma tarihi yoktur.

### Örnek

Kullanıcı adı `jdoe`, tam adı `John Doe` ve parolası `password123` olan yeni bir kullanıcı eklemek için:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Bir kullanıcı ekleyip hesap son kullanma tarihi ayarlamak için:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## `delete-user` Komutunun Kullanımı
  
`delete-user` komutu, ***digna*** CLI'de mevcut bir kullanıcıyı sistemden kaldırmak için kullanılır.
  
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
  
Bu komut çalıştırıldığında `jdoe` kullanıcısı ***digna*** sisteminden kaldırılacak, erişimi iptal edilecek ve repository'deki ilişkili veri ve izinleri silinecektir.

## `modify-user` Komutunun Kullanımı

`modify-user` komutu, ***digna*** CLI'de mevcut bir kullanıcının bilgilerini güncellemek için kullanılır.

### Komut Kullanımı
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argümanlar
  
- **USER_NAME**: Güncellenecek kullanıcının kullanıcı adı (zorunlu).
- **USER_FULL_NAME**: Kullanıcı için yeni tam ad (zorunlu).
  
### Seçenekler  
  
- `--is_superuser`, `-su`: Kullanıcıyı süper kullanıcı olarak ayarlar; yükseltilmiş ayrıcalık tanır. Bu bayrak değer gerektirmez.  
- `--valid_until`, `-vu`: Kullanıcı hesabı için `YYYY-MM-DD HH:MI:SS` formatında bir son kullanma tarihi belirler. Belirtilmezse, hesap süresiz geçerli kalır.  
  
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

`list-users` komutu, ***digna*** CLI'de kayıtlı tüm kullanıcıları listelemek için kullanılır.

### Komut Kullanımı

```bash
dignacli list-users
```

Bu komut çalıştırıldığında, ***digna*** repository'sine bağlanır ve tüm kullanıcıları ID, kullanıcı adı, tam ad, süper kullanıcı durumu ve son geçerlilik zaman damgaları ile birlikte listeler.

# Repository Yönetimi

### `upgrade-repo` Komutunun Kullanımı
  
`upgrade-repo` komutu, ***digna*** CLI'de repository'yi yükseltmek veya başlatmak için kullanılır. Bu komut, güncellemeleri uygulamak veya repository altyapısını ilk kez kurmak için gereklidir.
  
### Komut Kullanımı

```bash
dignacli upgrade-repo [options]
```
  
### Seçenekler
  
- `--simulation-mode`, `-s`: Etkinleştirildiğinde komutu simülasyon modunda çalıştırır; yürütülecek SQL ifadelerini yazdırır ancak bunları gerçekten çalıştırmaz. Değişiklikleri uygulamadan önizleme yapmak için yararlıdır.  

  
### Örnek
  
***digna*** repository'sini yükseltmek için komutu herhangi bir seçenek olmadan çalıştırabilirsiniz:
  
```bash
dignacli upgrade-repo
```  
Yükseltmeyi simülasyon modunda çalıştırmak (SQL ifadelerini uygulamadan görmek) için:
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Bu komut, ***digna*** sisteminin bakımında kritik öneme sahiptir; veritabanı şemasının ve diğer repository bileşenlerinin yazılımın en son sürümüyle uyumlu olmasını sağlar.

## `encrypt` Komutunun Kullanımı
  
`encrypt` komutu, ***digna*** CLI'de bir parolayı şifrelemek için kullanılır.
  
### Komut Kullanımı
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argümanlar
- **PASSWORD**: Şifrelenmesi gereken parola (zorunlu).
  
### Örnek
  
Bir parolayı şifrelemek için parola argümanını sağlamanız gerekir.  
Örneğin, `mypassword123` parolasını şifrelemek için:
```bash
dignacli encrypt mypassword123
```
Bu komut sağlanan parolanın şifrelenmiş halini çıktı olarak verir; bu çıktı daha sonra güvenli ortamlarda kullanılabilir. Parola argümanı sağlanmazsa, CLI eksik argüman hatası gösterecektir.

## `generate-key` Komutunun Kullanımı
  
`generate-key` komutu, ***digna*** repository'sinde saklanan parolaları güvence altına almak için gerekli olan bir Fernet anahtarı oluşturmak için kullanılır.
  
### Komut Kullanımı
```bash
dignacli generate-key
```
  
# Veri Yönetimi

## `clean-up` Komutunun Kullanımı

`clean-up` komutu, ***digna*** CLI'de belirtilen bir projedeki bir veya daha fazla veri kaynağı için profilleri, tahminleri ve Trafik Işık Sistemi verilerini (Traffic Light System, TLS) silmek için kullanılır. Bu komut, veri yaşam döngüsü yönetimi açısından önemlidir; güncel olmayan veya gereksiz verileri temizleyerek düzenli ve verimli bir veri ortamı sağlar.

### Komut Kullanımı

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argümanlar
  
- **PROJECT_NAME**: Verinin silineceği projenin adı (zorunlu). Bu argümanda all-projects anahtar kelimesinin kullanılması, ***digna***'nın mevcut tüm projeler üzerinde yineleme yapmasını ve komutu uygulamasını sağlar.
- **FROM_DATE**: Veri silme işlemine başlama tarihi ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (zorunlu).
- **TO_DATE**: Veri silme işlemine bitiş tarihi ve saati; FROM_DATE ile aynı formatları kullanır (zorunlu).
  
### Seçenekler
  
- `--table-name`, `-tn`: Temizleme işlemini proje içindeki belirli bir tabloyla sınırlar.
- `--table-filter`, `-tf`: Tablo adlarında belirtilen alt diziyi içeren tablolarla sınırlamak için filtre uygular.
- `--timing`, `-tm`: İşlem tamamlandıktan sonra temizleme süresini gösterir.
- `--help`: clean-up komutu için yardım bilgilerini görüntüler ve çıkış yapar.
  
### Örnek
  
ProjectA projesinden 1 Ocak 2023 ile 30 Haziran 2023 arasındaki verileri silmek için:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Sadece `Table1` adlı belirli bir tablodan veri silmek için:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Bu komut, veri depolamayı yönetmeye ve repository'nin yalnızca ilgili bilgileri içermesini sağlamaya yardımcı olur.

## `inspect` Komutunun Kullanımı

`inspect` komutu, ***digna*** CLI'de belirtilen bir proje içindeki bir veya daha fazla veri kaynağı için profiller, tahminler ve Trafik Işık Sistemi verileri oluşturmak için kullanılır. Bu komut, belirli bir dönem için veri analizine ve izlemeye yardımcı olur.

### Komut Kullanımı

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argümanlar
  
- **PROJECT_NAME**: İnceleme yapılacak projenin adı (zorunlu). Bu argümanda all-projects anahtar kelimesinin kullanılması, ***digna***'nın mevcut tüm projeler üzerinde yineleme yapmasını ve komutu uygulamasını sağlar.
- **FROM_DATE**: Veri incelemesine başlama tarihi ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (zorunlu).
- **TO_DATE**: Veri incelemesinin bitiş tarihi ve saati; FROM_DATE ile aynı formatları kullanır (zorunlu).
  
### Seçenekler

- `--table-name`, `-tn`: İncelemeyi proje içindeki belirli bir tabloyla sınırlar.
- `--table-filter`, `-tf`: Adında belirtilen alt diziyi içeren tabloları incelemek için filtre uygular.
- `--do-profile`: Profillerin yeniden toplanmasını tetikler. Varsayılan olarak do-profile etkindir.
- `--no-do-profile`: Profillerin yeniden toplanmasını engeller.
- `--do-prediction`: Tahminlerin yeniden hesaplanmasını tetikler. Varsayılan olarak do-prediction etkindir.
- `--no-do-prediction`: Tahminlerin yeniden hesaplanmasını engeller.
- `--do-alert-status`: Uyarı durumlarının yeniden hesaplanmasını tetikler. Varsayılan olarak do-alert-status etkindir.
- `--no-do-alert-status`: Uyarı durumlarının yeniden hesaplanmasını engeller.
- `--iterative`: Belirtilen dönemin günlük yinelemelerle incelenmesini tetikler. Varsayılan olarak iterative etkindir.
- `--no-iterative`: Tüm dönemin tek seferde incelenmesini tetikler.
- `--timing`, `-tm`: İnceleme işlemi tamamlandıktan sonra süresini gösterir.
  
### Örnek
  
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

`tls-status` komutu, ***digna*** CLI'de belirli bir proje içindeki bir tablonun belirli bir tarihteki Traffic Light System (TLS) durumunu sorgulamak için kullanılır. Trafik Işık Sistemi, verinin sağlığı ve kalitesi hakkında içgörü sağlar; dikkat edilmesi gereken sorunlar veya uyarılar hakkında bilgi verir.
  
### Komut Kullanımı
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argümanlar
  
- **PROJECT_NAME**: TLS durumu sorgulanan projenin adı (zorunlu).
- **TABLE_NAME**: TLS durumu istenen proje içindeki belirli tablo (zorunlu).
- **DATE**: TLS durumunun sorgulandığı tarih, genellikle %Y-%m-%d formatında (zorunlu).
  
### Örnek
  
`ProjectA` projesinde `UserData` adlı tablonun 1 Temmuz 2024 tarihindeki TLS durumunu kontrol etmek için:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Bu komut, önceden tanımlanmış kriterlere dayalı olarak açık ve uygulanabilir bir durum raporu sağlayarak kullanıcıların veri kalitesini izlemelerine ve sürdürmelerine yardımcı olur.

## `list-projects` Komutunun Kullanımı
  
`list-projects` komutu, ***digna*** CLI'de mevcut tüm projelerin bir listesini görüntülemek için kullanılır.
  
### Komut Kullanımı
  
```bash
dignacli list-projects
```

Bu komut, birden fazla projeyi yöneten yöneticiler ve kullanıcılar için özellikle faydalıdır; ***digna*** repository'sindeki kullanılabilir projelerin hızlı bir özetini sağlar.

## `list-ds` Komutunun Kullanımı

`list-ds` komutu, ***digna*** CLI'de belirtilen bir proje içindeki mevcut tüm veri kaynaklarının bir listesini görüntülemek için kullanılır. Bu komut, ***digna*** sisteminde analiz ve yönetim için hangi veri varlıklarının mevcut olduğunu anlamaya yardımcı olur.

### Komut Kullanımı
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının listelendiği projenin adı (zorunlu).
  
### Örnek
  
`ProjectA` adlı projedeki tüm veri kaynaklarını listelemek için:
  
```bash
dignacli list-ds ProjectA
```
  
Bu komut, bir projede mevcut olan veri kaynakları hakkında kullanıcıya genel bir bakış sağlar ve veri ortamını daha etkili yönetmelerine yardımcı olur.