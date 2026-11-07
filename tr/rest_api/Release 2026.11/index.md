# digna REST API 2026.11

*digna* REST API, kendi araçlarınızın ve pipeline'larınızın HTTP ve JSON üzerinden *digna* ile
çalışmasını sağlar: projeleri ve denetim sonuçlarını okuyabilir, veri kaynaklarını, veri kümelerini
ve öznitelikleri yönetebilir ve denetimleri başlatabilirler; örneğin bir veri yüklemesinin sonunda.
[Python SDK](../../sdk/Release%202026.11/index.md) da aynı API'yi kullanır.

Bu sayfa her isteğin ortak yönlerini ele alır. Kaynak sayfaları her uç noktayı parametreleri, istek
gövdesi, yanıtları ve şemalarıyla birlikte listeler:

| Kaynak | Uç noktalar |
|---|---|
| [Projects](projects.md) | Projeleri okuma |
| [DB Connections](db_connections.md) | Veritabanı bağlantılarını okuma |
| [Data Sources](data_sources.md) | Veri kaynaklarını oluşturma, okuma, güncelleme ve silme |
| [Data Sets](data_sets.md) | Veri kümelerini oluşturma, okuma, güncelleme ve silme |
| [Attributes](attributes.md) | Öznitelikleri oluşturma, okuma, güncelleme ve silme |
| [Check Definitions](check_definitions.md) | Kontrol tanımlarını okuma |
| [Inspection Requests](inspection_requests.md) | Denetimleri başlatma ve ilerlemelerini izleme |
| [Inspection Statuses](inspection_statuses.md) | Denetim sonuçlarını proje, veri kaynağı ve veri kümesi bazında okuma |

---

## Temel URL {: #base-url }

API, *digna* backend'inin bir parçasıdır. Her yol, backend'in adresinden sonra `/v1` ile başlar:

```text
https://digna.example.com/v1/projects
```

Backend'in adresi, dashboard'un kullandığı adrestir: `dashboard/dashboard_config.toml` dosyasının
`[api]` bölümündeki `baseUrl`. Çağıran taraf ile *digna* aynı makinede değilse her zaman HTTPS
kullanın, çünkü her istek bir API anahtarı taşır.

---

## Kimlik Doğrulama {: #authentication }

Her istek, bir *digna* kullanıcısının API anahtarını `Authorization` başlığında gönderir:

```text
Authorization: Bearer <api key>
```

Bir anahtar oluşturmak için dashboard'un sol alt köşesindeki kullanıcı profilinizi açın,
**API Keys**'e, ardından **Add API Key**'e tıklayın ve anahtarı kopyalayın. Anahtar yalnızca bir
kez gösterilir. Aynı anahtarlar [digna MCP Server](../../ai_agents/overview.md) için de çalışır.

Bir istek, anahtarın ait olduğu kullanıcının izinleriyle çalışır. Oluşturma, değiştirme ve silme
işlemleri projede editör rolü gerektirir; aksi takdirde istek `403` koduyla ve
`You don't have permission to edit this project` mesajıyla reddedilir.

!!! tip "Otomasyon İçin Ayrı Bir Kullanıcı Kullanın"

    Her entegrasyon için ayrı bir *digna* kullanıcısı oluşturun, ona yalnızca ihtiyaç duyduğu
    projeleri ve rolleri verin ve anahtarını bir son kullanma tarihiyle oluşturun. Böylece başka
    kimseyi etkilemeden, bir entegrasyonun erişimini anahtarını silerek iptal edebilirsiniz.

---

## İstek Gönderme {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

Yanıtlar JSON biçimindedir. Listeler bir JSON dizisi olarak döndürülür. İstek gövdeleri de JSON
biçimindedir ve `Content-Type: application/json` ile gönderilir.

---

## Sınırlar ve Filtreler {: #limits-and-filters }

Liste uç noktaları en fazla `limit` kadar öğe döndürür: varsayılan olarak 200, en fazla 5000. Bu
aralığın dışındaki bir değer `400` ile reddedilir. Offset veya sayfa belirteci yoktur; bu nedenle
bir listeyi filtreleriyle daraltın, örneğin `project_id`, `data_source_id` ya da denetim
durumlarında `start_date` ve `end_date` ile.

60 saniyeden uzun süren bir istek `408 Request Timeout` ile iptal edilir.

---

## Hatalar {: #errors }

Bir hata yanıtı, bir kod ve bir mesaj içeren bir JSON gövdesine sahiptir:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| Durum | Kod | Anlamı |
|---|---|---|
| `400` | `BAD_REQUEST` | İstek geçersiz, örneğin aralık dışında bir `limit` |
| `401` | `NOT_AUTHENTICATED` | API anahtarı eksik, hatalı biçimlendirilmiş, bilinmiyor veya süresi dolmuş |
| `403` | `NOT_AUTHORIZED` | Anahtarın kullanıcısı bu isteğin gerektirdiği role sahip değil |
| `403` | `INVALID_LICENSE` | *digna* lisansının süresi dolmuş |
| `404` | `NOT_FOUND` | Proje, veri kaynağı veya başka bir öğe mevcut değil |
| `500` | `INTERNAL_ERROR` | *digna*'da beklenmeyen bir hata. Ayrıntılar backend log'undadır |

Bir `401` yanıtının `message` alanı, anahtarla ilgili sorunun ne olduğunu belirtir:

| Mesaj | Neden |
|---|---|
| `Missing Authorization header` | `Authorization` başlığı gönderilmedi |
| `Invalid Authorization header format` | Değer `Bearer ` ile başlamıyor |
| `Invalid API key` | Anahtar yanlış veya silinmiş |
| `API key expired` | Anahtarın süresi dolmuş. Yeni bir anahtar oluşturun |

---

## Denetim Çalıştırma {: #running-an-inspection }

Tipik bir entegrasyon, bir veri yüklemesi bittiğinde bir denetim başlatır, tamamlanmasını bekler ve
sonucu okur:

1. [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request) ile
   **denetimi başlatın**. Yanıt, isteğin `id` değerini içerir.
2. [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request)
   ile **ilerlemesini izleyin**. `status` değeri `PENDING` durumundan `RUNNING` üzerinden
   `COMPLETED` durumuna geçer ya da `FAILED`, `ABORTED` veya `CANCELLED` olarak sona erer. Artık
   değişmeyene kadar birkaç saniyede bir yeniden sorgulayın.
3. Denetlenen tarihler için [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses)
   ile **sonucu okuyun**. Her öğenin genel bir `status` değeri vardır: `0` (OK), `1` (uyarı),
   `2` (kritik) veya `-1` (durum yok); ayrıca başarılı, belirsiz ve başarısız kontrollerin
   sayısını içeren modül başına bir durum bulunur.

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

## OpenAPI Belgesi {: #openapi-document }

Her *digna* kurulumu bu API'yi bir OpenAPI 3.1 belgesinde tanımlar ve istekleri denemek için
etkileşimli bir Swagger UI sunar:

| Ne | Adres |
|---|---|
| OpenAPI belgesi | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Release 2026.11 belgesi burada da mevcuttur: [openapi.json](openapi.json). Başka bir dilde istemci
oluşturmak için bu belgeyi kullanın.

!!! note "Yalnızca /v1 Uç Noktaları Kapsanır"

    Dashboard, backend ile başka, dahili uç noktalar üzerinden de iletişim kurar. Bunlar bu API'nin
    parçası değildir ve herhangi bir sürümle değişebilir; bu nedenle entegrasyonları yalnızca `/v1`
    uç noktaları üzerine kurun.