---
title: Linux स्थापना मार्गदर्शिका – digna रिलीज 2026.06 | digna प्रलेखन
description: Linux पर digna रिलीज 2026.06 स्थापित करने के लिए चरण-दर-चरण मार्गदर्शिका — सिस्टम आवश्यकताएँ, PostgreSQL सेटअप, nginx या Apache विन्यास, backend और dashboard कॉन्फ़िगरेशन, digna को systemd सेवा के रूप में चलाना, और नए रिलीज में अपग्रेड करना।
keywords: digna लिनक्स स्थापना, digna डिप्लॉयमेंट गाइड, digna backend सेटअप, digna डैशबोर्ड स्थापना, postgresql linux, nginx linux, digna systemd सेवा, digna अपग्रेड गाइड
image: /assets/logo_square.png
---

# digna रिलीज 2026.06 के लिए Linux स्थापना मार्गदर्शिका

**रिलीज़:** 2026.06

**अंतिम अपडेट:** 5 सितंबर, 2026


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

- **dignabackend**: एप्लिकेशन का मुख्य इंजन, जो डेटा संसाधित करने और गुणवत्ता जांच करने के लिए जिम्मेदार है।
- **dignadashboard**: एक वेब-आधारित इंटरफ़ेस जो वेब सर्वर पर होस्ट किया जाता है और digna प्लेटफ़ॉर्म के साथ इंटरैक्ट करने व डेटा गुणवत्ता मेट्रिक्स को विज़ुअलाइज़ करने का यूजर-फ्रेंडली तरीका प्रदान करता है।

### रिलीज 2026.06 में क्या नया है

यह रिलीज़ डेटा ऑब्ज़र्वेबिलिटी क्षमताओं को सीधे आपके कोड में लाती है, जिससे डेवलपर्स स्रोत पर ही डेटा गुणवत्ता की निगरानी कर सकते हैं। पूर्ण विवरण के लिए देखें [release notes](http://docs.digna.ai/changelog/Release_202606/)।

### Windows या macOS के लिए मार्गदर्शिका चाहिए?

यह गाइड Linux को कवर करता है। अन्य प्लेटफार्मों के लिए देखें [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) या [macOS Installation Guide](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md)।

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
   - `config.toml` — कॉन्फ़िगरेशन फ़ाइल
   - `license.toml` — लाइसेंस फ़ाइल (अपनी फ़ाइल यहाँ कॉपी करें)

शेल से निकालने के लिए:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
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
| `digna_APP_PORT` | `8082` (डिफ़ॉल्ट) | REST API एंडपॉइंट्स के लिए पोर्ट |
| `digna_APP_CORS_ALLOW_ORIGINS` | फ्रंटएंड URL | यदि डैशबोर्ड अलग सर्वर पर है तो उसका URL शामिल करें |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | क्रेडेंशियल्स के साथ CORS के लिए आवश्यक |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | सभी HTTP मेथड्स की अनुमति दें |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | सभी हेडर्स की अनुमति दें |

!!! note "नोट"

    यदि आप डैशबोर्ड को डिफ़ॉल्ट HTTP पोर्ट पर nginx या Apache से सर्व करते हैं, तो अनुमति देने वाला origin `http://localhost` है — या जब डैशबोर्ड अन्य मशीनों से पहुँचने योग्य हो तो सर्वर का सार्वजनिक URL।

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
| `digna_REPO_HOST` | `localhost` या IP | PostgreSQL सर्वर का hostname/IP |
| `digna_REPO_PORT` | `5432` (डिफ़ॉल्ट) | PostgreSQL पोर्ट |
| `digna_REPO_DB` | `postgres` | डेटाबेस नाम |
| `digna_REPO_SCHEMA` | `dignarepo` | पहले बनाई गई स्कीमा |
| `digna_REPO_USER` | `digna_user` | PostgreSQL सेटअप में बनाया गया उपयोगकर्ता |
| `digna_REPO_PASSWORD` | आपका पासवर्ड | स्कीमा निर्माण के दौरान सेट किया गया पासवर्ड |

!!! tip "सर्वोत्तम प्रथा"

    `config.toml` में डेटाबेस पासवर्ड प्लेन टेक्स्ट में होता है। इसकी अनुमतियाँ सीमित करें ताकि केवल सर्विस अकाउंट इसे पढ़ सके:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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
| `digna_FERNET_KEY` | एन्क्रिप्शन कुंजी | टोकन और कुकीज़ एन्क्रिप्ट करने के लिए उपयोग होती है (डिफ़ॉल्ट प्रदान किया जाता है) |
| `digna_COOKIE_DOMAIN` | `localhost` | अपने फ्रंटएंड डोमेन से मिलाएँ |
| `digna_COOKIE_SECURE` | `false` (लोकल) / `true` (प्रोडक्शन) | HTTPS कनेक्शन्स के लिए `true` का उपयोग करें |
| `digna_COOKIE_HTTPONLY` | `true` | सुरक्षा के लिए हमेशा सक्षम रखें |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF हमलों से बचाने में मदद करता है |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 घंटे) | सेकंड में सत्र का टाइमआउट |
| `digna_MAX_WORKERS` | CPU कोर की संख्या - 1 | समानांतर निरीक्षण कार्यों की संख्या |

!!! tip "टिप"

    अपने सर्वर पर उपलब्ध CPU कोरों की संख्या जानने के लिए `nproc` चलाएँ।

#### [logging] सेक्शन

यह सेक्शन लॉगिंग व्यवहार को कॉन्फ़िगर करता है:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| पैरामीटर | मान | नोट्स |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` या `DEBUG` | प्रोडक्शन के लिए `INFO`, ट्रबलशूटिंग के लिए `DEBUG` |
| `digna_LOGGING_BACKUP_COUNT` | `10` | रोज़ाना लॉग बैकअप रखने की संख्या |

---

### चरण 2: रिपॉज़िटरी इनिशियलाइज़ करें

1. एक टर्मिनल खोलें
2. अपनी digna इंस्टॉलेशन डायरेक्टरी में नेविगेट करें (जहाँ `config.toml` और `digna` executable स्थित हैं)
3. कनेक्शन टेस्ट चलाएँ:

```bash
cd /opt/digna
./digna repo check
```

आपको पुष्टि दिखाई देनी चाहिए कि कनेक्शन स्थापित है (रिपॉज़िटरी अभी इनिशियलाइज़ नहीं हुई है)।

!!! note "नोट"

    Linux पर वर्तमान डायरेक्टरी आपके PATH में नहीं होती, इसलिए executable को `./digna` के रूप में बुलाया जाता है न कि `digna` के रूप में। शॉर्ट फॉर्म हर जगह उपयोग करने के लिए, एक symbolic लिंक जोड़ें:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### चरण 3: रिपॉज़िटरी स्कीमा इंस्टॉल करें

एक ही डायरेक्टरी में चलाएँ:

```bash
./digna repo install
```

यह कमान्ड आपके PostgreSQL डेटाबेस में आवश्यक टेबल और स्कीमा इंस्टॉल करती है।

### चरण 4: digna सर्वर शुरू करें

digna इंस्टॉलेशन डायरेक्टरी में, सर्वर शुरू करें:

```bash
./digna serve --address <host> --port <port>
```

**पैरामीटर्स:**
- `--address` — सर्वर होस्टनाम/IP
- `--port` — सर्वर पोर्ट

आपको स्टार्टअप मैसेज दिखाई देने चाहिए जो पुष्टि करते हैं कि सर्वर चल रहा है:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "टिप"

    यदि डैशबोर्ड बैकएंड से अलग मशीन पर सर्व किया जा रहा है, तो API पोर्ट को फ़ायरवॉल में भी खोलें:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

### चरण 5: एक एडमिन उपयोगकर्ता बनाएं

1. एक **नई** टर्मिनल विंडो खोलें
2. अपनी digna इंस्टॉलेशन डायरेक्टरी में जाएँ
3. निम्न कमान्ड चलाकर एक एडमिन उपयोगकर्ता बनाएँ:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**उदाहरण:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

यह `admin` उपयोगकर्ता नाम और पूर्ण प्रशासनिक अधिकारों के साथ एक उपयोगकर्ता बनाता है।

!!! tip "टिप"

    पासवर्ड को सिंगल कोट्स में रैप करें। `bash` और `zsh` विशिष्ट कैरेक्टर्स जैसे `!`, `$` और `*` का विशेष व्यवहार करते हैं, और बिना कोट किए गए पासवर्ड में ये सही तरीके से पास नहीं होंगे।

!!! tip "सर्वोत्तम प्रथा"

    ऊपरी, नीचले अक्षर, संख्याएँ और विशेष अंक मिलाकर मजबूत पासवर्ड का उपयोग करें।

---

## डैशबोर्ड कॉन्फ़िगरेशन {: #dashboard-configuration }

### चरण 1: डैशबोर्ड को वेब सर्वर पर डिप्लॉय करें

digna डैशबोर्ड की अपनी अलग `config.toml` फ़ाइल `dashboard/` डायरेक्टरी में स्थित है। यह कॉन्फ़िगरेशन पहले से प्रदान की गई है और प्रारम्भिक सेटअप के दौरान बदलने की आवश्यकता नहीं है। केवल तब कॉन्फ़िगर करें जब आपको बैकएंड कनेक्शन कस्टमाइज़ करना हो।

यदि आपको डैशबोर्ड कॉन्फ़िगरेशन बदलने की ज़रूरत हो (उदा., मल्टी-इंस्टेंस डिप्लॉयमेंट के लिए), तो डैशबोर्ड के दस्तावेज़ देखें।

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

### अपग्रेड करने से पहले

**digna रिपॉज़िटरी का बैकअप बनाना अनिवार्य है**

digna को अपग्रेड करने से पहले अपने रिपॉज़िटरी (PostgreSQL) का बैकअप लें ताकि डेटा लॉस से बचा जा सके।
बैकअप यह सुनिश्चित करता है कि यदि अपग्रेड के दौरान अनपेक्षित समस्याएँ आयीं तो आप रिकवर कर सकें।

शेल से बैकअप बनाने के लिए:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### अपग्रेड प्रक्रिया

#### चरण 1: digna सेवा बंद करें

यदि digna systemd सेवा के रूप में चल रही है, तो पहले उसे बंद करें:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

यदि digna foreground में चल रहा है, तो उसके टर्मिनल विंडो में `Ctrl + C` दबाएँ।

#### चरण 2: वर्तमान बैकएंड इंस्टॉलेशन का बैकअप लें

अपनी digna इंस्टॉलेशन डायरेक्टरी में:

```bash
cd /opt/digna
sudo mv digna digna_old
```
```bash
sudo mv dashboard dashboard_old
```

#### चरण 3: नया वर्शन निकालें और डिप्लॉय करें

1. नया digna इंस्टॉलेशन ZIP फाइल निकालें
2. नई `digna` executable और `dashboard` फ़ोल्डर को अपने इंस्टॉलेशन डायरेक्टरी में कॉपी करें
3. executable बिट और सर्विस अकाउंट के स्वामित्व को पुनर्स्थापित करें:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "महत्वपूर्ण"

    `config.toml` फ़ाइल इंस्टॉलेशन ZIP में **कभी नहीं** शामिल की जाती। आपकी मौजूदा कॉन्फ़िगरेशन सुरक्षित रहती है।

### चरण 4: अपनी कॉन्फ़िगरेशन फ़ाइलें पुनर्स्थापित करें

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### चरण 5: रिपॉज़िटरी स्कीमा अपग्रेड करें

अपनी digna इंस्टॉलेशन डायरेक्टरी में नेविगेट करें और चलाएँ:

```bash
cd /opt/digna
./digna repo upgrade
```

यह मौजूद सभी डेटा को संरक्षित रखते हुए PostgreSQL स्कीमा को नवीनतम वर्शन में अपडेट कर देता है।

### चरण 6: सेवाएँ पुनः प्रारंभ करें

यदि systemd सेवा के रूप में चल रही है:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

यदि मैन्युअल रूप से चलाती हैं, तो सर्वर पुनरारंभ करें:

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

#### चरण 7: अपग्रेड सत्यापित करें

1. digna डैशबोर्ड एक्सेस करें
2. सुनिश्चित करें कि इंटरफ़ेस सही ढंग से लोड हो रहा है
3. किसी भी त्रुटि के लिए सर्वर लॉग्स जाँचें:

```bash
sudo journalctl -u digna -n 100
```