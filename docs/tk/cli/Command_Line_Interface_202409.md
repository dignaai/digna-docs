---
title: digna CLI Referansı 2024.09 – Komutlar ve Örnekler | digna Dokümantasyonu
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

--help seçeneği, kullanılabilir komutlar ve bunların kullanımı hakkında bilgi sağlar. Bu seçeneğin iki ana kullanım yolu vardır:

1. **Genel Yardımı Görüntüleme:**
   
    --help'i ***digna*** komutundan hemen sonra kullanın  
   bash
   dignacli --help

3.  **Belirli Komutlar İçin Yardım Alma:**  
  
    Belirli bir komut hakkında ayrıntılı bilgi almak için o komuta --help ekleyin.  
    Örneğin, add-user komutu hakkında yardım almak için şu komutu çalıştırın:
     bash
     dignacli add-user --help
     

     ### çıktı:
      
     - **Komut Açıklaması:** Komutun ne yaptığını detaylı olarak açıklar.  
     - **Sözdizimi:** Gerekli ve isteğe bağlı argümanlar dahil olmak üzere tam sözdizimini gösterir.  
     - **Seçenekler:** Komuta özgü seçenekleri ve açıklamalarını listeler.  
     - **Örnekler:** Komutun nasıl etkili şekilde çalıştırılacağını gösteren örnekler sağlar.

  
###   check-repo-connection

check-repo-connection komutu, belirli bir ***digna*** deposuna bağlantı ve erişimi test etmek için tasarlanmış ***digna*** CLI aracındaki bir yardımcı programdır. Bu komut, CLI'nın depoyla etkileşime geçebildiğini doğrular.
      
##### Komut Kullanımı
bash
dignacli check-repo-connection


Başarılı yürütme durumunda komut, bağlantının onayını ve depo ile ilgili bilgileri çıktı olarak verir: Repository version, Host, Database ve Schema.  
  
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
  
Varsayılan olarak, ***digna*** komutlarının konsol çıktısı minimalist olacak şekilde tasarlanmıştır. Çoğu komut, aşağıdaki seçenekleri kullanarak ek bilgi sağlamayı destekler:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” ve “debug” detay seviyesini belirlerken, “logfile” anahtarı çıktıyı konsol penceresi yerine bir dosyaya yönlendirmeyi sağlar.

## Kullanıcı Yönetimi

###   add-user
  
add-user komutu, ***digna*** CLI içinde yeni bir kullanıcıyı ***digna*** sistemine eklemek için kullanılır.
  
#### Komut Kullanımı
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argümanlar

- **USER_NAME**: Yeni kullanıcının kullanıcı adı (zorunlu).
- **USER_FULL_NAME**: Yeni kullanıcının tam adı (zorunlu).
- **USER_PASSWORD**: Yeni kullanıcının parolası (zorunlu).

#### Seçenekler

- --is_superuser, -su: Yeni kullanıcıyı yönetici (superuser) olarak belirlemek için bayrak.
- --valid_until, -vu: Kullanıcı hesabı için YYYY-MM-DD HH:MI:SS formatında bir sona erme tarihi belirler. Ayarlanmamışsa, hesabın bir sona erme tarihi yoktur.

#### Örnek

jdoe kullanıcı adı, John Doe tam adı ve password123 parolasıyla yeni bir kullanıcı eklemek için:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Bir kullanıcı ekleyip hesap sona erme tarihi ayarlamak için:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
delete-user komutu, ***digna*** CLI içinde mevcut bir kullanıcıyı ***digna*** sisteminden kaldırmak için kullanılır.
  
##### Komut Kullanımı
bash
dignacli delete-user USER_NAME

  
#### Argümanlar
- **USER_NAME**: Silinecek kullanıcının kullanıcı adı (zorunlu). Bu komutun gerektirdiği tek argümandır.

#### Örnek
bash
dignacli delete-user jdoe

  
Bu komut çalıştırıldığında, jdoe kullanıcısı ***digna*** sisteminden kaldırılacak, erişimi iptal edilecek ve depodaki ilişkili veri ve izinleri silinecektir.

###   modify-user

modify-user komutu, ***digna*** CLI içinde mevcut bir kullanıcının bilgilerini güncellemek için kullanılır.

##### Komut Kullanımı
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argümanlar
  
- **USER_NAME**: Bilgileri değiştirilecek kullanıcının kullanıcı adı (zorunlu).
- **USER_FULL_NAME**: Kullanıcı için yeni tam ad (zorunlu).
  
#### Seçenekler  
  
- --is_superuser, -su: Kullanıcıyı superuser olarak ayarlar ve yükseltilmiş ayrıcalıklar verir. Bu bayrağın değere ihtiyacı yoktur.  
- --valid_until, -vu: Kullanıcı hesabı için YYYY-MM-DD HH:MI:SS formatında bir sona erme tarihi belirler. Verilmezse hesap süresiz geçerli kalır.  
  
#### Örnek
  
jdoe kullanıcısının tam adını “Johnathan Doe” olarak değiştirmek ve kullanıcıyı superuser yapmak için:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
modify-user-pwd komutu, ***digna*** CLI içinde mevcut bir kullanıcının parolasını değiştirmek için kullanılır.
  
##### Komut Kullanımı
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argümanlar
  
- **USER_NAME**: Parolası değiştirilecek kullanıcının kullanıcı adı (zorunlu).
- **USER_PWD**: Kullanıcı için yeni parola (zorunlu).
  
#### Örnek
  
jdoe kullanıcısının parolasını newpassword123 olarak değiştirmek için:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

list-users komutu, ***digna*** CLI içinde ***digna*** sistemine kayıtlı tüm kullanıcıların listesini görüntüler.

##### Komut Kullanımı

bash
dignacli list-users


Bu komutu ***digna*** CLI'da çalıştırmak, ***digna*** deposuna bağlanarak tüm kullanıcıları listeler ve bunların ID'si, kullanıcı adı, tam adı, superuser durumu ve sona erme zaman damgalarını gösterir.

# Depo Yönetimi

###   upgrade-repo
  
upgrade-repo komutu, ***digna*** CLI içinde ***digna*** deposunu yükseltmek veya başlatmak için kullanılır. Bu komut, güncellemeleri uygulamak veya depo altyapısını ilk kez kurmak için gereklidir.
  
#### Komut Kullanımı

bash
dignacli upgrade-repo [options]

  
#### Seçenekler
  
- --simulation-mode, -s: Etkinleştirildiğinde komutu simülasyon modunda çalıştırır; yürütülecek SQL ifadelerini yazdırır ancak gerçekte çalıştırmaz. Bu, depoda değişiklik yapmadan değişiklikleri önizlemek için kullanışlıdır.  

  
#### Örnek
  
***digna*** deposunu yükseltmek için seçenek olmadan komutu çalıştırabilirsiniz:
  
bash
dignacli upgrade-repo
  
Yükseltmeyi simülasyon modunda çalıştırmak (SQL ifadelerini uygulamadan görmek) için:
  
bash
dignacli upgrade-repo --simulation-mode

  
Bu komut, veritabanı şeması ve diğer depo bileşenlerinin yazılımın en son sürümüyle uyumlu ve güncel olmasını sağlayarak ***digna*** sisteminin bakımında kritik öneme sahiptir.

###   encrypt
  
encrypt komutu, ***digna*** CLI içinde bir parolayı şifrelemek için kullanılır.
  
#### Komut Kullanımı
  
bash
dignacli encrypt <PASSWORD>

    
#### Argümanlar
- **PASSWORD**: Şifrelenmesi gereken parola (zorunlu).
  
#### Örnek
  
Bir parolayı şifrelemek için parolayı argüman olarak vermeniz gerekir.   
Örneğin, mypassword123 parolasını şifrelemek için:
bash
dignacli encrypt mypassword123

Bu komut, verilen parolanın şifrelenmiş halini çıktılar; bu çıktı daha sonra güvenli bağlamlarda kullanılabilir. Parola argümanı sağlanmazsa, CLI eksik argümanı belirten bir hata gösterir.

###   generate-key
  
generate-key komutu, ***digna*** deposunda depolanan parolaların güvenliğini sağlamak için gerekli olan bir Fernet anahtarı oluşturmak için kullanılır.
  
#### Komut Kullanımı
bash
dignacli generate-key

  
## Veri Yönetimi

###   clean-up

clean-up komutu, ***digna*** CLI içinde belirli bir proje altındaki bir veya daha fazla veri kaynağı için profilleri, tahminleri ve Trafik Işıkları Sistemi (TLS) verilerini kaldırmak için kullanılır. Bu komut, veri yaşam döngüsü yönetimi için önemlidir ve eski veya gereksiz verilerin temizlenmesine yardımcı olarak düzenli ve verimli bir veri ortamı sağlar.

#### Komut Kullanımı

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argümanlar
  
- **PROJECT_NAME**: Verilerin kaldırılacağı projenin adı (zorunlu). Bu argümanda all-projects anahtar kelimesinin kullanılması, ***digna***'nın mevcut tüm projeler üzerinde yineleme yapmasını ve komutu uygulamasını sağlar.
- **FROM_DATE**: Veri kaldırma için başlangıç tarih ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (zorunlu).
- **TO_DATE**: Veri kaldırma için bitiş tarih ve saati, FROM_DATE ile aynı formatları takip eder (zorunlu).
  
#### Seçenekler
  
- --table-name, -tn: Temizleme işlemini proje içindeki belirli bir tabloyla sınırlamak için.
- --table-filter, -tf: İsimlerinde belirtilen alt dizeyi içeren tablolarla sınırlamak için filtre uygular.
- --timing, -tm: Temizleme işlemi tamamlandıktan sonra süre bilgisini gösterir.
- --help: clean-up komutu için yardım bilgisi gösterir ve çıkar.
  
#### Örnek
  
ProjectA projesinden 1 Ocak 2023 ile 30 Haziran 2023 arasındaki verileri kaldırmak için:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Sadece Table1 adlı belirli bir tablodan veri kaldırmak için:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Bu komut, veri depolamayı yönetmeye ve deponun yalnızca ilgili bilgileri içermesini sağlamaya yardımcı olur.

###   inspect

inspect komutu, ***digna*** CLI içinde belirli bir proje altındaki bir veya daha fazla veri kaynağı için profiller, tahminler ve Trafik Işıkları Sistemi (TLS) verileri oluşturmak için kullanılır. Bu komut, belirli bir dönem boyunca verilerin analiz edilmesine ve izlenmesine yardımcı olur.

#### Komut Kullanımı

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argümanlar
  
- **PROJECT_NAME**: Verilerin inceleneceği projenin adı (zorunlu). Bu argümanda all-projects anahtar kelimesinin kullanılması, ***digna***'nın mevcut tüm projeler üzerinde yineleme yapmasını ve komutu uygulamasını sağlar.
- **FROM_DATE**: Veri incelemesi için başlangıç tarih ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S (zorunlu).
- **TO_DATE**: Veri incelemesi için bitiş tarih ve saati, FROM_DATE ile aynı formatları takip eder (zorunlu).
  
#### Seçenekler

- --table-name, -tn: İncelemeyi proje içindeki belirli bir tabloyla sınırlamak için.
- --table-filter, -tf: İsimlerinde belirtilen alt dizeyi içeren tablolara yönelik inceleme yapmak için filtre uygular.
- --force-profile: Profillerin yeniden toplanmasını zorlar. Varsayılan ayar force-profile'dır.
- --no-force-profile: Profillerin yeniden toplanmasını engeller.
- --force-prediction: Tahminlerin yeniden hesaplanmasını zorlar. Varsayılan ayar force-prediction'dır.
- --no-force-prediction: Tahminlerin yeniden hesaplanmasını engeller.
- --force-alert-status: Uyarı durumlarının yeniden hesaplanmasını zorlar. Varsayılan ayar force-alert-status'dur.
- --no-force-alert-status: Uyarı durumlarının yeniden hesaplanmasını engeller.
- --timing, -tm: İnceleme işlemi tamamlandıktan sonra süre bilgisini gösterir.
- --alert-notification, -an: Abone olunan kanallara uyarı bildirimleri gönderir.
  
#### Örnek
  
ProjectA projesi için 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri incelemek için:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Sadece belirli bir tabloyu incelemek ve tahminlerin yeniden hesaplanmasını zorlamak için:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Bu komut, güncellenmiş profiller ve tahminler oluşturmak, veri bütünlüğünü izlemek ve belirli bir proje zaman aralığında uyarı sistemlerini yönetmek için kullanışlıdır.

###   tls-status

tls-status komutu, ***digna*** CLI içinde belirli bir proje altındaki bir tablonun belirli bir tarihteki Trafik Işıkları Sistemi (TLS) durumunu sorgulamak için kullanılır. Trafik Işıkları Sistemi, verinin sağlığı ve kalitesi hakkında uyarı veya dikkat gerektiren durumları gösterir.
  
#### Komut Kullanımı
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Argümanlar
  
- **PROJECT_NAME**: TLS durumu sorgulanan projenin adı (zorunlu).
- **TABLE_NAME**: TLS durumu gereken proje içindeki belirli tablo (zorunlu).
- **DATE**: TLS durumunun sorgulandığı tarih, genellikle %Y-%m-%d formatında (zorunlu).
  
#### Örnek
  
ProjectA projesinde UserData adlı tablonun 1 Temmuz 2024 tarihindeki TLS durumunu kontrol etmek için:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Bu komut, önceden tanımlanmış kriterlere dayalı olarak açık ve uygulanabilir bir durum raporu sağlayarak kullanıcıların veri kalitesini izlemesine ve sürdürmesine yardımcı olur.

###   list-projects
  
list-projects komutu, ***digna*** CLI içinde mevcut tüm projelerin listesini görüntülemek için kullanılır.
  
#### Komut Kullanımı
  
bash
dignacli list-projects


Bu komut, birden çok projeyi yöneten yöneticiler ve kullanıcılar için özellikle faydalıdır; ***digna*** deposunda mevcut projelere hızlı bir genel bakış sağlar.

###   list-ds

list-ds komutu, ***digna*** CLI içinde belirli bir proje altındaki mevcut tüm veri kaynaklarının listesini görüntülemek için kullanılır. Bu komut, ***digna*** sistemindeki analiz ve yönetim için mevcut veri varlıklarını anlamada yararlıdır.

#### Komut Kullanımı
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının listelendiği projenin adı (zorunlu).
  
#### Örnek
  
ProjectA adlı projedeki tüm veri kaynaklarını listelemek için:
  
bash
dignacli list-ds ProjectA

  
Bu komut, bir projedeki mevcut veri kaynaklarına genel bir bakış sağlayarak kullanıcıların veri ortamını daha etkili yönetmesine yardımcı olur.