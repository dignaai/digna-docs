---
title: Data Schema Tracker – Şema Evrimini İzleyin | digna Dokümantasyonu
description: digna Data Schema Tracker sütun değişikliklerini, veri tipi güncellemelerini ve şema driftini izler. Hem kasıtlı hem de kasıtsız şema değişikliklerini tespit edip uyarılar göndererek ETL hatalarını, bozuk dashboard'ları ve veri gözlemlenebilirliğinin kaybını önleyin.
image: /assets/logo_square.png
keywords:
  - veri şeması izleme
  - şema drift tespiti
  - şema evrimi izleme
  - metadata gözlemlenebilirliği
  - veri gözlemlenebilirliği
  - veri kalitesi
  - veri yapısı izleme
  - veritabanı metadata
  - etl boru hattı kararlılığı
  - digna Data Schema Tracker
lang: tr
robots: index, follow
og_title: Data Schema Tracker – Şema Evrimini İzleyin | digna Dokümantasyonu
og_description: digna Data Schema Tracker şema driftini, veri tipi değişikliklerini ve sütun güncellemelerini izler. Beklenmeyen yapı değişiklikleri nedeniyle ETL boru hatları veya dashboard'lar arızalanmadan önce uyarılar alın.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Schema Tracker – Şema Evrimini İzleyin
<h1 style="display:none;">AI Destekli Metadata Gözlemlenebilirlik ve Veri Kalitesi Modülü – digna Data Schema Tracker</h1>

---

## Amaç

**Data Schema Tracker** veritabanı yapılarınınızın nasıl evrildiği hakkında sizi bilgilendirir.  
Sürekli olarak **tablo şemalarını, sütunları ve veri tiplerini** izleyerek, boru hatlarını, ETL işleri veya BI dashboard'larını aksatabilecek **şema driftini** — kasıtlı ya da kasıtsız yapısal değişiklikleri — tespit eder.

Şema evriminde şeffaflık sağlayarak digna, kuruluşların **veri kalitesine güveni** korumasına, **veri sistemlerinin gözlemlenebilirliğini** sağlamasına ve tespit edilmemiş şema değişikliklerinden kaynaklanan maliyetli üretim olaylarını önlemesine yardımcı olur.

---

## Teknik Genel Bakış

### Neleri İzler

- **Eklenen veya Kaldırılan Sütunlar** – Yeni eklenen, yeniden adlandırılan veya silinen sütunları tespit eder.  
- **Veri Tipi Değişiklikleri** – `INT → VARCHAR` veya `DATE → TIMESTAMP` gibi değişiklikleri belirler.  
- **Tablo ve View Değişiklikleri** – Tablo ve view oluşturma, yeniden adlandırma veya kaldırma işlemlerini takip eder.  
- **Çevreler Arası Farklılıklar** – Geliştirme (Dev), Test ve Üretim ortamları arasındaki şema sürümlerini karşılaştırır.  

### Tespit & Uyarı

- Doğrudan veri platformunuz içindeki **veritabanı metadata'sını** veya **system catalog**'ları tarar.  
- Her şema anlık görüntüsünü digna’nın observability şemasında saklanan önceki bilinen sürümle karşılaştırır.  
- Gösterge panosunda, API üzerinden veya dış bildirim kanallarında (e-posta, Slack, webhook) **gerçek zamanlı uyarılar** üretir.  
- Her şema sürümünü **tarihsel izleme ve denetim hazır olması** için kaydeder.

---

## Mimari ve Çalışma

- **Veritabanı İçinde Çalışma:** digna tamamen kendi ortamınız içinde çalışır ve veri çıkarmadan metadata görünümlerine sorgular gönderir.  
- **Hafif Taramalar:** yalnızca yapısal bilgilere erişir — asla kullanıcı verilerine dokunmaz.  
- **Merkezi Depolama:** şema metadata'sı ve drift kayıtları görselleştirme ve analiz için digna observability şemasında saklanır.  
- **Otomasyon:** digna Core veya harici orkestrasyon araçları aracılığıyla zamanlanmış veya olay tabanlı taramaları destekler.  

---

## Örnek Kullanım Senaryoları

| Use Case | Description |
|-----------|--------------|
| **ETL Stability Monitoring** | Yukarı akıştaki yapı değişikliklerini, şema uyumsuzlukları nedeniyle boru hatları başarısız olmadan önce tespit edin. |
| **Business Intelligence Reliability** | Yeniden adlandırılmış veya eksik sütunlardan kaynaklanan bozuk dashboard'ların oluşmasını önleyin. |
| **Data Warehouse Governance** | Uyumluluk ve etki analizi için şema evriminin denetlenebilir bir geçmişini tutun. |
| **Integration Oversight** | Yapısal güncellemeler sonrasında veri gölü ve veri ambarı şemalarının senkronize kalmasını sağlayın. |

---

## Faydalar

| Area | Benefit |
|------|----------|
| **Data Quality** | Verileri bozabilecek veya geçersiz kılabilecek tespit edilmemiş şema driftini önler. |
| **Observability** | Veri ekosistemlerinin genel gözlemlenebilirliğine yapısal izleme ekler. |
| **Compliance** | Denetim, izlenebilirlik ve değişiklik kontrolü için sürümlenmiş şema geçmişi sağlar. |
| **Prevention** | Yapısal sorunların raporlama veya üretim hatalarına dönüşmeden önce tespit edilmesini sağlar. |

---

## Nasıl Çalışır

1. **Snapshot Toplama** – digna mevcut şema metadata'sının anlık görüntüsünü alır.  
2. **Karşılaştırma** – yeni snapshot, önceki sürüm ile karşılaştırılır