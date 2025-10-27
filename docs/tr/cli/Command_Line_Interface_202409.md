---
title: digna CLI Referansı 2024.09 – Komutlar & Örnekler | digna Belgeleri
description: digna CLI sürümü 2024.09 için eksiksiz referans. add-user, check-repo-connection, upgrade-repo, inspect, tls-status ve daha fazlası gibi komutlarla kullanıcıları, depoları ve verileri nasıl yöneteceğinizi öğrenin.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202408/
image: /assets/logo_square.png
---

# digna CLI Referansı 2024.09
**2024-08-24**

---

## CLI Temelleri

---

###   help

--help seçeneği, kullanılabilir komutlar ve bunların kullanımı hakkında bilgi sağlar. Bu seçeneğin kullanılmasının iki temel yolu vardır:

1. **Genel Yardımı Görüntüleme:**
   
    --help'i ***digna*** komutunun hemen ardından kullanın  
   bash
   dignacli --help

3.  **Belirli Komutlar İçin Yardım Alma:**  
  
    Belirli bir komut hakkında detaylı bilgi almak için o komuta --help ekleyin.
    Örneğin, add-user komutu için yardım almak istiyorsanız çalıştırın:
     bash
     dignacli add-user --help
     

     ### çıktı:
      
     - **Komut Açıklaması:** Komutun ne yaptığını ayrıntılı olarak açıklar.  
     - **Sözdizimi:** Gerekli ve isteğe bağlı argümanlar dahil olmak üzere tam sözdizimini gösterir.  
     - **Seçenekler:** Komuta özgü seçenekleri ve açıklamalarını listeler.  
     - **Örnekler:** Komutun nasıl etkili şekilde çalıştırılacağına dair örnekler sağlar.

  
###   check-repo-connection

check-repo-connection komutu, ***digna*** CLI aracında belirtilen bir ***digna*** deposuna (repository) erişim ve bağlantıyı test etmek için kullanılan bir yardımcı programdır. Bu komut, CLI'nın depoyla etkileşime geçebildiğini doğrular.
      
##### Komut Kullanımı
bash
dignacli check-repo-connection


Başarılı bir yürütme durumunda komut bağlantının doğrulandığını ve depo ile ilgili bilgileri (Repository version, Host, Database ve Schema) çıktılar.  
  
Eğer depo bağlantısı başarılı değilse, doğru yapılandırma ayarları için config.toml dosyasını kontrol edin.

###   version

Yüklü *dignacli* sürümünü kontrol etmek için --version seçeneğini kullanın.  
  
#### Komut Kullanımı
bash
dignacli --version

  
#### Örnek Çıktı
bash
dignacli version 2024.09


###   logging options
  
Varsayılan olarak, ***digna*** komutlarının konsol çıktısı minimal olacak şekilde tasarlanmıştır. Çoğu komut ek bilgi sağlama olanağı sunar; bunun için aşağıdaki seçenekler kullanılabilir:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” ve “debug” ayrıntı düzeyini tanımlar, “logfile” seçeneği ise çıktının konsol yerine bir dosyaya yönlendirilmesini sağlar.

## Kullanıcı Yönetimi

###   add-user
  
***digna*** CLI'deki add-user komutu, sisteme yeni bir kullanıcı eklemek için kullanılır.
  
#### Komut Kullanımı
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argümanlar

- **USER_NAME**: Yeni kullanıcı için kullanıcı adı (gereklidir).
- **USER_FULL_NAME**: Yeni kullanıcının tam adı (gereklidir).
- **USER_PASSWORD**: Yeni kullanıcı için parola (gereklidir).

#### Seçenekler

- --is_superuser, -su: Yeni kullanıcıyı yönetici (admin) olarak belirlemek için bayrak.
- --valid_until, -vu: Kullanıcı hesabı için YYYY-MM-DD HH:MI:SS formatında bir son kullanma tarihi ayarlar. Ayarlanmazsa hesapın bir son kullanma tarihi yoktur.

#### Örnek

jdoe kullanıcı adı, John Doe tam adı ve password123 parolası ile yeni bir kullanıcı eklemek için:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Hesap son kullanma tarihi belirleyerek yeni bir kullanıcı eklemek için:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
***digna*** CLI'deki delete-user komutu, mevcut bir kullanıcıyı ***digna*** sisteminden kaldırmak için kullanılır.
  
##### Komut Kullanımı
bash
dignacli delete-user USER_NAME

  
#### Argümanlar
- **USER_NAME**: Silinecek kullanıcının kullanıcı adı (gereklidir). Bu komutun gerektirdiği tek argümandır.

#### Örnek
bash
dignacli delete-user jdoe

  
Bu komut yürütüldüğünde jdoe kullanıcısı ***digna*** sisteminden kaldırılacak, erişimi iptal edilecek ve depodaki ilişkili verileri ile izinleri silinecektir.

###   modify-user

***digna*** CLI'deki modify-user komutu, mevcut bir kullanıcının bilgilerini güncellemek için kullanılır.

##### Komut Kullanımı
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argümanlar
  
- **USER_NAME**: Değiştirilecek kullanıcının kullanıcı adı (gereklidir).
- **USER_FULL_NAME**: Kullanıcı için yeni tam ad (gereklidir).
  
#### Seçenekler  
  
- --is_superuser, -su: Kullanıcıyı süper kullanıcı yapar ve yükseltilmiş yetkiler verir. Bu bayrak değer gerektirmez.  
- --valid_until, -vu: Kullanıcı hesabı için YYYY-MM-DD HH:MI:SS formatında bir son kullanma tarihi ayarlar. Sağlanmazsa hesap süresiz geçerli kalır.  
  
#### Örnek
  
jdoe kullanıcısının tam adını “Johnathan Doe” olarak değiştirmek ve kullanıcıyı süper kullanıcı yapmak için:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
***digna*** CLI'deki modify-user-pwd komutu, mevcut bir kullanıcının parolasını değiştirmek için kullanılır.
  
##### Komut Kullanımı
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argümanlar
  
- **USER_NAME**: Parolası değiştirilecek kullanıcının kullanıcı adı (gereklidir).
- **USER_PWD**: Kullanıcı için yeni parola (gereklidir).
  
#### Örnek
  
jdoe kullanıcısının parolasını newpassword123 olarak değiştirmek için:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

***digna*** CLI'deki list-users komutu, ***digna*** sistemine kayıtlı tüm kullanıcıların listesini gösterir.

##### Komut Kullanımı

bash
dignacli list-users


Bu komutu çalıştırmak, ***digna*** deposuna bağlanacak ve kullanıcıların ID'si, kullanıcı adı, tam adı, süper kullanıcı durumu ve son geçerlilik zaman damgalarını göstererek tüm kullanıcıları listeleyecektir.

# Depo Yönetimi

###   upgrade-repo
  
***digna*** CLI'deki upgrade-repo komutu, ***digna*** deposunu yükseltmek veya başlatmak için kullanılır. Bu komut, güncellemeleri uygulamak veya depoyu ilk kez kurmak için gereklidir.
  
#### Komut Kullanımı

bash
dignacli upgrade-repo [options]

  
#### Seçenekler
  
- --simulation-mode, -s: Etkinleştirildiğinde komut simülasyon modunda çalışır; yürütülecek SQL ifadelerini yazdırır ancak bunları gerçekten çalıştırmaz. Depoya değişiklik yapmadan değişiklikleri önizlemek için yararlıdır.  

  
#### Örnek
  
***digna*** deposunu yükseltmek için seçenek olmadan komutu çalıştırabilirsiniz:
  
bash
dignacli upgrade-repo
  
Yükseltmeyi simülasyon modunda çalıştırmak (SQL ifadelerini görüp uygulamamak) için:
  
bash
dignacli upgrade-repo --simulation-mode

  
Bu komut, veritabanı şeması ve diğer depo bileşenlerinin yazılımın en son sürümüyle güncel kalmasını sağlayarak ***digna*** sisteminin bakımında kritik öneme sahiptir.

###   encrypt
  
***digna*** CLI'deki encrypt komutu bir parolayı şifrelemek için kullanılır.
  
#### Komut Kullanımı
  
bash
dignacli encrypt <PASSWORD>

    
#### Argümanlar
- **PASSWORD**: Şifrelenmesi gereken parola (gereklidir).
  
#### Örnek
  
Bir parolayı şifrelemek için parolayı argüman olarak vermeniz gerekir.   
Örneğin, mypassword123 parolasını şifrelemek için:
bash
dignacli encrypt mypassword123

Bu komut, verilen parolanın şifrelenmiş halini çıktılar; bu çıktı daha sonra güvenli bağlamlarda kullanılabilir. Parola argümanı sağlanmazsa CLI eksik argümanı belirten bir hata gösterir.

###   generate-key
  
generate-key komutu, ***digna*** deposunda saklanan parolaları güvence altına almak için gerekli olan bir Fernet anahtarı (key) oluşturmak için kullanılır.
  
#### Komut Kullanımı
bash
dignacli generate-key

  
## Veri Yönetimi

###   clean-up

***digna*** CLI'deki clean-up komutu, belirli bir projedeki bir veya daha fazla veri kaynağı için profilleri, tahminleri ve Traffic Light System verilerini silmek için kullanılır. Bu komut veri yaşam döngüsü yönetimi için önemlidir; güncel olmayan veya gereksiz verileri temizleyerek düzenli ve verimli bir veri ortamının korunmasına yardımcı olur.

#### Komut Kullanımı

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argümanlar
  
- **PROJECT_NAME**: Verilerin kaldırılacağı projenin adı (gereklidir). Bu argümana all-projects anahtar kelimesi verildiğinde ***digna*** mevcut tüm projeler üzerinde yineleme yaparak bu komutu uygular.
- **FROM_DATE**: Verilerin silme başlangıç tarihi ve zamanı. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (gereklidir).
- **TO_DATE**: Verilerin silme bitiş tarihi ve zamanı; FROM_DATE ile aynı formatları takip eder (gereklidir).
  
#### Seçenekler
  
- --table-name, -tn: Temizleme işlemine yalnızca belirtilen bir tabloyla sınırlamak için.
- --table-filter, -tf: Tablo adlarında belirtilen alt dizeyi içeren tablolarla sınırlamak için filtre uygular.
- --timing, -tm: Temizleme işlemi tamamlandıktan sonra süre bilgisini gösterir.
- --help: clean-up komutu için yardım bilgilerini görüntüler ve çıkar.
  
#### Örnek
  
ProjectA projesinden 1 Ocak 2023 ile 30 Haziran 2023 arasındaki verileri kaldırmak için:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Sadece Table1 adlı belirli bir tablodan veri kaldırmak için:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Bu komut, veri depolamayı yönetmeye ve deponun yalnızca ilgili bilgileri içermesini sağlamaya yardımcı olur.

###   inspect

***digna*** CLI'deki inspect komutu, belirli bir projedeki bir veya daha fazla veri kaynağı için profiller, tahminler ve Traffic Light System verileri oluşturmak için kullanılır. Bu komut, belirli bir dönem içinde veri analizine ve izlemeye yardımcı olur.

#### Komut Kullanımı

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argümanlar
  
- **PROJECT_NAME**: İncelemenin yapılacağı projenin adı (gereklidir). Bu argümana all-projects anahtar kelimesi verildiğinde ***digna*** mevcut tüm projeler üzerinde yineleme yaparak bu komutu uygular.
- **FROM_DATE**: İncelemenin başlayacağı tarih ve zaman. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (gereklidir).
- **TO_DATE**: İncelemenin biteceği tarih ve zaman; FROM_DATE ile aynı formatları takip eder (gereklidir).
  
#### Seçenekler

- --table-name, -tn: İncelemeyi projenin belirli bir tablosuyla sınırlamak için.
- --table-filter, -tf: İsimlerinde belirtilen alt dizeyi içeren tabloları incelemek için filtre uygular.
- --force-profile: Profillerin yeniden toplanmasını zorlar. Varsayılan olarak force-profile'dır.
- --no-force-profile: Profillerin yeniden toplanmasını engeller.
- --force-prediction: Tahminlerin yeniden hesaplanmasını zorlar. Varsayılan olarak force-prediction'dır.
- --no-force-prediction: Tahminlerin yeniden hesaplanmasını engeller.
- --force-alert-status: Uyarı durumlarının yeniden hesaplanmasını zorlar. Varsayılan olarak force-alert-status'dur.
- --no-force-alert-status: Uyarı durumlarının yeniden hesaplanmasını engeller.
- --timing, -tm: İnceleme işlemi tamamlandıktan sonra süresini gösterir.
- --alert-notification, -an: Abone kanallara uyarı bildirimleri gönderir.
  
#### Örnek
  
ProjectA projesi için 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri incelemek için:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Sadece belirli bir tabloyu inceleyip tahminlerin yeniden hesaplanmasını zorlamak için:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Bu komut, güncellenmiş profiller ve tahminler oluşturmak, veri bütünlüğünü izlemek ve belirtilen proje zaman aralığı içinde uyarı sistemlerini yönetmek için kullanışlıdır.

###   tls-status

***digna*** CLI'deki tls-status komutu, belirli bir tarihte bir projedeki belirli bir tablo için Traffic Light System (TLS) durumunu sorgulamak için kullanılır. Traffic Light System, verinin sağlık ve kalite durumu hakkında bilgi sağlar ve dikkat gerektiren olası sorunları veya uyarıları gösterir.
  
#### Komut Kullanımı
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Argümanlar
  
- **PROJECT_NAME**: TLS durumunun sorgulandığı proje adı (gereklidir).
- **TABLE_NAME**: TLS durumunun gerektiği proje içindeki belirli tablo (gereklidir).
- **DATE**: TLS durumunun sorgulandığı tarih; genellikle %Y-%m-%d formatında verilir (gereklidir).
  
#### Örnek
  
ProjectA projesinde UserData adlı tablonun 1 Temmuz 2024 tarihindeki TLS durumunu kontrol etmek için:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Bu komut, önceden tanımlanmış kriterlere dayalı olarak net ve uygulanabilir bir durum raporu sağlayarak kullanıcıların veri kalitesini izlemelerine ve sürdürmelerine yardımcı olur.

###   list-projects
  
***digna*** CLI'deki list-projects komutu, ***digna*** sistemindeki tüm mevcut projelerin listesini görüntülemek için kullanılır.
  
#### Komut Kullanımı
  
bash
dignacli list-projects


Bu komut, birden çok proje yöneten yönetici ve kullanıcılar için özellikle faydalıdır; ***digna*** deposundaki mevcut projelerin hızlı bir özetini sağlar.

###   list-ds

***digna*** CLI'deki list-ds komutu, belirli bir proje içindeki tüm mevcut veri kaynaklarının (data sources) listesini görüntülemek için kullanılır. Bu komut, ***digna*** sisteminde analiz ve yönetim için mevcut veri varlıklarını anlamaya yardımcı olur.

#### Komut Kullanımı
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının listelendiği proje adı (gereklidir).
  
#### Örnek
  
ProjectA adlı projedeki tüm veri kaynaklarını listelemek için:
  
bash
dignacli list-ds ProjectA

  
Bu komut, bir projedeki kullanılabilir veri kaynaklarının genel bir görünümünü sağlar ve kullanıcıların veri ortamını daha etkili bir şekilde gezinmesine ve yönetmesine yardımcı olur.