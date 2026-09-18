# مرجع digna Python SDK 2026.06

يوثّق هذا القسم حزمة تطوير Python الخاصة بـ ***digna***. وهو منظَّم كمرجع متعدد الصفحات: استخدم هذه النظرة العامة لفهم العميل، ثم تابع في الصفحات المخصّصة للبدء السريع والموارد والنماذج والأخطاء ووثائق واجهة البرمجة المُولَّدة تلقائيًا.

تُنشر الحزمة باسم `digna-sdk` وتوفّر عميلًا مستقرًا ومُصدَّرًا بإصدارات لواجهة REST الخاصة بـ ***digna***.

---

## أساسيات حزمة التطوير

---

### نظرة عامة

تعتمد الحزمة تصميم عميل موجَّهًا نحو الموارد. يُتاح كل مجال من مجالات واجهة البرمجة كعميل مستقل ضمن الكائن الأعلى `DignaClient`، مع نماذج طلب واستجابة محدَّدة الأنواع ومعالجة موحَّدة للأخطاء.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### الميزات الأساسية

- **نماذج محدَّدة الأنواع** — يجري التحقق من كل طلب وكل استجابة باستخدام pydantic، بحيث يكتشف المحرّر ومدقّق الأنواع الأخطاء قبل أي اتصال بالشبكة.
- **توجُّه نحو الموارد** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` و `client.inspection_statuses` يوفّر كل منها أساليب بسيطة هي `list` / `get` / `create` / `update` / `delete`.
- **أخطاء واضحة** — تُطلق أخطاء واجهة البرمجة الاستثناء `DignaAPIError` (أو فئة فرعية أدق مثل `DignaAuthenticationError` أو `DignaAuthorizationError` أو `DignaNotFoundError`) بدلًا من إرجاع `None` بصمت.

### التثبيت

```bash
pip install digna-sdk
```

---

## صفحات المرجع

يتوزّع هذا الإصدار على الصفحات التالية:

- [البدء السريع](quickstart.md) — الاتصال وإجراء أولى الاستدعاءات.
- [الموارد](resources.md) — القائمة الكاملة لعملاء الموارد المتاحة.
- [النماذج](models.md) — نماذج pydantic المستخدَمة للإدخال والإخراج.
- [الأخطاء](errors.md) — التسلسل الهرمي للاستثناءات.
- [مرجع واجهة البرمجة](reference.md) — وثائق مرجعية مُولَّدة تلقائيًا.