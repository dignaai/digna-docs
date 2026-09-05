# Databricks के लिए स्रोत कनेक्टर - Unity Catalog के साथ

यह मार्गदर्शिका बताती है कि *digna* को Databricks से कैसे कनेक्ट किया जाए, या तो नатив Python कनेक्टर या ODBC ड्राइवर का उपयोग करके।

यह स्क्रीन **"Create a Database Connection"** को संदर्भित करता है।

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> अन्य प्रमाणीकरण विधियों के लिए, कृपया ODBC ड्राइवर का उपयोग करें।

### Personal Access Token (PAT)

Personal Access Token का उपयोग करके प्रमाणीकरण करने के लिए, आधिकारिक Databricks दस्तावेज़ देखें:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

**"Create a Database Connection"** स्क्रीन में निम्न जानकारी प्रदान करें:

```
Technology:      Databricks
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Name of the catalog to use. 
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC ड्राइवर व्यापक प्रमाणीकरण और कनेक्टिविटी विकल्पों का समर्थन करता है। यह अनुभाग Simba Spark ODBC Driver का उपयोग करके token-आधारित प्रमाणीकरण पर केन्द्रित है।

### 1. Install the ODBC Driver

Simba Spark ODBC Driver को वेंडर के आधिकारिक इंस्टॉलेशन गाइड का पालन करके इंस्टॉल करें।

### 2. Configure the ODBC Data Source

Personal Access Token का उपयोग करके नया ODBC डेटा स्रोत कॉन्फ़िगर करने के लिए निम्न चरणों का पालन करें:

#### चरण 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### चरण 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### चरण 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### चरण 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### चरण 5 – कनेक्शन का परीक्षण

**TEST** बटन पर क्लिक करें। सफल कनेक्शन इस तरह दिखना चाहिए:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

अब आप *digna* को ODBC कनेक्शन का उपयोग करने के लिए कॉन्फ़िगर कर सकते हैं, या तो **DSN (Data Source Name)** के साथ या **DSN-less** सेटअप के साथ।

---

### A. DSN-आधारित कॉन्फ़िगरेशन

#### *digna* Configuration

**"Create a Database Connection"** स्क्रीन में निम्नलिखित प्रदान करें:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> `DSN` आपके ODBC ड्राइवर कॉन्फ़िगरेशन में परिभाषित नाम से मेल खाना चाहिए।

---

### B. DSN-less कॉन्फ़िगरेशन

#### *digna* Configuration

**"Create a Database Connection"** स्क्रीन में निम्नलिखित प्रदान करें:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
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