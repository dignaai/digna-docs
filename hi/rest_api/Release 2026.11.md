# digna REST API 2026.11

*digna* REST API आपके अपने टूल और पाइपलाइनों को HTTP और JSON के माध्यम से *digna* के साथ काम करने देता है:
प्रोजेक्ट और निरीक्षण परिणाम पढ़ें, डेटा स्रोत, डेटासेट और एट्रिब्यूट प्रबंधित करें, और निरीक्षण शुरू करें,
उदाहरण के लिए किसी डेटा लोड के अंत में। [Python SDK](../../sdk/Release%202026.11/index.md)
भी इसी API का उपयोग करता है।

यह पृष्ठ उन बातों को बताता है जो हर अनुरोध में समान होती हैं। संसाधन पृष्ठों पर प्रत्येक एंडपॉइंट उसके
पैरामीटर, अनुरोध बॉडी, प्रतिक्रियाओं और स्कीमा के साथ सूचीबद्ध है:

| संसाधन | एंडपॉइंट |
|---|---|
| [Projects](projects.md) | प्रोजेक्ट पढ़ें |
| [DB Connections](db_connections.md) | डेटाबेस कनेक्शन पढ़ें |
| [Data Sources](data_sources.md) | डेटा स्रोत बनाएँ, पढ़ें, अपडेट करें और हटाएँ |
| [Data Sets](data_sets.md) | डेटासेट बनाएँ, पढ़ें, अपडेट करें और हटाएँ |
| [Attributes](attributes.md) | एट्रिब्यूट बनाएँ, पढ़ें, अपडेट करें और हटाएँ |
| [Check Definitions](check_definitions.md) | जाँच परिभाषाएँ पढ़ें |
| [Inspection Requests](inspection_requests.md) | निरीक्षण शुरू करें और उनकी प्रगति पर नज़र रखें |
| [Inspection Statuses](inspection_statuses.md) | प्रोजेक्ट, डेटा स्रोत और डेटासेट के अनुसार निरीक्षण परिणाम पढ़ें |

---

## बेस URL {: #base-url }

API *digna* बैकएंड का हिस्सा है। हर पथ बैकएंड के पते के बाद `/v1` से शुरू होता है:

```text
https://digna.example.com/v1/projects
```

बैकएंड का पता वही है जिसका उपयोग डैशबोर्ड करता है, यानी `dashboard/dashboard_config.toml` के `[api]`
अनुभाग में `baseUrl`। जब भी कॉल करने वाला और *digna* एक ही मशीन पर न हों, HTTPS का उपयोग करें, क्योंकि
हर अनुरोध एक API कुंजी साथ ले जाता है।

---

## प्रमाणीकरण {: #authentication }

हर अनुरोध किसी *digna* उपयोगकर्ता की API कुंजी `Authorization` हेडर में भेजता है:

```text
Authorization: Bearer <api key>
```

कुंजी बनाने के लिए डैशबोर्ड के निचले-बाएँ कोने में अपनी उपयोगकर्ता प्रोफ़ाइल खोलें, **API Keys** पर क्लिक करें,
फिर **Add API Key** पर, और कुंजी कॉपी करें। यह केवल एक बार दिखाई जाती है। यही कुंजियाँ
[digna MCP Server](../../ai_agents/overview.md) के लिए भी काम करती हैं।

अनुरोध कुंजी के उपयोगकर्ता की अनुमतियों के साथ चलता है। बनाने, बदलने और हटाने के लिए प्रोजेक्ट में editor
भूमिका आवश्यक है; अन्यथा अनुरोध `403` और संदेश `You don't have permission to edit this project` के साथ
अस्वीकार कर दिया जाता है।

!!! tip "स्वचालन के लिए एक समर्पित उपयोगकर्ता का उपयोग करें"

    हर एकीकरण के लिए एक *digna* उपयोगकर्ता बनाएँ, उसे केवल वही प्रोजेक्ट और भूमिकाएँ दें जिनकी उसे
    आवश्यकता है, और उसकी कुंजी समाप्ति तिथि के साथ बनाएँ। तब आप किसी एक एकीकरण की पहुँच उसकी कुंजी हटाकर
    रद्द कर सकते हैं, और किसी और पर कोई असर नहीं पड़ता।

---

## अनुरोध भेजना {: #making-a-request }

```bash
export DIGNA_API_KEY='<api key>'
curl https://digna.example.com/v1/projects -H "Authorization: Bearer $DIGNA_API_KEY"
```

प्रतिक्रियाएँ JSON में होती हैं। सूचियाँ JSON ऐरे के रूप में लौटाई जाती हैं। अनुरोध बॉडी भी JSON में होती है और
`Content-Type: application/json` के साथ भेजी जाती है।

---

## सीमाएँ और फ़िल्टर {: #limits-and-filters }

सूची वाले एंडपॉइंट अधिकतम `limit` आइटम लौटाते हैं: डिफ़ॉल्ट रूप से 200, और अधिकतम 5000। इस सीमा से बाहर का मान
`400` के साथ अस्वीकार कर दिया जाता है। कोई ऑफ़सेट या पेज टोकन नहीं है, इसलिए इसके बजाय सूची को उसके फ़िल्टरों से
सीमित करें, उदाहरण के लिए `project_id`, `data_source_id`, या निरीक्षण स्थितियों पर `start_date` और `end_date`।

60 सेकंड से अधिक समय लेने वाला अनुरोध `408 Request Timeout` के साथ रद्द कर दिया जाता है।

---

## त्रुटियाँ {: #errors }

त्रुटि प्रतिक्रिया में एक कोड और एक संदेश वाली JSON बॉडी होती है:

```json
{
  "code": "NOT_FOUND",
  "message": "Data set not found"
}
```

| स्थिति | कोड | अर्थ |
|---|---|---|
| `400` | `BAD_REQUEST` | अनुरोध अमान्य है, उदाहरण के लिए `limit` सीमा से बाहर है |
| `401` | `NOT_AUTHENTICATED` | API कुंजी अनुपस्थित, गलत स्वरूप वाली, अज्ञात या समाप्त है |
| `403` | `NOT_AUTHORIZED` | कुंजी के उपयोगकर्ता के पास वह भूमिका नहीं है जिसकी इस अनुरोध को आवश्यकता है |
| `403` | `INVALID_LICENSE` | *digna* लाइसेंस समाप्त हो गया है |
| `404` | `NOT_FOUND` | प्रोजेक्ट, डेटा स्रोत या कोई अन्य आइटम मौजूद नहीं है |
| `500` | `INTERNAL_ERROR` | *digna* में एक अनपेक्षित त्रुटि। विवरण बैकएंड लॉग में है |

`401` का `message` बताता है कि कुंजी में क्या गलत है:

| संदेश | कारण |
|---|---|
| `Missing Authorization header` | कोई `Authorization` हेडर नहीं भेजा गया |
| `Invalid Authorization header format` | मान `Bearer ` से शुरू नहीं होता |
| `Invalid API key` | कुंजी गलत है, या उसे हटा दिया गया था |
| `API key expired` | कुंजी समाप्त हो गई है। नई कुंजी बनाएँ |

---

## निरीक्षण चलाना {: #running-an-inspection }

एक सामान्य एकीकरण डेटा लोड पूरा होने पर निरीक्षण शुरू करता है, उसके पूरा होने की प्रतीक्षा करता है, और परिणाम
पढ़ता है:

1. [`POST /v1/inspection-requests`](inspection_requests.md#submit-inspection-request) से **निरीक्षण शुरू करें**।
   प्रतिक्रिया में अनुरोध का `id` होता है।
2. [`GET /v1/inspection-requests/{inspection_request_id}`](inspection_requests.md#get-inspection-request) से **उसकी प्रगति पर नज़र रखें**।
   उसका `status` `PENDING` से `RUNNING` होते हुए `COMPLETED` तक जाता है, या `FAILED`, `ABORTED` या
   `CANCELLED` के रूप में समाप्त होता है। हर कुछ सेकंड में दोबारा पूछें, जब तक कि वह बदलना बंद न कर दे।
3. निरीक्षण की गई तिथियों के लिए [`GET /v1/inspection-statuses/data-sources`](inspection_statuses.md#get-data-source-inspection-statuses) से **परिणाम पढ़ें**।
   हर आइटम की एक समग्र `status` होती है: `0` (OK), `1` (चेतावनी), `2` (गंभीर) या `-1` (कोई स्थिति नहीं),
   और प्रत्येक मॉड्यूल की स्थिति, जिसमें पास हुई, अनिश्चित और विफल जाँचों की संख्या होती है।

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

## OpenAPI दस्तावेज़ {: #openapi-document }

हर *digna* इंस्टॉलेशन इस API का वर्णन एक OpenAPI 3.1 दस्तावेज़ में करता है, और उस पर अनुरोध आज़माने के लिए
एक इंटरैक्टिव Swagger UI उपलब्ध कराता है:

| क्या | पता |
|---|---|
| OpenAPI दस्तावेज़ | `https://digna.example.com/api-docs/stable/v1/openapi.json` |
| Swagger UI | `https://digna.example.com/v1/swagger-ui` |

Release 2026.11 का दस्तावेज़ यहाँ भी उपलब्ध है: [openapi.json](openapi.json)। किसी अन्य भाषा में क्लाइंट
जनरेट करने के लिए इसका उपयोग करें।

!!! note "केवल /v1 एंडपॉइंट शामिल हैं"

    डैशबोर्ड बैकएंड से अन्य, आंतरिक एंडपॉइंट के माध्यम से भी बात करता है। वे इस API का हिस्सा नहीं हैं और
    किसी भी रिलीज़ में बदल सकते हैं, इसलिए एकीकरण केवल `/v1` एंडपॉइंट पर ही बनाएँ।