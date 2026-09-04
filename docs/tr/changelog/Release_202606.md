---
title: digna Sürüm 2026.06 | Python SDK, Docker Dağıtımı & Geliştirilmiş Doğrulama Yönetimi
description: digna Sürüm 2026.06'da neler yenilendi öğrenin. Bu sürüm yeni digna Python SDK'sını, Docker dağıtım desteğini, yenilenmiş bir dashboard deneyimini ve doğrulama kuralı yönetimi için genişletilmiş içe/dışa aktarma yeteneklerini tanıtıyor.
keywords: digna Sürüm 2026.06, digna Python SDK, digna Docker desteği, veri kalite otomasyonu, veri profilleme, doğrulama kuralı içe/dışa aktarımı, digna dashboard, veri gözlemlenebilirlik platformu, Python API, metadata otomasyonu
image: /assets/logo_square.png
---

# Sürüm Notları – 2026.06  

Sürüm 2026.06 ile digna otomasyon, genişletilebilirlik ve platform kullanılabilirliğinde önemli bir adım atıyor.  
Bu sürüm yeni **digna Python SDK**'sını, resmi **Docker dağıtım desteğini**, yenilenmiş bir dashboard deneyimini ve doğrulama kuralı yönetimi için geliştirilmiş taşınabilirlik özelliklerini sunuyor.

---

## Yeni Özellikler  

### digna Python SDK – Her şeyi Python ile Otomatikleştirin  
- Kurulum:
  ```bash
  pip install digna-sdk
  ```
- digna'yı Python ile programatik olarak yönetme ve otomatikleştirme  
- Projeleri kod ile oluşturma ve yapılandırma  
- İncelemeleri ve izleme yürütmelerini tetikleme  
- Veri setlerini, kuralları ve yapılandırmaları programatik olarak yönetme  
- Tabloları profilleme ve meta veri içgörüleri çıkarma  
- Profil ve veri kalite sonuçlarını harici depo ve sistemlere aktarma  
- Notebook'lar, orkestrasyon araçları ve CI/CD pipeline'ları ile entegrasyon  

Etkisi: Python kullanarak tam altyapı-as-code (infrastructure-as-code) ve veri kalitesi ile gözlemlenebilirlik iş akışlarının derin otomasyonunu mümkün kılar.

---

### Docker Desteği – Basitleştirilmiş Dağıtım ve Operasyon  
- digna için resmi Docker imajı desteği  
- Ortamlar arasında hızlı ve tutarlı kurulum  
- Geliştirme, test ve üretim için basitleştirilmiş onboarding  
- Kubernetes ve konteyner platformları ile kolay entegrasyon  
- Dağıtımların daha iyi taşınabilirliği ve tekrarlanabilirliği  

Etkisi: digna'yı modern bulut yerel mimarilerde dağıtmayı ve işletmeyi kolaylaştırır.

---

### QueryMode – Esnek SQL Yürütme Stratejisi

Sorgu yürütme stratejisini yapılandırın: **Single** veya **Combined** mode

**Single Mode**: Her istatistik, kendine ait tek bir SQL sorgusu ile hesaplanır

  - Bellek kısıtlarının önemli olduğu büyük veri kaynakları için ideal
  - Birleştirilmiş sorgunun kaynak tükenmesini (bellek tükenmesi, spool limitleri) önler
  - Daha yüksek sorgu sayısı ancak sorgu başına daha düşük bellek kullanımı

**Combined Mode**: Tüm istatistikler tek bir SQL sorgusunda hesaplanır

  - Toplam sorgu sayısını ve ağ yükünü azaltır
  - Veri kaynakları bellekte yönetilebilir olduğunda performansı optimize eder
  - Sık ve paralel yürütmeler için daha verimlidir

Etkisi: Kullanıcılara veri kaynağı özelliklerine göre performans, kaynak kullanımı ve bellek güvenliği arasında denge kurmak için ince ayar yapma imkanı verir.

---

### Yeniden Tasarlanmış Dashboard Deneyimi  
- Modernize edilmiş ve geliştirilmiş UI/UX tasarımı  
- Daha net gezinme ve yapı  
- İzleme sonuçları ve veri kalite içgörülerinin daha iyi görünürlüğü  
- Alarm, istatistik ve dashboard okunuşunun iyileştirilmesi  
- Ana operasyonel bilgilere daha hızlı erişim  

Etkisi: Tüm kullanıcılar için kullanılabilirliği ve günlük verimliliği artırır.

---

### Doğrulama Kuralları için Gelişmiş İçe/Dışa Aktarım  
- Doğrulama kuralları için geliştirilmiş içe/dışa aktarma işlevselliği  
- Ortamlar ve projeler arasında daha kolay göç  
- Standartlaştırılmış kural setlerinin daha iyi yeniden kullanımı  
- Daha iyi yönetişim ve kural yaşam döngüsü yönetimi  
- Ekipler arası iş birliğinin basitleştirilmesi  

Etkisi: Kuruluş genelinde ölçeklenebilir ve tutarlı veri kalite yönetişimi sağlar.

---

## Platform Geliştirmeleri  

- Otomasyon için tam Python SDK entegrasyonu  
- Docker ile konteynerleştirilmiş dağıtım  
- Yeniden tasarlanmış dashboard ile geliştirilmiş UX  
- Doğrulama mantığının genişletilmiş taşınabilirliği  

---

## Bu Sürümden Kim Yararlanır  

- Veri Mühendisleri: otomasyon, SDK kullanımı, pipeline entegrasyonu  
- Platform Ekipleri: Docker ile basitleştirilmiş dağıtım  
- Veri Yönetişim Ekipleri: yeniden kullanılabilir doğrulama kuralı yönetimi  
- Analitik Ekipleri: geliştirilmiş kullanılabilirlik ve içgörü görünürlüğü  

---

## CLI Güncellemeleri  
- SDK entegrasyon desteği eklendi  
- İçe/dışa aktarma iş akışları iyileştirildi  
- Genel kararlılık ve performans iyileştirmeleri  
