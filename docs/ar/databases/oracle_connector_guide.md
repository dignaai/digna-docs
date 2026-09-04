---
title: موصل Oracle – تكامل قواعد البيانات | توثيق digna
description: قم بتكوين digna للاتصال بـ Oracle باستخدام برنامج التشغيل python-oracledb أو برنامج تشغيل Oracle ODBC. يدعم المصادقة المعتمدة على كلمة المرور سواء عبر إعدادات DSN أو بدون DSN.
image: /assets/logo_square.png
---


# Source Connector for Oracle

يصف هذا الدليل كيفية تكوين *digna* للاتصال بقاعدة بيانات Oracle باستخدام либо الموصل الأصلي الخاص بـ Python أو برنامج تشغيل ODBC.

يشير هذا الدليل إلى الشاشة **"Create a Database Connection"**.

![إنشاء اتصال بقاعدة بيانات](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `python-oracledb`  
**Supported Authentication:** Password-based authentication only

> لأساليب المصادقة الأخرى، الرجاء استخدام برنامج تشغيل ODBC.

### تكوين *digna* (برنامج التشغيل الأصلي)

قدّم المعلومات التالية في شاشة **"Create a Database Connection"**:

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

قد يدعم برنامج تشغيل ODBC مجموعة أوسع من خيارات المصادقة والاتصال. تركز هذه الفقرة على المصادقة المعتمدة على كلمة المرور باستخدام برنامج التشغيل **Oracle in OraDB21Home1**.

### 1. Install the ODBC Driver

قم بتثبيت **Oracle in OraDB21Home1** (أو ما شابهه) باتباع دليل التثبيت الرسمي للمورد.

### 2. Configure the ODBC Data Source

اتبع الخطوات التالية لتكوين مصدر بيانات ODBC جديد باستخدام المصادقة المعتمدة على كلمة المرور:

#### Step 1
![الخطوة 1](images/oracle/create_odbc_data_source_step1.png)

ملاحظة:
يجب تكوين اسم خدمة TNS في ملف tnsnames.ora الخاص بتثبيت عميل Oracle لديك. هنا تقوم بتقديم وصف الاتصال (المضيف، المنفذ، اسم الخدمة).

#### Step 2 – Test the connection

انقر زر **Test Connection**.

![الخطوة 2](images/oracle/create_odbc_data_source_step2.png)

أدخل كلمة المرور ثم انقر زر **OK**.

![الخطوة 2](images/oracle/create_odbc_data_source_step3.png)

---

الآن يمكنك تكوين *digna* لاستخدام اتصال ODBC، إما عبر **DSN (Data Source Name)** أو عبر إعداد **بدون DSN**.

---

### A. DSN-Based Configuration

#### تكوين *digna*

في شاشة **"Create a Database Connection"**، قدّم ما يلي:

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

> يجب أن يتطابق `DSN` مع الاسم المحدد في تكوين برنامج تشغيل ODBC الخاص بك.

---

### B. DSN-less Configuration

#### تكوين *digna*

في شاشة **"Create a Database Connection"**، قدّم ما يلي:

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