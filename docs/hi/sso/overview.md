---
title: सिंगल साइन-ऑन (SSO) अवलोकन | digna डोक्यूमेंटेशन
description: digna में OpenID Connect (OIDC) का उपयोग कर Single Sign-On कैसे काम करता है। डैशबोर्ड और बैकएंड कॉन्फ़िगरेशन, परीक्षण, समस्या निवारण और Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak, OneLogin, PingOne और AD FS के प्रति-प्रदाता सेटअप गाइड के लिंक शामिल हैं।
image: /assets/logo_square.png
keywords:
  - digna SSO
  - सिंगल साइन-ऑन
  - oidc integration
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta integration
  - enterprise authentication
lang: en
robots: index, follow
og_title: digna Single Sign-On (SSO) Integration Guide
og_description: Configure Single Sign-On for digna using OpenID Connect. Step-by-step setup for Microsoft Entra ID, Google Workspace, Okta, and other OIDC-compliant identity providers.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# सिंगल साइन-ऑन अवलोकन

---

## सामग्री तालिका

1. [परिचय और अवलोकन](#introduction-and-overview)
2. [प्रदाता गाइड](#provider-guides)
3. [कॉन्फ़िगरेशन चरण](#configuration-steps)
4. [डैशबोर्ड कॉन्फ़िगरेशन](#dashboard-configuration)
5. [बैकएंड कॉन्फ़िगरेशन](#backend-configuration)
6. [लॉगिन परीक्षण](#testing-login)
7. [समस्या निवारण](#troubleshooting)
8. [समर्थित प्रदाता](#supported-providers)

---

## परिचय और अवलोकन {: #introduction-and-overview }

यह गाइड digna प्लेटफ़ॉर्म के साथ Single Sign-On (SSO) को OpenID Connect (OIDC) का उपयोग करके एकीकृत करने के चरण-दर-चरण निर्देश प्रदान करता है।

### SSO क्या है?

Single Sign-On उपयोगकर्ताओं को बाहरी identity providers के माध्यम से उनके एंटरप्राइज़ प्रमाण-पत्रों का उपयोग करके सुरक्षित रूप से digna में लॉगिन करने की अनुमति देता है। उपयोगकर्ता अलग digna पासवर्ड प्रबंधित करने के बजाय अपने कॉर्पोरेट क्रेडेंशियल्स का उपयोग कर सकते हैं।

### यह कैसे काम करता है

digna में SSO OIDC प्रोटोकॉल का उपयोग करके लागू किया गया है। कई identity providers को समानांतर में कॉन्फ़िगर किया जा सकता है — इसके लिए दो मुख्य कॉन्फ़िगरेशन फ़ाइलों को समायोजित करना होता है:

- **`dashboard_config.toml`** — फ्रंटेंड लॉगिन इंटरफ़ेस नियंत्रित करता है
- **`config.toml`** — बैकएंड OIDC कनेक्शन्स कॉन्फ़िगर करता है

### समर्थित प्रदाता {: #supported-providers-overview }

इस गाइड के उदाहरणों में **Microsoft** और **Google** का उपयोग किया गया है, लेकिन **किसी भी OIDC-अनुकूल प्रदाता** को समान संरचना का पालन करके एकीकृत किया जा सकता है।

---

## प्रदाता गाइड {: #provider-guides }

हर प्रदाता के लिए वही चार मान आवश्यक होते हैं — एक client ID, एक client secret, एक redirect URI और एक discovery URL — लेकिन हर प्रदाता अपने एडमिन कंसोल में इन्हें अलग जगह पर रखता है, और कई के पास कोई-न-कोई विशेष कदम भी होता है जो दूसरों में नहीं होता। नीचे के गाइड उस आधे काम को कवर करते हैं; यह पृष्ठ digna पक्ष को कवर करता है, जो सभी के लिए समान है।

| Provider | Guide | Worth knowing |
|---|---|---|
| **AD FS** | [AD FS के साथ SSO सेटअप करें](adfs_sso_guide.md) | Self-hosted; यहाँ एकमात्र प्रदाता जहाँ आप token सेवा नियंत्रित करते हैं |
| **Auth0** | [Auth0 के साथ SSO सेटअप करें](auth0_sso_guide.md) | Discovery URL प्रति-टेनेंट होता है, और कस्टम डोमेन इसे बदल देते हैं |
| **Google Workspace** | [Google Workspace के साथ SSO सेटअप करें](google_workspace_sso_guide.md) | Consent स्क्रीन प्रकाशित होना चाहिए तभी नॉन-टेस्ट उपयोगकर्ता लॉगिन कर सकते हैं |
| **Keycloak** | [Keycloak के साथ SSO सेटअप करें](keycloak_sso_guide.md) | Self-hosted; discovery URL प्रति-रियल्म होता है |
| **Microsoft Entra ID** | [Microsoft Entra ID के साथ SSO सेटअप करें](microsoft_entra_id_sso_guide.md) | Tenant ID discovery URL में आता है; secrets की समय-सीमा होती है |
| **Okta** | [Okta के साथ SSO सेटअप करें](okta_sso_guide.md) | Authorization server के चयन से discovery URL बदलता है |
| **OneLogin** | [OneLogin के साथ SSO सेटअप करें](onelogin_sso_guide.md) | OIDC ऐप टाइप बनाते समय चुना जाना चाहिए और बाद में बदला नहीं जा सकता |
| **PingOne** | [PingOne के साथ SSO सेटअप करें](pingone_sso_guide.md) | Environment ID discovery URL में आता है |

कोई अन्य OIDC-अनुकूल प्रदाता भी समान तरीके से काम करता है — देखें [Other OIDC Providers](#supported-providers)।

---

## कॉन्फ़िगरेशन चरण {: #configuration-steps }

SSO कॉन्फ़िगरेशन के लिए दो फ़ाइलों को अपडेट करना आवश्यक है। यह अनुभाग प्रत्येक फ़ाइल को कैसे कॉन्फ़िगर किया जाए बताता है।

### कॉन्फ़िगरेशन फ़ाइलों का अवलोकन

| फ़ाइल | स्थान | उद्देश्य |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | फ्रंटेंड लॉगिन इंटरफ़ेस |
| **config.toml** | `/config.toml` | बैकएंड OIDC कनेक्शन्स |

SSO ठीक से काम करने के लिए दोनों फ़ाइलों को कॉन्फ़िगर करना आवश्यक है।

---

## डैशबोर्ड कॉन्फ़िगरेशन {: #dashboard-configuration }

### फ़ाइल स्थान

```
dashboard/dashboard_config.toml
```

### चरण 1: OIDC प्रदाताओं को जोड़ें

प्रत्येक identity provider के लिए `[[login.oidc]]` ऐरे के तहत एंट्री जोड़ें जिसे आप समर्थन करना चाहते हैं।

**Microsoft और Google के साथ उदाहरण:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### चरण 2: लॉगिन विकल्प कॉन्फ़िगर करें

निर्दिष्ट करें कि पासवर्ड-आधारित लॉगिन की अनुमति दी जानी चाहिए या नहीं:

```toml
[login]
usePassword = true
```

### कॉन्फ़िगरेशन पैरामीटर

#### `[[login.oidc]]` अनुभाग

| पैरामीटर | प्रकार | आवश्यक | विवरण |
|---|---|---|---|
| `key` | string | हाँ | OIDC कनेक्शन के लिए यूनिक पहचानकर्ता (यह config.toml में key से मेल खाना चाहिए) |
| `label` | string | हाँ | लॉगिन बटन पर दिखने वाला टेक्स्ट (उदा., "Login with Microsoft") |

#### `[login]` अनुभाग

| पैरामीटर | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `usePassword` | boolean | false | SSO के अलावा पासवर्ड-आधारित लॉगिन की अनुमति दें |

### usePassword को समझना

**यदि `usePassword = true`:**
- लॉगिन स्क्रीन पर SSO बटन दिखेंगे (उदा., "Login with Microsoft")
- लॉगिन स्क्रीन पर username और password फ़ील्ड भी दिखेंगे
- उपयोगकर्ता किसी भी विधि से प्रमाणीकृत कर सकते हैं
- हाइब्रिड सेटअप की अनुमति देता है जहाँ कुछ उपयोगकर्ता SSO और अन्य पासवर्ड उपयोग करते हैं

**यदि `usePassword = false` (या छोड़ दिया गया):**
- लॉगिन स्क्रीन केवल SSO बटनों को दिखाती है
- कोई username/password फ़ील्ड नहीं दिखेगा
- केवल OIDC प्रमाणिकरण उपलब्ध होगा

!!! tip "सुझाव"

    पासवर्ड-आधारित लॉगिन केवल उन उपयोगकर्ताओं के लिए उपलब्ध है जिन्हें `digna user add` कमांड या डैशबोर्ड के माध्यम से पासवर्ड के साथ बनाया गया था।

### पूर्ण उदाहरण

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

## बैकएंड कॉन्फ़िगरेशन {: #backend-configuration }

### फ़ाइल स्थान

```
/config.toml
```

(Root digna installation directory)

### चरण 1: OIDC प्रदाता अनुभाग जोड़ें

प्रत्येक प्रदाता के लिए एक समर्पित `[oidc.<key>]` अनुभाग होना चाहिए। key वह ही होना चाहिए जो `dashboard_config.toml` में परिभाषित किया गया है।

### Microsoft कॉन्फ़िगरेशन

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google कॉन्फ़िगरेशन

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### कॉन्फ़िगरेशन पैरामीटर

| पैरामीटर | प्रकार | आवश्यक | विवरण | उदाहरण |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | हाँ | identity provider से प्राप्त Client ID | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | हाँ | identity provider से प्राप्त Client Secret | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | हाँ | प्रमाणीकरण के बाद callback URL | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | हाँ | OIDC कॉन्फ़िगरेशन endpoint | `https://login.microsoftonline.com/...` |

!!! warning "महत्वपूर्ण"

    प्लेसहोल्डर मानों (`<client_id>`, `<client_secret>`, `<tenant_id>`) को अपने identity provider के developer portal से वास्तविक क्रेडेंशियल्स से बदलें।

### Redirect URI

Redirect URI आपकी identity provider कॉन्फ़िगरेशन में वही होना चाहिए:

```
http://localhost:5173/oidc/callback
```

यदि digna किसी वैकल्पिक डोमेन पर होस्ट है, तो उसे उसी के अनुसार अपडेट करें:
- लोकल: `http://localhost:5173/oidc/callback`
- प्रोडक्शन: `https://digna.yourdomain.com/oidc/callback`

### पूर्ण उदाहरण

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

## लॉगिन परीक्षण {: #testing-login }

कॉन्फ़िगरेशन पूरा करने के बाद, सुनिश्चित करें कि SSO सही ढंग से कार्य कर रहा है।

### परीक्षण से पहले की जाँच सूची

परीक्षण से पहले सुनिश्चित करें:

- [ ] `dashboard_config.toml` में OIDC प्रदाताओं को अपडेट किया गया है
- [ ] `config.toml` में OIDC क्रेडेंशियल्स अपडेट हुए हैं
- [ ] दोनों फ़ाइलें सेव की गई हैं
- [ ] क्रेडेंशियल्स सही हैं (client ID, client secret)
- [ ] Redirect URI आपकी डिप्लॉयमेंट URL से मेल खाता है
- [ ] Identity provider एप्लिकेशन में redirect URI कॉन्फ़िगर किया गया है

### परीक्षण चरण

#### चरण 1: सर्विसेज़ पुनरारम्भ करें

परिवर्तनों को लागू करने के लिए digna बैकएंड और वेब सर्वर को पुनरारम्भ करें।

**यदि Windows पर सर्विस के रूप में चल रहा है:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**यदि Linux या macOS पर सर्विस के रूप में चल रहा है:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**यदि मैन्युअली चला रहे हैं:**
```bash
digna serve --address localhost --port 8082
```

**वेब सर्वर भी पुनरारम्भ करें** — Windows पर IIS या Tomcat, Linux/macOS पर nginx या Apache।

#### चरण 2: डैशबोर्ड खोलें

अपने ब्राउज़र में digna डैशबोर्ड खोलें:

```
http://localhost:5173
```

(या आपकी कॉन्फ़िगर्ड डैशबोर्ड URL)

#### चरण 3: लॉगिन बटनों की जाँच करें

जाँचें कि प्रत्येक कॉन्फ़िगर्ड प्रदाता के लिए लॉगिन बटन दिखाई दे रहे हैं:

- "Login with Microsoft" बटन दिखाई देना चाहिए
- "Login with Google" बटन दिखाई देना चाहिए
- (यदि usePassword = true) username/password फ़ील्ड दिखाई देने चाहिए

यदि बटन दिखाई नहीं देते:
- जाँचें कि `dashboard_config.toml` सेव हुआ है
- जाँचें कि डैशबोर्ड सर्विस पुनरारम्भ हुई है
- ब्राउज़र कंसोल (F12) में त्रुटियों की जाँच करें

#### चरण 4: SSO लॉगिन का परीक्षण करें

किसी एक SSO बटन पर क्लिक करें (उदा., "Login with Microsoft"):

1. आपको identity provider के लॉगिन पेज पर रिडायरेक्ट किया जाना चाहिए
2. अपने एंटरप्राइज़ क्रेडेंशियल्स से लॉगिन करें
3. आपको digna पर वापस रिडायरेक्ट किया जाना चाहिए
4. आपको digna में लॉग इन होना चाहिए

#### चरण 5: उपयोगकर्ता निर्माण सत्यापित करें

सफल SSO लॉगिन के बाद:

- उपयोगकर्ता स्वचालित रूप से digna में बनाया जाना चाहिए
- उपयोगकर्ता लॉग इन होना चाहिए
- उपयोगकर्ता प्रोफ़ाइल में आपके identity provider क्रेडेंशियल्स दिखाई देने चाहिए
- आपको digna डैशबोर्ड दिखाई देना चाहिए

#### चरण 6: पासवर्ड लॉगिन का परीक्षण (यदि सक्षम)

यदि `usePassword = true`:

1. digna से लॉग आउट करें
2. लॉगिन पेज पर username और password दर्ज करें
3. आपको पासवर्ड क्रेडेंशियल्स के साथ लॉग इन कर पाने में सक्षम होना चाहिए

---

## समस्या निवारण {: #troubleshooting }

### लॉगिन बटन दिखाई नहीं दे रहे

**लक्षण:**
- लॉगिन पेज पर OIDC लॉगिन बटन दिखाई नहीं दे रहे
- केवल पासवर्ड फ़ील्ड दिख रहे हैं (यदि usePassword = true)

**कारण और समाधान:**
1. जाँचें कि `dashboard_config.toml` `dashboard/` डायरेक्टरी में है
2. सत्यापित करें कि `[[login.oidc]]` सेक्शन्स सही सिन्टैक्स के साथ मौजूद हैं
3. डैशबोर्ड सर्विस पुनरारम्भ करें
4. ब्राउज़र कैश क्लियर करें (Ctrl+Shift+Delete या Cmd+Shift+Delete)
5. ब्राउज़र कंसोल (F12 → Console tab) में त्रुटियाँ जाँचें

---

### Redirect URI mismatch त्रुटि

**लक्षण:**
- SSO बटन पर क्लिक करने के बाद "redirect_uri mismatch" के बारे में त्रुटि
- "The redirect URI is not registered" त्रुटि

**कारण और समाधान:**
1. सत्यापित करें कि `DIGNA_OIDC_REDIRECT_URI` `config.toml` में सही है
2. सुनिश्चित करें redirect URI identity provider settings में रजिस्टर है
3. सुनिश्चित करें दोनों URLs समान हैं (protocol, domain, path सहित)
4. redirect URI में टाइपो न हों
5. यदि HTTPS का उपयोग कर रहे हैं, तो सर्टिफिकेट मान्य है यह जाँचें

---

### Invalid Client Credentials त्रुटि

**लक्षण:**
- "Invalid client ID or secret" त्रुटि
- प्रमाणिकरण क्रेडेंशियल त्रुटि के साथ विफल

**कारण और समाधान:**
1. सत्यापित करें कि `DIGNA_OIDC_CLIENT_ID` और `DIGNA_OIDC_CLIENT_SECRET` सही हैं
2. सुनिश्चित करें कि कोई अतिरिक्त स्पेस या अनचाहे कैरेक्टर नहीं हैं
3. जाँचें कि क्रेडेंशियल्स expire या revoke नहीं हुए हैं
4. कॉन्फ़िग अपडेट करने के बाद बैकएंड सर्विस पुनरारम्भ करें
5. identity provider कंसोल में पुष्टि करें कि क्रेडेंशियल्स सक्रिय हैं

---

### लॉगिन अटक जाता है या टाइमआउट हो जाता है

**लक्षण:**
- SSO बटन पर क्लिक करने पर कुछ नहीं होता
- कुछ सेकंड बाद टाइमआउट हो जाता है
- ब्राउज़र "Failed to connect" जैसा संदेश दिखाता है

**कारण और समाधान:**
1. सुनिश्चित करें digna बैकएंड चल रहा है: `digna repo check`
2. identity provider तक नेटवर्क कनेक्टिविटी जाँचें
3. सत्यापित करें कि `DIGNA_OIDC_CONFIGURATION_URL` सुलभ है
4. फ़ायरवॉल नियम बाहर HTTPS कनेक्शन्स की अनुमति दें
5. सत्यापित करें कि बैकएंड और डैशबोर्ड एक-दूसरे तक पहुँच सकते हैं

---

### उपयोगकर्ता स्वचालित रूप से नहीं बन रहे

**लक्षण:**
- SSO लॉगिन सफल होता है पर उपयोगकर्ता digna में नहीं बनते
- SSO लॉगिन के बाद अनुमति त्रुटि मिलती है

**कारण और समाधान:**
1. सत्यापित करें कि OIDC कॉन्फ़िगरेशन सही है
2. उपयोगकर्ता अनुमतियाँ सही तरीके से सेट हैं यह जाँचें
3. digna लॉग्स में त्रुटि संदेशों की समीक्षा करें
4. बैकएंड सर्विस पुनरारम्भ करें
5. समस्या बनी रहने पर support@digna.ai से संपर्क करें

---

## समर्थित प्रदाता {: #supported-providers }

### परीक्षण और समर्थित

नीचे दिए गए OIDC प्रदाताओं का परीक्षण किया गया है और ज्ञात रूप से काम करते हैं:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [AD FS के साथ SSO सेटअप करें](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Auth0 के साथ SSO सेटअप करें](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Workspace के साथ SSO सेटअप करें](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Keycloak के साथ SSO सेटअप करें](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Entra ID के साथ SSO सेटअप करें](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta के साथ SSO सेटअप करें](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [OneLogin के साथ SSO सेटअप करें](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [PingOne के साथ SSO सेटअप करें](pingone_sso_guide.md) |

### अन्य OIDC प्रदाता

कोई भी प्रदाता जो OpenID Connect का समर्थन करता है उसे एकीकृत किया जा सकता है। आवश्यक जानकारी:

- Client ID
- Client secret
- OpenID कॉन्फ़िगरेशन URL (आमतौर पर `/.well-known/openid-configuration` पर)
- समर्थित scopes (सामान्यतः `openid profile email`)

किसी विशिष्ट प्रदाता को एकीकृत करने में मदद चाहिए तो support@digna.ai से संपर्क करें।

---

## सर्वोत्तम प्रथाएँ

**करें:**
- प्रोडक्शन में HTTPS का उपयोग करें (HTTP का नहीं)
- client secrets को सुरक्षित रूप से संग्रहित करें (यदि संभव हो तो environment variables का उपयोग करें)
- समय-समय पर secrets को रोटेट करें
- पहले गैर-प्रोडक्शन वातावरण में परीक्षण करें
- जिन प्रदाताओं को कॉन्फ़िगर किया गया है उनका दस्तावेज़ बनाएँ
- अनियमित गतिविधि के लिए लॉगिन लॉग्स की निगरानी करें
- identity provider कॉन्फ़िगरेशन को digna कॉन्फ़िग के साथ सिंक में रखें

**न करें:**
- client secrets को version control में स्टोर न करें
- प्रोडक्शन में HTTP redirect URIs का उपयोग न करें
- एक ही key के साथ कई प्रदाताओं को कॉन्फ़िगर न करें
- प्रोडक्शन में डिफ़ॉल्ट/टेस्ट क्रेडेंशियल्स न छोड़ें
- क्रेडेंशियल्स वाले कॉन्फ़िग फाइल्स को एक्सपोज़ न करें
- डेवलपमेंट और प्रोडक्शन क्रेडेंशियल्स को मिलाएं नहीं

---

## सहायता

क्या SSO कॉन्फ़िगरेशन में मदद चाहिए?

- **ईमेल:** support@digna.ai
- **डॉक्यूमेंटेशन:** https://docs.digna.ai
- **वेबसाइट:** https://www.digna.ai

---

**अंतिम अपडेट:** August 30, 2026  
**रिलीज़:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**