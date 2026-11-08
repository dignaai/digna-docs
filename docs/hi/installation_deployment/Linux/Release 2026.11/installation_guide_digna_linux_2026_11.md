---
title: Linux स्थापना मार्गदर्शिका – digna रिलीज 2026.11 | digna प्रलेखन
description: Linux पर digna रिलीज 2026.11 स्थापित करने के लिए चरण-दर-चरण मार्गदर्शिका — सिस्टम आवश्यकताएँ, PostgreSQL सेटअप, nginx या Apache विन्यास, backend और dashboard कॉन्फ़िगरेशन, digna को systemd सेवा के रूप में चलाना, और रिलीज़ 2026.06 से अपग्रेड करना।
keywords: digna लिनक्स स्थापना, digna डिप्लॉयमेंट गाइड, digna backend सेटअप, digna डैशबोर्ड स्थापना, postgresql linux, nginx linux, digna systemd सेवा, digna अपग्रेड गाइड
image: /assets/logo_square.png
---

# digna रिलीज 2026.11 के लिए Linux स्थापना मार्गदर्शिका

**रिलीज़:** 2026.11

**अंतिम अपडेट:** 7 नवंबर, 2026


---

## सामग्री सूची

1. [परिचय](#introduction)
2. [सिस्टम आवश्यकताएँ](#system-requirements)
3. [पूर्व-स्थापन सेटअप](#pre-installation-setup)
4. [PostgreSQL सर्वर सेटअप](#postgresql-server-setup)
5. [वेब सर्वर विन्यास](#web-server-configuration)
6. [प्रारम्भिक स्थापना](#initial-installation)
7. [बैकएंड कॉन्फ़िगरेशन](#backend-configuration)
8. [डैशबोर्ड कॉन्फ़िगरेशन](#dashboard-configuration)
9. [digna को systemd सेवा के रूप में चलाना](#running-digna-as-a-systemd-service)
10. [नए रिलीज़ में अपग्रेड करना](#upgrading-to-a-new-release)

---

## परिचय {: #introduction }

### digna के बारे में

digna एक व्यापक AI-संचालित प्लेटफ़ॉर्म है जो वेयरहाउस, लेक्स और लेकहाउस जैसे विभिन्न डेटा वातावरणों में डेटा गुणवत्ता प्रबंधन को अनुकूलित करने के लिए डिज़ाइन किया गया है। यह उच्च मात्रा में स्केलेबल और अनुकूलनीय है और ऑटोमेशन, वास्तविक समय निगरानी और अनोमली डिटेक्शन के माध्यम से आधुनिक डेटा चुनौतियों को संबोधित करता है।

digna दो मुख्य घटकों से मिलकर बनता है:

- **digna**: एप्लिकेशन का केंद्र, जो डेटा संसाधित करने और गुणवत्ता जाँच चलाने के लिए ज़िम्मेदार है। यह बैकएंड और कमांड लाइन इंटरफ़ेस को एक ही निष्पादन योग्य फ़ाइल में जोड़ता है और पिछली रिलीज़ के अलग-अलग प्रोग्राम `dignabackend` तथा `dignacli` की जगह लेता है।
- **dignadashboard**: एक वेब-आधारित इंटरफ़ेस जो वेब सर्वर पर होस्ट किया जाता है और digna प्लेटफ़ॉर्म के साथ इंटरैक्ट करने व डेटा गुणवत्ता मेट्रिक्स को विज़ुअलाइज़ करने का यूजर-फ्रेंडली तरीका प्रदान करता है।

### रिलीज 2026.11 में क्या नया है

यह रिलीज़ digna Data Reconciliation, digna MCP Server के साथ digna Agentic, और digna Engine जोड़ती है, जो digna के भीतर डेटा को प्रोफाइल कर सकता है और अलग-अलग डेटाबेस तकनीकों के बीच रेफरेंशियल इंटीग्रिटी की जाँच कर सकता है। पूर्ण विवरण के लिए देखें [रिलीज़ नोट्स](../../../changelog/Release_202611.md)।

इंस्टॉलेशन के लिए यह रिलीज़ एक नया रिपॉज़िटरी माइग्रेशन तंत्र, digna Engine के लिए `config.toml` में एक वैकल्पिक `[duckdb]` सेक्शन, और एक नई लाइसेंस फ़ाइल लाती है। [अपग्रेड सेक्शन](#upgrading-to-a-new-release) इनमें से हर एक को कवर करता है।

### Windows या macOS के लिए मार्गदर्शिका चाहिए?

यह गाइड Linux को कवर करता है। अन्य प्लेटफार्मों के लिए देखें [Windows Installation Guide](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) या [macOS Installation Guide](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md)।

### यह गाइड किस वितरण के लिए है?

निर्देश दोनों सामान्य सर्वर परिवारों के लिए लिखे गए हैं। जहाँ फर्क होता है, दोनों कमान्ड दिए गए हैं:

- **Debian परिवार** — Debian, Ubuntu। पैकेज मैनेजर: `apt`.
- **RHEL परिवार** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora। पैकेज मैनेजर: `dnf`.

कोई भी आधुनिक वितरण जिसमें `systemd` है काम करेगा; केवल पैकेज नाम और कुछ कॉन्फ़िगरेशन पाथ बदलते हैं।

---

## सिस्टम आवश्यकताएँ {: #system-requirements }

स्थापना शुरू करने से पहले सुनिश्चित करें कि आपका सिस्टम निम्न न्यूनतम आवश्यकताओं को पूरा करता है:

| आवश्यकता | विनिर्देश |
|---|---|
| **ऑपरेटिंग सिस्टम** | Ubuntu 22.04 LTS या बाद का, Debian 12 या बाद का, RHEL 9 / Rocky 9 / AlmaLinux 9 या बाद का |
| **आर्किटेक्चर** | x86_64 (amd64) या arm64 |
| **Init सिस्टम** | systemd |
| **मेमोरी (न्यूनतम सेटअप)** | 16 GB RAM |
| **डिस्क स्थान** | 10 GB उपलब्ध स्टोरेज |
| **डेटाबेस** | PostgreSQL Server 12 या उच्चतर |
| **वेब सर्वर** | nginx, Apache httpd, या समकक्ष |

!!! info "digna Engine"

    जो डेटाबेस कनेक्शन प्रोफाइलिंग लोकेशन के रूप में digna Engine का उपयोग करते हैं, उन्हें स्वयं
    digna होस्ट पर प्रोफाइल किया जाता है। उनके लिए अतिरिक्त मेमोरी और डिस्क स्थान की योजना बनाएँ, देखें
    [\[duckdb\] सेक्शन](#duckdb-section)।

### डेटाबेस इंस्टॉलेशन विकल्प

**यदि PostgreSQL पहले से इंस्टॉल है:**
आप अपने मौजूदा PostgreSQL सर्वर में digna के लिए नया डेटाबेस जोड़ सकते हैं।

**यदि आप PostgreSQL को उसी मशीन पर इंस्टॉल कर रहे हैं जहाँ digna चलेगा:**

!!! info "अनुशंसित विनिर्देश"

    - **मेमोरी**: 32 GB RAM (16 GB की बजाय)
    - **डिस्क स्थान**: 50 GB उपलब्ध स्टोरेज (10 GB की बजाय)

    ये उच्च विनिर्देश digna और PostgreSQL डेटाबेस दोनों को एक साथ चलाने के लिए सहायक हैं।

### अपना वितरण और आर्किटेक्चर कैसे जाँचें

इस गाइड में कई कमान्ड Debian और RHEL परिवारों के बीच अलग हैं। यह जाँचने के लिए चलाएँ:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` या `ID=debian` — `apt` कमान्ड का उपयोग करें।
- `ID=rhel`, `rocky`, `almalinux` या `fedora` — `dnf` कमान्ड का उपयोग करें।
- `x86_64` या `aarch64` — उस आर्किटेक्चर का नाम जिसका इंस्टॉलेशन पैकेज आपको चाहिए।

---

## पूर्व-स्थापन सेटअप {: #pre-installation-setup }

digna स्थापित करने से पहले सुनिश्चित करें कि दो प्रमुख पूर्वापेक्षाएँ मौजूद हैं:

1. **PostgreSQL सर्वर** – गणना किए गए मेट्रिक्स और प्रदर्शन डेटा संग्रहीत करने के लिए
2. **वेब सर्वर** – digna Dashboard को होस्ट करने के लिए

यदि ये कंपोनेंट पहले से सेटअप नहीं हैं, तो उन्हें इंस्टॉल और कॉन्फ़िगर करने के लिए नीचे दिए गए सेक्शन का पालन करें।

### पैकेज इंडेक्स रिफ्रेश करना

कुछ भी इंस्टॉल करने से पहले अपने पैकेज लिस्ट अपडेट करें:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "नोट"

    इस गाइड में जोड़ी में दी गई पहली कमान्ड **Debian परिवार** के लिए है और दूसरी **RHEL परिवार** के लिए। केवल वही कमान्ड चलाएँ जो आपके सिस्टम से मेल खाती हो।

---

## PostgreSQL सर्वर सेटअप {: #postgresql-server-setup }

### यदि आपके पास पहले से PostgreSQL है

यदि PostgreSQL स्थानीय मशीन पर पहले से इंस्टॉल और चल रहा है या आप किसी मैनेज्ड रिमोट PostgreSQL सर्वर का उपयोग कर रहे हैं, तो आप [अगले सेक्शन](#web-server-configuration) पर जा सकते हैं।

### PostgreSQL इंस्टॉल करना

#### चरण 1: सर्वर पैकेज इंस्टॉल करें

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "टिप"

    वितरण के पैकेज वर्तमान PostgreSQL रिलीज़ से पीछे हो सकते हैं। यदि आपको किसी विशिष्ट नए संस्करण की आवश्यकता है, तो आधिकारिक [PostgreSQL apt या yum रिपोजिटरी](https://www.postgresql.org/download/linux/) का उपयोग करें।

#### चरण 2: डेटाबेस क्लस्टर इनिशियलाइज़ करें

**Debian परिवार** पर पैकेज क्लस्टर स्वतः बना देता है और शुरू कर देता है — अगले चरण पर जाएँ।

**RHEL परिवार** पर क्लस्टर को स्पष्ट रूप से बनाया जाना चाहिए:

```bash
sudo postgresql-setup --initdb
```

#### चरण 3: सेवा शुरू और सक्षम करें

```bash
sudo systemctl enable --now postgresql
```

यह PostgreSQL को तुरंत शुरू कर देता है और बूट पर ऑटो स्टार्ट के लिए कॉन्फ़िगर कर देता है।

#### चरण 4: इंस्टॉलेशन सत्यापित करें

```bash
psql --version
sudo systemctl status postgresql
```

आपको PostgreSQL का वर्ज़न और `active (running)` सेवा दिखना चाहिए।

#### चरण 5: सर्वर से कनेक्ट करें

एक Linux PostgreSQL पैकेज `postgres` सिस्टम अकाउंट बनाता है जो क्लस्टर का मालिक होता है। इसके माध्यम से कनेक्ट करें:

```bash
sudo -u postgres psql
```

!!! note "नोट — Linux यहाँ Windows से अलग है"

    Windows इंस्टॉलर सेटअप के दौरान `postgres` सुपरयूज़र के लिए पासवर्ड सेट करने के लिए कहता है। Linux पैकेज ऐसा नहीं करते। इसके बजाय लोकल कनेक्शन्स **peer authentication** द्वारा प्रमाणीकृत होती हैं: `postgres` ऑपरेटिंग-सिस्टम उपयोगकर्ता को बिना पासवर्ड के `postgres` डेटाबेस उपयोगकर्ता के रूप में कनेक्ट करने की अनुमति होती है।

    इसलिए ऊपर दिया गया कमान्ड `sudo -u postgres` का उपयोग करता है। digna backend TCP के ऊपर उपयोगकर्ता नाम और पासवर्ड के साथ कनेक्ट करता है, इसलिए आप [Initial Installation](#initial-installation) में एक स्पष्ट digna उपयोगकर्ता बनाएँगे।

#### चरण 6: पोर्ट की पुष्टि करें

डिफ़ॉल्ट PostgreSQL पोर्ट `5432` है। यह पुष्टि करने के लिए कि आपका सर्वर किस पोर्ट पर सुन रहा है:

```bash
sudo -u postgres psql -c "SHOW port;"
```

मान नोट कर लें — आपको इसे digna backend कॉन्फ़िगरेशन में चाहिए होगा।

#### चरण 7: digna उपयोगकर्ता के लिए पासवर्ड प्रमाणीकरण सक्षम करें

digna TCP पर `digna_user` के रूप में PostgreSQL से कनेक्ट करता है, जिसे peer प्रमाणीकरण के बजाय पासवर्ड प्रमाणीकरण की आवश्यकता होती है। सुनिश्चित करें कि आपका `pg_hba.conf` इसे अनुमति देता है।

फ़ाइल का स्थान खोजें:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

इसे किसी संपादक में खोलें और पुष्टि करें कि स्थानीय TCP लाइनों में `ident` की बजाय `scram-sha-256` (या पुराने सर्वरों पर `md5`) का उपयोग हो रहा है:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

किसी भी परिवर्तन के बाद PostgreSQL को रीलोड करें:

```bash
sudo systemctl reload postgresql
```

!!! warning "महत्वपूर्ण"

    यदि digna रिपोर्ट करता है `FATAL: Ident authentication failed for user "digna_user"` तो इसका कारण यही सेटिंग है।

#### चरण 8: यदि PostgreSQL किसी अन्य मशीन पर चलता है

यदि किसी अन्य होस्ट से कनेक्शन्स स्वीकार करना है, तो `postgresql.conf` में `listen_addresses` सेट करें और अपने नेटवर्क के लिए `pg_hba.conf` में एक मेल खाने वाली `host` लाइन जोड़ें:

```
listen_addresses = '*'
```

फिर फ़ायरवॉल में पोर्ट खोलें और सेवा को पुनरारंभ करें:

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## वेब सर्वर विन्यास {: #web-server-configuration }

digna को डैशबोर्ड होस्ट करने के लिए एक वेब सर्वर की आवश्यकता है। निम्न में से किसी एक विकल्प को चुनें:

- [nginx](#nginx-setup) — हल्का और अनुशंसित
- [Apache httpd](#apache-setup) — व्यापक रूप से उपयोग किया जाने वाला विकल्प

आपको केवल इनमें से **एक** सर्वर इंस्टॉल और कॉन्फ़िगर करना है।

दोनों सेक्शन उन दो चीज़ों को कॉन्फ़िगर करते हैं जिन पर डैशबोर्ड निर्भर है:

- **एक सिंगल-पेज-एप्लिकेशन फॉलबैक**, ताकि डैशबोर्ड URL रिफ्रेश करने पर 404 न लौटे
- **एक `.md` MIME टाइप**, ताकि Markdown फाइलें सही ढंग से सर्व हों

### nginx सेटअप {: #nginx-setup }

#### अवलोकन

nginx एक हल्का, उच्च-प्रदर्शन वेब सर्वर है जो static digna डैशबोर्ड सर्व करने के लिए उपयुक्त है।

#### इंस्टॉलेशन

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### nginx शुरू करना

```bash
sudo systemctl enable --now nginx
```

#### इंस्टॉलेशन सत्यापित करें

1. अपना ब्राउज़र खोलें
2. `http://localhost` पर नेविगेट करें
3. आपको nginx स्वागत पृष्ठ दिखाई देना चाहिए

#### फ़ायरवॉल खोलना

यदि सर्वर अन्य मशीनों से पहुँचा जाता है, तो HTTP ट्रैफ़िक की अनुमति दें:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### डैशबोर्ड के लिए साइट कॉन्फ़िगर करना

nginx दोनों वितरण परिवारों पर अपने `conf.d` डायरेक्टरी में हर फ़ाइल को शामिल करता है। वहाँ digna के लिए एक समर्पित कॉन्फ़िगरेशन फ़ाइल बनाएँ:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

निम्न पेस्ट करें, `/opt/digna/dashboard` को आपके निकाले गए `dashboard` फ़ोल्डर के वास्तविक पाथ से बदलना सुनिश्चित करें:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
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

    `try_files` निर्देश के बिना, रूट URL के अलावा किसी भी डैशबोर्ड पेज को रीलोड करने पर 404 लौटेगा। यह nginx का वही व्यवहार है जो Windows पर IIS के URL Rewrite मॉड्यूल की आवश्यकता को पूरा करता है।

#### डिफ़ॉल्ट साइट अक्षम करें

किसी पोर्ट के लिए केवल एक सर्वर ब्लॉक `default_server` हो सकता है। **Debian परिवार** पर पैकेज्ड डिफ़ॉल्ट को हटाएँ ताकि यह टकराव न करे:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

**RHEL परिवार** पर `/etc/nginx/nginx.conf` के अंदर `server { ... }` ब्लॉक को कमेंट या डिलीट करें।

#### कॉन्फ़िगरेशन लागू करें

सिनटैक्स त्रुटियों के लिए कॉन्फ़िगरेशन परीक्षण करें, फिर nginx रीलोड करें:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Apache httpd सेटअप {: #apache-setup }

#### अवलोकन

Apache httpd हर समर्थित वितरण के डिफ़ॉल्ट रिपॉज़िटरीज़ में उपलब्ध है। पैकेज Debian परिवार पर `apache2` नाम से और RHEL परिवार पर `httpd` नाम से आता है।

#### इंस्टॉलेशन

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Apache शुरू करना

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### इंस्टॉलेशन सत्यापित करें

1. अपना ब्राउज़र खोलें
2. `http://localhost` पर नेविगेट करें
3. आपको वितरण का डिफ़ॉल्ट Apache पेज दिखाई देना चाहिए

#### आवश्यक: mod_rewrite सक्षम करें

डैशबोर्ड को URL rewriting की आवश्यकता है।

**Debian परिवार** पर मॉड्यूल सक्षम करें और पुनरारंभ करें:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

**RHEL परिवार** पर `mod_rewrite` डिफ़ॉल्ट रूप से लोड होता है। यह पुष्टि करें:

```bash
httpd -M | grep rewrite
```

#### आवश्यक: .htaccess ओवरराइड अनुमति दें

अपने डॉक्यूमेंट रूट के लिए कॉन्फ़िगरेशन फ़ाइल खोलें:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

अपने डॉक्यूमेंट रूट (`/var/www/html` दोनों परिवारों पर) को कवर करने वाले `<Directory>` ब्लॉक को ढूँढें और बदलें:

```apache
AllowOverride None
```

को:

```apache
AllowOverride All
```

#### आवश्यक: Markdown फाइलों के लिए MIME टाइप

इसी फ़ाइल में निम्न लाइन जोड़ें ताकि Markdown फाइलें सही ढंग से सर्व हो सकें:

```apache
AddType text/markdown .md
```

!!! warning "महत्वपूर्ण"

    इस सेटिंग के बिना, `.md` फाइलें सही ढंग से सर्व नहीं हो सकती हैं।

#### कॉन्फ़िगरेशन लागू करें

सिनटैक्स त्रुटियों के लिए कॉन्फ़िगरेशन जांचें, फिर Apache पुनरारंभ करें:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## प्रारम्भिक स्थापना {: #initial-installation }

### चरण 1: digna रिपॉज़िटरी सेटअप करें

digna रिपॉज़िटरी सभी मेट्रिक्स को संग्रहित करती है जो digna द्वारा गणना किए जाते हैं। यह विश्लेषणात्मक और प्रदर्शन डेटा के लिए केंद्रीय डेटाबेस के रूप में कार्य करती है।

#### रिपॉज़िटरी स्कीमा और उपयोगकर्ता बनाएँ

अपना PostgreSQL क्लाइंट (psql, pgAdmin, या समान) खोलें और निम्न SQL कमान्ड्स चलाएँ:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**निम्न प्लेसहोल्डर्स को बदलें:**

- `<digna_repo_schema>` — अपनी इच्छित स्कीमा का नाम (उदा., `dignarepo`)
- `<digna_repo_user>` — अपना इच्छित उपयोगकर्ता नाम (उदा., `digna_user`)
- `<digna_repo_password>` — इस उपयोगकर्ता के लिए एक सुरक्षित पासवर्ड

**उदाहरण:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

शेल से इन्हें एक ही चरण में चलाने के लिए:

```bash
sudo -u postgres psql
```

फिर `postgres=#` प्रॉम्प्ट पर स्टेटमेंट पेस्ट करें और बाहर निकलने के लिए `\q` टाइप करें।

!!! tip "सर्वोत्तम प्रथा"

    डेटाबेस उपयोगकर्ताओं के लिए मजबूत, जटिल पासवर्ड का उपयोग करें। आसानी से अनुमान लगाने योग्य क्रेडेंशियल से बचें।

---

### चरण 2: digna इंस्टॉलेशन पैकेज निकालें

1. आपको प्रदान किया गया digna इंस्टॉलेशन ZIP फाइल ढूँढें
2. इसे अपने इच्छित इंस्टॉलेशन लोकेशन पर निकालें — उदाहरण के लिए `/opt/digna`
3. निकाले जाने के बाद, आपको निम्न आइटम दिखाई देने चाहिए:
   - `dashboard/` — वेब डैशबोर्ड इंटरफ़ेस
   - `digna` — मुख्य executable (backend + CLI संयुक्त)

!!! info "कॉन्फ़िगरेशन और लाइसेंस फ़ाइलें पैकेज में नहीं हैं"

    न तो `config.toml` और न ही `dashboard/dashboard_config.toml` इंस्टॉलेशन के साथ आती है — दोनों को आप
    स्वयं बनाते हैं, [बैकएंड कॉन्फ़िगरेशन](#backend-configuration) और
    [डैशबोर्ड कॉन्फ़िगरेशन](#dashboard-configuration) में। `license.toml` भी साथ नहीं आती;
    digna इसे अलग से उपलब्ध कराता है, जैसा कि चरण 3 में बताया गया है।

शेल से निकालने के लिए:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
```

!!! note "नोट"

    यदि `unzip` इंस्टॉल नहीं है, तो इसे जोड़ें: `sudo apt install -y unzip` या `sudo dnf install -y unzip`।

#### executable को runnable बनाएं

यह निर्भर करता है कि आर्काइव कैसे ट्रांसफर किया गया था, executable बिट extraction के दौरान सुरक्षित नहीं रह सकता। इसे स्पष्ट रूप से सेट करें:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### सर्विस अकाउंट बनाएं

प्रोडक्शन डिप्लॉयमेंट के लिए बैकएंड को एक समर्पित अनप्रिविलेज्ड उपयोगकर्ता के रूप में चलाना अनुशंसित है:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "नोट"

    RHEL परिवार पर समकक्ष शेल पाथ `/sbin/nologin` है।

### चरण 3: लाइसेंस फ़ाइल इंस्टॉल करें

!!! warning "महत्वपूर्ण"

    लाइसेंस फ़ाइल इंस्टॉलेशन पैकेज में **शामिल नहीं** होती है और इसे digna द्वारा अलग से प्रदान किया जाएगा।

1. आपको दिया गया `license.toml` फ़ाइल ढूँढें
2. इसे root digna इंस्टॉलेशन डायरेक्टरी में कॉपी करें (जहाँ `config.toml` और `digna` executable स्थित हैं)

**क्यों यह महत्वपूर्ण है:**
लाइसेंस फ़ाइल में आपका ग्राहक जानकारी, लाइसेंस समाप्ति तिथि, और डिजिटल सिग्नेचर होता है। **इस फ़ाइल में कोई परिवर्तन न करें** — किसी भी परिवर्तन से यह अमान्य हो जाएगी।

**सेटअप के बाद निर्देशिका संरचना:**

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

### चरण 1: कॉन्फ़िगरेशन फ़ाइल बनाएं और संपादित करें

`config_template.toml` फ़ाइल आपके digna इंस्टॉलेशन डायरेक्टरी में प्रदान की गई है। आपको इसे केवल `config.toml` में नाम बदलना है।

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**स्थान:** `/opt/digna/config.toml`

`config.toml` को किसी टेक्स्ट एडिटर में खोलें और नीचे दिए प्रत्येक सेक्शन को कॉन्फ़िगर करें।

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

    यदि आप डैशबोर्ड को डिफ़ॉल्ट HTTP पोर्ट पर nginx या Apache से सर्व करते हैं, तो अनुमति देने वाला origin `http://localhost` है — या जब डैशबोर्ड अन्य मशीनों से पहुँचने योग्य हो तो सर्वर का सार्वजनिक URL।

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
| `DIGNA_REPO_HOST` | `localhost` या IP | PostgreSQL सर्वर का hostname/IP |
| `DIGNA_REPO_PORT` | `5432` (डिफ़ॉल्ट) | PostgreSQL पोर्ट |
| `DIGNA_REPO_DB` | `postgres` | डेटाबेस नाम |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | पहले बनाई गई स्कीमा |
| `DIGNA_REPO_USER` | `digna_user` | PostgreSQL सेटअप में बनाया गया उपयोगकर्ता |
| `DIGNA_REPO_PASSWORD` | आपका पासवर्ड | स्कीमा निर्माण के दौरान सेट किया गया पासवर्ड |
| `DIGNA_REPO_SSLMODE` | `prefer` (डिफ़ॉल्ट) | वैकल्पिक। PostgreSQL SSL मोड: `disable`, `allow`, `prefer`, `require`, `verify-ca` या `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (डिफ़ॉल्ट) | वैकल्पिक। रिपॉज़िटरी से digna द्वारा खुले रखे जाने वाले कनेक्शनों की संख्या |

!!! tip "सर्वोत्तम प्रथा"

    `config.toml` में डेटाबेस पासवर्ड प्लेन टेक्स्ट में होता है। इसकी अनुमतियाँ सीमित करें ताकि केवल सर्विस अकाउंट इसे पढ़ सके:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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

!!! tip "टिप"

    अपने सर्वर पर उपलब्ध CPU कोरों की संख्या जानने के लिए `nproc` चलाएँ।

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
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | डिफ़ॉल्ट: सिस्टम की अस्थायी डायरेक्टरी (`$TMPDIR`, या सेट न होने पर `/tmp`) | अस्थायी फ़ाइलों के लिए डायरेक्टरी, जब डेटा मेमोरी में नहीं समाता |

!!! tip "digna Engine का आकार निर्धारण"

    digna होस्ट पर, digna के अपने उपयोग के अतिरिक्त, अधिकतम `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB`
    मेमोरी की योजना बनाएँ, और अस्थायी डायरेक्टरी में इतने खाली डिस्क स्थान की, जिसमें digna Engine का
    उपयोग करने वाले डेटा स्रोतों की सबसे बड़ी निरीक्षित तिथि समा सके। `DIGNA_DUCKDB_TEMP_DIRECTORY` को ऐसी
    डिस्क पर इंगित करें जिसमें यह स्थान हो और जिस पर digna चलाने वाला खाता लिख सके:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
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

### चरण 3: रिपॉज़िटरी इनिशियलाइज़ करें

1. एक टर्मिनल खोलें
2. अपनी digna इंस्टॉलेशन डायरेक्टरी में नेविगेट करें (जहाँ `config.toml` और `digna` executable स्थित हैं)
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

    Linux पर वर्तमान डायरेक्टरी आपके PATH में नहीं होती, इसलिए executable को `./digna` के रूप में बुलाया जाता है न कि `digna` के रूप में। शॉर्ट फॉर्म हर जगह उपयोग करने के लिए, एक symbolic लिंक जोड़ें:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### चरण 4: रिपॉज़िटरी स्कीमा इंस्टॉल करें

एक ही डायरेक्टरी में चलाएँ:

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

### चरण 5: एक एडमिन उपयोगकर्ता बनाएं

1. एक **नई** टर्मिनल विंडो खोलें
2. अपनी digna इंस्टॉलेशन डायरेक्टरी में जाएँ
3. निम्न कमान्ड चलाकर एक एडमिन उपयोगकर्ता बनाएँ:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**उदाहरण:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

इससे `admin@example.com` ईमेल पते और पूर्ण प्रशासनिक अधिकारों वाला एक उपयोगकर्ता बनता है।

!!! tip "टिप"

    पासवर्ड को सिंगल कोट्स में रैप करें। `bash` और `zsh` विशिष्ट कैरेक्टर्स जैसे `!`, `$` और `*` का विशेष व्यवहार करते हैं, और बिना कोट किए गए पासवर्ड में ये सही तरीके से पास नहीं होंगे।

!!! tip "सर्वोत्तम प्रथा"

    ऊपरी, नीचले अक्षर, संख्याएँ और विशेष अंक मिलाकर मजबूत पासवर्ड का उपयोग करें।

---

### चरण 6: digna सर्वर शुरू करें

digna इंस्टॉलेशन डायरेक्टरी में, सर्वर शुरू करें:

```bash
./digna serve --address <host> --port <port>
```

**पैरामीटर्स:**
- `--address` — सर्वर होस्टनाम/IP (डिफ़ॉल्ट `127.0.0.1`)
- `--port` — सर्वर पोर्ट (डिफ़ॉल्ट `8000`)

सर्वर चालू होने पर, वह उस पते को प्रिंट करता है जिस पर वह सुनता है:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "टिप"

    यदि डैशबोर्ड बैकएंड से अलग मशीन पर सर्व किया जा रहा है, तो API पोर्ट को फ़ायरवॉल में भी खोलें:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "सर्वर टर्मिनल को व्यस्त रखता है"

    `serve` अग्रभूमि में चलता है और तब तक चलता रहता है जब तक आप इसे ++ctrl+c++ से रोक नहीं देते। सेटअप पूरा करते समय इसे चलता रहने दें; इसके बजाय बूट पर स्वतः प्रारंभ करने के लिए देखें [digna को systemd सेवा के रूप में चलाना](#running-digna-as-a-systemd-service).

## डैशबोर्ड कॉन्फ़िगरेशन {: #dashboard-configuration }

### चरण 1: डैशबोर्ड को वेब सर्वर पर डिप्लॉय करें

digna डैशबोर्ड अपनी कॉन्फ़िगरेशन `dashboard/dashboard_config.toml` से पढ़ता है। यह फ़ाइल इंस्टॉलेशन के साथ नहीं आती — आप इसे `dashboard/` डायरेक्टरी में डैशबोर्ड फ़ाइलों के साथ बनाते हैं।

इसकी सामग्री [सिंगल साइन-ऑन](../../../sso/overview.md) के अंतर्गत बताई गई है, और वहीं इस फ़ाइल की आवश्यकता भी होती है: इसमें वे लॉगिन विकल्प होते हैं जो डैशबोर्ड प्रदान करता है और, मल्टी-इंस्टेंस डिप्लॉयमेंट के लिए, बैकएंड कनेक्शन।

अपने वेब सर्वर का चयन करें और संबंधित डिप्लॉयमेंट स्टेप्स का पालन करें।

#### nginx पर डिप्लॉय करना

यदि आपने [nginx सेटअप](#nginx-setup) का पालन किया है, तो server block पहले से ही आपके `dashboard` फ़ोल्डर की ओर पॉइंट करता है और कॉपी करने की आवश्यकता नहीं है।

1. **पाथ की पुष्टि करें**
   - `/etc/nginx/conf.d/digna.conf` खोलें
   - पुष्टि करें कि `root` आपके निकाले गए `dashboard` फ़ोल्डर की ओर पॉइंट करता है

2. **यह सुनिश्चित करें कि फ़ोल्डर पढ़ने योग्य है**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **nginx रीलोड करें**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **इंस्टॉलेशन का परीक्षण करें**
   - अपना ब्राउज़र खोलें
   - `http://localhost` (या आपका कॉन्फ़िगर किया गया URL) पर नेविगेट करें
   - आपको digna डैशबोर्ड लॉगिन पेज दिखाई देना चाहिए

#### Apache httpd पर डिप्लॉय करना

1. **डैशबोर्ड को डॉक्यूमेंट रूट में कॉपी करें**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **रीराइट नियम जोड़ें**

   डैशबोर्ड रूट होने पर ब्राउज़र रिफ्रेश से बचने के लिए तैनात फ़ोल्डर के अंदर एक `.htaccess` फ़ाइल बनाएँ:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
   ```

   निम्न पेस्ट करें:

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

3. **Apache पुनरारंभ करें**
   ```bash
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **डैशबोर्ड तक पहुँचें**
   - अपना ब्राउज़र खोलें
   - `http://localhost/digna` पर नेविगेट करें
   - आपको digna डैशबोर्ड लॉगिन पेज दिखाई देना चाहिए

### चरण 2: SELinux (केवल RHEL परिवार)

RHEL, Rocky, AlmaLinux और Fedora पर SELinux डिफ़ॉल्ट रूप से enforcing होता है और यह वेब सर्वर को उसकी अपेक्षित लोकेशनों के बाहर फाइलें पढ़ने से ब्लॉक कर देगा। जाँचें कि यह सक्रिय है या नहीं:

```bash
getenforce
```

यदि परिणाम `Enforcing` है और आप `/opt/digna/dashboard` से डैशबोर्ड सर्व कर रहे हैं, तो डायरेक्टरी को लेबल करें ताकि वेब सर्वर इसे पढ़ सके:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "नोट"

    यदि `semanage` नहीं मिला, तो इसे इंस्टॉल करें: `sudo dnf install -y policycoreutils-python-utils`।

!!! warning "महत्वपूर्ण"

    एक ताजगी से कॉन्फ़िगर किए गए RHEL सर्वर पर यदि डैशबोर्ड **403 Forbidden** लौटाता है, तो यह लगभग हमेशा फाइल-परमिशन की बजाय SELinux लेबलिंग समस्या होती है। पुष्टि के लिए चलाएँ `sudo ausearch -m avc -ts recent`।

---

## digna को systemd सेवा के रूप में चलाना {: #running-digna-as-a-systemd-service }

### digna को सेवा के रूप में क्यों चलाएँ?

digna बैकएंड को systemd सेवा के रूप में चलाने से यह सुनिश्चित होता है कि यह:

- मशीन बूट होने पर स्वचालित रूप से शुरू हो जाए
- बैकग्राउंड में बिना खुले टर्मिनल विंडो के चले
- यदि क्रैश करे तो स्वतः पुनरारंभ हो
- `systemctl` के माध्यम से मैनेज किया जा सके — जो कि मानक Linux सेवा प्रबंधक है

### सेवा प्रबंधन फ़ाइलें

सभी आवश्यक फ़ाइलें digna इंस्टॉलेशन डायरेक्टरी के अंतर्गत: `bin/` में स्थित हैं

उपलब्ध shell स्क्रिप्ट्स:

- `install_service.sh` — digna को systemd के साथ रजिस्टर करता है
- `uninstall_service.sh` — सेवा का रजिस्ट्रेशन हटाता है
- `start_service.sh` — रजिस्टर की गई सेवा शुरू करता है
- `stop_service.sh` — चल रही सेवा को रोकता है

!!! warning "रूट अनुमतियाँ आवश्यक"

    सभी स्क्रिप्ट्स को `sudo` के साथ चलाया जाना चाहिए, क्योंकि बूट पर शुरू होने वाली सेवा रजिस्टर करने के लिए `/etc/systemd/system` में एक यूनिट फ़ाइल लिखी जाती है।

### स्क्रिप्ट्स को executable बनाना

Extraction executable बिट को संरक्षित नहीं कर सकता। पहली बार उपयोग से पहले:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### सेवा इंस्टॉल करना

1. **एक टर्मिनल खोलें**

2. **bin फ़ोल्डर में नेविगेट करें**
   ```bash
   cd /opt/digna/bin
   ```

3. **इंस्टॉलेशन स्क्रिप्ट चलाएँ**
   ```bash
   sudo ./install_service.sh
   ```

digna सर्वर अब systemd के साथ स्वचालित स्टार्टअप सक्षम करके रजिस्टर हो गया है। सेवा तुरंत शुरू नहीं होती — इसे शुरू करने के लिए अगले सेक्शन को देखें।

### सेवा शुरू और रोकना

#### सेवा शुरू करने के लिए

1. एक टर्मिनल खोलें
2. `/opt/digna/bin` में नेविगेट करें
3. चलाएँ:
   ```bash
   sudo ./start_service.sh
   ```

#### सेवा रोकने के लिए

1. एक टर्मिनल खोलें
2. `/opt/digna/bin` में नेविगेट करें
3. चलाएँ:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "टिप"

    एप्लिकेशन फ़ाइलें अपडेट करने से पहले हमेशा सेवा को रोकें।

### systemctl के साथ सेवा प्रबंधन

एक बार रजिस्टर हो जाने पर, सेवा को किसी भी डायरेक्टरी से मानक systemd कमांड्स से नियंत्रित किया जा सकता है:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### सेवा सत्यापित करना

सुनिश्चित करने के लिए कि सेवा रजिस्टर और चल रही है:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` का अर्थ है सेवा बूट पर शुरू होगी; `active` का अर्थ है यह अभी चल रही है।

### सेवा लॉग देखना

systemd कंसोल पर बैकएंड द्वारा लिखी गई सभी चीज़ें कैप्चर करता है। इसे पढ़ने के लिए:

```bash
sudo journalctl -u digna -n 100
```

समस्या उत्पन्न करते समय लाइव रूप में लॉग फॉलो करने के लिए:

```bash
sudo journalctl -u digna -f
```

!!! tip "टिप"

    यह उस समस्या का निदान करने का सबसे तेज़ तरीका है जिसमें सेवा शुरू होने के तुरंत बाद बंद हो जाती है। रिपॉज़िटरी कनेक्शन फेल्योर या गुम `license.toml` जैसी त्रुटियाँ यहाँ रिपोर्ट होती हैं।

### सेवा को नई डायरेक्टरी में स्थानांतरित करना

यूनिट फ़ाइल executable के absolute पाथ को स्टोर करती है, इसलिए इंस्टॉलेशन को स्थानांतरित करने पर सेवा को फिर से रजिस्टर करना आवश्यक है:

1. **वर्तमान सेवा अनइंस्टॉल करें**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **एप्लिकेशन फ़ाइलें स्थानांतरित करें**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **सेवा फिर से इंस्टॉल करें**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **सेवा शुरू करें**
   ```bash
   sudo ./start_service.sh
   ```

### सेवा अनइंस्टॉल करना

1. **चल रही सेवा को रोकें**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **सेवा अनइंस्टॉल करें**
   ```bash
   sudo ./uninstall_service.sh
   ```

अब digna सर्वर systemd से अनरजिस्टर कर दिया गया है।

---

## नए रिलीज़ में अपग्रेड करना {: #upgrading-to-a-new-release }

यह अनुभाग रिलीज़ 2026.06 के इंस्टॉलेशन को रिलीज़ 2026.11 में अपग्रेड करता है।

!!! warning "2026.06 से पुराने रिलीज़ से अपग्रेड"

    पहले रिलीज़ 2026.06 के अपग्रेड चरण पूरे करें: [नए रिलीज़ में अपग्रेड करना](../Release%202026.06/installation_guide_digna_linux_2026_06.md#upgrading-to-a-new-release)। इसके बाद नीचे दिए गए चरणों के साथ आगे बढ़ें।

### अपग्रेड करने से पहले

**digna रिपॉज़िटरी का बैकअप बनाना अनिवार्य है**

digna को अपग्रेड करने से पहले अपने रिपॉज़िटरी (PostgreSQL) का बैकअप लें ताकि डेटा लॉस से बचा जा सके।
बैकअप यह सुनिश्चित करता है कि यदि अपग्रेड के दौरान अनपेक्षित समस्याएँ आयीं तो आप रिकवर कर सकें।

शेल से बैकअप बनाने के लिए:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**रिलीज़ 2026.11 के लिए लाइसेंस फ़ाइल का अनुरोध करना**

रिलीज़ 2026.11 को एक नई `license.toml` की आवश्यकता है। शुरू करने से पहले digna टीम से इसका अनुरोध करें, और
इसे [चरण 7](#step-7-replace-the-license-file) के लिए तैयार रखें।

### अपग्रेड प्रक्रिया

#### चरण 1: digna सेवा बंद करें {: #step-1-stop-the-digna-service }

यदि digna systemd सेवा के रूप में चल रहा है, तो पहले उसे बंद करें:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

यदि digna फ़ोरग्राउंड में चल रहा है, तो उसकी टर्मिनल विंडो में ++ctrl+c++ दबाएँ।

#### चरण 2: वर्तमान इंस्टॉलेशन का बैकअप लें {: #step-2-backup-current-installation }

अपनी digna इंस्टॉलेशन डायरेक्टरी में वर्तमान इंस्टॉलेशन की executable और डैशबोर्ड फ़ोल्डर के नाम बदलें,
ताकि नई रिलीज़ उनके साथ डिप्लॉय की जा सके:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

`digna_old` को तब तक रखें जब तक आप अपग्रेड की पुष्टि न कर लें, और `dashboard_old` को तब तक जब तक आप उससे
अपनी कॉन्फ़िगरेशन फ़ाइलें पुनर्स्थापित न कर लें (चरण 4 देखें)। उसके बाद आप दोनों को हटा सकते हैं।

#### चरण 3: नया वर्शन निकालें और डिप्लॉय करें {: #step-3-extract-and-deploy-new-version }

1. नई digna इंस्टॉलेशन ZIP फ़ाइल निकालें
2. नई `digna` executable और `dashboard` फ़ोल्डर को अपनी इंस्टॉलेशन डायरेक्टरी में कॉपी करें
3. executable बिट और सर्विस अकाउंट के स्वामित्व को पुनर्स्थापित करें:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "महत्वपूर्ण"

    न तो `config.toml` और न ही `dashboard/dashboard_config.toml` कभी भी
    इंस्टॉलेशन ZIP में शामिल की जाती है — digna टीम इनमें से कोई भी फ़ाइल कभी नहीं भेजती। इसलिए अपग्रेड से
    आपकी मौजूदा कॉन्फ़िगरेशन अप्रभावित रहती है, और नाम बदले गए `*_old` फ़ोल्डरों में मौजूद प्रतियाँ ही
    आपके पास एकमात्र प्रतियाँ हैं।

#### चरण 4: अपनी कॉन्फ़िगरेशन फ़ाइलें पुनर्स्थापित करें {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
फिर हार्ड रिफ़्रेश (++ctrl+f5++) के साथ पेज रीलोड करें।

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
sudo cp /path/to/new/license.toml /opt/digna/license.toml
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

यदि systemd सेवा के रूप में चल रहा है:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

यदि मैन्युअल रूप से चला रहे हैं, तो सर्वर पुनरारंभ करें:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

यदि nginx या Apache का उपयोग कर रहे हैं, तो संबंधित वेब सर्वर रीलोड करें:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

RHEL परिवार पर, यदि `dashboard` डायरेक्टरी प्रतिस्थापित की गई थी तो SELinux लेबलिंग फिर से लागू करें:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### चरण 10: अपग्रेड सत्यापित करें {: #step-10-verify-the-upgrade }

1. नई executable की रिलीज़ की पुष्टि करें:

    ```bash
    ./digna version
    ```

    पहली पंक्ति में `Release: 2026.11` होना चाहिए।

2. digna डैशबोर्ड एक्सेस करें और सुनिश्चित करें कि इंटरफ़ेस सही ढंग से लोड हो रहा है।
3. त्रुटियों के लिए सर्वर लॉग्स जाँचें:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. अपने डेटाबेस कनेक्शनों का परीक्षण करें — देखें
   [कनेक्शन का परीक्षण](../../../databases/overview.md#testing-a-connection)। रिलीज़ 2026.06 से पहले की रिलीज़
   से अपग्रेड के बाद, पहले हर उस कनेक्शन को ODBC में बदलें जो अभी तक ODBC का उपयोग नहीं करता था।

नए मॉड्यूल के साथ शुरुआत करने के लिए देखें [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
digna MCP Server के लिए [AI एजेंट कनेक्ट करना](../../../platform/agentic/connect_ai_agent.md), और
digna Engine के लिए [प्रोफाइलिंग लोकेशन](../../../platform/profiling/profiling_location.md)।
