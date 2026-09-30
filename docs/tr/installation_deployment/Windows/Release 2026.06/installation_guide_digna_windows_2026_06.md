---
title: Windows Kurulum Kılavuzu – digna Sürüm 2026.06 | digna Belgeleri
description: digna Sürüm 2026.06'i Windows'ta kurmaya yönelik adım adım rehber — sistem gereksinimleri, PostgreSQL kurulumu, web sunucusu yapılandırması, backend ve dashboard yapılandırması, digna'yı Windows hizmeti olarak çalıştırma ve yeni sürüme yükseltme.
keywords: digna windows kurulumu, digna dağıtım rehberi, digna backend kurulumu, digna dashboard kurulumu, postgresql kurulumu, digna windows servisi, digna yükseltme rehberi
image: /assets/logo_square.png
---

# digna Sürüm 2026.06 için Windows Kurulum Kılavuzu

**Sürüm:** 2026.06

**Son Güncelleme:** 30 Ağustos 2026


---

## İçindekiler

1. [Giriş](#introduction)
2. [Sistem Gereksinimleri](#system-requirements)
3. [Kurulum Öncesi Hazırlık](#pre-installation-setup)
4. [PostgreSQL Sunucu Kurulumu](#postgresql-server-setup)
5. [Web Sunucusu Yapılandırması](#web-server-configuration)
6. [İlk Kurulum](#initial-installation)
7. [Backend Yapılandırması](#backend-configuration)
8. [Dashboard Yapılandırması](#dashboard-configuration)
9. [digna'yı Windows Hizmeti Olarak Çalıştırma](#running-digna-as-a-windows-service)
10. [Yeni Bir Sürüme Yükseltme](#upgrading-to-a-new-release)

---

## Giriş {: #introduction }

### digna Hakkında

digna, veri ambarları, veri gölleri ve lakehouse'lar gibi çeşitli veri ortamlarında veri kalitesi yönetimini optimize etmek için tasarlanmış kapsamlı, yapay zekâ destekli bir platformdur. Yüksek ölçeklenebilirlik ve uyarlanabilirlik göz önünde bulundurularak geliştirilen digna, otomasyon, gerçek zamanlı izleme ve anomali tespiti ile modern veri zorluklarına yanıt verir.

digna iki ana bileşenden oluşur:

- **digna**: uygulamanın çekirdeği; verileri işlemekten ve kalite denetimlerini yürütmekten sorumludur. Arka ucu ve komut satırı arayüzünü tek bir çalıştırılabilir dosyada birleştirir ve önceki sürümlerdeki ayrı `dignabackend` ile `dignacli` programlarının yerini alır.
- **dignadashboard**: Bir web sunucusunda barındırılan, digna platformuyla etkileşim kurmayı ve veri kalite metriklerini görselleştirmeyi sağlayan web tabanlı arayüz.

### 2026.06 Sürümünde Yenilikler

Bu sürüm, veri gözlemlenebilirliğini doğrudan kodunuza getirerek geliştiricilerin kaynakta veri kalitesini izlemesini sağlar. Tam ayrıntılar için [sürüm notlarına](http://docs.digna.ai/changelog/Release_202606/) bakın.

### macOS veya Linux mu arıyorsunuz?

Bu kılavuz Windows içindir. Diğer platformlar için [macOS Kurulum Kılavuzu](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) veya [Linux Kurulum Kılavuzu](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md) belgelerine bakın.

---

## Sistem Gereksinimleri {: #system-requirements }

Kuruluma başlamadan önce sisteminizin aşağıdaki minimum gereksinimleri karşıladığından emin olun:

| Gereksinim | Özellik |
|---|---|
| **İşletim Sistemi** | Windows Server veya Windows 10/11 |
| **Bellek (Minimum Kurulum)** | 16 GB RAM |
| **Disk Alanı** | 10 GB kullanılabilir depolama |
| **Veritabanı** | PostgreSQL Server 12 veya üzeri |
| **Web Sunucusu** | IIS, Apache Tomcat veya eşdeğeri |

### Veritabanı Kurulum Seçenekleri

**PostgreSQL zaten kuruluysa:**
Mevcut PostgreSQL sunucunuza digna için yeni bir veritabanı ekleyebilirsiniz.

**PostgreSQL'i digna ile aynı makineye kuruyorsanız:**

!!! info "Önerilen Özellikler"

    - **Bellek**: 32 GB RAM (16 GB yerine)
    - **Disk Alanı**: 50 GB kullanılabilir depolama (10 GB yerine)

    Bu daha yüksek özellikler, digna ile PostgreSQL veritabanının aynı anda çalışmasını rahatlıkla karşılayacak şekilde önerilir.

---

## Kurulum Öncesi Hazırlık {: #pre-installation-setup }

digna'yı kurmadan önce iki temel önkoşulun yerinde olduğundan emin olun:

1. **PostgreSQL Server** – hesaplanmış metrikler ve performans verileri için depolama
2. **Web Server** – digna Dashboard'u barındırmak için

Bu bileşenler henüz kurulu değilse, aşağıdaki bölümlerde bunları kurup yapılandırma adımlarını izleyin.

---

## PostgreSQL Sunucu Kurulumu {: #postgresql-server-setup }

### PostgreSQL Zaten Kuruluysa

PostgreSQL yerel makinenizde zaten kurulu ve çalışıyorsa veya yönetilen uzak bir PostgreSQL sunucusu kullanıyorsanız, [bir sonraki bölüme](#web-server-configuration) geçebilirsiniz.

### PostgreSQL Kurulumu

Windows üzerinde PostgreSQL kurmak için şu adımları izleyin:

#### Adım 1: PostgreSQL İndirin

1. [PostgreSQL Downloads sayfasını](https://www.postgresql.org/download/) ziyaret edin
2. **Windows** seçin
3. En güncel yükleyiciyi indirin

#### Adım 2: Yükleyiciyi Çalıştırın

1. İndirilen yükleyici dosyasına çift tıklayın
2. Kurulum sihirbazındaki yönergeleri izleyin

#### Adım 3: Kurulum Dizini Seçin

PostgreSQL'in kurulacağı dizini seçin. Varsayılan konum genellikle uygundur.

#### Adım 4: Bileşenleri Seçin

Standart kurulum için varsayılan bileşen seçeneklerini koruyun.

#### Adım 5: PostgreSQL Süper Kullanıcı Parolasını Belirleyin

PostgreSQL süper kullanıcısı (`postgres`) için bir parola girip doğrulayın. **Bu parolayı güvenli bir şekilde saklayın** — daha sonra ihtiyaç duyacaksınız.

#### Adım 6: Port Numarasını Yapılandırın

Varsayılan PostgreSQL portu `5432`'dir. İster varsayılanı kullanın ister gerekirse farklı bir port belirleyin.

!!! tip "İpucu"

    Eğer 5432 portu zaten kullanımdaysa, alternatif bir port seçin ve ilerideki yapılandırmalar için not edin.

#### Adım 7: Yerel Ayarı (Locale) Seçin

Veritabanınız için uygun yeri (locale) seçin. Varsayılan genellikle çoğu kurulum için uygundur.

#### Adım 8: Kurulumu Tamamlayın

Kalan adımlarda **Next** butonuna tıklayarak ilerleyin, ardından **Finish** ile tamamlayın.

#### Adım 9: Kurulumu Doğrulayın

Komut İstemi'ni açın ve PostgreSQL'in kurulu olduğunu doğrulayın:

```bash
psql --version
```

Kurulum başarılıysa PostgreSQL sürümünü görmelisiniz.

---

## Web Sunucusu Yapılandırması {: #web-server-configuration }

digna dashboard'unu barındırmak için bir web sunucusuna ihtiyaç vardır. Aşağıdaki seçeneklerden birini seçin:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Bu sunuculardan yalnızca birini kurmanız ve yapılandırmanız yeterlidir.

### IIS Kurulumu {: #iis-setup }

#### Genel Bakış

Internet Information Services (IIS), Microsoft'un web siteleri ve web uygulamalarını barındırmak için sunduğu web sunucusudur.

#### IIS'i Etkinleştirme

1. **Denetim Masasını Açın**
   - `Win + R` tuşlarına basın
   - `control` yazıp Enter tuşuna basın

2. **Windows Özelliklerine Gidin**
   - **Programlar**'a tıklayın
   - **Windows özelliklerini aç veya kapat**'ı seçin

3. **Internet Information Services'i Etkinleştirin**
   - Aşağı kaydırıp **Internet Information Services (IIS)** öğesini bulun
   - Onay kutusunu işaretleyin
   - Alt bileşenleri genişletmek için **+** işaretine tıklayın ve şu alt bileşenlerin seçili olduğundan emin olun:
     - **Web Management Tools**
     - **World Wide Web Services**

4. Değişiklikleri uygulamak için **OK** tuşuna basın

5. **IIS Kurulumunu Doğrulayın**
   - Tarayıcınızı açın
   - `http://localhost` adresine gidin
   - IIS Hoş Geldiniz sayfasını görmelisiniz

#### Gerekli: URL Rewrite Modülü

IIS, URL Rewrite bileşeni gerektirir. [Resmi Microsoft sayfasından](https://www.iis.net/downloads/microsoft/url-rewrite) indirin ve yükleyin.

#### Gerekli: Markdown Dosyaları için MIME Türü

IIS'in Markdown dosyalarını (`.md`) doğru şekilde servis edebilmesi için:

1. **IIS Manager**'ı açın ( `Win + R`, `inetmgr`, Enter )
2. **Your Site > MIME Types** bölümüne gidin
3. **Add...** butonuna tıklayın
4. Yapılandırın:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Önemli"

    Bu ayar olmadan `.md` dosyaları doğru şekilde servis edilmeyebilir.

---

### Apache Tomcat Kurulumu {: #apache-tomcat-setup }

#### Genel Bakış

Apache Tomcat, Java servlet container ve web sunucusu olarak kullanılan açık kaynaklı bir projedir.

#### Kurulum

1. **Apache Tomcat İndirin**
   - [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi) sayfasını ziyaret edin
   - Windows ZIP dağıtımını indirin

2. **Arşivi Çıkarın**
   - ZIP dosyasını sisteminizde bir dizine çıkarın
   - Örnek: `C:\Program Files\Apache Tomcat`

3. **Tomcat'in Çalıştığını Doğrulayın**
   - Tarayıcınızı açın
   - `http://localhost:8080` adresine gidin
   - Apache Tomcat karşılama sayfasını görmelisiniz

!!! tip "İpucu"

    Apache Tomcat genellikle kurulumdan sonra otomatik olarak başlar. Başlamazsa, `bin` klasörüne gidip `startup.bat` dosyasını çalıştırın.

---

## İlk Kurulum {: #initial-installation }

### Adım 1: digna Repository'sini Oluşturun

digna repository'si, digna tarafından hesaplanan tüm metrikleri saklar. Analitik ve performans verileri için merkezi veritabanı görevi görür.

#### Repository Şeması ve Kullanıcısı Oluşturma

PostgreSQL istemcinizi (pgAdmin, psql veya benzeri) açın ve aşağıdaki SQL komutlarını çalıştırın:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Aşağıdaki yer tutucuları değiştirin:**

- `<digna_repo_schema>` — İstediğiniz şema adı (ör. `dignarepo`)
- `<digna_repo_user>` — İstediğiniz kullanıcı adı (ör. `digna_user`)
- `<digna_repo_password>` — Bu kullanıcı için güvenli bir parola

**Örnek:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "En İyi Uygulama"

    Veritabanı kullanıcıları için güçlü, karmaşık parolalar kullanın. Kolay tahmin edilebilir kimlik bilgilerini kullanmaktan kaçının.

---

### Adım 2: digna Kurulum Paketini Çıkarın

1. Size sağlanan digna kurulum ZIP dosyasını bulun
2. İstediğiniz kurulum dizinine çıkarın
3. Çıkarma sonrası aşağıdaki öğeleri görmelisiniz:
   - `dashboard/` — Web dashboard arayüzü
   - `digna` — Ana yürütülebilir dosya (backend + CLI birleşik)

!!! info "Yapılandırma ve lisans dosyaları pakette yer almaz"

    Ne `config.toml` ne de `dashboard/dashboard_config.toml` kurulumla birlikte gelir — ikisini de
    kendiniz, [Backend Yapılandırması](#backend-configuration) ve
    [Dashboard Yapılandırması](#dashboard-configuration) bölümlerinde oluşturursunuz. `license.toml` da pakete dahil değildir;
    Adım 3'te açıklandığı gibi digna tarafından ayrı olarak sağlanır.

### Adım 3: Lisans Dosyasını Yükleyin

!!! warning "Önemli"

    Lisans dosyası kurulum paketine dahil değildir ve digna tarafından ayrı olarak sağlanacaktır.

1. Size sağlanan `license.toml` dosyasını bulun
2. Bunu digna kurulum dizininin köküne kopyalayın (`config.toml` ve `digna` yürütülebilir dosyasının bulunduğu dizin)

**Neden önemli:**
Lisans dosyası müşteri bilgilerini, lisans bitiş tarihini ve dijital imzayı içerir. **Bu dosyayı değiştirmeyin** — herhangi bir değişiklik lisansın geçersiz olmasına neden olur.

**Kurulum sonrası dizin yapısı:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backend Yapılandırması {: #backend-configuration }

### Adım 1: Yapılandırma Dosyasını Oluşturun ve Düzenleyin

`config_template.toml` dosyası digna kurulum dizininde sağlanır. Bunu `config.toml` olarak yeniden adlandırmanız yeterlidir.

**Konum:** `digna_installation/config.toml`

`config.toml` dosyasını bir metin düzenleyici ile açın ve aşağıdaki bölümleri yapılandırın.

#### [app] Bölümü

Bu bölüm digna backend uygulama ayarlarını yapılandırır:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend URL | Dashboard farklı bir sunucuda ise onun URL'sini ekleyin |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Kimlik bilgileri ile CORS için gerekli |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Tüm HTTP yöntemlerine izin ver |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Tüm başlıklara izin ver |

#### [repo] Bölümü

Bu bölüm PostgreSQL veritabanı bağlantısını yapılandırır:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_REPO_HOST` | `localhost` or IP | PostgreSQL sunucu hostname/IP |
| `digna_REPO_PORT` | `5432` (default) | PostgreSQL portu |
| `digna_REPO_DB` | `postgres` | Veritabanı adı |
| `digna_REPO_SCHEMA` | `dignarepo` | Daha önce oluşturduğunuz şema |
| `digna_REPO_USER` | `digna_user` | PostgreSQL kurulumu sırasında oluşturduğunuz kullanıcı |
| `digna_REPO_PASSWORD` | Your password | Şema oluşturma sırasında belirlenen parola |

#### [base] Bölümü

Bu bölüm güvenlik ve çerez (cookie) ayarlarını içerir:

```toml
[base]
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
DIGNA_SCHEDULER_MAX_DELAY = 100
DIGNA_CLEANUP_TIME = "12:00"
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Frontend domain'i ile eşleşsin |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (production) | HTTPS bağlantıları için `true` kullanın |
| `digna_COOKIE_HTTPONLY` | `true` | Güvenlik için her zaman etkin |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF saldırılarını önlemeye yardımcı olur |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 hours) | Oturum zaman aşımı (saniye cinsinden) |
| `digna_MAX_WORKERS` | Number of CPU cores - 1 | Paralel denetim görevlerinin sayısı |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Zamanlayıcının, vadesi gelmiş bir işi başlatmadan önce ekleyebileceği saniye cinsinden azami gecikme |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Günlük temizliğin başladığı saat (24 saat biçiminde `HH:MM`) |

#### [encryption] Bölümü

Bu bölüm, depoda saklanan hassas değerleri şifrelemek için kullanılan anahtarı içerir. **Zorunludur** — anahtar eksikse `config check`, `[encryption]` bölümünü FAILED olarak bildirir.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64 kodlu anahtar | digna deposunda saklanan hassas değerleri şifreler |

!!! warning "config.toml dosyasını koruyun"

    Bu anahtar sabit bir değerdir, tüm digna kurulumlarında aynıdır ve deponuzdaki hassas değerlerin şifresini çözen şey odur. `config.toml` erişimini digna'nın çalıştığı hesapla sınırlayın, dosyayı sürüm denetiminin ve paylaşılan sürücülerin dışında tutun ve deponun kendisinden daha az güvenli saklanan her yedeğin dışında bırakın.

#### [logging] Bölümü

Bu bölüm günlükleme davranışını yapılandırır:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` or `DEBUG` | Üretim için `INFO`, sorun giderme için `DEBUG` |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Saklanacak günlük yedek sayısı (günlük bazda) |

---

### Adım 2: Yapılandırmayı Doğrulayın

Depoyu başlatmadan önce `config.toml` dosyasının eksiksiz ve doğru kurulmuş olduğunu denetleyin. digna kurulum dizininizde şunu çalıştırın:

```bash
digna config check
```

Her bölüm ayrı ayrı doğrulanır, böylece tek bir hata diğerlerinin durumunu gizlemez:

```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: OK
 - OIDC config(s): OK

Overall: OK
```

FAILED olarak bildirilen her şeyi düzeltin ve devam etmeden önce komutu yeniden çalıştırın. Seçeneklerin tam listesi [CLI başvurusunda](../../../cli/Command_Line_Interface_202606.md) yer alır.

### Adım 3: Repository Bağlantısını Test Edin

1. Komut İstemi'ni açın
2. digna kurulum dizinine gidin ( `config.toml` ve `digna` yürütülebilir dosyasının bulunduğu dizin )
3. Bağlantı testi çalıştırın:

```bash
digna repo check
```

Bağlantının kurulduğuna dair bir onay görmelisiniz (repository henüz başlatılmamıştır).

### Adım 4: Repository Şemasını Kurun

Aynı dizinde şu komutu çalıştırın:

```bash
digna repo install
```

Bu komut PostgreSQL veritabanınıza gerekli tabloları ve şemayı yükler.

### Adım 5: Yönetici (Admin) Kullanıcısı Oluşturun

1. Yeni bir Komut İstemi penceresi açın
2. digna kurulum dizinine gidin
3. Yönetici kullanıcısı oluşturmak için şu komutu çalıştırın:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Örnek:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Bu komut tam idari ayrıcalıklara sahip bir kullanıcı oluşturur.

!!! tip "En İyi Uygulama"

    Büyük küçük harf, sayı ve özel karakter içeren güçlü bir parola kullanın.

---

### Adım 6: digna Sunucusunu Başlatın

digna kurulum dizininde sunucuyu başlatın:

```bash
digna serve --address <host> --port <port>
```

**Parametreler:**
- `--address` — Sunucu hostname/IP
- `--port` — Sunucu portu 

Sunucunun çalıştığını doğrulayan başlangıç mesajları görmelisiniz:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! note "Sunucu terminali meşgul eder"

    `serve` ön planda çalışır ve siz ++ctrl+c++ ile durdurana kadar çalışmayı sürdürür. Kurulumu tamamlarken çalışır durumda bırakın; bunun yerine sistem açılışında otomatik başlatmak için bkz. [digna'yı Windows Hizmeti Olarak Çalıştırma](#running-digna-as-a-windows-service).

## Dashboard Yapılandırması {: #dashboard-configuration }

### Adım 1: Dashboard'u Web Sunucusuna Dağıtın

digna dashboard'u kendi yapılandırmasını `dashboard/dashboard_config.toml` dosyasından okur. Bu dosya kurulumla birlikte gelmez — onu `dashboard/` dizininde, dashboard dosyalarının yanında siz oluşturursunuz.

Dosyanın içeriği [Çoklu Oturum Açma (Single Sign-On)](../../../sso/overview.md) bölümünde açıklanmıştır; dosyaya ihtiyaç duyulan yer de burasıdır: dashboard'un sunduğu oturum açma seçeneklerini ve çoklu örnek dağıtımlarında backend bağlantısını içerir.

Web sunucunuzu seçin ve ilgili dağıtım adımlarını izleyin.

#### IIS'e Dağıtım

1. **IIS Manager**'ı açın
   - `Win + R` tuşlarına basın, `inetmgr` yazın, Enter

2. **Yeni Bir Web Sitesi Oluşturun**
   - Sol panelde **Sites** üstüne sağ tıklayın
   - **Add Website...**'i seçin

3. **Siteyi Yapılandırın**
   - **Site Name**: Bir ad girin (ör. "dignaDashboard")
   - **Physical Path**: Browse'a tıklayıp `dashboard` klasörünüzü seçin
   - **Binding**: IP adresi ve portu ayarlayın (HTTP için varsayılan 80, HTTPS için 443)

4. **Siteyi Başlatın**
   - **OK** ile siteyi oluşturun
   - Yeni siteye sağ tıklayıp **Start** seçeneğini tıklayın

5. **Kurulumu Test Edin**
   - Tarayıcınızı açın
   - `http://localhost` (veya yapılandırdığınız URL) adresine gidin
   - digna dashboard giriş sayfasını görmelisiniz

#### Apache Tomcat'e Dağıtım

1. **Dashboard'u Tomcat'e Kopyalayın**
   - `dashboard` klasörünü Tomcat `webapps` dizinine kopyalayın
   - İsterseniz adını değiştirin (ör. `digna`)
   - Örnek: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Dağıtımı Doğrulayın**
   - Tomcat yönetim sayfasını yenileyin veya yeniden yükleyin (http://localhost:8080)
   - Dağıtılmış uygulamalar arasında "digna" (veya seçtiğiniz isim) görünmelidir

3. **Dashboard'a Erişim**
   - Tarayıcınızı açın
   - `http://localhost:8080/digna` adresine gidin
   - digna dashboard giriş sayfasını görmelisiniz

---

## digna'yı Windows Hizmeti Olarak Çalıştırma {: #running-digna-as-a-windows-service }

### Neden Windows Hizmeti Kullanılır?

digna backend'i Windows hizmeti olarak çalıştırmak şu avantajları sağlar:
- Sunucu başlatıldığında otomatik olarak başlar
- Komut İstemi açık olmadan arka planda çalışır
- Çöktüğünde otomatik yeniden başlatma sağlar
- Windows Hizmetleri üzerinden yönetilebilir

### `windows` Komutları

Hizmet, `digna` yürütülebilir dosyasının kendisi tarafından, `digna windows`
alt komutlarıyla yönetilir. Çalıştırılacak batch dosyası yoktur.

| Komut | Amaç |
|---|---|
| `digna windows install` | digna'yı Windows hizmeti olarak kaydeder |
| `digna windows start` | Kayıtlı hizmeti başlatır |
| `digna windows stop` | Çalışan hizmeti durdurur |
| `digna windows uninstall` | Hizmet kaydını kaldırır |

!!! warning "Yönetici Gereklidir"

    Dört komutun tamamı, Yönetici olarak açılmış bir Komut İstemi'nden çalıştırılmalıdır.

Her komut, varsayılan olmayan bir adla kaydedilmiş bir hizmete erişmek için `--name` seçeneğini kabul eder. Seçeneklerin
tam listesi [CLI başvurusunda](../../../cli/Command_Line_Interface_202606.md) yer alır.

### Hizmeti Yükleme

1. **Komut İstemi'ni Yönetici Olarak Açın**
   - Komut İstemi üzerine sağ tıklayın
   - "Run as Administrator" (Yönetici olarak çalıştır) seçeneğini seçin

2. **digna kurulum dizininize gidin**
   ```bash
   cd C:\path\to\digna
   ```

3. **Hizmeti kaydedin**
   ```bash
   digna windows install
   ```

!!! important "Varsayılanlar size uymuyorsa adresi ve bağlantı noktasını belirtin"

    `install`, adresi ve bağlantı noktasını hizmet kaydına yazar ve hizmet tam olarak kaydedilen
    değerlere bağlanır. Varsayılanlar `127.0.0.1` ve `8000`'dir; bunlar yalnızca makinenin kendisinden
    gelen bağlantıları kabul eder. Başka bir ana bilgisayardaki dashboard buna erişemez; bu nedenle
    backend'in dinlemesi gereken adresi verin:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Bu değerler `config.toml` dosyasından okunmaz. Bunları sonradan değiştirmek için hizmeti kaldırın ve
    yeni değerlerle yeniden yükleyin.

Hizmet **otomatik başlatma** ile kaydedilir, bu nedenle Windows ile birlikte başlar. Hemen
başlamaz — bir sonraki bölüme bakın.

#### Yükleme Seçenekleri

| Seçenek | Varsayılan | Amaç |
|---|---|---|
| `--name` | `digna` | Hizmetin kaydedileceği ad |
| `--display-name` | `digna` | services.msc'de gösterilen ad |
| `--description` | `digna data quality backend` | services.msc'de gösterilen açıklama |
| `--address` | `127.0.0.1` | Hizmetin API'sini bağladığı adres |
| `--port` | `8000` | Hizmetin API'sini bağladığı bağlantı noktası |
| `--working-dir` | `digna` yürütülebilir dosyasının bulunduğu dizin | `config.toml` ve `license.toml` dosyalarını içeren ve hizmetin çalışma dizini olarak kullandığı dizin |
| `--start-type` | `auto` | `auto` Windows ile birlikte başlar, `manual` yalnızca istendiğinde başlar, `disabled` hizmeti kaydeder ancak başlatılmasını reddeder |
| `--account` | `LocalSystem` | Hizmetin çalışacağı hesap, ör. `DOMAIN\user` veya `.\user` |
| `--password` | | `--account` hesabının parolası |

!!! tip "Etki alanı hesabıyla çalıştırma"

    `LocalSystem` hesabının ağ kimliği yoktur; bu nedenle SQL Server'a Windows Kimlik Doğrulaması ve
    ağ paylaşımlarına her türlü erişim başarısız olur. Hizmetin kaynaklara belirli bir kullanıcı olarak
    erişmesi gerekiyorsa `--account` ve `--password` ile yükleyin.

### Hizmeti Başlatma ve Durdurma

#### Hizmeti Başlatmak İçin

```bash
digna windows start
```

#### Hizmeti Durdurmak İçin

```bash
digna windows stop
```

!!! tip "İpucu"

    Uygulama dosyalarını güncellemeden önce hizmeti her zaman durdurun.

### Hizmeti Yeni Bir Dizin Altına Taşımak

digna kurulumunu taşımaya ihtiyacınız varsa:

1. **Mevcut hizmeti durdurun ve kaydını kaldırın**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Uygulama Dosyalarını Taşıyın**
   - Tüm digna kurulum klasörünü yeni konuma taşıyın

3. **Hizmeti yeni konumdan yeniden kaydedin**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   İlk seferde kullandığınız `--address`, `--port` veya `--account` değerlerini yineleyin — önceki
   kayıt artık yoktur.

4. **Hizmeti Başlatın**
   ```bash
   digna windows start
   ```

### Hizmeti Kaldırma

1. **Çalışan Hizmeti Durdurun**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Hizmetin Kaydını Kaldırın**
   ```bash
   digna windows uninstall
   ```

digna sunucusu artık Windows hizmeti olarak kayıtlı olmayacaktır.

---

## Yeni Bir Sürüme Yükseltme {: #upgrading-to-a-new-release }

### Yükseltme Öncesi

**Önce Tüm Veritabanı Bağlantılarını Doğrulayın**

2026.06 sürümünden itibaren digna, her kaynak teknolojisine **ODBC** üzerinden erişir. Önceki sürümler, **Use ODBC** anahtarıyla seçilen, teknolojiye özgü sürücü ile ODBC arasında bir seçim sunuyordu. digna ekibi yalnızca ODBC üzerine inşa etmeye karar verdi; çünkü tek ve standart bir arayüz, ısmarlama sürücülerden oluşan bir kümeden daha fazlasını sağlar:

- **Kimlik doğrulama** — kimlik doğrulama ODBC'nin bir parçasıdır; dolayısıyla bir bağlantı, sürücüsünün desteklediği her şeyi kullanabilir: parolalar, belirteçler ve PAT'ler, Kerberos ve Active Directory, MFA ve tarayıcı tabanlı çoklu oturum açma, bulut kimlikleri, istemci sertifikaları ve TLS. Yeni yöntemler, bir digna sürümünü beklemek yerine sürücü güncellemesiyle gelir.
- **Veritabanı üreticilerince bakımı yapılan sürücüler** — üreticinin kendi sürücüsü yeni sunucu sürümlerini ve güvenlik düzeltmelerini izler; siz de onu digna'dan bağımsız olarak kendi takviminize göre güncelleyebilirsiniz.
- **Her şeyi yapılandırmanın tek yolu** — her teknoloji, aynı arayüz, hassas değerlerin aynı şifrelenmesi ve aynı sorun giderme ile anahtar/değer özelliklerinden oluşan bir listedir; kaynak başına farklı alan kümeleri yoktur.
- **İnce ayar ve kapsam** — zaman aşımları, TLS ayarları, vekil sunucular ve getirme boyutları gibi sürücü düzeyindeki seçenekler her kaynak için kullanılabilir ve uyumlu bir ODBC sürücüsü bulunan her teknoloji, digna'nın ayrı bir kılavuz yayımlamadıkları da dahil olmak üzere bağlanabilir.

Uygulamada bu, **Use ODBC** anahtarının ve ayrı ana bilgisayar, bağlantı noktası, veritabanı, kullanıcı ve parola alanlarının artık bulunmadığı anlamına gelir. **Halihazırda ODBC kullanmayan her bağlantı ODBC'ye taşınmalıdır** — otomatik dönüştürme yoktur, bu nedenle bunu yükseltmeden önce planlayın:

1. Kurulumunuzda tanımlı her veritabanı bağlantısını gözden geçirin ve henüz ODBC kullanmayanları not edin — her biri yeniden yapılandırılmalıdır.
2. İlgili ODBC sürücüsünü digna ana bilgisayarına kurun — bağlantılar, tarayıcıdan değil, digna arka ucunu çalıştıran sunucudan açılır. Bkz. [ODBC Sürücüsünü digna Ana Bilgisayarına Kurma](../../../databases/overview.md#install-the-driver).
3. Etkilenen her bağlantı için ODBC özelliklerini hazır bulundurun. [Teknoloji kılavuzları](../../../databases/overview.md#technology-guides) her kaynak için denenmiş bir özellik kümesi listeler.

Yükseltmeden sonra etkilenen her bağlantıyı ODBC'ye taşıyın ve panodan sınayın — bkz. [Veritabanı Bağlantısı Oluşturma](../../../databases/overview.md#create-a-database-connection) ve [Bağlantıyı Sınama](../../../databases/overview.md#testing-a-connection).

!!! warning "Databricks Legacy bağlantıları"

    Databricks Legacy bağlayıcısı bu sürümde kaldırıldı. Bu bağlantıları [Databricks](../../../databases/databricks_connector_guide.md) bağlayıcısına taşıyın.

**digna Repository Yedeği Almak Zorunludur**

digna'yı yükseltmeden önce veri kaybını önlemek için repository'nizin (PostgreSQL) yedeğini alın.
Bir yedek, yükseltme sırasında beklenmeyen sorunlar çıkarsa geri dönüş yapabilmenizi sağlar.

### Yükseltme Süreci

#### Adım 1: Eski Hizmeti Durdurun ve Kaydını Kaldırın

digna bir Windows hizmeti olarak çalışıyorsa, onu **mevcut kurulumunuzun batch
dosyalarıyla** durdurun — `digna windows` komutları yeni sürüme aittir ve henüz
kullanılamaz:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

Ardından hizmetin kaydını, yine eski batch dosyasıyla kaldırın. Kayıt, eski yürütülebilir dosyayı
ve betiklerini gösterir; bu yükseltme ikisini de değiştirdiği için kayıt yeniden kullanılamaz:

```bash
uninstall_service.bat
```

!!! warning "Herhangi bir şeyi yeniden adlandırmadan önce kaydı kaldırın"

    `uninstall_service.bat`, birazdan yeniden adlandıracağınız `bin` klasöründe bulunur ve oluşturduğu
    kaydı kaldırabilen tek şey odur. Eski kurulum hâlâ yerindeyken çalıştırın. Klasör zaten
    yeniden adlandırılmışsa eski adına geri çevirin, kaydı kaldırın ve ardından devam edin.

    Hizmetin çalıştığı hesabı ve hizmet verdiği adres ile bağlantı noktasını not edin — bunlara
    Adım 9'da ihtiyacınız olacak.

#### Adım 2: Mevcut Kurulumu Yedekleyin

digna kurulum dizininizde, yeni sürümün yanlarına dağıtılabilmesi için mevcut kurulumunuzun klasörlerini yeniden adlandırın:

```bash
# Rename the folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename the folder containing dignacli
ren dignacli dignacli_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

!!! info "dignabackend ve dignacli artık kullanılmıyor"

    2026.06 sürümünden itibaren `dignabackend` ve `dignacli`, arka uç ile CLI'yi birleştiren tek `digna` çalıştırılabilir dosyasıyla değiştirilmiştir. `dignabackend_old` ve `dignacli_old` klasörlerini yalnızca yükseltmeyi doğrulayana kadar saklayın — sonrasında her ikisini de silebilirsiniz. `dashboard_old` klasörünü, yapılandırma dosyalarınızı oradan geri yükleyene kadar saklayın (bkz. adım 4). `bin` klasörü de kaldırılır: içindeki batch dosyaları eski hizmeti yönetiyordu ve 2026.06 bunları içermez; bu nedenle hizmetin kaydı Adım 1'de kaldırıldıktan sonra yanıltmaktan başka bir işe yaramazlar.

#### Adım 3: Yeni Sürümü Çıkarın ve Dağıtın

1. Yeni digna kurulum ZIP dosyasını çıkarın
2. Yeni `digna` yürütülebilir dosyasını ve `dashboard` klasörünü kurulum dizinine kopyalayın


!!! warning "Önemli"

    Ne `config.toml` ne de `dashboard/dashboard_config.toml` hiçbir zaman kurulum ZIP'ine
    dahil edilmez — digna ekibi bu dosyaların hiçbirini göndermez. Bu nedenle mevcut yapılandırmanız
    yükseltmeden etkilenmez ve yeniden adlandırılan `*_old` klasörlerindeki kopyalar elinizdeki
    tek kopyalardır.

#### Adım 4: Yapılandırma Dosyalarınızı Geri Yükleyin

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
!!! warning "2026.06 sürümü config.toml dosyasını değiştiriyor"

    Üç ayar yeni ve zorunludur, üçü ise artık kullanılmamaktadır. Önceki bir sürümden devralınan `config.toml` yeni ayarları içermez ve bunlar eksik olduğu sürece digna başlatılmaz. Mevcut `config.toml` dosyanıza şunları ekleyin:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    İki `[base]` anahtarını mevcut `[base]` bölümünüze ekleyin ve `[encryption]` bölümünü yeni bir bölüm olarak ekleyin. Ardından artık kullanılmayan ayarları kaldırın: `[base]` bölümünden **`digna_FERNET_KEY`**, `[app]` bölümünden ise **`digna_APP_HOST`** ve **`digna_APP_PORT`** — sunucu adresini ve bağlantı noktasını artık `digna serve` komutundan alır.

    Her ayarın ne yaptığı şurada açıklanmıştır: [Arka Uç Yapılandırması](#backend-configuration).

!!! warning "Çoklu oturum açma: [oidc_clients] biçimi değişti"

    2026.06 sürümü, tablo dizisini her sağlayıcı için birer tabloyla değiştirir; tablolar sağlayıcı anahtarıyla adlandırılır. `DIGNA_OIDC_KEY` kaldırıldı — anahtar artık bölüm başlığının bir parçasıdır.

    Önce:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Sonra:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Bölümü her sağlayıcı için yineleyin ve her anahtarı `dashboard_config.toml` içindeki `key` ile aynı tutun. Eski biçim yerinde kaldığı sürece `digna config check`, `oidc_clients` bölümünü FAILED olarak bildirir. Yalnızca çoklu oturum açma kullanan kurulumlar etkilenir.

#### Adım 5: Web Sunucusunu Yeniden Yükleyin

Dashboard bir statik dosyalar kümesidir; bu nedenle web sunucunuz — ve tarayıcı — hâlâ önceki
sürümü sunuyor olabilir. `dashboard` klasörünü barındıran web sunucusunu yeniden yükleyin veya yeniden başlatın,
ardından sayfayı zorla yenileyin (++ctrl+f5++).

#### Adım 6: Yapılandırmayı Doğrulayın

Depoya dokunmadan önce güncellenmiş `config.toml` dosyasının eksiksiz olduğunu doğrulayın:

```bash
digna config check
```

Her bölüm OK bildirmelidir. FAILED olarak bildirilen her şeyi düzeltin ve devam etmeden önce komutu yeniden çalıştırın.

#### Adım 7: Lisans Dosyasını Değiştirin

Her sürüm ayrı olarak lisanslanır. digna ekibinin bu sürüm için sağladığı `license.toml` dosyasını
kurulum dizinine kopyalayarak eskisinin yerine koyun:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Önceki lisansı saklamayın"

    Önceki bir sürüm için verilmiş bir `license.toml` bu sürümü kapsamaz ve lisansı denetleyen
    her komut — `user`, `inspection`, `repo` — denetim başarısız olduğunda depoya dokunmadan önce
    sonlanır. Devam etmeden önce lisansı doğrulayın:

    ```bash
    digna license check
    ```

#### Adım 8: Repository Şemasını Yükseltin

digna kurulum dizinine gidin ve şu komutu çalıştırın:

```bash
digna repo upgrade
```

Bu komut PostgreSQL şemasını en son sürüme günceller ve mevcut tüm verileri korur.

#### Adım 9: Hizmeti Kaydedin ve Başlatın

Eski kayıt Adım 1'de kaldırıldığı için hizmet yeniden kaydedilir — bu kez batch dosyası
olmayan `digna` yürütülebilir dosyasıyla:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

Yeni `127.0.0.1` ve `8000` varsayılanlarını istemiyorsanız `--address` ve `--port` için eski hizmetin
hizmet verdiği değerleri verin; bu değerler kayda yazılır ve artık `config.toml` dosyasından
okunmaz. Eski hizmet bir etki alanı hesabıyla çalışıyorsa `--account` ve `--password` ekleyin. Seçeneklerin
tam listesi için bkz.
[digna'yı Windows Hizmeti Olarak Çalıştırma](#running-digna-as-a-windows-service).

Manuel olarak çalıştırıyorsanız, sunucuyu yeniden başlatın:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

IIS veya Tomcat kullanıyorsanız ilgili web sunucusunu yeniden başlatın.

#### Adım 10: Yükseltmeyi Doğrulayın

1. digna dashboard'a erişin
2. Arayüzün düzgün yüklendiğini doğrulayın
3. Sunucu günlüklerini herhangi bir hata için kontrol edin
4. Henüz ODBC kullanmayan her bağlantıyı ODBC'ye taşıyın, ardından tüm bağlantıları sınayın — bkz. [Bağlantıyı Sınama](../../../databases/overview.md#testing-a-connection)