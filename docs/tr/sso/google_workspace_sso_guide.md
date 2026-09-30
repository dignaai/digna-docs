---
title: Google Workspace SSO – Çoklu Oturum Açma Entegrasyonu | digna Dokümantasyonu
description: "OpenID Connect kullanarak Google Workspace ile digna için çoklu oturum açmayı yapılandırın: OAuth onay ekranı, OAuth istemci kimliği, yetkili yönlendirme URI'leri ve buna uygun digna yapılandırması."
image: /assets/logo_square.png
keywords: digna sso, google workspace sso, google oidc, oauth onay ekranı, openid connect, kurumsal kimlik doğrulama
---

# Google Workspace ile SSO Kurulumu

Google'ın kimlik platformu OIDC uyumludur ve her müşteri için tek, iyi bilinen bir keşif URL'si kullanır; bu nedenle kuruluşa özel değerler yalnızca istemci kimliği ve gizli anahtardır.

Bu kılavuz **Google tarafını** kapsar: OAuth istemcisini oluşturma ve digna'nın ihtiyaç duyduğu değerleri toplama. digna tarafı (`dashboard_config.toml`, test ve sorun giderme) her sağlayıcı için aynıdır ve [Çoklu Oturum Açma Genel Bakış](overview.md) sayfasında açıklanmıştır.

---

## Başlamadan Önce

| Gereksinim | Notlar |
|---|---|
| **Google Cloud projesi** | Workspace alan adınızla aynı kuruluştaki herhangi bir proje |
| **Rol** | Projede Editor veya Owner |
| **digna yönlendirme URI'si** | Kullanıcıların oturum açtıktan sonra döndüğü URL, ör. `https://digna.yourdomain.com/oidc/callback` |

---

## Adım 1: OAuth Onay Ekranını Yapılandırın

Google, onay ekranı oluşturulmadan kimlik bilgisi vermez.

1. [Google Cloud Console](https://console.cloud.google.com)'u açın ve projenizi seçin
2. **APIs & Services → OAuth consent screen** bölümüne gidin
3. Kullanıcı türünü seçin:
   - **Internal**: yalnızca Workspace alan adınızdaki hesaplar oturum açabilir. Önerilir.
   - **External**: herhangi bir Google hesabı oturum açmayı deneyebilir.
4. Uygulama adını, kullanıcı destek e-postasını ve geliştirici iletişim e-postasını doldurun
5. **Scopes** adımında `openid`, `.../auth/userinfo.email` ve `.../auth/userinfo.profile` kapsamlarını ekleyin
6. Kaydedin

!!! warning "External Uygulamalar Yayımlanmalıdır"

    **External** bir onay ekranı *Testing* durumunda başlar; bu durumda yalnızca test kullanıcısı listesine açıkça eklenmiş hesaplar oturum açmayı tamamlayabilir. Diğer herkes "digna has not completed the Google verification process" mesajını görür. Uygulamayı **Publishing status** altında **In production** durumuna geçirin ya da böyle bir kısıtlaması olmayan ve yalnızca Workspace'e yönelik bir dağıtım için doğru seçim olan **Internal**'ı kullanın.

---

## Adım 2: OAuth İstemcisini Oluşturun

1. **APIs & Services → Credentials** bölümüne gidin
2. **Create Credentials → OAuth client ID**'ye tıklayın
3. **Application type** değerini **Web application** olarak ayarlayın
4. Bir ad verin, ör. `digna`
5. **Authorized redirect URIs** altında **Add URI**'ye tıklayın ve şunu girin:

```
https://digna.yourdomain.com/oidc/callback
```

6. **Create**'e tıklayın

!!! note "Authorized JavaScript Origins Gerekli Değildir"

    digna yetkilendirme kodunu tarayıcıdan değil arka uçtan değiştirir, bu nedenle **Authorized JavaScript origins** alanı boş bırakılabilir. Yalnızca yönlendirme URI'si önemlidir.

---

## Adım 3: Kimlik Bilgilerini Toplayın

Oluşturmanın ardından açılan iletişim kutusunda şunlar gösterilir:

- **Client ID**: `.apps.googleusercontent.com` ile biter → `DIGNA_OIDC_CLIENT_ID` olur
- **Client secret** → `DIGNA_OIDC_CLIENT_SECRET` olur

Diğer çoğu sağlayıcının aksine, her ikisi de daha sonra kimlik bilgisinin ayrıntı sayfasından tekrar alınabilir.

---

## Adım 4: Keşif URL'si

Google tüm müşteriler için tek bir keşif URL'si kullanır; yerine konacak bir şey yoktur:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Adım 5: digna'yı Yapılandırın

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### `config.toml`

```toml
[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

Her iki dosyadaki `key` eşleşmelidir; burada `google`.

---

## Adım 6: Test Edin

Arka ucu ve web sunucusunu yeniden başlatın, ardından dashboard'u açın. Tam kontrol listesi için bkz. [Oturum Açmayı Test Etme](overview.md#testing-login).

---

## Google Workspace Sorunlarını Giderme

### Error 400: redirect_uri_mismatch

`DIGNA_OIDC_REDIRECT_URI` içindeki URI **Authorized redirect URIs** listesinde değil veya sondaki bir eğik çizgi ya da şema nedeniyle farklı. Google'ın hata sayfası aldığı URI'yi gösterir; bunu kayıtlı URI ile karakteri karakterine karşılaştırın.

### Bu Uygulama Engellendi / Doğrulamayı Tamamlamadı

Onay ekranı **External** ve hâlâ *Testing* durumunda. Yayımlayın veya uygulamayı **Internal**'a geçirin.

### Erişim Engellendi: Yetkilendirme Hatası

Onay ekranı **Internal** iken oturum açmaya çalışan hesap Workspace alan adınızın dışında. Bu amaçlanan davranıştır; Internal uygulamalar yalnızca kuruluştaki hesapları kabul eder.

### Değişikliklerin Etkinleşmesi Birkaç Dakika Sürer

Google, kimlik bilgisi ve onay ekranı değişikliklerini eşzamansız olarak yayar. Yeni eklenen bir yönlendirme URI'sinin etkinleşmesi birkaç dakika sürebilir; bir değişiklik dikkate alınmamış gibi görünüyorsa daha fazla araştırmadan önce bekleyin ve yeniden deneyin.

---

## Ayrıca Bakınız

- [Çoklu Oturum Açma Genel Bakış](overview.md): yapılandırma başvurusu, test ve genel sorun giderme
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
