# موصل المصدر لـ Hive

يشرح هذا الدليل كيفية تهيئة *digna* للاتصال بـ Apache Hive عبر **ODBC**، باستخدام سلسلة اتصال **بدون DSN**.

جانب *digna* من الإعداد متطابق لكل التقنيات — أين تُنشأ الاتصالات، وكيف تُشفَّر قيم الخصائص، وكيف يُختبر الاتصال، وما معنى أوضاع التنميط (profiling). وهو موضح في [نظرة عامة على اتصالات قواعد البيانات](overview.md). تغطي هذه الصفحة ما هو خاص بـ Hive.

---

## 1. تثبيت برنامج تشغيل ODBC {: #1-install-the-odbc-driver }

ثبّت **Cloudera ODBC Driver for Apache Hive** على الجهاز الذي يشغّل الواجهة الخلفية لـ *digna*، باتباع دليل التثبيت الرسمي من المورّد.

اقرأ اسم برنامج التشغيل المسجَّل بدقة على مضيفك كما هو موضح في [تثبيت برنامج تشغيل ODBC على مضيف digna](overview.md#install-the-driver).

---

## 2. خصائص ODBC {: #2-odbc-properties }

!!! important "مثال، وليس مواصفة"

    المجموعة أدناه هي تركيبة واحدة معروف أنها تعمل. الخصائص تابعة لبرنامج تشغيل Cloudera Hive، لذا تختلف أسماؤها وقيمها الافتراضية والقيم المقبولة بين إصدارات برنامج التشغيل والأنظمة الأساسية، وما يقبله HiveServer2 يعتمد كليًا على كيفية تأمين العنقود — آلية المصادقة، ووضع النقل، وTLS، والبوابة. استخدم هذه المجموعة كنقطة بداية وراجع وثائق إصدار برنامج التشغيل الذي ثبّته.

أضف الخصائص التالية في شاشة **Add DB Connection**:

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | يجب أن يطابق اسم برنامج التشغيل المسجَّل على مضيف *digna* |
| `HOST` | `hive.example.com` | اسم مضيف HiveServer2 أو عنوان IP |
| `PORT` | `10000` | منفذ HiveServer2؛ `10001` لنقل HTTP |

تبدو سلسلة الاتصال الناتجة كما يلي:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### المصادقة

يقبل HiveServer2 غير المؤمَّن الخصائص الثلاث أعلاه كما هي. حيثما تكون المصادقة مفعّلة، أضف:

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `AuthMech` | `3` | `0` بلا مصادقة، `2` اسم المستخدم فقط، `3` اسم المستخدم وكلمة المرور، `1` Kerberos |
| `UID` | `digna_source_user` | مطلوب لقيمتي `AuthMech` `2` و`3` |
| `PWD` | `<password>` | مطلوب لقيمة `AuthMech` `3`. فعّل **Encrypted** |

بالنسبة لـ Kerberos (`AuthMech=1`)، يحتاج مضيف *digna* أيضًا إلى تذكرة صالحة أو ملف keytab، إضافةً إلى الخصائص `KrbHostFQDN` و`KrbServiceName` و`KrbRealm` الموثّقة في برنامج التشغيل.

### النقل وTLS

| المفتاح | قيمة مثال | ملاحظات |
|---|---|---|
| `ThriftTransport` | `2` | `0` ثنائي (الافتراضي، المنفذ 10000)، `1` SASL، `2` HTTP (المنفذ 10001، وهو ما تتوقعه بوابة Knox) |
| `HTTPPath` | `cliservice` | مع `ThriftTransport=2` |
| `SSL` | `1` | حيثما يكون HiveServer2 مؤمَّنًا بـ TLS |
| `Schema` | `dignadata` | قاعدة بيانات Hive التي تبدأ فيها الجلسة. اختياري — يؤهّل *digna* استعلاماته بالأسماء الكاملة |

---

## 3. تهيئة *digna* {: #3-digna-configuration }

في شاشة **Add DB Connection**، قدّم ما يلي:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. ملاحظات حول Hive {: #4-notes-on-hive }

- **تأتي الكتالوجات من برنامج التشغيل.** لا يملك Hive كتالوجًا خاصًا به، لذا يأخذ *digna* ما يُبلغ عنه برنامج التشغيل — عادةً مدخل واحد باسم `HIVE` — ويعرض قواعد بيانات Hive كمخططات تحته.
- **Work Schema هو قاعدة بيانات Hive.** للتنميط *Permanent*، يحتاج المستخدم إلى صلاحية إنشاء الجداول وحذفها فيه، ويجب أن يكون موقع التخزين الأساسي قابلًا للكتابة.
- **أوضاع التنميط.** ينشئ *Permanent* جداول العمل في **Work Schema**. يستخدم *Session* الأمر `CREATE TEMPORARY TABLE`، الذي يتطلب HiveServer2 يدعم الجداول المؤقتة، ولا يمسّ **Work Schema**. يحتاج *Standard* إلى صلاحية القراءة فقط، وهو الوضع الذي يجب اختياره على عنقود لا يملك فيه *digna* أي صلاحية كتابة على الإطلاق.
- **التنميط مجموعة من الاستعلامات، وليس مسحًا.** يحسب HiveServer2 كل إحصائية، لذا يجب أن تمتلك قائمة الانتظار (queue) التي يرسل إليها مستخدم *digna* سعة كافية لنافذة الفحص.

---

## 5. التحقق من برنامج التشغيل (اختياري) {: #5-verifying-the-driver-optional }

تهيئة مصدر بيانات ODBC ليست مطلوبة لاتصال بدون DSN، لكن نافذة برنامج التشغيل نفسه طريقة مريحة للتأكد من أن برنامج التشغيل ووضع النقل وبيانات اعتمادك تعمل قبل إدخالها في *digna*.

#### الخطوة 1
![Step 1](images/hive/create_odbc_data_source_step1.png)

الحقول **Host** و**Port** و**Database** و**Mechanism** و**Thrift Transport** هنا هي الخصائص `HOST` و`PORT` و`Schema` و`AuthMech` و`ThriftTransport` في [القسم 2](#2-odbc-properties).

#### الخطوة 2 – اختبار الاتصال

أدخل كلمة المرور وانقر الزر **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

بعد نجاح الاختبار، انقر الزر **OK**.