---
title: digna Sürüm 2025.04 | Inspection Hub, Çok Dilli, Module Analytics
description: digna Sürüm 2025.04'te nelerin yeni olduğunu öğrenin. Bu sürüm Inspection Hub'ı, çoklu dil desteğini (İngilizce, Almanca, Lehçe), dignacli ile veri kaynaklarının içe/dışa aktarımını, Module Analytics'in ilk sürümünü ve geliştirilmiş bir gösterge paneli deneyimini sunuyor.
keywords: digna Sürüm 2025.04, digna değişiklik günlüğü, digna inspection hub, digna çoklu dil desteği, digna module analytics, digna içe dışa aktarma, digna CLI, sürüm notları, veri gözlemlenebilirliği, veri kalitesi izleme
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Değişiklik Günlüğü – Sürüm 2025.04

Sürüm 2025.04 ile digna, veri kalitesi ve gözlemlenebilirliğini yönetmeyi daha kolay, ekipler için daha şeffaf ve dünya çapında kullanıcılar için daha erişilebilir hale getirmede önemli bir adım atıyor.  
Bu sürüm, **güçlü yeni özellikleri**, **iş akışı otomasyonu iyileştirmelerini** ve **kullanıcı deneyimi geliştirmelerini** bir araya getiriyor.  

---

## Yeni Özellikler

### Inspection Hub – Yeni Bir Komuta Merkezi
Yeni **Inspection Hub**, tüm inspection job'larınızı yönetmek için merkezi bir yer olarak kullanılabilir. Farklı modüller arasında geçiş yapmak veya yalnızca komut satırı üzerinden çalışmaya bağımlı kalmak yerine, artık inspection'larınızı tek, sade bir arayüzden izleyebilir ve kontrol edebilirsiniz.  

Temel yetenekler şunlardır:  
- İstek üzerine inspection'lar: Yeni job'ları anında başlatın ve güncel sonuçlara hızlıca erişin.  
- Inspection geçmişi: Hangi görevlerin çalıştırıldığını, kimin tetiklediğini ve ne zaman çalıştığını zaman çizelgesi şeklinde görün.  
- Durum takibi: Job'lar tamamlandı, devam ediyor veya beklemede olarak net şekilde işaretlenir.  
- Tetikleyici bilgisi: Bir inspection'ın kullanıcı, scheduler veya CLI tarafından tetiklenip tetiklenmediğini hızlıca kontrol edin.  
- Temizlik araçları: Eski veya gereksiz job'ları silerek çalışma alanınızı düzenli tutun.  
- Ayrıntılı log'lar: Her job'ın ne kadar sürdüğünü, hangi kaynakların dahil edildiğini ve eşiklerin nasıl uygulandığını inceleyin.  

Inspection Hub, ekiplerin **uçtan uca görünürlük ve kontrol** sahibi olmasını sağlayarak büyük projelerde inspection yönetimini kolaylaştırır.  

---

### Çok Dilli Destek – digna Kendi Dilinizde Konuşuyor
digna, **çok dilli destek** sunarak uluslararası ekipler için hazır hale geldi.  

Bu sürümde **tercih ettiğiniz arayüz dilini** doğrudan Kullanıcı Tercihleri'nden ayarlayabilirsiniz. Desteklenen diller şunlardır:  
- İngilizce (UK, US, CA, AU)  
- Almanca (DE, AT, CH)  
- Lehçe (PL)  

Bu, çok dilli organizasyonlar için digna'yı daha kolay kullanılabilir kılar ve farklı bölgelerde çalışan ekiplerin benimsemesini hızlandırır. Gelecek sürümlerde daha fazla dil eklenecektir.  

---

### Veri Kaynaklarının İçe/Dışa Aktarımı – Konfigürasyon Basitleşti
Kurumsal dağıtımlarda ortamlarda tutarlılık çok önemlidir. 2025.04 ile digna, gelişmiş kullanıcılar için komut satırı aracı **dignacli** üzerinden **veri kaynaklarının içe/dışa aktarımı** özelliğini tanıtıyor.  

Faydaları:  
- Bir veri kaynağı konfigürasyonunu bir kez dışa aktarın, ardından Geliştirme, Test ve Üretim ortamlarında yeniden kullanın.  
- Manuel yeniden yapılandırmayı ortadan kaldırın ve maliyetli hatalardan kaçının.  
- Basit CLI komutları (`export-ds` ve `import-ds`) ile otomatik iş akışlarını ve CI/CD boru hatlarını destekleyin.  
- Projeler arasında veri kaynaklarını hızlıca kopyalayarak iş birliğini kolaylaştırın.  

Bu işlevsellik, ekiplerin her ortamda konfigürasyonların tutarlı olduğundan emin olarak güvenle dağıtım yapmasını sağlar.  

---

### Module Analytics (v1) – Tespit Etmekten Anlamaya
digna, başlangıçta anomali tespiti ve veri kalitesi izleme için bir platform olarak başladı. Sürüm 2025.04 ile birlikte platform, **Module Analytics'in ilk sürümü** ile daha da evriliyor.  

Module Analytics, kullanıcıların sadece sorunlara tepki vermek yerine **verilerini anlamalarına** yardımcı olur. Bu yeni modülle şunları yapabilirsiniz:  
- Veri kümelerinizde uzun vadeli trendleri izleyin.  
- Dalgalanmaları anlamak için volatiliteyi tespit edin ve izleyin.  
- Daha derin bağlam için zaman içinde veri davranışını keşfedin.  

Örneğin, digna otomatik olarak *“Satır sayısı yıl başından beri %15.8 arttı.”* gibi vurgular yapabilir.  
SQL sorguları yok, manuel kontroller yok — sadece **bir bakışta eyleme dönüştürülebilir içgörüler**.  

Bu, digna'nın ileri veri analitiğine doğru yolculuğunun temelini oluşturur ve veri ekiplerinin reaktif izleme yerine proaktif izlemeye geçmesini sağlar.  

---

### Gösterge Paneli İyileştirmeleri – Daha Akıcı Bir Kullanıcı Deneyimi
Ana özelliklerin ötesinde, Sürüm 2025.04 digna'yı daha sezgisel ve keyifli hale getirmek için bir dizi **gösterge paneli iyileştirmesi** içeriyor:  
- Projeler ve inspection'lar arasında daha hızlı gezinme.  
- Inspection log'ları ve job gönderimleri için daha temiz bir düzen.  
- İçgörüleri daha hızlı bulmanıza yardımcı olan ince tasarım ayarlamaları.  

Bu iyileştirmeler doğrudan müşteri geri bildirimlerine dayanır ve digna'yı **günlük kullanım için inşa edilmiş bir platform** yapma taahhüdümüzü gösterir.  

---

## Genel İyileştirmeler
- Büyük veri kümeleri üzerinde inspection job'ları için performans optimizasyonları.  
- Daha net geri bildirim sağlamak için dignacli'de geliştirilmiş hata işleme.  
- Aynı anda çok sayıda job'a sahip projeler için kararlılık iyileştirmeleri.  
- Job log filtreleme ve proje yönetimi için UI iyileştirmeleri.  

---

## Özet
Sürüm 2025.04, **kontrol, erişilebilirlik ve içgörü** üzerine odaklanıyor.  

- Yeni **Inspection Hub**, kullanıcılara inspection job'ları üzerinde tam görünürlük sağlar.  
- **Çok dilli destek**, digna'nın küresel ekipler tarafından kullanılabilmesini sağlar.  
- **İçe/dışa aktarma işlevselliği**, ortamlar arası konfigürasyon yönetimini basitleştirir.  
- **Module Analytics (v1)**, trend ve volatilite takibi ile odak noktayı tespit etmekten anlamaya kaydırır.  
- **Gösterge paneli iyileştirmeleri**, genel kullanıcı deneyimini rafine eder.  

Birlikte, bu güncellemeler digna'yı her zamankinden daha güçlü, kullanıcı dostu ve uluslararası kullanıma hazır hale getiriyor.