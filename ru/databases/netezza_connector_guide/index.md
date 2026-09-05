# Коннектор источника для Netezza

В этом руководстве описывается, как настроить *digna* для подключения к Netezza с помощью ODBC‑драйвера.

Руководство относится к экрану **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Драйвер ODBC

Драйвер ODBC может поддерживать различные варианты аутентификации и параметров подключения. В этом разделе рассматривается аутентификация по паролю с использованием драйвера **NetezzaSQL**.

### 1. Установка драйвера ODBC

Установите драйвер **NetezzaSQL** (или аналогичный) в соответствии с официальным руководством поставщика.

### 2. Настройка источника данных ODBC

Выполните следующие шаги, чтобы настроить новый источник данных ODBC с аутентификацией по паролю:

#### Шаг 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

В зависимости от вашего драйвера Netezza, требований к установке и безопасности, вам может потребоваться также указать данные на вкладках **Advanced DSN Options**, **SSL DSN Options** или **Driver Options**. Для самой простой настройки достаточно заполнить данные в **DSN Options**.

Нажмите кнопку **Test Connection**.

#### Шаг 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Когда вы увидите экран успешного подключения, ODBC настроен корректно.

---

Теперь вы можете настроить *digna* для использования ODBC‑соединения — либо с **DSN (Data Source Name)**, либо в конфигурации **DSN-less**.

---

### A. Конфигурация с использованием DSN

#### Конфигурация *digna*

В экране **"Create a Database Connection"** укажите следующее:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Свойства ODBC

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> `DSN` должен совпадать с именем, указанным в конфигурации вашего ODBC‑драйвера.

---

### B. Конфигурация без DSN (DSN-less)

#### Конфигурация *digna*

В экране **"Create a Database Connection"** укажите следующее:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Свойства ODBC

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```