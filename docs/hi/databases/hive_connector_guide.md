---
title: Apache Hive कनेक्टर – Database Integration | digna Documentation
description: नेटिव PyHive ड्राइवर या Cloudera ODBC ड्राइवर का उपयोग करके digna को Apache Hive से कनेक्ट करने के लिए कॉन्फ़िगर करें। पासवर्ड-आधारित प्रमाणीकरण और DSN या DSN-लेस सेटअप सपोर्ट करता है।
image: /assets/logo_square.png
---


# Hive के लिए स्रोत कनेक्टर

यह गाइड बताता है कि *digna* को Hive से कनेक्ट करने के लिए या तो नेटिव Python कनेक्टर या ODBC ड्राइवर का उपयोग करके कैसे कॉन्फ़िगर किया जाए।

यह **"Create a Database Connection"** स्क्रीन का संदर्भ देता है।

![Create a database connection](images/data_source_config_input_mask.png)

---

## नेटिव Python ड्राइवर

**लाइब्रेरी:** `PyHive`  
**सपोर्टेड प्रमाणीकरण:** केवल पासवर्ड-आधारित प्रमाणीकरण

> ⚠️ अन्य प्रमाणीकरण विधियों के लिए, कृपया ODBC ड्राइवर का उपयोग करें।

### *digna* कॉन्फ़िगरेशन (नेटिव ड्राइवर)

**"Create a Database Connection"** स्क्रीन में निम्नलिखित जानकारी प्रदान करें:

```
Technology:      Apache Hive
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 10000
Database Name:   Schema that contains the source data
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC ड्राइवर

ODBC ड्राइवर प्रमाणीकरण और कनेक्टिविटी विकल्पों की व्यापक रेंज का समर्थन कर सकता है। यह सेक्शन ड्राइवर **Cloudera ODBC Driver for Apache Hive** का उपयोग करके पासवर्ड-आधारित प्रमाणीकरण पर केंद्रित है।

### 1. ODBC ड्राइवर इंस्टॉल करें

वेंडर के आधिकारिक इंस्टॉलेशन गाइड का पालन करते हुए **Cloudera ODBC Driver for Apache Hive** (या समान) इंस्टॉल करें।

### 2. ODBC डेटा स्रोत कॉन्फ़िगर करें

पासवर्ड-आधारित प्रमाणीकरण का उपयोग करके नया ODBC डेटा स्रोत कॉन्फ़िगर करने के लिए इन चरणों का पालन करें:

#### चरण 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### चरण 2 – कनेक्शन का परीक्षण

पासवर्ड दें और **Test** बटन पर क्लिक करें।

![Step 2](images/hive/create_odbc_data_source_step2.png)

सफल परीक्षण के बाद, **OK** बटन पर क्लिक करें।

---

अब आप *digna* को ODBC कनेक्शन का उपयोग करने के लिए कॉन्फ़िगर कर सकते हैं, या तो **DSN (Data Source Name)** के साथ या **DSN-less** सेटअप के साथ।

---

### A. DSN-आधारित कॉन्फ़िगरेशन

#### *digna* कॉन्फ़िगरेशन

**"Create a Database Connection"** स्क्रीन में निम्नलिखित प्रदान करें:

```
Technology:      Apache Hive
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{your password in curly braces}"
```

> 🔹 The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSन-लेस कॉन्फ़िगरेशन

#### *digna* कॉन्फ़िगरेशन

**"Create a Database Connection"** स्क्रीन में निम्नलिखित प्रदान करें:

```
Technology:      Apache Hive
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 10000"
name: "Schema",     value: "Schema that contains the source data"
name: "UID",        value: "your hive user'
name: "PWD",        value: "your hive password"
name: "AuthMech",   value: "3"
```