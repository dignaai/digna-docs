---
title: Microsoft Entra ID SSO – Çoklu Oturum Açma Entegrasyonu | digna Dokümantasyonu
description: "OpenID Connect kullanarak Microsoft Entra ID (eski adıyla Azure AD) ile digna için çoklu oturum açmayı yapılandırın: uygulama kaydı, yönlendirme URI'si, istemci gizli anahtarı, kiracı kimliği ve buna uygun digna yapılandırması."
image: /assets/logo_square.png
keywords: digna sso, microsoft entra id, azure ad sso, oidc entegrasyonu, uygulama kaydı, kurumsal kimlik doğrulama
---

# Microsoft Entra ID ile SSO Kurulumu

Microsoft Entra ID (eski adıyla Azure Active Directory) OIDC ile tam uyumlu bir sağlayıcıdır; bu nedenle digna onunla standart keşif uç noktası üzerinden entegre olur.

Bu kılavuz **Entra ID tarafını** kapsar: uygulamayı kaydetme ve digna'nın ihtiyaç duyduğu dört değeri toplama. digna tarafı (`dashboard_config.toml`, test ve sorun giderme) her sağlayıcı için aynıdır ve [Çoklu Oturum Açma Genel Bakış](overview.md) sayfasında açıklanmıştır.

---

## Başlamadan Önce

| Gereksinim | Notlar |
|---|---|
| **Entra ID rolü** | Application Administrator, Cloud Application Administrator veya Global Administrator |
| **digna yönlendirme URI'si** | Kullanıcıların oturum açtıktan sonra döndüğü URL, ör. `https://digna.yourdomain.com/oidc/callback` |
| **Kiracı** | Kullanıcılarınızın oturum açtığı dizin |

---

## Adım 1: Uygulamayı Kaydedin

1. [Microsoft Entra admin center](https://entra.microsoft.com)'da oturum açın
2. **Identity → Applications → App registrations** bölümüne gidin
3. **New registration**'a tıklayın
4. Şunları yapılandırın:
   - **Name**: `digna` (onay ekranında kullanıcılara gösterilir)
   - **Supported account types**: tek kiracılı bir dağıtım için *Accounts in this organizational directory only*
5. **Redirect URI** altında **Web** platformunu seçin ve digna geri çağırma URL'nizi girin:

```
https://digna.yourdomain.com/oidc/callback
```

6. **Register**'a tıklayın

!!! warning "Önemli"

    Platform *Single-page application* değil, **Web** olmalıdır. digna yetkilendirme kodunu arka uçtan bir istemci gizli anahtarı kullanarak değiştirir; SPA platform türü buna izin vermez.

---

## Adım 2: İstemci ve Kiracı Kimliklerini Toplayın

Uygulamanın **Overview** sayfasında şunları kopyalayın:

- **Application (client) ID** → `DIGNA_OIDC_CLIENT_ID` olur
- **Directory (tenant) ID** → keşif URL'sine girer

---

## Adım 3: Bir İstemci Gizli Anahtarı Oluşturun

1. **Certificates & secrets → Client secrets** bölümüne gidin
2. **New client secret**'a tıklayın
3. Bir açıklama girin ve bir geçerlilik süresi seçin
4. **Add**'e tıklayın
5. **Value** sütununu hemen kopyalayın

!!! warning "Secret ID'yi Değil, Value'yu Kopyalayın"

    **Value** yalnızca bir kez, bu sayfada gösterilir ve daha sonra alınamaz. Yanındaki **Secret ID** benzer görünür ancak gizli anahtar değildir; onu kullanmak oturum açmada `invalid_client` hatasına yol açar. Kopyalamadan sayfadan ayrılırsanız gizli anahtarı silin ve yenisini oluşturun.

!!! tip "İpucu"

    Entra ID gizli anahtar ömrünü en fazla 24 ay ile sınırlar, bu nedenle her SSO entegrasyonunun bir son kullanma tarihi vardır. Bunu göreceğiniz bir yere not edin; süresi dolmuş bir gizli anahtar, oturum açma sayfasında hiçbir uyarı olmadan SSO'yu tüm kullanıcılar için aynı anda devre dışı bırakır.

---

## Adım 4: API İzinlerini Doğrulayın

1. **API permissions** bölümüne gidin
2. **Microsoft Graph → User.Read** (delegated) izninin mevcut olduğunu doğrulayın; bu izin varsayılan olarak eklenir

digna'nın istediği `openid`, `profile` ve `email` kapsamları standart OIDC kümesinin bir parçasıdır ve ayrı bir izin gerektirmez. Kiracınız tüm uygulamalar için yönetici onayı gerektiriyorsa **Grant admin consent for &lt;tenant&gt;**'e tıklayın.

---

## Adım 5: Keşif URL'sini Oluşturun

Adım 2'deki **Directory (tenant) ID** değerini yerine koyun:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "v2.0 Uç Noktasını Kullanın"

    `/v2.0/` kısmı önemlidir. `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` adresindeki v1.0 uç noktası token'ları daha eski bir biçimde verir ve digna'nın beklediği standart OIDC talep (claim) değerlerini döndürmez.

Devam etmeden önce URL'yi bir tarayıcıda açın. Bir JSON belgesi, kiracı kimliğinin doğru olduğunu doğrular.

---

## Adım 6: digna'yı Yapılandırın

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"
```

### `config.toml`

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

Her iki dosyadaki `key` eşleşmelidir; burada `microsoft`.

---

## Adım 7: Test Edin

Arka ucu ve web sunucusunu yeniden başlatın, ardından dashboard'u açın. Tam kontrol listesi için bkz. [Oturum Açmayı Test Etme](overview.md#testing-login).

---

## Entra ID Sorunlarını Giderme

### AADSTS50011: Yönlendirme URI'si Uyuşmazlığı

`DIGNA_OIDC_REDIRECT_URI` içindeki URI, Adım 1'de kaydedilenden farklı. Entra ID dizenin tamamını karşılaştırır; bu nedenle sondaki bir eğik çizgi, `http` ile `https` farkı veya farklı bir port uyuşmazlık sayılır. **Authentication → Web → Redirect URIs** bölümünü kontrol edin.

### AADSTS7000215: Geçersiz İstemci Gizli Anahtarı

Ya **Value** yerine **Secret ID** kopyalanmış ya da gizli anahtarın süresi dolmuş. Yeni bir gizli anahtar oluşturun ve Value sütununu kopyalayın.

### AADSTS650057: Geçersiz Kaynak

Uygulama kaydı silinmiş veya keşif URL'sindekinden farklı bir kiracıya ait. Overview sayfasındaki Directory (tenant) ID değerini doğrulayın.

### Kullanıcılar Oturum Açıyor Ancak Hiçbir Şey Olmuyor

Kiracı yönetici onayı gerektiriyorsa ve bu onay verilmemişse yönlendirme, kullanılabilir bir token olmadan geri döner. **API permissions** altında yönetici onayını verin.

---

## Ayrıca Bakınız

- [Çoklu Oturum Açma Genel Bakış](overview.md): yapılandırma başvurusu, test ve genel sorun giderme
- [Microsoft: OAuth 2.0 yetkilendirme kodu akışı](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
