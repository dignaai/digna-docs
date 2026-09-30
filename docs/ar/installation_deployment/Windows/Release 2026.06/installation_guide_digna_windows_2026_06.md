---
title: دليل التثبيت على Windows – إصدارة digna 2026.06 | وثائق digna
description: دليل خطوة بخطوة لتثبيت digna إصدار 2026.06 على Windows — متطلبات النظام، إعداد PostgreSQL، تكوين خادم الويب، إعداد الواجهة الخلفية واللوحة، تشغيل digna كخدمة Windows، والترقية إلى إصدار جديد.
keywords: digna تثبيت ويندوز, دليل نشر digna, إعداد الواجهة الخلفية digna, تثبيت لوحة digna, إعداد postgresql, خدمة ويندوز digna, دليل ترقية digna
image: /assets/logo_square.png
---

# دليل التثبيت على Windows لإصدار digna 2026.06

**الإصدار:** 2026.06

**آخر تحديث:** 30 أغسطس 2026


---

## جدول المحتويات

1. [مقدمة](#introduction)
2. [متطلبات النظام](#system-requirements)
3. [إعداد ما قبل التثبيت](#pre-installation-setup)
4. [إعداد خادم PostgreSQL](#postgresql-server-setup)
5. [تكوين خادم الويب](#web-server-configuration)
6. [التثبيت الأولي](#initial-installation)
7. [تكوين الواجهة الخلفية](#backend-configuration)
8. [تكوين اللوحة](#dashboard-configuration)
9. [تشغيل digna كخدمة Windows](#running-digna-as-a-windows-service)
10. [الترقية إلى إصدار جديد](#upgrading-to-a-new-release)

---

## المقدمة {: #introduction }

### حول digna

digna هي منصة شاملة تعتمد على الذكاء الاصطناعي مصممة لتحسين إدارة جودة البيانات عبر بيئات بيانات متنوعة مثل المستودعات (warehouses)، والبحيرات (lakes)، والـ lakehouses. تم بناؤها لتكون قابلة للتوسع والتكيف بدرجة عالية، وتتعامل digna مع تحديات البيانات الحديثة من خلال الأتمتة، والمراقبة في الوقت الحقيقي، وكشف الشذوذ.

يتكون digna من مكونين رئيسيين:

- **digna**: نواة التطبيق، وهي المسؤولة عن معالجة البيانات وتنفيذ فحوص الجودة. تجمع الواجهة الخلفية وواجهة سطر الأوامر في ملف تنفيذي واحد، وتحل محل البرنامجين المنفصلين `dignabackend` و`dignacli` في الإصدارات السابقة.
- **dignadashboard**: واجهة ويب مستضافة على خادم ويب، توفر طريقة سهلة للتفاعل مع منصة digna وتصوير مؤشرات جودة البيانات.

### ما الجديد في الإصدار 2026.06

يجلب هذا الإصدار قدرات مراقبة البيانات (data observability) مباشرة إلى التعليمات البرمجية الخاصة بك، مما يمكّن المطورين من مراقبة جودة البيانات عند المصدر. راجع ملاحظات الإصدارة في [ملاحظات الإصدار](http://docs.digna.ai/changelog/Release_202606/) للاطلاع على التفاصيل الكاملة.

### تبحث عن macOS أو Linux؟

يغطي هذا الدليل Windows. للمنصات الأخرى، راجع [دليل التثبيت على macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) أو [دليل التثبيت على Linux](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## متطلبات النظام {: #system-requirements }

قبل البدء في التثبيت، تأكد من أن نظامك يستوفي الحد الأدنى من المتطلبات التالية:

| المتطلب | المواصفة |
|---|---|
| **نظام التشغيل** | Windows Server أو Windows 10/11 |
| **الذاكرة (إعداد بسيط)** | 16 جيجابايت RAM |
| **مساحة القرص** | 10 جيجابايت مساحة متاحة |
| **قاعدة البيانات** | PostgreSQL Server إصدار 12 أو أعلى |
| **خادم الويب** | IIS أو Apache Tomcat أو ما يعادلهما |

### خيارات تثبيت قاعدة البيانات

**إذا كان PostgreSQL مثبتًا بالفعل:**
يمكنك إضافة قاعدة بيانات جديدة لـ digna إلى خادم PostgreSQL الموجود لديك.

**إذا كنت ستثبت PostgreSQL على نفس الجهاز الذي سيشغل digna:**

!!! info "المواصفات الموصى بها"

    - **الذاكرة**: 32 جيجابايت RAM (بدلاً من 16 جيجابايت)
    - **مساحة القرص**: 50 جيجابايت مساحة متاحة (بدلاً من 10 جيجابايت)

    هذه المواصفات الأعلى تستوعب تشغيل digna وقاعدة بيانات PostgreSQL معًا على نفس الجهاز.

---

## إعداد ما قبل التثبيت {: #pre-installation-setup }

قبل تثبيت digna، تأكد من توفر متطلبين أساسيين:

1. **خادم PostgreSQL** – لتخزين المقاييس المحسوبة وبيانات الأداء
2. **خادم ويب** – لاستضافة لوحة digna

إذا لم تكن هذه المكونات معدة بالفعل، اتبع الأقسام أدناه لتثبيتها وتكوينها.

---

## إعداد خادم PostgreSQL {: #postgresql-server-setup }

### إذا كان PostgreSQL مثبتًا بالفعل

إذا كان PostgreSQL مثبتًا ويعمل على جهازك المحلي أو إذا كنت تستخدم خادم PostgreSQL مُدار عن بُعد، يمكنك الانتقال إلى القسم التالي: [تكوين خادم الويب](#web-server-configuration).

### تثبيت PostgreSQL

اتبع هذه الخطوات لتثبيت PostgreSQL على Windows:

#### الخطوة 1: تنزيل PostgreSQL

1. زر صفحة [تنزيلات PostgreSQL](https://www.postgresql.org/download/)
2. اختر **Windows**
3. قم بتنزيل أحدث مثبت

#### الخطوة 2: تشغيل المثبت

1. انقر نقرًا مزدوجًا على ملف المثبت الذي تم تنزيله
2. اتبع المطالبات في معالج التثبيت

#### الخطوة 3: اختيار دليل التثبيت

حدد الدليل الذي سيتم تثبيت PostgreSQL فيه. الموقع الافتراضي عادةً ما يكون مناسبًا.

#### الخطوة 4: اختيار المكونات

لإعداد قياسي، احتفظ بخيارات المكونات الافتراضية محددة.

#### الخطوة 5: تعيين كلمة مرور مستخدم PostgreSQL الخارق

أدخل وأكد كلمة مرور لمستخدم PostgreSQL الخارق (`postgres`). **احفظ هذه الكلمة بأمان** — ستحتاجها لاحقًا.

#### الخطوة 6: تكوين رقم المنفذ

المنفذ الافتراضي لـ PostgreSQL هو `5432`. يمكنك استخدام الافتراضي أو تحديد منفذ مختلف إذا لزم الأمر.

!!! tip "نصيحة"

    إذا كان المنفذ 5432 مستخدمًا بالفعل، اختر منفذًا بديلًا ودوِّنَه للتكوين لاحقًا.

#### الخطوة 7: اختيار اللغة المحلية (Locale)

اختر اللغة المحلية لقاعدة البيانات. الافتراضي عادةً ما يكون مناسبًا لمعظم التثبيتات.

#### الخطوة 8: إكمال التثبيت

انقر **التالي** عبر الخطوات المتبقية، ثم انقر **إنهاء**.

#### الخطوة 9: التحقق من التثبيت

افتح موجه الأوامر وتحقق من تثبيت PostgreSQL:

```bash
psql --version
```

يجب أن ترى إصدار PostgreSQL إذا كان التثبيت ناجحًا.

---

## تكوين خادم الويب {: #web-server-configuration }

تتطلب digna خادم ويب لاستضافة اللوحة. اختر أحد الخيارات التالية:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

تحتاج إلى تثبيت وتكوين **واحد** فقط من هذه الخوادم.

### إعداد IIS {: #iis-setup }

#### نظرة عامة

Internet Information Services (IIS) هو خادم الويب من Microsoft لاستضافة مواقع الويب والتطبيقات على الويب.

#### تمكين IIS

1. **افتح لوحة التحكم**
   - اضغط `Win + R`
   - اكتب `control` واضغط Enter

2. **انتقل إلى ميزات Windows**
   - انقر **البرامج**
   - اختر **تشغيل ميزات Windows أو إيقافها**

3. **تمكين Internet Information Services**
   - مرر لأسفل وابحث عن **Internet Information Services (IIS)**
   - ضع علامة في مربع الاختيار لتمكينه
   - انقر على **+** لتوسيع وتحقق من تحديد المكونات الفرعية التالية:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **انقر موافق** لتطبيق التغييرات

5. **التحقق من تثبيت IIS**
   - افتح المتصفح
   - انتقل إلى `http://localhost`
   - يجب أن ترى صفحة ترحيب IIS

#### مطلوب: مكون URL Rewrite

يتطلب IIS مكون URL Rewrite. قم بتنزيله وتثبيته من [الصفحة الرسمية لمايكروسوفت](https://www.iis.net/downloads/microsoft/url-rewrite).

#### مطلوب: نوع MIME لملفات Markdown

لضمان تقديم ملفات Markdown (`.md`) بشكل صحيح عبر IIS:

1. افتح **IIS Manager** (اضغط `Win + R`، اكتب `inetmgr`، اضغط Enter)
2. انتقل إلى **Your Site > MIME Types**
3. انقر **Add...**
4. اضبط:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "مهم"

    بدون هذا الإعداد، قد لا يتم تقديم ملفات `.md` بشكل صحيح.

---

### إعداد Apache Tomcat {: #apache-tomcat-setup }

#### نظرة عامة

Apache Tomcat هو حاوية Java Servlet وخادم ويب مفتوح المصدر.

#### التثبيت

1. **تنزيل Apache Tomcat**
   - زر [تنزيلات Apache Tomcat](https://tomcat.apache.org/download-90.cgi)
   - قم بتنزيل توزيع ZIP لنظام Windows

2. **فك ضغط الأرشيف**
   - فك ضغط ملف ZIP إلى مجلد على نظامك
   - مثال: `C:\Program Files\Apache Tomcat`

3. **التحقق من تشغيل Tomcat**
   - افتح المتصفح
   - انتقل إلى `http://localhost:8080`
   - يجب أن ترى صفحة الترحيب لـ Apache Tomcat

!!! tip "نصيحة"

    عادةً ما يبدأ Apache Tomcat تلقائيًا بعد التثبيت. إذا لم يبدأ، انتقل إلى مجلد `bin` وقم بتشغيل `startup.bat`.

---

## التثبيت الأولي {: #initial-installation }

### الخطوة 1: إعداد مستودع digna

يخزن مستودع digna جميع المقاييس المحسوبة بواسطة digna. يعمل كمركز قاعدة البيانات للبيانات التحليلية وأداء النظام.

#### إنشاء مخطط المستودع ومستخدم

افتح عميل PostgreSQL الخاص بك (pgAdmin أو psql أو ما شابه) ونفّذ أوامر SQL التالية:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**استبدل العناصر النائبة التالية:**

- `<digna_repo_schema>` — اسم المخطط الذي تريده (مثال: `dignarepo`)
- `<digna_repo_user>` — اسم المستخدم الذي تريده (مثال: `digna_user`)
- `<digna_repo_password>` — كلمة مرور آمنة لهذا المستخدم

**مثال:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "أفضل الممارسات"

    استخدم كلمات مرور قوية ومعقدة لمستخدمي قواعد البيانات. تجنب بيانات الاعتماد سهلة التخمين.

---

### الخطوة 2: فك حزمة تثبيت digna

1. اعثر على ملف ZIP لتثبيت digna المقدم إليك
2. فك ضغطه إلى موقع التثبيت الذي تختاره
3. بعد الفك، يجب أن ترى العناصر التالية:
   - `dashboard/` — واجهة الويب للوحة
   - `digna` — الملف التنفيذي الرئيسي (الواجهة الخلفية + CLI مدمجان)

!!! info "ملفا التهيئة والترخيص غير موجودين في الحزمة"

    لا يأتي `config.toml` ولا `dashboard/dashboard_config.toml` مع التثبيت — بل تنشئ كليهما بنفسك، في
    [تهيئة الواجهة الخلفية](#backend-configuration) و
    [تهيئة اللوحة](#dashboard-configuration). ولا يأتي `license.toml` معه كذلك؛
    إذ يقدّمه digna بشكل منفصل، كما هو موضّح في الخطوة 3.

### الخطوة 3: تثبيت ملف الترخيص

!!! warning "مهم"

    ملف الترخيص **غير** مشمول في حزمة التثبيت وسيُقدّم لك بشكل منفصل من digna.

1. اعثر على ملف `license.toml` المقدم لك
2. انسخه إلى الدليل الجذري لتثبيت digna (حيث يوجد `config.toml` والملف التنفيذي `digna`)

**لماذا هذا مهم:**
يحتوي ملف الترخيص على معلومات العميل وتاريخ انتهاء صلاحية الترخيص والتوقيع الرقمي. **لا تقم بتعديل هذا الملف** — أي تغييرات ستبطل صلاحيته.

**هيكل الدليل بعد الإعداد:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## تكوين الواجهة الخلفية {: #backend-configuration }

### الخطوة 1: إنشاء وتحرير ملف التكوين

ملف `config_template.toml` موجود في دليل تثبيت digna الخاص بك. كل ما عليك هو إعادة تسميته إلى `config.toml`.

الموقع: `digna_installation/config.toml`

افتح `config.toml` في محرر نصوص وغيّر كل قسم كما هو موضح أدناه.

#### قسم [app]

هذا القسم يضبط إعدادات تطبيق الواجهة الخلفية لـ digna:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| المعامل | القيمة | ملاحظات |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | عنوان الواجهة الأمامية | إذا كانت اللوحة على خادم مختلف، أدرج عنوان URL الخاص بها |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | مطلوب لـ CORS مع بيانات الاعتماد |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | السماح بجميع طرق HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | السماح بجميع الرؤوس |

#### قسم [repo]

هذا القسم يضبط الاتصال بقاعدة بيانات PostgreSQL:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| المعامل | القيمة | ملاحظات |
|---|---|---|
| `digna_REPO_HOST` | `localhost` أو IP | اسم مضيف/عنوان IP خادم PostgreSQL |
| `digna_REPO_PORT` | `5432` (افتراضي) | منفذ PostgreSQL |
| `digna_REPO_DB` | `postgres` | اسم قاعدة البيانات |
| `digna_REPO_SCHEMA` | `dignarepo` | المخطط الذي تم إنشاؤه سابقًا |
| `digna_REPO_USER` | `digna_user` | المستخدم الذي تم إنشاؤه في إعداد PostgreSQL |
| `digna_REPO_PASSWORD` | كلمة مرورك | كلمة المرور التي تم تعيينها أثناء إنشاء المخطط |

#### قسم [base]

يحتوي هذا القسم على إعدادات الأمان وملفات تعريف الارتباط:

```toml
[base]
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
DIGNA_SCHEDULER_MAX_DELAY = 100
DIGNA_CLEANUP_TIME = "12:00"
```

| المعامل | القيمة | ملاحظات |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | طابق مع نطاق الواجهة الأمامية |
| `digna_COOKIE_SECURE` | `false` (محلي) / `true` (إنتاج) | استخدم `true` للاتصالات عبر HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | مُمكّن دائمًا لأغراض الأمان |
| `digna_COOKIE_SAME_SITE` | `lax` | يساعد في منع هجمات CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ساعة) | مهلة الجلسة بالثواني |
| `digna_MAX_WORKERS` | عدد أنوية المعالج - 1 | عدد مهام الفحص المتوازية |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | أقصى تأخير بالثواني يمكن للمجدول إضافته قبل بدء مهمة حان موعدها |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | وقت اليوم (تنسيق 24 ساعة `HH:MM`) الذي يبدأ عنده التنظيف اليومي |

#### قسم [encryption]

يحتوي هذا القسم على المفتاح المستخدم لتشفير القيم الحساسة المخزنة في المستودع. وهو **إلزامي** — يُبلغ `config check` عن القسم `[encryption]` بحالة FAILED إذا كان المفتاح مفقودًا.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| المعامل | القيمة | ملاحظات |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | مفتاح مُرمّز بصيغة Base64 | يشفّر القيم الحساسة المخزنة في مستودع digna |

!!! warning "احمِ الملف config.toml"

    هذا المفتاح قيمة ثابتة ومتطابقة في جميع تثبيتات digna، وهو ما يفك تشفير القيم الحساسة في مستودعك. اقصر الوصول إلى `config.toml` على الحساب الذي يشغّل digna، وأبقِ الملف خارج نظام إدارة الإصدارات والأقراص المشتركة، واستبعده من أي نسخة احتياطية تُحفظ بأمان أقل من المستودع نفسه.

#### قسم [logging]

هذا القسم يضبط سلوك السجلات:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| المعامل | القيمة | ملاحظات |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` أو `DEBUG` | `INFO` للإنتاج، `DEBUG` لاستكشاف الأخطاء |
| `digna_LOGGING_BACKUP_COUNT` | `10` | عدد النسخ الاحتياطية اليومية للسجلات التي سيتم الاحتفاظ بها |

---

### الخطوة 2: تحقق من التهيئة

قبل تهيئة المستودع، تحقق من أن `config.toml` مكتمل ومبني بشكل صحيح. نفّذ في دليل تثبيت digna:

```bash
digna config check
```

يُتحقق من كل قسم على حدة، بحيث لا يخفي خطأ واحد حالة الأقسام الأخرى:

```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: OK
 - OIDC config(s): OK

Overall: OK
```

صحّح كل ما يُبلَّغ عنه بحالة FAILED، وأعد تنفيذ الأمر قبل المتابعة. القائمة الكاملة للخيارات موجودة في [مرجع CLI](../../../cli/Command_Line_Interface_202606.md).

### الخطوة 3: تهيئة المستودع

1. افتح موجه الأوامر
2. انتقل إلى دليل تثبيت digna الخاص بك (حيث يوجد `config.toml` والملف التنفيذي `digna`)
3. شغّل اختبار الاتصال:

```bash
digna repo check
```

يجب أن ترى تأكيدًا بأن الاتصال قد تم (المستودع نفسه لم يتم تهيئته بعد).

### الخطوة 4: تثبيت مخطط المستودع

في نفس الدليل، نفّذ:

```bash
digna repo install
```

هذا الأمر يثبت الجداول والمخطط الضروريين في قاعدة بيانات PostgreSQL الخاصة بك.

### الخطوة 5: إنشاء مستخدم مسؤول

1. افتح نافذة موجه أوامر **جديدة**
2. انتقل إلى دليل تثبيت digna الخاص بك
3. شغّل الأمر التالي لإنشاء مستخدم مسؤول:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**مثال:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

سيُنشئ هذا مستخدمًا بصلاحيات إدارية كاملة.

!!! tip "أفضل الممارسات"

    استخدم كلمة مرور قوية تشتمل على أحرف كبيرة وصغيرة وأرقام ورموز خاصة.

---

### الخطوة 6: بدء خادم digna

في دليل تثبيت digna، ابدأ الخادم بـ:

```bash
digna serve --address <host> --port <port>
```

**المعلمات:**
- `--address` — اسم المضيف/عنوان IP للخادم
- `--port` — منفذ الخادم

يجب أن ترى رسائل بدء تؤكد أن الخادم يعمل:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! note "الخادم يشغل الطرفية"

    يعمل `serve` في المقدمة ويستمر حتى توقفه بالضغط على ++ctrl+c++. اتركه يعمل بينما تكمل الإعداد؛ ولتشغيله تلقائيًا عند الإقلاع بدلًا من ذلك انظر [تشغيل digna كخدمة Windows](#running-digna-as-a-windows-service).

## تكوين اللوحة {: #dashboard-configuration }

### الخطوة 1: نشر اللوحة على خادم الويب

تقرأ لوحة digna تهيئتها الخاصة من `dashboard/dashboard_config.toml`. هذا الملف لا يأتي مع التثبيت — بل تنشئه في مجلد `dashboard/` إلى جانب ملفات اللوحة.

محتوياته موضّحة في [الدخول الموحّد (SSO)](../../../sso/overview.md)، وهناك أيضًا يلزم الملف: فهو يحمل خيارات تسجيل الدخول التي تعرضها اللوحة، وفي عمليات النشر متعددة النسخ، اتصال الواجهة الخلفية.

اختر خادم الويب الخاص بك واتبع خطوات النشر المناسبة.

#### النشر على IIS

1. **افتح IIS Manager**
   - اضغط `Win + R`، اكتب `inetmgr`، اضغط Enter

2. **إنشاء موقع ويب جديد**
   - في اللوحة اليسرى، انقر بزر الماوس الأيمن على **Sites**
   - اختر **Add Website...**

3. **تكوين الموقع**
   - **Site Name**: أدخل اسمًا (مثال: "dignaDashboard")
   - **Physical Path**: اضغط Browse وحدد مجلد `dashboard`
   - **Binding**: عيّن عنوان IP والمنفذ (المنفذ الافتراضي 80 لـ HTTP و443 لـ HTTPS)

4. **بدء الموقع**
   - انقر **OK** لإنشاء الموقع
   - انقر بزر الماوس الأيمن على الموقع الجديد واختر **Start**

5. **اختبار التثبيت**
   - افتح المتصفح
   - انتقل إلى `http://localhost` (أو عنوان URL الذي قمت بتكوينه)
   - يجب أن ترى صفحة تسجيل دخول لوحة digna

#### النشر على Apache Tomcat

1. **نسخ اللوحة إلى Tomcat**
   - انسخ مجلد `dashboard` إلى مجلد `webapps` في Tomcat
   - أعد تسميته إذا لزم (مثال: إلى `digna`)
   - مثال: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **التحقق من النشر**
   - حدّث أو أعد تحميل صفحة إدارة Tomcat (http://localhost:8080)
   - يجب أن ترى "digna" (أو الاسم الذي اخترته) مدرجًا ضمن التطبيقات المنشورة

3. **الوصول إلى اللوحة**
   - افتح المتصفح
   - انتقل إلى `http://localhost:8080/digna`
   - يجب أن ترى صفحة تسجيل دخول لوحة digna

---

## تشغيل digna كخدمة Windows {: #running-digna-as-a-windows-service }

### لماذا نستخدم خدمة Windows؟

تشغيل الواجهة الخلفية لـ digna كخدمة Windows يضمن أنها:
- تبدأ تلقائيًا عند إقلاع الخادم
- تعمل في الخلفية دون الحاجة لفتح نافذة موجه الأوامر
- تعيد التشغيل تلقائيًا إذا تعطّلت
- يمكن إدارتها عبر أدوات خدمات Windows

### أوامر `windows`

تُدار الخدمة بواسطة الملف التنفيذي `digna` نفسه، من خلال الأوامر الفرعية `digna windows`.
لا توجد ملفات دُفعات (batch) لتشغيلها.

| الأمر | الغرض |
|---|---|
| `digna windows install` | يسجل digna كخدمة Windows |
| `digna windows start` | يشغّل الخدمة المسجلة |
| `digna windows stop` | يوقف الخدمة الجارية |
| `digna windows uninstall` | يلغي تسجيل الخدمة |

!!! warning "يتطلب صلاحيات المسؤول"

    يجب تنفيذ الأوامر الأربعة جميعها من موجه أوامر (Command Prompt) مفتوح بصلاحيات Administrator.

يقبل كل أمر الخيار `--name` لاستهداف خدمة مسجلة باسم غير الاسم الافتراضي. القائمة الكاملة
للخيارات موجودة في [مرجع CLI](../../../cli/Command_Line_Interface_202606.md).

### تثبيت الخدمة

1. **افتح موجه الأوامر كمسؤول**
   - انقر بزر الماوس الأيمن على Command Prompt
   - اختر "Run as Administrator"

2. **انتقل إلى دليل تثبيت digna**
   ```bash
   cd C:\path\to\digna
   ```

3. **سجّل الخدمة**
   ```bash
   digna windows install
   ```

!!! important "حدّد العنوان والمنفذ ما لم تناسبك القيم الافتراضية"

    يسجّل `install` العنوان والمنفذ في تسجيل الخدمة، وترتبط الخدمة بما سُجّل
    بالضبط. القيم الافتراضية هي `127.0.0.1` و`8000`، وهي لا تقبل الاتصالات
    إلا من الجهاز نفسه. لا تستطيع لوحة على مضيف آخر الوصول إلى ذلك، لذا حدّد
    العنوان الذي يجب أن تستمع عليه الواجهة الخلفية:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    لا تُقرأ هذه القيم من `config.toml`. لتغييرها لاحقًا، ألغِ تثبيت الخدمة ثم
    ثبّتها مجددًا بالقيم الجديدة.

تُسجَّل الخدمة مع **التشغيل التلقائي**، لذا ستبدأ مع Windows. لكنها لا تبدأ
فورًا — راجع القسم التالي.

#### خيارات التثبيت

| الخيار | القيمة الافتراضية | الغرض |
|---|---|---|
| `--name` | `digna` | الاسم الذي تُسجَّل الخدمة تحته |
| `--display-name` | `digna` | الاسم المعروض في services.msc |
| `--description` | `digna data quality backend` | الوصف المعروض في services.msc |
| `--address` | `127.0.0.1` | العنوان الذي تربط الخدمة واجهتها البرمجية (API) به |
| `--port` | `8000` | المنفذ الذي تربط الخدمة واجهتها البرمجية (API) به |
| `--working-dir` | دليل الملف التنفيذي `digna` | الدليل الذي يحتوي على `config.toml` و`license.toml`، والذي تجعله الخدمة دليل عملها |
| `--start-type` | `auto` | `auto` يبدأ مع Windows، و`manual` يبدأ عند الطلب فقط، و`disabled` يسجّل الخدمة لكنه يرفض تشغيلها |
| `--account` | `LocalSystem` | الحساب الذي تعمل الخدمة به، مثل `DOMAIN\user` أو `.\user` |
| `--password` | | كلمة مرور `--account` |

!!! tip "التشغيل بحساب نطاق (domain)"

    لا يملك `LocalSystem` هوية على الشبكة، لذا ستفشل مصادقة Windows (Windows Authentication) مع SQL Server
    وأي وصول إلى مجلد مشترك على الشبكة. ثبّت الخدمة مع `--account` و`--password` عندما تحتاج
    الخدمة إلى الوصول إلى الموارد بصفة مستخدم محدد.

### بدء وإيقاف الخدمة

#### لبدء الخدمة

```bash
digna windows start
```

#### لإيقاف الخدمة

```bash
digna windows stop
```

!!! tip "نصيحة"

    أوقف دائمًا الخدمة قبل تحديث ملفات التطبيق.

### نقل الخدمة إلى دليل جديد

إذا احتجت إلى نقل تثبيت digna:

1. **أوقف الخدمة الحالية وألغِ تسجيلها**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **نقل ملفات التطبيق**
   - انقل مجلد تثبيت digna بالكامل إلى الموقع الجديد

3. **سجّل الخدمة مجددًا من الموقع الجديد**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   كرّر أي قيم `--address` أو `--port` أو `--account` استخدمتها في المرة الأولى — فالتسجيل
   السابق قد أُزيل.

4. **بدء الخدمة**
   ```bash
   digna windows start
   ```

### إلغاء تثبيت الخدمة

1. **أوقف الخدمة الجارية**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **ألغِ تسجيل الخدمة**
   ```bash
   digna windows uninstall
   ```

تم الآن إلغاء تسجيل خادم digna كخدمة Windows.

---

## الترقية إلى إصدار جديد {: #upgrading-to-a-new-release }

### قبل الترقية

**تحقق أولًا من جميع اتصالات قواعد البيانات**

ابتداءً من الإصدار 2026.06، يصل digna إلى كل تقنية مصدر عبر **ODBC**. كانت الإصدارات السابقة تتيح الاختيار بين برنامج تشغيل خاص بكل تقنية وبين ODBC، عبر المفتاح **Use ODBC**. قرر فريق digna الاعتماد على ODBC وحده، لأن واجهة قياسية واحدة تقدّم أكثر مما تقدّمه مجموعة من برامج التشغيل المصممة خصيصًا:

- **المصادقة** — المصادقة جزء من ODBC، لذا يمكن للاتصال استخدام كل ما يدعمه برنامج التشغيل الخاص به: كلمات المرور، والرموز المميزة و PAT، وKerberos وActive Directory، والمصادقة متعددة العوامل وتسجيل الدخول الموحّد عبر المتصفح، وهويات السحابة، وشهادات العميل وTLS. تصل الطرق الجديدة مع تحديث برنامج التشغيل، بدلًا من انتظار إصدار من digna.
- **برامج تشغيل تتولى صيانتها شركات قواعد البيانات** — يتابع برنامج التشغيل الخاص بالشركة المصنّعة إصدارات الخادم الجديدة والإصلاحات الأمنية، ويمكنك تحديثه وفق جدولك الخاص وبمعزل عن digna.
- **طريقة واحدة لتهيئة كل شيء** — كل تقنية هي قائمة من خصائص المفتاح/القيمة، بالواجهة نفسها، وتشفير القيم الحساسة نفسه، وأسلوب استكشاف الأخطاء نفسه، بدلًا من مجموعة حقول مختلفة لكل مصدر.
- **الضبط والاتساع** — خيارات برنامج التشغيل مثل المهل الزمنية وإعدادات TLS والوسطاء وأحجام الجلب متاحة لكل مصدر، ويمكن توصيل أي تقنية لديها برنامج تشغيل ODBC متوافق، بما في ذلك تلك التي لا ينشر digna دليلًا خاصًا بها.

عمليًا يعني ذلك أن المفتاح **Use ODBC** والحقول المنفصلة للمضيف والمنفذ وقاعدة البيانات والمستخدم وكلمة المرور لم تعد موجودة. **كل اتصال لا يستخدم ODBC بالفعل يجب تحويله إلى ODBC** — لا يوجد تحويل تلقائي، لذا خطّط لذلك قبل الترقية:

1. راجع كل اتصال بقاعدة بيانات مُعرَّف في تثبيتك ودوّن الاتصالات التي لا تستخدم ODBC بعد — كل منها يحتاج إلى إعادة تهيئة.
2. ثبّت برنامج تشغيل ODBC المناسب على مضيف digna — تُفتح الاتصالات من الخادم الذي يشغّل الواجهة الخلفية لـ digna، لا من المتصفح. انظر [تثبيت برنامج تشغيل ODBC على مضيف digna](../../../databases/overview.md#install-the-driver).
3. جهّز خصائص ODBC لكل اتصال متأثر. [أدلة التقنيات](../../../databases/overview.md#technology-guides) تسرد لكل مصدر مجموعة خصائص مجرَّبة.

بعد الترقية، حوّل كل اتصال متأثر إلى ODBC واختبره من لوحة المعلومات — انظر [إنشاء اتصال بقاعدة بيانات](../../../databases/overview.md#create-a-database-connection) و [اختبار اتصال](../../../databases/overview.md#testing-a-connection).

!!! warning "اتصالات Databricks Legacy"

    أُزيل موصل Databricks Legacy في هذا الإصدار. انقل تلك الاتصالات إلى موصل [Databricks](../../../databases/databricks_connector_guide.md).

إنشاء نسخة احتياطية من مستودع digna إلزامي

قبل ترقية digna، احفظ نسخة احتياطية من المستودع (PostgreSQL) للحماية من فقدان البيانات.
النسخة الاحتياطية تضمن إمكانية الاسترجاع إذا واجهت الترقية مشكلات غير متوقعة.

### عملية الترقية

#### الخطوة 1: أوقف الخدمة القديمة وألغِ تسجيلها

إذا كانت digna تعمل كخدمة Windows، أوقفها باستخدام **ملفات الدُفعات الخاصة بتثبيتك
الحالي** — فأوامر `digna windows` تنتمي إلى الإصدار الجديد وليست متاحة
بعد:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

ثم ألغِ تسجيل الخدمة، مرة أخرى باستخدام ملف الدُفعات القديم. يشير التسجيل إلى الملف
التنفيذي القديم وسكربتاته، وكلاهما تستبدلهما هذه الترقية، لذا لا يمكن إعادة استخدامه:

```bash
uninstall_service.bat
```

!!! warning "ألغِ التسجيل قبل أن تعيد تسمية أي شيء"

    يوجد `uninstall_service.bat` في مجلد `bin` الذي أنت على وشك إعادة تسميته، وهو الشيء الوحيد
    القادر على إزالة التسجيل الذي أنشأه. نفّذه بينما لا يزال التثبيت القديم في مكانه.
    إذا كان المجلد قد أُعيدت تسميته بالفعل، فأعد اسمه الأصلي، وألغِ التسجيل، ثم تابع.

    دوّن الحساب الذي كانت الخدمة تعمل به، والعنوان والمنفذ اللذين كانت تخدم عليهما — ستحتاج
    إليها في الخطوة 7.

#### الخطوة 2: انسخ التثبيت الحالي احتياطيًا

في دليل تثبيت digna، أعد تسمية مجلدات التثبيت الحالي حتى يمكن نشر الإصدار الجديد بجوارها:

```bash
# Rename the folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename the folder containing dignacli
ren dignacli dignacli_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

!!! info "لم يعد dignabackend وdignacli مستخدمَين"

    ابتداءً من الإصدار 2026.06، يحل الملف التنفيذي الواحد `digna` محل `dignabackend` و`dignacli`، وهو يجمع الواجهة الخلفية وواجهة سطر الأوامر. احتفظ بـ `dignabackend_old` و`dignacli_old` فقط حتى تتحقق من الترقية — بعدها يمكنك حذف المجلدين. احتفظ بـ `dashboard_old` حتى تستعيد منه ملفات التهيئة الخاصة بك (انظر الخطوة 4). ويُحذف مجلد `bin` أيضًا: فملفات الدُفعات فيه كانت تشغّل الخدمة القديمة، والإصدار 2026.06 لا يتضمنها، لذا بعد إلغاء تسجيل الخدمة في الخطوة 1 لا تفعل شيئًا سوى التضليل.

#### الخطوة 3: فك واستخراج الإصدار الجديد

1. فك ضغط ملف ZIP الخاص بالإصدار الجديد من digna
2. انسخ الملف التنفيذي الجديد `digna` ومجلد `dashboard` إلى دليل التثبيت الخاص بك


!!! warning "مهم"

    لا يُضمَّن `config.toml` ولا `dashboard/dashboard_config.toml` أبدًا في
    أرشيف ZIP الخاص بالتثبيت — فريق digna لا يرسل أيًّا من الملفين أبدًا. لذلك تبقى تهيئتك الحالية
    بمنأى عن الترقية، والنسخ الموجودة في المجلدات المعاد تسميتها `*_old` هي
    النسخ الوحيدة التي لديك.

#### الخطوة 4: استعادة ملفات التكوين الخاصة بك

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
!!! warning "الإصدار 2026.06 يغيّر الملف config.toml"

    ثلاثة إعدادات جديدة وإلزامية، وثلاثة لم تعد مستخدمة. الملف `config.toml` المنقول من إصدار سابق لا يحتوي على الإعدادات الجديدة، ولن يبدأ digna ما دامت مفقودة. أضف ما يلي إلى ملف `config.toml` الحالي:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    أضف مفتاحَي `[base]` إلى قسم `[base]` الحالي، وأضف `[encryption]` كقسم جديد. ثم احذف الإعدادات التي لم تعد مستخدمة: **`digna_FERNET_KEY`** من `[base]`، و**`digna_APP_HOST`** و**`digna_APP_PORT`** من `[app]` — إذ صار الخادم يأخذ عنوانه ومنفذه من `digna serve`.

    ما تفعله كل إعداد موضّح في [تهيئة الواجهة الخلفية](#backend-configuration).

!!! warning "الدخول الموحّد: تغيّرت صيغة [oidc_clients]"

    يستبدل الإصدار 2026.06 مصفوفة الجداول بجدول واحد لكل مزوّد، يحمل اسم مفتاح المزوّد. أُلغي `DIGNA_OIDC_KEY` — فالمفتاح صار جزءًا من عنوان القسم.

    قبل:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    بعد:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    كرّر القسم لكل مزوّد، وأبقِ كل مفتاح مطابقًا لـ `key` في `dashboard_config.toml`. يُبلغ `digna config check` عن `oidc_clients` بحالة FAILED ما دامت الصيغة القديمة قائمة. لا يتأثر بذلك سوى التثبيتات التي تستخدم الدخول الموحّد.

#### الخطوة 5: إعادة تحميل خادم الويب

اللوحة عبارة عن مجموعة من الملفات الثابتة، لذا قد يظل خادم الويب — والمتصفح — يقدّمان
الإصدار السابق. أعد تحميل أو أعد تشغيل خادم الويب الذي يستضيف مجلد `dashboard`،
ثم أعد تحميل الصفحة بتحديث كامل (++ctrl+f5++).

#### الخطوة 6: تحقق من التهيئة

تأكد من أن ملف `config.toml` المحدَّث مكتمل قبل أن تمسّ المستودع:

```bash
digna config check
```

يجب أن يُبلِّغ كل قسم بحالة OK. صحّح كل ما يُبلَّغ عنه بحالة FAILED، وأعد تنفيذ الأمر قبل المتابعة.

#### الخطوة 7: استبدال ملف الترخيص

يُرخَّص كل إصدار على حدة. انسخ ملف `license.toml` الذي قدّمه فريق digna لهذا
الإصدار إلى دليل التثبيت، ليحل محل الملف القديم:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "لا تحتفظ بالترخيص السابق"

    ملف `license.toml` الصادر لإصدار سابق لا يغطي هذا الإصدار، وكل أمر
    يتحقق من الترخيص — `user` و`inspection` و`repo` — يتوقف قبل أن يمسّ
    المستودع عند فشل التحقق. تحقّق منه قبل المتابعة:

    ```bash
    digna license check
    ```

#### الخطوة 8: ترقية مخطط المستودع

انتقل إلى دليل تثبيت digna ونفّذ:

```bash
digna repo upgrade
```

هذا يقوم بتحديث مخطط PostgreSQL إلى أحدث إصدار مع الحفاظ على جميع البيانات الموجودة.

#### الخطوة 9: سجّل الخدمة وشغّلها

أُزيل التسجيل القديم في الخطوة 1، لذا تُسجَّل الخدمة مجددًا — هذه المرة باستخدام
الملف التنفيذي `digna`، الذي لا يحتوي على ملفات دُفعات:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

أعطِ `--address` و`--port` القيم التي كانت الخدمة القديمة تخدم عليها، ما لم ترغب في القيم الافتراضية
الجديدة `127.0.0.1` و`8000`؛ فهي تُسجَّل في تسجيل الخدمة ولم تعد تُقرأ
من `config.toml`. أضف `--account` و`--password` إذا كانت الخدمة القديمة تعمل بحساب
نطاق (domain). انظر
[تشغيل digna كخدمة Windows](#running-digna-as-a-windows-service) للاطلاع على القائمة الكاملة
للخيارات.

إذا كانت تعمل يدويًا، أعد تشغيل الخادم:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

إذا كنت تستخدم IIS أو Tomcat، أعد تشغيل خادم الويب المعني.

#### الخطوة 10: التحقق من الترقية

1. ادخل إلى لوحة digna
2. تحقق من تحميل الواجهة بشكل صحيح
3. تفقد سجلات الخادم للتأكد من عدم وجود أخطاء
4. حوّل إلى ODBC كل اتصال لم يكن يستخدمه بعد، ثم اختبر جميع الاتصالات — انظر [اختبار اتصال](../../../databases/overview.md#testing-a-connection)