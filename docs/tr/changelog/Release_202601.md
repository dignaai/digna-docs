---
title: digna Sürüm 2026.01 | Mantıksal Veri Kaynakları, Küresel Bağlantılar ve Gelişmiş Veri Doğrulama
description: digna Sürüm 2026.01'de nelerin yeni olduğunu öğrenin. Bu sürüm küresel veritabanı bağlantıları, mantıksal veri kaynakları, anomali önem koşulları, CSV dışa aktarımları ve referans bütünlüğü kontrollerini içeren gelişmiş veri doğrulamayı tanıtır.
keywords: digna Sürüm 2026.01, digna değişiklik günlüğü, digna veri kaynağı, digna veritabanı bağlantıları, digna Data Anomalies, digna Data Validation, referans bütünlüğü doğrulama, veri kalitesi kuralları, veri gözlemlenebilirliği, digna CSV dışa aktarımı
image: /assets/logo_square.png
---

# Değişiklik Günlüğü – Sürüm 2026.01  

Sürüm 2026.01 ile digna, veri kaynağı modelleme, bağlantı yönetimi ve inceleme kullanılabilirliğinde önemli iyileştirmeler sunuyor.  
Bu sürüm tüm modüller genelinde esnekliği artırır ve **veri kalitesi ve doğrulama kapsamını** önemli ölçüde genişletir.

---

## Yeni Özellikler  

### Küresel Veritabanı Bağlantıları  
- Veritabanı bağlantıları artık **küresel düzeyde** yapılandırılabiliyor.  
- Küresel bağlantılar **tüm projeler** arasında yeniden kullanılabilir; yapılandırma ve bakım basitleşir.  
- **Etkisi:** Operasyonel yükü azaltır ve ortamlar arasında tutarlı bağlantı sağlar.

### Proje Başına Birden Fazla Kaynak Bağlantısı  
- Projeler artık **birden fazla kaynak bağlantı yapılandırmasına** referans verebilir.  
- Karmaşık veri ortamları için daha esnek kurulumlara imkân sağlar.  
- **Etkisi:** Heterojen veri kaynaklarına sahip gerçek dünya kurumsal mimarilerini destekler.

### Mantıksal Veri Kaynakları  
- Veri kaynakları artık bir proje içinde **mantıksal bir katmanı** temsil ediyor.  
- Her veri kaynağı şu unsurlarla desteklenebilir:
    - bir **veritabanı tablosu**
    - bir **veritabanı görünümü**
    - bir **özel SQL ifadesi**  
- Bu ayrım yeniden kullanım, açıklık ve modüller arası inceleme modellemesini iyileştirir.  
- **Etkisi:** İncelemeleri ve veri kalitesi kurallarını fiziksel depolamadan ayırarak bakım kolaylığı ve yeniden kullanım sağlar.

### Anomali Önem Koşulu  
- Artık bir veri kümesi düzeyinde anomali durum değerlendirmesini kontrol etmek için bir **Anomali Önem Koşulu** tanımlanabilir.  
- İstatistikler, koşulun ayarlanıp ayarlanmadığından veya yerine getirilip getirilmediğinden bağımsız olarak hesaplanır.  
- Koşul **karşılanmıyorsa**, **digna Data Anomalies** anomali durumu (yeşil / sarı / kırmızı) sağlamaz.  
- **Örnek:** Kayıt sayısı 10'un altında olduğunda veri kümesini anomali değerlendirmesinden hariç tutun.  
- **Etkisi:** Anomalilerin yalnızca ilgili iş bağlamlarında değerlendirilmesini sağlar.

### Modül Bazında Bildirim Yapılandırması  
- Bildirimler artık digna içinde **modül bazında** yapılandırılabilir.  
- **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** ve diğer modüller için uyarı davranışının bağımsız kontrolüne olanak tanır.  
- **Etkisi:** Ekip sorumlulukları ve önceliklerle uyumlu hassas uyarı stratejileri oluşturmayı sağlar.

### İnceleme Sonuçlarını Dışa Aktarma (CSV)  
- Kullanıcılar artık **inceleme sonuçlarını CSV dosyası olarak indirebilir**.  
- Çevrimdışı analiz, raporlama ve harici araçlarla entegrasyon imkânı sağlar.  
- **Etkisi:** Denetimleri, raporlamayı ve sonraki süreçlerde veri kalitesi analizini kolaylaştırır.

---

## Genişletilmiş Veri Doğrulama Yetenekleri  

Bu sürümle birlikte **digna Data Validation**, kapsamlı bir veri kalitesi kural setini destekler:

- **Satır düzeyinde doğrulama kuralları**  
- **Çok sütunlu benzersizlik kontrolleri**  
- **Veri kaynakları arası referans bütünlüğü doğrulaması**

Bu kontroller birlikte, karmaşık veri ortamlarında **yapısal ve ilişkisel veri kalitesi kurallarının** uygulanmasını mümkün kılar.

### Birden Fazla Sütun İçin Benzersizlik Kontrolleri
- Yapılandırılabilir bir **sütun kümesi** için **Benzersizlik Kontrolleri** eklendi.  
- Bileşik anahtarların ve iş düzeyindeki benzersizlik kısıtlarının doğrulanmasını sağlar.  
- **Etkisi:** Tek sütun kontrolleriyle tespit edilemeyen yinelenen iş varlıklarını ortaya çıkarır.

### Referans Bütünlüğü Kontrolleri
- Veri kaynakları arasındaki ilişkileri doğrulamak için **Referans Bütünlüğü Kontrolleri** eklendi.  
- Bir kaynak veri kümesindeki **yabancı anahtar değerlerinin** referans verilen hedef veri kümesinde var olduğunu doğrular.  
- Sahipsiz kayıtları, kırık ilişkileri ve veri tutarlılığı sorunlarını erken tespit etmeye yardımcı olur.  
- Görünümler ve özel SQL dahil olmak üzere **mantıksal veri kaynakları** ile çalışacak şekilde tasarlanmıştır.  
- **Kullanım örnekleri:** veri ambarı bütünlüğü, düzenleyici raporlama, ana veri tutarlılığı ve güvenilir ileri analizler.

---

## Bu Sürümlerden Kimler Yararlanır  

- **Veri Mühendisleri:** Daha esnek veri kaynağı modelleme ve yeniden kullanılabilir veritabanı bağlantıları  
- **Veri Kalitesi & Yönetişim Ekipleri:** İlişkisel bütünlük kurallarını da içerecek şekilde genişletilmiş doğrulama kapsamı  
- **Analitik & BI Ekipleri:** Daha temiz girdiler ve dışa aktarılabilir inceleme sonuçları  
- **Platform Sahipleri:** Azaltılmış yapılandırma karmaşıklığı ve iyileştirilmiş operasyonel sürdürülebilirlik

---

## CLI Güncellemeleri  
- Değişiklik yok

---