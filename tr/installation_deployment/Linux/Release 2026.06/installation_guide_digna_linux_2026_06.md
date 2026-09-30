# digna Sürüm 2026.06 için Linux Kurulum Kılavuzu

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
9. [digna'yı systemd Hizmeti Olarak Çalıştırma](#running-digna-as-a-systemd-service)
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

### Windows veya macOS mu arıyorsunuz?

Bu kılavuz Linux içindir. Diğer platformlar için [Windows Kurulum Kılavuzu](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) veya [macOS Kurulum Kılavuzu](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) belgelerine bakın.

### Bu Kılavuz Hangi Dağıtımları Kapsar?

Yönergeler en yaygın iki sunucu ailesi için yazılmıştır. İkisinin farklılaştığı yerlerde her iki komut da verilir:

- **Debian ailesi** — Debian, Ubuntu. Paket yöneticisi: `apt`.
- **RHEL ailesi** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Paket yöneticisi: `dnf`.

`systemd` kullanan her modern dağıtım çalışır; yalnızca paket adları ve birkaç yapılandırma yolu değişir.

---

## Sistem Gereksinimleri {: #system-requirements }

Kuruluma başlamadan önce sisteminizin aşağıdaki minimum gereksinimleri karşıladığından emin olun:

| Gereksinim | Özellik |
|---|---|
| **İşletim Sistemi** | Ubuntu 22.04 LTS veya üzeri, Debian 12 veya üzeri, RHEL 9 / Rocky 9 / AlmaLinux 9 veya üzeri |
| **Mimari** | x86_64 (amd64) veya arm64 |
| **Init Sistemi** | systemd |
| **Bellek (Minimum Kurulum)** | 16 GB RAM |
| **Disk Alanı** | 10 GB kullanılabilir depolama |
| **Veritabanı** | PostgreSQL Server 12 veya üzeri |
| **Web Sunucusu** | nginx, Apache httpd veya eşdeğeri |

### Veritabanı Kurulum Seçenekleri

**PostgreSQL zaten kuruluysa:**
Mevcut PostgreSQL sunucunuza digna için yeni bir veritabanı ekleyebilirsiniz.

**PostgreSQL'i digna ile aynı makineye kuruyorsanız:**

!!! info "Önerilen Özellikler"

    - **Bellek**: 32 GB RAM (16 GB yerine)
    - **Disk Alanı**: 50 GB kullanılabilir depolama (10 GB yerine)

    Bu daha yüksek özellikler, digna ile PostgreSQL veritabanının aynı anda çalışmasını rahatlıkla karşılayacak şekilde önerilir.

### Dağıtımınızı ve Mimarinizi Denetleme

Bu kılavuzdaki birkaç komut Debian ve RHEL aileleri arasında farklılık gösterir. Hangisini kullandığınızı öğrenmek için şunu çalıştırın:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` veya `ID=debian` — `apt` komutlarını kullanın.
- `ID=rhel`, `rocky`, `almalinux` veya `fedora` — `dnf` komutlarını kullanın.
- `x86_64` veya `aarch64` — ihtiyacınız olan kurulum paketinin mimarisi.

---

## Kurulum Öncesi Hazırlık {: #pre-installation-setup }

digna'yı kurmadan önce iki temel önkoşulun yerinde olduğundan emin olun:

1. **PostgreSQL Server** – hesaplanmış metrikler ve performans verileri için depolama
2. **Web Server** – digna Dashboard'u barındırmak için

Bu bileşenler henüz kurulu değilse, aşağıdaki bölümlerde bunları kurup yapılandırma adımlarını izleyin.

### Paket Dizinini Yenileme

Herhangi bir şey kurmadan önce paket listelerinizi güncelleyin:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Not"

    Bu kılavuz boyunca, bir komut çiftindeki ilk komut **Debian ailesi**, ikincisi ise **RHEL ailesi** içindir. Yalnızca sisteminize uyanı çalıştırın.

---

## PostgreSQL Sunucu Kurulumu {: #postgresql-server-setup }

### PostgreSQL Zaten Kuruluysa

PostgreSQL yerel makinenizde zaten kurulu ve çalışıyorsa veya yönetilen uzak bir PostgreSQL sunucusu kullanıyorsanız, [bir sonraki bölüme](#web-server-configuration) geçebilirsiniz.

### PostgreSQL Kurulumu

#### Adım 1: Sunucu Paketini Kurun

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "İpucu"

    Dağıtım paketleri güncel PostgreSQL sürümünün gerisinde kalabilir. Belirli bir yeni sürüme ihtiyacınız varsa bunun yerine resmi [PostgreSQL apt veya yum deposunu](https://www.postgresql.org/download/linux/) kullanın.

#### Adım 2: Veritabanı Kümesini Başlatın

**Debian ailesinde** paket bir kümeyi otomatik olarak oluşturur ve başlatır — bir sonraki adıma geçin.

**RHEL ailesinde** küme açıkça oluşturulmalıdır:

```bash
sudo postgresql-setup --initdb
```

#### Adım 3: Hizmeti Başlatın ve Etkinleştirin

```bash
sudo systemctl enable --now postgresql
```

Bu komut PostgreSQL'i hemen başlatır ve sistem açılışında otomatik olarak yeniden başlayacak şekilde yapılandırır.

#### Adım 4: Kurulumu Doğrulayın

```bash
psql --version
sudo systemctl status postgresql
```

PostgreSQL sürümünü ve `active (running)` durumundaki bir hizmeti görmelisiniz.

#### Adım 5: Sunucuya Bağlanın

Linux PostgreSQL paketi, kümenin sahibi olan bir `postgres` sistem hesabı oluşturur. Bu hesap üzerinden bağlanın:

```bash
sudo -u postgres psql
```

!!! note "Not — Linux Burada Windows'tan Farklıdır"

    Windows yükleyicisi, kurulum sırasında `postgres` süper kullanıcısı için bir parola belirlemenizi ister. Linux paketleri bunu yapmaz. Bunun yerine yerel bağlantılar **peer kimlik doğrulaması** ile doğrulanır: `postgres` işletim sistemi kullanıcısının, parola olmadan `postgres` veritabanı kullanıcısı olarak bağlanmasına izin verilir.

    Yukarıdaki komutun `sudo -u postgres` kullanmasının nedeni budur. digna backend'i TCP üzerinden bir kullanıcı adı ve parolayla bağlanır; bu nedenle [İlk Kurulum](#initial-installation) bölümünde açık bir digna kullanıcısı oluşturacaksınız.

#### Adım 6: Portu Doğrulayın

Varsayılan PostgreSQL portu `5432`'dir. Sunucunuzun dinlediği portu doğrulamak için:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Değeri not edin — digna backend'ini yapılandırırken ihtiyacınız olacak.

#### Adım 7: digna Kullanıcısı için Parola Kimlik Doğrulamasını Etkinleştirin

digna, PostgreSQL'e TCP üzerinden `digna_user` olarak bağlanır; bu da peer kimlik doğrulaması yerine parola kimlik doğrulaması gerektirir. `pg_hba.conf` dosyanızın buna izin verdiğini denetleyin.

Dosyanın yerini bulun:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Dosyayı bir düzenleyicide açın ve yerel TCP satırlarının `ident` yerine `scram-sha-256` (eski sunucularda `md5`) kullandığını doğrulayın:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Herhangi bir değişiklikten sonra PostgreSQL'i yeniden yükleyin:

```bash
sudo systemctl reload postgresql
```

!!! warning "Önemli"

    digna `FATAL: Ident authentication failed for user "digna_user"` bildiriyorsa nedeni bu ayardır.

#### Adım 8: PostgreSQL Başka Bir Makinede Çalışıyorsa

Farklı bir ana bilgisayardan gelen bağlantıları kabul etmek için `postgresql.conf` içinde `listen_addresses` değerini ayarlayın ve `pg_hba.conf` dosyasına ağınız için uygun bir `host` satırı ekleyin:

```
listen_addresses = '*'
```

Ardından güvenlik duvarında portu açın ve hizmeti yeniden başlatın:

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## Web Sunucusu Yapılandırması {: #web-server-configuration }

digna dashboard'unu barındırmak için bir web sunucusuna ihtiyaç vardır. Aşağıdaki seçeneklerden birini seçin:

- [nginx](#nginx-setup) — hafif ve önerilen
- [Apache httpd](#apache-setup) — yaygın olarak kullanılan alternatif

Bu sunuculardan yalnızca **birini** kurmanız ve yapılandırmanız yeterlidir.

Her iki bölüm de dashboard'un bağlı olduğu iki şeyi yapılandırır:

- **Tek sayfalı uygulama (SPA) geri dönüşü**; böylece bir dashboard URL'sini yenilemek 404 döndürmez
- **`.md` MIME türü**; böylece Markdown dosyaları doğru şekilde sunulur

### nginx Kurulumu {: #nginx-setup }

#### Genel Bakış

nginx, statik digna dashboard'unu sunmaya çok uygun, hafif ve yüksek performanslı bir web sunucusudur.

#### Kurulum

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### nginx'i Başlatma

```bash
sudo systemctl enable --now nginx
```

#### Kurulumu Doğrulayın

1. Tarayıcınızı açın
2. `http://localhost` adresine gidin
3. nginx karşılama sayfasını görmelisiniz

#### Güvenlik Duvarını Açma

Sunucuya başka makinelerden erişiliyorsa HTTP trafiğine izin verin:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Dashboard için Bir Site Yapılandırma

nginx, her iki dağıtım ailesinde de `conf.d` dizinindeki tüm dosyaları dahil eder. Orada digna için ayrı bir yapılandırma dosyası oluşturun:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Aşağıdakini yapıştırın ve `/opt/digna/dashboard` yolunu, çıkardığınız `dashboard` klasörünün gerçek yoluyla değiştirin:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
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

#### Varsayılan Siteyi Devre Dışı Bırakın

Bir port için yalnızca bir server bloğu `default_server` olabilir. **Debian ailesinde**, çakışmaması için paketle gelen varsayılan siteyi kaldırın:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

**RHEL ailesinde**, `/etc/nginx/nginx.conf` içindeki `server { ... }` bloğunu yorum satırına alın veya silin.

#### Yapılandırmayı Uygulayın

Yapılandırmada söz dizimi hatası olup olmadığını test edin, ardından nginx'i yeniden yükleyin:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Apache httpd Kurulumu {: #apache-setup }

#### Genel Bakış

Apache httpd, desteklenen her dağıtımın varsayılan depolarında bulunur. Paketin adı Debian ailesinde `apache2`, RHEL ailesinde `httpd`'dir.

#### Kurulum

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Apache'yi Başlatma

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Kurulumu Doğrulayın

1. Tarayıcınızı açın
2. `http://localhost` adresine gidin
3. Dağıtımın varsayılan Apache sayfasını görmelisiniz

#### Gerekli: mod_rewrite'ı Etkinleştirin

Dashboard, URL yeniden yazmayı gerektirir.

**Debian ailesinde** modülü etkinleştirin ve yeniden başlatın:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

**RHEL ailesinde** `mod_rewrite` varsayılan olarak yüklüdür. Bunu doğrulayın:

```bash
httpd -M | grep rewrite
```

#### Gerekli: .htaccess Geçersiz Kılmalarına İzin Verin

Belge kökünüz için yapılandırma dosyasını açın:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Belge kökünüzü kapsayan `<Directory>` bloğunu bulun (her iki ailede de `/var/www/html`) ve şunu:

```apache
AllowOverride None
```

şununla değiştirin:

```apache
AllowOverride All
```

#### Gerekli: Markdown Dosyaları için MIME Türü

Markdown dosyalarının doğru şekilde sunulması için aynı dosyaya şu satırı ekleyin:

```apache
AddType text/markdown .md
```

!!! warning "Önemli"

    Bu ayar olmadan `.md` dosyaları doğru şekilde servis edilmeyebilir.

#### Yapılandırmayı Uygulayın

Yapılandırmada söz dizimi hatası olup olmadığını denetleyin, ardından Apache'yi yeniden başlatın:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
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

Bunları kabuktan tek adımda çalıştırmak için:

```bash
sudo -u postgres psql
```

Ardından ifadeleri `postgres=#` isteminde yapıştırın ve çıkmak için `\q` yazın.

!!! tip "En İyi Uygulama"

    Veritabanı kullanıcıları için güçlü, karmaşık parolalar kullanın. Kolay tahmin edilebilir kimlik bilgilerini kullanmaktan kaçının.

---

### Adım 2: digna Kurulum Paketini Çıkarın

1. Size sağlanan digna kurulum ZIP dosyasını bulun
2. İstediğiniz kurulum konumuna çıkarın — örneğin `/opt/digna`
3. Çıkarma sonrası aşağıdaki öğeleri görmelisiniz:
   - `dashboard/` — Web dashboard arayüzü
   - `digna` — Ana yürütülebilir dosya (backend + CLI birleşik)

!!! info "Yapılandırma ve lisans dosyaları pakette yer almaz"

    Ne `config.toml` ne de `dashboard/dashboard_config.toml` kurulumla birlikte gelir — ikisini de
    kendiniz, [Backend Yapılandırması](#backend-configuration) ve
    [Dashboard Yapılandırması](#dashboard-configuration) bölümlerinde oluşturursunuz. `license.toml` da pakete dahil değildir;
    Adım 3'te açıklandığı gibi digna tarafından ayrı olarak sağlanır.

Kabuktan çıkarmak için:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
```

!!! note "Not"

    `unzip` kurulu değilse `sudo apt install -y unzip` veya `sudo dnf install -y unzip` ile ekleyin.

#### Yürütülebilir Dosyayı Çalıştırılabilir Yapın

Arşivin nasıl aktarıldığına bağlı olarak, çalıştırma izni biti çıkarma sırasında korunmayabilir. Bunu açıkça ayarlayın:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Bir Hizmet Hesabı Oluşturun

Üretim dağıtımları için backend'in ayrı, ayrıcalıksız bir kullanıcı olarak çalıştırılması önerilir:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Not"

    RHEL ailesinde eşdeğer kabuk yolu `/sbin/nologin`'dir.

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
sudo mv config_template.toml config.toml
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

    Dashboard'u nginx veya Apache üzerinden varsayılan HTTP portunda sunuyorsanız izin verilecek kaynak `http://localhost`'tur — dashboard'a başka makinelerden erişiliyorsa sunucunun genel URL'sidir.

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

!!! tip "En İyi Uygulama"

    `config.toml`, bir veritabanı parolasını düz metin olarak içerir. İzinlerini, dosyayı yalnızca hizmet hesabı okuyabilecek şekilde kısıtlayın:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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

    Sunucunuzda kullanılabilir CPU çekirdeği sayısını öğrenmek için `nproc` komutunu çalıştırın.

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

1. Bir terminal açın
2. digna kurulum dizinine gidin (`config.toml` ve `digna` yürütülebilir dosyasının bulunduğu dizin)
3. Bağlantı testini çalıştırın:

```bash
cd /opt/digna
./digna repo check
```

Bağlantının kurulduğuna dair bir onay görmelisiniz (repository henüz başlatılmamıştır).

!!! note "Not"

    Linux'ta geçerli dizin PATH'inizde bulunmaz; bu nedenle yürütülebilir dosya `digna` yerine `./digna` olarak çağrılır. Kısa biçimi her yerde kullanmak için bir sembolik bağlantı ekleyin:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
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

    Parolayı tek tırnak içine alın. `bash` ve `zsh`, `!`, `$` ve `*` gibi karakterleri özel olarak ele alır ve bu karakterleri içeren tırnaksız bir parola yazıldığı gibi aktarılmaz.

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

    Dashboard backend'den farklı bir makineden sunuluyorsa API portunu da güvenlik duvarında açın:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "Sunucu terminali meşgul eder"

    `serve` ön planda çalışır ve siz ++ctrl+c++ ile durdurana kadar çalışmayı sürdürür. Kurulumu tamamlarken çalışır durumda bırakın; bunun yerine sistem açılışında otomatik başlatmak için bkz. [digna'yı systemd Hizmeti Olarak Çalıştırma](#running-digna-as-a-systemd-service).

---

## Dashboard Yapılandırması {: #dashboard-configuration }

### Adım 1: Dashboard'u Web Sunucusuna Dağıtın

digna dashboard'u kendi yapılandırmasını `dashboard/dashboard_config.toml` dosyasından okur. Bu dosya kurulumla birlikte gelmez — onu `dashboard/` dizininde, dashboard dosyalarının yanında siz oluşturursunuz.

Dosyanın içeriği [Çoklu Oturum Açma (Single Sign-On)](../../../sso/overview.md) bölümünde açıklanmıştır; dosyaya ihtiyaç duyulan yer de burasıdır: dashboard'un sunduğu oturum açma seçeneklerini ve çoklu örnek dağıtımlarında backend bağlantısını içerir.

Web sunucunuzu seçin ve ilgili dağıtım adımlarını izleyin.

#### nginx'e Dağıtım

[nginx Kurulumu](#nginx-setup) bölümünü izlediyseniz server bloğu zaten `dashboard` klasörünüzü gösterir ve herhangi bir kopyalama gerekmez.

1. **Yolu doğrulayın**
   - `/etc/nginx/conf.d/digna.conf` dosyasını açın
   - `root` değerinin çıkardığınız `dashboard` klasörünü gösterdiğini doğrulayın

2. **Klasörün okunabilir olduğundan emin olun**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **nginx'i yeniden yükleyin**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Kurulumu Test Edin**
   - Tarayıcınızı açın
   - `http://localhost` (veya yapılandırdığınız URL) adresine gidin
   - digna dashboard giriş sayfasını görmelisiniz

#### Apache httpd'ye Dağıtım

1. **Dashboard'u Belge Köküne Kopyalayın**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Yeniden Yazma Kurallarını Ekleyin**

   Dashboard rotalarının tarayıcı yenilemesinden sonra da çalışması için dağıtılan klasörün içinde bir `.htaccess` dosyası oluşturun:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
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
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Dashboard'a Erişim**
   - Tarayıcınızı açın
   - `http://localhost/digna` adresine gidin
   - digna dashboard giriş sayfasını görmelisiniz

### Adım 2: SELinux (Yalnızca RHEL Ailesi)

RHEL, Rocky, AlmaLinux ve Fedora'da SELinux varsayılan olarak zorlayıcı (enforcing) moddadır ve web sunucusunun beklenen konumlarının dışındaki dosyaları okumasını engeller. Etkin olup olmadığını denetleyin:

```bash
getenforce
```

Sonuç `Enforcing` ise ve dashboard'u `/opt/digna/dashboard` konumundan sunuyorsanız, web sunucusunun okuyabilmesi için dizini etiketleyin:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Not"

    `semanage` bulunamazsa `sudo dnf install -y policycoreutils-python-utils` ile kurun.

!!! warning "Önemli"

    Yeni yapılandırılmış bir RHEL sunucusunda **403 Forbidden** döndüren bir dashboard, neredeyse her zaman dosya izni sorunu değil, bir SELinux etiketleme sorunudur. `sudo ausearch -m avc -ts recent` ile doğrulayın.

---

## digna'yı systemd Hizmeti Olarak Çalıştırma {: #running-digna-as-a-systemd-service }

### Neden digna'yı Hizmet Olarak Çalıştırmalı?

digna backend'ini systemd hizmeti olarak çalıştırmak şu avantajları sağlar:

- Makine açıldığında otomatik olarak başlar
- Açık bir terminal penceresi olmadan arka planda çalışır
- Çöktüğünde otomatik olarak yeniden başlar
- Standart Linux hizmet yöneticisi olan `systemctl` üzerinden yönetilebilir

### Hizmet Yönetim Dosyaları

Gerekli tüm dosyalar digna kurulum dizininin altında: `bin/` dizininde bulunur.

Mevcut kabuk betikleri:

- `install_service.sh` — digna'yı systemd'ye kaydeder
- `uninstall_service.sh` — hizmet kaydını kaldırır
- `start_service.sh` — kayıtlı hizmeti başlatır
- `stop_service.sh` — çalışan hizmeti durdurur

!!! warning "Root Ayrıcalıkları Gereklidir"

    Sistem açılışında başlayan bir hizmeti kaydetmek `/etc/systemd/system` dizinine bir unit dosyası yazdığından, tüm betikler `sudo` ile çalıştırılmalıdır.

### Betikleri Çalıştırılabilir Yapma

Çıkarma işlemi çalıştırma izni bitini korumayabilir. İlk kullanımdan önce:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Hizmeti Yükleme

1. **Bir terminal açın**

2. **bin Klasörüne Gidin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Kurulum Betiğini Çalıştırın**
   ```bash
   sudo ./install_service.sh
   ```

digna sunucusu artık **otomatik başlatma** etkinleştirilmiş şekilde systemd'ye kayıtlıdır. Hizmet hemen başlamaz — başlatmak için bir sonraki bölüme bakın.

### Hizmeti Başlatma ve Durdurma

#### Hizmeti Başlatmak İçin

1. Bir terminal açın
2. `/opt/digna/bin` dizinine gidin
3. Şunu çalıştırın:
   ```bash
   sudo ./start_service.sh
   ```

#### Hizmeti Durdurmak İçin

1. Bir terminal açın
2. `/opt/digna/bin` dizinine gidin
3. Şunu çalıştırın:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "İpucu"

    Uygulama dosyalarını güncellemeden önce hizmeti her zaman durdurun.

### Hizmeti systemctl ile Yönetme

Kaydedildikten sonra hizmet, herhangi bir dizinden standart systemd komutlarıyla da denetlenebilir:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Hizmeti Doğrulama

Hizmetin kayıtlı olduğunu ve çalıştığını doğrulamak için:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled`, hizmetin sistem açılışında başladığı; `active` ise şu anda çalıştığı anlamına gelir.

### Hizmet Günlüklerini Görüntüleme

systemd, backend'in konsola yazdığı her şeyi yakalar. Okumak için:

```bash
sudo journalctl -u digna -n 100
```

Bir sorunu yeniden oluştururken günlüğü canlı izlemek için:

```bash
sudo journalctl -u digna -f
```

!!! tip "İpucu"

    Başlayıp hemen duran bir hizmeti teşhis etmenin en hızlı yolu budur. Repository bağlantı hatası veya eksik bir `license.toml` burada bildirilir.

### Hizmeti Yeni Bir Dizine Taşıma

Unit dosyası yürütülebilir dosyanın mutlak yolunu sakladığından, kurulumun yerini değiştirmek hizmetin yeniden kaydedilmesini gerektirir:

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

digna sunucusunun systemd kaydı artık kaldırılmıştır.

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

Kabuktan yedek almak için:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Yükseltme Süreci

#### Adım 1: digna Hizmetini Durdurun

digna bir systemd hizmeti olarak çalışıyorsa, önce durdurun:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

digna ön planda çalışıyorsa, terminal penceresinde `Ctrl + C` tuşlarına basın.

#### Adım 2: Mevcut Kurulumu Yedekleyin

digna kurulum dizininizde, yeni sürümün yanlarına dağıtılabilmesi için mevcut kurulumunuzun klasörlerini yeniden adlandırın:

```bash
cd /opt/digna
sudo mv dignabackend dignabackend_old
```
```bash
sudo mv dignacli dignacli_old
```
```bash
sudo mv dashboard dashboard_old
```

!!! info "dignabackend ve dignacli artık kullanılmıyor"

    2026.06 sürümünden itibaren `dignabackend` ve `dignacli`, arka uç ile CLI'yi birleştiren tek `digna` çalıştırılabilir dosyasıyla değiştirilmiştir. `dignabackend_old` ve `dignacli_old` klasörlerini yalnızca yükseltmeyi doğrulayana kadar saklayın — sonrasında her ikisini de silebilirsiniz. `dashboard_old` klasörünü, yapılandırma dosyalarınızı oradan geri yükleyene kadar saklayın (bkz. adım 4).

#### Adım 3: Yeni Sürümü Çıkarın ve Dağıtın

1. Yeni digna kurulum ZIP dosyasını çıkarın
2. Yeni `digna` yürütülebilir dosyasını ve `dashboard` klasörünü kurulum dizinine kopyalayın
3. Çalıştırma izni bitini ve hizmet hesabının sahipliğini geri yükleyin:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Önemli"

    Ne `config.toml` ne de `dashboard/dashboard_config.toml` hiçbir zaman kurulum ZIP'ine
    dahil edilmez — digna ekibi bu dosyaların hiçbirini göndermez. Bu nedenle mevcut yapılandırmanız
    yükseltmeden etkilenmez ve yeniden adlandırılan `*_old` klasörlerindeki kopyalar elinizdeki
    tek kopyalardır.

#### Adım 4: Yapılandırma Dosyalarınızı Geri Yükleyin

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
ardından sayfayı zorla yenileyin (++ctrl+f5++).

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
sudo cp /path/to/new/license.toml /opt/digna/license.toml
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

systemd hizmeti olarak çalışıyorsa:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Manuel olarak çalıştırıyorsanız, sunucuyu yeniden başlatın:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

nginx veya Apache kullanıyorsanız ilgili web sunucusunu yeniden yükleyin:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

RHEL ailesinde, `dashboard` dizini değiştirildiyse SELinux etiketlemesini yeniden uygulayın:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Adım 10: Yükseltmeyi Doğrulayın

1. digna dashboard'a erişin
2. Arayüzün düzgün yüklendiğini doğrulayın
3. Sunucu günlüklerini herhangi bir hata için kontrol edin
4. Henüz ODBC kullanmayan her bağlantıyı ODBC'ye taşıyın, ardından tüm bağlantıları sınayın
   — bkz. [Bağlantıyı Sınama](../../../databases/overview.md#testing-a-connection):

```bash
sudo journalctl -u digna -n 100
```