---
title: Her Gün Çalıştırılan Bir Job Nasıl Oluşturulur
description: digna kullanarak dashboard üzerinden günlük bir inceleme job'ı nasıl zamanlanacağını öğrenin.
keywords: digna zamanlama, veri kalite otomasyonu, günlük job
---

# Günlük bir job nasıl zamanlanır

Zamanlama, denetimleri manuel müdahale olmadan otomatik olarak çalıştırmanızı sağlar.  
Bu kılavuzda, verilerinizin sürekli izlenmesini sağlamak için **günde bir kez** çalışan bir job'ın nasıl oluşturulacağını öğreneceksiniz.

---

## Etkileşimli Demo

Süreci uygulamalı olarak görmek için etkileşimli eğitimi izleyin:  

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/Ra9E19A0QfMpzKqm3Yhu?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a New Data Inspection Job" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Neler Öğreneceksiniz

- digna dashboard'taki **Scheduling** bölümüne nasıl erişileceği  
- Yeni bir zamanlanmış job nasıl oluşturulur  
- **günlük, sabit bir saatte** çalışacak şekilde nasıl yapılandırılacağı  
- Doğru proje ve datasource nasıl seçileceği  
- Job'ın otomatik olarak çalışması için nasıl etkinleştirileceği  

---

## Günlük Job'lar Neden Faydalıdır

Günlük zamanlama, üretim ortamlarında en yaygın kurulumdur. Şunları sağlar:  

- **Tazelik** — her günün verisi doğrulanır.  
- **Tutarlılık** — anormallikler, aşağı akışa yayılmadan önce erken tespit edilir.  
- **Otomasyon** — denetimleri elle tetiklemenize gerek kalmaz.  

---

## Sonraki Adımlar

- Daha gelişmiş özel zamanlamalar için [crontab tanımı nasıl kullanılır](how_to_use_crontab.md) bölümünü inceleyin.  
- Anormallikler tespit edildiğinde bildirim almak için günlük job'ları **alerting** ile birleştirin.