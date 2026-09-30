# موصل المصدر لـ Oracle

يشرح هذا الدليل كيفية تهيئة *digna* للاتصال بـ Oracle Database عبر **ODBC**، باستخدام سلسلة اتصال **بدون DSN**.

جانب *digna* من الإعداد متطابق لكل التقنيات — أين تُنشأ الاتصالات، وكيف تُشفَّر قيم الخصائص، وكيف يُختبر الاتصال، وما معنى أوضاع التنميط (profiling). وهو موضح في [نظرة عامة على اتصالات قواعد البيانات](overview.md). تغطي هذه الصفحة ما هو خاص بـ Oracle.

---

## 1. تثبيت برنامج تشغيل ODBC {: #1-install-the-odbc-driver }

برنامج تشغيل Oracle ODBC جزء من **Oracle Client** (تكفي حزمة "ODBC" من Instant Client). ثبّته على الجهاز الذي يشغّل الواجهة الخلفية لـ *digna*، باتباع دليل التثبيت الرسمي من المورّد.

يسجّل برنامج التشغيل نفسه باسم **Oracle in `<OracleHomeName>`** — على سبيل المثال `Oracle in OraDB21Home1` أو `Oracle in instantclient_21_13`. يختلف اسم الـ home من تثبيت لآخر، لذا اقرأ الاسم بدقة على مضيفك كما هو موضح في [تثبيت برنامج تشغيل ODBC على مضيف digna](overview.md#install-the-driver).

---

## 2. خصائص ODBC {: #2-odbc-properties }

!!! important "مثال، وليس مواصفة"

    المجموعة أدناه هي تركيبة واحدة معروف أنها تعمل. الخصائص تابعة لبرنامج تشغيل Oracle ODBC، لذا تختلف أسماؤها وقيمها الافتراضية والقيم المقبولة بين إصدارات العميل، ويعتمد اسم برنامج التشغيل بشكل خاص على Oracle home الموجود على مضيفك. استخدم هذه المجموعة كنقطة بداية وراجع وثائق إصدار العميل الذي ثبّته.

أضف الخصائص التالية في شاشة **Add DB Connection**:

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | يجب أن يطابق اسم برنامج التشغيل المسجَّل على مضيف *digna* |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | قاعدة البيانات المراد الاتصال بها — انظر أدناه |
| `UID` | `DIGNA_SOURCE_USER` | مستخدم قاعدة البيانات |
| `PWD` | `<password>` | فعّل **Encrypted** |

تبدو سلسلة الاتصال الناتجة كما يلي:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### قيمة `DBQ`

يقبل `DBQ` ثلاث صيغ. وهي متكافئة بالنسبة لـ *digna*؛ ويكمن الفرق بينها فيما يجب تهيئته على مضيف *digna*:

| الصيغة | مثال | المتطلبات |
|---|---|---|
| **واصف الاتصال الكامل** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | لا شيء — كل شيء موجود في الخاصية. موصى به |
| **اسم TNS مستعار** | `DIGNA_SOURCE` | يجب أن يوجد الاسم المستعار في ملف `tnsnames.ora` الخاص بـ Oracle Client على مضيف *digna* |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Oracle Client يدعم Easy Connect (الإصدار 12c وما بعده) |

!!! tip "فضّل الواصف الكامل"

    ينقل اسم TNS المستعار نصف تعريف الاتصال إلى ملف على مضيف *digna*، حيث يسهل نسيانه عند إعادة بناء المضيف أو نقل *digna*. أما الواصف الكامل فيُبقي الاتصال مكتفيًا بذاته — وهذا هو الهدف من الإعداد بدون DSN.

لاحظ أن الأقواس داخل الواصف لا تسبب مشكلة في سلسلة الاتصال، لكن إذا احتوت كلمة المرور على `;`، فضعها بين أقواس معقوفة: `PWD={p@ss;word}`.

---

## 3. تهيئة *digna* {: #3-digna-configuration }

في شاشة **Add DB Connection**، قدّم ما يلي:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. ملاحظات حول Oracle {: #4-notes-on-oracle }

- **المخططات هي المستخدمون.** يعرض *digna* مستخدمي Oracle كمخططات، لذا فإن مخطط المصدر هو مالك الجداول — `DIGNA_SOURCE_USER` في المثال أعلاه. يحتاج مستخدم الاتصال إلى `SELECT` على هذه الجداول، إما مباشرة أو عبر دور (role).
- **الاتصال الواحد يرى قاعدة بيانات واحدة.** الكتالوج الذي يعرضه *digna* هو قاعدة البيانات المرتبط بها الاتصال، لذا يحدد `DBQ` أي خدمة، وبالتالي أي قاعدة بيانات، يجري تنميطها.
- **المعرّفات حساسة لحالة الأحرف بمجرد وضعها بين علامات اقتباس.** يضع *digna* بين علامات اقتباس الأسماءَ التي يقرؤها من قاموس البيانات، وهي ما يخزّنه Oracle — أحرف كبيرة للكائنات غير المقتبسة.
- **أوضاع التنميط.** ينشئ *Permanent* جداول العمل في **Work Schema**، لذا يحتاج المستخدم إلى `CREATE TABLE` هناك وإلى حصة (quota) في مساحة الجداول (tablespace). يستخدم *Session* جدولًا مؤقتًا خاصًا (`ORA$PTT_…`، في Oracle 18c وما بعده) ولا يمسّ **Work Schema**. يحتاج *Standard* إلى صلاحية القراءة فقط.

---

## 5. التحقق من برنامج التشغيل (اختياري) {: #5-verifying-the-driver-optional }

تهيئة مصدر بيانات ODBC ليست مطلوبة لاتصال بدون DSN، لكن نافذة برنامج التشغيل نفسه طريقة مريحة للتأكد من أن Oracle Client واسم الخدمة وبيانات اعتمادك تعمل قبل إدخالها في *digna*.

#### الخطوة 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

يأتي **TNS Service Name** المعروض هنا من ملف `tnsnames.ora` في تثبيت Oracle Client لديك — فهناك يُعرَّف الاسم المستعار، ومعه المضيف والمنفذ واسم الخدمة. في *digna* يمكنك استخدام الاسم المستعار كقيمة لـ `DBQ`، أو استخدام الواصف الكامل بدلًا منه.

#### الخطوة 2 – اختبار الاتصال

انقر الزر **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

أدخل كلمة المرور وانقر الزر **OK**.

![Step 3](images/oracle/create_odbc_data_source_step3.png)

تؤكد رسالة النجاح أن برنامج التشغيل وبيانات الاعتماد تعمل.