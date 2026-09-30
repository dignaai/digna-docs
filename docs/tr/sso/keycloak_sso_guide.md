---
title: Keycloak SSO – Çoklu Oturum Açma Entegrasyonu | digna Dokümantasyonu
description: "OpenID Connect kullanarak Keycloak ile digna için çoklu oturum açmayı yapılandırın: realm ve istemci kurulumu, istemci kimlik doğrulaması, geçerli yönlendirme URI'leri, istemci gizli anahtarı ve buna uygun digna yapılandırması."
image: /assets/logo_square.png
keywords: digna sso, keycloak sso, keycloak oidc, realm, gizli istemci, openid connect, kendi sunucunuzda barındırılan kimlik sağlayıcı
---

# Keycloak ile SSO Kurulumu

Keycloak, kendi sunucunuzda barındırılan ve OIDC ile tam uyumlu bir kimlik sağlayıcıdır. Onu kendiniz çalıştırdığınız için keşif URL'si bir üretici alan adından değil, kendi ana makine adınızdan ve realm'inizden oluşturulur.

Bu kılavuz **Keycloak tarafını** kapsar: istemciyi oluşturma ve digna'nın ihtiyaç duyduğu değerleri toplama. digna tarafı (`dashboard_config.toml`, test ve sorun giderme) her sağlayıcı için aynıdır ve [Çoklu Oturum Açma Genel Bakış](overview.md) sayfasında açıklanmıştır.

---

## Başlamadan Önce

| Gereksinim | Notlar |
|---|---|
| **Keycloak sürümü** | Burada kullanılan URL yolları için 17 veya üzeri; Adım 4'teki nota bakın |
| **Keycloak rolü** | Hedef realm'de `realm-admin` veya bir sunucu yöneticisi |
| **Realm** | digna kullanıcılarınızın ait olduğu realm; mutlaka `master` olması gerekmez |
| **digna yönlendirme URI'si** | Kullanıcıların oturum açtıktan sonra döndüğü URL, ör. `https://digna.yourdomain.com/oidc/callback` |

---

## Adım 1: Realm'i Seçin

1. Keycloak yönetim konsolunu açın
2. Kullanıcılarınızın bulunduğu realm'e geçmek için sol üstteki realm seçicisini kullanın

!!! warning "master Realm'ini Kullanmayın"

    `master` realm'i Keycloak'ın kendisini yönetmek için tasarlanmıştır. Uygulama istemcileri ayrılmış bir realm'e aittir; digna'yı `master` içine koymak, kullanıcılarına Keycloak yönetim konsoluna giden bir yol açar.

---

## Adım 2: İstemciyi Oluşturun

1. **Clients** bölümüne gidin ve **Create client**'a tıklayın
2. Şunları yapılandırın:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna`; bu değer `DIGNA_OIDC_CLIENT_ID` olur
3. **Next**'e tıklayın
4. **Capability config** adımında **Client authentication** seçeneğini **On** konumuna getirin
5. **Standard flow**'u etkin bırakın; diğer akışlara gerek yoktur
6. **Next**'e tıklayın

!!! warning "Client Authentication Açık Olmalıdır"

    **Client authentication** kapalıyken Keycloak, hiçbir kimlik bilgisi olmayan *genel* bir istemci oluşturur; Adım 4'teki **Credentials** sekmesi mevcut olmaz. digna gizli (confidential) bir istemciye ihtiyaç duyar. Yanlış ayarladıysanız bu anahtar oluşturmadan sonra değiştirilebilir.

---

## Adım 3: Yönlendirme URI'sini Ayarlayın

**Login settings** adımında (veya daha sonra **Settings** sekmesinde):

1. **Valid redirect URIs**: digna geri çağırma URL'nizi girin:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: boş bırakın veya yönlendirme URI'lerini yansıtmak için `+` olarak ayarlayın
3. **Save**'e tıklayın

!!! tip "Joker Karakterlerden Kaçının"

    Keycloak, `https://digna.yourdomain.com/*` gibi kalıpları kabul eder. Joker karakter, o ana makinedeki herhangi bir yolun yetkilendirme kodu almasına izin verir; bu nedenle tam geri çağırma URL'sini tercih edin.

---

## Adım 4: İstemci Gizli Anahtarını Alın

1. **Credentials** sekmesini açın
2. **Client Authenticator** değerinin *Client Id and Secret* olduğunu doğrulayın
3. **Client secret** değerini kopyalayın → `DIGNA_OIDC_CLIENT_SECRET` olur

Gizli anahtar burada tekrar alınabilir durumda kalır ve **Regenerate** ile yeniden oluşturulabilir.

---

## Adım 5: Keşif URL'sini Oluşturun

Keycloak ana makinenizi ve realm adınızı yerine koyun:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Örneğin:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 ve Öncesi /auth İçerir"

    Keycloak 17'den önce her uç nokta bir `/auth` önekinin altında bulunuyordu:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    `KC_HTTP_RELATIVE_PATH=/auth` ayarını yapan dağıtımlar güncel sürümlerde de eski düzeni korur. `/auth` içermeyen URL 404 döndürüyorsa `/auth` ile deneyin.

Devam etmeden önce URL'yi bir tarayıcıda açın. Bir JSON belgesi, ana makinenin ve realm'in doğru olduğunu doğrular.

---

## Adım 6: digna'yı Yapılandırın

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Login with Keycloak"
```

### `config.toml`

```toml
[oidc_clients.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

Her iki dosyadaki `key` eşleşmelidir; burada `keycloak`. Bunun Keycloak **Client ID** değerine eşit olması gerekmediğini unutmayın, ancak ikisini aynı tutmak takibi kolaylaştırır.

---

## Adım 7: Test Edin

Arka ucu ve web sunucusunu yeniden başlatın, ardından dashboard'u açın. Tam kontrol listesi için bkz. [Oturum Açmayı Test Etme](overview.md#testing-login).

---

## Keycloak Sorunlarını Giderme

### Invalid parameter: redirect_uri

Geri çağırma URL'si **Valid redirect URIs** kapsamında değil. Keycloak aldığı URI'yi sunucu günlüğüne kaydeder; tam uyuşmazlığı görmenin en hızlı yolu budur.

### Credentials Sekmesi Eksik

İstemci genel (public). **Settings → Capability config** altında **Client authentication** seçeneğini açın.

### Keşif URL'sinde 404

Ya realm adı yanlış ya da dağıtım `/auth` önekini kullanıyor. Yönetim konsolundaki realm listesini kontrol edin ve her iki URL biçimini de deneyin.

### unauthorized_client veya invalid_client

**Capability config** altında **Standard flow** devre dışı ya da gizli anahtar Keycloak'ta `config.toml` güncellenmeden yeniden oluşturulmuş.

### Arka Uçtan Gelen Sertifika Hataları

Özel veya kendinden imzalı bir sertifikanın arkasındaki, kendi sunucunuzda barındırılan bir Keycloak, digna'nın keşif URL'sine yaptığı giden HTTPS çağrısının başarısız olmasına neden olur. Sertifikayı veren CA'yı digna arka ucunu çalıştıran makinenin güven deposuna kurun.

---

## Ayrıca Bakınız

- [Çoklu Oturum Açma Genel Bakış](overview.md): yapılandırma başvurusu, test ve genel sorun giderme
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)
