---
title: PingOne SSO – सिंगल साइन-ऑन एकीकरण | digna दस्तावेज़
description: OpenID Connect का उपयोग करके PingOne के साथ digna के लिए सिंगल साइन-ऑन कॉन्फ़िगर करें — OIDC वेब ऐप सेटअप, रीडायरेक्ट URIs, क्लाइंट क्रेडेंशियल, environment ID, क्षेत्रीय डोमेनों और मिलती-जुलती digna कॉन्फ़िगरेशन।
image: /assets/logo_square.png
keywords: digna sso, pingone sso, ping identity, pingone oidc, environment id, openid connect, enterprise authentication
---

# PingOne के साथ SSO सेटअप करें

PingOne OIDC-अनुरूप है। इसके दो मानों पर ध्यान चाहिए: **environment ID**, जो हर एंडपॉइंट URL में दिखाई देता है, और **regional domain**, जो North American, European, Canadian, Asia-Pacific और Australian टेनेंट्स में अलग होता है।

यह मार्गदर्शिका केवल **PingOne पक्ष** को कवर करती है: एप्लिकेशन बनाना और वे मान इकट्ठा करना जो digna को चाहिए। digna पक्ष — `dashboard_config.toml`, परीक्षण और समस्या निवारण — हर प्रदाता के लिए समान है और [Single Sign-On Overview](overview.md) में वर्णित है।

---

## शुरू करने से पहले

| आवश्यकता | नोट्स |
|---|---|
| **PingOne भूमिका** | लक्षित environment पर Environment Admin या Identity Data Admin |
| **Environment** | वह PingOne environment जिसमें आपके digna उपयोगकर्ता हैं |
| **digna redirect URI** | लॉगिन के बाद उपयोगकर्ता जहाँ लौटते हैं उसका URL, उदाहरण: `https://digna.yourdomain.com/oidc/callback` |

---

## चरण 1: एप्लिकेशन बनाएं

1. PingOne एडमिन कंसोल में साइन इन करें और अपना environment चुनें
2. **Applications → Applications** पर जाएँ
3. **+** बटन पर क्लिक करें
4. **Application Name** में `digna` दर्ज करें
5. **OIDC Web App** चुनें
6. **Save** पर क्लिक करें

!!! warning "OIDC Web App चुनें, Single-Page App नहीं"

    *Single-Page App* और *Native App* पब्लिक क्लाइंट बनाते हैं जो सीक्रेट नहीं रख सकते। digna अपने बैकएंड से authorization code का विनिमय करता है और उसे confidential **OIDC Web App** प्रकार की आवश्यकता होती है।

---

## चरण 2: Redirect URI कॉन्फ़िगर करें

1. एप्लिकेशन की **Configuration** टैब खोलें
2. एडिट करने के लिए पेंसिल आइकन पर क्लिक करें
3. पुष्टि करें कि **Response Type** *Code* है और **Grant Type** *Authorization Code* है
4. **Redirect URIs** के तहत अपने digna callback URL दर्ज करें:

```
https://digna.yourdomain.com/oidc/callback
```

5. **Token Endpoint Authentication Method** को *Client Secret Post* या *Client Secret Basic* पर सेट करें
6. **Save** पर क्लिक करें

---

## चरण 3: एप्लिकेशन सक्षम करें

एप्लिकेशन की पंक्ति या डिटेल पैनल पर टॉगल को **enabled** पर स्विच करें।

!!! warning "नई एप्लिकेशन शुरू में Disabled होती हैं"

    PingOne एप्लिकेशन को disabled स्थिति में बनाता है। एक disabled एप्लिकेशन authorization चरण पर एक त्रुटि पैदा करता है जो टॉगल का उल्लेख नहीं करती, इसलिए किसी और चीज़ को डिबग करने से पहले इसे सत्यापित करना उपयोगी होता है।

---

## चरण 4: Scopes दें

1. **Resources** टैब खोलें
2. सुनिश्चित करें कि `openid` दिया गया है, और **OpenID Connect** संसाधन से `profile` और `email` जोड़ें
3. **Save** पर क्लिक करें

---

## चरण 5: उपयोगकर्ता असाइन करें

1. **Access** टैब खोलें
2. वह पॉपुलेशन या समूह जोड़ें जिनके सदस्य digna का उपयोग कर सकते हैं
3. **Save** पर क्लिक करें

---

## चरण 6: क्रेडेंशियल्स और Environment ID इकट्ठा करें

**Configuration** टैब पर, **General** खोलें:

- **Client ID** → यह `DIGNA_OIDC_CLIENT_ID` बन जाता है
- **Client Secret** → यह `DIGNA_OIDC_CLIENT_SECRET` बन जाता है (आईकन पर क्लिक करके देखें)
- **Environment ID** → यह discovery URL में जाता है

उसी टैब पर तैयार-निर्मित **OIDC Discovery Endpoint** भी सूचीबद्ध होता है, जिसे आप हाथ से बनाने के बजाय सीधे कॉपी कर सकते हैं।

---

## चरण 7: Discovery URL बनाएँ

environment ID और अपने क्षेत्र का डोमेन सब्स्टिट्यूट करें:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Region | Domain |
|---|---|
| North America | `auth.pingone.com` |
| Europe | `auth.pingone.eu` |
| Canada | `auth.pingone.ca` |
| Asia-Pacific | `auth.pingone.asia` |
| Australia | `auth.pingone.com.au` |

एक European environment के लिए:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "टाइप करने से बेहतर है कि आप कॉपी करें"

    क्षेत्रीय डोमेन PingOne एकीकरण में सबसे सामान्य गलती है, और गलत क्षेत्र 404 देता है न कि उपयोगी संदेश। Step 6 में दिखाई देने वाले **OIDC Discovery Endpoint** मान का उपयोग करें।

---

## चरण 8: digna कॉन्फ़िगर करें

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "PingOne से लॉगिन"
```

### `config.toml`

```toml
[oidc.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

दोनों फ़ाइलों में `key` मेल खाना चाहिए — यहाँ `pingone`।

---

## चरण 9: परीक्षण करें

बैकएंड और वेब सर्वर को रीस्टार्ट करें, फिर डैशबोर्ड खोलें। पूरा चेकलिस्ट देखने के लिए [Testing Login](overview.md#testing-login) देखें।

---

## PingOne समस्या निवारण

### Discovery URL पर 404

क्षेत्रीय डोमेन या environment ID गलत है। एप्लिकेशन की Configuration टैब पर दिखाई जाने वाली **OIDC Discovery Endpoint** से तुलना करें।

### NOT_FOUND या Application Disabled

Step 3 में टॉगल अभी भी बंद है।

### Redirect URI मेल नहीं खा रही

PingOne पूरे स्ट्रिंग से मैच करता है। **Configuration → Redirect URIs** में ट्रेलिंग स्लैश या स्कीम अंतर की जाँच करें।

### लॉगिन सफल लेकिन कोई Email Claim digna तक नहीं पहुँचता

**Resources** टैब पर `email` और `profile` स्कोप दिए गए नहीं हैं।

### उपयोगकर्ता एप्लिकेशन नहीं देख सकता

**Access** टैब पर किसी पॉपुलेशन या समूह को एक्सेस नहीं दिया गया है।

---

## संबंधित

- [Single Sign-On Overview](overview.md) — कॉन्फ़िगरेशन संदर्भ, परीक्षण और सामान्य समस्या निवारण
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)