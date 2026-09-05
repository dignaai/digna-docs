# Databricks के लिए Source Connector - Unity Catalog के बिना

यह गाइड बताता है कि *digna* को Databricks से कनेक्ट करने के लिए कैसे कॉन्फ़िगर किया जाए — या तो नैटिव Python कनेक्टर का उपयोग करके या ODBC ड्राइवर के माध्यम से।

यह स्क्रीन **"Create a Database Connection"** का संदर्भ देता है।

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> अन्य प्रमाणीकरण विधियों के लिए, कृपया ODBC ड्राइवर का उपयोग करें।

### Personal Access Token (PAT)

Personal Access Token का उपयोग करके प्रमाणीकृत करने के लिए, आधिकारिक Databricks डॉक्स देखें:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* कॉन्फ़िगरेशन (नैटिव ड्राइवर)

**"Create a Database Connection"** स्क्रीन में निम्न जानकारी प्रदान करें:

```
Technology:      Databricks (Legacy)
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC ड्राइवर अधिक व्यापक प्रमाणीकरण और कनेक्टिविटी विकल्पों का समर्थन करता है। यह अनुभाग टोकन-आधारित प्रमाणीकरण पर केंद्रित है, विशेष रूप से **Simba Spark ODBC Driver** का उपयोग करते हुए।

### 1. ODBC ड्राइवर इंस्टॉल करें

वेंडर के आधिकारिक इंस्टॉलेशन गाइड का पालन करके **Simba Spark ODBC Driver** इंस्टॉल करें।

### 2. ODBC डेटा सोर्स कॉन्फ़िगर करें

Personal Access Token का उपयोग करके नया ODBC डेटा सोर्स कॉन्फ़िगर करने के लिए निम्न चरणों का पालन करें:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – कनेक्शन टेस्ट करें

**TEST** बटन पर क्लिक करें। सफल कनेक्शन इस तरह दिखना चाहिए:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

अब आप *digna* को ODBC कनेक्शन का उपयोग करने के लिए कॉन्फ़िगर कर सकते हैं, या तो **DSN (Data Source Name)** के साथ या **DSN-less** सेटअप के साथ।

---

### A. DSN-Based Configuration

#### *digna* कॉन्फ़िगरेशन

**"Create a Database Connection"** स्क्रीन में निम्न प्रदान करें:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> `DSN` उसी नाम से मेल खाना चाहिए जो आपने अपने ODBC ड्राइवर कॉन्फ़िगरेशन में परिभाषित किया है।

---

### B. DSN-less Configuration

#### *digna* कॉन्फ़िगरेशन

**"Create a Database Connection"** स्क्रीन में निम्न प्रदान करें:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name = "Driver",          value = "{Simba Spark ODBC Driver}"
name = "Host",            value = "xxxxxxxxxxxxxxxxxxx.databricks.com"
name = "Port",            value = "443"
name = "HTTPPath",        value = "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
name = "SSL",             value = "1"
name = "ThriftTransport", value = "2"
name = "AuthMech",        value = "3"
name = "UID",             value = "token"
name = "PWD",             value = "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```