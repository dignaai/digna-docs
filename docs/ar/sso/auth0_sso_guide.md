---
title: Auth0 SSO – تكامل تسجيل الدخول الموحد | توثيق digna
description: إعداد تسجيل الدخول الموحد (Single Sign-On) لـ digna باستخدام OpenID Connect — إعداد تطبيق ويب عادي، عناوين callback المسموح بها، بيانات اعتماد العميل، نطاق المستأجر وتكوين digna المطابق.
image: /assets/logo_square.png
keywords: digna sso, auth0 sso, auth0 oidc, تطبيق ويب عادي, callback urls, openid connect, مصادقة المؤسسات
---

# إعداد SSO مع Auth0

Auth0 متوافق مع OIDC ويعرض نقطة اكتشاف (discovery) لكل مستأجر. الأمر الأساسي الذي يجب ضبطه بشكل صحيح هو نطاق المستأجر، الذي يظهر في عنوان الاكتشاف ويتغير إذا قمت بتمكين نطاق مخصص.

يغطي هذا الدليل جانب **Auth0**: إنشاء التطبيق وجمع القيم التي تحتاجها digna. جانب digna — `dashboard_config.toml`، الاختبار واستكشاف الأخطاء وإصلاحها — هو نفسه بالنسبة لكل مزود ومذكور في [Single Sign-On Overview](overview.md).

---

## قبل أن تبدأ

| Requirement | Notes |
|---|---|
| **Auth0 role** | Admin on the tenant |
| **Tenant domain** | e.g. `yourcompany.eu.auth0.com` — the region segment matters |
| **digna redirect URI** | The URL users return to after login, e.g. `https://digna.yourdomain.com/oidc/callback` |

---

## الخطوة 1: إنشاء التطبيق

1. سجّل الدخول إلى [Auth0 Dashboard](https://manage.auth0.com)
2. انتقل إلى **Applications → Applications**
3. انقر **Create Application**
4. سمّه `digna` واختر **Regular Web Applications**
5. انقر **Create**

!!! warning "اختر Regular Web Applications"

    *Single Page Application* و *Native* ينشئان عملاء عامين بدون سر. تقوم digna بإجراء مقايضة الترميز (code exchange) من الخلفية وتحتاج إلى عميل سري (confidential client)، لذا فإن **Regular Web Applications** هو النوع الصحيح. على عكس بعض المزودين، يتيح Auth0 تغيير النوع لاحقًا ضمن **Settings → Application Type**.

---

## الخطوة 2: إضافة عنوان الاستدعاء (Callback URL)

في تبويب **Settings** الخاص بالتطبيق:

1. اعثر على **Allowed Callback URLs**
2. أدخل عنوان callback الخاص بـ digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. اختياريًا عيّن **Allowed Logout URLs** إلى عنوان لوحة التحكم الخاصة بك
4. انتقل إلى الأسفل وانقر **Save Changes**

!!! note "مفصولة بفواصل، ليست مفصولة بأسطر جديدة"

    يقبل Auth0 عدة عناوين callback في هذا الحقل، مفصولة بفواصل. القائمة المفصولة بأسطر جديدة فقط تُقرأ كعنوان واحد معطّل وتطابق لا شيء بصمت.

---

## الخطوة 3: جمع بيانات الاعتماد

ما زلت في **Settings**، في لوحة **Basic Information**:

- **Domain** → توضع في عنوان الاكتشاف (discovery URL)
- **Client ID** → يصبح `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → يصبح `DIGNA_OIDC_CLIENT_SECRET` (انقر للكشف)

---

## الخطوة 4: تأكيد نوع التفويض (Grant Type)

1. انتقل إلى **Settings → Advanced Settings → Grant Types**
2. تأكد من وضع علامة على **Authorization Code**

يتم تمكينه افتراضيًا لتطبيقات Regular Web Applications. إذا أُزيل، يفشل تسجيل دخول digna مع `unauthorized_client`.

---

## الخطوة 5: بناء عنوان الاكتشاف (Discovery URL)

استبدل **Domain** من الخطوة 3:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

على سبيل المثال:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "النطاقات المخصصة تغير issuer"

    إذا كان مستأجرك يستخدم نطاقًا مخصصًا مثل `login.yourcompany.com`، فاستخدم ذلك النطاق في عنوان الاكتشاف. المزج بين الاثنين — النطاق الرسمي في عنوان الاكتشاف، والنطاق المخصص في المتصفح — يؤدي إلى عدم تطابق issuer، ويتم رفض التوكن بعد تسجيل دخول ناجح خلاف ذلك.

---

## الخطوة 6: تكوين digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Login with Auth0"
```

### `config.toml`

```toml
[oidc.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

يجب أن يتطابق الـ `key` في الملفين — هنا `auth0`.

---

## الخطوة 7: الاختبار

أعد تشغيل الخادم الخلفي وخادم الويب، ثم افتح لوحة التحكم. راجع [Testing Login](overview.md#testing-login) للقائمة الكاملة لفحص الأمور.

---

## استكشاف أخطاء Auth0 وإصلاحها

### عدم تطابق Callback URL

تظهر صفحة خطأ Auth0 العنوان الذي استلمه. أضفه إلى **Allowed Callback URLs**، وتحقق من أن الإدخالات مفصولة بفواصل.

### unauthorized_client

لم يتم تفعيل **Authorization Code** ضمن **Advanced Settings → Grant Types**، أو أن نوع التطبيق ليس Regular Web Applications.

### رفض الوصول بعد تسجيل دخول ناجح

قاعدة (Rule) أو Action أو مشغل ما بعد الدخول (Post-Login trigger) في المستأجر يرفض المستخدم. تحقق من **Actions → Flows → Login** وسجلات المستأجر تحت **Monitoring → Logs**، والتي تُظهر السبب الدقيق.

### عدم تطابق issuer

عنوان الاكتشاف والنطاق الذي أُرسل إليه المتصفح يختلفان — عادةً النطاق الرسمي للمستأجر مقابل نطاق مخصص. استخدم واحدًا بشكل متسق.

---

## راجع أيضًا

- [Single Sign-On Overview](overview.md) — مرجع التكوين، والاختبار واستكشاف الأخطاء العام
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)