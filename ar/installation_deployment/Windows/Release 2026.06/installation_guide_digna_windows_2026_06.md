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
8. [تكوين اللوحة (Dashboard)](#dashboard-configuration)
9. [تشغيل digna كخدمة Windows](#running-digna-as-a-windows-service)
10. [الترقية إلى إصدار جديد](#upgrading-to-a-new-release)

---

## مقدمة {: #introduction }

### عن digna

digna هي منصة شاملة مدفوعة بالذكاء الاصطناعي مصممة لتحسين إدارة جودة البيانات عبر بيئات بيانات متنوعة مثل المستودعات، والبحيرات، والـ lakehouses. تم بناؤها لتكون قابلة للتوسع والتكيّف، وتتعامل digna مع تحديات البيانات الحديثة من خلال الأتمتة، والمراقبة في الوقت الحقيقي، والكشف عن الشذوذ.

تتكون digna من مكونين رئيسيين:

- **dignabackend**: المحرك الأساسي للتطبيق، المسؤول عن معالجة البيانات وإجراء فحوصات الجودة.
- **dignadashboard**: واجهة ويب مستضافة على خادم ويب، توفر طريقة سهلة للتفاعل مع منصة digna وتصوّر مقاييس جودة البيانات.

### ما الجديد في الإصدار 2026.06

يجلب هذا الإصدار قدرات رصد البيانات (data observability) مباشرة إلى الكود الخاص بك، مما يتيح للمطورين مراقبة جودة البيانات من المصدر. راجع [ملاحظات الإصدار](http://docs.digna.ai/changelog/Release_202606/) للتفاصيل الكاملة.

---

## متطلبات النظام {: #system-requirements }

قبل البدء بالتثبيت، تأكد من أن نظامك يفي بالحد الأدنى من المتطلبات التالية:

| Requirement | Specification |
|---|---|
| **Operating System** | Windows Server أو Windows 10/11 |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB متاح للتخزين |
| **Database** | PostgreSQL Server 12 أو أحدث |
| **Web Server** | IIS أو Apache Tomcat أو ما يعادله |

### خيارات تثبيت قاعدة البيانات

**إذا كان PostgreSQL مثبتًا بالفعل:**
يمكنك إضافة قاعدة بيانات جديدة لـ digna على خادم PostgreSQL الحالي لديك.

**إذا كنت تقوم بتثبيت PostgreSQL على نفس الجهاز الذي سيشغّل digna:**

!!! info "المواصفات الموصى بها"

    - **الذاكرة**: 32 GB RAM (بدلاً من 16 GB)
    - **مساحة التخزين**: 50 GB متاحة (بدلاً من 10 GB)

    هذه المواصفات الأعلى تستوعب تشغيل digna وقاعدة بيانات PostgreSQL في آنٍ واحد.

---

## إعداد ما قبل التثبيت {: #pre-installation-setup }

قبل تثبيت digna، تأكد من توفر متطلبين أساسيين:

1. **خادم PostgreSQL** – لتخزين المقاييس المحسوبة وبيانات الأداء
2. **خادم ويب** – لاستضافة لوحة digna

إذا لم تكن هذه المكونات مُعدة بالفعل، اتبع الأقسام أدناه لتثبيتها وتكوينها.

---

## إعداد خادم PostgreSQL {: #postgresql-server-setup }

### إذا كان PostgreSQL مثبتًا لديك بالفعل

إذا كان PostgreSQL مثبتًا ويعمل على جهازك المحلي أو إذا كنت تستخدم خادم PostgreSQL مُدار عن بُعد، يمكنك الانتقال إلى [القسم التالي](#web-server-configuration).

### تثبيت PostgreSQL

اتبع الخطوات التالية لتثبيت PostgreSQL على Windows:

#### الخطوة 1: تنزيل PostgreSQL

1. زر [صفحة تنزيلات PostgreSQL](https://www.postgresql.org/download/)
2. اختر **Windows**
3. حمّل أحدث برنامج التثبيت

#### الخطوة 2: تشغيل برنامج التثبيت

1. انقر نقرًا مزدوجًا على ملف برنامج التثبيت الذي تم تنزيله
2. اتبع التعليمات في معالج الإعداد

#### الخطوة 3: اختيار دليل التثبيت

اختر الدليل الذي سيتم تثبيت PostgreSQL فيه. الموقع الافتراضي عادةً مناسب.

#### الخطوة 4: اختيار المكونات

لإعداد قياسي، احتفظ بخيارات المكونات الافتراضية محددة.

#### الخطوة 5: تعيين كلمة مرور المستخدم الخارق لـ PostgreSQL

أدخل وأكد كلمة مرور لمستخدم PostgreSQL الخارق (`postgres`). **احفظ هذه الكلمة بأمان** — ستحتاجها لاحقًا.

#### الخطوة 6: تكوين رقم المنفذ

المنفذ الافتراضي لـ PostgreSQL هو `5432`. يمكنك استخدام الافتراضي أو تحديد منفذ آخر إذا لزم الأمر.

!!! tip "نصيحة"

    إذا كان المنفذ 5432 مستخدمًا بالفعل، اختر منفذًا بديلًا وسجّله للتكوين لاحقًا.

#### الخطوة 7: اختيار الإعدادات المحلية (Locale)

اختر الإعداد المحلي لقاعدة البيانات. الإعداد الافتراضي مناسب لمعظم الحالات.

#### الخطوة 8: إكمال التثبيت

انقر **Next** خلال الخطوات المتبقية، ثم انقر **Finish**.

#### الخطوة 9: التحقق من التثبيت

افتح موجه الأوامر وتحقق من تثبيت PostgreSQL:

```bash
psql --version
```

يجب أن ترى إصدار PostgreSQL إذا تم التثبيت بنجاح.

---

## تكوين خادم الويب {: #web-server-configuration }

تتطلب digna خادم ويب لاستضافة اللوحة (dashboard). اختر أحد الخيارات التالية:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

لا تحتاج إلى تثبيت أو تكوين إلا **واحد** من هذه الخوادم.

### إعداد IIS {: #iis-setup }

#### نظرة عامة

Internet Information Services (IIS) هو خادم الويب من Microsoft لاستضافة المواقع والتطبيقات الويب.

#### تفعيل IIS

1. **افتح لوحة التحكم**
   - اضغط `Win + R`
   - اكتب `control` واضغط Enter

2. **انتقل إلى ميزات Windows**
   - انقر **Programs**
   - اختر **Turn Windows features on or off**

3. **تفعيل Internet Information Services**
   - مرّر للأسفل وابحث عن **Internet Information Services (IIS)**
   - ضع علامة الاختيار لتفعيله
   - انقر على **+** لتوسيع وتحقق من تحديد المكونات الفرعية التالية:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **انقر OK** لتطبيق التغييرات

5. **التحقق من تثبيت IIS**
   - افتح متصفحك
   - انتقل إلى `http://localhost`
   - يجب أن ترى صفحة الترحيب الخاصة بـ IIS

#### مطلوب: مكوّن URL Rewrite

يتطلب IIS مكوّن URL Rewrite. حمّله وثبته من [صفحة Microsoft الرسمية](https://www.iis.net/downloads/microsoft/url-rewrite).

#### مطلوب: نوع MIME لملفات Markdown

لضمان تقديم ملفات Markdown (`.md`) بشكل صحيح عبر IIS:

1. افتح **IIS Manager** (اضغط `Win + R`، اكتب `inetmgr`، اضغط Enter)
2. انتقل إلى **Your Site > MIME Types**
3. انقر **Add...**
4. قم بالتكوين:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "مهم"

    بدون هذا الإعداد، قد لا تُقدَّم ملفات `.md` بشكل صحيح.

---

### إعداد Apache Tomcat {: #apache-tomcat-setup }

#### نظرة عامة

Apache Tomcat هو حاوية Java Servlet وخادم ويب مفتوح المصدر.

#### التثبيت

1. **تنزيل Apache Tomcat**
   - زر [صفحة تنزيلات Apache Tomcat](https://tomcat.apache.org/download-90.cgi)
   - حمّل توزيعة ZIP الخاصة بنظام Windows

2. **فك ضغط الأرشيف**
   - فك ضغط ملف ZIP إلى دليل على نظامك
   - مثال: `C:\Program Files\Apache Tomcat`

3. **التحقق من تشغيل Tomcat**
   - افتح متصفحك
   - انتقل إلى `http://localhost:8080`
   - يجب أن ترى صفحة الترحيب الخاصة بـ Apache Tomcat

!!! tip "نصيحة"

    عادةً ما يبدأ Apache Tomcat تلقائيًا بعد التثبيت. إذا لم يبدأ، انتقل إلى مجلد `bin` وشغّل `startup.bat`.

---

## التثبيت الأولي {: #initial-installation }

### الخطوة 1: إعداد مستودع digna

يخزن مستودع digna جميع المقاييس المحسوبة بواسطة digna. يعمل كمركز بيانات تحليلي وأداء.

#### إنشاء الـ Schema والمستخدم للمستودع

افتح عميل PostgreSQL الخاص بك (pgAdmin، psql، أو ما شابهه) ونفّذ أوامر SQL التالية:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**استبدل العناصر النائبة التالية:**

- `<digna_repo_schema>` — اسم الـ schema المرغوب (مثال: `dignarepo`)
- `<digna_repo_user>` — اسم المستخدم المرغوب (مثال: `digna_user`)
- `<digna_repo_password>` — كلمة مرور آمنة لهذا المستخدم

**مثال:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "أفضل الممارسات"

    استخدم كلمات مرور قوية ومعقدة لمستخدمي قواعد البيانات. تجنب بيانات اعتماد سهلة التخمين.

---

### الخطوة 2: فك حزمة تثبيت digna

1. حدّد ملف ZIP الخاص بتثبيت digna الذي تم تزويدك به
2. فك ضغطه إلى موقع التثبيت المرغوب
3. بعد فك الضغط، يجب أن ترى العناصر التالية:
   - `dashboard/` — واجهة الويب للوحة
   - `digna` — الملف التنفيذي الرئيسي (الواجهة الخلفية + CLI مدمجين)
   - `config.toml` — ملف التكوين
   - `license.toml` — ملف الترخيص (انسخ ملف الترخيص الخاص بك هنا)

### الخطوة 3: تثبيت ملف الترخيص

!!! warning "مهم"

    ملف الترخيص **غير** مضمن في حزمة التثبيت وسيتم تزويدك به بشكل منفصل من digna.

1. حدّد ملف `license.toml` الذي تم تزويدك به
2. انسخه إلى الدليل الجذري لتثبيت digna (حيث يوجد `config.toml` والملف التنفيذي `digna`)

**أهمية هذا الإجراء:**
يحتوي ملف الترخيص على معلومات العميل وتاريخ انتهاء الترخيص والتوقيع الرقمي. **لا تقم بتعديل هذا الملف** — أي تغييرات ستؤدي إلى إبطال صلاحيته.

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

يتم توفير ملف `config_template.toml` في دليل تثبيت digna. كل ما عليك هو إعادة تسميته إلى `config.toml`.

**الموقع:** `digna_installation/config.toml`

افتح `config.toml` في محرر نصوص وقم بتكوين كل قسم أدناه.

#### قسم [app]

هذا القسم يكوّن إعدادات تطبيق الواجهة الخلفية الخاصة بـ digna:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_APP_HOST` | `localhost` أو عنوان IP | اسم المضيف أو عنوان IP حيث يستضاف dignabackend |
| `digna_APP_PORT` | `8082` (افتراضي) | المنفذ لواجهات REST API |
| `digna_APP_CORS_ALLOW_ORIGINS` | عنوان الواجهة الأمامية | إذا كانت اللوحة على خادم مختلف، أضف عنوانها هنا |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | مطلوب عند استخدام CORS مع بيانات الاعتماد |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | السماح بجميع طرق HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | السماح بجميع رؤوس الطلب |

#### قسم [repo]

هذا القسم يكوّن الاتصال بقواعد بيانات PostgreSQL:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_REPO_HOST` | `localhost` أو IP | اسم مضيف/عنوان IP لخادم PostgreSQL |
| `digna_REPO_PORT` | `5432` (افتراضي) | منفذ PostgreSQL |
| `digna_REPO_DB` | `postgres` | اسم قاعدة البيانات |
| `digna_REPO_SCHEMA` | `dignarepo` | الـ schema التي قمت بإنشائها سابقًا |
| `digna_REPO_USER` | `digna_user` | المستخدم الذي تم إنشاؤه في إعداد PostgreSQL |
| `digna_REPO_PASSWORD` | كلمة مرورك | كلمة المرور التي تم تعيينها أثناء إنشاء الـ schema |

#### قسم [base]

يحتوي هذا القسم على إعدادات الأمان والكوكيز:

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

| Parameter | Value | Notes |
|---|---|---|
| `digna_FERNET_KEY` | مفتاح التشفير | يُستخدم لتشفير الرموز والكوكيز (يتم توفير قيمة افتراضية) |
| `digna_COOKIE_DOMAIN` | `localhost` | يجب أن يتوافق مع نطاق الواجهة الأمامية |
| `digna_COOKIE_SECURE` | `false` (محلي) / `true` (إنتاج) | استخدم `true` لاتصالات HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | مفعل دائمًا لأمان أفضل |
| `digna_COOKIE_SAME_SITE` | `lax` | يساعد في منع هجمات CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ساعة) | مدة انتهاء الجلسة بالثواني |
| `digna_MAX_WORKERS` | عدد أنوية CPU - 1 | عدد مهام الفحص المتوازية |

#### قسم [logging]

هذا القسم يكوّن سلوك تسجيل الدخول (اللوغات):

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` أو `DEBUG` | استخدم `INFO` للإنتاج، و`DEBUG` لاستكشاف الأخطاء |
| `digna_LOGGING_BACKUP_COUNT` | `10` | عدد النسخ الاحتياطية اليومية للوغز التي يتم الاحتفاظ بها |

---

### الخطوة 3: اختبار الاتصال بالمستودع

1. افتح موجه الأوامر
2. انتقل إلى دليل تثبيت digna (حيث يوجد `config.toml` والملف التنفيذي `digna`)
3. شغل اختبار الاتصال:

```bash
digna repo check
```

يجب أن ترى تأكيدًا بأن الاتصال تم إنشاؤه (المستودع نفسه لم يتم تهيئته بعد).

### الخطوة 4: تثبيت الـ Schema للمستودع

في نفس الدليل، شغّل:

```bash
digna repo install
```

يقوم هذا الأمر بتثبيت الجداول والـ schema اللازمة في قاعدة بيانات PostgreSQL الخاصة بك.

### الخطوة 5: تشغيل خادم digna

في دليل تثبيت digna، شغّل الخادم باستخدام:

```bash
digna serve --address <host> --port <port>
```

**المعلمات:**
- `--address` — اسم المضيف/عنوان IP للخادم
- `--port` — منفذ الخادم

يجب أن ترى رسائل بدء التشغيل تؤكد أن الخادم قيد التشغيل:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### الخطوة 6: إنشاء مستخدم إداري

1. افتح نافذة موجه أوامر **جديدة**
2. انتقل إلى دليل تثبيت digna
3. شغل الأمر التالي لإنشاء مستخدم إداري:

```bash
digna user add <username> "<full_name>" <password> --su
```

**مثال:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

سيُنشئ هذا مستخدمًا بصلاحيات إدارية كاملة.

!!! tip "أفضل الممارسات"

    استخدم كلمة مرور قوية تحتوي على مزيج من أحرف كبيرة وصغيرة وأرقام وحروف خاصة.

---

## تكوين اللوحة (Dashboard) {: #dashboard-configuration }

### الخطوة 1: نشر اللوحة إلى خادم الويب

للوحة digna ملف `config.toml` منفصل موجود داخل مجلد `dashboard/`. يتم توفير هذا التكوين مسبقًا ولا يتطلب تغييرات أثناء الإعداد الأولي. تحتاج إلى تعديله فقط إذا كنت بحاجة إلى تخصيص اتصال الواجهة الخلفية.

إذا احتجت لتعديل تكوين اللوحة (مثل نشر متعدد النسخ)، ارجع إلى توثيق اللوحة.

اختر خادم الويب الذي قمت بتثبيته واتبع خطوات النشر المقابلة.

#### النشر على IIS

1. **افتح IIS Manager**
   - اضغط `Win + R`، اكتب `inetmgr`، اضغط Enter

2. **إنشاء موقع ويب جديد**
   - في اللوحة اليسرى، انقر بزر الماوس الأيمن على **Sites**
   - اختر **Add Website...**

3. **تكوين الموقع**
   - **Site Name**: أدخل اسمًا (مثال: "dignaDashboard")
   - **Physical Path**: انقر Browse وحدد مجلد `dashboard`
   - **Binding**: اضبط عنوان IP والمنفذ (المنفذ الافتراضي 80 لـ HTTP، 443 لـ HTTPS)

4. **ابدأ الموقع**
   - انقر **OK** لإنشاء الموقع
   - انقر بزر الماوس الأيمن على الموقع الجديد واختر **Start**

5. **اختبار التثبيت**
   - افتح متصفحك
   - انتقل إلى `http://localhost` (أو عنوان URL الذي قمت بتكوينه)
   - يجب أن ترى صفحة تسجيل الدخول للوحة digna

#### النشر على Apache Tomcat

1. **نسخ اللوحة إلى Tomcat**
   - انسخ مجلد `dashboard` إلى دليل `webapps` الخاص بـ Tomcat
   - أعد تسميته إذا لزم الأمر (مثال: إلى `digna`)
   - مثال: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **التحقق من النشر**
   - حدّث أو أعد تحميل صفحة إدارة Tomcat (http://localhost:8080)
   - يجب أن ترى "digna" (أو الاسم الذي اخترته) مدرجًا ضمن التطبيقات المنشورة

3. **الوصول إلى اللوحة**
   - افتح متصفحك
   - انتقل إلى `http://localhost:8080/digna`
   - يجب أن ترى صفحة تسجيل الدخول للوحة digna

---

## تشغيل digna كخدمة Windows {: #running-digna-as-a-windows-service }

### لماذا استخدام خدمة Windows؟

تشغيل الواجهة الخلفية لـ digna كخدمة Windows يضمن أنها:
- تبدأ تلقائيًا عند إقلاع الخادم
- تعمل في الخلفية دون الحاجة إلى نافذة موجه أوامر مفتوحة
- تعيد التشغيل تلقائيًا عند حدوث تعطل
- يمكن إدارتها عبر خدمات Windows

### ملفات إدارة الخدمة

جميع الملفات اللازمة موجودة في دليل تثبيت digna تحت: `bin/`

ملفات الدُفعات (batch) المتاحة:
- `install_service.bat` — يسجل digna كخدمة Windows
- `uninstall_service.bat` — يزيل تسجيل الخدمة
- `start_service.bat` — يبدأ الخدمة
- `stop_service.bat` — يوقف الخدمة

!!! warning "مطلوب صلاحيات المسؤول"

    يجب تنفيذ جميع ملفات الدُفعات بامتيازات المسؤول (Administrator).

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
3. شغّل:
   ```bash
   start_service.bat
   ```

#### لإيقاف الخدمة

1. افتح موجه الأوامر كمسؤول
2. انتقل إلى `digna\bin`
3. شغّل:
   ```bash
   stop_service.bat
   ```

!!! tip "نصيحة"

    أوقف الخدمة دائمًا قبل تحديث ملفات التطبيق.

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

2. **إزالة تثبيت الخدمة**
   ```bash
   uninstall_service.bat
   ```

تم الآن إلغاء تسجيل خادم digna كخدمة Windows.

---

## الترقية إلى إصدار جديد {: #upgrading-to-a-new-release }

### قبل الترقية

**إنشاء نسخة احتياطية من مستودع digna أمر إلزامي**

قبل ترقية digna، قم بعمل نسخة احتياطية لمستودعك (PostgreSQL) لحماية البيانات من الفقدان.
النسخة الاحتياطية تضمن إمكانية الاسترجاع إذا حدثت مشكلات غير متوقعة أثناء الترقية.

### عملية الترقية

#### الخطوة 1: إيقاف خدمة digna

إذا كانت digna تعمل كخدمة Windows، أوقفها أولًا:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### الخطوة 2: نسخ احتياطي للتثبيت الحالي للواجهة الخلفية

في دليل تثبيت digna:

```bash
# إعادة تسمية المجلد المحتوي على dignabackend
ren dignabackend dignabackend_old
```
```bash
# إعادة تسمية لوحة العرض (dashboard)
ren dashboard dashboard_old
```

#### الخطوة 3: فك وتوزيع النسخة الجديدة

1. فك ضغط ملف ZIP الخاص بالإصدار الجديد من digna
2. انسخ الملف التنفيذي الجديد `digna` ومجلد `dashboard` إلى دليل التثبيت الخاص بك


!!! warning "مهم"

    ملف `config.toml` **غير** مضمن أبدًا في ملف ZIP للتثبيت. تبقى إعداداتك الحالية آمنة.

### الخطوة 4: استعادة ملفات التكوين الخاصة بك

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### الخطوة 5: ترقية مخطط المستودع (Repository Schema)

انتقل إلى دليل تثبيت digna وشغّل:

```bash
digna repo upgrade
```

سيقوم هذا بتحديث مخطط PostgreSQL إلى الإصدار الأحدث مع الحفاظ على جميع البيانات الحالية.

### الخطوة 6: إعادة تشغيل الخدمات

إذا كنت تعمل كخدمة Windows:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

إذا كنت تشغّل التطبيق يدويًا، أعد تشغيل الخادم:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

إذا كنت تستخدم IIS أو Tomcat، أعد تشغيل خادم الويب المقابل.

#### الخطوة 7: التحقق من الترقية

1. ادخل إلى لوحة digna
2. تأكد من تحميل الواجهة بشكل صحيح
3. افحص سجلات الخادم للتأكد من عدم وجود أخطاء