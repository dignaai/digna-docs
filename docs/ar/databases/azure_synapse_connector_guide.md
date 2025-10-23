---
title: موصل Azure Synapse – تكامل قاعدة البيانات | توثيق digna
description: قم بتكوين digna للاتصال بـ Azure Synapse Analytics باستخدام إما الموصل الأصلي لـ Python أو برنامج تشغيل ODBC. يدعم كلًا من SQL pools بدون خادم والمخصصة.
image: /assets/logo_square.png
---


# موصل المصدر لـ Azure Synapse Analytics

يصف هذا الدليل كيفية تكوين *digna* للاتصال بـ Azure Synapse Analytics باستخدام إما الموصل الأصلي لـ Python أو برنامج تشغيل ODBC.
يدعم كلًا من SQL pools بدون خادم والمخصصة.

يشير هذا إلى الشاشة **"إنشاء اتصال قاعدة بيانات"**.

![إنشاء اتصال قاعدة بيانات](images/data_source_config_input_mask.png)

---

## الموصل الأصلي لـ Python

**المكتبة:** `pymssql`  
**أسلوب المصادقة المدعوم:** المصادقة باستخدام كلمة المرور فقط

> ⚠️ لأساليب المصادقة الأخرى، يرجى استخدام برنامج تشغيل ODBC.

### تكوين *digna* (الموصل الأصلي)

زوّد المعلومات التالية في شاشة **"إنشاء اتصال قاعدة بيانات"**:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## برنامج تشغيل ODBC

قد يدعم برنامج تشغيل ODBC مجموعة أوسع من خيارات المصادقة والاتصال. يركز هذا القسم على المصادقة باستخدام كلمة المرور عبر برنامج التشغيل **ODBC Driver 18 for SQL Server**.

### 1. تثبيت برنامج تشغيل ODBC

قم بتثبيت برنامج التشغيل **ODBC Driver 18 for SQL Server** (أو ما يماثله) باتباع دليل التثبيت الرسمي للمورد.

### 2. تكوين مصدر بيانات ODBC

اتبع الخطوات التالية لتكوين مصدر بيانات ODBC جديد باستخدام المصادقة عبر كلمة المرور:

#### الخطوة 1
![الخطوة 1](images/azure_synapse/create_odbc_data_source_step1.png)

املأ حقل "Server".
استخدم اسم مساحة عمل Synapse وقم بتمديده بـ ".sql.azuresynapse.net".  
**تنبيه**، إذا أردت الاتصال باستخدام SQL pool بدون خادم، تأكد من تضمين "-ondemand" كما هو موضح في لقطة الشاشة أدناه.

انقر على زر **Next >**.

#### الخطوة 2
![الخطوة 2](images/azure_synapse/create_odbc_data_source_step2.png)

اختر طريقة المصادقة (مثل اسم المستخدم وكلمة المرور)
وقم بتعبئة البيانات المطلوبة.

انقر على زر **Next >**.

#### الخطوة 3
![الخطوة 3](images/azure_synapse/create_odbc_data_source_step3.png)

اختر إعدادات متوافقة مع ANSI ثم انقر على زر **Next >**.

#### الخطوة 4
![الخطوة 4](images/azure_synapse/create_odbc_data_source_step4.png)

يمكنك ترك الإعدادات الافتراضية أو اختيار الخيارات حسب الحاجة
ثم انقر على زر **Finish**. 

#### الخطوة 5
![الخطوة 5](images/azure_synapse/create_odbc_data_source_step5.png)

الآن انقر على زر **Test datasource**.

#### الخطوة 6
![الخطوة 1](images/azure_synapse/create_odbc_data_source_step6.png)

عندما تتلقى شاشة النجاح، فإن ODBC مُكوّن بشكل صحيح.

---

الآن يمكنك تكوين *digna* لاستخدام اتصال ODBC، إما باستخدام **DSN (Data Source Name)** أو إعداد **بدون DSN**.

---

### A. التكوين القائم على DSN

#### تكوين *digna*

في شاشة **"إنشاء اتصال قاعدة بيانات"**، قدّم ما يلي:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### خصائص ODBC

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 يجب أن يتطابق `DSN` مع الاسم المحدد في تكوين برنامج تشغيل ODBC الخاص بك.

---

### B. التكوين بدون DSN

#### تكوين *digna*

في شاشة **"إنشاء اتصال قاعدة بيانات"**، قدّم ما يلي:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### خصائص ODBC

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**ملاحظة** بخصوص الخاصية SERVER:  
استخدم اسم مساحة عمل Synapse وقم بتمديده بـ ".sql.azuresynapse.net". إذا كنت تريد الاتصال باستخدام SQL pool بدون خادم، فتأكد من تضمين "-ondemand" كما هو موضح في لقطة الشاشة أدناه.