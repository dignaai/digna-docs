---
title: Azure Synapse Connector – Database Integration | digna Documentation
description: Configure digna to connect to Azure Synapse Analytics using either the native Python driver or the ODBC driver. Supports both serverless and dedicated SQL pools.
image: /assets/logo_square.png
---


# Source Connector for Azure Synapse Analytics

Bu kılavuz, *digna*'yı Azure Synapse Analytics'e ya yerel Python bağlayıcısıyla ya da ODBC sürücüsüyle nasıl bağlayacağınızı açıklar.
Hem sunucusuz (serverless) hem de dedicated SQL pool'ları destekler.

Bu belge **"Create a Database Connection"** ekranına atıfta bulunur.

![Veritabanı bağlantısı oluştur](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Kütüphane:** `pymssql`  
**Desteklenen Kimlik Doğrulama:** Yalnızca parola tabanlı kimlik doğrulama

> ⚠️ Diğer kimlik doğrulama yöntemleri için lütfen ODBC sürücüsünü kullanın.

### *digna* Yapılandırması (Yerel Sürücü)

**"Create a Database Connection"** ekranında aşağıdaki bilgileri sağlayın:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port numarası, örn. 1433
Database Name:   Veritabanı adı
Schema Name:     Kaynak veriyi içeren şema
User Name:       Veritabanı kullanıcı adı
User Password:   Kullanıcının parolası
Use ODBC:        Devre dışı (varsayılan)
```

---

## ODBC Driver

ODBC sürücüsü, daha geniş bir kimlik doğrulama ve bağlantı seçenekleri yelpazesini destekleyebilir. Bu bölüm, **ODBC Driver 18 for SQL Server** sürücüsünü kullanarak parola tabanlı kimlik doğrulama üzerine odaklanır.

### 1. ODBC Sürücüsünü Yükleyin

Tedarikçinin resmi kurulum kılavuzunu izleyerek **ODBC Driver 18 for SQL Server** (veya benzeri) sürücüsünü yükleyin.

### 2. ODBC Veri Kaynağını Yapılandırın

Parola tabanlı kimlik doğrulamayı kullanarak yeni bir ODBC veri kaynağı yapılandırmak için şu adımları izleyin:

#### Adım 1
![Adım 1](images/azure_synapse/create_odbc_data_source_step1.png)

"Server" alanını doldurun.
Synapse çalışma alanı adını kullanın ve sonuna ".sql.azuresynapse.net" ekleyin.  
**Dikkat**, sunucusuz (serverless) bir SQL havuzuna bağlanmak istiyorsanız, aşağıdaki ekran görüntüsünde gösterildiği gibi "-ondemand" eklediğinizden emin olun.

**Next >** düğmesine tıklayın.

#### Adım 2
![Adım 2](images/azure_synapse/create_odbc_data_source_step2.png)

Kimlik doğrulama yöntemini (ör. kullanıcı adı ve parola) seçin
ve gerekli bilgileri sağlayın.

**Next >** düğmesine tıklayın.

#### Adım 3
![Adım 3](images/azure_synapse/create_odbc_data_source_step3.png)

ANSI uyumlu ayarları seçin, ardından **Next >** düğmesine tıklayın.

#### Adım 4
![Adım 4](images/azure_synapse/create_odbc_data_source_step4.png)

Varsayılan ayarları bırakabilir veya gerektiği şekilde seçenekleri belirleyip
**Finish** düğmesine tıklayabilirsiniz. 

#### Adım 5
![Adım 5](images/azure_synapse/create_odbc_data_source_step5.png)

Şimdi ** Test datasource ** düğmesine tıklayın.

#### Adım 6
![Adım 1](images/azure_synapse/create_odbc_data_source_step6.png)

Başarılı ekranını aldığınızda, ODBC düzgün şekilde yapılandırılmış demektir.

---

Artık *digna*'yı ODBC bağlantısını kullanacak şekilde, ya **DSN (Data Source Name)** ile ya da **DSN-less** bir kurulumla yapılandırabilirsiniz.

---

### A. DSN Tabanlı Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri sağlayın:

```
Technology:      MS SQL Server
Database Name:   Kaynak şemayı içeren veritabanı
Schema Name:     Kaynak veriyi içeren şema
Use ODBC:        Etkin
```

#### ODBC Özellikleri

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "veritabanı kullanıcı adınız"
name: "PWD",        value: "veritabanı parolanız"
name: "DATABASE",   value: "kaynak veri şemasını içeren veritabanının adı"
```

> 🔹 `DSN`, ODBC sürücü yapılandırmanızda tanımlı olan ad ile eşleşmelidir.

---

### B. DSN-less Yapılandırma

#### *digna* Yapılandırması

**"Create a Database Connection"** ekranında aşağıdakileri sağlayın:

```
Technology:      MS SQL Server
Database Name:   Kaynak veriyi içeren şema (Schema Name ile aynı)
Schema Name:     Kaynak veriyi içeren şema
Use ODBC:        Etkin
```

#### ODBC Özellikleri

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "veritabanı kullanıcı adınız"
name: "PWD",        value: "veritabanı parolanız"
name: "DATABASE",   value: "kaynak veri şemasını içeren veritabanının adı"
```

**Not**: SERVER özelliği ile ilgili açıklama:  
Synapse çalışma alanı adını kullanın ve sonuna ".sql.azuresynapse.net" ekleyin. Sunucusuz (serverless) bir SQL havuzuna bağlanmak istiyorsanız, aşağıdaki ekran görüntüsünde gösterildiği gibi "-ondemand" eklediğinizden emin olun.