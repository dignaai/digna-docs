# Microsoft Entra ID के साथ SSO सेट अप करें

Microsoft Entra ID (पूर्व में Azure Active Directory) एक पूर्ण OIDC-अनुपालन प्रदाता है, इसलिए digna इसे मानक discovery endpoint के माध्यम से एकीकृत करता है।

यह गाइड केवल **Entra ID पक्ष** को कवर करता: एप्लिकेशन पंजीकरण और वे चार मान एकत्र करना जिनकी digna को आवश्यकता है। digna पक्ष — `dashboard_config.toml`, परीक्षण और समस्या निवारण — हर प्रदाता के लिए समान है और [Single Sign-On Overview](overview.md) में वर्णित है।

---

## शुरू करने से पहले

| Requirement | Notes |
|---|---|
| **Entra ID role** | Application Administrator, Cloud Application Administrator, or Global Administrator |
| **digna redirect URI** | लॉगिन के बाद उपयोगकर्ता जहाँ लौटते हैं उस URL का उदाहरण, जैसे `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | वह directory जहाँ आपके उपयोगकर्ता साइन इन करते हैं |

---

## चरण 1: एप्लिकेशन पंजीकृत करें

1. [Microsoft Entra एडमिन सेंटर](https://entra.microsoft.com) में साइन इन करें
2. Identity → Applications → App registrations पर जाएँ
3. **New registration** पर क्लिक करें
4. कॉन्फ़िगर करें:
   - **Name**: `digna` (सहमति स्क्रीन पर उपयोगकर्ताओं को दिखाया जाता है)
   - **Supported account types**: एक single-tenant डिप्लॉयमेंट के लिए *Accounts in this organizational directory only*
5. **Redirect URI** के अंतर्गत प्लेटफ़ॉर्म **Web** चुनें और अपना digna callback URL दर्ज करें:

```
https://digna.yourdomain.com/oidc/callback
```

6. **Register** पर क्लिक करें

!!! warning "महत्वपूर्ण"

    प्लेटफ़ॉर्म **Web** होना चाहिए, *Single-page application* नहीं। digna बैकएंड से authorization code का आदान-प्रदान एक client secret का उपयोग करके करता है, जो SPA प्लेटफ़ॉर्म प्रकार अनुमति नहीं देता।

---

## चरण 2: Client और Tenant IDs प्राप्त करें

एप्लिकेशन के **Overview** पृष्ठ पर, कॉपी करें:

- **Application (client) ID** → यह `DIGNA_OIDC_CLIENT_ID` बन जाता है
- **Directory (tenant) ID** → discovery URL में जाएगा

---

## चरण 3: एक Client Secret बनाएं

1. **Certificates & secrets → Client secrets** पर जाएँ
2. **New client secret** पर क्लिक करें
3. एक विवरण दर्ज करें और एक्सपायरी चुनें
4. **Add** पर क्लिक करें
5. तुरंत **Value** कॉलम को कॉपी करें

!!! warning "Value कॉपी करें, Secret ID नहीं"

    **Value** केवल एक बार इस पृष्ठ पर दिखाया जाता है और बाद में पुनः प्राप्त नहीं किया जा सकता। इसके बगल में दिखने वाला **Secret ID** मिलते-जुलते दिखता है पर वह secret नहीं है — इसे उपयोग करने पर लॉगिन पर `invalid_client` त्रुटि आती है। यदि आप कॉपी करने से पहले पृष्ठ से चले जाते हैं, तो secret को हटाकर नया बनाएं।

!!! tip "टिप"

    Entra ID secret की lifetime को 24 महीनों तक सीमित करता है, इसलिए हर SSO इंटीग्रेशन की एक समाप्ति तिथि होती है। इसे कहीं नोट कर लें जहाँ आप देख सकें — एक एक्सपायर हो चुका secret एक ही बार में हर उपयोगकर्ता के लिए SSO बंद कर देता है, और लॉगिन पृष्ठ पर कोई चेतावनी नहीं मिलती।

---

## चरण 4: API अनुमतियों की पुष्टि करें

1. **API permissions** पर जाएँ
2. पुष्टि करें कि **Microsoft Graph → User.Read** (delegated) मौजूद है — यह डिफ़ॉल्ट रूप से जोड़ा जाता है

digna द्वारा अनुरोधित `openid`, `profile` और `email` स्कोप्स मानक OIDC सेट का हिस्सा हैं और इनके लिए अलग से ग्रांट की आवश्यकता नहीं होती। यदि आपका टेनेंट सभी एप्लिकेशनों के लिए admin consent की आवश्यकता रखता है, तो **Grant admin consent for &lt;tenant&gt;** पर क्लिक करें।

---

## चरण 5: Discovery URL बनाएं

Step 2 से **Directory (tenant) ID** प्रतिस्थापित करें:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "v2.0 Endpoint का उपयोग करें"

    `/v2.0/` segment मायने रखता है। v1.0 endpoint `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` पुराने फ़ॉर्मैट में टोकन जारी करता है और वह मानक OIDC claims नहीं लौटाता जिसकी digna अपेक्षा करता है।

जारी रखने से पहले ब्राउज़र में URL खोलें। एक JSON दस्तावेज़ पुष्टि करता है कि tenant ID सही है।

---

## चरण 6: digna को कॉन्फ़िगर करें

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"
```

### `config.toml`

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

दोनों फाइलों में `key` मेल खाना चाहिए — यहाँ `microsoft` है।

---

## चरण 7: परीक्षण करें

बैकएंड और वेब सर्वर को पुनः प्रारंभ करें, फिर डैशबोर्ड खोलें। पूरी चेकलिस्ट के लिए देखें [Testing Login](overview.md#testing-login)।

---

## Entra ID समस्या निवारण

### AADSTS50011: Redirect URI Mismatch

`DIGNA_OIDC_REDIRECT_URI` में दिया गया URI Step 1 में रजिस्टर किए गए URI से अलग है। Entra ID पूरे स्ट्रिंग की तुलना करता है, इसलिए एक trailing slash, `http` बनाम `https`, या कोई अलग पोर्ट सभी असंगति माने जाते हैं। **Authentication → Web → Redirect URIs** की जाँच करें।

### AADSTS7000215: Invalid Client Secret

या तो **Secret ID** को कॉपी किया गया था बजाय **Value** के, या secret की अवधि समाप्त हो चुकी है। एक नया secret बनाकर Value कॉलम को कॉपी करें।

### AADSTS650057: Invalid Resource

एप्लिकेशन रजिस्ट्रेशन हटाया गया है या discovery URL में दिए गए टेनेंट से अलग टेनेंट का है। Overview पृष्ठ पर Directory (tenant) ID की पुष्टि करें।

### उपयोगकर्ता लॉग इन करते हैं लेकिन कुछ भी नहीं होता

यदि टेनेंट admin consent की आवश्यकता रखता है और उसे प्रदान नहीं किया गया है, तो redirect बिना उपयोगी टोकन के लौटता है। **API permissions** के तहत admin consent प्रदान करें।

---

## संदर्भ

- [Single Sign-On Overview](overview.md) — कॉन्फ़िगरेशन संदर्भ, परीक्षण और सामान्य समस्या निवारण
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)