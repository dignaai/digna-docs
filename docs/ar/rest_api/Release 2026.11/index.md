---
title: نظرة عامة على REST API 2026.11 | وثائق digna
description: استخدم digna REST API v1 لقراءة المشاريع ونتائج الفحص، وإدارة مصادر البيانات ومجموعات البيانات والسمات، وبدء عمليات الفحص — عنوان URL الأساسي، والمصادقة بمفتاح API، وحدود القوائم، والأخطاء، ومستند OpenAPI.
image: /assets/logo_square.png
keywords: digna REST API, digna API, digna OpenAPI, مفتاح API لـ digna, API طلبات الفحص, API جودة البيانات, Swagger UI
---

# digna REST API 2026.11

تتيح REST API الخاصة بـ *digna* لأدواتك ومسارات البيانات الخاصة بك العمل مع *digna* عبر HTTP وJSON: قراءة
المشاريع ونتائج الفحص، وإدارة مصادر البيانات ومجموعات البيانات والسمات، وبدء عمليات الفحص، على سبيل المثال
في نهاية تحميل البيانات. وتستخدم [Python SDK](../../sdk/Release%202026.11/index.md)
واجهة API نفسها.

تتناول هذه الصفحة ما تشترك فيه جميع الطلبات. وتسرد صفحات الموارد كل نقطة نهاية مع معاملاتها ونص الطلب
والاستجابات والمخططات:

| المورد | نقاط النهاية |
|---|---|
| [Projects](projects.md) | قراءة المشاريع |
| [DB Connections](db_connections.md) | قراءة اتصالات قواعد البيانات |
| [Data Sources](data_sources.md) | إنشاء مصادر البيانات وقراءتها وتحديثها وحذفها |
| [Data Sets](data_sets.md) | إنشاء مجموعات البيانات وقراءتها وتحديثها وحذفها |
| [Attributes](attributes.md) | إنشاء السمات وقراءتها وتحديثها وحذفها |
| [Check Definitions](check_definitions.md) | قراءة تعريفات الفحوصات |
| [Inspection Requests](inspection_requests.md) | بدء عمليات الفحص ومتابعة تقدّمها |
| [Inspection Statuses](inspection_statuses.md) | قراءة نتائج الفحص لكل مشروع ومصدر بيانات ومجموعة بيانات |

---

## عنوان URL الأساسي {: #base-url }

واجهة API جزء من الواجهة الخلفية لـ *digna*. يبدأ كل مسار بـ `/v1` بعد عنوان الواجهة الخلفية:

```text
https://digna.example.com/v1/projects
```

عنوان الواجهة الخلفية هو العنوان نفسه الذي تستخدمه لوحة التحكم، أي `baseUrl` في القسم `[api]` من الملف
`dashboard/dashboard_config.toml`. استخدم HTTPS كلما لم يكن المستدعي و*digna* على الجهاز نفسه، لأن كل طلب
يحمل مفتاح API.

---

## المصادقة {: #authentication }

يرسل كل طلب مفتاح API لمستخدم في *digna* في الترويسة `Authorization`:

```text
Authorization: Bearer <api key>
```

لإنشاء مفتاح، افتح ملفك الشخصي في الزاوية السفلية اليسرى من لوحة التحكم، وانقر على **API Keys**، ثم على
**Add API Key**، وانسخ المفتاح. لا يُعرض إلا مرة واحدة. وتعمل المفاتيح نفسها أيضًا مع
[digna MCP Server](../../ai_agents/overview.md).

يُنفَّذ الطلب بصلاحيات المستخدم صاحب المفتاح. ويتطلب الإنشاء والتغيير والحذف دور editor في المشروع؛ وإلا يُرفض
الطلب بالرمز `403` والرسالة `You don't have permission to edit this project`.

!!! tip "استخدم مستخدمًا مخصّصًا للأتمتة"

    أنشئ مستخدمًا في *digna* لكل تكامل، وامنحه فقط المشاريع والأدوار التي يحتاجها، وأنشئ مفتاحه مع
    تاريخ انتهاء صلاحية. وبذلك يمكنك إلغاء وصول تكامل واحد بحذف مفتاحه، دون التأثير في أي شخص آخر.

---

## إرسال طلب {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

الاستجابات بتنسيق JSON. وتُعاد القوائم كمصفوفة JSON. ونصوص الطلبات بتنسيق JSON أيضًا، وتُرسل مع
`Content-Type: application/json`.

---

## الحدود وعوامل التصفية {: #limits-and-filters }

تُعيد نقاط نهاية القوائم `limit` عنصرًا على الأكثر: 200 افتراضيًا، وحتى 5000. وتُرفض القيمة الواقعة خارج هذا
النطاق بالرمز `400`. لا توجد إزاحة ولا رمز صفحة، لذا ضيّق القائمة بعوامل التصفية الخاصة بها بدلًا من ذلك، على
سبيل المثال `project_id` أو `data_source_id` أو `start_date` و`end_date` في حالات الفحص.

يُلغى الطلب الذي يستغرق أكثر من 60 ثانية مع `408 Request Timeout`.

---

## الأخطاء {: #errors }

تحتوي استجابة الخطأ على نص JSON يتضمن رمزًا ورسالة:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| الحالة | الرمز | المعنى |
|---|---|---|
| `400` | `BAD_REQUEST` | الطلب غير صالح، على سبيل المثال `limit` خارج النطاق |
| `401` | `NOT_AUTHENTICATED` | مفتاح API مفقود أو مشوَّه أو غير معروف أو منتهي الصلاحية |
| `403` | `NOT_AUTHORIZED` | لا يملك مستخدم المفتاح الدور الذي يحتاجه هذا الطلب |
| `403` | `INVALID_LICENSE` | انتهت صلاحية ترخيص *digna* |
| `404` | `NOT_FOUND` | المشروع أو مصدر البيانات أو العنصر الآخر غير موجود |
| `500` | `INTERNAL_ERROR` | خطأ غير متوقع في *digna*. توجد التفاصيل في سجل الواجهة الخلفية |

يوضح `message` في استجابة `401` ما المشكلة في المفتاح:

| الرسالة | السبب |
|---|---|
| `Missing Authorization header` | لم تُرسل الترويسة `Authorization` |
| `Invalid Authorization header format` | لا تبدأ القيمة بـ `Bearer ` |
| `Invalid API key` | المفتاح خاطئ، أو تم حذفه |
| `API key expired` | انتهت صلاحية المفتاح. أنشئ مفتاحًا جديدًا |

---

## تشغيل فحص {: #running-an-inspection }

يبدأ التكامل النموذجي فحصًا عند انتهاء تحميل البيانات، وينتظر اكتماله، ثم يقرأ النتيجة:

1. **ابدأ الفحص** باستخدام [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request).
   تحتوي الاستجابة على `id` الطلب.
2. **تابع تقدّمه** باستخدام [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request).
   تنتقل قيمة `status` من `PENDING` مرورًا بـ `RUNNING` إلى `COMPLETED`، أو تنتهي بـ `FAILED` أو
   `ABORTED` أو `CANCELLED`. اسأل مجددًا كل بضع ثوانٍ إلى أن تتوقف عن التغيّر.
3. **اقرأ النتيجة** باستخدام [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   للتواريخ التي جرى فحصها. لكل عنصر `status` إجمالية: `0` (OK) أو `1` (تحذير) أو `2` (حرجة) أو
   `-1` (بلا حالة)، وحالة لكل وحدة مع عدد الفحوصات الناجحة وغير المؤكدة والفاشلة.

```bash
curl -X POST https://digna.example.com/v1/inspection-requests \
  -H "Authorization: Bearer $DIGNA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "project_id": 1,
    "include_all_data_sources": true,
    "data_source_ids": [],
    "start_date": "2026-11-06",
    "end_date": "2026-11-06",
    "mode": "DAILY",
    "weekly_mode_weekdays": [],
    "monthly_mode_days": [],
    "use_notification": true
  }'
```

---

## مستند OpenAPI {: #openapi-document }

تصف كل عملية تثبيت لـ *digna* واجهة API هذه في مستند OpenAPI 3.1، وتوفّر Swagger UI تفاعلية لتجربة الطلبات
عليها:

| ماذا | العنوان |
|---|---|
| مستند OpenAPI | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

مستند Release 2026.11 متاح هنا أيضًا: [openapi.json](openapi.json). استخدمه لتوليد عميل بلغة برمجة أخرى.

!!! note "تقتصر التغطية على نقاط النهاية /v1"

    تتواصل لوحة التحكم أيضًا مع الواجهة الخلفية عبر نقاط نهاية داخلية أخرى. وهي ليست جزءًا من واجهة API
    هذه وقد تتغير مع أي إصدار، لذا ابنِ التكاملات على نقاط النهاية `/v1` فقط.
