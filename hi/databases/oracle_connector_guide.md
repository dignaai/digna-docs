# Oracle के लिए सोर्स कनेक्टर

यह गाइड बताता है कि *digna* को **DSN-less** कनेक्शन स्ट्रिंग का उपयोग करके **ODBC** के माध्यम से
Oracle Database से कनेक्ट करने के लिए कैसे कॉन्फ़िगर करें।

सेटअप का *digna* पक्ष हर तकनीक के लिए समान है — कनेक्शन कहाँ बनाए जाते हैं, प्रॉपर्टी मान कैसे
एन्क्रिप्ट होते हैं, कनेक्शन का परीक्षण कैसे होता है और प्रोफ़ाइलिंग मोड का क्या अर्थ है। इसका वर्णन
[डेटाबेस कनेक्शन अवलोकन](overview.md) में किया गया है। यह पृष्ठ केवल वही कवर करता है जो
Oracle के लिए विशिष्ट है।

---

## 1. ODBC ड्राइवर इंस्टॉल करें {: #1-install-the-odbc-driver }

Oracle ODBC ड्राइवर **Oracle Client** का हिस्सा है (Instant Client का "ODBC" पैकेज पर्याप्त है)।
विक्रेता की आधिकारिक इंस्टॉलेशन गाइड का पालन करते हुए इसे उस मशीन पर इंस्टॉल करें जिस पर *digna*
बैकएंड चलता है।

ड्राइवर **Oracle in `<OracleHomeName>`** के रूप में रजिस्टर होता है — उदाहरण के लिए
`Oracle in OraDB21Home1` या `Oracle in instantclient_21_13`। Home नाम हर इंस्टॉलेशन में अलग होता है,
इसलिए सटीक नाम अपने होस्ट से पढ़ें, जैसा कि
[digna होस्ट पर ODBC ड्राइवर इंस्टॉल करें](overview.md#install-the-driver) में बताया गया है।

---

## 2. ODBC प्रॉपर्टीज़ {: #2-odbc-properties }

!!! important "एक उदाहरण, कोई विनिर्देश नहीं"

    नीचे दिया गया सेट एक ऐसा संयोजन है जो काम करने के लिए जाना जाता है। प्रॉपर्टीज़ Oracle ODBC
    ड्राइवर की हैं, इसलिए उनके नाम, डिफ़ॉल्ट और स्वीकृत मान client संस्करणों के बीच अलग होते हैं, और
    विशेष रूप से ड्राइवर नाम आपके होस्ट पर Oracle home पर निर्भर करता है। इसे शुरुआती बिंदु के रूप में
    उपयोग करें और आपके द्वारा इंस्टॉल किए गए client संस्करण का दस्तावेज़ देखें।

**Add DB Connection** स्क्रीन में निम्नलिखित प्रॉपर्टीज़ जोड़ें:

| Key | उदाहरण मान | टिप्पणियाँ |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | *digna* होस्ट पर रजिस्टर ड्राइवर नाम से मेल खाना चाहिए |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | जिस डेटाबेस से कनेक्ट करना है — नीचे देखें |
| `UID` | `DIGNA_SOURCE_USER` | डेटाबेस उपयोगकर्ता |
| `PWD` | `<password>` | **Encrypted** पर टिक करें |

परिणामी कनेक्शन स्ट्रिंग इस प्रकार दिखती है:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### `DBQ` मान

`DBQ` तीन रूप स्वीकार करता है। *digna* के लिए ये समान हैं; अंतर इसमें है कि *digna* होस्ट पर क्या
कॉन्फ़िगर करना होता है:

| रूप | उदाहरण | आवश्यकता |
|---|---|---|
| **पूरा connect descriptor** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | कुछ नहीं — सब कुछ प्रॉपर्टी में है। अनुशंसित |
| **TNS alias** | `DIGNA_SOURCE` | alias *digna* होस्ट पर Oracle Client की `tnsnames.ora` में मौजूद होना चाहिए |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Easy Connect का समर्थन करने वाला Oracle Client (12c और बाद के) |

!!! tip "पूरे descriptor को प्राथमिकता दें"

    TNS alias कनेक्शन परिभाषा का आधा हिस्सा *digna* होस्ट पर एक फ़ाइल में ले जाता है, जहाँ होस्ट को
    फिर से बनाने या *digna* को स्थानांतरित करने पर उसे भूलना आसान है। पूरा descriptor कनेक्शन को
    आत्मनिर्भर रखता है — और DSN-less सेटअप का उद्देश्य यही है।

ध्यान दें कि descriptor में कोष्ठक कनेक्शन स्ट्रिंग के अंदर ठीक हैं, लेकिन यदि आपके पासवर्ड में `;`
है, तो उसे ब्रेसेस में रखें: `PWD={p@ss;word}`।

---

## 3. *digna* कॉन्फ़िगरेशन {: #3-digna-configuration }

**Add DB Connection** स्क्रीन में निम्नलिखित जानकारी दें:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Oracle पर टिप्पणियाँ {: #4-notes-on-oracle }

- **स्कीमा उपयोगकर्ता होते हैं।** *digna* Oracle उपयोगकर्ताओं को स्कीमा के रूप में सूचीबद्ध करता है,
  इसलिए सोर्स स्कीमा टेबल्स का owner है — ऊपर के उदाहरण में `DIGNA_SOURCE_USER`। कनेक्शन उपयोगकर्ता
  को उन टेबल्स पर `SELECT` अधिकार चाहिए, सीधे या किसी role के माध्यम से।
- **एक कनेक्शन एक डेटाबेस देखता है।** *digna* जो catalog प्रस्तुत करता है वह वही डेटाबेस है जिससे
  कनेक्शन जुड़ा है, इसलिए `DBQ` तय करता है कि कौन-सी service, और इसलिए कौन-सा डेटाबेस, प्रोफ़ाइल
  किया जाता है।
- **Quote किए जाने के बाद identifiers case-sensitive होते हैं।** *digna* data dictionary से पढ़े गए
  नामों को quote करता है, जो Oracle संग्रहीत करता है — unquoted objects के लिए बड़े अक्षर।
- **प्रोफ़ाइलिंग मोड।** *Permanent* वर्क टेबल्स को **Work Schema** में बनाता है, इसलिए उपयोगकर्ता को
  वहाँ `CREATE TABLE` अधिकार और tablespace पर quota चाहिए। *Session* एक private temporary table
  (`ORA$PTT_…`, Oracle 18c और बाद के) का उपयोग करता है और **Work Schema** को नहीं छूता। *Standard*
  को केवल रीड एक्सेस चाहिए।

---

## 5. ड्राइवर का सत्यापन (वैकल्पिक) {: #5-verifying-the-driver-optional }

DSN-less कनेक्शन के लिए ODBC डेटा सोर्स कॉन्फ़िगर करना आवश्यक नहीं है, लेकिन ड्राइवर का अपना डायलॉग
यह पुष्टि करने का सुविधाजनक तरीका है कि Oracle Client, service name और आपके क्रेडेंशियल्स काम करते
हैं, इससे पहले कि आप उन्हें *digna* में दर्ज करें।

#### चरण 1
![चरण 1](images/oracle/create_odbc_data_source_step1.png)

यहाँ प्रस्तुत **TNS Service Name** आपके Oracle Client इंस्टॉलेशन की `tnsnames.ora` से आता है —
वहीं alias, और उसके साथ होस्ट, पोर्ट और service name, परिभाषित होते हैं। *digna* में आप alias को
`DBQ` के रूप में, या इसके बजाय पूरे descriptor का उपयोग कर सकते हैं।

#### चरण 2 – कनेक्शन का परीक्षण करें

**Test Connection** बटन पर क्लिक करें।

![चरण 2](images/oracle/create_odbc_data_source_step2.png)

पासवर्ड दें और **OK** बटन पर क्लिक करें।

![चरण 3](images/oracle/create_odbc_data_source_step3.png)

सफलता संदेश पुष्टि करता है कि ड्राइवर और क्रेडेंशियल्स काम करते हैं।