# إعداد SSO مع OneLogin

OneLogin متوافق مع OIDC. ميزته المميزة هي أن نوع الموصل يُختار من الكتالوج عند إنشاء التطبيق ولا يمكن تغييره لاحقًا.

يغطي هذا الدليل جانب **OneLogin**: إنشاء التطبيق وجمع القيم التي يحتاجها digna. جانب digna — `dashboard_config.toml`، الاختبار واستكشاف الأخطاء وإصلاحها — هو نفسه لكل مزود ويتم وصفه في [نظرة عامة على تسجيل الدخول الموحد](overview.md).

---

## قبل أن تبدأ

| المتطلب | ملاحظات |
|---|---|
| **دور في OneLogin** | مالك الحساب أو مسؤول مخول بإضافة التطبيقات |
| **النطاق الفرعي** | على سبيل المثال `yourcompany.onelogin.com` |
| **URI إعادة توجيه digna** | عنوان URL الذي يعود إليه المستخدمون بعد تسجيل الدخول، على سبيل المثال `https://digna.yourdomain.com/oidc/callback` |

---

## الخطوة 1: إنشاء تطبيق OIDC

1. سجّل الدخول إلى بوابة OneLogin الإدارية
2. اذهب إلى **Applications → Applications**
3. انقر **Add App**
4. ابحث عن `OpenId Connect` واختر موصل **OpenId Connect (OIDC)**
5. عيّن **Display Name** إلى `digna`
6. انقر **Save**

!!! warning "نوع الموصل ثابت عند الإنشاء"

    لدى OneLogin إدخالات كتالوج منفصلة لـ SAML وOIDC، ولا يمكن تحويل التطبيق من أحدهما إلى الآخر. إذا اخترت موصل SAML عن طريق الخطأ، احذف التطبيق وأعد إضافته — لا توجد إعدادات لتبديل البروتوكولات.

---

## الخطوة 2: تكوين URI إعادة التوجيه

1. افتح علامة التبويب **Configuration**
2. في **Redirect URI's**، ادخل عنوان الاستدعاء (callback) الخاص بـ digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. اختياريًا، عيّن **Post Logout Redirect URIs** إلى عنوان لوحة التحكم (dashboard) الخاص بك
4. انقر **Save**

!!! note "URI واحد في كل سطر"

    على عكس مزودين يتوقعون قائمة مفصولة بفواصل، حقل OneLogin **Redirect URI's** يقبل URI واحدًا في كل سطر.

---

## الخطوة 3: تعيين نوع التطبيق وطريقة المصادقة

1. افتح علامة التبويب **SSO**
2. تأكد أن **Application Type** هو *Web*
3. عيّن **Token Endpoint → Authentication Method** إلى *POST* (`client_secret_post`) أو *Basic* (`client_secret_basic`)

!!! warning "لا تختَر None"

    تعيين طريقة المصادقة إلى *None* يجعل التطبيق عميلًا عامًا بدون سر، وسيُرفض تبادل الكود في خلفية digna. إما POST أو Basic سيعملان.

---

## الخطوة 4: جمع بيانات الاعتماد

ما زلت في علامة التبويب **SSO**:

- **Client ID** → يصبح `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → يصبح `DIGNA_OIDC_CLIENT_SECRET` (انقر **Show client secret**)

تُظهر الصفحة أيضًا **Issuer URL**، الذي يؤكد عنوان الاكتشاف في الخطوة التالية.

---

## الخطوة 5: تعيين المستخدمين

1. افتح علامة التبويب **Access**
2. أضف الأدوار أو المجموعات التي يُسمح لأعضائها باستخدام digna
3. انقر **Save**

!!! note "المستخدمون غير المعينين يُرفضون بعد تسجيل الدخول"

    كما هو الحال مع معظم المزودين، يقوم OneLogin بمصادقة المستخدم أولًا ثم التحقق من الاستحقاق ثانيًا. يتمكن المستخدم غير المعين من تسجيل الدخول بنجاح ثم يتم رفضه، مما يبدو كخطأ في digna بدلاً من قرار تحكم في الوصول.

---

## الخطوة 6: بناء عنوان اكتشاف الخدمة (Discovery URL)

استبدل النطاق الفرعي الخاص بك:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

على سبيل المثال:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "الـ /2 هي إصدار الـ API"

    تنفيذ OIDC الحالي لـ OneLogin يوجد تحت `/oidc/2/`. الوثائق الأقدم تظهر `/oidc/` بدون إصدار، والذي يشير إلى الإصدار الأول المتقاعد. تحقق من **Issuer URL** في علامة التبويب SSO إذا كان لديك شك — عنوان الاكتشاف هو العنوان المعطى في issuer مضافًا إليه `/.well-known/openid-configuration`.

---

## الخطوة 7: تكوين digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Login with OneLogin"
```

### `config.toml`

```toml
[oidc.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

يجب أن يتطابق `key` في كلا الملفين — هنا `onelogin`.

---

## الخطوة 8: الاختبار

أعد تشغيل الخادم الخلفي وخادم الويب، ثم افتح لوحة التحكم. راجع [اختبار تسجيل الدخول](overview.md#testing-login) للقائمة الكاملة للشيكات.

---

## استكشاف أخطاء OneLogin وإصلاحها

### redirect_uri did not match

عنوان الاستدعاء مفقود من **Configuration → Redirect URI's**، أو كانت المدخلات مفصولة بفواصل بدلًا من أسطر جديدة.

### invalid_client at the Token Step

تم تعيين **Token Endpoint → Authentication Method** إلى *None*، أو أن سر العميل في `config.toml` قديم. اكشف السر في علامة التبويب **SSO** وقارنه.

### التطبيق لا يظهر للمستخدمين

لم تُمنح أي دور أو مجموعة حق الوصول على علامة التبويب **Access**.

### 404 على عنوان الاكتشاف

النطاق الفرعي خاطئ، أو أن العنوان يحذف `/oidc/2/`. قارن مع **Issuer URL** المعروض على علامة التبويب SSO.

---

## انظر أيضًا

- [نظرة عامة على تسجيل الدخول الموحد](overview.md) — مرجع التكوين، الاختبار واستكشاف الأخطاء العامة
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)