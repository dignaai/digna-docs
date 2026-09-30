# موصل المصدر لـ Netezza

يشرح هذا الدليل كيفية تهيئة *digna* للاتصال بـ Netezza عبر **ODBC**، باستخدام سلسلة اتصال **بدون DSN**.

جانب *digna* من الإعداد متطابق لكل التقنيات — أين تُنشأ الاتصالات، وكيف تُشفَّر قيم الخصائص، وكيف يُختبر الاتصال، وما معنى أوضاع التنميط (profiling). وهو موضح في [نظرة عامة على اتصالات قواعد البيانات](overview.md). تغطي هذه الصفحة ما هو خاص بـ Netezza.

---

## 1. تثبيت برنامج تشغيل ODBC {: #1-install-the-odbc-driver }

ثبّت برنامج تشغيل ODBC **NetezzaSQL** (وهو جزء من أدوات عميل IBM Netezza) على الجهاز الذي يشغّل الواجهة الخلفية لـ *digna*، باتباع دليل التثبيت الرسمي من المورّد.

اقرأ اسم برنامج التشغيل المسجَّل بدقة على مضيفك كما هو موضح في [تثبيت برنامج تشغيل ODBC على مضيف digna](overview.md#install-the-driver).

---

## 2. خصائص ODBC {: #2-odbc-properties }

!!! important "مثال، وليس مواصفة"

    المجموعة أدناه هي تركيبة واحدة معروف أنها تعمل. الخصائص تابعة لبرنامج التشغيل NetezzaSQL، لذا تختلف أسماؤها وقيمها الافتراضية والقيم المقبولة بين إصدارات العميل والأنظمة الأساسية، ويحتاج الجهاز (appliance) المؤمَّن بـ TLS إلى أكثر من الخصائص المعروضة هنا. استخدم هذه المجموعة كنقطة بداية وراجع وثائق إصدار العميل الذي ثبّته.

أضف الخصائص التالية في شاشة **Add DB Connection**:

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | يجب أن يطابق اسم برنامج التشغيل المسجَّل على مضيف *digna*. الأقواس المعقوفة هي الطريقة المعتادة لكتابة هذا الاسم |
| `SERVER` | `netezza.example.com` | اسم الخادم أو عنوان IP |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | قاعدة البيانات التي تبدأ فيها الجلسة |
| `UID` | `ADMIN` | مستخدم قاعدة البيانات |
| `PWD` | `<password>` | فعّل **Encrypted** |

تبدو سلسلة الاتصال الناتجة كما يلي:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

بحسب إصدار برنامج التشغيل والإعداد ومتطلبات الأمان لديك، قد تلزم خصائص إضافية — على سبيل المثال `SecurityLevel` و`CaCertFile` لجهاز مؤمَّن بـ TLS. يمكن إضافة كل خيار تتيحه نوافذ *Advanced* و*SSL* و*Driver* في برنامج التشغيل كخاصية.

---

## 3. تهيئة *digna* {: #3-digna-configuration }

في شاشة **Add DB Connection**، قدّم ما يلي:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. ملاحظات حول Netezza {: #4-notes-on-netezza }

- **الكتالوجات والمخططات كلاهما معتمد.** يعرض *digna* قواعد البيانات التي يُسمح للمستخدم برؤيتها (من `_V_DATABASE`) ككتالوجات، ومخططاتها (من `_V_SCHEMA`) تحتها، لذا يمكن لاتصال واحد أن يخدم مصادر في أكثر من قاعدة بيانات. يحدد `DATABASE` فقط أين تبدأ الجلسة.
- **المعرّفات بأحرف كبيرة** ما لم تُنشأ بين علامات اقتباس، ولهذا تستخدم الأمثلة أعلاه `TEST` و`ADMIN`.
- **أوضاع التنميط.** ينشئ *Permanent* جداول العمل في **Work Schema**، لذا يحتاج المستخدم إلى `CREATE TABLE` هناك. يستخدم *Session* الأمر `CREATE TEMPORARY TABLE` ولا يمسّ **Work Schema**. يحتاج *Standard* إلى صلاحية القراءة فقط.

---

## 5. التحقق من برنامج التشغيل (اختياري) {: #5-verifying-the-driver-optional }

تهيئة مصدر بيانات ODBC ليست مطلوبة لاتصال بدون DSN، لكن نافذة برنامج التشغيل نفسه طريقة مريحة للتأكد من أن برنامج التشغيل وبيانات اعتمادك تعمل قبل إدخالها في *digna*.

#### الخطوة 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

الحقول في **DSN Options** تقابل الخصائص في [القسم 2](#2-odbc-properties) واحدًا لواحد. بحسب برنامج تشغيل Netezza والإعداد ومتطلبات الأمان لديك، قد تحتاج أيضًا إلى إدخال بيانات في علامات التبويب **Advanced DSN Options** أو **SSL DSN Options** أو **Driver Options**؛ أما لأبسط إعداد فتكفي **DSN Options**.

انقر الزر **Test Connection**.

#### الخطوة 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

عندما تظهر لك شاشة النجاح، يكون برنامج التشغيل يعمل والقيم صحيحة.