---
title: Databricks Connector (Legacy, without Unity Catalog) | توثيق digna
description: قم بتكوين digna للاتصال بـ Databricks بدون Unity Catalog باستخدام الموصل الأصلي لـ Python أو برنامج تشغيل Simba Spark ODBC. يدعم المصادقة عبر الرموز وإمكانيات اتصال مرنة.
image: /assets/logo_square.png
---

# موصل المصدر لـ Databricks - بدون Unity Catalog

يوضح هذا الدليل كيفية تكوين *digna* للاتصال بـ Databricks باستخدام إما الموصل الأصلي للـ Python أو برنامج تشغيل ODBC.

يشير هذا الدليل إلى الشاشة **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## برنامج تشغيل Python الأصلي

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> لطرق المصادقة الأخرى، يرجى استخدام برنامج تشغيل ODBC.

### Personal Access Token (PAT)

للمصادقة باستخدام رمز الوصول الشخصي، راجع توثيق Databricks الرسمي:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### تكوين *digna* (برنامج التشغيل الأصلي)

قدم المعلومات التالية في شاشة **"Create a Database Connection"**:

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

## برنامج تشغيل ODBC

يدعم برنامج تشغيل ODBC مجموعة أوسع من خيارات المصادقة والاتصال. يركز هذا القسم على المصادقة عبر الرموز باستخدام **Simba Spark ODBC Driver**.

### 1. تثبيت برنامج تشغيل ODBC

قم بتثبيت **Simba Spark ODBC Driver** باتباع دليل التثبيت الرسمي من البائع.

### 2. تكوين مصدر بيانات ODBC

اتبع هذه الخطوات لتكوين مصدر بيانات ODBC جديد باستخدام رمز وصول شخصي:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test the connection

انقر على الزر **TEST**. يجب أن تبدو عملية الاتصال الناجحة كما يلي:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

الآن يمكنك تكوين *digna* لاستخدام اتصال ODBC، إما باستخدام **DSN (Data Source Name)** أو إعداد **بدون DSN**.

---

### A. التهيئة باستخدام DSN

#### تكوين *digna*

في شاشة **"Create a Database Connection"**، قدّم ما يلي:

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

> يجب أن يتطابق `DSN` مع الاسم المحدد في تكوين برنامج تشغيل ODBC الخاص بك.

---

### B. تهيئة بدون DSN

#### تكوين *digna*

في شاشة **"Create a Database Connection"**، قدّم ما يلي:

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