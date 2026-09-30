---
title: Azure Synapse कनेक्टर – डेटाबेस इंटीग्रेशन | digna दस्तावेज़
description: digna को DSN-less कनेक्शन स्ट्रिंग के साथ ODBC के माध्यम से Azure Synapse Analytics से कनेक्ट करने के लिए कॉन्फ़िगर करें। Serverless और dedicated SQL pools समर्थित हैं, आवश्यक ODBC प्रॉपर्टीज़ और digna-पक्ष की कनेक्शन सेटिंग्स के साथ।
image: /assets/logo_square.png
---


# Azure Synapse Analytics के लिए सोर्स कनेक्टर

यह गाइड बताता है कि *digna* को **DSN-less** कनेक्शन स्ट्रिंग का उपयोग करके **ODBC** के माध्यम से
Azure Synapse Analytics से कनेक्ट करने के लिए कैसे कॉन्फ़िगर करें। Serverless और dedicated SQL
pools दोनों समर्थित हैं।

सेटअप का *digna* पक्ष हर तकनीक के लिए समान है — कनेक्शन कहाँ बनाए जाते हैं, प्रॉपर्टी मान कैसे
एन्क्रिप्ट होते हैं, कनेक्शन का परीक्षण कैसे होता है और प्रोफ़ाइलिंग मोड का क्या अर्थ है। इसका वर्णन
[डेटाबेस कनेक्शन अवलोकन](overview.md) में किया गया है। यह पृष्ठ केवल वही कवर करता है जो
Azure Synapse के लिए विशिष्ट है।

!!! note "Technology"

    Synapse SQL Server बोली का उपयोग करता है, इसलिए कनेक्शन **Technology:
    SQL Server** के साथ बनाया जाता है। ऑन-प्रिमाइसेस सर्वर के लिए [MS SQL Server](sqlserver_connector_guide.md) देखें।

---

## 1. ODBC ड्राइवर इंस्टॉल करें {: #1-install-the-odbc-driver }

[Microsoft की इंस्टॉलेशन गाइड](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
का पालन करते हुए, **ODBC Driver 18 for SQL Server** को उस मशीन पर इंस्टॉल करें जिस पर *digna* बैकएंड
चलता है, और रजिस्टर ड्राइवर का सटीक नाम अपने होस्ट से पढ़ें, जैसा कि
[digna होस्ट पर ODBC ड्राइवर इंस्टॉल करें](overview.md#install-the-driver) में बताया गया है।

---

## 2. ODBC प्रॉपर्टीज़ {: #2-odbc-properties }

!!! important "एक उदाहरण, कोई विनिर्देश नहीं"

    नीचे दिया गया सेट एक ऐसा संयोजन है जो काम करने के लिए जाना जाता है। प्रॉपर्टीज़ Microsoft ODBC
    ड्राइवर की हैं, इसलिए उनके नाम, डिफ़ॉल्ट और स्वीकृत मान ड्राइवर संस्करणों और प्लेटफ़ॉर्म के बीच
    अलग होते हैं, और workspace को क्या चाहिए यह उसके कॉन्फ़िगरेशन पर निर्भर करता है — pool प्रकार,
    प्रमाणीकरण विधि, फ़ायरवॉल। इसे शुरुआती बिंदु के रूप में उपयोग करें और आपके द्वारा इंस्टॉल किए गए
    ड्राइवर संस्करण का दस्तावेज़ देखें।

**Add DB Connection** स्क्रीन में निम्नलिखित प्रॉपर्टीज़ जोड़ें:

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | *digna* होस्ट पर रजिस्टर ड्राइवर नाम से मेल खाना चाहिए |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Workspace नाम और endpoint प्रत्यय — नीचे देखें |
| `DATABASE` | `dignadata` | वह डेटाबेस जिसमें सोर्स स्कीमा हैं। यही एकमात्र डेटाबेस है जिसे यह कनेक्शन प्रोफ़ाइल कर सकता है |
| `UID` | `sqladminuser` | SQL लॉगिन |
| `PWD` | `<password>` | **Encrypted** पर टिक करें |

परिणामी कनेक्शन स्ट्रिंग इस प्रकार दिखती है:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### `SERVER` मान

Synapse workspace का नाम लें और उसमें endpoint प्रत्यय जोड़ें:

| Pool | `SERVER` |
|---|---|
| **Serverless SQL pool** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Dedicated SQL pool** | `<workspace>.sql.azuresynapse.net` |

!!! warning "`-ondemand` वाला हिस्सा आसानी से छूट जाता है"

    इसके बिना, नाम dedicated endpoint पर रिज़ॉल्व होता है, और कनेक्शन या तो विफल हो जाता है या
    चुपचाप अपेक्षित pool के बजाय किसी दूसरे pool तक पहुँच जाता है। दोनों endpoints Azure portal में
    workspace के overview पृष्ठ पर दिखाए जाते हैं।

### फ़ायरवॉल

Synapse workspace फ़ायरवॉल को *digna* होस्ट के आउटबाउंड पते की अनुमति देनी चाहिए। कनेक्शन का परीक्षण
करने से पहले इसे workspace में **Networking** के अंतर्गत जोड़ें — ब्लॉक किया गया पता प्रमाणीकरण
त्रुटि के बजाय कनेक्शन टाइमआउट के रूप में दिखता है।

### Microsoft Entra ID प्रमाणीकरण

SQL लॉगिन के बजाय, ड्राइवर Entra ID के विरुद्ध प्रमाणीकरण कर सकता है। `UID`/`PWD` को उस प्रमाणीकरण
विधि से बदलें जिसकी आपका workspace अपेक्षा करता है, उदाहरण के लिए:

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | तब `UID` application (client) ID लेता है और `PWD` client secret |
| `Authentication` | `ActiveDirectoryMSI` | *digna* होस्ट की managed identity, किसी क्रेडेंशियल की आवश्यकता नहीं |

---

## 3. *digna* कॉन्फ़िगरेशन {: #3-digna-configuration }

**Add DB Connection** स्क्रीन में निम्नलिखित जानकारी दें:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Azure Synapse पर टिप्पणियाँ {: #4-notes-on-azure-synapse }

- **Serverless pools केवल *Standard* प्रोफ़ाइलिंग का समर्थन करते हैं।** Serverless SQL pool किसी
  डेटाबेस में टेबल्स नहीं बना सकता, इसलिए न *Permanent* और न *Session* प्रोफ़ाइलिंग चल सकती है।
  *Standard* मेट्रिक्स की गणना सीधे सोर्स पर करता है, जो सस्ता विकल्प भी है, क्योंकि serverless का
  बिल प्रोसेस किए गए डेटा के अनुसार होता है।
- **एक कनेक्शन एक डेटाबेस देखता है।** *digna* `DATABASE` में नामित डेटाबेस के स्कीमा प्रस्तुत करता
  है, क्योंकि Synapse, SQL Server की तरह, केवल वर्तमान डेटाबेस को catalog के रूप में रिपोर्ट करता है।
- **एन्क्रिप्शन डिफ़ॉल्ट रूप से चालू है** Driver 18 में, और Synapse endpoints मान्य सार्वजनिक
  सर्टिफ़िकेट प्रस्तुत करते हैं, इसलिए किसी `Encrypt` या `TrustServerCertificate` प्रॉपर्टी की
  आवश्यकता नहीं है।
- **Serverless endpoint पहले कनेक्ट पर निष्क्रियता से फिर शुरू हो सकता है।** यदि कुछ समय से अप्रयुक्त
  pool पर कनेक्शन परीक्षण टाइमआउट हो जाता है, तो पुनः प्रयास करें।

---

## 5. ड्राइवर का सत्यापन (वैकल्पिक) {: #5-verifying-the-driver-optional }

DSN-less कनेक्शन के लिए ODBC डेटा सोर्स कॉन्फ़िगर करना आवश्यक नहीं है, लेकिन ड्राइवर का अपना विज़ार्ड
यह पुष्टि करने का सुविधाजनक तरीका है कि ड्राइवर काम करता है और workspace आपके क्रेडेंशियल्स स्वीकार
करता है, इससे पहले कि आप उन्हें *digna* में दर्ज करें।

#### चरण 1
![चरण 1](images/azure_synapse/create_odbc_data_source_step1.png)

"Server" फ़ील्ड भरें।
Synapse workspace के नाम का उपयोग करें और उसमें ".sql.azuresynapse.net" जोड़ें।  
**ध्यान दें**, यदि आप serverless SQL pool का उपयोग करके कनेक्ट करना चाहते हैं, तो ऊपर के
स्क्रीनशॉट में दिखाए अनुसार "-ondemand" शामिल करना सुनिश्चित करें।

**Next >** बटन पर क्लिक करें।

#### चरण 2
![चरण 2](images/azure_synapse/create_odbc_data_source_step2.png)

प्रमाणीकरण विधि चुनें (उदा. उपयोगकर्ता नाम और पासवर्ड)
और आवश्यक डेटा प्रदान करें।

**Next >** बटन पर क्लिक करें।

#### चरण 3
![चरण 3](images/azure_synapse/create_odbc_data_source_step3.png)

ANSI-अनुरूप सेटिंग्स चुनें, फिर **Next >** बटन पर क्लिक करें।

#### चरण 4
![चरण 4](images/azure_synapse/create_odbc_data_source_step4.png)

आप डिफ़ॉल्ट सेटिंग्स रहने दे सकते हैं या आवश्यकतानुसार विकल्प चुन सकते हैं
और **Finish** बटन पर क्लिक करें।

#### चरण 5
![चरण 5](images/azure_synapse/create_odbc_data_source_step5.png)

अब **Test datasource** बटन पर क्लिक करें।

#### चरण 6
![चरण 6](images/azure_synapse/create_odbc_data_source_step6.png)

सफलता स्क्रीन पुष्टि करती है कि ड्राइवर, endpoint और क्रेडेंशियल्स काम करते हैं। आपके द्वारा दर्ज
किए गए मान ठीक वही मान हैं जो [अनुभाग 2](#2-odbc-properties) की प्रॉपर्टीज़ लेती हैं।
