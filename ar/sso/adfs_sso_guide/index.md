# إعداد تسجيل الدخول الموحد مع AD FS

Active Directory Federation Services هو الخيار المحلي: تقوم خوادمكم الخاصة بإصدار الرموز، وعنوان الاكتشاف (discovery URL) هو اسم مضيفكم. يدعم AD FS بروتوكول OpenID Connect اعتبارًا من **Windows Server 2016** فصاعدًا.

يغطي هذا الدليل **جانب AD FS**: إنشاء مجموعة التطبيق وجمع القيم التي يحتاجها digna. جانب digna — `dashboard_config.toml`، الاختبار واستكشاف الأخطاء وإصلاحها — متطابق لكل مزود ويُوصف في [نظرة عامة على تسجيل الدخول الموحد](overview.md).

---

## قبل أن تبدأ

| المتطلب | ملاحظات |
|---|---|
| **إصدار AD FS** | Windows Server 2016 أو أحدث — الإصدارات الأقدم لا تدعم OIDC |
| **الوصول** | مسؤول محلي على خادم AD FS |
| **اسم خدمة الاتحاد (federation service name)** | مثال: `adfs.yourdomain.com` |
| **URI إعادة التوجيه لـ digna** | عنوان URL الذي يعود إليه المستخدمون بعد تسجيل الدخول، مثال: `https://digna.yourdomain.com/oidc/callback` |

---

## الخطوة 1: إنشاء مجموعة التطبيق

1. على خادم AD FS، افتح **AD FS Management**
2. انقر بزر الماوس الأيمن على **Application Groups** واختر **Add Application Group**
3. أدخل `digna` كاسم
4. ضمن **Standalone applications** — أو **Client-Server applications** حسب إصدارك — اختر **Server application accessing a web API**
5. انقر **Next**

---

## الخطوة 2: تكوين تطبيق الخادم

1. **الاسم**: `digna backend`
2. **معرف العميل (Client Identifier)**: يقوم AD FS بإنشاء GUID. انسخه — هذا يصبح `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: أدخل عنوان callback الخاص بـ digna ثم انقر **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. انقر **Next**

!!! warning "اضغط Add، لا تكتفِ بالضغط على Next"

    حقل Redirect URI يحتوي على زر **Add** خاص به. كتابة URI والضغط على **Next** دون الضغط على **Add** سيلغي الإدخال، ولن يعرض المعالج أي تحذير. تأكد من ظهور URI في القائمة أسفل الحقل قبل المتابعة.

---

## الخطوة 3: إنشاء السر المشترك

1. ضع علامة على **Generate a shared secret**
2. انسخ السر المُولد → يصبح `DIGNA_OIDC_CLIENT_SECRET`
3. انقر **Next**

!!! warning "يُعرض السر مرة واحدة فقط"

    يعرض AD FS السر المشترك فقط في صفحة المعالج هذه ولا يمكنه عرضه مرة أخرى. إذا فقدته، أعد تعيينه لاحقًا من خصائص مجموعة التطبيق.

---

## الخطوة 4: تكوين Web API

1. **Identifier**: أدخل نفس معرف العميل من الخطوة 2 ثم انقر **Add**
2. انقر **Next**
3. اختر **سياسة التحكم بالوصول (Access Control Policy)** — *Permit everyone* هو أبسط خيار للتجربة؛ قيده لمجموعة للاستخدام في الإنتاج
4. انقر **Next**

---

## الخطوة 5: منح النطاقات المسموح بها

في خطوة **Configure Application Permissions**، ضع علامة على:

- `openid`
- `profile`
- `email`

ثم انقر **Next** وأكمل المعالج.

!!! warning "النطاق openid ليس محددًا افتراضيًا"

    يحدد AD FS في بعض الإصدارات فقط `user_impersonation` بشكل افتراضي. بدون `openid`، يعيد نقطة انتهاء التوكن (token endpoint) رمز وصول OAuth بدلاً من ID token، ولا يمكن لـ digna التعرف على المستخدم.

---

## الخطوة 6: التأكد من نقطة اكتشاف الاعدادات (Discovery Endpoint)

استبدل اسم خدمة الاتحاد الخاص بك:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

على سبيل المثال:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

افتحه في متصفح. ستؤكد وثيقة JSON أن OIDC مفعل واسم المضيف صحيح.

!!! note "يجب أن يثق الـ Backend في الشهادة"

    من الشائع استخدام سلطة شهادات داخلية لـ AD FS. الآلة التي تشغّل الـ digna backend تجري طلب HTTPS خارجي إلى هذا العنوان، لذا يجب أن تكون الجهة المصدرة للشهادة موجودة في مخزن الثقة لتلك الآلة — وليس فقط في متصفحات الأشخاص الذين يسجلون الدخول.

---

## الخطوة 7: تكوين digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Login with Active Directory"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

يجب أن يتطابق `key` في الملفين — هنا `adfs`.

---

## الخطوة 8: الاختبار

أعد تشغيل الـ backend وخادم الويب، ثم افتح لوحة التحكم. راجع [اختبار تسجيل الدخول](overview.md#testing-login) للقائمة الكاملة للفحص.

---

## استكشاف أخطاء AD FS وإصلاحها

### MSIS9611: العميل غير مسموح له بالوصول إلى المورد

معرف Web API في الخطوة 4 لا يطابق معرف العميل، أو لم تُمنح النطاقات في الخطوة 5. كلاهما قابل للتعديل من خصائص مجموعة التطبيق.

### MSIS9602: redirect_uri غير صالح

تم كتابة URI ولم يتم إضافته عبر زر **Add**، أو يختلف عن `DIGNA_OIDC_REDIRECT_URI`. تحقق من **Application Groups → digna → digna backend → Properties**.

### لم يتم إرجاع ID Token

نطاق `openid` مفقود من أذونات التطبيق.

### لا يمكن للـ Backend الوصول إلى عنوان الاكتشاف

إما أن DNS على مضيف الـ backend لا يحل اسم خدمة الاتحاد، أو أن شهادة AD FS غير موثوقة هناك. اختبر باستخدام `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` من خادم digna نفسه.

### الأحداث التي يجب التحقق منها

يسجل خادم AD FS حالات الفشل في **Applications and Services Logs → AD FS → Admin** في Event Viewer، عادةً مع سبب أكثر تحديدًا مما يظهر في المتصفح.

---

## انظر أيضًا

- [نظرة عامة على تسجيل الدخول الموحد](overview.md) — مرجع التكوين، الاختبار واستكشاف الأخطاء العامة
- [Microsoft: AD FS OpenID Connect scenarios](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)