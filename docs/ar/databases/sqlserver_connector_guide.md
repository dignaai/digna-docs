---
title: موصل MS SQL Server – تكامل قاعدة البيانات | توثيق digna
description: قم بتهيئة digna للاتصال بـ Microsoft SQL Server عبر ODBC باستخدام سلسلة اتصال بدون DSN. يغطي برنامج تشغيل Microsoft ODBC وخصائص ODBC المطلوبة وإعدادات التشفير وإعدادات الاتصال في جانب digna.
image: /assets/logo_square.png
---


# موصل المصدر لـ MS SQL Server

يشرح هذا الدليل كيفية تهيئة *digna* للاتصال بـ Microsoft SQL Server عبر **ODBC**، باستخدام سلسلة اتصال **بدون DSN**.

جانب *digna* من الإعداد متطابق لكل التقنيات — أين تُنشأ الاتصالات، وكيف تُشفَّر قيم الخصائص، وكيف يُختبر الاتصال، وما معنى أوضاع التنميط (profiling). وهو موضح في [نظرة عامة على اتصالات قواعد البيانات](overview.md). تغطي هذه الصفحة ما هو خاص بـ SQL Server.

!!! note "Azure Synapse Analytics"

    يُهيَّأ Synapse أيضًا كاتصال SQL Server، مع اسم مضيف مختلف وبعض الاعتبارات الإضافية — انظر [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. تثبيت برنامج تشغيل ODBC {: #1-install-the-odbc-driver }

ثبّت **ODBC Driver 18 for SQL Server** على الجهاز الذي يشغّل الواجهة الخلفية لـ *digna*، باتباع [دليل التثبيت من Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

برنامج التشغيل المرفق مع Windows تحت الاسم البسيط **SQL Server** يعمل أيضًا، لكنه قديم منذ زمن طويل ولا يدعم إعدادات TLS الحديثة ولا مصادقة Azure. استخدمه فقط حيث لا يكون تثبيت برنامج التشغيل الحالي ممكنًا.

اقرأ اسم برنامج التشغيل المسجَّل بدقة على مضيفك كما هو موضح في [تثبيت برنامج تشغيل ODBC على مضيف digna](overview.md#install-the-driver).

---

## 2. خصائص ODBC {: #2-odbc-properties }

!!! important "مثال، وليس مواصفة"

    المجموعة أدناه هي تركيبة واحدة معروف أنها تعمل. الخصائص تابعة لبرنامج تشغيل Microsoft ODBC، لذا تختلف أسماؤها وقيمها الافتراضية والقيم المقبولة بين إصدارات برنامج التشغيل — فمثلًا يشفّر Driver 18 افتراضيًا بينما لم يكن Driver 17 يفعل ذلك — وبين الأنظمة الأساسية. استخدم هذه المجموعة كنقطة بداية وراجع وثائق إصدار برنامج التشغيل الذي ثبّته.

أضف الخصائص التالية في شاشة **Add DB Connection**:

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | يجب أن يطابق اسم برنامج التشغيل المسجَّل على مضيف *digna* |
| `SERVER` | `sql.example.com` | اسم الخادم أو عنوان IP. للمثيلات المسماة: `host\instance`؛ لمنفذ غير افتراضي: `host,1433` |
| `PORT` | `1433` | احذفه عندما يكون المنفذ جزءًا من `SERVER` بالفعل |
| `DATABASE` | `digna_source_db` | قاعدة البيانات التي تحتوي على مخططات المصدر. وهي قاعدة البيانات الوحيدة التي يمكن لهذا الاتصال تنميطها |
| `UID` | `digna_source_user` | مستخدم قاعدة البيانات |
| `PWD` | `<password>` | فعّل **Encrypted** |

تبدو سلسلة الاتصال الناتجة كما يلي:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### التشفير مع ODBC Driver 18

يشفّر Driver 18 الاتصالات افتراضيًا ويتحقق من شهادة الخادم. مع خادم يستخدم شهادة لا يثق بها مضيف *digna* — شهادة موقّعة ذاتيًا في الغالب — يفشل الاتصال بخطأ في سلسلة الشهادات. أضف:

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `Encrypt` | `yes` | الافتراضي في Driver 18؛ اضبطه على `no` فقط إذا كان الخادم لا يدعم TLS |
| `TrustServerCertificate` | `yes` | يتخطى التحقق من الشهادة. مريح في بيئات الاختبار؛ أما في الإنتاج فالأفضل تثبيت الشهادة |

### مصادقة Windows

للاتصال بالحساب الذي يشغّل خدمة *digna* بدلًا من تسجيل دخول SQL، احذف `UID` و`PWD` وأضف:

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `Trusted_Connection` | `yes` | يحتاج حساب خدمة *digna* إلى صلاحيات قاعدة البيانات |

---

## 3. تهيئة *digna* {: #3-digna-configuration }

في شاشة **Add DB Connection**، قدّم ما يلي:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. ملاحظات حول MS SQL Server {: #4-notes-on-ms-sql-server }

- **الاتصال الواحد يرى قاعدة بيانات واحدة.** يعرض *digna* مخططات قاعدة البيانات المسماة في `DATABASE`، لأن SQL Server يُبلغ عن قاعدة البيانات الحالية فقط ككتالوج. جداول المصدر الموجودة في قاعدة بيانات أخرى تحتاج إلى اتصال خاص بها.
- **أوضاع التنميط.** ينشئ *Permanent* جداول العمل في **Work Schema**، لذا يحتاج المستخدم إلى `CREATE TABLE` هناك. يستخدم *Session* جداول مؤقتة محلية (`#wt_…`) في `tempdb` ولا يمسّ **Work Schema**. يحتاج *Standard* إلى صلاحية القراءة فقط.
- **يحمل `SERVER` المثيل والمنفذ.** مع مثيل مسمى، يتطلب `host\instance` أن تكون خدمة SQL Server Browser قابلة للوصول؛ أما `host,port` فيتجنب ذلك.

---

## 5. التحقق من برنامج التشغيل (اختياري) {: #5-verifying-the-driver-optional }

تهيئة مصدر بيانات ODBC ليست مطلوبة لاتصال بدون DSN، لكن معالج برنامج التشغيل نفسه طريقة مريحة للتأكد من أن برنامج التشغيل يعمل وأن الخادم يقبل بيانات اعتمادك قبل إدخالها في *digna*.

#### الخطوة 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

انقر الزر **Next >**.

#### الخطوة 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

اختر طريقة المصادقة (مثل اسم المستخدم وكلمة المرور) وقدّم البيانات المطلوبة.

انقر الزر **Next >**.

#### الخطوة 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

اختر الإعدادات المتوافقة مع ANSI ثم انقر الزر **Next >**.

#### الخطوة 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

يمكنك ترك الإعدادات الافتراضية أو اختيار خيارات التسجيل (logging) حسب الحاجة، ثم انقر الزر **Finish**.

#### الخطوة 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

الآن انقر الزر **Test datasource**.

#### الخطوة 6
![Step 6](images/sqlserver/create_odbc_data_source_step6.png)

تؤكد شاشة النجاح أن برنامج التشغيل وبيانات الاعتماد تعمل. القيم التي أدخلتها هي بالضبط القيم التي تأخذها الخصائص في [القسم 2](#2-odbc-properties).
