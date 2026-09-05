# Windows इंस्टॉलेशन गाइड के लिए digna Release 2026.06

**Release:** 2026.06

**Last Updated:** August 30, 2026


---

## सामग्री की तालिका

1. [परिचय](#introduction)
2. [सिस्टम आवश्यकताएँ](#system-requirements)
3. [पूर्व-स्थापना सेटअप](#pre-installation-setup)
4. [PostgreSQL सर्वर सेटअप](#postgresql-server-setup)
5. [वेब सर्वर कॉन्फ़िगरेशन](#web-server-configuration)
6. [प्रारंभिक इंस्टॉलेशन](#initial-installation)
7. [बैकएंड कॉन्फ़िगरेशन](#backend-configuration)
8. [डैशबोर्ड कॉन्फ़िगरेशन](#dashboard-configuration)
9. [digna को Windows सेवा के रूप में चलाना](#running-digna-as-a-windows-service)
10. [नए रिलीज़ में अपग्रेड करना](#upgrading-to-a-new-release)

---

## परिचय {: #introduction }

### digna के बारे में

digna एक व्यापक AI-आधारित प्लेटफ़ॉर्म है जो वेयरहाउस, लेक्स और लेकहाउस जैसे विभिन्न डेटा वातावरणों में डेटा गुणवत्ता प्रबंधन को अनुकूलित करने के लिए डिज़ाइन किया गया है। यह अत्यधिक स्केलेबल और अनुकूलनीय बनाने के लिए निर्मित है और ऑटोमेशन, वास्तविक-समय मॉनिटरिंग, और अनॉमली डिटेक्शन के माध्यम से आधुनिक डेटा चुनौतियों को संबोधित करता है।

digna दो मुख्य घटकों से मिलकर बनता है:

- **dignabackend**: एप्लिकेशन का मुख्य इंजन, जो डेटा प्रोसेसिंग और गुणवत्ता जाँच करने के लिए ज़िम्मेदार है।
- **dignadashboard**: एक वेब-आधारित इंटरफ़ेस जो वेब सर्वर पर होस्ट होता है और digna प्लेटफ़ॉर्म के साथ इंटरैक्ट करने और डेटा गुणवत्ता मेट्रिक्स को विज़ुअलाइज़ करने का यूज़र-फ्रेंडली तरीका प्रदान करता है।

### Release 2026.06 में क्या नया है

यह रिलीज़ डेटा ऑब्ज़र्वेबिलिटी क्षमताओं को सीधे आपके कोड में लाती है, जिससे डेवलपर स्रोत पर ही डेटा गुणवत्ता मॉनिटर कर सकते हैं। पूर्ण विवरण के लिए [release notes](http://docs.digna.ai/changelog/Release_202606/) देखें।

---

## सिस्टम आवश्यकताएँ {: #system-requirements }

इंस्टॉलेशन शुरू करने से पहले, सुनिश्चित करें कि आपका सिस्टम निम्न न्यूनतम आवश्यकताओं को पूरा करता है:

| Requirement | Specification |
|---|---|
| **Operating System** | Windows Server या Windows 10/11 |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB उपलब्ध स्टोरेज |
| **Database** | PostgreSQL Server 12 या उससे ऊपर |
| **Web Server** | IIS, Apache Tomcat, या समतुल्य |

### डेटाबेस इंस्टॉलेशन विकल्प

**यदि PostgreSQL पहले से इंस्टॉल है:**
आप अपने मौजूदा PostgreSQL Server में digna के लिए एक नया डेटाबेस जोड़ सकते हैं।

**यदि आप उसी मशीन पर PostgreSQL इंस्टॉल कर रहे हैं जहाँ digna चलेगा:**

!!! info "Recommended Specifications"

    - **Memory**: 32 GB RAM (16 GB के बजाय)
    - **Disk Space**: 50 GB उपलब्ध स्टोरेज (10 GB के बजाय)

    ये उच्च विशिष्टताएँ दोनों, digna और PostgreSQL डेटाबेस को एक साथ चलाने के लिए उपयुक्त हैं।

---

## पूर्व-स्थापना सेटअप {: #pre-installation-setup }

digna इंस्टॉल करने से पहले, सुनिश्चित करें कि दो मुख्य पूर्वापेक्षाएँ मौजूद हैं:

1. **PostgreSQL Server** – यानी गणना किए गए मेट्रिक्स और प्रदर्शन डेटा को स्टोर करने के लिए
2. **Web Server** – digna Dashboard को होस्ट करने के लिए

यदि ये घटक पहले से सेटअप नहीं हैं, तो उन्हें इंस्टॉल और कॉन्फ़िगर करने के लिए नीचे के सेक्शनों का पालन करें।

---

## PostgreSQL सर्वर सेटअप {: #postgresql-server-setup }

### यदि आपके पास पहले से PostgreSQL है

यदि PostgreSQL पहले से आपके लोकल मशीन पर इंस्टॉल और चल रहा है या आप किसी प्रबंधित रिमोट PostgreSQL सर्वर का उपयोग कर रहे हैं, तो आप [अगले सेक्शन](#web-server-configuration) पर जा सकते हैं।

### PostgreSQL इंस्टॉल करना

Windows पर PostgreSQL इंस्टॉल करने के लिए इन चरणों का पालन करें:

#### चरण 1: PostgreSQL डाउनलोड करें

1. [PostgreSQL Downloads page](https://www.postgresql.org/download/) पर जाएँ
2. **Windows** चुनें
3. नवीनतम इंस्टॉलर डाउनलोड करें

#### चरण 2: इंस्टॉलर चलाएँ

1. डाउनलोड किए गए इंस्टॉलर फ़ाइल पर डबल-क्लिक करें
2. सेटअप विज़ार्ड में दिए गए संकेतों का पालन करें

#### चरण 3: इंस्टॉलेशन डायरेक्टरी चुनें

उस डायरेक्टरी का चयन करें जहां PostgreSQL इंस्टॉल होगा। डिफ़ॉल्ट स्थान सामान्यतः उपयुक्त होता है।

#### चरण 4: घटक चुनें

स्टैंडर्ड सेटअप के लिए डिफ़ॉल्ट कंपोनेंट विकल्पों को बनाए रखें।

#### चरण 5: PostgreSQL सुपरयूज़र पासवर्ड सेट करें

PostgreSQL सुपरयूज़र (`postgres`) के लिए एक पासवर्ड दर्ज करें और पुष्टि करें। **इस पासवर्ड को सुरक्षित रूप से सहेजें** — आपको बाद में इसकी आवश्यकता होगी।

#### चरण 6: पोर्ट नंबर कॉन्फ़िगर करें

डिफ़ॉल्ट PostgreSQL पोर्ट `5432` है। आप डिफ़ॉल्ट का उपयोग कर सकते हैं या आवश्यकता अनुसार अलग पोर्ट निर्दिष्ट कर सकते हैं।

!!! tip "Tip"

    यदि पोर्ट 5432 पहले से उपयोग में है, तो एक वैकल्पिक पोर्ट चुनें और बाद में कॉन्फ़िगरेशन के लिए उसे नोट कर लें।

#### चरण 7: लोकेल चुनें

अपने डेटाबेस के लिए लोकेल चुनें। अधिकांश इंस्टॉलेशनों के लिए डिफ़ॉल्ट उपयुक्त होता है।

#### चरण 8: इंस्टॉलेशन पूरा करें

बाकी चरणों में **Next** पर क्लिक करते जाएँ, फिर **Finish** पर क्लिक करें।

#### चरण 9: इंस्टॉलेशन सत्यापित करें

Command Prompt खोलें और सत्यापित करें कि PostgreSQL इंस्टॉल हुआ है:

```bash
psql --version
```

यदि इंस्टॉलेशन सफल रहा है तो आपको PostgreSQL संस्करण दिखेगा।

---

## वेब सर्वर कॉन्फ़िगरेशन {: #web-server-configuration }

digna को डैशबोर्ड होस्ट करने के लिए एक वेब सर्वर की आवश्यकता है। निम्नलिखित विकल्पों में से किसी एक को चुनें:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

आपको केवल इन में से **एक** सर्वर इंस्टॉल और कॉन्फ़िगर करना होगा।

### IIS सेटअप {: #iis-setup }

#### अवलोकन

Internet Information Services (IIS) Microsoft का वेब सर्वर है जो वेबसाइट्स और वेब एप्लिकेशन होस्ट करने के लिए उपयोग होता है।

#### IIS सक्षम करना

1. **Control Panel खोलें**
   - `Win + R` दबाएँ
   - टाइप करें `control` और Enter दबाएँ

2. **Windows Features पर जाएँ**
   - **Programs** पर क्लिक करें
   - **Turn Windows features on or off** चुनें

3. **Internet Information Services सक्षम करें**
   - नीचे स्क्रॉल करें और **Internet Information Services (IIS)** खोजें
   - इसे सक्षम करने के लिए चेकबॉक्स चेक करें
   - **+** पर क्लिक कर उपघटक चयन की पुष्टि करें:
     - **Web Management Tools**
     - **World Wide Web Services**

4. परिवर्तन लागू करने के लिए **OK** पर क्लिक करें

5. **IIS इंस्टॉलेशन सत्यापित करें**
   - अपना ब्राउज़र खोलें
   - `http://localhost` पर नेविगेट करें
   - आपको IIS Welcome पेज दिखाई देना चाहिए

#### आवश्यक: URL Rewrite मॉड्यूल

IIS को URL Rewrite कॉम्पोनेंट की आवश्यकता है। इसे [official Microsoft page](https://www.iis.net/downloads/microsoft/url-rewrite) से डाउनलोड और इंस्टॉल करें।

#### आवश्यक: Markdown फ़ाइलों के लिए MIME टाइप

यह सुनिश्चित करने के लिए कि Markdown फ़ाइलें (`.md`) IIS द्वारा ठीक से सर्व हों:

1. **IIS Manager** खोलें ( `Win + R`, टाइप करें `inetmgr`, Enter दबाएँ )
2. **Your Site > MIME Types** पर नेविगेट करें
3. **Add...** पर क्लिक करें
4. कॉन्फ़िगर करें:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Important"

    इस सेटिंग के बिना, `.md` फ़ाइलें सही तरीके से सर्व नहीं हो सकती हैं।

---

### Apache Tomcat सेटअप {: #apache-tomcat-setup }

#### अवलोकन

Apache Tomcat एक ओपन-सोर्स Java servlet कंटेनर और वेब सर्वर है।

#### इंस्टॉलेशन

1. **Apache Tomcat डाउनलोड करें**
   - [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi) पर जाएँ
   - Windows ZIP वितरण डाउनलोड करें

2. **आर्काइव को एक्स्ट्रैक्ट करें**
   - ZIP फ़ाइल को अपने सिस्टम पर किसी डायरेक्टरी में एक्सट्रैक्ट करें
   - उदाहरण: `C:\Program Files\Apache Tomcat`

3. **Tomcat चलने की पुष्टि करें**
   - अपना ब्राउज़र खोलें
   - `http://localhost:8080` पर नेविगेट करें
   - आपको Apache Tomcat का welcome पेज दिखाई देना चाहिए

!!! tip "Tip"

    Apache Tomcat आम तौर पर इंस्टॉलेशन के बाद स्वतः प्रारंभ हो जाता है। यदि यह नहीं होता है, तो `bin` फ़ोल्डर में जाकर `startup.bat` चलाएँ।

---

## प्रारंभिक इंस्टॉलेशन {: #initial-installation }

### चरण 1: digna Repository सेट करें

digna रिपॉज़िटरी उन सभी मेट्रिक्स को स्टोर करती है जो digna द्वारा गणना की जाती हैं। यह एनालिटिकल और प्रदर्शन डेटा के लिए केंद्रीय डेटाबेस के रूप में कार्य करती है।

#### रिपॉज़िटरी स्कीमा और उपयोगकर्ता बनाएं

अपने PostgreSQL क्लाइंट (pgAdmin, psql, या समान) खोलें और निम्न SQL कमांड्स निष्पादित करें:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**निम्न प्लेसहोल्डर्स को बदलें:**

- `<digna_repo_schema>` — आपकी इच्छित स्कीमा का नाम (उदा., `dignarepo`)
- `<digna_repo_user>` — आपकी इच्छित यूज़रनेम (उदा., `digna_user`)
- `<digna_repo_password>` — इस यूज़र के लिए एक सुरक्षित पासवर्ड

**उदाहरण:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Best Practice"

    डेटाबेस यूज़र्स के लिए मजबूत, जटिल पासवर्ड का उपयोग करें। आसानी से अनुमान लगाने योग्य क्रेडेंशियल्स से बचें।

---

### चरण 2: digna इंस्टॉलेशन पैकेज एक्स्ट्रैक्ट करें

1. आपको प्रदान किए गए digna इंस्टॉलेशन ZIP फ़ाइल का स्थान तलाशें
2. इसे अपनी इच्छित इंस्टॉलेशन लोकेशन पर एक्स्ट्रैक्ट करें
3. एक्स्ट्रैक्शन के बाद, आपको निम्न आइटम दिखाई देने चाहिए:
   - `dashboard/` — वेब डैशबोर्ड इंटरफ़ेस
   - `digna` — मुख्य executable (backend + CLI सम्मिलित)
   - `config.toml` — कॉन्फ़िगरेशन फ़ाइल
   - `license.toml` — लाइसेंस फ़ाइल (अपना कॉपी यहाँ रखें)

### चरण 3: लाइसेंस फ़ाइल इंस्टॉल करें

!!! warning "Important"

    लाइसेंस फ़ाइल इंस्टॉलेशन पैकेज में **शामिल नहीं** होती और digna द्वारा अलग से प्रदान की जाएगी।

1. आपको प्रदान की गई `license.toml` फ़ाइल खोजें
2. इसे digna इंस्टॉलेशन की रूट डायरेक्टरी में कॉपी करें (जहाँ `config.toml` और `digna` executable होते हैं)

**क्यों यह महत्वपूर्ण है:**
लाइसेंस फ़ाइल में आपका ग्राहक जानकारी, लाइसेंस समाप्ति तिथि और डिजिटल सिग्नेचर शामिल होता है। **इस फ़ाइल में कोई परिवर्तन न करें** — किसी भी परिवर्तन से यह अमान्य हो जाएगी।

**सेटअप के बाद डायरेक्टरी संरचना:**

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

### चरण 1: कॉन्फ़िगरेशन फ़ाइल बनाएँ और संपादित करें

आपके digna इंस्टॉलेशन डायरेक्टरी में `config_template.toml` फ़ाइल प्रदान की जाती है। आपको केवल इसे `config.toml` में नाम बदलने की आवश्यकता है।

**स्थान:** `digna_installation/config.toml`

`config.toml` को किसी टेक्स्ट एडिटर में खोलें और नीचे दिए गए प्रत्येक सेक्शन को कॉन्फ़िगर करें।

#### [app] सेक्शन

यह सेक्शन digna backend एप्लिकेशन सेटिंग्स को कॉन्फ़िगर करता है:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_APP_HOST` | `localhost` या IP पता | Hostname या IP जहाँ dignabackend होस्ट है |
| `digna_APP_PORT` | `8082` (डिफ़ॉल्ट) | REST API endpoints के लिए पोर्ट |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend URL | यदि dashboard अलग सर्वर पर है तो उसकी URL शामिल करें |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | क्रेडेंशियल्स के साथ CORS के लिए आवश्यक |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | सभी HTTP मेथड्स की अनुमति देता है |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | सभी हेडर्स की अनुमति देता है |

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

| Parameter | Value | Notes |
|---|---|---|
| `digna_REPO_HOST` | `localhost` या IP | PostgreSQL सर्वर hostname/IP |
| `digna_REPO_PORT` | `5432` (डिफ़ॉल्ट) | PostgreSQL पोर्ट |
| `digna_REPO_DB` | `postgres` | डेटाबेस नाम |
| `digna_REPO_SCHEMA` | `dignarepo` | पहले बनाई गई स्कीमा |
| `digna_REPO_USER` | `digna_user` | PostgreSQL सेटअप में बनाया गया यूज़र |
| `digna_REPO_PASSWORD` | आपका पासवर्ड | स्कीमा क्रिएशन के दौरान सेट किया गया पासवर्ड |

#### [base] सेक्शन

यह सेक्शन सुरक्षा और कुकी सेटिंग्स को समाहित करता है:

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

| Parameter | Value | Notes |
|---|---|---|
| `digna_FERNET_KEY` | Encryption key | टोकन और कुकीज़ को एन्क्रिप्ट करने के लिए उपयोग होता है (default उपलब्ध) |
| `digna_COOKIE_DOMAIN` | `localhost` | अपने frontend डोमेन से मेल खाएँ |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (production) | HTTPS कनेक्शन्स के लिए `true` का उपयोग करें |
| `digna_COOKIE_HTTPONLY` | `true` | सुरक्षा के लिए हमेशा सक्षम रखें |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF हमलों को रोकता है |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 घंटे) | सेकंड में सेशन समय-सीमा |
| `digna_MAX_WORKERS` | CPU कोर की संख्या - 1 | समानांतर निरीक्षण कार्यों की संख्या |

#### [logging] सेक्शन

यह सेक्शन लॉगिंग व्यवहार को कॉन्फ़िगर करता है:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` या `DEBUG` | प्रोडक्शन के लिए `INFO`, ट्रबलशूटिंग के लिए `DEBUG` |
| `digna_LOGGING_BACKUP_COUNT` | `10` | प्रतिदिन की लॉग बैकअप फाइल्स की संख्या जो रखी जाएँगी |

---

### चरण 3: रिपॉज़िटरी इनिशियलाइज़ करें

1. Command Prompt खोलें
2. अपने digna इंस्टॉलेशन डायरेक्टरी पर नेविगेट करें (जहाँ `config.toml` और `digna` executable मौज़ूद हैं)
3. कनेक्शन टेस्ट चलाएँ:

```bash
digna repo check
```

आपको पुष्टि दिखनी चाहिए कि कनेक्शन स्थापित हो गया है (रिपॉज़िटरी स्वयं अभी इनिशियलाइज़ नहीं हुई है)।

### चरण 4: रिपॉज़िटरी स्कीमा इंस्टॉल करें

उसी डायरेक्टरी में चलाएँ:

```bash
digna repo install
```

यह कमांड आपके PostgreSQL डेटाबेस में आवश्यक तालिकाएँ और स्कीमा इंस्टॉल कर देता है।

### चरण 5: digna सर्वर शुरू करें

digna इंस्टॉलेशन डायरेक्टरी में, सर्वर शुरू करने के लिए चलाएँ:

```bash
digna serve --address <host> --port <port>
```

**पैरामीटर्स:**
- `--address` — सर्वर hostname/IP
- `--port` — सर्वर पोर्ट

आपको स्टार्टअप संदेश दिखाई देने चाहिए जो पुष्टि करते हों कि सर्वर चल रहा है:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### चरण 6: एक Admin यूज़र बनाएं

1. एक नया Command Prompt विंडो खोलें
2. अपने digna इंस्टॉलेशन डायरेक्टरी पर नेविगेट करें
3. एक admin यूज़र बनाने के लिए निम्न कमांड चलाएँ:

```bash
digna user add <username> "<full_name>" <password> --su
```

**उदाहरण:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

यह एक उपयोगकर्ता बनाता है जिसके पास पूर्ण प्रशासनिक अधिकार होंगे।

!!! tip "Best Practice"

    अपरकेस, लोअरकेस, नंबर और स्पेशल कैरेक्टर्स का मिश्रण करके एक मजबूत पासवर्ड उपयोग करें।

---

## डैशबोर्ड कॉन्फ़िगरेशन {: #dashboard-configuration }

### चरण 1: डैशबोर्ड को वेब सर्वर पर डिप्लॉय करें

digna डैशबोर्ड का अपना अलग `config.toml` फाइल `dashboard/` डायरेक्टरी में स्थित है। यह कॉन्फ़िगरेशन पहले से प्रदान किया गया है और प्रारंभिक सेटअप के दौरान परिवर्तन की आवश्यकता नहीं है। केवल तब बदलें यदि आपको बैकएंड कनेक्शन को कस्टमाइज़ करने की आवश्यकता हो।

यदि आपको डैशबोर्ड कॉन्फ़िगरेशन संशोधित करने की जरूरत है (उदा., मल्टी-इंस्टेंस तैनाती के लिए), तो डैशबोर्ड के दस्तावेज़ीकरण को देखें।

अपने वेब सर्वर चुनें और संबंधित तैनाती चरणों का पालन करें।

#### IIS पर डिप्लॉय करना

1. **IIS Manager खोलें**
   - `Win + R` दबाएँ, टाइप करें `inetmgr`, Enter दबाएँ

2. **नया Website बनाएं**
   - बाएँ पैनल में, **Sites** पर राइट-क्लिक करें
   - **Add Website...** चुनें

3. **Website कॉन्फ़िगर करें**
   - **Site Name**: एक नाम दर्ज करें (उदा., "dignaDashboard")
   - **Physical Path**: Browse पर क्लिक कर अपने `dashboard` फ़ोल्डर का चयन करें
   - **Binding**: IP पता और पोर्ट सेट करें (HTTP के लिए डिफ़ॉल्ट पोर्ट 80, HTTPS के लिए 443)

4. **Website शुरू करें**
   - साइट बनाने के लिए **OK** पर क्लिक करें
   - नई साइट पर राइट-क्लिक करें और **Start** चुनें

5. **इंस्टॉलेशन का परीक्षण करें**
   - अपना ब्राउज़र खोलें
   - `http://localhost` (या आपका कॉन्फ़िगर किया गया URL) पर नेविगेट करें
   - आपको digna डैशबोर्ड लॉगिन पेज दिखाई देना चाहिए

#### Apache Tomcat पर डिप्लॉय करना

1. **Dashboard को Tomcat में कॉपी करें**
   - `dashboard` फ़ोल्डर को अपने Tomcat `webapps` डायरेक्टरी में कॉपी करें
   - यदि आवश्यक हो तो नाम बदलें (उदा., `digna`)
   - उदाहरण: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **डिप्लॉयमेंट सत्यापित करें**
   - Tomcat प्रबंधन पेज (http://localhost:8080) को रिफ्रेश या रीलोड करें
   - आपको "digna" (या आपका चुना गया नाम) लिस्टेड दिखाई देना चाहिए

3. **डैशबोर्ड एक्सेस करें**
   - अपना ब्राउज़र खोलें
   - `http://localhost:8080/digna` पर नेविगेट करें
   - आपको digna डैशबोर्ड लॉगिन पेज दिखाई देना चाहिए

---

## digna को Windows सेवा के रूप में चलाना {: #running-digna-as-a-windows-service }

### Windows सेवा का उपयोग क्यों करें?

digna बैकएंड को Windows सेवा के रूप में चलाने से यह सुनिश्चित होता है कि यह:
- सर्वर बूट होने पर स्वचालित रूप से शुरू हो
- बैकग्राउंड में खुले Command Prompt के बिना चले
- क्रैश होने पर स्वतः पुनः शुरू हो सके
- Windows Services के माध्यम से मैनेज किया जा सके

### सेवा प्रबंधन फाइलें

सभी आवश्यक फ़ाइलें digna इंस्टॉलेशन डायरेक्टरी के अंदर: `bin/` में स्थित हैं।

उपलब्ध बैच फ़ाइलें:
- `install_service.bat` — digna को Windows सेवा के रूप में रजिस्टर करता है
- `uninstall_service.bat` — सेवा का अनरजिस्टर करता है
- `start_service.bat` — चलती सेवा को शुरू करता है
- `stop_service.bat` — चलती सेवा को रोकता है

!!! warning "Administrator Required"

    सभी बैच फ़ाइलें Administrator विशेषाधिकारों के साथ चलानी होंगी।

### सेवा इंस्टॉल करना

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

digna सर्वर अब Windows सेवा के रूप में रजिस्टर हो चुका है और **automatic startup** सक्षम है। सेवा तुरंत शुरू नहीं होती — इसे शुरू करने के लिए अगले सेक्शन देखें।

### सेवा शुरू और रोकना

#### सेवा शुरू करने के लिए

1. Command Prompt को Administrator के रूप में खोलें
2. `digna\bin` पर नेविगेट करें
3. चलाएँ:
   ```bash
   start_service.bat
   ```

#### सेवा रोकने के लिए

1. Command Prompt को Administrator के रूप में खोलें
2. `digna\bin` पर नेविगेट करें
3. चलाएँ:
   ```bash
   stop_service.bat
   ```

!!! tip "Tip"

    एप्लिकेशन फाइल्स को अपडेट करने से पहले हमेशा सेवा को रोकें।

### सेवा को नई डायरेक्टरी में मूव करना

यदि आपको digna इंस्टॉलेशन को स्थानांतरित करने की आवश्यकता है:

1. **मौजूदा सेवा अनइंस्टॉल करें**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **एप्लिकेशन फाइल्स को मूव करें**
   - पूरे digna इंस्टॉलेशन फ़ोल्डर को नई लोकेशन पर मूव करें

3. **सेवा री-इंस्टॉल करें**
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

digna सर्वर अब Windows सेवा के रूप में अनरजिस्टर हो चुका है।

---

## नए रिलीज़ में अपग्रेड करना {: #upgrading-to-a-new-release }

### अपग्रेड करने से पहले

**digna Repository का बैकअप बनाना अनिवार्य है**

digna को अपग्रेड करने से पहले अपने रिपॉज़िटरी (PostgreSQL) का बैकअप लें ताकि डेटा लॉस से बचा जा सके।
एक बैकअप सुनिश्चित करता है कि यदि अपग्रेड के दौरान कोई अनपेक्षित समस्या आए तो आप डेटा रिकवर कर सकें।

### अपग्रेड प्रक्रिया

#### चरण 1: digna सेवा को रोकें

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

#### चरण 3: नई संस्करण निकालें और डिप्लॉय करें

1. नए digna इंस्टॉलेशन ZIP फ़ाइल को एक्स्ट्रैक्ट करें
2. नई `digna` executable और `dashboard` फ़ोल्डर को अपनी इंस्टॉलेशन डायरेक्टरी में कॉपी करें


!!! warning "Important"

    `config.toml` फ़ाइल इंस्टॉलेशन ZIP में **कभी भी** शामिल नहीं होती। आपकी मौजूदा कॉन्फ़िगरेशन सुरक्षित रहती है।

### चरण 4: अपनी कॉन्फ़िगरेशन फ़ाइलें रिस्टोर करें

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### चरण 5: रिपॉज़िटरी स्कीमा अपग्रेड करें

अपने digna इंस्टॉलेशन डायरेक्टरी पर नेविगेट करें और चलाएँ:

```bash
digna repo upgrade
```

यह PostgreSQL स्कीमा को नवीनतम संस्करण में अपडेट कर देगा जबकि सभी मौजूदा डेटा संरक्षित रहेगा।

### चरण 6: सर्विसेस को पुनःप्रारंभ करें

यदि Windows सेवा के रूप में चल रहा है:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

यदि मैन्युअली चला रहे हैं, तो सर्वर को पुनःस्टार्ट करें:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

यदि आप IIS या Tomcat का उपयोग कर रहे हैं, तो संबंधित वेब सर्वर को पुनःस्टार्ट करें।

#### चरण 7: अपग्रेड सत्यापित करें

1. digna डैशबोर्ड एक्सेस करें
2. सत्यापित करें कि इंटरफ़ेस सही ढंग से लोड हो रहा है
3. सर्वर लॉग्स में किसी भी त्रुटि की जाँच करें