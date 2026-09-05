---
title: Bir Veritabanını Bağlama | digna Dokümantasyonu
description: digna içinde mevcut bir projeye bir veritabanı bağlama adım adım kılavuzu. Bağlantıları nasıl yapılandıracağınızı, kimlik bilgilerini nasıl sağlayacağınızı ve güvenli erişimi nasıl etkinleştireceğinizi öğrenin.
image: /assets/logo_square.png
---

# Bir Veritabanını Bağlama

Bu kılavuz projeye bir veritabanı bağlantısı eklemek için gerekli minimum adımları gösterir.

## Etkileşimli Demo

<!--ARCADE EMBED START-->
<div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;">
  <iframe
    src="https://demo.arcade.software/NhlhDLqeW9wC5zaLlYPa?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true"
    title="Connect a Database to a Project"
    frameborder="0"
    loading="lazy"
    webkitallowfullscreen
    mozallowfullscreen
    allowfullscreen
    allow="clipboard-write"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;">
  </iframe>
</div>
<!--ARCADE EMBED END-->

---

### Adımlar

1. **Projenizi Açın**  
   Sol menüden **Projects**'i tıklayın ve hedef projeyi seçin.

2. **Bağlantı Ekle**  
   **Connections**'a gidin ve **Add Connection**'a tıklayın.

3. **Veritabanı Türünü Seçin**  
   Bağlamak istediğiniz veritabanını seçin (ör. PostgreSQL, MySQL, SQL Server, Oracle, Snowflake, Teradata).

4. **Bağlantı Bilgilerini Girin**  
   **Name**, **Host**, **Port**, **Database/Service** ve **Credentials** (kullanıcı adı/parola veya gerekiyorsa SSO) bilgilerini sağlayın.

5. **Test Et & Kaydet**  
   **Test**'e tıklayın. Başarılıysa **Save**'e tıklayın. Bağlantı proje için **Connections** altında görünecektir.