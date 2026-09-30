---
title: PostgreSQL कनेक्टर – डेटाबेस इंटीग्रेशन | digna दस्तावेज़
description: digna को DSN-less कनेक्शन स्ट्रिंग के साथ ODBC के माध्यम से PostgreSQL से कनेक्ट करने के लिए कॉन्फ़िगर करें। इसमें psqlODBC ड्राइवर, आवश्यक ODBC प्रॉपर्टीज़, SSL मोड और digna-पक्ष की कनेक्शन सेटिंग्स शामिल हैं।
image: /assets/logo_square.png
---


# PostgreSQL के लिए सोर्स कनेक्टर

यह गाइड बताता है कि *digna* को **DSN-less** कनेक्शन स्ट्रिंग का उपयोग करके **ODBC** के माध्यम से
PostgreSQL से कनेक्ट करने के लिए कैसे कॉन्फ़िगर करें।

सेटअप का *digna* पक्ष हर तकनीक के लिए समान है — कनेक्शन कहाँ बनाए जाते हैं, प्रॉपर्टी मान कैसे
एन्क्रिप्ट होते हैं, कनेक्शन का परीक्षण कैसे होता है और प्रोफ़ाइलिंग मोड का क्या अर्थ है। इसका वर्णन
[डेटाबेस कनेक्शन अवलोकन](overview.md) में किया गया है। यह पृष्ठ केवल वही कवर करता है जो
PostgreSQL के लिए विशिष्ट है।

---

## 1. ODBC ड्राइवर इंस्टॉल करें {: #1-install-the-odbc-driver }

विक्रेता की आधिकारिक इंस्टॉलेशन गाइड का पालन करते हुए, PostgreSQL ODBC ड्राइवर (**psqlODBC**) को उस
मशीन पर इंस्टॉल करें जिस पर *digna* बैकएंड चलता है।

ड्राइवर एक ऐसे नाम से रजिस्टर होता है जो प्लेटफ़ॉर्म और पैकेज के अनुसार अलग होता है — आमतौर पर
Windows पर **PostgreSQL Unicode(x64)** और Linux पर **PostgreSQL ODBC Driver(UNICODE)**। सटीक
नाम अपने होस्ट से पढ़ें, जैसा कि
[digna होस्ट पर ODBC ड्राइवर इंस्टॉल करें](overview.md#install-the-driver) में बताया गया है, और
नीचे `DRIVER` प्रॉपर्टी के लिए उसी नाम का उपयोग करें।

---

## 2. ODBC प्रॉपर्टीज़ {: #2-odbc-properties }

!!! important "एक उदाहरण, कोई विनिर्देश नहीं"

    नीचे दिया गया सेट एक ऐसा संयोजन है जो काम करने के लिए जाना जाता है। प्रॉपर्टीज़ psqlODBC
    ड्राइवर की हैं, इसलिए उनके नाम, डिफ़ॉल्ट और स्वीकृत मान ड्राइवर संस्करणों और प्लेटफ़ॉर्म के
    बीच अलग होते हैं, और आपका सर्वर क्या माँगता है — विशेषकर SSL — वह भी अलग हो सकता है। इसे
    शुरुआती बिंदु के रूप में उपयोग करें और आपके द्वारा इंस्टॉल किए गए ड्राइवर संस्करण का
    दस्तावेज़ देखें।

**Add DB Connection** स्क्रीन में निम्नलिखित प्रॉपर्टीज़ जोड़ें:

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | *digna* होस्ट पर रजिस्टर ड्राइवर नाम से मेल खाना चाहिए |
| `SERVER` | `db.example.com` | सर्वर नाम या IP पता |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | वह डेटाबेस जिसमें सोर्स स्कीमा हैं। यही एकमात्र डेटाबेस है जिसे यह कनेक्शन प्रोफ़ाइल कर सकता है |
| `UID` | `digna_source_user` | डेटाबेस उपयोगकर्ता |
| `PWD` | `<password>` | **Encrypted** पर टिक करें |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` या `verify-full` — सर्वर द्वारा स्वीकार्य होना चाहिए |

परिणामी कनेक्शन स्ट्रिंग इस प्रकार दिखती है:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

कोई भी अन्य psqlODBC विकल्प अतिरिक्त प्रॉपर्टी के रूप में जोड़ा जा सकता है — उदाहरण के लिए
रीड-ओनली सेशन के लिए `ReadOnly=1`, या कनेक्ट करते समय `SET` स्टेटमेंट चलाने के लिए
`ConnSettings`।

---

## 3. *digna* कॉन्फ़िगरेशन {: #3-digna-configuration }

**Add DB Connection** स्क्रीन में निम्नलिखित जानकारी दें:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. PostgreSQL पर टिप्पणियाँ {: #4-notes-on-postgresql }

- **`SSLMode` सर्वर से मेल खाना चाहिए।** `hostssl` के साथ कॉन्फ़िगर किया गया सर्वर
  `SSLMode=disable` को अस्वीकार कर देता है, और `verify-ca` या `verify-full` के लिए अतिरिक्त रूप से
  *digna* होस्ट पर ड्राइवर को रूट सर्टिफ़िकेट उपलब्ध होना चाहिए। यदि ड्राइवर का परीक्षण करते समय
  आपको कोई विशिष्ट मोड चुनना पड़ा था, तो यहाँ भी वही उपयोग करें।
- **एक कनेक्शन एक डेटाबेस देखता है।** *digna* `DATABASE` में नामित डेटाबेस के स्कीमा प्रस्तुत करता
  है, क्योंकि PostgreSQL केवल वर्तमान डेटाबेस को catalog के रूप में रिपोर्ट करता है। किसी अन्य
  डेटाबेस की सोर्स टेबल्स के लिए अलग कनेक्शन चाहिए।
- **प्रोफ़ाइलिंग मोड।** *Permanent* वर्क टेबल्स को **Work Schema** में बनाता है, इसलिए उपयोगकर्ता को
  उस स्कीमा पर `CREATE` अधिकार चाहिए। *Session* `CREATE TEMPORARY TABLE` का उपयोग करता है और
  **Work Schema** को नहीं छूता। *Standard* को केवल रीड एक्सेस चाहिए।

---

## 5. ड्राइवर का सत्यापन (वैकल्पिक) {: #5-verifying-the-driver-optional }

DSN-less कनेक्शन के लिए ODBC डेटा सोर्स कॉन्फ़िगर करना आवश्यक नहीं है, लेकिन ड्राइवर का अपना डायलॉग
यह पुष्टि करने का सुविधाजनक तरीका है कि ड्राइवर काम करता है और सर्वर आपके क्रेडेंशियल्स और SSL मोड
को स्वीकार करता है, इससे पहले कि आप उन्हें *digna* में दर्ज करें।

#### चरण 1
![चरण 1](images/postgres/create_odbc_data_source_step1.png)

#### चरण 2 – कनेक्शन का परीक्षण करें

**Test Connection** बटन पर क्लिक करें।

![चरण 2](images/postgres/create_odbc_data_source_step2.png)

यहाँ दर्ज किए गए मान ठीक वही मान हैं जो [अनुभाग 2](#2-odbc-properties) की प्रॉपर्टीज़
लेती हैं।
