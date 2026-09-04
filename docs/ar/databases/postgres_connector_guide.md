---
title: موصل PostgreSQL – تكامل قاعدة البيانات | وثائق digna
description: قم بتكوين digna للاتصال بـ PostgreSQL باستخدام سائق Python `psycopg` أو سائق ODBC الخاص بـ PostgreSQL. يدعم المصادقة المعتمدة على كلمة المرور بإعدادات DSN أو بدون DSN.
image: /assets/logo_square.png
---


# موصل المصدر لـ PostgreSQL

يصف هذا الدليل كيفية تكوين *digna* للاتصال بـ Postgres باستخدام موصل Python الأصلي أو سائق ODBC.

يشير إلى الشاشة **"إنشاء اتصال بقاعدة بيانات"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## السائق الأصلي لـ Python

**المكتبة:** `psycopg`  
**المصادقة المدعومة:** مصادقة معتمدة على كلمة المرور فقط

> لطرق المصادقة الأخرى، يرجى استخدام سائق ODBC.

### تكوين *digna* (السائق الأصلي)

قدّم المعلومات التالية في شاشة **"Create a Database Connection"**:

```
التقنية:         Postgres
عنوان المضيف:    اسم الخادم أو عنوان IP
منفذ المضيف:     رقم المنفذ، مثلاً 5432
اسم قاعدة البيانات: اسم قاعدة البيانات
اسم المخطط:      المخطط الذي يحتوي على البيانات المصدر
اسم المستخدم:    اسم مستخدم قاعدة البيانات
كلمة مرور المستخدم: كلمة المرور للمستخدم
استخدام ODBC:    معطل (افتراضي)
```

---

## سائق ODBC

قد يدعم سائق ODBC نطاقًا أوسع من خيارات المصادقة والاتصال. تركز هذه الفقرة على المصادقة المعتمدة على كلمة المرور باستخدام السائق **PostgreSQL Unicode(x64)**.

### 1. تثبيت سائق ODBC

قم بتثبيت **PostgreSQL Unicode(x64)** (أو ما شابهه) باتباع دليل التثبيت الرسمي الخاص بالمورد.

### 2. تكوين مصدر بيانات ODBC

اتبع هذه الخطوات لتكوين مصدر بيانات ODBC جديد باستخدام مصادقة معتمدة على كلمة المرور:

#### الخطوة 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

ملاحظة: إذا كانت إعدادات قاعدة البيانات تتطلب اختيار "SSLMode" محددًا، فتأكد من استخدامه أيضًا عند تعريف تكوين بدون DSN.

#### الخطوة 2 – اختبار الاتصال

انقر زر **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

يمكنك الآن تكوين *digna* لاستخدام اتصال ODBC، إما بإعداد **DSN (اسم مصدر البيانات)** أو بإعداد **بدون DSN**.

---

### أ. التكوين المعتمد على DSN

#### تكوين *digna*

في شاشة **"Create a Database Connection"**، قدّم ما يلي:

```
التقنية:         PostgreSQL
اسم قاعدة البيانات: قاعدة البيانات التي تحتوي على المخطط المصدر
اسم المخطط:      المخطط الذي يحتوي على البيانات المصدر
استخدام ODBC:    ممكّن
```

#### خصائص ODBC

```
name: "DSN",    value: "PostgreSQL35W"
```

> يجب أن يتطابق `DSN` مع الاسم المُعرف في تكوين سائق ODBC لديك.

---

### ب. التكوين بدون DSN

#### تكوين *digna*

في شاشة **"Create a Database Connection"**، قدّم ما يلي:

```
التقنية:         PostgreSQL
اسم قاعدة البيانات: المخطط الذي يحتوي على البيانات المصدر (نفس اسم المخطط)
اسم المخطط:      المخطط الذي يحتوي على البيانات المصدر
استخدام ODBC:    ممكّن
```

#### خصائص ODBC

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user"
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```