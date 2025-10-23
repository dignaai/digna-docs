---
title: Snowflake कनेक्टर – डेटाबेस इंटीग्रेशन | digna दस्तावेज़ीकरण
description: Python कनेक्टर या Snowflake ODBC ड्राइवर का उपयोग करके Snowflake से कनेक्ट करने के लिए digna को कॉन्फ़िगर करें। DSN या DSN-less सेटअप के साथ पासवर्ड-आधारित प्रमाणीकरण का समर्थन।
image: /assets/logo_square.png
---


# Snowflake के लिए स्रोत कनेक्टर

यह गाइड बताती है कि *digna* को Snowflake से कनेक्ट करने के लिए कैसे कॉन्फ़िगर किया जाए — या तो नेटिव Python कनेक्टर के माध्यम से या ODBC ड्राइवर के जरिए।

यह स्क्रीन **"Create a Database Connection"** का संदर्भ देती है।

![एक डेटाबेस कनेक्शन बनाएं](images/data_source_config_input_mask.png)

---

## नेटिव Python ड्राइवर

**Library:** `snowflake-connector-python`  
**Supported Authentication:** केवल पासवर्ड-आधारित प्रमाणीकरण

> ⚠️ अन्य प्रमाणीकरण विधियों के लिए, कृपया ODBC ड्राइवर का उपयोग करें।

### *digna* कॉन्फ़िगरेशन (नेटिव ड्राइवर)

**"Create a Database Connection"** स्क्रीन में निम्न जानकारी प्रदान करें:

```
Technology:      Snowflake
Host Address:    Snowflake account name
Host Port:       Not needed
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
User Name:       User name and warehouse in the format "user<@>warehouse"
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC ड्राइवर

ODBC ड्राइवर प्रमाणीकरण और कनेक्टिविटी के अधिक विकल्पों का समर्थन कर सकता है। यह अनुभाग पासवर्ड-आधारित प्रमाणीकरण पर ध्यान केंद्रित करता है जिसमें **SnowflakeDSIIDriver** का उपयोग होता है।

### 1. ODBC ड्राइवर इंस्टॉल करें

वेंडर के आधिकारिक इंस्टॉलेशन गाइड का पालन करके **SnowflakeDSIIDriver** इंस्टॉल करें।

### 2. ODBC डेटा स्रोत कॉन्फ़िगर करें

पासवर्ड-आधारित प्रमाणीकरण का उपयोग करके नया ODBC डेटा स्रोत कॉन्फ़िगर करने के लिए ये चरण अपनाएँ:

#### चरण 1
![चरण 1](images/snowflake/create_odbc_data_source_step1.png)

नोट:
- यदि आप Database, Schema और Warehouse के लिए मान प्रदान नहीं करते हैं, तो आपको *digna* डेटा स्रोत कॉन्फ़िगरेशन के दौरान इन्हें ODBC प्रॉपर्टीज़ के रूप में प्रदान करना होगा।
- "Server" का मान आपके Snowflake अकाउंट नाम के साथ ".snowflakecomputing.com" जुड़ा हुआ होता है

#### चरण 2 – कनेक्शन का परीक्षण

**TEST** बटन पर क्लिक करें। सफल कनेक्शन कुछ इस तरह दिखना चाहिए:

![चरण 2](images/snowflake/create_odbc_data_source_step2.png)

---

अब आप *digna* को ODBC कनेक्शन का उपयोग करने के लिए कॉन्फ़िगर कर सकते हैं, या तो **DSN (Data Source Name)** के साथ या **DSN-less** सेटअप के साथ।

---

### A. DSN-आधारित कॉन्फ़िगरेशन

#### *digna* कॉन्फ़िगरेशन

**"Create a Database Connection"** स्क्रीन में निम्न प्रदान करें:

```
Technology:      Snowflake
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC प्रॉपर्टीज़

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionally:
name: "Database",       value: "Database that contains the source schema"
name: "Schema",         value: "Schema that contains the source data"
name: "Warehouse",      value: "Warehouse to use for the execution of the SQLs"
```

> 🔹 `DSN` को आपके ODBC ड्राइवर कॉन्फ़िगरेशन में परिभाषित नाम से मेल खाना चाहिए।

---

### B. DSN-less कॉन्फ़िगरेशन

#### *digna* कॉन्फ़िगरेशन

**"Create a Database Connection"** स्क्रीन में निम्न प्रदान करें:

```
Technology:      Snowflake
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC प्रॉपर्टीज़

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Database that contains the source schema"
name: "Schema",     value: "Schema that contains the source data"
name: "Warehouse",  value: "Warehouse to use for the execution of the SQLs"
```
