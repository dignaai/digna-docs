# Çoklu Oturum Açma Genel Bakış

---

## İçindekiler

1. [Giriş ve Genel Bakış](#introduction-and-overview)
2. [Sağlayıcı Kılavuzları](#provider-guides)
3. [Yapılandırma Adımları](#configuration-steps)
4. [Dashboard Yapılandırması](#dashboard-configuration)
5. [Arka Uç Yapılandırması](#backend-configuration)
6. [Oturum Açmayı Test Etme](#testing-login)
7. [Sorun Giderme](#troubleshooting)
8. [Desteklenen Sağlayıcılar](#supported-providers)

---

## Giriş ve Genel Bakış {: #introduction-and-overview }

Bu kılavuz, **OpenID Connect (OIDC)** kullanarak çoklu oturum açmayı (SSO) digna platformuyla entegre etmek için adım adım talimatlar sunar.

### SSO Nedir?

Çoklu oturum açma, kullanıcıların harici kimlik sağlayıcılar aracılığıyla kurumsal kimlik bilgilerini kullanarak digna'da güvenli bir şekilde oturum açmasını sağlar. Kullanıcılar ayrı digna parolaları yönetmek yerine kurumsal kimlik bilgileriyle kimlik doğrulaması yapabilir.

### Nasıl Çalışır

digna'da SSO, OIDC protokolü kullanılarak uygulanır. İki temel yapılandırma dosyası ayarlanarak birden fazla kimlik sağlayıcı paralel olarak yapılandırılabilir:

- **`dashboard_config.toml`**: Ön uç oturum açma arayüzünü kontrol eder
- **`config.toml`**: Arka uç OIDC bağlantılarını yapılandırır

### Desteklenen Sağlayıcılar {: #supported-providers-overview }

Bu kılavuzdaki örnekler **Microsoft** ve **Google** kullanır, ancak **OIDC uyumlu her sağlayıcı** aynı yapı izlenerek entegre edilebilir.

---

## Sağlayıcı Kılavuzları {: #provider-guides }

Her sağlayıcı aynı dört değere ihtiyaç duyar (bir istemci kimliği, bir istemci gizli anahtarı, bir yönlendirme URI'si ve bir keşif URL'si), ancak her biri bunları yönetim konsolunda farklı bir yere koyar ve birçoğunun diğerlerinde bulunmayan sağlayıcıya özel bir adımı vardır. Aşağıdaki kılavuzlar işin bu yarısını kapsar; bu sayfa ise hepsi için aynı olan digna yarısını ele alır.

| Sağlayıcı | Kılavuz | Bilinmesi gerekenler |
|---|---|---|
| **AD FS** | [AD FS ile SSO kurulumu](adfs_sso_guide.md) | Kendi sunucunuzda barındırılır; token hizmetini sizin kontrol ettiğiniz tek sağlayıcıdır |
| **Auth0** | [Auth0 ile SSO kurulumu](auth0_sso_guide.md) | Keşif URL'si kiracıya özeldir ve özel alan adları onu değiştirir |
| **Google Workspace** | [Google Workspace ile SSO kurulumu](google_workspace_sso_guide.md) | Test kullanıcısı olmayanların oturum açabilmesi için onay ekranı yayımlanmalıdır |
| **Keycloak** | [Keycloak ile SSO kurulumu](keycloak_sso_guide.md) | Kendi sunucunuzda barındırılır; keşif URL'si realm'e özeldir |
| **Microsoft Entra ID** | [Microsoft Entra ID ile SSO kurulumu](microsoft_entra_id_sso_guide.md) | Kiracı kimliği keşif URL'sinde yer alır; gizli anahtarların süresi dolar |
| **Okta** | [Okta ile SSO kurulumu](okta_sso_guide.md) | Yetkilendirme sunucusu seçimi keşif URL'sini değiştirir |
| **OneLogin** | [OneLogin ile SSO kurulumu](onelogin_sso_guide.md) | OIDC uygulama türü oluşturma sırasında seçilmelidir ve sonradan değiştirilemez |
| **PingOne** | [PingOne ile SSO kurulumu](pingone_sso_guide.md) | Ortam kimliği keşif URL'sinde yer alır |

OIDC uyumlu diğer tüm sağlayıcılar da aynı şekilde çalışır; bkz. [Diğer OIDC Sağlayıcıları](#supported-providers).

---

## Yapılandırma Adımları {: #configuration-steps }

SSO yapılandırması iki dosyada güncelleme gerektirir. Bu bölüm her birinin nasıl yapılandırılacağını açıklar.

### Yapılandırma Dosyalarına Genel Bakış

| Dosya | Konum | Amaç |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Ön uç oturum açma arayüzü |
| **config.toml** | `/config.toml` | Arka uç OIDC bağlantıları |

SSO'nun düzgün çalışması için her iki dosyanın da yapılandırılması gerekir.

---

## Dashboard Yapılandırması {: #dashboard-configuration }

### Dosya Konumu

```
dashboard/dashboard_config.toml
```

### Adım 1: OIDC Sağlayıcılarını Ekleyin

Desteklemek istediğiniz her kimlik sağlayıcı için `[[login.oidc]]` dizisi altına girişler ekleyin.

**Microsoft ve Google ile örnek:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Adım 2: Oturum Açma Seçeneklerini Yapılandırın

Parola tabanlı oturum açmaya izin verilip verilmeyeceğini belirtin:

```toml
[login]
usePassword = true
```

### Yapılandırma Parametreleri

#### `[[login.oidc]]` Bölümü

| Parametre | Tür | Zorunlu | Açıklama |
|---|---|---|---|
| `key` | string | Evet | OIDC bağlantısı için benzersiz tanımlayıcı (config.toml içindeki key ile eşleşmelidir) |
| `label` | string | Evet | Oturum açma düğmesinde görüntülenen metin (ör. "Login with Microsoft") |

#### `[login]` Bölümü

| Parametre | Tür | Varsayılan | Açıklama |
|---|---|---|---|
| `usePassword` | boolean | false | SSO'ya ek olarak parola tabanlı oturum açmaya izin verir |

### usePassword'ü Anlamak

**`usePassword = true` ise:**
- Oturum açma ekranı SSO düğmelerini gösterir (ör. "Login with Microsoft")
- Oturum açma ekranı ayrıca kullanıcı adı ve parola alanlarını da gösterir
- Kullanıcılar her iki yöntemle de kimlik doğrulaması yapabilir
- Bazı kullanıcıların SSO, diğerlerinin parola kullandığı karma kurulumlara olanak tanır

**`usePassword = false` ise (veya belirtilmemişse):**
- Oturum açma ekranı yalnızca SSO düğmelerini gösterir
- Kullanıcı adı/parola alanları yoktur
- Yalnızca OIDC kimlik doğrulaması kullanılabilir

!!! tip "İpucu"

    Parola tabanlı oturum açma yalnızca `digna user add` komutuyla veya dashboard üzerinden parolayla oluşturulmuş kullanıcılar için kullanılabilir.

### Tam Örnek

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## Arka Uç Yapılandırması {: #backend-configuration }

### Dosya Konumu

```
/config.toml
```

(digna kurulumunun kök dizini)

### Adım 1: OIDC Sağlayıcı Bölümlerini Ekleyin

Her sağlayıcının kendine ayrılmış bir `[oidc_clients.<key>]` bölümü olmalıdır. Anahtar, `dashboard_config.toml` içinde tanımlanan `key` ile eşleşmelidir.

### Microsoft Yapılandırması

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google Yapılandırması

```toml
[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Yapılandırma Parametreleri

| Parametre | Tür | Zorunlu | Açıklama | Örnek |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Evet | Kimlik sağlayıcıdan alınan istemci kimliği | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Evet | Kimlik sağlayıcıdan alınan istemci gizli anahtarı | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Evet | Kimlik doğrulamadan sonraki geri çağırma URL'si | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Evet | OIDC yapılandırma uç noktası | `https://login.microsoftonline.com/...` |

!!! warning "Önemli"

    Yer tutucu değerleri (`<client_id>`, `<client_secret>`, `<tenant_id>`) kimlik sağlayıcınızın geliştirici portalından alınan gerçek kimlik bilgileriyle değiştirin.

### Yönlendirme URI'si

Yönlendirme URI'si, kimlik sağlayıcı yapılandırmanızdakiyle aynı olmalıdır:

```
http://localhost:5173/oidc/callback
```

digna farklı bir alan adında barındırılıyorsa buna göre güncelleyin:
- Yerel: `http://localhost:5173/oidc/callback`
- Üretim: `https://digna.yourdomain.com/oidc/callback`

### Tam Örnek

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Oturum Açmayı Test Etme {: #testing-login }

Yapılandırmayı tamamladıktan sonra SSO'nun doğru çalıştığını doğrulayın.

### Test Öncesi Kontrol Listesi

Test etmeden önce şunlardan emin olun:

- [ ] `dashboard_config.toml` OIDC sağlayıcılarıyla güncellendi
- [ ] `config.toml` OIDC kimlik bilgileriyle güncellendi
- [ ] Her iki dosya da kaydedildi
- [ ] Kimlik bilgileri doğru (istemci kimliği, istemci gizli anahtarı)
- [ ] Yönlendirme URI'si dağıtım URL'nizle eşleşiyor
- [ ] Kimlik sağlayıcı uygulaması yönlendirme URI'siyle yapılandırıldı

### Test Adımları

#### Adım 1: Hizmetleri Yeniden Başlatın

Değişiklikleri uygulamak için digna arka ucunu ve web sunucusunu yeniden başlatın.

**Windows'ta hizmet olarak çalışıyorsa:**
```bash
cd C:\path\to\digna
digna windows stop
digna windows start
```

**Linux veya macOS'ta hizmet olarak çalışıyorsa:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Elle çalıştırılıyorsa:**
```bash
digna serve --address localhost --port 8082
```

**Web sunucusunu da yeniden başlatın**: Windows'ta IIS veya Tomcat, Linux ve macOS'ta nginx veya Apache.

#### Adım 2: Dashboard'u Açın

digna dashboard'unu tarayıcınızda açın:

```
http://localhost:5173
```

(veya yapılandırdığınız dashboard URL'si)

#### Adım 3: Oturum Açma Düğmelerini Doğrulayın

Yapılandırılan her sağlayıcı için oturum açma düğmelerinin göründüğünü kontrol edin:

- "Login with Microsoft" düğmesini görmelisiniz
- "Login with Google" düğmesini görmelisiniz
- (usePassword = true ise) Kullanıcı adı/parola alanlarını görmelisiniz

Düğmeler görünmüyorsa:
- `dashboard_config.toml` dosyasının kaydedildiğini kontrol edin
- Dashboard hizmetinin yeniden başlatıldığını kontrol edin
- Hatalar için tarayıcı konsolunu (F12) kontrol edin

#### Adım 4: SSO ile Oturum Açmayı Test Edin

SSO düğmelerinden birine tıklayın (ör. "Login with Microsoft"):

1. Kimlik sağlayıcının oturum açma sayfasına yönlendirilmelisiniz
2. Kurumsal kimlik bilgilerinizle oturum açın
3. digna'ya geri yönlendirilmelisiniz
4. digna'da oturum açmış olmalısınız

#### Adım 5: Kullanıcı Oluşturulmasını Doğrulayın

Başarılı bir SSO oturum açma işleminden sonra:

- Kullanıcı digna'da otomatik olarak oluşturulmuş olmalıdır
- Kullanıcı oturum açmış olmalıdır
- Kullanıcı profili, kimlik sağlayıcınızdaki kimlik bilgilerini göstermelidir
- digna dashboard'unu görmelisiniz

#### Adım 6: Parola ile Oturum Açmayı Test Edin (Etkinse)

`usePassword = true` ise:

1. digna'dan oturumu kapatın
2. Oturum açma sayfasında bir kullanıcı adı ve parola girin
3. Parola kimlik bilgileriyle oturum açabilmelisiniz

---

## Sorun Giderme {: #troubleshooting }

### Oturum Açma Düğmeleri Görünmüyor

**Belirtiler:**
- OIDC oturum açma düğmeleri oturum açma sayfasında görünmüyor
- Yalnızca parola alanları görünüyor (usePassword = true ise)

**Nedenler ve Çözümler:**
1. `dashboard_config.toml` dosyasının `dashboard/` dizininde olduğunu kontrol edin
2. `[[login.oidc]]` bölümlerinin doğru sözdizimiyle mevcut olduğunu doğrulayın
3. Dashboard hizmetini yeniden başlatın
4. Tarayıcı önbelleğini temizleyin (Ctrl+Shift+Delete veya Cmd+Shift+Delete)
5. Hatalar için tarayıcı konsolunu (F12 → Console sekmesi) kontrol edin

---

### Yönlendirme URI'si Uyuşmazlığı Hatası

**Belirtiler:**
- SSO düğmesine tıkladıktan sonra "redirect_uri mismatch" ile ilgili bir hata
- "The redirect URI is not registered" hatası

**Nedenler ve Çözümler:**
1. `config.toml` içindeki `DIGNA_OIDC_REDIRECT_URI` değerinin doğru olduğunu doğrulayın
2. Yönlendirme URI'sinin kimlik sağlayıcı ayarlarında kayıtlı olduğunu doğrulayın
3. Her ikisinin de birebir aynı URL'yi (protokol, alan adı ve yol dahil) kullandığından emin olun
4. Yönlendirme URI'sinde yazım hatası olup olmadığını kontrol edin
5. HTTPS kullanıyorsanız sertifikanın geçerli olduğundan emin olun

---

### Geçersiz İstemci Kimlik Bilgileri Hatası

**Belirtiler:**
- "Invalid client ID or secret" hatası
- Kimlik doğrulama bir kimlik bilgisi hatasıyla başarısız oluyor

**Nedenler ve Çözümler:**
1. `DIGNA_OIDC_CLIENT_ID` ve `DIGNA_OIDC_CLIENT_SECRET` değerlerinin doğru olduğunu doğrulayın
2. Fazladan boşluk veya özel karakter olmadığından emin olun
3. Kimlik bilgilerinin süresinin dolmadığını veya iptal edilmediğini kontrol edin
4. Yapılandırmayı güncelledikten sonra arka uç hizmetini yeniden başlatın
5. Kimlik bilgilerinin etkin olduğunu doğrulamak için kimlik sağlayıcı konsolunu kontrol edin

---

### Oturum Açma Takılıyor veya Zaman Aşımına Uğruyor

**Belirtiler:**
- SSO düğmesine tıklamak hiçbir şey yapmıyor
- Birkaç saniye sonra zaman aşımı
- Tarayıcı "Failed to connect" veya benzeri bir mesaj gösteriyor

**Nedenler ve Çözümler:**
1. digna arka ucunun çalıştığını doğrulayın: `digna repo check`
2. Kimlik sağlayıcıya ağ bağlantısını kontrol edin
3. `DIGNA_OIDC_CONFIGURATION_URL` adresine erişilebildiğini doğrulayın
4. Güvenlik duvarı kurallarının giden HTTPS bağlantılarına izin verdiğini kontrol edin
5. Arka uç ile dashboard'un birbirine erişebildiğini doğrulayın

---

### Kullanıcılar Otomatik Olarak Oluşturulmuyor

**Belirtiler:**
- SSO ile oturum açma başarılı ancak kullanıcı digna'da oluşturulmuyor
- SSO ile oturum açtıktan sonra yetki hatası alınıyor

**Nedenler ve Çözümler:**
1. OIDC yapılandırmasının doğru olduğunu doğrulayın
2. Kullanıcı yetkilerinin ayarlandığını kontrol edin
3. Hata mesajları için digna günlüklerini inceleyin
4. Arka uç hizmetini yeniden başlatın
5. Sorun devam ederse support@digna.ai ile iletişime geçin

---

## Desteklenen Sağlayıcılar {: #supported-providers }

### Test Edilmiş ve Desteklenen

Aşağıdaki OIDC sağlayıcıları test edilmiştir ve çalıştıkları bilinmektedir:

| Sağlayıcı | Yapılandırma URL'si | Kurulum Kılavuzu |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [AD FS ile SSO kurulumu](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Auth0 ile SSO kurulumu](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Workspace ile SSO kurulumu](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Keycloak ile SSO kurulumu](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Entra ID ile SSO kurulumu](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta ile SSO kurulumu](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [OneLogin ile SSO kurulumu](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [PingOne ile SSO kurulumu](pingone_sso_guide.md) |

### Diğer OIDC Sağlayıcıları

OpenID Connect'i destekleyen her sağlayıcı entegre edilebilir. Gerekli bilgiler:

- İstemci kimliği
- İstemci gizli anahtarı
- OpenID yapılandırma URL'si (genellikle `/.well-known/openid-configuration` adresinde)
- Desteklenen kapsamlar (genellikle `openid profile email`)

Belirli bir sağlayıcıyı entegre etmek için yardıma ihtiyacınız varsa support@digna.ai ile iletişime geçin.

---

## En İyi Uygulamalar

**YAPIN:**
- Üretimde HTTPS kullanın (HTTP değil)
- İstemci gizli anahtarlarını güvenli bir şekilde saklayın (mümkünse ortam değişkenleri kullanın)
- Gizli anahtarları düzenli aralıklarla yenileyin
- Önce üretim dışı bir ortamda test edin
- Hangi sağlayıcıların yapılandırıldığını belgeleyin
- Olağandışı etkinlikler için oturum açma günlüklerini izleyin
- Kimlik sağlayıcı yapılandırmasını digna yapılandırmasıyla eşit tutun

**YAPMAYIN:**
- İstemci gizli anahtarlarını sürüm kontrolünde saklamayın
- Üretimde HTTP yönlendirme URI'leri kullanmayın
- Birden fazla sağlayıcıyı aynı anahtarla yapılandırmayın
- Üretimde varsayılan/test kimlik bilgilerini bırakmayın
- Gizli bilgiler içeren yapılandırma dosyalarını açığa çıkarmayın
- Geliştirme ve üretim kimlik bilgilerini karıştırmayın

---

## Destek

SSO yapılandırması konusunda yardıma mı ihtiyacınız var?

- **E-posta:** support@digna.ai
- **Dokümantasyon:** https://docs.digna.ai
- **Web sitesi:** https://www.digna.ai

---

**Son Güncelleme:** 30 Ağustos 2026  
**Sürüm:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**