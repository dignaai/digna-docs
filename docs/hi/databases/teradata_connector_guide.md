---
title: Teradata कनेक्टर – डेटाबेस एकीकरण | digna डॉ큐मेंटेशन
description: teradatasql Python ड्राइवर या Teradata ODBC ड्राइवर का उपयोग करके digna को Teradata से कनेक्ट करने के लिए कॉन्फ़िगर करें। DSN या DSN-less सेटअप के साथ पासवर्ड-आधारित प्रमाणीकरण समर्थित है।
image: /assets/logo_square.png
---


# Teradata के लिए स्रोत कनेक्टर

यह गाइड बताता है कि *digna* को नैटिव Python कनेक्टर या ODBC ड्राइवर में से किसी एक का उपयोग करके Teradata से कैसे कनेक्ट करने के लिए कॉन्फ़िगर किया जाए।

यह स्क्रीन **"Create a Database Connection"** का संदर्भ देती है।

![Create a database connection](images/data_source_config_input_mask.png)

---

## नैटिव Python ड्राइवर

**लाइब्रेरी:** `teradatasql`  
**समर्थित प्रमाणीकरण:** केवल पासवर्ड-आधारित प्रमाणीकरण

> ⚠️ अन्य प्रमाणीकरण विधियों के लिए, कृपया ODBC ड्राइवर का उपयोग करें।

### *digna* कॉन्फ़िगरेशन (नैटिव ड्राइवर)

**"Create a Database Connection"** स्क्रीन में निम्नलिखित जानकारी दें:

```
Technology:      Teradata
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1025
Database Name:   Database name
Schema Name:     Database name
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC ड्राइवर

ODBC ड्राइवर प्रमाणीकरण और कनेक्टिविटी के अधिक विकल्प समर्थन कर सकता है। यह अनुभाग ड्राइवर **Teradata Database ODBC Driver 20.00** का उपयोग करके पासवर्ड-आधारित प्रमाणीकरण पर केंद्रित है।

### 1. ODBC ड्राइवर इंस्टॉल करें

वेंडर के आधिकारिक इंस्टॉलेशन गाइड का अनुसरण करके **Teradata Database ODBC Driver 20.00** (या समान) इंस्टॉल करें।

### 2. ODBC डेटा स्रोत कॉन्फ़िगर करें

पासवर्ड-आधारित प्रमाणीकरण का उपयोग करते हुए नया ODBC डेटा स्रोत कॉन्फ़िगर करने के लिए निम्न चरणों का पालन करें:

#### Step 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

**Test** बटन पर क्लिक करें।

#### Step 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

यूज़रनेम और पासवर्ड प्रदान करें।

**OK** बटन पर क्लिक करें। जब आपको सफलता स्क्रीन मिलती है, तो ODBC सही ढंग से कॉन्फ़िगर हो गया है।

---

अब आप *digna* को ODBC कनेक्शन का उपयोग करने के लिए कॉन्फ़िगर कर सकते हैं, चाहे **DSN (Data Source Name)** के साथ हो या **DSN-less** सेटअप के साथ।

---

### A. DSN-आधारित कॉन्फ़िगरेशन

#### *digna* कॉन्फ़िगरेशन

**"Create a Database Connection"** स्क्रीन में निम्नलिखित प्रदान करें:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC गुण (Properties)

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 `DSN` वही होना चाहिए जो आपके ODBC ड्राइवर कॉन्फ़िगरेशन में परिभाषित किया गया है।

---

### B. DSN-less कॉन्फ़िगरेशन

#### *digna* कॉन्फ़िगरेशन

**"Create a Database Connection"** स्क्रीन में निम्नलिखित प्रदान करें:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC गुण (Properties)

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```
