---
title: Teradata कनेक्टर – डेटाबेस इंटीग्रेशन | digna दस्तावेज़
description: digna को DSN-less कनेक्शन स्ट्रिंग के साथ ODBC के माध्यम से Teradata से कनेक्ट करने के लिए कॉन्फ़िगर करें। इसमें Teradata ODBC ड्राइवर, DBCNAME प्रॉपर्टी, logon mechanisms और digna-पक्ष की कनेक्शन सेटिंग्स शामिल हैं।
image: /assets/logo_square.png
---


# Teradata के लिए सोर्स कनेक्टर

यह गाइड बताता है कि *digna* को **DSN-less** कनेक्शन स्ट्रिंग का उपयोग करके **ODBC** के माध्यम से
Teradata से कनेक्ट करने के लिए कैसे कॉन्फ़िगर करें।

सेटअप का *digna* पक्ष हर तकनीक के लिए समान है — कनेक्शन कहाँ बनाए जाते हैं, प्रॉपर्टी मान कैसे
एन्क्रिप्ट होते हैं, कनेक्शन का परीक्षण कैसे होता है और प्रोफ़ाइलिंग मोड का क्या अर्थ है। इसका वर्णन
[डेटाबेस कनेक्शन अवलोकन](overview.md) में किया गया है। यह पृष्ठ केवल वही कवर करता है जो
Teradata के लिए विशिष्ट है।

---

## 1. ODBC ड्राइवर इंस्टॉल करें {: #1-install-the-odbc-driver }

विक्रेता की आधिकारिक इंस्टॉलेशन गाइड का पालन करते हुए, **ODBC Driver for Teradata** को उस मशीन पर
इंस्टॉल करें जिस पर *digna* बैकएंड चलता है।

ड्राइवर अपने नाम में संस्करण के साथ रजिस्टर होता है, उदाहरण के लिए
**Teradata Database ODBC Driver 20.00**। रजिस्टर नाम का सटीक रूप अपने होस्ट से पढ़ें, जैसा कि
[digna होस्ट पर ODBC ड्राइवर इंस्टॉल करें](overview.md#install-the-driver) में बताया गया है।

---

## 2. ODBC प्रॉपर्टीज़ {: #2-odbc-properties }

!!! important "एक उदाहरण, कोई विनिर्देश नहीं"

    नीचे दिया गया सेट एक ऐसा संयोजन है जो काम करने के लिए जाना जाता है। प्रॉपर्टीज़ Teradata ODBC
    ड्राइवर की हैं, इसलिए उनके नाम, डिफ़ॉल्ट और स्वीकृत मान ड्राइवर संस्करणों के बीच — संस्करण स्वयं
    ड्राइवर नाम का हिस्सा है — और प्लेटफ़ॉर्म के बीच अलग होते हैं। इसे शुरुआती बिंदु के रूप में उपयोग
    करें और आपके द्वारा इंस्टॉल किए गए ड्राइवर संस्करण का दस्तावेज़ देखें।

**Add DB Connection** स्क्रीन में निम्नलिखित प्रॉपर्टीज़ जोड़ें:

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | *digna* होस्ट पर रजिस्टर ड्राइवर नाम से मेल खाना चाहिए |
| `DBCNAME` | `teradata.example.com` | सर्वर नाम या IP पता। होस्ट प्रॉपर्टी के लिए Teradata का अपना नाम |
| `UID` | `digna_source_user` | डेटाबेस उपयोगकर्ता |
| `PWD` | `<password>` | **Encrypted** पर टिक करें |

परिणामी कनेक्शन स्ट्रिंग इस प्रकार दिखती है:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

उपयोगी अतिरिक्त प्रॉपर्टीज़:

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `MechanismName` | `TD2` | Logon mechanism। `TD2` Teradata का डिफ़ॉल्ट है; directory प्रमाणीकरण के लिए `LDAP` का उपयोग करें |
| `DefaultDatabase` | `dad` | डेटाबेस जिसमें session शुरू होता है |
| `CharacterSet` | `UTF8` | इसे वहाँ सेट करें जहाँ डिफ़ॉल्ट session character set गैर-ASCII डेटा को बिगाड़ देगा |

---

## 3. *digna* कॉन्फ़िगरेशन {: #3-digna-configuration }

**Add DB Connection** स्क्रीन में निम्नलिखित जानकारी दें:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Teradata पर टिप्पणियाँ {: #4-notes-on-teradata }

- **Teradata डेटाबेस एक catalog है, स्कीमा नहीं।** *digna* उपयोगकर्ता को दिखने वाले डेटाबेस
  (`DBC.DatabasesV` से) को catalogs के रूप में सूचीबद्ध करता है, और स्कीमा स्तर लागू नहीं होता। डेटा
  सोर्स जोड़ते समय, डेटाबेस को catalog के रूप में चुनें; स्कीमा *not applicable* के रूप में रिपोर्ट
  होता है।
- **एक कनेक्शन हर अनुमत डेटाबेस तक पहुँचता है**, इसलिए एक ही कनेक्शन कई डेटाबेस के सोर्सेज़ की सेवा
  कर सकता है — उन तकनीकों के विपरीत जहाँ कनेक्शन एक डेटाबेस से बँधा होता है।
- **Work Schema एक डेटाबेस है।** *Permanent* प्रोफ़ाइलिंग के लिए, उस Teradata डेटाबेस का नाम दें जिसमें
  वर्क टेबल्स रहती हैं, और उपयोगकर्ता को उसमें `CREATE TABLE` अधिकार और `PERM` space आवंटन दें — शून्य
  perm space वाला डेटाबेस कोई टेबल नहीं रख सकता।
- **प्रोफ़ाइलिंग मोड।** *Permanent* **Work Schema** में टेबल्स बनाता है। *Session* एक `VOLATILE` टेबल
  का उपयोग करता है, जिसके लिए `SPOOL` space चाहिए लेकिन न perm space और न **Work
  Schema** में कोई अधिकार। *Standard* को केवल रीड एक्सेस चाहिए।

---

## 5. ड्राइवर का सत्यापन (वैकल्पिक) {: #5-verifying-the-driver-optional }

DSN-less कनेक्शन के लिए ODBC डेटा सोर्स कॉन्फ़िगर करना आवश्यक नहीं है, लेकिन ड्राइवर का अपना डायलॉग
यह पुष्टि करने का सुविधाजनक तरीका है कि ड्राइवर और आपके क्रेडेंशियल्स काम करते हैं, इससे पहले कि आप
उन्हें *digna* में दर्ज करें।

#### चरण 1
![चरण 1](images/teradata/create_odbc_data_source_step1.png)

यहाँ का **Name or IP address** फ़ील्ड [अनुभाग 2](#2-odbc-properties) की `DBCNAME` प्रॉपर्टी है।

**Test** बटन पर क्लिक करें।

#### चरण 2
![चरण 2](images/teradata/create_odbc_data_source_step2.png)

उपयोगकर्ता नाम और पासवर्ड दें, फिर **OK** बटन पर क्लिक करें। सफलता स्क्रीन पुष्टि करती है कि ड्राइवर
और क्रेडेंशियल्स काम करते हैं।
