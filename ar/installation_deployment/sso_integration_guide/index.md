# دليل تكامل تسجيل الدخول الموحد

---

## جدول المحتويات

1. [مقدمة ونظرة عامة](#introduction-and-overview)
2. [خطوات التكوين](#configuration-steps)
3. [تكوين لوحة التحكم](#dashboard-configuration)
4. [تكوين الواجهة الخلفية](#backend-configuration)
5. [اختبار تسجيل الدخول](#testing-login)
6. [استكشاف الأخطاء وإصلاحها](#troubleshooting)
7. [المزودون المدعومون](#supported-providers)

---

## مقدمة ونظرة عامة {: #introduction-and-overview }

يوفر هذا الدليل تعليمات خطوة بخطوة لدمج تسجيل الدخول الموحد (SSO) مع منصة digna باستخدام **OpenID Connect (OIDC)**.

### ما هو SSO؟

يسمح تسجيل الدخول الموحد للمستخدمين بتسجيل الدخول إلى digna بأمان باستخدام بيانات اعتماد المؤسسة الخاصة بهم عبر مزودي هوية خارجيين. يمكن للمستخدمين المصادقة باستخدام بيانات اعتماد المؤسسة بدلًا من إدارة كلمات مرور منفصلة لـ digna.

### كيف يعمل

يتم تنفيذ SSO في digna باستخدام بروتوكول OIDC. يمكن تكوين مزودي هوية متعددين بالتوازي عن طريق تعديل ملفين أساسيين:

- **`dashboard_config.toml`** — يتحكم بواجهة تسجيل الدخول في الواجهة الأمامية
- **`config.toml`** — يكوّن اتصالات OIDC في الواجهة الخلفية

### المزودون المدعومون {: #supported-providers-overview }

الأمثلة في هذا الدليل تستخدم **Microsoft** و **Google**، لكن **أي مزود متوافق مع OIDC** يمكن دمجه باتباع نفس الهيكل.

من مزودي OIDC الشائعين:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- مزودو هوية آخرون متوافقون مع OIDC

---

## خطوات التكوين {: #configuration-steps }

يتطلب تكوين SSO تحديث ملفين. يشرح هذا القسم كيفية تكوين كل منهما.

### نظرة عامة على ملفات التكوين

| الملف | الموقع | الغرض |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | واجهة تسجيل الدخول في الواجهة الأمامية |
| **config.toml** | `/config.toml` | اتصالات OIDC في الواجهة الخلفية |

يجب تكوين كلا الملفين لكي يعمل SSO بشكل صحيح.

---

## تكوين لوحة التحكم {: #dashboard-configuration }

### موقع الملف

```
dashboard/dashboard_config.toml
```

### الخطوة 1: إضافة مزودي OIDC

أضف مدخلات تحت مصفوفة `[[login.oidc]]` لكل مزود هوية تريد دعمه.

**مثال مع Microsoft و Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "تسجيل الدخول باستخدام Microsoft"

[[login.oidc]]
key = "google"
label = "تسجيل الدخول باستخدام Google"
```

### الخطوة 2: تكوين خيارات تسجيل الدخول

حدد ما إذا كان يجب السماح بتسجيل الدخول باستخدام كلمة المرور:

```toml
[login]
usePassword = true
```

### معلمات التكوين

#### قسم `[[login.oidc]]`

| المعامل | النوع | مطلوب | الوصف |
|---|---|---|---|
| `key` | string | نعم | معرف فريد لاتصال OIDC (يجب أن يطابق المفتاح في config.toml) |
| `label` | string | نعم | النص المعروض على زر الدخول (مثل "تسجيل الدخول باستخدام Microsoft") |

#### قسم `[login]`

| المعامل | النوع | الافتراضي | الوصف |
|---|---|---|---|
| `usePassword` | boolean | false | السماح بتسجيل الدخول باستخدام كلمة المرور بالإضافة إلى SSO |

### فهم usePassword

**إذا كان `usePassword = true`:**
- شاشة تسجيل الدخول تعرض أزرار SSO (مثل "تسجيل الدخول باستخدام Microsoft")
- شاشة تسجيل الدخول تعرض أيضًا حقول اسم المستخدم وكلمة المرور
- يمكن للمستخدمين المصادقة بأي من الطريقتين
- يسمح بإعدادات هجينة حيث يستخدم بعض المستخدمين SSO والآخرون كلمات مرور

**إذا كان `usePassword = false` (أو تم حذفه):**
- شاشة تسجيل الدخول تعرض أزرار SSO فقط
- لا توجد حقول اسم المستخدم/كلمة المرور
- المصادقة تكون متاحة فقط عبر OIDC

!!! tip "تلميح"

    تسجيل الدخول باستخدام كلمة المرور متاح فقط للمستخدمين الذين تم إنشاؤهم بكلمات مرور عبر أمر `digna user add` أو عبر لوحة التحكم.

### مثال مكتمل

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "تسجيل الدخول باستخدام Microsoft"

[[login.oidc]]
key = "google"
label = "تسجيل الدخول باستخدام Google"

[[login.oidc]]
key = "okta"
label = "تسجيل الدخول باستخدام Okta"
```

---

## تكوين الواجهة الخلفية {: #backend-configuration }

### موقع الملف

```
/config.toml
```

(دليل تثبيت digna الجذري)

### الخطوة 1: إضافة أقسام مزود OIDC

يجب أن يحتوي كل مزود على قسم مخصص `[oidc.<key>]`. يجب أن يطابق المفتاح المفتاح المعرفة في `dashboard_config.toml`.

### تكوين Microsoft

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### تكوين Google

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### معلمات التكوين

| المعامل | النوع | مطلوب | الوصف | مثال |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | نعم | معرف العميل من مزود الهوية | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | نعم | سر العميل من مزود الهوية | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | نعم | عنوان الاستدعاء بعد المصادقة | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | نعم | نقطة تكوين OIDC | `https://login.microsoftonline.com/...` |

!!! warning "هام"

    استبدل القيم النائبة (`<client_id>`, `<client_secret>`, `<tenant_id>`) بالبيانات الفعلية من بوابة مطوري مزود الهوية الخاص بك.

### عنوان الاستدعاء (Redirect URI)

يجب أن يكون عنوان الاستدعاء نفس الموجود في إعدادات مزود الهوية:

```
http://localhost:5173/oidc/callback
```

إذا كان digna مستضافًا على نطاق مختلف، قم بالتحديث وفقًا لذلك:
- محليًا: `http://localhost:5173/oidc/callback`
- في الإنتاج: `https://digna.yourdomain.com/oidc/callback`

### مثال مكتمل

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## اختبار تسجيل الدخول {: #testing-login }

بعد إكمال التكوين، تحقق من أن SSO يعمل بشكل صحيح.

### قائمة التحقق قبل الاختبار

قبل الاختبار تأكد من:

- [ ] تم تحديث `dashboard_config.toml` بمزودي OIDC
- [ ] تم تحديث `config.toml` ببيانات اعتماد OIDC
- [ ] تم حفظ كلا الملفين
- [ ] بيانات الاعتماد صحيحة (client ID، client secret)
- [ ] عنوان الاستدعاء يطابق عنوان نشر التطبيق
- [ ] تم تكوين تطبيق مزود الهوية بعنوان الاستدعاء

### خطوات الاختبار

#### الخطوة 1: إعادة تشغيل الخدمات

أعد تشغيل الواجهة الخلفية و خادم الويب لتطبيق التغييرات.

**إذا كان يعمل كخدمة Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**إذا كنت تشغّله يدويًا:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**إذا كنت تستخدم IIS أو Tomcat:**
أعد تشغيل خدمة خادم الويب الخاص بك.

#### الخطوة 2: افتح لوحة التحكم

افتح لوحة تحكم digna في متصفحك:

```
http://localhost:5173
```

(أو عنوان لوحة التحكم الذي قمت بتكوينه)

#### الخطوة 3: التحقق من أزرار الدخول

تحقق من ظهور أزرار الدخول لكل مزود تم تكوينه:

- يجب أن ترى زر "تسجيل الدخول باستخدام Microsoft"
- يجب أن ترى زر "تسجيل الدخول باستخدام Google"
- (إذا كان usePassword = true) يجب أن ترى حقول اسم المستخدم/كلمة المرور

إذا لم تظهر الأزرار:
- تحقق من حفظ `dashboard_config.toml`
- تحقق من إعادة تشغيل خدمة لوحة التحكم
- تحقق من وحدة تحكم المتصفح (F12) للأخطاء

#### الخطوة 4: اختبار تسجيل الدخول عبر SSO

انقر على أحد أزرار SSO (مثال: "تسجيل الدخول باستخدام Microsoft"):

1. يجب أن يتم توجيهك إلى صفحة تسجيل الدخول الخاصة بمزود الهوية
2. سجّل الدخول باستخدام بيانات اعتماد المؤسسة
3. يجب أن تعود إلى digna
4. يجب أن تكون مسجلاً في digna

#### الخطوة 5: التحقق من إنشاء المستخدم

بعد تسجيل الدخول الناجح عبر SSO:

- يجب إنشاء المستخدم تلقائيًا في digna
- يجب أن يتم تسجيل دخول المستخدم
- يجب أن يعرض ملف التعريف بيانات مزود الهوية الخاص بك
- يجب أن ترى لوحة تحكم digna

#### الخطوة 6: اختبار تسجيل الدخول باستخدام كلمة المرور (إذا كان مفعلًا)

إذا كان `usePassword = true`:

1. سجّل الخروج من digna
2. في صفحة تسجيل الدخول، أدخل اسم المستخدم وكلمة المرور
3. يجب أن تتمكن من تسجيل الدخول باستخدام بيانات كلمة المرور

---

## استكشاف الأخطاء وإصلاحها {: #troubleshooting }

### عدم ظهور أزرار الدخول

**الأعراض:**
- أزرار OIDC غير مرئية في صفحة الدخول
- ترى حقول كلمة المرور فقط (إذا كان usePassword = true)

**الأسباب والحلول:**
1. تحقق أن `dashboard_config.toml` موجود في دليل `dashboard/`
2. تحقق من وجود أقسام `[[login.oidc]]` وبالصياغة الصحيحة
3. أعد تشغيل خدمة لوحة التحكم
4. امسح ذاكرة تخزين المتصفح (Ctrl+Shift+Delete أو Cmd+Shift+Delete)
5. تحقق من وحدة تحكم المتصفح (F12 → تبويب Console) للأخطاء

---

### خطأ عدم تطابق Redirect URI

**الأعراض:**
- بعد النقر على زر SSO يظهر خطأ حول "redirect_uri mismatch"
- خطأ "The redirect URI is not registered"

**الأسباب والحلول:**
1. تحقق من صحة `DIGNA_OIDC_REDIRECT_URI` في `config.toml`
2. تحقق أن عنوان الاستدعاء مسجل في إعدادات مزود الهوية
3. تأكد من تطابق العنوانين تمامًا (بروتوكول، نطاق، المسار)
4. ابحث عن أخطاء مطبعية في عنوان الاستدعاء
5. إذا كنت تستخدم HTTPS تأكد من صحة الشهادة

---

### خطأ بيانات اعتماد العميل غير صالحة

**الأعراض:**
- خطأ "Invalid client ID or secret"
- فشل المصادقة بسبب خطأ في البيانات

**الأسباب والحلول:**
1. تحقق من صحة `DIGNA_OIDC_CLIENT_ID` و `DIGNA_OIDC_CLIENT_SECRET`
2. تأكد من عدم وجود مسافات زائدة أو أحرف غير مقصودة
3. تحقق أن البيانات لم تنتهِ صلاحيتها أو لم تُلغي
4. أعد تشغيل الواجهة الخلفية بعد تحديث التكوين
5. تحقق من وحدة تحكم مزود الهوية لتأكيد أن البيانات نشطة

---

### تعليق أو انتهاء مهلة تسجيل الدخول

**الأعراض:**
- النقر على زر SSO لا يفعل شيئًا
- انتهاء مهلة بعد عدة ثوانٍ
- المتصفح يعرض "Failed to connect" أو ما يشابهه

**الأسباب والحلول:**
1. تحقق أن الواجهة الخلفية لـ digna تعمل: `digna repo check`
2. تحقق من اتصال الشبكة إلى مزود الهوية
3. تحقق من إمكانية الوصول إلى `DIGNA_OIDC_CONFIGURATION_URL`
4. تحقق من قواعد الجدار الناري للسماح باتصالات HTTPS الصادرة
5. تحقق أن الواجهة الخلفية واللوحة الأمامية يمكنهما الوصول إلى بعضهما البعض

---

### لم يتم إنشاء المستخدم تلقائيًا

**الأعراض:**
- تسجيل الدخول عبر SSO ينجح لكن لم يُنشأ مستخدم في digna
- تحصل على خطأ أذونات بعد SSO

**الأسباب والحلول:**
1. تحقق من صحة تكوين OIDC
2. تحقق من إعدادات أذونات المستخدمين
3. راجع سجلات digna للرسائل الخطأ
4. أعد تشغيل الواجهة الخلفية
5. اتصل بـ support@digna.ai إذا استمرت المشكلة

---

## المزودون المدعومون {: #supported-providers }

### تم الاختبار والدعم

المزودون التاليون متوافقون وتم اختبارهم ويعملون:

| المزود | عنوان تكوين OIDC | دليل الإعداد |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### مزودو OIDC الآخرون

أي مزود يدعم OpenID Connect يمكن دمجه. المعلومات المطلوبة:

- Client ID
- Client secret
- عنوان تكوين OpenID (عادةً عند `/.well-known/openid-configuration`)
- الصلاحيات المدعومة (عادةً `openid profile email`)

اتصل بـ support@digna.ai إذا احتجت مساعدة في دمج مزود محدد.

---

## أفضل الممارسات

افعل:
- استخدم HTTPS في بيئة الإنتاج (لا تستخدم HTTP)
- خزّن أسرار العملاء بأمان (استخدم متغيرات البيئة إن أمكن)
- قم بتدوير الأسرار دوريًا
- اختبر في بيئة غير إنتاجية أولًا
- وثّق المزودين المكونين
- راقب سجلات تسجيل الدخول للنشاط غير المألوف
- حافظ على تزامن إعدادات مزود الهوية مع تكوين digna

لا تفعل:
- خزّن أسرار العملاء في نظام التحكم بالإصدارات
- استخدم عناوين إعادة التوجيه HTTP في الإنتاج
- قم بتكوين مزودين متعددين بنفس المفتاح
- اترك بيانات اعتماد افتراضية/تجريبية في الإنتاج
- اكشف ملفات التكوين التي تحتوي على أسرار
- اخلط بين بيانات اعتماد التطوير والإنتاج

---

## الدعم

تحتاج مساعدة في تكوين SSO؟

- **البريد الإلكتروني:** support@digna.ai
- **التوثيق:** https://docs.digna.ai
- **الموقع:** https://www.digna.ai

---

**آخر تحديث:** 30 أغسطس 2026  
**الإصدار:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**