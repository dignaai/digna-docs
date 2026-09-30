# digna Sürüm 2026.06 için macOS Kurulum Kılavuzu

**Sürüm:** 2026.06

**Son Güncelleme:** 5 Eylül 2026


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
9. [digna'yı Arka Plan Hizmeti Olarak Çalıştırma](#running-digna-as-a-background-service)
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

### Windows veya Linux mu arıyorsunuz?

Bu kılavuz macOS içindir. Diğer platformlar için [Windows Kurulum Kılavuzu](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) veya [Linux Kurulum Kılavuzu](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md) belgelerine bakın.

---

## Sistem Gereksinimleri {: #system-requirements }

Kuruluma başlamadan önce sisteminizin aşağıdaki minimum gereksinimleri karşıladığından emin olun:

| Gereksinim | Özellik |
|---|---|
| **İşletim Sistemi** | macOS 13 (Ventura) veya üzeri |
| **Mimari** | Apple Silicon (arm64) veya Intel (x86_64) |
| **Bellek (Minimum Kurulum)** | 16 GB RAM |
| **Disk Alanı** | 10 GB kullanılabilir depolama |
| **Veritabanı** | PostgreSQL Server 12 veya üzeri |
| **Web Sunucusu** | nginx, Apache httpd veya eşdeğeri |
| **Komut Satırı Araçları** | Xcode Command Line Tools (Homebrew için gereklidir) |

### Veritabanı Kurulum Seçenekleri

**PostgreSQL zaten kuruluysa:**
Mevcut PostgreSQL sunucunuza digna için yeni bir veritabanı ekleyebilirsiniz.

**PostgreSQL'i digna ile aynı makineye kuruyorsanız:**

!!! info "Önerilen Özellikler"

    - **Bellek**: 32 GB RAM (16 GB yerine)
    - **Disk Alanı**: 50 GB kullanılabilir depolama (10 GB yerine)

    Bu daha yüksek özellikler, digna ile PostgreSQL veritabanının aynı anda çalışmasını rahatlıkla karşılayacak şekilde önerilir.

### Mimarinizi Denetleme

Bu kılavuzdaki birkaç yol Apple Silicon ve Intel Mac'ler arasında farklılık gösterir. Hangisine sahip olduğunuzu öğrenmek için **Terminal**'i açın ve şunu çalıştırın:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew `/opt/homebrew` konumuna kurulur.
- `x86_64` — Intel. Homebrew `/usr/local` konumuna kurulur.

!!! tip "İpucu"

    Bu kılavuz, iki yoldan birini sabit olarak yazmak yerine her iki mimaride de doğru konuma genişleyen `$(brew --prefix)` ifadesini kullanır. Komutları olduğu gibi kopyalayabilirsiniz.

---

## Kurulum Öncesi Hazırlık {: #pre-installation-setup }

digna'yı kurmadan önce üç temel önkoşulun yerinde olduğundan emin olun:

1. **Homebrew** – aşağıdaki bileşenleri kurmak için kullanılan paket yöneticisi
2. **PostgreSQL Server** – hesaplanmış metrikler ve performans verileri için depolama
3. **Web Server** – digna Dashboard'u barındırmak için

Bu bileşenler henüz kurulu değilse, aşağıdaki bölümlerde bunları kurup yapılandırma adımlarını izleyin.

### Homebrew Kurulumu

Homebrew, macOS için standart paket yöneticisidir ve bu kılavuz boyunca PostgreSQL ile nginx'i kurmak için kullanılır.

#### Adım 1: Homebrew'un Zaten Kurulu Olup Olmadığını Denetleyin

**Terminal**'i açın (`Cmd + Space` tuşlarına basın, `Terminal` yazın, Enter tuşuna basın) ve şunu çalıştırın:

```bash
brew --version
```

Bir sürüm numarası dönerse [PostgreSQL Sunucu Kurulumu](#postgresql-server-setup) bölümüne geçin.

#### Adım 2: Homebrew'u Kurun

Komut bulunamadıysa Homebrew'u [resmi Homebrew sitesindeki](https://brew.sh) yönergeleri izleyerek kurun. Yükleyici, Xcode Command Line Tools henüz yoksa bunları da kurar.

#### Adım 3: Homebrew'u PATH'inize Ekleyin

Apple Silicon'da yükleyici, Homebrew'u kabuk ortamınıza eklemek için iki komut yazdırır. Bunları belirtildiği gibi çalıştırın, ardından doğrulayın:

```bash
brew --prefix
```

Bu komut Apple Silicon'da `/opt/homebrew`, Intel'de ise `/usr/local` yazdırmalıdır.

---

## PostgreSQL Sunucu Kurulumu {: #postgresql-server-setup }

### PostgreSQL Zaten Kuruluysa

PostgreSQL yerel makinenizde zaten kurulu ve çalışıyorsa veya yönetilen uzak bir PostgreSQL sunucusu kullanıyorsanız, [bir sonraki bölüme](#web-server-configuration) geçebilirsiniz.

### Kurulum Seçenekleri

macOS, PostgreSQL'i kurmak için iki kolay yol sunar. **Birini** seçin:

- [Homebrew](#postgresql-homebrew) — komut satırından kurulum, sunucu dağıtımları için önerilir
- [Postgres.app](#postgresql-app) — grafik arayüzle kurulum, yerel değerlendirme için pratiktir

### PostgreSQL'i Homebrew ile Kurma {: #postgresql-homebrew }

#### Adım 1: PostgreSQL Formülünü Kurun

```bash
brew install postgresql@16
```

#### Adım 2: PostgreSQL'i PATH'inize Ekleyin

Sürümlü PostgreSQL formülleri *keg-only*'dir; yani Homebrew bunların komutlarını PATH'inize otomatik olarak bağlamaz. Bunları kendiniz ekleyin:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Not"

    Bu, macOS'un kullandığı varsayılan `zsh` kabuğunu varsayar. `bash` kullanıyorsanız aynı satırı bunun yerine `~/.bash_profile` dosyasına ekleyin.

#### Adım 3: PostgreSQL Hizmetini Başlatın

```bash
brew services start postgresql@16
```

Bu komut PostgreSQL'i hemen başlatır ve oturum açtığınızda otomatik olarak yeniden başlayacak şekilde yapılandırır.

#### Adım 4: Kurulumu Doğrulayın

```bash
psql --version
```

Kurulum başarılıysa PostgreSQL sürümünü görmelisiniz.

#### Adım 5: Sunucuya Bağlanın

```bash
psql postgres
```

!!! warning "Önemli — macOS Burada Windows'tan Farklıdır"

    Windows yükleyicisi bir `postgres` süper kullanıcısı ve parolası oluşturmanızı ister. Homebrew bunu yapmaz. Bunun yerine **macOS hesabınızın** adını taşıyan, parolası olmayan ve yalnızca yerel makineden erişilebilen bir süper kullanıcı oluşturur.

    Bu, yeni bir Homebrew kurulumunda `postgres` rolünün bulunmadığı anlamına gelir. Bir süper kullanıcıya ihtiyaç duyduğunuzda kendi hesap adınızı kullanın ve [İlk Kurulum](#initial-installation) bölümünde açıklandığı gibi açık bir digna kullanıcısı oluşturun.

#### Adım 6: Portu Doğrulayın

Varsayılan PostgreSQL portu `5432`'dir. Sunucunuzun dinlediği portu doğrulamak için:

```bash
psql postgres -c "SHOW port;"
```

Değeri not edin — digna backend'ini yapılandırırken ihtiyacınız olacak.

### PostgreSQL'i Postgres.app ile Kurma {: #postgresql-app }

Grafik arayüzle kurulumu tercih ediyorsanız:

1. [Postgres.app](https://postgresapp.com) uygulamasını indirin ve **Applications** klasörünüze sürükleyin
2. Uygulamayı açın ve yeni bir sunucu oluşturmak için **Initialize** düğmesine tıklayın
3. Komut satırı araçlarını PATH'inize eklemek için uygulamanın yönergelerini izleyin
4. Kurulumu doğrulayın:

```bash
psql --version
```

Postgres.app de macOS hesabınızın adını taşıyan bir süper kullanıcı oluşturur.

---

## Web Sunucusu Yapılandırması {: #web-server-configuration }

digna dashboard'unu barındırmak için bir web sunucusuna ihtiyaç vardır. Aşağıdaki seçeneklerden birini seçin:

- [nginx](#nginx-setup) — Homebrew ile kurulur, önerilir
- [Apache httpd](#apache-setup) — macOS ile birlikte gelir

Bu sunuculardan yalnızca **birini** kurmanız ve yapılandırmanız yeterlidir.

Her iki bölüm de dashboard'un bağlı olduğu iki şeyi yapılandırır:

- **Tek sayfalı uygulama (SPA) geri dönüşü**; böylece bir dashboard URL'sini yenilemek 404 döndürmez
- **`.md` MIME türü**; böylece Markdown dosyaları doğru şekilde sunulur

### nginx Kurulumu {: #nginx-setup }

#### Genel Bakış

nginx, statik digna dashboard'unu sunmaya çok uygun, hafif ve yüksek performanslı bir web sunucusudur.

#### Kurulum

```bash
brew install nginx
```

#### nginx'i Başlatma

```bash
brew services start nginx
```

#### Kurulumu Doğrulayın

1. Tarayıcınızı açın
2. `http://localhost:8080` adresine gidin
3. nginx karşılama sayfasını görmelisiniz

!!! note "Not — Varsayılan Port 80 Değil, 8080'dir"

    Homebrew, nginx'i yönetici ayrıcalıkları olmadan çalışabilmesi için `8080` portunu dinleyecek şekilde yapılandırır. macOS'ta `80` portuna veya 1024'ün altındaki herhangi bir porta bağlanmak root yetkisi gerektirir.

    Dashboard'u 80 portunda sunmak için aşağıdaki yapılandırmada `listen 8080;` satırını `listen 80;` olarak değiştirin ve nginx'i bunun yerine `sudo brew services start nginx` ile başlatın.

#### Dashboard için Bir Site Yapılandırma

Homebrew'un nginx yapılandırması, `servers` dizinindeki tüm dosyaları dahil eder. Orada digna için ayrı bir yapılandırma dosyası oluşturun:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Aşağıdakini yapıştırın ve `/path/to/digna/dashboard` yolunu, çıkardığınız `dashboard` klasörünün gerçek yoluyla değiştirin:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Önemli"

    `try_files` yönergesi olmadan, kök URL dışındaki herhangi bir dashboard sayfasını yeniden yüklemek 404 döndürür. Bu, Windows'ta IIS için gereken URL Rewrite modülünün nginx karşılığıdır.

#### Yapılandırmayı Uygulayın

Yapılandırmada söz dizimi hatası olup olmadığını test edin, ardından nginx'i yeniden yükleyin:

```bash
nginx -t
brew services restart nginx
```

---

### Apache httpd Kurulumu {: #apache-setup }

#### Genel Bakış

macOS, Apache httpd'yi içerir; bu nedenle kurulum gerekmez. Varsayılan olarak devre dışıdır.

#### Apache'yi Başlatma

```bash
sudo apachectl start
```

#### Kurulumu Doğrulayın

1. Tarayıcınızı açın
2. `http://localhost` adresine gidin
3. "It works!" iletisini görmelisiniz

#### Gerekli: mod_rewrite'ı Etkinleştirin

Dashboard, URL yeniden yazmayı gerektirir. Apache yapılandırmasını açın:

```bash
sudo nano /etc/apache2/httpd.conf
```

Aşağıdaki satırı bulun ve yorumdan çıkarmak için baştaki `#` işaretini kaldırın:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Gerekli: .htaccess Geçersiz Kılmalarına İzin Verin

Aynı dosyada `<Directory "/Library/WebServer/Documents">` bloğunu bulun ve şunu:

```apache
AllowOverride None
```

şununla değiştirin:

```apache
AllowOverride All
```

#### Gerekli: Markdown Dosyaları için MIME Türü

Markdown dosyalarının doğru şekilde sunulması için yine `httpd.conf` içinde şu satırı ekleyin:

```apache
AddType text/markdown .md
```

!!! warning "Önemli"

    Bu ayar olmadan `.md` dosyaları doğru şekilde servis edilmeyebilir.

#### Yapılandırmayı Uygulayın

Yapılandırmada söz dizimi hatası olup olmadığını denetleyin, ardından Apache'yi yeniden başlatın:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## İlk Kurulum {: #initial-installation }

### Adım 1: digna Repository'sini Oluşturun

digna repository'si, digna tarafından hesaplanan tüm metrikleri saklar. Analitik ve performans verileri için merkezi veritabanı görevi görür.

#### Repository Şeması ve Kullanıcısı Oluşturma

PostgreSQL istemcinizi (psql, pgAdmin veya benzeri) açın ve aşağıdaki SQL komutlarını çalıştırın:

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

Bunları Terminal'den tek adımda çalıştırmak için:

```bash
psql postgres
```

Ardından ifadeleri `postgres=#` isteminde yapıştırın ve çıkmak için `\q` yazın.

!!! tip "En İyi Uygulama"

    Veritabanı kullanıcıları için güçlü, karmaşık parolalar kullanın. Kolay tahmin edilebilir kimlik bilgilerini kullanmaktan kaçının.

---

### Adım 2: digna Kurulum Paketini Çıkarın

1. Size sağlanan digna kurulum ZIP dosyasını bulun
2. İstediğiniz kurulum konumuna çıkarın — örneğin `/opt/digna` veya `~/digna`
3. Çıkarma sonrası aşağıdaki öğeleri görmelisiniz:
   - `dashboard/` — Web dashboard arayüzü
   - `digna` — Ana yürütülebilir dosya (backend + CLI birleşik)

!!! info "Yapılandırma ve lisans dosyaları pakette yer almaz"

    Ne `config.toml` ne de `dashboard/dashboard_config.toml` kurulumla birlikte gelir — ikisini de
    kendiniz, [Backend Yapılandırması](#backend-configuration) ve
    [Dashboard Yapılandırması](#dashboard-configuration) bölümlerinde oluşturursunuz. `license.toml` da pakete dahil değildir;
    Adım 3'te açıklandığı gibi digna tarafından ayrı olarak sağlanır.

Terminal'den çıkarmak için:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
```

#### Yürütülebilir Dosyayı Çalıştırılabilir Yapın

Arşivin nasıl aktarıldığına bağlı olarak, çalıştırma izni biti çıkarma sırasında korunmayabilir. Bunu açıkça ayarlayın:

```bash
cd /opt/digna
chmod +x digna
```

#### macOS Uygulamayı Engellerse

Bir tarayıcı veya e-posta istemcisi aracılığıyla indirilen dosyalar bir karantina özniteliğiyle etiketlenir. macOS, uygulamanın *"cannot be opened because the developer cannot be verified"* olduğunu bildirirse özniteliği kurulum dizininden kaldırın:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Alternatif olarak **System Settings → Privacy & Security** bölümünü açın, engellenen öğeyi sayfanın altına yakın bir yerde bulun ve **Open Anyway** düğmesine tıklayın.

!!! note "Not"

    Bu adım yalnızca macOS yürütülebilir dosyayı gerçekten engellerse gereklidir. SSH üzerinden veya dahili dosya paylaşımlarından aktarılan paketler genellikle karantinaya alınmaz.

### Adım 3: Lisans Dosyasını Yükleyin

!!! warning "Önemli"

    Lisans dosyası kurulum paketine **dahil değildir** ve digna tarafından ayrı olarak sağlanacaktır.

1. Size sağlanan `license.toml` dosyasını bulun
2. Bunu digna kurulum dizininin köküne kopyalayın (`config.toml` ve `digna` yürütülebilir dosyasının bulunduğu dizin)

**Neden önemli:**
Lisans dosyası müşteri bilgilerini, lisans bitiş tarihini ve dijital imzayı içerir. **Bu dosyayı değiştirmeyin** — herhangi bir değişiklik lisansın geçersiz olmasına neden olur.

**Kurulum sonrası dizin yapısı:**

```
/opt/digna/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
├── bin/                (service management scripts)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backend Yapılandırması {: #backend-configuration }

### Adım 1: Yapılandırma Dosyasını Oluşturun ve Düzenleyin

`config_template.toml` dosyası digna kurulum dizininde sağlanır. Bunu `config.toml` olarak yeniden adlandırmanız yeterlidir.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Konum:** `/opt/digna/config.toml`

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

| Parametre | Değer | Notlar |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend URL'si | Dashboard farklı bir sunucuda ise onun URL'sini ekleyin |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Kimlik bilgileri ile CORS için gerekli |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Tüm HTTP yöntemlerine izin ver |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Tüm başlıklara izin ver |

!!! note "Not"

    Dashboard'u Homebrew'un nginx'i üzerinden varsayılan portunda sunuyorsanız izin verilecek kaynak `http://localhost:8080`'dir.

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

| Parametre | Değer | Notlar |
|---|---|---|
| `digna_REPO_HOST` | `localhost` veya IP | PostgreSQL sunucu hostname/IP |
| `digna_REPO_PORT` | `5432` (varsayılan) | PostgreSQL portu |
| `digna_REPO_DB` | `postgres` | Veritabanı adı |
| `digna_REPO_SCHEMA` | `dignarepo` | Daha önce oluşturduğunuz şema |
| `digna_REPO_USER` | `digna_user` | PostgreSQL kurulumu sırasında oluşturduğunuz kullanıcı |
| `digna_REPO_PASSWORD` | Parolanız | Şema oluşturma sırasında belirlenen parola |

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

| Parametre | Değer | Notlar |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Frontend domain'i ile eşleşsin |
| `digna_COOKIE_SECURE` | `false` (yerel) / `true` (üretim) | HTTPS bağlantıları için `true` kullanın |
| `digna_COOKIE_HTTPONLY` | `true` | Güvenlik için her zaman etkin |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF saldırılarını önlemeye yardımcı olur |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 saat) | Oturum zaman aşımı (saniye cinsinden) |
| `digna_MAX_WORKERS` | CPU çekirdeği sayısı - 1 | Paralel denetim görevlerinin sayısı |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Zamanlayıcının, vadesi gelmiş bir işi başlatmadan önce ekleyebileceği saniye cinsinden azami gecikme |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Günlük temizliğin başladığı saat (24 saat biçiminde `HH:MM`) |

!!! tip "İpucu"

    Mac'inizde kullanılabilir CPU çekirdeği sayısını öğrenmek için `sysctl -n hw.ncpu` komutunu çalıştırın.

#### [encryption] Bölümü

Bu bölüm, depoda saklanan hassas değerleri şifrelemek için kullanılan anahtarı içerir. **Zorunludur** — anahtar eksikse `config check`, `[encryption]` bölümünü FAILED olarak bildirir.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parametre | Değer | Notlar |
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

| Parametre | Değer | Notlar |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` veya `DEBUG` | Üretim için `INFO`, sorun giderme için `DEBUG` |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Saklanacak günlük yedek sayısı (günlük bazda) |

---

### Adım 2: Yapılandırmayı Doğrulayın

Depoyu başlatmadan önce `config.toml` dosyasının eksiksiz ve doğru kurulmuş olduğunu denetleyin. digna kurulum dizininizde şunu çalıştırın:

```bash
./digna config check
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

### Adım 3: Repository'yi Başlatın

1. **Terminal**'i açın
2. digna kurulum dizinine gidin (`config.toml` ve `digna` yürütülebilir dosyasının bulunduğu dizin)
3. Bağlantı testini çalıştırın:

```bash
cd /opt/digna
./digna repo check
```

Bağlantının kurulduğuna dair bir onay görmelisiniz (repository henüz başlatılmamıştır).

!!! note "Not"

    macOS'ta geçerli dizindeki komutlar PATH'inizde bulunmaz; bu nedenle yürütülebilir dosya `digna` yerine `./digna` olarak çağrılır. Kısa biçimi her yerde kullanmak için kurulum dizinini PATH'inize ekleyin:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Adım 4: Repository Şemasını Kurun

Aynı dizinde şu komutu çalıştırın:

```bash
./digna repo install
```

Bu komut PostgreSQL veritabanınıza gerekli tabloları ve şemayı yükler.

### Adım 5: Yönetici (Admin) Kullanıcısı Oluşturun

Yönetici kullanıcısı doğrudan repository şemasında oluşturulur; bu nedenle sunucunun henüz çalışıyor olması gerekmez. digna kurulum dizininde şunu çalıştırın:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Örnek:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Bu komut, `admin@example.com` e-posta adresine ve tam idari ayrıcalıklara sahip bir kullanıcı oluşturur.

!!! tip "İpucu"

    Parolayı tek tırnak içine alın. `zsh`, `!`, `$` ve `*` gibi karakterleri özel olarak ele alır ve bu karakterleri içeren tırnaksız bir parola yazıldığı gibi aktarılmaz.

!!! tip "En İyi Uygulama"

    Büyük küçük harf, sayı ve özel karakter içeren güçlü bir parola kullanın.

### Adım 6: digna Sunucusunu Başlatın

digna kurulum dizininde sunucuyu başlatın:

```bash
./digna serve --address <host> --port <port>
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

!!! tip "İpucu"

    Sunucuyu ilk kez başlattığınızda macOS, uygulamanın gelen ağ bağlantılarını kabul etmesini isteyip istemediğinizi sorabilir. **Allow** düğmesine tıklayın; aksi takdirde dashboard backend'e erişemez.

!!! note "Sunucu terminali meşgul eder"

    `serve` ön planda çalışır ve siz ++ctrl+c++ ile durdurana kadar çalışmayı sürdürür. Kurulumu tamamlarken çalışır durumda bırakın; bunun yerine sistem açılışında otomatik başlatmak için bkz. [digna'yı Arka Plan Hizmeti Olarak Çalıştırma](#running-digna-as-a-background-service).

---

## Dashboard Yapılandırması {: #dashboard-configuration }

### Adım 1: Dashboard'u Web Sunucusuna Dağıtın

digna dashboard'u kendi yapılandırmasını `dashboard/dashboard_config.toml` dosyasından okur. Bu dosya kurulumla birlikte gelmez — onu `dashboard/` dizininde, dashboard dosyalarının yanında siz oluşturursunuz.

Dosyanın içeriği [Çoklu Oturum Açma (Single Sign-On)](../../../sso/overview.md) bölümünde açıklanmıştır; dosyaya ihtiyaç duyulan yer de burasıdır: dashboard'un sunduğu oturum açma seçeneklerini ve çoklu örnek dağıtımlarında backend bağlantısını içerir.

Web sunucunuzu seçin ve ilgili dağıtım adımlarını izleyin.

#### nginx'e Dağıtım

[nginx Kurulumu](#nginx-setup) bölümünü izlediyseniz server bloğu zaten `dashboard` klasörünüzü gösterir ve herhangi bir kopyalama gerekmez.

1. **Yolu doğrulayın**
   - `$(brew --prefix)/etc/nginx/servers/digna.conf` dosyasını açın
   - `root` değerinin çıkardığınız `dashboard` klasörünü gösterdiğini doğrulayın

2. **Klasörün okunabilir olduğundan emin olun**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **nginx'i yeniden yükleyin**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Kurulumu Test Edin**
   - Tarayıcınızı açın
   - `http://localhost:8080` (veya yapılandırdığınız URL) adresine gidin
   - digna dashboard giriş sayfasını görmelisiniz

#### Apache httpd'ye Dağıtım

1. **Dashboard'u Belge Köküne Kopyalayın**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Yeniden Yazma Kurallarını Ekleyin**

   Dashboard rotalarının tarayıcı yenilemesinden sonra da çalışması için dağıtılan klasörün içinde bir `.htaccess` dosyası oluşturun:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Aşağıdakini yapıştırın:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **Apache'yi Yeniden Başlatın**
   ```bash
   sudo apachectl restart
   ```

4. **Dashboard'a Erişim**
   - Tarayıcınızı açın
   - `http://localhost/digna` adresine gidin
   - digna dashboard giriş sayfasını görmelisiniz

---

## digna'yı Arka Plan Hizmeti Olarak Çalıştırma {: #running-digna-as-a-background-service }

### Neden digna'yı Hizmet Olarak Çalıştırmalı?

digna backend'ini arka plan hizmeti olarak çalıştırmak şu avantajları sağlar:

- Makine açıldığında otomatik olarak başlar
- Açık bir Terminal penceresi olmadan arka planda çalışır
- Çöktüğünde otomatik olarak yeniden başlar
- macOS'un hizmet yöneticisi olan `launchctl` üzerinden yönetilebilir

### Hizmet Yönetim Dosyaları

Gerekli tüm dosyalar digna kurulum dizininin altında: `bin/` dizininde bulunur.

Mevcut kabuk betikleri:

- `install_service.sh` — digna'yı launchd'ye kaydeder
- `uninstall_service.sh` — hizmet kaydını kaldırır
- `start_service.sh` — kayıtlı hizmeti başlatır
- `stop_service.sh` — çalışan hizmeti durdurur

!!! warning "Yönetici Gereklidir"

    Sistem açılışında başlayan bir hizmeti kaydetmek `/Library/LaunchDaemons` dizinine yazdığından, tüm betikler `sudo` ile çalıştırılmalıdır.

### Betikleri Çalıştırılabilir Yapma

Çıkarma işlemi çalıştırma izni bitini korumayabilir. İlk kullanımdan önce:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Hizmeti Yükleme

1. **Terminal'i açın**

2. **bin Klasörüne Gidin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Kurulum Betiğini Çalıştırın**
   ```bash
   sudo ./install_service.sh
   ```

digna sunucusu artık **otomatik başlatma** etkinleştirilmiş şekilde launchd'ye kayıtlıdır. Hizmet hemen başlamaz — başlatmak için bir sonraki bölüme bakın.

### Hizmeti Başlatma ve Durdurma

#### Hizmeti Başlatmak İçin

1. Terminal'i açın
2. `/opt/digna/bin` dizinine gidin
3. Şunu çalıştırın:
   ```bash
   sudo ./start_service.sh
   ```

#### Hizmeti Durdurmak İçin

1. Terminal'i açın
2. `/opt/digna/bin` dizinine gidin
3. Şunu çalıştırın:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "İpucu"

    Uygulama dosyalarını güncellemeden önce hizmeti her zaman durdurun.

### Hizmeti Doğrulama

Hizmetin kayıtlı olduğunu ve çalıştığını doğrulamak için:

```bash
sudo launchctl list | grep digna
```

Bir süreç kimliğiyle (PID) başlayan satır, hizmetin çalıştığını gösterir. İlk sütundaki `-`, hizmetin kayıtlı ancak durdurulmuş olduğu anlamına gelir.

### Hizmeti Yeni Bir Dizine Taşıma

launchd yürütülebilir dosyanın mutlak yolunu sakladığından, kurulumun yerini değiştirmek hizmetin yeniden kaydedilmesini gerektirir:

1. **Mevcut Hizmeti Kaldırın**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Uygulama Dosyalarını Taşıyın**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Hizmeti Yeniden Kurun**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Hizmeti Başlatın**
   ```bash
   sudo ./start_service.sh
   ```

### Hizmeti Kaldırma

1. **Çalışan Hizmeti Durdurun**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Hizmeti Kaldırın**
   ```bash
   sudo ./uninstall_service.sh
   ```

digna sunucusunun launchd kaydı artık kaldırılmıştır.

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

Yükseltmeden sonra etkilenen her bağlantıyı ODBC'ye taşıyın ve dashboard'dan sınayın — bkz. [Veritabanı Bağlantısı Oluşturma](../../../databases/overview.md#create-a-database-connection) ve [Bağlantıyı Sınama](../../../databases/overview.md#testing-a-connection).

!!! warning "Databricks Legacy bağlantıları"

    Databricks Legacy bağlayıcısı bu sürümde kaldırıldı. Bu bağlantıları [Databricks](../../../databases/databricks_connector_guide.md) bağlayıcısına taşıyın.

**digna Repository Yedeği Almak Zorunludur**

digna'yı yükseltmeden önce veri kaybını önlemek için repository'nizin (PostgreSQL) yedeğini alın.
Bir yedek, yükseltme sırasında beklenmeyen sorunlar çıkarsa geri dönüş yapabilmenizi sağlar.

Terminal'den yedek almak için:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Yükseltme Süreci

#### Adım 1: digna Hizmetini Durdurun

digna bir arka plan hizmeti olarak çalışıyorsa, önce durdurun:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

digna ön planda çalışıyorsa, Terminal penceresinde `Ctrl + C` tuşlarına basın.

#### Adım 2: Mevcut Kurulumu Yedekleyin

digna kurulum dizininizde, yeni sürümün yanlarına dağıtılabilmesi için mevcut kurulumunuzun klasörlerini yeniden adlandırın:

```bash
cd /opt/digna
mv dignabackend dignabackend_old
```
```bash
mv dignacli dignacli_old
```
```bash
mv dashboard dashboard_old
```

!!! info "dignabackend ve dignacli artık kullanılmıyor"

    2026.06 sürümünden itibaren `dignabackend` ve `dignacli`, arka uç ile CLI'yi birleştiren tek `digna` çalıştırılabilir dosyasıyla değiştirilmiştir. `dignabackend_old` ve `dignacli_old` klasörlerini yalnızca yükseltmeyi doğrulayana kadar saklayın — sonrasında her ikisini de silebilirsiniz. `dashboard_old` klasörünü, yapılandırma dosyalarınızı oradan geri yükleyene kadar saklayın (bkz. adım 4).

#### Adım 3: Yeni Sürümü Çıkarın ve Dağıtın

1. Yeni digna kurulum ZIP dosyasını çıkarın
2. Yeni `digna` yürütülebilir dosyasını ve `dashboard` klasörünü kurulum dizinine kopyalayın
3. Çalıştırma izni bitini geri yükleyin ve gerekirse karantina özniteliğini kaldırın:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Önemli"

    Ne `config.toml` ne de `dashboard/dashboard_config.toml` hiçbir zaman kurulum ZIP'ine
    dahil edilmez — digna ekibi bu dosyaların hiçbirini göndermez. Bu nedenle mevcut yapılandırmanız
    yükseltmeden etkilenmez ve yeniden adlandırılan `*_old` klasörlerindeki kopyalar elinizdeki
    tek kopyalardır.

#### Adım 4: Yapılandırma Dosyalarınızı Geri Yükleyin

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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

    Her ayarın ne yaptığı şurada açıklanmıştır: [Backend Yapılandırması](#backend-configuration).

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
ardından sayfayı zorla yenileyin (++cmd+shift+r++).

#### Adım 6: Yapılandırmayı Doğrulayın

Depoya dokunmadan önce güncellenmiş `config.toml` dosyasının eksiksiz olduğunu doğrulayın:

```bash
./digna config check
```

Her bölüm OK bildirmelidir. FAILED olarak bildirilen her şeyi düzeltin ve devam etmeden önce komutu yeniden çalıştırın.

#### Adım 7: Lisans Dosyasını Değiştirin

Her sürüm ayrı olarak lisanslanır. digna ekibinin bu sürüm için sağladığı `license.toml` dosyasını
kurulum dizinine kopyalayarak eskisinin yerine koyun:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Önceki lisansı saklamayın"

    Önceki bir sürüm için verilmiş bir `license.toml` bu sürümü kapsamaz ve lisansı denetleyen
    her komut — `user`, `inspection`, `repo` — denetim başarısız olduğunda depoya dokunmadan önce
    sonlanır. Devam etmeden önce lisansı doğrulayın:

    ```bash
    ./digna license check
    ```

#### Adım 8: Repository Şemasını Yükseltin

digna kurulum dizinine gidin ve şu komutu çalıştırın:

```bash
cd /opt/digna
./digna repo upgrade
```

Bu komut PostgreSQL şemasını en son sürüme günceller ve mevcut tüm verileri korur.

#### Adım 9: Hizmetleri Yeniden Başlatın

Arka plan hizmeti olarak çalışıyorsa:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Manuel olarak çalıştırıyorsanız, sunucuyu yeniden başlatın:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

nginx veya Apache kullanıyorsanız ilgili web sunucusunu yeniden başlatın:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Adım 10: Yükseltmeyi Doğrulayın

1. digna dashboard'a erişin
2. Arayüzün düzgün yüklendiğini doğrulayın
3. Sunucu günlüklerini herhangi bir hata için kontrol edin
4. Henüz ODBC kullanmayan her bağlantıyı ODBC'ye taşıyın, ardından tüm bağlantıları sınayın
   — bkz. [Bağlantıyı Sınama](../../../databases/overview.md#testing-a-connection)