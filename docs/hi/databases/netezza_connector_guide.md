---
title: Netezza कनेक्टर – डेटाबेस एकीकरण | digna दस्तावेज़ीकरण
description: digna को NetezzaSQL ODBC ड्राइवर का उपयोग करके Netezza से कनेक्ट करने के लिए कॉन्फ़िगर करें। फ्लेक्सिबल कनेक्टिविटी के लिए DSN या DSN-less सेटअप के साथ पासवर्ड-आधारित प्रमाणीकरण का समर्थन।
image: /assets/logo_square.png
---


# Source Connector for Netezza

यह गाइड बताती है कि *digna* को ODBC ड्राइवर का उपयोग करके Netezza से कैसे कनेक्ट करने के लिए कॉन्फ़िगर किया जाए।

यह स्क्रीन **"Create a Database Connection"** का उल्लेख करती है।

![एक डेटाबेस कनेक्शन बनाएँ](images/data_source_config_input_mask.png)

---

## ODBC Driver

ODBC ड्राइवर विभिन्न प्रमाणीकरण और कनेक्टिविटी विकल्पों का समर्थन कर सकता है। यह अनुभाग ड्राइवर **NetezzaSQL** का उपयोग करके पासवर्ड-आधारित प्रमाणीकरण पर केंद्रित है।

### 1. Install the ODBC Driver

ड्राइवर **NetezzaSQL** (या समान) को विक्रेता के आधिकारिक इंस्टॉलेशन गाइड का पालन करके इंस्टॉल करें।

### 2. Configure the ODBC Data Source

पासवर्ड-आधारित प्रमाणीकरण का उपयोग करके नया ODBC डेटा सोर्स कॉन्फ़िगर करने के लिए इन चरणों का पालन करें:

#### Step 1
![चरण 1](images/netezza/create_odbc_data_source_step1.png)

आपके Netezza ड्राइवर, सेटअप और सुरक्षा आवश्यकताओं के आधार पर, आपको **Advanced DSN Options**, **SSL DSN Options** या **Driver Options** टैब में भी डेटा प्रदान करने की आवश्यकता हो सकती है। सबसे सरल सेटअप के लिए **DSN Options** में डेटा प्रदान करना पर्याप्त होता है।

**Test Connection** बटन पर क्लिक करें।

#### Step 2
![चरण 2](images/netezza/create_odbc_data_source_step2.png)

जब आपको सफलता स्क्रीन मिले, तो ODBC सही तरीके से कॉन्फ़िगर हो चुका है।

---

अब आप *digna* को ODBC कनेक्शन का उपयोग करने के लिए कॉन्फ़िगर कर सकते हैं, या तो **DSN (Data Source Name)** के साथ या **DSN-less** सेटअप के साथ।

---

### A. DSN-Based Configuration

#### *digna* Configuration

**"Create a Database Connection"** स्क्रीन में निम्नलिखित दें:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 `DSN` को आपके ODBC ड्राइवर कॉन्फ़िगरेशन में परिभाषित नाम से मेल खाना चाहिए।

---

### B. DSN-less Configuration

#### *digna* Configuration

**"Create a Database Connection"** स्क्रीन में निम्नलिखित दें:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```