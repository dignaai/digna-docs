---
title: AD FS SSO – सिंगल साइन-ऑन इंटीग्रेशन | digna दस्तावेज़
description: OpenID Connect का उपयोग करके Active Directory Federation Services के साथ digna के लिए सिंगल साइन-ऑन कॉन्फ़िगर करें — application group, server application, shared secret, permitted scopes और मेल खाने वाला digna कॉन्फ़िगरेशन।
image: /assets/logo_square.png
keywords: digna sso, adfs sso, Active Directory Federation Services, adfs oidc, application group, OpenID Connect, ऑन-प्रिमाइस पहचान प्रदाता
---

# AD FS के साथ SSO सेट करें

Active Directory Federation Services ऑन-प्रिमाइज़ विकल्प है: आपके अपने सर्वर टोकन जारी करते हैं, और discovery URL आपका अपना होस्ट नाम होगा। AD FS **Windows Server 2016** से OpenID Connect का समर्थन करता है।

यह गाइड केवल **AD FS पक्ष** को कवर करती है: application group बनाना और वे मान इकट्ठा करना जो digna को चाहिए। digna पक्ष — `dashboard_config.toml`, परीक्षण और समस्याएँ हल करना — हर प्रदाता के लिए वही है और [सिंगल साइन-ऑन अवलोकन](overview.md) में वर्णित है।

---

## शुरू करने से पहले

| आवश्यकता | नोट्स |
|---|---|
| **AD FS version** | Windows Server 2016 या बाद — पुराने संस्करणों में OIDC समर्थन नहीं है |
| **Access** | AD FS सर्वर पर लोकल एडमिनिस्ट्रेटर |
| **Federation service name** | उदाहरण: `adfs.yourdomain.com` |
| **digna redirect URI** | लॉगिन के बाद उपयोगकर्ता जहाँ लौटते हैं वह URL, उदाहरण: `https://digna.yourdomain.com/oidc/callback` |

---

## कदम 1: Application Group बनाएं

1. AD FS सर्वर पर, **AD FS Management** खोलें
2. **Application Groups** पर राइट‑क्लिक करें और **Add Application Group** चुनें
3. नाम में `digna` दर्ज करें
4. **Standalone applications** — या आपकी वर्ज़न के अनुसार **Client-Server applications** — के अंतर्गत **Server application accessing a web API** चुनें
5. **Next** पर क्लिक करें

---

## कदम 2: Server Application कॉन्फ़िगर करें

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS एक GUID जनरेट करता है। इसे कॉपी करें — यह `DIGNA_OIDC_CLIENT_ID` बन जाएगा
3. **Redirect URI**: अपना digna callback URL दर्ज करें और **Add** पर क्लिक करें:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Next** पर क्लिक करें

!!! warning "Add पर क्लिक करें, केवल Next मत दबाएं"

    Redirect URI फील्ड का अपना **Add** बटन होता है। URI टाइप करके केवल **Next** पर क्लिक करने से वह सुरक्षित नहीं होता और विज़ार्ड कोई चेतावनी नहीं देता। जारी रखने से पहले सुनिश्चित करें कि URI फील्ड के नीचे सूची में दिखाई दे रहा है।

---

## कदम 3: साझा रहस्य (Shared Secret) जनरेट करें

1. **Generate a shared secret** को टिक करें
2. जनरेट किया गया secret कॉपी करें → यह `DIGNA_OIDC_CLIENT_SECRET` बन जाएगा
3. **Next** पर क्लिक करें

!!! warning "गोपनीय कुंजी केवल एक बार दिखाई जाती है"

    AD FS यह shared secret केवल इस विज़ार्ड पृष्ठ पर दिखाता है और इसे बाद में फिर नहीं दिखा सकता। यदि आप इसे खो देते हैं, तो बाद में application group की properties से इसे रीसेट करें।

---

## कदम 4: Web API कॉन्फ़िगर करें

1. **Identifier**: Step 2 से वही client identifier दर्ज करें और **Add** पर क्लिक करें
2. **Next** पर क्लिक करें
3. कोई **Access Control Policy** चुनें — *Permit everyone* सबसे सरल आरंभिक विकल्प है; प्रोडक्शन में इसे किसी समूह तक सीमित करें
4. **Next** पर क्लिक करें

---

## कदम 5: अनुमति प्राप्त Scopes दें

**Configure Application Permissions** चरण में, निम्न को टिक करें:

- `openid`
- `profile`
- `email`

फिर **Next** पर क्लिक करें और विज़ार्ड पूरा करें।

!!! warning "openid डिफ़ॉल्ट रूप से चयनित नहीं होता"

    कुछ वर्ज़नों में AD FS केवल `user_impersonation` को प्री‑सेलेक्ट करता है। यदि `openid` नहीं है तो token endpoint एक OAuth access token लौटाता है न कि ID token, और digna उपयोगकर्ता की पहचान नहीं कर पाएगा।

---

## कदम 6: Discovery Endpoint सत्यापित करें

अपना federation service नाम यहाँ रखें:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

उदाहरण के लिए:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

इसे ब्राउज़र में खोलें। एक JSON दस्तावेज़ बताएगा कि OIDC सक्षम है और होस्ट नाम सही है।

!!! note "बैकएंड को सर्टिफिकेट पर भरोसा होना चाहिए"

    AD FS के लिए आंतरिक सर्टिफिकेट प्राधिकरण सामान्य है। जो मशीन digna backend चला रही है वह इस URL पर अपना आउटबाउंड HTTPS कॉल खुद करती है, इसलिए जारी करने वाली CA उस मशीन के ट्रस्ट स्टोर में होनी चाहिए — केवल लॉगिन करने वाले लोगों के ब्राउज़रों में नहीं।

---

## कदम 7: digna कॉन्फ़िगर करें

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

दोनों फ़ाइलों में `key` मेल खाना चाहिए — यहाँ `adfs`।

---

## कदम 8: परीक्षण करें

बैकएंड और वेब सर्वर पुनरारंभ करें, फिर डैशबोर्ड खोलें। पूरी चेकलिस्ट के लिए [लॉगिन का परीक्षण](overview.md#testing-login) देखें।

---

## AD FS समस्याओं का निवारण

### MSIS9611: The Client Is Not Allowed to Access the Resource

Step 4 में दिया गया वेब API identifier client identifier से मेल नहीं खाता, या Step 5 में scopes अनुदानित नहीं किए गए। दोनों application group की properties से संपादित किए जा सकते हैं।

### MSIS9602: Invalid redirect_uri

URI टाइप किया गया था लेकिन **Add** बटन के साथ जोड़ा नहीं गया, या यह `DIGNA_OIDC_REDIRECT_URI` से अलग है। जाँचें: **Application Groups → digna → digna backend → Properties**।

### कोई ID Token वापस नहीं आ रहा

Application permissions में `openid` scope गायब है।

### बैकएंड Discovery URL तक पहुँच नहीं पा रहा

या तो बैकएंड होस्ट पर DNS federation service नाम को हल नहीं कर रहा है, या AD FS सर्टिफिकेट वहां ट्रस्टेड नहीं है। digna सर्वर से यह कमांड चलाकर जाँचें: `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration`

### जांचने के लिए इवेंट्स

AD FS सर्वर Event Viewer में **Applications and Services Logs → AD FS → Admin** में विफलताओं को लॉग करता है, जो आमतौर पर ब्राउज़र में दिखने वाले संदेश से अधिक विशिष्ट कारण देते हैं।

---

## संबंधित सामग्री

- [सिंगल साइन-ऑन अवलोकन](overview.md) — कॉन्फ़िगरेशन संदर्भ, परीक्षण और सामान्य समस्या निवारण
- [Microsoft: AD FS OpenID Connect परिदृश्य](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)