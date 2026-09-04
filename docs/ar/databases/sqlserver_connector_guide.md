---
title: موصل MS SQL Server – تكامل قاعدة البيانات | وثائق digna
description: تكوين digna للاتصال بـ Microsoft SQL Server باستخدام برنامج التشغيل pymssql الخاص بـ Python أو برنامج تشغيل SQL Server عبر ODBC. يدعم المصادقة عن طريق كلمة المرور مع إعدادات DSN أو بدون DSN.
image: /assets/logo_square.png
---


# موصل المصدر لـ MS SQL Server

تصف هذه الإرشادات كيفية تكوين *digna* للاتصال بـ SQL Server سواءً باستخدام الموصل الأصلي لـ Python أو عبر برنامج تشغيل ODBC.

تشير هذه الإرشادات إلى الشاشة **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## الموصل الأصلي لـ Python

**المكتبة:** `pymssql`  
**طرق المصادقة المدعومة:** مصادقة باستخدام كلمة المرور فقط

> لطرق مصادقة أخرى، يرجى استخدام برنامج تشغيل ODBC.

### تكوين *digna* (الموصل الأصلي)

زوّد المعلومات التالية في شاشة **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    اسم الخادم أو عنوان IP
Host Port:       رقم المنفذ، مثلاً 1433
Database Name:   اسم قاعدة البيانات
Schema Name:     المخطط الذي يحتوي على بيانات المصدر
User Name:       اسم مستخدم قاعدة البيانات
User Password:   كلمة مرور المستخدم
Use ODBC:        Disabled (default)
```

---

## برنامج تشغيل ODBC

قد يدعم برنامج تشغيل ODBC نطاقًا أوسع من خيارات المصادقة والاتصال. تركز هذه الفقرة على المصادقة باستخدام كلمة المرور عبر برنامج التشغيل **SQL Server**.

### 1. تثبيت برنامج تشغيل ODBC

ثبت برنامج التشغيل **SQL Server** (أو ما يماثله) باتباع دليل التثبيت الرسمي للبائع.

### 2. تكوين مصدر بيانات ODBC

اتبع هذه الخطوات لتكوين مصدر بيانات ODBC جديد باستخدام المصادقة عبر كلمة المرور:

#### الخطوة 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

انقر زر **Next >**.

#### الخطوة 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

اختر طريقة المصادقة (مثل اسم المستخدم وكلمة المرور)
وقم بتوفير البيانات المطلوبة.

انقر زر **Next >**.

#### الخطوة 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

اختر إعدادات التوافق مع ANSI ثم انقر زر **Next >**.

#### الخطوة 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

يمكنك ترك الإعدادات الافتراضية أو اختيار خيارات التسجيل حسب الحاجة 
ثم انقر زر **Finish**. 

#### الخطوة 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

الآن انقر زر ** Test datasource **.

#### الخطوة 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

عند ظهور شاشة النجاح، يكون ODBC مُكوَّنًا بشكل صحيح.

---

الآن يمكنك تكوين *digna* لاستخدام اتصال ODBC، إما عبر **DSN (Data Source Name)** أو إعداد **بدون DSN**.

---

### A. تكوين قائم على DSN

#### تكوين *digna*

في شاشة **"Create a Database Connection"**، قم بتوفير ما يلي:

```
Technology:      MS SQL Server
Database Name:   قاعدة البيانات التي تحتوي على المخطط المصدر
Schema Name:     المخطط الذي يحتوي على بيانات المصدر
Use ODBC:        Enabled
```

#### خصائص ODBC

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> يجب أن يتطابق `DSN` مع الاسم المُعرف في تكوين برنامج تشغيل ODBC الخاص بك.

---

### B. تكوين بدون DSN

#### تكوين *digna*

في شاشة **"Create a Database Connection"**، قم بتوفير ما يلي:

```
Technology:      MS SQL Server
Database Name:   المخطط الذي يحتوي على بيانات المصدر (نفس Schema Name)
Schema Name:     المخطط الذي يحتوي على بيانات المصدر
Use ODBC:        Enabled
```

#### خصائص ODBC

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```