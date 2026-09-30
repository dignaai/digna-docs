# Auth0 ile SSO Kurulumu

Auth0 OIDC uyumludur ve her kiracı için bir keşif uç noktası sunar. Doğru yapılması gereken asıl şey, keşif URL'sinde yer alan ve özel bir alan adı etkinleştirirseniz değişen kiracı alan adıdır.

Bu kılavuz **Auth0 tarafını** kapsar: uygulamayı oluşturma ve digna'nın ihtiyaç duyduğu değerleri toplama. digna tarafı (`dashboard_config.toml`, test ve sorun giderme) her sağlayıcı için aynıdır ve [Çoklu Oturum Açma Genel Bakış](overview.md) sayfasında açıklanmıştır.

---

## Başlamadan Önce

| Gereksinim | Notlar |
|---|---|
| **Auth0 rolü** | Kiracıda yönetici |
| **Kiracı alan adı** | ör. `yourcompany.eu.auth0.com`; bölge kısmı önemlidir |
| **digna yönlendirme URI'si** | Kullanıcıların oturum açtıktan sonra döndüğü URL, ör. `https://digna.yourdomain.com/oidc/callback` |

---

## Adım 1: Uygulamayı Oluşturun

1. [Auth0 Dashboard](https://manage.auth0.com)'da oturum açın
2. **Applications → Applications** bölümüne gidin
3. **Create Application**'a tıklayın
4. Uygulamaya `digna` adını verin ve **Regular Web Applications**'ı seçin
5. **Create**'e tıklayın

!!! warning "Regular Web Applications'ı Seçin"

    *Single Page Application* ve *Native*, gizli anahtarı olmayan genel istemciler oluşturur. digna kod değişimini arka ucundan gerçekleştirir ve gizli (confidential) bir istemciye ihtiyaç duyar; bu nedenle doğru tür **Regular Web Applications**'dır. Bazı sağlayıcıların aksine Auth0, türü daha sonra **Settings → Application Type** altından değiştirmenize izin verir.

---

## Adım 2: Geri Çağırma URL'sini Ekleyin

Uygulamanın **Settings** sekmesinde:

1. **Allowed Callback URLs** alanını bulun
2. digna geri çağırma URL'nizi girin:

```
https://digna.yourdomain.com/oidc/callback
```

3. İsteğe bağlı olarak **Allowed Logout URLs** alanını dashboard URL'niz olarak ayarlayın
4. Sayfanın en altına kaydırın ve **Save Changes**'a tıklayın

!!! note "Satır Sonuyla Değil, Virgülle Ayrılmış"

    Auth0 bu alanda virgülle ayrılmış birden fazla geri çağırma URL'sini kabul eder. Yalnızca satır sonlarıyla ayrılmış bir liste tek bir hatalı URL olarak okunur ve fark edilmeden hiçbir şeyle eşleşmez.

---

## Adım 3: Kimlik Bilgilerini Toplayın

Yine **Settings** sekmesinde, **Basic Information** panelinde:

- **Domain** → keşif URL'sine girer
- **Client ID** → `DIGNA_OIDC_CLIENT_ID` olur
- **Client Secret** → `DIGNA_OIDC_CLIENT_SECRET` olur (görmek için tıklayın)

---

## Adım 4: İzin Türünü Doğrulayın

1. **Settings → Advanced Settings → Grant Types** bölümüne gidin
2. **Authorization Code** seçeneğinin işaretli olduğunu doğrulayın

Bu, Regular Web Applications için varsayılan olarak etkindir. İşareti kaldırılmışsa digna'da oturum açma `unauthorized_client` hatasıyla başarısız olur.

---

## Adım 5: Keşif URL'sini Oluşturun

Adım 3'teki **Domain** değerini yerine koyun:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Örneğin:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Özel Alan Adları Yayıncıyı (Issuer) Değiştirir"

    Kiracınız `login.yourcompany.com` gibi özel bir alan adı kullanıyorsa keşif URL'sinde o alan adını kullanın. İkisini karıştırmak (keşif URL'sinde standart alan adı, tarayıcıda özel alan adı) bir issuer uyuşmazlığına yol açar ve token, aksi halde başarılı olan bir oturum açmanın ardından reddedilir.

---

## Adım 6: digna'yı Yapılandırın

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Login with Auth0"
```

### `config.toml`

```toml
[oidc_clients.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

Her iki dosyadaki `key` eşleşmelidir; burada `auth0`.

---

## Adım 7: Test Edin

Arka ucu ve web sunucusunu yeniden başlatın, ardından dashboard'u açın. Tam kontrol listesi için bkz. [Oturum Açmayı Test Etme](overview.md#testing-login).

---

## Auth0 Sorunlarını Giderme

### Geri Çağırma URL'si Uyuşmazlığı

Auth0'ın hata sayfası aldığı URL'yi belirtir. Girişlerin virgülle ayrıldığını kontrol ederek bu URL'yi **Allowed Callback URLs** alanına ekleyin.

### unauthorized_client

**Advanced Settings → Grant Types** altında **Authorization Code** etkin değil veya uygulama türü Regular Web Applications değil.

### Başarılı Oturum Açmanın Ardından Erişim Reddediliyor

Kiracıdaki bir Rule, Action veya Post-Login tetikleyicisi kullanıcıyı reddediyor. **Actions → Flows → Login** bölümünü ve tam nedeni gösteren **Monitoring → Logs** altındaki kiracı günlüklerini kontrol edin.

### Issuer Uyuşmazlığı

Keşif URL'si ile tarayıcının yönlendirildiği alan adı farklı; genellikle standart kiracı alan adı ile özel alan adı arasındaki fark. Tutarlı bir şekilde birini kullanın.

---

## Ayrıca Bakınız

- [Çoklu Oturum Açma Genel Bakış](overview.md): yapılandırma başvurusu, test ve genel sorun giderme
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)