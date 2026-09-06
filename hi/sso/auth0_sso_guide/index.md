# Auth0 के साथ SSO सेट अप करें

Auth0 OIDC-अनुरूप है और प्रत्येक tenant के लिए एक discovery endpoint प्रदान करता है। मुख्य चीज़ जो सही होनी चाहिए वह है tenant डोमेन, जो discovery URL में प्रकट होता है और यदि आप कस्टम डोमेन सक्षम करते हैं तो बदलता है।

यह गाइड **Auth0 पक्ष** को कवर करता है: एप्लिकेशन बनाना और वे मान एकत्र करना जिनकी digna को जरूरत है। digna पक्ष — `dashboard_config.toml`, परीक्षण और ट्रबलशूटिंग — हर प्रदाता के लिए समान है और [Single Sign-On Overview](overview.md) में वर्णित है।

---

## शुरू करने से पहले

| आवश्यकता | नोट्स |
|---|---|
| **Auth0 role** | टेनेंट पर Admin |
| **Tenant domain** | उदाहरण: `yourcompany.eu.auth0.com` — region segment मायने रखता है |
| **digna redirect URI** | वह URL जहाँ उपयोगकर्ता लॉगिन के बाद लौटता है, उदाहरण: `https://digna.yourdomain.com/oidc/callback` |

---

## चरण 1: एप्लिकेशन बनाएं

1. [Auth0 डैशबोर्ड](https://manage.auth0.com) में साइन इन करें
2. जाएँ **Applications → Applications**
3. क्लिक करें **Create Application**
4. नाम दें `digna` और चुनें **Regular Web Applications**
5. क्लिक करें **Create**

!!! warning "Regular Web Applications चुनें"

    *Single Page Application* और *Native* सार्वजनिक क्लाइंट बनाते हैं जिनमें कोई secret नहीं होता। digna बैकएंड से code exchange करता है और एक confidential client की आवश्यकता होती है, इसलिए **Regular Web Applications** सही प्रकार है। कुछ प्रदाताओं के विपरीत, Auth0 आपको बाद में **Settings → Application Type** के अंतर्गत प्रकार बदलने देता है।

---

## चरण 2: Callback URL जोड़ें

एप्लिकेशन के **Settings** टैब पर:

1. खोजें **Allowed Callback URLs**
2. अपना digna callback URL दर्ज करें:

```
https://digna.yourdomain.com/oidc/callback
```

3. वैकल्पिक रूप से **Allowed Logout URLs** को अपने डैशबोर्ड URL पर सेट करें
4. नीचे स्क्रॉल करें और क्लिक करें **Save Changes**

!!! note "कॉमा से अलग करें, नई लाइन से नहीं"

    Auth0 इस फ़ील्ड में कई callback URLs स्वीकार करता है, जिनको कॉमा से अलग किया गया होना चाहिए। केवल नई लाइनों से अलग की गई सूची को एक malformed URL माना जाता है और यह चुपचाप किसी से मेल नहीं खाती।

---

## चरण 3: क्रेडेंशियल्स एकत्र करें

अभी भी **Settings** पर, **Basic Information** पैनल में:

- **Domain** → discovery URL में जाता है
- **Client ID** → बन जाएगा `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → बन जाएगा `DIGNA_OIDC_CLIENT_SECRET` (प्रकट करने के लिए क्लिक करें)

---

## चरण 4: Grant Type की पुष्टि करें

1. जाएँ **Settings → Advanced Settings → Grant Types**
2. पुष्टि करें कि **Authorization Code** टिक किया गया है

यह Regular Web Applications के लिए डिफ़ॉल्ट रूप से सक्षम है। यदि यह अनचेक किया गया है, तो digna का लॉगिन `unauthorized_client` के साथ फेल हो जाता है।

---

## चरण 5: Discovery URL बनाएं

Step 3 से **Domain** प्रतिस्थापित करें:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

उदाहरण के लिए:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "कस्टम डोमेन Issuer बदल देते हैं"

    यदि आपका tenant किसी कस्टम डोमेन जैसे `login.yourcompany.com` का उपयोग करता है, तो discovery URL में वही डोमेन उपयोग करें। दोनों को मिलाना — discovery URL में canonical domain और ब्राउज़र में custom domain — issuer mismatch उत्पन्न करता है, और एक अन्यथा सफल लॉगिन के बाद टोकन अस्वीकार कर दिया जाएगा।

---

## चरण 6: digna कॉन्फ़िगर करें

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

दोनों फाइलों में `key` मैच करनी चाहिए — यहाँ `auth0`।

---

## चरण 7: परीक्षण करें

बैकएंड और वेब सर्वर रीस्टार्ट करें, फिर डैशबोर्ड खोलें। पूर्ण चेकलिस्ट के लिए देखें [Testing Login](overview.md#testing-login)।

---

## Auth0 के लिए ट्रबलशूटिंग

### Callback URL मेल नहीं खा रही

Auth0 की त्रुटि पृष्ठ उस URL का नाम बताती है जो उसे मिला। उसे **Allowed Callback URLs** में जोड़ें, यह सुनिश्चित करते हुए कि एंट्रीज़ कॉमा-सेपरेटेड हैं।

### unauthorized_client

**Authorization Code** **Advanced Settings → Grant Types** के अंतर्गत सक्षम नहीं है, या एप्लिकेशन प्रकार Regular Web Applications नहीं है।

### सफल लॉगिन के बाद Access Denied

टेनेंट में कोई Rule, Action या Post-Login trigger उपयोगकर्ता को अस्वीकार कर रहा है। जाँच करें **Actions → Flows → Login** और टेनेंट लॉग्स **Monitoring → Logs** के अंतर्गत, जो सटीक कारण दिखाते हैं।

### Issuer Mismatch

discovery URL और जिस डोमेन पर ब्राउज़र भेजा गया था वे अलग हैं — आमतौर पर canonical tenant domain बनाम कस्टम डोमेन। एक ही डोमेन का लगातार उपयोग करें।

---

## संबंधित विषय

- [सिंगल साइन-ऑन अवलोकन](overview.md) — कॉन्फ़िगरेशन संदर्भ, परीक्षण और सामान्य ट्रबलशूटिंग
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)