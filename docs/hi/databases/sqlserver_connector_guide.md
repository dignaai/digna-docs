---
title: MS SQL Server कनेक्टर – डेटाबेस इंटीग्रेशन | digna दस्तावेज़ीकरण
description: pymssql Python ड्राइवर या SQL Server ODBC ड्राइवर का उपयोग करके Microsoft SQL Server से कनेक्ट करने के लिए digna को कॉन्फ़िगर करें। DSN या DSN-less सेटअप के साथ पासवर्ड-आधारित प्रमाणीकरण का समर्थन।
image: /assets/logo_square.png
---


# MS SQL Server के लिए स्रोत कनेक्टर

यह मार्गदर्शिका बताती है कि *digna* को SQL Server से कनेक्ट करने के लिए नेटिव Python कनेक्टर या ODBC ड्राइवर में से किसी एक का उपयोग करके कैसे कॉन्फ़िगर किया जाए।

यह स्क्रीन **"Create a Database Connection"** का संदर्भ देती है।

![Create a database connection](images/data_source_config_input_mask.png)

---

## नेटिव Python ड्राइवर

**Library:** `pymssql`  
**समर्थित प्रमाणीकरण:** केवल पासवर्ड-आधारित प्रमाणीकरण

> ⚠️ अन्य प्रमाणीकरण विधियों के लिए कृपया ODBC ड्राइवर का उपयोग करें।

### *digna* कॉन्फ़िगरेशन (नेटिव ड्राइवर)

**"Create a Database Connection"** स्क्रीन में निम्न जानकारी दें:

```
Technology:      MS SQL Server
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC ड्राइवर

ODBC ड्राइवर प्रमाणीकरण और कनेक्टिविटी विकल्पों की अधिक विस्तृत रेंज का समर्थन कर सकता है। यह अनुभाग ड्राइवर **SQL Server** का उपयोग करके पासवर्ड-आधारित प्रमाणीकरण पर केंद्रित है।

### 1. ODBC ड्राइवर इंस्टॉल करें

वेंडर के आधिकारिक इंस्टॉलेशन गाइड का पालन करके **SQL Server** (या समान) ड्राइवर इंस्टॉल करें।

### 2. ODBC डेटा स्रोत कॉन्फ़िगर करें

पासवर्ड-आधारित प्रमाणीकरण का उपयोग करते हुए नया ODBC डेटा स्रोत कॉन्फ़िगर करने के लिए ये कदम फ़ॉलो करें:

#### Step 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

**Next >** बटन पर क्लिक करें।

#### Step 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

प्रमाणीकरण विधि चुनें (उदाहरण: उपयोगकर्ता नाम और पासवर्ड) और आवश्यक डेटा प्रदान करें।

**Next >** बटन पर क्लिक करें।

#### Step 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

ANSI कम्पलाइंट सेटिंग्स चुनें फिर **Next >** बटन पर क्लिक करें।

#### Step 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

आप डिफ़ॉल्ट सेटिंग्स छोड़ सकते हैं या आवश्यकतानुसार लॉगिंग विकल्प चुन सकते हैं और फिर **Finish** बटन पर क्लिक करें। 

#### Step 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

अब ** Test datasource ** बटन पर क्लिक करें।

#### Step 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

जब आपको सफल स्क्रीन मिल जाए, तो ODBC सही ढंग से कॉन्फ़िगर हो चुका है।

---

अब आप *digna* को ODBC कनेक्शन का उपयोग करने के लिए कॉन्फ़िगर कर सकते हैं, या तो **DSN (Data Source Name)** के साथ या **DSN-less** सेटअप के साथ।

---

### A. DSN-आधारित कॉन्फ़िगरेशन

#### *digna* कॉन्फ़िगरेशन

**"Create a Database Connection"** स्क्रीन में निम्न जानकारी दें:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC गुण (ODBC Properties)

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 `DSN` आपके ODBC ड्राइवर कॉन्फ़िगरेशन में परिभाषित नाम से मेल खाना चाहिए।

---

### B. DSN-less कॉन्फ़िगरेशन

#### *digna* कॉन्फ़िगरेशन

**"Create a Database Connection"** स्क्रीन में निम्न जानकारी दें:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC गुण (ODBC Properties)

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```