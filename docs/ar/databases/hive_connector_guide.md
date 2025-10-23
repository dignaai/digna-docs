---
title: موصل Apache Hive – تكامل قاعدة البيانات | توثيق digna
description: تكوين digna للاتصال بـ Apache Hive باستخدام برنامج PyHive الأصلي أو برنامج تشغيل Cloudera ODBC. يدعم المصادقة المعتمدة على كلمة المرور وإعدادات DSN أو بدون DSN.
image: /assets/logo_square.png
---


# موصل المصدر لـ Hive

يضّح هذا الدليل كيفية تكوين *digna* للاتصال بـ Hive باستخدام إما الموصل الأصلي لـ Python أو برنامج تشغيل ODBC.

يشير إلى الشاشة **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## برنامج التشغيل الأصلي لـ Python

**المكتبة:** `PyHive`  
**طرق المصادقة المدعومة:** المصادقة المعتمدة على كلمة المرور فقط

> ⚠️ بالنسبة لطرق المصادقة الأخرى، يرجى استخدام برنامج تشغيل ODBC.

### تكوين *digna* (برنامج التشغيل الأصلي)

زوّد المعلومات التالية في شاشة **"Create a Database Connection"**:

```
Technology:      Apache Hive
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 10000
Database Name:   Schema that contains the source data
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## برنامج تشغيل ODBC

قد يدعم برنامج تشغيل ODBC مجموعة أوسع من خيارات المصادقة والاتصال. يركّز هذا القسم على المصادقة المعتمدة على كلمة المرور باستخدام برنامج التشغيل **Cloudera ODBC Driver for Apache Hive**.

### 1. تثبيت برنامج تشغيل ODBC

قم بتثبيت **Cloudera ODBC Driver for Apache Hive** (أو ما شابه) باتباع دليل التثبيت الرسمي للمورد.

### 2. تكوين مصدر بيانات ODBC

اتبع الخطوات التالية لتكوين مصدر بيانات ODBC جديد باستخدام المصادقة المعتمدة على كلمة المرور:

#### Step 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Step 2 – اختبار الاتصال

زوّد كلمة المرور واضغط زر **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

بعد نجاح الاختبار، اضغط زر **OK**.

---

الآن يمكنك تكوين *digna* لاستخدام اتصال ODBC، إما باستخدام **DSN (Data Source Name)** أو إعداد **بدون DSN**.

---

### A. تكوين قائم على DSN

#### تكوين *digna*

في شاشة **"Create a Database Connection"**، زوّد ما يلي:

```
Technology:      Apache Hive
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### خصائص ODBC

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{your password in curly braces}"
```

> 🔹 يجب أن يطابق `DSN` الاسم المُعرف في تكوين برنامج تشغيل ODBC الخاص بك.

---

### B. تكوين بدون DSN

#### تكوين *digna*

في شاشة **"Create a Database Connection"**، زوّد ما يلي:

```
Technology:      Apache Hive
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### خصائص ODBC

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 10000"
name: "Schema",     value: "Schema that contains the source data"
name: "UID",        value: "your hive user'
name: "PWD",        value: "your hive password"
name: "AuthMech",   value: "3"
```