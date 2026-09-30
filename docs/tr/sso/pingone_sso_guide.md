---
title: PingOne SSO – Çoklu Oturum Açma Entegrasyonu | digna Dokümantasyonu
description: "OpenID Connect kullanarak PingOne ile digna için çoklu oturum açmayı yapılandırın: OIDC web uygulaması kurulumu, yönlendirme URI'leri, istemci kimlik bilgileri, ortam kimliği, bölgesel alan adları ve buna uygun digna yapılandırması."
image: /assets/logo_square.png
keywords: digna sso, pingone sso, ping identity, pingone oidc, ortam kimliği, openid connect, kurumsal kimlik doğrulama
---

# PingOne ile SSO Kurulumu

PingOne OIDC uyumludur. Değerlerinden ikisi dikkat gerektirir: her uç nokta URL'sinde yer alan **ortam kimliği** (environment ID) ve Kuzey Amerika, Avrupa, Kanada, Asya-Pasifik ve Avustralya kiracıları arasında farklılık gösteren **bölgesel alan adı**.

Bu kılavuz **PingOne tarafını** kapsar: uygulamayı oluşturma ve digna'nın ihtiyaç duyduğu değerleri toplama. digna tarafı (`dashboard_config.toml`, test ve sorun giderme) her sağlayıcı için aynıdır ve [Çoklu Oturum Açma Genel Bakış](overview.md) sayfasında açıklanmıştır.

---

## Başlamadan Önce

| Gereksinim | Notlar |
|---|---|
| **PingOne rolü** | Hedef ortamda Environment Admin veya Identity Data Admin |
| **Ortam** | digna kullanıcılarınızın ait olduğu PingOne ortamı |
| **digna yönlendirme URI'si** | Kullanıcıların oturum açtıktan sonra döndüğü URL, ör. `https://digna.yourdomain.com/oidc/callback` |

---

## Adım 1: Uygulamayı Oluşturun

1. PingOne yönetim konsolunda oturum açın ve ortamınızı seçin
2. **Applications → Applications** bölümüne gidin
3. **+** düğmesine tıklayın
4. **Application Name** olarak `digna` girin
5. **OIDC Web App**'i seçin
6. **Save**'e tıklayın

!!! warning "Single-Page App'i Değil, OIDC Web App'i Seçin"

    *Single-Page App* ve *Native App*, gizli anahtar tutamayan genel istemciler oluşturur. digna yetkilendirme kodunu arka ucundan değiştirir ve gizli (confidential) **OIDC Web App** türüne ihtiyaç duyar.

---

## Adım 2: Yönlendirme URI'sini Yapılandırın

1. Uygulamanın **Configuration** sekmesini açın
2. Düzenlemek için kalem simgesine tıklayın
3. **Response Type** değerinin *Code* ve **Grant Type** değerinin *Authorization Code* olduğunu doğrulayın
4. **Redirect URIs** altına digna geri çağırma URL'nizi girin:

```
https://digna.yourdomain.com/oidc/callback
```

5. **Token Endpoint Authentication Method** değerini *Client Secret Post* veya *Client Secret Basic* olarak ayarlayın
6. **Save**'e tıklayın

---

## Adım 3: Uygulamayı Etkinleştirin

Uygulamanın satırında veya ayrıntı panelinde anahtarı **enabled** konumuna getirin.

!!! warning "Yeni Uygulamalar Devre Dışı Başlar"

    PingOne uygulamaları devre dışı durumda oluşturur. Devre dışı bir uygulama, yetkilendirme adımında anahtardan hiç söz etmeyen bir hata üretir; bu nedenle başka bir şeyde hata ayıklamadan önce bunu doğrulamaya değer.

---

## Adım 4: Kapsamları Tanımlayın

1. **Resources** sekmesini açın
2. `openid` kapsamının verildiğini doğrulayın ve **OpenID Connect** kaynağından `profile` ve `email` kapsamlarını ekleyin
3. **Save**'e tıklayın

---

## Adım 5: Kullanıcıları Atayın

1. **Access** sekmesini açın
2. Üyelerinin digna'yı kullanabileceği popülasyonu veya grupları ekleyin
3. **Save**'e tıklayın

---

## Adım 6: Kimlik Bilgilerini ve Ortam Kimliğini Toplayın

**Configuration** sekmesinde **General** bölümünü genişletin:

- **Client ID** → `DIGNA_OIDC_CLIENT_ID` olur
- **Client Secret** → `DIGNA_OIDC_CLIENT_SECRET` olur (göz simgesine tıklayın)
- **Environment ID** → keşif URL'sine girer

Aynı sekme, elle oluşturmak yerine doğrudan kopyalayabileceğiniz hazır **OIDC Discovery Endpoint** değerini de listeler.

---

## Adım 7: Keşif URL'sini Oluşturun

Ortam kimliğini ve bölgenize ait alan adını yerine koyun:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Bölge | Alan adı |
|---|---|
| Kuzey Amerika | `auth.pingone.com` |
| Avrupa | `auth.pingone.eu` |
| Kanada | `auth.pingone.ca` |
| Asya-Pasifik | `auth.pingone.asia` |
| Avustralya | `auth.pingone.com.au` |

Avrupa'daki bir ortam için:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Yazmak Yerine Kopyalayın"

    Bölgesel alan adı, bir PingOne entegrasyonunda en sık yapılan hatadır ve yanlış bir bölge yardımcı bir mesaj yerine 404 döndürür. Adım 6'daki **OIDC Discovery Endpoint** değerini kullanın.

---

## Adım 8: digna'yı Yapılandırın

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Login with PingOne"
```

### `config.toml`

```toml
[oidc_clients.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

Her iki dosyadaki `key` eşleşmelidir; burada `pingone`.

---

## Adım 9: Test Edin

Arka ucu ve web sunucusunu yeniden başlatın, ardından dashboard'u açın. Tam kontrol listesi için bkz. [Oturum Açmayı Test Etme](overview.md#testing-login).

---

## PingOne Sorunlarını Giderme

### Keşif URL'sinde 404

Bölgesel alan adı veya ortam kimliği yanlış. Uygulamanın Configuration sekmesinde gösterilen **OIDC Discovery Endpoint** ile karşılaştırın.

### NOT_FOUND veya Uygulama Devre Dışı

Adım 3'teki uygulama anahtarı hâlâ kapalı.

### Yönlendirme URI'si Uyuşmazlığı

PingOne dizenin tamamını eşleştirir. **Configuration → Redirect URIs** bölümünde sondaki bir eğik çizgi veya şema farkı olup olmadığını kontrol edin.

### Oturum Açma Başarılı Ancak digna'ya E-posta Talebi Ulaşmıyor

**Resources** sekmesinde `email` ve `profile` kapsamları verilmemiş.

### Kullanıcı Uygulamayı Göremiyor

**Access** sekmesinde hiçbir popülasyona veya gruba erişim verilmemiş.

---

## Ayrıca Bakınız

- [Çoklu Oturum Açma Genel Bakış](overview.md): yapılandırma başvurusu, test ve genel sorun giderme
- [PingOne: OIDC uygulama yapılandırması](https://docs.pingidentity.com/pingone/)
