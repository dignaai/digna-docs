---
title: OneLogin SSO – सिंगल साइन-ऑन इंटीग्रेशन | digna दस्तावेज़
description: OpenID Connect का उपयोग करके OneLogin के साथ digna के लिए सिंगल साइन-ऑन कॉन्फ़िगर करें — OIDC एप बनाना, redirect URIs, क्लाइंट क्रेडेंशियल्स, token endpoint प्रमाणीकरण और अनुरूप digna कॉन्फ़िगरेशन।
image: /assets/logo_square.png
keywords: digna SSO, OneLogin SSO, OneLogin OIDC, OpenID Connect, टोकन एंडपॉइंट प्रमाणीकरण, एंटरप्राइज़ प्रमाणीकरण
---

# OneLogin के साथ SSO सेटअप

OneLogin OIDC-आधारित है। इसकी खास बात यह है कि एप बनाने के समय connector प्रकार कैटलॉग से चुना जाता है और बाद में इसे बदला नहीं जा सकता।

यह गाइड केवल **OneLogin पक्ष** को कवर करता: एप बनाना और वे मान इकट्ठा करना जो digna को चाहिए। digna पक्ष — `dashboard_config.toml`, टेस्टिंग और ट्रबलशूटिंग — हर प्रदाता के लिए समान है और उसे [Single Sign-On Overview](overview.md) में बताया गया है।

---

## शुरू करने से पहले

| Requirement | Notes |
|---|---|
| **OneLogin role** | Account owner या किसी ऐसे एडमिनिस्ट्रेटर की अनुमति जो एप्लिकेशन जोड़ सके |
| **Subdomain** | उदाहरण: `yourcompany.onelogin.com` |
| **digna redirect URI** | लॉगिन के बाद उपयोगकर्ता जहाँ लौटते हैं वह URL, उदाहरण: `https://digna.yourdomain.com/oidc/callback` |

---

## कदम 1: OIDC एप्लिकेशन बनाएँ

1. OneLogin Admin पोर्टल में साइन इन करें
2. **Applications → Applications** पर जाएँ
3. **Add App** पर क्लिक करें
4. `OpenId Connect` खोजें और **OpenId Connect (OIDC)** connector चुनें
5. **Display Name** को `digna` सेट करें
6. **Save** पर क्लिक करें

!!! warning "कनेक्टर प्रकार निर्माण के समय तय हो जाता है"

    OneLogin में SAML और OIDC के अलग-अलग कैटलॉग एंट्री होते हैं, और एक एप्लिकेशन को एक से दूसरे में बदला नहीं जा सकता। अगर आपने गलती से SAML कनेक्टर चुना है, तो एप को डिलीट करें और फिर से जोड़ें — प्रोटोकॉल बदलने का कोई सेटिंग नहीं है।

---

## कदम 2: Redirect URI कॉन्फ़िगर करें

1. **Configuration** टैब खोलें
2. **Redirect URI's** में अपना digna callback URL दर्ज करें:

```
https://digna.yourdomain.com/oidc/callback
```

3. वैकल्पिक रूप से **Post Logout Redirect URIs** को अपने डैशबोर्ड URL पर सेट करें
4. **Save** पर क्लिक करें

!!! note "एक URI प्रति लाइन"

    कुछ प्रदाताओं की तरह कॉमा-सेपरेटेड सूची की अपेक्षा के विपरीत, OneLogin का **Redirect URI's** फील्ड हर URI को अलग लाइन में लेता है।

---

## कदम 3: एप्लिकेशन प्रकार और प्रमाणीकरण विधि सेट करें

1. **SSO** टैब खोलें
2. पुष्टि करें कि **Application Type** *Web* है
3. **Token Endpoint → Authentication Method** को *POST* (`client_secret_post`) या *Basic* (`client_secret_basic`) पर सेट करें

!!! warning "None न चुनें"

    Authentication method को *None* पर सेट करने से एप्लिकेशन एक public client बन जाता है बिना किसी सीक्रेट के, और digna का बैकएंड कोड एक्सचेंज अस्वीकृत कर देगा। POST या Basic दोनों काम करते हैं।

---

## कदम 4: क्रेडेंशियल्स इकट्ठा करें

अभी भी **SSO** टैब पर:

- **Client ID** → यह बन जाएगा `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → यह बन जाएगा `DIGNA_OIDC_CLIENT_SECRET` (क्लिक करें **Show client secret**)

पेज पर **Issuer URL** भी दिखेगा, जो अगले चरण में discovery URL की पुष्टि करता है।

---

## कदम 5: उपयोगकर्ताओं को असाइन करें

1. **Access** टैब खोलें
2. उन रोल्स या समूहों को जोड़ें जिनके सदस्य digna का उपयोग कर सकते हैं
3. **Save** पर क्लिक करें

!!! note "अनअसाइन्ड उपयोगकर्ताओं को लॉगिन के बाद रिजेक्ट किया जाएगा"

    अधिकांश प्रदाताओं की तरह, OneLogin पहले उपयोगकर्ता को प्रमाणित करता है और फिर अधिकार जांचता है। बिना असाइन किए हुए उपयोगकर्ता सफलतापूर्वक साइन इन कर लेते हैं और फिर अस्वीकार कर दिए जाते हैं — जो दिखने में digna त्रुटि लगता है न कि एक्सेस-कंट्रोल निर्णय।

---

## कदम 6: Discovery URL बनाएं

अपने OneLogin सबडोमेन को सब्स्टिट्यूट करें:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

उदाहरण के लिए:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "/2 API वर्ज़न है"

    OneLogin का वर्तमान OIDC इम्प्लिमेंटेशन `/oidc/2/` के तहत है। पुरानी डॉ큐मेंटेशन में `/oidc/` बिना वर्ज़न के दिखता है, जो पहले रिटायर्ड वर्ज़न की ओर इशारा करता है। शंका होने पर **SSO** टैब पर दिख रहे **Issuer URL** से मिलान करें — discovery URL issuer के साथ `/.well-known/openid-configuration` जोड़कर बनता है।

---

## कदम 7: digna कॉन्फ़िगर करें

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Login with OneLogin"
```

### `config.toml`

```toml
[oidc.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

दोनों फाइलों में `key` मेल खाना चाहिए — यहाँ `onelogin` है।

---

## कदम 8: टेस्ट करें

बैकएंड और वेब सर्वर को रीस्टार्ट करें, फिर डैशबोर्ड खोलें। पूरी चेकलिस्ट के लिए [Testing Login](overview.md#testing-login) देखें।

---

## OneLogin ट्रबलशूटिंग

### redirect_uri did not match

Callback URL **Configuration → Redirect URI's** में मौजूद नहीं है, या एंट्रीज़ को कॉमिक-सेपरेटेड की बजाय कमाओं से अलग किया गया था।

### invalid_client at the Token Step

**Token Endpoint → Authentication Method** *None* पर सेट है, या `config.toml` में क्लाइंट सीक्रेट पुराना है। **SSO** टैब पर सीक्रेट दिखाएँ और तुलना करें।

### एप उपयोगकर्ताओं के लिए दिखाई नहीं देता

**Access** टैब पर किसी रोल या समूह को एक्सेस नहीं दिया गया है।

### Discovery URL पर 404

सबडोमेन गलत है, या URL में `/oidc/2/` छूटा हुआ है। **SSO** टैब पर दिख रहे **Issuer URL** से तुलना करें।

---

## संबंधित जानकारी

- [Single Sign-On Overview](overview.md) — कॉन्फ़िगरेशन संदर्भ, परीक्षण और सामान्य ट्रबलशूटिंग
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)