# Izmaiņu žurnāls – izlaidums 2025.09  

Ar izlaidumu 2025.09 digna ievieš jaunu **modulāru arhitektūru** un palaid piecus specializētus moduļus Data Quality un Observability jomā.  
Šis izlaidums arī pastiprina autentifikāciju un uzlabo paziņojumu apstrādi visā platformā.  

---

## Jaunas funkcijas  

### Modulārais dizains  
- digna tagad seko **modulārai arhitektūrai**.  
- Klienti var iespējot tikai tos moduļus, kas nepieciešami, un pievienot vairāk, kad prasības pieaug.  
- Iepriekšējā funkcionalitāte tagad ir daļa no **digna Data Anomalies**.  

### Jaunie moduļi  
- **digna Data Anomalies** – AI darbināta anomāliju atklāšana datu apjomos, sadalījumos un trūkstošajās vērtībās.  
- **digna Data Analytics** – Novērojamības metriku laika rindas izvērtēšana, lai atklātu ilgtermiņa tendences un svārstīgumu.  
- **digna Data Timeliness** – Paredzētā datu ierašanās laika monitorings, gan AI-bāzēts, gan noteikumu bāzēts.  
- **digna Data Validation** – Noteikumu bāzētas ierakstu līmeņa pārbaudes, lai nodrošinātu atbilstību biznesa noteikumiem.  
- **digna Data Schema Tracker** – Shēmas izmaiņu (DDL modifikāciju) atklāšana monitorētajās datu bāzēs.  

### MFA via OIDC  
- Atbalsts **Multi-Factor Authentication (MFA)** izmantošanai kopā ar OIDC Single Sign-On.  
- Nodrošina uzņēmuma līmeņa drošību visām lietotāju pieslēgšanām.  

### Paziņojumu e-pasti pa moduļiem  
- Paziņojumi tagad tiek sūtīti **pa moduļiem**, kas atvieglo brīdinājumu atdalīšanu no Data Anomalies, Data Analytics un citiem moduļiem.  

---

## CLI atjauninājumi  

- **Jauna komanda: `inspect-cancel`** – Atcelt inspekcijas pēc pieprasījuma ID vai pārtraukt visus aktīvos pieprasījumus.  
- **Jauna komanda: `check-config`** – Validēt konfigurācijas failus pirms palaišanas.  
- **Jauna komanda: `remove-orphans`** – Notīrīt pamestos repozitoriju ierakstus.  
- **Uzlabota komanda `inspect`** – Jauna opcija `--bypass-backend` (`-bb`) un standartizēti atgriešanas kodi (`0 = OK, 1 = INFO, 2 = WARNING`).  


## Dokumentācija  
- Jauni ceļveži:  
  - Single Sign-On integrācijas ceļvedis