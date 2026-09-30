# AD FS ile SSO Kurulumu

Active Directory Federation Services şirket içi seçenektir: token'ları kendi sunucularınız verir ve keşif URL'si kendi ana makine adınızdır. AD FS, **Windows Server 2016** ve sonrasında OpenID Connect'i destekler.

Bu kılavuz **AD FS tarafını** kapsar: uygulama grubunu oluşturma ve digna'nın ihtiyaç duyduğu değerleri toplama. digna tarafı (`dashboard_config.toml`, test ve sorun giderme) her sağlayıcı için aynıdır ve [Çoklu Oturum Açma Genel Bakış](overview.md) sayfasında açıklanmıştır.

---

## Başlamadan Önce

| Gereksinim | Notlar |
|---|---|
| **AD FS sürümü** | Windows Server 2016 veya üzeri; önceki sürümlerde OIDC desteği yoktur |
| **Erişim** | AD FS sunucusunda yerel yönetici |
| **Federasyon hizmeti adı** | ör. `adfs.yourdomain.com` |
| **digna yönlendirme URI'si** | Kullanıcıların oturum açtıktan sonra döndüğü URL, ör. `https://digna.yourdomain.com/oidc/callback` |

---

## Adım 1: Uygulama Grubunu Oluşturun

1. AD FS sunucusunda **AD FS Management**'ı açın
2. **Application Groups** öğesine sağ tıklayın ve **Add Application Group**'u seçin
3. Ad olarak `digna` girin
4. **Standalone applications** altında (sürümünüze bağlı olarak **Client-Server applications** altında) **Server application accessing a web API** seçeneğini seçin
5. **Next**'e tıklayın

---

## Adım 2: Sunucu Uygulamasını Yapılandırın

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS bir GUID oluşturur. Bunu kopyalayın; bu değer `DIGNA_OIDC_CLIENT_ID` olur
3. **Redirect URI**: digna geri çağırma URL'nizi girin ve **Add**'e tıklayın:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Next**'e tıklayın

!!! warning "Yalnızca Next'e Değil, Add'e Tıklayın"

    Yönlendirme URI'si alanının kendi **Add** düğmesi vardır. Bir URI yazıp **Add**'e basmadan **Next**'e tıklamak URI'yi atar ve sihirbaz hiçbir uyarı vermez. Devam etmeden önce URI'nin alanın altındaki listede göründüğünü doğrulayın.

---

## Adım 3: Paylaşılan Gizli Anahtarı Oluşturun

1. **Generate a shared secret** seçeneğini işaretleyin
2. Oluşturulan gizli anahtarı kopyalayın → `DIGNA_OIDC_CLIENT_SECRET` olur
3. **Next**'e tıklayın

!!! warning "Gizli Anahtar Yalnızca Bir Kez Gösterilir"

    AD FS paylaşılan gizli anahtarı yalnızca bu sihirbaz sayfasında gösterir ve tekrar gösteremez. Kaybederseniz daha sonra uygulama grubunun özelliklerinden sıfırlayın.

---

## Adım 4: Web API'sini Yapılandırın

1. **Identifier**: Adım 2'deki istemci tanımlayıcısının aynısını girin ve **Add**'e tıklayın
2. **Next**'e tıklayın
3. Bir **Access Control Policy** seçin; *Permit everyone* en basit başlangıç noktasıdır, üretim için bunu bir grupla sınırlandırın
4. **Next**'e tıklayın

---

## Adım 5: İzin Verilen Kapsamları Tanımlayın

**Configure Application Permissions** adımında şunları işaretleyin:

- `openid`
- `profile`
- `email`

Ardından **Next**'e tıklayın ve sihirbazı tamamlayın.

!!! warning "openid Varsayılan Olarak İşaretli Değildir"

    Bazı sürümlerde AD FS yalnızca `user_impersonation` kapsamını önceden seçer. `openid` olmadan token uç noktası bir ID token yerine bir OAuth erişim token'ı döndürür ve digna kullanıcıyı tanımlayamaz.

---

## Adım 6: Keşif Uç Noktasını Doğrulayın

Federasyon hizmeti adınızı yerine koyun:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Örneğin:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Bunu bir tarayıcıda açın. Bir JSON belgesi, OIDC'nin etkin ve ana makine adının doğru olduğunu doğrular.

!!! note "Arka Uç Sertifikaya Güvenmelidir"

    AD FS için dahili bir sertifika yetkilisi kullanılması yaygındır. digna arka ucunu çalıştıran makine bu URL'ye kendi giden HTTPS çağrısını yapar; bu nedenle sertifikayı veren CA, yalnızca oturum açan kişilerin tarayıcılarında değil, o makinenin güven deposunda da bulunmalıdır.

---

## Adım 7: digna'yı Yapılandırın

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Login with Active Directory"
```

### `config.toml`

```toml
[oidc_clients.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

Her iki dosyadaki `key` eşleşmelidir; burada `adfs`.

---

## Adım 8: Test Edin

Arka ucu ve web sunucusunu yeniden başlatın, ardından dashboard'u açın. Tam kontrol listesi için bkz. [Oturum Açmayı Test Etme](overview.md#testing-login).

---

## AD FS Sorunlarını Giderme

### MSIS9611: İstemcinin Kaynağa Erişmesine İzin Verilmiyor

Adım 4'teki web API tanımlayıcısı istemci tanımlayıcısıyla eşleşmiyor veya Adım 5'teki kapsamlar verilmemiş. Her ikisi de uygulama grubunun özelliklerinden düzenlenebilir.

### MSIS9602: Geçersiz redirect_uri

URI yazılmış ancak **Add** düğmesiyle eklenmemiş veya `DIGNA_OIDC_REDIRECT_URI` değerinden farklı. **Application Groups → digna → digna backend → Properties** bölümünü kontrol edin.

### ID Token Döndürülmüyor

Uygulama izinlerinde `openid` kapsamı eksik.

### Arka Uç Keşif URL'sine Erişemiyor

Ya arka uç ana makinesindeki DNS federasyon hizmeti adını çözümlemiyor ya da AD FS sertifikasına orada güvenilmiyor. digna sunucusunun kendisinden `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` ile test edin.

### Kontrol Edilecek Olaylar

AD FS sunucusu hataları Event Viewer'da **Applications and Services Logs → AD FS → Admin** altına, genellikle tarayıcının gösterdiğinden daha belirgin bir nedenle kaydeder.

---

## Ayrıca Bakınız

- [Çoklu Oturum Açma Genel Bakış](overview.md): yapılandırma başvurusu, test ve genel sorun giderme
- [Microsoft: AD FS OpenID Connect senaryoları](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)