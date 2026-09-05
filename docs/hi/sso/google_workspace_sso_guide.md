---
title: Google Workspace SSO – सिंगल साइन-ऑन एकीकरण | digna Documentation
description: OpenID Connect का उपयोग करके Google Workspace के साथ digna के लिए सिंगल साइन-ऑन कॉन्फ़िगर करें — OAuth consent screen, OAuth client ID, प्रमाणित redirect URIs और संबंधित digna कॉन्फ़िगरेशन।
image: /assets/logo_square.png
keywords: digna sso, google workspace sso, google oidc, oauth consent screen, openid connect, एंटरप्राइज़ प्रमाणीकरण
---

# Google Workspace के साथ SSO सेटअप करें

Google की identity platform OIDC-समर्थित है और प्रत्येक ग्राहक के लिए एक ही, well-known discovery URL का उपयोग करती है, इसलिए प्रति-ऑर्गेनाइज़ेशन केवल client ID और secret अलग होते हैं।

यह गाइड **Google पक्ष** को कवर करता: OAuth क्लाइंट बनाना और वे मान एकत्र करना जिन्हें digna को चाहिए। digna पक्ष — `dashboard_config.toml`, परीक्षण और ट्रबलशूटिंग — हर provider के लिए समान है और [Single Sign-On Overview](overview.md) में वर्णित है।

---

## शुरू करने से पहले

| आवश्यकता | नोट्स |
|---|---|
| **Google Cloud project** | आपकी Workspace डोमेन के साथ उसी संगठन में कोई भी प्रोजेक्ट |
| **भूमिका** | प्रोजेक्ट पर Editor या Owner |
| **digna redirect URI** | लॉगिन के बाद उपयोगकर्ता जहाँ वापस आते हैं वह URL, उदाहरण: `https://digna.yourdomain.com/oidc/callback` |

---

## चरण 1: OAuth सहमति स्क्रीन कॉन्फ़िगर करें

Google तब तक क्रेडेंशियल जारी नहीं करेगा जब तक कि सहमति स्क्रीन मौजूद न हो।

1. [Google Cloud Console](https://console.cloud.google.com) खोलें और अपना प्रोजेक्ट चुनें
2. **APIs & Services → OAuth consent screen** पर जाएँ
3. उपयोगकर्ता प्रकार चुनें:
   - **Internal** — केवल आपकी Workspace डोमेन के खाते लॉग इन कर सकते हैं। अनुशंसित।
   - **External** — कोई भी Google खाता लॉगिन का प्रयास कर सकता है।
4. ऐप नाम, user support email और developer contact email भरें
5. **Scopes** चरण पर, `openid`, `.../auth/userinfo.email` और `.../auth/userinfo.profile` जोड़ें
6. सेव करें

!!! warning "बाहरी ऐप्स प्रकाशित होने चाहिए"

    एक **External** सहमति स्क्रीन *Testing* स्थिति में शुरू होती है, जहाँ केवल उन खातों को जो टेस्ट-यूजर सूची में स्पष्ट रूप से जोड़े गए हैं लॉगिन पूरा कर सकते हैं। बाकी सभी को "digna has not completed the Google verification process" दिखेगा। या तो ऐप को **In production** के अंतर्गत **Publishing status** में स्विच करें, या **Internal** का उपयोग करें — जिसके लिए ऐसी कोई बाधा नहीं है और यह Workspace-केवल डिप्लॉयमेंट के लिए सही विकल्प है।

---

## चरण 2: OAuth क्लाइंट बनाएं

1. **APIs & Services → Credentials** पर जाएँ
2. **Create Credentials → OAuth client ID** पर क्लिक करें
3. **Application type** को **Web application** पर सेट करें
4. इसे एक नाम दें, उदाहरण के लिए `digna`
5. **Authorized redirect URIs** के अंतर्गत **Add URI** पर क्लिक करें और दर्ज करें:

```
https://digna.yourdomain.com/oidc/callback
```

6. **Create** पर क्लिक करें

!!! note "Authorized JavaScript Origins आवश्यक नहीं हैं"

    digna authorization code बैकएंड से एक्सचेंज करता है, ब्राउज़र से नहीं, इसलिए **Authorized JavaScript origins** फ़ील्ड खाली छोड़ा जा सकता है। केवल redirect URI मायने रखता है।

---

## चरण 3: प्रमाण-पत्र जमा करें

बनाने के बाद जो डायलॉग दिखाई देता है उसमें दिखता है:

- **Client ID** — `.apps.googleusercontent.com` पर समाप्त होता है → यह `DIGNA_OIDC_CLIENT_ID` बनता है
- **Client secret** → यह `DIGNA_OIDC_CLIENT_SECRET` बनता है

दोनों बाद में क्रेडेंशियल के विवरण पृष्ठ से पुनः प्राप्त किए जा सकते हैं, जो कि अधिकतर अन्य प्रदाताओं के विपरीत है।

---

## चरण 4: डिस्कवरी URL

Google सभी ग्राहकों के लिए एक ही डिस्कवरी URL का उपयोग करता है — यहाँ कोई प्रतिस्थापन नहीं है:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## चरण 5: digna कॉन्फ़िगर करें

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

दोनों फ़ाइलों में `key` मेल खाना चाहिए — यहाँ `google`।

---

## चरण 6: परीक्षण

बैकएंड और वेब सर्वर को रीस्टार्ट करें, फिर डैशबोर्ड खोलें। पूर्ण चेकलिस्ट के लिए देखें [Testing Login](overview.md#testing-login)।

---

## Google Workspace के लिए ट्रबलशूटिंग

### Error 400: redirect_uri_mismatch

`DIGNA_OIDC_REDIRECT_URI` में दिया गया URI **Authorized redirect URIs** सूचि में नहीं है, या यह ट्रेलिंग स्लैश या स्कीम से अलग है। Google का त्रुटि पेज वह URI दिखाता है जो उसे मिला — उसे पंजीकृत URI के साथ शब्द-दर-शब्द तुलना करें।

### This App Is Blocked / Has Not Completed Verification

सहमति स्क्रीन **External** है और अभी भी *Testing* में है। इसे प्रकाशित करें, या ऐप को **Internal** में बदलें।

### Access Blocked: Authorization Error

लॉगिन का प्रयास कर रहा खाता आपकी Workspace डोमेन के बाहर है जबकि सहमति स्क्रीन **Internal** है। यह इच्छित व्यवहार है — Internal ऐप केवल संगठन के भीतर के खातों को स्वीकार करते हैं।

### बदलावों में कुछ मिनट लगते हैं

Google asynchronously क्रेडेंशियल और सहमति-स्क्रीन परिवर्तनों को फैलाता है। नया जोड़ा गया redirect URI प्रभावी होने में कुछ मिनट ले सकता है; अगर कोई परिवर्तन अनदेखा दिखता है, तो आगे जाँच करने से पहले प्रतीक्षा करें और पुनः प्रयास करें।

---

## संदर्भ

- [Single Sign-On Overview](overview.md) — कॉन्फ़िगरेशन संदर्भ, परीक्षण और सामान्य ट्रबलशूटिंग
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)