# إعداد SSO مع Okta

تلتزم Okta بمواصفات OIDC، مع فارق واحد يواجه معظم التكاملات لأول مرة: تعرض مؤسسة Okta أكثر من خادم تفويض واحد، ولكلٍ منها عنوان اكتشاف خاص به.

يغطي هذا الدليل جانب **Okta**: إنشاء تكامل التطبيق وجمع القيم التي تحتاجها digna. جانب digna — `dashboard_config.toml`، الاختبار واستكشاف الأخطاء — هو نفسه لكل مزود وهو موضح في [نظرة عامة على تسجيل الدخول الموحد](overview.md).

---

## قبل أن تبدأ

| Requirement | Notes |
|---|---|
| **Okta role** | Super Administrator, or an admin role permitted to create app integrations |
| **Okta domain** | e.g. `yourcompany.okta.com`, or a custom domain if configured |
| **digna redirect URI** | The URL users return to after login, e.g. `https://digna.yourdomain.com/oidc/callback` |

---

## الخطوة 1: إنشاء تكامل التطبيق

1. سجّل الدخول إلى لوحة إدارة Okta
2. اذهب إلى **Applications → Applications**
3. انقر **Create App Integration**
4. اختر:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. انقر **Next**

!!! warning "نوع التطبيق لا يمكن تغييره"

    اختيار *Single-Page Application* بدلًا من *Web Application* ينشئ عميلًا عامًا بدون secret، وتبادل رمز الخلفية في digna سيفشل مع `invalid_client`. النوع ثابت عند الإنشاء — الاختيار الخاطئ يعني حذف التطبيق والبدء من جديد.

---

## الخطوة 2: تكوين التكامل

1. **App integration name**: `digna`
2. **Grant type**: اترك *Authorization Code* محددًا
3. **Sign-in redirect URIs**: أدخل عنوان استدعاء digna الخاص بك:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: اختياري
5. تحت **Assignments**، اختر من يمكنه استخدام التكامل — مجموعة محددة أكثر أمانًا من *Allow everyone in your organization to access*
6. انقر **Save**

!!! note "التعيين مطلوب"

    تقوم Okta بمصادقة المستخدم ثم تتحقق مما إذا كان مُعينًا للتطبيق. سيصل المستخدم غير المعين إلى صفحة تسجيل دخول Okta، ويسجل الدخول بنجاح، ثم يُرفض عند إعادة التوجيه. إذا نجح تسجيل الدخول لديك لكنه لا يعمل لزملائك، ففحص التعيين هو أول ما يجب التحقق منه.

---

## الخطوة 3: جمع بيانات الاعتماد

في علامة التبويب **General** للتطبيق، تحت **Client Credentials**:

- **Client ID** → يصبح `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → يصبح `DIGNA_OIDC_CLIENT_SECRET` (انقر على أيقونة العين للكشف)

---

## الخطوة 4: اختيار خادم التفويض

هذه الخطوة هي التي تحدد عنوان الاكتشاف (discovery URL). اذهب إلى **Security → API** لرؤية خوادم التفويض في مؤسستك.

**Org authorization server** — يصدر رموزًا لمؤسسة Okta نفسها:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — بما في ذلك الخادم الذي تنشئه Okta باسم `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

بالنسبة للخادم المدمج، يكون `<auth_server_id>` حرفيًا `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "أي واحد؟"

    استخدم خادم التفويض الخاص **بالمنظمة (org)** ما لم تكن منظمتك تقرر بالفعل استخدام خادم مخصص لسياسات وصول API. حسابات Okta Developer تُفعل `default` افتراضيًا؛ العديد من المؤسسات تعطّلها. افتح كلا العنوانين في المتصفح — الذي يعيد JSON بدلًا من خطأ هو المتاح لك.

---

## الخطوة 5: تكوين digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

### `config.toml`

```toml
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

يجب أن يطابق `key` في كلا الملفين — هنا `okta`.

---

## الخطوة 6: الاختبار

أعد تشغيل الbackend وweb server، ثم افتح لوحة التحكم. راجع [اختبار تسجيل الدخول](overview.md#testing-login) للقائمة الكاملة للفحص.

---

## استكشاف أخطاء Okta وإصلاحها

### لم يُسجّل عنوان إعادة التوجيه

تذكر Okta عنوان URI المسبّب للخطأ في رسالة الخطأ. قارنها مع **General → Sign-in redirect URIs**؛ تطابق Okta السلسلة الكاملة بما في ذلك أي شرطة مائلة في النهاية.

### المستخدم غير معين لتطبيق العميل

الحساب غير موجود في قائمة التعيين الخاصة بالتطبيق. أضف المستخدم أو مجموعته تحت **Assignments**.

### 400 Bad Request: Invalid Authorization Server

`<auth_server_id>` في عنوان الاكتشاف غير موجود، غالبًا `default` في مؤسسة تم إزالة هذا الخادم منها. تحقق من **Security → API** للخوادم المتاحة بالفعل.

### invalid_client في خطوة التوكن

تم إنشاء التكامل كـ Single-Page Application وله no client secret. أعد إنشاؤه كتطبيق Web Application.

---

## انظر أيضًا

- [نظرة عامة على تسجيل الدخول الموحد](overview.md) — مرجع التكوين، الاختبار واستكشاف الأخطاء العام
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)