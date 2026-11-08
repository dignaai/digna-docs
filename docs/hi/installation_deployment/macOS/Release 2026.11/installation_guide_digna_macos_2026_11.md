---
title: macOS इंस्टॉलेशन गाइड – digna रिलीज 2026.11 | digna डॉक्यूमेंटेशन
description: macOS पर digna रिलीज 2026.11 इंस्टॉल करने के चरण-दर-चरण निर्देश — सिस्टम आवश्यकताएँ, Homebrew और PostgreSQL सेटअप, nginx या Apache कॉन्फ़िगरेशन, बैकएंड और डैशबोर्ड कॉन्फ़िगरेशन, digna को बैकग्राउंड सेवा के रूप में चलाना, और रिलीज़ 2026.06 से अपग्रेड करना।
keywords: digna macOS इंस्टॉलेशन, digna mac डिप्लॉयमेंट गाइड, digna बैकएंड सेटअप, digna डैशबोर्ड इंस्टॉलेशन, postgresql homebrew, nginx macOS, digna launchd सेवा, digna अपग्रेड गाइड
image: /assets/logo_square.png
---

# macOS इंस्टॉलेशन गाइड — digna रिलीज 2026.11

**रिलीज:** 2026.11

**अंतिम अद्यतन:** 7 नवम्बर, 2026


---

## सामग्री तालिका

1. [परिचय](#introduction)
2. [सिस्टम आवश्यकताएँ](#system-requirements)
3. [पूर्व-इंस्टॉलेशन सेटअप](#pre-installation-setup)
4. [PostgreSQL सर्वर सेटअप](#postgresql-server-setup)
5. [वेब सर्वर कॉन्फ़िगरेशन](#web-server-configuration)
6. [प्रारम्भिक इंस्टॉलेशन](#initial-installation)
7. [बैकएंड कॉन्फ़िगरेशन](#backend-configuration)
8. [डैशबोर्ड कॉन्फ़िगरेशन](#dashboard-configuration)
9. [digna को बैकग्राउंड सेवा के रूप में चलाना](#running-digna-as-a-background-service)
10. [नए रिलीज़ में अपग्रेड करना](#upgrading-to-a-new-release)

---

## परिचय {: #introduction }

### digna के बारे में

digna एक व्यापक AI-समर्थित प्लेटफ़ॉर्म है जो विभिन्न डेटा वातावरणों (वेयरहाउस, लेक्स और लेकहाउस जैसे) में डेटा गुणवत्ता प्रबंधन को अनुकूलित करने के लिए डिज़ाइन किया गया है। यह उच्च स्केलेबल और अनुकूलनीय बनाने के लिए ऑटोमेशन, वास्तविक समय की निगरानी और अनॉमली डिटेक्शन के माध्यम से आधुनिक डेटा चुनौतियों को संबोधित करता है।

digna दो मुख्य घटकों से मिलकर बनता है:

- **digna**: एप्लिकेशन का केंद्र, जो डेटा संसाधित करने और गुणवत्ता जाँच चलाने के लिए ज़िम्मेदार है। यह बैकएंड और कमांड लाइन इंटरफ़ेस को एक ही निष्पादन योग्य फ़ाइल में जोड़ता है और पिछली रिलीज़ के अलग-अलग प्रोग्राम `dignabackend` तथा `dignacli` की जगह लेता है।
- **dignadashboard**: एक वेब-आधारित इंटरफ़ेस जो वेब सर्वर पर होस्ट होता है और digna प्लेटफ़ॉर्म के साथ इंटरैक्ट करने तथा डेटा गुणवत्ता मीट्रिक्स को विज़ुअलाइज़ करने का उपयोगकर्ता-अनुकूल तरीका प्रदान करता है।

### रिलीज 2026.11 में नया क्या है

यह रिलीज़ digna Data Reconciliation, digna MCP Server के साथ digna Agentic, और digna Engine जोड़ती है, जो digna के भीतर डेटा को प्रोफाइल कर सकता है और अलग-अलग डेटाबेस तकनीकों के बीच रेफरेंशियल इंटीग्रिटी की जाँच कर सकता है। पूर्ण विवरण के लिए देखें [रिलीज़ नोट्स](../../../changelog/Release_202611.md)।

इंस्टॉलेशन के लिए यह रिलीज़ एक नया रिपॉज़िटरी माइग्रेशन तंत्र, digna Engine के लिए `config.toml` में एक वैकल्पिक `[duckdb]` सेक्शन, और एक नई लाइसेंस फ़ाइल लाती है। [अपग्रेड सेक्शन](#upgrading-to-a-new-release) इनमें से हर एक को कवर करता है।

### क्या आप Windows या Linux ढूंढ रहे हैं?

यह गाइड macOS के लिए है। अन्य प्लेटफार्मों के लिए देखें [Windows Installation Guide](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) या [Linux Installation Guide](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## सिस्टम आवश्यकताएँ {: #system-requirements }

इंस्टॉलेशन शुरू करने से पहले सुनिश्चित करें कि आपका सिस्टम निम्न न्यूनतम आवश्यकताओं को पूरा करता है:

| आवश्यकता | विनिर्देश |
|---|---|
| **ऑपरेटिंग सिस्टम** | macOS 13 (Ventura) या बाद वाला |
| **आर्किटेक्चर** | Apple Silicon (arm64) या Intel (x86_64) |
| **मेमोरी (मिनिमल सेटअप)** | 16 GB RAM |
| **डिस्क स्पेस** | 10 GB उपलब्ध स्टोरेज |
| **डेटाबेस** | PostgreSQL Server 12 या उससे ऊपर |
| **वेब सर्वर** | nginx, Apache httpd, या समकक्ष |
| **कमान्ड लाइन टूल्स** | Xcode Command Line Tools (Homebrew के लिए आवश्यक) |

!!! info "digna Engine"

    जो डेटाबेस कनेक्शन प्रोफाइलिंग लोकेशन के रूप में digna Engine का उपयोग करते हैं, उन्हें स्वयं
    digna होस्ट पर प्रोफाइल किया जाता है। उनके लिए अतिरिक्त मेमोरी और डिस्क स्थान की योजना बनाएँ, देखें
    [\[duckdb\] सेक्शन](#duckdb-section)।

### डेटाबेस इंस्टॉलेशन विकल्प

**यदि PostgreSQL पहले से इंस्टॉल है:**
आप मौजूदा PostgreSQL सर्वर में digna के लिए नया डेटाबेस जोड़ सकते हैं।

**यदि आप PostgreSQL को उसी मशीन पर इंस्टॉल कर रहे हैं जहाँ digna है:**

!!! info "सिफारिश की गई विनिर्देश"

    - **मेमोरी**: 32 GB RAM (16 GB की जगह)
    - **डिस्क स्पेस**: 50 GB उपलब्ध स्टोरेज (10 GB की जगह)

    ये उच्च विनिर्देश दोनों, digna और PostgreSQL डेटाबेस को एक साथ चलाने के लिए उपयुक्त हैं।

### अपनी आर्किटेक्चर की जाँच

इस गाइड में कई पाथ Apple Silicon और Intel Mac के बीच अलग होते हैं। यह जाँचने के लिए **Terminal** खोलकर चलाएँ:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew `/opt/homebrew` पर इंस्टॉल होता है।
- `x86_64` — Intel. Homebrew `/usr/local` पर इंस्टॉल होता है।

!!! tip "सुझाव"

    किसी भी एक पाथ को हार्ड-कोड करने के बजाय, यह गाइड `$(brew --prefix)` का उपयोग करती है, जो दोनों आर्किटेक्चरों पर सही स्थान में विस्तारित होता है। आप कमांड्स यथावत कॉपी कर सकते हैं।

---

## पूर्व-इंस्टॉलेशन सेटअप {: #pre-installation-setup }

digna इंस्टॉल करने से पहले सुनिश्चित करें कि तीन प्रमुख पूर्वापेक्षित चीज़ें मौजूद हों:

1. **Homebrew** – पैकेज मैनेजर जिसका उपयोग नीचे दिए गए कंपोनेंट्स को इंस्टॉल करने के लिए किया जाता है
2. **PostgreSQL Server** – गणना किए गए मीट्रिक्स और प्रदर्शन डेटा को स्टोर करने के लिए
3. **Web Server** – digna Dashboard की होस्टिंग के लिए

यदि ये कंपोनेंट्स पहले से सेट नहीं हैं, तो इन्हें इंस्टॉल और कॉन्फ़िगर करने के लिए नीचे के सेक्शनों का पालन करें।

### Homebrew इंस्टॉल करना

Homebrew macOS के लिए मानक पैकेज मैनेजर है और इस गाइड में PostgreSQL और nginx इंस्टॉल करने के लिए उपयोग किया जाता है।

#### चरण 1: जाँचें कि Homebrew पहले से इंस्टॉल है या नहीं

**Terminal** खोलें (press `Cmd + Space`, type `Terminal`, press Enter) और चलाएँ:

```bash
brew --version
```

यदि कोई वर्शन नंबर लौटता है, तो [PostgreSQL Server Setup](#postgresql-server-setup) अनुभाग पर जाएँ।

#### चरण 2: Homebrew इंस्टॉल करें

यदि कमांड नहीं मिला, तो Homebrew इंस्टॉल करने के लिए [official Homebrew site](https://brew.sh) पर दिए निर्देशों का पालन करें। इंस्टॉलर Xcode Command Line Tools भी इंस्टॉल कर देता है यदि वे पहले से मौजूद नहीं हैं।

#### चरण 3: Homebrew को अपने PATH में जोड़ें

Apple Silicon पर, इंस्टॉलर आपके शेल पर्यावरण में Homebrew जोड़ने के लिए दो कमांड प्रिंट करता है। उन्हें निर्देशानुसार चलाएँ, फिर पुष्टि करें:

```bash
brew --prefix
```

यह Apple Silicon पर `/opt/homebrew` या Intel पर `/usr/local` प्रिंट करेगा।

---

## PostgreSQL सर्वर सेटअप {: #postgresql-server-setup }

### यदि आपके पास पहले से PostgreSQL मौजूद है

यदि PostgreSQL पहले से आपके लोकल मशीन पर इंस्टॉल और रन कर रहा है, या आप किसी मैनेज्ड रिमोट PostgreSQL सर्वर का उपयोग कर रहे हैं, तो आप [अगले अनुभाग](#web-server-configuration) पर जा सकते हैं।

### इंस्टॉलेशन विकल्प

macOS दो सरल तरीकों की पेशकश करता है PostgreSQL इंस्टॉल करने के लिए। एक चुनें:

- [Homebrew](#postgresql-homebrew) — कमांड-लाइन इंस्टॉलेशन, सर्वर डिप्लॉयमेंट के लिए अनुशंसित
- [Postgres.app](#postgresql-app) — ग्राफिकल इंस्टॉलेशन, लोकल मूल्यांकन के लिए सुविधाजनक

### Homebrew के साथ PostgreSQL इंस्टॉल करना {: #postgresql-homebrew }

#### चरण 1: PostgreSQL फॉर्मूला इंस्टॉल करें

```bash
brew install postgresql@16
```

#### चरण 2: PostgreSQL को अपने PATH में जोड़ें

वर्ज़न्ड PostgreSQL फॉर्मूलाज *keg-only* होते हैं, जिसका मतलब है कि Homebrew उनके कमांड्स को अपने PATH में स्वतः लिंक नहीं करता। इन्हें स्वयं जोड़ें:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "नोट"

    यह macOS द्वारा उपयोग किए जाने वाले डिफ़ॉल्ट `zsh` शेल को मानकर है। यदि आप `bash` उपयोग करते हैं, तो समान लाइन को `~/.bash_profile` में जोड़ें।

#### चरण 3: PostgreSQL सर्विस शुरू करें

```bash
brew services start postgresql@16
```

यह PostgreSQL को तुरंत शुरू कर देता है तथा इसे लॉगिन पर ऑटोमैटिक रूप से शुरू होने के लिए कॉन्फ़िगर करता है।

#### चरण 4: इंस्टॉलेशन सत्यापित करें

```bash
psql --version
```

यदि इंस्टॉलेशन सफल रहा तो PostgreSQL वर्शन दिखाई देगा।

#### चरण 5: सर्वर से कनेक्ट करें

```bash
psql postgres
```

!!! warning "महत्वपूर्ण — macOS यहाँ Windows से अलग है"

    Windows इंस्टॉलर आपसे `postgres` सुपरयूज़र और पासवर्ड बनाने के लिए कहता है। Homebrew ऐसा नहीं करता। इसके बजाय यह आपके **macOS अकाउंट** के नाम का एक सुपरयूज़र बनाता है, बिना पासवर्ड के, और केवल लोकल मशीन से पहुँच योग्य होता है।

    इसका मतलब है कि एक फ्रेश Homebrew इंस्टॉलेशन पर `postgres` रोल मौजूद नहीं होता। जब आपको सुपरयूज़र की आवश्यकता हो तब अपने अकाउंट नाम का उपयोग करें, और [प्रारम्भिक इंस्टॉलेशन](#initial-installation) में बताए अनुसार एक स्पष्ट digna यूज़र बनाएं।

#### चरण 6: पोर्ट की पुष्टि करें

डिफ़ॉल्ट PostgreSQL पोर्ट `5432` है। यह पुष्टि करने के लिए कि आपका सर्वर किस पोर्ट पर सुन रहा है:

```bash
psql postgres -c "SHOW port;"
```

मान नोट कर लें — आपको digna बैकएंड कॉन्फ़िगर करते समय इसकी आवश्यकता होगी।

### Postgres.app के साथ PostgreSQL इंस्टॉल करना {: #postgresql-app }

यदि आप ग्राफिकल इंस्टॉलेशन पसंद करते हैं:

1. [Postgres.app](https://postgresapp.com) डाउनलोड करें और उसे **Applications** फ़ोल्डर में ड्रैग करें
2. ऐप खोलें और नई सर्वर बनाने के लिए **Initialize** पर क्लिक करें
3. ऐप के निर्देशों का पालन करके उसके कमांड-लाइन टूल्स को अपने PATH में जोड़ें
4. इंस्टॉलेशन सत्यापित करें:

```bash
psql --version
```

Postgres.app भी आपके macOS अकाउंट के नाम का एक सुपरयूज़र बनाता है।

---

## वेब सर्वर कॉन्फ़िगरेशन {: #web-server-configuration }

digna को डैशबोर्ड होस्ट करने के लिए एक वेब सर्वर की आवश्यकता है। निम्नलिखित विकल्पों में से एक चुनें:

- [nginx](#nginx-setup) — Homebrew के माध्यम से इंस्टॉल, अनुशंसित
- [Apache httpd](#apache-setup) — macOS के साथ शामिल

आपको केवल इन में से किसी एक सर्वर को इंस्टॉल और कॉन्फ़िगर करने की आवश्यकता है।

दोनों सेक्शन उन दो चीज़ों को कॉन्फ़िगर करते हैं जिन पर डैशबोर्ड निर्भर करता है:

- **सिंगल-पेज-एप्लिकेशन fallback**, ताकि डैशबोर्ड URL को रिफ़्रेश करने पर 404 न मिले
- **`.md` MIME टाइप**, ताकि Markdown फ़ाइलें सही ढंग से सर्व हों

### nginx सेटअप {: #nginx-setup }

#### अवलोकन

nginx एक हल्का, उच्च-प्रदर्शन वेब सर्वर है जो स्टेटिक digna डैशबोर्ड सर्व करने के लिए उपयुक्त है।

#### इंस्टॉलेशन

```bash
brew install nginx
```

#### nginx शुरू करना

```bash
brew services start nginx
```

#### इंस्टॉलेशन सत्यापित करें

1. ब्राउज़र खोलें
2. `http://localhost:8080` पर नेविगेट करें
3. आपको nginx स्वागत पृष्ठ दिखाई देना चाहिए

!!! note "नोट — डिफ़ॉल्ट पोर्ट 8080 है, 80 नहीं"

    Homebrew nginx को पोर्ट `8080` पर सुनने के लिए कॉन्फ़िगर करता है ताकि यह बिना एडमिनिस्ट्रेटर विशेषाधिकार के चल सके। macOS पर पोर्ट `80` या 1024 से कम किसी भी पोर्ट पर बाइंड करने के लिए रूट की आवश्यकता होती है।

    डैशबोर्ड को पोर्ट 80 पर सर्व करने के लिए, नीचे दी गई कॉन्फ़िगरेशन में `listen 8080;` को `listen 80;` में बदलें और फिर `sudo brew services start nginx` के साथ nginx को शुरू करें।

#### डैशबोर्ड के लिए साइट कॉन्फ़िगर करना

Homebrew की nginx कॉन्फ़िगरेशन उसकी `servers` डायरेक्टरी में हर फ़ाइल को शामिल करती है। वहां digna के लिए एक समर्पित कॉन्फ़िगरेशन फ़ाइल बनाएँ:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

निम्नलिखित पेस्ट करें, `/path/to/digna/dashboard` को अपने एक्सट्रैक्ट किए हुए `dashboard` फ़ोल्डर के वास्तविक पाथ से बदलें:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "महत्वपूर्ण"

    `try_files` निर्देश के बिना, रूट URL के अलावा किसी भी डैशबोर्ड पेज को रीलोड करने पर 404 लौटेगा। यह nginx का वह समाधान है जो Windows पर IIS के URL Rewrite मॉड्यूल के बराबर है।

#### कॉन्फ़िगरेशन लागू करें

सिंटैक्स त्रुटियों के लिए कॉन्फ़िगरेशन का परीक्षण करें, फिर nginx रीलोड करें:

```bash
nginx -t
brew services restart nginx
```

---

### Apache httpd सेटअप {: #apache-setup }

#### अवलोकन

macOS में Apache httpd शामिल है, इसलिए इंस्टॉलेशन की आवश्यकता नहीं है। यह डिफ़ॉल्ट रूप से अक्षम होता है।

#### Apache शुरू करना

```bash
sudo apachectl start
```

#### इंस्टॉलेशन सत्यापित करें

1. ब्राउज़र खोलें
2. `http://localhost` पर नेविगेट करें
3. आपको "It works!" संदेश दिखाई देना चाहिए

#### आवश्यक: mod_rewrite सक्षम करें

डैशबोर्ड के लिए URL री-राइटिंग आवश्यक है। Apache कॉन्फ़िगरेशन खोलें:

```bash
sudo nano /etc/apache2/httpd.conf
```

निम्नलिखित लाइन ढूँढें और उसके आगे का `#` हटा दें ताकि यह अनकमेंट हो जाए:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### आवश्यक: .htaccess ओवरराइड की अनुमति दें

उसी फ़ाइल में `<Directory "/Library/WebServer/Documents">` ब्लॉक खोजें और बदलें:

```apache
AllowOverride None
```

से:

```apache
AllowOverride All
```

#### आवश्यक: Markdown फ़ाइलों के लिए MIME टाइप

इसी `httpd.conf` में निम्न लाइन जोड़ें ताकि Markdown फ़ाइलें सही तरीके से सर्व हों:

```apache
AddType text/markdown .md
```

!!! warning "महत्वपूर्ण"

    इस सेटिंग के बिना, `.md` फ़ाइलें सही ढंग से सर्व नहीं हो सकती हैं।

#### कॉन्फ़िगरेशन लागू करें

सिंटैक्स की जाँच करें, फिर Apache को रीस्टार्ट करें:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## प्रारम्भिक इंस्टॉलेशन {: #initial-installation }

### चरण 1: digna Repository सेट करें

digna रिपॉज़िटरी सभी गणना किए गए मीट्रिक्स को स्टोर करती है। यह विश्लेषणात्मक और प्रदर्शन डेटा के लिए केंद्रीय डेटाबेस का काम करती है।

#### Repository Schema और यूज़र बनाएँ

अपना PostgreSQL क्लाइंट (psql, pgAdmin, या समान) खोलें और निम्न SQL कमांड्स चलाएँ:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**निम्न प्लेसहोल्डर्स को बदलें:**

- `<digna_repo_schema>` — आपकी इच्छित schema का नाम (उदा., `dignarepo`)
- `<digna_repo_user>` — आपका इच्छित यूज़रनेम (उदा., `digna_user`)
- `<digna_repo_password>` — इस यूज़र के लिए एक सुरक्षित पासवर्ड

**उदाहरण:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

टर्मिनल से इन्हें एक ही स्टेप में चलाने के लिए:

```bash
psql postgres
```

फिर `postgres=#` प्रॉम्प्ट पर स्टेटमेंट पेस्ट करें और बाहर निकलने के लिए `\q` टाइप करें।

!!! tip "सर्वोत्तम प्रथा"

    डेटाबेस यूज़र्स के लिए मजबूत, जटिल पासवर्ड का उपयोग करें। आसान से अनुमान लगाए जाने योग्य क्रेडेंशियल्स से बचें।

---

### चरण 2: digna इंस्टॉलेशन पैकेज को अनज़िप करें

1. आपको प्रदान किए गए digna इंस्टॉलेशन ZIP फ़ाइल का पता लगाएँ
2. इसे अपनी इच्छित इंस्टॉलेशन लोकेशन पर निकालें — उदाहरण के लिए `/opt/digna` या `~/digna`
3. एक्सट्रैक्शन के बाद, आपको निम्न आइटम दिखाई देने चाहिए:
   - `dashboard/` — वेब डैशबोर्ड इंटरफेस
   - `digna` — मुख्य executable (बैकएंड + CLI संयुक्त)

!!! info "कॉन्फ़िगरेशन और लाइसेंस फ़ाइलें पैकेज में नहीं हैं"

    न तो `config.toml` और न ही `dashboard/dashboard_config.toml` इंस्टॉलेशन के साथ आती है — दोनों को आप
    स्वयं बनाते हैं, [बैकएंड कॉन्फ़िगरेशन](#backend-configuration) और
    [डैशबोर्ड कॉन्फ़िगरेशन](#dashboard-configuration) में। `license.toml` भी साथ नहीं आती;
    digna इसे अलग से उपलब्ध कराता है, जैसा कि चरण 3 में बताया गया है।

Terminal से अनज़िप करने के लिए:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
```

#### Executable को runnable बनाएँ

किस तरह का आर्काइव ट्रांसफर हुआ है उसके आधार पर executable bit रह न भी सकता है। इसे स्पष्ट रूप से सेट करें:

```bash
cd /opt/digna
chmod +x digna
```

#### यदि macOS ऐप को ब्लॉक करता है

ब्राउज़र या मेल क्लाइंट के माध्यम से डाउनलोड की गई फ़ाइलों पर क्वारैंटाइन एट्रिब्यूट हो सकता है। यदि macOS रिपोर्ट करता है कि ऐप *"cannot be opened because the developer cannot be verified"*, तो इंस्टॉलेशन डायरेक्टरी से एट्रिब्यूट हटाएं:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

वैकल्पिक रूप से, **System Settings → Privacy & Security** खोलें, पेज के नीचे नज़दीक ब्लॉक किए गए आइटम को खोजें और **Open Anyway** पर क्लिक करें।

!!! note "नोट"

    यह चरण केवल तभी आवश्यक है जब macOS वास्तव में executable को ब्लॉक करता है। SSH या आंतरिक फ़ाइल शेयर के माध्यम से ट्रांसफर्ड पैकेज आमतौर पर क्वारैंटाइन नहीं होते।

### चरण 3: लाइसेंस फ़ाइल इंस्टॉल करें

!!! warning "महत्वपूर्ण"

    लाइसेंस फ़ाइल इंस्टॉलेशन पैकेज में **शामिल नहीं** होती और यह digna द्वारा अलग से प्रदान की जाएगी।

1. आपको प्रदान की गई `license.toml` फ़ाइल का पता लगाएँ
2. इसे रूट digna इंस्टॉलेशन डायरेक्टरी (जहाँ `config.toml` और `digna` executable स्थित हैं) में कॉपी करें

**यह क्यों महत्वपूर्ण है:**
लाइसेंस फ़ाइल में आपके ग्राहक जानकारी, लाइसेंस समाप्ति तिथि, और डिजिटल सिग्नेचर होती है। **इस फ़ाइल को संशोधित न करें** — कोई भी परिवर्तन इसे अमान्य कर देगा।

**सेटअप के बाद डायरेक्टरी संरचना:**

```
/opt/digna/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
├── bin/                (service management scripts)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## बैकएंड कॉन्फ़िगरेशन {: #backend-configuration }

### चरण 1: कॉन्फ़िगरेशन फ़ाइल बनाएँ और संपादित करें

`config_template.toml` फ़ाइल आपकी digna इंस्टॉलेशन डायरेक्टरी में प्रदान की गई है। इसे केवल `config.toml` में रेनैम करें।

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**स्थान:** `/opt/digna/config.toml`

`config.toml` को किसी टेक्स्ट एडिटर में खोलें और नीचे दिए गए प्रत्येक सेक्शन को कॉन्फ़िगर करें।

#### [app] सेक्शन

यह सेक्शन डैशबोर्ड और बैकएंड के बीच क्रॉस-ओरिजिन रिसोर्स शेयरिंग (CORS) को कॉन्फ़िगर करता है:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| पैरामीटर | मान | नोट्स |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | डैशबोर्ड URL | वे URL जिनसे डैशबोर्ड सर्व किया जाता है। किसी अन्य origin से आने वाले ब्राउज़र अनुरोध अस्वीकार कर दिए जाते हैं |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | आवश्यक, ताकि ब्राउज़र हर अनुरोध के साथ सत्र कुकी भेजे |

!!! note "नोट"

    यदि आप डैशबोर्ड को Homebrew के nginx पर उसके डिफ़ॉल्ट पोर्ट पर सर्व कर रहे हैं, तो अनुमति देने के लिए origin `http://localhost:8080` है।

!!! info "[app] सेक्शन वैकल्पिक है"

    रिलीज़ 2026.11 से दोनों कुंजियाँ, और पूरा `[app]` सेक्शन, छोड़े जा सकते हैं। यह तब सही सेटअप है
    जब कोई रिवर्स प्रॉक्सी डैशबोर्ड और बैकएंड को एक ही origin के अंतर्गत सर्व करता है: तब ब्राउज़र
    कोई क्रॉस-ओरिजिन अनुरोध नहीं करता, और डिफ़ॉल्ट रूप से किसी की अनुमति नहीं होती।

#### [repo] सेक्शन

यह सेक्शन PostgreSQL डेटाबेस से कनेक्शन को कॉन्फ़िगर करता है:

```toml
[repo]
DIGNA_REPO_HOST = "localhost"
DIGNA_REPO_PORT = 5432
DIGNA_REPO_DB = "postgres"
DIGNA_REPO_SCHEMA = "dignarepo"
DIGNA_REPO_USER = "digna_user"
DIGNA_REPO_PASSWORD = "YourSecurePassword123!"
DIGNA_REPO_SSLMODE = "prefer"
DIGNA_REPO_NUM_CONNS = 16
```

| पैरामीटर | मान | नोट्स |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` या IP | PostgreSQL सर्वर होस्टनाम/IP |
| `DIGNA_REPO_PORT` | `5432` (डिफ़ॉल्ट) | PostgreSQL पोर्ट |
| `DIGNA_REPO_DB` | `postgres` | डेटाबेस का नाम |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | पहले बनाया गया schema |
| `DIGNA_REPO_USER` | `digna_user` | PostgreSQL सेटअप में बनाया गया यूज़र |
| `DIGNA_REPO_PASSWORD` | आपका पासवर्ड | schema क्रिएशन के दौरान सेट किया गया पासवर्ड |
| `DIGNA_REPO_SSLMODE` | `prefer` (डिफ़ॉल्ट) | वैकल्पिक। PostgreSQL SSL मोड: `disable`, `allow`, `prefer`, `require`, `verify-ca` या `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (डिफ़ॉल्ट) | वैकल्पिक। रिपॉज़िटरी से digna द्वारा खुले रखे जाने वाले कनेक्शनों की संख्या |

#### [base] सेक्शन

यह सेक्शन सुरक्षा, कुकी और निरीक्षण सेटिंग्स रखता है:

```toml
[base]
DIGNA_FERNET_KEY = "DU4a0yJ-OqvbKCL4hNQn_CsknH-V1vWmHZqBUl-AY44="
DIGNA_COOKIE_DOMAIN = "localhost"
DIGNA_COOKIE_SECURE = false
DIGNA_COOKIE_HTTPONLY = true
DIGNA_TOKEN_EXPIRES_IN = 86400
DIGNA_MAX_WORKERS = 4
DIGNA_FRONTEND_BASEURL = "http://localhost/"
DIGNA_SOURCE_QUERY_TIMEOUT_SEC = 3600
DIGNA_SOURCE_LOGIN_TIMEOUT_SEC = 30
```

| पैरामीटर | मान | नोट्स |
|---|---|---|
| `DIGNA_FERNET_KEY` | ऊपर दिखाया गया मान | पिछली रिलीज़ द्वारा उपयोग किए गए एन्क्रिप्शन की कुंजी। यह मौजूद होनी चाहिए; दिखाया गया मान ही रखें |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | वह होस्ट जिसके अंतर्गत डैशबोर्ड तक पहुँचा जाता है। `""` कोई डोमेन सेट नहीं करता, जो ऐसे प्रॉक्सी के पीछे सही है जो डैशबोर्ड और बैकएंड को एक ही origin के अंतर्गत सर्व करता है |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | जब भी digna HTTPS पर सर्व किया जाता है, इसे `true` होना चाहिए |
| `DIGNA_COOKIE_HTTPONLY` | `true` | सत्र कुकी को स्क्रिप्ट्स की पहुँच से बाहर रखता है |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 घंटे) | सेकंड में सत्र का टाइमआउट |
| `DIGNA_MAX_WORKERS` | CPU कोर की संख्या - 1 | एक ही समय में चल सकने वाले निरीक्षणों की संख्या |
| `DIGNA_FRONTEND_BASEURL` | डैशबोर्ड URL | आवश्यक। सूचना संदेशों के लिंक के लिए उपयोग होता है, इसलिए यह ऐसा URL होना चाहिए जिसे प्राप्तकर्ता खोल सकें |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (डिफ़ॉल्ट) | वैकल्पिक। किसी स्रोत डेटाबेस पर एक क्वेरी रद्द किए जाने से पहले कितने सेकंड चल सकती है; `0` टाइमआउट को अक्षम करता है |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (डिफ़ॉल्ट) | वैकल्पिक। किसी स्रोत डेटाबेस से कनेक्शन के लिए प्रतीक्षा के सेकंड; `0` अनिश्चित काल तक प्रतीक्षा करता है |

!!! tip "सुझाव"

    अपने Mac पर उपलब्ध CPU कोर की संख्या जानने के लिए चलाएँ `sysctl -n hw.ncpu`।

#### [encryption] सेक्शन

इस सेक्शन में वह कुंजी होती है जिससे रिपॉज़िटरी में संग्रहीत संवेदनशील मान एन्क्रिप्ट किए जाते हैं। यह **आवश्यक** है — कुंजी न होने पर `config check` सेक्शन `[encryption]` को FAILED बताता है।

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| पैरामीटर | मान | नोट्स |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64 में एन्कोड की गई कुंजी | digna रिपॉज़िटरी में संग्रहीत संवेदनशील मानों को एन्क्रिप्ट करती है |

!!! warning "config.toml की सुरक्षा करें"

    यह कुंजी एक निश्चित मान है, जो सभी digna संस्थापनों में एक समान है, और यही आपकी रिपॉज़िटरी के संवेदनशील मानों को डिक्रिप्ट करती है। `config.toml` तक पहुँच उसी खाते तक सीमित रखें जिससे digna चलता है, फ़ाइल को संस्करण नियंत्रण और साझा ड्राइव से बाहर रखें, और उसे हर ऐसे बैकअप से हटा दें जो रिपॉज़िटरी की तुलना में कम सुरक्षित रखा जाता है।

#### [logging] सेक्शन

यह सेक्शन लॉगिंग व्यवहार को कॉन्फ़िगर करता है:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| पैरामीटर | मान | नोट्स |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` या `DEBUG` | प्रोडक्शन के लिए `INFO`, ट्रबलशूटिंग के लिए `DEBUG`। `TRACE`, `WARN` और `ERROR` भी स्वीकार किए जाते हैं |
| `DIGNA_LOGGING_DIR` | `logs` (डिफ़ॉल्ट) | वैकल्पिक। रोटेट होने वाली लॉग फ़ाइलों की डायरेक्टरी, कार्यशील डायरेक्टरी के सापेक्ष |
| `DIGNA_LOGGING_MAX_FILES` | `30` (डिफ़ॉल्ट) | वैकल्पिक। रखी जाने वाली रोटेट की गई लॉग फ़ाइलों की संख्या |

#### [duckdb] सेक्शन (वैकल्पिक) {: #duckdb-section }

रिलीज़ 2026.11 में नया। यह सेक्शन **digna Engine** के संसाधन निर्धारित करता है, जो उन डेटाबेस
कनेक्शनों के लिए digna के भीतर डेटा को प्रोफाइल करता है जिनकी प्रोफाइलिंग लोकेशन **digna Engine** है, और
अलग-अलग डेटाबेस कनेक्शनों पर स्थित डेटा स्रोतों के बीच रेफरेंशियल इंटीग्रिटी जाँच चलाता है। देखें
[प्रोफाइलिंग लोकेशन](../../../platform/profiling/profiling_location.md)।

यह सेक्शन वैकल्पिक है। इसके बिना नीचे दिए गए डिफ़ॉल्ट लागू होते हैं।

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| पैरामीटर | मान | नोट्स |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (डिफ़ॉल्ट) | MB में वह मेमोरी जिसका उपयोग digna Engine का एक रन कर सकता है। एक ही समय में अधिकतम `DIGNA_MAX_WORKERS` रन सक्रिय हो सकते हैं |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | डिफ़ॉल्ट: सिस्टम की अस्थायी डायरेक्टरी (digna चलाने वाले खाते का `$TMPDIR`) | अस्थायी फ़ाइलों के लिए डायरेक्टरी, जब डेटा मेमोरी में नहीं समाता |

!!! tip "digna Engine का आकार निर्धारण"

    digna होस्ट पर, digna के अपने उपयोग के अतिरिक्त, अधिकतम `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB`
    मेमोरी की योजना बनाएँ, और अस्थायी डायरेक्टरी में इतने खाली डिस्क स्थान की, जिसमें digna Engine का
    उपयोग करने वाले डेटा स्रोतों की सबसे बड़ी निरीक्षित तिथि समा सके। `DIGNA_DUCKDB_TEMP_DIRECTORY` को ऐसी
    डिस्क पर इंगित करें जिसमें यह स्थान हो और जिस पर digna चलाने वाला खाता लिख सके:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    आपको इस सेक्शन की आवश्यकता तभी है जब कम से कम एक डेटाबेस कनेक्शन digna Engine का उपयोग करता हो, या
    कोई रेफरेंशियल इंटीग्रिटी जाँच अलग-अलग कनेक्शनों पर स्थित डेटा स्रोतों की तुलना करती हो।

---

### चरण 2: कॉन्फ़िगरेशन जाँचें

रिपॉज़िटरी आरंभ करने से पहले जाँचें कि `config.toml` पूर्ण और सही ढंग से बना है। अपनी digna संस्थापन निर्देशिका में चलाएँ:

```bash
./digna config check
```

प्रत्येक सेक्शन की जाँच अलग से होती है, इसलिए एक अकेली गलती बाकी की स्थिति नहीं छिपाती:

```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: OK
 - OIDC config(s): OK
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

जो कुछ भी FAILED बताया जाए उसे ठीक करें और आगे बढ़ने से पहले कमांड फिर चलाएँ। **Unknown keys** के अंतर्गत WARNING उन कुंजियों को सूचीबद्ध करता है जो `config.toml` में हैं लेकिन जिन्हें digna नहीं पढ़ता; उनका कोई प्रभाव नहीं होता, इसलिए उन्हें हटाएँ या उनकी वर्तनी ठीक करें। विकल्पों की पूरी सूची [CLI संदर्भ](../../../cli/Command_Line_Interface_202611.md) में है।

### चरण 3: Repository इनिशियलाइज़ करें

1. **Terminal** खोलें
2. अपने digna इंस्टॉलेशन डायरेक्टरी पर जाएँ (जहाँ `config.toml` और `digna` executable स्थित हैं)
3. कनेक्शन टेस्ट चलाएँ:

```bash
cd /opt/digna
./digna repo check
```

नए स्कीमा पर कमांड कनेक्ट होती है और फिर बताती है कि अभी कोई रिपॉज़िटरी इंस्टॉल नहीं है:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

इस चरण पर यही अपेक्षित परिणाम है: यह पुष्टि करता है कि digna PostgreSQL और स्कीमा तक पहुँचता है। इसके बजाय कोई कनेक्शन या प्रमाणीकरण त्रुटि `[repo]` सेक्शन या PostgreSQL सेटअप की ओर इशारा करती है।

!!! note "नोट"

    macOS पर, करंट डायरेक्टरी में कमांड्स आपके PATH पर नहीं होते, इसलिए executable को `./digna` के रूप में ही चलाया जाता है न कि `digna` के रूप में। शॉर्टर रूप हर जगह उपयोग करने के लिए इंस्टॉलेशन डायरेक्टरी को अपने PATH में जोड़ें:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### चरण 4: Repository Schema इंस्टॉल करें

उसी डायरेक्टरी में चलाएँ:

```bash
./digna repo upgrade
```

यह कमांड रिपॉज़िटरी स्कीमा में आवश्यक टेबल इंस्टॉल करती है और इस संदेश के साथ समाप्त होती है:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade इंस्टॉल और अपग्रेड दोनों करता है"

    रिलीज़ 2026.11 से `repo upgrade` नई रिपॉज़िटरी इंस्टॉल करता है और मौजूदा रिपॉज़िटरी को अपग्रेड करता है।
    `repo install` अब भी उसी कमांड के दूसरे नाम के रूप में काम करता है।

### चरण 5: एक Admin यूज़र बनायें

1. एक **नया** Terminal विंडो खोलें
2. अपने digna इंस्टॉलेशन डायरेक्टरी पर जाएँ
3. एक एडमिन यूज़र बनाने के लिए निम्न कमांड चलाएँ:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**उदाहरण:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

इससे `admin@example.com` ईमेल पते और पूर्ण प्रशासनिक अधिकारों वाला एक उपयोगकर्ता बनता है।

!!! tip "सुझाव"

    पासवर्ड को सिंगल कोट्स में रखें। `zsh` जैसे शेल `!`, `$` और `*` जैसे करैक्टर को विशेष मानते हैं; बिना उद्धरण के ऐसे पासवर्ड सही तरीके से पारित नहीं होंगे।

!!! tip "सर्वोत्तम प्रथा"

    बड़े, छोटे अक्षर, संख्याएँ और स्पेशल करैक्टर मिलाकर मजबूत पासवर्ड उपयोग करें।

---

### चरण 6: digna सर्वर शुरू करें

digna इंस्टॉलेशन डायरेक्टरी में सर्वर शुरू करें:

```bash
./digna serve --address <host> --port <port>
```

**पैरामीटर:**
- `--address` — सर्वर होस्टनाम/IP (डिफ़ॉल्ट `127.0.0.1`)
- `--port` — सर्वर पोर्ट (डिफ़ॉल्ट `8000`)

सर्वर चालू होने पर, वह उस पते को प्रिंट करता है जिस पर वह सुनता है:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "सुझाव"

    पहली बार सर्वर शुरू करने पर macOS आपसे पूछ सकता है कि क्या आप एप्लिकेशन को इनकमिंग नेटवर्क कनेक्शनों को स्वीकार करने की अनुमति देना चाहते हैं। **Allow** पर क्लिक करें, अन्यथा डैशबोर्ड बैकएंड से कनेक्ट नहीं कर पाएगा।

!!! note "सर्वर टर्मिनल को व्यस्त रखता है"

    `serve` अग्रभूमि में चलता है और तब तक चलता रहता है जब तक आप इसे ++ctrl+c++ से रोक नहीं देते। सेटअप पूरा करते समय इसे चलता रहने दें; इसके बजाय बूट पर स्वतः प्रारंभ करने के लिए देखें [digna को पृष्ठभूमि सेवा के रूप में चलाना](#running-digna-as-a-background-service).

## डैशबोर्ड कॉन्फ़िगरेशन {: #dashboard-configuration }

### चरण 1: डैशबोर्ड को वेब सर्वर पर डिप्लॉय करें

digna डैशबोर्ड अपनी कॉन्फ़िगरेशन `dashboard/dashboard_config.toml` से पढ़ता है। यह फ़ाइल इंस्टॉलेशन के साथ नहीं आती — आप इसे `dashboard/` डायरेक्टरी में डैशबोर्ड फ़ाइलों के साथ बनाते हैं।

इसकी सामग्री [सिंगल साइन-ऑन](../../../sso/overview.md) के अंतर्गत बताई गई है, और वहीं इस फ़ाइल की आवश्यकता भी होती है: इसमें वे लॉगिन विकल्प होते हैं जो डैशबोर्ड प्रदान करता है और, मल्टी-इंस्टेंस डिप्लॉयमेंट के लिए, बैकएंड कनेक्शन।

अपने वेब सर्वर का चयन करें और संबंधित डिप्लॉयमेंट स्टेप्स का पालन करें।

#### nginx पर डिप्लॉय करना

यदि आपने [nginx Setup](#nginx-setup) सेक्शन का पालन किया है, तो सर्वर ब्लॉक पहले से ही आपके `dashboard` फ़ोल्डर की ओर पॉइंट करता है और कॉपी करने की आवश्यकता नहीं है।

1. **पाथ की पुष्टि करें**
   - खोलें `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - सत्यापित करें कि `root` आपके एक्सट्रैक्ट किए हुए `dashboard` फ़ोल्डर की ओर पॉइंट कर रहा है

2. **सुनिश्चित करें कि फ़ोल्डर पठनीय है**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **nginx रीलोड करें**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **इंस्टॉलेशन टेस्ट करें**
   - ब्राउज़र खोलें
   - `http://localhost:8080` (या आपका कॉन्फ़िगर किया गया URL) खोलें
   - आपको digna डैशबोर्ड लॉगिन पेज दिखाई देना चाहिए

#### Apache httpd पर डिप्लॉय करना

1. **डैशबोर्ड को डॉक्यूमेंट रूट में कॉपी करें**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **रीराइट नियम जोड़ें**

   डिप्लॉय किए गए फ़ोल्डर के अंदर एक `.htaccess` फ़ाइल बनाएं ताकि डैशबोर्ड रूट पर ब्राउज़र रिफ्रेश होने पर रूटिंग बनी रहे:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   निम्नलिखित पेस्ट करें:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **Apache रीस्टार्ट करें**
   ```bash
   sudo apachectl restart
   ```

4. **डैशबोर्ड एक्सेस करें**
   - ब्राउज़र खोलें
   - `http://localhost/digna` पर नेविगेट करें
   - आपको digna डैशबोर्ड लॉगिन पेज दिखाई देना चाहिए

---

## digna को बैकग्राउंड सेवा के रूप में चलाना {: #running-digna-as-a-background-service }

### digna को सेवा के रूप में चलाने का कारण

digna बैकएंड को बैकग्राउंड सेवा के रूप में चलाने से यह सुनिश्चित होता है कि यह:

- मशीन के बूट होने पर स्वचालित रूप से शुरू हो
- बिना खुले Terminal विंडो के बैकग्राउंड में चले
- क्रैश होने पर स्वतः पुनः आरंभ हो
- macOS के सेवा प्रबंधक `launchctl` के माध्यम से प्रबंधित किया जा सके

### सेवा प्रबंधन फाइलें

सारी आवश्यक फाइलें digna इंस्टॉलेशन डायरेक्टरी के अंदर स्थित हैं: `bin/`

उपलब्ध शेल स्क्रिप्ट्स:

- `install_service.sh` — digna को launchd के साथ रजिस्टर करता है
- `uninstall_service.sh` — सर्विस का अनरजिस्टर करता है
- `start_service.sh` — रजिस्टर की गई सर्विस को स्टार्ट करता है
- `stop_service.sh` — चल रही सर्विस को स्टॉप करता है

!!! warning "एडमिनिस्ट्रेटर आवश्यक"

    सभी स्क्रिप्ट्स को `sudo` के साथ चलाना अनिवार्य है, क्योंकि बूट पर शुरू होने वाली सर्विस को रजिस्टर करना `/Library/LaunchDaemons` में लिखता है।

### स्क्रिप्ट्स को executable बनाना

एक्सट्रैक्शन executable बिट को बनाए नहीं रख सकता। पहले उपयोग से पहले:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### सर्विस इंस्टॉल करना

1. **Terminal खोलें**

2. **bin फोल्डर पर जाएँ**
   ```bash
   cd /opt/digna/bin
   ```

3. **इंस्टॉलेशन स्क्रिप्ट चलाएँ**
   ```bash
   sudo ./install_service.sh
   ```

digna सर्वर अब launchd के साथ रजिस्टर हो गया है और **ऑटोमेटिक स्टार्टअप** सक्षम है। सर्विस तुरंत शुरू नहीं होती — इसे शुरू करने के लिए अगला सेक्शन देखें।

### सर्विस शुरू करना और रोकना

#### सर्विस शुरू करने के लिए

1. Terminal खोलें
2. `/opt/digna/bin` पर जाएँ
3. चलाएँ:
   ```bash
   sudo ./start_service.sh
   ```

#### सर्विस रोकने के लिए

1. Terminal खोलें
2. `/opt/digna/bin` पर जाएँ
3. चलाएँ:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "सुझाव"

    एप्लिकेशन फ़ाइलों को अपडेट करने से पहले हमेशा सर्विस को रोकें।

### सर्विस को सत्यापित करना

यह पुष्टि करने के लिए कि सर्विस रजिस्टर और रन कर रही है:

```bash
sudo launchctl list | grep digna
```

यदि पहली कॉलम में प्रक्रिया ID के साथ एक लाइन शुरू होती है तो सर्विस चल रही है। पहले कॉलम में `-` होने का मतलब है कि यह रजिस्टर तो है पर रुकी हुई है।

### सर्विस को नई डायरेक्टरी पर ले जाना

launchd executable का absolute पाथ स्टोर करता है, इसलिए इंस्टॉलेशन को स्थानांतरित करने पर सर्विस को पुनः रजिस्टर करना आवश्यक है:

1. **वर्तमान सर्विस अनइंस्टॉल करें**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **एप्लिकेशन फाइलें मूव करें**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **सर्विस पुनः इंस्टॉल करें**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **सर्विस शुरू करें**
   ```bash
   sudo ./start_service.sh
   ```

### सर्विस अनइंस्टॉल करना

1. **चल रही सर्विस रोकें**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **सर्विस अनइंस्टॉल करें**
   ```bash
   sudo ./uninstall_service.sh
   ```

अब digna सर्वर launchd से अनरजिस्टर हो चुका है।

---

## नए रिलीज़ में अपग्रेड करना {: #upgrading-to-a-new-release }

यह अनुभाग रिलीज़ 2026.06 के इंस्टॉलेशन को रिलीज़ 2026.11 में अपग्रेड करता है।

!!! warning "2026.06 से पुराने रिलीज़ से अपग्रेड"

    पहले रिलीज़ 2026.06 के अपग्रेड चरण पूरे करें: [नए रिलीज़ में अपग्रेड करना](../Release%202026.06/installation_guide_digna_macos_2026_06.md#upgrading-to-a-new-release)। इसके बाद नीचे दिए गए चरणों के साथ आगे बढ़ें।

### अपग्रेड करने से पहले

**digna रिपॉज़िटरी का बैकअप बनाना अनिवार्य है**

digna को अपग्रेड करने से पहले अपने रिपॉज़िटरी (PostgreSQL) का बैकअप लें ताकि डेटा लॉस से बचा जा सके।
बैकअप यह सुनिश्चित करता है कि यदि अपग्रेड के दौरान अनपेक्षित समस्याएँ आयीं तो आप रिकवर कर सकें।

Terminal से बैकअप बनाने के लिए:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**रिलीज़ 2026.11 के लिए लाइसेंस फ़ाइल का अनुरोध करना**

रिलीज़ 2026.11 को एक नई `license.toml` की आवश्यकता है। शुरू करने से पहले digna टीम से इसका अनुरोध करें, और
इसे [चरण 7](#step-7-replace-the-license-file) के लिए तैयार रखें।

### अपग्रेड प्रक्रिया

#### चरण 1: digna सेवा बंद करें {: #step-1-stop-the-digna-service }

यदि digna बैकग्राउंड सेवा के रूप में चल रहा है, तो पहले उसे बंद करें:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

यदि digna फ़ोरग्राउंड में चल रहा है, तो उसकी Terminal विंडो में ++ctrl+c++ दबाएँ।

#### चरण 2: वर्तमान इंस्टॉलेशन का बैकअप लें {: #step-2-backup-current-installation }

अपनी digna इंस्टॉलेशन डायरेक्टरी में वर्तमान इंस्टॉलेशन की executable और डैशबोर्ड फ़ोल्डर के नाम बदलें,
ताकि नई रिलीज़ उनके साथ डिप्लॉय की जा सके:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

`digna_old` को तब तक रखें जब तक आप अपग्रेड की पुष्टि न कर लें, और `dashboard_old` को तब तक जब तक आप उससे
अपनी कॉन्फ़िगरेशन फ़ाइलें पुनर्स्थापित न कर लें (चरण 4 देखें)। उसके बाद आप दोनों को हटा सकते हैं।

#### चरण 3: नया वर्शन निकालें और डिप्लॉय करें {: #step-3-extract-and-deploy-new-version }

1. नई digna इंस्टॉलेशन ZIP फ़ाइल निकालें
2. नई `digna` executable और `dashboard` फ़ोल्डर को अपनी इंस्टॉलेशन डायरेक्टरी में कॉपी करें
3. executable बिट पुनर्स्थापित करें और, यदि आवश्यक हो, क्वारैंटाइन एट्रिब्यूट हटाएँ:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "महत्वपूर्ण"

    न तो `config.toml` और न ही `dashboard/dashboard_config.toml` कभी भी
    इंस्टॉलेशन ZIP में शामिल की जाती है — digna टीम इनमें से कोई भी फ़ाइल कभी नहीं भेजती। इसलिए अपग्रेड से
    आपकी मौजूदा कॉन्फ़िगरेशन अप्रभावित रहती है, और नाम बदले गए `*_old` फ़ोल्डरों में मौजूद प्रतियाँ ही
    आपके पास एकमात्र प्रतियाँ हैं।

#### चरण 4: अपनी कॉन्फ़िगरेशन फ़ाइलें पुनर्स्थापित करें {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

रिलीज़ 2026.11 को `config.toml` में किसी बदलाव की आवश्यकता नहीं है: जो फ़ाइल रिलीज़ 2026.06 के साथ काम करती है,
वह काम करती रहती है। दो बदलाव वैकल्पिक हैं:

- यदि डेटाबेस कनेक्शनों को digna Engine का उपयोग करना है और उसके डिफ़ॉल्ट आपके होस्ट के अनुकूल नहीं हैं, तो
  एक [`[duckdb]` सेक्शन](#duckdb-section) जोड़ें।
- यदि कोई रिवर्स प्रॉक्सी डैशबोर्ड और बैकएंड को एक ही origin के अंतर्गत सर्व करता है, तो `[app]` सेक्शन
  छोड़ दें।

!!! warning "वे सेटिंग्स जिन्हें digna नहीं पढ़ता"

    इस गाइड के पुराने संस्करणों में कुछ ऐसी सेटिंग्स दिखाई गई थीं जिन्हें digna नहीं पढ़ता। उनका कोई
    प्रभाव नहीं होता, और चरण 6 में `config check` उन्हें **Unknown keys** के अंतर्गत सूचीबद्ध करता है। उन्हें
    हटाएँ या ठीक करें:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` और
      `digna_LOGGING_BACKUP_COUNT` मौजूद नहीं हैं। उन्हें हटाएँ।
    - सेटिंग के नाम केस-संवेदी हैं। digna `DIGNA_REPO_HOST` पढ़ता है, `digna_REPO_HOST` नहीं।
      हर नाम बड़े अक्षरों में लिखें, जैसा [बैकएंड कॉन्फ़िगरेशन](#backend-configuration) में है।

!!! warning "सिंगल साइन-ऑन: [[oidc_clients]] बनाए रखें"

    digna सिंगल साइन-ऑन प्रदाताओं को `[[oidc_clients]]` प्रविष्टियों की सूची के रूप में पढ़ता है, जिनमें से
    हर एक का अपना `DIGNA_OIDC_KEY` होता है। यदि आपने अपने प्रदाताओं को `[oidc_clients.<key>]` सेक्शनों में
    बदल दिया था, जैसा इस गाइड के एक पुराने संस्करण में दिखाया गया था, तो उन्हें वापस बदलें। जब तक वह रूप
    बना रहता है, `config check` `OIDC config(s)` को FAILED बताता है:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    हर प्रदाता के लिए प्रविष्टि दोहराएँ, और हर `DIGNA_OIDC_KEY` को `dashboard_config.toml` की `key` के समान
    रखें। यह केवल उन इंस्टॉलेशनों को प्रभावित करता है जो सिंगल साइन-ऑन का उपयोग करते हैं।

#### चरण 5: वेब सर्वर रीलोड करें {: #step-5-reload-the-web-server }

डैशबोर्ड स्टैटिक फ़ाइलों का एक सेट है, इसलिए आपका वेब सर्वर — और ब्राउज़र — अभी भी
पिछला वर्शन दिखा सकते हैं। जो भी वेब सर्वर `dashboard` फ़ोल्डर को होस्ट करता है, उसे रीलोड या रीस्टार्ट करें,
फिर हार्ड रिफ़्रेश (++cmd+shift+r++) के साथ पेज रीलोड करें।

#### चरण 6: कॉन्फ़िगरेशन जाँचें {: #step-6-validate-the-configuration }

रिपॉज़िटरी को छूने से पहले पुष्टि करें कि `config.toml` पूर्ण है:

```bash
./digna config check
```

प्रत्येक सेक्शन को OK बताना चाहिए। जो कुछ भी FAILED बताया जाए उसे ठीक करें, **Unknown keys** के अंतर्गत
सूचीबद्ध कुंजियाँ हटाएँ, और आगे बढ़ने से पहले कमांड फिर चलाएँ।

#### चरण 7: लाइसेंस फ़ाइल बदलें {: #step-7-replace-the-license-file }

सामान्यतः लाइसेंस फ़ाइल एक रिलीज़ से अगली रिलीज़ में भी काम करती रहती है। रिलीज़ 2026.11 इसका अपवाद है: यह
दो लाइसेंस वाले मॉड्यूल जोड़ती है, digna Data Reconciliation और digna Agentic, और 2026.11 से पहले जारी किए गए
लाइसेंस में ये शामिल नहीं हैं। digna टीम द्वारा रिलीज़ 2026.11 के लिए दी गई `license.toml` को
इंस्टॉलेशन डायरेक्टरी में कॉपी करें, जिससे पुरानी फ़ाइल बदल जाए:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "पिछला लाइसेंस न रखें"

    पिछले लाइसेंस के साथ digna फिर भी शुरू होता है, लेकिन digna Data Reconciliation और digna
    MCP Server बंद रहते हैं। लाइसेंस की जाँच करने वाला हर कमांड — `user`,
    `inspection`, `repo` — जाँच विफल होने पर रिपॉज़िटरी को छूने से पहले ही रुक जाता है। आगे बढ़ने से
    पहले नए लाइसेंस को सत्यापित करें:

    ```bash
    ./digna license check
    ```

#### चरण 8: रिपॉज़िटरी स्कीमा अपग्रेड करें {: #step-8-upgrade-the-repository-schema }

अपनी digna इंस्टॉलेशन डायरेक्टरी में चलाएँ:

```bash
cd /opt/digna
./digna repo upgrade
```

रिलीज़ 2026.11 रिपॉज़िटरी स्कीमा को संस्करणबद्ध माइग्रेशनों से प्रबंधित करती है। किसी पिछली रिलीज़ से पहला
अपग्रेड स्कीमा को पिछली पद्धति के अंतिम संस्करण तक लाता है, उसे अपने प्रारंभिक बिंदु के रूप में दर्ज करता है,
और फिर रिलीज़ 2026.11 के माइग्रेशन लागू करता है। यह इस संदेश के साथ समाप्त होता है:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

सभी मौजूदा डेटा संरक्षित रहता है। किसी भी समय रिपॉज़िटरी की स्थिति देखने के लिए
`./digna repo check` चलाएँ: यह अंतिम लागू माइग्रेशन और कोई भी लंबित माइग्रेशन सूचीबद्ध करता है।

!!! warning "पुरानी रिपॉज़िटरी पर digna शुरू नहीं होता"

    रिलीज़ 2026.11 से, जब तक रिपॉज़िटरी को अपग्रेड की आवश्यकता है, सर्वर शुरू होने से इनकार करता है और
    इसकी सूचना देता है, उदाहरण के लिए:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    सर्वर या सेवा शुरू करने से पहले `repo upgrade` चलाएँ।

#### चरण 9: सेवाएँ पुनः प्रारंभ करें {: #step-9-restart-services }

यदि बैकग्राउंड सेवा के रूप में चल रहा है:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

यदि मैन्युअल रूप से चला रहे हैं, तो सर्वर पुनरारंभ करें:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

यदि nginx या Apache का उपयोग कर रहे हैं, तो संबंधित वेब सर्वर रीस्टार्ट करें:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### चरण 10: अपग्रेड सत्यापित करें {: #step-10-verify-the-upgrade }

1. नई executable की रिलीज़ की पुष्टि करें:

    ```bash
    ./digna version
    ```

    पहली पंक्ति में `Release: 2026.11` होना चाहिए।

2. digna डैशबोर्ड एक्सेस करें और सुनिश्चित करें कि इंटरफ़ेस सही ढंग से लोड हो रहा है।
3. त्रुटियों के लिए सर्वर आउटपुट और `logs` डायरेक्टरी की फ़ाइलें जाँचें।
4. अपने डेटाबेस कनेक्शनों का परीक्षण करें — देखें
   [कनेक्शन का परीक्षण](../../../databases/overview.md#testing-a-connection)। रिलीज़ 2026.06 से पहले की रिलीज़
   से अपग्रेड के बाद, पहले हर उस कनेक्शन को ODBC में बदलें जो अभी तक ODBC का उपयोग नहीं करता था।

नए मॉड्यूल के साथ शुरुआत करने के लिए देखें [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
digna MCP Server के लिए [AI एजेंट कनेक्ट करना](../../../platform/agentic/connect_ai_agent.md), और
digna Engine के लिए [प्रोफाइलिंग लोकेशन](../../../platform/profiling/profiling_location.md)।
