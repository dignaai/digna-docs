# digna Release 2026.06 के लिए Windows स्थापना मार्गदर्शिका

**रिलीज़:** 2026.06

**अंतिम अपडेट:** August 30, 2026


---

## विषय-सूची

1. [परिचय](#introduction)
2. [सिस्टम आवश्यकताएँ](#system-requirements)
3. [पूर्व-स्थापना सेटअप](#pre-installation-setup)
4. [PostgreSQL सर्वर सेटअप](#postgresql-server-setup)
5. [वेब सर्वर कॉन्फ़िगरेशन](#web-server-configuration)
6. [प्रारंभिक स्थापना](#initial-installation)
7. [बैकएंड कॉन्फ़िगरेशन](#backend-configuration)
8. [डैशबोर्ड कॉन्फ़िगरेशन](#dashboard-configuration)
9. [digna को Windows सेवा के रूप में चलाना](#running-digna-as-a-windows-service)
10. [नई रिलीज़ में उन्नयन](#upgrading-to-a-new-release)

---

## परिचय {: #introduction }

### digna के बारे में

digna एक व्यापक AI-चालित प्लेटफ़ॉर्म है जो डेटा वेयरहाउस, लेक्स और लेकहाउस जैसे विभिन्न डेटा परिवेशों में डेटा क्वालिटी प्रबंधन को अनुकूलित करने के लिए डिज़ाइन किया गया है। उच्च स्केलेबिलिटी और अनुकूलनशीलता के साथ बनाया गया, digna स्वचालन, रीयल-टाइम मॉनिटरिंग और एनॉमली डिटेक्शन के माध्यम से आधुनिक डेटा चुनौतियों का समाधान करता है।

digna मुख्य रूप से दो घटकों से मिलकर बनता है:

- **dignabackend**: एप्लिकेशन का मुख्य इंजन, जो डेटा प्रोसेसिंग और गुणवत्ता जांचों के लिए जिम्मेदार है।
- **dignadashboard**: एक वेब-आधारित इंटरफ़ेस जो वेब सर्वर पर होस्ट होता है और digna प्लेटफ़ॉर्म के साथ इंटरैक्ट करने तथा डेटा गुणवत्ता मेट्रिक्स को विज़ुअलाइज़ करने के लिए उपयोगकर्ता-अनुकूल तरीका प्रदान करता है।

### रिलीज़ 2026.06 में नया क्या है

इस रिलीज़ के साथ डेटा ऑब्ज़र्वेबिलिटी की क्षमताएँ सीधे आपके कोड में लाई गई हैं, जिससे डेवलपर्स स्रोत पर ही डेटा गुणवत्ता की निगरानी कर सकते हैं। पूरी जानकारी के लिए [रिलीज़ नोट्स](http://docs.digna.ai/changelog/Release_202606/) देखें।

### macOS या Linux ढूँढ रहे हैं?

यह गाइड Windows के लिए है। अन्य प्लेटफ़ॉर्म के लिए, देखिए [macOS स्थापना मार्गदर्शिका](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) या [Linux स्थापना मार्गदर्शिका](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md)।

---

## सिस्टम आवश्यकताएँ {: #system-requirements }

स्थापना शुरू करने से पहले सुनिश्चित करें कि आपका सिस्टम निम्नलिखित न्यूनतम आवश्यकताओं को पूरा करता है:

| आवश्यकता | विशिष्टता |
|---|---|
| **ऑपरेटिंग सिस्टम** | Windows Server या Windows 10/11 |
| **मेमोरी (न्यूनतम सेटअप)** | 16 GB RAM |
| **डिस्क स्थान** | 10 GB उपलब्ध स्टोरेज |
| **डेटाबेस** | PostgreSQL Server 12 या ऊपर |
| **वेब सर्वर** | IIS, Apache Tomcat, या समकक्ष |

### डेटाबेस इंस्टॉलेशन विकल्प

**यदि PostgreSQL पहले से स्थापित है:**
आप अपने मौजूदा PostgreSQL Server में digna के लिए एक नया डेटाबेस जोड़ सकते हैं।

**यदि आप PostgreSQL को उसी मशीन पर इंस्टॉल कर रहे हैं जहाँ digna है:**

!!! info "अनुशंसित विनिर्देश"

    - **मेमोरी**: 32 GB RAM (16 GB के बजाय)
    - **डिस्क स्थान**: 50 GB उपलब्ध स्टोरेज (10 GB के बजाय)

    ये उच्चतर विनिर्देश दोनों, digna और PostgreSQL डेटाबेस को एक साथ चलाने के लिए उपयुक्त हैं।

---

## पूर्व-स्थापना सेटअप {: #pre-installation-setup }

digna स्थापित करने से पहले सुनिश्चित करें कि दो प्रमुख पूर्व-आवश्यकताएँ मौजूद हैं:

1. **PostgreSQL Server** – गणना किए गए मेट्रिक्स और प्रदर्शन डेटा को संग्रहीत करने के लिए
2. **वेब सर्वर** – digna Dashboard होस्ट करने के लिए

यदि ये घटक पहले से सेटअप नहीं हैं, तो उन्हें इंस्टॉल और कॉन्फ़िगर करने के लिए नीचे दिए गए अनुभागों का पालन करें।

---

## PostgreSQL सर्वर सेटअप {: #postgresql-server-setup }

### यदि आपके पास पहले से PostgreSQL है

यदि PostgreSQL पहले से आपके लोकल मशीन पर इंस्टॉल और चल रहा है या आप मैनज्ड रिमोट PostgreSQL सर्वर का उपयोग कर रहे हैं, तो आप [अगले अनुभाग](#web-server-configuration) पर जा सकते हैं।

### PostgreSQL इंस्टॉल करना

Windows पर PostgreSQL इंस्टॉल करने के लिए निम्न चरणों का पालन करें:

#### चरण 1: PostgreSQL डाउनलोड करें

1. [PostgreSQL Downloads पेज](https://www.postgresql.org/download/) पर जाएँ
2. **Windows** चुनें
3. नवीनतम इंस्टॉलर डाउनलोड करें

#### चरण 2: इंस्टॉलर चलाएँ

1. डाउनलोड किए गए इंस्टॉलर फ़ाइल पर डबल-क्लिक करें
2. सेटअप विज़ार्ड में दिए गए निर्देशों का पालन करें

#### चरण 3: इंस्टॉलेशन डायरेक्टरी चुनें

PostgreSQL किस डायरेक्टरी में इंस्टॉल होगा यह चुनें। डिफ़ॉल्ट लोकेशन आम तौर पर उपयुक्त होती है।

#### चरण 4: कंपोनेंट्स चुनें

मानक सेटअप के लिए, डिफ़ॉल्ट कंपोनेंट विकल्पों को चुन कर रखें।

#### चरण 5: PostgreSQL सुपरयूज़र पासवर्ड सेट करें

PostgreSQL सुपरयूज़र (`postgres`) के लिए एक पासवर्ड दर्ज करें और पुष्टि करें। **इस पासवर्ड को सुरक्षित रखें** — आपको बाद में इसकी आवश्यकता होगी।

#### चरण 6: पोर्ट नंबर कॉन्फ़िगर करें

डिफ़ॉल्ट PostgreSQL पोर्ट `5432` है। आप डिफ़ॉल्ट उपयोग कर सकते हैं या आवश्यकता अनुसार अलग पोर्ट निर्दिष्ट कर सकते हैं।

!!! tip "सुझाव"

    यदि पोर्ट 5432 पहले ही उपयोग में है, तो एक वैकल्पिक पोर्ट चुनें और बाद में कॉन्फ़िगरेशन के लिए उसे नोट कर लें।

#### चरण 7: स्थानीयकरण (Locale) चुनें

अपने डेटाबेस के लिए लोकेल चुनें। अधिकांश इंस्टॉलेशन के लिए डिफ़ॉल्ट सामान्यतः उपयुक्त होता है।

#### चरण 8: इंस्टॉलेशन पूर्ण करें

बचे हुए चरणों में **Next** पर क्लिक करें, फिर **Finish** पर क्लिक करें।

#### चरण 9: इंस्टॉलेशन सत्यापित करें

Command Prompt खोलें और सत्यापित करें कि PostgreSQL इंस्टॉल हुआ है:

```bash
psql --version
```

यदि इंस्टॉलेशन सफल था तो आपको PostgreSQL संस्करण दिखाई देगा।

---

## वेब सर्वर कॉन्फ़िगरेशन {: #web-server-configuration }

digna को डैशबोर्ड होस्ट करने के लिए एक वेब सर्वर की आवश्यकता होती है। निम्नलिखित विकल्पों में से किसी एक को चुनें:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

आपको केवल इनमें से **एक** सर्वर इंस्टॉल और कॉन्फ़िगर करना होगा।

### IIS सेटअप {: #iis-setup }

#### अवलोकन

Internet Information Services (IIS) माइक्रोसॉफ्ट का वेब सर्वर है जो वेबसाइट्स और वेब एप्लिकेशन होस्ट करने के लिए उपयोग होता है।

#### IIS सक्षम करना

1. **Control Panel खोलें**
   - `Win + R` दबाएँ
   - टाइप करें `control` और Enter दबाएँ

2. **Windows Features पर जाएँ**
   - **Programs** पर क्लिक करें
   - **Turn Windows features on or off** चुनें

3. **Internet Information Services सक्षम करें**
   - नीचे स्क्रॉल करें और **Internet Information Services (IIS)** ढूँढें
   - इसे सक्षम करने के लिए चेकबॉक्स पर टिक करें
   - विस्तार के लिए **+** पर क्लिक करें और सुनिश्चित करें कि ये सबकंपोनेंट्स चुने गए हैं:
     - **Web Management Tools**
     - **World Wide Web Services**

4. परिवर्तन लागू करने के लिए **OK** पर क्लिक करें

5. **IIS इंस्टॉलेशन सत्यापित करें**
   - अपना ब्राउज़र खोलें
   - `http://localhost` पर जाएँ
   - आपको IIS Welcome पेज दिखाई देना चाहिए

#### आवश्यक: URL Rewrite मॉड्यूल

IIS के लिए URL Rewrite कंपोनेंट आवश्यक है। इसे [आधिकारिक Microsoft पेज](https://www.iis.net/downloads/microsoft/url-rewrite) से डाउनलोड और इंस्टॉल करें।

#### आवश्यक: Markdown फ़ाइलों के लिए MIME प्रकार

यह सुनिश्चित करने के लिए कि Markdown फ़ाइलें (`.md`) IIS द्वारा सही ढंग से सर्व हों:

1. **IIS Manager** खोलें ( `Win + R`, टाइप करें `inetmgr`, Enter दबाएँ )
2. **Your Site > MIME Types** पर नेविगेट करें
3. **Add...** पर क्लिक करें
4. कॉन्फ़िगर करें:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "महत्वपूर्ण"

    इस सेटिंग के बिना, `.md` फ़ाइलें सही ढंग से सर्व नहीं हो सकती हैं।

---

### Apache Tomcat सेटअप {: #apache-tomcat-setup }

#### अवलोकन

Apache Tomcat एक ओपन-सोर्स Java servlet कंटेनर और वेब सर्वर है।

#### इंस्टॉलेशन

1. **Apache Tomcat डाउनलोड करें**
   - [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi) पर जाएँ
   - Windows ZIP distribution डाउनलोड करें

2. **आर्काइव एक्सट्रैक्ट करें**
   - ZIP फ़ाइल को अपने सिस्टम की किसी डायरेक्टरी में एक्सट्रैक्ट करें
   - उदाहरण: `C:\Program Files\Apache Tomcat`

3. **Tomcat चल रहा है यह सत्यापित करें**
   - अपना ब्राउज़र खोलें
   - `http://localhost:8080` पर जाएँ
   - आपको Apache Tomcat welcome पेज दिखाई देना चाहिए

!!! tip "सुझाव"

    इंस्टॉलेशन के बाद Apache Tomcat सामान्यतः स्वतः शुरू हो जाता है। यदि ऐसा नहीं होता है, तो `bin` फ़ोल्डर में जाएँ और `startup.bat` चलाएँ।

---

## प्रारंभिक स्थापना {: #initial-installation }

### चरण 1: digna रिपॉज़िटरी सेट करें

digna रिपॉज़िटरी उन सभी मेट्रिक्स को संग्रहीत करती है जो digna द्वारा गणना किए जाते हैं। यह विश्लेषणात्मक और प्रदर्शन डेटा के लिए केंद्रीय डेटाबेस के रूप में कार्य करती है।

#### रिपॉज़िटरी स्कीमा और यूज़र बनाएं

अपना PostgreSQL क्लाइंट (pgAdmin, psql, या समान) खोलें और निम्न SQL कमांड्स चलाएँ:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**निम्न प्लेसहोल्डर्स बदलें:**

- `<digna_repo_schema>` — आपका वांछित स्कीमा नाम (उदा., `dignarepo`)
- `<digna_repo_user>` — आपका वांछित उपयोगकर्ता नाम (उदा., `digna_user`)
- `<digna_repo_password>` — इस उपयोगकर्ता के लिए एक सुरक्षित पासवर्ड

**उदाहरण:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "सर्वोत्तम अभ्यास"

    डेटाबेस उपयोगकर्ताओं के लिए मजबूत, जटिल पासवर्ड का उपयोग करें। आसानी से अनुमान लगाने योग्य क्रेडेंशियल्स से बचें।

---

### चरण 2: digna इंस्टॉलेशन पैकेज एक्सट्रैक्ट करें

1. आपको दिए गए digna इंस्टॉलेशन ZIP फ़ाइल का स्थान ढूँढें
2. इसे अपनी वांछित इंस्टॉलेशन लोकेशन में एक्सट्रैक्ट करें
3. एक्सट्रैक्शन के बाद आपको निम्न आइटम दिखाई देने चाहिए:
   - `dashboard/` — वेब डैशबोर्ड इंटरफ़ेस
   - `digna` — मुख्य executable (बैकएंड + CLI संयुक्त)
   - `config.toml` — कॉन्फ़िगरेशन फाइल
   - `license.toml` — लाइसेंस फ़ाइल (अपनी फ़ाइल यहाँ कॉपी करें)

### चरण 3: लाइसेंस फ़ाइल इंस्टॉल करें

!!! warning "महत्वपूर्ण"

    लाइसेंस फ़ाइल इंस्टॉलेशन पैकेज में शामिल नहीं होती और आपको अलग से digna द्वारा प्रदान की जाएगी।

1. आपको प्रदान की गई `license.toml` फ़ाइल खोजें
2. इसे digna इंस्टॉलेशन के रूट डायरेक्टरी में कॉपी करें (जहाँ `config.toml` और `digna` executable स्थित हैं)

**क्यों यह महत्वपूर्ण है:**
लाइसेंस फ़ाइल में आपका ग्राहक विवरण, लाइसेंस एक्सपायरी तिथि, और डिजिटल सिग्नेचर होती है। **इस फ़ाइल में बदलाव न करें** — किसी भी परिवर्तन से यह अमान्य हो जाएगी।

**सेटअप के बाद निर्देशिका संरचना:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## बैकएंड कॉन्फ़िगरेशन {: #backend-configuration }

### चरण 1: कॉन्फ़िगरेशन फ़ाइल बनाएं और संपादित करें

आपके digna इंस्टॉलेशन डायरेक्टरी में `config_template.toml` फ़ाइल दी गई है। आपको इसे केवल `config.toml` में नाम बदलने की आवश्यकता है।

**स्थान:** `digna_installation/config.toml`

`config.toml` को किसी टेक्स्ट एडिटर में खोलें और नीचे दिए गए प्रत्येक सेक्शन को कॉन्फ़िगर करें।

#### [app] सेक्शन

यह सेक्शन digna बैकएंड एप्लिकेशन सेटिंग्स को कॉन्फ़िगर करता है:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| पैरामीटर | मान | नोट्स |
|---|---|---|
| `digna_APP_HOST` | `localhost` या IP पता | वह होस्टनाम या IP जहाँ dignabackend होस्ट है |
| `digna_APP_PORT` | `8082` (डिफ़ॉल्ट) | REST API endpoints के लिए पोर्ट |
| `digna_APP_CORS_ALLOW_ORIGINS` | फ्रंटएंड URL | यदि डैशबोर्ड किसी अलग सर्वर पर है तो उसका URL शामिल करें |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | क्रेडेंशियल्स के साथ CORS के लिए आवश्यक |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | सभी HTTP मेथड्स की अनुमति दें |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | सभी हेडर्स की अनुमति दें |

#### [repo] सेक्शन

यह सेक्शन PostgreSQL डेटाबेस से कनेक्शन को कॉन्फ़िगर करता है:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| पैरामीटर | मान | नोट्स |
|---|---|---|
| `digna_REPO_HOST` | `localhost` या IP | PostgreSQL सर्वर होस्टनाम/IP |
| `digna_REPO_PORT` | `5432` (डिफ़ॉल्ट) | PostgreSQL पोर्ट |
| `digna_REPO_DB` | `postgres` | डेटाबेस नाम |
| `digna_REPO_SCHEMA` | `dignarepo` | पहले बनाया गया स्कीमा |
| `digna_REPO_USER` | `digna_user` | PostgreSQL सेटअप में बनाया गया उपयोगकर्ता |
| `digna_REPO_PASSWORD` | आपका पासवर्ड | स्कीमा निर्माण के दौरान सेट किया गया पासवर्ड |

#### [base] सेक्शन

यह सेक्शन सुरक्षा और कुकी सेटिंग्स रखता है:

```toml
[base]
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| पैरामीटर | मान | नोट्स |
|---|---|---|
| `digna_FERNET_KEY` | एन्क्रिप्शन की | टोकन और कुकीज़ को एन्क्रिप्ट करने के लिए उपयोग होती है (डिफ़ॉल्ट प्रदान किया गया) |
| `digna_COOKIE_DOMAIN` | `localhost` | अपने फ्रंटएंड डोमेन से मेल खड़ा करें |
| `digna_COOKIE_SECURE` | `false` (लोकल) / `true` (प्रोडक्शन) | HTTPS कनेक्शनों के लिए `true` का उपयोग करें |
| `digna_COOKIE_HTTPONLY` | `true` | सुरक्षा के लिए हमेशा सक्षम रखें |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF हमलों को रोकने में मदद करता है |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 घंटे) | सेकंड में सत्र टाइमआउट |
| `digna_MAX_WORKERS` | CPU कोर - 1 | समानांतर निरीक्षण कार्यों की संख्या |

#### [logging] सेक्शन

यह सेक्शन लॉगिंग व्यवहार को कॉन्फ़िगर करता है:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| पैरामीटर | मान | नोट्स |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` या `DEBUG` | प्रोडक्शन के लिए `INFO`, समस्या निवारण के लिए `DEBUG` |
| `digna_LOGGING_BACKUP_COUNT` | `10` | प्रतिदिन के लॉग बैकअप की संख्या जिसे रखा जाएगा |

---

### चरण 3: रिपॉज़िटरी इनिशियलाइज़ करें

1. Command Prompt खोलें
2. अपने digna इंस्टॉलेशन डायरेक्टरी में नेविगेट करें (जहाँ `config.toml` और `digna` executable स्थित हैं)
3. कनेक्शन टेस्ट चलाएँ:

```bash
digna repo check
```

आपको पुष्टि दिखनी चाहिए कि कनेक्शन स्थापित है (रिपॉज़िटरी अभी तक इनिशियलाइज़ नहीं की गई है)।

### चरण 4: रिपॉज़िटरी स्कीमा इंस्टॉल करें

उसी डायरेक्टरी में चलाएँ:

```bash
digna repo install
```

यह कमांड आपके PostgreSQL डेटाबेस में आवश्यक तालिकाएँ और स्कीमा इंस्टॉल कर देती है।

### चरण 5: digna सर्वर शुरू करें

digna इंस्टॉलेशन डायरेक्टरी में, सर्वर शुरू करें:

```bash
digna serve --address <host> --port <port>
```

**पैरामीटर:**
- `--address` — सर्वर होस्टनाम/IP
- `--port` — सर्वर पोर्ट 

आपको स्टार्टअप संदेश दिखाई देने चाहिए जो सर्वर चलने की पुष्टि करें:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### चरण 6: एक एडमिन यूज़र बनाएं

1. एक **नया** Command Prompt विंडो खोलें
2. अपने digna इंस्टॉलेशन डायरेक्टरी में नेविगेट करें
3. एक एडमिन यूज़र बनाने के लिए निम्न कमांड चलाएँ:

```bash
digna user add <username> "<full_name>" <password> --su
```

**उदाहरण:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

यह पूरा प्रशासनिक अधिकारों वाला उपयोगकर्ता बना देगा।

!!! tip "सर्वोत्तम अभ्यास"

    ऊपरी-निचले अक्षर, संख्याएँ और विशेष वर्णों का मिश्रण करके मजबूत पासवर्ड का उपयोग करें।

---

## डैशबोर्ड कॉन्फ़िगरेशन {: #dashboard-configuration }

### चरण 1: डैशबोर्ड को वेब सर्वर पर तैनात करें

digna डैशबोर्ड की अपनी अलग `config.toml` फ़ाइल `dashboard/` डायरेक्टरी में स्थित है। यह कॉन्फ़िगरेशन पहले से प्रदान की गई है और प्रारंभिक सेटअप के दौरान बदलाव की आवश्यकता नहीं होती। केवल तब कॉन्फ़िगर करें जब बैकएंड कनेक्शन को कस्टमाइज़ करने की आवश्यकता हो।

यदि आपको डैशबोर्ड कॉन्फ़िगरेशन संशोधित करने की आवश्यकता है (उदा., मल्टी-इंस्टेंस तैनाती के लिए), तो डैशबोर्ड के डॉ큐मेंटेशन का संदर्भ लें।

अपना वेब सर्वर चुनें और संबंधित तैनाती चरणों का पालन करें।

#### IIS पर डिप्लॉय करना

1. **IIS Manager खोलें**
   - `Win + R` दबाएँ, टाइप करें `inetmgr`, Enter दबाएँ

2. **नई वेबसाइट बनाएं**
   - बाएँ पैनल में, **Sites** पर राइट-क्लिक करें
   - **Add Website...** चुनें

3. **वेबसाइट कॉन्फ़िगर करें**
   - **Site Name**: एक नाम दर्ज करें (उदा., "dignaDashboard")
   - **Physical Path**: Browse पर क्लिक करें और अपनी `dashboard` फ़ोल्डर चुनें
   - **Binding**: IP पता और पोर्ट सेट करें (HTTP के लिए डिफ़ॉल्ट पोर्ट 80, HTTPS के लिए 443)

4. **वेबसाइट शुरू करें**
   - साइट बनाने के लिए **OK** पर क्लिक करें
   - नई साइट पर राइट-क्लिक करें और **Start** चुनें

5. **इंस्टॉलेशन परीक्षण करें**
   - अपना ब्राउज़र खोलें
   - `http://localhost` (या आपका कॉन्फ़िगर किया गया URL) पर जाएँ
   - आपको digna डैशबोर्ड लॉगिन पेज दिखाई देना चाहिए

#### Apache Tomcat पर डिप्लॉय करना

1. **डैशबोर्ड को Tomcat में कॉपी करें**
   - `dashboard` फ़ोल्डर को अपने Tomcat `webapps` डायरेक्टरी में कॉपी करें
   - आवश्यकता अनुसार नाम बदलें (उदा., `digna`)
   - उदाहरण: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **तैनाती सत्यापित करें**
   - Tomcat प्रबंधन पेज (http://localhost:8080) को रिफ्रेश या रीलोड करें
   - आप "digna" (या आपने जो नाम चुना है) को सूचीबद्ध एप्लीकेशन्स में देखेंगे

3. **डैशबोर्ड एक्सेस करें**
   - अपना ब्राउज़र खोलें
   - `http://localhost:8080/digna` पर जाएँ
   - आपको digna डैशबोर्ड लॉगिन पेज दिखाई देना चाहिए

---

## digna को Windows सेवा के रूप में चलाना {: #running-digna-as-a-windows-service }

### Windows सेवा क्यों उपयोग करें?

digna बैकएंड को Windows सेवा के रूप में चलाने से यह सुनिश्चित होता है कि यह:
- सर्वर बूट होने पर स्वचालित रूप से शुरू हो जाए
- बैकग्राउंड में खुले Command Prompt के बिना चले
- क्रैश होने पर स्वतः पुनरारंभ हो सके
- Windows Services के माध्यम से प्रबंधित किया जा सके

### सेवा प्रबंधन फाइलें

सभी आवश्यक फाइलें digna इंस्टॉलेशन डायरेक्टरी के अंतर्गत: `bin/` में स्थित हैं।

निम्न बैच फ़ाइलें उपलब्ध हैं:
- `install_service.bat` — digna को Windows सेवा के रूप में रजिस्टर करता है
- `uninstall_service.bat` — सेवा को अनरजिस्टर करता है
- `start_service.bat` — चल रही सेवा को शुरू करता है
- `stop_service.bat` — चल रही सेवा को रोकता है

!!! warning "प्रशासक आवश्यक"

    सभी बैच फ़ाइलों को Administrator विशेषाधिकारों के साथ चलाना आवश्यक है।

### सेवा स्थापित करना

1. **Command Prompt को Administrator के रूप में खोलें**
   - Command Prompt पर राइट-क्लिक करें
   - "Run as Administrator" चुनें

2. **bin फ़ोल्डर में नेविगेट करें**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **इंस्टॉलेशन स्क्रिप्ट चलाएँ**
   ```bash
   install_service.bat
   ```

अब digna सर्वर Windows सेवा के रूप में रजिस्टर हो गया है और **स्वचालित स्टार्टअप** सक्षम है। सेवा तुरंत शुरू नहीं होगी — इसे शुरू करने के लिए अगले अनुभाग देखें।

### सेवा शुरू करना और रोकना

#### सेवा शुरू करने के लिए

1. Command Prompt को Administrator के रूप में खोलें
2. `digna\bin` में नेविगेट करें
3. चलाएँ:
   ```bash
   start_service.bat
   ```

#### सेवा रोकने के लिए

1. Command Prompt को Administrator के रूप में खोलें
2. `digna\bin` में नेविगेट करें
3. चलाएँ:
   ```bash
   stop_service.bat
   ```

!!! tip "सुझाव"

    आवेदन फ़ाइलों को अपडेट करने से पहले हमेशा सेवा को रोकें।

### सेवा को नई डायरेक्टरी में ले जाना

यदि आपको digna इंस्टॉलेशन को स्थानांतरित करने की आवश्यकता है:

1. **वर्तमान सेवा अनइंस्टॉल करें**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **एप्लिकेशन फाइलें स्थानांतरित करें**
   - पूरी digna इंस्टॉलेशन फ़ोल्डर को नई लोकेशन पर ले जाएँ

3. **सेवा पुनः इंस्टॉल करें**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **सेवा शुरू करें**
   ```bash
   start_service.bat
   ```

### सेवा अनइंस्टॉल करना

1. **चलती सेवा को रोकें**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **सेवा अनइंस्टॉल करें**
   ```bash
   uninstall_service.bat
   ```

अब digna सर्वर Windows सेवा के रूप में अनरजिस्टर हो चुका है।

---

## नई रिलीज़ में उन्नयन {: #upgrading-to-a-new-release }

### उन्नयन से पहले

**digna रिपॉज़िटरी का बैकअप बनाना अनिवार्य है**

digna को अपग्रेड करने से पहले अपने रिपॉज़िटरी (PostgreSQL) का बैकअप लें ताकि डेटा लॉस से बचा जा सके।
एक बैकअप यह सुनिश्चित करता है कि यदि उन्नयन के दौरान अनपेक्षित समस्याएँ आएँ तो आप रिकवर कर सकें।

### उन्नयन प्रक्रिया

#### चरण 1: digna सेवा रोकें

यदि digna Windows सेवा के रूप में चल रहा है, तो पहले उसे रोकें:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### चरण 2: वर्तमान बैकएंड इंस्टॉलेशन का बैकअप लें

अपने digna इंस्टॉलेशन डायरेक्टरी में:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### चरण 3: नई संस्करण निकालें और तैनात करें

1. नए digna इंस्टॉलेशन ZIP फ़ाइल को एक्सट्रैक्ट करें
2. नई `digna` executable और `dashboard` फ़ोल्डर को अपनी इंस्टॉलेशन डायरेक्टरी में कॉपी करें


!!! warning "महत्वपूर्ण"

    `config.toml` फ़ाइल कभी भी इंस्टॉलेशन ZIP में शामिल नहीं होती। आपकी मौजूदा कॉन्फ़िगरेशन सुरक्षित रहती है।

### चरण 4: अपनी कॉन्फ़िगरेशन फ़ाइलें पुनर्स्थापित करें

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### चरण 5: रिपॉज़िटरी स्कीमा अपग्रेड करें

अपने digna इंस्टॉलेशन डायरेक्टरी में नेविगेट करें और चलाएँ:

```bash
digna repo upgrade
```

यह PostgreSQL स्कीमा को नवीनतम संस्करण में अपडेट करता है जबकि सभी मौजूदा डेटा को सुरक्षित रखता है।

### चरण 6: सेवाएँ पुनरारंभ करें

यदि आप Windows सेवा के रूप में चला रहे हैं:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

यदि आप मैन्युअली चला रहे हैं, तो सर्वर को फिर से शुरू करें:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

यदि आप IIS या Tomcat का उपयोग कर रहे हैं, तो संबंधित वेब सर्वर को पुनरारंभ करें।

#### चरण 7: उन्नयन सत्यापित करें

1. digna डैशबोर्ड एक्सेस करें
2. सत्यापित करें कि इंटरफ़ेस सही ढंग से लोड हो रहा है
3. किसी भी त्रुटि के लिए सर्वर लॉग्स जांचें