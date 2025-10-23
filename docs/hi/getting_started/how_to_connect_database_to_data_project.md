---
title: डेटाबेस कनेक्ट करें | digna दस्तावेज़ीकरण
description: digna में किसी मौजूदा प्रोजेक्ट से एक डेटाबेस कनेक्ट करने के लिए चरण-दर-चरण मार्गदर्शिका। जानें कि कनेक्शन कैसे कॉन्फ़िगर करें, क्रेडेंशियल्स कैसे प्रदान करें, और सुरक्षित एक्सेस कैसे सक्षम करें।
---

# डेटाबेस कनेक्ट करें

यह मार्गदर्शिका आपके प्रोजेक्ट में एक डेटाबेस कनेक्शन जोड़ने के लिए न्यूनतम चरण दिखाती है।

## इंटरैक्टिव डेमो

<!--ARCADE EMBED START-->
<div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;">
  <iframe
    src="https://demo.arcade.software/NhlhDLqeW9wC5zaLlYPa?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true"
    title="Connect a Database to a Project"
    frameborder="0"
    loading="lazy"
    webkitallowfullscreen
    mozallowfullscreen
    allowfullscreen
    allow="clipboard-write"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;">
  </iframe>
</div>
<!--ARCADE EMBED END-->

---

### चरण

1. **अपना प्रोजेक्ट खोलें**  
   बाएँ नेविगेशन में **Projects** पर क्लिक करें और लक्ष्य प्रोजेक्ट चुनें।

2. **कनेक्शन जोड़ें**  
   **Connections** पर जाएँ और **Add Connection** पर क्लिक करें।

3. **डेटाबेस प्रकार चुनें**  
   कनेक्ट करने के लिए वह डेटाबेस चुनें (उदा., PostgreSQL, MySQL, SQL Server, Oracle, Snowflake, Teradata)।

4. **कनेक्शन विवरण भरें**  
   प्रदान करें **Name**, **Host**, **Port**, **Database/Service**, और **Credentials** (username/password या SSO, जैसा लागू हो)।

5. **परीक्षण और सहेजें**  
   **Test** पर क्लिक करें। यदि सफल हुआ, तो **Save** पर क्लिक करें। कनेक्शन प्रोजेक्ट के लिए **Connections** के अंतर्गत दिखाई देगा।