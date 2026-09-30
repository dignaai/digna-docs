# Hive के लिए सोर्स कनेक्टर

यह गाइड बताता है कि *digna* को **DSN-less** कनेक्शन स्ट्रिंग का उपयोग करके **ODBC** के माध्यम से
Apache Hive से कनेक्ट करने के लिए कैसे कॉन्फ़िगर करें।

सेटअप का *digna* पक्ष हर तकनीक के लिए समान है — कनेक्शन कहाँ बनाए जाते हैं, प्रॉपर्टी मान कैसे
एन्क्रिप्ट होते हैं, कनेक्शन का परीक्षण कैसे होता है और प्रोफ़ाइलिंग मोड का क्या अर्थ है। इसका वर्णन
[डेटाबेस कनेक्शन अवलोकन](overview.md) में किया गया है। यह पृष्ठ केवल वही कवर करता है जो
Hive के लिए विशिष्ट है।

---

## 1. ODBC ड्राइवर इंस्टॉल करें {: #1-install-the-odbc-driver }

विक्रेता की आधिकारिक इंस्टॉलेशन गाइड का पालन करते हुए, **Cloudera ODBC Driver for Apache Hive** को
उस मशीन पर इंस्टॉल करें जिस पर *digna* बैकएंड चलता है।

रजिस्टर ड्राइवर का सटीक नाम अपने होस्ट से पढ़ें, जैसा कि
[digna होस्ट पर ODBC ड्राइवर इंस्टॉल करें](overview.md#install-the-driver) में बताया गया है।

---

## 2. ODBC प्रॉपर्टीज़ {: #2-odbc-properties }

!!! important "एक उदाहरण, कोई विनिर्देश नहीं"

    नीचे दिया गया सेट एक ऐसा संयोजन है जो काम करने के लिए जाना जाता है। प्रॉपर्टीज़ Cloudera Hive
    ड्राइवर की हैं, इसलिए उनके नाम, डिफ़ॉल्ट और स्वीकृत मान ड्राइवर संस्करणों और प्लेटफ़ॉर्म के बीच
    अलग होते हैं, और HiveServer2 क्या स्वीकार करता है यह पूरी तरह इस पर निर्भर करता है कि cluster को
    कैसे सुरक्षित किया गया है — प्रमाणीकरण तंत्र, transport मोड, TLS, गेटवे। इसे शुरुआती बिंदु के रूप
    में उपयोग करें और आपके द्वारा इंस्टॉल किए गए ड्राइवर संस्करण का दस्तावेज़ देखें।

**Add DB Connection** स्क्रीन में निम्नलिखित प्रॉपर्टीज़ जोड़ें:

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | *digna* होस्ट पर रजिस्टर ड्राइवर नाम से मेल खाना चाहिए |
| `HOST` | `hive.example.com` | HiveServer2 होस्ट नाम या IP पता |
| `PORT` | `10000` | HiveServer2 पोर्ट; HTTP transport के लिए `10001` |

परिणामी कनेक्शन स्ट्रिंग इस प्रकार दिखती है:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### प्रमाणीकरण

असुरक्षित HiveServer2 ऊपर की तीन प्रॉपर्टीज़ को जैसी हैं वैसी ही स्वीकार करता है। जहाँ प्रमाणीकरण
सक्षम है, वहाँ जोड़ें:

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `AuthMech` | `3` | `0` कोई प्रमाणीकरण नहीं, `2` केवल उपयोगकर्ता नाम, `3` उपयोगकर्ता नाम और पासवर्ड, `1` Kerberos |
| `UID` | `digna_source_user` | `AuthMech` `2` और `3` के लिए आवश्यक |
| `PWD` | `<password>` | `AuthMech` `3` के लिए आवश्यक। **Encrypted** पर टिक करें |

Kerberos (`AuthMech=1`) के लिए, *digna* होस्ट को अतिरिक्त रूप से एक मान्य ticket या keytab चाहिए, साथ
ही ड्राइवर द्वारा दस्तावेज़ित `KrbHostFQDN`, `KrbServiceName` और `KrbRealm` प्रॉपर्टीज़।

### Transport और TLS

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `ThriftTransport` | `2` | `0` binary (डिफ़ॉल्ट, पोर्ट 10000), `1` SASL, `2` HTTP (पोर्ट 10001, और जिसकी Knox गेटवे अपेक्षा करता है) |
| `HTTPPath` | `cliservice` | `ThriftTransport=2` के साथ |
| `SSL` | `1` | जहाँ HiveServer2 TLS से सुरक्षित है |
| `Schema` | `dignadata` | Hive डेटाबेस जिसमें session शुरू होता है। वैकल्पिक — *digna* अपनी क्वेरीज़ को qualify करता है |

---

## 3. *digna* कॉन्फ़िगरेशन {: #3-digna-configuration }

**Add DB Connection** स्क्रीन में निम्नलिखित जानकारी दें:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Hive पर टिप्पणियाँ {: #4-notes-on-hive }

- **Catalogs ड्राइवर से आते हैं।** Hive का अपना कोई catalog नहीं है, इसलिए *digna* वही लेता है जो
  ड्राइवर रिपोर्ट करता है — सामान्यतः `HIVE` नाम की एक ही प्रविष्टि — और उसके नीचे Hive डेटाबेस को
  स्कीमा के रूप में सूचीबद्ध करता है।
- **Work Schema एक Hive डेटाबेस है।** *Permanent* प्रोफ़ाइलिंग के लिए, उपयोगकर्ता को उसमें टेबल्स
  बनाने और हटाने का अधिकार चाहिए, और अंतर्निहित storage location लिखने योग्य होनी चाहिए।
- **प्रोफ़ाइलिंग मोड।** *Permanent* वर्क टेबल्स को **Work Schema** में बनाता है। *Session*
  `CREATE TEMPORARY TABLE` का उपयोग करता है, जिसके लिए अस्थायी टेबल्स का समर्थन करने वाला HiveServer2
  चाहिए, और यह **Work Schema** को नहीं छूता। *Standard* को केवल रीड एक्सेस चाहिए, और यही वह मोड है
  जिसे ऐसे cluster पर चुनना चाहिए जहाँ *digna* के पास कोई लिखने का अधिकार नहीं है।
- **प्रोफ़ाइलिंग क्वेरीज़ का एक सेट है, स्कैन नहीं।** हर सांख्यिकी HiveServer2 द्वारा गणना की जाती है,
  इसलिए जिस queue में *digna* का उपयोगकर्ता क्वेरीज़ भेजता है, उसमें इंस्पेक्शन अवधि के लिए पर्याप्त
  क्षमता होनी चाहिए।

---

## 5. ड्राइवर का सत्यापन (वैकल्पिक) {: #5-verifying-the-driver-optional }

DSN-less कनेक्शन के लिए ODBC डेटा सोर्स कॉन्फ़िगर करना आवश्यक नहीं है, लेकिन ड्राइवर का अपना डायलॉग
यह पुष्टि करने का सुविधाजनक तरीका है कि ड्राइवर, transport मोड और आपके क्रेडेंशियल्स काम करते हैं,
इससे पहले कि आप उन्हें *digna* में दर्ज करें।

#### चरण 1
![चरण 1](images/hive/create_odbc_data_source_step1.png)

यहाँ के **Host**, **Port**, **Database**, **Mechanism** और **Thrift Transport** फ़ील्ड
[अनुभाग 2](#2-odbc-properties) की `HOST`, `PORT`, `Schema`, `AuthMech` और `ThriftTransport`
प्रॉपर्टीज़ हैं।

#### चरण 2 – कनेक्शन का परीक्षण करें

पासवर्ड दें और **Test** बटन पर क्लिक करें।

![चरण 2](images/hive/create_odbc_data_source_step2.png)

सफल परीक्षण के बाद, **OK** बटन पर क्लिक करें।