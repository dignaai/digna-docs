---
title: ربط قاعدة بيانات | توثيق digna
description: دليل خطوة بخطوة لربط قاعدة بيانات بمشروع موجود في digna. تعلّم كيفية تكوين الاتصالات، إدخال بيانات الاعتماد، وتمكين الوصول الآمن.
---

# ربط قاعدة بيانات

يُبيّن هذا الدليل الحد الأدنى من الخطوات لإضافة اتصال قاعدة بيانات إلى مشروعك.

## العرض التفاعلي

<!--ARCADE EMBED START-->
<div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;">
  <iframe
    src="https://demo.arcade.software/NhlhDLqeW9wC5zaLlYPa?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true"
    title="ربط قاعدة بيانات بمشروع"
    frameborder="0"
    loading="lazy"
    webkitallowfullscreen
    mozallowfullscreen
    allowfullscreen
    allow="clipboard-write"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;">
  </iframe>
</div>
<!--ARCADE EMBED END-->

---

### الخطوات

1. **افتح مشروعك**  
   من قائمة التنقل اليسرى، انقر على **Projects** واختر المشروع المستهدف.

2. **أضف اتصالًا**  
   اذهب إلى **Connections** وانقر على **Add Connection**.

3. **اختر نوع قاعدة البيانات**  
   اختر قاعدة البيانات التي تريد الاتصال بها (مثل: PostgreSQL، MySQL، SQL Server، Oracle، Snowflake، Teradata).

4. **أدخل تفاصيل الاتصال**  
   قدّم **Name**، **Host**، **Port**، **Database/Service**، و**Credentials** (اسم المستخدم/كلمة المرور أو SSO، حسب الاقتضاء).

5. **اختبار وحفظ**  
   انقر على **Test**. إذا نجح الاختبار، انقر على **Save**. سيظهر الاتصال تحت **Connections** للمشروع.