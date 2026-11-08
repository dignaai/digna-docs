---
title: دليل التثبيت على macOS – إصدار digna 2026.11 | توثيق digna
description: دليل خطوة بخطوة لتثبيت إصدار digna 2026.11 على macOS — متطلبات النظام، إعداد Homebrew و PostgreSQL، تكوين nginx أو Apache، إعداد الbackend واللوحة، تشغيل digna كخدمة في الخلفية، والترقية من الإصدار 2026.06.
keywords: تثبيت digna على macos, دليل نشر digna على ماك, إعداد backend digna, تثبيت لوحة digna, postgresql homebrew, nginx macos, خدمة launchd digna, دليل ترقية digna
image: /assets/logo_square.png
---

# دليل التثبيت على macOS لإصدار digna 2026.11

**الإصدار:** 2026.11

**آخر تحديث:** 7 نوفمبر، 2026


---

## جدول المحتويات

1. [مقدمة](#introduction)
2. [متطلبات النظام](#system-requirements)
3. [الإعداد قبل التثبيت](#pre-installation-setup)
4. [إعداد خادم PostgreSQL](#postgresql-server-setup)
5. [تكوين خادم الويب](#web-server-configuration)
6. [التثبيت الابتدائي](#initial-installation)
7. [تكوين الBackend](#backend-configuration)
8. [تكوين اللوحة](#dashboard-configuration)
9. [تشغيل digna كخدمة في الخلفية](#running-digna-as-a-background-service)
10. [الترقية إلى إصدار جديد](#upgrading-to-a-new-release)

---

## مقدمة {: #introduction }

### عن digna

digna هي منصة شاملة مدعومة بالذكاء الاصطناعي مصممة لتحسين إدارة جودة البيانات عبر بيئات بيانات متعددة مثل المخازن، والـ lakes، و lakehouses. بُنيت لتكون قابلة للتوسع والتكيف بدرجة عالية، وتتعامل digna مع تحديات البيانات الحديثة من خلال الأتمتة، والمراقبة في الوقت الفعلي، واكتشاف الشذوذ.

يتكون digna من مكوّنين رئيسيين:

- **digna**: نواة التطبيق، وهي المسؤولة عن معالجة البيانات وتنفيذ فحوص الجودة. تجمع الواجهة الخلفية وواجهة سطر الأوامر في ملف تنفيذي واحد، وتحل محل البرنامجين المنفصلين `dignabackend` و`dignacli` في الإصدارات السابقة.
- **dignadashboard**: واجهة ويب مستضافة على خادم ويب، توفّر طريقة سهلة للتفاعل مع منصة digna وعرض مقاييس جودة البيانات.

### الجديد في إصدار 2026.11

يضيف هذا الإصدار digna Data Reconciliation، وdigna Agentic مع digna MCP Server، وdigna Engine الذي يستطيع إجراء تنميط البيانات (profiling) داخل digna والتحقق من التكامل المرجعي بين تقنيات قواعد بيانات مختلفة. راجع [ملاحظات الإصدار](../../../changelog/Release_202611.md) للتفاصيل الكاملة.

بالنسبة إلى التثبيت، يجلب الإصدار آلية جديدة لترحيل المستودع، وقسمًا اختياريًا `[duckdb]` في `config.toml` من أجل digna Engine، وملف ترخيص جديدًا. يتناول [قسم الترقية](#upgrading-to-a-new-release) كلًّا منها.

### تبحث عن Windows أو Linux؟

يغطي هذا الدليل macOS. للمنصات الأخرى، راجع [دليل التثبيت على Windows](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) أو [دليل التثبيت على Linux](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## متطلبات النظام {: #system-requirements }

قبل البدء بالتثبيت، تأكد من أن النظام يلبي متطلبات الحد الأدنى التالية:

| المتطلب | المواصفة |
|---|---|
| **نظام التشغيل** | macOS 13 (Ventura) أو أحدث |
| **المعمارية** | Apple Silicon (arm64) أو Intel (x86_64) |
| **الذاكرة (إعداد أدنى)** | 16 غيغابايت RAM |
| **مساحة القرص** | 10 غيغابايت مساحة متاحة |
| **قاعدة البيانات** | PostgreSQL Server 12 أو أحدث |
| **خادم الويب** | nginx، Apache httpd، أو ما يعادله |
| **أدوات سطر الأوامر** | Xcode Command Line Tools (مطلوبة بواسطة Homebrew) |

!!! info "digna Engine"

    اتصالات قواعد البيانات التي تستخدم digna Engine موقعًا للتنميط يُجرى تنميطها على مضيف
    digna نفسه. خطّط لذاكرة ومساحة قرص إضافيتين من أجلها، انظر
    [قسم \[duckdb\]](#duckdb-section).

### خيارات تثبيت قاعدة البيانات

**إذا كان PostgreSQL مثبتًا بالفعل:**
يمكنك إضافة قاعدة بيانات جديدة لـ digna إلى خادم PostgreSQL الموجود لديك.

**إذا كنت تثبت PostgreSQL على نفس الجهاز الذي سيجري عليه تشغيل digna:**

!!! info "المواصفات الموصى بها"

    - **الذاكرة**: 32 غيغابايت RAM (بدلاً من 16 غيغابايت)
    - **مساحة القرص**: 50 غيغابايت مساحة متاحة (بدلاً من 10 غيغابايت)

    هذه المواصفات الأعلى تستوعب تشغيل digna و PostgreSQL معًا على الجهاز نفسه.

### التحقق من المعمارية الخاصة بك

تختلف العديد من المسارات في هذا الدليل بين أجهزة Apple Silicon و Intel. للتحقق من نوع المعالج، افتح **Terminal** وشغّل:

```bash
uname -m
```

- `arm64` — Apple Silicon. يثبت Homebrew في `/opt/homebrew`.
- `x86_64` — Intel. يثبت Homebrew في `/usr/local`.

!!! tip "نصيحة"

    بدلاً من ترميز أحد المسارين بشكل ثابت، يستخدم هذا الدليل `$(brew --prefix)`، التي تتوسع إلى الموقع الصحيح على كلتا المعماريتين. يمكنك نسخ الأوامر كما هي.

---

## الإعداد قبل التثبيت {: #pre-installation-setup }

قبل تثبيت digna، تأكد من وجود ثلاثة متطلبات أساسية:

1. **Homebrew** – مدير الحزم المستخدم لتثبيت المكوّنات أدناه
2. **PostgreSQL Server** – لتخزين المقاييس المحسوبة وبيانات الأداء
3. **خادم الويب** – لاستضافة لوحة digna

إذا لم تكن هذه المكوّنات مُعدة بالفعل، اتبع الأقسام أدناه لتثبيتها وتكوينها.

### تثبيت Homebrew

Homebrew هو مدير الحزم القياسي لنظام macOS ويُستخدم طوال هذا الدليل لتثبيت PostgreSQL و nginx.

#### الخطوة 1: تحقق مما إذا كان Homebrew مثبتًا بالفعل

افتح **Terminal** (اضغط `Cmd + Space`، اكتب `Terminal`، واضغط Enter) وشغّل:

```bash
brew --version
```

إذا تم إرجاع رقم إصدار، انتقل إلى قسم [إعداد خادم PostgreSQL](#postgresql-server-setup).

#### الخطوة 2: تثبيت Homebrew

إذا لم يتم العثور على الأمر، ثبّت Homebrew باتباع التعليمات على [موقع Homebrew الرسمي](https://brew.sh). يقوم المثبّت أيضًا بتثبيت Xcode Command Line Tools إذا لم تكن موجودة بالفعل.

#### الخطوة 3: أضف Homebrew إلى PATH

على Apple Silicon، يعرض المثبّت أمرين لإضافة Homebrew إلى بيئة الصدفة الخاصة بك. نفّذهما كما هو مذكور، ثم تأكد:

```bash
brew --prefix
```

يجب أن يعرض `/opt/homebrew` على Apple Silicon أو `/usr/local` على Intel.

---

## إعداد خادم PostgreSQL {: #postgresql-server-setup }

### إذا كان لديك PostgreSQL بالفعل

إذا كان PostgreSQL مثبتًا ويعمل على جهازك المحلي أو إذا كنت تستخدم خادم PostgreSQL مُدار عن بُعد، يمكنك الانتقال إلى [القسم التالي](#web-server-configuration).

### خيارات التثبيت

يوفر macOS طريقتين بسيطتين لتثبيت PostgreSQL. اختر **واحدة** فقط:

- [Homebrew](#postgresql-homebrew) — تثبيت عبر سطر الأوامر، موصى به لنشر الخادم
- [Postgres.app](#postgresql-app) — تثبيت رسومي، مناسب للتقييم المحلي

### تثبيت PostgreSQL باستخدام Homebrew {: #postgresql-homebrew }

#### الخطوة 1: تثبيت الصيغة الخاصة بـ PostgreSQL

```bash
brew install postgresql@16
```

#### الخطوة 2: أضف PostgreSQL إلى PATH

الصيغ ذات الإصدار المحدد تكون *keg-only*، مما يعني أن Homebrew لا يربط أوتوماتيكيًا أوامره في PATH لديك. أضفها بنفسك:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "ملاحظة"

    هذا يفترض استخدام الصدفة الافتراضية `zsh` التي يستخدمها macOS. إذا كنت تستخدم `bash`، أضف نفس السطر إلى `~/.bash_profile` بدلًا من ذلك.

#### الخطوة 3: ابدأ خدمة PostgreSQL

```bash
brew services start postgresql@16
```

هذا يشغل PostgreSQL فورًا ويضبطه ليبدأ تلقائيًا عند تسجيل الدخول.

#### الخطوة 4: تحقق من التثبيت

```bash
psql --version
```

يجب أن ترى إصدار PostgreSQL إذا نجح التثبيت.

#### الخطوة 5: الاتصال بالخادم

```bash
psql postgres
```

!!! warning "مهم — يختلف macOS عن Windows هنا"

    يطالب مُثبت Windows بإنشاء مستخدم `postgres` بكلمة مرور. Homebrew لا يفعل ذلك. بدلًا من ذلك ينشئ superuser باسم **حساب macOS الخاص بك**، دون كلمة مرور، ويمكن الوصول إليه فقط من الجهاز المحلي.

    هذا يعني أنه لا يوجد دور `postgres` على تثبيت Homebrew الطازج. استخدم اسم حسابك عند الحاجة إلى صلاحيات superuser، وأنشئ مستخدم digna صريحًا كما هو موضح في [التثبيت الابتدائي](#initial-installation).

#### الخطوة 6: تأكد من المنفذ

المنفذ الافتراضي لـ PostgreSQL هو `5432`. لتأكيد المنفذ الذي يستمع عليه الخادم:

```bash
psql postgres -c "SHOW port;"
```

سجّل القيمة — ستحتاجها عند تكوين backend الخاص بـ digna.

### تثبيت PostgreSQL باستخدام Postgres.app {: #postgresql-app }

إذا فضّلت التثبيت الرسومي:

1. حمّل [Postgres.app](https://postgresapp.com) واسحبه إلى مجلد **Applications**
2. افتح التطبيق وانقر **Initialize** لإنشاء خادم جديد
3. اتبع تعليمات التطبيق لإضافة أدوات سطر الأوامر إلى PATH
4. تحقق من التثبيت:

```bash
psql --version
```

يقوم Postgres.app أيضًا بإنشاء superuser باسم حساب macOS الخاص بك.

---

## تكوين خادم الويب {: #web-server-configuration }

تتطلب digna خادم ويب لاستضافة اللوحة. اختر أحد الخيارات التالية:

- [nginx](#nginx-setup) — يُثبت عبر Homebrew، موصى به
- [Apache httpd](#apache-setup) — مُضمّن مع macOS

تحتاج فقط إلى تثبيت وتكوين **أحد** هذه الخوادم.

يُكوّن كلا القسمين شيئين تعتمد عليهما اللوحة:

- **آلية تراجع لتطبيق الصفحة الواحدة (SPA)**، حتى لا يعيد تحديث عنوان URL للوحة صفحة 404
- **نوع MIME لملفات `.md`**، حتى تُخدم ملفات Markdown بشكل صحيح

### إعداد nginx {: #nginx-setup }

#### نظرة عامة

nginx هو خادم ويب خفيف وعالي الأداء مناسب لخدمة لوحة digna الثابتة.

#### التثبيت

```bash
brew install nginx
```

#### بدء nginx

```bash
brew services start nginx
```

#### التحقق من التثبيت

1. افتح متصفحك
2. انتقل إلى `http://localhost:8080`
3. يجب أن ترى صفحة الترحيب الخاصة بـ nginx

!!! note "ملاحظة — المنفذ الافتراضي هو 8080، وليس 80"

    يضبط Homebrew nginx للاستماع على المنفذ `8080` حتى يعمل بدون امتيازات المسؤول. على macOS، ربط المنفذ `80` أو أي منفذ أقل من 1024 يتطلب صلاحيات root.

    لخدمة اللوحة على المنفذ 80، غيّر `listen 8080;` إلى `listen 80;` في التكوين أدناه وابدأ nginx باستخدام `sudo brew services start nginx` بدلًا من ذلك.

#### تكوين موقع للوحة

يشمل تكوين nginx الخاص بـ Homebrew كل ملف في دليل `servers` الخاص به. أنشئ ملف تكوين مخصص لـ digna هناك:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

ألصق التالي، مع استبدال `/path/to/digna/dashboard` بالمسار الفعلي لمجلد `dashboard` المستخرج لديك:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "مهم"

    بدون توجيه `try_files`، سيؤدي إعادة تحميل أي صفحة للوحة بخلاف عنوان الجذر إلى إرجاع 404. هذا مكافئ nginx لوحدة إعادة كتابة العناوين المطلوبة في IIS على Windows.

#### تطبيق التكوين

اختبر التكوين للأخطاء النحوية، ثم أعد تحميل nginx:

```bash
nginx -t
brew services restart nginx
```

---

### إعداد Apache httpd {: #apache-setup }

#### نظرة عامة

يتضمن macOS Apache httpd، لذا لا حاجة لتثبيته. هو معطَّل افتراضيًا.

#### بدء Apache

```bash
sudo apachectl start
```

#### التحقق من التثبيت

1. افتح متصفحك
2. انتقل إلى `http://localhost`
3. يجب أن ترى الرسالة "It works!"

#### مطلوب: تمكين mod_rewrite

تتطلب اللوحة إعادة كتابة URL. افتح ملف تكوين Apache:

```bash
sudo nano /etc/apache2/httpd.conf
```

ابحث عن السطر التالي وأزل الـ `#` القيّمة لفتحه:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### مطلوب: السماح بتجاوزات .htaccess

في نفس الملف، حدد الكتلة `<Directory "/Library/WebServer/Documents">` وغير:

```apache
AllowOverride None
```

إلى:

```apache
AllowOverride All
```

#### مطلوب: نوع MIME لملفات Markdown

لا تزال في `httpd.conf`، أضف السطر التالي حتى تُخدم ملفات Markdown بشكل صحيح:

```apache
AddType text/markdown .md
```

!!! warning "مهم"

    بدون هذا الإعداد، قد لا تُخدم ملفات `.md` بشكل صحيح.

#### تطبيق التكوين

تحقق من التكوين للأخطاء النحوية، ثم أعد تشغيل Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## التثبيت الابتدائي {: #initial-installation }

### الخطوة 1: إعداد مستودع digna

يخزن مستودع digna كل المقاييس المحسوبة بواسطة digna. يعمل كمركز قاعدة بيانات للبيانات التحليلية وبيانات الأداء.

#### إنشاء الـ Schema والمستخدم للمستودع

افتح عميل PostgreSQL الخاص بك (psql، pgAdmin، أو ما شابه) ونفّذ أوامر SQL التالية:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**استبدل العناصر النائبة التالية:**

- `<digna_repo_schema>` — اسم الـ schema الذي تريده (مثلاً، `dignarepo`)
- `<digna_repo_user>` — اسم المستخدم المطلوب (مثلاً، `digna_user`)
- `<digna_repo_password>` — كلمة مرور آمنة لهذا المستخدم

**مثال:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

لتنفيذ هذه من الـ Terminal في خطوة واحدة:

```bash
psql postgres
```

ثم ألصق العبارات عند موجه `postgres=#` واكتب `\q` للخروج.

!!! tip "أفضل الممارسات"

    استخدم كلمات مرور قوية ومعقّدة لمستخدمي قاعدة البيانات. تجنّب بيانات اعتماد يسهل تخمينها.

---

### الخطوة 2: فك حزمة تثبيت digna

1. حدّد ملف ZIP لتثبيت digna المقدم لك
2. فك ضغطه إلى موقع التثبيت المرغوب — على سبيل المثال `/opt/digna` أو `~/digna`
3. بعد الاستخراج، يجب أن ترى العناصر التالية:
   - `dashboard/` — واجهة الويب للوحة
   - `digna` — الملف التنفيذي الرئيسي (backend + CLI مدمجان)

!!! info "ملفا التهيئة والترخيص غير موجودين في الحزمة"

    لا يأتي `config.toml` ولا `dashboard/dashboard_config.toml` مع التثبيت — بل تنشئ كليهما بنفسك، في
    [تهيئة الواجهة الخلفية](#backend-configuration) و
    [تهيئة لوحة التحكم](#dashboard-configuration). ولا يأتي `license.toml` معه كذلك؛
    إذ يقدّمه digna بشكل منفصل، كما هو موضّح في الخطوة 3.

لفك الضغط من الـ Terminal:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
```

#### اجعل الملف التنفيذي قابلاً للتشغيل

اعتمادًا على طريقة نقل الأرشيف، قد لا يبقى بت التشغيل بعد الاستخراج. حدده صراحةً:

```bash
cd /opt/digna
chmod +x digna
```

#### إذا قام macOS بحظر التطبيق

الملفات التي تُحمّل عبر متصفح أو عميل بريد يتم وسمها بصفة الحجر الصحي (quarantine). إذا أبلغك macOS أن التطبيق *"cannot be opened because the developer cannot be verified"*, نظّف السمة من دليل التثبيت:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

بدلاً من ذلك، افتح **System Settings → Privacy & Security**، ابحث عن العنصر المحظور قرب أسفل الصفحة، وانقر **Open Anyway**.

!!! note "ملاحظة"

    هذه الخطوة مطلوبة فقط إذا قام macOS فعليًا بحظر الملف التنفيذي. الحزم المنقولة عبر SSH أو من مشاركات ملفات داخلية عادةً لا تُعلّق بالحجر الصحي.

### الخطوة 3: تثبيت ملف الترخيص

!!! warning "مهم"

    ملف الترخيص **غير** متضمن في حزمة التثبيت وسيُقدّم لك بشكل منفصل من قِبل digna.

1. حدّد ملف `license.toml` المزوّد لك
2. انسخه إلى جذر دليل تثبيت digna (حيث يتواجد `config.toml` والملف التنفيذي `digna`)

**لماذا هذا مهم:**
يحتوي ملف الترخيص على معلومات العميل، وتاريخ انتهاء الترخيص، والتوقيع الرقمي. **لا تعدّل هذا الملف** — أي تغييرات ستبطل صحته.

**هيكل الدليل بعد الإعداد:**

```
/opt/digna/
├── config.toml         (ملف التكوين)
├── license.toml        (ملف الترخيص الخاص بك - انسخه هنا)
├── digna               (الملف التنفيذي الرئيسي)
├── bin/                (سكريبتات إدارة الخدمة)
└── dashboard/          (واجهة الويب)
    └── (ملفات اللوحة)
```

---

## تكوين الBackend {: #backend-configuration }

### الخطوة 1: إنشاء وتعديل ملف التكوين

يوجد ملف `config_template.toml` في دليل تثبيت digna الخاص بك. كل ما عليك هو إعادة تسميته إلى `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**الموقع:** `/opt/digna/config.toml`

افتح `config.toml` في محرر نصي وقم بتكوين كل قسم أدناه.

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

!!! note "ملاحظة"

    إذا قمت بخدمة اللوحة من nginx الخاص بـ Homebrew على المنفذ الافتراضي، فإن الأصل الذي يجب السماح به هو `http://localhost:8080`.

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
| `DIGNA_REPO_HOST` | `localhost` أو IP | اسم مضيف/IP خادم PostgreSQL |
| `DIGNA_REPO_PORT` | `5432` (افتراضي) | منفذ PostgreSQL |
| `DIGNA_REPO_DB` | `postgres` | اسم قاعدة البيانات |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | الـ schema الذي أنشأته سابقًا |
| `DIGNA_REPO_USER` | `digna_user` | المستخدم الذي أنشأته في إعداد PostgreSQL |
| `DIGNA_REPO_PASSWORD` | كلمة مرورك | كلمة المرور التي تم تعيينها أثناء إنشاء الـ schema |
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

!!! tip "نصيحة"

    لمعرفة عدد أنوية المعالج المتاحة على جهاز Mac، شغّل `sysctl -n hw.ncpu`.

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

هذا القسم يضبط سلوك التسجيل:

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

#### قسم [duckdb] (اختياري) {: #duckdb-section }

جديد في الإصدار 2026.11. يحدد هذا القسم موارد **digna Engine**، الذي يُجري تنميط البيانات داخل
digna لاتصالات قواعد البيانات التي يكون موقع التنميط فيها **digna Engine**، ويُشغّل فحوصات التكامل
المرجعي بين مصادر بيانات موجودة على اتصالات قواعد بيانات مختلفة. انظر
[موقع التنميط](../../../platform/profiling/profiling_location.md).

هذا القسم اختياري. من دونه تُطبَّق القيم الافتراضية أدناه.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| المعامل | القيمة | ملاحظات |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (افتراضي) | الذاكرة بالميغابايت التي يمكن أن يستخدمها تشغيل واحد لـ digna Engine. يمكن أن يكون ما يصل إلى `DIGNA_MAX_WORKERS` من عمليات التشغيل نشطًا في الوقت نفسه |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | الافتراضي: الدليل المؤقت للنظام (`$TMPDIR` للحساب الذي يشغّل digna) | دليل الملفات المؤقتة عندما لا تتسع الذاكرة للبيانات |

!!! tip "تحديد حجم digna Engine"

    خطّط لما يصل إلى `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` من الذاكرة على مضيف
    digna، فوق ما يستخدمه digna نفسه، ولمساحة قرص حرة كافية في الدليل المؤقت تتسع لأكبر تاريخ
    مفحوص من مصادر البيانات التي تستخدم digna Engine. وجّه `DIGNA_DUCKDB_TEMP_DIRECTORY` إلى قرص
    تتوفر فيه هذه المساحة ويستطيع الحساب الذي يشغّل digna الكتابة فيه:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    لا تحتاج إلى هذا القسم إلا إذا كان اتصال واحد على الأقل بقاعدة بيانات يستخدم digna Engine، أو كان
    فحص تكامل مرجعي يقارن مصادر بيانات موجودة على اتصالات مختلفة.

---

### الخطوة 2: تحقق من التهيئة

قبل تهيئة المستودع، تحقق من أن `config.toml` مكتمل ومبني بشكل صحيح. نفّذ في دليل تثبيت digna:

```bash
./digna config check
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

1. افتح **Terminal**
2. انتقل إلى دليل تثبيت digna (حيث يوجد `config.toml` والملف التنفيذي `digna`)
3. شغّل اختبار الاتصال:

```bash
cd /opt/digna
./digna repo check
```

على مخطط جديد، يتصل الأمر ثم يُبلغ بأنه لا يوجد مستودع مثبّت بعد:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

في هذه المرحلة هذه هي النتيجة المتوقعة: فهي تؤكد أن digna يصل إلى PostgreSQL وإلى المخطط. أما خطأ الاتصال أو المصادقة فيشير بدلًا من ذلك إلى القسم `[repo]` أو إلى إعداد PostgreSQL.

!!! note "ملاحظة"

    على macOS، الأوامر في الدليل الحالي ليست في PATH، لذا يُستدعى الملف التنفيذي كـ `./digna` بدلًا من `digna`. لاستخدام الشكل الأقصر في كل مكان، أضف دليل التثبيت إلى PATH لديك:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### الخطوة 4: تثبيت مخطط المستودع

في نفس الدليل، شغّل:

```bash
./digna repo upgrade
```

يُثبّت هذا الأمر الجداول اللازمة في مخطط المستودع وينتهي بالرسالة:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "الأمر repo upgrade يثبّت ويرقّي"

    ابتداءً من الإصدار 2026.11، يثبّت `repo upgrade` مستودعًا جديدًا ويرقّي مستودعًا موجودًا.
    ولا يزال `repo install` يعمل كاسم آخر للأمر نفسه.

### الخطوة 5: إنشاء مستخدم مسؤول (Admin)

1. افتح نافذة Terminal **جديدة**
2. انتقل إلى دليل تثبيت digna
3. شغّل الأمر التالي لإنشاء مستخدم مسؤول:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**مثال:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

يؤدي ذلك إلى إنشاء مستخدم بعنوان البريد الإلكتروني `admin@example.com` وامتيازات إدارية كاملة.

!!! tip "نصيحة"

    ضع كلمة المرور بين علامات اقتباس مفردة. يتعامل `zsh` مع أحرف مثل `!` و `$` و `*` بشكل خاص، والكلمة غير المقتبسة التي تحتوي عليها لن تُمرَّر كما كتبت.

!!! tip "أفضل الممارسات"

    استخدم كلمة مرور قوية تحتوي مزيجًا من أحرف كبيرة، وصغيرة، وأرقام، ورموز خاصة.

---

### الخطوة 6: بدء خادم digna

في دليل تثبيت digna، ابدأ الخادم بـ:

```bash
./digna serve --address <host> --port <port>
```

**المعلمات:**
- `--address` — اسم المضيف/IP للخادم (الافتراضي `127.0.0.1`)
- `--port` — منفذ الخادم (الافتراضي `8000`)

عندما يعمل الخادم، يطبع العنوان الذي يستمع عليه:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "نصيحة"

    في المرة الأولى التي تشغّل فيها الخادم، قد يسألك macOS ما إذا كنت تريد السماح للتطبيق بقبول اتصالات الشبكة الواردة. انقر **Allow**، وإلا فلن تتمكن اللوحة من الوصول إلى الـ backend.

!!! note "الخادم يشغل الطرفية"

    يعمل `serve` في المقدمة ويستمر حتى توقفه بالضغط على ++ctrl+c++. اتركه يعمل بينما تكمل الإعداد؛ ولتشغيله تلقائيًا عند الإقلاع بدلًا من ذلك انظر [تشغيل digna كخدمة في الخلفية](#running-digna-as-a-background-service).

## تكوين اللوحة {: #dashboard-configuration }

### الخطوة 1: نشر اللوحة على خادم الويب

تقرأ لوحة digna تهيئتها الخاصة من `dashboard/dashboard_config.toml`. هذا الملف لا يأتي مع التثبيت — بل تنشئه في دليل `dashboard/` إلى جانب ملفات لوحة التحكم.

محتوياته موضّحة في [الدخول الموحّد (SSO)](../../../sso/overview.md)، وهناك أيضًا يلزم الملف: فهو يحمل خيارات تسجيل الدخول التي تعرضها لوحة التحكم، وفي عمليات النشر متعددة النسخ، اتصال الواجهة الخلفية.

اختر خادم الويب الخاص بك واتبع خطوات النشر المناسبة.

#### النشر على nginx

إذا اتبعت قسم [إعداد nginx](#nginx-setup)، فإن كتلة الخادم تشير بالفعل إلى مجلد `dashboard` الخاص بك ولا حاجة للنسخ.

1. **تأكد من المسار**
   - افتح `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - تحقق أن `root` يشير إلى مجلد `dashboard` المستخرج

2. **تأكد أن المجلد قابل للقراءة**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **أعد تحميل nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **اختبر التثبيت**
   - افتح متصفحك
   - انتقل إلى `http://localhost:8080` (أو عنوان URL الذي ضبطته)
   - يجب أن ترى صفحة تسجيل دخول لوحة digna

#### النشر على Apache httpd

1. **انسخ اللوحة إلى جذر المستندات**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **أضف قواعد إعادة الكتابة**

   أنشئ ملف `.htaccess` داخل المجلد المنشور حتى تبقى مسارات اللوحة صالحة عند تحديث المتصفح:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   ألصق التالي:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **أعد تشغيل Apache**
   ```bash
   sudo apachectl restart
   ```

4. **الوصول إلى اللوحة**
   - افتح متصفحك
   - انتقل إلى `http://localhost/digna`
   - يجب أن ترى صفحة تسجيل دخول لوحة digna

---

## تشغيل digna كخدمة في الخلفية {: #running-digna-as-a-background-service }

### لماذا تشغيل digna كخدمة؟

تشغيل backend الخاص بـ digna كخدمة في الخلفية يضمن أن:

- يبدأ تلقائيًا عند إقلاع الجهاز
- يعمل في الخلفية دون الحاجة إلى نافذة Terminal مفتوحة
- يعاد تشغيله تلقائيًا إذا تعطل
- يمكن إدارته عبر `launchctl`، مدير الخدمات في macOS

### ملفات إدارة الخدمة

جميع الملفات اللازمة تقع في دليل تثبيت digna تحت: `bin/`

السكربتات الشل التالية متاحة:

- `install_service.sh` — يسجل digna لدى launchd
- `uninstall_service.sh` — يلغى تسجيل الخدمة
- `start_service.sh` — يشغّل الخدمة المسجلة
- `stop_service.sh` — يوقف الخدمة العاملة

!!! warning "مطلوب صلاحيات المسؤول"

    يجب تنفيذ كل السكربتات باستخدام `sudo`، لأن تسجيل خدمة تبدأ عند الإقلاع يكتب إلى `/Library/LaunchDaemons`.

### جعل السكربتات قابلة للتنفيذ

قد لا تحفظ عملية الاستخراج بت التشغيل. قبل الاستخدام الأول:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### تثبيت الخدمة

1. **افتح Terminal**

2. **انتقل إلى مجلد bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **شغّل سكربت التثبيت**
   ```bash
   sudo ./install_service.sh
   ```

تم الآن تسجيل خادم digna لدى launchd مع تشغيل تلقائي عند الإقلاع. لا تبدأ الخدمة فورًا — راجع القسم التالي لبدئها.

### بدء وإيقاف الخدمة

#### لبدء الخدمة

1. افتح Terminal
2. انتقل إلى `/opt/digna/bin`
3. شغّل:
   ```bash
   sudo ./start_service.sh
   ```

#### لإيقاف الخدمة

1. افتح Terminal
2. انتقل إلى `/opt/digna/bin`
3. شغّل:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "نصيحة"

    أوقِف دائمًا الخدمة قبل تحديث ملفات التطبيق.

### التحقق من الخدمة

لتأكيد أن الخدمة مسجلة وتعمل:

```bash
sudo launchctl list | grep digna
```

سطر يبدأ بمعرف عملية يدل على أن الخدمة تعمل. وجود `-` في العمود الأول يعني أنها مسجلة ولكن متوقفة.

### نقل الخدمة إلى دليل جديد

يخزن launchd المسار المطلق للملف التنفيذي، لذا يتطلب نقل التثبيت إعادة تسجيل الخدمة:

1. **إلغاء تثبيت الخدمة الحالية**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **نقل ملفات التطبيق**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **إعادة تثبيت الخدمة**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **بدء الخدمة**
   ```bash
   sudo ./start_service.sh
   ```

### إلغاء تثبيت الخدمة

1. **أوقف الخدمة العاملة**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **ألغِ تثبيت الخدمة**
   ```bash
   sudo ./uninstall_service.sh
   ```

تم الآن إلغاء تسجيل خادم digna من launchd.

---

## الترقية إلى إصدار جديد {: #upgrading-to-a-new-release }

يشرح هذا القسم ترقية تثبيت الإصدار 2026.06 إلى الإصدار 2026.11.

!!! warning "الترقية من إصدار أقدم من 2026.06"

    نفّذ أولًا خطوات الترقية إلى الإصدار 2026.06: [الترقية إلى إصدار جديد](../Release%202026.06/installation_guide_digna_macos_2026_06.md#upgrading-to-a-new-release). ثم تابع بالخطوات أدناه.

### قبل الترقية

**النسخ الاحتياطي لمستودع digna إلزامي**

قبل ترقية digna، اعمل نسخة احتياطية من مستودعك (PostgreSQL) لحماية بياناتك من الضياع.
النسخة الاحتياطية تضمن إمكانية الاسترداد إذا واجهت الترقية مشكلات غير متوقعة.

لإنشاء نسخة احتياطية من الـ Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**طلب ملف الترخيص للإصدار 2026.11**

يحتاج الإصدار 2026.11 إلى ملف `license.toml` جديد. اطلبه من فريق digna قبل أن تبدأ، واجعله
جاهزًا لـ [الخطوة 7](#step-7-replace-the-license-file).

### عملية الترقية

#### الخطوة 1: إيقاف خدمة digna {: #step-1-stop-the-digna-service }

إذا كان digna يعمل كخدمة في الخلفية، فأوقفه أولًا:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

إذا كان digna يعمل في المقدمة (foreground)، اضغط ++ctrl+c++ في نافذة Terminal الخاصة به.

#### الخطوة 2: انسخ التثبيت الحالي احتياطيًا {: #step-2-backup-current-installation }

في دليل تثبيت digna، أعد تسمية الملف التنفيذي ومجلد لوحة التحكم في تثبيتك الحالي، حتى
يمكن نشر الإصدار الجديد بجوارهما:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

احتفظ بـ `digna_old` حتى تتحقق من الترقية، وبـ `dashboard_old` حتى تستعيد منه ملفات التهيئة
الخاصة بك (انظر الخطوة 4). بعد ذلك يمكنك حذفهما.

#### الخطوة 3: فك ونشر النسخة الجديدة {: #step-3-extract-and-deploy-new-version }

1. فك ملف ZIP للنسخة الجديدة من digna
2. انسخ الملف التنفيذي الجديد `digna` ومجلد `dashboard` إلى دليل التثبيت
3. أعد بت التنفيذ، وأزل سمة الحجر (quarantine) عند الحاجة:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "مهم"

    لا يُضمَّن `config.toml` ولا `dashboard/dashboard_config.toml` أبدًا في
    أرشيف ZIP الخاص بالتثبيت — فريق digna لا يرسل أيًّا من الملفين أبدًا. لذلك تبقى تهيئتك الحالية
    بمنأى عن الترقية، والنسخ الموجودة في المجلدات المعاد تسميتها `*_old` هي
    النسخ الوحيدة التي لديك.

#### الخطوة 4: استعادة ملفات التهيئة الخاصة بك {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
ثم أعد تحميل الصفحة بتحديث كامل (++cmd+shift+r++).

#### الخطوة 6: تحقق من التهيئة {: #step-6-validate-the-configuration }

تأكد من أن ملف `config.toml` مكتمل قبل أن تمسّ المستودع:

```bash
./digna config check
```

يجب أن يُبلِّغ كل قسم بحالة OK. صحّح كل ما يُبلَّغ عنه بحالة FAILED، واحذف المفاتيح المدرجة تحت
**Unknown keys**، وأعد تنفيذ الأمر قبل المتابعة.

#### الخطوة 7: استبدال ملف الترخيص {: #step-7-replace-the-license-file }

ملف الترخيص الصادر لإصدار سابق لا يعمل مع الإصدار 2026.11. انسخ ملف `license.toml` الذي قدّمه
فريق digna للإصدار 2026.11 إلى دليل التثبيت، ليحل محل الملف القديم:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "لا تحتفظ بالترخيص السابق"

    مع الترخيص السابق يفشل كل أمر يتحقق من الترخيص — `serve` و`user` و`inspection` و`repo` —
    فلا يبدأ digna ولا يمكن ترقية المستودع. تحقّق من الترخيص الجديد قبل المتابعة:

    ```bash
    ./digna license check
    ```

#### الخطوة 8: ترقية مخطط المستودع {: #step-8-upgrade-the-repository-schema }

في دليل تثبيت digna، شغّل:

```bash
cd /opt/digna
./digna repo upgrade
```

يدير الإصدار 2026.11 مخطط المستودع بعمليات ترحيل ذات أرقام إصدارات (versioned migrations). أول ترقية
من إصدار سابق تنقل المخطط إلى آخر نسخة من الآلية السابقة، وتسجّل ذلك نقطةَ بداية له، ثم تطبّق
عمليات ترحيل الإصدار 2026.11. وتنتهي بالرسالة:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

تُحفظ جميع البيانات الحالية. لمعرفة حالة المستودع في أي وقت، شغّل
`./digna repo check`: فهو يسرد آخر عملية ترحيل مطبّقة وأي عمليات ترحيل معلّقة.

!!! warning "لا يبدأ digna على مستودع قديم"

    ابتداءً من الإصدار 2026.11، يرفض الخادم البدء ما دام المستودع يحتاج إلى ترقية، ويُبلغ بذلك،
    على سبيل المثال:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    شغّل `repo upgrade` قبل أن تبدأ الخادم أو الخدمة.

#### الخطوة 9: إعادة تشغيل الخدمات {: #step-9-restart-services }

إذا كان يعمل كخدمة في الخلفية:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

إذا كنت تشغّله يدويًا، أعد تشغيل الخادم:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

إذا كنت تستخدم nginx أو Apache، أعد تشغيل خادم الويب المعني:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### الخطوة 10: التحقق من الترقية {: #step-10-verify-the-upgrade }

1. تأكد من إصدار الملف التنفيذي الجديد:

    ```bash
    ./digna version
    ```

    يجب أن يكون السطر الأول `Release: 2026.11`.

2. افتح لوحة digna وتحقق من تحميل الواجهة بشكل صحيح.
3. تحقق من مخرجات الخادم ومن الملفات في الدليل `logs` بحثًا عن أخطاء.
4. اختبر اتصالات قواعد البيانات — انظر
   [اختبار اتصال](../../../databases/overview.md#testing-a-connection).

للبدء مع الوحدات الجديدة، انظر [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md)،
و[ربط وكيل ذكاء اصطناعي](../../../platform/agentic/connect_ai_agent.md) من أجل digna MCP Server،
و[موقع التنميط](../../../platform/profiling/profiling_location.md) من أجل digna Engine.
