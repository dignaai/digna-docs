---
title: digna Sürüm 2024.12 | Değişiklik Günlüğü & Yeni Özellikler
description: digna Sürüm 2024.12'te nelerin yeni olduğunu keşfedin. Bu sürüm dahili bir zamanlayıcı, PDF raporlama, esnek özel sütunlar, dinamik snapshot sorgu yer tutucuları ve anomali tespiti ile veri kalitesi izlemeyi iyileştirmek için daha akıllı eşik optimizasyonu sunar.
keywords: digna Sürüm 2024.12, digna değişiklik günlüğü, sürüm notları, dahili zamanlayıcı, PDF raporları, özel sütun türü, snapshot sorgu yer tutucuları, eşik optimizasyonu, veri gözlemlenebilirliği, veri kalitesi izleme, anomali tespiti
image: /assets/logo_square.png
---



# Değişiklik Günlüğü – Sürüm 2024.12

2024.12 sürümü, digna'yı daha otomatik, esnek ve iş kullanımına hazır hale getiren yeni özellikler ve iyileştirmeler getiriyor.  
Bu sürüm zamanlama, raporlama, sorgu işleme ve anomali tespiti doğruluğunu geliştiriyor.  

---

## Yeni Özellikler

### Yerleşik Zamanlayıcı
İncelemeler artık yalnızca komut satırına veya API çağrılarına bağlı değil.  
Yeni **digna Scheduler** ile incelemeler tanımlı zamanlarda otomatik olarak çalıştırılabilir.  

- Yinelenen zamanlamalar (günlük, haftalık veya özel aralıklar) için **Cron ifadelerini** destekler.  
- **Offset**, **başlangıç tarihleri** ve **bitiş tarihleri** ile hassas kontrol sağlar.  
- Ekiplerin tüm kritik veri kaynaklarının tutarlı şekilde ve manuel çaba gerektirmeden incelenmesini sağlar.  

---

### PDF Formatında Raporlar
Ekipler artık sonuçları paydaşlarla kolayca paylaşmak için **PDF dışa aktarımlarını** kullanabilir.  

- Grafikler, metrikler ve anomali sonuçları profesyonel bir PDF formatında dışa aktarılabilir.  
- Raporlar hem teknik hem de iş kullanıcılarına hizmet edecek şekilde **görselleştirmeleri** ve **altyapı verilerini** birleştirir.  
- Rapor oluşturmak için harici araçlara ihtiyaç duyulmasını ortadan kaldırır.  

---

### Yeni Sütun Türü: `CUSTOM`
Daha fazla esneklik sağlamak için digna yeni bir **`CUSTOM` sütun türü** sunuyor.  

- Kullanıcılar belirli özniteliklere hangi **istatistiklerin ve metriklerin** uygulanacağını tam olarak tanımlayabilir.  
- NUMERICAL veya CATEGORICAL gibi standart kategorilere uymayan özel durumlar için idealdir.  
- Analizleri odaklı tutmaya ve sonuçları iş bağlamına uygun hale getirmeye yardımcı olur.  

---

### Snapshot Sorgularında Yeni Yer Tutucular
Snapshot sorguları artık **dinamik yer tutucular** sayesinde daha basit ve daha az hata eğilimli.  

- `#date+n#` veya `#date-n#` gibi token'lar sorgulardaki tarihleri otomatik olarak ayarlar.  
- Örnek:  
  - `#date+1#` → yarın  
  - `#date-2#` → iki gün önce  
- Manuel tarih hesaplamalarını ortadan kaldırır ve ekipler arasında tutarlılığı sağlar.  

---

### Eşik Optimizasyonu
Anomali eşikleri artık daha akıllı ve bağlama duyarlı.  

- **NULL COUNT** gibi metrikler için alt eşikler otomatik olarak **0** ile sınırlandırılır.  
- Geçersiz veya anlamsız eşiklerin oluşmasını engeller.  
- Daha az yanlış pozitif ve daha güvenilir anomali tespiti sağlar.  

---

## Genel İyileştirmeler
- Proje ve öznitelik yapılandırma görünümlerinde rafine edilmiş **UI bileşenleri**.  
- Büyük veri hacimleri için geliştirilmiş **dashboard performansı**.  
- Sorun giderme için geliştirilmiş **günlük kaydı ve hata mesajları**.  

---

## Özet
2024.12 sürümü, digna'yı **veri kalitesi, anomali tespiti ve veri gözlemlenebilirliği** için daha güçlü bir platform haline getiriyor.  
Zamanlama ile otomasyon, paylaşılıp dışa aktarılabilir PDF raporlar, özelleştirilebilir sütunlar, basitleştirilmiş snapshot sorguları ve daha akıllı eşikler sayesinde digna, hem teknik kullanıcılar hem de iş paydaşları için daha değerli hale geliyor.