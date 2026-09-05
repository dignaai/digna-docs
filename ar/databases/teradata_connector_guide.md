# موصل المصدر لـ Teradata

يوضح هذا الدليل كيفية تكوين *digna* للاتصال بـ Teradata باستخدام إما الموصل الأصلي لـ Python أو برنامج تشغيل ODBC.

يُشار إلى الشاشة **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## برنامج التشغيل الأصلي لـ Python

**المكتبة:** `teradatasql`  
**المصادقة المدعومة:** المصادقة بواسطة كلمة المرور فقط

> لأساليب مصادقة أخرى، يرجى استخدام برنامج تشغيل ODBC.

### تهيئة *digna* (المشغل الأصلي)

قدّم المعلومات التالية في شاشة **"Create a Database Connection"**:

```
Technology:      Teradata
Host Address:    اسم الخادم أو عنوان IP
Host Port:       رقم المنفذ، مثلاً 1025
Database Name:   اسم قاعدة البيانات
Schema Name:     اسم المخطط
User Name:       اسم مستخدم قاعدة البيانات
User Password:   كلمة المرور للمستخدم
Use ODBC:        Disabled (default)
```

---

## برنامج تشغيل ODBC

قد يدعم برنامج تشغيل ODBC مجموعة أوسع من خيارات المصادقة والاتصال. يركّز هذا القسم على المصادقة بواسطة كلمة المرور باستخدام برنامج التشغيل **Teradata Database ODBC Driver 20.00**.

### 1. تثبيت برنامج تشغيل ODBC

قم بتثبيت برنامج التشغيل **Teradata Database ODBC Driver 20.00** (أو ما شابه) باتباع دليل التثبيت الرسمي الخاص بالمورد.

### 2. تكوين مصدر بيانات ODBC

اتبع هذه الخطوات لتكوين مصدر بيانات ODBC جديد باستخدام المصادقة بواسطة كلمة المرور:

#### Step 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

انقر على زر **Test**.

#### Step 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

قدّم اسم المستخدم وكلمة المرور.

انقر على زر **OK**.  
عند ظهور شاشة النجاح، يكون ODBC مكوّنًا بشكل صحيح.

---

الآن يمكنك تكوين *digna* لاستخدام اتصال ODBC، إما باستخدام **DSN (Data Source Name)** أو إعداد **بدون DSN**.

---

### A. تكوين يعتمد على DSN

#### تهيئة *digna*

في شاشة **"Create a Database Connection"**، قدّم ما يلي:

```
Technology:      Teradata
Database Name:   قاعدة البيانات التي تحتوي على المخطط المصدر
Schema Name:     المخطط الذي يحتوي على البيانات المصدر
Use ODBC:        Enabled
```

#### خصائص ODBC

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> يجب أن تتطابق قيمة `DSN` مع الاسم المعرف في تكوين برنامج تشغيل ODBC الخاص بك.

---

### B. تكوين بدون DSN

#### تهيئة *digna*

في شاشة **"Create a Database Connection"**، قدّم ما يلي:

```
Technology:      Teradata
Database Name:   المخطط الذي يحتوي على البيانات المصدر (نفس اسم Schema Name)
Schema Name:     المخطط الذي يحتوي على البيانات المصدر
Use ODBC:        Enabled
```

#### خصائص ODBC

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```