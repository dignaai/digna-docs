---
title: Databricks कनेक्टर – डेटाबेस इंटीग्रेशन | digna दस्तावेज़
description: digna को DSN-less कनेक्शन स्ट्रिंग के साथ ODBC के माध्यम से Unity Catalog वाले Databricks से कनेक्ट करने के लिए कॉन्फ़िगर करें। इसमें Databricks ODBC ड्राइवर, personal access tokens, HTTP path और digna-पक्ष की कनेक्शन सेटिंग्स शामिल हैं।
image: /assets/logo_square.png
---

# Databricks के लिए सोर्स कनेक्टर

यह गाइड बताता है कि *digna* को **DSN-less** कनेक्शन स्ट्रिंग का उपयोग करके **ODBC** के माध्यम से
Databricks से कनेक्ट करने के लिए कैसे कॉन्फ़िगर करें।

सेटअप का *digna* पक्ष हर तकनीक के लिए समान है — कनेक्शन कहाँ बनाए जाते हैं, प्रॉपर्टी मान कैसे
एन्क्रिप्ट होते हैं, कनेक्शन का परीक्षण कैसे होता है और प्रोफ़ाइलिंग मोड का क्या अर्थ है। इसका वर्णन
[डेटाबेस कनेक्शन अवलोकन](overview.md) में किया गया है। यह पृष्ठ केवल वही कवर करता है जो
Databricks के लिए विशिष्ट है।

!!! note "Unity Catalog आवश्यक है"

    *digna* उपलब्ध catalogs को `system.information_schema.catalogs` से पढ़ता है, इसलिए workspace में
    Unity Catalog सक्षम होना चाहिए। पिछली *digna* रिलीज़ में Unity Catalog के बिना workspaces के लिए
    एक अलग "Databricks Legacy" तकनीक उपलब्ध थी; वह अब उपलब्ध नहीं है।

---

## 1. ODBC ड्राइवर इंस्टॉल करें {: #1-install-the-odbc-driver }

[Databricks की इंस्टॉलेशन गाइड](https://docs.databricks.com/aws/en/integrations/odbc/) का पालन करते
हुए, **Databricks ODBC Driver** को उस मशीन पर इंस्टॉल करें जिस पर *digna* बैकएंड चलता है।

संस्करण के अनुसार, ड्राइवर **Simba Spark ODBC Driver** या **Databricks ODBC Driver** के रूप में
रजिस्टर होता है। रजिस्टर नाम का सटीक रूप अपने होस्ट से पढ़ें, जैसा कि
[digna होस्ट पर ODBC ड्राइवर इंस्टॉल करें](overview.md#install-the-driver) में बताया गया है।

---

## 2. कनेक्शन विवरण एकत्र करें {: #2-gather-the-connection-details }

सभी मान उस SQL warehouse (या cluster) से आते हैं जिसका उपयोग आप *digna* से करवाना चाहते हैं। उसे
Databricks workspace में खोलें और **Connection details** पर जाएँ:

| Databricks फ़ील्ड | किस रूप में उपयोग होता है |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, सामान्यतः `443` |
| **HTTP path** | `HTTPPath` |

प्रमाणीकरण के लिए, एक **personal access token** बनाएँ — देखें
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat)।
टोकन किसी उपयोगकर्ता या service principal के होते हैं, और उस principal को सोर्स डेटा पर `USE CATALOG`,
`USE SCHEMA` और `SELECT` अधिकार चाहिए।

---

## 3. ODBC प्रॉपर्टीज़ {: #3-odbc-properties }

!!! important "एक उदाहरण, कोई विनिर्देश नहीं"

    नीचे दिया गया सेट एक ऐसा संयोजन है जो काम करने के लिए जाना जाता है। प्रॉपर्टीज़ Databricks/Simba
    ड्राइवर की हैं, इसलिए उनके नाम, डिफ़ॉल्ट और स्वीकृत मान ड्राइवर संस्करणों के बीच — ड्राइवर का नाम
    एक से अधिक बार बदला गया है और उसके प्रमाणीकरण विकल्प बढ़ाए गए हैं — और प्लेटफ़ॉर्म के बीच अलग होते
    हैं। इसे शुरुआती बिंदु के रूप में उपयोग करें और आपके द्वारा इंस्टॉल किए गए ड्राइवर संस्करण का
    दस्तावेज़ देखें।

**Add DB Connection** स्क्रीन में निम्नलिखित प्रॉपर्टीज़ जोड़ें:

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | *digna* होस्ट पर रजिस्टर ड्राइवर नाम से मेल खाना चाहिए |
| `Host` | `<workspace>.cloud.databricks.com` | warehouse का server hostname, उदा. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | warehouse या cluster का HTTP path |
| `SSL` | `1` | Databricks endpoints केवल TLS पर चलते हैं |
| `ThriftTransport` | `2` | HTTP transport, जिसका उपयोग SQL endpoints करते हैं |
| `AuthMech` | `3` | टोकन प्रमाणीकरण |
| `UID` | `token` | शाब्दिक शब्द `token`, कोई उपयोगकर्ता नाम नहीं |
| `PWD` | `dapi…` | personal access token। **Encrypted** पर टिक करें |
| `UseNativeQuery` | `1` | *digna* के SQL को बिना बदलाव के आगे भेजता है — नीचे देखें |

परिणामी कनेक्शन स्ट्रिंग इस प्रकार दिखती है:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "`UseNativeQuery=1` बनाए रखें"

    `UseNativeQuery=0` — ड्राइवर का डिफ़ॉल्ट — के साथ ड्राइवर आने वाले SQL को उस रूप में फिर से लिखता है
    जिसे वह पोर्टेबल ODBC सिंटैक्स मानता है। *digna* पहले से ही Databricks SQL उत्पन्न करता है, इसलिए
    यह पुनर्लेखन backtick quoting और date literals को बदल सकता है, और तब प्रोफ़ाइलिंग उन स्टेटमेंट्स पर
    विफल हो जाती है जो लिखे गए रूप में मान्य हैं।

### टोकन के बजाय OAuth

OAuth machine-to-machine प्रमाणीकरण वाले service principal के लिए, `AuthMech`, `UID` और `PWD` को
इनसे बदलें:

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Client credentials |
| `Auth_Client_ID` | `<application id>` | Service principal |
| `Auth_Client_Secret` | `<client secret>` | **Encrypted** पर टिक करें |

---

## 4. *digna* कॉन्फ़िगरेशन {: #4-digna-configuration }

**Add DB Connection** स्क्रीन में निम्नलिखित जानकारी दें:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Databricks पर टिप्पणियाँ {: #5-notes-on-databricks }

- **Warehouse चल रहा होना चाहिए**, या शुरू हो सकने योग्य होना चाहिए, जब *digna* कनेक्ट करता है। रुकी
  हुई अवस्था से फिर शुरू होने वाले warehouse को कनेक्शन टाइमआउट से अधिक समय लग सकता है — यदि निष्क्रिय
  अवधि के बाद पहले प्रयास में परीक्षण विफल हो, तो पुनः प्रयास करें।
- **Catalogs workspace से आते हैं।** अधिकांश तकनीकों के विपरीत, एक Databricks कनेक्शन हर उस catalog
  तक पहुँचता है जिसे principal देख सकता है, इसलिए एक ही कनेक्शन कई catalogs के सोर्सेज़ की सेवा कर
  सकता है।
- **प्रोफ़ाइलिंग मोड।** *Permanent* वर्क टेबल्स को सोर्स के catalog के अंदर **Work Schema** में
  बनाता है, इसलिए principal को वहाँ `CREATE TABLE` अधिकार चाहिए। *Session*
  `CREATE TEMPORARY TABLE` का उपयोग करता है और **Work Schema** को नहीं छूता। *Standard* को केवल रीड
  एक्सेस चाहिए।
- **Serverless warehouses भी इसी तरह काम करते हैं**; केवल `HTTPPath` अलग होता है।

---

## 6. ड्राइवर का सत्यापन (वैकल्पिक) {: #6-verifying-the-driver-optional }

DSN-less कनेक्शन के लिए ODBC डेटा सोर्स कॉन्फ़िगर करना आवश्यक नहीं है, लेकिन ड्राइवर का अपना डायलॉग
यह पुष्टि करने का सुविधाजनक तरीका है कि ड्राइवर, warehouse और टोकन काम करते हैं, इससे पहले कि आप
उन्हें *digna* में दर्ज करें।

#### चरण 1
![चरण 1](images/databricks/create_odbc_data_source_step1.png)

#### चरण 2
![चरण 2](images/databricks/create_odbc_data_source_step2.png)

#### चरण 3
![चरण 3](images/databricks/create_odbc_data_source_step3.png)

#### चरण 4
![चरण 4](images/databricks/create_odbc_data_source_step4.png)

#### चरण 5 – कनेक्शन का परीक्षण करें

**TEST** बटन पर क्लिक करें। सफल कनेक्शन इस प्रकार दिखना चाहिए:

![चरण 5](images/databricks/create_odbc_data_source_step5.png)

यहाँ दर्ज किए गए होस्ट, HTTP path और टोकन ठीक वही मान हैं जो [अनुभाग 3](#3-odbc-properties) की
प्रॉपर्टीज़ लेती हैं।
