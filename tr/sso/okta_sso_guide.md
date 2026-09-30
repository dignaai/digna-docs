# Okta ile SSO Kurulumu

Okta OIDC uyumludur, ancak ilk kez yapılan entegrasyonların çoğunu zorlayan bir ayrıntısı vardır: bir Okta org'u birden fazla yetkilendirme sunucusu sunar ve her birinin kendi keşif URL'si vardır.

Bu kılavuz **Okta tarafını** kapsar: uygulama entegrasyonunu oluşturma ve digna'nın ihtiyaç duyduğu değerleri toplama. digna tarafı (`dashboard_config.toml`, test ve sorun giderme) her sağlayıcı için aynıdır ve [Çoklu Oturum Açma Genel Bakış](overview.md) sayfasında açıklanmıştır.

---

## Başlamadan Önce

| Gereksinim | Notlar |
|---|---|
| **Okta rolü** | Super Administrator veya uygulama entegrasyonu oluşturma yetkisi olan bir yönetici rolü |
| **Okta alan adı** | ör. `yourcompany.okta.com` veya yapılandırılmışsa özel bir alan adı |
| **digna yönlendirme URI'si** | Kullanıcıların oturum açtıktan sonra döndüğü URL, ör. `https://digna.yourdomain.com/oidc/callback` |

---

## Adım 1: Uygulama Entegrasyonunu Oluşturun

1. Okta Admin Console'da oturum açın
2. **Applications → Applications** bölümüne gidin
3. **Create App Integration**'a tıklayın
4. Şunları seçin:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. **Next**'e tıklayın

!!! warning "Uygulama Türü Değiştirilemez"

    *Web Application* yerine *Single-Page Application* seçmek, gizli anahtarı olmayan genel bir istemci oluşturur ve digna arka ucunun kod değişimi `invalid_client` hatasıyla başarısız olur. Tür oluşturma sırasında sabitlenir; yanlış bir seçim, uygulamayı silip baştan başlamak anlamına gelir.

---

## Adım 2: Entegrasyonu Yapılandırın

1. **App integration name**: `digna`
2. **Grant type**: *Authorization Code* seçili bırakın
3. **Sign-in redirect URIs**: digna geri çağırma URL'nizi girin:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: isteğe bağlı
5. **Assignments** altında entegrasyonu kimlerin kullanabileceğini seçin; belirli bir grup, *Allow everyone in your organization to access* seçeneğinden daha güvenlidir
6. **Save**'e tıklayın

!!! note "Atama Gereklidir"

    Okta kullanıcının kimliğini doğrular ve ardından kullanıcının uygulamaya atanıp atanmadığını kontrol eder. Atanmamış bir kullanıcı Okta oturum açma sayfasına ulaşır, başarıyla oturum açar ve geri yönlendirme sırasında reddedilir. Oturum açma sizin için çalışıyor ancak iş arkadaşlarınız için çalışmıyorsa ilk kontrol etmeniz gereken şey atamadır.

---

## Adım 3: Kimlik Bilgilerini Toplayın

Uygulamanın **General** sekmesinde, **Client Credentials** altında:

- **Client ID** → `DIGNA_OIDC_CLIENT_ID` olur
- **Client secret** → `DIGNA_OIDC_CLIENT_SECRET` olur (görmek için göz simgesine tıklayın)

---

## Adım 4: Yetkilendirme Sunucusunu Seçin

Keşif URL'nizi belirleyen adım budur. Org'unuzdaki yetkilendirme sunucularını görmek için **Security → API** bölümüne gidin.

**Org yetkilendirme sunucusu**: Okta org'unun kendisi için token verir:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Özel yetkilendirme sunucusu**: Okta'nın oluşturduğu `default` adlı sunucu dahil:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Yerleşik sunucu için `<auth_server_id>` harfi harfine `default` değeridir:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Hangisi?"

    Kuruluşunuz API erişim politikaları için zaten özel bir sunucuyu standart olarak kullanmıyorsa **org** yetkilendirme sunucusunu kullanın. Okta Developer hesapları varsayılan olarak `default` kullanır; birçok kurumsal org ise bunu devre dışı bırakır. Her iki URL'yi de bir tarayıcıda açın; hata yerine JSON döndüren, sizin kullanabileceğiniz sunucudur.

---

## Adım 5: digna'yı Yapılandırın

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

### `config.toml`

```toml
[oidc_clients.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

Her iki dosyadaki `key` eşleşmelidir; burada `okta`.

---

## Adım 6: Test Edin

Arka ucu ve web sunucusunu yeniden başlatın, ardından dashboard'u açın. Tam kontrol listesi için bkz. [Oturum Açmayı Test Etme](overview.md#testing-login).

---

## Okta Sorunlarını Giderme

### Yönlendirme URI'si Kayıtlı Değil

Okta, sorunlu URI'yi hata mesajında belirtir. Bunu **General → Sign-in redirect URIs** ile karşılaştırın; Okta, sondaki eğik çizgi dahil dizenin tamamını eşleştirir.

### Kullanıcı İstemci Uygulamasına Atanmamış

Hesap, uygulamanın atama listesinde değil. Kullanıcıyı veya grubunu **Assignments** altına ekleyin.

### 400 Bad Request: Geçersiz Yetkilendirme Sunucusu

Keşif URL'sindeki `<auth_server_id>` mevcut değil; çoğunlukla kaldırılmış olduğu bir org'da `default`. Gerçekte kullanılabilen sunucular için **Security → API** bölümünü kontrol edin.

### Token Adımında invalid_client

Entegrasyon bir Single-Page Application olarak oluşturulmuş ve istemci gizli anahtarı yok. Bunu bir Web Application olarak yeniden oluşturun.

---

## Ayrıca Bakınız

- [Çoklu Oturum Açma Genel Bakış](overview.md): yapılandırma başvurusu, test ve genel sorun giderme
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)