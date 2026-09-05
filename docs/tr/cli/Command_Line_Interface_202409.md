---
title: digna CLI Başvuru 2024.09 – Komutlar & Örnekler | digna Belgeleri
description: digna CLI sürümü 2024.09 için eksiksiz başvuru. add-user, check-repo-connection, upgrade-repo, inspect, tls-status ve daha fazlası gibi komutlarla kullanıcıları, depoları ve veriyi nasıl yöneteceğinizi öğrenin.
image: /assets/logo_square.png
---

# digna CLI Başvuru 2024.09
**2024-08-24**

---

## CLI Temelleri

---

###   help

--help seçeneği kullanılabilir komutlar ve bunların kullanımı hakkında bilgi sağlar. Bu seçeneği kullanmanın iki ana yolu vardır:

1. **Genel Yardımı Görüntüleme:**
   
    --help seçeneğini ***digna*** kelimesinin hemen ardından kullanın.  
   bash
   dignacli --help

3.  **Belirli Komutlar İçin Yardım Alma:**  
  
    Belirli bir komut hakkında ayrıntılı bilgi almak için o komuta --help ekleyin.  
    Örneğin, add-user komutu ile ilgili yardım almak için şu komutu çalıştırın:
     bash
     dignacli add-user --help
     

     ### çıktı:
      
     - **Komut Açıklaması:** Komutun ne yaptığını detaylı şekilde açıklar.  
     - **Sözdizimi:** Gerekli ve isteğe bağlı argümanlar dahil olmak üzere doğru sözdizimini gösterir.  
     - **Seçenekler:** Komuta özgü seçenekleri ve bunların açıklamalarını listeler.  
     - **Örnekler:** Komutun nasıl etkili şekilde çalıştırılacağına dair örnekler sağlar.

  
###   check-repo-connection

check-repo-connection komutu, belirtilen bir ***digna*** deposuna bağlantı ve erişimi test etmek için ***digna*** CLI aracında bulunan bir yardımcı araçtır. Bu komut, CLI'nın depoyla etkileşim kurabildiğini doğrular.
      
##### Komut Kullanımı
bash
dignacli check-repo-connection


Başarılı yürütme durumunda, komut bağlantının onayını ve depoya ilişkin bilgileri görüntüler: Repository version, Host, Database ve Schema.  
  
Depo bağlantısı başarılı değilse, config.toml dosyasındaki yapılandırma ayarlarının doğru olduğundan emin olun.

###   version

Yüklü *dignacli* sürümünü kontrol etmek için --version seçeneğini kullanın.  
  
#### Komut Kullanımı
bash
dignacli --version

  
#### Örnek Çıktı
bash
dignacli version 2024.09


###   logging options
  
Varsayılan olarak, ***digna*** komutlarının konsol çıktısı minimalist olacak şekilde tasarlanmıştır. Çoğu komut aşağıdaki seçenekleri kullanarak ek bilgi sağlamayı mümkün kılar:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” ve “debug” detay seviyesini tanımlar, “logfile” anahtarı ise çıktının konsol penceresi yerine bir dosyaya yönlendirilmesine olanak tanır.

## Kullanıcı Yönetimi

###   add-user
  
add-user komutu, ***digna*** CLI içinde yeni bir kullanıcıyı ***digna*** sistemine eklemek için kullanılır.
  
#### Komut Kullanımı
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argümanlar

- **USER_NAME**: Yeni kullanıcı için kullanıcı adı (gerekli).
- **USER_FULL_NAME**: Yeni kullanıcının tam adı (gerekli).
- **USER_PASSWORD**: Yeni kullanıcı için parola (gerekli).

#### Seçenekler

- --is_superuser, -su: Yeni kullanıcıyı yönetici olarak belirlemek için bayrak.
- --valid_until, -vu: Kullanıcı hesabı için YYYY-MM-DD HH:MI:SS formatında bir son geçerlilik tarihi belirler. Belirtilmezse hesapın son kullanma tarihi yoktur.

#### Örnek

jdoe kullanıcı adı, John Doe tam adı ve password123 parolasıyla yeni bir kullanıcı eklemek için:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Hesaba son geçerlilik tarihi belirleyerek yeni bir kullanıcı eklemek için:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
delete-user komutu, ***digna*** CLI içinde mevcut bir kullanıcıyı ***digna*** sisteminden kaldırmak için kullanılır.
  
##### Komut Kullanımı
bash
dignacli delete-user USER_NAME

  
#### Argümanlar
- **USER_NAME**: Silinecek kullanıcının kullanıcı adı (gerekli). Bu komutun gerektirdiği tek argümandır.

#### Örnek
bash
dignacli delete-user jdoe

  
Bu komutu çalıştırmak, jdoe kullanıcısını ***digna*** sisteminden kaldırır, erişimini iptal eder ve depo içindeki ilişkili veri ve izinlerini siler.

###   modify-user

modify-user komutu, ***digna*** CLI içinde mevcut bir kullanıcının bilgilerini güncellemek için kullanılır.

##### Komut Kullanımı
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argümanlar
  
- **USER_NAME**: Değiştirilecek kullanıcının kullanıcı adı (gerekli).
- **USER_FULL_NAME**: Kullanıcının yeni tam adı (gerekli).
  
#### Seçenekler  
  
- --is_superuser, -su: Kullanıcıyı süper kullanıcı olarak ayarlar, yükseltilmiş ayrıcalıklar verir. Bu bayrak bir değer gerektirmez.  
- --valid_until, -vu: Kullanıcı hesabı için YYYY-MM-DD HH:MI:SS formatında bir son geçerlilik tarihi belirler. Sağlanmazsa hesap süresiz olarak geçerli kalır.  
  
#### Örnek
  
jdoe kullanıcısının tam adını “Johnathan Doe” olarak değiştirmek ve kullanıcıyı süper kullanıcı yapmak için:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
modify-user-pwd komutu, ***digna*** CLI içinde mevcut bir kullanıcının parolasını değiştirmek için kullanılır.
  
##### Komut Kullanımı
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argümanlar
  
- **USER_NAME**: Parolası değiştirilecek kullanıcının kullanıcı adı (gerekli).
- **USER_PWD**: Kullanıcının yeni parolası (gerekli).
  
#### Örnek
  
jdoe kullanıcısının parolasını newpassword123 olarak değiştirmek için:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

list-users komutu, ***digna*** CLI içinde ***digna*** sistemine kayıtlı tüm kullanıcıların listesini görüntüler.

##### Komut Kullanımı

bash
dignacli list-users


Bu komutu çalıştırmak, ***digna*** deposuna bağlanacak ve tüm kullanıcıları ID, kullanıcı adı, tam ad, süper kullanıcı durumu ve son geçerlilik zaman damgalarıyla birlikte listeleyecektir.

# Depo Yönetimi

###   upgrade-repo
  
upgrade-repo komutu, ***digna*** CLI içinde ***digna*** deposunu yükseltmek veya başlatmak için kullanılır. Bu komut, güncellemeleri uygulamak veya depo altyapısını ilk kez kurmak için gereklidir.
  
#### Komut Kullanımı

bash
dignacli upgrade-repo [options]

  
#### Seçenekler
  
- --simulation-mode, -s: Etkinleştirildiğinde, bu seçenek komutu simülasyon modunda çalıştırır; yürütülecek SQL ifadelerini yazdırır ancak bunları gerçekten yürütmez. Bu, değişiklikleri uygulamadan önce önizlemek için kullanışlıdır.  

  
#### Örnek
  
***digna*** deposunu yükseltmek için herhangi bir seçenek olmadan komutu çalıştırabilirsiniz:
  
bash
dignacli upgrade-repo
  
Yükseltmeyi simülasyon modunda çalıştırmak (SQL ifadelerini uygulamadan görmek) için:
  
bash
dignacli upgrade-repo --simulation-mode

  
Bu komut, veri tabanı şeması ve diğer depo bileşenlerinin yazılımın en son sürümüyle güncel olmasını sağlayarak ***digna*** sisteminin bakımında kritik öneme sahiptir.

###   encrypt
  
encrypt komutu, ***digna*** CLI içinde bir parolayı şifrelemek için kullanılır.
  
#### Komut Kullanımı
  
bash
dignacli encrypt <PASSWORD>

    
#### Argümanlar
- **PASSWORD**: Şifrelenmesi gereken parola (gerekli).
  
#### Örnek
  
Bir parolayı şifrelemek için parolayı argüman olarak vermelisiniz.  
Örneğin, mypassword123 parolasını şifrelemek için:
bash
dignacli encrypt mypassword123

Bu komut, verilen parolanın şifrelenmiş versiyonunu çıktılar; bu daha sonra güvenli bağlamlarda kullanılabilir. Parola argümanı sağlanmazsa, CLI eksik argümanı belirten bir hata görüntüler.

###   generate-key
  
generate-key komutu, ***digna*** deposunda saklanan parolaları korumak için gerekli olan bir Fernet anahtarı üretmek için kullanılır.
  
#### Komut Kullanımı
bash
dignacli generate-key

  
## Veri Yönetimi

###   clean-up

clean-up komutu, ***digna*** CLI içinde belirtilen bir projedeki bir veya birden fazla veri kaynağı için profilleri, tahminleri ve Traffic Light System (TLS) verilerini kaldırmak için kullanılır. Bu komut, veri yaşam döngüsü yönetimi için önemlidir; eski veya gereksiz verileri temizleyerek düzenli ve verimli bir veri ortamı sağlamaya yardımcı olur.

#### Komut Kullanımı

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argümanlar
  
- **PROJECT_NAME**: Verilerin kaldırılacağı projenin adı (gerekli). Bu argümanda all-projects anahtar kelimesini kullanmak, ***digna***'nın mevcut tüm projeler üzerinde yineleme yapmasını ve bu komutu uygulamasını sağlar.
- **FROM_DATE**: Veri kaldırma işleminin başlangıç tarih ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (gerekli).
- **TO_DATE**: Veri kaldırma işleminin bitiş tarih ve saati; FROM_DATE ile aynı formatları takip eder (gerekli).
  
#### Seçenekler
  
- --table-name, -tn: Temizleme işlemini proje içindeki belirli bir tablo ile sınırlar.
- --table-filter, -tf: Adlarında belirtilen alt dizeyi içeren tablolara temizleme uygulamak için filtreler.
- --timing, -tm: Tamamlandıktan sonra temizleme sürecinin zaman süresini gösterir.
- --help: clean-up komutu için yardım bilgilerini gösterir ve çıkar.
  
#### Örnek
  
ProjectA projesinden 1 Ocak 2023 ile 30 Haziran 2023 arasındaki verileri kaldırmak için:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Sadece Table1 adlı belirli bir tablodan veri kaldırmak için:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Bu komut, veri depolamayı yönetmeye ve deponun yalnızca ilgili bilgileri içermesini sağlamaya yardımcı olur.

###   inspect

inspect komutu, ***digna*** CLI içinde belirtilen bir projedeki bir veya birden fazla veri kaynağı için profiller, tahminler ve Traffic Light System (TLS) verileri oluşturmak için kullanılır. Bu komut, belirli bir dönem boyunca verilerin analiz edilmesine ve izlenmesine yardımcı olur.

#### Komut Kullanımı

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argümanlar
  
- **PROJECT_NAME**: İncelenecek verilerin ait olduğu projenin adı (gerekli). Bu argümanda all-projects anahtar kelimesini kullanmak, ***digna***'nın mevcut tüm projeler üzerinde yineleme yapmasını ve bu komutu uygulamasını sağlar.
- **FROM_DATE**: Veri incelemesinin başlangıç tarih ve saati. Kabul edilen formatlar %Y-%m-%d, %Y-%m-%dT%H:%M:%S veya %Y-%m-%d %H:%M:%S şeklindedir (gerekli).
- **TO_DATE**: Veri incelemesinin bitiş tarih ve saati; FROM_DATE ile aynı formatları takip eder (gerekli).
  
#### Seçenekler

- --table-name, -tn: İncelemeyi proje içindeki belirli bir tablo ile sınırlar.
- --table-filter, -tf: Adlarında belirtilen alt dizeyi içeren tablolarda inceleme yapar.
- --force-profile: Profillerin yeniden toplanmasını zorlar. Varsayılan olarak force-profile etkindir.
- --no-force-profile: Profillerin yeniden toplanmasını engeller.
- --force-prediction: Tahminlerin yeniden hesaplanmasını zorlar. Varsayılan olarak force-prediction etkindir.
- --no-force-prediction: Tahminlerin yeniden hesaplanmasını engeller.
- --force-alert-status: Uyarı durumlarının yeniden hesaplanmasını zorlar. Varsayılan olarak force-alert-status etkindir.
- --no-force-alert-status: Uyarı durumlarının yeniden hesaplanmasını engeller.
- --timing, -tm: İnceleme sürecinin süresini tamamlandıktan sonra gösterir.
- --alert-notification, -an: Abone kanallara uyarı bildirimleri gönderir.
  
#### Örnek
  
ProjectA projesi için 1 Ocak 2024 ile 31 Ocak 2024 arasındaki verileri incelemek için:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Sadece belirli bir tabloyu incelemek ve tahminlerin yeniden hesaplanmasını zorlamak için:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Bu komut, güncellenmiş profiller ve tahminler oluşturmak, veri bütünlüğünü izlemek ve belirtilen proje zaman aralığında uyarı sistemlerini yönetmek için kullanışlıdır.

###   tls-status

tls-status komutu, ***digna*** CLI içinde belirli bir proje içindeki bir tablo için belirli bir tarihte Traffic Light System (TLS) durumunu sorgulamak için kullanılır. Traffic Light System, verinin sağlığı ve kalitesi hakkında bilgi sağlar; dikkat edilmesi gereken sorunları veya uyarıları gösterir.
  
#### Komut Kullanımı
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Argümanlar
  
- **PROJECT_NAME**: TLS durumunun sorgulandığı projenin adı (gerekli).
- **TABLE_NAME**: TLS durumu için gerekli olan proje içindeki belirli tablo (gerekli).
- **DATE**: TLS durumunun sorgulandığı tarih, genellikle %Y-%m-%d formatında (gerekli).
  
#### Örnek
  
ProjectA projesinde UserData adlı tablonun 1 Temmuz 2024 tarihindeki TLS durumunu kontrol etmek için:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Bu komut, önceden tanımlanmış kriterlere dayalı olarak net ve eyleme geçirilebilir bir durum raporu sağlayarak kullanıcıların veri kalitesini izlemelerine ve sürdürmelerine yardımcı olur.

###   list-projects
  
list-projects komutu, ***digna*** CLI içinde ***digna*** sistemindeki mevcut tüm projelerin listesini görüntülemek için kullanılır.
  
#### Komut Kullanımı
  
bash
dignacli list-projects


Bu komut, özellikle birden fazla proje yöneten yöneticiler ve kullanıcılar için kullanışlıdır; ***digna*** deposundaki mevcut projelerin hızlı bir genel görünümünü sağlar.

###   list-ds

list-ds komutu, ***digna*** CLI içinde belirtilen bir proje içindeki mevcut tüm veri kaynaklarının listesini görüntülemek için kullanılır. Bu komut, analiz ve yönetim için kullanılabilir veri varlıklarını anlamaya yardımcı olur.

#### Komut Kullanımı
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının listelendiği proje adı (gerekli).
  
#### Örnek
  
ProjectA adlı projedeki tüm veri kaynaklarını listelemek için:
  
bash
dignacli list-ds ProjectA

  
Bu komut, bir projede mevcut veri kaynaklarının genel bir görünümünü sağlayarak veri ortamını daha etkili şekilde gezmeyi ve yönetmeyi kolaylaştırır.