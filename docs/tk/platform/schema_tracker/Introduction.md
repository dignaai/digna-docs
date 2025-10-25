---
title: Data Schema Tracker – Şema Evrimini İzleyin | digna Dokümantasyonu
description: digna Data Schema Tracker'ın sütun değişikliklerini, veri tipi güncellemelerini ve şema sapmasını nasıl izlediğini öğrenin. Kasıtlı ve kasıtsız değişiklikler için uyarılar alarak ETL hatalarını ve dashboard hatalarını önleyin.
---

# Data Schema Tracker – Şema Evrimini İzleyin

## Amaç
Şema evrimini izlemek ve uyarı vermek.

## Teknik Özellikler
- İzler:
  - Eklenen veya kaldırılan sütunlar
  - Veri tipi değişiklikleri
- Hem kasıtlı hem de kasıtsız şema değişiklikleri için uyarılar  
- ETL pipeline'larını veya dashboard'ları bozabilecek **sessiz şema sapmasını** önler  

## Örnek Kullanım Senaryoları
- İleri aşama hatalara neden olabilecek veri tipi değişikliklerini (ör. `INT` → `VARCHAR`) tespit etme  
- Şema uyumsuzlukları nedeniyle pipeline'lar başarısız olmadan önce veri mühendislerini uyarmak  

## Değer
Ekiplerin **hızla değişen, evrilen veri kümeleri** üzerinde kontrol sahibi olmasını sağlar.