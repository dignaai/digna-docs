---
title: موصل Snowflake – تكامل قاعدة البيانات | توثيق digna
description: قم بتكوين digna للاتصال بـ Snowflake باستخدام الموصل الأصلي الخاص بـ Python أو برنامج تشغيل ODBC الخاص بـ Snowflake. يدعم المصادقة بناءً على كلمة المرور بإعدادات DSN أو بدون DSN.
image: /assets/logo_square.png
---


# Source Connector for Snowflake

يصف هذا الدليل كيفية تكوين *digna* للاتصال بـ Snowflake باستخدام الموصل الأصلي لـ Python أو باستخدام برنامج تشغيل ODBC.

يشير إلى الشاشة **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `snowflake-connector-python`  
**Supported Authentication:** المصادقة بناءً على كلمة المرور فقط

> ⚠️ لطرق المصادقة الأخرى، يرجى استخدام برنامج تشغيل ODBC.

### *digna* Configuration (Native Driver)

قدّم المعلومات التالية في شاشة **"Create a Database Connection"**:

```
Technology:      Snowflake
Host Address:    اسم حساب Snowflake
Host Port:       غير مطلوب
Database Name:   قاعدة البيانات التي تحتوي على المخطط المصدر
Schema Name:     المخطط الذي يحتوي على البيانات المصدر
User Name:       اسم المستخدم والمستودع بالتنسيق "user<@>warehouse"
User Password:   كلمة المرور للمستخدم
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

قد يدعم برنامج تشغيل ODBC مجموعة أوسع من خيارات المصادقة والاتصال. تركز هذه الفقرة على المصادقة بناءً على كلمة المرور باستخدام **SnowflakeDSIIDriver**.

### 1. Install the ODBC Driver

قم بتثبيت **SnowflakeDSIIDriver** باتباع دليل التثبيت الرسمي الخاص بالبائع.

### 2. Configure the ODBC Data Source

اتبع هذه الخطوات لتكوين مصدر بيانات ODBC جديد باستخدام المصادقة بناءً على كلمة المرور:

#### Step 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

ملاحظات:
- إذا لم تُدخل قيمًا لـ Database و Schema و Warehouse، فستحتاج إلى تقديمها كخصائص ODBC أثناء تكوين مصدر بيانات *digna*.
- قيمة "Server" تتكون من اسم حساب Snowflake الخاص بك متبوعًا بـ ".snowflakecomputing.com"

#### Step 2 – Test the connection

انقر على زر **TEST**. يجب أن تبدو نتيجة الاتصال الناجح كما يلي:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

الآن يمكنك تكوين *digna* لاستخدام اتصال ODBC، إما باستخدام **DSN (Data Source Name)** أو إعداد **بدون DSN**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

في شاشة **"Create a Database Connection"**، قدّم ما يلي:

```
Technology:      Snowflake
Database Name:   قاعدة البيانات التي تحتوي على المخطط المصدر
Schema Name:     المخطط الذي يحتوي على البيانات المصدر
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionally:
name: "Database",       value: "Database that contains the source schema"
name: "Schema",         value: "Schema that contains the source data"
name: "Warehouse",      value: "Warehouse to use for the execution of the SQLs"
```

> 🔹 يجب أن يتطابق `DSN` مع الاسم المُعرف في تكوين برنامج تشغيل ODBC لديك.

---

### B. DSN-less Configuration

#### *digna* Configuration

في شاشة **"Create a Database Connection"**، قدّم ما يلي:

```
Technology:      Snowflake
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Database that contains the source schema"
name: "Schema",     value: "Schema that contains the source data"
name: "Warehouse",  value: "Warehouse to use for the execution of the SQLs"
```