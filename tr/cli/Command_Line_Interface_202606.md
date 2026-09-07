# digna CLI Başvurusu 2026.06
**2026-09-05**

Bu sayfa, ***digna*** CLI **2026.06** sürümünde bulunan komutların tamamını, kullanım örnekleri ve seçenekleriyle birlikte belgeler.

Çalıştırılabilir dosyanın adı `digna`.

---

## CLI Temelleri

---

### Genel Bakış ve Söz Dizimi

**2026.06** sürümünün CLI'si, kategori tabanlı ve yapılandırılmış bir komut hiyerarşisi kullanır:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` ve `serve`, alt komutu olmayan tek başına komutlardır:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Genel Seçenekler

Aşağıdaki genel seçenekler tüm komutlar için geçerlidir:

- `--help`, `-h`: CLI'ye ya da belirli bir komut kategorisine veya alt komuta ilişkin yardım bilgilerini görüntüler.
- `--stacktrace`: Hata durumunda yalnızca en üst düzey iletiyi değil, hata zincirinin tamamını görüntüler.

`--stacktrace` tam anlamıyla genel bir seçenektir: komut kategorisinden **önce** verilmelidir, sonra değil.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

`--version` diye bir bayrak yoktur. Bunun yerine [`version`](#version) komutunu kullanın.

### Ön Koşullar

Komutların çoğu okunabilir ve geçerli bir `config.toml` dosyasına ihtiyaç duyar; bazıları buna ek olarak geçerli bir lisans gerektirir.
Aşağıdaki tablo, her komut kategorisinin herhangi bir işlem yapmadan önce neleri yüklediğini gösterir:

| Komut kategorisi | `config.toml` gerekir mi | Geçerli lisans gerekir mi |
|---|---|---|
| `version` | hayır | hayır |
| `config check` | hayır (komutun raporladığı şeyin ta kendisidir) | hayır |
| `license check` | hayır | denetimin *kendisidir* |
| `crypt` | evet | hayır |
| `serve` | evet | hayır |
| `project` | evet | hayır |
| `user` | evet | evet |
| `inspection` | evet | evet |
| `repo` | evet | evet |

Lisansın gerekli olduğu yerlerde hem imzası hem de son kullanma tarihi denetlenir ve bunlardan herhangi biri başarısız olursa komut, depoya dokunmadan önce sonlanır.

### Çıkış Kodları

- `0`: komut başarılı oldu.
- `1`: komut başarısız oldu. Hata iletisi, başına `Error: ` öneki eklenerek stderr'e yazılır.

### help

`--help` seçeneği, kullanılabilir komut kategorileri, alt komutlar ve seçenekler hakkında bilgi verir:

1. **Genel yardımı görüntüleme:**
   ```bash
   digna --help
   ```

2. **Belirli kategoriler ve komutlar için yardım alma:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **Çıktı şunları içerir:**
   - **Komut Açıklaması:** Komutun amacının özeti.
   - **Söz Dizimi:** Zorunlu ve isteğe bağlı argümanlar.
   - **Seçenekler:** Komuta özgü bayraklar ve parametreler.

### version

`version` komutu, kurulu ***digna*** sürümünü yazdırır. Hiçbir yapılandırma okumaz ve hiçbir lisansı doğrulamaz; bu nedenle `config.toml` dosyası ya da lisansı eksik veya geçersiz olan bir kurulumda da çalışır.

Sürüm numarası, [`repo check`](#repo-check) tarafından bildirilen depo şeması sürümünden bağımsızdır.

#### Komut Kullanımı
```bash
digna version
```

#### Örnek Çıktı
```text
2026.06
```

---

## Yapılandırma Yönetimi

---

### config check

`config check` komutu, yapılandırma dosyasını (`config.toml`) doğrular ve zorunlu tüm bölümlerin ve ayarların mevcut ve doğru biçimlendirilmiş olup olmadığını denetler. Her bölüm kendi başına doğrulanır; böylece bozuk bir `[app]` bölümü, `[repo]` bölümünün durumunu gizlemez.

Raporlanan bölümler şunlardır:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — isteğe bağlıdır; anahtarın bulunmaması denetimi geçer, bulunup da hatalı biçimlendirilmiş bir liste ise geçmez

Komut, diğer komutların yaptığı biçimde uygulama yapılandırmasını bilinçli olarak yüklemez; böylece ***digna***'nın hiç başlamamasına yol açacak bir `config.toml` dosyasını tanılayabilir.

#### Komut Kullanımı
```bash
digna config check [OPTIONS]
```

#### Seçenekler
- `--configpath`, `-c`: Yapılandırma dosyasının ya da `config.toml` içeren bir dizinin yolu (varsayılan `./config.toml`).
- `--json`: Doğrulama raporunu JSON olarak verir. `--quiet` seçeneğine göre önceliklidir.
- `--quiet`, `-q`: Raporu bastırır ve yalnızca çıkış koduna dayanır.

#### Örnek
```bash
digna config check
```

Belirli bir yapılandırma dosyasını doğrulamak ve çıktıyı JSON olarak biçimlendirmek için:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Örnek Çıktı
```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: FAILED
    missing field `aes_gcm_key`
 - OIDC config(s): OK

Overall: FAILED
```

Eksik bir dosya veya bir TOML söz dizimi hatası, bölüm bölüm doğrulanacak hiçbir şey bırakmaz ve `--quiet` ya da `--json` seçeneklerinden bağımsız olarak rapor yerine tek bir hata olarak bildirilir.

---

## Depo Yönetimi

---

### repo check

`repo check` komutu veritabanı bağlantısını sınar, deponun kurulumunu ve sürümünü doğrular. Yapılandırılan şema yoksa ya da var olup da içinde bir ***digna*** deposu barındırmıyorsa başarısız olur.

Bildirilen sürüm, depo şemasının sürümüdür; bu sürüm, [`version`](#version) komutunun yazdırdığı ***digna*** sürümünden ayrı olarak numaralandırılır.

#### Komut Kullanımı
```bash
digna repo check
```

#### Örnek Çıktı
```text
Repo version 3.0.0 installed
```

### repo install

`repo install` komutu, `config.toml` dosyasında yapılandırılan şemaya yeni bir ***digna*** deposu kurar ve gereken tüm dizileri, tabloları, dizinleri, kısıtlamaları ve başlangıç kayıtlarını oluşturur.

Şemanın kendisi bu komut tarafından **oluşturulmaz** — önceden var olmalıdır. Ayrıca söz konusu şemada zaten bir depo kuruluysa komut çalışmayı reddeder ve kurulu sürüm daha eskiyse [`repo upgrade`](#repo-upgrade) komutuna yönlendirir.

#### Komut Kullanımı
```bash
digna repo install
```

#### Örnek Çıktı
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

`repo upgrade` komutu, mevcut bir depoyu kurulu sürümün beklediği sürüme getirmek için veritabanı şeması geçişlerini uygular. Yükseltmeler, sabit bir yükseltme yolu boyunca her seferinde bir sürüm adımı olarak uygulanır ve tamamlanan her adım depoya kaydedilir.

Depo zaten beklenen sürümdeyse komut, yükseltmeye gerek olmadığını bildirir ve hiçbir değişiklik yapmaz.

#### Komut Kullanımı
```bash
digna repo upgrade
```

#### Örnek Çıktı
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Şifreleme Yönetimi

---

### crypt gen-key

`crypt gen-key` komutu, `config.toml` içinde şifreleme anahtarı olarak kullanılmak üzere yeni bir AES-GCM şifreleme anahtarı üretir. Üretilen anahtar ona bağlı olmasa da, yüklenebilir bir `config.toml` dosyasının önceden bulunması gerekir.

#### Komut Kullanımı
```bash
digna crypt gen-key
```

#### Örnek Çıktı
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

`crypt encrypt` komutu, bir dizeyi (örneğin bir veritabanı parolasını) `config.toml` içinde yapılandırılmış AES-GCM anahtarıyla şifreler ve şifreli metni yazdırır.

#### Komut Kullanımı
```bash
digna crypt encrypt <VALUE>
```

#### Argümanlar
- **VALUE**: Şifrelenecek düz metin dizesi (zorunlu).

#### Örnek
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

`crypt decrypt` komutu, AES-GCM ile şifrelenmiş bir dizeyi `config.toml` içinde yapılandırılmış anahtarla çözer ve düz metni yazdırır.

#### Komut Kullanımı
```bash
digna crypt decrypt <VALUE>
```

#### Argümanlar
- **VALUE**: Çözülecek şifreli metin dizesi (zorunlu).

#### Örnek
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Kullanıcı Yönetimi

---

### user add

`user add` komutu, ***digna*** deposunda yeni bir kullanıcı hesabı oluşturur. Verilen e-posta adresine sahip bir kullanıcı zaten varsa komut başarısız olur.

#### Komut Kullanımı
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argümanlar
- **EMAIL**: Kullanıcının e-posta adresi (zorunlu).
- **PASSWORD**: Kullanıcının başlangıç parolası (zorunlu).
- **DISPLAY_NAME**: Kullanıcının tam görünen adı (zorunlu).

#### Seçenekler
- `--admin`, `-a`: Kullanıcıyı yönetici (superuser) ayrıcalıklarıyla oluşturur.

#### Örnek
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Bir yönetici hesabı oluşturmak için:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Örnek Çıktı
```text
User created with ID: 42
```

### user list

`user list` komutu, kayıtlı tüm kullanıcıları ID, e-posta, görünen ad ve yönetici bayrağıyla birlikte tablo biçiminde listeler.

#### Komut Kullanımı
```bash
digna user list
```

#### Örnek Çıktı
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

`user modify` komutu, e-posta adresiyle belirlenen mevcut bir kullanıcı hesabının görünen adını ve yönetici ayrıcalıklarını günceller.

Görünen ad da yönetici bayrağı da her zaman yazılır. `--admin` bir değer değil, bir anahtardır: **belirtilmemesi yönetici ayrıcalıklarını geri alır**, bu yüzden kullanıcının bu ayrıcalıkları koruması ya da kazanması gerektiği her durumda bu seçeneği verin.

#### Komut Kullanımı
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argümanlar
- **EMAIL**: Değiştirilecek kullanıcının e-posta adresi (zorunlu).
- **DISPLAY_NAME**: Güncellenmiş görünen ad (zorunlu).

#### Seçenekler
- `--admin`, `-a`: Yönetici ayrıcalıkları verir. Geri almak için belirtmeyin.
- `--valid-until`, `-v`: Uyumluluk için kabul edilir, ancak **şu anda uygulanmaz**. Verildiğinde bir uyarı yazdırılır ve hiçbir şey değişmez.

#### Örnek
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Örnek Çıktı
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

`user modify-pwd` komutu, mevcut bir kullanıcı hesabının parolasını günceller.

#### Komut Kullanımı
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argümanlar
- **EMAIL**: Parolası güncellenecek kullanıcının e-posta adresi (zorunlu).
- **PASSWORD**: Yeni parola (zorunlu).

#### Örnek
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

`user delete` komutu, bir kullanıcı hesabını sistemden kaldırır.

#### Komut Kullanımı
```bash
digna user delete <EMAIL>
```

#### Argümanlar
- **EMAIL**: Silinecek kullanıcının e-posta adresi (zorunlu).

#### Örnek
```bash
digna user delete jdoe@example.com
```

---

## Proje ve Veri Kaynağı Yönetimi

---

### project list

`project list` komutu, depodaki tüm kullanılabilir projeleri ID, ad ve açıklamalarıyla birlikte listeler.

#### Komut Kullanımı
```bash
digna project list
```

#### Örnek Çıktı
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

`project list-ds` komutu, belirli bir projeyle ilişkili tüm veri kaynaklarını ID, ad, tür, şema ve tablo adlarını göstererek listeler.

#### Komut Kullanımı
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynakları listelenecek projenin adı (zorunlu). Ad birebir eşleşmelidir.

#### Örnek
```bash
digna project list-ds ProjectA
```

#### Örnek Çıktı
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

`project export-ds` komutu, bir projedeki veri kaynaklarını bir JSON belgesine aktarır.

Ne `--table-name` ne de `--table-id` verilirse, projenin tüm veri kaynakları dışa aktarılır.

#### Komut Kullanımı
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argümanlar
- **PROJECT_NAME**: Veri kaynaklarının dışa aktarılacağı projenin adı (zorunlu).

#### Seçenekler
- `--table-name`, `-n`: Dışa aktarılacak veri kaynaklarının adları. Birden çok ad boşlukla ayrılarak verilebilir.
- `--table-id`, `-i`: Dışa aktarılacak veri kaynaklarının ID'leri. Birden çok ID boşlukla ayrılarak verilebilir.
- `--exportfile`, `-f`: Dışa aktarılan veri kaynaklarının kaydedileceği yol (varsayılan: `data_sources_export.json`).

#### Örnek
`ProjectA` içindeki tüm veri kaynaklarını dışa aktarmak için:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Belirli tabloları dışa aktarmak için:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Örnek Çıktı
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

`project import-ds` komutu, bir dışa aktarma dosyasındaki veri kaynaklarını hedef bir projeye aktarır ve her nesne için neyin oluşturulduğunu, güncellendiğini veya atlandığını bildirir.

#### Komut Kullanımı
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argümanlar
- **PROJECT_NAME**: İçe aktarmanın yapılacağı hedef projenin adı (zorunlu).
- **EXPORT_FILE**: JSON dışa aktarma dosyasının yolu (zorunlu).

#### Seçenekler
- `--output-file`, `-o`: İçe aktarma raporunun yazılacağı dosya. Bu seçenek olmadan rapor stdout'a gider.
- `--output-format`, `-f`: İçe aktarma raporunun biçimi — `table`, `json` veya `csv` (varsayılan: `table`).

#### Örnek
```bash
digna project import-ds ProjectB my_export.json
```

Makine tarafından okunabilir bir rapor almak için:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

Rapor dört nesne düzeyini kapsar — veri kaynağı, veri kümesi tanımı, öznitelik ve doğrulama kuralı — ve her biri için içe aktarma eylemini, sonucu, ortaya çıkan nesnenin ID'sini ve varsa ek bilgileri içerir.

### project plan-import-ds

`project plan-import-ds` komutu, hedef bir projeye yapılacak veri kaynağı içe aktarımının ön izlemesini sunar; hangi nesnelerin oluşturulacağını, güncelleneceğini veya atlanacağını hiçbir şeyi değiştirmeden gösterir. [`project import-ds`](#project-import-ds) ile aynı dışa aktarma dosyasını ve aynı raporlama seçeneklerini alır ve planlanan her nesne için bir adım numarası ekler.

#### Komut Kullanımı
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argümanlar
- **PROJECT_NAME**: Hedef projenin adı (zorunlu).
- **EXPORT_FILE**: Dışa aktarma dosyasının yolu (zorunlu).

#### Seçenekler
- `--output-file`, `-o`: İçe aktarma planının yazılacağı dosya. Bu seçenek olmadan plan stdout'a gider.
- `--output-format`, `-f`: İçe aktarma planının biçimi — `table`, `json` veya `csv` (varsayılan: `table`).

#### Örnek
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Denetim Yönetimi

---

### inspection run

`inspection run` komutu, bir proje ve bir tarih aralığı için denetim isteği oluşturur ve ardından — verilen seçeneklere bağlı olarak — ya isteği bekler, ya hemen geri döner ya da denetimi kendi süreci içinde çalıştırır.

Üç çalıştırma modu şunlardır:

- **Varsayılan (bayrak yok)**: istek arka uç için kuyruğa alınır ve CLI, denetim son bir duruma ulaşana kadar isteği iki saniyede bir yoklayarak görev ilerlemesini yazdırır. Çalışan bir `digna serve` gereklidir; aksi hâlde isteği alacak hiçbir şey olmaz.
- **`--async-mode`**: istek kuyruğa alınır ve ID'si hemen yazdırılır. İsteği izlemek için [`inspection status`](#inspection-status) komutunu kullanın.
- **`--bypass-backend`**: denetim, CLI sürecinin kendisi tarafından yürütülür ve kuyruğa alınmaz; bu nedenle çalışan bir sunucuya gerek yoktur.

`--async-mode` ile `--bypass-backend` birlikte kullanılamaz.

Denetim başarıyla tamamlanmadıysa komut, her modda sıfırdan farklı bir çıkış koduyla sonlanır.

#### Komut Kullanımı
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argümanlar
- **PROJECT_NAME**: Hedef projenin adı (zorunlu). Ad birebir eşleşmelidir.
- **START_DATE**: Tarih aralığının `YYYY-MM-DD` biçimindeki başlangıç tarihi (zorunlu).
- **END_DATE**: Tarih aralığının `YYYY-MM-DD` biçimindeki bitiş tarihi (zorunlu).

#### Seçenekler
- `--table-name`: Denetimi, veri kaynağı adıyla belirtilen tek bir proje veri kaynağıyla sınırlar. Bu seçenek olmadan projenin tüm veri kaynakları denetlenir.
- `--async-mode`: Denetimi kuyruğa alır ve beklemek yerine istek ID'sini yazdırır. `--bypass-backend` ile birlikte kullanılamaz.
- `--bypass-backend`: Denetimi arka uç için kuyruğa almak yerine doğrudan CLI sürecinde çalıştırır. `--async-mode` ile birlikte kullanılamaz.

#### Örnek
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Asenkron bir denetim göndermek için:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Tek bir veri kaynağını denetlemek için:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Örnek Çıktı
Varsayılan mod:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Asenkron mod:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

`inspection status` komutu, bir denetim isteğinin durumunu ve görev ilerlemesini istek ID'si üzerinden sorgular.

#### Komut Kullanımı
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argümanlar
- **INSPECTION_REQUEST_ID**: Denetim isteğinin sayısal ID'si (zorunlu).

#### Örnek
```bash
digna inspection status 1024
```

#### Örnek Çıktı
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

`inspection abort` komutu, çalışan veya bekleyen denetim isteklerinin iptalini talep eder. Etkilenen her istek için bir durdurma olayı kaydeder; bu olaya göre arka uç hareket ettiğinden, iptal anında bir sonlandırma değil, durdurma talebidir.

#### Komut Kullanımı
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argümanlar
- **INSPECTION_REQUEST_ID**: İptal edilecek denetim isteğinin ID'si. `--killall` verilmediği sürece zorunludur.

#### Seçenekler
- `--killall`: Çalışmakta olan ve bekleyen tüm denetim isteklerini iptal eder. Yanında verilen bir istek ID'sine göre önceliklidir.

#### Örnek
Belirli bir isteği iptal etmek için:
```bash
digna inspection abort 1024
```

Etkin ve kuyruktaki tüm denetimleri iptal etmek için:
```bash
digna inspection abort --killall
```

#### Örnek Çıktı
`--killall` ne yaptığını bildirir; tek bir isteğin iptali herhangi bir çıktı üretmez ve başarıyı çıkış koduyla bildirir.
```text
All running and pending inspections have been aborted.
```

---

## Lisans Yönetimi

---

### license check

`license check` komutu, `license.toml` dosyasını doğrular; imzasını kurulumla birlikte gelen genel anahtara karşı denetler ve süresinin dolmadığını kontrol eder. Hiçbir uygulama yapılandırması okumaz; bu nedenle `config.toml` henüz kurulmadan önce de çalışır.

#### Komut Kullanımı
```bash
digna license check
```

#### Örnek Çıktı
```text
License is valid
```

Geçersiz bir imza ile süresi dolmuş bir lisans, ikisi de çıkış kodu 1 ile olmak üzere ayrı hatalar olarak bildirilir.

---

## Sunucu ve Arka Plan Hizmetleri

---

### serve

`serve` komutu, ***digna*** REST API sunucusunu, arka planda çalışan denetim zamanlayıcısı ve denetim yöneticisiyle birlikte başlatır. Başlangıçta ayrıca, deponun hâlâ çalışıyor olarak kaydettiği tüm denetimleri başarısız olarak işaretler; çünkü önceki bir süreçten hiçbir şey ayakta kalmış olamaz.

Komut, durdurulana kadar ön planda çalışır.

#### Komut Kullanımı
```bash
digna serve [OPTIONS]
```

#### Seçenekler
- `--address`: API sunucusunun bağlanacağı ağ adresi (varsayılan: `127.0.0.1`).
- `--port`: Dinlenecek bağlantı noktası numarası (varsayılan: `8000`).

#### Örnek
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Örnek Çıktı
```text
Server running on http://0.0.0.0:8000
```