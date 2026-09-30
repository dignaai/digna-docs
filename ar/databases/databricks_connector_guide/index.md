# موصل المصدر لـ Databricks

يشرح هذا الدليل كيفية تهيئة *digna* للاتصال بـ Databricks عبر **ODBC**، باستخدام سلسلة اتصال **بدون DSN**.

جانب *digna* من الإعداد متطابق لكل التقنيات — أين تُنشأ الاتصالات، وكيف تُشفَّر قيم الخصائص، وكيف يُختبر الاتصال، وما معنى أوضاع التنميط (profiling). وهو موضح في [نظرة عامة على اتصالات قواعد البيانات](overview.md). تغطي هذه الصفحة ما هو خاص بـ Databricks.

!!! note "Unity Catalog مطلوب"

    يقرأ *digna* الكتالوجات المتاحة من `system.information_schema.catalogs`، لذا يجب أن تكون مساحة العمل مفعّلًا فيها Unity Catalog. كانت إصدارات *digna* السابقة تتيح تقنية منفصلة باسم "Databricks Legacy" لمساحات العمل التي لا تحتوي على Unity Catalog؛ ولم تعد متاحة.

---

## 1. تثبيت برنامج تشغيل ODBC {: #1-install-the-odbc-driver }

ثبّت **Databricks ODBC Driver** على الجهاز الذي يشغّل الواجهة الخلفية لـ *digna*، باتباع [دليل التثبيت من Databricks](https://docs.databricks.com/aws/en/integrations/odbc/).

بحسب الإصدار، يسجّل برنامج التشغيل نفسه باسم **Simba Spark ODBC Driver** أو باسم **Databricks ODBC Driver**. اقرأ الاسم المسجَّل بدقة على مضيفك كما هو موضح في [تثبيت برنامج تشغيل ODBC على مضيف digna](overview.md#install-the-driver).

---

## 2. جمع تفاصيل الاتصال {: #2-gather-the-connection-details }

تأتي جميع القيم من مستودع SQL (SQL warehouse) أو العنقود (cluster) الذي تريد أن يستخدمه *digna*. افتحه في مساحة عمل Databricks وانتقل إلى **Connection details**:

| حقل Databricks | يُستخدم كـ |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`، عادةً `443` |
| **HTTP path** | `HTTPPath` |

للمصادقة، أنشئ **رمز وصول شخصي** (personal access token) — انظر [Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat). تنتمي الرموز إلى مستخدم أو كيان خدمة (service principal)، ويحتاج هذا الكيان إلى الصلاحيات `USE CATALOG` و`USE SCHEMA` و`SELECT` على بيانات المصدر.

---

## 3. خصائص ODBC {: #3-odbc-properties }

!!! important "مثال، وليس مواصفة"

    المجموعة أدناه هي تركيبة واحدة معروف أنها تعمل. الخصائص تابعة لبرنامج تشغيل Databricks/Simba، لذا تختلف أسماؤها وقيمها الافتراضية والقيم المقبولة بين إصدارات برنامج التشغيل — فقد أُعيدت تسمية برنامج التشغيل ووُسّعت خيارات المصادقة فيه أكثر من مرة — وبين الأنظمة الأساسية. استخدم هذه المجموعة كنقطة بداية وراجع وثائق إصدار برنامج التشغيل الذي ثبّته.

أضف الخصائص التالية في شاشة **Add DB Connection**:

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | يجب أن يطابق اسم برنامج التشغيل المسجَّل على مضيف *digna* |
| `Host` | `<workspace>.cloud.databricks.com` | اسم مضيف الخادم للمستودع، مثل `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | مسار HTTP للمستودع أو العنقود |
| `SSL` | `1` | نقاط نهاية Databricks تعمل عبر TLS فقط |
| `ThriftTransport` | `2` | نقل HTTP، وهو ما تستخدمه نقاط نهاية SQL |
| `AuthMech` | `3` | المصادقة بالرمز |
| `UID` | `token` | الكلمة الحرفية `token`، وليس اسم مستخدم |
| `PWD` | `dapi…` | رمز الوصول الشخصي. فعّل **Encrypted** |
| `UseNativeQuery` | `1` | يمرّر SQL الخاص بـ *digna* دون تغيير — انظر أدناه |

تبدو سلسلة الاتصال الناتجة كما يلي:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "أبقِ `UseNativeQuery=1`"

    مع `UseNativeQuery=0` — وهي القيمة الافتراضية لبرنامج التشغيل — يعيد برنامج التشغيل كتابة SQL الوارد إلى ما يعتقد أنه صيغة ODBC قابلة للنقل. يولّد *digna* أصلًا SQL خاصًا بـ Databricks، لذا قد تغيّر إعادة الكتابة علامات الاقتباس المائلة (backtick) وقيم التواريخ الحرفية، فيفشل التنميط عندئذٍ على عبارات صحيحة كما هي مكتوبة.

### OAuth بدلًا من الرمز

لكيان خدمة يستخدم مصادقة OAuth من آلة إلى آلة، استبدل `AuthMech` و`UID` و`PWD` بما يلي:

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | بيانات اعتماد العميل (client credentials) |
| `Auth_Client_ID` | `<application id>` | كيان الخدمة |
| `Auth_Client_Secret` | `<client secret>` | فعّل **Encrypted** |

---

## 4. تهيئة *digna* {: #4-digna-configuration }

في شاشة **Add DB Connection**، قدّم ما يلي:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. ملاحظات حول Databricks {: #5-notes-on-databricks }

- **يجب أن يكون المستودع قيد التشغيل**، أو قادرًا على البدء، عندما يتصل *digna*. قد يستغرق المستودع الذي يُستأنف من حالة الإيقاف وقتًا أطول من مهلة الاتصال — إذا فشل الاختبار في المحاولة الأولى بعد فترة خمول، فأعد المحاولة.
- **تأتي الكتالوجات من مساحة العمل.** على عكس معظم التقنيات، يصل اتصال Databricks واحد إلى كل كتالوج مسموح للكيان برؤيته، لذا يمكن لاتصال واحد أن يخدم مصادر عبر عدة كتالوجات.
- **أوضاع التنميط.** ينشئ *Permanent* جداول العمل في **Work Schema** داخل كتالوج المصدر، لذا يحتاج الكيان إلى `CREATE TABLE` هناك. يستخدم *Session* الأمر `CREATE TEMPORARY TABLE` ولا يمسّ **Work Schema**. يحتاج *Standard* إلى صلاحية القراءة فقط.
- **المستودعات بلا خادم (serverless) تعمل** بالطريقة نفسها؛ يختلف `HTTPPath` فقط.

---

## 6. التحقق من برنامج التشغيل (اختياري) {: #6-verifying-the-driver-optional }

تهيئة مصدر بيانات ODBC ليست مطلوبة لاتصال بدون DSN، لكن نافذة برنامج التشغيل نفسه طريقة مريحة للتأكد من أن برنامج التشغيل والمستودع والرمز تعمل قبل إدخالها في *digna*.

#### الخطوة 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### الخطوة 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### الخطوة 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### الخطوة 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### الخطوة 5 – اختبار الاتصال

انقر الزر **TEST**. يجب أن يبدو الاتصال الناجح هكذا:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

المضيف ومسار HTTP والرمز التي تُدخلها هنا هي بالضبط القيم التي تأخذها الخصائص في [القسم 3](#3-odbc-properties).