---
title: موصل Netezza – تكامل قاعدة البيانات | توثيق digna
description: قم بتكوين digna للاتصال بـ Netezza باستخدام برنامج تشغيل ODBC NetezzaSQL. يدعم المصادقة بكلمة المرور عبر إعدادات DSN أو إعدادات بدون DSN لمرونة الاتصال.
image: /assets/logo_square.png
---


# موصل المصدر لـ Netezza

تشرح هذه الإرشادات كيفية تكوين *digna* للاتصال بـ Netezza باستخدام برنامج تشغيل ODBC.

تشير إلى الشاشة **"Create a Database Connection"**.

![إنشاء اتصال بقاعدة البيانات](images/data_source_config_input_mask.png)

---

## برنامج تشغيل ODBC

قد يدعم برنامج تشغيل ODBC مجموعة من خيارات المصادقة والاتصال. يركز هذا القسم على المصادقة بكلمة المرور باستخدام برنامج التشغيل **NetezzaSQL**.

### 1. تثبيت برنامج تشغيل ODBC

قم بتثبيت برنامج التشغيل **NetezzaSQL** (أو ما شابهه) باتباع دليل التثبيت الرسمي الخاص بالبائع.

### 2. تكوين مصدر بيانات ODBC

اتبع هذه الخطوات لتكوين مصدر بيانات ODBC جديد باستخدام المصادقة بكلمة المرور:

#### الخطوة 1
![الخطوة 1](images/netezza/create_odbc_data_source_step1.png)

اعتمادًا على برنامج تشغيل Netezza ومتطلبات الإعداد والأمان، قد تحتاج أيضًا إلى إدخال بيانات في علامات التبويب **Advanced DSN Options** أو **SSL DSN Options** أو **Driver Options**. لأبسط إعداد يكفي إدخال البيانات في **DSN Options**.

انقر على زر **Test Connection**.

#### الخطوة 2
![الخطوة 2](images/netezza/create_odbc_data_source_step2.png)

عند ظهور شاشة النجاح، يكون ODBC قد تم تكوينه بشكل صحيح.

---

الآن يمكنك تكوين *digna* لاستخدام اتصال ODBC، إما عبر **DSN (Data Source Name)** أو عبر إعداد **بدون DSN (DSN-less)**.

---

### A. تكوين قائم على DSN

#### تكوين *digna*

في شاشة **"Create a Database Connection"**، قم بتوفير ما يلي:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### خصائص ODBC

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. تكوين بدون DSN (DSN-less)

#### تكوين *digna*

في شاشة **"Create a Database Connection"**، قم بتوفير ما يلي:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### خصائص ODBC

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```