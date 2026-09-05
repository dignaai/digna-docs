# موصل مصدر لـ Databricks - مع Unity Catalog

يصف هذا الدليل كيفية تكوين *digna* للاتصال بـ Databricks باستخدام إما الموصل الأصلي لبايثون أو برنامج تشغيل ODBC.

يشير إلى الشاشة **"Create a Database Connection"**.

![إنشاء اتصال قاعدة بيانات](images/data_source_config_input_mask.png)

---

## الموصل الأصلي لبايثون

**المكتبة:** `databricks-sql-connector`  
**طرق المصادقة المدعومة:** رمز الوصول الشخصي (PAT) فقط

> بالنسبة لطرق المصادقة الأخرى، يرجى استخدام برنامج تشغيل ODBC.

### رمز الوصول الشخصي (PAT)

للمصادقة باستخدام رمز وصول شخصي، راجع الوثائق الرسمية لـ Databricks:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### تكوين *digna* (الموصل الأصلي)

قم بتوفير المعلومات التالية في شاشة **"Create a Database Connection"**:

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

## برنامج تشغيل ODBC

يدعم برنامج تشغيل ODBC مجموعة أوسع من خيارات المصادقة والاتصال. تركز هذه القسم على المصادقة عبر الرموز باستخدام **Simba Spark ODBC Driver**.

### 1. تثبيت برنامج تشغيل ODBC

قم بتثبيت **Simba Spark ODBC Driver** باتباع دليل التثبيت الرسمي للمورد.

### 2. تكوين مصدر بيانات ODBC

اتبع هذه الخطوات لتكوين مصدر بيانات ODBC جديد باستخدام رمز وصول شخصي:

#### الخطوة 1
![الخطوة 1](images/databricks/create_odbc_data_source_step1.png)

#### الخطوة 2
![الخطوة 2](images/databricks/create_odbc_data_source_step2.png)

#### الخطوة 3
![الخطوة 3](images/databricks/create_odbc_data_source_step3.png)

#### الخطوة 4
![الخطوة 4](images/databricks/create_odbc_data_source_step4.png)

#### الخطوة 5 – اختبار الاتصال

انقر على زر **TEST**. يجب أن يبدو الاتصال الناجح كما يلي:

![الخطوة 5](images/databricks/create_odbc_data_source_step5.png)

---

الآن يمكنك تكوين *digna* لاستخدام اتصال ODBC، إما باستخدام **DSN (Data Source Name)** أو إعداد **بدون DSN**.

---

### أ. التكوين باستخدام DSN

#### تكوين *digna*

في شاشة **"Create a Database Connection"**، قم بتوفير ما يلي:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### خصائص ODBC

```
name: "DSN",    value: "*digna*data_databricks"
```

> يجب أن يطابق `DSN` الاسم المعرفة في تكوين برنامج تشغيل ODBC الخاص بك.

---

### ب. التكوين بدون DSN

#### تكوين *digna*

في شاشة **"Create a Database Connection"**، قم بتوفير ما يلي:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### خصائص ODBC

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