# Snowflake के लिए सोर्स कनेक्टर

यह गाइड बताता है कि *digna* को **DSN-less** कनेक्शन स्ट्रिंग का उपयोग करके **ODBC** के माध्यम से
Snowflake से कनेक्ट करने के लिए कैसे कॉन्फ़िगर करें।

सेटअप का *digna* पक्ष हर तकनीक के लिए समान है — कनेक्शन कहाँ बनाए जाते हैं, प्रॉपर्टी मान कैसे
एन्क्रिप्ट होते हैं, कनेक्शन का परीक्षण कैसे होता है और प्रोफ़ाइलिंग मोड का क्या अर्थ है। इसका वर्णन
[डेटाबेस कनेक्शन अवलोकन](overview.md) में किया गया है। यह पृष्ठ केवल वही कवर करता है जो
Snowflake के लिए विशिष्ट है।

---

## 1. ODBC ड्राइवर इंस्टॉल करें {: #1-install-the-odbc-driver }

[Snowflake की इंस्टॉलेशन गाइड](https://docs.snowflake.com/en/developer-guide/odbc/odbc) का पालन करते
हुए, **Snowflake ODBC Driver** को उस मशीन पर इंस्टॉल करें जिस पर *digna* बैकएंड चलता है।

ड्राइवर **SnowflakeDSIIDriver** के रूप में रजिस्टर होता है। रजिस्टर नाम का सटीक रूप अपने होस्ट से
पढ़ें, जैसा कि [digna होस्ट पर ODBC ड्राइवर इंस्टॉल करें](overview.md#install-the-driver) में बताया
गया है।

---

## 2. ODBC प्रॉपर्टीज़ {: #2-odbc-properties }

Snowflake तक **programmatic access token (PAT)** के साथ पहुँचा जाता है — यही वह प्रमाणीकरण मार्ग है
जिसके विरुद्ध *digna* सत्यापित है, और जिसे Snowflake उन खातों के लिए अनिवार्य करता है जिन पर केवल
पासवर्ड से साइन-इन अवरुद्ध है।

!!! important "एक उदाहरण, कोई विनिर्देश नहीं"

    नीचे दिया गया सेट एक ऐसा संयोजन है जो काम करने के लिए जाना जाता है। प्रॉपर्टीज़ Snowflake ODBC
    ड्राइवर की हैं, इसलिए उनके नाम, डिफ़ॉल्ट और स्वीकृत मान ड्राइवर संस्करणों और प्लेटफ़ॉर्म के बीच
    अलग होते हैं, और आपका खाता कौन-से प्रमाणीकरण विकल्पों की अनुमति देता है, यह खाते की सुरक्षा नीति
    तय करती है। इसे शुरुआती बिंदु के रूप में उपयोग करें और आपके द्वारा इंस्टॉल किए गए ड्राइवर संस्करण
    का दस्तावेज़ देखें।

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | *digna* होस्ट पर रजिस्टर ड्राइवर नाम से मेल खाना चाहिए |
| `Server` | `<account>.snowflakecomputing.com` | Account identifier और प्रत्यय, उदा. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Snowflake उपयोगकर्ता जिसका टोकन है |
| `Database` | `TEST` | वह डेटाबेस जिसमें सोर्स स्कीमा हैं। यही एकमात्र डेटाबेस है जिसे यह कनेक्शन प्रोफ़ाइल कर सकता है |
| `Schema` | `PUBLIC` | session का डिफ़ॉल्ट स्कीमा |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | टोकन प्रमाणीकरण चुनता है |
| `token` | `<programmatic access token>` | **Encrypted** पर टिक करें |

परिणामी कनेक्शन स्ट्रिंग इस प्रकार दिखती है:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Warehouse और role

क्वेरीज़ को एक warehouse चाहिए। यदि *digna* उपयोगकर्ता का एक डिफ़ॉल्ट warehouse और एक डिफ़ॉल्ट role
है, तो session उन्हें अपने आप ले लेता है और कुछ भी कॉन्फ़िगर नहीं करना पड़ता। अन्यथा जोड़ें:

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Warehouse जो प्रोफ़ाइलिंग क्वेरीज़ चलाता है |
| `Role` | `DIGNA_READER` | Role जिसके grants का session उपयोग करता है |

!!! tip "digna को उसका अपना warehouse दें"

    एक अलग, छोटा, auto-suspend होने वाला warehouse प्रोफ़ाइलिंग की लागत को दृश्यमान रखता है और
    *digna* को compute के लिए इंटरैक्टिव उपयोगकर्ताओं से प्रतिस्पर्धा करने से रोकता है।

### पासवर्ड प्रमाणीकरण

जहाँ खाता अब भी इसकी अनुमति देता है, वहाँ टोकन के स्थान पर पासवर्ड काम करता है — `authenticator` और
`token` हटाएँ और जोड़ें:

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `PWD` | `<password>` | **Encrypted** पर टिक करें |

---

## 3. *digna* कॉन्फ़िगरेशन {: #3-digna-configuration }

**Add DB Connection** स्क्रीन में निम्नलिखित जानकारी दें:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Snowflake पर टिप्पणियाँ {: #4-notes-on-snowflake }

- **टोकन समाप्त होते हैं।** Programmatic access token एक जीवनकाल के साथ जारी किया जाता है, और जिस दिन
  वह समाप्त होता है उसी दिन प्रोफ़ाइलिंग रुक जाती है। बनाते समय समाप्ति तिथि नोट करें, और नया टोकन
  `token` प्रॉपर्टी में फिर से दर्ज करें — एन्क्रिप्टेड मान बदले जा सकते हैं लेकिन वापस पढ़े नहीं जा
  सकते।
- **एक कनेक्शन एक डेटाबेस देखता है।** *digna* `Database` में नामित डेटाबेस के स्कीमा प्रस्तुत करता है,
  क्योंकि Snowflake केवल वर्तमान डेटाबेस को catalog के रूप में रिपोर्ट करता है। किसी अन्य डेटाबेस की
  सोर्स टेबल्स के लिए अलग कनेक्शन चाहिए।
- **Identifiers बड़े अक्षरों (upper case) में होते हैं** जब तक उन्हें quotes के साथ नहीं बनाया गया हो।
  *digna* नामों का उपयोग वैसे ही करता है जैसे Snowflake उन्हें रिपोर्ट करता है।
- **प्रोफ़ाइलिंग मोड।** *Permanent* वर्क टेबल्स को **Work Schema** में बनाता है, इसलिए role को वहाँ
  `CREATE TABLE` अधिकार चाहिए। *Session* `CREATE TEMPORARY TABLE` का उपयोग करता है और
  **Work Schema** को नहीं छूता। *Standard* को केवल रीड एक्सेस चाहिए — और कोई भी write grant नहीं।

---

## 5. ड्राइवर का सत्यापन (वैकल्पिक) {: #5-verifying-the-driver-optional }

DSN-less कनेक्शन के लिए ODBC डेटा सोर्स कॉन्फ़िगर करना आवश्यक नहीं है, लेकिन ड्राइवर का अपना डायलॉग
यह पुष्टि करने का सुविधाजनक तरीका है कि ड्राइवर, account URL और आपके क्रेडेंशियल्स काम करते हैं,
इससे पहले कि आप उन्हें *digna* में दर्ज करें।

#### चरण 1
![चरण 1](images/snowflake/create_odbc_data_source_step1.png)

टिप्पणियाँ:

- **Server** का मान आपके Snowflake account identifier और उसके बाद
  `.snowflakecomputing.com` से बना होता है।
- यहाँ दर्ज **Database**, **Schema** और **Warehouse** [अनुभाग 2](#2-odbc-properties) की
  `Database`, `Schema` और `Warehouse` प्रॉपर्टीज़ से मेल खाते हैं।

#### चरण 2 – कनेक्शन का परीक्षण करें

**TEST** बटन पर क्लिक करें। सफल कनेक्शन इस प्रकार दिखना चाहिए:

![चरण 2](images/snowflake/create_odbc_data_source_step2.png)