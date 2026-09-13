---
title: دليل التثبيت على macOS – إصدار digna 2026.06 | توثيق digna
description: دليل خطوة بخطوة لتثبيت إصدار digna 2026.06 على macOS — متطلبات النظام، إعداد Homebrew و PostgreSQL، تكوين nginx أو Apache، إعداد الbackend واللوحة، تشغيل digna كخدمة في الخلفية، والترقية إلى إصدار جديد.
keywords: تثبيت digna على macos, دليل نشر digna على ماك, إعداد backend digna, تثبيت لوحة digna, postgresql homebrew, nginx macos, خدمة launchd digna, دليل ترقية digna
image: /assets/logo_square.png
---

# دليل التثبيت على macOS لإصدار digna 2026.06

**الإصدار:** 2026.06

**آخر تحديث:** 5 سبتمبر، 2026


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

### الجديد في إصدار 2026.06

يضيف هذا الإصدار قدرات مراقبة بيانات قابلة للملاحظة مباشرة داخل التعليمات البرمجية الخاصة بك، مما يمكّن المطورين من تتبع جودة البيانات عند المصدر. راجع [ملاحظات الإصدار](http://docs.digna.ai/changelog/Release_202606/) للحصول على التفاصيل الكاملة.

### تبحث عن Windows أو Linux؟

يغطي هذا الدليل macOS. للمنصات الأخرى، راجع [دليل التثبيت على Windows](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) أو [دليل التثبيت على Linux](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

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
   - `config.toml` — ملف التكوين
   - `license.toml` — ملف الترخيص (انسخ ملفك هنا)

لفك الضغط من الـ Terminal:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
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

هذا القسم يضبط إعدادات تطبيق backend الخاص بـ digna:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| المعامل | القيمة | ملاحظات |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | عنوان الواجهة الأمامية | إذا كانت اللوحة على خادم مختلف، أضف عنوان URL الخاص بها |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | مطلوب لطلبات CORS التي تحتوي على بيانات اعتماد |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | السماح بكل طرق HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | السماح بكل العناوين |

!!! note "ملاحظة"

    إذا قمت بخدمة اللوحة من nginx الخاص بـ Homebrew على المنفذ الافتراضي، فإن الأصل الذي يجب السماح به هو `http://localhost:8080`.

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
| `digna_REPO_HOST` | `localhost` أو IP | اسم مضيف/IP خادم PostgreSQL |
| `digna_REPO_PORT` | `5432` (افتراضي) | منفذ PostgreSQL |
| `digna_REPO_DB` | `postgres` | اسم قاعدة البيانات |
| `digna_REPO_SCHEMA` | `dignarepo` | الـ schema الذي أنشأته سابقًا |
| `digna_REPO_USER` | `digna_user` | المستخدم الذي أنشأته في إعداد PostgreSQL |
| `digna_REPO_PASSWORD` | كلمة مرورك | كلمة المرور التي تم تعيينها أثناء إنشاء الـ schema |

#### قسم [base]

يحتوي هذا القسم على إعدادات الأمان والكوكيز:

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
| `digna_COOKIE_DOMAIN` | `localhost` | طابق نطاق الواجهة الأمامية لديك |
| `digna_COOKIE_SECURE` | `false` (محلي) / `true` (إنتاج) | استخدم `true` لاتصالات HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | مفعّل دائمًا لأمن أفضل |
| `digna_COOKIE_SAME_SITE` | `lax` | يمنع هجومات CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ساعة) | انتهاء صلاحية الجلسة بالثواني |
| `digna_MAX_WORKERS` | عدد أنوية المعالج - 1 | عدد مهام الفحص المتوازية |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | أقصى تأخير بالثواني يمكن للمجدول إضافته قبل بدء مهمة حان موعدها |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | وقت اليوم (تنسيق 24 ساعة `HH:MM`) الذي يبدأ عنده التنظيف اليومي |

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
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| المعامل | القيمة | ملاحظات |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` أو `DEBUG` | استخدم `INFO` للإنتاج، و`DEBUG` لاستكشاف الأعطال |
| `digna_LOGGING_BACKUP_COUNT` | `10` | عدد نسخ النسخ الاحتياطية اليومية من السجلات المراد الاحتفاظ بها |

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

1. افتح **Terminal**
2. انتقل إلى دليل تثبيت digna (حيث يوجد `config.toml` والملف التنفيذي `digna`)
3. شغّل اختبار الاتصال:

```bash
cd /opt/digna
./digna repo check
```

يجب أن ترى تأكيدًا على أن الاتصال تم (المستودع نفسه لم يُهيأ بعد).

!!! note "ملاحظة"

    على macOS، الأوامر في الدليل الحالي ليست في PATH، لذا يُستدعى الملف التنفيذي كـ `./digna` بدلًا من `digna`. لاستخدام الشكل الأقصر في كل مكان، أضف دليل التثبيت إلى PATH لديك:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### الخطوة 4: تثبيت مخطط المستودع

في نفس الدليل، شغّل:

```bash
./digna repo install
```

يقوم هذا الأمر بتثبيت الجداول والمخططات اللازمة في قاعدة بيانات PostgreSQL الخاصة بك.

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
- `--address` — اسم المضيف/IP للخادم
- `--port` — منفذ الخادم

يجب أن ترى رسائل بدء تؤكد أن الخادم يعمل:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "نصيحة"

    في المرة الأولى التي تشغّل فيها الخادم، قد يسألك macOS ما إذا كنت تريد السماح للتطبيق بقبول اتصالات الشبكة الواردة. انقر **Allow**، وإلا فلن تتمكن اللوحة من الوصول إلى الـ backend.

!!! note "الخادم يشغل الطرفية"

    يعمل `serve` في المقدمة ويستمر حتى توقفه بالضغط على ++ctrl+c++. اتركه يعمل بينما تكمل الإعداد؛ ولتشغيله تلقائيًا عند الإقلاع بدلًا من ذلك انظر [تشغيل digna كخدمة في الخلفية](#running-digna-as-a-background-service).

## تكوين اللوحة {: #dashboard-configuration }

### الخطوة 1: نشر اللوحة على خادم الويب

تحتوي لوحة digna على ملف `config.toml` منفصل داخل مجلد `dashboard/`. يتم توفير هذا التكوين مسبقًا ولا يتطلب تغييرات أثناء التثبيت الابتدائي. تحتاج فقط لتعديله إذا رغبت في تخصيص اتصال الـ backend.

إذا احتجت لتعديل تكوين اللوحة (مثلًا للنشر متعدد النسخ)، ارجع إلى وثائق اللوحة.

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

إنشاء نسخة احتياطية من مستودع digna أمر إجباري

قبل ترقية digna، احتفظ بنسخة احتياطية من مستودعك (PostgreSQL) لحمايته من فقدان البيانات.
تضمن النسخة الاحتياطية إمكانية الاسترداد إذا واجهت الترقية مشكلات غير متوقعة.

لإنشاء نسخة احتياطية من الـ Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### عملية الترقية

#### الخطوة 1: أوقف خدمة digna

إذا كانت digna تعمل كخدمة في الخلفية، أوقفها أولًا:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

إذا كانت تعمل في الواجهة الأمامية، اضغط `Ctrl + C` في نافذة الـ Terminal الخاصة بها.

#### الخطوة 2: انسخ التثبيت الحالي احتياطيًا

في دليل تثبيت digna، أعد تسمية مجلدات التثبيت الحالي حتى يمكن نشر الإصدار الجديد بجوارها:

```bash
cd /opt/digna
mv dignabackend dignabackend_old
```
```bash
mv dignacli dignacli_old
```
```bash
mv dashboard dashboard_old
```

!!! info "لم يعد dignabackend وdignacli مستخدمَين"

    ابتداءً من الإصدار 2026.06، يحل الملف التنفيذي الواحد `digna` محل `dignabackend` و`dignacli`، وهو يجمع الواجهة الخلفية وواجهة سطر الأوامر. احتفظ بـ `dignabackend_old` و`dignacli_old` فقط حتى تتحقق من الترقية — بعدها يمكنك حذف المجلدين. احتفظ بـ `dashboard_old` حتى تستعيد منه ملفات التهيئة الخاصة بك (انظر الخطوة 4).

#### الخطوة 3: فك ونشر النسخة الجديدة

1. فكّ أرشيف التثبيت الجديد لـ digna
2. انسخ الملف التنفيذي الجديد `digna` ومجلد `dashboard` إلى دليل التثبيت الخاص بك
3. استعد بت تشغيل بت التنفيذ، وإذا لزم الأمر، نظّف سمة الحجر الصحي:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "مهم"

    ملف `config.toml` **غير** مضمن أبدًا في ZIP التثبيت. يبقى تكوينك الحالي آمنًا.

#### الخطوة 4: استعادة ملفات التكوين الخاصة بك

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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

#### الخطوة 5: تحقق من التهيئة

تأكد من أن ملف `config.toml` المحدَّث مكتمل قبل أن تمسّ المستودع:

```bash
./digna config check
```

يجب أن يُبلِّغ كل قسم بحالة OK. صحّح كل ما يُبلَّغ عنه بحالة FAILED، وأعد تنفيذ الأمر قبل المتابعة.

#### الخطوة 6: ترقية مخطط المستودع

انتقل إلى دليل تثبيت digna وشغّل:

```bash
cd /opt/digna
./digna repo upgrade
```

يقوم هذا بتحديث مخطط PostgreSQL إلى أحدث إصدار مع الحفاظ على جميع البيانات الحالية.

#### الخطوة 7: إعادة تشغيل الخدمات

إذا كانت تعمل كخدمة في الخلفية:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

إذا كانت تعمل يدويًا، أعد تشغيل الخادم:

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

#### الخطوة 8: التحقق من الترقية

1. ادخل إلى لوحة digna
2. تحقق من تحميل الواجهة بشكل صحيح
3. راجع سجلات الخادم لأي أخطاء
4. حوّل إلى ODBC كل اتصال لم يكن يستخدمه بعد، ثم اختبر جميع الاتصالات — انظر [اختبار اتصال](../../../databases/overview.md#testing-a-connection)