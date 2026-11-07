# digna Sürüm 2026.11 için Windows Kurulum Kılavuzu

**Sürüm:** 2026.11

**Son Güncelleme:** 7 Kasım 2026


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

### 2026.11 Sürümünde Yenilikler

Bu sürüm digna Data Reconciliation'ı, digna MCP Server ile birlikte digna Agentic'i ve verileri digna içinde profilleyebilen ve farklı veritabanı teknolojileri arasında referans bütünlüğünü denetleyebilen digna Engine'i ekler. Tam ayrıntılar için [sürüm notlarına](../../../changelog/Release_202611.md) bakın.

Kurulum açısından bu sürüm yeni bir repository geçiş (migration) mekanizması, `config.toml` içinde digna Engine için isteğe bağlı bir `[duckdb]` bölümü ve yeni bir lisans dosyası getirir. Bunların her biri [yükseltme bölümünde](#upgrading-to-a-new-release) ele alınır.

### macOS veya Linux mu arıyorsunuz?

Bu kılavuz Windows içindir. Diğer platformlar için [macOS Kurulum Kılavuzu](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) veya [Linux Kurulum Kılavuzu](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md) belgelerine bakın.

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

!!! info "digna Engine"

    Profilleme konumu olarak digna Engine'i kullanan veritabanı bağlantıları doğrudan digna ana
    bilgisayarında profillenir. Bunlar için ek bellek ve disk alanı planlayın; bkz.
    [\[duckdb\] bölümü](#duckdb-section).

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

Bu bölüm, dashboard ile backend arasındaki kaynaklar arası kaynak paylaşımını (CORS) yapılandırır:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Dashboard URL'leri | Dashboard'un sunulduğu URL'ler. Başka herhangi bir kaynaktan (origin) gelen tarayıcı istekleri reddedilir |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Tarayıcının oturum çerezini her istekle birlikte göndermesi için gereklidir |

!!! info "[app] bölümü isteğe bağlıdır"

    Sürüm 2026.11'den itibaren her iki anahtar da, hatta `[app]` bölümünün tamamı da
    çıkarılabilir. Bir ters vekil sunucu (reverse proxy) dashboard'u ve backend'i aynı kaynak
    (origin) altında sunuyorsa doğru kurulum budur: tarayıcı bu durumda kaynaklar arası istek
    yapmaz ve varsayılan olarak hiçbirine izin verilmez.

#### [repo] Bölümü

Bu bölüm PostgreSQL veritabanı bağlantısını yapılandırır:

```toml
[repo]
DIGNA_REPO_HOST = "localhost"
DIGNA_REPO_PORT = 5432
DIGNA_REPO_DB = "postgres"
DIGNA_REPO_SCHEMA = "dignarepo"
DIGNA_REPO_USER = "digna_user"
DIGNA_REPO_PASSWORD = "YourSecurePassword123!"
DIGNA_REPO_SSLMODE = "prefer"
DIGNA_REPO_NUM_CONNS = 16
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` or IP | PostgreSQL sunucu hostname/IP |
| `DIGNA_REPO_PORT` | `5432` (default) | PostgreSQL portu |
| `DIGNA_REPO_DB` | `postgres` | Veritabanı adı |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Daha önce oluşturduğunuz şema |
| `DIGNA_REPO_USER` | `digna_user` | PostgreSQL kurulumu sırasında oluşturduğunuz kullanıcı |
| `DIGNA_REPO_PASSWORD` | Your password | Şema oluşturma sırasında belirlenen parola |
| `DIGNA_REPO_SSLMODE` | `prefer` (varsayılan) | İsteğe bağlı. PostgreSQL SSL modu: `disable`, `allow`, `prefer`, `require`, `verify-ca` veya `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (varsayılan) | İsteğe bağlı. digna'nın repository'ye açık tuttuğu bağlantı sayısı |

#### [base] Bölümü

Bu bölüm güvenlik, çerez (cookie) ve denetim ayarlarını içerir:

```toml
[base]
DIGNA_FERNET_KEY = "DU4a0yJ-OqvbKCL4hNQn_CsknH-V1vWmHZqBUl-AY44="
DIGNA_COOKIE_DOMAIN = "localhost"
DIGNA_COOKIE_SECURE = false
DIGNA_COOKIE_HTTPONLY = true
DIGNA_TOKEN_EXPIRES_IN = 86400
DIGNA_MAX_WORKERS = 4
DIGNA_FRONTEND_BASEURL = "http://localhost/"
DIGNA_SOURCE_QUERY_TIMEOUT_SEC = 3600
DIGNA_SOURCE_LOGIN_TIMEOUT_SEC = 30
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_FERNET_KEY` | Yukarıda gösterilen değer | Önceki sürümlerin kullandığı şifrelemenin anahtarı. Bulunması zorunludur; gösterilen değeri koruyun |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Dashboard'a erişilen ana bilgisayar adı. `""` hiçbir domain belirlemez; dashboard'u ve backend'i aynı kaynak (origin) altında sunan bir vekil sunucunun arkasında doğru ayar budur |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | digna HTTPS üzerinden sunulduğunda her zaman `true` olmalıdır |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Oturum çerezini betiklerin erişiminden uzak tutar |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 saat) | Oturum zaman aşımı (saniye cinsinden) |
| `DIGNA_MAX_WORKERS` | CPU çekirdeği sayısı - 1 | Aynı anda çalışabilecek denetim sayısı |
| `DIGNA_FRONTEND_BASEURL` | Dashboard URL'si | Zorunlu. Bildirim mesajlarındaki bağlantılar için kullanılır; bu nedenle alıcıların açabileceği bir URL olmalıdır |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (varsayılan) | İsteğe bağlı. Bir kaynak veritabanına yönelik tek bir sorgunun iptal edilmeden önce çalışabileceği saniye sayısı; `0` zaman aşımını devre dışı bırakır |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (varsayılan) | İsteğe bağlı. Bir kaynak veritabanına bağlanmak için beklenecek saniye sayısı; `0` süresiz bekler |

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
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` veya `DEBUG` | Üretim için `INFO`, sorun giderme için `DEBUG`. `TRACE`, `WARN` ve `ERROR` da kabul edilir |
| `DIGNA_LOGGING_DIR` | `logs` (varsayılan) | İsteğe bağlı. Dönüşümlü (rotating) günlük dosyalarının dizini; çalışma dizinine göre görelidir |
| `DIGNA_LOGGING_MAX_FILES` | `30` (varsayılan) | İsteğe bağlı. Saklanacak dönüşümlü günlük dosyası sayısı |

!!! warning "Hizmet olarak çalışırken günlük dizinini koruyun"

    Bir Windows hizmetinin konsolu yoktur; bu nedenle günlük dosyaları, hizmetin ne yaptığının tek
    kaydıdır. `DIGNA_LOGGING_DIR` değerini boş bir dizeye ayarlamayın; bu, günlük dosyalarını kapatır.

#### [duckdb] Bölümü (İsteğe Bağlı) {: #duckdb-section }

Sürüm 2026.11'de yeni. Bu bölüm, profilleme konumu **digna Engine** olan veritabanı bağlantıları
için verileri digna içinde profilleyen ve farklı veritabanı bağlantılarındaki veri kaynakları
arasında referans bütünlüğü denetimlerini çalıştıran **digna Engine**'in kaynaklarını belirler.
Bkz. [Profilleme Konumu](../../../platform/profiling/profiling_location.md).

Bu bölüm isteğe bağlıdır. Bölüm yoksa aşağıdaki varsayılanlar geçerlidir.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parameter | Value | Notes |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (varsayılan) | Tek bir digna Engine çalıştırmasının kullanabileceği bellek (MB). Aynı anda en fazla `DIGNA_MAX_WORKERS` kadar çalıştırma etkin olabilir |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Varsayılan: digna'yı çalıştıran hesabın geçici dizini (`%TEMP%`) | Veriler belleğe sığmadığında geçici dosyalar için kullanılan dizin |

!!! tip "digna Engine'i boyutlandırma"

    digna ana bilgisayarında, digna'nın kendi kullandığı belleğe ek olarak en fazla
    `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` kadar bellek planlayın; geçici dizinde
    de digna Engine kullanan veri kaynaklarının denetlenen en büyük tarihinin verisini alacak kadar
    boş disk alanı ayırın. `DIGNA_DUCKDB_TEMP_DIRECTORY` değerini bu alana sahip olan ve digna'yı
    çalıştıran hesabın yazabildiği bir diske yönlendirin:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Bu bölüme yalnızca en az bir veritabanı bağlantısı digna Engine kullanıyorsa veya bir referans
    bütünlüğü denetimi farklı bağlantılardaki veri kaynaklarını karşılaştırıyorsa ihtiyacınız vardır.

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
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

FAILED olarak bildirilen her şeyi düzeltin ve devam etmeden önce komutu yeniden çalıştırın. **Unknown keys** altındaki bir WARNING, `config.toml` içinde digna'nın okumadığı anahtarları listeler; bunların hiçbir etkisi yoktur, bu nedenle kaldırın ya da yazımlarını düzeltin. Seçeneklerin tam listesi [CLI başvurusunda](../../../cli/Command_Line_Interface_202611.md) yer alır.

### Adım 3: Repository Bağlantısını Test Edin

1. Komut İstemi'ni açın
2. digna kurulum dizinine gidin ( `config.toml` ve `digna` yürütülebilir dosyasının bulunduğu dizin )
3. Bağlantı testi çalıştırın:

```bash
digna repo check
```

Yeni bir şemada komut bağlanır ve ardından henüz bir repository kurulu olmadığını bildirir:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Bu aşamada beklenen sonuç budur: digna'nın PostgreSQL'e ve şemaya ulaştığını doğrular. Bunun yerine bir bağlantı veya kimlik doğrulama hatası alırsanız sorun `[repo]` bölümündedir ya da PostgreSQL kurulumundadır.

### Adım 4: Repository Şemasını Kurun

Aynı dizinde şu komutu çalıştırın:

```bash
digna repo upgrade
```

Bu komut gerekli tabloları repository şemasına kurar ve şu çıktıyla tamamlanır:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade hem kurar hem yükseltir"

    Sürüm 2026.11'den itibaren `repo upgrade` yeni bir repository'yi kurar ve mevcut bir
    repository'yi yükseltir. `repo install`, aynı komutun diğer adı olarak çalışmaya devam eder.

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
- `--address` — Sunucu hostname/IP (varsayılan `127.0.0.1`)
- `--port` — Sunucu portu (varsayılan `8000`)

Sunucu çalışmaya başladığında dinlediği adresi yazdırır:

```text
Server running on http://127.0.0.1:8082
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
tam listesi [CLI başvurusunda](../../../cli/Command_Line_Interface_202611.md) yer alır.

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

Bu bölüm, Sürüm 2026.06 kurulumunu Sürüm 2026.11'e yükseltir. Kurulumunuz daha eskiyse önce
[2026.06'dan Önceki Bir Sürümden Yükseltme](#upgrading-from-a-release-before-2026-06)
bölümünü okuyun.

### Yükseltme Öncesi

**digna Repository Yedeği Almak Zorunludur**

digna'yı yükseltmeden önce veri kaybını önlemek için repository'nizin (PostgreSQL) yedeğini alın.
Bir yedek, yükseltme sırasında beklenmeyen sorunlar çıkarsa geri dönüş yapabilmenizi sağlar.

**Sürüm 2026.11 için Lisans Dosyasını Talep Etme**

Sürüm 2026.11 yeni bir `license.toml` gerektirir. Başlamadan önce bu dosyayı digna ekibinden talep
edin ve [Adım 7](#step-7-replace-the-license-file) için hazır bulundurun.

### 2026.06'dan Önceki Bir Sürümden Yükseltme {: #upgrading-from-a-release-before-2026-06 }

Sürüm 2026.06, eski bir kurulumu doğrudan 2026.11'e yükselttiğinizde hâlâ geçerli olan üç
değişiklik getirdi:

- **Yalnızca ODBC.** digna her kaynak teknolojisine ODBC üzerinden erişir. Henüz ODBC kullanmayan
  her veritabanı bağlantısı yükseltmeden sonra ODBC'ye taşınmalıdır; otomatik dönüştürme yoktur.
  ODBC sürücülerini önceden digna ana bilgisayarına kurun, bkz.
  [ODBC Sürücüsünü digna Ana Bilgisayarına Kurma](../../../databases/overview.md#install-the-driver),
  ve her bağlantının özelliklerini
  [teknoloji kılavuzlarından](../../../databases/overview.md#technology-guides) alarak hazır
  bulundurun. Databricks Legacy bağlayıcısı artık yoktur; bu bağlantıları
  [Databricks](../../../databases/databricks_connector_guide.md) bağlayıcısına taşıyın.
- **Tek yürütülebilir dosya.** `dignabackend` ve `dignacli`, backend ile CLI'yi birleştiren tek
  `digna` yürütülebilir dosyasıyla değiştirilmiştir.
- **config.toml.** `[encryption]` bölümü zorunludur; `DIGNA_APP_HOST` ve `DIGNA_APP_PORT` ise artık
  okunmaz: sunucu adresini ve portunu `digna serve` komutundan alır. Dosyanızı
  [Backend Yapılandırması](#backend-configuration) ile karşılaştırın.

Aşağıdaki adımlar, eski bir kurulumun nerede farklı bir işlem gerektirdiğini belirtir. Adım 8'deki
repository yükseltmesi, önceki herhangi bir sürümün repository'sini doğrudan 2026.11'e getirir.

### Yükseltme Süreci

#### Adım 1: digna Hizmetini Durdurun {: #step-1-stop-the-digna-service }

Yönetici olarak bir Komut İstemi açın ve hizmeti mevcut kurulumunuzun `digna` yürütülebilir
dosyasıyla durdurun:

```bash
cd C:\path\to\digna
digna windows stop
```

Hizmet kayıtlı kalır. Yeni yürütülebilir dosya aynı dizinde eskisinin yerini alır; bu nedenle kayıt
doğru dosyayı göstermeye devam eder.

digna ön planda çalışıyorsa, Komut İstemi penceresinde ++ctrl+c++ tuşlarına basın.

!!! warning "2026.06'dan önceki bir sürümden yükseltme"

    2026.06'dan önceki sürümler hizmeti batch dosyalarıyla kaydediyordu. Adım 2'de herhangi bir şeyi
    yeniden adlandırmadan **önce**, hizmeti mevcut kurulumunuzun batch dosyalarıyla durdurun ve
    kaydını kaldırın:

    ```bash
    cd C:\path\to\digna\bin
    stop_service.bat
    uninstall_service.bat
    ```

    Hizmetin çalıştığı hesabı ve hizmet verdiği adres ile portu not edin. Hizmeti Adım 9'da yeniden
    kaydedeceksiniz.

#### Adım 2: Mevcut Kurulumu Yedekleyin {: #step-2-backup-current-installation }

digna kurulum dizininizde, yeni sürümün yanına dağıtılabilmesi için mevcut kurulumunuzun
yürütülebilir dosyasını ve dashboard klasörünü yeniden adlandırın:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

`digna_old.exe` dosyasını yükseltmeyi doğrulayana kadar, `dashboard_old` klasörünü ise yapılandırma
dosyalarınızı oradan geri yükleyene kadar saklayın (bkz. Adım 4). Sonrasında ikisini de silebilirsiniz.

!!! info "2026.06'dan önceki bir sürümden yükseltme"

    Yürütülebilir dosya yerine `dignabackend` ve `dignacli` klasörlerini yeniden adlandırın:
    `ren dignabackend dignabackend_old` ve `ren dignacli dignacli_old`. Sürüm 2026.11 bu klasörlerin hiçbirini, batch dosyalarını içeren `bin` klasörünü de kullanmaz.

#### Adım 3: Yeni Sürümü Çıkarın ve Dağıtın {: #step-3-extract-and-deploy-new-version }

1. Yeni digna kurulum ZIP dosyasını çıkarın
2. Yeni `digna` yürütülebilir dosyasını ve `dashboard` klasörünü kurulum dizinine kopyalayın

!!! warning "Önemli"

    Ne `config.toml` ne de `dashboard/dashboard_config.toml` hiçbir zaman kurulum ZIP'ine
    dahil edilmez — digna ekibi bu dosyaların hiçbirini göndermez. Bu nedenle mevcut yapılandırmanız
    yükseltmeden etkilenmez ve yeniden adlandırılan `*_old` klasörlerindeki kopyalar elinizdeki
    tek kopyalardır.

#### Adım 4: Yapılandırma Dosyalarınızı Geri Yükleyin {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

Sürüm 2026.11, `config.toml` dosyasında değişiklik gerektirmez: Sürüm 2026.06 ile çalışan bir dosya
çalışmaya devam eder. İki değişiklik isteğe bağlıdır:

- Veritabanı bağlantıları digna Engine'i kullanacaksa ve varsayılanlar ana bilgisayarınıza uygun
  değilse bir [`[duckdb]` bölümü](#duckdb-section) ekleyin.
- Bir ters vekil sunucu dashboard'u ve backend'i aynı kaynak (origin) altında sunuyorsa `[app]`
  bölümünü çıkarın.

!!! warning "digna'nın okumadığı ayarlar"

    Bu kılavuzun önceki sürümlerinde digna'nın okumadığı bazı ayarlar gösteriliyordu. Bunların hiçbir
    etkisi yoktur ve `config check`, Adım 6'da bunları **Unknown keys** altında listeler. Bunları
    kaldırın veya düzeltin:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` ve
      `digna_LOGGING_BACKUP_COUNT` mevcut değildir. Bunları kaldırın.
    - Ayar adları büyük/küçük harfe duyarlıdır. digna `digna_REPO_HOST` değil, `DIGNA_REPO_HOST` okur.
      [Backend Yapılandırması](#backend-configuration) bölümündeki gibi her adı büyük harfle yazın.

!!! warning "Çoklu oturum açma: [[oidc_clients]] biçimini koruyun"

    digna, çoklu oturum açma sağlayıcılarını her biri kendi `DIGNA_OIDC_KEY` değerine sahip
    `[[oidc_clients]]` girdilerinden oluşan bir liste olarak okur. Sağlayıcılarınızı, bu kılavuzun
    önceki bir sürümünde gösterildiği gibi `[oidc_clients.<key>]` bölümlerine dönüştürdüyseniz eski
    hâline getirin. Bu biçim yerinde kaldığı sürece `config check`, `OIDC config(s)` öğesini FAILED
    olarak bildirir:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Girdiyi her sağlayıcı için yineleyin ve her `DIGNA_OIDC_KEY` değerini `dashboard_config.toml`
    içindeki `key` ile aynı tutun. Yalnızca çoklu oturum açma kullanan kurulumlar etkilenir.

#### Adım 5: Web Sunucusunu Yeniden Yükleyin {: #step-5-reload-the-web-server }

Dashboard bir statik dosyalar kümesidir; bu nedenle web sunucunuz — ve tarayıcı — hâlâ önceki
sürümü sunuyor olabilir. `dashboard` klasörünü barındıran web sunucusunu yeniden yükleyin veya yeniden başlatın,
ardından sayfayı zorla yenileyin (++ctrl+f5++).

#### Adım 6: Yapılandırmayı Doğrulayın {: #step-6-validate-the-configuration }

Depoya dokunmadan önce `config.toml` dosyasının eksiksiz olduğunu doğrulayın:

```bash
digna config check
```

Her bölüm OK bildirmelidir. FAILED olarak bildirilen her şeyi düzeltin, **Unknown keys** altında
listelenen anahtarları kaldırın ve devam etmeden önce komutu yeniden çalıştırın.

#### Adım 7: Lisans Dosyasını Değiştirin {: #step-7-replace-the-license-file }

Bir lisans dosyası normalde bir sürümden diğerine aktarılır. Sürüm 2026.11 bir istisnadır: iki
lisanslı modül, digna Data Reconciliation ve digna Agentic ekler ve 2026.11'den önce verilmiş bir
lisans bunları içermez. digna ekibinin Sürüm 2026.11 için sağladığı `license.toml` dosyasını
kurulum dizinine kopyalayarak eskisinin yerine koyun:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Önceki lisansı saklamayın"

    Önceki lisansla digna yine başlar, ancak digna Data Reconciliation ve digna MCP Server kapalı
    kalır. Lisansı denetleyen her komut — `user`, `inspection`, `repo` — denetim başarısız olduğunda
    depoya dokunmadan önce sonlanır. Devam etmeden önce yeni lisansı doğrulayın:

    ```bash
    digna license check
    ```

#### Adım 8: Repository Şemasını Yükseltin {: #step-8-upgrade-the-repository-schema }

digna kurulum dizininizde şunu çalıştırın:

```bash
digna repo upgrade
```

Sürüm 2026.11, repository şemasını sürümlendirilmiş geçişlerle (migration) yönetir. Önceki bir
sürümden yapılan ilk yükseltme, şemayı önceki düzenin son sürümüne getirir, bunu başlangıç noktası
olarak kaydeder ve ardından Sürüm 2026.11'in geçişlerini uygular. Şu çıktıyla tamamlanır:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Mevcut tüm veriler korunur. Repository'nin durumunu istediğiniz zaman görmek için
`digna repo check` komutunu çalıştırın: uygulanan en son geçişi ve bekleyen geçişleri listeler.

!!! warning "digna, güncel olmayan bir repository ile başlamaz"

    Sürüm 2026.11'den itibaren sunucu, repository'nin yükseltilmesi gerektiği sürece başlamayı
    reddeder ve bunu bildirir, örneğin:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Sunucuyu veya hizmeti başlatmadan önce `repo upgrade` komutunu çalıştırın.

#### Adım 9: Hizmetleri Yeniden Başlatın {: #step-9-restart-services }

digna bir Windows hizmeti olarak çalışıyorsa hizmeti tekrar başlatın:

```bash
cd C:\path\to\digna
digna windows start
```

2026.06'dan önceki bir sürümden yükselttiyseniz ve Adım 1'de hizmetin kaydını kaldırdıysanız, önce
hizmeti `digna` yürütülebilir dosyasıyla yeniden kaydedin:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

`127.0.0.1` ve `8000` varsayılanlarını istemiyorsanız `--address` ve `--port` için eski hizmetin
hizmet verdiği değerleri verin. Eski hizmet bir etki alanı hesabıyla çalışıyorsa `--account` ve
`--password` ekleyin. Seçeneklerin tam listesi için bkz.
[digna'yı Windows Hizmeti Olarak Çalıştırma](#running-digna-as-a-windows-service).

Manuel olarak çalıştırıyorsanız, sunucuyu yeniden başlatın:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

IIS veya Tomcat kullanıyorsanız ilgili web sunucusunu yeniden başlatın.

#### Adım 10: Yükseltmeyi Doğrulayın {: #step-10-verify-the-upgrade }

1. Yeni yürütülebilir dosyanın sürümünü doğrulayın:

    ```bash
    digna version
    ```

    İlk satır `Release: 2026.11` olmalıdır.

2. digna dashboard'a erişin ve arayüzün düzgün yüklendiğini doğrulayın.
3. Kurulumun `logs` dizinindeki dosyaları hatalara karşı kontrol edin.
4. Veritabanı bağlantılarınızı sınayın — bkz.
   [Bağlantıyı Sınama](../../../databases/overview.md#testing-a-connection). 2026.06'dan önceki
   bir sürümden yükselttiyseniz, önce henüz ODBC kullanmayan her bağlantıyı ODBC'ye taşıyın.

Yeni modüllerle çalışmaya başlamak için bkz. [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
digna MCP Server için [Bir Yapay Zekâ Ajanı Bağlama](../../../platform/agentic/connect_ai_agent.md) ve
digna Engine için [Profilleme Konumu](../../../platform/profiling/profiling_location.md).