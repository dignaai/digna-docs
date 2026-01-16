---
title: Data Anomalies – Verideki Düzensizliklerin Otomatik Tespiti | digna Documentation
description: digna Data Anomalies, manuel kural yazımı olmadan veri hacmi düşüşlerini, eksik değerleri, dağılım değişikliklerini ve beklenmeyen desenleri otomatik olarak tespit eder. AI tabanlı anomali tespiti ile veri kalitesini ve veri boru hatlarının gözlemlenebilirliğini iyileştirin.
image: /assets/logo_square.png
keywords:
  - veri anomalileri
  - ai anomali tespiti
  - veri kalitesi izleme
  - verinin kalitesi
  - veri gözlemlenebilirliği
  - eksik veri tespiti
  - veri hacmi izleme
  - dağılım kayması
  - veri güvenilirliği
  - digna data anomalies
lang: tr
robots: index, follow
og_title: Data Anomalies – Otomatik Tespit | digna Documentation
og_description: digna Data Anomalies, ham kurallar olmadan veri hacmi, değerler ve dağılımlardaki düzensizlikleri otomatik olarak tespit eder — platformlar arasında veri kalitesi ve gözlemlenebilirliği artırır.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Anomalies – Otomatik Tespit
<h1 style="display:none;">AI Tabanlı Veri Kalitesi ve Gözlemlenebilirlik Modülü – digna Data Anomalies</h1>

---

## Amaç

**Data Anomalies** modülü, veri kümelerinizdeki düzensizlikleri otomatik olarak tespit eder — kural yazmaya gerek yoktur.  
Sürekli olarak **veri teslimatının kalitesini** izler, “normal”i öğrenir ve gerçek zamanlı olarak sapmaları algılar.

AI tabanlı tespit kullanarak, digna raporları, ML modellerini ve panoları bozabilecek *sessiz veri hatalarını* (eksik, çoğaltılmış veya bozulmuş kayıtlar gibi) tanır.

---

## Teknik Genel Bakış

### Analiz edilen metrikler

digna aşağıdaki veri yönlerini sürekli olarak profilleştirir:

- **Kayıt hacmi** – toplam satır sayısı, günlük veya batch bazlı  
- **Eksik değerler** – null veya boş alanların tespiti  
- **Dağılımlar ve histogramlar** – veride şekil değişikliklerinin izlenmesi  
- **Değer aralıkları** – sınır dışı veya uç değerlerin otomatik tespiti  
- **Benzersizlik** – tekrar eden anahtarlar veya tekrar eden kayıtlar için kontroller  

### Akıllı anomali tespiti

- Beklenen sınırları dinamik olarak tanımlamak için **tarihi öğrenme** kullanır  
- **Hacim, değer dağılımları veya mantıksal ilişkilerdeki** sapmaları tespit eder  
- Zamanın saati veya mevsimsel desenlere göre eşiklerini otomatik uyarlamak için AI kullanır  
- **İstatistiksel dalgalanmalar** ile gerçek anomaliler arasındaki farkı ayırt eder  
- Her veri kümesi ve sütun için ayrıntılı metrikler ve güven skorları üretir  

---

## Tespit Senaryoları

Aşağıda **Data Anomalies** modülünün otomatik olarak yakaladığı gerçek dünya sorunlarına örnekler verilmiştir:

| Scenario | Description |
|-----------|--------------|
| **Volume drops or spikes** | Günlük işlemlerin yarısının eksik olması, tekrar eden batch yüklemeleri veya ani veri patlamaları |
| **Missing or null values** | Veri çekimleri tamamlanmış ancak kritik sütunların boş bırakılması |
| **Distribution drifts** | Bölge bazında ortalama satın alma tutarı veya işlem sayısının beklenmedik şekilde değişmesi |
| **Column swaps** | ETL sırasında *first_name* ve *last_name* gibi sütunların yanlışlıkla yer değiştirmesi |
| **Unexpected categorical values** | Örn. “Zurich”in Avusturya şehirleri listesinde görünmesi |
| **Sudden uniqueness loss** | Önceden benzersiz olan kimliklerin, upstream join hataları nedeniyle çoğalmaya başlaması |

---

## Mimari ve Çalışma

- **Veritabanı içinde yürütme:** Tüm anomali tespiti mantığı *veritabanı motoru içinde* çalıştırılır (Teradata, Snowflake, Databricks, PostgreSQL vb.)  
- **Veri taşınmaması:** digna yalnızca metrikleri okur, ham veriyi dışarı aktarmamış olur  
- **Artımlı güncellemeler:** Verimlilik için her çalıştırmada yalnızca yeni veri segmentleri analiz edilir  
- **Konfigüre edilebilir inceleme sıklığı:** Saatlik, günlük veya upstream süreçler tarafından tetiklenen  
- **Sonuç depolama:** Metrikler ve anomali bayrakları görselleştirme ve uyarı için digna’nın gözlemlenebilirlik şemasına yazılır  

---

## Faydalar

| Area | Benefit |
|------|----------|
| **Automation** | Yüzlerce manuel SQL veya kural tanımını ortadan kaldırır |
| **Precision** | Statik eşiklerin sıklıkla kaçırdığı sorunları tespit eder |
| **Scalability** | Tablonun milyonlarca kaydını verimli şekilde izler |
| **Integration** | Eğilim analizi için *digna Data Analytics* ile sorunsuz çalışır |
| **Compliance** | **veri kalitesi ve gözlemlenebilirliği** üzerinde sürekli kontrol sağlar |
| **Transparency** | Her anomali için güven skorları, zaman damgaları ve sebep kodları sunar |

---

## digna’nin “Normal”i Nasıl Öğrendiği

1. **Profil oluşturma aşaması:** digna geçmiş veri kümelerinden metrikler toplar.  
2. **Öğrenme aşaması:** AI modelleri tekrar eden desenleri (mevsimsel, haftalık, günlük) belirler.  
3. **İzleme aşaması:** Gelecek veri kümeleri dinamik olarak öğrenilmiş eşiklerle karşılaştırılır.  
4. **Uyarı aşaması:** İstatistiksel güven sınırlarını aşan sapmalar anomali olarak raporlanır.  

Tüm modeller açıklanabilir, determinizmdir ve kurumsal veri hacimleri için optimize edilmiştir.

---

## Örnek Kullanım Senaryoları

- **Banka işlem sistemlerinde** veri kalitesini izleme  
- **ETL veya veri ambarı işlerindeki** yükleme hatalarını tespit etme  
- **Telekom kayıtlarında** anormal müşteri etkinliklerini belirleme  
- **Sağlık analitiği boru hatlarında** klinik veri tutarlılığını gözlemleme  
- **BI ve raporlama ortamlarında** kırılan panoların önlenmesi

---

## Sıkça Sorulan Sorular

**Data Anomalies önceden tanımlanmış kurallar gerektirir mi?**  
Hayır — modül verinin davranışından otomatik olarak öğrenir.

**Gerekirse belirli eşikleri yine de tanımlayabilir miyim?**  
Evet. digna, AI tabanlı ve kural tabanlı tespiti birleştirmeye izin verir (via *Data Validation*).

**Yanlış pozitifler nasıl azaltılır?**  
Modül, normal mevsimsel varyasyonları göz ardı etmek için uyarlanabilir öğrenme ve istatistiksel güven puanlaması kullanır.

**Hesaplama nerede gerçekleşir?**  
Tüm işlem veritabanınız içinde çalışır — digna ham veriyi asla çıkartmaz.

**Hassas veya düzenlemeye tabi veriler için uygun mu?**  
Evet. digna tamamen kurum içi (on-premises) veya özel bulutta çalışır ve Avrupa uyumluluk standartlarına uyar.

---