---
title: digna Sürüm 2025.09 | Modüler Tasarım, Beş Yeni Modül, MFA via OIDC
description: digna Sürüm 2025.09'daki yenilikleri öğrenin. Bu sürüm modüler bir mimari, beş yeni modül, MFA via OIDC ve modül başına bildirimler sunuyor.
keywords: digna Sürüm 2025.09, digna değişiklik günlüğü, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna modüler tasarım, digna OIDC MFA
image: /assets/logo_square.png
---

# Değişiklikler – Sürüm 2025.09  

digna, Sürüm 2025.09 ile yeni bir **modüler mimari** tanıtıyor ve Veri Kalitesi ile gözlemlenebilirlik için **beş uzmanlaşmış modül** sunuyor.  
Bu sürüm ayrıca kimlik doğrulamayı güçlendirir ve platform genelinde bildirim yönetimini iyileştirir.  

---

## Yeni Özellikler  

### Modüler Tasarım  
- digna artık **modüler bir mimari** izliyor.  
- Müşteriler yalnızca ihtiyaç duydukları modülleri etkinleştirebilir ve gereksinimler büyüdükçe yeni modüller ekleyebilir.  
- Önceki işlevsellik artık **digna Data Anomalies** modülünün bir parçasıdır.  

### Yeni Modüller  
- **digna Data Anomalies** – Veri hacimlerindeki, dağılımlarındaki ve eksik değerlerdeki anomalileri AI destekli tespit eder.  
- **digna Data Analytics** – Gözlemlenebilirlik metriklerinin zaman serisi değerlendirmesini yaparak uzun vadeli eğilimleri ve oynaklığı tespit eder.  
- **digna Data Timeliness** – Beklenen veri varış zamanlarını hem AI tabanlı hem de kural tabanlı olarak izler.  
- **digna Data Validation** – İş kurallarına uyumu sağlamak için kayıt düzeyinde kural tabanlı kontroller uygular.  
- **digna Data Schema Tracker** – İzlenen veritabanlarındaki şema değişikliklerini (DDL değişiklikleri) tespit eder.  

### MFA via OIDC  
- OIDC Single Sign-On ile **Çok Faktörlü Kimlik Doğrulama (MFA)** desteği.  
- Tüm kullanıcı girişleri için kurumsal düzeyde güvenlik sağlar.  

### Modül Başına Bildirim E-postaları  
- Bildirimler artık **modül bazında** gönderiliyor; böylece Data Anomalies, Data Analytics ve diğer modüllerden gelen uyarılar kolayca ayrılabiliyor.  

---

## CLI Güncellemeleri  

- **Yeni komut: `inspect-cancel`** – Denetimleri istek kimliğine göre iptal edin veya tüm aktif istekleri sonlandırın.  
- **Yeni komut: `check-config`** – Başlangıç öncesinde yapılandırma dosyalarını doğrulayın.  
- **Yeni komut: `remove-orphans`** – Yetim depo girdilerini temizleyin.  
- **Geliştirilmiş `inspect` komutu** – Yeni seçenek `--bypass-backend` (`-bb`) ve standartlaştırılmış dönüş kodları (`0 = OK, 1 = INFO, 2 = WARNING`).  


## Dokümantasyon  
- Yeni kılavuzlar:  
  - Single Sign-On Entegrasyon Kılavuzu