# Okta के साथ SSO सेटअप करें

Okta OIDC-समर्थित है, लेकिन एक बात है जो पहली बार इंटीग्रेशन करने वाले लोगों को फँसा देती है: एक Okta ऑर्ग कई authorization server एक्सपोज़ करता है, और हर एक का अपना discovery URL होता है।

यह गाइड **Okta पक्ष** को कवर करती है: ऐप इंटीग्रेशन बनाना और वे मान इकट्ठा करना जो digna को चाहिए। digna पक्ष — `dashboard_config.toml`, परीक्षण और समस्या निवारण — हर प्रोवाइडर के लिए वही होता है और [सिंगल साइन-ऑन अवलोकन](overview.md) में बताया गया है।

---

## आरंभ करने से पहले

| आवश्यकता | नोट्स |
|---|---|
| **Okta भूमिका** | Super Administrator, या वह एडमिन रोल जिसे ऐप इंटीग्रेशन बनाने की अनुमति हो |
| **Okta डोमेन** | उदाहरण: `yourcompany.okta.com`, या यदि कॉन्फ़िगर किया गया हो तो कस्टम डोमेन |
| **digna रीडायरेक्ट URI** | वह URL जहाँ उपयोगकर्ता लॉगिन के बाद लौटते हैं, उदाहरण: `https://digna.yourdomain.com/oidc/callback` |

---

## चरण 1: ऐप इंटीग्रेशन बनाएं

1. Okta Admin Console में साइन इन करें
2. **Applications → Applications** पर जाएँ
3. **Create App Integration** पर क्लिक करें
4. चुनें:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. **Next** पर क्लिक करें

!!! warning "ऐप्लिकेशन प्रकार बदला नहीं जा सकता"

    *Single-Page Application* चुनने पर यह एक पब्लिक क्लाइंट बन जाता है जिसके पास कोई सीक्रेट नहीं होता, और digna का बैकएंड कोड एक्सचेंज `invalid_client` के साथ फेल हो जाएगा। प्रकार बनाने के समय तय होता है — गलत चयन का मतलब है कि ऐप को हटाकर फिर से शुरू करना होगा।

---

## चरण 2: इंटीग्रेशन कॉन्फ़िगर करें

1. **App integration name**: `digna`
2. **Grant type**: *Authorization Code* चुना छोड़ें
3. **Sign-in redirect URIs**: अपना digna कॉलबैक URL दर्ज करें:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: वैकल्पिक
5. **Assignments** के अंतर्गत चुनें कि कौन इंटीग्रेशन का उपयोग कर सकता है — किसी विशेष समूह को अनुमति देना *Allow everyone in your organization to access* की तुलना में सुरक्षित है
6. **Save** पर क्लिक करें

!!! note "असाइनमेंट आवश्यक है"

    Okta उपयोगकर्ता को प्रमाणीकृत करता है और फिर जांचता है कि क्या वे उस एप्लिकेशन को असाइन किये गए हैं। असाइन न किए गए उपयोगकर्ता Okta लॉगिन पेज तक पहुँचते हैं, सफलतापूर्वक साइन इन करते हैं, और रीडायरेक्ट के समय अस्वीकृत कर दिए जाते हैं। यदि आपके लिए लॉगिन काम करता है लेकिन सहकर्मियों के लिए नहीं, तो असाइनमेंट सबसे पहला स्थान है जिसे चेक करना चाहिए।

---

## चरण 3: क्रेडेंशियल इकट्ठा करें

एप्लिकेशन के **General** टैब पर, **Client Credentials** के अंतर्गत:

- **Client ID** → बन जाता है `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → बन जाता है `DIGNA_OIDC_CLIENT_SECRET` (दिखाने के लिए eye आइकन पर क्लिक करें)

---

## चरण 4: Authorization Server चुनें

यह वह कदम है जो आपके discovery URL को निर्धारित करता है। अपने ऑर्ग में authorization servers देखने के लिए **Security → API** पर जाएँ।

**Org authorization server** — Okta ऑर्ग के लिए ही टोकन जारी करता है:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — उनमें वह भी शामिल है जो Okta `default` नाम से बनाता है:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

बिल्ट-इन सर्वर के लिए, `<auth_server_id>` वाक्यात्मक रूप से `default` ही होता है:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "कौन सा?"

    **org** authorization server का उपयोग करें जब तक आपकी संगठन पहले से API एक्सेस नीतियों के लिए किसी कस्टम सर्वर को स्टैंडर्ड न कर चुकी हो। Okta Developer अकाउंट्स डिफ़ॉल्ट रूप से `default` पर होते हैं; कई एंटरप्राइज़ ऑर्ग इसे डिसेबल कर देते हैं। दोनों URL ब्राउज़र में खोलें — जो JSON रिटर्न करता है और एरर नहीं देता, वही आपके लिए उपलब्ध है।

---

## चरण 5: digna कॉन्फ़िगर करें

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

दोनों फ़ाइलों में `key` मेल खाना चाहिए — यहाँ `okta`।

---

## चरण 6: परीक्षण

बैकएंड और वेब सर्वर रीस्टार्ट करें, फिर डैशबोर्ड खोलें। पूरा चेकलिस्ट देखने के लिए [लॉगिन परीक्षण](overview.md#testing-login) देखें।

---

## Okta में समस्या निवारण

### रीडायरेक्ट URI पंजीकृत नहीं है

Okta एरर में दोषी URI बताता है। इसकी तुलना **General → Sign-in redirect URIs** से करें; Okta पूर्ण स्ट्रिंग का मिलान करता है जिसमें कोई भी ट्रेलिंग स्लैश शामिल है।

### उपयोगकर्ता क्लाइंट ऐप्लिकेशन को असाइन नहीं है

खाता ऐप्लिकेशन की असाइनमेंट सूची में नहीं है। **Assignments** के अंतर्गत उपयोगकर्ता या उनके समूह को जोड़ें।

### 400 Bad Request: Invalid Authorization Server

डिस्कवरी URL में `<auth_server_id>` मौजूद नहीं है, अक्सर `default` उस ऑर्ग में हटा दिया गया होता है। वास्तव में उपलब्ध सर्वरों के लिए **Security → API** जांचें।

### टोकन चरण पर invalid_client

इंटीग्रेशन Single-Page Application के रूप में बनाया गया था और उसके पास क्लाइंट सीक्रेट नहीं है। इसे Web Application के रूप में पुनः बनाएं।

---

## इन्हें भी देखें

- [सिंगल साइन-ऑन अवलोकन](overview.md) — कॉन्फ़िगरेशन संदर्भ, परीक्षण और सामान्य समस्या निवारण
- [Okta: OpenID Connect और OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)