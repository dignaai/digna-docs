---
title: Data Timeliness – Zamanında Teslimat İzleme | digna Dokümantasyonu
description: digna Data Timeliness'in verinin beklendiği zamanda gelmesini nasıl sağladığını öğrenin. Geciken veya eksik teslimatları tespit edin, SLA'ları izleyin ve iş süreçlerini sessiz gecikmelerden koruyun. Geliştirilmiş veri kalitesi ve veri boru hatlarının gözlemlenebilirliği için AI destekli tespit.
canonical_url: https://docs.digna.ai/platform/data_timeliness/
image: /assets/logo_square.png
keywords:
  - veri zamanlılığı
  - teslimat izleme
  - veri kalitesi
  - verinin kalitesi
  - veri gözlemlenebilirliği
  - gecikmiş veri tespiti
  - eksik veri uyarıları
  - sla izleme
  - ai teslimat analizi
  - digna data timeliness
lang: tr
robots: index, follow
og_title: Data Timeliness – Zamanında Teslimat İzleme | digna Dokümantasyonu
og_description: digna Data Timeliness, gecikmiş veya eksik veri teslimatlarını AI kullanarak otomatik olarak tespit eder. İş süreçlerini koruyun, SLA'ları izleyin ve tüm boru hatlarında zamanında, güvenilir veri sağlayın.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Timeliness – Zamanında Teslimat İzleme
<h1 style="display:none;">AI Destekli Data Timeliness Modülü Veri Kalitesi ve Gözlemlenebilirlik için – digna</h1>

---

## Amaç

**Data Timeliness** modülü, **verinin zamanında ulaşmasını** sağlar - her seferinde.  
Teslimat programlarını sürekli izler ve veri setleri, tablolar veya dosyaların **geciktiği, eksik olduğu veya tamamlanmadığı** durumları otomatik olarak tespit eder.  

AI öğrenimini kullanıcı tanımlı programlarla birleştirerek, *digna* kuruluşların alt süreç hatalarını önlemesine ve hem **Veri Kalitesi** hem de **veri boru hatlarının gözlemlenebilirliği** için katı **SLA (Hizmet Seviyesi Anlaşması)** hedeflerini sağlamasına olanak tanır.

---

## Teknik Genel Bakış

### Çift İzleme Modu
- **AI ile Öğrenilen Varış Davranışları**  
  digna, geçmiş zaman damgalarını ve tamamlama sürelerini analiz ederek veri teslimatlarınızın günlük, saatlik veya olay tetikli doğal ritmini otomatik olarak öğrenir.  
  İş takvimlerindeki değişikliklere, hafta sonlarına veya ay sonu yoğunluklarına uyum sağlar.

- **Kullanıcı Tanımlı Programlar**  
  Kullanıcılar beklenen teslimat zamanlarını açıkça tanımlayabilir (ör. *her işgünü 07:30'dan önce*).  
  digna, gerçek varış zamanını planlanan programla karşılaştırır ve veri geç kaldığında veya eksik olduğunda uyarılar oluşturur.

### Tespit Mekanizması
- **metadata zaman damgalarını**, **kayıt sayılarını** ve **tablo tazeliğini** değerlendirir  
- **duraksayan ETL işler**, **başarısız ekstraksiyonlar** ve **kısmi dosya gelişleri** tespit eder  
- Birleşik içgörüler için *Data Anomalies* ve *Data Validation* ile entegre olur

---

## Tespit Senaryoları

| Senaryo | Açıklama |
|-----------|--------------|
| **Geciken veri gelişi** | Günlük piyasa veri akışının iki saat gecikmesi, raporların SLA'ları kaçırmasına neden olur |
| **Eksik yükleme** | Planlı bir tablo veya partition'ın o gün için güncellenmemesi |
| **Zincirlenmiş bağımlılık gecikmesi** | Yukarı akıştaki bir işin gecikmesi aşağı akış hattın yenilenmesini etkiler |
| **Hafta sonu desen değişimi** | AI modeli, Pazar günleri veri beklenmediğinde otomatik olarak uyum sağlar |

---

## Mimari ve Yürütme

- **Veritabanı içinde yürütme:** digna zamanlılık kontrollerini doğrudan veritabanınızda veya veri ambarınızda çalıştırır.  
- **Hafif metadata erişimi:** iş zaman damgalarını, kayıt sayılarını ve partition bilgilerini okur — veri çıkarımı gerekmez.  
- **Yapılandırılabilir sıklık:** izlemeyi veri seti, şema veya boru hattı bazında zamanlayın.  
- **Modüller arası uyarılar:** sonuçlar *Inspection Hub* içinde görsel uyarılar veya e-posta, Slack ya da API üzerinden bildirimler tetikleyebilir.  

---

## Örnek Kullanım Durumları

- **Finansal Piyasa Akışları:** fiyat veya işlem verisi güncellemelerindeki gecikmeleri tespit edin.  
- **Veri Ambarı Yüklemeleri:** gece çalışması yapan ETL işlerinin beklenenden daha geç bitip bitmediğini izleyin.  
- **Ekipler Arası Veri Paylaşımı:** departmanlar arası veri teslimlerinin günlük kesme zamanlarından önce gerçekleştiğinden emin olun.  
- **Düzenleyici Raporlama:** gönderimlerin en güncel veri anlık görüntüsünü içerdiğini doğrulayın.  

---

## Faydalar

| Alan | Fayda |
|------|----------|
| **İş Sürekliliği** | Gecikmiş veya eksik veriye bağlı operasyonel aksaklıkları önler |
| **Veri Kalitesi** | Veri boru hatlarının güvenilirliğini ve tutarlılığını artırır |
| **Uyumluluk** | SLA uyumunu ve denetim şeffaflığını sağlar |
| **Otomasyon** | AI manuel program takibini ortadan kaldırır |
| **Entegrasyon** | Zaman içinde zamanlılık eğilimlerini görselleştirmek için *Data Analytics* ile sorunsuz çalışır |

---

## digna Beklenen Teslim Zamanlarını Nasıl Öğrenir

1. **Tarihsel Analiz:** digna önceki yükleme zamanlarını ve sürelerini gözlemler.  
2. **AI Modellemesi:** Makine öğrenimi, beklenen varış için dinamik bir temel oluşturur.  
3. **İzleme:** Her yeni teslimat bu temelle karşılaştırılır.  
4. **Uyarı:** Sapmalar, bağlamsal metrikler ve güven skorlarıyla birlikte uyarıları tetikler.  

Bu sürekli öğrenme yaklaşımı, süreçler evrildikçe uyum sağlar ve yanlış pozitifleri düşük tutar.

---

## Sıkça Sorulan Sorular

**Kendi teslimat zamanlarımı tanımlayabilir miyim?**  
Evet. digna hem sabit kullanıcı programlarını hem de AI ile öğrenilen desenleri destekler.

**ETL veya orkestrasyon aracımla entegre olabilir mi?**  
Evet. digna Airflow, dbt, Informatica veya özel zamanlayıcılar gibi araçlarla entegre olur.

**Hesaplama nerede gerçekleşir?**  
Tüm analizler veritabanınızda veya bulut ambarınızda çalışır — dış bir servis kullanılmaz.

**Veri geç kaldığında ne olur?**  
digna panoda, Inspection Hub'da ve API/webhook'lar aracılığıyla operasyon ekiplerini anında bilgilendiren uyarılar oluşturur.

---


**digna Data Timeliness**, **AI destekli tespit**, **yerinde yürütme** ve **veri gözlemlenebilirliğini** birleştirerek — tümünü kontrolünüz altındaki ortamda — **veriye güveni** sağlamaya yardımcı olur.