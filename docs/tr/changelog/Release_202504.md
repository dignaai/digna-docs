---
title: digna Sürüm 2025.04 | Inspection Hub, Çok Dilli, Module Analytics
description: digna Sürüm 2025.04'te neler yeni öğrenin. Bu sürüm Inspection Hub'ı, çok dil desteğini (İngilizce, Almanca, Lehçe), dignacli ile veri kaynaklarının içe/dışa aktarımını, Module Analytics'in ilk sürümünü ve geliştirilmiş bir gösterge paneli deneyimini tanıtıyor.
keywords: digna Sürüm 2025.04, digna değişiklik günlüğü, digna inspection hub, digna çoklu dil desteği, digna module analytics, digna içe dışa aktarma, digna CLI, sürüm notları, veri gözlemlenebilirliği, veri kalite izleme
image: /assets/logo_square.png
---

# Sürüm Notları – 2025.04

Sürüm 2025.04 ile digna, veri kalitesi ve gözlemlenebilirliğini yönetmeyi daha kolay, ekipler için daha şeffaf ve dünya çapında kullanıcılara erişilebilir hale getirmede büyük bir adım atıyor.  
Bu sürüm, **güçlü yeni özellikleri**, **iş akışı otomasyon iyileştirmelerini** ve **kullanıcı deneyimi düzenlemelerini** bir araya getiriyor.  

---

## Yeni Özellikler

### Inspection Hub – Yeni Bir Komuta Merkezi
**Inspection Hub**, tüm denetim (inspection) işlerinizin yönetildiği merkezi yer olarak artık kullanılabilir. Farklı modüller arasında gidip gelmek veya yalnızca komut satırı ile çalışmaya güvenmek yerine, denetimlerinizi tek bir sadeleştirilmiş arayüzden izle ve kontrol edebilirsiniz.  

Temel yetenekler:  
- İstek üzerine denetimler: Yeni işleri anında başlatın, taze sonuçlara ihtiyacınız olduğunda beklemeyin.  
- Denetim geçmişi: Çalıştırılan denetimlerin zaman çizelgesini — ne çalıştırıldı, kim tetikledi ve ne zaman — görün.  
- Durum takibi: İşler tamamlandı, devam ediyor veya beklemede olarak açıkça işaretlenir.  
- Tetikleyici bilgisi: Bir denetimin bir kullanıcı, zamanlayıcı (scheduler) veya CLI tarafından tetiklenip tetiklenmediğini hızla kontrol edin.  
- Temizlik araçları: Eski veya gereksiz işleri silerek çalışma alanınızı düzenli tutun.  
- Detaylı loglar: Her işin ne kadar sürdüğünü, hangi kaynakların dahil edildiğini ve eşiklerin nasıl uygulandığını ayrıntılı şekilde inceleyin.  

Inspection Hub ekiplerinize **uçtan uca görünürlük ve kontrol** sağlar; büyük projelerde denetimleri yönetmeyi kolaylaştırır.  

---

### Çok Dilli Destek – digna Dilinizi Konuşuyor
digna, **çok dilli destek** özelliğinin eklenmesiyle artık uluslararası ekipler için hazır.  

Bu sürümde kullanıcılar tercih ettikleri **arayüz dilini** Doğrudan Kullanıcı Tercihleri bölümünden ayarlayabilir. Desteklenen diller şunlardır:  
- İngilizce (UK, US, CA, AU)  
- Almanca (DE, AT, CH)  
- Lehçe (PL)  

Bu, digna’yı çok dilli organizasyonlar için kullanımı kolay hale getirir ve farklı bölgelerde çalışan ekipler arasında benimsemeyi kolaylaştırır. Gelecek sürümlerde daha fazla dil eklenecektir.  

---

### Veri Kaynaklarının İçe/Dışa Aktarımı – Yapılandırma Kolaylaştı
Kurumsal dağıtımlarda ortamlar arasında tutarlılık kritik önemdedir. 2025.04 ile digna, gelişmiş kullanıcılar için komut satırı aracı **dignacli** üzerinden **veri kaynaklarının içe/dışa aktarımı** özelliğini sunuyor.  

Avantajlar:  
- Bir veri kaynağı yapılandırmasını bir kez dışa aktarın, sonra Geliştirme, Test ve Üretim ortamlarında yeniden kullanın.  
- Manuel yeniden yapılandırmayı ortadan kaldırın ve maliyetli hatalardan kaçının.  
- Basit CLI komutları (`export-ds` ve `import-ds`) ile otomatik iş akışlarını ve CI/CD boru hatlarını destekleyin.  
- Projeler arasında veri kaynaklarını hızlıca kopyalayarak işbirliğini kolaylaştırın.  

Bu işlevsellik, ekiplerin her ortamda yapılandırmaların tutarlı olduğunu bilerek güvenle dağıtım yapmalarını sağlar.  

---

### Module Analytics (v1) – Tespitten Anlamaya
digna, başlangıçta anomalilerin tespiti ve veri kalitesi izleme platformu olarak ortaya çıktı. Sürüm 2025.04 ile platform, **Module Analytics'in ilk sürümü** ile daha da gelişiyor.  

Module Analytics, kullanıcıların sadece sorunlara tepki vermek yerine **verilerini anlamalarına** yardımcı olur. Bu yeni modülle şunları yapabilirsiniz:  
- Veri setlerinizde uzun vadeli eğilimleri takip etmek.  
- Dalgalanmaları anlamak için volatiliteyi tespit etmek ve izlemek.  
- Daha derin bağlam için verinin zaman içindeki davranışını keşfetmek.  

Örneğin, digna otomatik olarak "*Satır sayısı yıl başından bu yana %15,8 arttı.*" gibi vurgular yapabilir.  
SQL sorguları yok, manuel kontroller yok — sadece **bir bakışta eyleme dönüştürülebilir içgörüler**.  

Bu, digna’nın gelişmiş veri analitiğine yönelik yolculuğunun temelini oluşturur ve veri ekiplerinin reaktif izleme yerine proaktif izlemeye geçmesini sağlar.  

---

### Gösterge Paneli İyileştirmeleri – Daha Akıcı Bir Kullanıcı Deneyimi
Büyük özelliklerin ötesinde, Sürüm 2025.04 digna’yı daha sezgisel ve keyifli hale getirmek için tasarlanmış birkaç **gösterge paneli iyileştirmesini** içerir:  
- Projeler ve denetimler arasında daha hızlı gezinme.  
- Denetim logları ve iş gönderimleri için daha temiz bir düzen.  
- İçgörüleri daha hızlı bulmanıza yardımcı olan ince tasarım ayarlamaları.  

Bu iyileştirmeler doğrudan müşteri geri bildirimlerine dayanır ve digna’yı **günlük kullanım için inşa edilmiş bir platform** haline getirme taahhüdümüzü gösterir.  

---

## Genel İyileştirmeler
- Büyük veri setleri üzerinde denetim işler için performans optimizasyonları.  
- Daha net geri bildirim sağlamak için dignacli'de geliştirilmiş hata işleme.  
- Aynı anda çok sayıda iş bulunan projeler için kararlılık iyileştirmeleri.  
- İş logu filtreleme ve proje yönetimi için UI düzenlemeleri.  

---

## Özet
Sürüm 2025.04, **kontrol, erişilebilirlik ve içgörü** ile ilgilidir.  

- Yeni **Inspection Hub**, kullanıcılara denetim işleri üzerinde tam görünürlük sağlar.  
- **Çok dilli destek**, digna’nın küresel ekipler tarafından kullanılmasını mümkün kılar.  
- **İçe/dışa aktarma işlevi**, ortamlar arası yapılandırma yönetimini basitleştirir.  
- **Module Analytics (v1)**, eğilim ve volatilite takibi ile tespitten anlamaya odaklanmayı sağlar.  
- **Gösterge paneli iyileştirmeleri**, genel kullanıcı deneyimini geliştirir.  

Bu güncellemeler bir arada digna’yı her zamankinden daha güçlü, kullanıcı dostu ve uluslararası kullanıma hazır hale getirir.