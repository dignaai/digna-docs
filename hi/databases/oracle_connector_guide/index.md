# Oracle के लिए स्रोत कनेक्टर

यह गाइड बताता है कि *digna* को Oracle DB से कनेक्ट करने के लिए मूल Python कनेक्टर या ODBC ड्राइवर में से किसी एक का उपयोग करके कैसे कॉन्फ़िगर किया जाए।

यह स्क्रीन **"Create a Database Connection"** का संदर्भ देता है।

![डेटाबेस कनेक्शन बनाएं](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `python-oracledb`  
**Supported Authentication:** केवल पासवर्ड-आधारित प्रमाणीकरण

> अन्य प्रमाणीकरण विधियों के लिए, कृपया ODBC ड्राइवर का उपयोग करें।

### *digna* कॉन्फ़िगरेशन (Native Driver)

**"Create a Database Connection"** स्क्रीन में निम्नलिखित जानकारी प्रदान करें:

```
Technology:      Oracle
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1521
Database Name:   Instance name, service name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC ड्राइवर प्रमाणीकरण और कनेक्टिविटी विकल्पों की व्यापक श्रृंखला का समर्थन कर सकता है। यह अनुभाग ड्राइवर **Oracle in OraDB21Home1** का उपयोग करके पासवर्ड-आधारित प्रमाणीकरण पर केंद्रित है।

### 1. ODBC ड्राइवर इंस्टॉल करें

वेंडर के आधिकारिक इंस्टॉलेशन गाइड का पालन करके **Oracle in OraDB21Home1** (या समान) इंस्टॉल करें।

### 2. ODBC डेटा स्रोत कॉन्फ़िगर करें

पासवर्ड-आधारित प्रमाणीकरण का उपयोग करके नया ODBC डेटा स्रोत कॉन्फ़िगर करने के लिए निम्न चरणों का पालन करें:

#### Step 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

नोट:
TNS Service Name को आपके oracle क्लाइंट इंस्टॉलेशन की tnsnames.ora फ़ाइल में कॉन्फ़िगर किया जाना चाहिए। यही वह जगह है जहाँ आप कनेक्शन डिस्क्रिप्टर (host, port, service name) प्रदान करते हैं।

#### Step 2 – Test the connection

**Test Connection** बटन पर क्लिक करें।

![Step 2](images/oracle/create_odbc_data_source_step2.png)

पासवर्ड प्रदान करें और **OK** बटन पर क्लिक करें।

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

अब आप *digna* को ODBC कनेक्शन का उपयोग करने के लिए कॉन्फ़िगर कर सकते हैं, या तो **DSN (Data Source Name)** के साथ या **DSN-less** सेटअप के साथ।

---

### A. DSN-Based Configuration

#### *digna* कॉन्फ़िगरेशन

**"Create a Database Connection"** स्क्रीन में निम्नलिखित प्रदान करें:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> `DSN` आपके ODBC ड्राइवर कॉन्फ़िगरेशन में परिभाषित नाम से मेल खाना चाहिए।

---

### B. DSN-less Configuration

#### *digna* कॉन्फ़िगरेशन

**"Create a Database Connection"** स्क्रीन में निम्नलिखित प्रदान करें:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```