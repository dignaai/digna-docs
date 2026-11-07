---
title: Claude – ربط Claude بـ digna عبر MCP | توثيق digna
description: اربط Claude بـ digna عبر digna MCP Server — Claude Code من سطر الأوامر أو من ملف .mcp.json مشترك، وClaude Desktop مع جسر محلي، والموصلات المخصصة في claude.ai، مع مفتاح API في الترويسة Authorization.
image: /assets/logo_square.png
keywords: Claude MCP, Claude Code MCP, Claude Desktop MCP, موصل claude.ai المخصص, digna MCP server, mcp-remote, Authorization Bearer, مفتاح API لـ digna
---

# ربط Claude بـ digna

يربط هذا الدليل Claude بـ **digna MCP Server**. تحتاج إلى نقطة نهاية MCP الخاصة بتثبيت *digna* لديك ومفتاح API،
كما هو موضح في [نظرة عامة على وكلاء الذكاء الاصطناعي](overview.md).

تستخدم الأمثلة `https://digna.example.com/mcp` كنقطة نهاية. استبدلها بنقطة النهاية الخاصة بك.

## اختيار طريقة الاتصال {: #choose-how-to-connect }

| منتج Claude | يتصل من | يعمل مع *digna* داخل شبكتك |
|---|---|---|
| [Claude Code](#claude-code) | جهازك | نعم |
| [Claude Desktop مع جسر محلي](#claude-desktop-with-a-local-bridge) | جهازك | نعم |
| [الموصل المخصص](#custom-connector) في claude.ai وClaude Desktop وClaude للأجهزة المحمولة | سحابة Anthropic | لا. يجب أن تكون نقطة النهاية قابلة للوصول من الإنترنت |

بالنسبة لتثبيت *digna* يعمل داخل شبكة شركتك، استخدم Claude Code أو Claude Desktop مع جسر محلي.

---

## Claude Code {: #claude-code }

### 1. إضافة الخادم {: #1-add-the-server }

ضع مفتاح API في متغير بيئة، ثم أضف الخادم:

```bash
export DIGNA_API_KEY='<api key>'
claude mcp add --transport http --scope user digna https://digna.example.com/mcp --header "Authorization: Bearer $DIGNA_API_KEY"
```

تملأ الصدفة (shell) قيمة `$DIGNA_API_KEY` عند تشغيل الأمر، لذلك يخزّن Claude Code المفتاح في تهيئته الخاصة.

يحدد `--scope` أين يكون الخادم متاحًا:

| النطاق | متاح |
|---|---|
| `local` (افتراضي) | لك، في المشروع الحالي فقط |
| `user` | لك، في كل مشروع |
| `project` | لكل من يعمل في المشروع، عبر ملف `.mcp.json` في المشروع |

### 2. مشاركة الخادم مع فريقك (اختياري) {: #2-share-the-server-with-your-team }

لمنح كل من في المشروع الخادم نفسه، أضف ملف `.mcp.json` إلى جذر المشروع. لا تكتب المفتاح في الملف. يملأ Claude Code
قيمة `${DIGNA_API_KEY}` من بيئة كل شخص:

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

يضبط كل شخص `DIGNA_API_KEY` على مفتاحه الخاص. في المرة الأولى التي يجد فيها Claude Code الملف، يسأل عما إذا كان
سيستخدم الخوادم الموجودة فيه.

### 3. التحقق من الاتصال {: #3-verify-the-connection }

من الصدفة:

```bash
claude mcp list
```

يجب أن يظهر الخادم `digna` بالحالة `✔ Connected`. داخل جلسة Claude Code، شغّل `/mcp` لرؤية الخادم وأدواته.

---

## Claude Desktop مع جسر محلي {: #claude-desktop-with-a-local-bridge }

يشغّل ملف تهيئة Claude Desktop خوادم MCP محلية على جهازك. يعمل هناك جسر صغير، هو الحزمة مفتوحة المصدر
[`mcp-remote`](https://github.com/geelen/mcp-remote)، ويمرر كل طلب إلى نقطة نهاية *digna* مع مفتاح API الخاص بك.
ولأن الجسر يعمل على جهازك، فإن هذه الطريقة تعمل مع *digna* داخل شبكة شركتك.

!!! note "حزمة مجتمعية"

    يتولى مجتمعها مفتوح المصدر صيانة `mcp-remote`، وليس Anthropic أو digna. تحقق من أن مؤسستك تسمح باستخدامها
    قبل أن تستخدمها.

### 1. تثبيت Node.js {: #1-install-nodejs }

يحتاج الجسر إلى [Node.js](https://nodejs.org) 18 أو أحدث. يستخدم Claude Desktop إصدار Node.js المثبت على نظامك.
تحقق منه باستخدام:

```bash
node --version
```

### 2. تعديل ملف التهيئة {: #2-edit-the-configuration-file }

افتح `claude_desktop_config.json`:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

أضف الخادم `digna`. إذا كان الملف يحتوي بالفعل على قسم `mcpServers`، فأضف الإدخال `digna` إليه:

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

!!! warning "أبقِ الترويسة كما هي تمامًا"

    اكتب `Authorization:${AUTH_HEADER}` بدون مسافات، وضع `Bearer <api key>` في `env`. لا يقوم Claude Desktop على
    Windows بتهريب المسافات داخل `args`، لذا فإن أي مسافة هناك تُفسد الترويسة.

### 3. إعادة تشغيل Claude Desktop {: #3-restart-claude-desktop }

أغلق Claude Desktop بالكامل ثم شغّله مرة أخرى. في محادثة جديدة، انقر على **+** وافتح **Connectors**: يجب أن يظهر
`digna` في القائمة وأن يكون مفعّلًا.

---

## الموصل المخصص {: #custom-connector }

يجعل الموصل المخصص *digna* متاحًا في claude.ai وClaude Desktop وتطبيقات Claude للأجهزة المحمولة دون أي إعداد محلي.
تتصل سحابة Anthropic بنقطة النهاية، لذا لا يعمل هذا إلا عندما:

- تكون نقطة نهاية *digna* قابلة للوصول من الإنترنت عبر HTTPS
- يتوفر لدى مؤسستك في Claude الخيار **Request headers** في مربع الحوار **Add custom connector**. تقدمه Anthropic
  كإصدار تجريبي لمجموعة محدودة من المؤسسات

!!! warning "غير مناسب لـ digna داخل شبكتك"

    تتطلب أنفاق MCP في Claude، التي تصل إلى الخوادم داخل شبكة خاصة، استخدام OAuth على خادم MCP. يصادق digna MCP
    Server باستخدام مفاتيح API، لذا لا يمكن استخدام النفق. استخدم بدلًا من ذلك [Claude Code](#claude-code) أو
    [Claude Desktop مع جسر محلي](#claude-desktop-with-a-local-bridge).

### 1. فتح إعدادات الموصل {: #1-open-the-connector-settings }

- **خطط Free وPro وMax وUltra**: اذهب إلى **Customize > Connectors** وانقر على **Add custom connector**.
- **خطط Team وEnterprise**: يذهب المالك (Owner) إلى **Organization settings > Connectors**، وينقر على **Add**،
  ثم على **Custom**، ويختار **Web** إذا طُلب منه تحديد النوع.

### 2. إدخال تفاصيل الموصل {: #2-enter-the-connector-details }

1. **MCP server URL**: `https://digna.example.com/mcp`
2. **Authentication**: **No sign-in**
3. **Request headers**: اختر `authorization` كاسم للترويسة، وأدخل `Bearer <api key>` كقيمة، بما في ذلك كلمة
   `Bearer` والمسافة، وحدده على أنه **Required**.
4. انقر على **Add**.

!!! warning "الجميع يتشاركون المفتاح"

    كل عضو يستخدم الموصل يعمل بمفتاح API نفسه، وبالتالي بمستخدم *digna* نفسه. أنشئ مستخدم *digna* مخصصًا للموصل،
    وامنحه فقط المشاريع والأدوار المسموح بها للجميع، مثل دور reader.

في خطط Team وEnterprise، يتصل الأعضاء بعد ذلك من **Customize > Connectors**، حيث يحمل الموصل التسمية **Custom**.

لا يمكن تغيير ترويسة موصل موجود في Claude. لاستخدام مفتاح جديد، احذف الموصل وأضفه مرة أخرى.

---

## استكشاف أخطاء Claude وإصلاحها {: #troubleshooting-claude }

### يعرض claude mcp list الرسالة Failed to connect

شغّل `claude mcp get digna` لمعرفة السبب. تعني `401` أن المفتاح قد رُفض؛ راجع
[401 Unauthorized](overview.md#troubleshooting). ينبّه Claude Code أيضًا إلى وجود مسافات أو فاصل أسطر في بداية
المفتاح أو نهايته، وهو ما يحدث غالبًا عند نسخه.

### لا يظهر digna في Claude Desktop

- تحقق من تثبيت Node.js 18 أو أحدث: `node --version`.
- تحقق من أن `claude_desktop_config.json` ملف JSON صالح. فاصلة واحدة مفقودة تمنع تحميل كل الخوادم في الملف.
- أغلق Claude Desktop بالكامل، وليس النافذة فقط، ثم شغّله مرة أخرى.

### لا يستطيع الموصل المخصص الوصول إلى الخادم

لا تستطيع سحابة Anthropic الوصول إلى نقطة النهاية. تحقق من أنها قابلة للوصول من الإنترنت عبر HTTPS بشهادة صالحة،
أو اتصل بدلًا من ذلك عبر [Claude Code](#claude-code).

---

## انظر أيضًا {: #see-also }

- [نظرة عامة على وكلاء الذكاء الاصطناعي](overview.md): نقطة النهاية ومفتاح API والأمان واستكشاف الأخطاء العام
- [Gemini](gemini_mcp_guide.md): ربط Antigravity أو Gemini CLI
- [digna Agentic](../platform/agentic/Introduction.md): ما يمكن لوكلاء الذكاء الاصطناعي فعله مع *digna*
