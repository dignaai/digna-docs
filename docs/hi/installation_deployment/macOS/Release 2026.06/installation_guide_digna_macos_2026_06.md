---
title: macOS इंस्टॉलेशन गाइड – digna रिलीज 2026.06 | digna डॉ큐मेंटेशन
description: macOS पर digna रिलीज 2026.06 इंस्टॉल करने के चरण-दर-चरण निर्देश — सिस्टम आवश्यकताएँ, Homebrew और PostgreSQL सेटअप, nginx या Apache कॉन्फ़िगरेशन, बैकएंड और डैशबोर्ड कॉन्फ़िगरेशन, digna को बैकग्राउंड सेवा के रूप में चलाना, और नए रिलीज़ में अपग्रेड करना।
keywords: digna macOS इंस्टॉलेशन, digna mac डिप्लॉयमेंट गाइड, digna बैकएंड सेटअप, digna डैशबोर्ड इंस्टॉलेशन, postgresql homebrew, nginx macOS, digna launchd सेवा, digna अपग्रेड गाइड
image: /assets/logo_square.png
---

# macOS इंस्टॉलेशन गाइड — digna रिलीज 2026.06

**रिलीज:** 2026.06

**अंतिम अद्यतन:** 5 सितम्बर, 2026


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

- **dignabackend**: एप्लिकेशन का कोर इंजन, जो डेटा प्रोसेसिंग और गुणवत्ता जाँच के लिए जिम्मेदार है।
- **dignadashboard**: एक वेब-आधारित इंटरफ़ेस जो वेब सर्वर पर होस्ट होता है और digna प्लेटफ़ॉर्म के साथ इंटरैक्ट करने तथा डेटा गुणवत्ता मीट्रिक्स को विज़ुअलाइज़ करने का उपयोगकर्ता-अनुकूल तरीका प्रदान करता है।

### रिलीज 2026.06 में नया क्या है

यह रिलीज़ डेटा ऑब्ज़र्वेबिलिटी क्षमताएँ सीधे आपके कोड के अंदर लाती है, जिससे डेवलपर स्रोत पर ही डेटा गुणवत्ता की निगरानी कर सकते हैं। पूर्ण विवरण के लिए देखें [release notes](http://docs.digna.ai/changelog/Release_202606/).

### क्या आप Windows या Linux ढूंढ रहे हैं?

यह गाइड macOS के लिए है। अन्य प्लेटफार्मों के लिए देखें [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) या [Linux Installation Guide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

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

    इसका मतलब है कि एक फ्रेश Homebrew इंस्टॉलेशन पर `postgres` रोल मौजूद नहीं होता। जब आपको सुपरयूज़र की आवश्यकता हो तब अपने अकाउंट नाम का उपयोग करें, और Initial Installation में बताए अनुसार एक स्पष्ट digna यूज़र बनाएं।

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
   - `config.toml` — कॉन्फ़िगरेशन फ़ाइल
   - `license.toml` — लाइसेंस फ़ाइल (अपनी फ़ाइल यहाँ कॉपी करें)

Terminal से अनज़िप करने के लिए:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
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
| `digna_APP_PORT` | `8082` (डिफ़ॉल्ट) | REST API एंडपॉइंट के लिए पोर्ट |
| `digna_APP_CORS_ALLOW_ORIGINS` | फ्रंटेंड URL | यदि डैशबोर्ड किसी अलग सर्वर पर है, तो उसका URL यहाँ शामिल करें |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | क्रेडेंशियल्स के साथ CORS के लिए आवश्यक |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | सभी HTTP मेथड्स की अनुमति दें |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | सभी हेडर्स की अनुमति दें |

!!! note "नोट"

    यदि आप डैशबोर्ड को Homebrew के nginx पर उसके डिफ़ॉल्ट पोर्ट पर सर्व कर रहे हैं, तो अनुमति देने के लिए origin `http://localhost:8080` है।

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
| `digna_REPO_DB` | `postgres` | डेटाबेस का नाम |
| `digna_REPO_SCHEMA` | `dignarepo` | पहले बनाया गया schema |
| `digna_REPO_USER` | `digna_user` | PostgreSQL सेटअप में बनाया गया यूज़र |
| `digna_REPO_PASSWORD` | आपका पासवर्ड | schema क्रिएशन के दौरान सेट किया गया पासवर्ड |

#### [base] सेक्शन

यह सेक्शन सुरक्षा और कुकी सेटिंग्स को रखता है:

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
| `digna_FERNET_KEY` | एन्क्रिप्शन कुंजी | टोकन और कुकीज़ को एन्क्रिप्ट करने के लिए उपयोग होती है (डिफ़ॉल्ट प्रदान किया गया) |
| `digna_COOKIE_DOMAIN` | `localhost` | अपने फ्रंटेंड डोमेन से मेल खाएं |
| `digna_COOKIE_SECURE` | `false` (लोकल) / `true` (प्रोडक्शन) | HTTPS कनेक्शनों के लिए `true` का उपयोग करें |
| `digna_COOKIE_HTTPONLY` | `true` | सुरक्षा के लिए हमेशा सक्षम रखें |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF हमलों को रोकने में मदद करता है |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 घंटे) | सेकंड में सत्र समयसीमा |
| `digna_MAX_WORKERS` | Number of CPU cores - 1 | समानांतर निरीक्षण कार्यों की संख्या |

!!! tip "सुझाव"

    अपने Mac पर उपलब्ध CPU कोर की संख्या जानने के लिए चलाएँ `sysctl -n hw.ncpu`।

#### [logging] सेक्शन

यह सेक्शन लॉगिंग व्यवहार को कॉन्फ़िगर करता है:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| पैरामीटर | मान | नोट्स |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` या `DEBUG` | प्रोडक्शन के लिए `INFO`, त्रुटि निवारण के लिए `DEBUG` |
| `digna_LOGGING_BACKUP_COUNT` | `10` | प्रतिदिन के लॉग बैकअप की प्रतियाँ रखने की संख्या |

---

### चरण 2: Repository इनिशियलाइज़ करें

1. **Terminal** खोलें
2. अपने digna इंस्टॉलेशन डायरेक्टरी पर जाएँ (जहाँ `config.toml` और `digna` executable स्थित हैं)
3. कनेक्शन टेस्ट चलाएँ:

```bash
cd /opt/digna
./digna repo check
```

आपको पुष्टि दिखनी चाहिए कि कनेक्शन स्थापित है (रिपॉज़िटरी स्वयं अभी इनिशियलाइज़ नहीं हुई है)।

!!! note "नोट"

    macOS पर, करंट डायरेक्टरी में कमांड्स आपके PATH पर नहीं होते, इसलिए executable को `./digna` के रूप में ही चलाया जाता है न कि `digna` के रूप में। शॉर्टर रूप हर जगह उपयोग करने के लिए इंस्टॉलेशन डायरेक्टरी को अपने PATH में जोड़ें:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### चरण 3: Repository Schema इंस्टॉल करें

उसी डायरेक्टरी में चलाएँ:

```bash
./digna repo install
```

यह कमांड आपके PostgreSQL डेटाबेस में आवश्यक टेबल और schema इंस्टॉल करती है।

### चरण 4: digna सर्वर शुरू करें

digna इंस्टॉलेशन डायरेक्टरी में सर्वर शुरू करें:

```bash
./digna serve --address <host> --port <port>
```

**पैरामीटर:**
- `--address` — सर्वर होस्टनाम/IP
- `--port` — सर्वर पोर्ट

आपको स्टार्टअप संदेश दिखाई देने चाहिए जो पुष्टि करें कि सर्वर चल रहा है:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "सुझाव"

    पहली बार सर्वर शुरू करने पर macOS आपसे पूछ सकता है कि क्या आप एप्लिकेशन को इनकमिंग नेटवर्क कनेक्शनों को स्वीकार करने की अनुमति देना चाहते हैं। **Allow** पर क्लिक करें, अन्यथा डैशबोर्ड बैकएंड से कनेक्ट नहीं कर पाएगा।

### चरण 5: एक Admin यूज़र बनायें

1. एक **नया** Terminal विंडो खोलें
2. अपने digna इंस्टॉलेशन डायरेक्टरी पर जाएँ
3. एक एडमिन यूज़र बनाने के लिए निम्न कमांड चलाएँ:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**उदाहरण:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

यह `admin` नाम का यूज़र और पूर्ण प्रशासकीय विशेषाधिकार के साथ एक यूज़र बनाएगा।

!!! tip "सुझाव"

    पासवर्ड को सिंगल कोट्स में रखें। `zsh` जैसे शेल `!`, `$` और `*` जैसे करैक्टर को विशेष मानते हैं; बिना उद्धरण के ऐसे पासवर्ड सही तरीके से पारित नहीं होंगे।

!!! tip "सर्वोत्तम प्रथा"

    बड़े, छोटे अक्षर, संख्याएँ और स्पेशल करैक्टर मिलाकर मजबूत पासवर्ड उपयोग करें।

---

## डैशबोर्ड कॉन्फ़िगरेशन {: #dashboard-configuration }

### चरण 1: डैशबोर्ड को वेब सर्वर पर डिप्लॉय करें

digna डैशबोर्ड की अपनी अलग `config.toml` फ़ाइल `dashboard/` डायरेक्टरी में स्थित है। यह कॉन्फ़िगरेशन पहले से प्रदान की गई होती है और प्रारम्भिक सेटअप के दौरान बदलने की आवश्यकता नहीं है। केवल तभी संशोधित करें जब बैकएंड कनेक्शन कस्टमाइज़ करना हो।

यदि आपको डैशबोर्ड कॉन्फ़िगरेशन बदलने की आवश्यकता है (उदा., मल्टी-इन्स्टेंस डिप्लॉयमेंट के लिए), तो डैशबोर्ड के डॉक्यूमेंटेशन को देखें।

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

### अपग्रेड करने से पहले

**digna Repository बैकअप बनाना अनिवार्य है**

digna को अपग्रेड करने से पहले अपने रिपॉज़िटरी (PostgreSQL) का बैकअप लें ताकि डेटा लॉस से बचा जा सके।
बैकअप यह सुनिश्चित करता है कि अपग्रेड में अप्रत्याशित समस्याएँ आने पर आप पुनर्प्राप्त कर सकें।

Terminal से बैकअप बनाने के लिए:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### अपग्रेड प्रक्रिया

#### चरण 1: digna सर्विस रोकें

यदि digna बैकग्राउंड सेवा के रूप में चल रहा है, तो पहले इसे रोकें:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

यदि digna फ़ोरग्राउंड में चल रहा है, तो उसके Terminal विंडो में `Ctrl + C` दबाएँ।

#### चरण 2: वर्तमान बैकएंड इंस्टॉलेशन का बैकअप लें

अपने digna इंस्टॉलेशन डायरेक्टरी में:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### चरण 3: नई वर्ज़न को एक्सट्रैक्ट और डिप्लॉय करें

1. नई digna इंस्टॉलेशन ZIP फ़ाइल एक्सट्रैक्ट करें
2. नई `digna` executable और `dashboard` फ़ोल्डर को अपनी इंस्टॉलेशन डायरेक्टरी में कॉपी करें
3. executable बिट पुनर्स्थापित करें और यदि आवश्यक हो तो क्वारैंटाइन एट्रिब्यूट निकालें:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "महत्वपूर्ण"

    `config.toml` फ़ाइल इंस्टॉलेशन ZIP में **कभी भी** शामिल नहीं होती। आपकी मौजूदा कॉन्फ़िगरेशन सुरक्षित रहती है।

### चरण 4: अपनी कॉन्फ़िगरेशन फ़ाइलें पुनर्स्थापित करें

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### चरण 5: Repository Schema को अपग्रेड करें

अपने digna इंस्टॉलेशन डायरेक्टरी पर जाकर चलाएँ:

```bash
cd /opt/digna
./digna repo upgrade
```

यह PostgreSQL schema को नवीनतम वर्ज़न में अपडेट करेगा जबकि सभी मौजूदा डेटा सुरक्षित रहेंगे।

### चरण 6: सर्विसेज़ पुनः आरंभ करें

यदि बैकग्राउंड सर्विस के रूप में चल रहा है:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

यदि मैन्युअली चलाते हैं, तो सर्वर को फिर से शुरू करें:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

यदि आप nginx या Apache का उपयोग कर रहे हैं, तो संबंधित वेब सर्वर को रीस्टार्ट करें:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### चरण 7: अपग्रेड की पुष्टि करें

1. digna डैशबोर्ड एक्सेस करें
2. सत्यापित करें कि इंटरफ़ेस सही ढंग से लोड होता है
3. किसी भी त्रुटि के लिए सर्वर लॉग्स की जाँच करें