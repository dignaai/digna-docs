---
title: موصل Teradata – تكامل قاعدة البيانات | توثيق digna
description: قم بتهيئة digna للاتصال بـ Teradata عبر ODBC باستخدام سلسلة اتصال بدون DSN. يغطي برنامج تشغيل Teradata ODBC والخاصية DBCNAME وآليات تسجيل الدخول وإعدادات الاتصال في جانب digna.
image: /assets/logo_square.png
---


# موصل المصدر لـ Teradata

يشرح هذا الدليل كيفية تهيئة *digna* للاتصال بـ Teradata عبر **ODBC**، باستخدام سلسلة اتصال **بدون DSN**.

جانب *digna* من الإعداد متطابق لكل التقنيات — أين تُنشأ الاتصالات، وكيف تُشفَّر قيم الخصائص، وكيف يُختبر الاتصال، وما معنى أوضاع التنميط (profiling). وهو موضح في [نظرة عامة على اتصالات قواعد البيانات](overview.md). تغطي هذه الصفحة ما هو خاص بـ Teradata.

---

## 1. تثبيت برنامج تشغيل ODBC {: #1-install-the-odbc-driver }

ثبّت **ODBC Driver for Teradata** على الجهاز الذي يشغّل الواجهة الخلفية لـ *digna*، باتباع دليل التثبيت الرسمي من المورّد.

يسجّل برنامج التشغيل نفسه مع رقم الإصدار في اسمه، على سبيل المثال **Teradata Database ODBC Driver 20.00**. اقرأ الاسم المسجَّل بدقة على مضيفك كما هو موضح في [تثبيت برنامج تشغيل ODBC على مضيف digna](overview.md#install-the-driver).

---

## 2. خصائص ODBC {: #2-odbc-properties }

!!! important "مثال، وليس مواصفة"

    المجموعة أدناه هي تركيبة واحدة معروف أنها تعمل. الخصائص تابعة لبرنامج تشغيل Teradata ODBC، لذا تختلف أسماؤها وقيمها الافتراضية والقيم المقبولة بين إصدارات برنامج التشغيل — فالإصدار جزء من اسم برنامج التشغيل نفسه — وبين الأنظمة الأساسية. استخدم هذه المجموعة كنقطة بداية وراجع وثائق إصدار برنامج التشغيل الذي ثبّته.

أضف الخصائص التالية في شاشة **Add DB Connection**:

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | يجب أن يطابق اسم برنامج التشغيل المسجَّل على مضيف *digna* |
| `DBCNAME` | `teradata.example.com` | اسم الخادم أو عنوان IP. وهو الاسم الذي يستخدمه Teradata لخاصية المضيف |
| `UID` | `digna_source_user` | مستخدم قاعدة البيانات |
| `PWD` | `<password>` | فعّل **Encrypted** |

تبدو سلسلة الاتصال الناتجة كما يلي:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

خصائص إضافية مفيدة:

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `MechanismName` | `TD2` | آلية تسجيل الدخول. `TD2` هي الافتراضية في Teradata؛ استخدم `LDAP` للمصادقة عبر الدليل (directory) |
| `DefaultDatabase` | `dad` | قاعدة البيانات التي تبدأ فيها الجلسة |
| `CharacterSet` | `UTF8` | اضبطها حيث قد تُفسد مجموعة أحرف الجلسة الافتراضية البيانات غير ASCII |

---

## 3. تهيئة *digna* {: #3-digna-configuration }

في شاشة **Add DB Connection**، قدّم ما يلي:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. ملاحظات حول Teradata {: #4-notes-on-teradata }

- **قاعدة بيانات Teradata هي كتالوج، وليست مخططًا.** يعرض *digna* قواعد البيانات التي يُسمح للمستخدم برؤيتها (من `DBC.DatabasesV`) ككتالوجات، ولا ينطبق مستوى المخطط. عند إضافة مصدر بيانات، اختر قاعدة البيانات ككتالوج؛ ويُعرض المخطط على أنه *غير منطبق* (not applicable).
- **يصل الاتصال الواحد إلى كل قاعدة بيانات مسموح بها**، لذا يمكن لاتصال واحد أن يخدم مصادر عبر عدة قواعد بيانات — على عكس التقنيات التي يكون فيها الاتصال مثبّتًا على قاعدة بيانات واحدة.
- **Work Schema هو قاعدة بيانات.** للتنميط *Permanent*، حدّد قاعدة بيانات Teradata التي تحتوي على جداول العمل، وامنح المستخدم صلاحيات `CREATE TABLE` إضافةً إلى تخصيص مساحة `PERM` فيها — فقاعدة البيانات ذات مساحة perm صفرية لا يمكنها استيعاب جدول.
- **أوضاع التنميط.** ينشئ *Permanent* الجداول في **Work Schema**. يستخدم *Session* جدولًا من نوع `VOLATILE`، يحتاج إلى مساحة `SPOOL` لكنه لا يحتاج إلى مساحة perm ولا إلى أي صلاحيات في **Work Schema**. يحتاج *Standard* إلى صلاحية القراءة فقط.

---

## 5. التحقق من برنامج التشغيل (اختياري) {: #5-verifying-the-driver-optional }

تهيئة مصدر بيانات ODBC ليست مطلوبة لاتصال بدون DSN، لكن نافذة برنامج التشغيل نفسه طريقة مريحة للتأكد من أن برنامج التشغيل وبيانات اعتمادك تعمل قبل إدخالها في *digna*.

#### الخطوة 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

الحقل **Name or IP address** هنا هو الخاصية `DBCNAME` في [القسم 2](#2-odbc-properties).

انقر الزر **Test**.

#### الخطوة 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

أدخل اسم المستخدم وكلمة المرور، ثم انقر الزر **OK**. تؤكد شاشة النجاح أن برنامج التشغيل وبيانات الاعتماد تعمل.
