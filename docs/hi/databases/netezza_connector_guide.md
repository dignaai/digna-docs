---
title: Netezza कनेक्टर – डेटाबेस इंटीग्रेशन | digna दस्तावेज़
description: digna को DSN-less कनेक्शन स्ट्रिंग के साथ ODBC के माध्यम से Netezza से कनेक्ट करने के लिए कॉन्फ़िगर करें। इसमें NetezzaSQL ड्राइवर, आवश्यक ODBC प्रॉपर्टीज़ और digna-पक्ष की कनेक्शन सेटिंग्स शामिल हैं।
image: /assets/logo_square.png
---


# Netezza के लिए सोर्स कनेक्टर

यह गाइड बताता है कि *digna* को **DSN-less** कनेक्शन स्ट्रिंग का उपयोग करके **ODBC** के माध्यम से
Netezza से कनेक्ट करने के लिए कैसे कॉन्फ़िगर करें।

सेटअप का *digna* पक्ष हर तकनीक के लिए समान है — कनेक्शन कहाँ बनाए जाते हैं, प्रॉपर्टी मान कैसे
एन्क्रिप्ट होते हैं, कनेक्शन का परीक्षण कैसे होता है और प्रोफ़ाइलिंग मोड का क्या अर्थ है। इसका वर्णन
[डेटाबेस कनेक्शन अवलोकन](overview.md) में किया गया है। यह पृष्ठ केवल वही कवर करता है जो
Netezza के लिए विशिष्ट है।

---

## 1. ODBC ड्राइवर इंस्टॉल करें {: #1-install-the-odbc-driver }

विक्रेता की आधिकारिक इंस्टॉलेशन गाइड का पालन करते हुए, **NetezzaSQL** ODBC ड्राइवर (IBM Netezza
client tools का हिस्सा) को उस मशीन पर इंस्टॉल करें जिस पर *digna* बैकएंड चलता है।

रजिस्टर ड्राइवर का सटीक नाम अपने होस्ट से पढ़ें, जैसा कि
[digna होस्ट पर ODBC ड्राइवर इंस्टॉल करें](overview.md#install-the-driver) में बताया गया है।

---

## 2. ODBC प्रॉपर्टीज़ {: #2-odbc-properties }

!!! important "एक उदाहरण, कोई विनिर्देश नहीं"

    नीचे दिया गया सेट एक ऐसा संयोजन है जो काम करने के लिए जाना जाता है। प्रॉपर्टीज़ NetezzaSQL
    ड्राइवर की हैं, इसलिए उनके नाम, डिफ़ॉल्ट और स्वीकृत मान client संस्करणों और प्लेटफ़ॉर्म के बीच
    अलग होते हैं, और TLS से सुरक्षित appliance को यहाँ दिखाई गई प्रॉपर्टीज़ से अधिक की आवश्यकता होती
    है। इसे शुरुआती बिंदु के रूप में उपयोग करें और आपके द्वारा इंस्टॉल किए गए client संस्करण का
    दस्तावेज़ देखें।

**Add DB Connection** स्क्रीन में निम्नलिखित प्रॉपर्टीज़ जोड़ें:

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | *digna* होस्ट पर रजिस्टर ड्राइवर नाम से मेल खाना चाहिए। इस नाम को लिखने का सामान्य तरीका ब्रेसेस के साथ है |
| `SERVER` | `netezza.example.com` | सर्वर नाम या IP पता |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | डेटाबेस जिसमें session शुरू होता है |
| `UID` | `ADMIN` | डेटाबेस उपयोगकर्ता |
| `PWD` | `<password>` | **Encrypted** पर टिक करें |

परिणामी कनेक्शन स्ट्रिंग इस प्रकार दिखती है:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

आपके ड्राइवर संस्करण, सेटअप और सुरक्षा आवश्यकताओं के अनुसार, और प्रॉपर्टीज़ की आवश्यकता हो सकती है —
उदाहरण के लिए TLS से सुरक्षित appliance के लिए `SecurityLevel` और `CaCertFile`। ड्राइवर के
*Advanced*, *SSL* और *Driver* डायलॉग में उपलब्ध हर विकल्प को प्रॉपर्टी के रूप में जोड़ा जा सकता है।

---

## 3. *digna* कॉन्फ़िगरेशन {: #3-digna-configuration }

**Add DB Connection** स्क्रीन में निम्नलिखित जानकारी दें:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Netezza पर टिप्पणियाँ {: #4-notes-on-netezza }

- **Catalogs और स्कीमा दोनों लागू होते हैं।** *digna* उपयोगकर्ता को दिखने वाले डेटाबेस (`_V_DATABASE`
  से) को catalogs के रूप में और उनके स्कीमा (`_V_SCHEMA` से) को उनके नीचे सूचीबद्ध करता है, इसलिए एक
  कनेक्शन एक से अधिक डेटाबेस के सोर्सेज़ की सेवा कर सकता है। `DATABASE` केवल यह तय करता है कि session
  कहाँ शुरू होता है।
- **Identifiers बड़े अक्षरों (upper case) में होते हैं** जब तक उन्हें quotes के साथ नहीं बनाया गया हो,
  इसी कारण ऊपर के उदाहरण `TEST` और `ADMIN` का उपयोग करते हैं।
- **प्रोफ़ाइलिंग मोड।** *Permanent* वर्क टेबल्स को **Work Schema** में बनाता है, इसलिए उपयोगकर्ता को
  वहाँ `CREATE TABLE` अधिकार चाहिए। *Session* `CREATE TEMPORARY TABLE` का उपयोग करता है और
  **Work Schema** को नहीं छूता। *Standard* को केवल रीड एक्सेस चाहिए।

---

## 5. ड्राइवर का सत्यापन (वैकल्पिक) {: #5-verifying-the-driver-optional }

DSN-less कनेक्शन के लिए ODBC डेटा सोर्स कॉन्फ़िगर करना आवश्यक नहीं है, लेकिन ड्राइवर का अपना डायलॉग
यह पुष्टि करने का सुविधाजनक तरीका है कि ड्राइवर और आपके क्रेडेंशियल्स काम करते हैं, इससे पहले कि आप
उन्हें *digna* में दर्ज करें।

#### चरण 1
![चरण 1](images/netezza/create_odbc_data_source_step1.png)

**DSN Options** के फ़ील्ड [अनुभाग 2](#2-odbc-properties) की प्रॉपर्टीज़ से एक-एक करके मेल खाते हैं।
आपके Netezza ड्राइवर, सेटअप और सुरक्षा आवश्यकताओं के अनुसार, आपको **Advanced DSN Options**,
**SSL DSN Options** या **Driver Options** टैब में भी डेटा की आवश्यकता हो सकती है; सबसे सरल सेटअप
के लिए **DSN Options** पर्याप्त है।

**Test Connection** बटन पर क्लिक करें।

#### चरण 2
![चरण 2](images/netezza/create_odbc_data_source_step2.png)

जब आपको सफलता स्क्रीन मिलती है, तो ड्राइवर काम कर रहा है और मान सही हैं।
