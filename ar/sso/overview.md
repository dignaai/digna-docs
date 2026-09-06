# نظرة عامة على تسجيل الدخول الأحادي

---

## جدول المحتويات

1. [المقدمة ونظرة عامة](#introduction-and-overview)
2. [أدلة المزودين](#provider-guides)
3. [خطوات التهيئة](#configuration-steps)
4. [تهيئة لوحة القيادة](#dashboard-configuration)
5. [تهيئة الـ backend](#backend-configuration)
6. [اختبار تسجيل الدخول](#testing-login)
7. [استكشاف الأخطاء وإصلاحها](#troubleshooting)
8. [المزودون المدعومون](#supported-providers)

---

## المقدمة ونظرة عامة {: #introduction-and-overview }

هذا الدليل يقدّم تعليمات خطوة بخطوة لدمج تسجيل الدخول الأحادي (SSO) مع منصة digna باستخدام **OpenID Connect (OIDC)**.

### ما هو SSO؟

يسمح تسجيل الدخول الأحادي للمستخدمين بتسجيل الدخول إلى digna بأمان باستخدام بيانات اعتماد المؤسسة لديهم عبر مزودي الهوية الخارجيين. يمكن للمستخدمين المصادقة باستخدام بيانات اعتماد المؤسسة بدلاً من إدارة كلمات مرور منفصلة لـ digna.

### كيف يعمل

يتم تنفيذ SSO في digna باستخدام بروتوكول OIDC. يمكن تكوين عدة مزوّدي هوية بالتوازي عن طريق تعديل ملفي التهيئة الرئيسيين:

- **`dashboard_config.toml`** — يتحكم بواجهة تسجيل الدخول في الواجهة الأمامية
- **`config.toml`** — يهيئ اتصالات OIDC في الجانب الخلفي

### المزودون المدعومون {: #supported-providers-overview }

الأمثلة في هذا الدليل تستخدم **Microsoft** و**Google**، لكن **أي مزود متوافق مع OIDC** يمكن دمجه باتباع نفس البنية.

---

## أدلة المزودين {: #provider-guides }

كل مزود يحتاج نفس القيم الأربع — معرف العميل (client ID)، سر العميل (client secret)، URI إعادة التوجيه (redirect URI) ورابط الاكتشاف (discovery URL) — لكن كل مزود يضعها في مكان مختلف داخل وحدة التحكم الإدارية الخاصة به، وبعض المزودين لديهم خطوة خاصة بالمزود لا توجد في الآخرين. الأدلة أدناه تغطي تلك الحصة من العمل؛ هذه الصفحة تغطي جزء digna، وهو متطابق لكل المزودين.

| Provider | Guide | Worth knowing |
|---|---|---|
| **AD FS** | [Set up SSO with AD FS](adfs_sso_guide.md) | Self-hosted; the only provider here where you control the token service |
| **Auth0** | [Set up SSO with Auth0](auth0_sso_guide.md) | Discovery URL is per-tenant, and custom domains change it |
| **Google Workspace** | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) | Consent screen must be published before non-test users can log in |
| **Keycloak** | [Set up SSO with Keycloak](keycloak_sso_guide.md) | Self-hosted; discovery URL is per-realm |
| **Microsoft Entra ID** | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | Tenant ID appears in the discovery URL; secrets expire |
| **Okta** | [Set up SSO with Okta](okta_sso_guide.md) | Authorization server choice changes the discovery URL |
| **OneLogin** | [Set up SSO with OneLogin](onelogin_sso_guide.md) | The OIDC app type must be chosen at creation and cannot be changed |
| **PingOne** | [Set up SSO with PingOne](pingone_sso_guide.md) | Environment ID appears in the discovery URL |

أي مزود آخر متوافق مع OIDC يعمل بنفس الطريقة — انظر [Other OIDC Providers](#supported-providers).

---

## خطوات التهيئة {: #configuration-steps }

يتطلب تكوين SSO تحديث ملفين. تشرح هذه القسم كيفية تهيئة كل منهما.

### نظرة عامة على ملفات التهيئة

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend login interface |
| **config.toml** | `/config.toml` | Backend OIDC connections |

يجب تهيئة كلا الملفين ليعمل SSO بشكل صحيح.

---

## تهيئة لوحة القيادة {: #dashboard-configuration }

### موقع الملف

```
dashboard/dashboard_config.toml
```

### الخطوة 1: إضافة مزوّدي OIDC

أضف مدخلات تحت مصفوفة `[[login.oidc]]` لكل مزود هوية تريد دعمه.

**مثال مع Microsoft وGoogle:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### الخطوة 2: تكوين خيارات تسجيل الدخول

حدد ما إذا كان يجب السماح بتسجيل الدخول باستخدام كلمة المرور:

```toml
[login]
usePassword = true
```

### معلمات التهيئة

#### قسم `[[login.oidc]]`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | معرف فريد لاتصال OIDC (يجب أن يتطابق مع المفتاح في config.toml) |
| `label` | string | Yes | النص المعروض على زر تسجيل الدخول (مثال: "Login with Microsoft") |

#### قسم `[login]`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | السماح بتسجيل الدخول باستخدام كلمة المرور بالإضافة إلى SSO |

### فهم usePassword

**إذا كان `usePassword = true`:**
- تعرض شاشة الدخول أزرار SSO (مثل "Login with Microsoft")
- تعرض شاشة الدخول أيضًا حقول اسم المستخدم وكلمة المرور
- يمكن للمستخدمين المصادقة بأيٍ من الطريقتين
- يسمح بإعدادات هجينة حيث يستخدم بعض المستخدمين SSO وآخرون كلمات مرور

**إذا كان `usePassword = false` (أو تم تجاهله):**
- تعرض شاشة الدخول أزرار SSO فقط
- لا توجد حقول اسم مستخدم/كلمة مرور
- المصادقة متاحة فقط عبر OIDC

!!! tip "نصيحة"

    تسجيل الدخول باستخدام كلمة المرور متاح فقط للمستخدمين الذين تم إنشاؤهم بكلمات مرور باستخدام الأمر `digna user add` أو عبر لوحة القيادة.

### مثال كامل

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## تهيئة الـ backend {: #backend-configuration }

### موقع الملف

```
/config.toml
```

(دليل تثبيت digna الجذر)

### الخطوة 1: إضافة أقسام مزوّدي OIDC

يجب أن يكون لكل مزود قسم مخصص `[oidc.<key>]`. يجب أن يتطابق المفتاح مع `key` المعرفة في `dashboard_config.toml`.

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

### معلمات التهيئة

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | Client ID من مزود الهوية | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | Client secret من مزود الهوية | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | عنوان callback بعد المصادقة | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | نقطة نهاية تهيئة OIDC | `https://login.microsoftonline.com/...` |

!!! warning "مهم"

    استبدل القيم النائبة (`<client_id>`, `<client_secret>`, `<tenant_id>`) ببيانات الاعتماد الفعلية من بوابة المطورين لمزود الهوية لديك.

### URI إعادة التوجيه

يجب أن يكون URI إعادة التوجيه نفس الموجود في تكوين مزود الهوية:

```
http://localhost:5173/oidc/callback
```

إذا كان digna مستضافًا على نطاق مختلف، حدّثه بما يناسب:
- محليًا: `http://localhost:5173/oidc/callback`
- الإنتاج: `https://digna.yourdomain.com/oidc/callback`

### مثال كامل

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

بعد إكمال التهيئة، تحقق من أن SSO يعمل بشكل صحيح.

### قائمة التحقق قبل الاختبار

قبل الاختبار تأكد من:

- [ ] تم تحديث `dashboard_config.toml` بمزوّدي OIDC
- [ ] تم تحديث `config.toml` ببيانات اعتماد OIDC
- [ ] تم حفظ كلا الملفين
- [ ] بيانات الاعتماد صحيحة (client ID, client secret)
- [ ] URI إعادة التوجيه يطابق عنوان نشر التطبيق
- [ ] تم تكوين تطبيق مزود الهوية مع URI إعادة التوجيه

### خطوات الاختبار

#### الخطوة 1: إعادة تشغيل الخدمات

أعد تشغيل backend وweb server لتطبيق التغييرات.

**إذا كنت تشغله كخدمة على Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**إذا كنت تشغله كخدمة على Linux أو macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**إذا كنت تشغله يدويًا:**
```bash
digna serve --address localhost --port 8082
```

**أعد تشغيل خادم الويب أيضًا** — IIS أو Tomcat على Windows، nginx أو Apache على Linux وmacOS.

#### الخطوة 2: افتح لوحة القيادة

افتح لوحة digna في متصفحك:

```
http://localhost:5173
```

(أو عنوان لوحة القيادة الذي قمت بتكوينه)

#### الخطوة 3: التحقق من أزرار الدخول

تحقق من ظهور أزرار الدخول لكل مزود تم تكوينه:

- يجب أن ترى زر "Login with Microsoft"
- يجب أن ترى زر "Login with Google"
- (إذا كان usePassword = true) يجب أن ترى حقول اسم المستخدم/كلمة المرور

إذا لم تظهر الأزرار:
- تحقق من حفظ `dashboard_config.toml`
- تحقق من إعادة تشغيل خدمة لوحة القيادة
- تحقق من وحدة تحكم المتصفح لرؤية الأخطاء (F12)

#### الخطوة 4: اختبار تسجيل الدخول عبر SSO

انقر أحد أزرار SSO (مثال: "Login with Microsoft"):

1. يجب أن يعيد التوجيه إلى صفحة تسجيل مزود الهوية
2. سجّل الدخول باستخدام بيانات اعتماد مؤسستك
3. يجب أن يتم إعادة التوجيه إلى digna
4. يجب أن تكون قد سجّلت الدخول إلى digna

#### الخطوة 5: التحقق من إنشاء المستخدم

بعد نجاح تسجيل الدخول عبر SSO:

- يجب أن يتم إنشاء المستخدم تلقائيًا في digna
- يجب أن يتم تسجيل دخول المستخدم
- يجب أن يعرض ملف المستخدم بيانات مزود الهوية
- يجب أن ترى لوحة digna

#### الخطوة 6: اختبار تسجيل الدخول بكلمة مرور (إذا مفعل)

إذا كان `usePassword = true`:

1. سجّل الخروج من digna
2. في صفحة الدخول أدخل اسم مستخدم وكلمة مرور
3. يجب أن تتمكن من تسجيل الدخول باستخدام بيانات كلمة المرور

---

## استكشاف الأخطاء وإصلاحها {: #troubleshooting }

### أزرار الدخول لا تظهر

**الأعراض:**
- أزرار تسجيل الدخول عبر OIDC غير مرئية في صفحة الدخول
- ترى حقول كلمة المرور فقط (إذا كان usePassword = true)

**الأسباب والحلول:**
1. تحقق أن `dashboard_config.toml` موجود في مجلد `dashboard/`
2. تأكد من وجود أقسام `[[login.oidc]]` بصيغة صحيحة
3. أعد تشغيل خدمة لوحة القيادة
4. مسح ذاكرة التخزين المؤقت للمتصفح (Ctrl+Shift+Delete أو Cmd+Shift+Delete)
5. تحقق من وحدة تحكم المتصفح (F12 → تبويب Console) للأخطاء

---

### خطأ عدم تطابق Redirect URI

**الأعراض:**
- بعد النقر على زر SSO، يظهر خطأ حول "redirect_uri mismatch"
- خطأ "The redirect URI is not registered"

**الأسباب والحلول:**
1. تحقق من أن `DIGNA_OIDC_REDIRECT_URI` في `config.toml` صحيح
2. تحقق من تسجيل URI إعادة التوجيه في إعدادات مزود الهوية
3. تأكد من أن كلاهما يستخدمان نفس العنوان تمامًا (بما في ذلك البروتوكول والنطاق والمسار)
4. راجع الأخطاء الإملائية في URI
5. إذا كنت تستخدم HTTPS فتأكد من صلاحية الشهادة

---

### خطأ بيانات اعتماد العميل غير صالحة

**الأعراض:**
- خطأ "Invalid client ID or secret"
- تفشل المصادقة بخطأ بيانات الاعتماد

**الأسباب والحلول:**
1. تحقق من أن `DIGNA_OIDC_CLIENT_ID` و `DIGNA_OIDC_CLIENT_SECRET` صحيحان
2. تأكد من عدم وجود مسافات زائدة أو أحرف غير مقصودة
3. تحقق من أن البيانات لم تنته صلاحيتها أو لم تُلغَ
4. أعد تشغيل خدمة الـ backend بعد تحديث التهيئة
5. تحقق من وحدة تحكم مزود الهوية لتأكيد أن البيانات نشطة

---

### تعليق تسجيل الدخول أو انتهاء المهلة

**الأعراض:**
- النقر على زر SSO لا يفعل شيئًا
- انتهاء المهلة بعد عدة ثوانٍ
- المتصفح يعرض "Failed to connect" أو ما شابه

**الأسباب والحلول:**
1. تحقق من أن backend الخاص بـ digna يعمل: `digna repo check`
2. تحقق من الاتصال الشبكي إلى مزود الهوية
3. تحقق من إمكانية الوصول إلى `DIGNA_OIDC_CONFIGURATION_URL`
4. تأكد من أن قواعد الجدار الناري تسمح باتصالات HTTPS الصادرة
5. تحقق من إمكانية اتصال الـ backend والـ dashboard ببعضهما

---

### عدم إنشاء المستخدمين تلقائيًا

**الأعراض:**
- ينجح تسجيل الدخول عبر SSO لكن لا يتم إنشاء المستخدم في digna
- تحصل على خطأ أذونات بعد تسجيل الدخول عبر SSO

**الأسباب والحلول:**
1. تحقق من أن تهيئة OIDC صحيحة
2. تحقق من إعدادات أذونات المستخدمين
3. راجع سجلات digna للرسائل الخطأ
4. أعد تشغيل خدمة الـ backend
5. اتصل بـ support@digna.ai إذا استمر المشكلة

---

## المزودون المدعومون {: #supported-providers }

### تم الاختبار والدعم

مزودو OIDC التالية تم اختبارهم ومعروف أن يعملوا:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Set up SSO with AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Set up SSO with Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Set up SSO with Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Set up SSO with Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Set up SSO with OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Set up SSO with PingOne](pingone_sso_guide.md) |

### مزودون آخرون لـ OIDC

أي مزود يدعم OpenID Connect يمكن دمجه. المعلومات المطلوبة:

- Client ID
- Client secret
- رابط تهيئة OpenID (عادةً عند `/.well-known/openid-configuration`)
- الصلاحيات المطلوبة (عادةً `openid profile email`)

اتصل بـ support@digna.ai إذا كنت تحتاج مساعدة بدمج مزود محدد.

---

## أفضل الممارسات

**افعل:**
- استخدم HTTPS في بيئة الإنتاج (لا تستخدم HTTP)
- خزّن أسرار العميل بأمان (استخدم متغيرات البيئة إن أمكن)
- راجع الأسرار بشكل دوري ودوّرها
- اختبر في بيئة غير إنتاجية أولًا
- وثّق المزودين المكوّنين
- راقب سجلات الدخول لنشاط غير اعتيادي
- حافظ على تزامن إعدادات مزود الهوية مع إعدادات digna

**لا تفعل:**
- خزّن أسرار العميل في نظام التحكم بالمصدر (version control)
- استخدم عناوين إعادة توجيه HTTP في الإنتاج
- قم بتكوين مزودين متعددين بنفس المفتاح
- اترك بيانات اعتماد افتراضية/تجريبية في بيئة الإنتاج
- اكشف ملفات التهيئة التي تحتوي أسرارًا
- اخلط بين بيانات الاعتماد الخاصة بالتطوير والإنتاج

---

## الدعم

تحتاج مساعدة في تهيئة SSO؟

- **البريد الإلكتروني:** support@digna.ai
- **الوثائق:** https://docs.digna.ai
- **الموقع:** https://www.digna.ai

---

**آخر تحديث:** August 30, 2026  
**الإصدار:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**