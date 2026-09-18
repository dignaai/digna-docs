# digna Python SDK संदर्भ 2026.06

यह अनुभाग ***digna*** के Python SDK का दस्तावेज़ीकरण करता है। यह कई पृष्ठों वाले संदर्भ के रूप में व्यवस्थित है: क्लाइंट को समझने के लिए इस अवलोकन का उपयोग करें और फिर त्वरित शुरुआत, संसाधनों, मॉडलों, त्रुटियों और स्वतः उत्पन्न API दस्तावेज़ों के अलग-अलग पृष्ठों पर आगे बढ़ें।

SDK को `digna-sdk` पैकेज के रूप में प्रकाशित किया जाता है और यह ***digna*** REST API के लिए एक स्थिर, संस्करणित क्लाइंट उपलब्ध कराता है।

---

## SDK की मूल बातें

---

### अवलोकन

SDK संसाधन-केंद्रित क्लाइंट डिज़ाइन का पालन करता है। API का प्रत्येक क्षेत्र शीर्ष-स्तरीय `DignaClient` पर एक स्वतंत्र क्लाइंट के रूप में उपलब्ध है, जिसमें अनुरोध और प्रतिक्रिया के मॉडल टाइप किए गए हैं और त्रुटि प्रबंधन एकसमान है।

```python
from digna_sdk import DignaClient

client = DignaClient(
    base_url="https://your-digna-instance",
    token="...",
)
```

### मुख्य विशेषताएँ

- **टाइप किए गए मॉडल** — प्रत्येक अनुरोध और प्रतिक्रिया pydantic से मान्य की जाती है, इसलिए नेटवर्क कॉल से पहले ही आपका एडिटर और टाइप चेकर गलतियाँ पकड़ लेते हैं।
- **संसाधन-केंद्रित** — `client.projects`, `client.data_sources`, `client.data_sets`, `client.attributes`, `client.check_definitions`, `client.db_connections`, `client.inspection_requests` तथा `client.inspection_statuses` में से प्रत्येक सरल `list` / `get` / `create` / `update` / `delete` विधियाँ उपलब्ध कराता है।
- **स्पष्ट त्रुटियाँ** — API त्रुटियाँ चुपचाप `None` लौटाने के बजाय `DignaAPIError` (या अधिक विशिष्ट उपवर्ग, जैसे `DignaAuthenticationError`, `DignaAuthorizationError` या `DignaNotFoundError`) उठाती हैं।

### स्थापना

```bash
pip install digna-sdk
```

---

## संदर्भ पृष्ठ

यह रिलीज़ निम्नलिखित पृष्ठों में विभाजित है:

- [त्वरित शुरुआत](quickstart.md) — कनेक्ट करें और पहले कॉल करें।
- [संसाधन](resources.md) — उपलब्ध संसाधन क्लाइंट की पूरी सूची।
- [मॉडल](models.md) — इनपुट और आउटपुट के लिए उपयोग किए जाने वाले pydantic मॉडल।
- [त्रुटियाँ](errors.md) — अपवादों का पदानुक्रम।
- [API संदर्भ](reference.md) — स्वतः उत्पन्न संदर्भ दस्तावेज़।