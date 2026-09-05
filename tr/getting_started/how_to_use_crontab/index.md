# Crontab ile Gelişmiş Zamanlama

Bu rehber, *digna* içinde **crontab ifadeleri** kullanarak işlerin nasıl zamanlanacağını gösterir.  
Günlük, haftalık, aylık gibi standart desenlerin aksine, crontab özel zamanlamalar tanımlamada tam esneklik sağlar.

---

## Etkileşimli Demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Neler Öğreneceksiniz

- Gösterge panelinde **Scheduling** bölümünü nasıl açacağınızı  
- Bir **crontab ifadesi** kullanarak yeni bir görev nasıl oluşturulur  
- Sadece **hafta sonları saat 10:00'da** çalışacak bir zamanlama nasıl ayarlanır  

---

## Örnek: Hafta Sonu Zamanlaması

Bir görevin her **Cumartesi ve Pazar saat 10:00'da** çalışmasını planlamak için aşağıdaki ifadeyi kullanın:


- `0` → dakika (saat başı)  
- `10` → saat (saat 10:00)  
- `*` → ayın her günü  
- `*` → her ay  
- `sat,sun` → sadece Cumartesi ve Pazar günleri  

---

## Neden Crontab Kullanmalı?

- Standart günlük, haftalık veya aylık desenlerin ötesinde zamanlamalar oluşturun  
- Belirli günler, saatler veya aralıklar gibi hassas çalışma zamanları tanımlayın  
- Hafta sonu işler, mesai dışı kontroller veya sık izleme için kullanışlıdır  

---