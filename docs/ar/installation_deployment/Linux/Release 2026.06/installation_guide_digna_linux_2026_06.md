---
title: دليل التثبيت على Linux – digna إصدار 2026.06 | توثيق digna
description: دليل خطوة بخطوة لتثبيت digna إصدار 2026.06 على Linux — متطلبات النظام، إعداد PostgreSQL، تهيئة nginx أو Apache، تكوين الbackend و الdashboard، تشغيل digna كخدمة systemd، والترقية إلى إصدار جديد.
keywords: digna تثبيت linux, دليل نشر digna, إعداد backend لـ digna, تثبيت لوحة تحكم digna, postgresql linux, nginx linux, خدمة systemd digna, دليل ترقية digna
image: /assets/logo_square.png
---

# دليل التثبيت على Linux لـ digna إصدار 2026.06

**الإصدار:** 2026.06

**آخر تحديث:** 5 سبتمبر 2026


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

- **dignabackend**: المحرك الأساسي للتطبيق، المسؤول عن معالجة البيانات وتنفيذ فحوصات الجودة.
- **dignadashboard**: واجهة ويب مستضافة على خادم ويب، توفّر وسيلة سهلة التفاعل مع منصة digna وتصوّر مقاييس جودة البيانات.

### ما الجديد في إصدار 2026.06

يجلب هذا الإصدار قدرات مراقبة البيانات داخل الشيفرة نفسها، مما يتيح للمطورين مراقبة جودة البيانات من المصدر. راجع [ملاحظات الإصدار](http://docs.digna.ai/changelog/Release_202606/) للتفاصيل الكاملة.

### تبحث عن Windows أو macOS؟

يغطي هذا الدليل Linux. للمنصات الأخرى، راجع [دليل التثبيت على Windows](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) أو [دليل التثبيت على macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

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
   - `config.toml` — ملف التهيئة
   - `license.toml` — ملف الترخيص (انسخ ملف الترخيص الخاص بك هنا)

لفك الضغط من الشل:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
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

هذا القسم يضبط إعدادات تطبيق backend الخاص بـ digna:

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
| `digna_APP_HOST` | `localhost` أو عنوان IP | اسم المضيف أو IP حيث يتم استضافة dignabackend |
| `digna_APP_PORT` | `8082` (افتراضي) | منفذ نقاط REST API |
| `digna_APP_CORS_ALLOW_ORIGINS` | عنوان الواجهة الأمامية | إذا كانت الواجهة على خادم مختلف، أضف عنوانها هنا |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | مطلوب للـ CORS مع الاعتمادات |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | السماح بجميع طرق HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | السماح بجميع الرؤوس |

!!! note "ملاحظة"

    إذا كنت تخدم الواجهة من nginx أو Apache على منفذ HTTP الافتراضي، فالأصل المسموح هو `http://localhost` — أو عنوان الخادم العام عندما تُصل الواجهة من أجهزة أخرى.

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
| `digna_REPO_SCHEMA` | `dignarepo` | المخطط الذي أنشأته سابقًا |
| `digna_REPO_USER` | `digna_user` | المستخدم الذي أنشأته في إعداد PostgreSQL |
| `digna_REPO_PASSWORD` | كلمة مرورك | كلمة المرور التي عيّنتها أثناء إنشاء المخطط |

!!! tip "أفضل ممارسة"

    يحتوي `config.toml` على كلمة مرور قاعدة البيانات كنص صريح. قيد أذوناته بحيث لا يقرأه سوى حساب الخدمة:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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
| `digna_FERNET_KEY` | مفتاح تشفير | يُستخدم لتشفير الرموز وملفات تعريف الارتباط (يوجد مفتاح افتراضي) |
| `digna_COOKIE_DOMAIN` | `localhost` | طابق نطاق الواجهة الأمامية |
| `digna_COOKIE_SECURE` | `false` (محلي) / `true` (إنتاج) | استخدم `true` للاتصالات عبر HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | مفعل دائمًا لأسباب أمنية |
| `digna_COOKIE_SAME_SITE` | `lax` | يقي من هجمات CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ساعة) | مهلة الجلسة بالثواني |
| `digna_MAX_WORKERS` | عدد أنوية CPU - 1 | عدد مهام الفحص المتوازية |

!!! tip "نصيحة"

    لمعرفة عدد أنوية CPU المتاحة على الخادم، شغّل `nproc`.

#### قسم [logging]

هذا القسم يضبط سلوك التسجيل:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| المعامل | القيمة | ملاحظات |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` أو `DEBUG` | `INFO` للإنتاج، `DEBUG` لاستكشاف الأخطاء |
| `digna_LOGGING_BACKUP_COUNT` | `10` | عدد نُسَخ التسجيل اليومية التي سيتم الاحتفاظ بها |

---

### الخطوة 2: تهيئة المستودع

1. افتح طرفية
2. انتقل إلى دليل تثبيت digna (حيث يوجد `config.toml` والملف التنفيذي `digna`)
3. شغّل اختبار الاتصال:

```bash
cd /opt/digna
./digna repo check
```

يجب أن ترى تأكيدًا على نجاح الاتصال (المستودع نفسه لم يُهيأ بعد).

!!! note "ملاحظة"

    على Linux، الدليل الحالي ليس في PATH، لذا يُستدعى الملف التنفيذي كـ `./digna` بدلًا من `digna`. لاستخدام الشكل الأقصر في كل مكان، أضف رابطًا رمزيًا:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### الخطوة 3: تثبيت مخطط المستودع

في نفس الدليل، شغّل:

```bash
./digna repo install
```

يُنشئ هذا الأمر الجداول والمخططات اللازمة في قاعدة بيانات PostgreSQL الخاصة بك.

### الخطوة 4: بدء خادم digna

في دليل تثبيت digna، ابدأ الخادم بـ:

```bash
./digna serve --address <host> --port <port>
```

**المعلمات:**
- `--address` — اسم المضيف/عنوان IP للخادم
- `--port` — منفذ الخادم

يجب أن ترى رسائل بدء تُؤكِّد أن الخادم يعمل:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "نصيحة"

    إذا كانت الواجهة تُخدم من جهاز مختلف عن الـ backend، افتح منفذ API أيضًا في جدار الحماية:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

### الخطوة 5: إنشاء مستخدم مشرف

1. افتح نافذة طرفية **جديدة**
2. انتقل إلى دليل تثبيت digna
3. شغّل الأمر التالي لإنشاء مستخدم مشرف:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**مثال:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

يُنشيء هذا مستخدمًا باسم `admin` بصلاحيات إدارية كاملة.

!!! tip "نصيحة"

    ضمّن كلمة المرور بين علامات اقتباس مفردة. تتعامل `bash` و `zsh` مع الأحرف مثل `!` و `$` و `*` بشكل خاص، وكلمة مرور غير محاطة قد لا تُمرَّر كما كتبت.

!!! tip "أفضل ممارسة"

    استخدم كلمة مرور قوية تضم مزيجًا من أحرف كبيرة وصغيرة وأرقام ورموز خاصة.

---

## تكوين الواجهة (Dashboard) {: #dashboard-configuration }

### الخطوة 1: نشر الواجهة على خادم الويب

تمتلك لوحة digna ملف `config.toml` منفصلًا داخل دليل `dashboard/`. هذا التكوين مُقدّم بالفعل ولا يتطلب تغييرات أثناء الإعداد الابتدائي. تحتاج لتعديله فقط إذا أردت تخصيص اتصال الـ backend.

إذا احتجت لتعديل تهيئة الواجهة (مثلًا لانتشار متعدد النسخ)، ارجع إلى توثيق الواجهة.

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

### قبل الترقية

**النسخ الاحتياطي لمستودع digna إلزامي**

قبل ترقية digna، اعمل نسخة احتياطية من مستودعك (PostgreSQL) لحماية بياناتك من الضياع.
النسخة الاحتياطية تضمن إمكانية الاسترداد إذا واجهت الترقية مشكلات غير متوقعة.

لإنشاء نسخة احتياطية من الشل:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### عملية الترقية

#### الخطوة 1: إيقاف خدمة digna

إذا كانت digna تعمل كخدمة systemd، أوقفها أولًا:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

إذا كانت تعمل في المقدمة (foreground)، اضغط `Ctrl + C` في نافذة الطرفية الخاصة بها.

#### الخطوة 2: نسخ احتياطي للتثبيت الحالي للـ backend

في دليل تثبيت digna:

```bash
cd /opt/digna
sudo mv digna digna_old
```
```bash
sudo mv dashboard dashboard_old
```

#### الخطوة 3: فك ونشر النسخة الجديدة

1. فك ملف ZIP للنسخة الجديدة من digna
2. انسخ الملف التنفيذي الجديد `digna` ومجلد `dashboard` إلى دليل التثبيت
3. أعد بت التنفيذ وملكية حساب الخدمة:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "مهم"

    ملف `config.toml` **غير** مضمن أبدًا في أرشيف التثبيت. تظل تهيئتك الحالية سليمة.

### الخطوة 4: استعادة ملفات التهيئة الخاصة بك

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### الخطوة 5: ترقية مخطط المستودع

انتقل إلى دليل تثبيت digna وشغّل:

```bash
cd /opt/digna
./digna repo upgrade
```

سيحدِّث هذا مخطط PostgreSQL إلى أحدث إصدار مع المحافظة على جميع البيانات الحالية.

### الخطوة 6: إعادة تشغيل الخدمات

إذا كانت تعمل كخدمة systemd:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

إذا كنت تديرها يدويًا، أعد تشغيل الخادم:

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

#### الخطوة 7: التحقق من الترقية

1. افتح لوحة digna
2. تحقق من تحميل الواجهة بشكل صحيح
3. تحقق من سجلات الخادم لأي أخطاء:

```bash
sudo journalctl -u digna -n 100
```