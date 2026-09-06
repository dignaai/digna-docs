# إعداد SSO مع Microsoft Entra ID

Microsoft Entra ID (المعروف سابقًا باسم Azure Active Directory) هو مزوّد متوافق تمامًا مع OIDC، لذلك يتكامل digna معه عبر نقطة الاكتشاف القياسية.

يغطي هذا الدليل **جانب Entra ID**: تسجيل التطبيق وجمع القيم الأربع التي يحتاجها digna. جانب digna — `dashboard_config.toml`، الاختبار واستكشاف الأخطاء وإصلاحها — هو نفسه لكل مزوّد ومُوضّح في [نظرة عامة على تسجيل الدخول الأحادي](overview.md).

---

## قبل أن تبدأ

| المتطلب | الملاحظات |
|---|---|
| **دور Entra ID** | Application Administrator، Cloud Application Administrator، أو Global Administrator |
| **digna redirect URI** | عنوان URL الذي يعود إليه المستخدمون بعد تسجيل الدخول، مثال: `https://digna.yourdomain.com/oidc/callback` |
| **المستأجر** | الدليل الذي يقوم المستخدمون بتسجيل الدخول إليه |

---

## الخطوة 1: تسجيل التطبيق

1. سجّل الدخول إلى [مركز إدارة Microsoft Entra](https://entra.microsoft.com)
2. اذهب إلى **Identity → Applications → App registrations**
3. انقر **New registration**
4. التكوين:
   - **الاسم**: `digna` (يُعرض للمستخدمين في شاشة الموافقة)
   - **أنواع الحسابات المدعومة**: *Accounts in this organizational directory only* لنشر خاص بمستأجر واحد
5. تحت **Redirect URI**، اختر المنصة **Web** وأدخل عنوان callback الخاص بـ digna:

```
https://digna.yourdomain.com/oidc/callback
```

6. انقر **Register**

!!! warning "مهم"

    يجب أن تكون المنصة **Web**، لا *Single-page application*. يقوم digna بمبادلة رمز التفويض من الخادم الخلفي باستخدام سر العميل، وهو ما لا تسمح به نوع منصة SPA.

---

## الخطوة 2: جمع معرف العميل والمستأجر

في صفحة **Overview** الخاصة بالتطبيق، انسخ:

- **Application (client) ID** → يصبح `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → يُستخدم في عنوان URL الخاص بالاكتشاف

---

## الخطوة 3: إنشاء سر عميل

1. اذهب إلى **Certificates & secrets → Client secrets**
2. انقر **New client secret**
3. أدخل وصفًا واختر فترة انتهاء صلاحية
4. انقر **Add**
5. انسخ عمود **Value** فورًا

!!! warning "انسخ Value، لا Secret ID"

    يُعرض الـ **Value** مرة واحدة فقط، في هذه الصفحة، ولا يمكن استرجاعه لاحقًا. يبدو **Secret ID** المجاور مشابهًا لكنه ليس السر — استخدامه ينتج عنه خطأ `invalid_client` عند تسجيل الدخول. إذا تركت الصفحة قبل النسخ، احذف السر وأنشئ واحدًا جديدًا.

!!! tip "نصيحة"

    يقيّد Entra ID عمر الأسرار إلى 24 شهرًا كحد أقصى، لذا لكل تكامل SSO يوجد تاريخ انتهاء. دوّنه في مكان تراه — انتهاء السر يوقف SSO لجميع المستخدمين دفعة واحدة، دون تحذير على صفحة تسجيل الدخول.

---

## الخطوة 4: تأكيد أذونات API

1. اذهب إلى **API permissions**
2. تأكد من وجود **Microsoft Graph → User.Read** (delegated) — تُضاف بشكل افتراضي

نطاقات `openid` و`profile` و`email` التي يطلبها digna هي جزء من مجموعة OIDC القياسية ولا تحتاج لمنح منفصل. إذا كان المستأجر يطلب موافقة المسؤول لجميع التطبيقات، انقر **Grant admin consent for &lt;tenant&gt;**.

---

## الخطوة 5: بناء عنوان URL للاكتشاف

استبدل **Directory (tenant) ID** من الخطوة 2:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "استخدم نقطة النهاية v2.0"

    جزء `/v2.0/` مهم. نقطة النهاية v1.0 عند `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` تصدر رموزًا بصيغة أقدم ولا تُرجع مطالبات OIDC القياسية التي يتوقعها digna.

افتح عنوان URL في متصفح قبل المتابعة. تؤكد وثيقة JSON أن معرف المستأجر صحيح.

---

## الخطوة 6: تكوين digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"
```

### `config.toml`

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

يجب أن يتطابق `key` في الملفين — هنا `microsoft`.

---

## الخطوة 7: الاختبار

أعد تشغيل الخادم الخلفي وخادم الويب، ثم افتح لوحة التحكم. راجع [اختبار تسجيل الدخول](overview.md#testing-login) للقائمة الكاملة للاختبار.

---

## استكشاف أخطاء Entra ID وإصلاحها

### AADSTS50011: Redirect URI Mismatch

العنوان في `DIGNA_OIDC_REDIRECT_URI` يختلف عن المسجل في الخطوة 1. تقارن Entra ID السلسلة كاملة، لذا المسافة المائلة النهائية، `http` مقابل `https`، أو منفذ مختلف كلها تعد اختلافًا. تحقق من **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Invalid Client Secret

إما أنه تم نسخ **Secret ID** بدلًا من **Value**، أو أن السر منتهي الصلاحية. أنشئ سرًا جديدًا ونسخ عمود Value.

### AADSTS650057: Invalid Resource

تم حذف تسجيل التطبيق أو ينتمي إلى مستأجر مختلف عن الموجود في عنوان URL الخاص بالاكتشاف. تحقق من Directory (tenant) ID في صفحة Overview.

### المستخدمون يسجلون الدخول لكن لا يحدث شيء

إذا كان المستأجر يتطلب موافقة المسؤول ولم يتم منحها، فسيعود التحويل دون رمز صالح. امنح موافقة المسؤول تحت **API permissions**.

---

## انظر أيضًا

- [نظرة عامة على تسجيل الدخول الأحادي](overview.md) — مرجع التهيئة، الاختبار واستكشاف الأخطاء العام
- [Microsoft: تدفق رمز تفويض OAuth 2.0](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)