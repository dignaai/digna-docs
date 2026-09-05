# Data Validation – Kural Tabanlı Kontroller
<h1 style="display:none;">AI Destekli Data Validation Modülü Veri Kalitesi ve Gözlemlenebilirlik için – digna</h1>

---

## Amaç

The **Data Validation** module ensures the **quality of data** through precise, rule-based checks.  
Kuruluşların deterministik iş ve teknik doğrulama mantıklarını tanımlamasına olanak tanır; böylece verinin uyumluluk standartlarını, sözleşmesel SLA'ları ve düzenleyici gereksinimleri karşıladığından emin olunur.

*Veritabanı içinde kural yürütümü*, *tam denetim izleri* ve *diğer digna modülleriyle entegrasyon*un birleşimiyle, **Data Validation** karmaşık kurumsal ortamlarda tutarlı ve izlenebilir **Veri Kalitesi ve Gözlemlenebilirlik** sağlar.

---

## Teknik Genel Bakış

### Desteklenen Doğrulama Türleri

- **Eşitlik Kontrolleri**  
  Değerlerin beklenen sonuçlarla eşleşip eşleşmediğini doğrulayın (ör. referans kodları, Boolean bayraklar, kategorik eşlemeler).

- **Eşikler ve Aralıklar**  
  Sayısal ölçüleri veya KPI'ları tanımlanmış sınırlarla — statik veya dinamik olarak türetilmiş — doğrulayın.

- **Referans Listeleri ve Lookuplar**  
  Alan değerlerinin onaylı ana veri setleri içinde olup olmadığını kontrol edin (ör. KDV kodları, ISO ülke listeleri, ürün katalogları).

- **Sütunlar Arası Tutarlılık**  
  İlişkisel doğruluğu sağlayın (ör. para birimi bölge ile uyumlu mu, risk kategorisi varlık türü ile eşleşiyor mu).

- **Null İşleme Kuralları**  
  Kritik sütunlardaki beklenmeyen null veya boş değerleri tespit edin.

### Çalıştırma ve Kayıt

- **Veritabanı İçi İşleme** – Tüm doğrulama kuralları veritabanınızda doğrudan çalıştırılır (Teradata, Snowflake, Databricks, PostgreSQL vb.).  
- **Veri Dışa Aktarımı Yok** – digna ham veriyi ortamınızın dışına asla aktarmaz.  
- **Tam İzlenebilirlik** – Her kural sonucu zaman damgası, ilgili veri seti, kayıt sayıları ve geçme/kalma sonuçlarıyla kaydedilir.  
- **Denetim**