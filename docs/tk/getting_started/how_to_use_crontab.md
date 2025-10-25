---
title: Crontab ile Gelişmiş Zamanlama
description: Crontab ifadeleri kullanarak digna'da bir görevi gelişmiş zamanlamalar için nasıl planlayacağınızı öğrenin.
---

# Crontab ile Gelişmiş Zamanlama

Bu kılavuz, *digna* içinde **crontab ifadeleri** kullanarak görevlerin nasıl zamanlanacağını gösterir.  
Standart desenler (günlük, haftalık, aylık) aksine, crontab size özel zamanlamalar tanımlamada tam esneklik sağlar.

---

## Etkileşimli Demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Neler Öğreneceksiniz

- Gösterge panelinde **Zamanlama** bölümünü nasıl açacağınızı  
- Bir **crontab ifadesi** kullanarak yeni bir görev nasıl oluşturulur  
- Sadece **haftasonları 10:00'da** çalışacak bir zamanlama nasıl ayarlanır  

---

## Örnek: Hafta Sonu Zamanlaması

Bir görevi her **Cumartesi ve Pazar saat 10:00'da** çalışacak şekilde zamanlamak için aşağıdaki ifadeyi kullanın:


- `0` → dakika (saat başı)  
- `10` → saat (10:00)  
- `*` → ayın her günü  
- `*` → her ay  
- `sat,sun` → sadece Cumartesi ve Pazar  

---

## Neden Crontab Kullanmalı?

- Günlük, haftalık veya aylık gibi standart desenlerin ötesinde zamanlamalar oluşturun  
- Kesin çalışma zamanları tanımlayın (belirli günler, saatler veya aralıklar)  
- Hafta sonu görevleri, mesai dışı kontroller veya sık izleme için faydalıdır  

---