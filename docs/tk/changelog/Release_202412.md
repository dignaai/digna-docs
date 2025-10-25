---
title: digna Sürüm 2024.12 | Değişiklikler ve Yeni Özellikler
description: digna Sürüm 2024.12'te nelerin yeni olduğunu keşfedin. Bu sürüm yerleşik bir zamanlayıcı, PDF raporlama, esnek özel sütunlar, dinamik snapshot sorgu yer tutucuları ve anomali tespiti ile veri kalite izlemeyi geliştiren daha akıllı eşik optimizasyonu sunar.
keywords: digna Sürüm 2024.12, digna değişiklik kaydı, sürüm notları, yerleşik scheduler, PDF raporlar, custom column type, snapshot query placeholders, threshold optimization, veri gözlemlenebilirliği, veri kalite izleme, anomali tespiti
canonical_url: https://docs.digna.ai/changelog/Release_202412/
image: /assets/logo_square.png
---



# Değişiklikler – Sürüm 2024.12

2024.12 sürümü, digna'yı daha otomatik, esnek ve iş için hazır hale getiren yeni özellikler ve iyileştirmeler sunuyor.  
Bu sürüm zamanlama, raporlama, sorgu işleme ve anomali tespiti doğruluğunu geliştiriyor.  

---

## Yeni Özellikler

### Yerleşik Zamanlayıcı
İncelemeler artık yalnızca komut satırı veya API çağrılarına bağlı değil.  
Yeni **digna Scheduler** ile incelemeler belirlenen zamanlarda otomatik olarak çalıştırılabilir.  

- Yinelenen zamanlamalar (günlük, haftalık veya özel aralıklar) için **Cron ifadelerini** destekler.  
- **Offsets**, **başlangıç tarihleri** ve **bitiş tarihleri** ile hassas kontrol sağlar.  
- Ekiplerin tüm kritik veri kaynaklarının tutarlı ve manuel çaba gerektirmeden denetlendiğinden emin olmasını sağlar.  

---

### PDF Formatında Raporlar
Ekipler artık sonuçları paydaşlarla kolayca paylaşmak için **PDF dışa aktarımları** kullanabilir.  

- Grafikler, metrikler ve anomali sonuçları profesyonel bir PDF formatında dışa aktarılabilir.  
- Raporlar hem teknik hem de iş kullanıcılarına hizmet edecek şekilde **görselleştirmeleri** ve **altyapı verilerini** birleştirir.  
- Rapor oluşturmak için harici araçlara ihtiyaç duyulmasını ortadan kaldırır.  

---

### Yeni Sütun Türü: `CUSTOM`
Daha fazla esneklik sağlamak için digna yeni bir **`CUSTOM` sütun türü** tanıtıyor.  

- Kullanıcılar belirli özniteliklere hangi **istatistiklerin ve metriklerin** uygulanacağını tam olarak tanımlayabilir.  
- NUMERICAL veya CATEGORICAL gibi standart kategorilere uymayan özel durumlar için idealdir.  
- Analizlerin odaklı kalmasına ve sonuçların iş bağlamına uygun olmasına yardımcı olur.  

---

### Snapshot Sorgularında Yeni Yer Tutucular
Snapshot sorguları artık **dinamik yer tutucular** ile daha basit ve daha az hata eğilimli.  

- `#date+n#` veya `#date-n#` gibi tokenlar sorgulardaki tarihleri otomatik olarak ayarlar.  
- Örnek:  
  - `#date+1#` → yarın  
  - `#date-2#` → iki gün önce  
- Manuel tarih hesaplamalarını ortadan kaldırır ve ekipler arasında tutarlılık sağlar.  

---

### Eşik Optimizasyonu
Anomali eşikleri artık daha akıllı ve bağlama duyarlı.  

- **NULL COUNT** gibi metrikler için alt eşikler otomatik olarak **0** ile sınırlandırılır.  
- Geçersiz veya anlamsız eşiklerin oluşmasını önler.  
- Daha az yanlış pozitif ve daha güvenilir anomali tespiti sağlar.  

---

## Genel İyileştirmeler
- Proje ve öznitelik yapılandırma görünümlerinde rafine edilmiş **UI bileşenleri**.  
- Büyük veri hacimleri için geliştirilmiş **gösterge paneli performansı**.  
- Sorun giderme için geliştirilmiş **loglama ve hata mesajları**.  

---

## Özet
2024.12 sürümü, digna'yı **veri kalitesi, anomali tespiti ve gözlemlenebilirlik** için daha güçlü bir platform haline getiriyor.  
Zamanlama ile otomasyon, paylaşılabilir PDF raporlar, özelleştirilebilir sütunlar, basitleştirilmiş snapshot sorguları ve daha akıllı eşikler sayesinde digna, hem teknik kullanıcılar hem de iş paydaşları için daha değerli hale geliyor.