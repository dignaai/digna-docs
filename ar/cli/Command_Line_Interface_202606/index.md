# مرجع digna CLI 2026.06
**2026-09-05**

توثّق هذه الصفحة المجموعة الكاملة من الأوامر المتاحة في إصدار ***digna*** CLI **2026.06**، بما في ذلك أمثلة الاستخدام والخيارات.

الملف التنفيذي يُسمّى `digna`.

---

## أساسيات CLI

---

### نظرة عامة وبناء الجملة

يستخدم CLI في الإصدار **2026.06** تسلسلاً هرمياً منظّماً للأوامر قائماً على الفئات:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

الأمران `version` و`serve` هما أمران مفردان بلا أمر فرعي:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### الخيارات العامة

تنطبق الخيارات العامة التالية على جميع الأوامر:

- `--help`، `-h`: يعرض معلومات المساعدة لواجهة CLI أو لفئة أوامر أو أمر فرعي محدّد.
- `--stacktrace`: يعرض سلسلة الأخطاء الكاملة عند الإخفاق بدلاً من الرسالة العليا فقط.

الخيار `--stacktrace` هو خيار عام بالمعنى الدقيق: يجب تمريره **قبل** فئة الأمر، لا بعدها.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

لا يوجد خيار `--version`. استخدم الأمر [`version`](#version) بدلاً منه.

### المتطلبات المسبقة

تحتاج معظم الأوامر إلى ملف `config.toml` صالح وقابل للقراءة؛ ويتطلب بعضها إضافةً إلى ذلك ترخيصاً صالحاً.
يوضّح الجدول التالي ما تحمّله كل فئة من فئات الأوامر قبل أن تقوم بأي عمل:

| فئة الأمر | يحتاج إلى `config.toml` | يحتاج إلى ترخيص صالح |
|---|---|---|
| `version` | لا | لا |
| `config check` | لا (فهو موضوع تقرير الأمر نفسه) | لا |
| `license check` | لا | هو *ذاته* عملية الفحص |
| `crypt` | نعم | لا |
| `serve` | نعم | لا |
| `project` | نعم | لا |
| `user` | نعم | نعم |
| `inspection` | نعم | نعم |
| `repo` | نعم | نعم |

حيثما يكون الترخيص مطلوباً، يُتحقَّق من توقيعه ومن تاريخ انتهائه معاً، ويتوقف الأمر قبل المساس بالمستودع إذا أخفق أي منهما.

### رموز الخروج

- `0`: نجح الأمر.
- `1`: أخفق الأمر. تُكتب رسالة الخطأ إلى stderr مسبوقة بالبادئة `Error: `.

### help

يوفّر الخيار `--help` معلومات عن فئات الأوامر والأوامر الفرعية والخيارات المتاحة:

1. **عرض المساعدة العامة:**
   ```bash
   digna --help
   ```

2. **الحصول على المساعدة لفئات وأوامر محدّدة:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **تشمل المخرجات:**
   - **وصف الأمر:** ملخّص للغرض من الأمر.
   - **بناء الجملة:** الوسائط المطلوبة والاختيارية.
   - **الخيارات:** الرايات والمعاملات الخاصة بالأمر.

### version

يطبع الأمر `version` إصدار ***digna*** المثبَّت. وهو لا يقرأ أي تهيئة ولا يتحقق من أي ترخيص، لذا يعمل أيضاً على تثبيت يكون فيه `config.toml` أو الترخيص مفقوداً أو غير صالح.

إصدار الإصدارة مستقل عن إصدار مخطّط المستودع الذي يبلّغ عنه [`repo check`](#repo-check).

#### استخدام الأمر
```bash
digna version
```

#### مثال على المخرجات
```text
2026.06
```

---

## إدارة التهيئة

---

### config check

يتحقق الأمر `config check` من صحة ملف التهيئة (`config.toml`)، مؤكّداً أن جميع الأقسام والإعدادات الإلزامية موجودة ومنسّقة تنسيقاً سليماً. ويُتحقَّق من كل قسم على حدة، فلا يحجب قسم `[app]` معطوب حالةَ القسم `[repo]`.

الأقسام التي يشملها التقرير هي:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — اختياري؛ غياب المفتاح يجتاز الفحص، أما وجود قائمة مشوَّهة فيُخفق

لا يحمّل الأمر عمداً تهيئةَ التطبيق بالطريقة التي تتبعها الأوامر الأخرى، لكي يتمكّن من تشخيص ملف `config.toml` قد يمنع ***digna*** من الإقلاع أصلاً.

#### استخدام الأمر
```bash
digna config check [OPTIONS]
```

#### الخيارات
- `--configpath`، `-c`: مسار ملف التهيئة، أو مسار مجلد يحتوي على `config.toml` (الافتراضي `./config.toml`).
- `--json`: إخراج تقرير التحقق بصيغة JSON. له الأسبقية على `--quiet`.
- `--quiet`، `-q`: إخفاء التقرير والاعتماد على رمز الخروج وحده.

#### مثال
```bash
digna config check
```

التحقق من ملف تهيئة محدّد وإخراج النتيجة بصيغة JSON:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### مثال على المخرجات
```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: FAILED
    missing field `aes_gcm_key`
 - OIDC config(s): OK

Overall: FAILED
```

الملف المفقود أو خطأ بناء الجملة في TOML لا يترك شيئاً يمكن التحقق منه قسماً بقسم، ويُبلَّغ عنه كخطأ واحد بدلاً من تقرير، بصرف النظر عن `--quiet` أو `--json`.

---

## إدارة المستودع

---

### repo check

يختبر الأمر `repo check` الاتصال بقاعدة البيانات ويتحقق من تثبيت المستودع وإصداره. ويُخفق إذا لم يكن المخطّط المهيَّأ موجوداً، أو إذا كان موجوداً لكنه لا يحتوي على مستودع ***digna***.

الإصدار المبلَّغ عنه هو إصدار مخطّط المستودع، الذي يُرقَّم بشكل منفصل عن إصدار ***digna*** الذي يطبعه [`version`](#version).

#### استخدام الأمر
```bash
digna repo check
```

#### مثال على المخرجات
```text
Repo version 3.0.0 installed
```

### repo install

يثبّت الأمر `repo install` مستودع ***digna*** جديداً في المخطّط المهيَّأ في `config.toml`، منشئاً جميع المتتاليات والجداول والفهارس والقيود والسجلات الأولية المطلوبة.

أما المخطّط نفسه فهذا الأمر **لا** ينشئه — إذ يجب أن يكون موجوداً مسبقاً. كما يرفض الأمر التنفيذ إذا كان هناك مستودع مثبَّت بالفعل في ذلك المخطّط، ويحيل إلى [`repo upgrade`](#repo-upgrade) إذا كان الإصدار المثبَّت أقدم.

#### استخدام الأمر
```bash
digna repo install
```

#### مثال على المخرجات
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

يطبّق الأمر `repo upgrade` ترحيلات مخطّط قاعدة البيانات للارتقاء بمستودع قائم إلى الإصدار الذي تتوقعه الإصدارة المثبَّتة. وتُطبَّق الترقيات خطوةً إصداريةً واحدة في كل مرة على امتداد مسار ترقية ثابت، وتُسجَّل كل خطوة مكتملة في المستودع.

إذا كان المستودع عند الإصدار المتوقَّع أصلاً، يبلّغ الأمر بأنه لا حاجة إلى ترقية ولا يُجري أي تغييرات.

#### استخدام الأمر
```bash
digna repo upgrade
```

#### مثال على المخرجات
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## إدارة التشفير

---

### crypt gen-key

ينشئ الأمر `crypt gen-key` مفتاح تشفير AES-GCM جديداً لاستخدامه كمفتاح تشفير في `config.toml`. ويجب أن يكون هناك ملف `config.toml` قابل للتحميل بالفعل، حتى وإن كان المفتاح المُنشأ لا يعتمد عليه.

#### استخدام الأمر
```bash
digna crypt gen-key
```

#### مثال على المخرجات
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

يشفّر الأمر `crypt encrypt` سلسلة نصية (مثل كلمة مرور قاعدة بيانات) باستخدام مفتاح AES-GCM المهيَّأ في `config.toml`، ثم يطبع النص المشفَّر.

#### استخدام الأمر
```bash
digna crypt encrypt <VALUE>
```

#### الوسائط
- **VALUE**: السلسلة النصية الصريحة المراد تشفيرها (مطلوبة).

#### مثال
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

يفكّ الأمر `crypt decrypt` تشفير سلسلة مشفَّرة بخوارزمية AES-GCM باستخدام المفتاح المهيَّأ في `config.toml`، ثم يطبع النص الصريح.

#### استخدام الأمر
```bash
digna crypt decrypt <VALUE>
```

#### الوسائط
- **VALUE**: السلسلة المشفَّرة المراد فك تشفيرها (مطلوبة).

#### مثال
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## إدارة المستخدمين

---

### user add

ينشئ الأمر `user add` حساب مستخدم جديداً في مستودع ***digna***. ويُخفق الأمر إذا كان هناك مستخدم بعنوان البريد الإلكتروني المعطى موجوداً بالفعل.

#### استخدام الأمر
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### الوسائط
- **EMAIL**: عنوان البريد الإلكتروني للمستخدم (مطلوب).
- **PASSWORD**: كلمة المرور الأولية للمستخدم (مطلوبة).
- **DISPLAY_NAME**: الاسم الظاهر الكامل للمستخدم (مطلوب).

#### الخيارات
- `--admin`، `-a`: إنشاء المستخدم بصلاحيات مدير (مستخدم فائق).

#### مثال
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

لإنشاء حساب مدير:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### مثال على المخرجات
```text
User created with ID: 42
```

### user list

يسرد الأمر `user list` جميع المستخدمين المسجَّلين في هيئة جدول تتضمن المعرّف والبريد الإلكتروني والاسم الظاهر وراية المدير.

#### استخدام الأمر
```bash
digna user list
```

#### مثال على المخرجات
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

يحدّث الأمر `user modify` الاسم الظاهر وصلاحيات المدير لحساب مستخدم قائم، يُحدَّد بعنوان بريده الإلكتروني.

يُكتب كلٌّ من الاسم الظاهر وراية المدير في كل مرة. والخيار `--admin` مفتاح تبديل لا قيمة: **إغفاله يسحب صلاحيات المدير**، لذا مرّره كلما أُريد للمستخدم أن يحتفظ بها أو يكتسبها.

#### استخدام الأمر
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### الوسائط
- **EMAIL**: البريد الإلكتروني للمستخدم المراد تعديله (مطلوب).
- **DISPLAY_NAME**: الاسم الظاهر المحدَّث (مطلوب).

#### الخيارات
- `--admin`، `-a`: منح صلاحيات المدير. أغفله لسحبها.
- `--valid-until`، `-v`: مقبول لأغراض التوافق لكنه **غير مطبَّق حالياً**. تمريره يطبع تحذيراً ولا يغيّر شيئاً.

#### مثال
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### مثال على المخرجات
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

يحدّث الأمر `user modify-pwd` كلمة المرور لحساب مستخدم قائم.

#### استخدام الأمر
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### الوسائط
- **EMAIL**: البريد الإلكتروني للمستخدم المراد تحديث كلمة مروره (مطلوب).
- **PASSWORD**: كلمة المرور الجديدة (مطلوبة).

#### مثال
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

يزيل الأمر `user delete` حساب مستخدم من النظام.

#### استخدام الأمر
```bash
digna user delete <EMAIL>
```

#### الوسائط
- **EMAIL**: البريد الإلكتروني للمستخدم المراد حذفه (مطلوب).

#### مثال
```bash
digna user delete jdoe@example.com
```

---

## إدارة المشاريع ومصادر البيانات

---

### project list

يسرد الأمر `project list` جميع المشاريع المتاحة في المستودع، مع عرض معرّفها واسمها ووصفها.

#### استخدام الأمر
```bash
digna project list
```

#### مثال على المخرجات
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

يسرد الأمر `project list-ds` جميع مصادر البيانات المرتبطة بمشروع معيّن، مع عرض معرّفها واسمها ونوعها ومخطّطها واسم جدولها.

#### استخدام الأمر
```bash
digna project list-ds <PROJECT_NAME>
```

#### الوسائط
- **PROJECT_NAME**: اسم المشروع الذي تُسرد مصادر بياناته (مطلوب). ويجب أن يطابق الاسم تماماً.

#### مثال
```bash
digna project list-ds ProjectA
```

#### مثال على المخرجات
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

يصدّر الأمر `project export-ds` مصادر البيانات من مشروع إلى مستند JSON.

إذا لم يُعطَ `--table-name` ولا `--table-id`، تُصدَّر جميع مصادر بيانات المشروع.

#### استخدام الأمر
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### الوسائط
- **PROJECT_NAME**: اسم المشروع المراد تصدير مصادر بياناته (مطلوب).

#### الخيارات
- `--table-name`، `-n`: أسماء مصادر البيانات المراد تصديرها. يمكن إعطاء عدة أسماء مفصولة بمسافات.
- `--table-id`، `-i`: معرّفات مصادر البيانات المراد تصديرها. يمكن إعطاء عدة معرّفات مفصولة بمسافات.
- `--exportfile`، `-f`: المسار الذي تُحفظ فيه مصادر البيانات المصدَّرة (الافتراضي: `data_sources_export.json`).

#### مثال
لتصدير جميع مصادر البيانات من `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

لتصدير جداول محدّدة:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### مثال على المخرجات
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

يستورد الأمر `project import-ds` مصادر البيانات من ملف تصدير إلى مشروع هدف، ويبلّغ لكل كائن عمّا أُنشئ أو حُدِّث أو تُخطّي.

#### استخدام الأمر
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### الوسائط
- **PROJECT_NAME**: اسم المشروع الهدف المراد الاستيراد إليه (مطلوب).
- **EXPORT_FILE**: مسار ملف تصدير JSON (مطلوب).

#### الخيارات
- `--output-file`، `-o`: الملف الذي يُكتب فيه تقرير الاستيراد. وبدونه يذهب التقرير إلى stdout.
- `--output-format`، `-f`: صيغة تقرير الاستيراد — `table` أو `json` أو `csv` (الافتراضي: `table`).

#### مثال
```bash
digna project import-ds ProjectB my_export.json
```

للحصول على تقرير قابل للقراءة آلياً:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

يغطي التقرير أربعة مستويات من الكائنات — مصدر البيانات وتعريف مجموعة البيانات والسمة وقاعدة التحقق — ولكلٍّ منها إجراء الاستيراد ونتيجته ومعرّف الكائن الناتج وأي معلومات إضافية.

### project plan-import-ds

يعرض الأمر `project plan-import-ds` معاينةً لاستيراد مصادر البيانات إلى مشروع هدف، مبيّناً أي الكائنات ستُنشأ أو تُحدَّث أو تُتخطّى، من دون تغيير أي شيء. وهو يقبل ملف التصدير نفسه وخيارات التقرير نفسها التي يقبلها [`project import-ds`](#project-import-ds)، ويضيف رقم خطوة لكل كائن مخطّط له.

#### استخدام الأمر
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### الوسائط
- **PROJECT_NAME**: اسم المشروع الهدف (مطلوب).
- **EXPORT_FILE**: مسار ملف التصدير (مطلوب).

#### الخيارات
- `--output-file`، `-o`: الملف الذي تُكتب فيه خطة الاستيراد. وبدونه تذهب الخطة إلى stdout.
- `--output-format`، `-f`: صيغة خطة الاستيراد — `table` أو `json` أو `csv` (الافتراضي: `table`).

#### مثال
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## إدارة الفحوصات

---

### inspection run

ينشئ الأمر `inspection run` طلب فحص لمشروع ونطاق تواريخ، ثم — تبعاً للخيارات المعطاة — إما ينتظره، أو يعود فوراً، أو ينفّذه داخل العملية نفسها.

أنماط التنفيذ الثلاثة هي:

- **الافتراضي (بلا راية)**: يوضع الطلب في طابور الانتظار للواجهة الخلفية، ويستقصيه CLI كل ثانيتين مع طباعة تقدّم المهام حتى يبلغ الفحص حالة نهائية. ويلزم وجود `digna serve` قيد التشغيل، وإلا لن يلتقط أحد الطلب.
- **`--async-mode`**: يوضع الطلب في طابور الانتظار ويُطبع معرّفه فوراً. استخدم [`inspection status`](#inspection-status) لمتابعته.
- **`--bypass-backend`**: تُنفَّذ عملية الفحص بواسطة عملية CLI نفسها ولا توضع في طابور الانتظار، فلا حاجة إلى خادم قيد التشغيل.

الخياران `--async-mode` و`--bypass-backend` متنافيان.

وفي كل الأنماط ينتهي الأمر برمز خروج غير صفري إذا لم يكتمل الفحص بنجاح.

#### استخدام الأمر
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### الوسائط
- **PROJECT_NAME**: اسم المشروع الهدف (مطلوب). ويجب أن يطابق الاسم تماماً.
- **START_DATE**: تاريخ بداية النطاق بصيغة `YYYY-MM-DD` (مطلوب).
- **END_DATE**: تاريخ نهاية النطاق بصيغة `YYYY-MM-DD` (مطلوب).

#### الخيارات
- `--table-name`: يقصر الفحص على مصدر بيانات واحد من المشروع، يُعطى باسم مصدر البيانات. وبدونه تُفحص جميع مصادر بيانات المشروع.
- `--async-mode`: يضع الفحص في طابور الانتظار ويطبع معرّف الطلب بدلاً من انتظاره. لا يمكن دمجه مع `--bypass-backend`.
- `--bypass-backend`: ينفّذ الفحص مباشرة في عملية CLI بدلاً من وضعه في طابور الانتظار للواجهة الخلفية. لا يمكن دمجه مع `--async-mode`.

#### مثال
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

لتقديم فحص غير متزامن:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

لفحص مصدر بيانات واحد:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### مثال على المخرجات
النمط الافتراضي:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

النمط غير المتزامن:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

يستعلم الأمر `inspection status` عن حالة طلب فحص وتقدّم مهامه اعتماداً على معرّف الطلب.

#### استخدام الأمر
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### الوسائط
- **INSPECTION_REQUEST_ID**: المعرّف الرقمي لطلب الفحص (مطلوب).

#### مثال
```bash
digna inspection status 1024
```

#### مثال على المخرجات
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

يطلب الأمر `inspection abort` إلغاء طلبات الفحص الجارية أو المعلّقة. وهو يسجّل حدث إيقاف لكل طلب متأثّر؛ والواجهة الخلفية هي التي تتصرّف بناءً عليه، فالإجهاض طلبُ توقّف لا إنهاءٌ فوري.

#### استخدام الأمر
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### الوسائط
- **INSPECTION_REQUEST_ID**: معرّف طلب الفحص المراد إجهاضه. مطلوب ما لم يُعطَ `--killall`.

#### الخيارات
- `--killall`: يجهض جميع طلبات الفحص الجارية والمعلّقة حالياً. وله الأسبقية على أي معرّف طلب يُعطى معه.

#### مثال
لإجهاض طلب محدّد:
```bash
digna inspection abort 1024
```

لإجهاض جميع الفحوصات النشطة والمنتظرة:
```bash
digna inspection abort --killall
```

#### مثال على المخرجات
يبلّغ `--killall` عمّا فعله؛ أما إجهاض طلب واحد فلا ينتج عنه أي مخرجات ويبلّغ عن نجاحه عبر رمز خروجه.
```text
All running and pending inspections have been aborted.
```

---

## إدارة التراخيص

---

### license check

يتحقق الأمر `license check` من ملف `license.toml`، مؤكّداً توقيعه مقابل المفتاح العام المرفق مع التثبيت ومتحقّقاً من أنه لم ينتهِ. وهو لا يقرأ أي تهيئة للتطبيق، لذا يعمل أيضاً قبل إعداد `config.toml`.

#### استخدام الأمر
```bash
digna license check
```

#### مثال على المخرجات
```text
License is valid
```

يُبلَّغ عن التوقيع غير الصالح والترخيص المنتهي كخطأين متمايزين، وكلاهما برمز الخروج 1.

---

## الخادم والخدمات الخلفية

---

### serve

يشغّل الأمر `serve` خادم واجهة REST البرمجية لـ ***digna*** إلى جانب مجدول الفحوصات الخلفي ومدير الفحوصات. وعند الإقلاع يُخفق أيضاً أي فحص لا يزال المستودع يسجّله على أنه قيد التشغيل، إذ لا يمكن لشيء أن يكون قد نجا من عملية سابقة.

يعمل الأمر في المقدمة إلى أن يُوقَف.

#### استخدام الأمر
```bash
digna serve [OPTIONS]
```

#### الخيارات
- `--address`: عنوان الشبكة الذي يُربط به خادم الواجهة البرمجية (الافتراضي: `127.0.0.1`).
- `--port`: رقم المنفذ الذي يُستمع عليه (الافتراضي: `8000`).

#### مثال
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### مثال على المخرجات
```text
Server running on http://0.0.0.0:8000
```