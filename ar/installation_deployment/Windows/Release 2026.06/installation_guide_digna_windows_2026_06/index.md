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

- **dignabackend**: المحرك الأساسي للتطبيق، المسؤول عن معالجة البيانات وتنفيذ فحوصات الجودة.
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
   - `config.toml` — ملف التكوين
   - `license.toml` — ملف الترخيص (انسخ ملف الترخيص الخاص بك هنا)

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
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| المعامل | القيمة | ملاحظات |
|---|---|---|
| `digna_APP_HOST` | `localhost` أو عنوان IP | اسم المضيف أو IP الذي يستضيف dignabackend |
| `digna_APP_PORT` | `8082` (افتراضي) | المنفذ لنقاط نهاية واجهة برمجة التطبيقات REST |
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
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| المعامل | القيمة | ملاحظات |
|---|---|---|
| `digna_FERNET_KEY` | مفتاح التشفير | يستخدم لتشفير الرموز وملفات تعريف الارتباط (يوجد افتراضي) |
| `digna_COOKIE_DOMAIN` | `localhost` | طابق مع نطاق الواجهة الأمامية |
| `digna_COOKIE_SECURE` | `false` (محلي) / `true` (إنتاج) | استخدم `true` للاتصالات عبر HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | مُمكّن دائمًا لأغراض الأمان |
| `digna_COOKIE_SAME_SITE` | `lax` | يساعد في منع هجمات CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ساعة) | مهلة الجلسة بالثواني |
| `digna_MAX_WORKERS` | عدد أنوية المعالج - 1 | عدد مهام الفحص المتوازية |

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

### الخطوة 5: بدء خادم digna

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

### الخطوة 6: إنشاء مستخدم مسؤول

1. افتح نافذة موجه أوامر **جديدة**
2. انتقل إلى دليل تثبيت digna الخاص بك
3. شغّل الأمر التالي لإنشاء مستخدم مسؤول:

```bash
digna user add <username> "<full_name>" <password> --su
```

**مثال:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

سيُنشئ هذا مستخدمًا بصلاحيات إدارية كاملة.

!!! tip "أفضل الممارسات"

    استخدم كلمة مرور قوية تشتمل على أحرف كبيرة وصغيرة وأرقام ورموز خاصة.

---

## تكوين اللوحة {: #dashboard-configuration }

### الخطوة 1: نشر اللوحة على خادم الويب

للوحة digna ملف `config.toml` منفصل موجود في مجلد `dashboard/`. هذا التكوين مُقدَّم بالفعل ولا يتطلب تغييرات أثناء الإعداد الأولي. تحتاج لتعديله فقط إذا رغبت في تخصيص اتصال الواجهة الخلفية.

إذا كنت بحاجة لتعديل تكوين اللوحة (مثلاً لنشر متعدد الحركات)، ارجع إلى وثائق اللوحة.

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

### ملفات إدارة الخدمة

تقع جميع الملفات اللازمة في دليل تثبيت digna تحت: `bin/`

ملفات الدُفعات (batch) المتاحة:
- `install_service.bat` — يسجل digna كخدمة Windows
- `uninstall_service.bat` — يلغي تسجيل الخدمة
- `start_service.bat` — يشغل الخدمة المسجلة
- `stop_service.bat` — يوقف الخدمة المسجلة

!!! warning "يتطلب صلاحيات المسؤول"

    يجب تنفيذ جميع ملفات الدُفعات بصلاحيات Administrator.

### تثبيت الخدمة

1. **افتح موجه الأوامر كمسؤول**
   - انقر بزر الماوس الأيمن على Command Prompt
   - اختر "Run as Administrator"

2. **انتقل إلى مجلد bin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **شغّل سكربت التثبيت**
   ```bash
   install_service.bat
   ```

تم الآن تسجيل خادم digna كخدمة Windows مع تمكين التشغيل التلقائي. الخدمة لا تبدأ فورًا — راجع القسم التالي لبدئها.

### بدء وإيقاف الخدمة

#### لبدء الخدمة

1. افتح موجه الأوامر كمسؤول
2. انتقل إلى `digna\bin`
3. نفّذ:
   ```bash
   start_service.bat
   ```

#### لإيقاف الخدمة

1. افتح موجه الأوامر كمسؤول
2. انتقل إلى `digna\bin`
3. نفّذ:
   ```bash
   stop_service.bat
   ```

!!! tip "نصيحة"

    أوقف دائمًا الخدمة قبل تحديث ملفات التطبيق.

### نقل الخدمة إلى دليل جديد

إذا احتجت إلى نقل تثبيت digna:

1. **إلغاء تثبيت الخدمة الحالية**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **نقل ملفات التطبيق**
   - انقل مجلد تثبيت digna بالكامل إلى الموقع الجديد

3. **إعادة تثبيت الخدمة**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **بدء الخدمة**
   ```bash
   start_service.bat
   ```

### إلغاء تثبيت الخدمة

1. **أوقف الخدمة الجارية**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **إلغاء تثبيت الخدمة**
   ```bash
   uninstall_service.bat
   ```

تم الآن إلغاء تسجيل خادم digna كخدمة Windows.

---

## الترقية إلى إصدار جديد {: #upgrading-to-a-new-release }

### قبل الترقية

إنشاء نسخة احتياطية من مستودع digna إلزامي

قبل ترقية digna، احفظ نسخة احتياطية من المستودع (PostgreSQL) للحماية من فقدان البيانات.
النسخة الاحتياطية تضمن إمكانية الاسترجاع إذا واجهت الترقية مشكلات غير متوقعة.

### عملية الترقية

#### الخطوة 1: إيقاف خدمة digna

إذا كانت digna تعمل كخدمة Windows، أوقفها أولاً:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### الخطوة 2: نسخ احتياطي للتثبيت الحالي للواجهة الخلفية

في دليل تثبيت digna:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### الخطوة 3: فك واستخراج الإصدار الجديد

1. فك ضغط ملف ZIP الخاص بالإصدار الجديد من digna
2. انسخ الملف التنفيذي الجديد `digna` ومجلد `dashboard` إلى دليل التثبيت الخاص بك


!!! warning "مهم"

    ملف `config.toml` **غير** مشمول أبدًا في ملف ZIP للتثبيت. يظل تكوينك الحالي آمنًا.

### الخطوة 4: استعادة ملفات التكوين الخاصة بك

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### الخطوة 5: ترقية مخطط المستودع

انتقل إلى دليل تثبيت digna ونفّذ:

```bash
digna repo upgrade
```

هذا يقوم بتحديث مخطط PostgreSQL إلى أحدث إصدار مع الحفاظ على جميع البيانات الموجودة.

### الخطوة 6: إعادة تشغيل الخدمات

إذا كانت تعمل كخدمة Windows:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

إذا كانت تعمل يدويًا، أعد تشغيل الخادم:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

إذا كنت تستخدم IIS أو Tomcat، أعد تشغيل خادم الويب المعني.

#### الخطوة 7: التحقق من الترقية

1. ادخل إلى لوحة digna
2. تحقق من تحميل الواجهة بشكل صحيح
3. تفقد سجلات الخادم للتأكد من عدم وجود أخطاء