# Gemini को digna से कनेक्ट करें

यह गाइड Google के Gemini टूल को **digna MCP Server** से कनेक्ट करती है। आपको अपने *digna* इंस्टॉलेशन का MCP
एंडपॉइंट और एक API कुंजी चाहिए, जैसा कि [AI एजेंट अवलोकन](overview.md) में बताया गया है।

उदाहरणों में एंडपॉइंट के रूप में `https://digna.example.com/mcp` का उपयोग किया गया है। इसे अपने एंडपॉइंट से
बदलें।

## अपना टूल चुनें {: #choose-your-tool }

| टूल | किसके लिए | कॉन्फ़िगरेशन |
|---|---|---|
| [Antigravity](#antigravity) CLI, IDE और ऐप | Google के एजेंट टूल। जून 2026 में व्यक्तिगत Google खातों के लिए Antigravity CLI ने Gemini CLI की जगह ली | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | Gemini Code Assist Standard और Enterprise लाइसेंस, और सशुल्क Gemini API कुंजियाँ | `settings.json` या `gemini mcp add` |
| Gemini Enterprise ऐप | — | समर्थित नहीं। इसका कस्टम MCP कनेक्टर OAuth या Google Cloud सेवा खाते से साइन इन करता है, जबकि digna MCP Server API कुंजियों से प्रमाणीकरण करता है |

ये सभी टूल उसी मशीन से कनेक्ट होते हैं जिस पर वे चलते हैं, इसलिए वे आपकी कंपनी के नेटवर्क के भीतर *digna*
के साथ तब तक काम करते हैं जब तक वह मशीन एंडपॉइंट तक पहुँच सकती है।

---

## Antigravity {: #antigravity }

Antigravity अपने MCP सर्वर `mcp_config.json` से पढ़ता है, जिसे CLI, IDE और ऐप साझा करते हैं।

### 1. mcp_config.json खोलें {: #1-open-mcp-config-json }

| स्कोप | फ़ाइल |
|---|---|
| आपके सभी प्रोजेक्ट | `~/.gemini/config/mcp_config.json` |
| एक वर्कस्पेस | वर्कस्पेस में `.agents/mcp_config.json` |

उपयोग में आ रही फ़ाइल खोलने के लिए:

- **CLI**: `/mcp` टाइप करें और MCP मैनेजर खोलने के लिए ++enter++ दबाएँ।
- **IDE**: एजेंट साइड पैनल में **…** मेनू खोलें, **MCP Servers** चुनें, फिर **Manage MCP Servers**, फिर
  **View raw config**।
- **ऐप**: **Customizations** > **Installed** > **MCP Servers** पर जाएँ और **Copy Config File Path** का
  उपयोग करें।

### 2. digna सर्वर जोड़ें {: #2-add-the-digna-server }

`digna` प्रविष्टि जोड़ें। यदि फ़ाइल में पहले से `mcpServers` अनुभाग है, तो उसे वहीं जोड़ें:

```json
{
  "mcpServers": {
    "digna": {
      "serverUrl": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

Antigravity रिमोट सर्वरों तक केवल streamable HTTP पर पहुँचता है, जिसका उपयोग digna MCP Server करता है।
एंडपॉइंट को `serverUrl` के रूप में लिखें; Gemini CLI की `httpUrl` कुंजी समर्थित नहीं है।

### 3. कनेक्शन सत्यापित करें {: #3-verify-the-connection }

CLI में `/mcp` टाइप करें: MCP मैनेजर `digna` सर्वर को उसकी स्थिति और टूल के साथ दिखाता है, और कॉन्फ़िगरेशन को
फिर से लोड कर सकता है तथा कनेक्शन लॉग दिखा सकता है। IDE में सर्वर **Manage MCP Servers** के अंतर्गत दिखाई
देता है।

!!! warning "फ़ाइल को सुरक्षित रखें"

    `mcp_config.json` में API कुंजी सादे पाठ में होती है। वर्कस्पेस की `.agents/mcp_config.json` को संस्करण
    नियंत्रण से बाहर रखें, और ग्लोबल फ़ाइल को केवल अपना खाता पढ़ सके, ऐसा रखें।

---

## Gemini CLI {: #gemini-cli }

### 1. सर्वर जोड़ें {: #1-add-the-server }

API कुंजी को एक परिवेश चर में रखें, फिर सर्वर जोड़ें:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

कमांड चलाते समय आपका शेल `$DIGNA_API_KEY` भर देता है, इसलिए Gemini CLI कुंजी को अपनी सेटिंग्स में संग्रहीत
करता है। `--scope user` के बिना सर्वर केवल वर्तमान प्रोजेक्ट में जोड़ा जाता है।

### 2. या settings.json संपादित करें {: #2-or-edit-settings-json }

ऊपर दी गई कमांड `settings.json` में लिखती है। फ़ाइल को स्वयं संपादित करने के लिए:

| स्कोप | फ़ाइल |
|---|---|
| आपके सभी प्रोजेक्ट | `~/.gemini/settings.json` |
| एक प्रोजेक्ट | प्रोजेक्ट में `.gemini/settings.json` |

```json
{
  "mcpServers": {
    "digna": {
      "httpUrl": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <api key>"
      }
    }
  }
}
```

`httpUrl` का उपयोग करें, जो streamable HTTP की कुंजी है। मिलती-जुलती `url` कुंजी पुराना SSE ट्रांसपोर्ट चुनती
है, जो digna MCP Server प्रदान नहीं करता। सर्वर नाम में अंडरस्कोर का उपयोग न करें।

!!! tip "trust बंद रहने दें"

    Gemini CLI हर टूल कॉल से पहले पूछता है, जब तक सर्वर में `"trust": true` न हो। *digna* के लिए `trust` बंद
    रहने दें, ताकि एजेंट आपके कॉन्फ़िगरेशन में जो भी बदलाव करे, उसकी पुष्टि आप करें।

### 3. कनेक्शन सत्यापित करें {: #3-verify-the-connection-gemini-cli }

अपने शेल से:

```bash
gemini mcp list
```

`digna` सर्वर कनेक्टेड के रूप में दिखना चाहिए। Gemini CLI सत्र के भीतर, सर्वर और उसके टूल देखने के लिए `/mcp`
चलाएँ।

---

## Gemini समस्या निवारण {: #troubleshooting-gemini }

### सर्वर डिस्कनेक्टेड दिखता है

- जाँचें कि एंडपॉइंट `/mcp` पर समाप्त होता है और आपकी मशीन से पहुँच योग्य है।
- कुंजी का नाम जाँचें: Antigravity में `serverUrl`, Gemini CLI में `httpUrl`।
- `401` का अर्थ है कि कुंजी अस्वीकार कर दी गई; देखें [401 Unauthorized](overview.md#troubleshooting)।

### मेरे खाते के लिए Gemini CLI अब शुरू नहीं होता

जून 2026 से व्यक्तिगत Google खाते Gemini CLI के बजाय Antigravity CLI का उपयोग करते हैं। `digna` प्रविष्टि को
[Antigravity](#antigravity) के अंतर्गत बताए अनुसार `mcp_config.json` में ले जाएँ, और `httpUrl` का नाम बदलकर
`serverUrl` करें।

---

## यह भी देखें {: #see-also }

- [AI एजेंट अवलोकन](overview.md): एंडपॉइंट, API कुंजी, सुरक्षा और सामान्य समस्या निवारण
- [Claude](claude_mcp_guide.md): Claude Code, Claude Desktop या कस्टम कनेक्टर कनेक्ट करें
- [digna Agentic](../platform/agentic/Introduction.md): AI एजेंट *digna* के साथ क्या कर सकते हैं