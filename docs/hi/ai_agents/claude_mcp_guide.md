---
title: Claude – MCP के माध्यम से Claude को digna से कनेक्ट करें | digna दस्तावेज़
description: digna MCP Server के माध्यम से Claude को digna से कनेक्ट करें — कमांड लाइन या साझा .mcp.json से Claude Code, लोकल ब्रिज के साथ Claude Desktop, और claude.ai में कस्टम कनेक्टर, Authorization हेडर में API कुंजी के साथ।
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, claude.ai कस्टम कनेक्टर, digna MCP server, mcp-remote, Authorization Bearer, digna API कुंजी
---

# Claude को digna से कनेक्ट करें

यह गाइड Claude को **digna MCP Server** से कनेक्ट करती है। आपको अपने *digna* इंस्टॉलेशन का MCP एंडपॉइंट और
एक API कुंजी चाहिए, जैसा कि [AI एजेंट अवलोकन](overview.md) में बताया गया है।

उदाहरणों में एंडपॉइंट के रूप में `https://digna.example.com/mcp` का उपयोग किया गया है। इसे अपने एंडपॉइंट से
बदलें।

## कनेक्ट करने का तरीका चुनें {: #choose-how-to-connect }

| Claude उत्पाद | कहाँ से कनेक्ट होता है | आपके नेटवर्क के भीतर *digna* के साथ काम करता है |
|---|---|---|
| [Claude Code](#claude-code) | आपकी मशीन | हाँ |
| [लोकल ब्रिज के साथ Claude Desktop](#claude-desktop-with-a-local-bridge) | आपकी मशीन | हाँ |
| claude.ai, Claude Desktop और Claude मोबाइल में [कस्टम कनेक्टर](#custom-connector) | Anthropic का क्लाउड | नहीं। एंडपॉइंट इंटरनेट से पहुँच योग्य होना चाहिए |

आपकी कंपनी के नेटवर्क के भीतर चलने वाले *digna* इंस्टॉलेशन के लिए Claude Code या लोकल ब्रिज के साथ Claude
Desktop का उपयोग करें।

---

## Claude Code {: #claude-code }

### 1. सर्वर जोड़ें {: #1-add-the-server }

API कुंजी को एक परिवेश चर में रखें, फिर सर्वर जोड़ें:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

कमांड चलाते समय आपका शेल `$DIGNA_API_KEY` भर देता है, इसलिए Claude Code कुंजी को अपने कॉन्फ़िगरेशन में
संग्रहीत करता है।

`--scope` तय करता है कि सर्वर कहाँ उपलब्ध है:

| स्कोप | किसके लिए उपलब्ध |
|---|---|
| `local` (डिफ़ॉल्ट) | आपके लिए, केवल वर्तमान प्रोजेक्ट में |
| `user` | आपके लिए, हर प्रोजेक्ट में |
| `project` | प्रोजेक्ट में काम करने वाले हर व्यक्ति के लिए, प्रोजेक्ट में `.mcp.json` फ़ाइल के माध्यम से |

### 2. सर्वर को अपनी टीम के साथ साझा करें (वैकल्पिक) {: #2-share-the-server-with-your-team }

किसी प्रोजेक्ट में सभी को एक ही सर्वर देने के लिए, प्रोजेक्ट रूट में `.mcp.json` फ़ाइल जोड़ें। फ़ाइल में
कुंजी न लिखें। Claude Code हर व्यक्ति के अपने परिवेश से `${DIGNA_API_KEY}` भरता है:

```json
{
  "mcpServers": {
    "digna": {
      "type": "http",
      "url": "https://digna.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${DIGNA_API_KEY}"
      }
    }
  }
}
```

हर व्यक्ति `DIGNA_API_KEY` को अपनी कुंजी पर सेट करता है। जब Claude Code पहली बार यह फ़ाइल पाता है, तो वह
पूछता है कि इसमें दिए गए सर्वरों का उपयोग करना है या नहीं।

### 3. कनेक्शन सत्यापित करें {: #3-verify-the-connection }

अपने शेल से:

```bash
claude mcp list
```

`digna` सर्वर पर `✔ Connected` दिखना चाहिए। Claude Code सत्र के भीतर, सर्वर और उसके टूल देखने के लिए `/mcp`
चलाएँ।

---

## लोकल ब्रिज के साथ Claude Desktop {: #claude-desktop-with-a-local-bridge }

Claude Desktop की कॉन्फ़िगरेशन फ़ाइल आपकी मशीन पर लोकल MCP सर्वर शुरू करती है। एक छोटा ब्रिज, ओपन-सोर्स
[`mcp-remote`](https://github.com/geelen/mcp-remote) पैकेज, वहाँ चलता है और हर अनुरोध को आपकी API कुंजी के
साथ *digna* एंडपॉइंट तक फ़ॉरवर्ड करता है। क्योंकि ब्रिज आपकी मशीन पर चलता है, यह आपकी कंपनी के नेटवर्क के
भीतर *digna* के साथ काम करता है।

!!! note "एक समुदाय पैकेज"

    `mcp-remote` का रखरखाव उसका ओपन-सोर्स समुदाय करता है, Anthropic या digna नहीं। उपयोग करने से पहले जाँच लें
    कि आपका संगठन इसकी अनुमति देता है।

### 1. Node.js इंस्टॉल करें {: #1-install-nodejs }

ब्रिज को [Node.js](https://nodejs.org) 18 या उसके बाद का संस्करण चाहिए। Claude Desktop आपके सिस्टम पर
इंस्टॉल किए गए Node.js संस्करण का उपयोग करता है। इसे इस कमांड से जाँचें:

```bash
node --version
```

### 2. कॉन्फ़िगरेशन फ़ाइल संपादित करें {: #2-edit-the-configuration-file }

`claude_desktop_config.json` खोलें:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

`digna` सर्वर जोड़ें। यदि फ़ाइल में पहले से `mcpServers` अनुभाग है, तो `digna` प्रविष्टि उसी में जोड़ें:

```json
{
  "mcpServers": {
    "digna": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://digna.example.com/mcp",
        "--transport",
        "http-only",
        "--header",
        "Authorization:${AUTH_HEADER}"
      ],
      "env": {
        "AUTH_HEADER": "Bearer <api key>"
      }
    }
  }
}
```

!!! warning "हेडर को ठीक वैसा ही रखें जैसा दिखाया गया है"

    `Authorization:${AUTH_HEADER}` बिना स्पेस के लिखें, और `Bearer <api key>` को `env` में रखें। Windows पर
    Claude Desktop `args` के भीतर स्पेस को एस्केप नहीं करता, इसलिए वहाँ एक स्पेस हेडर को तोड़ देता है।

### 3. Claude Desktop को पुनः आरंभ करें {: #3-restart-claude-desktop }

Claude Desktop को पूरी तरह बंद करें और फिर से शुरू करें। नई चैट में **+** पर क्लिक करें और **Connectors**
खोलें: `digna` सूची में होना चाहिए और चालू होना चाहिए।

---

## कस्टम कनेक्टर {: #custom-connector }

कस्टम कनेक्टर बिना किसी लोकल सेटअप के *digna* को claude.ai, Claude Desktop और Claude मोबाइल ऐप में उपलब्ध
कराता है। Anthropic का क्लाउड एंडपॉइंट से कनेक्ट होता है, इसलिए यह केवल तभी काम करता है जब:

- *digna* एंडपॉइंट इंटरनेट से HTTPS पर पहुँच योग्य हो
- आपके Claude संगठन के **Add custom connector** डायलॉग में **Request headers** विकल्प हो। Anthropic इसे
  सीमित संगठनों को बीटा के रूप में देता है

!!! warning "आपके नेटवर्क के भीतर digna के लिए नहीं"

    Claude की MCP टनल, जो निजी नेटवर्क के भीतर के सर्वरों तक पहुँचती हैं, MCP सर्वर पर OAuth की माँग करती
    हैं। digna MCP Server API कुंजियों से प्रमाणीकरण करता है, इसलिए टनल का उपयोग नहीं किया जा सकता। इसके बजाय
    [Claude Code](#claude-code) या [लोकल ब्रिज के साथ Claude Desktop](#claude-desktop-with-a-local-bridge)
    का उपयोग करें।

### 1. कनेक्टर सेटिंग्स खोलें {: #1-open-the-connector-settings }

- **Free, Pro, Max और Ultra प्लान**: **Customize > Connectors** पर जाएँ और **Add custom connector** पर
  क्लिक करें।
- **Team और Enterprise प्लान**: एक Owner **Organization settings > Connectors** पर जाता है, **Add** पर,
  फिर **Custom** पर क्लिक करता है, और प्रकार पूछे जाने पर **Web** चुनता है।

### 2. कनेक्टर विवरण दर्ज करें {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: हेडर नाम के रूप में `authorization` चुनें, मान के रूप में `Bearer <api key>` दर्ज
   करें, जिसमें शब्द `Bearer` और स्पेस शामिल हों, और इसे **Required** चिह्नित करें।
4. **Add** पर क्लिक करें।

!!! warning "सभी एक ही कुंजी साझा करते हैं"

    कनेक्टर का उपयोग करने वाला हर सदस्य एक ही API कुंजी के साथ, और इसलिए एक ही *digna* उपयोगकर्ता के साथ काम
    करता है। कनेक्टर के लिए एक समर्पित *digna* उपयोगकर्ता बनाएँ और उसे केवल वे प्रोजेक्ट और भूमिकाएँ दें जो
    सभी के पास हो सकती हैं, जैसे reader भूमिका।

Team और Enterprise प्लान पर, सदस्य फिर **Customize > Connectors** के अंतर्गत कनेक्ट होते हैं, जहाँ कनेक्टर
पर **Custom** लेबल होता है।

Claude किसी मौजूदा कनेक्टर का हेडर नहीं बदल सकता। नई कुंजी का उपयोग करने के लिए कनेक्टर हटाएँ और उसे फिर से
जोड़ें।

---

## Claude समस्या निवारण {: #troubleshooting-claude }

### claude mcp list में Failed to connect दिखता है

कारण देखने के लिए `claude mcp get digna` चलाएँ। `401` का अर्थ है कि कुंजी अस्वीकार कर दी गई; देखें
[401 Unauthorized](overview.md#troubleshooting)। Claude Code कुंजी की शुरुआत या अंत में स्पेस या लाइन ब्रेक
के बारे में भी चेतावनी देता है, जो अक्सर कॉपी करते समय आ जाते हैं।

### Claude Desktop में digna दिखाई नहीं देता

- जाँचें कि Node.js 18 या उसके बाद का संस्करण इंस्टॉल है: `node --version`।
- जाँचें कि `claude_desktop_config.json` मान्य JSON है। एक छूटा हुआ कॉमा फ़ाइल के हर सर्वर को लोड होने से रोक
  देता है।
- Claude Desktop को पूरी तरह बंद करें, केवल विंडो नहीं, और फिर से शुरू करें।

### कस्टम कनेक्टर सर्वर तक नहीं पहुँच पाता

Anthropic का क्लाउड एंडपॉइंट तक नहीं पहुँच पाता। जाँचें कि वह मान्य प्रमाणपत्र के साथ इंटरनेट से HTTPS पर
पहुँच योग्य है, या इसके बजाय [Claude Code](#claude-code) के माध्यम से कनेक्ट करें।

---

## यह भी देखें {: #see-also }

- [AI एजेंट अवलोकन](overview.md): एंडपॉइंट, API कुंजी, सुरक्षा और सामान्य समस्या निवारण
- [Gemini](gemini_mcp_guide.md): Antigravity या Gemini CLI कनेक्ट करें
- [digna Agentic](../platform/agentic/Introduction.md): AI एजेंट *digna* के साथ क्या कर सकते हैं
