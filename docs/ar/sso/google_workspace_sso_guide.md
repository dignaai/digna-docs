---
title: إعداد SSO لـ Google Workspace – تكامل تسجيل الدخول الموحد | توثيق digna
description: قم بتكوين تسجيل الدخول الموحد لـ digna باستخدام Google Workspace عبر OpenID Connect — شاشة موافقة OAuth، معرف عميل OAuth، عناوين إعادة التوجيه المصرح بها وتكوين digna المطابق.
image: /assets/logo_square.png
keywords: digna sso, google workspace sso, google oidc, oauth consent screen, openid connect, enterprise authentication
---

# إعداد تسجيل الدخول الموحد مع Google Workspace

منصة الهوية من Google متوافقة مع OIDC وتستخدم عنوان اكتشاف واحد معروف لكل عميل، لذا القيم الخاصة بكل مؤسسة هي فقط معرف العميل والسر.

يغطي هذا الدليل الجانب الخاص بـ **Google**: إنشاء عميل OAuth وجمع القيم التي يحتاجها digna. الجانب الخاص بـ digna — `dashboard_config.toml`، الاختبار واستكشاف الأخطاء — متماثل لكل مزود ويُوصف في [نظرة عامة على تسجيل الدخول الموحد](overview.md).

---

## قبل أن تبدأ

| المتطلب | ملاحظات |
|---|---|
| **مشروع Google Cloud** | أي مشروع في نفس المؤسسة كالنطاق Workspace الخاص بك |
| **الدور** | محرر أو مالك على المشروع |
| **digna redirect URI** | عنوان URL يعود إليه المستخدمون بعد تسجيل الدخول، مثال `https://digna.yourdomain.com/oidc/callback` |

---

## الخطوة 1: تكوين شاشة موافقة OAuth

لن تصدر Google بيانات اعتماد حتى توجد شاشة الموافقة.

1. افتح [وحدة تحكم Google Cloud](https://console.cloud.google.com) واختر المشروع الخاص بك
2. اذهب إلى **APIs & Services → OAuth consent screen**
3. اختر نوع المستخدم:
   - **Internal** — يمكن تسجيل الدخول فقط للحسابات الموجودة في نطاق Workspace الخاص بك. يُنصح به.
   - **External** — يمكن لأي حساب Google محاولة تسجيل الدخول.
4. املأ اسم التطبيق، بريد دعم المستخدم وبريد اتصال المطور
5. في خطوة **Scopes**، أضف `openid` و `.../auth/userinfo.email` و `.../auth/userinfo.profile`
6. احفظ

!!! warning "يجب نشر التطبيقات الخارجية"

    شاشة موافقة **External** تبدأ بحالة *Testing*، حيث يمكن فقط للحسابات المضافة صراحة إلى قائمة المستخدمين الاختباريين إكمال تسجيل الدخول. سيرى الآخرون رسالة "digna has not completed the Google verification process". إما غيّر التطبيق إلى **In production** تحت **Publishing status**، أو استخدم **Internal** — الذي لا يفرض هذا القيد وهو الخيار الصحيح لنشر يقتصر على Workspace.

---

## الخطوة 2: إنشاء عميل OAuth

1. اذهب إلى **APIs & Services → Credentials**
2. انقر **Create Credentials → OAuth client ID**
3. اضبط **Application type** على **Web application**
4. أعطه اسمًا، مثل `digna`
5. ضمن **Authorized redirect URIs**، انقر **Add URI** وأدخل:

```
https://digna.yourdomain.com/oidc/callback
```

6. انقر **Create**

!!! note "لا حاجة لـ Authorized JavaScript Origins"

    digna يتبادل رمز التفويض من الخادم الخلفي، وليس من المتصفح، لذلك يمكن ترك حقل **Authorized JavaScript origins** فارغًا. فقط URI إعادة التوجيه هو المهم.

---

## الخطوة 3: جمع بيانات الاعتماد

يظهر في الحوار الذي يظهر بعد الإنشاء:

- **Client ID** — ينتهي بـ `.apps.googleusercontent.com` → يصبح `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → يصبح `DIGNA_OIDC_CLIENT_SECRET`

يمكن استرجاع كلاهما لاحقًا من صفحة تفاصيل بيانات الاعتماد، على عكس معظم المزودين الآخرين.

---

## الخطوة 4: عنوان الاكتشاف

تستخدم Google عنوان اكتشاف واحدًا لجميع العملاء — لا يوجد ما يستبدل:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## الخطوة 5: تكوين digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "تسجيل الدخول عبر Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

يجب أن يتطابق الـ `key` في كلا الملفين — هنا `google`.

---

## الخطوة 6: الاختبار

أعد تشغيل الخادم الخلفي وخادم الويب، ثم افتح لوحة التحكم. راجع [اختبار تسجيل الدخول](overview.md#testing-login) للحصول على قائمة التحقق الكاملة.

---

## استكشاف أخطاء Google Workspace وإصلاحها

### خطأ 400: redirect_uri_mismatch

الـ URI في `DIGNA_OIDC_REDIRECT_URI` غير موجود في قائمة **Authorized redirect URIs**، أو يختلف بسبب شرطة مائلة نهائية أو البروتوكول. تعرض صفحة الخطأ من Google الـ URI الذي استلمته — قارنها حرفًا بحرف مع المسجل.

### This App Is Blocked / Has Not Completed Verification

شاشة الموافقة هي **External** وما زالت في حالة *Testing*. انشرها، أو غيّر التطبيق إلى **Internal**.

### Access Blocked: Authorization Error

الحساب الذي يحاول تسجيل الدخول خارج نطاق Workspace الخاص بك بينما شاشة الموافقة هي **Internal**. هذا السلوك المقصود — التطبيقات Internal تقبل فقط حسابات المؤسسة.

### التغييرات تستغرق عدة دقائق

تقوم Google بترحيل تغييرات بيانات الاعتماد وشاشة الموافقة بشكل غير متزامن. قد يستغرق تفعيل URI إعادة توجيه تم إضافته حديثًا بضع دقائق؛ إذا بدا أن التغيير لم يؤثر، انتظر وأعد المحاولة قبل متابعة التحقيق.

---

## راجع أيضًا

- [نظرة عامة على تسجيل الدخول الموحد](overview.md) — مرجع التكوين، الاختبار واستكشاف الأخطاء العام
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)