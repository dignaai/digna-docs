---
title: Keycloak SSO – Single Sign-On एकीकरण | digna दस्तावेज़
description: OpenID Connect का उपयोग करते हुए Keycloak के साथ digna के लिए Single Sign-On कॉन्फ़िगर करें — realm और client सेटअप, client authentication, valid redirect URIs, client secret और संबंधित digna कॉन्फ़िगरेशन।
image: /assets/logo_square.png
keywords: digna sso, keycloak sso, keycloak oidc, realm, confidential client, openid connect, self-hosted identity provider
---

# Keycloak के साथ SSO सेट करें

Keycloak एक self-hosted, पूरी तरह OIDC-संगत identity provider है। क्योंकि आप इसे स्वयं चलाते हैं, discovery URL आपके होस्ट नाम और realm से बनता है, न कि किसी विक्रेता के डोमेन से।

यह मार्गदर्शिका **Keycloak पक्ष** को कवर करती है: client बनाना और वह मान एकत्र करना जिनकी digna को आवश्यकता है। digna पक्ष — `dashboard_config.toml`, परीक्षण और ट्रबलशूटिंग — हर प्रदाता के लिए समान है और [Single Sign-On अवलोकन](overview.md) में वर्णित है।

---

## शुरू करने से पहले

| आवश्यकता | नोट्स |
|---|---|
| **Keycloak version** | यहाँ प्रयुक्त URL पथों के लिए 17 या नया — Step 4 में नोट देखें |
| **Keycloak role** | लक्षित realm पर `realm-admin`, या सर्वर एडमिनिस्टेटर |
| **Realm** | वह realm जिसमें आपके digna उपयोगकर्ता हैं, जरूरी नहीं कि `master` हो |
| **digna redirect URI** | उपयोगकर्ता लॉगिन के बाद जिस URL पर लौटते हैं, उदाहरण: `https://digna.yourdomain.com/oidc/callback` |

---

## चरण 1: Realm चुनें

1. Keycloak admin console खोलें
2. ऊपर-बाएँ वाले realm selector का उपयोग करके उस realm पर स्विच करें जिसमें आपके उपयोगकर्ता हैं

!!! warning "master Realm का उपयोग न करें"

    `master` realm स्वयं Keycloak के प्रशासन के लिए है। एप्लिकेशन clients को एक समर्पित realm में रखना चाहिए; digna को `master` में रखने से उसके उपयोगकर्ताओं को Keycloak प्रशासनिक कंसोल में पहुँच मिल सकती है।

---

## चरण 2: Client बनाएं

1. **Clients** पर जाएँ और **Create client** पर क्लिक करें
2. कॉन्फ़िगर करें:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — यह `DIGNA_OIDC_CLIENT_ID` बन जाएगा
3. **Next** पर क्लिक करें
4. **Capability config** चरण पर, **Client authentication** को **On** करें
5. **Standard flow** को सक्षम छोड़ें; अन्य flows की आवश्यकता नहीं है
6. **Next** पर क्लिक करें

!!! warning "Client Authentication ऑन होना ज़रूरी है"

    यदि **Client authentication** बंद है, तो Keycloak एक *public* client बनाएगा, जिसके पास कोई credentials नहीं होंगे — Step 4 में **Credentials** टैब मौजूद नहीं होगा। digna को एक confidential client चाहिए। यदि गलती से यह बंद कर दिया गया तो इसे बाद में बदला जा सकता है।

---

## चरण 3: Redirect URI सेट करें

**Login settings** चरण पर (या बाद में **Settings** टैब में):

1. **Valid redirect URIs**: अपना digna callback URL दर्ज करें:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: खाली छोड़ें, या redirect URIs को मिरर करने के लिए `+` सेट करें
3. **Save** पर क्लिक करें

!!! tip "Wildcards से बचें"

    Keycloak ऐसे पैटर्न स्वीकार करता है जैसे `https://digna.yourdomain.com/*`. वाइल्डकार्ड किसी भी पाथ को उस होस्ट पर authorization code प्राप्त करने देता है, इसलिए सटीक callback URL प्राथमिकता दें।

---

## चरण 4: Client Secret प्राप्त करें

1. **Credentials** टैब खोलें
2. पुष्टि करें कि **Client Authenticator** *Client Id and Secret* है
3. **Client secret** कॉपी करें → यह `DIGNA_OIDC_CLIENT_SECRET` बन जाएगा

Secret यहाँ से पुनःप्राप्त किया जा सकता है और **Regenerate** के साथ पुन: जनरेट किया जा सकता है।

---

## चरण 5: Discovery URL बनाएं

अपने Keycloak host और realm नाम डालें:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

उदाहरण के लिए:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 और उससे पहले में /auth शामिल होता था"

    Keycloak 17 से पहले, हर endpoint `/auth` प्रीफिक्स के अंतर्गत था:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    जो वितरण `KC_HTTP_RELATIVE_PATH=/auth` सेट करते हैं वे वर्तमान संस्करणों पर भी पुराना लेआउट बनाए रखते हैं। यदि बिना `/auth` वाला URL 404 लौटाता है, तो `/auth` के साथ आज़माएँ।

ब्राउज़र में URL खोलें आगे बढ़ने से पहले। एक JSON डॉक्युमेंट यह पुष्टि करता है कि host और realm सही हैं।

---

## चरण 6: digna कॉन्फ़िगर करें

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Login with Keycloak"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

दोनों फाइलों में `key` मेल खाना चाहिए — यहाँ `keycloak`। ध्यान दें कि इसे Keycloak **Client ID** के समान होना जरूरी नहीं है, हालाँकि इन्हें एक जैसा रखना समझने में आसान होता है।

---

## चरण 7: टेस्ट करें

बैकएंड और वेब सर्वर को रिस्टार्ट करें, फिर डैशबोर्ड खोलें। पूरा चेकलिस्ट देखने के लिए [लॉगिन का परीक्षण](overview.md#testing-login) देखें।

---

## Keycloak ट्रबलशूटिंग

### Invalid parameter: redirect_uri

Callback URL **Valid redirect URIs** में शामिल नहीं है। Keycloak सर्वर लॉग में उस URI को लॉग करता है जो उसे मिला — यह सटीक असंगति देखने का सबसे तेज़ तरीका है।

### Credentials टैब गायब है

Client public है। **Settings → Capability config** के अंतर्गत **Client authentication** को ऑन करें।

### Discovery URL पर 404

या तो realm नाम गलत है, या deployment `/auth` प्रीफिक्स का उपयोग कर रहा है। admin console में realm सूची जांचें और दोनों URL रूप आजमाएँ।

### unauthorized_client या invalid_client

**Standard flow** **Capability config** में अक्षम है, या Keycloak में secret regenerate कर दिया गया है बिना `config.toml` अपडेट किए।

### Backend से सर्टिफिकेट त्रुटियाँ

एक self-hosted Keycloak जो निजी या self-signed सर्टिफिकेट के पीछे है, digna के discovery URL के लिए आउटबाउंड HTTPS कॉल विफल कर देगा। जिस मशीन पर digna बैकएंड चल रहा है, उसके trust store में जारी करने वाले CA को इंस्टॉल करें।

---

## अन्य संदर्भ

- [Single Sign-On अवलोकन](overview.md) — कॉन्फ़िगरेशन संदर्भ, परीक्षण और सामान्य ट्रबलशूटिंग
- [Keycloak: अनुप्रयोगों को सुरक्षित करना](https://www.keycloak.org/docs/latest/securing_apps/)