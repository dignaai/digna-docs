---
title: Gemini – ربط Antigravity وGemini CLI بـ digna عبر MCP | توثيق digna
description: اربط أدوات Gemini من Google بـ digna عبر digna MCP Server — Antigravity CLI وIDE والتطبيق باستخدام mcp_config.json، وGemini CLI باستخدام settings.json أو gemini mcp add، مع مفتاح API في الترويسة Authorization.
image: /assets/logo_square.png
keywords: Gemini MCP, Antigravity MCP, Antigravity CLI, agy, Gemini CLI MCP, mcp_config.json, digna MCP server, Authorization Bearer, مفتاح API لـ digna
---

# ربط Gemini بـ digna

يربط هذا الدليل أدوات Gemini من Google بـ **digna MCP Server**. تحتاج إلى نقطة نهاية MCP الخاصة بتثبيت *digna*
لديك ومفتاح API، كما هو موضح في [نظرة عامة على وكلاء الذكاء الاصطناعي](overview.md).

تستخدم الأمثلة `https://digna.example.com/mcp` كنقطة نهاية. استبدلها بنقطة النهاية الخاصة بك.

## اختيار الأداة {: #choose-your-tool }

| الأداة | لـ | التهيئة |
|---|---|---|
| [Antigravity](#antigravity) CLI وIDE والتطبيق | أدوات الوكلاء من Google. حلّ Antigravity CLI محل Gemini CLI لحسابات Google الفردية في يونيو 2026 | `mcp_config.json` |
| [Gemini CLI](#gemini-cli) | تراخيص Gemini Code Assist Standard وEnterprise، ومفاتيح Gemini API المدفوعة | `settings.json` أو `gemini mcp add` |
| تطبيق Gemini Enterprise | — | غير مدعوم. يسجّل موصل MCP المخصص فيه الدخول باستخدام OAuth أو حساب خدمة Google Cloud، بينما يصادق digna MCP Server باستخدام مفاتيح API |

تتصل كل هذه الأدوات من الجهاز الذي تعمل عليه، لذا فهي تعمل مع *digna* داخل شبكة شركتك ما دام ذلك الجهاز يستطيع
الوصول إلى نقطة النهاية.

---

## Antigravity {: #antigravity }

يقرأ Antigravity خوادم MCP الخاصة به من `mcp_config.json`، الذي تتشاركه واجهة CLI وبيئة IDE والتطبيق.

### 1. فتح mcp_config.json {: #1-open-mcp-config-json }

| النطاق | الملف |
|---|---|
| كل مشاريعك | `~/.gemini/config/mcp_config.json` |
| مساحة عمل واحدة | `.agents/mcp_config.json` في مساحة العمل |

لفتح الملف المستخدم:

- **CLI**: اكتب `/mcp` واضغط ++enter++ لفتح مدير MCP.
- **IDE**: في اللوحة الجانبية للوكيل، افتح القائمة **…**، واختر **MCP Servers**، ثم **Manage MCP Servers**، ثم
  **View raw config**.
- **التطبيق**: اذهب إلى **Customizations** > **Installed** > **MCP Servers** واستخدم
  **Copy Config File Path**.

### 2. إضافة خادم digna {: #2-add-the-digna-server }

أضف الإدخال `digna`. إذا كان الملف يحتوي بالفعل على قسم `mcpServers`، فأضفه هناك:

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

لا يصل Antigravity إلى الخوادم البعيدة إلا عبر streamable HTTP، وهو ما يستخدمه digna MCP Server. اكتب نقطة النهاية
في `serverUrl`؛ المفتاح `httpUrl` الخاص بـ Gemini CLI غير مدعوم.

### 3. التحقق من الاتصال {: #3-verify-the-connection }

في CLI، اكتب `/mcp`: يعرض مدير MCP الخادم `digna` مع حالته وأدواته، ويمكنه إعادة تحميل التهيئة وعرض سجلات الاتصال.
في IDE، يظهر الخادم تحت **Manage MCP Servers**.

!!! warning "احمِ الملف"

    يحتفظ `mcp_config.json` بمفتاح API كنص عادي. أبقِ ملف مساحة العمل `.agents/mcp_config.json` خارج نظام التحكم
    في الإصدارات، واجعل الملف العام قابلًا للقراءة من حسابك فقط.

---

## Gemini CLI {: #gemini-cli }

### 1. إضافة الخادم {: #1-add-the-server }

ضع مفتاح API في متغير بيئة، ثم أضف الخادم:

```bash
export DIGNA_API_KEY='<api key>'
gemini mcp add --transport http --scope user --header "Authorization: Bearer $DIGNA_API_KEY" digna https://digna.example.com/mcp
```

تملأ الصدفة (shell) قيمة `$DIGNA_API_KEY` عند تشغيل الأمر، لذلك يخزّن Gemini CLI المفتاح في إعداداته. بدون
`--scope user`، تتم إضافة الخادم إلى المشروع الحالي فقط.

### 2. أو تعديل settings.json {: #2-or-edit-settings-json }

يكتب الأمر أعلاه إلى `settings.json`. لتعديل الملف بنفسك:

| النطاق | الملف |
|---|---|
| كل مشاريعك | `~/.gemini/settings.json` |
| مشروع واحد | `.gemini/settings.json` في المشروع |

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

استخدم `httpUrl`، وهو المفتاح الخاص بـ streamable HTTP. أما المفتاح المشابه `url` فيختار نقل SSE الأقدم، الذي لا
يوفره digna MCP Server. لا تستخدم الشرطات السفلية في اسم الخادم.

!!! tip "اترك trust معطّلًا"

    يسأل Gemini CLI قبل كل استدعاء أداة ما لم يكن للخادم `"trust": true`. اترك `trust` معطّلًا بالنسبة لـ *digna*،
    حتى تؤكد بنفسك كل تغيير يجريه الوكيل على تهيئتك.

### 3. التحقق من الاتصال {: #3-verify-the-connection-gemini-cli }

من الصدفة:

```bash
gemini mcp list
```

يجب أن يظهر الخادم `digna` على أنه متصل. داخل جلسة Gemini CLI، شغّل `/mcp` لرؤية الخادم وأدواته.

---

## استكشاف أخطاء Gemini وإصلاحها {: #troubleshooting-gemini }

### يظهر الخادم على أنه غير متصل

- تحقق من أن نقطة النهاية تنتهي بـ `/mcp` وأنها قابلة للوصول من جهازك.
- تحقق من اسم المفتاح: `serverUrl` في Antigravity، و`httpUrl` في Gemini CLI.
- تعني `401` أن المفتاح قد رُفض؛ راجع [401 Unauthorized](overview.md#troubleshooting).

### لم يعد Gemini CLI يعمل لحسابي

منذ يونيو 2026، تستخدم حسابات Google الفردية Antigravity CLI بدلًا من Gemini CLI. انقل الإدخال `digna` إلى
`mcp_config.json` كما هو موضح في [Antigravity](#antigravity)، وأعد تسمية `httpUrl` إلى `serverUrl`.

---

## انظر أيضًا {: #see-also }

- [نظرة عامة على وكلاء الذكاء الاصطناعي](overview.md): نقطة النهاية ومفتاح API والأمان واستكشاف الأخطاء العام
- [Claude](claude_mcp_guide.md): ربط Claude Code أو Claude Desktop أو موصل مخصص
- [digna Agentic](../platform/agentic/Introduction.md): ما يمكن لوكلاء الذكاء الاصطناعي فعله مع *digna*
