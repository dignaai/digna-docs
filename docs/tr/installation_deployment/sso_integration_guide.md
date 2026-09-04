---
title: Tek Oturum Açma (SSO) Entegrasyon Kılavuzu | digna Dokümantasyonu
description: digna için OpenID Connect (OIDC) kullanarak Tek Oturum Açma (SSO) yapılandırmasına ilişkin adım adım kılavuz. Panel ve arka uç yapılandırması, test, sorun giderme ve Microsoft Entra ID, Google Workspace ve Okta dahil desteklenen kimlik sağlayıcıları ele alınır.
image: /assets/logo_square.png
keywords:
  - digna sso
  - tek oturum açma
  - oidc entegrasyonu
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta entegrasyonu
  - kurumsal kimlik doğrulama
lang: tr
robots: index, follow
og_title: digna Tek Oturum Açma (SSO) Entegrasyon Kılavuzu
og_description: OpenID Connect kullanarak digna için Tek Oturum Açma'yı yapılandırın. Microsoft Entra ID, Google Workspace, Okta ve diğer OIDC uyumlu kimlik sağlayıcıları için adım adım kurulum.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Tek Oturum Açma Entegrasyon Kılavuzu

---

## İçindekiler

1. [Giriş ve Genel Bakış](#introduction-and-overview)
2. [Yapılandırma Adımları](#configuration-steps)
3. [Panel Yapılandırması](#dashboard-configuration)
4. [Arka Uç Yapılandırması](#backend-configuration)
5. [Giriş Testi](#testing-login)
6. [Sorun Giderme](#troubleshooting)
7. [Desteklenen Sağlayıcılar](#supported-providers)

---

## Giriş ve Genel Bakış {: #introduction-and-overview }

Bu kılavuz, digna platformu için **OpenID Connect (OIDC)** kullanarak Tek Oturum Açma (SSO) entegrasyonuna ilişkin adım adım yönergeler sağlar.

### SSO Nedir?

Tek Oturum Açma, kullanıcıların kurumsal kimlik bilgilerini kullanarak digna'ya güvenli bir şekilde giriş yapmalarına olanak tanır. Kullanıcılar ayrı digna parolaları yönetmek yerine şirket kimlik bilgileriyle kimlik doğrulayabilirler.

### Nasıl Çalışır

digna'daki SSO, OIDC protokolü kullanılarak uygulanır. Birden fazla kimlik sağlayıcı, iki temel yapılandırma dosyasını düzenleyerek paralel olarak yapılandırılabilir:

- **`dashboard_config.toml`** — Önyüz (frontend) giriş arayüzünü kontrol eder
- **`config.toml`** — Arka uç OIDC bağlantılarını yapılandırır

### Desteklenen Sağlayıcılar {: #supported-providers-overview }

Bu kılavuzdaki örnekler **Microsoft** ve **Google** kullanır, ancak **herhangi bir OIDC-uyumlu sağlayıcı** aynı yapı izlenerek entegre edilebilir.

Yaygın OIDC sağlayıcıları şunlardır:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Diğer OIDC-uyumlu kimlik sağlayıcıları

---

## Yapılandırma Adımları {: #configuration-steps }

SSO yapılandırması iki dosyanın güncellenmesini gerektirir. Bu bölüm her bir dosyanın nasıl yapılandırılacağını açıklar.

### Yapılandırma Dosyalarının Genel Bakışı

| Dosya | Konum | Amaç |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Önyüz giriş arayüzü |
| **config.toml** | `/config.toml` | Arka uç OIDC bağlantıları |

SSO'nun düzgün çalışması için her iki dosyanın da yapılandırılması gereklidir.

---

## Panel Yapılandırması {: #dashboard-configuration }

### Dosya Konumu

```
dashboard/dashboard_config.toml
```

### Adım 1: OIDC Sağlayıcılarını Ekleyin

Desteklemek istediğiniz her kimlik sağlayıcısı için `[[login.oidc]]` dizisi altına girişler ekleyin.

**Microsoft ve Google ile örnek:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Microsoft ile giriş"

[[login.oidc]]
key = "google"
label = "Google ile giriş"
```

### Adım 2: Giriş Seçeneklerini Yapılandırın

Parola tabanlı girişe izin verilip verilmeyeceğini belirtin:

```toml
[login]
usePassword = true
```

### Yapılandırma Parametreleri

#### `[[login.oidc]]` Bölümü

| Parametre | Tür | Gereklilik | Açıklama |
|---|---|---|---|
| `key` | string | Evet | OIDC bağlantısı için benzersiz tanımlayıcı (config.toml'deki key ile eşleşmeli) |
| `label` | string | Evet | Giriş düğmesinde gösterilecek metin (ör. "Microsoft ile giriş") |

#### `[login]` Bölümü

| Parametre | Tür | Varsayılan | Açıklama |
|---|---|---|---|
| `usePassword` | boolean | false | SSO'ya ek olarak parola tabanlı girişe izin verilsin mi |

### usePassword'ın Anlaşılması

**Eğer `usePassword = true` ise:**
- Giriş ekranında SSO düğmeleri (ör. "Microsoft ile giriş") görünür
- Giriş ekranında ayrıca kullanıcı adı ve parola alanları görünür
- Kullanıcılar her iki yöntemle de kimlik doğrulayabilir
- Bazı kullanıcıların SSO, bazılarının parola kullanabileceği hibrit kurulumlara izin verir

**Eğer `usePassword = false` (veya belirtilmemiş) ise:**
- Giriş ekranında yalnızca SSO düğmeleri görünür
- Kullanıcı adı/parola alanı yoktur
- Sadece OIDC ile kimlik doğrulama kullanılabilir

> **İpucu**
>
> Parola tabanlı giriş, yalnızca `digna user add` komutuyla veya panel üzerinden parola ile oluşturulmuş kullanıcılar için kullanılabilir.

### Tam Örnek

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Microsoft ile giriş"

[[login.oidc]]
key = "google"
label = "Google ile giriş"

[[login.oidc]]
key = "okta"
label = "Okta ile giriş"
```

---

## Arka Uç Yapılandırması {: #backend-configuration }

### Dosya Konumu

```
/config.toml
```

(Root digna kurulum dizini)

### Adım 1: OIDC Sağlayıcı Bölümlerini Ekleyin

Her sağlayıcı için ayrılmış bir `[oidc.<key>]` bölümü olmalıdır. Key, `dashboard_config.toml` içinde tanımlanan `key` ile eşleşmelidir.

### Microsoft Yapılandırması

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google Yapılandırması

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Yapılandırma Parametreleri

| Parametre | Tür | Gereklilik | Açıklama | Örnek |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Evet | Kimlik sağlayıcıdan alınan Client ID | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Evet | Kimlik sağlayıcıdan alınan Client Secret | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Evet | Kimlik doğrulama sonrası geri çağırma (callback) URL'si | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Evet | OIDC yapılandırma uç noktası | `https://login.microsoftonline.com/...` |

> **Önemli**
>
> Yer tutucu değerleri (`<client_id>`, `<client_secret>`, `<tenant_id>`) kimlik sağlayıcınızın geliştirici portalından alınan gerçek kimlik bilgileriyle değiştirin.

### Redirect URI

Redirect URI, kimlik sağlayıcı yapılandırmasında da aynı olmalıdır:

```
http://localhost:5173/oidc/callback
```

digna farklı bir alan adında barındırılıyorsa uygun şekilde güncelleyin:
- Yerel: `http://localhost:5173/oidc/callback`
- Üretim: `https://digna.yourdomain.com/oidc/callback`

### Tam Örnek

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Giriş Testi {: #testing-login }

Yapılandırmayı tamamladıktan sonra SSO'nun doğru çalıştığını doğrulayın.

### Ön Test Kontrol Listesi

Testten önce emin olun:

- [ ] `dashboard_config.toml` OIDC sağlayıcılarıyla güncellendi
- [ ] `config.toml` OIDC kimlik bilgileriyle güncellendi
- [ ] Her iki dosya da kaydedildi
- [ ] Kimlik bilgileri doğru (client ID, client secret)
- [ ] Redirect URI dağıtım URL'inizle eşleşiyor
- [ ] Kimlik sağlayıcı uygulaması redirect URI ile yapılandırıldı

### Test Adımları

#### Adım 1: Servisleri Yeniden Başlatın

Değişikliklerin uygulanması için digna arka ucu ve web sunucusunu yeniden başlatın.

**Windows servisi olarak çalıştırılıyorsa:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Manuel çalıştırılıyorsa:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**IIS veya Tomcat kullanılıyorsa:**
Web sunucusu servisinizi yeniden başlatın.

#### Adım 2: Paneli Açın

Tarayıcınızda digna panelini açın:

```
http://localhost:5173
```

(veya yapılandırdığınız panel URL'si)

#### Adım 3: Giriş Düğmelerini Doğrulayın

Yapılandırılan her sağlayıcı için giriş düğmelerinin göründüğünü kontrol edin:

- "Microsoft ile giriş" düğmesi görünmeli
- "Google ile giriş" düğmesi görünmeli
- (`usePassword = true` ise) Kullanıcı adı/parola alanları görünmeli

Düğmeler görünmüyorsa:
- `dashboard_config.toml` dosyasının kaydedildiğini kontrol edin
- Panel servisinin yeniden başlatıldığını doğrulayın
- Tarayıcı konsolunu (F12) hata için kontrol edin

#### Adım 4: SSO Girişini Test Edin

SSO düğmelerinden birine tıklayın (ör. "Microsoft ile giriş"):

1. Kimlik sağlayıcının giriş sayfasına yönlendirilmelisiniz
2. Kurumsal kimlik bilgilerinizi kullanarak giriş yapın
3. digna'ya geri yönlendirilmelisiniz
4. digna'ya giriş yapmış olmalısınız

#### Adım 5: Kullanıcı Oluşumunu Doğrulayın

Başarılı SSO girişinden sonra:

- Kullanıcı otomatik olarak digna'da oluşturulmalı
- Kullanıcı giriş yapmış olmalı
- Kullanıcı profili kimlik sağlayıcı bilgilerinizi göstermeli
- digna panelini görmelisiniz

#### Adım 6: Parola Girişini Test Edin (Etkinse)

Eğer `usePassword = true` ise:

1. digna'dan çıkış yapın
2. Giriş sayfasında kullanıcı adı ve parola girin
3. Parola ile giriş yapabilmelisiniz

---

## Sorun Giderme {: #troubleshooting }

### Giriş Düğmeleri Görünmüyor

**Belirtiler:**
- Giriş sayfasında OIDC giriş düğmeleri görünmüyor
- Sadece parola alanları görünüyor (eğer usePassword = true ise)

**Nedenler & Çözümler:**
1. `dashboard_config.toml` dosyasının `dashboard/` dizininde olduğunu kontrol edin
2. `[[login.oidc]]` bölümlerinin doğru sözdizimiyle mevcut olduğunu doğrulayın
3. Panel servisini yeniden başlatın
4. Tarayıcı önbelleğini temizleyin (Ctrl+Shift+Delete veya Cmd+Shift+Delete)
5. Tarayıcı konsolunu (F12 → Console) hatalar için kontrol edin

---

### Redirect URI Uyuşmazlığı Hatası

**Belirtiler:**
- SSO düğmesine tıkladıktan sonra "redirect_uri mismatch" hatası
- "The redirect URI is not registered" hatası

**Nedenler & Çözümler:**
1. `config.toml` içindeki `DIGNA_OIDC_REDIRECT_URI` değerinin doğru olduğunu doğrulayın
2. Redirect URI'nin kimlik sağlayıcı ayarlarında kayıtlı olduğunu kontrol edin
3. Protokol, domain ve yol dahil olmak üzere her iki tarafta da URL'lerin tamamen aynı olduğundan emin olun
4. Redirect URI'de yazım hatası olup olmadığını kontrol edin
5. HTTPS kullanılıyorsa sertifikanın geçerli olduğundan emin olun

---

### Geçersiz İstemci Kimlik Bilgileri Hatası

**Belirtiler:**
- "Invalid client ID or secret" hatası
- Kimlik doğrulama kimlik bilgileri hatasıyla başarısız oluyor

**Nedenler & Çözümler:**
1. `DIGNA_OIDC_CLIENT_ID` ve `DIGNA_OIDC_CLIENT_SECRET` değerlerinin doğru olduğunu doğrulayın
2. Fazladan boşluk veya yanlış karakter olmadığından emin olun
3. Kimlik bilgilerinin süresinin dolmadığını veya iptal edilmediğini kontrol edin
4. Yapılandırmayı güncelledikten sonra arka uç servisini yeniden başlatın
5. Kimlik sağlayıcı konsolunda kimlik bilgilerini aktif olarak doğrulayın

---

### Giriş Donuyor veya Zaman Aşımı Oluyor

**Belirtiler:**
- SSO düğmesine tıklamak hiçbir şey yapmıyor
- Birkaç saniye sonra zaman aşımı oluyor
- Tarayıcı "Bağlanılamadı" veya benzeri gösteriyor

**Nedenler & Çözümler:**
1. digna arka ucunun çalıştığını doğrulayın: `digna repo check`
2. Kimlik sağlayıcıya ağ bağlantısını kontrol edin
3. `DIGNA_OIDC_CONFIGURATION_URL` erişilebilir mi kontrol edin
4. Güvenlik duvarı kurallarının çıkış HTTPS bağlantılarına izin verdiğini doğrulayın
5. Arka uç ile panelin birbirine erişebildiğini doğrulayın

---

### Kullanıcılar Otomatik Oluşturulmuyor

**Belirtiler:**
- SSO girişi başarılı ama digna içinde kullanıcı oluşturulmuyor
- SSO girişinden sonra izin hatası alınıyor

**Nedenler & Çözümler:**
1. OIDC yapılandırmasının doğru olduğunu doğrulayın
2. Kullanıcı izinlerinin düzgün ayarlandığını kontrol edin
3. digna loglarını hata mesajları için inceleyin
4. Arka uç servisini yeniden başlatın
5. Sorun devam ederse support@digna.ai ile iletişime geçin

---

## Desteklenen Sağlayıcılar {: #supported-providers }

### Test Edilen ve Desteklenenler

Aşağıdaki OIDC sağlayıcıları test edilmiş ve çalıştığı doğrulanmıştır:

| Sağlayıcı | Yapılandırma URL'si | Kurulum Kılavuzu |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Diğer OIDC Sağlayıcıları

OpenID Connect'i destekleyen herhangi bir sağlayıcı entegre edilebilir. Gerekli bilgiler:

- Client ID
- Client secret
- OpenID yapılandırma URL'si (genellikle `/.well-known/openid-configuration` altında)
- Desteklenen scope'lar (genellikle `openid profile email`)

Belirli bir sağlayıcının entegrasyonunda yardıma ihtiyacınız olursa support@digna.ai ile iletişime geçin.

---

## En İyi Uygulamalar

YAPIN:
- Üretimde HTTPS kullanın (HTTP kullanmayın)
- Client secret'ları güvenli şekilde saklayın (mümkünse ortam değişkenleri kullanın)
- Secret'ları düzenli olarak döndürün
- Önce üretim dışı ortamda test edin
- Hangi sağlayıcıların yapılandırıldığını belgeleyin
- Olağandışı etkinlikler için giriş loglarını izleyin
- Kimlik sağlayıcı yapılandırmasını digna yapılandırmasıyla senkron tutun

YAPMAYIN:
- Client secret'ları versiyon kontrol sisteminde saklamayın
- Üretimde HTTP redirect URI'leri kullanmayın
- Aynı key ile birden fazla sağlayıcı yapılandırmayın
- Üretimde varsayılan/test kimlik bilgilerini bırakmayın
- İçeriklerinde secret olan yapılandırma dosyalarını açığa çıkarmayın
- Geliştirme ve üretim kimlik bilgilerini karıştırmayın

---

## Destek

SSO yapılandırması ile ilgili yardıma mı ihtiyacınız var?

- **E-posta:** support@digna.ai
- **Dokümantasyon:** https://docs.digna.ai
- **Web sitesi:** https://www.digna.ai

---

**Son Güncelleme:** 30 Ağustos 2026  
**Sürüm:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**