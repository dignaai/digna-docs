# Değişiklik Günlüğü – Sürüm 2026.04  

Sürüm 2026.04 ile digna analitik ve veri doğrulama yeteneklerini önemli ölçüde geliştiriyor.  
Bu sürüm gelişmiş zaman serisi analizi, yeniden kullanılabilir doğrulama bileşenleri ve merkezi değer standardizasyonu sunuyor.

---

## Yeni Özellikler  

### Analytics Chart – Veri Bilimi Gerektirmeyen Zaman Serisi Analizi  
- Etkileşimli zaman serisi analizi için yeni **Analytics Chart**  
- Dahili analitik yöntemler:
    - Doğrusal, kuadratik ve kübik regresyon  
    - Yapılandırılabilir kırılma noktalarına sahip parçalı regresyon  
    - Düzgünleştirme teknikleri  
    - Kuantil analizi  
- Eğilim, mevsimsellik ve desen değişikliklerinin otomatik tespiti  
- Sapmalara dair daha derin içgörü için artık analizleri  
- Her veri kümesi için zaman serileri otomatik olarak hesaplanır  

**Etkisi:** Kullanıcıların veri bilimi uzmanlığı veya harici araçlara ihtiyaç duymadan karmaşık veri davranışlarını zaman içinde anlamasını sağlar.

---

### Enumerations – İzin Verilen Değerlerin Merkezi Tanımı  
- Yeniden kullanılabilir izin verilen değer setlerini tanımlayın (ör. ülkeler, eyaletler, durum kodları)  
- Sütun değerlerini önceden tanımlanmış enumerations ile **digna Data Validation** içinde doğrulayın  
- Enumerations’ları projeler ve veri kaynakları arasında yeniden kullanın  
- `#ENUM:MY_ENUM#` ile her yerde enumerations kullanın  
- Tüm kontroller **doğrudan kaynak veritabanında** yürütülür  

**Etkisi:** Kurum genelinde tutarlı ve standardize edilmiş veri değerleri sağlar.

---

### Doğrulama Kuralı Şablonları – Yeniden Kullanılabilir Veri Kalitesi Mantığı  
- Yeniden kullanılabilir doğrulama kuralları tanımlayın (ör. boşluk kontrolü, NOT NULL, format kontrolleri)  
- Şablonları birden çok veri kümesi üzerinde uygulayın  
- Projeler arasında tutarlı kural mantığı sağlayın  
- Yinelemeyi ve manuel konfigürasyonu azaltın  
- Tüm kontroller **doğrudan kaynak veritabanında** yürütülür  

**Etkisi:** Veriyi taşımaya gerek kalmadan ölçeklenebilir ve yüksek performanslı veri doğrulama sağlar.

---

### İstatistik Düzeyi Alaka Koşulları  
- Her istatistik için **sütun düzeyinde** alaka koşulları tanımlayın  
- Anomali alaka koşulları kavramını genişletir  
- Bir istatistiğin ne zaman alakalı sayılacağını kontrol edin  
- Kritik olmayan durumları hariç tutarak gürültüyü azaltın  

**Etkisi:** Sadece anlamlı sapmalara odaklanarak sinyal kalitesini iyileştirir.

---

## Genişletilmiş Data Analytics ve Doğrulama Yetkinlikleri  

Bu sürümle digna hem **veri anlama** hem de **veri doğrulama standardizasyonunu** genişletiyor:

- Veri bilimi bilgisi olmadan gelişmiş **zaman serisi yorumlama**  
- Enumerations ile **izin verilen değerlerin** merkezi tanımı  
- Şablonlar aracılığıyla yeniden kullanılabilir **doğrulama mantığı**  
- İstatistiklerin ve uyarıların **alakası** üzerinde ince ayar kontrolü  

Bu yetenekler birlikte kuruluşların sorunları tespit etmesinin ötesine geçip **veri kalitesini anlamasını, standardize etmesini ve kontrol etmesini** sağlar.

---

## Bu Sürümdən Kimler Faydalanır  

- **Veri Mühendisleri:** Yeniden kullanılabilir doğrulama mantığı ve izleme davranışı üzerinde gelişmiş kontrol  
- **Veri Kalitesi & Yönetişim Ekipleri:** Sistemler genelinde standardize kurallar ve tutarlı veri doğrulama  
- **Analitik & BI Ekipleri:** Eğilimler ve sapmalar hakkında daha iyi anlayış  
- **Platform Sahipleri:** Basitleştirilmiş analiz ve ölçeklenebilir doğrulama sayesinde artan benimseme  

---

## CLI Güncellemeleri  
- Değişiklik yok  

---