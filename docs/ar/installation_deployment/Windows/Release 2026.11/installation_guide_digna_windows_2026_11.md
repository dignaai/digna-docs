---
title: دليل التثبيت على Windows – إصدارة digna 2026.11 | وثائق digna
description: دليل خطوة بخطوة لتثبيت digna إصدار 2026.11 على Windows — متطلبات النظام، إعداد PostgreSQL، تكوين خادم الويب، إعداد الواجهة الخلفية واللوحة، تشغيل digna كخدمة Windows، والترقية من الإصدار 2026.06.
keywords: digna تثبيت ويندوز, دليل نشر digna, إعداد الواجهة الخلفية digna, تثبيت لوحة digna, إعداد postgresql, خدمة ويندوز digna, دليل ترقية digna
image: /assets/logo_square.png
---

# دليل التثبيت على Windows لإصدار digna 2026.11

**الإصدار:** 2026.11

**آخر تحديث:** 7 نوفمبر 2026


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

### ما الجديد في الإصدار 2026.11

يضيف هذا الإصدار digna Data Reconciliation، وdigna Agentic مع digna MCP Server، وdigna Engine الذي يستطيع إجراء تنميط البيانات (profiling) داخل digna والتحقق من التكامل المرجعي بين تقنيات قواعد بيانات مختلفة. راجع [ملاحظات الإصدار](../../../changelog/Release_202611.md) للتفاصيل الكاملة.

بالنسبة إلى التثبيت، يجلب الإصدار آلية جديدة لترحيل المستودع، وقسمًا اختياريًا `[duckdb]` في `config.toml` من أجل digna Engine، وملف ترخيص جديدًا. يتناول [قسم الترقية](#upgrading-to-a-new-release) كلًّا منها.

### تبحث عن macOS أو Linux؟

يغطي هذا الدليل Windows. للمنصات الأخرى، راجع [دليل التثبيت على macOS](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) أو [دليل التثبيت على Linux](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    اتصالات قواعد البيانات التي تستخدم digna Engine موقعًا للتنميط يُجرى تنميطها على مضيف
    digna نفسه. خطّط لذاكرة ومساحة قرص إضافيتين من أجلها، انظر
    [قسم \[duckdb\]](#duckdb-section).

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

يضبط هذا القسم مشاركة الموارد عبر المصادر (CORS) بين لوحة التحكم والواجهة الخلفية (backend):

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| المعامل | القيمة | ملاحظات |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | عناوين URL للوحة التحكم | عناوين URL التي تُقدَّم منها لوحة التحكم. تُرفض طلبات المتصفح الواردة من أي أصل آخر |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | مطلوب، كي يرسل المتصفح ملف تعريف ارتباط الجلسة مع كل طلب |

!!! info "القسم [app] اختياري"

    ابتداءً من الإصدار 2026.11، يمكن حذف المفتاحين، بل القسم `[app]` بأكمله. وهذا هو الإعداد
    الصحيح عندما يقدّم وكيل عكسي (reverse proxy) لوحة التحكم والواجهة الخلفية تحت أصل واحد: عندئذٍ
    لا يرسل المتصفح أي طلبات عبر المصادر، ولا يُسمح بأي منها افتراضيًا.

#### قسم [repo]

هذا القسم يضبط الاتصال بقاعدة بيانات PostgreSQL:

```toml
[repo]
DIGNA_REPO_HOST = "localhost"
DIGNA_REPO_PORT = 5432
DIGNA_REPO_DB = "postgres"
DIGNA_REPO_SCHEMA = "dignarepo"
DIGNA_REPO_USER = "digna_user"
DIGNA_REPO_PASSWORD = "YourSecurePassword123!"
DIGNA_REPO_SSLMODE = "prefer"
DIGNA_REPO_NUM_CONNS = 16
```

| المعامل | القيمة | ملاحظات |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` أو IP | اسم مضيف/عنوان IP خادم PostgreSQL |
| `DIGNA_REPO_PORT` | `5432` (افتراضي) | منفذ PostgreSQL |
| `DIGNA_REPO_DB` | `postgres` | اسم قاعدة البيانات |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | المخطط الذي تم إنشاؤه سابقًا |
| `DIGNA_REPO_USER` | `digna_user` | المستخدم الذي تم إنشاؤه في إعداد PostgreSQL |
| `DIGNA_REPO_PASSWORD` | كلمة مرورك | كلمة المرور التي تم تعيينها أثناء إنشاء المخطط |
| `DIGNA_REPO_SSLMODE` | `prefer` (افتراضي) | اختياري. وضع SSL في PostgreSQL: `disable` أو `allow` أو `prefer` أو `require` أو `verify-ca` أو `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (افتراضي) | اختياري. عدد الاتصالات التي يُبقيها digna مفتوحة مع المستودع |

#### قسم [base]

يحتوي هذا القسم على إعدادات الأمان وملفات تعريف الارتباط والفحص:

```toml
[base]
DIGNA_FERNET_KEY = "DU4a0yJ-OqvbKCL4hNQn_CsknH-V1vWmHZqBUl-AY44="
DIGNA_COOKIE_DOMAIN = "localhost"
DIGNA_COOKIE_SECURE = false
DIGNA_COOKIE_HTTPONLY = true
DIGNA_TOKEN_EXPIRES_IN = 86400
DIGNA_MAX_WORKERS = 4
DIGNA_FRONTEND_BASEURL = "http://localhost/"
DIGNA_SOURCE_QUERY_TIMEOUT_SEC = 3600
DIGNA_SOURCE_LOGIN_TIMEOUT_SEC = 30
```

| المعامل | القيمة | ملاحظات |
|---|---|---|
| `DIGNA_FERNET_KEY` | القيمة الموضحة أعلاه | مفتاح التشفير الذي استخدمته الإصدارات السابقة. يجب أن يكون موجودًا؛ احتفظ بالقيمة الموضحة |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | المضيف الذي يُوصَل عبره إلى لوحة التحكم. القيمة `""` لا تعيّن أي نطاق، وهذا هو الصحيح خلف وكيل يقدّم لوحة التحكم والواجهة الخلفية تحت أصل واحد |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | يجب أن تكون القيمة `true` كلما قُدِّم digna عبر HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | يُبقي ملف تعريف ارتباط الجلسة بعيدًا عن متناول السكربتات |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 ساعة) | مهلة الجلسة بالثواني |
| `DIGNA_MAX_WORKERS` | عدد أنوية CPU - 1 | عدد عمليات الفحص التي يمكن أن تعمل في الوقت نفسه |
| `DIGNA_FRONTEND_BASEURL` | عنوان URL للوحة التحكم | إلزامي. يُستخدم للروابط في رسائل الإشعارات، لذا يجب أن يكون عنوانًا يستطيع المستلمون فتحه |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (افتراضي) | اختياري. عدد الثواني التي يمكن أن يعمل خلالها استعلام واحد على قاعدة بيانات مصدر قبل إيقافه؛ القيمة `0` تعطّل المهلة |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (افتراضي) | اختياري. عدد ثواني انتظار الاتصال بقاعدة بيانات مصدر؛ القيمة `0` تعني الانتظار بلا حد |

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
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| المعامل | القيمة | ملاحظات |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` أو `DEBUG` | `INFO` للإنتاج، `DEBUG` لاستكشاف الأخطاء. تُقبل أيضًا القيم `TRACE` و`WARN` و`ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (افتراضي) | اختياري. دليل ملفات السجل المتناوبة، نسبةً إلى دليل العمل |
| `DIGNA_LOGGING_MAX_FILES` | `30` (افتراضي) | اختياري. عدد ملفات السجل المتناوبة التي يُحتفظ بها |

!!! warning "احتفظ بدليل السجلات عند التشغيل كخدمة"

    لا تملك خدمة Windows وحدة تحكم (console)، لذا فإن ملفات السجل هي السجل الوحيد لما تفعله
    الخدمة. لا تعيّن `DIGNA_LOGGING_DIR` إلى سلسلة فارغة، فذلك يوقف ملفات السجل.

#### قسم [duckdb] (اختياري) {: #duckdb-section }

جديد في الإصدار 2026.11. يحدد هذا القسم موارد **digna Engine**، الذي يُجري تنميط البيانات داخل
digna لاتصالات قواعد البيانات التي يكون موقع التنميط فيها **digna Engine**، ويُشغّل فحوصات التكامل
المرجعي بين مصادر بيانات موجودة على اتصالات قواعد بيانات مختلفة. انظر
[موقع التنميط](../../../platform/profiling/profiling_location.md).

هذا القسم اختياري. من دونه تُطبَّق القيم الافتراضية أدناه.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| المعامل | القيمة | ملاحظات |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (افتراضي) | الذاكرة بالميغابايت التي يمكن أن يستخدمها تشغيل واحد لـ digna Engine. يمكن أن يكون ما يصل إلى `DIGNA_MAX_WORKERS` من عمليات التشغيل نشطًا في الوقت نفسه |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | الافتراضي: الدليل المؤقت للحساب الذي يشغّل digna (`%TEMP%`) | دليل الملفات المؤقتة عندما لا تتسع الذاكرة للبيانات |

!!! tip "تحديد حجم digna Engine"

    خطّط لما يصل إلى `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` من الذاكرة على مضيف
    digna، فوق ما يستخدمه digna نفسه، ولمساحة قرص حرة كافية في الدليل المؤقت تتسع لأكبر تاريخ
    مفحوص من مصادر البيانات التي تستخدم digna Engine. وجّه `DIGNA_DUCKDB_TEMP_DIRECTORY` إلى قرص
    تتوفر فيه هذه المساحة ويستطيع الحساب الذي يشغّل digna الكتابة فيه:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    لا تحتاج إلى هذا القسم إلا إذا كان اتصال واحد على الأقل بقاعدة بيانات يستخدم digna Engine، أو كان
    فحص تكامل مرجعي يقارن مصادر بيانات موجودة على اتصالات مختلفة.

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
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

صحّح كل ما يُبلَّغ عنه بحالة FAILED، وأعد تنفيذ الأمر قبل المتابعة. يسرد WARNING تحت **Unknown keys** المفاتيح الموجودة في `config.toml` التي لا يقرؤها digna؛ ليس لها أي تأثير، لذا احذفها أو صحّح تهجئتها. القائمة الكاملة للخيارات موجودة في [مرجع CLI](../../../cli/Command_Line_Interface_202611.md).

### الخطوة 3: تهيئة المستودع

1. افتح موجه الأوامر
2. انتقل إلى دليل تثبيت digna الخاص بك (حيث يوجد `config.toml` والملف التنفيذي `digna`)
3. شغّل اختبار الاتصال:

```bash
digna repo check
```

على مخطط جديد، يتصل الأمر ثم يُبلغ بأنه لا يوجد مستودع مثبّت بعد:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

في هذه المرحلة هذه هي النتيجة المتوقعة: فهي تؤكد أن digna يصل إلى PostgreSQL وإلى المخطط. أما خطأ الاتصال أو المصادقة فيشير بدلًا من ذلك إلى القسم `[repo]` أو إلى إعداد PostgreSQL.

### الخطوة 4: تثبيت مخطط المستودع

في نفس الدليل، نفّذ:

```bash
digna repo upgrade
```

يُثبّت هذا الأمر الجداول اللازمة في مخطط المستودع وينتهي بالرسالة:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "الأمر repo upgrade يثبّت ويرقّي"

    ابتداءً من الإصدار 2026.11، يثبّت `repo upgrade` مستودعًا جديدًا ويرقّي مستودعًا موجودًا.
    ولا يزال `repo install` يعمل كاسم آخر للأمر نفسه.

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
- `--address` — اسم المضيف/عنوان IP للخادم (الافتراضي `127.0.0.1`)
- `--port` — منفذ الخادم (الافتراضي `8000`)

عندما يعمل الخادم، يطبع العنوان الذي يستمع عليه:

```text
Server running on http://127.0.0.1:8082
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
للخيارات موجودة في [مرجع CLI](../../../cli/Command_Line_Interface_202611.md).

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

يشرح هذا القسم ترقية تثبيت الإصدار 2026.06 إلى الإصدار 2026.11.

!!! warning "الترقية من إصدار أقدم من 2026.06"

    نفّذ أولًا خطوات الترقية إلى الإصدار 2026.06: [الترقية إلى إصدار جديد](../Release%202026.06/installation_guide_digna_windows_2026_06.md#upgrading-to-a-new-release). ثم تابع بالخطوات أدناه.

### قبل الترقية

**النسخ الاحتياطي لمستودع digna إلزامي**

قبل ترقية digna، اعمل نسخة احتياطية من مستودعك (PostgreSQL) لحماية بياناتك من الضياع.
النسخة الاحتياطية تضمن إمكانية الاسترداد إذا واجهت الترقية مشكلات غير متوقعة.

**طلب ملف الترخيص للإصدار 2026.11**

يحتاج الإصدار 2026.11 إلى ملف `license.toml` جديد. اطلبه من فريق digna قبل أن تبدأ، واجعله
جاهزًا لـ [الخطوة 7](#step-7-replace-the-license-file).

### عملية الترقية

#### الخطوة 1: إيقاف خدمة digna {: #step-1-stop-the-digna-service }

افتح موجه الأوامر (Command Prompt) كمسؤول (Administrator) وأوقف الخدمة باستخدام الملف التنفيذي
`digna` من تثبيتك الحالي:

```bash
cd C:\path\to\digna
digna windows stop
```

تبقى الخدمة مسجّلة. يحل الملف التنفيذي الجديد محل القديم في الدليل نفسه، لذا يظل التسجيل
يشير إلى الملف الصحيح.

إذا كان digna يعمل في المقدمة (foreground)، اضغط ++ctrl+c++ في نافذة موجه الأوامر الخاصة به.

#### الخطوة 2: انسخ التثبيت الحالي احتياطيًا {: #step-2-backup-current-installation }

في دليل تثبيت digna، أعد تسمية الملف التنفيذي ومجلد لوحة التحكم في تثبيتك الحالي، حتى
يمكن نشر الإصدار الجديد بجوارهما:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

احتفظ بـ `digna_old.exe` حتى تتحقق من الترقية، وبـ `dashboard_old` حتى تستعيد منه ملفات التهيئة
الخاصة بك (انظر الخطوة 4). بعد ذلك يمكنك حذفهما.

#### الخطوة 3: فك ونشر النسخة الجديدة {: #step-3-extract-and-deploy-new-version }

1. فك ملف ZIP للنسخة الجديدة من digna
2. انسخ الملف التنفيذي الجديد `digna` ومجلد `dashboard` إلى دليل التثبيت

!!! warning "مهم"

    لا يُضمَّن `config.toml` ولا `dashboard/dashboard_config.toml` أبدًا في
    أرشيف ZIP الخاص بالتثبيت — فريق digna لا يرسل أيًّا من الملفين أبدًا. لذلك تبقى تهيئتك الحالية
    بمنأى عن الترقية، والنسخ الموجودة في المجلدات المعاد تسميتها `*_old` هي
    النسخ الوحيدة التي لديك.

#### الخطوة 4: استعادة ملفات التهيئة الخاصة بك {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

لا يحتاج الإصدار 2026.11 إلى أي تغيير في `config.toml`: الملف الذي يعمل مع الإصدار 2026.06 يظل
يعمل. هناك تغييران اختياريان:

- أضف [قسم `[duckdb]`](#duckdb-section) إذا كانت اتصالات قواعد البيانات ستستخدم digna Engine
  ولم تكن قيمه الافتراضية مناسبة لمضيفك.
- احذف القسم `[app]` إذا كان وكيل عكسي يقدّم لوحة التحكم والواجهة الخلفية تحت أصل
  واحد.

!!! warning "إعدادات لا يقرؤها digna"

    عرضت نسخ سابقة من هذا الدليل بعض الإعدادات التي لا يقرؤها digna. ليس لها أي تأثير،
    ويسردها `config check` تحت **Unknown keys** في الخطوة 6. احذفها أو صحّحها:

    - `DIGNA_SCHEDULER_MAX_DELAY` و`DIGNA_CLEANUP_TIME` و`digna_COOKIE_PATH`
      و`digna_COOKIE_SAME_SITE` و`digna_APP_CORS_ALLOW_METHODS` و`digna_APP_CORS_ALLOW_HEADERS`
      و`digna_LOGGING_BACKUP_COUNT` غير موجودة. احذفها.
    - أسماء الإعدادات حساسة لحالة الأحرف. يقرأ digna `DIGNA_REPO_HOST`، لا `digna_REPO_HOST`.
      اكتب كل اسم بأحرف كبيرة، كما في [تكوين الخلفية (Backend)](#backend-configuration).

!!! warning "الدخول الموحّد: أبقِ على [[oidc_clients]]"

    يقرأ digna مزوّدي الدخول الموحّد كقائمة من إدخالات `[[oidc_clients]]`، لكلٍّ منها
    `DIGNA_OIDC_KEY` الخاص به. إذا كنت قد حوّلت مزوّديك إلى أقسام `[oidc_clients.<key>]`، كما عرضت
    نسخة سابقة من هذا الدليل، فأعدها إلى الصيغة السابقة. يُبلغ `config check` عن
    `OIDC config(s)` بحالة FAILED ما دامت تلك الصيغة قائمة:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    كرّر الإدخال لكل مزوّد، وأبقِ كل `DIGNA_OIDC_KEY` مطابقًا لـ `key` في
    `dashboard_config.toml`. لا يتأثر بذلك سوى التثبيتات التي تستخدم الدخول الموحّد.

#### الخطوة 5: إعادة تحميل خادم الويب {: #step-5-reload-the-web-server }

لوحة التحكم عبارة عن مجموعة من الملفات الثابتة، لذا قد يظل خادم الويب — والمتصفح — يقدّمان
الإصدار السابق. أعد تحميل أو أعد تشغيل خادم الويب الذي يستضيف مجلد `dashboard`،
ثم أعد تحميل الصفحة بتحديث كامل (++ctrl+f5++).

#### الخطوة 6: تحقق من التهيئة {: #step-6-validate-the-configuration }

تأكد من أن ملف `config.toml` مكتمل قبل أن تمسّ المستودع:

```bash
digna config check
```

يجب أن يُبلِّغ كل قسم بحالة OK. صحّح كل ما يُبلَّغ عنه بحالة FAILED، واحذف المفاتيح المدرجة تحت
**Unknown keys**، وأعد تنفيذ الأمر قبل المتابعة.

#### الخطوة 7: استبدال ملف الترخيص {: #step-7-replace-the-license-file }

ملف الترخيص الصادر لإصدار سابق لا يعمل مع الإصدار 2026.11. انسخ ملف `license.toml` الذي قدّمه
فريق digna للإصدار 2026.11 إلى دليل التثبيت، ليحل محل الملف القديم:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "لا تحتفظ بالترخيص السابق"

    مع الترخيص السابق يفشل كل أمر يتحقق من الترخيص — `serve` و`user` و`inspection` و`repo` —
    فلا يبدأ digna ولا يمكن ترقية المستودع. تحقّق من الترخيص الجديد قبل المتابعة:

    ```bash
    digna license check
    ```

#### الخطوة 8: ترقية مخطط المستودع {: #step-8-upgrade-the-repository-schema }

في دليل تثبيت digna، شغّل:

```bash
digna repo upgrade
```

يدير الإصدار 2026.11 مخطط المستودع بعمليات ترحيل ذات أرقام إصدارات (versioned migrations). أول ترقية
من إصدار سابق تنقل المخطط إلى آخر نسخة من الآلية السابقة، وتسجّل ذلك نقطةَ بداية له، ثم تطبّق
عمليات ترحيل الإصدار 2026.11. وتنتهي بالرسالة:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

تُحفظ جميع البيانات الحالية. لمعرفة حالة المستودع في أي وقت، شغّل
`digna repo check`: فهو يسرد آخر عملية ترحيل مطبّقة وأي عمليات ترحيل معلّقة.

!!! warning "لا يبدأ digna على مستودع قديم"

    ابتداءً من الإصدار 2026.11، يرفض الخادم البدء ما دام المستودع يحتاج إلى ترقية، ويُبلغ بذلك،
    على سبيل المثال:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    شغّل `repo upgrade` قبل أن تبدأ الخادم أو الخدمة.

#### الخطوة 9: إعادة تشغيل الخدمات {: #step-9-restart-services }

إذا كان digna يعمل كخدمة Windows، فشغّله مجددًا:

```bash
cd C:\path\to\digna
digna windows start
```

إذا كنت تشغّله يدويًا، أعد تشغيل الخادم:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

إذا كنت تستخدم IIS أو Tomcat، أعد تشغيل خادم الويب المعني.

#### الخطوة 10: التحقق من الترقية {: #step-10-verify-the-upgrade }

1. تأكد من إصدار الملف التنفيذي الجديد:

    ```bash
    digna version
    ```

    يجب أن يكون السطر الأول `Release: 2026.11`.

2. افتح لوحة digna وتحقق من تحميل الواجهة بشكل صحيح.
3. تحقق من الملفات في الدليل `logs` الخاص بالتثبيت بحثًا عن أخطاء.
4. اختبر اتصالات قواعد البيانات — انظر
   [اختبار اتصال](../../../databases/overview.md#testing-a-connection).

للبدء مع الوحدات الجديدة، انظر [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md)،
و[ربط وكيل ذكاء اصطناعي](../../../platform/agentic/connect_ai_agent.md) من أجل digna MCP Server،
و[موقع التنميط](../../../platform/profiling/profiling_location.md) من أجل digna Engine.
