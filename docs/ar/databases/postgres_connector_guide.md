---
title: موصل PostgreSQL – تكامل قاعدة البيانات | توثيق digna
description: قم بتهيئة digna للاتصال بـ PostgreSQL عبر ODBC باستخدام سلسلة اتصال بدون DSN. يغطي برنامج التشغيل psqlODBC وخصائص ODBC المطلوبة وأوضاع SSL وإعدادات الاتصال في جانب digna.
image: /assets/logo_square.png
---


# موصل المصدر لـ PostgreSQL

يشرح هذا الدليل كيفية تهيئة *digna* للاتصال بـ PostgreSQL عبر **ODBC**، باستخدام سلسلة اتصال **بدون DSN**.

جانب *digna* من الإعداد متطابق لكل التقنيات — أين تُنشأ الاتصالات، وكيف تُشفَّر قيم الخصائص، وكيف يُختبر الاتصال، وما معنى أوضاع التنميط (profiling). وهو موضح في [نظرة عامة على اتصالات قواعد البيانات](overview.md). تغطي هذه الصفحة ما هو خاص بـ PostgreSQL.

---

## 1. تثبيت برنامج تشغيل ODBC {: #1-install-the-odbc-driver }

ثبّت برنامج تشغيل PostgreSQL ODBC (**psqlODBC**) على الجهاز الذي يشغّل الواجهة الخلفية لـ *digna*، باتباع دليل التثبيت الرسمي من المورّد.

يسجّل برنامج التشغيل نفسه تحت اسم يختلف حسب النظام الأساسي والحزمة — عادةً **PostgreSQL Unicode(x64)** على Windows و**PostgreSQL ODBC Driver(UNICODE)** على Linux. اقرأ الاسم بدقة على مضيفك كما هو موضح في [تثبيت برنامج تشغيل ODBC على مضيف digna](overview.md#install-the-driver)، واستخدم هذا الاسم للخاصية `DRIVER` أدناه.

---

## 2. خصائص ODBC {: #2-odbc-properties }

!!! important "مثال، وليس مواصفة"

    المجموعة أدناه هي تركيبة واحدة معروف أنها تعمل. الخصائص تابعة لبرنامج التشغيل psqlODBC، لذا تختلف أسماؤها وقيمها الافتراضية والقيم المقبولة بين إصدارات برنامج التشغيل والأنظمة الأساسية، وقد يختلف أيضًا ما يتطلبه خادمك — ولا سيما SSL. استخدم هذه المجموعة كنقطة بداية وراجع وثائق إصدار برنامج التشغيل الذي ثبّته.

أضف الخصائص التالية في شاشة **Add DB Connection**:

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | يجب أن يطابق اسم برنامج التشغيل المسجَّل على مضيف *digna* |
| `SERVER` | `db.example.com` | اسم الخادم أو عنوان IP |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | قاعدة البيانات التي تحتوي على مخططات المصدر. وهي قاعدة البيانات الوحيدة التي يمكن لهذا الاتصال تنميطها |
| `UID` | `digna_source_user` | مستخدم قاعدة البيانات |
| `PWD` | `<password>` | فعّل **Encrypted** |
| `SSLMode` | `prefer` | `disable` أو `allow` أو `prefer` أو `require` أو `verify-ca` أو `verify-full` — يجب أن يقبلها الخادم |

تبدو سلسلة الاتصال الناتجة كما يلي:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

يمكن إضافة أي خيار آخر من خيارات psqlODBC كخاصية إضافية — على سبيل المثال `ReadOnly=1` لجلسة للقراءة فقط، أو `ConnSettings` لتنفيذ عبارات `SET` عند الاتصال.

---

## 3. تهيئة *digna* {: #3-digna-configuration }

في شاشة **Add DB Connection**، قدّم ما يلي:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. ملاحظات حول PostgreSQL {: #4-notes-on-postgresql }

- **يجب أن يطابق `SSLMode` الخادم.** يرفض الخادم المهيأ بـ `hostssl` القيمة `SSLMode=disable`، وتحتاج `verify-ca` أو `verify-full` أيضًا إلى أن تكون شهادة الجذر متاحة لبرنامج التشغيل على مضيف *digna*. إذا اضطررت إلى اختيار وضع معين عند اختبار برنامج التشغيل، فاستخدم الوضع نفسه هنا.
- **الاتصال الواحد يرى قاعدة بيانات واحدة.** يعرض *digna* مخططات قاعدة البيانات المسماة في `DATABASE`، لأن PostgreSQL يُبلغ عن قاعدة البيانات الحالية فقط ككتالوج. جداول المصدر الموجودة في قاعدة بيانات أخرى تحتاج إلى اتصال خاص بها.
- **أوضاع التنميط.** ينشئ *Permanent* جداول العمل في **Work Schema**، لذا يحتاج المستخدم إلى `CREATE` على ذلك المخطط. يستخدم *Session* الأمر `CREATE TEMPORARY TABLE` ولا يمسّ **Work Schema**. يحتاج *Standard* إلى صلاحية القراءة فقط.

---

## 5. التحقق من برنامج التشغيل (اختياري) {: #5-verifying-the-driver-optional }

تهيئة مصدر بيانات ODBC ليست مطلوبة لاتصال بدون DSN، لكن نافذة برنامج التشغيل نفسه طريقة مريحة للتأكد من أن برنامج التشغيل يعمل وأن الخادم يقبل بيانات اعتمادك ووضع SSL قبل إدخالها في *digna*.

#### الخطوة 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

#### الخطوة 2 – اختبار الاتصال

انقر الزر **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

القيم التي أدخلتها هنا هي بالضبط القيم التي تأخذها الخصائص في [القسم 2](#2-odbc-properties).
