---
title: Single Sign-On (SSO) एकीकरण मार्गदर्शिका | digna Documentation
description: OpenID Connect (OIDC) का उपयोग करके digna के लिए Single Sign-On (SSO) कॉन्फ़िगर करने के चरण-दर-चरण निर्देश। डैशबोर्ड और बैकएंड कॉन्फ़िगरेशन, परीक्षण, समस्या निवारण, और Microsoft Entra ID, Google Workspace, Okta सहित समर्थित पहचान प्रदाताओं को कवर करता है।
image: /assets/logo_square.png
keywords:
  - digna sso
  - single sign-on
  - oidc integration
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta integration
  - enterprise authentication
lang: en
robots: index, follow
og_title: digna Single Sign-On (SSO) एकीकरण मार्गदर्शिका
og_description: OpenID Connect का उपयोग करके digna के लिए Single Sign-On कॉन्फ़िगर करें। Microsoft Entra ID, Google Workspace, Okta और अन्य OIDC-अनुपालन पहचान प्रदाताओं के लिए चरण-दर-चरण सेटअप।
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Single Sign-On Integration Guide

---

## Table of Contents

1. [Introduction and Overview](#introduction-and-overview)
2. [Configuration Steps](#configuration-steps)
3. [Dashboard Configuration](#dashboard-configuration)
4. [Backend Configuration](#backend-configuration)
5. [Testing Login](#testing-login)
6. [Troubleshooting](#troubleshooting)
7. [Supported Providers](#supported-providers)

---

## Introduction and Overview {: #introduction-and-overview }

यह मार्गदर्शिका OpenID Connect (OIDC) का उपयोग करके digna प्लेटफ़ॉर्म में Single Sign-On (SSO) एकीकरण के लिए चरण-दर-चरण निर्देश प्रदान करती है।

### SSO क्या है?

Single Sign-On उपयोगकर्ताओं को बाहरी पहचान प्रदाताओं के माध्यम से उनके एंटरप्राइज़ क्रेडेंशियल का उपयोग करके सुरक्षित रूप से digna में लॉगिन करने की अनुमति देता है। उपयोगकर्ता अलग-अलग digna पासवर्ड प्रबंधित करने के बजाय अपने कॉर्पोरेट क्रेडेंशियल से प्रमाणीकरण कर सकते हैं।

### यह कैसे काम करता है

digna में SSO OIDC प्रोटोकॉल का उपयोग करके लागू किया गया है। कई पहचान प्रदाताओं को समान संरचना का पालन करते हुए समानांतर रूप से कॉन्फ़िगर किया जा सकता है—इसके लिए दो प्रमुख कॉन्फ़िगरेशन फ़ाइलों को समायोजित करना होगा:

- **`dashboard_config.toml`** — फ्रंटेंड लॉगिन इंटरफ़ेस को नियंत्रित करता है
- **`config.toml`** — बैकएंड OIDC कनेक्शनों को कॉन्फ़िगर करता है

### समर्थित प्रदाता {: #supported-providers-overview }

इस मार्गदर्शिका में दिए गए उदाहरण **Microsoft** और **Google** का उपयोग करते हैं, लेकिन **कोई भी OIDC-अनुपालन प्रदाता** उसी संरचना का पालन करके एकीकृत किया जा सकता है।

सामान्य OIDC प्रदाताओं में शामिल हैं:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- अन्य OIDC-अनुपालन पहचान प्रदाता

---

## Configuration Steps {: #configuration-steps }

SSO कॉन्फ़िगरेशन के लिए दो फ़ाइलों को अपडेट करने की आवश्यकता होती है। इस अनुभाग में प्रत्येक फ़ाइल को कैसे कॉन्फ़िगर करें बताया गया है।

### Overview of Configuration Files

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend login interface |
| **config.toml** | `/config.toml` | Backend OIDC connections |

दोनों फाइलें SSO सही तरीके से काम करने के लिए कॉन्फ़िगर होनी चाहिए।

---

## Dashboard Configuration {: #dashboard-configuration }

### File Location

```
dashboard/dashboard_config.toml
```

### Step 1: Add OIDC Providers

हर उस पहचान प्रदाता के लिए जिसे आप सपोर्ट करना चाहते हैं, `[[login.oidc]]` एरे के अन्तर्गत एंट्री जोड़ें।

**Microsoft और Google के साथ उदाहरण:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Step 2: Configure Login Options

निर्दिष्ट करें कि पासवर्ड-आधारित लॉगिन अनुमति होनी चाहिए या नहीं:

```toml
[login]
usePassword = true
```

### Configuration Parameters

#### `[[login.oidc]]` Section

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | OIDC कनेक्शन के लिए अद्वितीय पहचानकर्ता (config.toml में key से मेल खाना चाहिए) |
| `label` | string | Yes | लॉगिन बटन पर दिखने वाला टेक्स्ट (उदा., "Login with Microsoft") |

#### `[login]` Section

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | SSO के अलावा पासवर्ड-आधारित लॉगिन की अनुमति दें |

### usePassword को समझना

**यदि `usePassword = true`:**
- लॉगिन स्क्रीन पर SSO बटन दिखेंगे (उदा., "Login with Microsoft")
- लॉगिन स्क्रीन पर यूजरनेम और पासवर्ड फ़ील्ड भी दिखेंगे
- उपयोगकर्ता किसी भी विधि से प्रमाणीकरण कर सकते हैं
- हाइब्रिड सेटअप की अनुमति देता है जहाँ कुछ उपयोगकर्ता SSO का उपयोग करते हैं और कुछ पासवर्ड का

**यदि `usePassword = false` (या न दिया गया हो):**
- लॉगिन स्क्रीन पर केवल SSO बटन दिखेंगे
- कोई यूजरनेम/पासवर्ड फ़ील्ड नहीं होगा
- केवल OIDC प्रमाणीकरण उपलब्ध होगा

> **Tip**
>
> पासवर्ड-आधारित लॉगिन केवल उन उपयोगकर्ताओं के लिए उपलब्ध है जिन्हें `digna user add` कमांड या डैशबोर्ड के माध्यम से पासवर्ड के साथ बनाया गया हो।

### Complete Example

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## Backend Configuration {: #backend-configuration }

### File Location

```
/config.toml
```

(Root digna installation directory)

### Step 1: Add OIDC Provider Sections

प्रत्येक प्रदाता के लिए एक समर्पित `[oidc.<key>]` सेक्शन होना चाहिए। key वही होना चाहिए जो `dashboard_config.toml` में परिभाषित है।

### Microsoft Configuration

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google Configuration

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Configuration Parameters

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | पहचान प्रदाता से प्राप्त क्लाइंट ID | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | पहचान प्रदाता से प्राप्त क्लाइंट सीक्रेट | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | प्रमाणीकरण के बाद कॉलबैक URL | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | OIDC कॉन्फ़िगरेशन एंडपॉइंट | `https://login.microsoftonline.com/...` |

> **Important**
>
> प्लेसहोल्डर वैल्यूज़ (`<client_id>`, `<client_secret>`, `<tenant_id>`) को अपने पहचान प्रदाता के डेवलपर पोर्टल से प्राप्त वास्तविक क्रेडेंशियल से बदलें।

### Redirect URI

Redirect URI आपके पहचान प्रदाता की कॉन्फ़िगरेशन में वही होना चाहिए:

```
http://localhost:5173/oidc/callback
```

यदि digna किसी अलग डोमेन पर होस्ट है, तो उपयुक्त रूप से अपडेट करें:
- Local: `http://localhost:5173/oidc/callback`
- Production: `https://digna.yourdomain.com/oidc/callback`

### Complete Example

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Testing Login {: #testing-login }

कॉन्फ़िगरेशन पूरा करने के बाद सत्यापित करें कि SSO सही ढंग से काम कर रहा है।

### Pre-Testing Checklist

परीक्षण से पहले सुनिश्चित करें:

- [ ] `dashboard_config.toml` में OIDC प्रदाता अपडेट किए गए हैं
- [ ] `config.toml` में OIDC क्रेडेंशियल अपडेट किए गए हैं
- [ ] दोनों फ़ाइलें सेव की गई हैं
- [ ] क्रेडेंशियल सही हैं (client ID, client secret)
- [ ] Redirect URI आपके डिप्लॉयमेंट URL से मेल खाती है
- [ ] पहचान प्रदाता एप्लिकेशन में redirect URI कॉन्फ़िगर की गई है

### Testing Steps

#### Step 1: Restart Services

परिवर्तनों को लागू करने के लिए digna बैकएंड और वेब सर्वर को रीस्टार्ट करें।

**यदि Windows सेवा के रूप में चला रहे हैं:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**यदि मैन्युअली चला रहे हैं:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**यदि IIS या Tomcat उपयोग कर रहे हैं:**
अपने वेब सर्वर सेवा को रीस्टार्ट करें।

#### Step 2: Open Dashboard

अपने ब्राउज़र में digna डैशबोर्ड खोलें:

```
http://localhost:5173
```

(या आपका कॉन्फ़िगर किया गया डैशबोर्ड URL)

#### Step 3: Verify Login Buttons

जाँचें कि प्रत्येक कॉन्फ़िगर किए गए प्रदाता के लिए लॉगिन बटन दिखाई दे रहे हैं:

- "Login with Microsoft" बटन दिखाई देना चाहिए
- "Login with Google" बटन दिखाई देना चाहिए
- (यदि usePassword = true) यूजरनेम/पासवर्ड फ़ील्ड दिखाई देने चाहिए

यदि बटन दिखाई नहीं दे रहे हैं:
- जाँचें कि `dashboard_config.toml` सेव हुई है
- जाँचें कि डैशबोर्ड सेवा रीस्टार्ट हुई है
- ब्राउज़र कंसोल (F12) में त्रुटियाँ देखें

#### Step 4: Test SSO Login

किसी एक SSO बटन (उदा., "Login with Microsoft") पर क्लिक करें:

1. आपको पहचान प्रदाता के लॉगिन पेज पर रीडायरेक्ट किया जाना चाहिए
2. अपने एंटरप्राइज़ क्रेडेंशियल के साथ लॉग इन करें
3. आपको digna पर वापस रीडायरेक्ट किया जाना चाहिए
4. आपको digna में लॉग इन किया हुआ होना चाहिए

#### Step 5: Verify User Creation

सफल SSO लॉगिन के बाद:

- उपयोगकर्ता स्वचालित रूप से digna में बनाया जाना चाहिए
- उपयोगकर्ता लॉग इन होना चाहिए
- उपयोगकर्ता प्रोफ़ाइल में आपके पहचान प्रदाता की जानकारी दिखनी चाहिए
- आपको digna डैशबोर्ड दिखना चाहिए

#### Step 6: Test Password Login (If Enabled)

यदि `usePassword = true`:

1. digna से लॉग आउट करें
2. लॉगिन पेज पर यूजरनेम और पासवर्ड दर्ज करें
3. आप पासवर्ड क्रेडेंशियल के साथ लॉग इन कर पाएंगे

---

## Troubleshooting {: #troubleshooting }

### Login Buttons Don't Appear

**लक्षण:**
- लॉगिन पेज पर OIDC लॉगिन बटन दिखाई नहीं देते
- केवल पासवर्ड फ़ील्ड दिखाई देते हैं (यदि usePassword = true)

**कारण और समाधान:**
1. जाँचें कि `dashboard_config.toml` `dashboard/` डायरेक्टरी में है
2. सत्यापित करें कि `[[login.oidc]]` सेक्शन सही सिंटैक्स के साथ मौजूद हैं
3. डैशबोर्ड सेवा को रीस्टार्ट करें
4. ब्राउज़र कैश साफ़ करें (Ctrl+Shift+Delete या Cmd+Shift+Delete)
5. ब्राउज़र कंसोल (F12 → Console tab) में त्रुटियाँ जांचें

---

### Redirect URI Mismatch Error

**लक्षण:**
- SSO बटन पर क्लिक करने के बाद "redirect_uri mismatch" जैसी त्रुटि
- "The redirect URI is not registered" त्रुटि

**कारण और समाधान:**
1. `config.toml` में `DIGNA_OIDC_REDIRECT_URI` सही है या नहीं जाँचें
2. यह पुष्टि करें कि redirect URI पहचान प्रदाता सेटिंग्स में रजिस्टर है
3. सुनिश्चित करें कि दोनों एक ही URL (प्रोटोकॉल, डोमेन, पाथ सहित) उपयोग कर रहे हों
4. redirect URI में टाइपो न हो इसका जाँचें
5. यदि HTTPS उपयोग कर रहे हैं तो सर्टिफ़िकेट वैध हो यह सुनिश्चित करें

---

### Invalid Client Credentials Error

**लक्षण:**
- "Invalid client ID or secret" त्रुटि
- क्रेडेंशियल त्रुटि के साथ प्रमाणीकरण विफल

**कारण और समाधान:**
1. `DIGNA_OIDC_CLIENT_ID` और `DIGNA_OIDC_CLIENT_SECRET` सही हैं या नहीं जाँचें
2. सुनिश्चित करें कि अतिरिक्त स्पेस या विशेष वर्ण न हों
3. जाँचें कि क्रेडेंशियल की समयसीमा समाप्त नहीं हुई है या रद्द नहीं किया गया है
4. कॉन्फ़िग अपडेट करने के बाद बैकएंड सेवा को रीस्टार्ट करें
5. पहचान प्रदाता कंसोल में क्रेडेंशियल सक्रिय हैं यह पुष्टि करें

---

### Login Hangs or Times Out

**लक्षण:**
- SSO बटन पर क्लिक करने से कुछ नहीं होता
- कुछ सेकंड के बाद टाइमआउट
- ब्राउज़र "Failed to connect" या समान दिखाता है

**कारण और समाधान:**
1. digna बैकएंड चल रहा है यह सत्यापित करें: `digna repo check`
2. पहचान प्रदाता तक नेटवर्क कनेक्टिविटी जाँचें
3. सत्यापित करें कि `DIGNA_OIDC_CONFIGURATION_URL` सुलभ है
4. फ़ायरवॉल नियम आउटबाउंड HTTPS कनेक्शनों की अनुमति दें
5. बैकएंड और डैशबोर्ड एक-दूसरे तक पहुँच सकते हैं यह सत्यापित करें

---

### Users Not Automatically Created

**लक्षण:**
- SSO लॉगिन सफल होता है लेकिन उपयोगकर्ता digna में नहीं बनता
- SSO लॉगिन के बाद अनुमति त्रुटि मिलती है

**कारण और समाधान:**
1. OIDC कॉन्फ़िगरेशन सही है यह सत्यापित करें
2. उपयोगकर्ता अनुमतियाँ सेट हैं यह जांचें
3. digna लॉग्स में त्रुटि संदेश देखें
4. बैकएंड सेवा को रीस्टार्ट करें
5. समस्या बनी रहने पर support@digna.ai से संपर्क करें

---

## Supported Providers {: #supported-providers }

### Tested & Supported

निम्नलिखित OIDC प्रदाताओं का परीक्षण किया गया है और ये काम करने के लिए जानी जाती हैं:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Other OIDC Providers

कोई भी प्रदाता जो OpenID Connect सपोर्ट करता है उसे एकीकृत किया जा सकता है। आवश्यक जानकारी:

- Client ID
- Client secret
- OpenID configuration URL (आमतौर पर `/.well-known/openid-configuration` पर)
- समर्थित scopes (आमतौर पर `openid profile email`)

किसी विशेष प्रदाता को एकीकृत करने में मदद की आवश्यकता हो तो support@digna.ai से संपर्क करें।

---

## Best Practices

**करें:**
- प्रोडक्शन में HTTPS का उपयोग करें (HTTP का उपयोग न करें)
- क्लाइंट सीक्रेट्स को सुरक्षित रूप से स्टोर करें (यदि संभव हो तो environment variables का उपयोग करें)
- समय-समय पर सीक्रेट्स रोटेट करें
- पहले नॉन-प्रोडक्शन वातावरण में टेस्ट करें
- यह दस्तावेज़ रखें कि कौन से प्रदाता कॉन्फ़िगर किए गए हैं
- लॉगिन लॉग्स की निगरानी करें असामान्य गतिविधि के लिए
- पहचान प्रदाता कॉन्फ़िगरेशन को digna कॉन्फ़िग के साथ सिंक रखें

**न करें:**
- क्लाइंट सीक्रेट्स को वर्ज़न कंट्रोल में स्टोर न करें
- प्रोडक्शन में HTTP redirect URIs का उपयोग न करें
- एक ही key के साथ कई प्रदाताओं को कॉन्फ़िगर न करें
- प्रोडक्शन में डिफ़ॉल्ट/टेस्ट क्रेडेंशियल न छोड़ें
- सीक्रेट्स वाली कॉन्फ़िग फाइल्स को एक्सपोज़ न करें
- डेवलपमेंट और प्रोडक्शन क्रेडेंशियल को मिलाकर उपयोग न करें

---

## Support

SSO कॉन्फ़िगरेशन में मदद चाहिए?

- **Email:** support@digna.ai
- **Documentation:** https://docs.digna.ai
- **Website:** https://www.digna.ai

---

**Last Updated:** August 30, 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
