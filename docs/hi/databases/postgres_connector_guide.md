---
title: PostgreSQL Connector – Database Integration | digna डॉ큐मेंटेशन
description: psycopg Python ड्राइवर या PostgreSQL ODBC ड्राइवर का उपयोग करके digna को PostgreSQL से कनेक्ट करने के लिए कॉन्फ़िगर करें। DSN या DSN-less सेटअप के साथ पासवर्ड-आधारित प्रमाणिकरण का समर्थन।
image: /assets/logo_square.png
---


# PostgreSQL के लिए Source Connector

यह गाइड बताती है कि *digna* को नेटिव Python कनेक्टर या ODBC ड्राइवर का उपयोग करके Postgres से कैसे कनेक्ट करना है।

यह स्क्रीन **"Create a Database Connection"** को संदर्भित करती है।

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `psycopg`  
**Supported Authentication:** केवल पासवर्ड-आधारित प्रमाणिकरण

> ⚠️ अन्य प्रमाणिकरण विधियों के लिए, कृपया ODBC ड्राइवर का उपयोग करें।

### *digna* Configuration (Native Driver)

**"Create a Database Connection"** स्क्रीन में निम्नलिखित जानकारी प्रदान करें:

```
Technology:      Postgres
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 5432
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC ड्राइवर प्रमाणिकरण और कनेक्टिविटी विकल्पों की अधिक विस्तृत श्रृंखला का समर्थन कर सकता है। यह सेक्शन पासवर्ड-आधारित प्रमाणिकरण पर ध्यान केंद्रित करता है और ड्राइवर **PostgreSQL Unicode(x64)** का उपयोग दिखाता है।

### 1. ODBC ड्राइवर इंस्टॉल करें

वेंडर के आधिकारिक इंस्टॉलेशन गाइड का पालन करके **PostgreSQL Unicode(x64)** (या समान) इंस्टॉल करें।

### 2. ODBC Data Source कॉन्फ़िगर करें

पासवर्ड-आधारित प्रमाणिकरण का उपयोग करते हुए नया ODBC डेटा सोर्स कॉन्फ़िगर करने के लिए निम्न चरणों का पालन करें:

#### Step 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

नोट: यदि आपके डेटाबेस सेटअप में किसी विशेष "SSLMode" को चुनने की आवश्यकता है, तो कृपया DSN-less कॉन्फ़िगरेशन को परिभाषित करते समय भी वही उपयोग करें।

#### Step 2 – Test the connection

**Test Connection** बटन पर क्लिक करें।

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

अब आप *digna* को ODBC कनेक्शन का उपयोग करने के लिए कॉन्फ़िगर कर सकते हैं, या तो **DSN (Data Source Name)** के साथ या **DSN-less** सेटअप के साथ।

---

### A. DSN-Based Configuration

#### *digna* Configuration

**"Create a Database Connection"** स्क्रीन में निम्नलिखित प्रदान करें:

```
Technology:      PostgreSQL
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 `DSN` को आपके ODBC ड्राइवर कॉन्फ़िगरेशन में परिभाषित नाम से मिलना चाहिए।

---

### B. DSN-less Configuration

#### *digna* Configuration

**"Create a Database Connection"** स्क्रीन में निम्नलिखित प्रदान करें:

```
Technology:      PostgreSQL
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```