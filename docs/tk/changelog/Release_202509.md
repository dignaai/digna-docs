---
title: digna Sürüm 2025.09 | Modüler Tasarım, Beş Yeni Modül, OIDC ile MFA
description: digna Sürüm 2025.09'daki yenilikleri öğrenin. Bu sürüm modüler bir mimari, beş yeni modül, OIDC ile MFA ve modül başına bildirimleri içerir.
keywords: digna Sürüm 2025.09, digna değişiklik günlüğü, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna modüler tasarım, digna OIDC MFA
image: /assets/logo_square.png
---

# Değişiklik Günlüğü – Sürüm 2025.09  

Sürüm 2025.09 ile digna yeni bir **modüler mimari** tanıtıyor ve Veri Kalitesi ve Gözlemlenebilirlik için **beş uzmanlaşmış modül** sunuyor.  
Bu sürüm ayrıca kimlik doğrulamayı güçlendirir ve platform genelinde bildirim işleyişini iyileştirir.  

---

## 🚀 Yeni Özellikler  

### Modüler Tasarım  
- digna artık **modüler bir mimari** izler.  
- Müşteriler yalnızca ihtiyaç duydukları modülleri etkinleştirebilir ve gereksinimler arttıkça ek modüller ekleyebilir.  
- Önceki işlevsellik artık **digna Data Anomalies**'ın parçasıdır.  

### Yeni Modüller  
- **digna Data Anomalies** – Veri hacimleri, dağılımlar ve eksik değerlerde yapay zekâ destekli anomali tespiti.  
- **digna Data Analytics** – Gözlemlenebilirlik metriklerinin uzun vadeli eğilimlerini ve oynaklığını tespit etmek için zaman serisi değerlendirmesi.  
- **digna Data Timeliness** – Beklenen veri varış zamanlarının izlenmesi; hem yapay zekâ tabanlı hem de kural tabanlı.  
- **digna Data Validation** – İş kurallarına uyumu sağlamak için kural tabanlı kayıt düzeyi kontrolleri.  
- **digna Data Schema Tracker** – İzlenen veritabanlarındaki şema değişikliklerinin (DDL değişiklikleri) tespiti.  

### OIDC ile MFA  
- OIDC Single Sign-On ile **Çok Faktörlü Kimlik Doğrulama (MFA)** desteği.  
- Tüm kullanıcı girişleri için kurumsal düzeyde güvenlik sağlar.  

### Modül Başına Bildirim E-postaları  
- Bildirimler artık **modül başına** gönderiliyor; böylece Data Anomalies, Data Analytics ve diğer modüllerden gelen uyarıları ayırmak kolaylaşıyor.  

---

## 🛠 CLI Güncellemeleri  

- **Yeni komut: `inspect-cancel`** – İncelemeleri istek kimliğine göre iptal edin veya tüm aktif istekleri sonlandırın.  
- **Yeni komut: `check-config`** – Başlatmadan önce yapılandırma dosyalarını doğrulayın.  
- **Yeni komut: `remove-orphans`** – Yetim depo girişlerini temizleyin.  
- **Geliştirilmiş `inspect` komutu** – Yeni seçenek `--bypass-backend` (`-bb`) ve standartlaştırılmış dönüş kodları (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Dokümantasyon  
- Yeni rehberler:  
  - Single Sign-On Entegrasyon Kılavuzu