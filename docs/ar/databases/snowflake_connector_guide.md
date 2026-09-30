---
title: موصل Snowflake – تكامل قاعدة البيانات | توثيق digna
description: قم بتهيئة digna للاتصال بـ Snowflake عبر ODBC باستخدام سلسلة اتصال بدون DSN. يغطي برنامج تشغيل Snowflake ODBC ورموز الوصول البرمجية واختيار المستودع والدور وإعدادات الاتصال في جانب digna.
image: /assets/logo_square.png
---


# موصل المصدر لـ Snowflake

يشرح هذا الدليل كيفية تهيئة *digna* للاتصال بـ Snowflake عبر **ODBC**، باستخدام سلسلة اتصال **بدون DSN**.

جانب *digna* من الإعداد متطابق لكل التقنيات — أين تُنشأ الاتصالات، وكيف تُشفَّر قيم الخصائص، وكيف يُختبر الاتصال، وما معنى أوضاع التنميط (profiling). وهو موضح في [نظرة عامة على اتصالات قواعد البيانات](overview.md). تغطي هذه الصفحة ما هو خاص بـ Snowflake.

---

## 1. تثبيت برنامج تشغيل ODBC {: #1-install-the-odbc-driver }

ثبّت **Snowflake ODBC Driver** على الجهاز الذي يشغّل الواجهة الخلفية لـ *digna*، باتباع [دليل التثبيت من Snowflake](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

يسجّل برنامج التشغيل نفسه باسم **SnowflakeDSIIDriver**. اقرأ الاسم المسجَّل بدقة على مضيفك كما هو موضح في [تثبيت برنامج تشغيل ODBC على مضيف digna](overview.md#install-the-driver).

---

## 2. خصائص ODBC {: #2-odbc-properties }

يتم الوصول إلى Snowflake باستخدام **رمز وصول برمجي (programmatic access token، PAT)** — وهو مسار المصادقة الذي جرى التحقق من *digna* عليه، والمسار الذي يشترطه Snowflake للحسابات التي يُحظر فيها تسجيل الدخول بكلمة المرور وحدها.

!!! important "مثال، وليس مواصفة"

    المجموعة أدناه هي تركيبة واحدة معروف أنها تعمل. الخصائص تابعة لبرنامج تشغيل Snowflake ODBC، لذا تختلف أسماؤها وقيمها الافتراضية والقيم المقبولة بين إصدارات برنامج التشغيل والأنظمة الأساسية، وخيارات المصادقة التي يسمح بها حسابك تحددها سياسة الأمان الخاصة بالحساب. استخدم هذه المجموعة كنقطة بداية وراجع وثائق إصدار برنامج التشغيل الذي ثبّته.

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | يجب أن يطابق اسم برنامج التشغيل المسجَّل على مضيف *digna* |
| `Server` | `<account>.snowflakecomputing.com` | معرّف الحساب مع اللاحقة، مثل `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | مستخدم Snowflake الذي ينتمي إليه الرمز |
| `Database` | `TEST` | قاعدة البيانات التي تحتوي على مخططات المصدر. وهي قاعدة البيانات الوحيدة التي يمكن لهذا الاتصال تنميطها |
| `Schema` | `PUBLIC` | المخطط الافتراضي للجلسة |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | يختار المصادقة بالرمز |
| `token` | `<programmatic access token>` | فعّل **Encrypted** |

تبدو سلسلة الاتصال الناتجة كما يلي:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### المستودع والدور

تحتاج الاستعلامات إلى مستودع (warehouse). إذا كان لمستخدم *digna* مستودع افتراضي ودور افتراضي، فإن الجلسة تلتقطهما ولا حاجة إلى أي تهيئة. وإلا فأضف:

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | المستودع الذي ينفّذ استعلامات التنميط |
| `Role` | `DIGNA_READER` | الدور الذي تستخدم الجلسة صلاحياته |

!!! tip "خصّص لـ digna مستودعًا خاصًا به"

    يُبقي مستودع منفصل وصغير يتوقف تلقائيًا تكلفةَ التنميط واضحة، ويمنع *digna* من منافسة المستخدمين التفاعليين على موارد الحوسبة.

### المصادقة بكلمة المرور

حيثما لا يزال الحساب يسمح بذلك، تعمل كلمة المرور بدلًا من الرمز — احذف `authenticator` و`token` وأضف:

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `PWD` | `<password>` | فعّل **Encrypted** |

---

## 3. تهيئة *digna* {: #3-digna-configuration }

في شاشة **Add DB Connection**، قدّم ما يلي:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. ملاحظات حول Snowflake {: #4-notes-on-snowflake }

- **تنتهي صلاحية الرموز.** يُصدر رمز الوصول البرمجي بمدة صلاحية، ويتوقف التنميط في اليوم الذي تنتهي فيه. دوّن تاريخ الانتهاء عند إنشائه، وأعد إدخال الرمز الجديد في الخاصية `token` — يمكن استبدال القيم المشفرة لكن لا يمكن قراءتها مجددًا.
- **الاتصال الواحد يرى قاعدة بيانات واحدة.** يعرض *digna* مخططات قاعدة البيانات المسماة في `Database`، لأن Snowflake يُبلغ عن قاعدة البيانات الحالية فقط ككتالوج. جداول المصدر الموجودة في قاعدة بيانات أخرى تحتاج إلى اتصال خاص بها.
- **المعرّفات بأحرف كبيرة** ما لم تُنشأ بين علامات اقتباس. يستخدم *digna* الأسماء كما يُبلغ عنها Snowflake.
- **أوضاع التنميط.** ينشئ *Permanent* جداول العمل في **Work Schema**، لذا يحتاج الدور إلى `CREATE TABLE` هناك. يستخدم *Session* الأمر `CREATE TEMPORARY TABLE` ولا يمسّ **Work Schema**. يحتاج *Standard* إلى صلاحية القراءة فقط — ولا يحتاج إلى أي صلاحيات كتابة على الإطلاق.

---

## 5. التحقق من برنامج التشغيل (اختياري) {: #5-verifying-the-driver-optional }

تهيئة مصدر بيانات ODBC ليست مطلوبة لاتصال بدون DSN، لكن نافذة برنامج التشغيل نفسه طريقة مريحة للتأكد من أن برنامج التشغيل وعنوان URL للحساب وبيانات اعتمادك تعمل قبل إدخالها في *digna*.

#### الخطوة 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

ملاحظات:

- تتكون قيمة **Server** من معرّف حساب Snowflake الخاص بك متبوعًا بـ `.snowflakecomputing.com`.
- القيم **Database** و**Schema** و**Warehouse** المُدخلة هنا تقابل الخصائص `Database` و`Schema` و`Warehouse` في [القسم 2](#2-odbc-properties).

#### الخطوة 2 – اختبار الاتصال

انقر الزر **TEST**. يجب أن يبدو الاتصال الناجح هكذا:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)
