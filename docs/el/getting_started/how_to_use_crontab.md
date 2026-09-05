---
title: Προχωρημένος Προγραμματισμός με Crontab
description: Μάθετε πώς να προγραμματίζετε μια εργασία στο digna χρησιμοποιώντας crontab expressions για προχωρημένο χρονισμό.
image: /assets/logo_square.png
---

# Προχωρημένος Προγραμματισμός με Crontab

Αυτός ο οδηγός δείχνει πώς να προγραμματίσετε εργασίες στο *digna* χρησιμοποιώντας **crontab expressions**.  
Σε αντίθεση με τα προεπιλεγμένα πρότυπα (daily, weekly, monthly), το crontab σας προσφέρει πλήρη ευελιξία για να ορίσετε προσαρμοσμένα προγράμματα.

---

## Διαδραστικό Demo

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Τι Θα Μάθετε

- Πώς να ανοίξετε την ενότητα **Scheduling** στον πίνακα ελέγχου  
- Πώς να δημιουργήσετε μια νέα εργασία χρησιμοποιώντας μια **crontab expression**  
- Πώς να ορίσετε ένα πρόγραμμα που εκτελείται μόνο τα **σαββατοκύριακα στις 10:00**  

---

## Παράδειγμα: Πρόγραμμα Σαββατοκύριακου

Για να προγραμματίσετε μια εργασία να εκτελείται κάθε **Σάββατο και Κυριακή στις 10:00 π.μ.**, χρησιμοποιήστε την ακόλουθη έκφραση:


- `0` → λεπτό (στην ώρα)  
- `10` → ώρα (10 π.μ.)  
- `*` → κάθε μέρα του μήνα  
- `*` → κάθε μήνα  
- `sat,sun` → μόνο τα Σάββατα και τις Κυριακές  

---

## Γιατί να χρησιμοποιήσετε το Crontab;

- Δημιουργήστε προγράμματα πέρα από τα τυπικά πρότυπα daily, weekly, ή monthly  
- Ορίστε ακριβείς χρόνους εκτέλεσης (συγκεκριμένες μέρες, ώρες ή διαστήματα)  
- Χρήσιμο για εργασίες το σαββατοκύριακο, ελέγχους εκτός ωραρίου ή συχνή παρακολούθηση  

---