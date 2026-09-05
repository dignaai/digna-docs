---
title: एक ऐसा जॉब कैसे बनाएं जो दैनिक चले
description: जानें कि डैशबोर्ड का उपयोग करके digna में दैनिक निरीक्षण जॉब को कैसे शेड्यूल करें।
keywords: digna scheduling, डेटा गुणवत्ता ऑटोमेशन, दैनिक जॉब
image: /assets/logo_square.png
---

# दैनिक जॉब कैसे शेड्यूल करें

शेड्यूलिंग आपको मैन्युअल हस्तक्षेप के बिना निरीक्षणों को स्वचालित रूप से चलाने देती है।  
इस गाइड में, आप सीखेंगे कि एक ऐसा जॉब कैसे बनाएं जो **दिन में एक बार** चले, जिससे आपका डेटा निरंतर मॉनिटर किया जा सके।

---

## Interactive Demo

प्रक्रिया को क्रियाशील रूप में देखने के लिए इंटरैक्टिव ट्यूटोरियल का पालन करें:  

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/Ra9E19A0QfMpzKqm3Yhu?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a New Data Inspection Job" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## What You Will Learn

- digna डैशबोर्ड में **Scheduling** सेक्शन तक कैसे पहुँचें  
- एक नया शेड्यूल्ड जॉब कैसे बनाएं  
- इसे **निश्चित समय पर प्रतिदिन** चलाने के लिए कैसे कॉन्फ़िगर करें  
- सही प्रोजेक्ट और datasource कैसे चुनें  
- जॉब को सक्षम कैसे करें ताकि यह स्वचालित रूप से चले  

---

## Why Daily Jobs Are Useful

प्रोडक्शन वातावरण में दैनिक शेड्यूलिंग सबसे सामान्य सेटअप है। यह सुनिश्चित करता है:  

- **Freshness** — हर दिन के डेटा का सत्यापन होता है।  
- **Consistency** — असामान्यताएँ नीचे की प्रक्रियाओं तक फैलने से पहले जल्दी पता चल जाती हैं।  
- **Automation** — निरीक्षण मैन्युअल रूप से ट्रिगर करने की आवश्यकता नहीं रहती।  

---

## Next Steps

- अधिक उन्नत कस्टम शेड्यूल के लिए [How to use crontab definition](how_to_use_crontab.md) देखें।  
- दैनिक जॉब्स को **alerting** के साथ जोड़ें ताकि असामान्यताएँ मिलने पर आपको सूचित किया जा सके।