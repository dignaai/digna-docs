# الجدولة المتقدمة باستخدام Crontab

يُظهر هذا الدليل كيفية جدولة المهام في *digna* باستخدام **تعابير crontab**.  
بخلاف الأنماط القياسية (يوميًا، أسبوعيًا، شهريًا)، تمنحك crontab مرونة كاملة لتحديد جداول مخصّصة.

---

## العرض التفاعلي

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## ما الذي ستتعلمه

- كيفية فتح قسم **Scheduling** في dashboard  
- كيفية إنشاء مهمة جديدة باستخدام **تعبير crontab**  
- كيفية ضبط جدول يعمل فقط في **عطلات نهاية الأسبوع في الساعة 10:00**  

---

## مثال: جدول نهاية الأسبوع

لجدولة مهمة للتشغيل كل **السبت والأحد في الساعة 10:00 صباحًا**، استخدم التعبير التالي:


- `0` → الدقيقة (في بداية الساعة)  
- `10` → الساعة (10 صباحًا)  
- `*` → كل يوم من أيام الشهر  
- `*` → كل شهر  
- `sat,sun` → فقط في أيام السبت والأحد  

---

## لماذا تستخدم Crontab؟

- إنشاء جداول تتجاوز الأنماط القياسية اليومية أو الأسبوعية أو الشهرية  
- تحديد أوقات تشغيل دقيقة (أيام محددة، ساعات، أو فواصل زمنية)  
- مفيدة للمهام في عطلات نهاية الأسبوع، أو عمليات الفحص خارج ساعات العمل، أو المراقبة المتكررة  

---