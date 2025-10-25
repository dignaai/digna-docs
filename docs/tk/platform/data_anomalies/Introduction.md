---
title: Data Anomalies – Otomatik Tespit | digna Belgeleri
description: Elle kurallar yazmadan digna Data Anomalies'in hacim düşüşlerini, eksik değerleri, dağılım değişikliklerini ve beklenmeyen desenleri nasıl otomatik olarak tespit ettiğini keşfedin. Veri kalitesini yapay zekâ destekli anomali tespitiyle iyileştirin.
---

# Data Anomalies – Otomatik Tespit

## Amaç
Kurallar yazmadan anomalileri yakalayın.

## Teknik Özellikler
### Analiz edilen metrikler
- Kayıt hacmi  
- Eksik değerler  
- Dağılımlar ve histogramlar  
- Değer aralıkları  
- Benzersizlik  

### Akıllı tespit
- Beklenen aralıkları dinamik olarak tanımlamak için **geçmiş verilerden öğrenmeyi** kullanır  
- Gerçek veri beklenen sınırların dışına çıktığında anomalileri işaretler  

## Tespit Senaryoları
- **Hacim düşüşleri/piklenmeleri** → örn. günlük işlemlerin yarısının eksik olması  
- **Sütun yer değiştirmeleri** → örn. ad ve soyad sütunlarının tersine dönmesi  
- **Beklenmeyen değerler** → örn. Avusturyalı şehirlerde “Zurich” görünmesi  

## Değer
Normalde yüzlerce manuel kural gerektirecek işleri otomatikleştirir.