---
title: digna Sürüm 2025.09 | Modüler Tasarım, Beş Yeni Modül, OIDC ile MFA
description: digna Sürüm 2025.09'da nelerin yeni olduğunu öğrenin. Bu sürüm modüler bir mimari, beş yeni modül, OIDC üzerinden MFA ve modül başına bildirimler sunuyor.
keywords: digna Sürüm 2025.09, digna değişiklik günlüğü, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna modüler tasarım, digna OIDC MFA
image: /assets/logo_square.png
---

# Değişiklik Günlüğü – Sürüm 2025.09  

Sürüm 2025.09 ile digna yeni bir **modüler mimari** sunuyor ve Veri Kalitesi ile Observability için **beş özel modül** başlatıyor.  
Bu sürüm ayrıca kimlik doğrulamayı güçlendiriyor ve platform genelinde bildirim yönetimini iyileştiriyor.  

---

## 🚀 Yeni Özellikler  

### Modüler Tasarım  
- digna artık **modüler bir mimariye** sahip.  
- Müşteriler yalnızca ihtiyaç duydukları modülleri etkinleştirebilir ve gereksinimler arttıkça yenilerini ekleyebilir.  
- Önceki işlevsellik artık **digna Data Anomalies**’in bir parçasıdır.  

### Yeni Modüller  
- **digna Data Anomalies** – Veri hacimleri, dağılımlar ve eksik değerlerde AI destekli anomali tespiti.  
- **digna Data Analytics** – Uzun vadeli trendleri ve oynaklığı tespit etmek için gözlemlenebilirlik metriklerinin zaman serisi değerlendirmesi.  
- **digna Data Timeliness** – Beklenen veri varış zamanlarının izlenmesi; hem AI tabanlı hem kural tabanlı.  
- **digna Data Validation** – İş kurallarına uyumu sağlamak için kayıt düzeyinde kural tabanlı kontroller.  
- **digna Data Schema Tracker** – İzlenen veritabanlarındaki şema değişikliklerini (DDL değişiklikleri) tespiti.  

### OIDC ile MFA  
- OIDC Single Sign-On ile **Çok Faktörlü Kimlik Doğrulama (MFA)** desteği.  
- Tüm kullanıcı girişleri için kurumsal düzeyde güvenlik sağlar.  

### Modül Başına Bildirim E-postaları  
- Bildirimler artık **modül başına** gönderiliyor; bu sayede Data Anomalies, Data Analytics ve diğer modüllerden gelen uyarıları ayırmak daha kolay.  

---

## 🛠 CLI Güncellemeleri  

- **Yeni komut: `inspect-cancel`** – İnceleme isteklerini request ID ile iptal etme veya tüm aktif istekleri sonlandırma.  
- **Yeni komut: `check-config`** – Başlatmadan önce yapılandırma dosyalarını doğrulama.  
- **Yeni komut: `remove-orphans`** – Sahipsiz repository girdilerini temizleme.  
- **Geliştirilmiş `inspect` komutu** – Yeni seçenek `--bypass-backend` (`-bb`) ve standartlaştırılmış dönüş kodları (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Dokümantasyon  
- Yeni kılavuzlar:  
  - Single Sign-On Entegrasyon Kılavuzu