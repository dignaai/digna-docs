---
title: digna Sürüm 2025.04 | Inspection Hub, Çokdilli, Module Analytics
description: digna Sürüm 2025.04'te nelerin yeni olduğunu öğrenin. Bu sürüm Inspection Hub'ı, çokdilli desteği (İngilizce, Almanca, Lehçe), dignacli ile veri kaynaklarının içe/dışa aktarımını, Module Analytics'in ilk sürümünü ve geliştirilmiş bir gösterge paneli deneyimini sunar.
keywords: digna Sürüm 2025.04, digna değişiklik günlüğü, digna inspection hub, digna çokdilli destek, digna module analytics, digna içe dışa aktarım, digna CLI, sürüm notları, veri gözlemlenebilirliği, veri kalite izleme
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Değişiklik Günlüğü – Release 2025.04

Release 2025.04 ile digna, veri kalitesi ve gözlemlenebilirliğini yönetmeyi ekipler için daha kolay, daha şeffaf ve dünya çapında kullanıcılara erişilebilir hale getirme yolunda büyük bir adım atıyor.  
Bu sürüm, **güçlü yeni özellikleri**, **iş akışı otomasyon iyileştirmelerini** ve **kullanıcı deneyimi geliştirmelerini** bir araya getiriyor.  

---

## Yeni Özellikler

### Inspection Hub – Yeni Bir Komuta Merkezi
**Inspection Hub**, artık tüm denetim işlerinizin yönetilebileceği merkezi yer olarak kullanılabilir. Farklı modüller arasında geçiş yapmak veya yalnızca komut satırıyla çalışmaya güvenmek yerine, artık denetimlerinizi tek bir sadeleştirilmiş arayüzden izleyip kontrol edebilirsiniz.  

Ana yetenekler şunlardır:  
- İstek üzerine denetimler: Yeni sonuçlara ihtiyaç duyduğunuzda işleri anında başlatın.  
- Denetim geçmişi: Hangi denetimlerin çalıştırıldığını, kimin tetiklediğini ve ne zaman çalıştırıldığını zaman çizelgesi şeklinde görün.  
- Durum takibi: İşler tamamlandı, devam ediyor veya beklemede olarak net şekilde işaretlenir.  
- Tetikleyici bilgileri: Bir denetimin kullanıcı, zamanlayıcı veya CLI tarafından başlatılıp başlatılmadığını hızlıca kontrol edin.  
- Temizlik araçları: Çalışma alanınızı temiz tutmak için eski veya gereksiz işleri silin.  
- Ayrıntılı loglar: Her bir işe girerek ne kadar sürdüğünü, hangi kaynakların dahil edildiğini ve eşiklerin nasıl uygulandığını inceleyin.  

Inspection Hub, ekiplerin **uçtan uca görünürlük ve kontrol** sahibi olmasını sağlayarak büyük projelerde denetimleri yönetmeyi kolaylaştırır.  

---

### Çokdilli Destek – digna Kendi Dilinizde
digna, **çokdilli destek**in eklenmesiyle uluslararası ekipler için hazır hale geldi.  

Bu sürümde arayüz dil tercihinizi doğrudan Kullanıcı Tercihleri'nde ayarlayabilirsiniz. Desteklenen diller şunlardır:  
- İngilizce (UK, US, CA, AU)  
- Almanca (DE, AT, CH)  
- Lehçe (PL)  

Bu, çok dilli kuruluşlar için digna'yı daha kullanışlı hale getirir ve farklı bölgelerde çalışan ekipler arasında daha sorunsuz benimsenmeyi sağlar. Gelecek sürümlerde daha fazla dil eklenecektir.  

---

### Veri Kaynaklarının İçe & Dışa Aktarımı – Konfigürasyon Daha Basit
Kurumsal dağıtımlarda ortamlar arasında tutarlılık çok önemlidir. 2025.04 ile digna, gelişmiş kullanıcılar için komut satırı aracı olan **dignacli** üzerinden **veri kaynaklarının içe/dışa aktarımı** özelliğini sunuyor.  

Faydaları:  
- Bir veri kaynağı konfigürasyonunu bir kez dışa aktarın, sonra Development, Test ve Production ortamlarında yeniden kullanın.  
- Manuel yeniden yapılandırmayı ortadan kaldırın ve maliyetli hatalardan kaçının.  
- Basit CLI komutları (`export-ds` ve `import-ds`) ile otomatik iş akışlarını ve CI/CD hatlarını destekleyin.  
- Projeler arasında veri kaynaklarını hızla kopyalayarak iş birliğini kolaylaştırın.  

Bu işlevsellik, ekiplerin her ortamda konfigürasyonların tutarlı olduğundan emin olarak güvenle dağıtım yapmasını sağlar.  

---

### Module Analytics (v1) – Tespit Etmekten Anlamaya
digna, anomali tespiti ve veri kalite izleme platformu olarak başladı. Release 2025.04 ile birlikte **Module Analytics'in ilk sürümü** ile daha da ilerliyor.  

Module Analytics, kullanıcıların sadece sorunlara tepki vermek yerine **verilerini anlamalarına** yardımcı olur. Bu yeni modülle şunları yapabilirsiniz:  
- Veri setlerinizdeki uzun vadeli trendleri takip edin.  
- Dalgalanmaları anlamak için oynaklığı tespit edin ve izleyin.  
- Zaman içinde veri davranışını keşfederek daha derin bağlam kazanın.  

Örneğin, digna otomatik olarak *“Satır sayısı yılın başından bu yana %15,8 arttı.”* gibi vurgular yapabilir.  
SQL sorguları yok, manuel kontroller yok — sadece **anında uygulanabilir içgörüler**.  

Bu, digna'nın ileri veri analitiğine doğru yolculuğunun temelini oluşturur ve veri ekiplerinin reaktif izlemeden proaktif izlemeye geçmesini sağlar.  

---

### Gösterge Paneli İyileştirmeleri – Daha Akıcı Bir Kullanıcı Deneyimi
Ana özelliklerin ötesinde, Release 2025.04 digna'yı daha sezgisel ve keyifli hale getirmek için birkaç **gösterge paneli düzenlemesi** içeriyor:  
- Projeler ve denetimler arasında daha hızlı gezinme.  
- Denetim logları ve iş gönderimleri için daha temiz bir düzen.  
- İçgörüler bulmanızı kolaylaştıran ince tasarım ayarlamaları.  

Bu iyileştirmeler doğrudan müşteri geri bildirimlerine dayanmakta olup digna'nın **günlük kullanım için inşa edilmiş bir platform** olma taahhüdünü göstermektedir.  

---

## Genel İyileştirmeler
- Büyük veri kümelerinde denetim işleri için performans optimizasyonları.  
- Daha net geri bildirim sağlamak için dignacli'de geliştirilmiş hata yönetimi.  
- Aynı anda birçok iş olan projelerde kararlılık iyileştirmeleri.  
- İş logu filtreleme ve proje yönetimi için UI iyileştirmeleri.  

---

## Özet
Release 2025.04, **kontrol, erişilebilirlik ve içgörü** hakkında.  

- Yeni **Inspection Hub**, kullanıcılara denetim işleri üzerinde tam görünürlük sağlar.  
- **Çokdilli destek**, digna'nın küresel ekipler tarafından kullanılabilmesini sağlar.  
- **İçe/dışa aktarma işlevi**, ortamlar arası konfigürasyon yönetimini basitleştirir.  
- **Module Analytics (v1)**, trend ve oynaklık takibi ile odaklanmayı tespit etmekten anlamaya kaydırır.  
- **Gösterge paneli iyileştirmeleri**, genel kullanıcı deneyimini rafine eder.  

Bu güncellemeler bir araya gelerek digna'yı her zamankinden daha güçlü, kullanıcı dostu ve uluslararası kullanıma hazır hale getiriyor.