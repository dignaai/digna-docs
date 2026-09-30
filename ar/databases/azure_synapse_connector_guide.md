# موصل المصدر لـ Azure Synapse Analytics

يشرح هذا الدليل كيفية تهيئة *digna* للاتصال بـ Azure Synapse Analytics عبر **ODBC**، باستخدام سلسلة اتصال **بدون DSN**. يدعم كلٌّ من مجمّعات SQL بلا خادم (serverless) ومجمّعات SQL المخصصة (dedicated).

جانب *digna* من الإعداد متطابق لكل التقنيات — أين تُنشأ الاتصالات، وكيف تُشفَّر قيم الخصائص، وكيف يُختبر الاتصال، وما معنى أوضاع التنميط (profiling). وهو موضح في [نظرة عامة على اتصالات قواعد البيانات](overview.md). تغطي هذه الصفحة ما هو خاص بـ Azure Synapse.

!!! note "التقنية"

    يستخدم Synapse لهجة SQL Server، لذا يُنشأ الاتصال باختيار **Technology: SQL Server**. انظر [MS SQL Server](sqlserver_connector_guide.md) للخادم المحلي (on-premises).

---

## 1. تثبيت برنامج تشغيل ODBC {: #1-install-the-odbc-driver }

ثبّت **ODBC Driver 18 for SQL Server** على الجهاز الذي يشغّل الواجهة الخلفية لـ *digna*، باتباع [دليل التثبيت من Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)، ثم اقرأ اسم برنامج التشغيل المسجَّل بدقة على مضيفك كما هو موضح في [تثبيت برنامج تشغيل ODBC على مضيف digna](overview.md#install-the-driver).

---

## 2. خصائص ODBC {: #2-odbc-properties }

!!! important "مثال، وليس مواصفة"

    المجموعة أدناه هي تركيبة واحدة معروف أنها تعمل. الخصائص تابعة لبرنامج تشغيل ODBC من Microsoft، لذا تختلف أسماؤها وقيمها الافتراضية والقيم المقبولة بين إصدارات برنامج التشغيل والأنظمة الأساسية، وما تتطلبه مساحة العمل يعتمد على كيفية تهيئتها — نوع المجمّع، وطريقة المصادقة، والجدار الناري. استخدم هذه المجموعة كنقطة بداية وراجع وثائق إصدار برنامج التشغيل الذي ثبّته.

أضف الخصائص التالية في شاشة **Add DB Connection**:

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | يجب أن يطابق اسم برنامج التشغيل المسجَّل على مضيف *digna* |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | اسم مساحة العمل مع لاحقة نقطة النهاية — انظر أدناه |
| `DATABASE` | `dignadata` | قاعدة البيانات التي تحتوي على مخططات المصدر. وهي قاعدة البيانات الوحيدة التي يمكن لهذا الاتصال تنميطها |
| `UID` | `sqladminuser` | تسجيل دخول SQL |
| `PWD` | `<password>` | فعّل **Encrypted** |

تبدو سلسلة الاتصال الناتجة كما يلي:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### قيمة `SERVER`

خذ اسم مساحة عمل Synapse وأضف إليه لاحقة نقطة النهاية:

| المجمّع | `SERVER` |
|---|---|
| **مجمّع SQL بلا خادم (serverless)** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **مجمّع SQL مخصص (dedicated)** | `<workspace>.sql.azuresynapse.net` |

!!! warning "من السهل إغفال الجزء `-ondemand`"

    بدونه يُحَلّ الاسم إلى نقطة النهاية المخصصة، فإما أن يفشل الاتصال أو يصل بصمت إلى مجمّع غير المقصود. تظهر نقطتا النهاية كلتاهما في صفحة النظرة العامة لمساحة العمل في مدخل Azure.

### الجدار الناري

يجب أن يسمح جدار الحماية لمساحة عمل Synapse بالعنوان الصادر لمضيف *digna*. أضفه تحت **Networking** في مساحة العمل قبل اختبار الاتصال — يظهر العنوان المحظور على شكل انتهاء مهلة الاتصال وليس خطأ مصادقة.

### مصادقة Microsoft Entra ID

بدلًا من تسجيل دخول SQL، يمكن لبرنامج التشغيل المصادقة عبر Entra ID. استبدل `UID`/`PWD` بطريقة المصادقة التي تتوقعها مساحة العمل، على سبيل المثال:

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | عندها يأخذ `UID` معرّف التطبيق (العميل) ويأخذ `PWD` سر العميل |
| `Authentication` | `ActiveDirectoryMSI` | الهوية المُدارة لمضيف *digna*، دون الحاجة إلى بيانات اعتماد |

---

## 3. تهيئة *digna* {: #3-digna-configuration }

في شاشة **Add DB Connection**، قدّم ما يلي:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. ملاحظات حول Azure Synapse {: #4-notes-on-azure-synapse }

- **المجمّعات بلا خادم تدعم التنميط *Standard* فقط.** لا يستطيع مجمّع SQL بلا خادم إنشاء جداول في قاعدة بيانات، لذا لا يمكن تشغيل التنميط *Permanent* ولا *Session*. يحسب *Standard* المقاييس مباشرة على المصدر، وهو أيضًا الخيار الأرخص، لأن المجمّعات بلا خادم تُحتسب تكلفتها حسب حجم البيانات المعالجة.
- **الاتصال الواحد يرى قاعدة بيانات واحدة.** يعرض *digna* مخططات قاعدة البيانات المسماة في `DATABASE`، لأن Synapse، مثل SQL Server، يُبلغ عن قاعدة البيانات الحالية فقط ككتالوج.
- **التشفير مفعّل افتراضيًا** في Driver 18، وتقدّم نقاط نهاية Synapse شهادات عامة صالحة، لذا لا حاجة إلى الخاصية `Encrypt` أو `TrustServerCertificate`.
- **قد تستأنف نقطة النهاية بلا خادم عملها من حالة الخمول** عند أول اتصال. إذا انتهت مهلة اختبار الاتصال على مجمّع لم يُستخدم منذ فترة، فأعد المحاولة.

---

## 5. التحقق من برنامج التشغيل (اختياري) {: #5-verifying-the-driver-optional }

تهيئة مصدر بيانات ODBC ليست مطلوبة لاتصال بدون DSN، لكن معالج برنامج التشغيل نفسه طريقة مريحة للتأكد من أن برنامج التشغيل يعمل وأن مساحة العمل تقبل بيانات اعتمادك قبل إدخالها في *digna*.

#### الخطوة 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

املأ الحقل "Server".
استخدم اسم مساحة عمل Synapse وأضف إليه ".sql.azuresynapse.net".  
**تنبيه**: إذا أردت الاتصال باستخدام مجمّع SQL بلا خادم، فتأكد من تضمين "-ondemand" كما هو موضح في لقطة الشاشة أعلاه.

انقر الزر **Next >**.

#### الخطوة 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

اختر طريقة المصادقة (مثل اسم المستخدم وكلمة المرور) وقدّم البيانات المطلوبة.

انقر الزر **Next >**.

#### الخطوة 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

اختر الإعدادات المتوافقة مع ANSI ثم انقر الزر **Next >**.

#### الخطوة 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

يمكنك ترك الإعدادات الافتراضية أو اختيار الخيارات حسب الحاجة، ثم انقر الزر **Finish**.

#### الخطوة 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

الآن انقر الزر **Test datasource**.

#### الخطوة 6
![Step 6](images/azure_synapse/create_odbc_data_source_step6.png)

تؤكد شاشة النجاح أن برنامج التشغيل ونقطة النهاية وبيانات الاعتماد تعمل. القيم التي أدخلتها هي بالضبط القيم التي تأخذها الخصائص في [القسم 2](#2-odbc-properties).