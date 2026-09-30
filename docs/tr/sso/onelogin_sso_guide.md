---
title: OneLogin SSO – Çoklu Oturum Açma Entegrasyonu | digna Dokümantasyonu
description: "OpenID Connect kullanarak OneLogin ile digna için çoklu oturum açmayı yapılandırın: OIDC uygulaması oluşturma, yönlendirme URI'leri, istemci kimlik bilgileri, token uç noktası kimlik doğrulaması ve buna uygun digna yapılandırması."
image: /assets/logo_square.png
keywords: digna sso, onelogin sso, onelogin oidc, openid connect, token uç noktası kimlik doğrulaması, kurumsal kimlik doğrulama
---

# OneLogin ile SSO Kurulumu

OneLogin OIDC uyumludur. Ayırt edici özelliği, bağlayıcı türünün uygulama oluşturulurken bir katalogdan seçilmesi ve daha sonra değiştirilememesidir.

Bu kılavuz **OneLogin tarafını** kapsar: uygulamayı oluşturma ve digna'nın ihtiyaç duyduğu değerleri toplama. digna tarafı (`dashboard_config.toml`, test ve sorun giderme) her sağlayıcı için aynıdır ve [Çoklu Oturum Açma Genel Bakış](overview.md) sayfasında açıklanmıştır.

---

## Başlamadan Önce

| Gereksinim | Notlar |
|---|---|
| **OneLogin rolü** | Hesap sahibi veya uygulama ekleme yetkisi olan bir yönetici |
| **Alt alan adı** | ör. `yourcompany.onelogin.com` |
| **digna yönlendirme URI'si** | Kullanıcıların oturum açtıktan sonra döndüğü URL, ör. `https://digna.yourdomain.com/oidc/callback` |

---

## Adım 1: OIDC Uygulamasını Oluşturun

1. OneLogin Admin portalında oturum açın
2. **Applications → Applications** bölümüne gidin
3. **Add App**'e tıklayın
4. `OpenId Connect` araması yapın ve **OpenId Connect (OIDC)** bağlayıcısını seçin
5. **Display Name** değerini `digna` olarak ayarlayın
6. **Save**'e tıklayın

!!! warning "Bağlayıcı Türü Oluşturma Sırasında Sabitlenir"

    OneLogin'de SAML ve OIDC için ayrı katalog girişleri vardır ve bir uygulama birinden diğerine dönüştürülemez. Yanlışlıkla bir SAML bağlayıcısı seçerseniz uygulamayı silip yeniden ekleyin; protokol değiştirmek için bir ayar yoktur.

---

## Adım 2: Yönlendirme URI'sini Yapılandırın

1. **Configuration** sekmesini açın
2. **Redirect URI's** alanına digna geri çağırma URL'nizi girin:

```
https://digna.yourdomain.com/oidc/callback
```

3. İsteğe bağlı olarak **Post Logout Redirect URIs** alanını dashboard URL'niz olarak ayarlayın
4. **Save**'e tıklayın

!!! note "Her Satıra Bir URI"

    Virgülle ayrılmış bir liste bekleyen sağlayıcıların aksine OneLogin'in **Redirect URI's** alanı her satırda bir URI alır.

---

## Adım 3: Uygulama Türünü ve Kimlik Doğrulama Yöntemini Ayarlayın

1. **SSO** sekmesini açın
2. **Application Type** değerinin *Web* olduğunu doğrulayın
3. **Token Endpoint → Authentication Method** değerini *POST* (`client_secret_post`) veya *Basic* (`client_secret_basic`) olarak ayarlayın

!!! warning "None Seçmeyin"

    Kimlik doğrulama yöntemini *None* olarak ayarlamak uygulamayı gizli anahtarı olmayan genel bir istemci yapar ve digna arka ucunun kod değişimi reddedilir. POST veya Basic'in ikisi de çalışır.

---

## Adım 4: Kimlik Bilgilerini Toplayın

Yine **SSO** sekmesinde:

- **Client ID** → `DIGNA_OIDC_CLIENT_ID` olur
- **Client Secret** → `DIGNA_OIDC_CLIENT_SECRET` olur (**Show client secret**'a tıklayın)

Sayfa ayrıca bir sonraki adımdaki keşif URL'sini doğrulayan **Issuer URL** değerini de gösterir.

---

## Adım 5: Kullanıcıları Atayın

1. **Access** sekmesini açın
2. Üyelerinin digna'yı kullanabileceği rolleri veya grupları ekleyin
3. **Save**'e tıklayın

!!! note "Atanmamış Kullanıcılar Oturum Açtıktan Sonra Reddedilir"

    Çoğu sağlayıcıda olduğu gibi OneLogin önce kullanıcının kimliğini doğrular, ardından yetkisini kontrol eder. Atanmamış bir kullanıcı başarıyla oturum açar ve ardından reddedilir; bu durum bir erişim kontrolü kararı yerine bir digna hatası gibi görünür.

---

## Adım 6: Keşif URL'sini Oluşturun

OneLogin alt alan adınızı yerine koyun:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Örneğin:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "/2, API Sürümüdür"

    OneLogin'in güncel OIDC uygulaması `/oidc/2/` altında bulunur. Eski dokümantasyonlar, kullanımdan kaldırılmış ilk sürümü gösteren, sürümsüz `/oidc/` yolunu gösterir. Emin değilseniz SSO sekmesindeki **Issuer URL** değerini kontrol edin; keşif URL'si, issuer'a `/.well-known/openid-configuration` eklenmiş halidir.

---

## Adım 7: digna'yı Yapılandırın

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Login with OneLogin"
```

### `config.toml`

```toml
[oidc_clients.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

Her iki dosyadaki `key` eşleşmelidir; burada `onelogin`.

---

## Adım 8: Test Edin

Arka ucu ve web sunucusunu yeniden başlatın, ardından dashboard'u açın. Tam kontrol listesi için bkz. [Oturum Açmayı Test Etme](overview.md#testing-login).

---

## OneLogin Sorunlarını Giderme

### redirect_uri did not match

Geri çağırma URL'si **Configuration → Redirect URI's** alanında eksik veya girişler satır sonu yerine virgülle ayrılmış.

### Token Adımında invalid_client

**Token Endpoint → Authentication Method** değeri *None* olarak ayarlanmış veya `config.toml` içindeki istemci gizli anahtarı güncel değil. **SSO** sekmesinde gizli anahtarı görüntüleyin ve karşılaştırın.

### Uygulama Kullanıcılara Görünmüyor

**Access** sekmesinde hiçbir role veya gruba erişim verilmemiş.

### Keşif URL'sinde 404

Alt alan adı yanlış veya URL'de `/oidc/2/` eksik. SSO sekmesinde gösterilen **Issuer URL** ile karşılaştırın.

---

## Ayrıca Bakınız

- [Çoklu Oturum Açma Genel Bakış](overview.md): yapılandırma başvurusu, test ve genel sorun giderme
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)
