# digna Python SDK Başvurusu 2026.06

Bu bölüm ***digna*** için Python SDK'sını belgeler. Birden çok sayfadan oluşan bir başvuru kılavuzu olarak düzenlenmiştir: istemciyi anlamak için bu genel bakışı kullanın, ardından hızlı başlangıç, kaynaklar, modeller, hatalar ve otomatik oluşturulan API belgeleri için ayrı sayfalarla devam edin.

SDK, `digna-sdk` paketi olarak yayımlanır ve ***digna*** REST API'si için kararlı, sürümlenmiş bir istemci sunar.

---

## SDK Temelleri

---

### Genel Bakış

SDK, kaynak odaklı bir istemci tasarımını izler. Her API alanı, üst düzey `DignaClient` üzerinde birinci sınıf bir istemci olarak sunulur; istek ve yanıt modelleri türlendirilmiştir ve hata yönetimi tutarlıdır.

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### Temel Özellikler

- **Türlendirilmiş modeller** — her istek ve yanıt pydantic ile doğrulanır; böylece düzenleyiciniz ve tür denetleyiciniz hataları ağ çağrısından önce yakalar.
- **Kaynak odaklı** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` ve `client.inspection_statuses` istemcilerinin her biri basit `list` / `get` / `create` / `update` / `delete` yöntemleri sunar.
- **Açık hatalar** — API hataları sessizce `None` döndürmek yerine `DignaAPIError` (ya da `DignaAuthenticationError`, `DignaAuthorizationError` veya `DignaNotFoundError` gibi daha özel bir alt sınıf) fırlatır.

### Kurulum

```bash
pip install digna-sdk
```

---

## Başvuru Sayfaları

Bu sürüm aşağıdaki sayfalara ayrılmıştır:

- [Hızlı Başlangıç](quickstart.md) — bağlanın ve ilk çağrılarınızı yapın.
- [Kaynaklar](resources.md) — kullanılabilir kaynak istemcilerinin tam listesi.
- [Modeller](models.md) — giriş ve çıkış için kullanılan pydantic modelleri.
- [Hatalar](errors.md) — istisna hiyerarşisi.
- [API Başvurusu](reference.md) — otomatik oluşturulan başvuru belgeleri.