---
title: إعداد SSO مع PingOne – تكامل تسجيل الدخول الموحد | توثيق digna
description: إعداد تسجيل الدخول الموحد لـ digna مع PingOne باستخدام OpenID Connect — إعداد تطبيق OIDC على الويب، عناوين إعادة التوجيه، بيانات اعتماد العميل، معرف البيئة، المجالات الإقليمية وتطابق إعداد digna.
image: /assets/logo_square.png
keywords: digna sso, pingone sso, ping identity, pingone oidc, معرف البيئة, openid connect, مصادقة مؤسسية
---

# إعداد تسجيل الدخول الموحد (SSO) مع PingOne

PingOne متوافق مع OIDC. هناك قيمتان تحتاجان لعناية خاصة: **Environment ID** (معرف البيئة)، الذي يظهر في كل عنوان نهائي، و**regional domain** (المجال الإقليمي)، الذي يختلف بين مستأجري أمريكا الشمالية وأوروبا وكندا وآسيا والمحيط الهادئ وأستراليا.

يغطي هذا الدليل جانب **PingOne**: إنشاء التطبيق وجمع القيم التي تحتاجها digna. جانب digna — `dashboard_config.toml`، الاختبار واستكشاف الأخطاء وإصلاحها — هو نفسه لكل مزود ويُوصَف في [نظرة عامة على تسجيل الدخول الموحد](overview.md).

---

## قبل أن تبدأ

| المتطلب | ملاحظات |
|---|---|
| **PingOne role** | Environment Admin أو Identity Data Admin على البيئة المستهدفة |
| **Environment** | بيئة PingOne التي ينتمي إليها مستخدمو digna |
| **digna redirect URI** | عنوان URL الذي يعود إليه المستخدمون بعد تسجيل الدخول، مثال: `https://digna.yourdomain.com/oidc/callback` |

---

## الخطوة 1: إنشاء التطبيق

1. سجّل الدخول إلى وحدة تحكم المشرف في PingOne واختر بيئتك
2. اذهب إلى **Applications → Applications**
3. انقر زر **+**
4. أدخل `digna` كـ **Application Name**
5. اختر **OIDC Web App**
6. انقر **Save**

!!! warning "اختر OIDC Web App، وليس Single-Page App"

    *Single-Page App* و *Native App* تنشئان عملاء عامين لا يمكنهم الاحتفاظ بسر. digna تتبادل رمز التفويض من الخلفية وتحتاج إلى النوع السري **OIDC Web App**.

---

## الخطوة 2: تكوين Redirect URI

1. افتح تبويب **Configuration** الخاص بالتطبيق
2. انقر أيقونة القلم للتعديل
3. تأكد أن **Response Type** هي *Code* و **Grant Type** هي *Authorization Code*
4. تحت **Redirect URIs**، أدخل عنوان callback الخاص بـ digna:

```
https://digna.yourdomain.com/oidc/callback
```

5. اضبط **Token Endpoint Authentication Method** على *Client Secret Post* أو *Client Secret Basic*
6. انقر **Save**

---

## الخطوة 3: تفعيل التطبيق

في صف التطبيق أو لوحة التفاصيل، قم بتبديل المفتاح إلى **enabled**.

!!! warning "التطبيقات الجديدة تبدأ معطلة"

    يقوم PingOne بإنشاء التطبيقات في حالة معطلة. التطبيق المعطل يسبب خطأ في خطوة التفويض لا يذكر المفتاح، لذا من المفيد التأكد من هذا قبل محاولة استكشاف أي شيء آخر.

---

## الخطوة 4: منح الصلاحيات (Scopes)

1. افتح تبويب **Resources**
2. تأكد من منح `openid`، وأضف `profile` و `email` من مورد **OpenID Connect**
3. انقر **Save**

---

## الخطوة 5: إسناد المستخدمين

1. افتح تبويب **Access**
2. أضف السكان أو المجموعات الذين يُسمح لأعضائهم باستخدام digna
3. انقر **Save**

---

## الخطوة 6: جمع بيانات الاعتماد ومعرف البيئة

في تبويب **Configuration**، قم بتوسيع **General**:

- **Client ID** → يصبح `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → يصبح `DIGNA_OIDC_CLIENT_SECRET` (انقر أيقونة العين)
- **Environment ID** → يوضع في عنوان الاكتشاف (discovery URL)

يسرد نفس التبويب أيضًا **OIDC Discovery Endpoint** الجاهز، والذي يمكنك نسخه مباشرة بدل تجميعه يدويًا.

---

## الخطوة 7: بناء عنوان الاكتشاف (Discovery URL)

استبدل معرف البيئة والمجال الخاص بمنطقتك:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| المنطقة | المجال |
|---|---|
| أمريكا الشمالية | `auth.pingone.com` |
| أوروبا | `auth.pingone.eu` |
| كندا | `auth.pingone.ca` |
| آسيا والمحيط الهادئ | `auth.pingone.asia` |
| أستراليا | `auth.pingone.com.au` |

لمؤسسة أوروبية:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "انسخها بدلًا من كتابتها"

    المجال الإقليمي هو أكثر الأخطاء شيوعًا في تكامل PingOne، والمجال الخاطئ يعطي خطأ 404 بدل رسالة مفيدة. استخدم قيمة **OIDC Discovery Endpoint** من الخطوة 6.

---

## الخطوة 8: تكوين digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Login with PingOne"
```

### `config.toml`

```toml
[oidc.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

يجب أن يتطابق الـ `key` في كلا الملفين — هنا هو `pingone`.

---

## الخطوة 9: الاختبار

أعد تشغيل خادم الخلفية وخادم الويب، ثم افتح لوحة التحكم. راجع [اختبار تسجيل الدخول](overview.md#testing-login) للحصول على قائمة التحقق الكاملة.

---

## استكشاف مشكلات PingOne وإصلاحها

### 404 على عنوان الاكتشاف

المجال الإقليمي أو معرف البيئة خاطئان. قارن مع **OIDC Discovery Endpoint** المعروض في تبويب Configuration الخاص بالتطبيق.

### NOT_FOUND أو التطبيق معطل

مفتاح تفعيل التطبيق من الخطوة 3 لا يزال في وضع الإيقاف.

### تطابق Redirect URI

يقوم PingOne بمطابقة السلسلة كاملة. تحقق من **Configuration → Redirect URIs** لوجود شَرطة مائلة نهائية أو فرق في المخطط (scheme).

### تسجيل الدخول نجح لكن لا يصل claim البريد الإلكتروني إلى digna

لم تُمنح scopes `email` و `profile` في تبويب **Resources**.

### المستخدم لا يرى التطبيق

لم تُمنح أي مجموعة أو سكان حق الوصول في تبويب **Access**.

---

## انظر أيضًا

- [نظرة عامة على تسجيل الدخول الموحد](overview.md) — مرجع التكوين، الاختبار والاستكشاف العام للمشكلات
- [PingOne: تكوين تطبيق OIDC](https://docs.pingidentity.com/pingone/)