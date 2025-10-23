---
title: Azure Synapse कनेक्टर – Database Integration | digna Documentation
description: *digna* को Azure Synapse Analytics से कनेक्ट करने के लिए कॉन्फ़िगर करें, चाहे आप नेटिव Python ड्राइवर का उपयोग कर रहे हों या ODBC ड्राइवर का। सर्वरलेस और डेडिकेटेड दोनों SQL पूल्स समर्थित हैं।
image: /assets/logo_square.png
---


# Source Connector for Azure Synapse Analytics

यह गाइड बताता है कि *digna* को Azure Synapse Analytics से कनेक्ट करने के लिए कैसे कॉन्फ़िगर किया जाए — चाहे नेटिव Python कनेक्टर का उपयोग करें या ODBC ड्राइवर। यह सर्वरलेस और डेडिकेटेड दोनों SQL पूल्स का समर्थन करता है।

यह स्क्रीन **"Create a Database Connection"** का संदर्भ देता है।

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Supported Authentication:** केवल पासवर्ड-आधारित प्रमाणीकरण

> ⚠️ अन्य प्रमाणीकरण विधियों के लिए कृपया ODBC ड्राइवर का उपयोग करें।

### *digna* Configuration (Native Driver)

**"Create a Database Connection"** स्क्रीन में निम्नलिखित जानकारी प्रदान करें:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC ड्राइवर संभवतः प्रमाणीकरण और कनेक्टिविटी विकल्पों की एक विस्तृत रेंज का समर्थन करता है। यह सेक्शन पासवर्ड-आधारित प्रमाणीकरण पर केंद्रित है और ड्राइवर **ODBC Driver 18 for SQL Server** का उपयोग दिखाता है।

### 1. Install the ODBC Driver

विक्रेता के आधिकारिक इंस्टॉलेशन गाइड का पालन करके **ODBC Driver 18 for SQL Server** (या समान) ड्राइवर इंस्टॉल करें।

### 2. Configure the ODBC Data Source

पासवर्ड-आधारित प्रमाणीकरण का उपयोग करते हुए नया ODBC डेटा स्रोत कॉन्फ़िगर करने के लिए निम्नलिखित चरणों का पालन करें:

#### Step 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

"Server" फ़ील्ड भरें।  
Synapse वर्कस्पेस का नाम उपयोग करें और उसे ".sql.azuresynapse.net" से बढ़ाएं.  
**ध्यान दें**, यदि आप सर्वरलेस SQL पूल का उपयोग करके कनेक्ट करना चाहते हैं, तो सुनिश्चित करें कि "-ondemand" शामिल किया गया हो जैसा कि नीचे स्क्रीनशॉट में दिखाया गया है।

**Next >** बटन पर क्लिक करें।

#### Step 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

प्रमाणीकरण विधि चुनें (उदा. उपयोगकर्ता नाम और पासवर्ड) और आवश्यक जानकारी प्रदान करें।

**Next >** बटन पर क्लिक करें।

#### Step 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

ANSI कम्प्लायंट सेटिंग्स चुनें, फिर **Next >** बटन पर क्लिक करें।

#### Step 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

डिफ़ॉल्ट सेटिंग्स छोड़ सकते हैं या आवश्यकता के अनुसार विकल्प चुनें और **Finish** बटन पर क्लिक करें। 

#### Step 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

अब ** Test datasource ** बटन पर क्लिक करें।

#### Step 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

जब आपको सफलता स्क्रीन मिल जाए, तो ODBC सही तरीके से कॉन्फ़िगर हो गया है।

---

अब आप *digna* को ODBC कनेक्शन का उपयोग करने के लिए कॉन्फ़िगर कर सकते हैं, या तो **DSN (Data Source Name)** के साथ या **DSN-less** सेटअप के साथ।

---

### A. DSN-Based Configuration

#### *digna* Configuration

**"Create a Database Connection"** स्क्रीन में निम्नलिखित प्रदान करें:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 `DSN` वही होना चाहिए जो आपने अपने ODBC ड्राइवर कॉन्फ़िगरेशन में परिभाषित किया है।

---

### B. DSN-less Configuration

#### *digna* Configuration

**"Create a Database Connection"** स्क्रीन में निम्नलिखित प्रदान करें:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**नोट** SERVER प्रॉपर्टी के बारे में:  
Synapse वर्कस्पेस का नाम उपयोग करें और उसे ".sql.azuresynapse.net" से बढ़ाएं। यदि आप सर्वरलेस SQL पूल से कनेक्ट करना चाहते हैं, तो सुनिश्चित करें कि "-ondemand" शामिल किया गया हो जैसा कि नीचे स्क्रीनशॉट में दिखाया गया है।