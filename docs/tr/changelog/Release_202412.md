---
title: digna Sürüm 2024.12 | Değişiklik Günlüğü & Yeni Özellikler
description: digna Sürüm 2024.12'te nelerin yeni olduğunu keşfedin. Bu sürüm yerleşik zamanlayıcı, PDF raporlaması, esnek özel sütunlar, dinamik snapshot sorgu yer tutucuları ve anomali tespiti ile veri kalitesi izleme için daha akıllı eşik optimizasyonu sunar.
keywords: digna Sürüm 2024.12, digna değişiklik günlüğü, sürüm notları, yerleşik zamanlayıcı, PDF raporları, özel sütun türü, snapshot sorgu yer tutucuları, eşik optimizasyonu, veri gözlemlenebilirliği, veri kalitesi izleme, anomali tespiti
canonical_url: https://docs.digna.ai/changelog/Release_202412/
image: /assets/logo_square.png
---



# Değişiklik Günlüğü – Sürüm 2024.12

2024.12 sürümü, digna'yı daha otomatik, esnek ve iş odaklı hale getiren yeni özellikler ve iyileştirmeler sunar.  
Bu sürüm planlama, raporlama, sorgu işleme ve anomali tespiti doğruluğunu geliştirir.  

---

## Yeni Özellikler

### Yerleşik Zamanlayıcı
Denetimler artık yalnızca komut satırı veya API çağrılarına bağlı değil.  
**yeni digna Zamanlayıcı** ile denetimler tanımlı zamanlarda otomatik olarak çalıştırılabilir.  

- Tekrarlayan zamanlamalar (günlük, haftalık veya özel aralıklar) için **Cron ifadelerini** destekler.  
- **offset'ler**, **başlangıç tarihleri** ve **bitiş tarihleri** ile hassas kontrol sağlar.  
- Ekiplerin tüm kritik veri kaynaklarının tutarlı ve manuel müdahale olmadan denetlendiğinden emin olmasını sağlar.  

---

### PDF Formatında Raporlar
Ekipler artık sonuçları paydaşlarla kolayca paylaşmak için **PDF dışa aktarımları** kullanabilir.  

- Grafikler, metrikler ve anomali sonuçları profesyonel PDF formatında dışa aktarılabilir.  
- Raporlar hem teknik hem de iş kullanıcılarına hizmet edecek şekilde **görselleştirmeleri** ve **altyapı verilerini** birleştirir.  
- Rapor oluşturmak için harici araçlara ihtiyaç duyulmasını ortadan kaldırır.  

---

### Yeni Sütun Türü: `CUSTOM`
Daha fazla esneklik sağlamak için digna yeni bir **`CUSTOM` sütun türü** tanıtıyor.  

- Kullanıcılar belirli özniteliklere hangi **istatistiklerin ve metriklerin** uygulanacağını tam olarak tanımlayabilir.  
- NUMERICAL veya CATEGORICAL gibi standart kategorilere uymayan özel durumlar için idealdir.  
- Analizlerin odaklanmasını sağlar ve sonuçları iş bağlamına daha uygun hale getirir.  

---

### Snapshot Sorgularında Yeni Yer Tutucular
Snapshot sorguları, **dinamik yer tutucular** sayesinde artık daha basit ve hata yapmaya daha az yatkın.  

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
- Daha az yanlış pozitif ve daha güvenilir anomali tespitleri sağlar.  

---

## Genel İyileştirmeler
- Proje ve öznitelik yapılandırma görünümlerinde geliştirilmiş **UI bileşenleri**.  
- Büyük veri hacimleri için geliştirilmiş **gösterge paneli performansı**.  
- Sorun giderme için geliştirilmiş **loglama ve hata mesajları**.  

---

## Özet
Sürüm 2024.12, digna'yı **veri kalitesi, anomali tespiti ve gözlemlenebilirlik** platformu olarak güçlendirir.  
Zamanlama ile otomasyon, paylaşılabilir PDF raporlar, özelleştirilebilir sütunlar, sadeleştirilmiş snapshot sorguları ve daha akıllı eşikler sayesinde digna, hem teknik kullanıcılar hem de iş paydaşları için daha değerli hale gelir.