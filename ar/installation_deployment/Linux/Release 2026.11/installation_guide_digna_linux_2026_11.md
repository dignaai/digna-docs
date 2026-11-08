# دليل التثبيت على Linux لـ digna إصدار 2026.11

**الإصدار:** 2026.11

**آخر تحديث:** 7 نوفمبر 2026


---

## جدول المحتويات

1. [مقدمة](#introduction)
2. [متطلبات النظام](#system-requirements)
3. [التهيئة ما قبل التثبيت](#pre-installation-setup)
4. [إعداد خادم PostgreSQL](#postgresql-server-setup)
5. [تهيئة خادم الويب](#web-server-configuration)
6. [التثبيت الابتدائي](#initial-installation)
7. [تكوين الخلفية (Backend)](#backend-configuration)
8. [تكوين الواجهة (Dashboard)](#dashboard-configuration)
9. [تشغيل digna كخدمة systemd](#running-digna-as-a-systemd-service)
10. [الترقية إلى إصدار جديد](#upgrading-to-a-new-release)

---

## مقدمة {: #introduction }

### عن digna

digna هي منصة شاملة مدفوعة بالذكاء الاصطناعي مصممة لتحسين إدارة جودة البيانات عبر بيئات بيانات متعددة مثل المستودعات، البحيرات، وlakehouses. بُنيت لتكون قابلة للتوسع والتكيف بدرجة عالية، وتتعامل digna مع تحديات البيانات الحديثة عبر الأتمتة، المراقبة في الوقت الحقيقي، واكتشاف الشذوذ.

تتكون digna من مكوّنَين رئيسيين:

- **digna**: نواة التطبيق، وهي المسؤولة عن معالجة البيانات وتنفيذ فحوص الجودة. تجمع الواجهة الخلفية وواجهة سطر الأوامر في ملف تنفيذي واحد، وتحل محل البرنامجين المنفصلين `dignabackend` و`dignacli` في الإصدارات السابقة.
- **dignadashboard**: واجهة ويب مستضافة على خادم ويب، توفّر وسيلة سهلة التفاعل مع منصة digna وتصوّر مقاييس جودة البيانات.

### ما الجديد في إصدار 2026.11

يضيف هذا الإصدار digna Data Reconciliation، وdigna Agentic مع digna MCP Server، وdigna Engine الذي يستطيع إجراء تنميط البيانات (profiling) داخل digna والتحقق من التكامل المرجعي بين تقنيات قواعد بيانات مختلفة. راجع [ملاحظات الإصدار](../../../changelog/Release_202611.md) للتفاصيل الكاملة.

بالنسبة إلى التثبيت، يجلب الإصدار آلية جديدة لترحيل المستودع، وقسمًا اختياريًا `[duckdb]` في `config.toml` من أجل digna Engine، وملف ترخيص جديدًا. يتناول [قسم الترقية](#upgrading-to-a-new-release) كلًّا منها.

### تبحث عن Windows أو macOS؟

يغطي هذا الدليل Linux. للمنصات الأخرى، راجع [دليل التثبيت على Windows](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) أو [دليل التثبيت على macOS](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md).

### أي توزيعة يغطي هذا الدليل؟

التعليمات مكتوبة لعائلتين شائعتين من الخوادم. حيث تختلف الأوامر بينهما، يتم عرض كلا الأمرين:

- **عائلة Debian** — Debian، Ubuntu. مدير الحزم: `apt`.
- **عائلة RHEL** — Red Hat Enterprise Linux، Rocky Linux، AlmaLinux، Fedora. مدير الحزم: `dnf`.

أي توزيعة حديثة تحتوي على `systemd` ستعمل؛ ما يتغير فقط أسماء الحزم وبعض مسارات التهيئة.

---

## متطلبات النظام {: #system-requirements }

قبل أن تبدأ التثبيت، تأكد من أن نظامك يفي بالحد الأدنى من المتطلبات التالية:

| المتطلب | المواصفات |
|---|---|
| **نظام التشغيل** | Ubuntu 22.04 LTS أو أحدث، Debian 12 أو أحدث، RHEL 9 / Rocky 9 / AlmaLinux 9 أو أحدث |
| **العمارة** | x86_64 (amd64) أو arm64 |
| **نظام التهيئة (Init System)** | systemd |
| **الذاكرة (إعداد أدنى)** | 16 GB RAM |
| **مساحة القرص** | 10 GB مساحة متاحة |
| **قاعدة البيانات** | خادم PostgreSQL 12 أو أحدث |
| **خادم الويب** | nginx، Apache httpd، أو مكافئ |

!!! info "digna Engine"

    اتصالات قواعد البيانات التي تستخدم digna Engine موقعًا للتنميط يُجرى تنميطها على مضيف
    digna نفسه. خطّط لذاكرة ومساحة قرص إضافيتين من أجلها، انظر
    [قسم \[duckdb\]](#duckdb-section).

### خيارات تثبيت قاعدة البيانات

**إذا كان PostgreSQL مثبتًا بالفعل:**
يمكنك إضافة قاعدة بيانات جديدة لـ digna إلى خادم PostgreSQL الموجود لديك.

**إذا كنت ستثبت PostgreSQL على نفس الجهاز الذي سيشغّل digna:**

!!! info "المواصفات الموصى بها"

    - **الذاكرة**: 32 GB RAM (بدلاً من 16 GB)
    - **مساحة القرص**: 50 GB مساحة متاحة (بدلاً من 10 GB)

    هذه المواصفات الأعلى تستوعب تشغيل digna وقاعدة بيانات PostgreSQL معًا.

### التحقق من التوزيعة والعمارة

تختلف عدة أوامر في هذا الدليل بين عائلتي Debian و RHEL. للتحقق أي منهما تستخدم، شغّل:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` أو `ID=debian` — استخدم أوامر `apt`.
- `ID=rhel`, `rocky`, `almalinux` أو `fedora` — استخدم أوامر `dnf`.
- `x86_64` أو `aarch64` — هي معمارية حزمة التثبيت التي تحتاجها.

---

## التهيئة ما قبل التثبيت {: #pre-installation-setup }

قبل تثبيت digna، تأكد من توافر شرطين أساسيين:

1. **خادم PostgreSQL** – لتخزين المقاييس المحسوبة وبيانات الأداء
2. **خادم الويب** – لاستضافة لوحة تحكم digna

إذا لم تكن هذه المكونات معدّة بالفعل، اتبع الأقسام أدناه لتثبيتها وتكوينها.

### تحديث فهارس الحزم

حدّث قوائم الحزم قبل تثبيت أي شيء:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "ملاحظة"

    طوال هذا الدليل، الأمر الأول في كل زوج مخصص **لعائلة Debian** والثاني لعائلة **RHEL**. شغّل الأمر الذي يطابق نظامك فقط.

---

## إعداد خادم PostgreSQL {: #postgresql-server-setup }

### إذا كان PostgreSQL مثبتًا بالفعل

إذا كان PostgreSQL مثبتًا ويعمل على جهازك المحلي أو كنت تستخدم خادم PostgreSQL مدارًا عن بُعد، يمكنك الانتقال إلى [القسم التالي](#web-server-configuration).

### تثبيت PostgreSQL

#### الخطوة 1: تثبيت حزمة الخادم

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "نصيحة"

    حزم التوزيعة قد تتأخر عن إصدار PostgreSQL الحالي. إذا احتجت إلى إصدار أحدث محدد، استخدم المستودع الرسمي الخاص بـ [PostgreSQL apt أو yum](https://www.postgresql.org/download/linux/).

#### الخطوة 2: تهيئة عنقود قاعدة البيانات

على **عائلة Debian**، الحزمة تُنشئ وتبدأ العنقود تلقائيًا — انتقل إلى الخطوة التالية.

على **عائلة RHEL**، يجب إنشاء العنقود صراحة:

```bash
sudo postgresql-setup --initdb
```

#### الخطوة 3: بدء وتمكين الخدمة

```bash
sudo systemctl enable --now postgresql
```

هذا يبدأ PostgreSQL فورًا ويضبطه ليعمل تلقائيًا عند الإقلاع.

#### الخطوة 4: التحقق من التثبيت

```bash
psql --version
sudo systemctl status postgresql
```

يجب أن ترى إصدار PostgreSQL وخدمة في حالة `active (running)`.

#### الخطوة 5: الاتصال بالخادم

حزمة PostgreSQL على Linux تنشئ حساب نظامي `postgres` الذي يملك العنقود. اتصل من خلاله:

```bash
sudo -u postgres psql
```

!!! note "ملاحظة — يختلف Linux عن Windows هنا"

    مُثبِّت Windows يطالبك بتعيين كلمة مرور لمستخدم `postgres` أثناء التثبيت. حزم Linux لا تفعل ذلك. بدلًا من ذلك، تُجرى المصادقة على الاتصالات المحلية عبر **peer authentication**: يُسمح لمستخدم نظام التشغيل `postgres` بالاتصال كمستخدم قاعدة بيانات `postgres` بدون كلمة مرور.

    لهذا السبب يستخدم الأمر أعلاه `sudo -u postgres`. يتصل digna backend عبر TCP باسم مستخدم وكلمة مرور، لذا ستنشئ مستخدمًا صريحًا لـ digna في [التثبيت الابتدائي](#initial-installation).

#### الخطوة 6: تأكيد المنفذ

المنفذ الافتراضي لـ PostgreSQL هو `5432`. لتأكيد المنفذ الذي يستمع عليه خادمك:

```bash
sudo -u postgres psql -c "SHOW port;"
```

دوّن هذه القيمة — ستحتاجها عند تكوين backend الخاص بـ digna.

#### الخطوة 7: تمكين مصادقة كلمات المرور لمستخدم digna

digna يتصل بـ PostgreSQL عبر TCP كمستخدم `digna_user`، ويتطلب ذلك مصادقة بكلمة مرور بدلًا من peer authentication. تحقق أن `pg_hba.conf` يسمح بذلك.

حدد موقع الملف:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

افتحه بمحرر وتأكد أن الأسطر الخاصة بالاتصالات TCP المحلية تستخدم `scram-sha-256` (أو `md5` على الخوادم الأقدم) بدلاً من `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

أعد تحميل PostgreSQL بعد أي تغيير:

```bash
sudo systemctl reload postgresql
```

!!! warning "مهم"

    إذا أبلغت digna عن `FATAL: Ident authentication failed for user "digna_user"`, فهذه الإعدادات هي السبب.

#### الخطوة 8: إذا كان PostgreSQL يعمل على جهاز آخر

للسماح بالاتصالات من مضيف مختلف، اضبط `listen_addresses` في `postgresql.conf` وأضف سطر `host` مناسبًا لشبكتك في `pg_hba.conf`:

```
listen_addresses = '*'
```

ثم افتح المنفذ في جدار الحماية وأعد تشغيل الخدمة:

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## تهيئة خادم الويب {: #web-server-configuration }

تتطلب digna خادم ويب لاستضافة الواجهة. اختر أحد الخيارات التالية:

- [nginx](#nginx-setup) — خفيف ومُوصى به
- [Apache httpd](#apache-setup) — بديل واسع الانتشار

تحتاج فقط إلى تثبيت وتكوين **أحد** هذين الخادمين.

تقوم كلا القسمين بتكوين أمرين تعتمد عليهما الواجهة:

- **استرجاع تطبيق الصفحة الواحدة (single-page-application fallback)**، حتى لا يعيد تحديث عنوان URL في لوحة التحكم خطأ 404
- **نوع MIME للاحقة `.md`**، حتى تُخدَمّ ملفات Markdown بشكل صحيح

### إعداد nginx {: #nginx-setup }

#### نظرة عامة

nginx هو خادم ويب خفيف وعالي الأداء مناسب جيدًا لخدمة لوحة تحكم digna الثابتة.

#### التثبيت

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### بدء nginx

```bash
sudo systemctl enable --now nginx
```

#### التحقق من التثبيت

1. افتح المتصفح
2. انتقل إلى `http://localhost`
3. يجب أن ترى صفحة الترحيب الخاصة بـ nginx

#### فتح جدار الحماية

إذا كان الخادم مُتاحًا من أجهزة أخرى، سمح بحركة HTTP:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### تكوين موقع للوحة التحكم

nginx يضمن تضمين كل ملف في دليل `conf.d` على كلتا العائلتين. أنشئ ملف تهيئة مخصص لـ digna هناك:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

ألصق التالي، مع استبدال `/opt/digna/dashboard` بالمسار الفعلي لمجلد `dashboard` المستخرج لديك:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
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

    بدون توجيه `try_files`، يؤدي إعادة تحميل أي صفحة في لوحة التحكم غير صفحة الجذر إلى 404. هذا مكافئ nginx لوظيفة URL Rewrite المطلوبة في IIS على Windows.

#### تعطيل الموقع الافتراضي

يمكن أن يكون بلوك سيرفر واحد فقط هو الـ `default_server` لمنفذ. على **عائلة Debian**، احذف الإعداد الافتراضي المعبأ حتى لا يتعارض:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

على **عائلة RHEL**، علّق أو احذف بلوك `server { ... }` داخل `/etc/nginx/nginx.conf`.

#### تطبيق التهيئة

اختبر التهيئة لصياغة صحيحة، ثم أعد تحميل nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### إعداد Apache httpd {: #apache-setup }

#### نظرة عامة

Apache httpd متوفر في مستودعات التوزيعة الافتراضية لكل توزيعة مدعومة. اسم الحزمة هو `apache2` على عائلة Debian و `httpd` على عائلة RHEL.

#### التثبيت

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### بدء Apache

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### التحقق من التثبيت

1. افتح المتصفح
2. انتقل إلى `http://localhost`
3. يجب أن ترى صفحة Apache الافتراضية لتوزيعتك

#### مطلوب: تفعيل mod_rewrite

تتطلب الواجهة إعادة كتابة عناوين URL.

على **عائلة Debian**، فعّل الوِحدة وأعد التشغيل:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

على **عائلة RHEL**، `mod_rewrite` محمّل افتراضيًا. تأكد من وجوده:

```bash
httpd -M | grep rewrite
```

#### مطلوب: السماح بتجاوزات .htaccess

افتح ملف التهيئة لجذر المستندات:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

حدِّد بلوك `<Directory>` الذي يغطي جذر المستندات (`/var/www/html` على كلتا العائلتين) وغيّر:

```apache
AllowOverride None
```

إلى:

```apache
AllowOverride All
```

#### مطلوب: نوع MIME لملفات Markdown

في نفس الملف، أضف السطر التالي حتى تُخدم ملفات Markdown بشكل صحيح:

```apache
AddType text/markdown .md
```

!!! warning "مهم"

    بدون هذا الإعداد، قد لا تُخدم ملفات `.md` بشكل صحيح.

#### تطبيق التهيئة

تحقق من التهيئة لصياغة صحيحة، ثم أعد تشغيل Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## التثبيت الابتدائي {: #initial-installation }

### الخطوة 1: إعداد مستودع digna

مستودع digna يخزن جميع المقاييس المحسوبة بواسطة digna. يعمل كقاعدة بيانات مركزية للبيانات التحليلية وأداء النظام.

#### إنشاء مخطط المستودع والمستخدم

افتح عميل PostgreSQL الخاص بك (psql، pgAdmin، أو ما شابه) ونفّذ أوامر SQL التالية:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**استبدل العناصر النائبة التالية:**

- `<digna_repo_schema>` — اسم المخطط المطلوب (مثلاً `dignarepo`)
- `<digna_repo_user>` — اسم المستخدم المطلوب (مثلاً `digna_user`)
- `<digna_repo_password>` — كلمة مرور آمنة لهذا المستخدم

**مثال:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

لتنفيذ هذه الأوامر من الشل في خطوة واحدة:

```bash
sudo -u postgres psql
```

ثم ألصق العبارات عند موجه `postgres=#` واكتب `\q` للخروج.

!!! tip "أفضل ممارسة"

    استخدم كلمات مرور قوية ومعقدة لمستخدمي قاعدة البيانات. تجنّب بيانات اعتماد سهلة التخمين.

---

### الخطوة 2: فك حزمة تثبيت digna

1. حدّد ملف ZIP لتثبيت digna المزوَّد لك
2. فكّه في موقع التثبيت الذي تريده — على سبيل المثال `/opt/digna`
3. بعد الفك، يجب أن ترى العناصر التالية:
   - `dashboard/` — واجهة الويب
   - `digna` — الملف التنفيذي الرئيسي (backend + CLI مدمجان)

!!! info "ملفا التهيئة والترخيص غير موجودين في الحزمة"

    لا يأتي `config.toml` ولا `dashboard/dashboard_config.toml` مع التثبيت — بل تنشئ كليهما بنفسك، في
    [تهيئة الواجهة الخلفية](#backend-configuration) و
    [تهيئة لوحة التحكم](#dashboard-configuration). ولا يأتي `license.toml` معه كذلك؛
    إذ يقدّمه digna بشكل منفصل، كما هو موضّح في الخطوة 3.

لفك الضغط من الشل:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
```

!!! note "ملاحظة"

    إذا لم يكن `unzip` مثبتًا، أضفه بـ `sudo apt install -y unzip` أو `sudo dnf install -y unzip`.

#### جعل الملف التنفيذي قابلاً للتشغيل

اعتمادًا على طريقة نقل الأرشيف، قد لا تحتفظ بيانات الترخيص بحقوق التنفيذ عند الفك. اضبطها صراحة:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### إنشاء حساب خدمة

يوصى بتشغيل الخلفية كمستخدم غير مميز مخصص للإنتاج:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "ملاحظة"

    على عائلة RHEL، مسار الشِل المعادل هو `/sbin/nologin`.

### الخطوة 3: تثبيت ملف الترخيص

!!! warning "مهم"

    ملف الترخيص **غير** متضمن في حزمة التثبيت وسيزوَّد لك منفصلًا من digna.

1. حدّد ملف `license.toml` المزود لك
2. انسخه إلى دليل تثبيت digna الجذري (حيث يوجد `config.toml` والملف التنفيذي `digna`)

**لماذا هذا مهم:**
يحتوي ملف الترخيص على معلومات العميل، تاريخ انتهاء الترخيص، والتوقيع الرقمي. **لا تُعدِّل هذا الملف** — أي تغيّر سيبطله.

**هيكل الدليل بعد الإعداد:**

```
/opt/digna/
├── config.toml         (ملف التهيئة)
├── license.toml        (ملف الترخيص الخاص بك - انسخه هنا)
├── digna               (الملف التنفيذي الرئيسي)
├── bin/                (سكريبتات إدارة الخدمة)
└── dashboard/          (واجهة الويب)
    └── (ملفات الdashboard)
```

---

## تكوين الخلفية (Backend) {: #backend-configuration }

### الخطوة 1: إنشاء وتحرير ملف التهيئة

ملف `config_template.toml` مُقدم في دليل تثبيت digna. كل ما عليك هو إعادة تسميته إلى `config.toml`.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**الموقع:** `/opt/digna/config.toml`

افتح `config.toml` في محرر نصّي وقم بتكوين كل قسم أدناه.

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

    إذا كنت تخدم الواجهة من nginx أو Apache على منفذ HTTP الافتراضي، فالأصل المسموح هو `http://localhost` — أو عنوان الخادم العام عندما تُصل الواجهة من أجهزة أخرى.

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
| `DIGNA_REPO_SCHEMA` | `dignarepo` | المخطط الذي أنشأته سابقًا |
| `DIGNA_REPO_USER` | `digna_user` | المستخدم الذي أنشأته في إعداد PostgreSQL |
| `DIGNA_REPO_PASSWORD` | كلمة مرورك | كلمة المرور التي عيّنتها أثناء إنشاء المخطط |
| `DIGNA_REPO_SSLMODE` | `prefer` (افتراضي) | اختياري. وضع SSL في PostgreSQL: `disable` أو `allow` أو `prefer` أو `require` أو `verify-ca` أو `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (افتراضي) | اختياري. عدد الاتصالات التي يُبقيها digna مفتوحة مع المستودع |

!!! tip "أفضل ممارسة"

    يحتوي `config.toml` على كلمة مرور قاعدة البيانات كنص صريح. قيد أذوناته بحيث لا يقرأه سوى حساب الخدمة:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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

    لمعرفة عدد أنوية CPU المتاحة على الخادم، شغّل `nproc`.

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
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | الافتراضي: الدليل المؤقت للنظام (`$TMPDIR`، أو `/tmp` إذا لم يكن معيّنًا) | دليل الملفات المؤقتة عندما لا تتسع الذاكرة للبيانات |

!!! tip "تحديد حجم digna Engine"

    خطّط لما يصل إلى `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` من الذاكرة على مضيف
    digna، فوق ما يستخدمه digna نفسه، ولمساحة قرص حرة كافية في الدليل المؤقت تتسع لأكبر تاريخ
    مفحوص من مصادر البيانات التي تستخدم digna Engine. وجّه `DIGNA_DUCKDB_TEMP_DIRECTORY` إلى قرص
    تتوفر فيه هذه المساحة ويستطيع الحساب الذي يشغّل digna الكتابة فيه:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
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

1. افتح طرفية
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

    على Linux، الدليل الحالي ليس في PATH، لذا يُستدعى الملف التنفيذي كـ `./digna` بدلًا من `digna`. لاستخدام الشكل الأقصر في كل مكان، أضف رابطًا رمزيًا:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
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

### الخطوة 5: إنشاء مستخدم مشرف

1. افتح نافذة طرفية **جديدة**
2. انتقل إلى دليل تثبيت digna
3. شغّل الأمر التالي لإنشاء مستخدم مشرف:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**مثال:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

يؤدي ذلك إلى إنشاء مستخدم بعنوان البريد الإلكتروني `admin@example.com` وامتيازات إدارية كاملة.

!!! tip "نصيحة"

    ضمّن كلمة المرور بين علامات اقتباس مفردة. تتعامل `bash` و `zsh` مع الأحرف مثل `!` و `$` و `*` بشكل خاص، وكلمة مرور غير محاطة قد لا تُمرَّر كما كتبت.

!!! tip "أفضل ممارسة"

    استخدم كلمة مرور قوية تضم مزيجًا من أحرف كبيرة وصغيرة وأرقام ورموز خاصة.

---

### الخطوة 6: بدء خادم digna

في دليل تثبيت digna، ابدأ الخادم بـ:

```bash
./digna serve --address <host> --port <port>
```

**المعلمات:**
- `--address` — اسم المضيف/عنوان IP للخادم (الافتراضي `127.0.0.1`)
- `--port` — منفذ الخادم (الافتراضي `8000`)

عندما يعمل الخادم، يطبع العنوان الذي يستمع عليه:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "نصيحة"

    إذا كانت الواجهة تُخدم من جهاز مختلف عن الـ backend، افتح منفذ API أيضًا في جدار الحماية:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "الخادم يشغل الطرفية"

    يعمل `serve` في المقدمة ويستمر حتى توقفه بالضغط على ++ctrl+c++. اتركه يعمل بينما تكمل الإعداد؛ ولتشغيله تلقائيًا عند الإقلاع بدلًا من ذلك انظر [تشغيل digna كخدمة systemd](#running-digna-as-a-systemd-service).

## تكوين الواجهة (Dashboard) {: #dashboard-configuration }

### الخطوة 1: نشر الواجهة على خادم الويب

تقرأ لوحة digna تهيئتها الخاصة من `dashboard/dashboard_config.toml`. هذا الملف لا يأتي مع التثبيت — بل تنشئه في دليل `dashboard/` إلى جانب ملفات لوحة التحكم.

محتوياته موضّحة في [الدخول الموحّد (SSO)](../../../sso/overview.md)، وهناك أيضًا يلزم الملف: فهو يحمل خيارات تسجيل الدخول التي تعرضها لوحة التحكم، وفي عمليات النشر متعددة النسخ، اتصال الواجهة الخلفية.

اختر خادم الويب واتبع خطوات النشر المناسبة.

#### النشر على nginx

إذا اتبعت قسم [إعداد nginx](#nginx-setup)، فإن بلوك السيرفر يشير بالفعل إلى مجلد `dashboard` ولا حاجة للنسخ.

1. **أكد المسار**
   - افتح `/etc/nginx/conf.d/digna.conf`
   - تحقق أن `root` يشير إلى مجلد `dashboard` المستخرج

2. **تأكد من أن المجلد قابل للقراءة**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **أعد تحميل nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **اختبر التثبيت**
   - افتح المتصفح
   - انتقل إلى `http://localhost` (أو عنوان الـ URL المكوّن)
   - يجب أن ترى صفحة تسجيل دخول لوحة digna

#### النشر على Apache httpd

1. **انسخ الواجهة إلى جذر المستندات**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **أضف قواعد إعادة الكتابة**

   أنشئ ملف `.htaccess` داخل المجلد المنشور ليظلّت مسارات الواجهة صالحة بعد تحديث المتصفح:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
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
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **افتح الواجهة**
   - افتح المتصفح
   - انتقل إلى `http://localhost/digna`
   - يجب أن ترى صفحة تسجيل دخول لوحة digna

### الخطوة 2: SELinux (عائلة RHEL فقط)

على RHEL، Rocky، AlmaLinux و Fedora، يكون SELinux في الوضع المطبق (enforcing) افتراضيًا وسيمنع خادم الويب من قراءة الملفات خارج المواقع المتوقعة. تحقّق ما إذا كان مفعلًا:

```bash
getenforce
```

إذا كانت النتيجة `Enforcing` وكنت تخدم الواجهة من `/opt/digna/dashboard`، صنف المجلد بحيث يتمكن خادم الويب من قراءته:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "ملاحظة"

    إذا لم تجد `semanage`، ثبِّته بـ `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "مهم"

    غالبًا ما يكون سبب ظهور **403 Forbidden** على خادم RHEL مهيأ حديثًا هو مشكلة في تمييز SELinux وليس في أذونات الملفات. تأكد باستخدام `sudo ausearch -m avc -ts recent`.

---

## تشغيل digna كخدمة systemd {: #running-digna-as-a-systemd-service }

### لماذا تشغيل digna كخدمة؟

تشغيل backend الخاص بـ digna كخدمة systemd يضمن أنه:

- يبدأ تلقائيًا عند إقلاع الجهاز
- يعمل في الخلفية دون نافذة طرفية مفتوحة
- يعاد تشغيله تلقائيًا إذا تعطل
- يمكن إدارته عبر `systemctl`، مدير الخدمات القياسي على Linux

### ملفات إدارة الخدمة

جميع الملفات اللازمة موجودة في دليل تثبيت digna تحت: `bin/`

السكريبتات الشل التالية متاحة:

- `install_service.sh` — يسجل digna لدى systemd
- `uninstall_service.sh` — يلغى تسجيل الخدمة
- `start_service.sh` — يبدء الخدمة المسجلة
- `stop_service.sh` — يوقف الخدمة الجارية

!!! warning "مطلوب صلاحيات الروت"

    يجب تنفيذ جميع السكريبتات باستخدام `sudo`، لأن تسجيل خدمة تبدأ عند الإقلاع يكتب ملف وحدة إلى `/etc/systemd/system`.

### جعل السكريبتات قابلة للتنفيذ

قد لا تحافظ عملية الفك على بت التنفيذ. قبل الاستخدام الأول:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### تثبيت الخدمة

1. **افتح طرفية**

2. **انتقل إلى مجلد bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **شغّل سكريبت التثبيت**
   ```bash
   sudo ./install_service.sh
   ```

تم الآن تسجيل خادم digna لدى systemd مع تمكين بدء التشغيل التلقائي. الخدمة لا تبدأ فورًا — راجع القسم التالي لبدءها.

### بدء وإيقاف الخدمة

#### لبدء الخدمة

1. افتح طرفية
2. انتقل إلى `/opt/digna/bin`
3. شغّل:
   ```bash
   sudo ./start_service.sh
   ```

#### لإيقاف الخدمة

1. افتح طرفية
2. انتقل إلى `/opt/digna/bin`
3. شغّل:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "نصيحة"

    أوقف الخدمة دائمًا قبل تحديث ملفات التطبيق.

### إدارة الخدمة عبر systemctl

بعد التسجيل، يمكن أيضًا التحكم بالخدمة باستخدام أوامر systemd القياسية من أي دليل:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### التحقق من الخدمة

للتأكد أن الخدمة مسجلة وتعمل:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` يعني أن الخدمة تبدأ عند الإقلاع؛ `active` يعني أنها تعمل الآن.

### عرض سجلات الخدمة

يقوم systemd بالتقاط كل ما يطبعه الـ backend على الطرفية. لقراءته:

```bash
sudo journalctl -u digna -n 100
```

لمتابعة السجل مباشرًة أثناء إعادة إنتاج المشكلة:

```bash
sudo journalctl -u digna -f
```

!!! tip "نصيحة"

    هذه أسرع طريقة لتشخيص خدمة تبدأ ثم تتوقف فورًا. فشل اتصال المستودع أو افتقار `license.toml` يُبلغ عنه هنا.

### نقل الخدمة إلى دليل جديد

ملف الوحدة يخزن المسار المطلق للملف التنفيذي، لذا يتطلب نقل التثبيت إعادة تسجيل الخدمة:

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

1. **أوقف الخدمة الجارية**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **أزل الخدمة**
   ```bash
   sudo ./uninstall_service.sh
   ```

تم الآن إلغاء تسجيل خادم digna من systemd.

---

## الترقية إلى إصدار جديد {: #upgrading-to-a-new-release }

يشرح هذا القسم ترقية تثبيت الإصدار 2026.06 إلى الإصدار 2026.11.

!!! warning "الترقية من إصدار أقدم من 2026.06"

    نفّذ أولًا خطوات الترقية إلى الإصدار 2026.06: [الترقية إلى إصدار جديد](../Release%202026.06/installation_guide_digna_linux_2026_06.md#upgrading-to-a-new-release). ثم تابع بالخطوات أدناه.

### قبل الترقية

**النسخ الاحتياطي لمستودع digna إلزامي**

قبل ترقية digna، اعمل نسخة احتياطية من مستودعك (PostgreSQL) لحماية بياناتك من الضياع.
النسخة الاحتياطية تضمن إمكانية الاسترداد إذا واجهت الترقية مشكلات غير متوقعة.

لإنشاء نسخة احتياطية من الشل:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**طلب ملف الترخيص للإصدار 2026.11**

يحتاج الإصدار 2026.11 إلى ملف `license.toml` جديد. اطلبه من فريق digna قبل أن تبدأ، واجعله
جاهزًا لـ [الخطوة 7](#step-7-replace-the-license-file).

### عملية الترقية

#### الخطوة 1: إيقاف خدمة digna {: #step-1-stop-the-digna-service }

إذا كان digna يعمل كخدمة systemd، فأوقفه أولًا:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

إذا كان digna يعمل في المقدمة (foreground)، اضغط ++ctrl+c++ في نافذة الطرفية الخاصة به.

#### الخطوة 2: انسخ التثبيت الحالي احتياطيًا {: #step-2-backup-current-installation }

في دليل تثبيت digna، أعد تسمية الملف التنفيذي ومجلد لوحة التحكم في تثبيتك الحالي، حتى
يمكن نشر الإصدار الجديد بجوارهما:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

احتفظ بـ `digna_old` حتى تتحقق من الترقية، وبـ `dashboard_old` حتى تستعيد منه ملفات التهيئة
الخاصة بك (انظر الخطوة 4). بعد ذلك يمكنك حذفهما.

#### الخطوة 3: فك ونشر النسخة الجديدة {: #step-3-extract-and-deploy-new-version }

1. فك ملف ZIP للنسخة الجديدة من digna
2. انسخ الملف التنفيذي الجديد `digna` ومجلد `dashboard` إلى دليل التثبيت
3. أعد بت التنفيذ وملكية حساب الخدمة:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "مهم"

    لا يُضمَّن `config.toml` ولا `dashboard/dashboard_config.toml` أبدًا في
    أرشيف ZIP الخاص بالتثبيت — فريق digna لا يرسل أيًّا من الملفين أبدًا. لذلك تبقى تهيئتك الحالية
    بمنأى عن الترقية، والنسخ الموجودة في المجلدات المعاد تسميتها `*_old` هي
    النسخ الوحيدة التي لديك.

#### الخطوة 4: استعادة ملفات التهيئة الخاصة بك {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
./digna config check
```

يجب أن يُبلِّغ كل قسم بحالة OK. صحّح كل ما يُبلَّغ عنه بحالة FAILED، واحذف المفاتيح المدرجة تحت
**Unknown keys**، وأعد تنفيذ الأمر قبل المتابعة.

#### الخطوة 7: استبدال ملف الترخيص {: #step-7-replace-the-license-file }

ينتقل ملف الترخيص عادةً من إصدار إلى الإصدار الذي يليه. الإصدار 2026.11 استثناء: فهو يضيف وحدتين
مرخّصتين، digna Data Reconciliation وdigna Agentic، والترخيص الصادر قبل 2026.11 لا يتضمنهما. انسخ
ملف `license.toml` الذي قدّمه فريق digna للإصدار 2026.11 إلى دليل التثبيت، ليحل محل الملف القديم:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "لا تحتفظ بالترخيص السابق"

    مع الترخيص السابق يبدأ digna، لكن digna Data Reconciliation وdigna
    MCP Server يبقيان معطّلين. وكل أمر يتحقق من الترخيص — `user` و
    `inspection` و`repo` — يتوقف قبل أن يمسّ المستودع عند فشل التحقق. تحقّق من
    الترخيص الجديد قبل المتابعة:

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

إذا كان يعمل كخدمة systemd:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

إذا كنت تشغّله يدويًا، أعد تشغيل الخادم:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

إذا كنت تستخدم nginx أو Apache، أعد تحميل خادم الويب المعني:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

على عائلة RHEL، أعد تطبيق تمييز SELinux إذا استُبدل دليل `dashboard`:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### الخطوة 10: التحقق من الترقية {: #step-10-verify-the-upgrade }

1. تأكد من إصدار الملف التنفيذي الجديد:

    ```bash
    ./digna version
    ```

    يجب أن يكون السطر الأول `Release: 2026.11`.

2. افتح لوحة digna وتحقق من تحميل الواجهة بشكل صحيح.
3. تحقق من سجلات الخادم بحثًا عن أخطاء:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. اختبر اتصالات قواعد البيانات — انظر
   [اختبار اتصال](../../../databases/overview.md#testing-a-connection). بعد الترقية من إصدار سابق
   لـ 2026.06، حوّل أولًا إلى ODBC كل اتصال لم يكن يستخدمه بعد.

للبدء مع الوحدات الجديدة، انظر [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md)،
و[ربط وكيل ذكاء اصطناعي](../../../platform/agentic/connect_ai_agent.md) من أجل digna MCP Server،
و[موقع التنميط](../../../platform/profiling/profiling_location.md) من أجل digna Engine.