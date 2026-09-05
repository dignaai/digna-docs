# Crontab के साथ उन्नत शेड्यूलिंग

यह गाइड दिखाती है कि *digna* में **crontab expressions** का उपयोग करके जॉब्स को कैसे शेड्यूल किया जाए।  
मानक पैटर्न (daily, weekly, monthly) की तुलना में, crontab आपको कस्टम शेड्यूल पर पूरी लचीलापन देता है।

---

## इंटरएक्टिव डेमो

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## आप क्या सीखेंगे

- डैशबोर्ड में **Scheduling** सेक्शन कैसे खोलें  
- एक नया जॉब **crontab expression** का उपयोग करके कैसे बनाएं  
- ऐसा शेड्यूल कैसे सेट करें जो केवल **वीकेंड पर सुबह 10:00** चले  

---

## उदाहरण: वीकेंड शेड्यूल

किसी जॉब को हर **शनिवार और रविवार सुबह 10:00 बजे** चलाने के लिए निम्नलिखित अभिव्यक्ति का उपयोग करें:


- `0` → मिनट (घंटे पर)  
- `10` → घंटा (सुबह 10 बजे)  
- `*` → महीने के हर दिन पर  
- `*` → हर महीने में  
- `sat,sun` → केवल शनिवार और रविवार को  

---

## Crontab का उपयोग क्यों करें?

- मानक daily, weekly, या monthly पैटर्न से परे शेड्यूल बनाएं  
- सटीक रन टाइम परिभाषित करें (विशेष दिन, घंटे, या अंतराल)  
- वीकेंड जॉब्स, ऑफ‑आवर्स चेक, या बार‑बार निगरानी के लिए उपयोगी  

---