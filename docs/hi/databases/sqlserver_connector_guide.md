---
title: MS SQL Server कनेक्टर – डेटाबेस इंटीग्रेशन | digna दस्तावेज़
description: digna को DSN-less कनेक्शन स्ट्रिंग के साथ ODBC के माध्यम से Microsoft SQL Server से कनेक्ट करने के लिए कॉन्फ़िगर करें। इसमें Microsoft ODBC ड्राइवर, आवश्यक ODBC प्रॉपर्टीज़, एन्क्रिप्शन सेटिंग्स और digna-पक्ष की कनेक्शन सेटिंग्स शामिल हैं।
image: /assets/logo_square.png
---


# MS SQL Server के लिए सोर्स कनेक्टर

यह गाइड बताता है कि *digna* को **DSN-less** कनेक्शन स्ट्रिंग का उपयोग करके **ODBC** के माध्यम से
Microsoft SQL Server से कनेक्ट करने के लिए कैसे कॉन्फ़िगर करें।

सेटअप का *digna* पक्ष हर तकनीक के लिए समान है — कनेक्शन कहाँ बनाए जाते हैं, प्रॉपर्टी मान कैसे
एन्क्रिप्ट होते हैं, कनेक्शन का परीक्षण कैसे होता है और प्रोफ़ाइलिंग मोड का क्या अर्थ है। इसका वर्णन
[डेटाबेस कनेक्शन अवलोकन](overview.md) में किया गया है। यह पृष्ठ केवल वही कवर करता है जो
SQL Server के लिए विशिष्ट है।

!!! note "Azure Synapse Analytics"

    Synapse को भी SQL Server कनेक्शन के रूप में कॉन्फ़िगर किया जाता है, एक अलग होस्ट नाम और कुछ
    अतिरिक्त बातों के साथ — देखें [Azure Synapse](azure_synapse_connector_guide.md)।

---

## 1. ODBC ड्राइवर इंस्टॉल करें {: #1-install-the-odbc-driver }

[Microsoft की इंस्टॉलेशन गाइड](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
का पालन करते हुए, **ODBC Driver 18 for SQL Server** को उस मशीन पर इंस्टॉल करें जिस पर *digna* बैकएंड
चलता है।

Windows के साथ आने वाला, केवल **SQL Server** नाम वाला ड्राइवर भी काम करता है, लेकिन वह बहुत पहले
प्रतिस्थापित हो चुका है और न आधुनिक TLS सेटिंग्स का समर्थन करता है और न Azure प्रमाणीकरण का। इसका
उपयोग केवल वहीं करें जहाँ वर्तमान ड्राइवर इंस्टॉल करना संभव न हो।

रजिस्टर ड्राइवर का सटीक नाम अपने होस्ट से पढ़ें, जैसा कि
[digna होस्ट पर ODBC ड्राइवर इंस्टॉल करें](overview.md#install-the-driver) में बताया गया है।

---

## 2. ODBC प्रॉपर्टीज़ {: #2-odbc-properties }

!!! important "एक उदाहरण, कोई विनिर्देश नहीं"

    नीचे दिया गया सेट एक ऐसा संयोजन है जो काम करने के लिए जाना जाता है। प्रॉपर्टीज़ Microsoft ODBC
    ड्राइवर की हैं, इसलिए उनके नाम, डिफ़ॉल्ट और स्वीकृत मान ड्राइवर संस्करणों के बीच — उदाहरण के लिए
    Driver 18 डिफ़ॉल्ट रूप से एन्क्रिप्ट करता है जबकि Driver 17 नहीं करता था — और प्लेटफ़ॉर्म के बीच
    अलग होते हैं। इसे शुरुआती बिंदु के रूप में उपयोग करें और आपके द्वारा इंस्टॉल किए गए ड्राइवर
    संस्करण का दस्तावेज़ देखें।

**Add DB Connection** स्क्रीन में निम्नलिखित प्रॉपर्टीज़ जोड़ें:

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | *digna* होस्ट पर रजिस्टर ड्राइवर नाम से मेल खाना चाहिए |
| `SERVER` | `sql.example.com` | सर्वर नाम या IP पता। Named instances: `host\instance`; गैर-डिफ़ॉल्ट पोर्ट: `host,1433` |
| `PORT` | `1433` | जब पोर्ट पहले से `SERVER` का हिस्सा हो तो छोड़ दें |
| `DATABASE` | `digna_source_db` | वह डेटाबेस जिसमें सोर्स स्कीमा हैं। यही एकमात्र डेटाबेस है जिसे यह कनेक्शन प्रोफ़ाइल कर सकता है |
| `UID` | `digna_source_user` | डेटाबेस उपयोगकर्ता |
| `PWD` | `<password>` | **Encrypted** पर टिक करें |

परिणामी कनेक्शन स्ट्रिंग इस प्रकार दिखती है:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### ODBC Driver 18 के साथ एन्क्रिप्शन

Driver 18 डिफ़ॉल्ट रूप से कनेक्शन एन्क्रिप्ट करता है और सर्वर सर्टिफ़िकेट को सत्यापित करता है। ऐसे
सर्वर के विरुद्ध जिसके सर्टिफ़िकेट पर आपका *digna* होस्ट भरोसा नहीं करता — आमतौर पर एक self-signed
सर्टिफ़िकेट — कनेक्ट certificate-chain त्रुटि के साथ विफल हो जाता है। जोड़ें:

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `Encrypt` | `yes` | Driver 18 में डिफ़ॉल्ट; `no` पर केवल तभी सेट करें जब सर्वर TLS न कर सके |
| `TrustServerCertificate` | `yes` | सर्टिफ़िकेट सत्यापन छोड़ देता है। परीक्षण वातावरण में सुविधाजनक; प्रोडक्शन में सर्टिफ़िकेट इंस्टॉल करना बेहतर है |

### Windows Authentication

SQL लॉगिन के बजाय उस खाते के रूप में कनेक्ट करने के लिए जो *digna* सर्विस चलाता है, `UID` और `PWD`
हटाएँ और जोड़ें:

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `Trusted_Connection` | `yes` | *digna* सर्विस खाते को डेटाबेस अधिकार चाहिए |

---

## 3. *digna* कॉन्फ़िगरेशन {: #3-digna-configuration }

**Add DB Connection** स्क्रीन में निम्नलिखित जानकारी दें:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. MS SQL Server पर टिप्पणियाँ {: #4-notes-on-ms-sql-server }

- **एक कनेक्शन एक डेटाबेस देखता है।** *digna* `DATABASE` में नामित डेटाबेस के स्कीमा प्रस्तुत करता
  है, क्योंकि SQL Server केवल वर्तमान डेटाबेस को catalog के रूप में रिपोर्ट करता है। किसी अन्य डेटाबेस
  की सोर्स टेबल्स के लिए अलग कनेक्शन चाहिए।
- **प्रोफ़ाइलिंग मोड।** *Permanent* वर्क टेबल्स को **Work Schema** में बनाता है, इसलिए उपयोगकर्ता को
  वहाँ `CREATE TABLE` अधिकार चाहिए। *Session* `tempdb` में local temporary tables (`#wt_…`) का उपयोग
  करता है और **Work Schema** को नहीं छूता। *Standard* को केवल रीड एक्सेस चाहिए।
- **`SERVER` में instance और पोर्ट होते हैं।** Named instance के साथ, `host\instance` के लिए
  SQL Server Browser सर्विस पहुँच में होनी चाहिए; `host,port` इससे बचाता है।

---

## 5. ड्राइवर का सत्यापन (वैकल्पिक) {: #5-verifying-the-driver-optional }

DSN-less कनेक्शन के लिए ODBC डेटा सोर्स कॉन्फ़िगर करना आवश्यक नहीं है, लेकिन ड्राइवर का अपना विज़ार्ड
यह पुष्टि करने का सुविधाजनक तरीका है कि ड्राइवर काम करता है और सर्वर आपके क्रेडेंशियल्स स्वीकार करता
है, इससे पहले कि आप उन्हें *digna* में दर्ज करें।

#### चरण 1
![चरण 1](images/sqlserver/create_odbc_data_source_step1.png)

**Next >** बटन पर क्लिक करें।

#### चरण 2
![चरण 2](images/sqlserver/create_odbc_data_source_step2.png)

प्रमाणीकरण विधि चुनें (उदा. उपयोगकर्ता नाम और पासवर्ड)
और आवश्यक डेटा प्रदान करें।

**Next >** बटन पर क्लिक करें।

#### चरण 3
![चरण 3](images/sqlserver/create_odbc_data_source_step3.png)

ANSI-अनुरूप सेटिंग्स चुनें, फिर **Next >** बटन पर क्लिक करें।

#### चरण 4
![चरण 4](images/sqlserver/create_odbc_data_source_step4.png)

आप डिफ़ॉल्ट सेटिंग्स रहने दे सकते हैं या आवश्यकतानुसार logging विकल्प चुन सकते हैं
और **Finish** बटन पर क्लिक करें।

#### चरण 5
![चरण 5](images/sqlserver/create_odbc_data_source_step5.png)

अब **Test datasource** बटन पर क्लिक करें।

#### चरण 6
![चरण 6](images/sqlserver/create_odbc_data_source_step6.png)

सफलता स्क्रीन पुष्टि करती है कि ड्राइवर और क्रेडेंशियल्स काम करते हैं। आपके द्वारा दर्ज किए गए मान
ठीक वही मान हैं जो [अनुभाग 2](#2-odbc-properties) की प्रॉपर्टीज़ लेती हैं।
