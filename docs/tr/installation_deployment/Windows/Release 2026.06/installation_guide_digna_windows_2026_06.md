---
title: Windows Kurulum Kılavuzu – digna Sürüm 2026.06 | digna Belgeleri
description: digna Sürüm 2026.06'i Windows'ta kurmaya yönelik adım adım rehber — sistem gereksinimleri, PostgreSQL kurulumu, web sunucusu yapılandırması, backend ve dashboard yapılandırması, digna'yı Windows hizmeti olarak çalıştırma ve yeni sürüme yükseltme.
keywords: digna windows kurulumu, digna dağıtım rehberi, digna backend kurulumu, digna dashboard kurulumu, postgresql kurulumu, digna windows servisi, digna yükseltme rehberi
image: /assets/logo_square.png
---

# Windows Installation Guide for digna Release 2026.06

**Release:** 2026.06

**Last Updated:** August 30, 2026


---

## Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Pre-Installation Setup](#pre-installation-setup)
4. [PostgreSQL Server Setup](#postgresql-server-setup)
5. [Web Server Configuration](#web-server-configuration)
6. [Initial Installation](#initial-installation)
7. [Backend Configuration](#backend-configuration)
8. [Dashboard Configuration](#dashboard-configuration)
9. [Running digna as a Windows Service](#running-digna-as-a-windows-service)
10. [Upgrading to a New Release](#upgrading-to-a-new-release)

---

## Giriş {: #introduction }

### digna Hakkında

digna, veri ambarları, veri gölleri ve lakehouse'lar gibi çeşitli veri ortamlarında veri kalitesi yönetimini optimize etmek için tasarlanmış kapsamlı, yapay zekâ destekli bir platformdur. Yüksek ölçeklenebilirlik ve uyarlanabilirlik göz önünde bulundurularak geliştirilen digna, otomasyon, gerçek zamanlı izleme ve anomali tespiti ile modern veri zorluklarına yanıt verir.

digna iki ana bileşenden oluşur:

- **dignabackend**: Verileri işlemek ve kalite kontrollerini gerçekleştirmekle sorumlu uygulamanın çekirdek motoru.
- **dignadashboard**: Bir web sunucusunda barındırılan, digna platformuyla etkileşim kurmayı ve veri kalite metriklerini görselleştirmeyi sağlayan web tabanlı arayüz.

### 2026.06 Sürümünde Yenilikler

Bu sürüm, veri gözlemlenebilirliğini doğrudan kodunuza getirerek geliştiricilerin kaynakta veri kalitesini izlemesini sağlar. Tam ayrıntılar için [sürüm notlarına](http://docs.digna.ai/changelog/Release_202606/) bakın.

---

## Sistem Gereksinimleri {: #system-requirements }

Kuruluma başlamadan önce sisteminizin aşağıdaki minimum gereksinimleri karşıladığından emin olun:

| Requirement | Specification |
|---|---|
| **Operating System** | Windows Server or Windows 10/11 |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB available storage |
| **Database** | PostgreSQL Server 12 or higher |
| **Web Server** | IIS, Apache Tomcat, or equivalent |

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
   - `config.toml` — Yapılandırma dosyası
   - `license.toml` — Lisans dosyası (kendi lisansınızı buraya kopyalayın)

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
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_APP_HOST` | `localhost` or IP address | dignabackend'in barındırıldığı host adı veya IP |
| `digna_APP_PORT` | `8082` (default) | REST API uç noktaları için port |
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
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_FERNET_KEY` | Encryption key | Tokenları ve çerezleri şifrelemek için kullanılır (varsayılan sağlanır) |
| `digna_COOKIE_DOMAIN` | `localhost` | Frontend domain'i ile eşleşsin |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (production) | HTTPS bağlantıları için `true` kullanın |
| `digna_COOKIE_HTTPONLY` | `true` | Güvenlik için her zaman etkin |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF saldırılarını önlemeye yardımcı olur |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 hours) | Oturum zaman aşımı (saniye cinsinden) |
| `digna_MAX_WORKERS` | Number of CPU cores - 1 | Paralel denetim görevlerinin sayısı |

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

### Adım 5: digna Sunucusunu Başlatın

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

### Adım 6: Yönetici (Admin) Kullanıcısı Oluşturun

1. Yeni bir Komut İstemi penceresi açın
2. digna kurulum dizinine gidin
3. Yönetici kullanıcısı oluşturmak için şu komutu çalıştırın:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Örnek:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

Bu komut tam idari ayrıcalıklara sahip bir kullanıcı oluşturur.

!!! tip "En İyi Uygulama"

    Büyük küçük harf, sayı ve özel karakter içeren güçlü bir parola kullanın.

---

## Dashboard Yapılandırması {: #dashboard-configuration }

### Adım 1: Dashboard'u Web Sunucusuna Dağıtın

digna dashboard'unun kendi ayrı `config.toml` dosyası `dashboard/` dizininde bulunur. Bu yapılandırma başlangıç kurulumu sırasında genellikle değişiklik gerektirmez. Sadece backend bağlantısını özelleştirmeniz gerekiyorsa düzenlemeniz gerekir.

Dashboard yapılandırmasını (ör. çoklu örnek dağıtımları için) değiştirme ihtiyacınız varsa dashboard belgelerine başvurun.

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

### Hizmet Yönetim Dosyaları

Gerekli tüm dosyalar digna kurulum dizininin altında: `bin/` dizininde bulunur.

Mevcut batch (.bat) dosyaları:
- `install_service.bat` — digna'yı Windows hizmeti olarak kaydeder
- `uninstall_service.bat` — hizmet kaydını kaldırır
- `start_service.bat` — hizmeti başlatır
- `stop_service.bat` — hizmeti durdurur

!!! warning "Yönetici Gereklidir"

    Tüm batch dosyaları Yönetici (Administrator) ayrıcalıklarıyla çalıştırılmalıdır.

### Hizmeti Yükleme

1. **Komut İstemi'ni Yönetici Olarak Açın**
   - Komut İstemi üzerine sağ tıklayın
   - "Run as Administrator" (Yönetici olarak çalıştır) seçeneğini seçin

2. **bin Klasörüne Gidin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Kurulum Script'ini Çalıştırın**
   ```bash
   install_service.bat
   ```

digna sunucusu artık otomatik başlatma etkinleştirilmiş bir Windows hizmeti olarak kayıtlıdır. Hizmet hemen başlamaz — başlatma için bir sonraki bölüme bakın.

### Hizmeti Başlatma ve Durdurma

#### Hizmeti Başlatmak İçin

1. Komut İstemi'ni Yönetici olarak açın
2. `digna\bin` dizinine gidin
3. Şunu çalıştırın:
   ```bash
   start_service.bat
   ```

#### Hizmeti Durdurmak İçin

1. Komut İstemi'ni Yönetici olarak açın
2. `digna\bin` dizinine gidin
3. Şunu çalıştırın:
   ```bash
   stop_service.bat
   ```

!!! tip "İpucu"

    Uygulama dosyalarını güncellemeden önce hizmeti her zaman durdurun.

### Hizmeti Yeni Bir Dizin Altına Taımak

digna kurulumunu taşımaya ihtiyacınız varsa:

1. **Mevcut Hizmeti Kaldırın**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Uygulama Dosyalarını Taşıyın**
   - Tüm digna kurulum klasörünü yeni konuma taşıyın

3. **Hizmeti Yeniden Kurun**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Hizmeti Başlatın**
   ```bash
   start_service.bat
   ```

### Hizmeti Kaldırma

1. **Çalışan Hizmeti Durdurun**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Hizmeti Kaldırın**
   ```bash
   uninstall_service.bat
   ```

digna sunucusu artık Windows hizmeti olarak kayıtlı olmayacaktır.

---

## Yeni Bir Sürüme Yükseltme {: #upgrading-to-a-new-release }

### Yükseltme Öncesi

**digna Repository Yedeği Almak Zorunludur**

digna'yı yükseltmeden önce veri kaybını önlemek için repository'nizin (PostgreSQL) yedeğini alın.
Bir yedek, yükseltme sırasında beklenmeyen sorunlar çıkarsa geri dönüş yapabilmenizi sağlar.

### Yükseltme Süreci

#### Adım 1: digna Hizmetini Durdurun

digna bir Windows hizmeti olarak çalışıyorsa, önce durdurun:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Adım 2: Mevcut Backend Kurulumunu Yedekleyin

digna kurulum dizininizde:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### Adım 3: Yeni Sürümü Çıkarın ve Dağıtın

1. Yeni digna kurulum ZIP dosyasını çıkarın
2. Yeni `digna` yürütülebilir dosyasını ve `dashboard` klasörünü kurulum dizinine kopyalayın


!!! warning "Önemli"

    `config.toml` dosyası asla kurulum ZIP'ine dahil edilmez. Mevcut yapılandırmanız korunur.

### Adım 4: Yapılandırma Dosyalarınızı Geri Yükleyin

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Adım 5: Repository Şemasını Yükseltin

digna kurulum dizinine gidin ve şu komutu çalıştırın:

```bash
digna repo upgrade
```

Bu komut PostgreSQL şemasını en son sürüme günceller ve mevcut tüm verileri korur.

### Adım 6: Servisleri Yeniden Başlatın

Windows hizmeti olarak çalışıyorsa:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Manuel olarak çalıştırıyorsanız, sunucuyu yeniden başlatın:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

IIS veya Tomcat kullanıyorsanız ilgili web sunucusunu yeniden başlatın.

#### Adım 7: Yükseltmeyi Doğrulayın

1. digna dashboard'a erişin
2. Arayüzün düzgün yüklendiğini doğrulayın
3. Sunucu günlüklerini herhangi bir hata için kontrol edin