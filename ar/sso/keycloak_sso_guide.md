# إعداد SSO مع Keycloak

Keycloak هو مزود هوية مستضاف ذاتيًا ومتوافق تمامًا مع OIDC. بما أنك تديره بنفسك، فإن عنوان الاكتشاف (discovery URL) يُبنى من اسم المضيف (host) وrealm الخاصين بك بدلاً من نطاق مزود خدمة.

هذا الدليل يغطي جانب **Keycloak**: إنشاء العميل وجمع القيم التي يحتاجها digna. جانب digna — `dashboard_config.toml` والاختبار واستكشاف الأخطاء — هو نفسه لكل مزود ويوضح في [نظرة عامة على تسجيل الدخول الأحادي](overview.md).

---

## قبل أن تبدأ

| المتطلب | ملاحظات |
|---|---|
| **إصدار Keycloak** | 17 أو أحدث للمسارات المستخدمة هنا — انظر الملاحظة في الخطوة 4 |
| **دور Keycloak** | `realm-admin` على الـ realm المستهدف، أو مسؤول خادم |
| **Realm** | الـ realm الذي ينتمي إليه مستخدمو digna، وليس بالضرورة `master` |
| **URI إعادة التوجيه لـ digna** | عنوان URL الذي يعود إليه المستخدمون بعد تسجيل الدخول، مثال: `https://digna.yourdomain.com/oidc/callback` |

---

## الخطوة 1: اختر الـ Realm

1. افتح وحدة تحكم إدارة Keycloak
2. استخدم محدد الـ realm في أعلى اليسار للتبديل إلى الـ realm الذي يتواجد فيه المستخدمون لديك

!!! warning "لا تستخدم الـ realm master"

    الـ `master` realm مخصص لإدارة Keycloak نفسه. يجب أن تتبع تطبيقات العملاء وجودها في realm مخصص؛ وضع digna في `master` يمنح مستخدميه طريقًا إلى وحدة إدارة Keycloak.

---

## الخطوة 2: إنشاء العميل

1. اذهب إلى **Clients** وانقر **Create client**
2. قم بالتكوين:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — هذا يصبح `DIGNA_OIDC_CLIENT_ID`
3. انقر **Next**
4. في خطوة **Capability config**، فعّل **Client authentication** **On**
5. اترك **Standard flow** ممكنًا؛ التدفقات الأخرى غير مطلوبة
6. انقر **Next**

!!! warning "يجب تفعيل مصادقة العميل"

    مع تعطيل **Client authentication**، ينشئ Keycloak عميلًا *public*، وهو ليس لديه بيانات اعتماد على الإطلاق — تبويب **Credentials** في الخطوة 4 لن يكون موجودًا. digna يحتاج إلى عميل سري (confidential client). يمكنك تغيير هذا الخيار بعد الإنشاء إذا أخطأت.

---

## الخطوة 3: ضبط URI إعادة التوجيه

في خطوة **Login settings** (أو في تبويب **Settings** لاحقًا):

1. **Valid redirect URIs**: أدخل عنوان callback الخاص بـ digna:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: اتركها فارغة، أو اضبطها على `+` لمزامنة عناوين إعادة التوجيه
3. انقر **Save**

!!! tip "تجنب الـ Wildcards"

    يقبل Keycloak أنماطًا مثل `https://digna.yourdomain.com/*`. تتيح الـ wildcard لأي مسار على ذلك المضيف استلام رمز التفويض، لذا الأفضل استخدام عنوان callback الدقيق.

---

## الخطوة 4: الحصول على سر العميل

1. افتح تبويب **Credentials**
2. أكد أن **Client Authenticator** هو *Client Id and Secret*
3. انسخ **Client secret** → يصبح `DIGNA_OIDC_CLIENT_SECRET`

السر يبقى قابلاً للاسترجاع هنا ويمكن إعادة توليده عبر **Regenerate**.

---

## الخطوة 5: بناء عنوان اكتشاف OpenID

استبدل مضيف Keycloak واسم الـ realm الخاصين بك:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

على سبيل المثال:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "في Keycloak 16 والإصدارات الأقدم يتم تضمين /auth"

    قبل Keycloak 17، كانت جميع النهايات (endpoints) تقع تحت بادئة `/auth`:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    التوزيعات التي تضبط `KC_HTTP_RELATIVE_PATH=/auth` تحتفظ بتخطيط العناوين القديم على الإصدارات الحالية أيضًا. إذا أعاد العنوان بدون `/auth` 404، جرّبه مع `/auth`.

افتح العنوان في متصفح قبل المتابعة. سيؤكد مستند JSON أن المضيف والـ realm صحيحان.

---

## الخطوة 6: تكوين digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Login with Keycloak"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

يجب أن تتطابق قيمة `key` في الملفين — هنا `keycloak`. لاحظ أنها لا يجب أن تتطابق بالضرورة مع Keycloak **Client ID**، رغم أن إبقائهما متطابقين أسهل للمتابعة.

---

## الخطوة 7: الاختبار

أعد تشغيل الـ backend وخادم الويب، ثم افتح لوحة التحكم. انظر [اختبار تسجيل الدخول](overview.md#testing-login) للقائمة الكاملة لفحص الأخطاء والتحقق.

---

## استكشاف أخطاء Keycloak وإصلاحها

### Invalid parameter: redirect_uri

عنوان callback غير مغطى في **Valid redirect URIs**. يسجل Keycloak الـ URI الذي استلمه في سجل الخادم، وهو أسرع طريقة لمعرفة عدم التطابق بالضبط.

### تبويب Credentials مفقود

العميل عام (public). فعّل **Client authentication** تحت **Settings → Capability config**.

### 404 على عنوان الاكتشاف

إما أن اسم الـ realm خاطئ، أو النشر يستخدم بادئة `/auth`. تحقق من قائمة الـ realms في وحدة الإدارة وجرب كلا شكلي العنوانين.

### unauthorized_client or invalid_client

تم تعطيل **Standard flow** تحت **Capability config**، أو تم إعادة توليد السر في Keycloak دون تحديث `config.toml`.

### أخطاء شهادات من الـ Backend

سيفشل استدعاء HTTPS الصادر من digna إلى عنوان الاكتشاف إذا كان Keycloak مستضافًا خلف شهادة خاصة أو موقعة ذاتيًا. قم بتثبيت الجهة المصدرة للشهادة (CA) في مخزن الثقة للجهاز الذي يعمل عليه backend الخاص بـ digna.

---

## انظر أيضًا

- [نظرة عامة على تسجيل الدخول الأحادي](overview.md) — مرجع التكوين، الاختبار واستكشاف الأخطاء العام
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)